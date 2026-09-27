#!/usr/bin/env python3
"""Check that every count claim in the repo matches live disk.

Why this gate is bigger than it used to be
------------------------------------------
Repo-scale numbers drifted repeatedly because nothing enforced them, so this
script was added to watch two files: the root INDEX footer and the 80-lane
scale row. Meanwhile the *rest* of the navigation surface carried its own
hand-maintained copies of the same numbers — README's footer and badge,
contributing.md, lanes/INDEX.md, the per-stack INDEX badges, the "Files"
column of every navigation table — and none of them were watched. By Sept
2026 they had drifted badly: README advertised "806 files / 345K lines"
against a live 851 / 361K, four stack INDEXes contradicted the computed
study-time line printed immediately above their own claim, and 15 of 158
`Files` badges disagreed with the folder they point at.

That last one is not a nitpick: the repo's own restructure spec
(`docs/superpowers/specs/2026-08-25-full-restructure-design.md`) lists
"badge counts == actual counts" as a completion criterion. It was never
automated, so it was never true for long.

The homepage hero button (`index.html`, "Search N Chapters") was one more
surface of the same kind — hard-coded since it shipped, with no writer to
restamp it when the corpus grew. It is owned here now (Sept 2026), on the
same chapter count README's search link uses.

Counting rule (one rule, applied per scope)
-------------------------------------------
  * repo total   — every `.md` in the tree, minus .git/node_modules/.archive
  * scope count  — `.md` files under that folder, excluding `INDEX.md` and
                   `README.md` and excluding the `personal/` data subtree
                   (personal campaign data is not study material)

The scope rule reproduces every number the corpus was built around: 121
frontend chapters, 143 backend, 36 abroad-lane docs, 22 FAANG-lane docs.

Usage:
  python3 scripts/check_counts.py            # report + exit 1 on drift
  python3 scripts/check_counts.py --write    # restamp every claim in place
  python3 scripts/check_counts.py --quiet

`--write` only ever replaces digits inside a claim; it never rewrites prose.
If a restamp changes the number of digits in a table cell, re-run
`python3 scripts/check_alignment.py --fix` to re-pad that column.
"""
import argparse
import os
import re
import sys

from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'.git', 'node_modules', '.archive', '.sass-cache'}
SKIP_NAMES = {'INDEX.md', 'README.md'}
PERSONAL = 'personal'

# read_time.py's scope: the 7 shared study stacks only. Used for the "550
# chapters" claim, so the two scripts cannot disagree about what a chapter is.
EXEMPT_TOP = {'80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang',
              'lanes', 'projects', 'docs'}
CONTENT_SKIP_NAMES = SKIP_NAMES | {'AGENTS.md', 'contributing.md',
                                   'ROADMAP.md', 'search.md'}

CHEAT_SHEET_HEAD = re.compile(r'^##+ Cheat Sheet\s*$', re.M)


# --------------------------------------------------------------------------
# live counts
# --------------------------------------------------------------------------

def walk_md(base, skip_personal=True):
    for root, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs
                         if d not in SKIP_DIRS
                         and not (skip_personal and d == PERSONAL))
        for f in sorted(files):
            if f.endswith('.md'):
                yield os.path.join(root, f)


def repo_totals():
    files = lines = 0
    for path in walk_md(ROOT, skip_personal=False):
        files += 1
        with open(path, encoding='utf-8') as fh:
            lines += fh.read().count('\n')
    return files, lines


def scope_chapters(subdir):
    """Files a reader studies in `subdir` (see counting rule above)."""
    base = os.path.join(ROOT, subdir)
    if not os.path.isdir(base):
        return None
    return sum(1 for p in walk_md(base)
               if os.path.basename(p) not in SKIP_NAMES)


def sub_stack_count(subdir):
    base = os.path.join(ROOT, subdir)
    return sum(1 for d in sorted(os.listdir(base))
               if os.path.isdir(os.path.join(base, d))
               and os.path.isfile(os.path.join(base, d, 'INDEX.md')))


def case_study_count():
    """Files in the system-design case-study folder (INDEX excluded)."""
    base = os.path.join(ROOT, '30-architecture', '30.2-system-design',
                        '02-case-studies')
    if not os.path.isdir(base):
        return 0
    return sum(1 for f in os.listdir(base)
               if f.endswith('.md') and f not in SKIP_NAMES)


