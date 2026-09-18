#!/usr/bin/env python3
"""Fence-aware broken-link checker for software-developer-bible.

Scans every .md file (skipping .git / node_modules / .archive) and verifies
that each *prose* markdown link resolves to a real file or directory inside
the repo, and that every in-page anchor (`#fragment`) resolves to a real
heading slug in its target file. This scripts the footer claims
("0 broken links") that previously were asserted by hand.

Fence-aware means links inside code fences (``` / ~~~), {% raw %} blocks,
and HTML comments are ignored — they are examples, not navigation. External
links (http/https/mailto/tel), anchor-only links, and relative targets that
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive'}

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
    comments)."""
    fence_char = None
    fence_len = 0
    in_raw = False
    in_comment = False
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

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


def main():
    broken = []
    stale_text = []
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

            for _kind, lineno, line in state_lines(lines):
                # Strip inline code spans so `[x](y)` examples don't count.
                line = re.sub(r'`[^`\n]*`', '', line)

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

    if stale_text:
        print(f'STALE LINK TEXT ({len(stale_text)}) — visible label is a path '
              f'that no longer exists:')
        for s in stale_text:
            print(f'  {s}')
        print("  fix: rewrite the label as the human title of the target"
              " (a reader should never see a folder path).\n")
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
          f'0 broken, 0 stale labels ({skipped} external links skipped).')


if __name__ == '__main__':
    main()
