#!/usr/bin/env python3
r"""Characterization tests for scripts/md_fences.py — the single fence owner.

md_fences.walk() replaced ten naive `in_fence = not in_fence` toggles across
the tooling. Every gate and fixer that classifies markdown lines as inside or
outside a code block now routes through this one function, so a regression
here corrupts link scanning, duplication detection, freshness rules, box
fixers and the structure gate *simultaneously* — silently, because none of
those gates fence-parse on their own anymore.

The suite pins the documented semantics (see md_fences.py's docstring):

  1. same character at >= the opener's length closes — including a labeled
     close, which renderers would read as content (the corpus gate rejects
     labeled closes, so no passing file can distinguish the two readings);
  2. a shorter or other-character fence line inside a block is content —
     what makes documented nested-fence examples (``` inside ````) parse;
  3. `in_fence` is the state AFTER the line (so the opener itself is
     "inside"); `is_fence_line` is True ONLY on lines that actually open or
     close a block — a ``` line inside a ```` block is content, not a
     delimiter. Writing these expectations pinned a real inconsistency: the
     old code flagged regex-matching content lines as delimiters, which a
     trusting fixer would have edited — the exact repair-pass bug class
     this module exists to prevent;
  4. indented fences (CommonMark allows up to 3 spaces) open and close.

Known limitation, pinned here so it is a *decision* not a surprise: fences
inside blockquote lines (`> ```` `) are not tracked — the corpus contains
none (gate-green), and FENCE_LINE's `^\s*` anchor deliberately excludes
`>`-prefixed lines.

Exits 0 when all cases pass; prints the failing case and exits 1 otherwise.
Run directly: python3 scripts/test_md_fences.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences  # noqa: E402


def fence_lines(text):
    """Indices of lines walk() flags as real delimiters (open or close)."""
    return [i for i, _, _, isl in md_fences.walk(text.splitlines()) if isl]


def inside(text):
    """Indices of lines classified as inside a fenced block (opener included)."""
    return [i for i, _, inf, _ in md_fences.walk(text.splitlines()) if inf]


CASES = [
    # (name, markdown text, expected delimiter indices, expected inside indices)
    (
        "unclosed fence: everything from the opener on is inside",
        "```\ncode\nprose that looks safe\n",
        [0],
        [0, 1, 2],
    ),
    (
        "basic pair: open, content, bare close",
        "```js\ncode\n```\nprose\n",
        [0, 2],
        [0, 1],
    ),
    (
        "tilde pair closes the same way",
        "~~~\ncode\n~~~\nprose\n",
        [0, 2],
        [0, 1],
    ),
    (
        "labeled close counts as close (documented trade-off)",
        "```\ncode\n```yaml\nafter\n",
        [0, 2],
        [0, 1],
    ),
    (
        "nested: ``` inside ```` is content, not a delimiter",
        "````\ncode\n```\nstill code\n````\nprose\n",
        [0, 4],
        [0, 1, 2, 3],
    ),
    (
        "other char inside block is content (~~~ inside ```)",
        "```\ncode\n~~~\nstill code\n```\nprose\n",
        [0, 4],
        [0, 1, 2, 3],
    ),
    (
        "longer close of same char closes (5 closes 3)",
        "```\ncode\n`````\nprose\n",
        [0, 2],
        [0, 1],
    ),
    (
        "shorter same-char line inside is content (3 inside 5)",
        "`````\ncode\n```\nstill code\n`````\nprose\n",
        [0, 4],
        [0, 1, 2, 3],
    ),
    (
        "indented fence (2 spaces) opens and closes",
        "  ```\n  code\n  ```\nprose\n",
        [0, 2],
        [0, 1],
    ),
    (
        "indented fences inside list items track pairwise",
        "- item\n\n  ```js\n  code\n  ```\n\n- next\n",
        [2, 4],
        [2, 3],
    ),
    (
        "blockquote fences are not tracked (documented limitation)",
        "> ```\n> code\n> ```\nprose\n",
        [],
        [],
    ),
    (
        "no fences: all prose",
        "# Title\n\ntext with `inline code` only\n",
        [],
        [],
    ),
    (
        "adjacent blocks: two independent pairs",
        "```a\nx\n```\n\n```b\ny\n```\nprose\n",
        [0, 2, 4, 6],
        [0, 1, 4, 5],
    ),
    (
        "real corpus shape: 4-backtick outer, 3-backtick literal inner",
        "````markdown\n# Example\n\n```yaml\nkey: value\n```\n\nSee, the inner block renders.\n````\nprose after\n",
        [0, 8],
        [0, 1, 2, 3, 4, 5, 6, 7],
    ),
    (
        "labeled opener with info string opens normally",
        "```python title=x\nprint(1)\n```\nprose\n",
        [0, 2],
        [0, 1],
    ),
    (
        "tildes and backticks do not cross-close",
        "~~~\n```\nstill tilde block\n~~~\nprose\n",
        [0, 3],
        [0, 1, 2],
    ),
]


def main() -> int:
    failures = 0
    for name, text, want_fences, want_inside in CASES:
        got_fences = fence_lines(text)
        got_inside = inside(text)
        if got_fences != want_fences or got_inside != want_inside:
            failures += 1
            print(f"FAIL {name}")
            print(f"  delimiters: got {got_fences}, want {want_fences}")
            print(f"  inside    : got {got_inside}, want {want_inside}")
        else:
            print(f"ok   {name}")
    if failures:
        print(f"\n{failures} case(s) failed — md_fences.walk semantics drifted; "
              f"fix md_fences.py, not these expectations.")
        return 1
    n = len(CASES)
    print(f"\nmd_fences: {n}/{n} cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
