#!/usr/bin/env python3
"""Template-compliance gate for teaching chapters and revision companions.

Concepts introduce Definition, then First Principles and mechanisms, and end
with Summary, See Also and References. TL;DR is retired. Retrieval practice
lives in the section's separate REVISION.md, not inside a learning chapter.
Interview banks and domain-shaped case studies retain their lighter contracts.
Metadata, fence grammar, raw wrappers and interview depth/count rules remain
part of this gate. INDEX, operational and personal documents have their own
conventions.
"""
import os
import re
import sys
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
from scan_scope import guard

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

# 2026-10-01 reading-flow revision: define the concept before deriving it,
# teach each mechanism once, and keep retrieval practice in a companion file.
# Noncanonical domain headings may intervene without flattening their outline.
CANON_A = [
    'Definition',
    'First Principles',
    'Why It Matters',
    'How It Works',
    'Code Examples',
    'Real-World Use Cases',
    'Common Mistakes',
    'Best Practices',
    'Performance Considerations',
    'Summary',
    'See Also',
    'References & Learn More',
]

CANON_B = [
    'Definition',
    'First Principles',
    'Why It Matters',
    'How It Works',
    'Code Examples',
    'Real-World Use Cases',
    'Common Mistakes',
    'Best Practices',
    'Performance Considerations',
    'Summary',
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
    'revision questions': 'Revision Questions',
    'revision question': 'Revision Questions',
    'review questions': 'Revision Questions',
    'see also': 'See Also',
}

# Required teaching sections. The definition serves as the single opening
# overview; the final summary is the only recap in the learning chapter.
REQUIRED_CONCEPT = {'First Principles', 'Definition', 'Summary', 'See Also', 'References & Learn More'}
REQUIRED_INTERVIEW = {'First Principles', 'Summary', 'See Also', 'References & Learn More'}
# Design case studies: domain-driven template, cross-reference contract only.
REQUIRED_CASE_STUDY = {'Summary', 'See Also', 'References & Learn More'}

FENCE = re.compile(r'^\s*(```|~~~)')
FENCE_FULL = re.compile(r'^\s*(`{3,}|~{3,})(.*)$')
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
    phase = 0
    for _, line, in_fence, _ in md_fences.walk(text.splitlines()):
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
    return ('cheat' in name) or ('reference' in name) or ('tracker' in name) or ('bank' in name) or name == 'revision.md'


def check_revision_companion(path: str, text: str):
    """Practice must cover the actual learning chapters, not just exist."""
    problems = []
    rows = [line for _, line, fenced, delimiter in md_fences.walk(text.splitlines())
            if not fenced and not delimiter]
    prose = '\n'.join(rows)
    questions = len(re.findall(r'\*\*Q:\*\*', prose))
    answers = len(re.findall(r'\*\*A:\*\*', prose))
    if questions < 5 or answers != questions:
        problems.append('revision companion needs at least five matched **Q:**/**A:** pairs')
    parent = os.path.dirname(path)
    for name in os.listdir(parent):
        sibling = os.path.join(parent, name)
        if (not name.endswith('.md') or name in {'INDEX.md', 'README.md', 'REVISION.md'}
                or is_interview_file(sibling) or is_reference_file(sibling)):
            continue
        sibling_text = open(sibling, encoding='utf-8').read()
        if is_guide_file(sibling_text):
            continue
        groups = re.split(r'^## ', prose, flags=re.M)
        linked_group = [g for g in groups if re.search(
            r'^Source:\s*\[[^\]]+\]\(' + re.escape(name) + r'(?:#[^)]*)?\)', g, re.M)]
        if not any('**Q:**' in g and '**A:**' in g for g in linked_group):
            problems.append(f'revision companion lacks a source-linked question group for {name}')
    return problems


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


def iter_rendered_md():
    """Public Markdown grammar, including operational docs and INDEXes.

    The teaching template is narrower; broken fences also damage reference
    and process documents. Personal data has its own private document format.
    """
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, ROOT)
        if 'personal' in rel.split(os.sep):
            continue
        for f in files:
            if f.endswith('.md'):
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
    tag_badge = re.search(r'\[!\[Tags\]\(https://img\.shields\.io/badge/tags-(.+)-lightgrey\)\]', header)
    if fields and tag_badge:
        badge_tags = unquote(tag_badge.group(1)).replace('--', '-').replace(' · ', ', ')
        comment_tags = fields.get('tags', '')
        if {t.strip().lower() for t in comment_tags.split(',')} != {t.strip().lower() for t in badge_tags.split(',')}:
            problems.append('metadata: comment tags disagree with the Tags badge (check for truncated values)')
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
    heads = []
    for i, line, in_fence, _ in md_fences.walk(lines):
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


