#!/usr/bin/env python3
"""Backfill the file-metadata block required by contributing.md.

contributing.md: "Every content file must begin with metadata in two forms"
(HTML comment + shields badges). 77 files predate the rule and no gate
enforced it, so they slipped through. This completes each header:

  1. partial block (comment present, a badge missing)  -> add the badge(s)
  2. fully headerless                                  -> comment + 3 badges
Values come from a metadata-carrying sibling in the same directory; wholly
headerless directories fall back to the STACK_MAP below. Tags derive from
the filename (interview / cheat-sheet -> reference genre, else concept).
Badge links follow the documented content-file rule: `#`.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_time import content_files, META  # noqa: E402

SKIP = {'INDEX.md', 'README.md', 'AGENTS.md', 'contributing.md'}
# Wholly headerless directories: no sibling to donate values to.
STACK_MAP = {
    '20-backend/20.13-java': ('Java', 'Backend'),
    '30-architecture/30.3-infra-patterns': ('Infra Patterns', 'Architecture'),
    '40-platform/40.12-iac': ('IaC', 'DevOps'),
    '70-interview-toolkit/70.2-coding-patterns': ('Coding Patterns', 'Interview'),
}
CAT_COLOR = {
    'Core': 'blue', 'Frontend': 'ff6b35', 'Backend': 'success', 'API': 'ff6b35',
    'Data': '8b5cf6', 'Architecture': '800080', 'DevOps': 'ff7f00',
    'Observability': '0ea5e9', 'Tooling': '64748b', 'Quality': '8b5cf6',
    'Real-Time': 'f59e0b', 'Interview': 'red', 'Reference': 'lightgrey',
    'Execution': 'ff6b35',
}
SECTION_COLOR = 'blue'   # corpus convention: every Section badge is blue
TAGS_COLOR = 'lightgrey'

BADGES = {
    'section': lambda v: f"[![Section](https://img.shields.io/badge/section-{q(v)}-{SECTION_COLOR})](#)",
    'category': lambda v: f"[![Category](https://img.shields.io/badge/category-{q(v)}-{CAT_COLOR.get(v, 'blue')})](#)",
    'tags': lambda v: f"[![Tags](https://img.shields.io/badge/tags-{q(v)}-{TAGS_COLOR})](#)",
}
HAS = {
    'section': re.compile(r'^\[\!\[Section\]\(https://img\.shields\.io/badge/section-', re.M),
    'category': re.compile(r'^\[\!\[Category\]\(https://img\.shields\.io/badge/category-', re.M),
    'tags': re.compile(r'^\[\!\[Tags\]\(https://img\.shields\.io/badge/tags-', re.M),
}


def q(v):
    """shields badge value: spaces -> %20, dashes -> '--' renders as one."""
    return v.replace(' ', '%20').replace('-', '--')


def tags_for(name):
    low = name.lower()
    if 'interview' in low:
        return 'interview-questions, reference'
    if 'cheat' in low:
        return 'cheat-sheet, reference'
    return 'concept'


def sibling_meta(rel):
    d = os.path.dirname(os.path.join(ROOT, rel))
    for f in sorted(os.listdir(d)):
        if not f.endswith('.md') or f in SKIP or f == os.path.basename(rel):
            continue
        m = META.search(open(os.path.join(d, f), encoding='utf-8').read())
        if m:
            return m.group('sec').strip(), m.group('cat').strip()
    return None


def stack_meta(rel):
    for prefix, val in STACK_MAP.items():
        if rel.startswith(prefix + '/'):
            return val
    return None


def backfill(rel):
    p = os.path.join(ROOT, rel)
    text = open(p, encoding='utf-8').read()
    orig = text
    comment = META.search(text)
    present = {k: bool(rx.search(text)) for k, rx in HAS.items()}

    if not comment:
        meta = sibling_meta(rel) or stack_meta(rel)
        if not meta:
            return None  # caller reports unmapped
        sec, cat = meta
        tags = tags_for(os.path.basename(rel))
        block = (f"<!-- section: {sec} | category: {cat} | tags: {tags} -->\n"
                 + BADGES['section'](sec) + "\n"
                 + BADGES['category'](cat) + "\n"
                 + BADGES['tags'](tags) + "\n\n")
        if text.lstrip().startswith('{% raw %}'):
            nl = text.index('\n')
            text = text[:nl + 1] + block + text[nl + 1:]
        else:
            text = block + text
    else:
        sec = comment.group('sec').strip()
        cat = comment.group('cat').strip()
        tags = tags_for(os.path.basename(rel))
        add = []
        for kind, val in (('section', sec), ('category', cat), ('tags', tags)):
            if not present[kind]:
                add.append(BADGES[kind](val))
        if add:
            lines = text.split('\n')
            idxs = [i for i, l in enumerate(lines) if l.startswith('[![')]
            if idxs:
                at = max(idxs) + 1
            else:
                # comment present but no badges at all: insert right after it
                at = next(i for i, l in enumerate(lines)
                          if l.startswith('<!-- section:')) + 1
            lines[at:at] = add
            text = '\n'.join(lines)
    if text != orig:
        open(p, 'w', encoding='utf-8').write(text)
        return 'header' if not comment else 'badges'
    return 'clean'


def main():
    done = {'header': 0, 'badges': 0, 'clean': 0}
    unmapped = []
    for rel in content_files():
        r = backfill(rel)
        if r is None:
            unmapped.append(rel)
        else:
            done[r] += 1
    print(f"headers written: {done['header']}, badge-only: {done['badges']}, "
          f"already complete: {done['clean']}")
    if unmapped:
        print("UNMAPPED (no sibling, no stack map entry):")
        for r in unmapped:
            print("  ", r)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
