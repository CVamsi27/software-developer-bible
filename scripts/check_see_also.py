#!/usr/bin/env python3
"""See Also hygiene — bare ceilings, label echoes and unfinished descriptions.

The 2026-09-22 measurement found 1958 of 2727 See Also entries (72%) bare and
deliberately DECLINED a bulk derivation: of 1888 entries a title-derivation
could reach, 1874 collapsed into four boilerplate templates — the bare link
with extra words. The recorded plan (gate-design-principles.md, health-report
non-actions) was: reasons may be *assisted* (derivation proposes, human
disposes), *hygiene-checked* (this gate), and improved *progressively*,
stack by stack.

2026-09-23: the pilot executed that plan. 10-frontend/10.1-javascript's 92
bare entries now carry hand-authored per-pair reasons — including the stamped
footer triple (Coding Patterns / Node.js / TypeScript), where the connecting
mechanism genuinely differs per chapter (`this` -> TS is `ThisType<T>`; the
event loop -> Node is libuv phases). This gate makes three properties standing:

  1. bare ceiling per top-level stack (see-also-baseline.json) — a stack's
     bare count may fall freely; rising above its committed maximum fails the
     build, so a new stack or file cannot regress the surface silently.
  2. label echo (always a defect, no baseline) — a reason whose content words
     add nothing beyond the link label is the declined boilerplate in
     miniature ("[Closures](closures.md) — closures"); the per-pair judgment
     must connect source to target, not restate the label.

  3. unfinished descriptions (always defects, no baseline) — clipped endings
     and copied heading/table fragments do not explain why to follow a link.

Check-only by design: authoring or fixing a reason is editorial. `--baseline`
re-commits the per-stack maxima deliberately. Scope: content markdown,
personal/ excluded, fences masked (an example inside a fence is not a link).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_scope import guard
from md_fences import walk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'see-also-baseline.json')
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'api', '_site', '.archive', '__pycache__',
             '.jekyll-cache', 'scripts'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')

ENTRY = re.compile(r'^[-*] \[([^\]]+)\]\(([^)\s]+)\)(?:\s+—\s+(.*))?$')
STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'for', 'vs',
        'versus', 'with', 'on', 'is', 'are'}


def corpus_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for n in filenames:
            if not n.endswith('.md'):
                continue
            p = os.path.join(rel, n) if rel != '.' else n
            if EXCLUDE_PATH.search(p):
                continue
            out.append(os.path.normpath(p))
    return sorted(out)


def see_also_entries(path):
    """(line_no_1indexed, label, target, reason_or_None) inside See Also."""
    try:
        lines = open(os.path.join(ROOT, path), encoding='utf-8').read().split('\n')
    except OSError:
        return []
    entries, in_sa = [], False
    for index, raw, in_fence, is_fence in walk(lines):
        if is_fence or in_fence:
            continue
        i = index + 1
        if raw.startswith('#'):
            in_sa = raw.lstrip('#').strip().lower().startswith('see also')
            continue
        if not in_sa:
            continue
        m = ENTRY.match(raw.strip())
        if m:
            entries.append((i, m.group(1), m.group(2), m.group(3)))
    return entries


def content_words(text):
    return {w for w in re.findall(r"[a-z0-9][a-z0-9'.-]*", text.lower())
            if w not in STOP}


def measure():
    bare = {}
    echo = []
    unfinished = []
    for path in corpus_files():
        stack = path.split('/')[0] if '/' in path else '(root)'
        for line, label, target, reason in see_also_entries(path):
            if not reason:
                bare[stack] = bare.get(stack, 0) + 1
            elif re.search(r'(?:…|\.\.\.)\s*$', reason):
                unfinished.append((path, line, 'clipped description'))
            elif re.match(r'^\s*(?:#{1,6}\s|\|)', reason):
                unfinished.append((path, line, 'markup fragment'))
            elif content_words(reason) <= content_words(label):
                echo.append((path, line, label, reason))
    return bare, echo, unfinished


def main(argv):
    if '--baseline' in argv:
        bare, echo, unfinished = measure()
        if echo or unfinished:
            for path, line, label, reason in echo:
                print(f"ECHO {path}:{line}: [{label}] — {reason}")
            for path, line, defect in unfinished:
                print(f"UNFINISHED {path}:{line}: {defect}")
            print("refusing to baseline with description defects present — fix them first")
            return 1
        data = {'stacks': dict(sorted(bare.items()))}
        with open(BASELINE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write('\n')
        print(f"baseline committed: {sum(bare.values())} bare across "
              f"{len(bare)} stacks")
        return 0

    try:
        with open(BASELINE, encoding='utf-8') as f:
            ceilings = json.load(f)['stacks']
    except (OSError, KeyError, ValueError):
        print(f"cannot read baseline {BASELINE} — run with --baseline")
        return 1

    bare, echo, unfinished = measure()
    files = corpus_files()
    guard(len(files), 'markdown files')
    total = sum(bare.values())
    problems = []
    for stack in sorted(set(bare) | set(ceilings)):
        have = bare.get(stack, 0)
        max_ = ceilings.get(stack, 0)
        if have > max_:
            problems.append(
                f"  {stack}: {have} bare entries > ceiling {max_} — author "
                f"reasons for the new entries (or re-baseline deliberately: "
                f"python3 scripts/check_see_also.py --baseline)")
    for path, line, label, reason in echo:
        problems.append(f"  {path}:{line}: [{label}] — {reason}"
                        f"  (echoes the label; adds no information)")

    for path, line, defect in unfinished:
        problems.append(f"  {path}:{line}: {defect} — author a complete reading reason")

    print(f"see-also: {total} bare across {len(bare)} stacks, "
          f"{len(echo)} echo defects, {len(unfinished)} unfinished descriptions")
    if problems:
        print("FAIL:")
        for p in problems:
            print(p)
        return 1
    print("OK: within ceilings, no label echoes or unfinished descriptions")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
