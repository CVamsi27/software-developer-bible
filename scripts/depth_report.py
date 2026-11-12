#!/usr/bin/env python3
"""depth_report.py — where the corpus is thin, as an inventory, never a gate.

The cover pass needs to know which chapters are candidates for a depth rewrite,
and a word-count *gate* would answer that question dishonestly: the cheapest way
to satisfy a floor is padding, which is the exact failure the reading pass is
trying to remove. So this script reports and exits 0. The rubric
(docs/2026-11-quality-rubric.md) says a chapter is deep when it moves from a
concrete problem to a mechanism to an observable result to the boundary where
the mechanism stops working; only a reader can judge that, and this report's job
is to tell the reader where to look first.

Signals reported per file, and why each one is worth a look:

  prose words      < 700 means the chapter may be naming a mechanism without
                   showing it; measured, not judged.
  code fences      0 in a learning chapter means no executable claim at all.
  sections         how many `##` mechanisms the chapter actually argues.
  Definition       the gate-19 floor already requires 25 prose words; a short
                   Definition is reported separately because it is the chapter's
                   one-sentence promise.

Usage:
  python3 scripts/depth_report.py              # summary + the thin list
  python3 scripts/depth_report.py --json       # machine-readable
  python3 scripts/depth_report.py --limit=40   # cap the printed rows
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
import prose_scan
from prose_hygiene import EXCLUDE_PATH, ROOT, SKIP_DIRS

# A learning chapter is a numbered file under a stack directory. INDEX files,
# interview banks, cheat sheets and revision companions answer a different
# question (navigation, recall, reference) and are excluded from the thin list.
LEARNING = re.compile(r'^(?:[0-9]{2}-|projects/|lanes/)')
NON_CHAPTER = re.compile(r'(INDEX\.md|REVISION\.md|interview|cheat|quick-reference)',
                         re.I)
SECTION = re.compile(r'^##\s+(?!#)')
DEFINITION = re.compile(r'^##\s+Definition\s*$')


def section_of(rel):
    """The study area a path belongs to, for the per-section summary."""
    head = rel.split('/')[0] if '/' in rel else '(root)'
    return head


def measure(path):
    with open(path, encoding='utf-8', errors='replace') as handle:
        text = handle.read()
    lines = text.split('\n')
    fences = 0
    code_lines = 0
    for _i, line, in_fence, is_fence_line in md_fences.walk(lines):
        if is_fence_line:
            fences += 1
            continue
        if in_fence:
            code_lines += 1
    sections = [line for _i, line, in_fence, is_fence in md_fences.walk(lines)
                if not in_fence and not is_fence and SECTION.match(line)]
    definition_words = 0
    in_definition = False
    for _i, line, in_fence, is_fence in md_fences.walk(lines):
        if in_fence or is_fence:
            continue
        if DEFINITION.match(line):
            in_definition = True
            continue
        if in_definition and SECTION.match(line):
            in_definition = False
        elif in_definition:
            definition_words += len(line.split())
    return {
        'prose_words': prose_scan.prose_words(lines),
        'code_lines': code_lines,
        'fences': fences // 2 if fences else 0,
        'sections': len(sections),
        'definition_words': definition_words,
        'revision': os.path.exists(os.path.join(os.path.dirname(path), 'REVISION.md')),
    }


def walk():
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith('.'))
        for name in sorted(names):
            if not name.endswith('.md'):
                continue
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT)
            if EXCLUDE_PATH.search(rel):
                continue
            yield rel, path


def collect():
    rows = []
    for rel, path in walk():
        stats = measure(path)
        stats['path'] = rel
        stats['chapter'] = bool(LEARNING.match(rel) and not NON_CHAPTER.search(rel))
        rows.append(stats)
    if not rows:
        print("SCOPE ERROR: no markdown files found — check ROOT")
        sys.exit(1)
    return rows


def summarise(rows):
    sections = {}
    for row in rows:
        key = section_of(row['path'])
        bucket = sections.setdefault(key, {'files': 0, 'prose_words': 0,
                                          'no_code': 0, 'thin': 0})
        bucket['files'] += 1
        bucket['prose_words'] += row['prose_words']
        if row['chapter']:
            if row['fences'] == 0:
                bucket['no_code'] += 1
            if row['prose_words'] < 700:
                bucket['thin'] += 1
    return sections


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--json', action='store_true', help='machine-readable output')
    parser.add_argument('--limit', type=int, default=25,
                        help='rows to print per list (default 25, 0 = all)')
    args = parser.parse_args()

    rows = collect()
    chapters = [r for r in rows if r['chapter']]
    thin = sorted((r for r in chapters if r['prose_words'] < 700),
                  key=lambda r: r['prose_words'])
    no_code = sorted((r for r in chapters if r['fences'] == 0),
                     key=lambda r: r['prose_words'])
    short_def = sorted((r for r in chapters if r['definition_words'] < 25),
                       key=lambda r: r['definition_words'])
    sections = summarise(rows)

    if args.json:
        print(json.dumps({
            'files': len(rows),
            'chapters': len(chapters),
            'sections': sections,
            'thin': [{'path': r['path'], 'prose_words': r['prose_words']} for r in thin],
            'no_code': [{'path': r['path'], 'prose_words': r['prose_words']} for r in no_code],
            'short_definition': [{'path': r['path'],
                                  'definition_words': r['definition_words']}
                                 for r in short_def],
        }, indent=2, sort_keys=True))
        return

    total_words = sum(r['prose_words'] for r in rows)
    print(f"{len(rows)} markdown files, {len(chapters)} learning chapters, "
          f"{total_words:,} prose words\n")
    print(f"{'section':44s} {'files':>6s} {'words':>9s} {'no-code':>8s} {'<700w':>6s}")
    for key in sorted(sections):
        bucket = sections[key]
        print(f"{key:44s} {bucket['files']:6d} {bucket['prose_words']:9,d} "
              f"{bucket['no_code']:8d} {bucket['thin']:6d}")

    def show(title, items, fmt):
        print(f"\n{title}: {len(items)}")
        shown = items if args.limit == 0 else items[:args.limit]
        for row in shown:
            print("  " + fmt(row))
        if len(items) > len(shown):
            print(f"  … {len(items) - len(shown)} more (--limit=0 for all)")

    show("learning chapters under 700 prose words", thin,
         lambda r: f"{r['prose_words']:4d}w  {r['path']}")
    show("learning chapters with no code fence", no_code,
         lambda r: f"{r['prose_words']:4d}w  {r['path']}")
    show("learning chapters with a Definition under 25 words", short_def,
         lambda r: f"{r['definition_words']:3d}w  {r['path']}")
    print("\nInventory only — no threshold here is a gate, and none of these "
          "numbers says a chapter is shallow.")


if __name__ == '__main__':
    main()
