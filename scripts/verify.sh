#!/usr/bin/env bash
# One-command verification gate for the software-developer-bible repo.
# Runs the eight mechanical checks in order; exits non-zero if any real
# failure is found. Known lane-80.x numbering GAPS are intentional (numbers
# owned by projects/docita prep docs) and reported as baseline noise, not
# failures.
#
# Usage:  bash scripts/verify.sh        (from the repo root)
set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0

echo ""
echo "1/15  check_counts.py — repo-total scale claims vs live disk"
echo "     python3 scripts/check_counts.py"
echo "------------------------------------------------------------"
if python3 scripts/check_counts.py; then
    echo "  PASS"
else
    FAIL=1
fi

echo ""
echo "2/15  check_alignment.py — table pipes + ASCII box walls"
echo "     python3 scripts/check_alignment.py   (--fix repairs in place)"
echo "------------------------------------------------------------"
if python3 scripts/check_alignment.py; then
    echo "  PASS"
else
    echo "  FAIL — run 'python3 scripts/check_alignment.py --fix' then re-verify"
    FAIL=1
fi

echo ""
echo "3/15  check_structure.py — IDs, sequences, interview-last"
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
echo "4/15  check_links.py — fence-aware broken-link scan"
echo "     python3 scripts/check_links.py"
echo "------------------------------------------------------------"
if python3 scripts/check_links.py; then
    echo "  PASS"
else
    echo "  FAIL — fix the reported links (or confirm they are example links)"
    FAIL=1
fi

echo ""
echo "5/15  check_freshness.py — stale-API signature scan"
echo "     python3 scripts/check_freshness.py"
echo "------------------------------------------------------------"
if python3 scripts/check_freshness.py; then
    echo "  PASS"
else
    echo "  FAIL — modernize the flagged code/links (or refine the rule if it is a false positive)"
    FAIL=1
fi

echo ""
echo "6/15  link_baseline.py diff — live docs vs committed citation baseline"
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
echo "7/15  check_claims.py — campaign-material claims integrity (purged phrases must not regress)"
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
echo "6b/15 check_template.py — template compliance (sections, order, genres)"
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
echo "8/15  check_code_whitespace.py — code-block indentation hygiene"
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
echo "8b/15 fix_box_code_indent.py --check — de-indented code inside box diagrams"
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
echo "8c/15 fix_box_width.py --check — over-padded ASCII boxes (screen wrap)"
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

echo "9/15 check_first_principles.py --diff — First Principles coverage must not regress"
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
echo "10/15 check_cross_refs.py — inline → N.N.N refs resolve to real files"
echo "     python3 scripts/check_cross_refs.py"
echo "------------------------------------------------------------"
# Cross-references name sibling chapters by file ID (→ 10.1.1.03). Renames
# and renumbering can orphan them silently; this fails the build on any
# ref that no longer resolves (padding-normalized, fence/prose aware).
if python3 scripts/check_cross_refs.py; then
    echo "  PASS"
else
    echo "  FAIL"
    FAILURES=$((FAILURES+1))
fi

echo ""
echo "11/15 check_duplication.py --strict — no chapter teaches another chapter's prose"
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
echo "12/15 check_topic_twins.py — twin chapters must cross-link"
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
if [ "$FAIL" -eq 0 ]; then
    echo "All checks passed — tree is clean."
    exit 0
else
    echo "One or more checks FAILED — fix the reported issues before pushing."
    exit 1
fi