# A Cheat Sheet whose fence body is essentially only its title bar is the
# generator-gap sibling of the empty fence: the sheet was added but the
# content generation failed (30.2.2.20 distributed counter, found 2026-09-21
# during the Jul–Aug bulk-pass sweep). Exempt by name: README.md's sheet is
# a deliberate placeholder.
THIN_SHEET_MIN_LINES = 5
THIN_SHEET_EXEMPT = {'readme.md'}


def thin_sheets(text):
    """-> [(lineno, content_lines)] for cheat sheets under the floor."""
    lines = text.split('\n')
    heads = [(i, m.group(2)) for i, line, in_fence, _ in md_fences.walk(lines)
             if not in_fence and (m := HEAD_ANY.match(line)) and m.group(2).strip() == 'Cheat Sheet']
    issues = []
    for k, (i, _title) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        events = list(md_fences.walk(lines[i:end]))
        openers = [j for j, l, inf, isf in events if isf and inf]
        closes = {j for j, l, inf, isf in events if isf and not inf}
        # Calibrated (13 false fires on first cut): only the FIRST fence —
        # the sheet proper — carries the floor. Later small fences in the
        # section are legitimate supplementary blocks (complexity tables,
        # mini-diagrams) that a floor would punish.
        op = openers[0] if openers else None
        if op is None:
            continue
        cl = next((c for c in sorted(closes) if c > op), None)
        if cl is None:
            continue
        content = sum(1 for j in range(op + 1, cl) if lines[i + j].strip())
        if content < THIN_SHEET_MIN_LINES:
            issues.append((i + op + 1, content))
    return issues


def fence_problems(text: str):
    """CommonMark: a closing fence may not carry an info string, and only a
    bare fence of the SAME character at >= the opener's length closes a block.
    A labeled close (` ```yaml ` while a block is open) does NOT close —
    renderers merge everything up to the next bare fence, swallowing headings
    into the code block. 38 instances repo-wide (2026-09-20): labeled closes
    after yaml blocks, and one prose-glued close. Nested-fence documentation
    (a ``` line inside a ```` block) is correctly treated as content.

    Rule 3 (2026-09-21): an EMPTY fence — an opener immediately followed by
    a closer, with no content line between — renders as a blank code block
    and is the fingerprint of a stray delimiter from a broken tool pass.
    Found 24 times that day: a stray close+open pair had collapsed 24 cheat
    sheets, spilling failure tables and code outside their blocks. Blank
    lines between the delimiters do not count as content (a blank-only
    fence is the same defect one step removed)."""
    problems = []
    in_fence = False
    open_char, open_len = '', 0
    saw_content = False
    for lineno, line in enumerate(text.splitlines(), 1):
        m = FENCE_FULL.match(line)
        if not m:
            if in_fence and line.strip():
                saw_content = True
            continue
        marker, rest = m.group(1), m.group(2)
        if in_fence:
            if marker[0] == open_char and len(marker) >= open_len:
                if rest.strip():
                    problems.append(
                        f"line {lineno}: closing fence carries an info string — "
                        f"closing fences must be bare, or renderers merge the "
                        f"following content into the code block (strip the "
                        f"label, or move trailing prose to its own line)")
                    in_fence = False
                else:
                    if not saw_content:
                        problems.append(
                            f"line {lineno}: empty fence — an opener with no "
                            f"content line before its closer renders as a blank "
                            f"code block, the fingerprint of a stray delimiter "
                            f"from a broken tool pass (see the 24-file cheat-"
                            f"sheet repair of 2026-09-21). Remove the pair or "
                            f"restore the missing content")
                    in_fence = False
            else:
                # shorter/other-char fence lines inside a block are content
                saw_content = True
        else:
            in_fence = True
            open_char, open_len = marker[0], len(marker)
            saw_content = False
    if in_fence:
        problems.append('unclosed code fence at end of file; later prose renders as code')
    return problems


def check_raw_wrapper(text: str):
    """contributing.md: files containing Liquid-syntax collisions open with
    {% raw %} on line 1 and close with a matching endraw tag as the last
    non-empty line — exactly one closer, at EOF. Unclosed wrappers crash
    the Jekyll render ('raw tag was never closed'); a literal endraw in
    prose (this sentence is inside a raw block, so it must never contain
    one) terminates the block early and makes the rest of the file live
    Liquid — both classes shipped to CI before this check. A literal
    {% raw %} mention inside a wrapped file is inert to Liquid and legal
    (that is how the convention gets documented).
    Files WITHOUT raw must lack a stray closer."""
    problems = []
    lines = text.splitlines()
    has_raw = bool(lines) and lines[0].strip() == "{% raw %}"
    endraw_n = text.count("{% endraw %}")
    if not has_raw:
        if "{% raw %}" in text:
            problems.append("raw-wrap: {% raw %} found but not on line 1")
        if endraw_n:
            problems.append("raw-wrap: endraw closer without an opening raw tag")
        return problems
    if endraw_n != 1:
        problems.append(
            f"raw-wrap: expected exactly one endraw closer (at EOF), found {endraw_n}")
        return problems
    tail = [l for l in lines if l.strip()]
    if tail[-1].strip() != "{% endraw %}":
        problems.append(
            "raw-wrap: endraw closer is not the last non-empty line (block closes early)")
    return problems


