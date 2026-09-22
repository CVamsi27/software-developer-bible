#!/usr/bin/env bash
# One-command verification gate for the software-developer-bible repo.
# Runs all 28 checks in order; exits non-zero if any real failure is
# found. Known lane-80.x numbering GAPS are intentional (numbers owned by
# projects/docita prep docs) and reported as baseline noise, not failures.
# Gate labels are append-only (8b/8c arrived after 8), so the label order in
# this file is the gate order a reader should follow.
#
# Usage:  bash scripts/verify.sh        (from the repo root)
set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0

echo ""
echo "1/28  check_counts.py — every count claim vs live disk"
echo "     python3 scripts/check_counts.py   (--write restamps them)"
echo "------------------------------------------------------------"
# Owns every count in the navigation surface, not just the two repo-scale
# rows: each INDEX's Files badge, the "N files in M sub-stacks" headers and
# the Files column of every navigation table. Nothing else measured those,
# so 15 of 159 badges had drifted away from the folder they point at.
if python3 scripts/check_counts.py; then
    echo "  PASS"
else
    FAIL=1
fi

echo ""
echo "2/28  check_alignment.py — table pipes + ASCII box walls"
echo "     python3 scripts/check_alignment.py   (--fix repairs in place)"
echo "------------------------------------------------------------"
if python3 scripts/check_alignment.py; then
    echo "  PASS"
else
    echo "  FAIL — run 'python3 scripts/check_alignment.py --fix' then re-verify"
    FAIL=1
fi

echo ""
echo "3/28  check_structure.py — IDs, sequences, interview-last"
echo "     python3 scripts/check_structure.py"
echo "------------------------------------------------------------"
OUT=$(python3 scripts/check_structure.py 2>&1)
CODE=$?
# (2026-09-13: the lane-80.x numbering gaps were FIXED - the five prep docs
# moved from projects/docita into the lane, sequence 1..36 complete. The old
# baseline filters below are kept one release as a no-op safety net.)
REAL=$(printf '%s\n' "$OUT" | grep -v "80-lanes-abroad-full-stack prefix 80.x" \
    | grep -v "projects/docita prefix 80.x" \
    | grep -v "^OK:" || true)
if [ "$CODE" -eq 0 ] || [ -z "$REAL" ]; then
    printf '%s\n' "$OUT" | grep "GAPS" | sed 's/^/  baseline (intentional): /'
    echo "  PASS"
else
    printf '%s\n' "$REAL"
    FAIL=1
fi

echo ""
echo "4/28  check_links.py — fence-aware broken-link scan"
echo "     python3 scripts/check_links.py"
echo "------------------------------------------------------------"
if python3 scripts/check_links.py; then
    echo "  PASS"
else
    echo "  FAIL — fix the reported links (or confirm they are example links)"
    FAIL=1
fi

echo ""
echo "5/28  check_freshness.py — stale-API signature scan"
echo "     python3 scripts/check_freshness.py"
echo "------------------------------------------------------------"
if python3 scripts/check_freshness.py; then
    echo "  PASS"
else
    echo "  FAIL — modernize the flagged code/links (or refine the rule if it is a false positive)"
    FAIL=1
fi

echo ""
echo "6/28  link_baseline.py diff — live docs vs committed citation baseline"
echo "     python3 scripts/link_baseline.py"
echo "------------------------------------------------------------"
# Fails when a doc cites an external URL that is not in the committed
# baseline (and lists REMOVED urls as informational). Every ADDED url
# must be probe-verified live BEFORE --update; committing the baseline
# JSON together with the doc change is the verification record.
if python3 scripts/link_baseline.py; then
    echo "  PASS"
else
    echo "  FAIL — probe-verify each ADDED url, then run: python3 scripts/link_baseline.py --update"
    FAIL=1
fi

echo ""
echo "6b/28 check_template.py — template compliance (sections, order, genres)"
echo "     python3 scripts/check_template.py"
echo "------------------------------------------------------------"
# Supersedes check_required_sections.py (its Summary/See Also/References and
# interview-Code-Examples rules are enforced here as part of the full
# template). Checks required sections per genre (concept / interview /
# case-study / reference), canonical section order, and the known TL;DR
# styles. Corpus reached zero violations (Sept 2026), so it blocks.
if python3 scripts/check_template.py; then
    echo "  PASS"
