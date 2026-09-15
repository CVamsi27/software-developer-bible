#!/usr/bin/env python3
"""Detect and fix de-indented code inside ASCII box diagrams.

Box diagrams (rows starting with '│ ') sometimes embed real code. In a
number of files that code lost its indentation — every row sat flat at
the box's column 0 — which renders as visibly broken indentation.

Approach: find a contiguous CODE STRETCH inside a box — a maximal run of
code-like rows (keyword-led or terminator-terminated), where blank rows
are transparent (a class body may contain blank rows) and ALL-CAPS
labels, arrow prose, and box-drawing rows end the stretch. Rebase the
whole stretch from brace depth 0 (2 spaces per level), preserving the
right box wall column exactly.

Safety rules:
  * A stretch is processed only if its FIRST row is flat (lead == 0) —
    the defect signature. Pre-indented stretches are never touched.
  * If ANY row in the stretch is indented MORE than its canonical depth
    (hand-aligned code), the stretch is skipped entirely — never strip.
  * Stretches start only at keyword-led rows (function/const/if/return/
    console./await/class/this. ...), so CSS, JSON, and pseudo-code that
    never uses those keywords are invisible to this tool.
  * Idempotent: a fixed file re-checks as zero.
"""
import re
import sys

FENCE = re.compile(r"^```")
KEYWORD = re.compile(
    r"^(function |const |let |var |if |for |while |return |console\.|import |export |"
    r"class |def |async |await |print\(|else|catch|finally|//|this\.)"
)
LABEL = re.compile(r"^[A-Z][A-Z0-9 /&+.'()-]{2,}:$")            # ALL-CAPS label
PROSE = re.compile(r"[A-Z]{3,}[A-Z0-9 /&+.'-]*:|→|^[A-Z][A-Z0-9]{2,}[\s(:&]")
TERMINATORS = (";", "{", "}", ")", ",", ">", "(")


def split_row(line):
    """Return (content_after_left_wall, right_wall_col_or_None)."""
    b = line.rstrip()
    wall = None
    if b.endswith("│"):
        wall = len(b) - 1
        b = b[:-1]
    if b.startswith("│ "):
        return b[2:], wall
    if b.startswith("│"):
        return b[1:], wall
    return None, wall


def code_like(st):
    if LABEL.match(st):
        return False
    if KEYWORD.match(st):
        return True
    body = st.split("//", 1)[0].rstrip()
    return bool(body) and body.endswith(TERMINATORS)


def canonical_ind(st, depth):
    starts_close = st.startswith("}")
    ind = max(depth - 1, 0) if starts_close else depth
    return ind, st.count("{") - st.count("}")


def scan(path, fix=False):
    content = open(path, encoding="utf-8").read()
    had_nl = content.endswith("\n")
    lines = content.splitlines()
    fence_in = False
    changed = 0
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if FENCE.match(ln):
            fence_in = not fence_in
            i += 1
            continue
        if not fence_in or not ln.startswith("│"):
            i += 1
            continue
        # Collect the box's contiguous interior rows.
        stretch = []  # (line_index, body, wall)
        j = i
        while j < n and lines[j].startswith("│") and not FENCE.match(lines[j]):
            body, wall = split_row(lines[j])
            if body is None:
                break
            stretch.append((j, body, wall))
            j += 1
        if j == i:
            i += 1
            continue
        # Walk code sub-stretches inside the box interior.
        k = 0
        while k < len(stretch):
            st0 = stretch[k][1].strip()
            if not st0 or PROSE.search(st0) or LABEL.match(st0) or not KEYWORD.match(st0):
                k += 1
                continue
            # Gather the stretch: blank rows transparent, prose/labels end.
            sub = []
            m = k
            while m < len(stretch):
                idx2, body2, wall2 = stretch[m]
                st2 = body2.strip()
                if not st2:
                    m += 1
                    continue
                if PROSE.search(st2) or LABEL.match(st2) or st2.startswith(("┌", "└", "├")):
                    break
                if not code_like(st2):
                    break
                sub.append((idx2, body2, wall2))
                m += 1
            # Defect signature: first row flat at the box column.
            if sub:
                lead0 = len(sub[0][1]) - len(sub[0][1].lstrip())
                if lead0 == 0:
                    depth = 0
                    ok = True
                    planned = []
                    for idx2, body2, wall2 in sub:
                        st2 = body2.strip()
                        ind, delta = canonical_ind(st2, depth)
                        depth += delta
                        cur = len(body2) - len(body2.lstrip())
                        # Over-indented row = hand-aligned code: veto whole stretch.
                        if cur > ind + 1:
                            ok = False
                            break
                        planned.append((idx2, ind, st2, wall2))
                    if ok:
                        for idx2, ind, st2, wall2 in planned:
                            new = "│ " + " " * (2 * ind) + st2
                            if wall2 is not None:
                                pad = wall2 - len(new)
                                if pad < 1:
                                    continue  # never break the wall
                                new += " " * pad + "│"
                            if new != lines[idx2]:
                                lines[idx2] = new
                                changed += 1
            k = m if m > k else k + 1
        i = j
    if fix and changed:
        open(path, "w", encoding="utf-8").write("\n".join(lines) + ("\n" if had_nl else ""))
    return changed


def main():
    import os

    fix = "--fix" in sys.argv
    skip = {".git", "node_modules", ".archive", "personal"}
    files = []
    for root, dirs, fs in os.walk("."):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in fs:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))
    total = 0
    hits = []
    for p in sorted(files):
        c = scan(p, fix=fix)
        if c:
            total += c
            hits.append((p, c))
    mode = "fixed" if fix else "de-indented lines found"
    for p, c in hits:
        print(f"  {c:3d}  {p}")
    print(f"{mode}: {total} lines in {len(hits)} files")
    sys.exit(1 if (hits and not fix) else 0)


if __name__ == "__main__":
    main()