def sd_subfolder_label():
    """The real subfolder names of 30.2-system-design, in roadmap style.

    ROADMAP's structure tree names these folders inline (`01-theory +
    02-case-studies`); they were restated from memory and had gone stale as
    `00-theory + 10-case-studies` long after the folders were renumbered.
    """
    base = os.path.join(ROOT, '30-architecture', '30.2-system-design')
    if not os.path.isdir(base):
        return ''
    subs = sorted(d for d in os.listdir(base)
                  if os.path.isdir(os.path.join(base, d))
                  and re.match(r'^\d\d-', d))
    return ' + '.join(subs)


def content_chapters():
    n = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs
                         if d not in SKIP_DIRS and d != PERSONAL)
        rel = os.path.relpath(root, ROOT).replace(os.sep, '/')
        if rel != '.' and rel.split('/')[0] in EXEMPT_TOP:
            continue
        n += sum(1 for f in files
                 if f.endswith('.md') and f not in CONTENT_SKIP_NAMES)
    return n


def interview_bank_count():
    return sum(1 for p in walk_md(ROOT, skip_personal=False)
               if p.endswith('-interview-questions.md'))


def api_totals():
    """Totals block of the live generated api/index.json (gate 14 byte-locks
    it to the corpus), so the api-contract example cannot drift from the real
    artifact. Empty when the file has not been generated yet."""
    import json
    p = os.path.join(ROOT, 'api', 'index.json')
    try:
        with open(p, encoding='utf-8') as fh:
            return json.load(fh).get('totals', {})
    except (OSError, ValueError):
        return {}


def freshness_rule_count():
    """Number of rules in check_freshness.py, read from the module itself so
    the doc claim IS the computation (a new rule bumps the count with zero
    doc edits)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'check_freshness', os.path.join(ROOT, 'scripts', 'check_freshness.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return len(mod.RULES)


def drill_class_counts():
    """(stale, review) class counts of drift_drill.py, read from the module's
    CLASSES table — the health report quotes these, and quoting from memory
    is how they drifted within an hour of being written."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'drift_drill', os.path.join(ROOT, 'scripts', 'drift_drill.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    stale = sum(1 for c in mod.CLASSES if c[1] == 'STALE')
    review = sum(1 for c in mod.CLASSES if c[1] == 'REVIEW')
    return stale, review


def cheat_sheet_formats():
    """Cheat Sheet sections that open with a fence vs. a table."""
    code = table = 0
    for path in walk_md(ROOT, skip_personal=False):
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        m = CHEAT_SHEET_HEAD.search(text)
        if not m:
            continue
        for line in text[m.end():].split('\n'):
            s = line.strip()
            if not s:
                continue
            if s.startswith('#'):
                break
            if s.startswith('```'):
                code += 1
            elif s.startswith('|'):
                table += 1
            break
    return code, table


def raw_tag_count():
    """Files that *open* with `{% raw %}` (the documented convention).

    Counting any mention of `{% raw %}` instead would also count the docs
    that describe the convention, making the claim self-referential: editing
    contributing.md's own sentence would bump its own number.
    """
    n = 0
    for path in walk_md(ROOT, skip_personal=False):
        with open(path, encoding='utf-8') as fh:
            for line in fh:
                s = line.strip()
                if not s:
                    continue
                if s == '{% raw %}':
                    n += 1
                break
    return n


# --------------------------------------------------------------------------
# claim rules
# --------------------------------------------------------------------------

def sub_groups(text, rx, values):
    """Replace the regex's capture groups with `values`, keeping the rest.

    Every other character of the match is preserved, so a rule can rewrite a
    number inside `"851 files, 361K lines"` without restating the quotes.
    """
    def rep(m):
        s, base = m.group(0), m.start(0)
        spans = [(m.start(i) - base, m.end(i) - base, str(v))
                 for i, v in enumerate(values, start=1)]
        for a, b, v in reversed(spans):
            s = s[:a] + v + s[b:]
        return s
    return rx.subn(rep, text)