else
    echo "  FAIL — run the reported file list and add the missing sections"
    FAIL=1
fi

echo ""
echo "7/28  check_claims.py — campaign-material claims integrity (purged phrases must not regress)"
echo "     python3 scripts/check_claims.py"
echo "------------------------------------------------------------"
# Born from the Sept 2026 cross-repo audits: claim phrases that were
# purged as unverifiable (Next.js-at-Docita, invented founder bios,
# unsourceable AI specifics) must never re-enter ACTIVE campaign files.
# Historical sent-application reports are allowlisted — they record what
# was actually sent and must stay frozen.
if python3 scripts/check_claims.py; then
    echo "  PASS"
else
    echo "  FAIL — reword with a source-verified claim, or extend CLAIM_ALLOWLIST if the file is historical"
    FAIL=1
fi

echo ""
echo "8/28  check_code_whitespace.py — code-block indentation hygiene"
echo "     python3 scripts/check_code_whitespace.py"
echo "------------------------------------------------------------"
# Trailing whitespace inside fences and whole-block paste-shift base
# indents (>=4 spaces on EVERY line of a lang-tagged block) render as
# sloppy code. Pass by design: gofmt-style go tabs, Anki TSV data,
# ASCII-diagram alignment in text fences. Fix with fix_code_whitespace.py.
if python3 scripts/check_code_whitespace.py; then
    echo "  PASS"
else
    echo "  FAIL — run: python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift"
    FAIL=1
fi

echo ""
echo "8b/28 fix_box_code_indent.py --check — de-indented code inside box diagrams"
echo "     python3 scripts/fix_box_code_indent.py --check --json --css"
echo "------------------------------------------------------------"
# Code embedded between ASCII box walls that lost its indentation (every
# row flat at the box column) renders as visibly broken code. Covers JS
# (keyword-anchored), JSON, and CSS stretches; each mode is strict — one
# non-conforming row makes a stretch invisible — and whole-stretch veto
# protects hand-aligned blocks. Fix with --fix (idempotent).
if python3 scripts/fix_box_code_indent.py --check --json --css >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/fix_box_code_indent.py --check --json --css 2>&1 | tail -20
    echo "  FAIL — review the listed stretches, then run: python3 scripts/fix_box_code_indent.py --fix --json --css"
    FAIL=1
fi

echo ""
echo "8c/28 fix_box_width.py --check — over-padded ASCII boxes (screen wrap)"
echo "     python3 scripts/fix_box_width.py --check"
echo "------------------------------------------------------------"
# Boxes whose right wall is pushed far past their content wrap on
# laptop screens. Shrinks single-box fences to content width (pure
# single-column rows only; nested/composite/adjacent boxes untouched).
# Fix with --fix (idempotent; run check_alignment.py --fix afterwards
# if walls drift).
if python3 scripts/fix_box_width.py --check >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/fix_box_width.py --check 2>&1 | tail -20
    echo "  FAIL — run: python3 scripts/fix_box_width.py --fix && python3 scripts/check_alignment.py --fix"
    FAIL=1
fi

echo "9/28 check_first_principles.py --diff — First Principles coverage must not regress"
echo "     python3 scripts/check_first_principles.py --diff"
echo "------------------------------------------------------------"
# Concept chapters carry a hand-authored ## First Principles section
# (derivation from unavoidable constraints, per contributing.md). The
# committed baseline locks per-stack counts: removing sections fails
# the build; growing coverage updates the baseline with --baseline.
if python3 scripts/check_first_principles.py --diff >/dev/null 2>&1; then
    python3 scripts/check_first_principles.py 2>/dev/null | tail -1
    echo "  PASS"
else
    python3 scripts/check_first_principles.py --diff 2>&1 | tail -10
    echo "  FAIL — restore removed sections or re-baseline deliberately: python3 scripts/check_first_principles.py --baseline"
    FAIL=1
fi

