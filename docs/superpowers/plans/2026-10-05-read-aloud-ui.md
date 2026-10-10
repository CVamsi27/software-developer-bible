# Read-Aloud UI Implementation Plan

> **Historical design record:** requirements, example paths and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md) and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; TL;DR and inline chapter cheat/revision sections are retired.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make chapter read-aloud controls compact beside the title, follow spoken paragraphs, add 0.5× playback, and render correctly in light and dark themes.

**Architecture:** Keep SpeechSynthesis and chapter reading in `assets/read-aloud.js`. Extract text from the live article while retaining each text chunk's source block; the reader signals each started chunk, and the mounted UI highlights and scrolls that block into view. Keep the toolbar's layout and theme styling in `assets/read-aloud.css`, and update chapter outline placement in `assets/reading-ui.js` to account for the title row.

**Tech Stack:** Browser SpeechSynthesis, plain JavaScript, Node built-in test runner, Playwright browser test, Jekyll.

## Global Constraints

- Preserve current chapter extraction content rules, play/pause/resume/stop behavior, unsupported-browser handling, and recoverable speech errors.
- Keep the control names accessible and keep playback status announced to assistive technology.
- Scroll only when the active block is outside a comfortable visible reading area; honor `prefers-reduced-motion`.
- Use existing theme tokens and explicit theme state for text, surfaces, focus, select controls, and active-block styling.
- Do not add dependencies or a server-side speech service.

---

## File Structure

- `assets/read-aloud.js`: extract live text with its source element, keep source references for chunks, notify the UI on utterance start, and mount the compact title-row player.
- `assets/read-aloud.css`: title-row layout, compact controls, theme-aware controls and active paragraph styling, responsive and reduced-motion behavior.
- `assets/reading-ui.js`: put the chapter outline after the full title row instead of inside it.
- `assets/reading-ui.css`: update title typography selector and theme color-scheme support if needed by browser tests.
- `assets/read-aloud.test.cjs`: unit tests for source mapping, utterance start, and reader state.
- `scripts/test_read_aloud_browser.cjs`: rendered-browser checks for placement, speed, follow behavior, themes, and responsive layout.
- `docs/superpowers/specs/2026-10-05-read-aloud-reader-ui-design.md`: approved behavior and verification criteria.

### Task 1: Preserve the source paragraph for each speech chunk

**Interfaces:** `extractChapter(content)` returns an ordered array of `{ text, element }` chunks. `createReader(synth, Utterance, update, onChunkStart)` accepts those chunks and invokes `onChunkStart(element, index)` when the corresponding utterance emits `onstart`.

- [x] **Step 1: Write failing unit tests**

In `assets/read-aloud.test.cjs`, assert that a long paragraph produces multiple chunks all carrying the same source-element reference, that distinct paragraphs carry distinct references, and that `onChunkStart` receives the current element when the utterance starts.

```js
test('chunk start reports its source element', () => {
  const spoken = [];
  const source = {};
  const started = [];
  const synth = { speak(u) { spoken.push(u); }, pause() {}, resume() {}, cancel() {} };
  const reader = createReader(synth, function (text) { this.text = text; }, () => {}, element => started.push(element));
  reader.start([{text: 'First paragraph', element: source}]);
  spoken[0].onstart();
  assert.deepEqual(started, [source]);
});
```

- [x] **Step 2: Run the unit suite and confirm the expected failure**

Run: `node --test assets/read-aloud.test.cjs`

Expected: fail because the reader currently accepts strings and does not expose an utterance-start callback.

- [x] **Step 3: Implement source-aware extraction and chunk sequencing**

Use a text-only TreeWalker over the original content. Reject text whose parent is inside `pre`, `script`, `style`, `nav`, `button`, `img`, `svg`, hidden or aria-hidden content, `.read-aloud`, `.chapter-outline`, `.heading-anchor`, or `.chapter-nav-footer`. Group remaining nodes by their nearest heading, paragraph, list item, table cell, or blockquote. Split each group with `splitText` and attach the original block element to each chunk. In `createReader`, speak `chunk.text`, retain the chunk, and call the fourth callback from `utterance.onstart` only when its generation token is still current.

- [x] **Step 4: Run unit tests and verify extraction order**

Run: `node --test assets/read-aloud.test.cjs`

Expected: all existing playback tests and new source-mapping tests pass. Update the browser extraction assertion to compare chunk text while asserting the returned elements point to the authored source blocks.

