#!/usr/bin/env python3
"""test_check_prose.py — the prose gate's detection contract, pinned.

`check_prose.py` is new, and its first calibration run found **10,154**
"defects" that were really 10,152 false positives: masking code spans with
spaces manufactured double spaces, `Server-side side effects` looked like a
stuttered word, and `apps/web/**` looked like an unbalanced bold run. That is
the failure mode a grammar gate has: one over-broad pattern reports the corpus
as broken and teaches the reader to ignore the gate.

So each rule is pinned twice — it must FIRE on a canonical defect, and it must
stay SILENT on the shape that produced its false positive in calibration.
Repair is pinned for idempotency, because `--write` runs before the gate and a
non-idempotent repair would change the tree on every run.

Run directly: python3 scripts/test_check_prose.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_prose

FAILURES = 0


def findings_for(text):
    """Findings from a whole document written to a temp file."""
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False,
                                     encoding='utf-8') as handle:
        handle.write(text)
        path = handle.name
    try:
        found, _lines = check_prose.scan_file(path)
        return [code for _number, code, _text in found]
    finally:
        os.unlink(path)


def case(name, text, want):
    """Assert the exact multiset of rule codes a document produces."""
    global FAILURES
    got = findings_for(text)
    if sorted(got) == sorted(want):
        print(f"ok   {name}")
    else:
        FAILURES += 1
        print(f"FAIL {name}: want {want}, got {got}")


def repaired(text):
    lines = text.split('\n')
    out = []
    for line in lines:
        out.append(check_prose.repair_line(line, check_prose.mask_prose(line)))
    return '\n'.join(out)


# --- P1: a stutter, but not a hyphenated compound --------------------------
case("P1 fires on a doubled word", "Ask the the server for state.\n", ['P1'])
case("P1 silent on a hyphenated compound",
     "Server-side side effects still happen.\n", [])
case("P1 silent on a header name followed by prose",
     "Setting Retry-After after res.json() is too late.\n", [])
case("P1 silent on a path-like first word",
     "Per-order order matters for distribution.\n", [])

# --- P2: a doubled space, but not indentation or table padding -------------
case("P2 fires between words", "Ask the  server for state.\n", ['P2'])
case("P2 silent on list indentation", "- item\n  - nested item\n", [])
case("P2 silent on table padding", "| a |  b  |\n|---|---|\n", [])
case("P2 silent across a code span", "Use `x` , then `y`.\n", [])

# --- P3: a run-together sentence, but not abbreviations or versions --------
case("P3 fires on a run-together sentence",
     "Retry is bounded.Next request starts fresh.\n", ['P3'])
case("P3 silent on e.g.", "Use a bound, e.g. This one.\n", [])

# --- P4: a space before punctuation, but not inside a code span ------------
case("P4 fires before a comma", "The timeout , then retry.\n", ['P4'])
case("P4 silent inside a code span", "Pass `a , b` as one argument.\n", [])

# --- P5: duplicated punctuation, but not an ellipsis ----------------------
case("P5 fires on a doubled comma", "Retry,, then stop.\n", ['P5'])
case("P5 silent on an ellipsis", "It waits... then returns.\n", [])

# --- P6: an article against a closed pronunciation list -------------------
case("P6 fires on 'a hour'", "You wait a hour before retrying.\n", ['P6'])
case("P6 fires on 'an user'", "An user requests the report.\n", ['P6'])
case("P6 silent on 'an hour'", "You wait an hour before retrying.\n", [])
case("P6 silent on 'a user'", "A user requests the report.\n", [])
case("P6 silent on acronyms whose sound the author chooses",
     "An API, a URL, an HTML page.\n", [])

# --- P7: an unbalanced bold run, but not a glob ---------------------------
case("P7 fires on an unclosed bold run", "This is **unfinished bold.\n", ['P7'])
case("P7 silent on a balanced run", "This is **finished** bold.\n", [])
case("P7 silent on bold that contains a glob", "The **projects/** folder.\n", [])
case("P7 silent on a glob alone", "Match src/**/*.ts in the filter.\n", [])

# --- fence and comment exclusion -----------------------------------------
case("fenced code is never scanned",
     "Real prose stays.\n\n```js\nconst the the = 1;\n```\n", [])
case("the metadata comment is never scanned",
     "<!-- section: X | tags: the the -->\n\nProse.\n", [])

# --- repair: idempotent, and offsets stay valid across code spans --------
FIXTURE = ("Ask the the server  for state.Next call retries , then stops,,\n"
           "Use `a , b` and `the  the` and `src/**/*.ts`.\n")
ONCE = repaired(FIXTURE)
TWICE = repaired(ONCE)
if ONCE == TWICE:
    print("ok   repair is idempotent")
else:
    FAILURES += 1
    print(f"FAIL repair is not idempotent:\n  once:  {ONCE!r}\n  twice: {TWICE!r}")

if "Ask the server for state. Next call retries, then stops," in ONCE:
    print("ok   repair fixes P1, P2, P3, P4 and P5 in one pass")
else:
    FAILURES += 1
    print(f"FAIL repair result unexpected: {ONCE!r}")

if "`a , b`" in ONCE and "`src/**/*.ts`" in ONCE:
    print("ok   repair leaves code spans byte-identical")
else:
    FAILURES += 1
    print(f"FAIL repair touched a code span: {ONCE!r}")

if FAILURES:
    print(f"\n{FAILURES} case(s) failed")
    sys.exit(1)
print("\nall check_prose cases pass")
