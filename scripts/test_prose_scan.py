#!/usr/bin/env python3
"""test_prose_scan.py — the prose scanner's classification contract, pinned.

`prose_scan.py` is the single owner of "what counts as reasoning prose"
(gate 19 consumes it; every future depth survey should too). This suite
pins that contract the way `test_md_fences.py` pins fence semantics: each
classification rule is asserted against a tiny known input, so a silent
change to what the scanner counts cannot ship — a scanner that starts
counting tables or fence content would re-open the exact table-only and
prose-in-code defect classes the scanner exists to close.

Deliberately NOT tested here (boundary decisions, recorded in the module
docstring and the gates doc):
  - reading-weight modeling (code lines / table rows costing time) — that
    is `read_time.py`'s different question, and the two must not merge;
  - the floors (25 words) — those live in `check_answer_depth.py`.

Run directly: python3 scripts/test_prose_scan.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prose_scan

FAILURES = 0


def check(name, lines, want_words):
    global FAILURES
    got = prose_scan.prose_words(lines)
    if got == want_words:
        print(f"ok   {name}")
    else:
        FAILURES += 1
        print(f"FAIL {name}: want {want_words} prose words, got {got}")


check(
    "fence content never counts as prose (the prose-in-code bug class)",
    ["Real sentence stays.", "", "```js", "const looksLikeProse = 'but is code';", "```", "More real prose."],
    3 + 3,
)

check(
    "the fence delimiter line itself is excluded",
    ["```", "not prose", "```"],
    0,
)

check(
    "nested fences: a ``` line inside a ```` block is content, still excluded",
    ["````markdown", "Example:", "", "```text", "inner prose-looking line", "```", "", "outside", "````"],
    0,  # "Example:" sits inside the outer block, so nothing here is prose
)

check(
    "nested fences: prose after the outer block closes resumes counting",
    ["````text", "code code", "````", "", "Real prose after the block."],
    5,
)

check(
    "tables are enumeration, not explanation — excluded (the table-only defect class)",
    ["| Aspect | Behavior |", "| --- | --- |", "| Lookup | Left prefix |"],
    0,
)

check(
    "headings are structure — excluded",
    ["## Definition", "### Sub", "Actual definitional prose appears here."],
    5,
)

check(
    "blockquotes, separators, HTML comments and shields badges are excluded",
    ["> A quote is not the answer body.", "---", "<!-- section: X -->",
     "[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)",
     "Only this line counts."],
    4,
)

check(
    "inline code counts as words: the corpus writes '`npm ci` installs'",
    # naive str.split: backticks fuse with adjacent text (`npm = one token),
    # so Run/`npm/ci`/to/install,/then/`npm/run/build`. = 9 tokens.
    ["Run `npm ci` to install, then `npm run build`."],
    9,
)

check(
    "blank lines contribute nothing",
    ["", "   ", "First line.", "", "", "Second line.", ""],
    4,
)

check(
    "table-only Definition shape (the rule-2 plant) measures zero",
    ["## Definition", "", "| Term | Meaning |", "| --- | --- |", "| Snapshot | Query-time view |", ""],
    0,
)

check(
    "mixed answer shape: prose + table + code counts only the prose",
    ["**Answer:**",
     "",
     "The mechanism is layer immutability — later layers cannot shrink earlier ones.",
     "",
     "| Technique | Impact |",
     "| --- | --- |",
     "| Alpine | Smaller |",
     "",
     "```dockerfile",
     "FROM node:22-alpine",
     "```"],
    # '**Answer:**' = 1; the sentence = 12 under naive split — a spaced
    # em-dash counts as a token. Known quirk, pinned on purpose: the floor
    # is 25 and corpus medians sit near 90, so the inflation is immaterial;
    # changing to regex word-splitting would silently re-baseline every
    # measured claim and is a deliberate decision, not a drive-by fix.
    13,
)

print()
if FAILURES:
    print(f"{FAILURES} case(s) failed — prose_scan's classification drifted; "
          "fix the module, not these expectations.")
    sys.exit(1)
print("prose_scan: classification contract holds.")
sys.exit(0)
