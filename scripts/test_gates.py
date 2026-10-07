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

A case may declare only the keys the runner reads, and its content assertions
must carry signal: an unrecognised key, an empty / bare-string assertion, or an
element that cannot discriminate (blank, one character, a verdict word) is
refused before any gate runs. A dropped assertion still prints "ok", which is
the silent-pass class this suite exists to catch.
"""

import os
import re
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

# The scope-floor case (gate 23) needs a synthetic verify.sh of its own: the
# gate derives its table from that file, so the case proves the *rule* without
# depending on today's gate inventory. Every synthetic gate but one fails
# honestly on an empty tree; the odd one out lies (exit 0), which is exactly
# the defect the gate exists to catch. The count must clear
# check_scope_floor.MIN_GATES — otherwise the case would trip the floor itself.
_SCOPE_GATES = 20


def _scope_floor_sandbox(vacuous_index=None):
    """{path: content} for a sandbox whose verify.sh wires _SCOPE_GATES gates."""
    lines = ["#!/usr/bin/env bash", "set -u", "FAIL=0"]
    files = {}
    for i in range(1, _SCOPE_GATES + 1):
        name = f"g{i:02d}"
        lines += [
            f'echo "{i}/{_SCOPE_GATES} {name}.py — synthetic gate for the scope-floor case"',
            f'echo "     python3 scripts/{name}.py"',
            'echo "------------------------------------------------------------"',
            f"if python3 scripts/{name}.py; then",
            '    echo "  PASS"',
            "else",
            "    FAIL=1",
            "fi",
            "",
        ]
        if i == vacuous_index:
            files[f"scripts/{name}.py"] = (
                "import sys\n"
                "print('Code-block whitespace: OK (0 trailing-ws, 0 unbalanced fences)')\n"
                "sys.exit(0)\n"
            )
        else:
            files[f"scripts/{name}.py"] = (
                "import sys\n"
                "print('SCOPE ERROR — 0 markdown files found.')\n"
                "sys.exit(1)\n"
            )
    lines += ['if [ "$FAIL" -eq 0 ]; then',
              '    echo "All checks passed — tree is clean."',
              "    exit 0", "fi", "exit 1", ""]
    files["scripts/verify.sh"] = "\n".join(lines)
    return files

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
        f"## First Principles\n\nDatabases reward designs that assume failure.\n\n"
        f"## Interview Questions\n\n"
        f"{_BANK_QS}\n\n## Summary\n\n{_BANK_NESTED}Covers databases.\n\n"
        f"## See Also\n\n- [PostgreSQL Foundations](../01-postgresql-foundations/INDEX.md)\n\n"
        f"## References & Learn More\n\n- None\n"
    )

BANK_OVER_CLAIM = _bank(26)
BANK_CLEAN = _bank(25)

FLOW_CLEAN = (
    _BANK_META.replace('category: Interview', 'category: Backend')
    .replace('category-Interview-orange', 'category-Backend-orange')
    + '\n# Database Transactions\n\n'
    '## Definition\n\nA transaction groups changes into one commit decision.\n\n'
    '> **Textbook Definition:** A transaction is a unit of database work with a shared commit or abort outcome.\n\n'
    '## First Principles\n\nPartial failure requires a shared commit boundary.\n\n'
    '## Code Examples\n\n```sql\nBEGIN;\nCOMMIT;\n```\n\n'
    '## Summary\n\nChoose isolation for the invariants you need to protect.\n\n'
    '## See Also\n\nReview the database section.\n\n'
    '## References & Learn More\n\nConsult the database documentation.\n'
)

# Rule 4: a Cheat Sheet fence holding fewer than THIN_SHEET_MIN_LINES content
# lines is a sheet that was added but never populated (the generator-gap
# family from 2535a0b4). The compliant bank gains a thin sheet; the clean
# side is the unmodified bank. Isolates the thin-sheet rule from the rest.
REVISION_CLEAN = (
    _BANK_META.replace('category: Interview', 'category: Reference')
    .replace('category-Interview-orange', 'category-Reference-lightgrey')
    + '\n# Transactions — Revision\n\n'
    '## Database Transactions\n\nSource: [Database Transactions](p.md)\n\n'
    + ''.join(f'**Q:** Which invariant does case {i} protect?\n**A:** The stated commit boundary.\n\n' for i in range(5))
    + '## Summary\n\nExplain the decision before checking the source.\n\n'
    '## See Also\n\nRead the learning chapter.\n\n'
    '## References & Learn More\n\nSee the source references.\n'
)

BANK_THIN_SHEET = BANK_CLEAN.replace(
    "## See Also",
    "## Cheat Sheet\n\n```text\nDATABASE BANK QUICK REFERENCE\n\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n```\n\n## See Also", 1)

# The compliant bank plus exactly one defect: an empty fence (opener immediately
# followed by a closer) — the stray-delimiter fingerprint that collapsed 24
# cheat sheets on 2026-09-21. Isolates fence rule 3 from all other checks.
BANK_EMPTY_FENCE = BANK_CLEAN.replace(
    "## First Principles", "```\n```\n\n## First Principles", 1)

def _wiring_sandbox():
    """{path: content} for a sandbox whose only defect is a workflow's trigger paths.

    The tooling is real — build_sandbox copies every script, so verify.sh, its
    gate inventory and the count claims in contributing.md all agree — and the
    single planted defect is a workflow whose `paths:` filter omits a gate
    script it actually runs.
    """
    plant = {
        rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for rel in ("contributing.md", os.path.join("docs", "verification-gates.md"))
    }
    plant[".github/workflows/narrow.yml"] = (
        "name: narrow\n\non:\n  push:\n    paths:\n"
        "      - 'scripts/check_links.py'\n"
        "      - 'scripts/verify.sh'\n\n"
        "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - name: gates\n"
        "        run: |\n"
        "          python3 scripts/check_study_live.py --print-contract\n"
        "          python3 scripts/test_study_live.py\n"
        "          python3 scripts/check_links.py\n"
        "          python3 scripts/check_alignment.py\n"
        "          bash scripts/verify.sh\n"
    )
    return plant


def _edge_trigger_sandbox():
    """{path: content} whose only defect is a filter blind to what it verifies.

    The real tooling, the real count claims, and one planted workflow that
    renders the site — `**.md` only — beside the edge tree it is supposed to
    cover. Rule 9 cannot see this defect: the workflow runs no gate script, so
    there is no invocation to check. Rule 11 exists for exactly this shape.
    """
    plant = {
        rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for rel in ("contributing.md", os.path.join("docs", "verification-gates.md"))
    }
    plant["functions/_middleware.ts"] = "export const onRequest = () => new Response(null);\n"
    plant[".github/workflows/site-build.yml"] = (
        "name: site-build\n\non:\n  push:\n    paths:\n"
        "      - '**.md'\n\n"
        "jobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - name: render\n        run: echo render\n"
    )
    # The other declared workflow, healthy, so the fire is attributable to the
    # blind filter rather than to the staleness branch that a missing name
    # would also trip.
    plant[".github/workflows/study-live.yml"] = (
        "name: study-live\n\non:\n  push:\n    paths:\n"
        "      - 'functions/**'\n      - 'auth/**'\n\n"
        "jobs:\n  probe:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - name: probe\n        run: echo probe\n"
    )
    return plant


def _unwired_suite_sandbox():
    """{path: content} whose only defect is a Functions suite no workflow runs.

    The tooling is real and the tree is otherwise coherent, so the single
    planted defect is a `functions/*.test.mjs` that no workflow step invokes.
    """
    plant = {
        rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for rel in ("contributing.md", os.path.join("docs", "verification-gates.md"))
    }
    plant["functions/orphan.test.mjs"] = "import test from 'node:test';\n"
    plant[".github/workflows/only.yml"] = (
        "name: only\n\non:\n  push: {}\n\njobs:\n  j:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - name: policy\n"
        "        run: node --test functions/_lib/study-access.test.mjs\n"
    )
    return plant


# The ownership fixtures (wiring rules 12-13, gate 1's homepage claim, gate
# 26's ceilings). The map ones plant the exact defects the 2026-09-27 pass
# removed: the map was missing the two live-probe scripts, its gate counts
# said 21/20, and the theme key had a second implementation.
_REAL_MAP = open(os.path.join(ROOT, "docs", "scripts-map.md"), encoding="utf-8").read()
_MAP_DROPS_SCRIPT = _REAL_MAP.replace("check_study_live.py", "check_live_probe.py")
_MAP_STALE_COUNT = _REAL_MAP.replace("30-gate", "21-gate")
_MAP_STALE_ROW = _REAL_MAP + (
    "\n- `check_ghosts.py` — a stale row planted by the sandbox: it names a "
    "script that does not exist.\n")
# The theme key is built from a split literal on purpose: rule 13 scans every
# code-bearing file — this fixture source included — so it must not itself
# contain the key it plants. (The checker is the one file exempt, because a
# rule has to name what it looks for.)
_THEME_KEY = "sdb-" "theme"
# The old two-owner shape of the theme *load path*: the include's
# `site.theme_asset` resolved back to a literal. Rule 13's load-path case
# plants this again.
_REAL_HEAD = open(os.path.join(ROOT, "_includes", "head-custom.html"),
                  encoding="utf-8").read()
_HEAD_HARDCODES = _REAL_HEAD.replace("site.theme_asset", "'/assets/theme.js'")
# The live probe's routing sources (scripts/check_study_live.py resolves them
# before it probes anything). The plants mirror the refactors that used to
# silently empty the must-answer-200 set: the intercept declaration re-spelled
# with single quotes, declared as a Set, and the adapter reimplementing the
# check inline with startsWith.
_REAL_ACCESS = open(os.path.join(ROOT, "functions", "_lib", "study-access.mjs"),
                    encoding="utf-8").read()
_REAL_ADAPTER = open(os.path.join(ROOT, "functions", "_middleware.ts"),
                     encoding="utf-8").read()
_ACCESS_SINGLE_QUOTES = _REAL_ACCESS.replace(
    '["/auth/callback.html", "/auth/callback"]',
    "['/auth/callback.html', '/auth/callback']")
# One single-quoted entry among double-quoted ones: a partially parsed list —
# the shape that used to drop the entry while the gate stayed green.
_ACCESS_MIXED_QUOTES = _REAL_ACCESS.replace(
    '  "/favicon.svg",',
    "  '/auth/refresh'," + chr(10) + '  "/favicon.svg",')
# Notes around the paths are prose, not entries: they must leave the surface
# resolvable. The old reader reported the note *and the path after it* as one
# unresolvable entry, which sent a maintainer to the wrong line (audit).
_ACCESS_COMMENTED = _REAL_ACCESS.replace(
    '  "/auth/login",',
    "  // legacy alias kept for old links" + chr(10)
    + '  "/auth/login", // trailing note' + chr(10)
    + "  /* block note */")
_ACCESS_COMMENTED_UNRESOLVED = _ACCESS_COMMENTED.replace(
    '  "/auth/logout",',
    "  // the older alias, still single-quoted" + chr(10) + "  '/auth/logout',")
_ACCESS_SET = _REAL_ACCESS.replace(
    'export const INTERCEPTED_PATHS = ["/auth/callback.html", "/auth/callback"];',
    'export const INTERCEPTED_PATHS = '
    'new Set(["/auth/callback.html", "/auth/callback"]);')
# The public declaration emptied: the reachable half of the emptied-surface
# refusal. An empty body is named and refused by the reader, so the loudness a
# dead check used to claim is pinned where it can actually fire.
_ACCESS_NO_PUBLIC = re.sub(r"new Set\(\[.*?\]\)", "new Set([])", _REAL_ACCESS,
                           count=1, flags=re.S)
_ADAPTER_INLINE = _REAL_ADAPTER.replace(
    "  INTERCEPTED_PATHS,\n", "").replace(
    "if (INTERCEPTED_PATHS.includes(url.pathname)) {",
    "if (url.pathname.startsWith('/auth/callback')) {")


def _owners_sandbox(map_text=None, extra=None):
    """{path: content} for a sandbox whose only defect is in a map/theme claim.

    The tooling, the count claims, the workflows and the shared theme files —
    `_config.yml`, `assets/theme.js` and both consumers — are the real ones, so
    rules 1-11 behave exactly as they do in the repo and a fire is attributable
    to the one planted map/theme defect; the sandbox exercises the shipped
    ownership layout rather than a stub.
    """
    files = {
        rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for rel in ("contributing.md", os.path.join("docs", "verification-gates.md"),
                    os.path.join("docs", "scripts-map.md"), "assets/theme.js",
                    "_config.yml", os.path.join("_includes", "head-custom.html"))
    }
    wf = os.path.join(ROOT, ".github", "workflows")
    for name in sorted(os.listdir(wf)):
        rel = os.path.join(".github", "workflows", name)
        files[rel] = open(os.path.join(wf, name), encoding="utf-8").read()
    if map_text is not None:
        files[os.path.join("docs", "scripts-map.md")] = map_text
    files.update(extra or {})
    return files


def _live_source_sandbox(access=None, adapter=None):
    """{path: content} for a sandbox whose only defect is the routing source.

    `check_study_live.py` resolves these two files before it probes anything,
    so `--print-contract` exercises the resolution offline: a plant the
    resolver cannot read must exit non-zero, never print a contract for a
    surface it could not see.
    """
    return {
        os.path.join("functions", "_lib", "study-access.mjs"):
            _REAL_ACCESS if access is None else access,
        os.path.join("functions", "_middleware.ts"):
            _REAL_ADAPTER if adapter is None else adapter,
    }


_DUP_TOPICS = ("invoice", "shipment", "webhook", "session", "payment", "catalog",
               "ticket", "message", "profile", "analytics", "gateway", "receipt")


def _dup_pair_sandbox(pairs, reword=True):
    """{path: content} holding exactly `pairs` cross-file duplicates.

    One >=10-line fenced example per topic per file. `reword` renames one
    identifier in the second file's copy, so each pair is near (Jaccard ~0.95)
    instead of raw-identical; the topics share no vocabulary, so cross-topic
    pairs stay far below the 0.80 threshold and the measured count is exactly
    `pairs` — which is what a ceiling case needs to pin a number.
    """
    def block(topic, renamed):
        stem = "aggregate" if renamed else "sum"
        head = topic.capitalize()
        return "\n".join([
            f"export function {topic}Reconcile({topic}Input: {head}Payload) {{",
            f"  const {topic}Total = {stem}{head}Lines({topic}Input.rows);",
            f"  if ({topic}Total === 0) return {topic}Retry({topic}Input, 30);",
            f'  await {topic}Persist({topic}Total, "{topic} ledger entry");',
            f'  return build{head}Report({topic}Total, "{topic} snapshot detail");',
            "}",
            f"export const {topic}TimeoutMs = 45000;",
            f"export function {topic}Healthy({topic}Total: number): boolean {{",
            f"  return {topic}Total <= {topic}TimeoutMs;",
            "}",
        ])

    def fenced(blocks):
        return "".join(f"# T{i}\n\n```typescript\n{b}\n```\n\n"
                       for i, b in enumerate(blocks))

    return {
        "10-frontend/a.md": fenced(block(t, False) for t in _DUP_TOPICS[:pairs]),
        "10-frontend/b.md": fenced(block(t, reword) for t in _DUP_TOPICS[:pairs]),
    }


CASES = [
    {
        "name": 'gate 5 rejects replay called on a live Temporal Worker instance',
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            '40-platform/40.7-serverless-edge/40.7.07-durable-execution-temporal-inngest.md': (
                '# Replay\n'
                '\n'
                '```typescript\n'
                "import { Worker } from '@temporalio/worker';\n"
                'const worker = await Worker.create({ workflowsPath });\n'
                'await worker.runReplayHistories(histories);\n'
                '```\n'
            ),
        },
        "clean": {
            '40-platform/40.7-serverless-edge/40.7.07-durable-execution-temporal-inngest.md': (
                '# Replay\n'
                '\n'
                '```typescript\n'
                "import { Worker } from '@temporalio/worker';\n"
                'await Worker.runReplayHistory({ workflowsPath }, history);\n'
                'for await (const result of Worker.runReplayHistories({ workflowsPath }, histories)) { console.log(result); }\n'
                '```\n'
            ),
        },
    },
    {
        "name": 'gate 5 rejects static ScrollTrigger.kill',
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            '10-frontend/10.6-animation/10.6.03-gsap.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                'ScrollTrigger.kill();\n'
                '```\n'
            ),
        },
        "clean": {
            '10-frontend/10.6-animation/10.6.03-gsap.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                'trigger.kill();\n'
                '```\n'
            ),
        },
    },
    {
        "name": 'gate 5 rejects CSS easing strings in GSAP',
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            '10-frontend/10.6-animation/10.6.03-gsap.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "gsap.to('.box', { ease: 'cubic-bezier(0.4, 0, 0.2, 1)' });\n"
                '```\n'
            ),
        },
        "clean": {
            '10-frontend/10.6-animation/10.6.03-gsap.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "gsap.to('.box', { ease: 'power2.out' });\n"
                '// CSS cubic-bezier is valid in CSS, not a GSAP ease string.\n'
                '```\n'
            ),
        },
    },
    {
        "name": 'gate 5 rejects obsolete built-in PubSub iterator',
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            '20-backend/20.7-graphql/02-execution/20.7.2.02-apollo-server.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "import { PubSub } from 'graphql-subscriptions';\n"
                'const pubsub = new PubSub();\n'
                "pubsub.asyncIterator('EVENT');\n"
                '```\n'
            ),
        },
        "clean": {
            '20-backend/20.7-graphql/02-execution/20.7.2.02-apollo-server.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "import { PubSub } from 'graphql-subscriptions';\n"
                'const pubsub = new PubSub();\n'
                "pubsub.asyncIterableIterator('EVENT');\n"
                'const redis = new RedisPubSub();\n'
                "redis.asyncIterator('EVENT');\n"
                '```\n'
            ),
        },
    },
    {
        "name": 'gate 5 rejects fabricated graphql-ws import',
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            '20-backend/20.7-graphql/02-execution/20.7.2.02-apollo-server.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "import { useServer } from 'ws.use/server';\n"
                '```\n'
            ),
        },
        "clean": {
            '20-backend/20.7-graphql/02-execution/20.7.2.02-apollo-server.md': (
                '# API example\n'
                '\n'
                '```typescript\n'
                "import { useServer } from 'graphql-ws/use/ws';\n"
                '```\n'
            ),
        },
    },
    {
        'name': 'gate 6b checks fence grammar in operational Markdown too',
        'gate': 'check_template.py', 'args': [],
        'plant': {'p.md': FLOW_CLEAN, 'docs/example.md': '# Example\n\n```text\nUnclosed sample\n'},
        'clean': {'p.md': FLOW_CLEAN, 'docs/example.md': '# Example\n\n```text\nClosed sample\n```\n'},
    },

    {
        'name': 'gate 6b requires a revision companion for indexed learning sections',
        'gate': 'check_template.py', 'args': [],
        'plant': {'learning/p.md': FLOW_CLEAN, 'learning/INDEX.md': '# Learning Index\n'},
        'clean': {'learning/p.md': FLOW_CLEAN, 'learning/INDEX.md': '# Learning Index\n', 'learning/REVISION.md': REVISION_CLEAN},
    },
    {
        'name': 'gate 6b rejects revision stubs and missing source coverage',
        'gate': 'check_template.py', 'args': [],
        'plant': {'p.md': FLOW_CLEAN, 'REVISION.md': REVISION_CLEAN.replace('](p.md)', '](wrong.md)').replace('**Q:**', '**Prompt:**')},
        'clean': {'p.md': FLOW_CLEAN, 'REVISION.md': REVISION_CLEAN},
    },

    {
        'name': 'gate 6b rejects retired TLDR while accepting definition-first flow',
        'gate': 'check_template.py',
        'args': [],
        'plant': {'p.md': FLOW_CLEAN.replace('## Definition', '## TL;DR\n\nDuplicate overview.\n\n## Definition', 1)},
        'clean': {'p.md': FLOW_CLEAN},
    },
    {
        'name': 'gate 6b rejects a duplicate cheat sheet inside a concept',
        'gate': 'check_template.py', 'args': [],
        'plant': {'p.md': FLOW_CLEAN.replace('## See Also', '## Cheat Sheet\n\nA duplicate recap of the concept.\n\n## See Also', 1)},
        'clean': {'p.md': FLOW_CLEAN},
    },
    {
        'name': 'gate 6b keeps revision questions outside learning chapters',
        'gate': 'check_template.py',
        'args': [],
        'plant': {'p.md': FLOW_CLEAN.replace('## See Also', '## Revision Questions\n\n**Q:** What is a transaction?\n**A:** One commit boundary.\n\n## See Also', 1)},
        'clean': {'p.md': FLOW_CLEAN},
    },
    {
        "name": "gate 2 rejects a table attached to a horizontal rule",
        "gate": "check_alignment.py", "args": [],
        "plant": {"p.md": "| A | B |\n| --- | --- |\n| 1 | 2 |\n---\n"},
        "clean": {"p.md": "| A | B |\n| --- | --- |\n| 1 | 2 |\n\n---\n"},
    },
    {
        "name": "gate 2 rejects a table attached to a heading",
        "gate": "check_alignment.py", "args": [],
        "plant": {"p.md": "### Cases\n| A | B |\n| --- | --- |\n| 1 | 2 |\n"},
        "clean": {"p.md": "### Cases\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n````markdown\n### Example\n| A | B |\n| --- | --- |\n| 1 | 2 |\n````\n"},
    },
    {
        "name": "gate 2 alignment fires on unspaced tables",
        "gate": "check_alignment.py",
        "args": [],
        "plant": {"p.md": "before\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"},
        "clean": {"p.md": "before\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n"},
    },
    {
        "name": "gate 4 checks navigation and headings inside whole-chapter raw wrappers",
        "gate": "check_links.py",
        "args": [],
        "plant": {
            "source.md": "{% raw %}\n# Source\n[Missing](missing.md)\n{% endraw %}\n",
        },
        "clean": {
            "source.md": "{% raw %}\n# Source\n[Details](target.md#details)\n{% endraw %}\n",
            "target.md": "{% raw %}\n# Target\n## Details\nReal section.\n{% endraw %}\n",
            "example.md": "# Example\n{% raw %}\n[Example only](not-real.md)\n{% endraw %}\n",
        },
    },
    {
        "name": "gate 4 links fires on broken internal links",
        "gate": "check_links.py",
        "args": [],
        "plant": {"p.md": "text\n\n[broken](no-such-file.md)\n"},
        "clean": {"a.md": "[ok](b.md)\n", "b.md": "target\n"},
    },
    {
        # The 2026-09-21 sweep: 53 prose code spans named files from three
        # earlier numbering generations. The clean side proves the rule's scope
        # — an illustrative path inside the reader's *own* project is not a
        # repo path, and neither is a format illustration.
        "name": "gate 4 links fires on a stale inline repo path",
        "gate": "check_links.py",
        "args": [],
        "plant": {
            "10-frontend/INDEX.md": "# I\n\nRead `10-frontend/10.1-javascript/01-Ghost.md`.\n"
        },
        "clean": {
            "10-frontend/INDEX.md": (
                "# I\n\nRead `10-frontend/10.1-javascript/01-real.md`, "
                "add `docs/runbooks/` to your project, and format "
                "`00-<trace-id>-<flags>`.\n"
            ),
            "10-frontend/10.1-javascript/01-real.md": "# Real\n",
        },
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
        # Clean side = the live repo, and this is the one case that needs it:
        # check_counts computes its live values from the real stack skeleton
        # (20-backend/…, the INDEX tree), so no synthetic temp tree can host a
        # legitimate clean run — and before the scope floor landed, the *fire*
        # side passed on a traceback from the same missing directories rather
        # than on the drifted badge. verify.sh already runs this gate on the
        # real corpus every push; running it here too makes the assertion local.
        "clean_in_repo": True,
    },
    {
        # The homepage hero button's "Search N Chapters" claim had no writer
        # until the 2026-09-27 pass; this pins that check_counts owns it now:
        # a drifted number fires, the live number passes. The stack dir is the
        # scaffold compute_live reads (as in the Files-badge case above), and
        # the two root chapters make the live count 2 rather than 0 — the clean
        # side proves a *non-empty* claim passes.
        "name": "gate 1 counts fires on a drifted homepage search claim",
        "gate": "check_counts.py",
        "args": [],
        "dirs": ["20-backend"],
        "plant": {
            "index.html": "<span>Search 5 Chapters</span>\n",
            "p1.md": "# A\n",
            "p2.md": "# B\n",
        },
        "clean": {
            "index.html": "<span>Search 2 Chapters</span>\n",
            "p1.md": "# A\n",
            "p2.md": "# B\n",
        },
    },
    {
        "name": "gate 3 structure fires on two H1s",
        "gate": "check_structure.py",
        "args": [],
        "plant": {"p.md": "# A\n\nx\n\n# B\n\ny\n"},
        "clean": {"p.md": "# A\n\nx\n\n## Sub\n\ny\n"},
    },
    {
        # The 2026-09-21 sweep found exactly one of these on disk (an H2
        # immediately followed by its own H3 twin); the clean side proves the
        # rule ignores the legitimate case — the same label at ### under a
        # different parent, separated by content.
        "name": "gate 3 structure fires on an adjacent duplicate heading",
        "gate": "check_structure.py",
        "args": [],
        "plant": {"p.md": "# T\n\n## Same\n\n### Same\n\nbody\n"},
        "clean": {
            "p.md": "# T\n\n## Same\n\ncontent\n\n### Same\n\nbody\n"
        },
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
        "name": "gate 6b metadata detects a clipped tag while preserving complete tags",
        "gate": "check_template.py",
        "args": [],
        "plant": {"interview-questions.md": BANK_CLEAN.replace('tags: interview-questions -->', 'tags: interview-question -->')},
        "clean": {"interview-questions.md": BANK_CLEAN},
    },
    {
        "name": "gate 6b requires a formal definition in prose rather than a code example",
        "gate": "check_template.py",
        "args": [],
        "plant": {"p.md": FLOW_CLEAN.replace('> **Textbook Definition:** A transaction is a unit of database work with a shared commit or abort outcome.', '```text\n> **Textbook Definition:** A transaction is a unit of database work with a shared commit or abort outcome.\n```')},
        "clean": {"p.md": FLOW_CLEAN},
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
        "name": "gate 6b raw-wrap fires on an unclosed wrapper (the CI-shipped bug)",
        "gate": "check_template.py",
        "args": [],
        "plant": {"p.md": "{% raw %}\n{{ width: '100%' }}\n"},
        "clean_real": [REAL_CHAPTER],
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
        "name": "gate 5 rejects fabricated Nest LazyModule imports",
        "gate": "check_freshness.py",
        "args": [],
        "dirs": ["20-backend/20.2-nestjs/01-core-architecture"],
        "plant": {
            "20-backend/20.2-nestjs/01-core-architecture/20.2.1.01-modules.md": (
                "# Modules\n\n```typescript\nimport {\n LazyModule,\n} from '@nestjs/core';\n```\n"
            ),
        },
        "clean": {
            "20-backend/20.2-nestjs/01-core-architecture/20.2.1.01-modules.md": (
                "# Modules\n\n```typescript\nimport { LazyModuleLoader } from '@nestjs/core';\n"
                "import { LazyModule } from './lazy.module';\n```\n"
                "\nThere is no framework LazyModule decorator.\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects nonexistent hydrateRoot onHydrated options",
        "gate": "check_freshness.py",
        "args": [],
        "dirs": ["10-frontend/10.3-react/01-react-internals"],
        "plant": {
            "10-frontend/10.3-react/01-react-internals/10.3.1.04-rendering.md": (
                "# Hydration\n\n```tsx\nhydrateRoot(container, <App />, {\n"
                "  onHydrated: () => console.log('ready'),\n});\n```\n"
            ),
        },
        "clean": {
            "10-frontend/10.3-react/01-react-internals/10.3.1.04-rendering.md": (
                "# Hydration\n\n```tsx\nhydrateRoot(container, <App />, {\n"
                "  onRecoverableError: reportError,\n});\n```\n"
                "\n```tsx\nconst widget = { onHydrated: () => {} };\n```\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects removed Next request.geo while accepting Worker geo",
        "gate": "check_freshness.py",
        "args": [],
        "dirs": ["10-frontend/10.4-next.js/02-routing-and-navigation"],
        "plant": {
            "10-frontend/10.4-next.js/02-routing-and-navigation/10.4.2.03-middleware.md": (
                "# Next Middleware\n\n```tsx\nconst country = request.geo?.country;\n```\n"
            ),
        },
        "clean": {
            "10-frontend/10.4-next.js/02-routing-and-navigation/10.4.2.03-middleware.md": (
                "# Next Middleware\n\n```tsx\nconst country = request.headers.get('x-vercel-ip-country');\n```\n"
                "\nLegacy API name: request.geo (removed in Next 15).\n"
            ),
            "40-platform/40.7-serverless-edge/40.7.01-workers.md": (
                "# Worker\n\n```typescript\nconst geo = request.geo;\n```\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects obsolete MSW rest imports including multiline declarations",
        "gate": "check_freshness.py",
        "args": [],
        "dirs": ["50-quality/50.1-testing"],
        "plant": {
            "50-quality/50.1-testing/50.1.01-mocking.md": (
                "# Mocking\n\n```typescript\nimport {\n  rest,\n} from 'msw';\n```\n"
            ),
        },
        "clean": {
            "50-quality/50.1-testing/50.1.01-mocking.md": (
                "# Mocking\n\n```typescript\nimport { http, HttpResponse } from 'msw';\n```\n"
                "\nMSW v1 used rest; current code uses http.\n"
            ),
        },
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
        "name": "gate 5 rejects end-of-life Node runtime pins",
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# CI Runtime\n\n```yaml\n"
                "with:\n  node-version: 20\n````\n"
                "\n```yaml\nRuntime: nodejs18.x\n```\n"
            ),
        },
        "clean": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# CI Runtime\n\n```yaml\n"
                "with:\n  node-version: 22\n````\n"
                "\n```yaml\nRuntime: nodejs22.x\n```\n"
                "\nNode.js 20 reached end-of-life in April 2026.\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects GitHub Actions releases tied to removed Node 20 runner",
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Actions Runtime\n\n```yaml\n"
                "steps:\n  - uses: actions/checkout@v4\n"
                "  - uses: actions/setup-node@v7\n````\n"
            ),
        },
        "clean": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Actions Runtime\n\n```yaml\n"
                "steps:\n  - uses: actions/checkout@v6\n"
                "  - uses: actions/setup-node@v7\n````\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects more action majors pinned to removed Node 20 runner",
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Actions Runtime\n\n```yaml\n"
                "steps:\n"
                "  - uses: actions/deploy-pages@v4\n"
                "  - uses: docker/login-action@v3\n"
                "  - uses: googleapis/release-please-action@v4\n````\n"
            ),
        },
        "clean": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Actions Runtime\n\n```yaml\n"
                "steps:\n"
                "  - uses: actions/deploy-pages@v5\n"
                "  - uses: docker/login-action@v4\n"
                "  - uses: googleapis/release-please-action@v5\n````\n"
            ),
        },
    },
    {
        "name": "gate 5 rejects GitHub Actions pinned to moving branch refs",
        "gate": "check_freshness.py",
        "args": [],
        "plant": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Action Pins\n\n```yaml\n"
                "steps:\n"
                "  - uses: aquasecurity/trivy-action@master\n"
                "  - uses: graphql-hive/graphql-inspector@main\n"
                "````\n"
            ),
        },
        "clean": {
            "40-platform/40.3-ci-cd/01-ci-platforms/40.3.1.01-github-actions.md": (
                "# Action Pins\n\n```yaml\n"
                "steps:\n"
                "  - uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25\n"
                "````\n"
            ),
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
        # Rule 4: a title-only cheat sheet — sheet added, content never
        # generated (the 2535a0b4 family's pure-stub variant).
        "name": "gate 6b fence grammar fires on a title-only cheat sheet",
        "gate": "check_template.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_THIN_SHEET,
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_CLEAN,
        },
    },
    {
        # Rule 3: an empty fence renders as a blank code block — the
        # stray-delimiter fingerprint of the 24-file cheat-sheet collapse.
        "name": "gate 6b fence grammar fires on an empty fence",
        "gate": "check_template.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_EMPTY_FENCE,
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": BANK_CLEAN,
        },
    },
    {
        # The 2026-09-21 navigation-surface sweep: one generator humanized
        # target slugs, leaving acronyms title-cased and 55 labels as raw
        # paths. Rule 2's repair is derived from the target's own H1, so the
        # plant carries a target whose title is the expected label.
        "name": "gate 21 nav labels fire on a path used as the label",
        "gate": "fix_nav_labels.py",
        "args": [],
        "plant": {
            "d/INDEX.md": "# Human Title\n",
            "p.md": "[Next: ../d/index](../d/INDEX.md)\n",
        },
        "clean": {
            "d/INDEX.md": "# Human Title\n",
            "p.md": "[Next: Human Title](../d/INDEX.md)\n",
        },
    },
    {
        # Rule 1: acronyms and brand names have fixed casing that humanizing a
        # slug destroys ("Mvcc", "Cqrs Di", "Typescript").
        "name": "gate 21 nav labels fire on non-canonical acronym casing",
        "gate": "fix_nav_labels.py",
        "args": [],
        "plant": {"p.md": "[Next: Mvcc →](x.md)\n"},
        "clean": {"p.md": "[Next: MVCC →](x.md)\n"},
    },
    {
        # The rarer footer style puts the marker before the bracket
        # (`Next: [CheatSheets →](…)`) instead of inside it; a label the
        # scanner skipped would be a label the gate cannot defend.
        "name": "gate 21 nav labels fire on the marker-outside footer style",
        "gate": "fix_nav_labels.py",
        "args": [],
        "plant": {
            "d/INDEX.md": "# Cheat Sheets — Index\n",
            "p.md": "Next: [CheatSheets →](d/INDEX.md)\n",
        },
        "clean": {
            "d/INDEX.md": "# Cheat Sheets — Index\n",
            "p.md": "Next: [Cheat Sheets →](d/INDEX.md)\n",
        },
    },
    {
        # Rule 3: the label equals its target's title once punctuation and case
        # are folded — the slug-humanization artifact. The clean side is a
        # deliberate *shortening* of the same title, which must be left alone.
        "name": "gate 21 nav labels fire on a slug-humanized label",
        "gate": "fix_nav_labels.py",
        "args": [],
        "plant": {
            "d/INDEX.md": "# useMemo & useCallback\n",
            "p.md": "[Next: Usememo Usecallback](d/INDEX.md)\n",
        },
        "clean": {
            "d/INDEX.md": "# useMemo & useCallback\n",
            "p.md": "[Next: useMemo](d/INDEX.md)\n",
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
    {
        # Rule 2: the same table-only failure mode in a study chapter —
        # a `## Definition` that is a bare comparison table.
        "name": "gate 19 answer-depth fires on a table-only chapter Definition",
        "gate": "check_answer_depth.py",
        "args": [],
        "dirs": ["20-backend/20.4-database/01-postgresql-foundations"],
        "plant": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.02-mvcc.md": (
                "# MVCC\n\n"
                "## Definition\n\n"
                "| Term | Meaning |\n| --- | --- |\n"
                "| Snapshot | Query-time view |\n| Version | Row history |\n"
            )
        },
        "clean": {
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.02-mvcc.md": (
                "# MVCC\n\n"
                "## Definition\n\n"
                "Multiversion concurrency control keeps old row versions so readers "
                "never block writers and writers never block readers — the mechanism "
                "that lets a long report query run beside hot writes without either "
                "stalling. The terms below name the moving parts.\n\n"
                "| Term | Meaning |\n| --- | --- |\n"
                "| Snapshot | Query-time view |\n| Version | Row history |\n"
            ),
            # The gate's scope floor (gate 23, scan_scope) requires it to have
            # read at least one interview bank: a tree with chapters but no
            # banks would let "every answer >= floor" pass over an empty set.
            # So the clean side carries both halves of the gate's contract.
            "20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-interview-questions.md": (
                "# Interview Bank\n\n### Question 1: What is a composite index?\n\n"
                "**Answer:**\n\n"
                "A composite index orders by its column list, so lookups match the "
                "leftmost prefix — the mechanism behind the rule. Column order also "
                "decides whether an ORDER BY avoids a sort node entirely.\n"
            ),
        },
    },
    {
        # The fixed-point contract: a clean tree must be a no-op for every
        # writer. The plant is a stale file a writer WILL edit (trailing
        # whitespace inside a code fence — gate 8's canonical defect, present
        # here precisely because no gate ran over this tree), so the gate has
        # to fail: something in the corpus is one writer away from changing.
        # The clean side is the same file already trimmed.
        "name": "gate 22 fixpoint fires when a writer edits corpus the suite calls clean",
        "gate": "check_fixpoint.py",
        "args": [],
        "plant": {
            "40-platform/40.1-docker/40.1.01-dockerfile.md": (
                "# Dockerfile\n\n```dockerfile\nFROM node:20-alpine\nRUN npm ci   \n```\n"
            )
        },
        "clean": {
            "40-platform/40.1-docker/40.1.01-dockerfile.md": (
                "# Dockerfile\n\n```dockerfile\nFROM node:20-alpine\nRUN npm ci\n```\n"
            )
        },
    },
    {
        # The scope-floor contract: a gate that exits 0 on an empty corpus is
        # invisible to every other test, because its output is the same
        # compliance sentence it prints on a real run. Both sides are synthetic
        # so the case proves the *rule*, not today's gate inventory: a minimal
        # verify.sh lists one gate, and that gate either lies or names its
        # empty scope.
        "name": "gate 23 scope floor fires when a gate passes on an empty corpus",
        "gate": "check_scope_floor.py",
        "args": [],
        "plant": _scope_floor_sandbox(vacuous_index=_SCOPE_GATES),
        "clean": _scope_floor_sandbox(),
    },
    {
        # Rule 9 must scope a workflow's invocations to that workflow. Merging
        # them with the suite-wide set made THIS repo fail its own gate: the
        # narrow, deliberate `paths:` filter in study-live.yml was told it fails
        # to trigger scripts only code-whitespace.yml runs, and the only visible
        # remedy was widening it to `scripts/**` and losing the point of having
        # one. The fire side proves the rule still catches an incomplete filter;
        # the clean side IS the live repo, where the narrow filter is correct —
        # which is what regresses the moment the two sets are merged again.
        "name": "gate 15 wiring fires when a paths filter misses a script it runs",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _wiring_sandbox(),
        "clean_in_repo": True,
    },
    {
        # Rule 11 generalizes rule 9 from "the scripts a workflow runs" to "the
        # trees a workflow verifies". A markdown-only filter on the workflow
        # that renders the artifact meant a push touching only the edge ran
        # neither the render backstop nor the live-edge probe. Fire side: the
        # blind filter in a sandbox. Clean side: the live repo, where both
        # filters name functions/** and auth/** — which is what regresses the
        # moment someone narrows one of them back.
        "name": "gate 15 wiring fires when a workflow filter ignores the tree it verifies",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _edge_trigger_sandbox(),
        "clean_in_repo": True,
    },
    {
        # The unwired-checker rule, one directory over: a Functions suite that
        # no workflow invokes is a suite nobody runs. Fire side: an orphan test
        # file beside a workflow that runs a different one. Clean side: the live
        # repo, where both suites are wired — which is what regresses the moment
        # someone adds a test file and forgets the workflow step.
        "name": "gate 15 wiring fires on a Functions suite no workflow runs",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _unwired_suite_sandbox(),
        "clean_in_repo": True,
    },
    {
        # Rule 12's coverage half: the map opens by claiming to list every
        # script, and the 2026-09-27 pass added the two it was missing. Removing
        # one name again must fire on that claim — not on a missing map or a
        # stale count, which have their own case.
        "name": "gate 15 wiring fires when the scripts map omits a script",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _owners_sandbox(map_text=_MAP_DROPS_SCRIPT),
        "clean": _owners_sandbox(),
    },
    {
        # Rule 12's count half: 21-gate / the 20-gate table was the stale pair
        # this pass restamped to 30 through the gate's own --write. The clean
        # side is the real map, so the case fails if either the check or the
        # committed count drifts.
        "name": "gate 15 wiring fires on a stale gate count in the scripts map",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _owners_sandbox(map_text=_MAP_STALE_COUNT),
        "clean": _owners_sandbox(),
    },
    {
        # Rule 12's other direction: a map row naming a script that no longer
        # exists sent readers to a file that is gone and stayed green. The
        # plant appends such a row while every real script is still named —
        # only the reverse check can fire.
        "name": "gate 15 wiring fires when the scripts map names a script that does not exist",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _owners_sandbox(map_text=_MAP_STALE_ROW),
        "clean": _owners_sandbox(),
    },
    {
        # Rule 13: the theme preference had two independent implementations
        # before this pass (the Jekyll include and the generator); the plant
        # puts a second one back. The clean side is the shipped single-source
        # layout — assets/theme.js plus both consumers loading it — which is
        # the property the rule exists to keep.
        "name": "gate 15 wiring fires on a second implementation of the theme key",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _owners_sandbox(extra={
            "_includes/theme-copy.html":
                f'var savedTheme = localStorage.getItem("{_THEME_KEY}");\n',
        }),
        "clean": _owners_sandbox(),
    },
    {
        # Rule 13's load-path half: the path one consumer loads lives once, in
        # _config.yml (`theme_asset`). The include resolves it through
        # relative_url and the generator emits it document-relative; restating
        # it is the drift that broke the generated page from file://, so the
        # old literal must fire again.
        "name": "gate 15 wiring fires when a theme consumer hardcodes the load path",
        "gate": "check_verify_wiring.py",
        "args": [],
        "plant": _owners_sandbox(extra={
            os.path.join("_includes", "head-custom.html"): _HEAD_HARDCODES,
        }),
        "clean": _owners_sandbox(),
    },
    {
        # The live probe's routing derivation had zero coverage and fell
        # silently to an empty tuple, which demoted the callback paths out of
        # the must-answer-200 set with every gate green. The declaration
        # re-spelled with single quotes is the first refactor that used to do
        # it; the clean side is the shipped single declaration, resolved from
        # the same module the middleware is built from.
        "name": "study-live resolver fires on a single-quoted interception declaration",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(access=_ACCESS_SINGLE_QUOTES),
        # The refusal has to name the entry it could not read and the
        # declaration it sits in — not the second entry, and not the list the
        # spread feeds, which would point a maintainer at the wrong name.
        "fire_names": ("INTERCEPTED_PATHS", "'/auth/callback.html'"),
        "fire_omits": ("PUBLIC_AUTH_PATHS", "'/auth/callback'"),
        "clean": _live_source_sandbox(),
    },
    {
        # Declared as a Set instead of an array: a shape the resolver cannot
        # read must fail loudly, not resolve to nothing.
        "name": "study-live resolver fires on an interception declaration it cannot read",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(access=_ACCESS_SET),
        # A shape the reader cannot resolve must be named as the declaration
        # that is unreadable, not as the surface that spreads it.
        "fire_names": ("INTERCEPTED_PATHS = [...]",),
        "fire_omits": ("PUBLIC_AUTH_PATHS",),
        "clean": _live_source_sandbox(),
    },
    {
        # A partially parsed list: one single-quoted entry among double-quoted
        # ones. It used to be dropped while the probe stayed green — the same
        # silent-drop class as the empty tuple, one entry wide. Now the entry
        # the resolver cannot read fails the gate instead of vanishing.
        "name": "study-live resolver fires on an entry it cannot resolve",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(access=_ACCESS_MIXED_QUOTES),
        # Naming the entries around the bad one is the wrong-line defect one
        # entry wide: the refusal must name the entry it refused, and only it.
        "fire_names": ("PUBLIC_AUTH_PATHS", "'/auth/refresh'"),
        "fire_omits": ('"/favicon.svg"',),
        "clean": _live_source_sandbox(),
    },
    {
        # A comment in the body is prose, not an entry. The clean side carries
        # notes among its paths, so a reader that treats them as entries again
        # fails here — that is the wrong-line message the audit found. The
        # plant keeps a single-quoted entry after a note, so stepping over the
        # note cannot make the reader blind to what follows it.
        "name": "study-live resolver steps over a comment in the declaration body",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(access=_ACCESS_COMMENTED_UNRESOLVED),
        # The note is prose, so the refusal must name the single-quoted entry
        # alone — not a note, and not the note-plus-path merge the old reader
        # reported, which is how this case exited non-zero and passed anyway.
        "fire_names": ("PUBLIC_AUTH_PATHS", "'/auth/logout'"),
        "fire_omits": ("legacy alias", '"/auth/login"', "trailing note",
                       "block note"),
        "clean": _live_source_sandbox(access=_ACCESS_COMMENTED),
    },
    {
        # The adapter reimplementing the intercept inline (startsWith, single
        # quotes, no INTERCEPTED_PATHS): the probe would be checking a routing
        # the adapter no longer reads, so it must refuse to run.
        "name": "study-live resolver fires when the adapter reimplements the intercept inline",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(adapter=_ADAPTER_INLINE),
        # The refusal has to name the adapter file and the declaration it
        # stopped consuming, because that pair is the defect.
        "fire_names": ("functions/_middleware.ts no longer consumes "
                       "INTERCEPTED_PATHS",),
        "clean": _live_source_sandbox(),
    },
    {
        # The emptied surface, through the half of it that is still reachable:
        # an emptied public declaration. The reader refuses the empty body by
        # name instead of resolving to nothing and demoting every path out of
        # the must-answer-200 set — the loudness the dead "declares no paths"
        # check claimed, pinned where it can actually fire.
        "name": "study-live resolver refuses an emptied public declaration",
        "gate": "check_study_live.py",
        "args": ["--print-contract"],
        "plant": _live_source_sandbox(access=_ACCESS_NO_PUBLIC),
        "clean": _live_source_sandbox(),
        "fire_names": ("PUBLIC_AUTH_PATHS", "declares no entries"),
    },
    {
        # Rule 1: the corpus keeps one spelling convention (behavior 845 /
        # behaviour 26). The clean side is the scope proof — a proper noun that
        # contains the minority form must not be reported, which is the whole
        # reason the exemption list is named rather than a blanket word rule.
        "name": "gate 24 prose hygiene fires on a minority spelling",
        "gate": "prose_hygiene.py",
        "args": [],
        "plant": {"p.md": "text\n\nThe behaviour is deterministic.\n"},
        "clean": {"p.md": (
            "text\n\nThe behavior is deterministic, and the Colour Contrast "
            "Analyser is the tool's own registered name.\n")},
    },
    {
        # Rule 2: CommonMark needs the space, so a glued heading renders as
        # literal text and the section loses its structure. The clean side pins
        # the scope that matters — a real heading, and a `#` inside a fence
        # (a shebang) that is not a heading at all.
        "name": "gate 24 prose hygiene fires on a heading with no space",
        "gate": "prose_hygiene.py",
        "args": [],
        "plant": {"p.md": "text\n\n##Glued heading\n"},
        "clean": {"p.md": "text\n\n## Real heading\n\n```bash\n#!/bin/sh\n```\n"},
    },
    {
        # Rule 3: GFM splits on `|` before inline parsing, so an unescaped pipe
        # inside a code span silently breaks the cell grid and the table stops
        # lining up. The clean side is the repair this gate proposes.
        "name": "gate 24 prose hygiene fires on an unescaped pipe in a cell",
        "gate": "prose_hygiene.py",
        "args": [],
        "plant": {"p.md": "text\n\n| A | B |\n| --- | --- |\n| one | `??` vs `||` |\n"},
        "clean": {"p.md": "text\n\n| A | B |\n| --- | --- |\n| one | `??` vs `\\|\\|` |\n"},
    },
    {
        # Rule 4: empty discourse filler. Check-only, because deleting a phrase
        # leaves worse prose than the phrase did. The clean side is the reason
        # the list stays short — `essentially` and `the fact that` are used for
        # real work in this corpus and a phrase rule must not touch them.
        "name": "gate 24 prose hygiene fires on empty filler",
        "gate": "prose_hygiene.py",
        "args": [],
        "plant": {"p.md": "text\n\nIt is important to note that the cache is bounded.\n"},
        "clean": {"p.md": (
            "text\n\nThe cache is bounded, which is essentially a Strategy + "
            "coordinator, and the O(n) bound comes from the fact that each "
            "element is pushed once.\n")},
    },
    {
        # Gate 25 is a ceiling baseline: the plant exceeds it with a paragraph
        # restated 20+ lines apart — the "same point made twice in one chapter"
        # class gate 11 cannot see because the files differ. The restatements
        # must NOT be consecutive rows (an unrelated paragraph sits between),
        # or the adjacent detector would fire instead of the intra one this
        # case names; the fence supplies the line distance a real chapter has.
        # First version of this plant had the restatement 6 lines away — inside
        # no detector's reach — and the gate correctly refused to fire on it.
        "name": "gate 25 dilution fires on a chapter restating itself",
        "gate": "check_dilution.py",
        "args": [],
        "plant": {"10-frontend/p.md": (
            "# T\n\n"
            "The retry budget must be smaller than the upstream timeout, or "
            "every attempt doubles the tail latency of the slowest path and "
            "the caller sees the worst case twice.\n\n"
            "Cache aside, the read path is independent: a warm cache absorbs "
            "the burst and the origin never sees it.\n\n"
            "```js\n"
            + "".join(f"const step{i} = advance(state{i});\n" for i in range(16))
            + "```\n\n"
            "The retry budget has to be smaller than the upstream timeout, or "
            "each attempt doubles the tail latency of the slowest path and "
            "the caller observes the worst case two times.\n")},
        "clean": {"10-frontend/p.md": (
            "# T\n\n"
            "The retry budget must be smaller than the upstream timeout, or "
            "every attempt doubles the tail latency of the slowest path.\n\n"
            "- retries are bounded by the budget\n"
            "- the budget is smaller than the timeout\n"
            "- therefore the caller never waits twice\n\n"
            "Backpressure is the complementary control: it slows the caller "
            "instead of failing the request.\n")},
    },
    {
        # Gate 26 is a ceiling baseline over cross-file code examples. The
        # plant adds a second file carrying a raw-identical >=10-line example
        # that also exists in the first — the "chapter re-teaches another
        # chapter's code" class. The real baseline is copied into every
        # sandbox, so the case overwrites it with a zero ceiling: with both
        # files present the gate must fire (1 pair > 0); with the copy
        # replaced by a pointer it must pass.
        "name": "gate 26 code_dup fires on a re-taught code example",
        "gate": "check_code_dup.py",
        "args": [],
        "sandbox": {"scripts/code-dup-baseline.json": "{\"identical\": 0, \"near\": 0}\n"},
        "plant": {"10-frontend/a.md": (
            "# T\n\n"
            "```typescript\n"
            "export function slugify(input: string): string {\n"
            "  return input.toLowerCase().trim().replace(/\\s+/g, '-');\n"
            "}\n\n"
            "export function unslugify(slug: string): string {\n"
            "  return slug.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');\n"
            "}\n\n"
            "export const SEPARATORS = ['-', '_'] as const;\n"
            "export const MAX_SLUG_LENGTH = 96;\n"
            "```\n"),
            "10-frontend/b.md": (
            "# T2\n\n"
            "```typescript\n"
            "export function slugify(input: string): string {\n"
            "  return input.toLowerCase().trim().replace(/\\s+/g, '-');\n"
            "}\n\n"
            "export function unslugify(slug: string): string {\n"
            "  return slug.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');\n"
            "}\n\n"
            "export const SEPARATORS = ['-', '_'] as const;\n"
            "export const MAX_SLUG_LENGTH = 96;\n"
            "```\n")},
        "clean": {"10-frontend/b.md": (
            "# T2\n\n"
            "The slug helpers are owned by [the canonical chapter](a.md); "
            "this chapter only consumes them.\n\n"
            "```typescript\n"
            "import { slugify } from './a';\n\n"
            "export function routeFor(title: string): string {\n"
            "  return `/posts/${slugify(title)}`;\n"
            "}\n"
            "```\n")},
    },
    {
        # The identical half of gate 26's re-baseline after the Docita trim:
        # the committed ceiling is 1 (the recorded git-rebase keep), so the
        # plant — the shape the trim removed, two files sharing two raw copies —
        # fires, and one copy passes at the ceiling. Under the old ceiling of 2
        # the plant would have passed, which is the regression this pins.
        "name": "gate 26 code_dup fires when a new identical pair exceeds the re-baselined ceiling",
        "gate": "check_code_dup.py",
        "args": [],
        "plant": _dup_pair_sandbox(2, reword=False),
        "clean": _dup_pair_sandbox(1, reword=False),
    },
    {
        # The near half of the same re-baseline (16 -> 11): twelve reworded
        # cross-file pairs are one above the committed ceiling, eleven sit at
        # it. The generator keeps the pair count exact, so a re-baseline above
        # 11 stops this case from firing — and the 0/0-overridden case above
        # deliberately cannot see the committed values at all.
        "name": "gate 26 code_dup fires when a new near pair exceeds the re-baselined ceiling",
        "gate": "check_code_dup.py",
        "args": [],
        "plant": _dup_pair_sandbox(12),
        "clean": _dup_pair_sandbox(11),
    },
    {
        # Gate 27 has two rules; the plant fires the baseline-free one (label
        # echo) so the case needs no sandbox baseline override — an echo is
        # always a defect, while the bare ceiling depends on which stack the
        # sandbox file lands in. The clean side is a reason whose content
        # words go beyond the label — the property the echo rule protects.
        "name": "gate 27 see_also fires on a label-echo reason",
        "gate": "check_see_also.py",
        "args": [],
        "plant": {"p.md": (
            "# T\n\n"
            "## See Also\n\n"
            "- [Closures](closures.md) — closures\n")},
        "clean": {"p.md": (
            "# T\n\n"
            "## See Also\n\n"
            "- [Closures](closures.md) — the returned inner function keeps "
            "the outer scope alive, which is what bounds this chapter's "
            "cache lifetime\n")},
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


# Every key a case may carry. A key the runner does not read is a dropped
# assertion: rename `fire_names` to `fire_name` and the refusal-content pin
# stops executing while the case still prints "ok" on content it must reject
# (2026-09-29 audit). The set is checked, not assumed.
CASE_KEYS = frozenset((
    "name", "gate", "args", "plant", "clean", "dirs", "dirs_clean",
    "clean_in_repo", "clean_real", "sandbox", "fire_names", "fire_omits",
))


# The words this suite announces a verdict with — verify.sh's per-gate PASS /
# FAIL, the probe's PASS / WARN / FAIL, this harness's own ok / FAIL. An
# element made of them names no defect: it is present in a refusal whatever the
# gate found, which is how ("FAIL",) passed on content it had to reject
# (2026-09-29 audit). Read as whole words, not substrings — `ok` lives inside
# `lookup`, and a pin on a real phrase has to stay legal.
VERDICT_WORDS = frozenset(("fail", "pass", "warn", "ok"))


def discriminating(text):
    """Whether an assertion element can tell one refusal from another.

    Two families cannot: an element with nothing in it to match (blank, or a
    single character, which matches nearly any output), and one whose every
    word is a verdict word. A longer generic phrase can still be weak, which is
    the author's judgement to make, not the runner's.
    """
    stripped = text.strip()
    if len(stripped) < 2:
        return False
    words = re.findall(r"[a-z]+", stripped.lower())
    return not (words and all(word in VERDICT_WORDS for word in words))


def case_problems(case):
    """Why this case cannot test what it says it does, or [] if it can.

    Shapes of assertion that silently stop testing: a key the runner never
    reads (a typo), an assertion carrying no signal — empty, or a bare string,
    which is iterated character by character, so a single character appearing
    anywhere in the output satisfies it — and an element that cannot
    discriminate one refusal from another.
    """
    problems = []
    unknown = sorted(set(case) - CASE_KEYS)
    if unknown:
        problems.append(
            f"unknown key(s) {', '.join(map(repr, unknown))} — the runner never "
            f"reads them, so whatever they were meant to assert never runs")
    for key in ("fire_names", "fire_omits"):
        if key not in case:
            continue
        value = case[key]
        if not isinstance(value, (list, tuple)):
            problems.append(
                f"{key} must be a tuple of substrings, not "
                f"{type(value).__name__} — a string is iterated character by "
                f"character, and any one character in the output passes it")
        elif not (value and all(isinstance(text, str) and text for text in value)):
            # `not value` is load-bearing: `all()` over an empty tuple is True,
            # so an empty assertion would otherwise pass as a valid one.
            problems.append(f"{key} must name at least one non-empty substring")
        else:
            weak = sorted({text for text in value if not discriminating(text)})
            if weak:
                problems.append(
                    f"{key} element(s) {', '.join(map(repr, weak))} cannot "
                    f"discriminate — blank or single-character text matches "
                    f"almost any output, and text made of the verdict words "
                    f"({', '.join(sorted(VERDICT_WORDS))}) is printed whatever "
                    f"the defect, so the case would pass on content it must "
                    f"reject; pin text the defect alone produces")
    return problems


def refusal_problems(case, output):
    """Substrings the fire side's refusal must carry, and must leave out.

    A gate that exits non-zero while blaming the wrong line satisfies an
    exit-code check and still sends a maintainer to the wrong place — the
    merged note-plus-path message the resolver audit found. A case that cares
    declares what the refusal must name (`fire_names`) and what it must not
    (`fire_omits`); both are read off the gate's own output.
    """
    unnamed = [text for text in case.get("fire_names", ()) if text not in output]
    blamed = [text for text in case.get("fire_omits", ()) if text in output]
    return unnamed, blamed


def main() -> int:
    if not os.path.exists(REAL_CHAPTER):
        print(f"clean-side control chapter missing: {REAL_CHAPTER}")
        return 1
    declared = [(case.get("name") or "<unnamed case>", problem)
                for case in CASES for problem in case_problems(case)]
    if declared:
        for name, problem in declared:
            print(f"FAIL {name}\n  {problem}")
        print(f"\n{len(declared)} case declaration(s) name something the runner "
              f"does not read — a dropped assertion is a silent pass, so the "
              f"suite refuses to run until the case is fixed.")
        return 1
    failures = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as fire_tmp, tempfile.TemporaryDirectory() as clean_tmp:
            build_sandbox(fire_tmp, case["plant"], [], case.get("dirs", ()))
            for rel, content in case.get("sandbox", {}).items():
                path = os.path.join(fire_tmp, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
            r = run_gate(fire_tmp, case["gate"], case["args"])
            output = r.stdout + r.stderr
            fire_ok = r.returncode != 0
            unnamed, blamed = refusal_problems(case, output)

            if case.get("clean_in_repo"):
                # A corpus-scale gate whose live values come from the real
                # stack skeleton: its clean side IS the live repo.
                rc = run_gate(ROOT, case["gate"], case["args"])
            else:
                clean_files = case.get("clean", {})
                clean_real = case.get("clean_real", [])
                build_sandbox(
                    clean_tmp, clean_files, clean_real,
                    case.get("dirs_clean", case.get("dirs", ())),
                )
                for rel, content in case.get("sandbox", {}).items():
                    path = os.path.join(clean_tmp, rel)
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(content)
                rc = run_gate(clean_tmp, case["gate"], case["args"])
            clean_ok = rc.returncode == 0

        if fire_ok and clean_ok and not unnamed and not blamed:
            print(f"ok   {case['name']}")
            continue
        failures += 1
        print(f"FAIL {case['name']}")
        if not fire_ok:
            print(f"  fire side: gate exited 0 on its canonical defect — detection is broken")
        elif unnamed:
            print(f"  fire side: the refusal never names {unnamed[0]!r} — it "
                  f"blames something other than the defect")
        elif blamed:
            print(f"  fire side: the refusal also names {blamed[0]!r} — it "
                  f"points at what is not the defect")
        if not fire_ok or unnamed or blamed:
            print("  " + output.strip().replace("\n", "\n  ")[:500])
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
