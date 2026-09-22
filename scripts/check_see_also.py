#!/usr/bin/env python3
"""See Also hygiene — per-stack bare ceiling + the always-wrong label echo.

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
event loop -> Node is libuv phases). This gate makes two properties standing:

  1. bare ceiling per top-level stack (see-also-baseline.json) — a stack's
     bare count may fall freely; rising above its committed maximum fails the
     build, so a new stack or file cannot regress the surface silently.
  2. label echo (always a defect, no baseline) — a reason whose content words
     add nothing beyond the link label is the declined boilerplate in
     miniature ("[Closures](closures.md) — closures"); the per-pair judgment
     must connect source to target, not restate the label.

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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'see-also-baseline.json')
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'api', '_site', '__pycache__',
             '.jekyll-cache', 'scripts'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')

FENCE_OPEN = re.compile(r'^```(\w[\w+-]*)\s*$')
FENCE_CLOSE = re.compile(r'^```\s*$')
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
    entries, in_fence, in_sa = [], False, False
    for i, raw in enumerate(lines, 1):
        if in_fence:
            if FENCE_CLOSE.match(raw):
                in_fence = False
            continue
        m = FENCE_OPEN.match(raw)
        if m:
            in_fence = True
            continue
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
    for path in corpus_files():
        stack = path.split('/')[0] if '/' in path else '(root)'
        for line, label, target, reason in see_also_entries(path):
            if not reason:
                bare[stack] = bare.get(stack, 0) + 1
            elif content_words(reason) <= content_words(label):
                echo.append((path, line, label, reason))
    return bare, echo


def main(argv):
    if '--baseline' in argv:
        bare, echo = measure()
        if echo:
            for path, line, label, reason in echo:
                print(f"ECHO {path}:{line}: [{label}] — {reason}")
            print("refusing to baseline with echo defects present — fix them first")
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

    bare, echo = measure()
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

    print(f"see-also: {total} bare across {len(bare)} stacks, "
          f"{len(echo)} echo defects")
    if problems:
        print("FAIL:")
        for p in problems:
            print(p)
        return 1
    print("OK: within ceilings, no label echoes")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
