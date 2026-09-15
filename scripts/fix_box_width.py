#!/usr/bin/env python3
"""Shrink ASCII box diagrams to the width their content requires.

Wide boxes (the outer right wall pushed far past the last content by
padding) wrap on laptop screens and read as broken layout. This tool
rewrites each box at shrink-to-fit width:

  * every content character is preserved — only trailing padding spaces
    between the last content and the right wall are removed;
  * rows that span the full box width and consist of box-drawing rules
    (top/bottom borders, ├─┤ dividers, pure ─── rules) are regenerated
    at the new width (their dash count is padding by definition);
  * nested boxes keep their own shape: their walls sit at fixed columns
    and are preserved verbatim;
  * a box whose content still requires > 100 columns after shrinking is
    left unchanged (irreducible without re-layout) and reported.

--check  exits 1 if any box is wider than its content requires
--fix    rewrites the shrinkable boxes in place (idempotent)
--report lists boxes that remain > 100 after shrinking (informational)
"""
import re
import sys

FENCE = re.compile(r"^```")
WALL = "│"
RULE_FULL = re.compile(r"^[┌├└][─]*[┐┤┘]?$")   # spans the box: borders/dividers
RULE_DASH = re.compile(r"^[─]+$")
MAX_W = 100


def split_outer_wall(line):
    """('inner content' (rstripped), right_wall_col) for a '│ ... │' row."""
    b = line.rstrip()
    if len(b) >= 2 and b.endswith(WALL) and b.startswith(WALL + " "):
        return b[2:-1].rstrip(), len(b) - 1
    if len(b) >= 1 and b.endswith(WALL) and b.startswith(WALL):
        return b[1:-1].rstrip(), len(b) - 1
    return None, None


def row_kind(inner):
    """'rule' if the row is an outer full-width divider, else 'content'.

    Only ├─┤ dividers and bare ─── rules are regenerated. Nested box
    borders (┌─┐ / └─┘ appearing mid-block) are CONTENT at fixed
    columns and must be preserved verbatim."""
    if inner.startswith("├") and inner.endswith("┤"):
        return "rule"
    if RULE_DASH.match(inner):
        return "rule"
    return "content"


def rewrite_box(block, inner_w):
    """Rebuild all rows of a box at the given inner width.

    Every row totals inner_w + 4 columns: '│ ' + content + ' │' for
    content rows, '┌' + (inner_w + 2) dashes + '┐' for borders, so the
    right walls align exactly."""
    span = inner_w + 2  # dashes between corners
    out = []
    top = block[0]
    corners = (top[0], top.rstrip()[-1])
    out.append(corners[0] + "─" * span + corners[1])
    for line in block[1:-1]:
        stripped = line.rstrip()
        # Wall-less outer divider: ├────┤ spanning the full box width.
        if stripped.startswith("├") and stripped.endswith("┤") and RULE_DASH.match(stripped[1:-1]):
            out.append("├" + "─" * span + "┤")
            continue
        # Wall-less bare rule.
        if RULE_DASH.match(stripped):
            out.append("─" * (span + 2))
            continue
        inner, _ = split_outer_wall(line)
        if inner is None:
            out.append(line)
            continue
        if row_kind(inner) == "rule":
            if inner.startswith("├") and inner.endswith("┤"):
                out.append("├" + "─" * span + "┤")
            else:
                out.append("│ " + "─" * inner_w + " │")
            continue
        out.append("│ " + inner + " " * (inner_w - len(inner)) + " │")
    bot = block[-1]
    corners = (bot[0], bot.rstrip()[-1])
    out.append(corners[0] + "─" * span + corners[1])
    return out


