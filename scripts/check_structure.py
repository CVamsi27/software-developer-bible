#!/usr/bin/env python3
"""Verify bible structure: relative md links resolve; numeric IDs unique; sequences contiguous.

Usage:
  python3 scripts/check_structure.py [--root .] [--links-only]

--links-only skips the contiguity check (useful mid-restructure).
"""
import re
import sys
from pathlib import Path
import md_fences

args = [a for a in sys.argv[1:] if not a.startswith("--")]
links_only = "--links-only" in sys.argv
ROOT = Path(args[0] if args else ".").resolve()
SKIP = ("/.git/", "/node_modules/", "/.archive/", "/.freebuff/", "/.sass-cache/")
MD = [p for p in sorted(ROOT.rglob("*.md")) if not any(s in str(p) for s in SKIP)]
errors = []

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODESPAN = re.compile(r"`[^`]*`")


def strip_code(text: str) -> str:
    out = []
    for _, line, in_fence, _ in md_fences.walk(text.splitlines()):
        out.append("" if in_fence else CODESPAN.sub("", line))
    return "\n".join(out)


for p in MD:
    text = strip_code(p.read_text(encoding="utf-8", errors="replace"))
    for m in LINK.finditer(text):
        t = m.group(1)
        if t.startswith(("http", "mailto:", "#")):
            continue
        target = (p.parent / t.split("#")[0]).resolve()
        if not target.exists():
            errors.append(f"BROKEN LINK {p.relative_to(ROOT)} -> {t}")

idre = re.compile(r"^(?:\d+\.)+\d+-")
seen = {}
for p in MD:
    if idre.match(p.name):
        if p.name in seen:
            errors.append(f"DUPLICATE ID {p.name}: {seen[p.name]} & {p.relative_to(ROOT)}")
        seen[p.name] = str(p.relative_to(ROOT))

if not links_only:
    fam = {}
    for p in MD:
        m2 = re.match(r"^((?:\d+\.)*)(\d+)\.(\d+)-", p.name)
        if not m2 or p.name == "INDEX.md":
            continue
        prefix = (m2.group(1) or "") + m2.group(2)
        key = (str(p.parent), prefix)
        fam.setdefault(key, []).append(int(m2.group(3)))
    for (d, pref), nums in sorted(fam.items()):
        exp = list(range(1, len(nums) + 1))
        if sorted(nums) != exp:
            errors.append(f"GAPS {d} prefix {pref}.x: has {sorted(nums)} expected 1..{len(nums)}")

# Flat stacks end with their interview bank. Repo convention (AGENTS.md:
# "interview-questions files always last") is observable as: every flat stack
# (NN.N-slug/ holding files directly, no NN-category subfolders) carries at
# least one *-interview-questions.md. Category stacks instead carry a single
# bank in a dedicated final interview category — enforced here only for the
# flat case, which is where drift happened (40.9, 40.11 gained concept
# chapters but no bank; 40.12 had one).
#
# Deliberate exemptions (the stack IS interview material already):
#   70.1-behavioral  — behavioral stories and question drills
#   70.3-cheatsheets — cheat-sheet genre, not a question bank
STACK_RX = re.compile(r"^\d{2}\.\d{1,2}-")
CAT_RX = re.compile(r"^\d{2}-")
BANK_RX = re.compile(r"\d+(\.\d+)*-interview-questions\.md$")
BANK_EXEMPT = {
    "70.1",  # behavioral stories/drills — already interview material
    "70.3",  # cheat sheets — a different prep genre
}
for top in sorted(ROOT.iterdir()):
    if not top.is_dir() or top.name.startswith((".", "_")):
        continue
    for stack in sorted(top.iterdir()):
        if not stack.is_dir() or not STACK_RX.match(stack.name):
            continue
        entries = list(stack.iterdir())
        if any(e.is_dir() and CAT_RX.match(e.name) for e in entries):
            continue  # category stack: bank lives in its own final category
        mds = [
            e.name
            for e in entries
            if e.is_file() and e.suffix == ".md" and e.name not in {"INDEX.md", "README.md"}
        ]
        if not mds:
            continue
        stack_id = stack.name.split("-")[0]
        if stack_id in BANK_EXEMPT:
            continue
        if not any(BANK_RX.search(n) for n in mds):
            errors.append(
                f"MISSING BANK {stack.relative_to(ROOT)}: flat stack has no "
                f"*-interview-questions.md (repo convention: banks last in every stack)"
            )

# Heading outline: no two H2 sections in one file may share a slug. A duplicate
# means two identically-named entries in the outline and an ambiguous anchor,
# and it is the tell that repeated sub-structures were written as *siblings*
# instead of nested under the section they belong to — 80.12 presented 13
# stories as 65 sibling H2s with no story titles at all, and 81.05 declared
# "Segment Tree" twice in a row while mixing topic titles with their own
# subsections. Repeats belong at ### or deeper, where the same label under a
# different parent is legitimate (per-story Situation/Task/Action/Result).
#
# One H1 per document is gated below: the title IS the document, and the
# legacy `# Phase N:` / `# Wave N:` document-stubs (81.01–81.04, the outreach
# playbook) buried it under competing H1s and flattened the outline. That
# normalization was done in one deliberate pass (2026-09); the rule is now
# enforced so the shape cannot return.
H2 = re.compile(r"^##\s+(.*\S)\s*$", re.M)


