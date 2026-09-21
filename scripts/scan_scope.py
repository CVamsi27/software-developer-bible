#!/usr/bin/env python3
"""One owner for the scope floor: a checker that scans nothing must not pass.

Every gate in this repo ends its run with a compliance verdict — "OK — 0 links
checked", "template compliance OK", "0 file(s) with misaligned boxes/tables".
Read those again: the *first* one names its own empty scope, and the others
would print exactly the same sentence if their discovery broke. A gate whose
scope silently collapses (a renamed stack folder, a changed glob, a wrong root,
an `iter_md` whose skip list grew too far) keeps exiting 0 forever, and its
silence is **indistinguishable from a pass** — the same false-green family as a
writer editing what its checker calls clean (gate 22), one level up.

The 2026-09-21 probe measured the class by running every checker against an
empty tree:

    15 of 19 checkers exited 0. Only check_counts and check_verify_wiring
    failed (both by traceback, which is not an honest failure either).

So each checker now asserts its own reach before trusting its verdict, through
this one helper — mirroring how `md_fences` owns fence parsing and
`prose_scan` owns prose classification. Gate 23 (`check_scope_floor.py`) proves
the property for every gate at once by running each one against an empty tree
and requiring a *clean* non-zero exit.

Usage in a checker, right after discovery:

    from scan_scope import guard
    guard(len(files), 'markdown files')          # exits 1 with a scope error if 0

`guard` is silent when it passes — the gates' own OK lines carry their counts,
and a compliant corpus should not print noise on every push. The floor is a
deliberate constant, not a derived value: the human-readable number belongs in
each gate's summary line, where a reader can see what it actually looked at.
"""
import sys


def guard(count: int, what: str, where: str = "") -> int:
    """Fail the build when a checker discovered nothing to check.

    Returns the count so callers can write `n = guard(len(files), 'files')`.
    """
    if count > 0:
        return count
    spot = f" under {where}" if where else ""
    print(
        f"SCOPE ERROR — 0 {what} found{spot}.\n"
        f"  A gate that scans nothing cannot certify anything: this verdict would\n"
        f"  be identical if the corpus moved, or a glob broke, or a skip list\n"
        f"  grew too far — and the build would stay green forever. Fix the gate's\n"
        f"  discovery (root, pattern, excludes) before trusting it. If the scope\n"
        f"  is now legitimately empty, change the floor deliberately in\n"
        f"  scripts/scan_scope.py's caller and say why in the commit."
    )
    raise SystemExit(1)