def process(path, fix=False, report=False):
    content = open(path, encoding="utf-8").read()
    had_nl = content.endswith("\n")
    lines = content.splitlines()
    fence_in = False
    changed = 0
    remaining = []
    i, n = 0, len(lines)
    while i < n:
        if FENCE.match(lines[i]):
            fence_in = not fence_in
            i += 1
            continue
        if fence_in and lines[i].rstrip().startswith("┌"):
            # Fence-level analysis: find the extent of this fence, then
            # count boxes in it. Only fences containing exactly ONE box
            # are shrinkable — adjacent/stacked boxes in one fence are
            # aligned as a group by the alignment gate; shrinking one
            # member breaks group alignment (and invites destructive
            # auto-fixing).
            f_end = i
            while f_end < n and not FENCE.match(lines[f_end]):
                f_end += 1
            n_boxes = sum(
                1 for l in lines[i:f_end] if l.rstrip().startswith("┌")
            )
            if n_boxes != 1:
                i = f_end
                fence_in = False
                continue
            j = i
            block = []
            while j < n and not FENCE.match(lines[j]):
                block.append(lines[j])
                if lines[j].rstrip().startswith("└"):
                    break
                j += 1
            # Malformed run (never closed, or not a pure box) — skip.
            if (
                not block
                or not block[-1].rstrip().startswith("└")
                or not all(l.rstrip()[:1] in ("│", "┌", "├", "└") for l in block)
            ):
                i = j + 1
                continue
            old_w = max(len(l.rstrip()) for l in block)
            # Composite gate: every interior row must be pure single-
            # column — end with the right wall and contain NO box-drawing
            # chars inside (interior │┌└├┐┘┤ = side-by-side or nested
            # structure, unsafe to shrink as a unit). Top/bottom borders
            # must be pure dashes inside.
            BOXCHARS = set("│┌└├┐┘┤")
            composite = False
            for bi, l in enumerate(block):
                s = l.rstrip()
                if bi == 0 or bi == len(block) - 1:
                    if any(c in BOXCHARS for c in s[1:-1]):
                        composite = True
                        break
                    continue
                if s.endswith(WALL) and s.startswith("│ "):
                    if any(c in BOXCHARS for c in s[2:-1]):
                        composite = True
                        break
                    continue
                if s.startswith("├") and s.endswith("┤") and RULE_DASH.match(s[1:-1]):
                    continue
                if RULE_DASH.match(s):
                    continue
                composite = True
                break
            if composite:
                if report and old_w > MAX_W:
                    remaining.append((i + 1, old_w, old_w))
                i = j + 1
                continue
            if old_w > 3:
                need = 0
                for line in block[1:-1]:
                    inner, _ = split_outer_wall(line)
                    if inner is None:
                        continue
                    if row_kind(inner) == "rule":
                        continue
                    need = max(need, len(inner))
                need = max(need, 10)
                new_w = need + 4  # '│ ' + content + ' │'
                if new_w < old_w:
                    if new_w <= MAX_W:
                        new_block = rewrite_box(block, need)
                        if fix:
                            lines[i:j + 1] = new_block
                        changed += 1
                    elif report:
                        remaining.append((i + 1, old_w, need + 3))
                elif report and old_w > MAX_W:
                    remaining.append((i + 1, old_w, old_w))
            i = j + 1
        else:
            i += 1
    if fix and changed:
        open(path, "w", encoding="utf-8").write("\n".join(lines) + ("\n" if had_nl else ""))
    return changed, remaining


def main():
    import os

    argv = sys.argv[1:]
    fix = "--fix" in argv
    report = "--report" in argv
    skip = {".git", "node_modules", ".archive", "personal"}
    files = []
    for root, dirs, fs in os.walk("."):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in fs:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))
    total = 0
    hits = []
    all_remaining = []
    for p in sorted(files):
        c, rem = process(p, fix=fix, report=report)
        if c:
            total += c
            hits.append((p, c))
        for ln, old, new in rem:
            all_remaining.append((p, ln, old, new))
    mode = "narrowed" if fix else "over-padded boxes found"
    for p, c in hits:
        print(f"  {c:3d}  {p}")
    print(f"{mode}: {total} boxes in {len(hits)} files")
    if report:
        print(f"\nboxes remaining over {MAX_W} cols after shrink (irreducible without re-layout):")
        for p, ln, old, new in sorted(all_remaining, key=lambda x: -x[2]):
            print(f"  W={old} (min {new})  {p}:{ln}")
    sys.exit(1 if (hits and not fix) else 0)


if __name__ == "__main__":
    main()
