# Study Flow UI/UX Implementation Plan

> **For agentic workers:** Execute this approved plan inline, task by task. The user requested refinement followed by implementation in this session. Keep unrelated authored edits intact.

**Goal:** Make finding, reading, revising and resuming study material a continuous flow.

**Architecture:** Enhance the existing Jekyll output with small vanilla JavaScript modules. Search remains generated from canonical metadata. Jekyll emits actual published paths for safe continuation and resume validation.

**Tech Stack:** Jekyll/Minima, Liquid, CSS, vanilla JavaScript, Python generator, Node tests and jsdom for DOM behavior.

## Global Constraints

- Keep authored Markdown, chapter IDs, URLs, API metadata contract and learning order intact.
- Keep the default wide reading layout; Comfortable width is optional.
- Revision companions are separate from interview practice. No completion scores.
- Resume stores one published learning path, anchor, bounded labels and timestamp; no query context or private data.
- No framework migration, new runtime dependency or deployment. The user subsequently authorized committing and pushing the completed changes.
- Use native controls, 44 px targets, theme tokens and reduced-motion support.

### Task 1: Search and shared navigation

**Files:** `_includes/header.html`, `_includes/head-custom.html`, `assets/study-state.js`, `assets/study-catalog.js`, `assets/search-ui.js`, `assets/search-ui.css`, `scripts/gen_master_index.py`, generated `search.html` and `api/index.json`.

**Interfaces:** `StudyState.material(row)` returns learn/revision/interview/reference; `StudyPublishedPaths` is an array of Jekyll-emitted URLs. Search consumes embedded `#study-search-data` JSON and keeps q/sec/cat/tag/material in the URL.

- [x] Write DOM tests using a three-row corpus. Filter Revision; assert only its companion is visible. Clear filters; assert query remains. Restore URL state and validated roadmap context.
- [x] Run `NODE_PATH=/tmp/bible-study-ui-test/node_modules node --test assets/study-ui.test.cjs`; verify the current page fails on missing Material filtering.
- [x] Replace the generated page template with a compact labeled query, Stack/Material selects, advanced Category/Tag controls, selected chips and semantic result rows. Render titles via textContent. Handle Back via popstate; ignore unavailable published paths on HTTP.
- [x] Run DOM tests and `python3 scripts/gen_master_index.py --check`.

### Task 2: Reader and onward actions

**Files:** `assets/reading-ui.js`, `assets/reading-ui.css`, `assets/read-aloud.js`, `assets/read-aloud.css`.

**Interfaces:** Reader consumes published paths, authored metadata badges/headings/links and fixed-origin roadmap context. Emits `study:section` with `{heading, deliberate}`. Narration emits `study:narration` with `{element}`.

- [x] Test that learning pages expose a width selector and retain original metadata in Chapter details. Assert next/revision links point to authored, published targets; indexes receive no chapter controls.
- [x] Run tests and inspect expected missing-control failures before editing.
- [x] Build compact breadcrumb/metadata, optional width, desktop outline and mobile disclosure. Preserve focus on explicit outline navigation and use aria-current during scroll. Insert next/revision actions after Summary, before See Also. Gate narration to learning/revision pages and exclude enhancement UI from speech.
- [x] Run DOM tests plus existing narration and roadmap Node tests.

### Task 3: Revision and resume

**Files:** `assets/revision-ui.js`, `assets/study-resume.js`, `assets/study-state.js`, `index.html`, `assets/study-ui.test.cjs`.

**Interfaces:** `StudyState.createStore(storage, paths)` exposes `read()`, `write(record)`, `clear()`; records have version/path/anchor/title/section/savedAt. Revision groups only explicit Q/A blocks on REVISION.html.

- [x] Test multi-paragraph/code/list answers remain grouped and uncertain blocks stay visible. Assert interview pages are unchanged. Test published-path validation, bad schemas, denied storage, explicit fragment precedence and reversible clearing.
- [x] Run the tests before implementing each behavior.
- [x] Wrap answers in native details; add Show all answers. Track deliberate reading only, throttle saves, and flush on pagehide. Home shows one valid saved position; Resume is explicit. Missing anchors produce a status message. Keep storage failures in memory and never save query parameters.
- [x] Run all focused Node tests.

### Task 4: Build, visual QA and repository gates

**Files:** `design-qa.md`, design evidence under `docs/superpowers/specs/assets/2026-10-11-study-flow/`, count-managed repository docs.

- [x] Build with the repository-pinned Ruby 3.4.11: `PATH=/opt/homebrew/opt/ruby@3.4/bin:$PATH BUNDLE_PATH=vendor/bundle bundle exec jekyll build --destination /tmp/bible-uiux-2026-10-11`.
- [x] Render the home layout separately to home-preview.html because macOS treats index.html and INDEX.html as the same output filename. Do not change production URLs to compensate.
- [x] Open the local build in the in-app browser. Verify query/filter/Back, outline/width, reveal-all, deliberate save/reload/resume and mobile navigation in light/dark themes. Inspect 320 px overflow and visible targets. Compare the final reader reference with a rendered screenshot.
- [x] Record actual passes, intentional content differences, and limits in design-qa.md. Restamp counts with `python3 scripts/check_counts.py --write`; format only our Markdown tables.
- [x] Run `python3 scripts/check_links.py` and `bash scripts/verify.sh`. Report any pre-existing baseline failure without changing unrelated source.

## Self-review

All four study stages, no-JS/print fallbacks, publication availability, theme ownership, accessibility and storage boundaries are covered. Existing browser behavior is checked through the in-app browser; DOM tests do not automate a separate browser. The API digest will regenerate from the current working corpus, including the pre-existing auth chapter edit; no API schema changes are planned.

## Execution evidence

The initial DOM run failed five planned behaviors and passed the existing interview-page separation behavior. Implementation then passed 24 focused Node tests, including existing narration/roadmap tests. The pinned Jekyll build passed. DOM tests use jsdom 26.1.0 as a development-only dependency installed outside the repository, and CI installs the same version in its temporary directory. Final browser evidence and repository gate results are in the project-root design QA report.
