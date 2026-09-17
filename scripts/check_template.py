#!/usr/bin/env python3
"""Template-compliance gate for concept chapters.

Contributing.md defines the chapter template; the audits normalized the
whole corpus to it. This gate keeps it that way:

  - Concept files must carry the required `##` sections (Definition,
    First Principles, Summary, See Also, References & Learn More) —
    plus Code Examples for full concept files.
  - Sections that appear must appear in canonical order (a Why It
    Matters after Summary reads as damage, not style).
  - Interview-questions files (per repo convention, last in every
    category) carry a lighter contract: TL;DR, First Principles,
    Summary, See Also, References — and must not carry a
    `## Code Examples` heading (there it is a mislabeled Q&A block).
  - Design case studies (`NN.N-system-design/NN-case-studies/`) follow
    the case-study template (Requirements -> Capacity -> API -> data
    model -> architecture -> trade-offs): a domain-driven shape where a
    generic Definition would only duplicate the TL;DR. They require the
    cross-reference contract instead (TL;DR, Summary, See Also,
    References). Documented in contributing.md.

Known TL;DR styles: the corpus uses both a `## TL;DR` section (328
files) and an opening `> **TL;DR:** …` blockquote (129 files), so either
satisfies the requirement.

Known-variant headings (e.g. `## Why It Matters (TL;DR)`) are
normalized before matching. Files under personal/ and .archive are
skipped; INDEX.md files have their own conventions, and role-guide files
(multiple `# Phase`/`# Part` H1 sections) are exempt.

This gate supersedes `check_required_sections.py`, which checked only
Summary/See Also/References plus the interview Code-Examples rule; that
subset is enforced here as part of the full template, so the repo has
exactly one template gate.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal'}
# Campaign/project docs are not concept chapters; they have their own
# conventions (the First Principles gate covers them separately).
# `docs/` holds project meta (changelogs, reports, plans, specs) that
# describe work rather than teach a topic — not chapter-shaped.
EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang', 'projects', 'docs')

# --- File metadata (contributing.md "File Metadata" section) ---------------
# Every content file must begin with the HTML comment plus the four shields
# badges (Section, Category, Tags, Read time). The Read-time badge *value*
# is not checked here — read_time.py gate 13 owns value consistency; this
# gate owns presence, placement and order.
META_COMMENT = re.compile(r'^<!--\s*(section:.*?)\s*-->', re.M)
BADGE_RX = re.compile(
    r'^\[\!\[(Section|Category|Tags|Read time)\]\(https://img\.shields\.io/', re.M)
BADGE_ORDER = ('Section', 'Category', 'Tags', 'Read time')
VALID_CATEGORIES = {
    'Core', 'Frontend', 'Backend', 'API', 'Data', 'Architecture', 'DevOps',
    'Observability', 'Tooling', 'Quality', 'Real-Time', 'Interview',
    'Reference', 'Execution',
}


def parse_meta(text):
    """Field-aware parse of the meta comment.

    The comment is `k: v` pairs separated by `|` (values may themselves be
    scanned oddly if parsed positionally — e.g. an optional `subcategory:`
    field after category). Splitting on `|` then on the first `:` keeps
    each field clean.
    """
    m = META_COMMENT.search(text)
    if not m:
        return None
    fields = {}
    for part in m.group(1).split('|'):
        if ':' in part:
            k, v = part.split(':', 1)
            fields[k.strip()] = v.strip()
    return fields

# Canonical order (only checked for the sections a file actually has;
# files may legitimately omit optional sections like How It Works)
# The corpus carries two documented Definition orders — Why-first (older
# stacks) and Definition-first (newer) — both accepted (contributing.md
# only mandates TL;DR -> Definition).
CANON_A = [
    'TL;DR',
    'First Principles',
    'Why It Matters',
    'Definition',
    'How It Works',
    'Code Examples',
    'Real-World Use Cases',
    'Common Mistakes',
    'Best Practices',
    'Performance Considerations',
    'Summary',
    'Cheat Sheet',
    'See Also',
    'References & Learn More',
]

CANON_B = [
    'TL;DR',
    'First Principles',
    'Definition',
    'Why It Matters',
    'How It Works',
    'Code Examples',
    'Real-World Use Cases',
    'Common Mistakes',
    'Best Practices',
    'Performance Considerations',
    'Summary',
    'Cheat Sheet',
    'See Also',
    'References & Learn More',
]
CANONS = (CANON_A, CANON_B)

# Normalize heading variants to canonical names
VARIANTS = {
    'why it matters (tldr)': 'Why It Matters',
    'why it matters (tl;dr)': 'Why It Matters',
    'why do we need it?': 'Why It Matters',
    'why it matters': 'Why It Matters',
    'references & learn more': 'References & Learn More',
    'references': 'References & Learn More',
    'real-world case studies': 'Real-World Use Cases',
    'real-world use cases': 'Real-World Use Cases',
    'use cases': 'Real-World Use Cases',
    'common pitfalls': 'Common Mistakes',
    'common mistakes': 'Common Mistakes',
    'best practices': 'Best Practices',
    'summary': 'Summary',
    'tl;dr': 'TL;DR',
    'first principles': 'First Principles',
    'definition': 'Definition',
    'how it works': 'How It Works',
    'code examples': 'Code Examples',
    'code examples (javascript)': 'Code Examples',
    'cheat sheet': 'Cheat Sheet',
    'see also': 'See Also',
}

# TL;DR is the chapter template's *first* section (AGENTS.md): a concept file
# that never states its main point forces the reader to derive it from the
# body. Both documented forms (a `## TL;DR` section or an opening
# `> **TL;DR:** …` blockquote) satisfy it — see normalisation below.
REQUIRED_CONCEPT = {'TL;DR', 'First Principles', 'Definition', 'Summary', 'See Also', 'References & Learn More'}
REQUIRED_INTERVIEW = {'TL;DR', 'First Principles', 'Summary', 'See Also', 'References & Learn More'}
# Design case studies: domain-driven template, cross-reference contract only.
REQUIRED_CASE_STUDY = {'TL;DR', 'Summary', 'See Also', 'References & Learn More'}

FENCE = re.compile(r'^\s*(```|~~~)')
HEAD = re.compile(r'^## (.+?)\s*$')
# Blockquote TL;DR style: `> **TL;DR:** …` (or bolded without the quote)
TLDR_BQ = re.compile(r'^\s*>?\s*\*\*TL;?DR:?\*\*', re.I)


def normalize(name: str) -> str:
    name = name.strip()
    return VARIANTS.get(name.lower(), name)


def is_interview_file(path: str) -> bool:
    return 'interview' in os.path.basename(path).lower()


def is_guide_file(text: str) -> bool:
    """Role-guide convention (contributing.md): multiple `# Phase`/`# Part`
    H1 sections instead of the chapter template. Fence-aware: `# Phase 2`
    style comments inside code blocks are shell comments, not headings."""
    in_fence = False
    phase = 0
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith('# ') and (line[2:].lstrip().startswith('Phase')
                                      or line[2:].lstrip().startswith('Part')):
            phase += 1
    return phase >= 2


def is_case_study(path: str) -> bool:
    """System-design case studies use the Requirements->Capacity->API
    ->architecture template instead of the generic concept template."""
    parts = path.replace(os.sep, '/').split('/')
    return any('case-studies' in p for p in parts)


def is_reference_file(path: str) -> bool:
    """Cheat sheets / trackers / banks: reference genre, not concept chapters."""
    name = os.path.basename(path).lower()
    return ('cheat' in name) or ('reference' in name) or ('tracker' in name) or ('bank' in name)


def iter_md():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, ROOT)
        if rel.startswith(EXEMPT_PREFIXES):
            continue
        if 'personal' in rel.split(os.sep):
            continue
        for f in files:
            if f.endswith('.md') and f not in ('INDEX.md', 'README.md', 'AGENTS.md', 'contributing.md', 'ROADMAP.md', 'search.md'):
                yield os.path.join(root, f)


def check_metadata(text: str):
    """contributing.md: every content file begins with the meta comment and
    the four badges, comment at the top, badges under it before the title."""
    problems = []
    fields = parse_meta(text)
    if fields is None:
        problems.append("metadata: missing `<!-- section: ... | category: ... | tags: ... -->` comment")
    else:
        # Allow the documented {% raw %} line above the comment.
        m = META_COMMENT.search(text)
        if m.start() > 20:
            problems.append("metadata: comment not at file top (only {% raw %} may precede it)")
        cat = fields.get('category', '')
        if cat not in VALID_CATEGORIES:
            problems.append(f"metadata: non-canonical category {cat!r} "
                            f"(contributing.md's 14 only)")
        if not fields.get('section'):
            problems.append("metadata: empty section value")
        if not fields.get('tags'):
            problems.append("metadata: empty tags value")
    # Header zone: everything before the first real H1 title.
    title = re.search(r'^# (?!#)\S', text, re.M)
    header = text[:title.start()] if title else text[:3000]
    found = BADGE_RX.findall(header)
    missing = [b for b in BADGE_ORDER if b not in found]
    if missing:
        problems.append(f"metadata: missing badge(s) in header: {missing}")
    # Order: the badges that exist must appear in canonical order.
    ranks = [BADGE_ORDER.index(b) for b in found]
    if ranks != sorted(ranks):
        problems.append(f"metadata: badges out of order (got {found})")
    return problems


def check(path: str):
    """Return list of problem strings for one file."""
    problems = []
    text = open(path, encoding='utf-8').read()
    # Metadata applies to every genre, guides included (contributing.md rule).
    problems += check_metadata(text)
    if is_guide_file(text):
        return problems
    in_fence = False
    heads = []
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEAD.match(line)
        if m:
            heads.append(normalize(m.group(1)))

    has_blockquote_tldr = any(
        TLDR_BQ.match(l) for l in text.splitlines()
    )
    file_heads = set(heads)
    if has_blockquote_tldr:
        file_heads.add('TL;DR')

    if is_interview_file(path):
        req = REQUIRED_INTERVIEW
    elif is_case_study(path):
        req = REQUIRED_CASE_STUDY
    elif is_reference_file(path):
        # reference genre: TL;DR + Summary + See Also + References, no Definition/FP mandate
        req = {'Summary', 'See Also', 'References & Learn More'}
    else:
        req = REQUIRED_CONCEPT
    missing = req - file_heads
    if missing:
        problems.append(f"missing required sections: {sorted(missing)}")

    # Interview banks must not carry `## Code Examples`: that heading there is
    # a mislabeled Q&A block (Sept 2026 audit rule, inherited from
    # check_required_sections.py).
    if is_interview_file(path) and 'Code Examples' in file_heads:
        problems.append("interview bank has a `## Code Examples` heading "
                        "(rename to `## Interview Questions`)")

    # order check: accept any of the canonical orders, on the subset present
    sub = [h for h in heads if h in CANON_A]
    ok = False
    for canon in CANONS:
        sub_idx = [canon.index(h) for h in sub]
        if sub_idx == sorted(sub_idx):
            ok = True
            break
    if not ok:
        problems.append("sections out of canonical order")

    return problems


def main() -> int:
    bad = 0
    for path in iter_md():
        rel = os.path.relpath(path, ROOT)
        problems = check(path)
        if problems:
            bad += 1
            print(f"{rel}")
            for p in problems:
                print(f"    - {p}")
    if bad:
        print(f"\nTEMPLATE VIOLATIONS: {bad} file(s)")
        return 1
    print("template compliance OK")
    return 0


if __name__ == '__main__':
    sys.exit(main())
