# Reading and Interview Quality Implementation Plan

> **Historical design record:** requirements, example paths and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md) and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; TL;DR and inline chapter cheat/revision sections are retired.

> **For agentic workers:** Execute this plan task by task in the current session, recording validation and remaining limitations in the audit report.

**Goal:** Make the learning corpus concise and formally grounded, fix full-width reading and theme defects, and align senior interview preparation with supported resume evidence.

**Architecture:** Markdown remains the canonical content. Shared reader CSS and theme JavaScript own presentation; the existing generators own counts and navigation. Personal resume sources remain under the private personal directory.

**Tech Stack:** Markdown, Python verification/generation, Jekyll/Minima, vanilla CSS/JavaScript, Playwright and ReportLab.

## Global Constraints

- Preserve original practical definitions and stable numbered IDs.
- Keep revision drills in REVISION.md and preserve existing authored questions.
- Keep personal data canonical under 80-lanes-abroad-full-stack/personal/.
- Generate counts with check_counts.py --write; do not hand-edit count claims.
- Verify new external citations before updating the citation baseline.
- Do not add unsupported resume metrics or experience from study material.

## Task 1: Establish the inventory and reproduce reader defects

- [x] Enumerate all Markdown by genre, inspect existing gates and recent changes, and run the baseline harness.
- [x] Measure paragraph/article widths and inspect both themes on desktop and mobile.
- [x] Record coverage and concrete findings in docs/2026-10-07-reading-quality-report.md.

## Task 2: Repair shared reader behavior

**Files:** assets/reading-ui.css, _includes/head-custom.html, assets/theme.js, scripts/test_reading_ui_browser.cjs.

- [x] Add browser assertions comparing paragraph width with article width at 1280px and 1920px; run before the fix and capture the failure.
- [x] Remove both independent prose width caps. Retain responsive gutters and local horizontal scrolling for code/tables.
- [x] Reproduce and repair any theme state, control contrast or mobile-navigation defects discovered by browser tests.
- [x] Build the site, run reader/read-aloud tests, and inspect desktop/mobile screenshots in both themes.

## Task 3: Complete concept definitions and editorial review

**Files:** numbered concept chapters across the study stacks, existing revision companions and interview routes; scripts/check_template.py if a new coverage rule is needed.

- [x] Read each definition-bearing introduction and add an original, topic-specific textbook-style definition where absent.
- [x] Preserve existing definitions; correct factual or grammatical defects with the smallest justified edit.
- [x] Scan all Markdown for grammar, malformed rendering, stale APIs and repetition. Review candidates before editing.
- [x] Review senior-role gaps in mechanism, trade-off and failure reasoning; add missing material to canonical homes and source-linked revision practice.
- [x] Validate textbook coverage independently of mere file modification counts.

## Task 4: Align the resume with defensible senior evidence

**Files:** personal/resume/generator/resume_content.py, personal/resume/README.md, existing claim/targeting companions and generated application/public PDFs.

- [x] Read current resume, crosswalk, targeting rules and tests; distinguish existing supported evidence from study goals.
- [x] Tighten supported scope/ownership and add genuinely missing supported skills only.
- [x] Regenerate all current variants together, run resume/cover-letter/claim checks and inspect PDF renders.

## Task 5: Regenerate and verify

- [x] Run read_time.py, check_counts.py --write, alignment repair as required and gen_master_index.py.
- [x] Run python3 scripts/check_links.py and bash scripts/verify.sh; repair regressions without weakening gates.
- [x] Rebuild the final site; verify private content exclusions and rerun browser checks after final edits.
- [x] Record exact results and any incomplete editorial/deployment scope, then provide a concise final handoff.

## Review scope

The corpus-wide pass combines automated scans, concept-introduction review and targeted deep semantic verification. It does not certify that every sentence and snippet has been independently proofread or executed. The audit report records that distinction and the final checks.

## Task 6: Continued final pass

- [x] Sweep rendered navigation and long-content pages in both themes at mobile and desktop widths, including opened menus and keyboard/Copy behavior.
- [x] Review complete role-relevant chapters beyond their definitions; check grammar candidates and technical failure boundaries against primary sources.
- [x] Repair confirmed findings and carry their implications into revision practice and regression checks where appropriate.
- [x] Update the audit record, regenerate affected artifacts and rerun the final verification/build/browser checks.
