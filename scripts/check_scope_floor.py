#!/usr/bin/env python3
"""Gate 23 — every corpus gate must fail *honestly* when its scope is empty.

The false-green family, third level. Gate 22 closed writers that edit what
their checker calls clean. This closes the checker side: a gate whose scope
silently collapses prints the same compliance sentence it prints every day.

    2026-09-21 probe, every checker run against an empty tree:
      15 of 19 exited 0 — "OK — 0 links checked", "template compliance OK",
      "0 file(s) with misaligned boxes/tables".
      check_counts and check_verify_wiring failed, but by traceback, which is
      not an honest failure either.

A gate whose walk finds nothing (a renamed stack folder, a changed glob, a skip
list that grew too far, a wrong root) is indistinguishable from a passing one.
So every corpus gate now asserts its own reach through `scan_scope.guard`, and
this gate proves the property for all of them at once: copy the scripts into an
empty tree, run each gate, and require

    exit code 1  AND  the words "SCOPE ERROR" on stdout

requiring both halves is what makes it honest — a crash also exits 1, and a
crash is exactly the failure mode that hides a broken walk behind noise.

The gate list is *derived* from `verify.sh` (through check_verify_wiring's
parser, the single owner of that format) with the gate's own documented flags,
so a new gate cannot quietly skip this check: it must either carry a scope
floor or be named in EXEMPT below with a reason. That is the same
no-unwired-checker discipline gate 15 applies to the suite.

Exemptions (harness gates and one byte-locked generator) are listed with why.

Usage:  python3 scripts/check_scope_floor.py
"""
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

import check_verify_wiring as wiring  # noqa: E402  (single owner of verify.sh parsing)

# Gates this test does not apply to, with the reason. Anything wired into
# verify.sh must appear here or carry a scope floor.
EXEMPT = {
    'check_verify_wiring.py':
        'harness gate — it audits verify.sh, not the corpus; its subject is '
        'the wiring itself, which the empty sandbox still provides',
    'test_gates.py':
        'the self-test — it plants defects in its own sandboxes and asserts '
        'gate behaviour; it has no corpus scope of its own',
    'test_fixers.py':
        'fixer-contract suite — same reason: it builds its own sandboxes',
    'test_md_fences.py':
        'fence-parser characterization suite — operates on literals, not files',
    'test_prose_scan.py':
        'prose-classifier characterization suite — same reason',
    'gen_master_index.py':
        'byte-locked generator — on an empty tree it fails for a different '
        'honest reason (search.html missing); the byte lock is its plant test',
    'check_scope_floor.py':
        'cannot check itself: the sandbox it builds still contains verify.sh, '
        'so a nested run would recurse without end (found by running it, not by '
        'reading it). Its own floor is MIN_GATES below — a derived gate list '
        'that came back empty or truncated is a broken parse, not a clean tree',
}

# Every wired gate must be accounted for: checked, or exempt with a reason.
# A parse bug that silently yielded one gate would otherwise "prove" the
# property for a single script and pass.
MIN_GATES = 15


def empty_tree(work):
    """A tree with the tooling but no corpus at all."""
    scripts = os.path.join(work, 'scripts')
    os.makedirs(scripts, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith(('.py', '.sh', '.json')):
            shutil.copy(os.path.join(HERE, fn), scripts)
    return work


def invocations():
    """(script, args) for every gate wired into verify.sh, in gate order."""
    text = open(os.path.join(HERE, 'verify.sh'), encoding='utf-8').read()
    out = []
    for gate in wiring.parse_gates(text, wiring.summary_start(text)):
        script = gate['script']
        args = []
        for line in gate['body']:
            # Only real invocation lines: `echo "... python3 scripts/x.py --write"`
            # labels must not be mistaken for the gate's flags.
            m = re.match(r'\s*(?:if\s+)?python3\s+scripts/' + re.escape(script) + r'(.*)$', line)
            if m:
                tail = shlex.split(m.group(1))
                cut = next((i for i, t in enumerate(tail)
                            if t.startswith(('>', ';', '&&', '||', '|'))), len(tail))
                args = tail[:cut]
                break
        out.append((script, args))
    return out


def main() -> int:
    if not os.path.exists(os.path.join(HERE, 'verify.sh')):
        print('SCOPE ERROR — no verify.sh in scripts/; the gate list cannot be derived')
        return 1

    table = invocations()
    if len(table) < MIN_GATES:
        print(f'SCOPE ERROR — the gate list derived from verify.sh has only '
              f'{len(table)} entries (floor {MIN_GATES}).\n'
              f'  That list is parsed out of verify.sh, so a truncated or broken '
              f'parse would "prove" the property for a single gate and pass.')
        return 1

    checked, skipped, problems = 0, [], []
    with tempfile.TemporaryDirectory() as tmp:
        work = empty_tree(tmp)
        for script, args in table:
            if script in EXEMPT:
                skipped.append(script)
                continue
            checked += 1
            r = subprocess.run([sys.executable, os.path.join('scripts', script), *args],
                               cwd=work, capture_output=True, text=True)
            honest = r.returncode == 1 and 'SCOPE ERROR' in r.stdout
            if honest:
                continue
            first = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ['(no output)'])[0]
            if r.returncode == 0:
                why = 'exited 0 on an empty corpus — it would report compliance forever'
            elif 'Traceback' in (r.stdout + r.stderr):
                why = 'died in a traceback instead of naming the empty scope'
            else:
                why = f'exited {r.returncode} without a SCOPE ERROR'
            problems.append(f'{script} {" ".join(args)}: {why}\n      {first[:110]}')

    if problems:
        print(f'SCOPE-FLOOR FAIL — {len(problems)} gate(s) pass or crash on an empty corpus:\n')
        for p in problems:
            print(f'   {p}')
        print('\n  Add `from scan_scope import guard` and assert the gate\'s own reach '
              '(see scan_scope.py), or list it in EXEMPT with a reason.')
        return 1

    print(f'scope floor OK — {checked} gates each fail with a SCOPE ERROR on an empty '
          f'corpus ({len(skipped)} exempt: ' + ', '.join(sorted(skipped)) + ')')
    return 0


if __name__ == '__main__':
    sys.exit(main())
