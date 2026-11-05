# Listening Experience Implementation Plan

> **For agentic workers:** Execute inline, task by task, with the test cycle and
> checks below. The design is in the companion specification.

**Goal:** Improve the browser-only listening player, voice choices, and speeds.

**Architecture:** Keep speech sequencing and voice ranking in read-aloud.js and
the dock presentation in read-aloud.css. Keep chapter extraction and its source
ranges intact. The mounted player owns preferences, voice preview coordination,
and passage-level navigation.

**Tech Stack:** Vanilla JavaScript, CSS, SpeechSynthesis, Jekyll, Node test runner,
and Playwright installed outside the checkout.

## Global constraints

- Only local English browser voices; no external speech service or dependency.
- Speeds 0.2 through 2.0 in steps of 0.1, plus 0.75 and 1.25.
- Preserve chapter prose, source ranges, paragraph selection, and start from view.
- Ignore obsolete speech callbacks after cancellation or preview.
- Controls remain usable at 320 pixels wide, in both themes, with keyboard focus.
- Implementation was initially local; the subsequent final-pass request
  authorizes committing, pushing, and merging through a pull request after checks.

## Task 1: Speech and voice behavior

- [x] Add failing unit cases for low speeds, current-word restarts, pause/resume,
  late events, and local voice filtering/ranking.
- [x] Run `node --test assets/read-aloud.test.cjs` and inspect expected failures.
- [x] Implement shared text segmentation, resumable utterances, immediate voice
  and speed changes, and `rankVoices(voices)` in `assets/read-aloud.js`.
- [x] Re-run the engine suite; preserve source-block grouping and extraction.

## Task 2: Player and settings

- [x] Extend `scripts/test_read_aloud_browser.cjs` with failing cases covering
  settings before playback, all speeds, previews, navigation, continuous/manual
  playback, storage, delayed/missing voices, and narrow viewports.
- [x] Implement dock markup, preference persistence, preview coordination, and
  navigation in `assets/read-aloud.js`; style it in `assets/read-aloud.css`.
- [x] Update asset cache parameters in `_includes/head-custom.html`.
- [x] Run the browser suite and existing related Node suites.

## Task 3: Rendered verification and evidence

- [x] Build with the compatible installed Ruby 3.4 and Jekyll dependencies.
- [x] Inspect actual chapter screenshots on desktop/mobile, in both themes, with
  settings closed/open; verify no overflow and keyboard/focus behavior.
- [x] Run `bash scripts/verify.sh`; record any failures without weakening gates.
- [x] Update `design-qa.md` with the resulting behavior, checks, and limitations.

## Verification support

Imported chat files are ignored by Git and the theme-ownership source scan.
The existing paired gate test now accepts quoted theme code in an attachment
while still rejecting a second implementation in a real include. The full
verification uses the pinned example runtimes and final Markdown review hashes.

## Task 4: Spoken word alongside the paragraph

- [x] Add failing engine cases for word lengths, unknown lengths, invalid events,
  and original chunk offsets after speed changes and pause/resume.
- [x] Add browser cases for simultaneous word/paragraph emphasis, inline source
  mapping, whitespace between formatted words, later chunks, lifecycle cleanup,
  contrast, and fallback rectangles after resize.
- [x] Implement a word-boundary callback, normalized-character source ranges,
  CSS Custom Highlight styling, and a non-interactive rectangle fallback.
- [x] Verify the controlled suite and a muted native Samantha playback, including
  pause/resume and cleanup; inspect desktop/mobile screenshots.
- [x] Refresh the production build, cache parameters, QA, and review records;
  run the related tests and full repository gates on the final source.