def scale_edits(live):
    """(file, regex) pairs whose two groups are `N files` / `NK lines`."""
    total, k = live['repo_files'], live['repo_k']
    edits = [
        ('INDEX.md', r'(\d+) files, (\d+)K lines', [total, k]),
        ('README.md', r'(\d+) files · (\d+)K lines', [total, k]),
        ('80-lanes-abroad-full-stack/INDEX.md',
         r'(\d+) files, (\d+)K lines', [total, k]),
        ('contributing.md', r'(\d+) `\.md` files / (\d+)K lines',
         [total, k]),
        ('contributing.md', r'\("(\d+) files, (\d+)K lines"\)', [total, k]),
        ('docs/verification-gates.md', r'\("(\d+) files, (\d+)K lines"\)',
         [total, k]),
        # Bare repo-file claims that carry no line count.
        ('80-lanes-abroad-full-stack/INDEX.md',
         r'Covers all (\d+) files', [total]),
        ('README.md', r'search all (\d+) chapters', [live['content']]),
        # The homepage hero button advertises the same search index README's
        # link does; both read the one chapter count, so they cannot disagree.
        ('index.html', r'Search (\d+) Chapters', [live['content']]),
        ('README.md', r'\((\d+) across all stacks\)',
         [live['interview_banks']]),
        ('contributing.md', r'\((\d+) files use this today\)',
         [live['raw_tag']]),
        ('contributing.md', r'\*\*Code-block format\*\* \((\d+) files',
         [live['cheat_code']]),
        ('contributing.md', r'\*\*Table format\*\* \((\d+) files',
         [live['cheat_table']]),
        # Doc self-description: the gates page states the walker scope size.
        ('docs/verification-gates.md', r"today's (\d+) content files",
         [live['content']]),
        # Health-report live-state claims about the gate system itself,
        # sourced from the gate modules (a new rule restamps the docs).
        ('docs/2026-09-19-corpus-health-report.md',
         r'\*\*(\d+) rules\*\*, incl\. two date-gated',
         [live['freshness_rules']]),
        ('docs/2026-09-19-corpus-health-report.md',
         r'(\d+) freshness rules across two date-gated',
         [live['freshness_rules']]),
        ('docs/2026-09-19-corpus-health-report.md',
         r'(\d+) STALE classes that open a tracking issue, (\d+) REVIEW classes',
         [live['drill_stale'], live['drill_review']]),
    ]
    # The api-contract example block mirrors the shipped artifact's totals.
    api = live.get('api') or {}
    if api.get('chapters'):
        edits.append((
            'docs/api-contract.md',
            r'"chapters": (\d+), "sections": (\d+), "categories": (\d+),\s*'
            r'"read_minutes": (\d+)',
            [api.get('chapters'), api.get('sections'),
             api.get('categories'), api.get('read_minutes')]))
    return edits


def header_edits(live):
    """(file, regex, scope, subdir) for `### … (N files in M sub-stacks)`."""
    return [
        ('INDEX.md', r'^### 10-frontend — Frontend \((\d+) files in (\d+) sub-stacks\)$', '10-frontend'),
        ('INDEX.md', r'^### 20-backend — Backend \((\d+) files in (\d+) sub-stacks\)$', '20-backend'),
        ('INDEX.md', r'^### 30-architecture — Architecture \((\d+) files in (\d+) sub-stacks\)$', '30-architecture'),
        ('INDEX.md', r'^### Platform \((\d+) files in (\d+) sub-stacks\)$', '40-platform'),
        ('INDEX.md', r'^### Quality \((\d+) files in (\d+) sub-stacks\)$', '50-quality'),
        ('INDEX.md', r'^### Interview Toolkit \((\d+) files in (\d+) sub-stacks\)$', '70-interview-toolkit'),
        ('INDEX.md', r'^### Real-Time \((\d+) files\)$', '60-realtime'),
    ]


def roadmap_edits(live):
    """Structural claims in ROADMAP.md.

    ROADMAP is the primary navigation doc, so it restates structure the same
    way INDEXes do — case-study totals, sub-stack counts, folder names. Those
    claims were ungated and drifted (`Case studies ×20` against 31 on disk,
    `9 sub-stacks` against 10). Deriving them here keeps ROADMAP honest from
    the same computation as everything else.
    """
    return [
        ('ROADMAP.md', r'\[Case studies ×(\d+)\]', [live['case_studies']]),
        ('ROADMAP.md', r'└─ (\d+) case ', [live['case_studies']]),
        ('ROADMAP.md', r'20-backend/ ← (\d+) sub-stacks',
         [live['backend_substacks']]),
        ('ROADMAP.md', r'30\.2-system-design/ ([\d\-a-z]+ \+ [\d\-a-z]+)',
         [live['sd_subfolders']]),
    ]


def section_blurb_edits():
    """Counts in the root INDEX's per-section blurbs (it has no table)."""
    return [
        ('INDEX.md', r'^> (\d+) files\. Cross-lane', '00-strategy'),
    ]


REPO_SCOPE_BADGES = {'INDEX.md', 'README.md', 'lanes/INDEX.md'}

# The `> **N files** — description` blurb that opens every INDEX (see
# contributing.md's "INDEX.md Format"). It is the same claim as the Files
# badge, stated in prose, so it is held to the same number — and to the
# sub-stack/category count when the blurb spells that out too.
BLURB = re.compile(r'^> (\*{0,2})(\d+) files(?: across (\d+) (sub-stacks|categories))?',
                   re.M)


