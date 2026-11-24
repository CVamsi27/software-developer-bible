# Read-Aloud Voice, Width, and Dock Design

## Goal

Make the best available English voices easier to find, use the reader's full
text column, and make the Listen dock clear and well-aligned at rest and during
playback.

## Approved behavior

- Keep only English voices in the menu, capped at five. Prefer available browser voices by this fixed name order: Samantha, Ava, Allison, Alex, and Victoria; if one is unavailable, fill the remaining slots with other English browser voices in stable name, language, and Uniform Resource Identifier (URI) order. Version the saved voice key so a prior selection does not override the new shortlist, keep a saved voice only while it remains in the visible five, and if no English voice is available, disable the menu while retaining the `en-US` fallback.
- Remove the Width dropdown and all stored width preference behavior. Set prose, lists, quotes, alerts, and revision answers to use the full available article column instead of the former 62ch comfortable measure.
- Keep paragraph click selection as the narration start point. In the idle dock, show a short visible cue explaining "Click a paragraph, then Listen", update the cue after selection, and preserve the separate screen-reader live status.
- Keep Listen and the back-to-top arrow in the same aligned idle row. Correct the old reader-title transform that overrides centering of the fixed dock at desktop widths.
- During playback, present Listen, Pause, Next, and Stop as one compact action group, with voice and speed as clearly separated settings. Preserve responsive wrap behavior, visible keyboard focus, and existing speech interactions.

## Design choices

Voice labels are ranked with a fixed shortlist based on names the user identified as preferred. Because the browser supplies only voices installed and available in that session, missing names are skipped and remaining slots use stable name, language, and voice URI ordering; the user can still choose any of the five shown voices.

"Wide" means the full existing article column (the reader's grid remains capped at its existing page width), not extending text across the sidebar or browser viewport. The fixed dock stays compact while idle and makes the paragraph-selection instruction visible there instead of hiding the only cue inside a tooltip or live region.

## Boundaries

Keep the browser `SpeechSynthesis` API, paragraph extraction and selection, pause and resume, stop, next-block behavior, reduced-motion behavior, and `en-US` fallback. Do not add an external text-to-speech (TTS) service or dependencies, keep the five-voice maximum, and do not restore a width selector.

## Acceptance criteria

- The voice menu contains at most five English voices, with available Samantha, Ava, Allison, Alex, and Victoria voices first in order and remaining slots filled in stable name, language, and URI order.
- A saved voice is retained only if it remains in the visible five, selecting the first ranked English voice otherwise; a no-English state remains disabled with the existing fallback.
- No Width control, persisted width choice, or 62ch article-block cap remains, so text blocks fill the full reader column.
- The idle dock visibly explains paragraph selection and Listen, shows the selected paragraph state, and keeps the arrow vertically aligned beside Listen.
- The dock is horizontally centered on desktop, and at narrow widths controls wrap without overlap or horizontal scrolling.
- Playback actions and voice and speed settings remain keyboard accessible, with visible focus and existing speech state transitions.

## Verification scope

Review the implementation diff and existing reader checks. When a browser test runtime is available, cover ranking with mixed quality labels, local and remote voices, and non-English entries; wide text measure; idle instruction; dock centering and arrow alignment; and active playback layout.
