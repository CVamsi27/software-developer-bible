#!/usr/bin/env python3
"""Round-trip tests for the markdown fixers — planted defects, exact repairs.

The gates catch defects; these tests catch *fixers that repair wrongly*.
Each case plants one canonical defect in a temp-tree copy of the corpus
scaffold, runs the fixer, and asserts the repaired file byte-for-byte
against the recorded canonical output. The expected outputs were pinned by
running each fixer against its defect and recording what it actually does —
so they are the fixers' recorded contract, not aspirational output.

Why exact asserts: an approximate assert ("file changed", "defect gone")
would pass a fixer that over-strips, mangles box walls, or eats the
canonical spacing the alignment gate then enforces. The whole point is that
fixer output and gate expectations can never disagree.

Also asserted: idempotence (running the fixer twice changes nothing the
second time) and a negative case (already-canonical content passes through
byte-identical — a fixer must not mangle good files).

Sandboxing: every fixer derives its repo root from __file__, so the runner
copies each fixer plus md_fences.py into a temp scripts/ dir and runs it
against files in that tree — the real corpus is never touched.

Exits 0 when all cases pass. Run directly: python3 scripts/test_fixers.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = sys.executable

# --- recorded contracts (pinned by probe runs, 2026-09-20) -----------------

TABLE_BEFORE = """before

| A | B |
|---|---|
| 1 | 2 |

after
"""

TABLE_AFTER = """before

| A | B |
| --- | --- |
| 1 | 2 |

after
"""

BOX_BEFORE = """text

```
┌──────────┐
│ hi │
│ world │
└──────────┘
```
"""

BOX_AFTER = """text

```
┌──────────┐
│ hi       │
│ world    │
└──────────┘
```
"""

WS_BEFORE = """text

```js
const y = 3;
```
"""

WS_AFTER = """text

```js
const y = 3;
```
"""

SHIFT_BEFORE = """text

```js
    const x = 1;
    if (x) {
      return 2;
    }
```

more
"""

SHIFT_AFTER = """text

```js
const x = 1;
if (x) {
  return 2;
}
```

more
"""

WIDE_BEFORE = """# T

```text
┌──────────────────────────────────────────┐
│ hello                                    │
│ world                                    │
└──────────────────────────────────────────┘
```
"""

WIDE_AFTER = """# T

```text
┌────────────┐
│ hello      │
│ world      │
└────────────┘
```
"""

FLAT_BEFORE = """```text
┌──────────────────────────────┐
│ function load() {            │
│ try {                        │
│ return 1;                    │
│ } catch (e) {}               │
│ }                            │
└──────────────────────────────┘
```
"""

FLAT_AFTER = """```text
┌──────────────────────────────┐
│ function load() {            │
│   try {                      │
│     return 1;                │
│   } catch (e) {}             │
│ }                            │
└──────────────────────────────┘
```
"""

CLEAN = """# Clean

| A | B |
| --- | --- |
| 1 | 2 |

```
┌──────────┐
│ hi       │
│ world    │
└──────────┘
```
"""

CASES = [
    {
        "name": "table alignment: separator spacing + row padding",
        "fixer": "check_alignment.py",
        "args": ["--fix"],
        "before": TABLE_BEFORE,
        "after": TABLE_AFTER,
    },
    {
        "name": "box alignment: ragged walls realigned to widest row",
        "fixer": "check_alignment.py",
        "args": ["--fix"],
        "before": BOX_BEFORE,
        "after": BOX_AFTER,
    },
    {
        "name": "trailing whitespace stripped inside fences only",
        "fixer": "fix_code_whitespace.py",
        "args": ["--trailing-ws", "--paste-shift"],
        "before": WS_BEFORE,
        "after": WS_AFTER,
    },
    {
        "name": "paste-shift: 4-space base indent dedented, inner kept",
        "fixer": "fix_code_whitespace.py",
        "args": ["--trailing-ws", "--paste-shift"],
        "before": SHIFT_BEFORE,
        "after": SHIFT_AFTER,
    },
    {
        "name": "box width: over-padded single box narrowed to content",
        "fixer": "fix_box_width.py",
        "args": ["--fix"],
        "before": WIDE_BEFORE,
        "after": WIDE_AFTER,
    },
    {
        "name": "box code indent: flat JS stretch rebased from brace depth",
        "fixer": "fix_box_code_indent.py",
        "args": ["--fix"],
        "before": FLAT_BEFORE,
        "after": FLAT_AFTER,
    },
    {
        "name": "negative: canonical content passes through byte-identical",
        "fixer": "check_alignment.py",
        "args": ["--fix"],
        "before": CLEAN,
        "after": CLEAN,
    },
]


def run_case(case, tmp):
    scripts = os.path.join(tmp, "scripts")
    os.makedirs(scripts, exist_ok=True)
    shutil.copy(os.path.join(HERE, case["fixer"]), scripts)
    shutil.copy(os.path.join(HERE, "md_fences.py"), scripts)
    target = os.path.join(tmp, "sample.md")
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(case["before"])

    r = subprocess.run(
        [RUNNER, os.path.join("scripts", case["fixer"]), *case["args"], "sample.md"],
        cwd=tmp, capture_output=True, text=True,
    )
    if r.returncode != 0:
        return [f"fixer exited {r.returncode}: {r.stdout.strip()} {r.stderr.strip()}"]

    with open(target, encoding="utf-8") as fh:
        got = fh.read()
    problems = []
    if got != case["after"]:
        problems.append("repaired output differs from the recorded contract:")
        gl, al = got.splitlines(), case["after"].splitlines()
        for n in range(max(len(gl), len(al))):
            g = gl[n] if n < len(gl) else "<missing>"
            a = al[n] if n < len(al) else "<missing>"
            if g != a:
                problems.append(f"  line {n + 1}: got {g!r}, want {a!r}")

    # idempotence: second run must not change the file again
    subprocess.run(
        [RUNNER, os.path.join("scripts", case["fixer"]), *case["args"], "sample.md"],
        cwd=tmp, capture_output=True, text=True,
    )
    with open(target, encoding="utf-8") as fh:
        got2 = fh.read()
    if got2 != case["after"]:
        problems.append("fixer is not idempotent — second run changed the file again")
    return problems


def main() -> int:
    failures = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            problems = run_case(case, tmp)
        if problems:
            failures += 1
            print(f"FAIL {case['name']}")
            for p in problems:
                print(f"  {p}")
        else:
            print(f"ok   {case['name']}")
    if failures:
        print(f"\n{failures} case(s) failed — a fixer's output drifted from its "
              f"recorded contract; fix the fixer, or re-pin the contract "
              f"deliberately with a probe run and a note in the commit.")
        return 1
    print(f"\nfixers: {len(CASES)}/{len(CASES)} round-trips pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