def fix_blurbs(rel, text):
    """Correct the `> **N files** ...` opening blurb of one INDEX."""
    if rel in REPO_SCOPE_BADGES or os.path.basename(rel) != 'INDEX.md':
        return text  # root/lanes INDEX blurbs belong to their sections
    sub = os.path.dirname(rel)
    want = scope_chapters(sub)
    if want is None:
        return text
    nsub = sub_stack_count(sub)

    def rep(m):
        bold, _num, across, word = m.groups()
        out = f'> {bold}{want} files'
        if across is not None:
            out += f' across {nsub} {word}'
        return out

    return BLURB.sub(rep, text)


def badge_edits(live, texts):
    """Every INDEX.md must carry a Files badge equal to its scope count."""
    problems = []
    for rel in sorted(texts):
        base = os.path.basename(rel)
        if base not in ('INDEX.md', 'README.md'):
            continue
        m = re.search(r'badge/files-(\d+)-', texts[rel])
        if m is None:
            if base == 'INDEX.md':
                problems.append((rel, None, expected_badge(rel, live)))
            continue
        want = expected_badge(rel, live)
        if want is None:
            continue
        if int(m.group(1)) != want:
            problems.append((rel, int(m.group(1)), want))
    return problems


def expected_badge(rel, live):
    if rel in REPO_SCOPE_BADGES:
        return live['repo_files']
    return scope_chapters(os.path.dirname(rel))


def table_edits(rel, text, live):
    """Fix the `Files` cell of any navigation table row that links a folder.

    Only tables whose header carries a `Files` cell next to a
    Stack/Sub-stack/Lane cell are touched — the "Study order cheat sheet" and
    "Lane vs Stack" tables use their integer columns for other things.
    """
    lines = text.split('\n')
    header = None
    changed = 0
    for i, line in enumerate(lines):
        if not line.startswith('|'):
            header = None
            continue
        raw_cells = line.strip().strip('|').split('|')
        if all(re.fullmatch(r'\s*:?-{2,}:?\s*', c) for c in raw_cells if c.strip()):
            continue  # separator row keeps the header mode
        low = [c.strip().lower() for c in raw_cells]
        if 'files' in low and ({'stack', 'sub-stack'} & set(low) or 'lane' in low):
            header = low
            continue
        if header is None:
            continue
        fi = header.index('files')
        if fi >= len(raw_cells) or not raw_cells[fi].strip().isdigit():
            continue
        target = None
        for c in raw_cells:
            m = re.search(r'\]\(([^)\s]+)\)', c)
            if m and (m.group(1).endswith('/INDEX.md')
                      or m.group(1).endswith('/')):
                target = m.group(1)
                break
        if target is None:
            continue
        sub = target[:-len('INDEX.md')].rstrip('/') if target.endswith('/INDEX.md') \
            else target.rstrip('/')
        sub = os.path.normpath(os.path.join(os.path.dirname(rel), sub))
        want = scope_chapters(sub)
        if want is None or int(raw_cells[fi].strip()) == want:
            continue
        # Replace only the digits, in place, to preserve column padding.
        pipes = [m.start() for m in re.finditer(r'\|', line)]
        a, b = pipes[fi] + 1, pipes[fi + 1]
        seg = line[a:b]
        lines[i] = line[:a] + re.sub(r'\d+', str(want), seg) + line[b:]
        changed += 1
    return '\n'.join(lines), changed


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def load(paths):
    texts = {}
    for rel in paths:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            with open(p, encoding='utf-8') as fh:
                texts[rel] = fh.read()
    return texts


def compute_live():
    repo_files, repo_lines = repo_totals()
    cheat_code, cheat_table = cheat_sheet_formats()
    return {
        'repo_files': repo_files,
        'repo_k': repo_lines // 1000,
        'content': content_chapters(),
        'interview_banks': interview_bank_count(),
        'raw_tag': raw_tag_count(),
        'cheat_code': cheat_code,
        'cheat_table': cheat_table,
        'case_studies': case_study_count(),
        'backend_substacks': sub_stack_count('20-backend'),
        'sd_subfolders': sd_subfolder_label(),
        'api': api_totals(),
        'freshness_rules': freshness_rule_count(),
        'drill_stale': drill_class_counts()[0],
        'drill_review': drill_class_counts()[1],
    }


