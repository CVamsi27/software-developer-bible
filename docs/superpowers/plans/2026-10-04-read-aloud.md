# Read Aloud Implementation Plan

> **Historical design record:** requirements, example paths, and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md), and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; `TL;DR` and inline chapter cheat and revision sections are retired.

**Goal:** Read study chapters using browser speech with play, pause and resume, stop, and speed controls.

**Architecture:** One shared browser script owns chapter extraction, short utterance sequencing, and playback state, loaded from the shared Jekyll head while omitting navigation and code blocks. Browser voices determine audio quality, no application text-to-speech (TTS) backend is added, and page departure cancels narration.

**Tech Stack:** Browser `SpeechSynthesis`, plain JavaScript, Node test runner, and Jekyll.

## Tasks

- [x] Test chunking, playback progression, paused completion, cancellation, and errors before implementation.
- [x] Implement the controller and content extraction, and inject an accessible toolbar into chapter content.
- [x] Check unsupported-browser behavior and real rendered chapter extraction in a browser.
- [ ] Run repository gates, build, commit, push, and check deployment status.

## Reading behavior

Read headings, prose, list items, and table cells in document order while omitting navigation, metadata badges, code blocks, and generated copy or anchor controls; inline code remains part of prose.

Speed changes take effect at the next short utterance, Stop resets playback to the start, and restart is explicit. Unsupported speech shows a clear unavailable message, and controls remain usable via keyboard and on narrow screens.

## Reproducing the checks

Run `node --test assets/read-aloud.test.cjs` for playback behavior. Build Jekyll, serve its output on loopback port `4337`, and run `node scripts/test_read_aloud_browser.cjs` in an environment with `@playwright/test` and Chromium installed.

`STUDY_TEST_URL` can point to another rendered lexical-environment page, and `STUDY_SCREENSHOT` saves a preview. Browser tests substitute the external speech service to verify text and controls rather than proving audible output or voice quality on every device; device and browser voices may use local or network-backed speech services.