echo "------------------------------------------------------------"
echo "10/28 check_cross_refs.py — inline → N.N.N refs resolve to real files"
echo "     python3 scripts/check_cross_refs.py"
echo "------------------------------------------------------------"
# Cross-references name sibling chapters by file ID (→ 10.1.1.03). Renames
# and renumbering can orphan them silently; this fails the build on any
# ref that no longer resolves (padding-normalized, fence/prose aware).
if python3 scripts/check_cross_refs.py; then
    echo "  PASS"
else
    echo "  FAIL"
    FAIL=1
fi

echo ""
echo "11/28 check_duplication.py --strict — no chapter teaches another chapter's prose"
echo "     python3 scripts/check_duplication.py --strict"
echo "------------------------------------------------------------"
# The \"every topic lives in exactly ONE place\" rule is only as good as the
# tooling behind it: the chaos-engineering pair grew to ~250 overlapping
# lines before anything measured overlap. Fence-aware 5-word shingles over
# `##` bodies, template sections excluded, --min-words floors short
# paragraphs. 1.00 on a planted copy is the negative test.
if python3 scripts/check_duplication.py --strict >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/check_duplication.py --strict 2>&1 | tail -20
    echo "  FAIL — merge the overlapping sections into one chapter, or scope the pair apart"
    FAIL=1
fi

echo ""
echo "12/28 check_topic_twins.py — twin chapters must cross-link"
echo "     python3 scripts/check_topic_twins.py"
echo "------------------------------------------------------------"
# A pattern chapter, its framework implementation and its case study are a
# deliberate parallel treatment — but only if they route to each other.
# Unlinked twins are how the chaos pair drifted into two copies. Fix with
# python3 scripts/link_topic_twins.py (descriptions derived from the
# target chapter's own opening, never generic filler).
if python3 scripts/check_topic_twins.py >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/check_topic_twins.py 2>&1 | sed -n '/MISSING TWIN LINKS/,$p'
    echo "  FAIL — run: python3 scripts/link_topic_twins.py"
    FAIL=1
fi

echo ""
echo "13/28 read_time.py --check — declared study times vs computed estimates"
echo "     python3 scripts/read_time.py --check"
echo "------------------------------------------------------------"
# Read times were hand-guessed and contradicted each other (2,912 words
# labelled 15 min beside 2,353 labelled 20 min). They are now computed from
# one documented model, and every INDEX must agree with it.
if python3 scripts/read_time.py --check >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/read_time.py --check 2>&1 | tail -10
    echo "  FAIL — run: python3 scripts/read_time.py --write"
    FAIL=1
fi

echo ""
echo "14/28 gen_master_index.py --check — generated search page in sync with the corpus"
echo "     python3 scripts/gen_master_index.py --check"
echo "------------------------------------------------------------"
# search.html is generated from the same enforced metadata (gate 6b) and
# read times (gate 13); hand-edits or corpus changes without regeneration
# would make the site's search page lie.
if python3 scripts/gen_master_index.py --check >/dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/gen_master_index.py --check 2>&1 | tail -3
    echo "  FAIL — run: python3 scripts/gen_master_index.py"
    FAIL=1
fi

echo ""
echo "15/28 check_verify_wiring.py — verify.sh's own wiring + gate-count self-consistency"
echo "     python3 scripts/check_verify_wiring.py"
echo "------------------------------------------------------------"
# The one gate that watches the harness instead of the corpus. Gate 10's
# failure branch once wrote a variable that nothing else read, so under
# `set -u` the unbound arithmetic aborted this script BEFORE its trailing
# `exit $FAIL` was reached: a broken cross-reference printed FAIL, skipped
# gates 11-14, and still exited 0. Every individual gate script was
# correct throughout - nothing checked whether verify.sh listened. This
# also owns the gate count, which was hand-maintained in three files.
if python3 scripts/check_verify_wiring.py; then
    echo "  PASS"
else
    echo "  FAIL — the harness, not the corpus, is broken: every failure branch must set FAIL=1"
    FAIL=1
fi

echo ""
echo "16/28 test_md_fences.py — the fence owner's semantics are pinned"
echo "     python3 scripts/test_md_fences.py"
echo "------------------------------------------------------------"
# md_fences.walk() is the single fence parser behind ten gates and fixers. A
# regression there corrupts link scanning, duplication detection, the box
# fixers and the structure gate simultaneously — and silently, because none
# of them fence-parse on their own anymore. These characterization tests pin
# the documented semantics (same char >= length closes; nested fences are
# content; is_fence_line means a real delimiter) so the owner cannot drift.
if python3 scripts/test_md_fences.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/test_md_fences.py | tail -6
    echo "  FAIL — md_fences.walk semantics drifted; fix the module, not the expectations"
    FAIL=1
