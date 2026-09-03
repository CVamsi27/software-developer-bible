#!/usr/bin/env python3
"""Check (and optionally fix) alignment of ASCII box diagrams and markdown tables.

Boxes: within each code-block diagram, content pipes and border corners at
every nesting level must land on one target column per level (fixed point, so
inner expansion grows outer walls). Top/bottom borders and dividers participate
even across blank lines inside the diagram. Side-by-side layouts, sibling
boxes, ERD/tee-line groups, and lines with odd pipe counts are skipped — they
are not nesting and must not be force-aligned.

Tables: every | in a column forms a straight line (checked outside fenced code
blocks only).

Usage:
  python3 scripts/check_alignment.py            # report issues, exit 1 if any
  python3 scripts/check_alignment.py --fix      # apply fixes in place
  python3 scripts/check_alignment.py --files a.md b.md   # limit scope
"""
import os
import re
import sys

BOXCHARS = set('─│┌┐└┘├┤┬┴┼═━┄┈╭╮╰╯')
OPENERS = set('┌├└')
CLOSERS = set('┐┤┘')
SKIPCHARS = set('┼┬┴═')


# ---------------------------------------------------------------------------
# ASCII boxes
# ---------------------------------------------------------------------------
def pipe_positions(line):
    return [i for i, ch in enumerate(line) if ch == '│']


def analyze(line):
    """-> (pipes, corners|None); corners = [(opener_pos, closer_pos, level)]."""
    pipes = pipe_positions(line)
    if any(ch in line for ch in SKIPCHARS):
        return pipes, None
    corners = []
    for i, ch in enumerate(line):
        if ch not in OPENERS:
            continue
        c = None
        for j in range(i + 1, len(line)):
            if line[j] in CLOSERS:
                c = j
                break
        if c is not None:
            corners.append((i, c, sum(1 for p in pipes if p < i)))
    return pipes, corners


def fix_group(group):
    info = [analyze(l) for l in group]

    # guards: odd pipes, side-by-side levels, sibling left walls
    for pipes, _ in info:
        if len(pipes) % 2 == 1:
            return group
    for _, corners in info:
        if corners:
            lvls = [lvl for _, _, lvl in corners]
            if len(set(lvls)) != len(lvls):
                return group
    lefts = {}
    for _, corners in info:
        for o, _c, lvl in corners or []:
            lefts.setdefault(lvl, set()).add(o)
    if any(len(ls) > 1 for ls in lefts.values()):
        return group
    corner_levels = {lvl for _, corners in info for _, _, lvl in corners or []}
    if not corner_levels:
        return group
    max_corner_r = max((c for _, corners in info if corners for _, c, _ in corners),
                       default=-1)

    contrib = {}
    for pipes, corners in info:
        k = len(pipes) - 1
        for t in range(1, k + 1):
            j = k - t
            if k > 2 * j and j in corner_levels and pipes[t] <= max_corner_r + 40:
                contrib[j] = max(contrib.get(j, 0), pipes[t])
        for o, c, lvl in corners or []:
            contrib[lvl] = max(contrib.get(lvl, 0), c)
    if not contrib:
        return group

    targets = dict(contrib)

    def sim_inserts(pipes):
        ins_at, shift = {}, 0
        k = len(pipes) - 1
        for t in range(1, k + 1):
            j = k - t
            if k > 2 * j and j in targets:
                ins = targets[j] - (pipes[t] + shift)
                if ins > 0:
                    ins_at[t] = ins
                    shift += ins
        pos, s = list(pipes), 0
        for t in range(1, k + 1):
            if t in ins_at:
                s += ins_at[t]
            pos[t] = pipes[t] + s
        return ins_at, pos

    for _ in range(40):  # fixed point: inner growth pushes outer walls
        changed = False
        for pipes, corners in info:
            if not pipes and not corners:
                continue
            k = len(pipes) - 1
            ins_at, pos = sim_inserts(pipes)
            if k >= 1 and pos[k] > targets.get(0, pos[k]):
                targets[0] = pos[k]
                changed = True
            for o, c, lvl in corners or []:
                sb = sum(ins_at[t] for t in ins_at if pipes[t] < c)
                if c + sb > targets.get(lvl, c + sb):
                    targets[lvl] = c + sb
                    changed = True
        if not changed:
            break

    out = []
    for line, (pipes, corners) in zip(group, info):
        if not pipes and not corners:
            out.append(line)
            continue
        k = len(pipes) - 1
        ins_at, _ = sim_inserts(pipes)
        pipe_ins = {pipes[t]: amt for t, amt in ins_at.items()}
        corner_ins = {}
        for o, c, lvl in corners or []:
            sb = sum(ins_at[t] for t in ins_at if pipes[t] < c)
            cur = c + sb
            if cur < targets.get(lvl, cur):
                corner_ins[c] = targets[lvl] - cur
        result = []
        for i, ch in enumerate(line):
            if i in pipe_ins:
                result.append(' ' * pipe_ins[i])
            if i in corner_ins and ch in CLOSERS:
                result.append('─' * corner_ins[i])
            result.append(ch)
        out.append(''.join(result).rstrip())
    return out


