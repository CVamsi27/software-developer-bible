#!/usr/bin/env python3
"""Estimated study time per chapter, per category, per stack.

The numbers are computed, never guessed, so the "Read time" column means one
thing everywhere and cannot drift. A previous hand-guessed pass produced a
chapter with 2,912 words labelled 15 min next to one with 2,353 words labelled
20 min — the column was decoration.

Model (a *study* estimate, not a skim):
    prose words / 200        reading at 200 wpm
    code lines  / 25         reading code to understand it, ~2.4 s/line
    table rows  / 40         scanning tabular data
    round up, floor of 2 min for any substantive chapter

Usage:
  python3 scripts/read_time.py --file 10-frontend/10.1-javascript/...md
  python3 scripts/read_time.py --all                      # per-stack totals
  python3 scripts/read_time.py --check                    # gate: INDEX + badge drift
  python3 scripts/read_time.py --write                    # refresh INDEXes and badges

The same estimate is stamped twice, and the gate holds both:
  - a `> **Study time:**` line in every INDEX (category/stack/root totals)
  - a 4th shields badge in every content file's header block:
        [![Read time](https://img.shields.io/badge/read--time-12_min-informational)](#)
    (shields renders `_` as a space; `read--time` renders as "read time")
"""
import argparse
import os
import re
import sys
import md_fences
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal', 'docs', '.freebuff'}
SKIP_FILES = {'INDEX.md', 'README.md', 'AGENTS.md', 'contributing.md', 'ROADMAP.md', 'search.md'}
EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang',
                   '80-lanes', '81-lanes', 'lanes/', 'projects/')

FENCE = re.compile(r'^\s*(```|~~~)')
H1 = re.compile(r'^#\s+(.+?)\s*$', re.M)
ROW_LINK = re.compile(r'^\|\s*\d+\s*\|\s*\[[^\]]+\]\(([^)]+\.md)\)')
TIME_LINE = re.compile(r'^> \*\*Study time:\*\* .*$', re.M)
META = re.compile(r'^<!-- section: (?P<sec>[^|]+) \| category: (?P<cat>[^|]+) \|', re.M)

BADGE_READ = re.compile(r'^\[\!\[Read time\]\(https://img\.shields\.io/badge/read--time-[^)]+\)\]\(#\)[ \t]*$', re.M)
TAGS_BADGE = re.compile(r'^\[\!\[Tags\]\(https://img\.shields\.io/badge/tags-[^)]+\)\]\(#\)[ \t]*$', re.M)
CATEGORY_BADGE = re.compile(r'^\[\!\[Category\]\(https://img\.shields\.io/badge/category-[^)]+\)\]\(#\)[ \t]*$', re.M)

PROSE_WPM = 200
CODE_LPM = 25
TABLE_RPM = 40
MINUTES_FLOOR = 2


def style(path):
    """Classify a markdown file so estimates are comparable."""
    name = os.path.basename(path).lower()
    if 'interview' in name or 'cheat-sheet' in name or name == 'revision.md':
        return 'reference'          # scanned, not read linearly
    if 'cheat' in name or 'tracker' in name:
        return 'reference'
    return 'concept'


def count(path):
    prose = code = rows = 0
    in_fence = False
    for _, line, in_fence, is_fence in md_fences.walk(open(path, encoding='utf-8')):
        if is_fence:
            continue
        if in_fence:
            code += 1
            continue
        if line.lstrip().startswith('|') and line.count('|') >= 2:
            rows += 1
            continue
        prose += len(line.split())
    return prose, code, rows


def minutes(path):
    prose, code, rows = count(path)
    if style(path) == 'reference':
        # Reference material is searched, not read end to end; halve the prose.
        raw = prose / 2 / PROSE_WPM + code / CODE_LPM + rows / TABLE_RPM
    else:
        raw = prose / PROSE_WPM + code / CODE_LPM + rows / TABLE_RPM
    return max(MINUTES_FLOOR, int(raw + 0.5))


def human(mins):
    h, m = divmod(int(mins), 60)
    if h and m:
        return f'{h} h {m} m'
    if h:
        return f'{h} h'
    return f'{m} min'


def badge_line(rel):
    """The exact Read-time badge line the file's header must carry."""
    return (f"[![Read time](https://img.shields.io/badge/read--time-"
            f"{minutes(os.path.join(ROOT, rel))}_min-informational)](#)")