fi

echo ""
echo "17/28 test_fixers.py — the fixers' repair output is pinned"
echo "     python3 scripts/test_fixers.py"
echo "------------------------------------------------------------"
# Gates catch defects; these round-trip tests catch FIXERS THAT REPAIR
# WRONGLY. Each case plants one canonical defect in a temp-tree sandbox and
# asserts the repaired file byte-for-byte against the fixer's recorded
# contract, plus idempotence and a no-mangle negative case. Exact asserts
# keep fixer output and gate expectations from ever disagreeing — the same
# single-owner discipline as gate 16, applied to the writers instead of the
# readers.
if python3 scripts/test_fixers.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/test_fixers.py | tail -8
    echo "  FAIL — a fixer's output drifted from its recorded contract"
    FAIL=1
fi

echo ""
echo "18/28 test_gates.py — the gates still catch their defects"
echo "     python3 scripts/test_gates.py"
echo "------------------------------------------------------------"
# The meta-gate: plants each sandboxable gate's canonical defect in a temp
# tree and asserts the gate exits non-zero (fire side), then runs it on
# clean content including a real passing chapter (clean side, so a gate
# broken to fire on everything cannot pass either). Closes the gap gates
# 15-17 leave: they watch wiring, the fence reader, and the fixers — not
# whether detection itself still works.
if python3 scripts/test_gates.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/test_gates.py | tail -10
    echo "  FAIL — a gate no longer detects its canonical defect"
    FAIL=1
fi


echo "19/28 check_answer_depth.py — every interview answer carries real prose"
echo "     python3 scripts/check_answer_depth.py"
echo "------------------------------------------------------------"
# The 2026-09-21 arc deepened 247 answers; the follow-up probe found 27
# table-only answers (tables enumerate, they don't explain) that the arc's
# own table-counting scanner had masked. This gate keeps the floor:
# >= 25 prose words per answer, fence- and table-aware via md_fences.
if python3 scripts/check_answer_depth.py; then
    echo "  PASS"
else
    echo "  FAIL — add mechanism/trade-off prose to the listed answers"
    FAIL=1
fi


echo "20/28 test_prose_scan.py — the prose scanner's classification contract"
echo "     python3 scripts/test_prose_scan.py"
echo "------------------------------------------------------------"
# prose_scan.py is the one owner of "what counts as reasoning prose"
# (gate 19 consumes it). This pins the contract: tables, headings, quotes,
# badges and fences never count; inline code does; naive token split is
# pinned on purpose. A silent classifier change cannot ship.
if python3 scripts/test_prose_scan.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/test_prose_scan.py | tail -10
    echo "  FAIL — prose_scan classification drifted; fix the module, not the tests"
    FAIL=1
fi


echo "21/28 fix_nav_labels.py --check — nav labels are human titles, not paths"
echo "     python3 scripts/fix_nav_labels.py   (--fix repairs them)"
echo "------------------------------------------------------------"
# The navigation surface's Previous/Next labels were generated by a pass
# that humanized target slugs: it title-cased acronyms ("Mvcc", "Cqrs Di",
# "Sli Slo Sla") and left 55 raw relative paths in place of titles. Both are
# uniform-and-wrong generator signatures — the same family as the 2026-09
# collapsed cheat sheets. Rule 2 derives a path label's replacement from the
# target file's own H1, so the label cannot drift from what it links to.
if python3 scripts/fix_nav_labels.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/fix_nav_labels.py | tail -12
    echo "  FAIL — run: python3 scripts/fix_nav_labels.py --fix"
    FAIL=1
fi