def corner_pairs(line):
    """-> [(opener_pos, closer_pos, opener_ch, closer_ch, level)] on this line."""
    pipes = pipe_positions(line)
    pairs = []
    for i, ch in enumerate(line):
        if ch not in OPENERS:
            continue
        for j in range(i + 1, len(line)):
            if line[j] in CLOSERS:
                pairs.append((i, j, ch, line[j], sum(1 for p in pipes if p < i)))
                break
    return pairs


def border_unify(lines):
    """Phase 2: expand a box's top/bottom/divider borders to the unanimous
    content wall column. Only inserts dashes; only fires when every even-pipe
    content line inside the box agrees on one wall column, so side-by-side
    diagrams (many columns) and odd-line layouts are never touched."""
    lines = list(lines)
    stack = {}
    boxes = []
    for idx, l in enumerate(lines):
        for o, c, oc, _cc, lvl in corner_pairs(l):
            key = (o, lvl)
            if oc == '┌':
                stack.setdefault(key, []).append((idx, c))
            elif oc == '└' and stack.get(key):
                top_idx, _ = stack[key].pop()
                boxes.append((top_idx, idx, o, lvl))
    changed = 0
    for top_idx, bot_idx, o, lvl in boxes:
        walls = set()
        for k in range(top_idx + 1, bot_idx):
            lk = lines[k]
            pk = pipe_positions(lk)
            if not pk or len(pk) % 2 == 1 or pk[0] != o:
                continue
            rightmost = max([i for i, ch in enumerate(lk) if ch in '│┐┘┤'],
                            default=-1)
            if rightmost > 0:
                walls.add(rightmost)
        if len(walls) != 1:
            continue
        W = walls.pop()
        for k in range(top_idx, bot_idx + 1):
            lk = lines[k]
            for o2, c2, oc2, _cc2, lvl2 in corner_pairs(lk):
                if (o2, lvl2) == (o, lvl) and oc2 in '┌└├' and c2 < W:
                    lines[k] = lk[:c2] + '─' * (W - c2) + lk[c2:]
                    changed += 1
                    break
    return lines, changed


def fix_boxes(text):
    lines = text.split('\n')
    out, i, n, changed = [], 0, len(lines), 0
    while i < n:
        line = lines[i]
        if not any(ch in line for ch in BOXCHARS):
            out.append(line)
            i += 1
            continue
        j = i
        while j < n:
            lj = lines[j]
            if any(ch in lj for ch in BOXCHARS):
                j += 1
            elif lj.strip() == '':
                k = j + 1
                while k < n and lines[k].strip() == '':
                    k += 1
                j = k
            else:
                break
        group = lines[i:j]
        fixed = fix_group(group)
        if fixed != group:
            changed += 1
        fixed, c2 = border_unify(fixed)
        changed += c2
        out.extend(fixed)
        i = j
    return '\n'.join(out), changed


