#!/usr/bin/env python3
"""Fence-aware broken-link checker for software-developer-bible.

Scans every source .md file (skipping generated output, vendored dependencies,
and .git) and verifies
that each *prose* markdown link resolves to a real file or directory inside
the repo, and that every in-page anchor (`#fragment`) resolves to a real
heading slug in its target file. This scripts the footer claims
("0 broken links") that previously were asserted by hand.

Fence-aware means links inside code fences (``` / ~~~), inline {% raw %}
examples, and HTML comments are ignored. A whole-document raw wrapper
protects Liquid interpolation, not Markdown; its navigation/headings are real.
External links (http/https/mailto/tel), anchor-only links, and relative targets that
escape the repo root are reported as skipped, never as broken.

It also checks *display text*: a link whose visible label is a relative path
(`../../2-Backend-Stack/12-Microservices/03-Saga-Pattern.md`) must point at a
path that exists. Those are pre-renumbering relics — the target resolves, so a
target-only checker never sees them, but the reader is shown archaeology from
a folder layout that no longer exists. A humanized label that happens to
contain `../` (the generated `← Previous: ../02 Io And Data/index` footers)
has a space and a capital, so it is not treated as a path.

Heading slugs follow GitHub-style slugging: lowercase, strip punctuation
(dropping characters like `.` and `+`), each whitespace run becomes a
hyphen, and duplicate headings within a file get -1, -2 suffixes.

Usage:
  python3 scripts/check_links.py          # report + exit 1 on any broken link
"""
import os
import re
import sys
import urllib.parse
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', 'vendor', '.archive', '_site'}

# Protocols / target forms that cannot or should not be resolved to a file.
EXTERNAL_PREFIXES = (
    'http://', 'https://', 'mailto:', 'tel:', 'ftp://', 'data:',
    '//', 'javascript:', '<',
)

# Post-mortem reports quote dead paths as *documentation* of a past defect,
# so their visible text is deliberately unresolvable. Nothing else is exempt.
STALE_TEXT_EXEMPT = ('80-lanes-abroad-full-stack/personal/',)

LINK_RE = re.compile(r'\[([^\]\n]*)\]\(([^)\n]+)\)')
# A fence opener may carry an info string (```js); a closer must be an
# otherwise-empty line of at least as many of the same marker chars.
FENCE_OPEN_RE = re.compile(r'^( {0,3})(`{3,}|~{3,})')
FENCE_CLOSE_RE = re.compile(r'^ {0,3}(`{3,}|~{3,})\s*$')
RAW_START_RE = re.compile(r'^\s*\{\%\s*raw')
RAW_END_RE = re.compile(r'\{\%\s*endraw')
HTML_COMMENT_START = re.compile(r'<!--')
HTML_COMMENT_END = re.compile(r'-->')
HEADING_RE = re.compile(r'^ {0,3}#{1,6}[ \t]+(.+)$')


def gh_slug(text):
    """GitHub-style heading slug (mirrors github-slugger).

    Lowercase, drop every character that is not a word char, whitespace, or
    hyphen (this removes `.`, `+`, `()`, `:`, em dashes, quotes, ...), then
    replace EACH whitespace char with a hyphen (no run collapsing — an em
    dash surrounded by spaces therefore yields `--`, exactly like GitHub),
    and trim edge hyphens.
    """
    s = re.sub(r'[^\w\s-]', '', text.lower())
    s = re.sub(r'\s', '-', s)
    return s.strip('-')


