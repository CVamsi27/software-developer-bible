# Read-Aloud Controls Implementation Plan

> **For agentic workers:** Execute this plan inline task by task. Keep each change within the approved design in `docs/superpowers/specs/2026-11-02-read-aloud-controls-design.md`.

**Goal:** Let readers choose a paragraph to narrate, limit voice choices to five English voices, remove reading-width controls, and align the back-to-top action beside the audio dock.

**Architecture:** Keep speech extraction and start-position state in `assets/read-aloud.js`. Keep width and dock presentation changes in the existing reader styles and DOM builder. Move the existing back-to-top button into the dock only on reader pages; preserve its standalone positioning elsewhere.

**Tech Stack:** Browser SpeechSynthesis API, plain JavaScript, CSS, Jekyll-rendered HTML.

## Global Constraints

- Preserve chapter text extraction, speech rate, pause/resume, stop, next-block behavior, reduced-motion behavior, and the `en-US` speech-language fallback.
- Keep the default reader measure at the existing 62ch comfortable width.
- Keep non-reader pages' back-to-top behavior unchanged.
- Do not add an external audio service or dependencies.

---

## File Structure

- `assets/read-aloud.js`: voice filtering, selected paragraph state, start-at-selection behavior, and reader-page docking of the existing arrow.
- `assets/read-aloud.css`: selected-paragraph styling, compact arrow-in-dock styling, and removal of reader-width styles and the old raised-arrow offset.
- `assets/reading-ui.js`: remove creation of the Width dropdown and stored-width behavior.
- `assets/reading-ui.css`: remove the `data-width="wide"` override and width-control styles; keep the comfortable measure rules.
- `assets/study-ui.test.cjs`, `scripts/test_reading_ui_browser.cjs`, and `scripts/test_read_aloud_browser.cjs`: update reader assertions and cover the visible selection, English voice limit, dock alignment, and removed width control.

## Task 1: Remove the Width control and cap English voice choices

**Files:**

- Modify: `assets/reading-ui.js`
- Modify: `assets/reading-ui.css`
- Modify: `assets/read-aloud.js`
- Modify: `assets/read-aloud.css`

**Implementation:**

1. Remove `reading-width` label/select creation, `sdb-reading-width` storage, and writes to `content.dataset.width` from `assets/reading-ui.js`.
2. Remove `.reading-width` rules and the `data-width="wide"` rule from `assets/reading-ui.css`. Retain the existing 62ch paragraph/list/quote measure rules.
3. In `refreshVoices()`, keep only entries whose locale matches `^en(?:-|_|$)` case-insensitively, sort by voice name, and expose the first five.
4. Remove the generic Default voice option. Keep the saved voice only if it is among those five; otherwise select the first English voice. If the browser has no English voice, disable the select and let utterances use the existing `en-US` fallback.
5. Remove `.reading-width` from the read-aloud exclusion selector if no matching element remains; keep all other text-extraction exclusions intact.

**Acceptance:** The source and rendered reader contain no width control or width preference, and the voice picker has at most five English choices with no generic or non-English option.

## Task 2: Select a paragraph as the narration start point

**Files:**

- Modify: `assets/read-aloud.js`
- Modify: `assets/read-aloud.css`

**Implementation:**

1. Maintain `selectedGroup`, initially `-1`, separately from `currentGroup` so an explicit pending selection does not change the current speech mid-utterance.
2. Add a delegated click handler on `.post-content`. If the target is inside a readable `p` group and outside links, buttons, inputs, selects, or other interactive elements, select its group and update the status message.
3. Mark the selected paragraph with `data-read-aloud-selected="true"`; clear the previous selected marker whenever the selection changes. Style the selected marker distinctly from the active spoken-block marker.
4. Make the Listen handler prefer `selectedGroup`; if there is no selection, keep the current viewport-based `pickStartGroup()` behavior. Consume the pending selection when playback starts so the active spoken block remains visually distinct from any new selection.
5. Clear the selected marker when Stop is pressed or the player is otherwise reset. Do not clear the pending marker during the normal transition from one speech chunk to another.

**Acceptance:** A paragraph click/tap updates the announced selection; Listen begins at that paragraph; Next advances from it; selecting during playback leaves current speech alone and reveals Listen to switch paragraphs; a click inside a link follows the link and does not change the selected paragraph.

## Task 3: Align the back-to-top arrow beside the audio dock

**Files:**

- Modify: `assets/read-aloud.js`
- Modify: `assets/read-aloud.css`

**Implementation:**

1. After creating the reader dock, find the existing `.back-to-top` button and append it to `.read-aloud-controls` inside the dock. In the idle state this places it directly beside Listen.
2. Keep the arrow's existing click handler, accessible label, and visibility behavior. If the reader dock is absent, do not move the button.
3. Override its global fixed-position, bottom, right, opacity transform, shadow, and z-index presentation only while it is a child of `.read-aloud`; style it as a 44px circular control aligned with the Listen button.
4. Let the idle dock and controls size to their contents so Listen and the arrow remain on one row at narrow widths. Keep the active dock's wrap behavior for voice and speed controls.
5. Remove `body.has-read-aloud .back-to-top`'s former raised-bottom offset; retain bottom padding that keeps chapter content clear of the dock.

**Acceptance:** On reader pages, the arrow shares the dock row with Listen and remains unobstructed on narrow widths. On other pages, the existing floating arrow remains fixed at the viewport corner.

## Final review

- Inspect the final diff against the approved spec and ensure no unrelated files enter the change.
- Update the reader tests to cover the approved behavior.
- Run the repository-required verification gates before committing or pushing; report any unavailable rendered-browser checks.