# ---------------------------------------------------------------------------
# Markdown tables
# ---------------------------------------------------------------------------
def split_cells(row):
    cells, cur, i, n, in_span = [], [], 0, len(row), False
    while i < n:
        ch = row[i]
        if ch == '\\' and i + 1 < n and row[i + 1] == '|':
            cur.append('\\|')
            i += 2
            continue
        if ch == '`':
            in_span = not in_span
            cur.append(ch)
            i += 1
            continue
        if ch == '|' and not in_span:
            cells.append(''.join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append(''.join(cur))
    return cells


SEP = re.compile(r':?-{3,}:?$')


def align_table(rows):
    parsed = []
    for r in rows:
        cells = split_cells(r)
        if len(cells) >= 2 and cells[0] == '' and cells[-1] == '':
            cells = cells[1:-1]
        parsed.append(cells)
    ncols = max(len(c) for c in parsed)
    for c in parsed:
        c += [''] * (ncols - len(c))
    sep_row = [i for i, c in enumerate(parsed) if all(SEP.match(x.strip()) for x in c)]
    widths = [0] * ncols
    for c in parsed:
        for i, cell in enumerate(c):
            widths[i] = max(widths[i], len(cell.strip()))
    out = []
    for ci, c in enumerate(parsed):
        cells_out = []
        for i, cell in enumerate(c):
            s = cell.strip()
            if ci in sep_row:
                left, right = s.startswith(':'), s.endswith(':')
                if left and right:
                    s = ':' + '-' * max(widths[i] - 2, 3) + ':'
                elif left:
                    s = ':' + '-' * max(widths[i] - 1, 3)
                elif right:
                    s = '-' * max(widths[i] - 1, 3) + ':'
                else:
                    s = '-' * widths[i]
            cells_out.append(s)
        out.append('| ' + ' | '.join(cells_out) + ' |')
    return out


def fix_tables(text):
    lines = text.split('\n')
    out, i, n, changed, in_code = [], 0, len(lines), 0, False
    while i < n:
        s = lines[i]
        if s.strip().startswith('```'):
            in_code = not in_code
            out.append(s)
            i += 1
            continue
        if not in_code and s.startswith('|') and s.endswith('|') and '|' in s[1:-1]:
            j = i
            rows = []
            while j < n and lines[j].startswith('|') and lines[j].endswith('|'):
                rows.append(lines[j])
                j += 1
            if len(rows) >= 2 and len({len(split_cells(r)) for r in rows}) == 1:
                aligned = align_table(rows)
                if aligned != rows:
                    changed += 1
                out.extend(aligned)
            else:
                out.extend(rows)
            i = j
        else:
            out.append(s)
            i += 1
    return '\n'.join(out), changed


# ---------------------------------------------------------------------------
def process_file(path, fix):
    with open(path, encoding='utf-8') as f:
        orig = f.read()
    text = orig
    box_groups = box_files = 0
    text, g = fix_boxes(text)
    box_groups += g
    text, t = fix_tables(text)
    if text == orig:
        return 0
    box_changed = text != orig
    if fix:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    return 1


def main():
    fix = '--fix' in sys.argv
    targets = [a for a in sys.argv[1:] if not a.startswith('--')]
    if targets:
        paths = [p for p in targets if p.endswith('.md')]
    else:
        paths = [os.path.join(r, f)
                 for r, _, fs in os.walk('.')
                 if '.git' not in r and 'node_modules' not in r
                 for f in fs if f.endswith('.md')]
    bad = []
    for p in sorted(paths):
        if process_file(p, fix):
            bad.append(p)
    if not fix:
        print(f"{len(bad)} file(s) with misaligned boxes/tables"
              + ("" if not bad else ":\n  " + "\n  ".join(bad)))
        sys.exit(1 if bad else 0)
    print(f"{len(bad)} file(s) fixed" if bad else "Nothing to fix — all aligned.")


if __name__ == '__main__':
    main()