def state_lines(lines):
    """Yield ('heading', lineno, text) / ('prose', lineno, line) for every
    line that is real document content (outside fences, raw blocks, and HTML
    comments). Whole-chapter Liquid wrappers are real Markdown, not samples.
    """
    nonblank = [i for i, line in enumerate(lines) if line.strip()]
    whole_raw = (
        len(nonblank) >= 3
        and lines[nonblank[0]].strip() == '{% raw %}'
        and lines[nonblank[-1]].strip() == '{% endraw %}'
        and any(re.match(r'^# [^#]', line) for line in lines)
    )
    wrapper_edges = {nonblank[0], nonblank[-1]} if whole_raw else set()
    fence_char = None
    fence_len = 0
    in_raw = False
    in_comment = False
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if lineno - 1 in wrapper_edges:
            continue

        if in_comment:
            if HTML_COMMENT_END.search(stripped):
                in_comment = False
            continue
        if not in_comment and HTML_COMMENT_START.search(stripped) \
                and not HTML_COMMENT_END.search(stripped):
            in_comment = True
            continue
        if HTML_COMMENT_START.search(stripped) \
                and HTML_COMMENT_END.search(stripped):
            continue  # single-line comment

        if in_raw:
            if RAW_END_RE.search(stripped):
                in_raw = False
            continue
        if RAW_START_RE.search(stripped):
            in_raw = True
            continue

        if fence_char:
            close = FENCE_CLOSE_RE.match(line)
            if close and close.group(1)[0] == fence_char \
                    and len(close.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        opener = FENCE_OPEN_RE.match(line)
        if opener:
            fence_char = opener.group(2)[0]
            fence_len = len(opener.group(2))
            continue

        heading = HEADING_RE.match(line)
        if heading:
            yield ('heading', lineno, heading.group(1))
            continue
        yield ('prose', lineno, line)


def heading_slugs(path):
    """All GitHub-style slugs for headings in one file (duplicates get -N)."""
    slugs = set()
    counts = {}
    try:
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return slugs
    for kind, _lineno, text in state_lines(lines):
        if kind != 'heading':
            continue
        base = gh_slug(text)
        if not base:
            continue
        n = counts.get(base, 0)
        counts[base] = n + 1
        slugs.add(base if n == 0 else f'{base}-{n}')
    return slugs


def is_external(target):
    return target.startswith(EXTERNAL_PREFIXES) or os.path.isabs(target)


# Inline code spans may name a repo file (`path/to/file.md`), and a stale one
# sends the reader to a file that isn't there — the 2026-09-21 sweep found 53
# such relics in the two lane study docs, from three generations of
# renumbering: the `software-developer-bible/16-Testing/01-Overview.md`
# layout, then `30.2-system-design/13-Rate-Limiter.md` before the case studies
# moved under `02-case-studies/`. No markdown link checker can see them: they
# are not links.
#
# Judging *which* spans are repo paths took two calibration rounds. A span is
# judged only when it claims to be one:
#   * it ends in `.md` — a file reference is a path by intent; or
#   * its first segment is a real top-level stack folder; or
#   * its first segment is legacy stack shape (`16-Testing`, `0-Interview-Strategy`).
# That keeps plan/design docs' fragments (`01-auth/`, `02-creational/`,
# `40-frontend-tooling`) and bare names (`check_template.py`, `santifer/career-ops`)
# out, since a first calibration pass fired on 123 such fragments — a design
# document listing the folder tree it intends to create is not a broken link.
# docs/ is exempt wholesale: changelogs and specs are historical records that
# must keep quoting the paths of their time.
INLINE_CODE_SPAN = re.compile(r'`([^`\n]+)`')
LEGACY_STACK = re.compile(r'^\d{1,2}-[A-Z]')
NUMERIC_RANGE = re.compile(r'^\d[\d.-]*$')
INLINE_PATH_EXEMPT = ('docs/', '80-lanes-abroad-full-stack/personal/')


# Only the numbered *study stacks* are this repo's own structure. A third
# calibration round taught this: chapter prose legitimately names paths inside
# the reader's hypothetical project (`scripts/checks/check-prisma-boundary.mjs`,
# `docs/runbooks/`, `.github/workflows/deploy.yml`) — those are illustrations of
# a layout to build, and judging them fired on 92 spans.
STACK_HEAD = re.compile(
    r'^(?:0\d|10|20|30|40|50|60|70|80|81)-')
LEGACY_REPO = 'software-developer-bible/'


def is_repo_path_token(token):
    """Does this prose code span claim to be a path inside this repo?"""
    if not token or ' ' in token or NUMERIC_RANGE.match(token):
        return False
    # Format illustrations cannot be paths: a W3C traceparent
    # (`00-<trace-id>-<parent-span-id>-<flags>`) matched the stack-head shape
    # until placeholders and globs were excluded.
    if re.search(r'[<>{}*]', token):
        return False
    if token.startswith(LEGACY_REPO):
        # A bare `software-developer-bible/` names the external tool's layout
        # (its own repo), not a path into this one.
        return len(token) > len(LEGACY_REPO)
    head = token.split('/')[0]
    return bool(STACK_HEAD.match(head)) or bool(LEGACY_STACK.match(head))


def main():
    broken = []
    stale_text = []
    stale_paths = []
    total = 0
    anchors_ok = 0
    anchors_broken = 0
    skipped = 0

    # Pass 1 — heading-slug map for every file (anchor targets).
    slugs_map = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            slugs_map[rel] = heading_slugs(path)

    # A link gate that finds no files certifies nothing (see scan_scope):
    # "OK — 0 links checked" is what a broken root would print forever.
    guard(len(slugs_map), 'markdown files', ROOT)

    # Pass 2 — link + anchor checks.
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            try:
                with open(path, encoding='utf-8') as fh:
                    lines = fh.read().splitlines()
            except (OSError, UnicodeDecodeError) as exc:
                broken.append(f'{rel}: unreadable ({exc})')
                continue

            for _kind, lineno, raw_line in state_lines(lines):
                # Strip inline code spans so `[x](y)` examples don't count.
                line = re.sub(r'`[^`\n]*`', '', raw_line)

                # Inline code spans can name a repo file too (`path/to.md`),
                # and a stale one sends the reader to a file that isn't there —
                # the 2026-09-21 sweep found 53 such relics in the two lane
                # study docs, from three generations of renumbering (the
                # `software-developer-bible/16-Testing/01-Overview.md` layout,
                # then `30.2-system-design/13-Rate-Limiter.md`). A markdown
                # link checker can never see them: they are not links. Only
                # unambiguous repo paths are judged — a token must start with a
                # `NN-` stack prefix or the legacy repo name. Bare file names
                # (`check_template.py`), GitHub slugs (`santifer/career-ops`),
                # template patterns (`NN.N-slug/`) and numeric ranges
                # (`35-44`) are left alone.
                if not rel.startswith(INLINE_PATH_EXEMPT):
                    for cm in INLINE_CODE_SPAN.finditer(raw_line):
                        token = cm.group(1).strip()
                        if not is_repo_path_token(token):
                            continue
                        cands = (os.path.join(ROOT, token),
                                 os.path.join(os.path.dirname(path), token))
                        if not any(os.path.exists(c) for c in cands):
                            stale_paths.append(
                                f'{rel}:{lineno}: inline path "{token}" does '
                                f'not exist in the repo')

                for m in LINK_RE.finditer(line):
                    label = m.group(1).strip()
                    # A relative path as *visible text* must resolve. Spaced
                    # labels are humanized titles (the nav-footer convention),
                    # not paths, so they are not judged as one.
                    if not rel.startswith(STALE_TEXT_EXEMPT) \
                            and label.startswith(('../', './')) \
                            and ' ' not in label:
                        as_path = os.path.normpath(
                            os.path.join(os.path.dirname(path), label))
                        if not os.path.exists(as_path):
                            stale_text.append(f'{rel}:{lineno}: link text '
                                              f'"{label}" is a path that no '
                                              f'longer exists')
                    raw_target = m.group(2).strip()
                    # Optional markdown title after whitespace, angle brackets.
                    target = raw_target.split()[0].strip('\'"') \
                        if raw_target.split() else ''
                    if target.startswith('<'):
                        target = target[1:]
                        target = target.split('>')[0]
                    target = target.strip()

                    if not target or is_external(target):
                        skipped += 1
                        continue

                    head, sep, frag = target.partition('#')
                    if sep and not head and not frag:
                        skipped += 1  # dangling '#'
                        continue

                    # If only a fragment (no path), the target is this file.
                    if head:
                        head_unq = urllib.parse.unquote(head)
                        base = head_unq.split('?', 1)[0]
                        resolved = os.path.normpath(
                            os.path.join(os.path.dirname(path), base))
                        if not (resolved == ROOT
                                or resolved.startswith(ROOT + os.sep)):
                            # Escapes the repo root -> external, can't verify.
                            skipped += 1
                            continue
                        if not os.path.exists(resolved):
                            broken.append(f'{rel}:{lineno}: {target} -> '
                                          f'{os.path.relpath(resolved, ROOT)}')
                            continue
                        target_rel = os.path.relpath(resolved, ROOT)
                    else:
                        target_rel = rel

                    total += 1
                    if not frag:
                        continue  # file link only, already verified

                    frag_unq = urllib.parse.unquote(frag).strip()
                    slugs = slugs_map.get(target_rel, set())
                    if frag_unq.lower() in slugs \
                            or gh_slug(frag_unq) in slugs:
                        anchors_ok += 1
                    else:
                        anchors_broken += 1
                        broken.append(
                            f'{rel}:{lineno}: anchor #{frag_unq} has no '
                            f'matching heading in {target_rel}')

    if stale_paths:
        print(f'STALE INLINE PATHS ({len(stale_paths)}) — a prose code span '
              f'names a file that does not exist:')
        for s in stale_paths:
            print(f'  {s}')
        print("  fix: point the reference at the current path (renumbering "
              "moved it) or delete it.\n")
    if stale_text:
        print(f'STALE LINK TEXT ({len(stale_text)}) — visible label is a path '
              f'that no longer exists:')
        for s in stale_text:
            print(f'  {s}')
        print("  fix: rewrite the label as the human title of the target"
              " (a reader should never see a folder path).\n")
    if stale_paths:
        sys.exit(1)
    if broken:
        print(f'BROKEN LINKS ({len(broken)}):')
        for b in broken:
            print(f'  {b}')
        print(f'\n{total} links checked ({anchors_ok} anchors OK), '
              f'{len(broken)} broken ({skipped} external links skipped).')
        sys.exit(1)
    if stale_text:
        sys.exit(1)
    print(f'OK — {total} links checked ({anchors_ok} anchors verified), '
          f'0 broken, 0 stale labels, 0 stale inline paths '
          f'({skipped} external links skipped).')


if __name__ == '__main__':
    main()
