#!/usr/bin/env python3
"""Detect and fix de-indented code inside ASCII box diagrams.

Box diagrams (rows starting with '│ ') sometimes embed real code. In a
number of files that code lost its indentation — every row sat flat at
the box's column 0 — which renders as visibly broken indentation.

Modes (combinable; default is JS only, which is what the verify/CI gate
runs):
  (default)  JS/TS stretches anchored at keyword-led rows
  --json     JSON object stretches anchored at a flat '{' row
  --css      CSS rule stretches anchored at a flat 'selector {' row

Approach per mode: find a contiguous stretch — blank rows are
transparent, ALL-CAPS labels, arrow prose, and box-drawing rows end it
— then rebase the whole stretch from brace depth (2 spaces per level),
preserving the right box wall column exactly.

Safety rules (all modes):
  * A stretch is processed only if its FIRST row is flat (lead == 0) —
    the defect signature. Pre-indented stretches are never touched.
  * Non-default modes are strict: EVERY row must conform to the
    language shape, or the stretch is invisible. One odd row (a TS
    catch, a prose line) vetoes the stretch.
  * If ANY row is indented MORE than its canonical depth (hand-aligned
    code), the stretch is skipped entirely — never strip.
  * A JSON/CSS stretch must close: depth must return to 0 inside the
    gathered rows, else the stretch is skipped as incomplete.
  * Idempotent: a fixed file re-checks as zero.
"""
import re
import sys
import md_fences

FENCE = re.compile(r"^```")
KEYWORD = re.compile(
    r"^(function |const |let |var |if |for |while |return |console\.|import |export |"
    r"class |def |async |await |print\(|else|catch|finally|//|this\.)"
)
LABEL = re.compile(r"^[A-Z][A-Z0-9 /&+.'()-]{2,}:$")            # ALL-CAPS label
PROSE = re.compile(r"[A-Z]{3,}[A-Z0-9 /&+.'-]*:|→|^[A-Z][A-Z0-9]{2,}[\s(:&]")
TERMINATORS = (";", "{", "}", ")", ",", ">", "(")

STR_LIT = re.compile(r'"(?:[^"\\]|\\.)*"')                       # JSON strings
CSS_COMMENT = re.compile(r"/\*.*?\*/")


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


# --------------------------------------------------------------- JS mode
def js_code_like(st):
    if LABEL.match(st):
        return False
    if KEYWORD.match(st):
        return True
    body = st.split("//", 1)[0].rstrip()
    return bool(body) and body.endswith(TERMINATORS)


# -------------------------------------------------------------- JSON mode
def json_row_ok(st):
    """Strict: every row must be structurally valid inside pretty JSON."""
    if KEYWORD.match(st) or PROSE.search(st) or LABEL.match(st):
        return False
    s = STR_LIT.sub("S", st).strip()
    if re.fullmatch(r"\{|\}|\[|\]", s):
        return True
    if re.fullmatch(r"[\{\}\[\]]+[\s,]*", s):        # '},' '}}' ...
        return True
    if re.fullmatch(r"S\s*:\s*S[\s,]*", s):          # "key": "value",
        return True
    if re.fullmatch(r"S\s*:\s*[\{\[]+[\s,]*", s):    # "key": {
        return True
    if re.fullmatch(r"S\s*:\s*", s):                 # "key":
        return True
    if re.fullmatch(r"S[\s,]*", s):                  # bare array element
        return True
    return False


# --------------------------------------------------------------- CSS mode
def css_row_ok(st):
    """Strict: every row must be a selector line, property, or brace."""
    if KEYWORD.match(st) or PROSE.search(st) or LABEL.match(st):
        return False
    s = CSS_COMMENT.sub("", st).strip()
    if not s:
        return True                                   # pure comment row
    if s == "}":
        return True
    if s.endswith("{") and ";" not in s and len(s) > 1:
        return True                                   # selector opener
    if re.fullmatch(r"[a-zA-Z-]+\s*:\s*[^;{}]+;", s):  # prop / --var: value;
        return True
    return False


def canonical_ind(st, depth, skeleton=None):
    starts_close = st.startswith("}")
    ind = max(depth - 1, 0) if starts_close else depth
    if skeleton is not None:
        delta = skeleton.count("{") - skeleton.count("}")
    else:
        delta = st.count("{") - st.count("}")
    return ind, delta


def apply_planned(lines, planned, changed):
    """Write planned rows; never break the right wall."""
    for idx2, ind, st2, wall2 in planned:
        new = "│ " + " " * (2 * ind) + st2
        if wall2 is not None:
            pad = wall2 - len(new)
            if pad < 1:
                continue
            new += " " * pad + "│"
        if new != lines[idx2]:
            lines[idx2] = new
            changed[0] += 1