def content_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        rel = os.path.relpath(root, ROOT).replace(os.sep, '/')
        if rel.startswith(EXEMPT_PREFIXES):
            continue
        for f in sorted(files):
            if f.endswith('.md') and f not in SKIP_FILES:
                p = os.path.join(root, f)
                yield os.path.relpath(p, ROOT).replace(os.sep, '/')


def stack_of(rel):
    return rel.split('/')[0]


def index_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        if 'INDEX.md' in files:
            yield os.path.join(root, 'INDEX.md')


def linked_files(index_path):
    """Files listed by an INDEX: table rows plus plain markdown links."""
    out = []
    d = os.path.dirname(index_path)
    for line in open(index_path, encoding='utf-8'):
        targets = []
        m = ROW_LINK.match(line)
        if m:
            targets.append(m.group(1))
        else:
            targets += re.findall(r'\]\(([^)\s]+\.md)\)', line)
        for t in targets:
            if t.startswith(('http', '#')):
                continue
            p = os.path.normpath(os.path.join(d, t))
            if os.path.isfile(p):
                rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
                if rel not in out:
                    out.append(rel)
    return out


def content_under(dirpath):
    """Content files in an INDEX's own directory subtree.

    Summing the files an INDEX *links* would be wrong for stack and root
    INDEXes, which link other INDEXes — the count has to come from the disk.
    """
    out = []
    base = os.path.relpath(dirpath, ROOT).replace(os.sep, '/')
    for rel in content_files():
        if base in ('.', '') or rel == base or rel.startswith(base + '/'):
            out.append(rel)
    return out


def category_totals():
    """Map each INDEX file to (sum minutes, count) of its subtree's files."""
    totals = {}
    for idx in index_files():
        files = content_under(os.path.dirname(idx))
        totals[idx] = (sum(minutes(os.path.join(ROOT, f)) for f in files), len(files))
    return totals


def refresh_columns(text, idx_dir):
    """Rewrite per-file minutes in any table whose header has `Read time`.

    Only tables that already carry the column are touched: other tables use
    their last cell for something else (`Purpose`, `Topics`), and inventing a
    column in them would fight the alignment gate for no benefit.
    """
    out, in_read_time_table = [], False
    for line in text.split('\n'):
        if line.startswith('|'):
            if 'Read time' in line:
                in_read_time_table = True
            elif re.match(r'^\|[\s\-:|]+\|\s*$', line):
                pass  # separator row keeps the table mode
        else:
            in_read_time_table = False
        if in_read_time_table and line.startswith('|'):
            m = re.match(r'^(\|\s*\d+\s*\|\s*\[[^\]]+\]\(([^)]+\.md)\)\s*\|.*\|)\s*[^|]*\|\s*$', line)
            if m:
                p = os.path.normpath(os.path.join(idx_dir, m.group(2)))
                if os.path.isfile(p):
                    mine = minutes(p)
                    cells = [c for c in line.split('|')]
                    cells[-2] = f" {mine} min "
                    out.append('|'.join(cells).rstrip())
                    continue
        out.append(line)
    return '\n'.join(out)


def write_indexes(dry_run=False):
    totals = category_totals()
    changed = 0
    for idx, (total, n) in sorted(totals.items()):
        rel = os.path.relpath(idx, ROOT).replace(os.sep, '/')
        if not n:
            # Excluded subtrees (lanes, projects) carry no study time; a stale
            # line from an earlier pass would be a claim with no source.
            text = open(idx, encoding='utf-8').read()
            if TIME_LINE.search(text):
                new = TIME_LINE.sub('', text).replace('\n\n\n', '\n\n')
                changed += 1
                if not dry_run:
                    open(idx, 'w', encoding='utf-8').write(new)
            continue
        text = refresh_columns(open(idx, encoding='utf-8').read(), os.path.dirname(idx))
        line = f"> **Study time:** ≈ {human(total)} of reading ({n} files, ~{round(total / n)} min average)."
        lines = text.split('\n')
        placed = False
        for i, l in enumerate(lines):
            if TIME_LINE.match(l):
                lines[i] = line
                placed = True
                break
        if not placed:
            hi = next((i for i, l in enumerate(lines) if l.startswith('# ')), None)
            if hi is None:
                continue
            # exactly one blank line between the title and the new line
            while hi + 1 < len(lines) and not lines[hi + 1].strip():
                del lines[hi + 1]
            lines[hi + 1:hi + 1] = ['', line]
        new = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines))
        if new == text:
            continue
        changed += 1
        if not dry_run:
            open(idx, 'w', encoding='utf-8').write(new)
    return changed


