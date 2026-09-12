#!/usr/bin/env bash
# One-command verification gate for the software-developer-bible repo.
# Runs the six mechanical checks in order; exits non-zero if any real
# failure is found. Known lane-80.x numbering GAPS are intentional (numbers
# owned by projects/docita prep docs) and reported as baseline noise, not
# failures.
#
# Usage:  bash scripts/verify.sh        (from the repo root)
set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0

echo ""
echo "1/6  check_counts.py — repo-total scale claims vs live disk"
echo "     python3 scripts/check_counts.py"
echo "------------------------------------------------------------"
if python3 scripts/check_counts.py; then
    echo "  PASS"
else
    FAIL=1
fi

echo ""
echo "2/6  check_alignment.py — table pipes + ASCII box walls"
echo "     python3 scripts/check_alignment.py   (--fix repairs in place)"
echo "------------------------------------------------------------"
if python3 scripts/check_alignment.py; then
    echo "  PASS"
else
    echo "  FAIL — run 'python3 scripts/check_alignment.py --fix' then re-verify"
    FAIL=1
fi

echo ""
echo "3/6  check_structure.py — IDs, sequences, interview-last"
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
echo "4/6  check_links.py — fence-aware broken-link scan"
echo "     python3 scripts/check_links.py"
echo "------------------------------------------------------------"
if python3 scripts/check_links.py; then
    echo "  PASS"
else
    echo "  FAIL — fix the reported links (or confirm they are example links)"
    FAIL=1
fi

echo ""
echo "5/6  check_freshness.py — stale-API signature scan"
echo "     python3 scripts/check_freshness.py"
echo "------------------------------------------------------------"
if python3 scripts/check_freshness.py; then
    echo "  PASS"
else
    echo "  FAIL — modernize the flagged code/links (or refine the rule if it is a false positive)"
    FAIL=1
fi

echo ""
echo "6/6  link_baseline.py diff — live docs vs committed citation baseline"
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
    echo "All checks passed — tree is clean."
    exit 0
else
    echo "One or more checks FAILED — fix the reported issues before pushing."
    exit 1
fi