def scan(path, fix=False, modes=("js",)):
    content = open(path, encoding="utf-8").read()
    had_nl = content.endswith("\n")
    lines = content.splitlines()
    fence_in = False
    fence_state = {idx: (inf, isf) for idx, _, inf, isf in md_fences.walk(lines)}
    changed = [0]
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        inf, isf = fence_state[i]
        if isf:
            fence_in = inf
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

        # ---------------- JS stretches (default mode) ----------------
        if "js" in modes:
            k = 0
            while k < len(stretch):
                st0 = stretch[k][1].strip()
                if not st0 or PROSE.search(st0) or LABEL.match(st0) or not KEYWORD.match(st0):
                    k += 1
                    continue
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
                    if not js_code_like(st2):
                        break
                    sub.append((idx2, body2, wall2))
                    m += 1
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
                            if cur > ind + 1:      # hand-aligned: veto
                                ok = False
                                break
                            planned.append((idx2, ind, st2, wall2))
                        if ok:
                            apply_planned(lines, planned, changed)
                k = m if m > k else k + 1

        # ---------------- JSON stretches (--json) --------------------
        if "json" in modes:
            k = 0
            while k < len(stretch):
                idx, _, _ = stretch[k]
                body = split_row(lines[idx])[0]
                st = body.strip()
                flat = (len(body) - len(body.lstrip())) == 0
                if st != "{" or not flat:
                    k += 1
                    continue
                sub, m, depth, closed = [], k, 0, False
                while m < len(stretch):
                    idx2, _, _ = stretch[m]
                    b2, w2 = split_row(lines[idx2])
                    st2 = b2.strip()
                    if not st2:
                        m += 1
                        continue
                    if not json_row_ok(st2):
                        break
                    lead2 = len(b2) - len(b2.lstrip())
                    sub.append((idx2, st2, w2, lead2))
                    depth += STR_LIT.sub("S", st2).count("{") - STR_LIT.sub("S", st2).count("}")
                    m += 1
                    if depth == 0 and st2.startswith("}"):
                        closed = True
                        break
                if closed and len(sub) >= 3 and depth == 0:
                    d = 0
                    ok = True
                    planned = []
                    for idx2, st2, w2, lead2 in sub:
                        sk = STR_LIT.sub("S", st2)
                        ind, delta = canonical_ind(st2, d, skeleton=sk)
                        d += delta
                        if lead2 > ind + 1:        # hand-aligned: veto
                            ok = False
                            break
                        planned.append((idx2, ind, st2, w2))
                    if ok:
                        apply_planned(lines, planned, changed)
                k = m if m > k else k + 1

        # ---------------- CSS stretches (--css) ----------------------
        if "css" in modes:
            k = 0
            while k < len(stretch):
                idx, _, _ = stretch[k]
                body = split_row(lines[idx])[0]
                st = body.strip()
                flat = (len(body) - len(body.lstrip())) == 0
                is_selector = (
                    flat and st.endswith("{") and ";" not in st
                    and len(st) > 1 and not KEYWORD.match(st)
                    and not PROSE.search(st) and not LABEL.match(st)
                )
                if not is_selector:
                    k += 1
                    continue
                sub, m, depth, closed = [], k, 0, False
                while m < len(stretch):
                    idx2, _, _ = stretch[m]
                    b2, w2 = split_row(lines[idx2])
                    st2 = b2.strip()
                    if not st2:
                        m += 1
                        continue
                    if not css_row_ok(st2):
                        break
                    lead2 = len(b2) - len(b2.lstrip())
                    sub.append((idx2, st2, w2, lead2))
                    depth += st2.count("{") - st2.count("}")
                    m += 1
                    if depth == 0 and st2 == "}":
                        closed = True
                        break
                if closed and len(sub) >= 3 and depth == 0:
                    d = 0
                    ok = True
                    planned = []
                    for idx2, st2, w2, lead2 in sub:
                        ind, delta = canonical_ind(st2, d)
                        d += delta
                        if lead2 > ind + 1:        # hand-aligned: veto
                            ok = False
                            break
                        planned.append((idx2, ind, st2, w2))
                    if ok:
                        apply_planned(lines, planned, changed)
                k = m if m > k else k + 1

        i = j
    if fix and changed[0]:
        open(path, "w", encoding="utf-8").write("\n".join(lines) + ("\n" if had_nl else ""))
    return changed[0]


def main():
    import os

    argv = sys.argv[1:]
    fix = "--fix" in argv
    modes = {"js"}
    if "--json" in argv:
        modes.add("json")
    if "--css" in argv:
        modes.add("css")
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
        c = scan(p, fix=fix, modes=modes)
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
