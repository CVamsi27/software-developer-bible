# Read-Aloud Reader UI Design

## Problem

The read-aloud player currently takes a full row below the chapter title. It has no 0.5× speed option and does not keep the spoken paragraph in view. Its controls also do not consistently follow the reader's active theme.

## Design

Place a compact player at the right side of the chapter title, keeping the title and controls aligned on wide screens and allowing a clean wrap on narrow screens. Keep accessible names and status announcements while reducing visual weight. Add 0.5× to the existing speed choices.

Keep a source-element reference for each spoken text chunk. When speech starts for a chunk, mark its source block as active and scroll it into the visible reading area only when needed, using reduced-motion-aware behavior. Clear the active state when playback stops, completes, or errors.

Use the existing theme tokens for player surfaces, controls, text, focus rings, and active-block styling. Set native form-control color handling from the selected theme so the speed menu remains legible in light and dark modes.

## Boundaries and failures

Keep the browser SpeechSynthesis API and current play, pause/resume, stop, unsupported-browser, and error behavior. Do not change chapter extraction rules or add a server-side audio service. A missing source block must not interrupt narration. If speech synthesis is unavailable, keep the compact control disabled and its explanation accessible.

## Verification

Extend unit and browser coverage to verify 0.5× selection, chunk-to-source association, active-block follow and clearing, title-row placement, responsive width, and contrast-aware controls in both explicit themes. Run the relevant read-aloud tests and repository verification gates before committing or pushing.
