# Read Aloud Implementation Plan

**Goal:** Read study chapters using browser speech, with play, pause/resume, stop and speed controls.

**Architecture:** One shared browser script owns chapter extraction, short utterance sequencing and playback state. The shared Jekyll head loads it; navigation and code blocks are omitted. Browser voices determine audio quality; no application TTS backend is added. Departure cancels narration.

**Tech Stack:** Browser SpeechSynthesis, plain JavaScript, Node test runner and Jekyll.

## Tasks

- [x] Test chunking, playback progression, paused completion, cancellation and errors before implementation.
- [x] Implement the controller and content extraction; inject an accessible toolbar into chapter content.
- [x] Check unsupported-browser behavior and real rendered chapter extraction in a browser.
- [ ] Run repository gates, build, commit, push and check deployment status.

## Reading behavior

Read headings, prose, list items and table cells in document order. Omit navigation, metadata badges, code blocks and generated copy/anchor controls. Inline code remains part of prose. Speed changes take effect at the next short utterance. Stop resets to the start; restart is explicit. Unsupported speech shows a clear unavailable message. Controls remain usable with keyboard and on narrow screens.

## Reproducing the checks

Run `node --test assets/read-aloud.test.cjs` for playback behavior. Build Jekyll and serve its output on loopback port 4337, then run `node scripts/test_read_aloud_browser.cjs` in an environment with `@playwright/test` and Chromium installed. `STUDY_TEST_URL` can point to another rendered lexical-environment page; `STUDY_SCREENSHOT` saves a preview. Browser tests substitute the external speech service to verify text and controls; they do not prove audible output or voice quality on every device. Device/browser voices may use local or network-backed speech services.