def check(path: str):
    """Return list of problem strings for one file."""
    problems = []
    text = open(path, encoding='utf-8').read()
    # Metadata applies to every genre, guides included (contributing.md rule).
    problems += check_metadata(text)
    problems += check_raw_wrapper(text)
    if is_guide_file(text):
        return problems
    problems += fence_problems(text)
    heads = []
    q_lines = set()
    for _, line, in_fence, _ in md_fences.walk(text.splitlines()):
        if in_fence:
            continue
        m = HEAD.match(line)
        if m:
            heads.append(normalize(m.group(1)))
        if QMARK.match(line):
            q_lines.add(line.strip())

    has_blockquote_tldr = any(
        TLDR_BQ.match(l) for _, l, fenced, delimiter in md_fences.walk(text.splitlines())
        if not fenced and not delimiter
    )
    file_heads = set(heads)
    if has_blockquote_tldr:
        file_heads.add('TL;DR')

    if 'TL;DR' in file_heads:
        problems.append('retired TL;DR opening duplicates the definition; preserve unique facts in the relevant body section')
    if 'Cheat Sheet' in file_heads and not is_reference_file(path) and not is_interview_file(path):
        problems.append('retired in-chapter Cheat Sheet repeats the summary; keep one recap and link separate revision practice')
    if 'Revision Questions' in file_heads and os.path.basename(path) != 'REVISION.md':
        problems.append('revision questions belong in the separate section REVISION.md companion')

    if os.path.basename(path) == 'REVISION.md':
        problems += check_revision_companion(path, text)
    elif (not is_interview_file(path) and not is_reference_file(path)
          and os.path.exists(os.path.join(os.path.dirname(path), 'INDEX.md'))
          and not os.path.exists(os.path.join(os.path.dirname(path), 'REVISION.md'))):
        problems.append('learning section has no separate REVISION.md companion')

    if is_interview_file(path):
        req = REQUIRED_INTERVIEW
    elif is_case_study(path):
        req = REQUIRED_CASE_STUDY
    elif is_reference_file(path):
        # reference genre: Summary + See Also + References, no Definition/FP mandate
        req = {'Summary', 'See Also', 'References & Learn More'}
    else:
        req = REQUIRED_CONCEPT
    missing = req - file_heads
    if missing:
        problems.append(f"missing required sections: {sorted(missing)}")
    if 'Definition' in req and 'Definition' in file_heads:
        in_definition = False
        formal = []
        for _, line, fenced, delimiter in md_fences.walk(text.splitlines()):
            if fenced or delimiter:
                continue
            heading = HEAD.match(line)
            if heading:
                in_definition = normalize(heading.group(1)) == 'Definition'
            if in_definition and line.startswith('> **Textbook Definition:**'):
                formal.append(line.removeprefix('> **Textbook Definition:**').strip())
        if len(formal) != 1 or not formal[0]:
            problems.append('definition: include exactly one nonempty original Textbook Definition in the Definition section')

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

    # Title-only cheat sheets: the sheet exists but its content never did.
    if os.path.basename(path).lower() not in THIN_SHEET_EXEMPT:
        for lineno, content in thin_sheets(text):
            problems.append(
                f"line {lineno}: cheat sheet fence holds only {content} content "
                f"line(s) — a quick-reference that was never populated (write "
                f"the sheet from the chapter's own material)")

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
    n_files = 0
    for path in iter_md():
        n_files += 1
        rel = os.path.relpath(path, ROOT)
        problems = check(path)
        if problems:
            bad += 1
            print(f"{rel}")
            for p in problems:
                print(f"    - {p}")
    # Grammar on public Markdown beyond the teaching-template scope.
    for path in iter_rendered_md():
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding='utf-8').read()
        problems = check_raw_wrapper(text) + fence_problems(text)
        if problems:
            bad += 1
            print(f"{rel}")
            for p in problems:
                print(f"    - {p}")
    if bad:
        print(f"\nTEMPLATE VIOLATIONS: {bad} file(s)")
        return 1
    # A template gate that read no chapters certifies no templates (scan_scope).
    guard(n_files, 'markdown files')
    print(f"template compliance OK — {n_files} markdown files read")
    return 0


if __name__ == '__main__':
    sys.exit(main())