def gh_slug(text: str) -> str:
    """GitHub-style heading slug (mirrors check_links.py)."""
    s = re.sub(r"`([^`]*)`", r"\1", text.lower())
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s_]+", "-", s).strip("-")


for p in MD:
    text = strip_code(p.read_text(encoding="utf-8", errors="replace"))
    counts = {}
    for m in H2.finditer(text):
        slug = gh_slug(m.group(1))
        if slug:
            counts[slug] = counts.get(slug, 0) + 1
    dups = sorted(s for s, n in counts.items() if n > 1)
    if dups:
        errors.append(
            f"DUPLICATE H2 {p.relative_to(ROOT)}: {', '.join(dups)} "
            f"(section names must be unique — nest repeats as ###)"
        )

# Exactly one H1 per document. Exempt: Jekyll front-matter pages (search.md
# has no heading at all — the layout supplies the title).
H1 = re.compile(r"^# \S", re.M)
for p in MD:
    text = p.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        continue
    n_h1 = len(H1.findall(strip_code(text)))
    if n_h1 != 1:
        errors.append(
            f"H1 COUNT {p.relative_to(ROOT)}: {n_h1} H1s (expected exactly 1 — "
            f"one title H1; demote section stubs like `# Phase N:` to ##)"
        )

# INDEX completeness: an INDEX.md must link every numbered subdirectory that has
# its own INDEX.md (root INDEX -> lanes, lane INDEX -> stacks, stack INDEX ->
# categories). Prevents invisible sub-stacks — the 20.9-class omission where a
# computed count said one thing and the navigation said less. A link counts if
# it targets the subdir itself, anything directly inside it (its INDEX.md, a
# chapter, a deep page), or the subdir with an anchor.
for p in MD:
    if p.name != "INDEX.md":
        continue
    if p.parent != ROOT and not re.match(r"\d", p.parent.name):
        continue
    linked = set()
    for m in LINK.finditer(strip_code(p.read_text(encoding="utf-8", errors="replace"))):
        t = m.group(1)
        if t.startswith(("http", "mailto:", "#")):
            continue
        linked.add((p.parent / t.split("#")[0]).resolve())
    for sub in sorted(p.parent.iterdir()):
        if not (sub.is_dir() and re.match(r"\d", sub.name) and (sub / "INDEX.md").exists()):
            continue
        sub_res = sub.resolve()
        if sub_res not in linked and not any(t.parent == sub_res for t in linked):
            errors.append(
                f"INDEX GAP {p.relative_to(ROOT)}: numbered subdir {sub.name}/ has an "
                f"INDEX.md but is not linked from this INDEX (invisible sub-stack)"
            )

# Doc reachability: every doc under docs/ (excluding superpowers/ planning
# material) must be reachable from an entry point — README.md, the root
# INDEX, contributing.md, any lane/stack INDEX, or another reachable doc.
# The first-visitor pass found 7 of 10 docs linked from nowhere outside the
# folder; invisible docs are the documentation equivalent of the invisible
# sub-stack defect, so this is enforced rather than re-scanned by hand.
SKIP_DOCS = ROOT / "docs" / "superpowers"
ENTRY_POINTS = [ROOT / "README.md", ROOT / "INDEX.md", ROOT / "contributing.md"]
ENTRY_POINTS += [p for p in MD if ("/INDEX.md" in str(p) and "docs" not in p.relative_to(ROOT).parts)]
REACHABLE = set()
queue = [p for p in ENTRY_POINTS if p.exists()]
while queue:
    cur = queue.pop()
    if cur in REACHABLE or SKIP_DOCS in cur.parents:
        continue
    REACHABLE.add(cur)
    cur_text = strip_code(cur.read_text(encoding="utf-8", errors="replace"))
    for m in LINK.finditer(cur_text):
        t = m.group(1)
        if t.startswith(("http", "mailto:", "#")):
            continue
        target = (cur.parent / t.split("#")[0]).resolve()
        if target.exists() and target.suffix == ".md":
            queue.append(target)
for p in MD:
    rp = p.relative_to(ROOT)
    if str(rp).startswith("docs/") and not str(rp).startswith("docs/superpowers/") and p not in REACHABLE:
        errors.append(
            f"ORPHAN DOC {rp}: not reachable from README/INDEX/contributing or any "
            f"INDEX — link it from an entry point (invisible documentation)"
        )

print("\n".join(errors) if errors else f"OK: {len(MD)} md files checked")
sys.exit(1 if errors else 0)