def write_badge(rel, dry_run=False):
    """Insert or refresh the 4th (Read time) badge in one content file.

    Returns 1 if the file changed. Position: directly under the Tags badge,
    keeping the documented header block intact.
    """
    p = os.path.join(ROOT, rel)
    text = open(p, encoding='utf-8').read()
    want = badge_line(rel)
    m = BADGE_READ.search(text)
    if m:
        if m.group(0).rstrip() == want:
            return 0
        new = BADGE_READ.sub(lambda _mm: want, text, count=1)
    else:
        # No badge yet: insert after the Tags badge (or Category as fallback).
        anchor = TAGS_BADGE.search(text) or CATEGORY_BADGE.search(text)
        if not anchor:
            return 0  # headerless — count it so the gap is visible
        nl = text.find('\n', anchor.end())
        if nl == -1:
            new = text.rstrip('\n') + '\n' + want + '\n'
        else:
            new = text[:nl] + '\n' + want + text[nl:]
    if not dry_run:
        open(p, 'w', encoding='utf-8').write(new)
    return 1


def badge_check():
    """Every content file's Read-time badge must exist and match the estimate."""
    bad_missing, bad_value = [], []
    n = 0
    for rel in content_files():
        n += 1
        text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        want = badge_line(rel)
        m = BADGE_READ.search(text)
        if not m:
            bad_missing.append(rel)
        elif m.group(0).rstrip() != want:
            bad_value.append((rel, m.group(0).strip(), want))
    if bad_missing or bad_value:
        print(f"READ-TIME BADGE DRIFT: {len(bad_missing)} missing, {len(bad_value)} stale of {n}")
        for rel in bad_missing[:10]:
            print(f"  missing: {rel}")
        for rel, got, want in bad_value[:10]:
            print(f"  stale:   {rel}\n    got:    {got}\n    want:   {want}")
        print("\nFix: python3 scripts/read_time.py --write")
        return 1
    # Same vacuity on the badge half: 0 content files would print the same
    # sentence as a clean corpus (scan_scope).
    guard(n, 'content files', str(ROOT))
    print(f"read-time badges consistent on {n} content files")
    return 0


def check():
    """Every INDEX's declared study time must match the computed one."""
    totals = category_totals()
    bad = []
    for idx, (total, n) in sorted(totals.items()):
        if not n:
            continue
        rel = os.path.relpath(idx, ROOT).replace(os.sep, '/')
        text = open(idx, encoding='utf-8').read()
        m = TIME_LINE.search(text)
        expect = f"≈ {human(total)}"
        if not m:
            bad.append((rel, 'missing study-time line', expect))
        elif expect not in m.group(0):
            bad.append((rel, m.group(0), expect))
    if bad:
        print(f"READ-TIME DRIFT: {len(bad)} INDEX file(s) disagree with the computed estimate")
        for rel, got, expect in bad:
            print(f"  {rel}\n    declared: {got}\n    computed: {expect}")
        print("\nFix: python3 scripts/read_time.py --write")
        return 1
    # A study-time gate over no INDEXes and no content files finds nothing to
    # disagree with (see scan_scope): "consistent across 0 INDEX files" is
    # what a broken walk prints, identical to a real pass.
    n_idx = len([t for t in totals.values() if t[1]])
    guard(n_idx, 'INDEX files', str(ROOT))
    rc = badge_check()
    if rc == 0:
        print(f"read times consistent across {n_idx} INDEX files")
    return rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if args.file:
        p = os.path.join(ROOT, args.file)
        print(f"{minutes(p)} min  {args.file}\n  badge: {badge_line(args.file)}")
        return 0
    if args.check:
        return check()
    if args.write or args.dry_run:
        n_idx = write_indexes(args.dry_run)
        n_badge = sum(write_badge(rel, args.dry_run) for rel in content_files())
        print(f"{n_idx} INDEX file(s), {n_badge} content badge(s) updated")
        return 0

    per_stack = {}
    for rel in content_files():
        per_stack.setdefault(stack_of(rel), []).append(minutes(os.path.join(ROOT, rel)))
    grand = 0
    for stack in sorted(per_stack):
        vals = per_stack[stack]
        grand += sum(vals)
        print(f"{stack:32s} {len(vals):4d} files  {human(sum(vals)):>9}  ({round(sum(vals)/len(vals))} min avg)")
    print(f"{'TOTAL':32s} {sum(len(v) for v in per_stack.values()):4d} files  {human(grand):>9}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