def restamp(texts, live):
    """Return {rel: new_text} for every file whose claims are stale.

    `texts` is left untouched so the caller can diff old against new.
    """
    out, missing = {}, []
    old = dict(texts)
    texts = dict(texts)

    for rel, rx, values in scale_edits(live):
        if rel not in texts:
            continue
        new, n = sub_groups(texts[rel], re.compile(rx, re.M), values)
        if n == 0:
            missing.append((rel, rx))
        texts[rel] = new

    for rel, rx, subdir in header_edits(live):
        if rel not in texts:
            continue
        values = [scope_chapters(subdir), sub_stack_count(subdir)]
        rx_c = re.compile(rx, re.M)
        n_groups = rx_c.groups
        values = values[:n_groups]
        texts[rel], n = sub_groups(texts[rel], rx_c, values)
        if n == 0:
            missing.append((rel, rx))

    for rel, rx, values in roadmap_edits(live):
        if rel not in texts:
            continue
        texts[rel], n = sub_groups(texts[rel], re.compile(rx, re.M), values)
        if n == 0:
            missing.append((rel, rx))

    for rel, rx, subdir in section_blurb_edits():
        if rel not in texts:
            continue
        texts[rel], n = sub_groups(texts[rel], re.compile(rx, re.M),
                                   [scope_chapters(subdir)])
        if n == 0:
            missing.append((rel, rx))

    for rel in ('INDEX.md', 'README.md', 'lanes/INDEX.md'):
        if rel not in texts:
            continue
        texts[rel], _ = table_edits(rel, texts[rel], live)

    for rel, got, want in badge_edits(live, texts):
        if got is None:
            continue  # reported as a missing badge, nothing to restamp
        texts[rel] = re.sub(r'badge/files-\d+-', f'badge/files-{want}-',
                            texts[rel], count=1)

    # INDEX blurbs are diffed at the end like any other restamp.
    for rel in list(texts):
        texts[rel] = fix_blurbs(rel, texts[rel])

    for rel, new in texts.items():
        if new != old[rel]:
            out[rel] = new
    return out, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true',
                    help='restamp every claim in place')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    # Every INDEX/README plus the navigation surface that quotes repo totals —
    # the docs, and the homepage hero button's search-count claim.
    nav = []
    for p in walk_md(ROOT, skip_personal=False):
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel.startswith('docs/superpowers/'):
            continue  # historical design docs quote the numbers of their day
        if os.path.basename(rel) in ('INDEX.md', 'README.md'):
            nav.append(rel)
    nav += ['index.html', 'contributing.md', 'docs/verification-gates.md',
            'lanes/INDEX.md', 'ROADMAP.md', 'docs/api-contract.md',
            'docs/2026-09-19-corpus-health-report.md']
    texts = load(sorted(set(nav)))

    # A count gate that loaded no documents has verified no claims
    # (see scan_scope) — and compute_live() itself reads the corpus, so a
    # broken root used to die in a traceback instead of saying so plainly.
    guard(len(texts), 'navigation documents', ROOT)

    live = compute_live()
    changed, missing = restamp(texts, live)

    if args.write:
        for rel, new in changed.items():
            with open(os.path.join(ROOT, rel), 'w', encoding='utf-8') as fh:
                fh.write(new)
        print(f'restamped {len(changed)} file(s) to match live disk')
        for rel in sorted(changed):
            print(f'  {rel}')
        return 0

    if missing:
        print('count claims that could not be located (format changed?):')
        for rel, rx in missing:
            print(f'  {rel}: {rx}')
        print('\nFix the rule or restore the claim, then re-run.')

    badges = badge_edits(live, texts)
    if changed or badges or missing:
        print(f'COUNT DRIFT — {len(changed)} file(s) disagree with live disk')
        print(f'  live: {live["repo_files"]} files, {live["repo_k"]}K lines')
        for rel, got, want in badges:
            if got is None:
                print(f'  {rel}: MISSING Files badge (should be files-{want})')
            else:
                print(f'  {rel}: badge files-{got} → files-{want}')
        for rel in sorted(changed):
            for old_line, new_line in zip(texts[rel].split('\n'),
                                          changed[rel].split('\n')):
                if old_line != new_line:
                    print(f'  {rel}:  - {old_line.strip()}')
                    print(f'  {rel}:  + {new_line.strip()}')
        print('\nFix: python3 scripts/check_counts.py --write')
        return 1


    if not args.quiet:
        print(f'OK — {live["repo_files"]} files, {live["repo_k"]}K lines; '
              f'every Files badge, INDEX blurb, stack header, navigation-table '
              f'count and quoted total agrees with live disk '
              f'({live["content"]} study chapters, '
              f'{live["interview_banks"]} interview banks).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
