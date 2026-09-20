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

Honest exclusions — gates that need corpus-scale or git context and thus
cannot fire deterministically in a sandbox:
  - check_cross_refs / check_duplication / check_topic_twins /
    check_first_principles: need real corpus structure for their
    thresholds and baselines to mean anything;
  - check_freshness: its rules anchor to content-file contexts, not bare
    snippets;
  - link_baseline (diff): needs git history to diff against;
  - read_time / gen_master_index --check / wiring's count restamp: these
    are byte-lock/self-restamp designs — their verify-time run IS the
    plant test (any drift fails);
  - test_md_fences / test_fixers: already suites themselves (gates 16/17).

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
]


def build_sandbox(tmp, files, real_copies, dirs=()):
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
            build_sandbox(clean_tmp, clean_files, clean_real, case.get("dirs", ()))
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
