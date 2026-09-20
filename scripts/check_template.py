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
# Same badge line, but capturing the link *target* as well. contributing.md
# ("File Metadata") says badges in content files link to `#`; only INDEX/README
# badges point at the central INDEX. This gate walks content files only, so `#`
# is the sole valid target — twelve recently authored chapters had drifted to
# `INDEX.md` / `../../INDEX.md` because only presence and order were checked.
BADGE_TARGET_RX = re.compile(
    r'^\[\!\[(Section|Category|Tags|Read time)\]\(https://img\.shields\.io/[^)]*\)\]'
    r'\(([^)]*)\)[ \t]*$', re.M)
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

# --- Interview-bank question-count claims (2026-09-19) ----------------------
# A bank's opening blockquote / TL;DR states how many questions it holds;
# the count must match the question markers actually present. 20.13.06
# claimed "30 questions" and held 20 — its own Summary advertised a Spring
# section the bank stopped short of writing. Only overpromises fire (an
# underclaim like "the first 20 of 50" is legitimate framing), and claims
# are read ONLY from the intro blockquote and the TL;DR body, so per-section
# subtotals ("Beginner (10 Questions)") can never fire.
QMARK = re.compile(
    r'^\s*(?:\*\*Q\d+|#{2,4}\s+(?:Q\d+|Question\s+\d+|\d+\.))')
WORDNUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
    'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100,
}
CLAIM_DIGIT = re.compile(r'\b(\d{1,3})\+?\s+(?:\w+\s+){0,2}?questions\b', re.I)
CLAIM_WORD = re.compile(
    r'\b(' + '|'.join(WORDNUM) + r')\s+(?:\w+\s+){0,2}?questions\b', re.I)

# --- Interview-bank question floor (2026-09-20) ------------------------------
# Every bank in the corpus was completed to 25 questions (the standard the
# bank-completion rounds established); the claim-vs-actual check above only
# catches OVER-promising, so a thin bank passed silently. The floor makes the
# standard enforceable. Exemptions are by name with a reason — same pattern
# as the advisory-workflow map — because a bank whose FORMAT predates the
# counted markers is not thin, and forcing the floor there demands a
# mechanical reformat for no content gain.
MIN_BANK_QUESTIONS = 25
BANK_FLOOR_EXEMPTIONS = {
    # 10 counted deep-dives + a 50-item rapid-fire section in the older
    # `1. **question**` list format the QMARK regex does not count.
    '20-backend/20.3-rest-apis/05-interview-drills/20.3.5.01-interview-questions.md':
        'mixed format: 10 counted deep-dives plus 50 rapid-fire items in the '
        'older list format',
}


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
    # Targets: contributing.md — content-file badges must link to `#`.
    for name, target in BADGE_TARGET_RX.findall(header):
        if target != '#':
            problems.append(f"metadata: {name} badge links to {target!r}, "
                            f"expected '#' (contributing.md 'File Metadata')")
    return problems


# An empty section is a heading immediately followed by another heading at the
# SAME or shallower level: nothing belongs to it, so it renders as a dead entry
# in the document outline and its apparent children sit beside it instead of
# under it. The subtlety that made this worth gating carefully: a heading
# followed by a DEEPER heading is completely normal — it is how every
# `## How It Works` opens its subsections — so a naive "heading followed by a
# heading" test fires on 1765 legitimate places. Only same-or-shallower counts.
HEAD_ANY = re.compile(r'^(#{2,6}) (.+?)\s*$')


def empty_sections(text):
    """-> list of (lineno, level, title) for headings with no content."""
    lines = text.split('\n')
    in_fence = False
    heads = []
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEAD_ANY.match(line)
        if m:
            heads.append((i + 1, len(m.group(1)), m.group(2)))
    issues = []
    for k in range(len(heads) - 1):
        ln, lvl, title = heads[k]
        nxt, nlvl, _ = heads[k + 1]
        if nlvl <= lvl and not [x for x in lines[ln:nxt - 1] if x.strip()]:
            issues.append((ln, lvl, title))
    return issues


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
    q_lines = set()
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEAD.match(line)
        if m:
            heads.append(normalize(m.group(1)))
        if QMARK.match(line):
            q_lines.add(line.strip())

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

    # Interview banks must not promise more questions than they hold. See the
    # QMARK/CLAIM block comment above for scope and history. Banks with < 5
    # detected markers are skipped: that means a numbering format the markers
    # miss, not a thin bank — wire the format into QMARK first.
    if is_interview_file(path) and len(q_lines) >= 5:
        lines = text.splitlines()
        claim_regions = [l for l in lines[:15] if l.lstrip().startswith('>')]
        in_tldr = False
        for l in lines:
            hm = HEAD.match(l)
            if hm:
                if in_tldr:
                    break
                in_tldr = normalize(hm.group(1)) == 'TL;DR'
                continue
            if in_tldr:
                claim_regions.append(l)
        claims = []
        for l in claim_regions:
            claims += [(int(m.group(1)), m.group(0)) for m in CLAIM_DIGIT.finditer(l)]
            claims += [(WORDNUM[m.group(1).lower()], m.group(0)) for m in CLAIM_WORD.finditer(l)]
        over = [c for c in claims if c[0] > len(q_lines)]
        if over:
            worst = max(over)
            problems.append(
                f"question-count claim '{worst[1]}' exceeds the {len(q_lines)} "
                f"questions present — the opening/TL;DR must not promise more "
                f"than the bank holds (add the section or fix the number)")

        rel_path = os.path.relpath(path, ROOT)
        if (len(q_lines) < MIN_BANK_QUESTIONS
                and rel_path not in BANK_FLOOR_EXEMPTIONS):
            problems.append(
                f"bank holds {len(q_lines)} questions — the corpus floor is "
                f"{MIN_BANK_QUESTIONS} (complete the bank to the standard, or "
                f"add the path to BANK_FLOOR_EXEMPTIONS with a reason if its "
                f"format predates the counted markers)")

    # order check: accept any of the canonical orders, on the subset present
    # Empty sections (a heading with nothing under it at its own level).
    for lineno, lvl, title in empty_sections(text):
        problems.append(f"empty section at line {lineno}: '{'#' * lvl} {title}' has no "
                        f"content and no deeper heading beneath it (give it content, "
                        f"or fold it into the section it labels)")

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
