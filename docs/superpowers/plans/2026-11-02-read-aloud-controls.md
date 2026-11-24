# Read-Aloud Voice, Width, and Dock Implementation Plan

> **For agentic workers:** Execute this plan inline task by task. Keep each change within the approved design in `docs/superpowers/specs/2026-11-02-read-aloud-controls-design.md`.

**Goal:** Rank the five most promising English browser voices, make chapter text use the full reader column, and clarify the Listen dock.

**Architecture:** Keep voice selection, paragraph targeting, and dock markup in `assets/read-aloud.js`. Keep responsive dock presentation in `assets/read-aloud.css`; remove old reader-toolbar overrides from `assets/reference-reader.css`. Keep the full-column measure in `assets/reading-ui.css`.

**Tech Stack:** Browser SpeechSynthesis API, plain JavaScript, CSS, Jekyll-rendered HTML.

## Global Constraints

- Keep the browser speech engine, paragraph selection, pause and resume, stop, next-block behavior, reduced-motion behavior, and `en-US` fallback.
- Show at most five English voices, ranked deterministically by available metadata rather than an asserted listening-quality score.
- Use the full article column while retaining the reader grid's current page-width and sidebar limits.
- Keep paragraph selection and the back-to-top action keyboard accessible and responsive.
- Do not add an external text-to-speech (TTS) service or runtime dependency.
- Do not add or run tests in this pass; review changes against approved acceptance criteria and report this verification limit.

---

## File Structure

- `assets/read-aloud.js`: deterministic voice ranking, visible idle cue, primary and action groups, and existing speech state transitions.
- `assets/read-aloud.css`: idle cue, primary action grouping, active dock spacing, and fixed dock centering and alignment.
- `assets/reading-ui.css`: remove the 62ch cap from prose, lists, quotes, alerts, and revision answers.
- `assets/reference-reader.css`: remove stale title-row transforms and toolbar styles overriding the fixed dock.
- `docs/superpowers/specs/2026-11-02-read-aloud-controls-design.md`: approved behavior and boundaries.
- `docs/superpowers/plans/2026-11-02-read-aloud-controls.md`: implementation sequence and acceptance checks.

## Task 1: Rank English voices with available quality hints

**Files:**

- Modify: `assets/read-aloud.js`

**Ranking contract:**

1. Keep voices whose `lang` matches `^en(?:-|_|$)` case-insensitively and that define a `voiceURI` (Uniform Resource Identifier).
2. Give +100 for a name containing a whole-word quality marker (`neural`, `natural`, `premium`, `enhanced`, `studio`, `wavenet`, or `hd`).
3. Give +50 when `localService === false` (remote or cloud synthesis).
4. Give +20 when the name contains `Google` or `Microsoft`.
5. Give +1 when `default === true`.
6. Sort by descending score, then case-insensitive voice name, then `voiceURI`, exposing only the first five.

**Implementation:**

1. Keep the existing English-only filter and replace alphabetical-only sorting with a small pure score-and-sort helper inside the reader initializer.
2. Build the menu from the first five sorted voices, preserving `savedVoice` only when it remains in that menu and otherwise picking the first ranked voice.
3. Preserve the disabled "No English voices available" state and `en-US` fallback when the filtered list is empty.
4. Keep the current `localStorage` key so an existing saved selection remains valid when it still ranks in the visible five.

**Acceptance:** A voice with a quality marker ranks above a generic remote voice, a generic remote voice ranks above a generic local voice, non-English voices never appear, and ties have deterministic name and URI ordering.

## Task 2: Use the full reader column

**Files:**

- Modify: `assets/reading-ui.css`

**Implementation:**

1. Remove the `62ch` and derived `calc(62ch - …)` max-width rules for paragraphs, lists, blockquotes and alerts, and revision answers.
2. Add one explicit full-column rule for those block types without changing the reader grid, article column, sidebar, or mobile gutters.
3. Update the rule comment to say that reader text fills the available column.

**Acceptance:** Text blocks can use the entire main reader column at desktop and mobile widths, with no Width control or stored preference introduced.

## Task 3: Clarify and align the Listen dock

**Files:**

- Modify: `assets/read-aloud.js`
- Modify: `assets/read-aloud.css`
- Modify: `assets/reference-reader.css`

**Implementation:**

1. Group `Listen` and the back-to-top button in `.read-aloud-primary`, group `Pause`, `Next`, and `Stop` in `.read-aloud-actions`, and keep voice and speed in labeled fields.
2. Add a visible idle hint (`"Click a paragraph, then Listen."`), update it to explain that `Listen` starts from the selected paragraph, and keep the visually hidden `role="status"` live region separate.
3. Move the back-to-top button into `.read-aloud-primary`, preserving click behavior and its accessible label.
4. Remove stale reader-title transforms and toolbar styles in `reference-reader.css` that override fixed positioning or duplicate dock button styling.
5. Style the idle dock as a compact centered bar with `Listen` prominent and the arrow aligned beside it; in active state, space the action group and voice and speed fields as distinct groups.
6. At narrow widths, let active controls wrap inside the dock while keeping the idle `Listen` and arrow row together without horizontal overflow.

**Acceptance:** Idle users see the paragraph-selection instruction, selecting a paragraph updates that cue, `Listen` and the arrow share one baseline, the dock stays centered on desktop and wraps cleanly on mobile, and keyboard focus remains visible.

## Final review

- Compare the changed files with the approved spec and this plan.
- Inspect all reader-specific selectors for stale fixed-toolbar transforms or width controls.
- Do not run a test suite in this pass. Report the browser-test limitation and identify the changed files so the user can request verification separately.
