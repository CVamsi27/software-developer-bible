# Read-Aloud Voice, Width, and Dock Implementation Plan

> **For agentic workers:** Execute this plan inline task by task. Keep each change within the approved design in `docs/superpowers/specs/2026-11-02-read-aloud-controls-design.md`.

**Goal:** Rank the five most promising English browser voices, make chapter text use the full reader column, and clarify the Listen dock.

**Architecture:** Keep voice selection, paragraph targeting, and dock markup in `assets/read-aloud.js`. Keep responsive dock presentation in `assets/read-aloud.css`; remove old reader-toolbar overrides from `assets/reference-reader.css`. Keep the full-column measure in `assets/reading-ui.css`.

**Tech Stack:** Browser SpeechSynthesis API, plain JavaScript, CSS, Jekyll-rendered HTML.

## Global Constraints

- Keep the browser speech engine, paragraph selection, pause/resume, stop, next-block behavior, reduced-motion behavior, and `en-US` fallback.
- Show at most five English voices; rank deterministically by the available metadata, not an asserted listening-quality score.
- Use the full article column, while retaining the reader grid's current page-width and sidebar limits.
- Keep paragraph selection and the back-to-top action keyboard accessible and responsive.
- Do not add an external TTS service or runtime dependency.
- Do not add or run tests in this pass; review the change against the approved acceptance criteria and report this verification limit.

---

## File Structure

- `assets/read-aloud.js`: deterministic voice ranking, visible idle cue, primary/action groups, and existing speech state transitions.
- `assets/read-aloud.css`: idle cue, primary action grouping, active dock spacing, and fixed dock centering/alignment.
- `assets/reading-ui.css`: remove the 62ch cap from prose, lists, quotes, alerts, and revision answers.
- `assets/reference-reader.css`: remove stale title-row transforms and toolbar styles that override the fixed dock.
- `docs/superpowers/specs/2026-11-02-read-aloud-controls-design.md`: record the approved behavior and boundaries.
- `docs/superpowers/plans/2026-11-02-read-aloud-controls.md`: implementation sequence and acceptance checks.

## Task 1: Rank English voices with available quality hints

**Files:**

- Modify: `assets/read-aloud.js`

**Ranking contract:**

1. Keep voices whose `lang` matches `^en(?:-|_|$)` case-insensitively and has a `voiceURI`.
2. Give +100 for a name containing a whole-word quality marker: `neural`, `natural`, `premium`, `enhanced`, `studio`, `wavenet`, or `hd`.
3. Give +50 when `localService === false` (remote/cloud synthesis).
4. Give +20 when the name contains `Google` or `Microsoft`.
5. Give +1 when `default === true`.
6. Sort by descending score, then case-insensitive voice name, then `voiceURI`; expose only the first five.

**Implementation:**

1. Keep the existing English-only filter. Replace alphabetical-only sorting with a small pure score-and-sort helper inside the reader initializer.
2. Build the menu from the first five sorted voices. Preserve `savedVoice` only when it is still in that menu; otherwise choose the first ranked voice.
3. Preserve the disabled “No English voices available” state and `en-US` fallback when the filtered list is empty.
4. Keep the current localStorage key so an existing saved selection remains valid when it still ranks in the visible five.

**Acceptance:** A voice with a quality marker ranks above a generic remote voice; a generic remote voice ranks above a generic local voice; non-English voices never appear; ties have deterministic name/URI ordering.

## Task 2: Use the full reader column

**Files:**

- Modify: `assets/reading-ui.css`

**Implementation:**

1. Remove the `62ch` and derived `calc(62ch - …)` max-width rules for paragraphs, lists, blockquotes/alerts, and revision answers.
2. Add one explicit full-column rule for those block types, without changing the reader grid, article column, sidebar, or mobile gutters.
3. Update the rule comment to say that reader text fills the available column.

**Acceptance:** Text blocks can use the entire main reader column at desktop and mobile widths; no Width control or stored preference is introduced.

## Task 3: Clarify and align the Listen dock

**Files:**

- Modify: `assets/read-aloud.js`
- Modify: `assets/read-aloud.css`
- Modify: `assets/reference-reader.css`

**Implementation:**

1. Group Listen and the existing back-to-top button in `.read-aloud-primary`; group Pause/Next/Stop in `.read-aloud-actions`; keep voice and speed in their labeled fields.
2. Add a visible idle hint: “Click a paragraph, then Listen.” Change it to explain that Listen starts from the selected paragraph. Keep the existing visually hidden `role="status"` live region separate.
3. Move the existing back-to-top button into `.read-aloud-primary`, preserving its click behavior and accessible label.
4. Remove stale reader-title transforms and toolbar styles in `reference-reader.css` that override fixed positioning or duplicate the dock's button styling.
5. Style idle as a compact centered dock. Keep Listen prominent; align the arrow beside it. In active state, space the action group and voice/speed fields as distinct groups.
6. At narrow widths, let active controls wrap inside the dock. Keep the idle Listen/arrow row together and prevent horizontal overflow.

**Acceptance:** Idle users see the paragraph-selection instruction; selecting a paragraph updates that cue; Listen and the arrow share one baseline; the dock stays centered on desktop and wraps cleanly on mobile; keyboard focus remains visible.

## Final review

- Compare the changed files with the approved spec and this plan.
- Inspect all reader-specific selectors for stale fixed-toolbar transforms or width controls.
- Do not run a test suite in this pass. Report the browser-test limitation and identify the changed files so the user can request verification separately.