echo "22/28 check_fixpoint.py — a clean corpus is a no-op for every writer"
echo "     python3 scripts/check_fixpoint.py"
echo "------------------------------------------------------------"
# The strongest guarantee the harness can make about its own writers: run all
# nine repair/restamp tools over a COPY of the corpus and require every file to
# come back byte-identical. A writer that edits a file while its checker calls
# it clean is making an edit *nothing can flag* — the one failure mode a
# self-auditing suite cannot see from the inside. The 2026-09-21 probe found
# two by hand: a whitespace fixer stripping trailing whitespace inside layout
# fences the checker deliberately exempts, and a fence labeler proposing
# `typescript` for mixed cheat-sheet fences (title bar + code + tips prose).
if python3 scripts/check_fixpoint.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/check_fixpoint.py | head -20
    echo "  FAIL — a writer edits what its checker calls clean; align their scope"
    FAIL=1
fi


echo "23/28 check_scope_floor.py — every corpus gate fails honestly on an empty tree"
echo "     python3 scripts/check_scope_floor.py"
echo "------------------------------------------------------------"
# The false-green family, checker side: a gate whose walk finds nothing prints
# the same compliance sentence it prints every day. The 2026-09-21 probe ran
# every checker against an empty tree and 15 of 19 exited 0 ("OK — 0 links
# checked", "template compliance OK"); two more died in a traceback, which is
# not an honest failure either. Every corpus gate now asserts its own reach via
# scan_scope.guard, and this gate proves it for all of them at once, deriving
# the gate list from verify.sh itself so a new gate cannot skip the check.
if python3 scripts/check_scope_floor.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/check_scope_floor.py | head -20
    echo "  FAIL — a gate passes or crashes on an empty corpus; assert its scope"
    FAIL=1
fi

echo ""
echo "24/28  prose_hygiene.py — spelling convention + rendering breaks + empty-filler register"
echo "     python3 scripts/prose_hygiene.py   (--write repairs them)"
echo "------------------------------------------------------------"
# Four reader-visible classes no other gate owned (measured 2026-09-22):
# 13 spelling pairs carried BOTH forms in a corpus that is American by an
# 845-to-26 margin (62 instances of the minority form), one ATX heading had
# no space after its hashes (CommonMark then renders it as literal text and
# the section loses its structure), and two GFM table rows held unescaped
# pipes inside a code span — GFM splits on `|` before inline parsing, so
# those rows rendered with extra columns and the table stopped lining up.
# Spans, link targets, URLs and table cells are masked before matching, so a
# CSS `color:` or a `colour` inside a URL is never touched; `Sopra Steria
# Defence`, `Colour Contrast Analyser` and `aria-labelledby` are named
# exemptions because a word rule cannot know a proper noun. The fourth class is
# the corpus's own register: eighteen empty openers, none of which it uses
# today, gated so that "the prose states claims" cannot regress. That one is the
# only finding `--write` cannot repair — deleting a phrase leaves worse prose
# than the phrase did — so the run reports it and exits non-zero for the author.
if python3 scripts/prose_hygiene.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/prose_hygiene.py | tail -20
    echo "  FAIL — run: python3 scripts/prose_hygiene.py --write"
    FAIL=1
fi

echo ""
echo "25/28  check_dilution.py — a chapter must not restate itself"
echo "     python3 scripts/check_dilution.py   (--baseline re-baselines deliberately)"
echo "------------------------------------------------------------"
# The 2026-09-22 audit measured the recurring reader complaint ("the corpus
# repeats itself and buries its main point") instead of assuming it: adjacent-
# sentence restatement 0, the partial band 0, intra-chapter near-duplicates 0,
# TL;DR-vs-Summary overlap median 0.00. This gate makes that measurement
# standing: a ceiling baseline per class, so a chapter that grows a second
# copy of a point it already made fails the build. Ceiling, not floor —
# improvement below it needs no action. Complements gate 11, which owns
# cross-chapter copying: this is the within-chapter, sentence-granularity
# half. Check-only by design — a hit is an editorial decision (merge or cut),
# not a mechanical repair.
if python3 scripts/check_dilution.py > /dev/null 2>&1; then
    echo "  PASS"
else
    python3 scripts/check_dilution.py | tail -20
    echo "  FAIL — merge the restated passages (or re-baseline deliberately: python3 scripts/check_dilution.py --baseline)"
    FAIL=1
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "All checks passed — tree is clean."
    exit 0
else
    echo "One or more checks FAILED — fix the reported issues before pushing."
    exit 1
fi
