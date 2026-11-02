# Read-Aloud Controls Design

## Goal

Make it easy to choose what to hear, keep the voice choices English-only, and
reduce controls around the chapter reader.

## Approved behavior

- The voice menu contains at most five English voices. Keep the current
  alphabetical voice-name order among English voices. Do not list voices for
  other languages or a generic system-default choice. Preserve a saved voice
  while it remains in the visible five; otherwise select the first available
  English voice. If the browser exposes no English voices, disable the menu and
  retain the reader's `en-US` language fallback.
- Clicking or tapping a readable paragraph selects that paragraph as the next
  narration start point and gives it a visible selected state. The **Listen**
  button starts at that selection; **Next** continues with the next source
  block. Without an explicit selection, **Listen** keeps its current behavior
  of starting at the first readable block at or below the reading line. Clicks
  on links or other interactive content inside a paragraph keep their normal
  behavior.
- Remove the Width dropdown, the persisted width preference, and the wide
  layout override. Keep the existing comfortable reading measure as the only
  reader width.
- On reader pages, place the existing back-to-top arrow beside the audio dock
  in the same horizontal row as **Listen**, with spacing that avoids overlap at
  narrow widths. On pages without the audio dock, the arrow keeps its existing
  floating position.

## Design choices

Paragraph selection uses the paragraph itself instead of adding a separate
button to every paragraph. This keeps the floating dock compact and avoids
repeating controls throughout long chapters. The selected paragraph must be
visually distinct from the paragraph currently being spoken, and the status
region must announce the selected paragraph so the choice is clear before
playback.

The arrow joins the reader dock rather than receiving a second fixed position.
That gives it a stable alignment with **Listen** and lets the dock's responsive
layout manage spacing on small screens.

## Boundaries

Keep the browser SpeechSynthesis API, speed control, pause/resume, stop, current
paragraph-follow behavior, and reduced-motion behavior. Do not add an external
audio service or change chapter text extraction. Width remains the established
comfortable measure; this change removes the choice, not the measure.

## Acceptance criteria

- The voice menu lists no more than five voices, all with an English locale,
  and never lists a generic default or non-English voice.
- Choosing a paragraph changes the pending start point; pressing **Listen**
  begins at that paragraph, and **Next** advances from there.
- Clicking a link inside a paragraph follows the link without selecting the
  paragraph for narration.
- No Reading width control or width preference remains in the reader UI; the
  article uses the comfortable measure.
- On reader pages, the back-to-top arrow aligns horizontally with **Listen**
  without overlapping the dock on narrow screens. Other pages retain the
  floating arrow.
- Existing narration behavior remains intact when there is no paragraph
  selection or no English voice is exposed by the browser.

## Verification scope

Review the reader behavior and responsive layout in a rendered chapter. Check
English voice filtering, paragraph selection and start position, the removed
width control, and the arrow alignment. Record any browser limitation when the
local environment does not expose SpeechSynthesis voices.
