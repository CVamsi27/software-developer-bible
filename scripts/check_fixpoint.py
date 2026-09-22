#!/usr/bin/env python3
"""Fixed-point gate: the corpus must be a no-op for every writer.

A repair tool is only safe if running it on a clean tree changes NOTHING. If it
changes something, then either the corpus was stale (a gate is missing) or —
the case this gate exists for — the writer's scope is wider than the checker's,
so it edits files the suite calls clean and **nothing can ever flag the edit**.
That is an invisible edit: the one failure mode a self-auditing suite cannot
detect from inside.

The 2026-09-21 probe found two of them by hand, both real:

  * `fix_code_whitespace.py --trailing-ws` stripped trailing whitespace in
    *layout* fences (`text`, `csv`, `tsv`, `anki`, `diff`, `mermaid`) while
    `check_code_whitespace.py` deliberately exempts them ("any layout IS
    content" — and in a csv/anki fence a trailing tab is an empty FIELD). It
    was quietly rewriting one file of the live corpus: a box diagram's padding.
  * `fix_fence_labels.py` proposed relabeling four mixed cheat-sheet fences
    (`text` → `typescript`) — fences holding a title bar, code snippets and
    tips prose. Applying that would have rendered the title and tips as broken
    TypeScript. Nothing invokes this script, so it was a loaded but un-fired
    gun aimed at the corpus.

So this gate copies the corpus to a temp tree, runs every writer with its
writing flags there, and fails if any file differs. Writers are listed with the
exact flags the repo documents; adding a writer is one line.

Scope note: only the *repair/restamp* family (the tools whose documented
contract is "a clean corpus needs no change") is listed. One-shot authoring
tools (insert_section, fix_section_order, link_topic_twins, fix_depth) are not
idempotent by contract and are deliberately excluded.

Usage:  python3 scripts/check_fixpoint.py      # exit 1 if any writer edits the corpus
"""
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile

from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY_SKIP = {'.git', 'node_modules', '.archive', '__pycache__'}

# (script, args) — the exact invocations the repo documents for repair.
WRITERS = [
    ('check_alignment.py', ['--fix']),
    ('read_time.py', ['--write']),
    ('gen_master_index.py', []),
    ('check_counts.py', ['--write']),
    ('fix_nav_labels.py', ['--fix']),
    ('fix_box_width.py', ['--fix']),
    ('fix_box_code_indent.py', ['--fix']),
    ('fix_code_whitespace.py', ['--trailing-ws', '--paste-shift']),
    ('fix_fence_labels.py', ['--apply']),
    ('prose_hygiene.py', ['--write']),
]


def copy_corpus(dest):
    shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(*COPY_SKIP),
                    dirs_exist_ok=True)


def diff_tree(orig, copy, sub=''):
    """Relative paths of files whose bytes differ between the two trees."""
    changed = []
    base = os.path.join(orig, sub) if sub else orig
    other = os.path.join(copy, sub) if sub else copy
    for name in sorted(os.listdir(base)):
        if name in COPY_SKIP:
            continue
        a, b = os.path.join(base, name), os.path.join(other, name)
        rel = os.path.join(sub, name) if sub else name
        if os.path.isdir(a):
            if not os.path.isdir(b):
                changed.append(rel + '/ (missing in copy)')
                continue
            changed.extend(diff_tree(orig, copy, rel))
        elif not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
            changed.append(rel)
    return changed


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, 'corpus')
        copy_corpus(work)
        # The gate's own scope floor (see scan_scope): an empty copy is a
        # fixed point of everything, so "no writer changed a byte" over zero
        # files would certify nothing. This gate is not immune to the class
        # it exists to catch.
        n_md = sum(1 for _, _, fs in os.walk(work) for f in fs if f.endswith('.md'))
        guard(n_md, 'markdown files in the corpus copy', work)
        for script, args in WRITERS:
            subprocess.run([sys.executable, os.path.join('scripts', script), *args],
                           cwd=work, capture_output=True, text=True)
        changed = diff_tree(ROOT, work)

    if changed:
        print(f"FIXED POINT FAIL — {len(changed)} file(s) change when the "
              f"writers run on a tree this suite calls clean:\n")
        for rel in changed[:40]:
            print(f"  {rel}")
        if len(changed) > 40:
            print(f"  … and {len(changed) - 40} more")
        print("\n  Either a gate is missing for that content, or a writer's scope "
              "is wider than its checker's — an edit nothing can flag. Fix the "
              "scope so check and fix agree, then re-run.")
        return 1
    print(f"fixed point OK — {len(WRITERS)} writers run over a corpus copy "
          f"leave every file byte-identical (check and fix agree on scope)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
