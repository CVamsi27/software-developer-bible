#!/usr/bin/env python3
"""Reorder template sections into canonical order (one-off normalizer).

Why: 22 concept chapters had their cross-reference/teaching sections in a
non-canonical sequence (most commonly `## See Also` before `## Summary`).
Editing them by hand invites transposition errors; this does a stable sort
instead.

How it sorts:
  - Canonical sections sort by their index in contributing.md's template.
  - Domain-specific headings (e.g. `## The 3 Properties`,
    `## Capacity Estimation`) keep their position relative to the canonical
    section they follow, so a chapter's own narrative order is preserved.

Separators travel with their sections unchanged, so the diff is a pure
reorder. The only forced rule is contributing.md rule 8: a `---` always
precedes `## See Also`.

Usage:
  python3 scripts/fix_section_order.py --dry-run <files...>
  python3 scripts/fix_section_order.py <files...>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_template import CANON_A, normalize, HEAD  # noqa: E402
import md_fences  # noqa: E402

CANON_INDEX = {name: i for i, name in enumerate(CANON_A)}
# Optional section that may sit before Summary
CANON_INDEX.setdefault('Interview Questions', 10)


def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    heads = []
    for i, line, in_fence, _ in md_fences.walk(lines):
        if in_fence:
            continue
        m = HEAD.match(line)
        if m:
            heads.append((i, m.group(1)))
    if not heads:
        return lines, []
    preamble = lines[:heads[0][0]]
    sections = []
    for k, (i, raw_name) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        sections.append({'name': raw_name, 'norm': normalize(raw_name),
                         'head': lines[i], 'body': lines[i + 1:end]})
    return preamble, sections


def strip_trailing_rule(body):
    """Remove a trailing `---` separator (and the blanks around it)."""
    out = list(body)
    while out and not out[-1].strip():
        out.pop()
    if out and out[-1].strip() == '---':
        out.pop()
        while out and not out[-1].strip():
            out.pop()
        return out, True
    return out, False


def attribute_rules(sections):
    """A `---` sits *between* sections, so attribute it to the section that
    follows it (contributing.md: the rule goes between Revision Questions and
    See Also). Keeps a pure reorder from shuffling separators around."""
    for k, s in enumerate(sections):
        body, trailing = strip_trailing_rule(s['body'])
        s['body'] = body
        if trailing and k + 1 < len(sections):
            sections[k + 1]['had_rule'] = True
        s.setdefault('had_rule', False)
    return sections


def sort_key(sec, state):
    """Stable-canonical key. Non-canonical headings anchor after the last
    canonical heading seen, preserving their relative narrative order."""
    n = sec['norm']
    if n in CANON_INDEX:
        state['last'] = CANON_INDEX[n]
        state['seq'] = 0
        return (CANON_INDEX[n], 0, 0)
    state['seq'] += 1
    return (state['last'], 1, state['seq'])


def reorder(path, dry_run=False):
    preamble, sections = parse(path)
    if not sections:
        return False
    out_sections = attribute_rules([dict(s, had_rule=False) for s in sections])
    state = {'last': -1, 'seq': 0}
    ordered = [s for _, _, s in sorted(
        ((sort_key(s, state), i, s) for i, s in enumerate(out_sections)),
        key=lambda t: (t[0], t[1]))]

    new_lines = list(preamble)
    for s in ordered:
        while new_lines and not new_lines[-1].strip():
            new_lines.pop()
        # Keep the section's own `---` (it travels with the block); force one
        # before See Also per contributing.md rule 8.
        want_rule = s['had_rule'] or s['norm'] == 'See Also'
        if want_rule:
            new_lines += ['', '---', '', s['head']]
        else:
            new_lines += ['', s['head']]
        new_lines += s['body']
    # normalize: collapse >2 blank lines that may have appeared
    text = '\n'.join(new_lines)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    if not text.endswith('\n'):
        text += '\n'

    if dry_run:
        print(f"{path}\n    OLD: {' > '.join(s['norm'] for s in sections)}")
        print(f"    NEW: {' > '.join(s['norm'] for s in ordered)}")
        return False
    open(path, 'w', encoding='utf-8').write(text)
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    changed = 0
    for p in args:
        if reorder(p, dry_run=dry):
            changed += 1
            print(f"reordered {p}")
    if not dry:
        print(f"\n{changed} file(s) reordered")


if __name__ == '__main__':
    main()
