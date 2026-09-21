#!/usr/bin/env python3
"""The suite self-test: proves the gates still CATCH, not just that the
corpus currently passes.

Every new rule this session added was plant-tested once, at creation, and
never again. A gate that silently stops firing — after a refactor, a path
change, an over-eager "cleanup" — would keep reporting green forever, and
the one thing gates 15-17 do not watch is detection itself. This closes
that gap: for each sandboxable gate, plant its canonical defect in a temp
tree and assert the gate exits non-zero (fire side); then run the same
gate against clean content — including a real, currently-passing corpus
chapter — and assert it exits zero (clean side, so a gate that fires on
everything cannot pass).

Sandbox: every script derives its repo root from __file__, so copying
scripts/ into a temp tree redirects all scanning there. The real corpus is
never touched.

Honest exclusions — gates that need git history or corpus-scale state and
cannot fire deterministically in a sandbox:
  - link_baseline (diff): needs git history to diff against;
  - check_topic_twins / check_first_principles: need real corpus baselines
    (twin maps, coverage floors) to mean anything;
  - read_time / gen_master_index --check / wiring's count restamp: these
    are byte-lock/self-restamp designs — their verify-time run IS the
    plant test (any drift fails);
  - test_md_fences / test_fixers: already suites themselves (gates 16/17).

The corpus-scale gates ARE coverable — but only with realistic plants:
check_cross_refs, check_freshness and check_duplication all recognize
chapter-shaped input (real directory structure, template-compliant files,
fence-anchored rules), and their cases below use exactly that. Naive
plants (bare snippets) do not fire, which is itself a fact worth having
pinned: these gates are calibrated against real corpus shape.

Exits 0 when every case passes. Run directly: python3 scripts/test_gates.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNNER = sys.executable

# A real chapter that passes the template gate today — the clean-side
# control for check_template (a gate broken to fire on everything must
# fail this case).
REAL_CHAPTER = os.path.join(
    ROOT, "40-platform", "40.1-docker", "40.1.05-dockerfile-best-practices.md"
)

# Template-compliant chapter bodies for the duplication case (metadata + H1
# + How It Works + Summary are what check_duplication's section scanner
# recognizes as non-template sections).
_DUP_TEXT_A = "\n".join(
    f"Sentence {i} about connection pooling behavior with distinct wording {i}."
    for i in range(30)
)
_DUP_META = "<!-- section: Platform | category: Architecture | tags: concept -->\n"
DUP_BODY_A = (
    f"{_DUP_META}\n# Dup Chapter\n\n## How It Works\n\n{_DUP_TEXT_A}\n\n"
    f"## Summary\n\nSame {_DUP_TEXT_A[:200]}\n"
)
_DUP_TEXT_B = "\n".join(
    f"Alternative {i} covering queue backpressure with different phrasing {i}."
    for i in range(30)
)
DUP_BODY_B = (
    f"{_DUP_META}\n# Dup Chapter\n\n## How It Works\n\n{_DUP_TEXT_B}\n\n"
    f"## Summary\n\nSame {_DUP_TEXT_B[:200]}\n"
)

# A fully template-compliant interview bank (metadata, four '#' badges,
# blockquote TL;DR claim, Q1..Q25 markers, nested-fence example inside a
# 4-backtick wrapper). The nested example carries a literal '**Q99' line:
# under the naive fence toggle it was counted as a question, so a claim of
# 26 looked honest while the bank held 25. Under md_fences the literal is
# content and the over-claim fires. The clean variant claims 25 and passes.
_BANK_QS = "\n".join(
    f"**Q{i}:** Question {i} about databases?\n\nAnswer {i} with enough depth."
    for i in range(1, 26)
)
_BANK_NESTED = (
    "````markdown\nExample embed:\n\n```text\n"
    "**Q99: A literal example question, not a real one**\n"
    "```\n\nEnd of example.\n````\n"
)
_BANK_META = (
    "<!-- section: Backend | category: Interview | tags: interview-questions -->\n"
    "[![Section](https://img.shields.io/badge/section-Backend-blue)](#)\n"
    "[![Category](https://img.shields.io/badge/category-Interview-orange)](#)\n"
    "[![Tags](https://img.shields.io/badge/tags-interview--questions-lightgrey)](#)\n"
    "[![Read time](https://img.shields.io/badge/read--time-30_min-informational)](#)\n"
)

def _bank(claim):
    return (
        f"{_BANK_META}\n# Database Interview Bank\n\n"
        f"> {claim} questions on databases, senior depth.\n\n"
        f"## TL;DR\n\n{claim} questions.\n\n"
        f"## First Principles\n\nDatabases reward designs that assume failure.\n\n"
        f"## Interview Questions\n\n"
        f"{_BANK_QS}\n\n## Summary\n\n{_BANK_NESTED}Covers databases.\n\n"
        f"## See Also\n\n- [PostgreSQL Foundations](../01-postgresql-foundations/INDEX.md)\n\n"
        f"## References & Learn More\n\n- None\n"
    )

BANK_OVER_CLAIM = _bank(26)
BANK_CLEAN = _bank(25)

CASES = [
    {
        "name": "gate 2 alignment fires on unspaced tables",
        "gate": "check_alignment.py",
        "args": [],
        "plant": {"p.md": "before\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"},
        "clean": {"p.md": "before\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n"},
    },
    {
        "name": "gate 4 links fires on broken internal links",
        "gate": "check_links.py",
        "args": [],
        "plant": {"p.md": "text\n\n[broken](no-such-file.md)\n"},
        "clean": {"a.md": "[ok](b.md)\n", "b.md": "target\n"},
    },
    {
        "name": "gate 8 whitespace fires on trailing ws in fences",
        "gate": "check_code_whitespace.py",
        "args": [],
        "plant": {"p.md": "text\n\n```js\nconst y = 3;   \n```\n"},
        "clean": {"p.md": "text\n\n```js\nconst y = 3;\n```\n"},
    },
    {
        "name": "gate 1 counts fires on a drifted Files badge",
        "gate": "check_counts.py",
        "args": [],
        "dirs": ["20-backend"],   # compute_live reads the sub-stack scaffold
        "plant": {
            "INDEX.md": (
                "> files\n\n# I\n\n"
                "[![Files](https://img.shields.io/badge/files-99-blue)](INDEX.md)\n\n"
                "| File | Why |\n| ---- | --- |\n"
            )
        },
        "clean": {"note.md": "plain chapter, no nav surface\n"},
    },
    {
        "name": "gate 3 structure fires on two H1s",
        "gate": "check_structure.py",
        "args": [],
        "plant": {"p.md": "# A\n\nx\n\n# B\n\ny\n"},
        "clean": {"p.md": "# A\n\nx\n\n## Sub\n\ny\n"},
    },
    {
        "name": "gate 8c box width fires on over-padded boxes",
        "gate": "fix_box_width.py",
        "args": ["--check"],
        "plant": {
            "p.md": (
                "# T\n\n```text\n"
                "┌──────────────────────────────────────────┐\n"
                "│ hello                                    │\n"
                "│ world                                    │\n"
                "└──────────────────────────────────────────┘\n"
                "```\n"
            )
        },
        "clean": {
            "p.md": (
                "# T\n\n```text\n"
                "┌────────────┐\n"
                "│ hello      │\n"
                "│ world      │\n"
                "└────────────┘\n"
                "```\n"
            )
        },
    },
    {
        "name": "gate 6b template fires on missing metadata (clean: real chapter)",
        "gate": "check_template.py",
        "args": [],
        "plant": {"p.md": "x\n"},
        "clean_real": [REAL_CHAPTER],
    },
    {
        "name": "gate 6b question-claim fires through a nested-fence example",
        "gate": "check_template.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_OVER_CLAIM,
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_CLEAN,
        },
    },
    {
        "name": "gate 10 cross-refs fires on a dangling → N.N ref",
        "gate": "check_cross_refs.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-t.md": (
                "# T\n\nDetails at → 20.4.9.\n"
            )
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-t.md": (
                "# T\n\nMechanism chapter.\n"
            ),
            "10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-x.md": (
                "# X\n\nSee → 20.4.1 for the mechanism.\n"
            ),
        },
        "dirs_clean": [
            "10-frontend/10.1-javascript/01-execution-and-scope",
            "20-backend/20.4-database/01-postgresql-foundations",
        ],
    },
    {
        "name": "gate 5 freshness fires on a stale signature in a real chapter shape",
        "gate": "check_freshness.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-f.md": (
                "text\n\n```js\nconst u = url.parse(req.url);\n```\n"
            )
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-f.md": (
                "text\n\n```js\nconst u = new URL(req.url);\n```\n"
            )
        },
    },
    {
        "name": "gate 11 duplication fires on identical sections across stacks",
        "gate": "check_duplication.py",
        "args": ["--strict"],
        "dirs": [
            "10-frontend/10.1-javascript/01-execution-and-scope",
            "20-backend/20.4-database/01-postgresql-foundations",
        ],
        "plant": {
            "10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-d.md": DUP_BODY_A,
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-d.md": DUP_BODY_A,
        },
        "clean": {
            "10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-d.md": DUP_BODY_A,
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-d.md": DUP_BODY_B,
        },
    },
    {
        # The table-only defect class the 2026-09-21 probe found: a table
        # plus one label line reads as zero prose under the depth gate.
        "name": "gate 19 answer-depth fires on a table-only answer",
        "gate": "check_answer_depth.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": (
                "# Interview Bank\n\n"
                "### Question 1: What is a composite index?\n\n"
                "**Answer:**\n\n"
                "| Aspect | Behavior |\n| --- | --- |\n"
                "| Lookup | Left prefix |\n| Sort | Matches order |\n"
            )
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": (
                "# Interview Bank\n\n"
                "### Question 1: What is a composite index?\n\n"
                "**Answer:**\n\n"
                "A composite index orders by its column list, so lookups match the "
                "leftmost prefix — the mechanism behind the rule. Column order also "
                "decides whether an ORDER BY avoids a sort node entirely, and whether "
                "the index can serve the query covering.\n\n"
                "| Aspect | Behavior |\n| --- | --- |\n"
                "| Lookup | Left prefix |\n| Sort | Matches order |\n"
            )
        },
    },
]


def build_sandbox(tmp, files, real_copies, dirs=()):  # noqa: ARG001
    scripts = os.path.join(tmp, "scripts")
    os.makedirs(scripts, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith((".py", ".sh", ".json")):
            shutil.copy(os.path.join(HERE, fn), scripts)
    for d in dirs:
        os.makedirs(os.path.join(tmp, d), exist_ok=True)
    for rel, content in files.items():
        path = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    for src in real_copies:
        shutil.copy(src, os.path.join(tmp, os.path.basename(src)))


def run_gate(tmp, gate, args):
    return subprocess.run(
        [RUNNER, os.path.join("scripts", gate), *args],
        cwd=tmp, capture_output=True, text=True,
    )


def main() -> int:
    if not os.path.exists(REAL_CHAPTER):
        print(f"clean-side control chapter missing: {REAL_CHAPTER}")
        return 1
    failures = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as fire_tmp, tempfile.TemporaryDirectory() as clean_tmp:
            build_sandbox(fire_tmp, case["plant"], [], case.get("dirs", ()))
            r = run_gate(fire_tmp, case["gate"], case["args"])
            fire_ok = r.returncode != 0

            clean_files = case.get("clean", {})
            clean_real = case.get("clean_real", [])
            build_sandbox(
                clean_tmp, clean_files, clean_real,
                case.get("dirs_clean", case.get("dirs", ())),
            )
            rc = run_gate(clean_tmp, case["gate"], case["args"])
            clean_ok = rc.returncode == 0

        if fire_ok and clean_ok:
            print(f"ok   {case['name']}")
            continue
        failures += 1
        print(f"FAIL {case['name']}")
        if not fire_ok:
            print(f"  fire side: gate exited 0 on its canonical defect — detection is broken")
            print("  " + (r.stdout.strip() or r.stderr.strip()).replace("\n", "\n  ")[:500])
        if not clean_ok:
            print(f"  clean side: gate exited {rc.returncode} on clean content — it fires on everything")
            print("  " + (rc.stdout.strip() or rc.stderr.strip()).replace("\n", "\n  ")[:500])
    if failures:
        print(f"\n{failures} case(s) failed — a gate's detection drifted; "
              f"fix the gate, then re-verify.")
        return 1
    print(f"\ngates: {len(CASES)}/{len(CASES)} catch their defect and pass clean content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