### Task 2: Put a compact accessible toolbar beside the chapter title

**Interfaces:** `mount()` wraps the existing `h1` in `.chapter-title-row` and places `.read-aloud` beside it. The speed select includes the value `0.5`; the status remains a live region with visually-hidden presentation.

- [x] **Step 1: Add failing browser assertions**

In `scripts/test_read_aloud_browser.cjs`, assert that the player is a sibling of the `h1` inside `.chapter-title-row`, that the `0.5×` option exists, and that clicking Play exposes a visible Pause and Stop control while retaining the accessible status.

```js
assert.equal(await page.locator('.chapter-title-row > h1').count(), 1);
assert.equal(await page.locator('.chapter-title-row > .read-aloud').count(), 1);
assert.equal(await page.locator('[aria-label="Reading speed"] option[value="0.5"]').textContent(), '0.5×');
```

- [x] **Step 2: Run the browser test and confirm the expected failure**

Run the browser test against the local Jekyll server: `node scripts/test_read_aloud_browser.cjs`.

Expected: fail on missing title-row placement and 0.5× option.

- [x] **Step 3: Implement the compact title row and theme-aware control styling**

Wrap the h1 without changing its text or heading anchors, append a compact player after it, and insert `0.5×` before the current speed options. Keep button names and status available to screen readers. Use theme tokens, inherit the selected `color-scheme` on controls, add a visible active-block indicator, and let the title and toolbar wrap without horizontal overflow. Update `assets/reading-ui.js` to append `.chapter-outline` after `.chapter-title-row`, and change the typography selector in `assets/reading-ui.css` to target the wrapped h1.

- [x] **Step 4: Run browser assertions for placement, speed, and responsive width**

Run: `node scripts/test_read_aloud_browser.cjs`.

Expected: title and player align as one row at desktop width, wrap cleanly at 375px, and the speed selector accepts `0.5` and the existing values.

### Task 3: Follow spoken blocks and verify theme behavior

**Interfaces:** On `utterance.onstart`, the mounted UI applies `data-read-aloud-active` to the source block and moves that block into view only if it falls outside the reading viewport. Stop, completion, error, and restart clear the active marker.

- [x] **Step 1: Add failing browser assertions for scrolling, active state, and themes**

In the Playwright test's synthetic article, use two paragraphs and a tall spacer. Stub `scrollIntoView` on the source paragraph, start reading, dispatch the first utterance's `onstart`, and assert the source paragraph is marked active and the stub was called when outside the viewport. Stop playback and assert the marker clears. Set `data-theme="dark"` and `data-theme="light"` and assert the player surface, text, select, and active marker use computed values from the current theme.

- [x] **Step 2: Run the browser test and confirm the expected failures**

Run: `node scripts/test_read_aloud_browser.cjs`.

Expected: the test reports that no active block is marked or scrolled and that the toolbar does not reflect the selected color scheme.

- [x] **Step 3: Implement active-block follow and cleanup**

When a current utterance starts, remove the active marker from the previous element, set it on the new source block, and scroll only if its rectangle is above the top safe margin or below the bottom safe margin. Use `scrollIntoView({block: 'start', behavior: 'smooth'})` when motion is allowed and `behavior: 'auto'` for reduced motion. Clear the marker and active reference on stop, restart, completion, and speech error.

- [x] **Step 4: Verify the browser and unit suites**

Run: `node --test assets/read-aloud.test.cjs` and `node scripts/test_read_aloud_browser.cjs`.

Expected: both pass; the browser test confirms light and dark styling, 375px overflow safety, 0.5× playback, active paragraph follow, and active-state cleanup.

### Task 4: Recompute counts and run repository release gates

- [x] **Step 1: Recompute count-bearing navigation claims from disk**

Run: `python3 scripts/check_counts.py --write`.

Expected: the generated count claims and badges match the current markdown file count.

- [x] **Step 2: Run all required repository gates**

Run: `bash scripts/verify.sh` and confirm the count guard, alignment, structure, link, freshness, and remaining gates pass. If the previously observed `test_gates.py` fixture failure or fixed-point failure remains, isolate it from read-aloud changes and report it without weakening the gate.

- [x] **Step 3: Commit and push after the gates pass**

Stage the read-aloud changes, approved spec, plan, and the count files generated by `check_counts.py`; preserve unrelated existing work unless it is part of the user's already requested final pass. Commit with a focused message and push the current authorized branch only after verifying its upstream and target.
