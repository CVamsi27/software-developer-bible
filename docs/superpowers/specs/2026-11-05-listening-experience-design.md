# Listening experience

## Goal

Make chapter listening easy to configure, follow, and control using voices
already available on the device. This supersedes the voice shortlist and
playback defaults in the November 2 read-aloud design.

## Interaction

Use a fixed, compact player with the chapter title, visible playback status,
passage count, progress bar, previous/next passage, Listen/Pause/Resume, and Stop.
An Audio settings disclosure is available before playback. Keep the existing
paragraph selection and start-from-view behavior. The chapter continues by
default; a One passage at a time mode preserves deliberate study pauses.

Settings contain voice, a sample preview, speed, playback mode, and a follow-text
checkbox. Remember these choices locally. Offer every tenth from 0.2 through
2.0, retaining the existing 0.75 and 1.25 choices. Show the current speed in the
collapsed player. Changing speed or voice applies at the latest reported word
boundary; without boundary events, replay only the current short chunk.

Pause cancels the current utterance and retains its position. Resume creates a
fresh utterance, avoiding dependence on inconsistent native pause behavior.
Preview pauses chapter speech and leaves it paused afterward; it never advances
the chapter. Completion, errors, and cancellation ignore obsolete speech events.

## Spoken word and paragraph

Keep the source paragraph highlighted and give the word currently being spoken
a stronger accent background and contrasting text. Use speech word-boundary
events and their character offsets; when word length is unavailable, identify
the word from the chunk text. Preserve offsets into the original chunk after
pause/resume and live voice/speed changes.

Map normalized speech characters back to source text nodes, including whitespace
between adjacent inline elements and words split by emphasis or inline code.
Use a CSS Custom Highlight range without rewriting the chapter or changing the
reader's selection. If that API is unavailable, draw non-interactive range
rectangles and refresh them on scrolling or reflow. Follow the current word
when follow-text is enabled. Pause freezes the word; a new chunk, navigation,
passage completion, stop, error, and departure clear obsolete word highlights.
Voices without word-boundary events retain the paragraph highlight.

## Voice selection

Use only English voices returned by SpeechSynthesis with localService true.
Prefer Samantha, including its premium/enhanced variants, then voices whose
names indicate premium, enhanced, natural, or neural variants. Filter known
novelty/robot voices, deduplicate voice URIs, and sort ties deterministically.
Show up to five suggestions, with remaining eligible installed voices in a
separate option group. Keep an explicit saved choice when it is still available.
Migrate the old saved choice only if it is still a suggested voice.

Voice metadata cannot prove perceived quality. Label suggestions honestly and
provide a preview. When voices arrive asynchronously, refresh the selection
without overriding a manual choice. With no eligible local English voice,
disable playback and explain how to enable a device voice; do not invoke an
unspecified system or network voice.

## Presentation and verification

Keep the reader's existing type and theme tokens. Use a quiet, rounded dock with
a slim passage-progress line and a settings panel above the transport. On small
screens, stack settings and retain 44-pixel controls. In short viewports, scroll
the settings panel internally. Escape closes settings and restores focus.
Follow-text respects reduced motion and can be disabled. Reserve page-bottom
space for the actual dock height.

Verify engine sequencing, rates, boundary bookmarks, cancellation, and voice
ranking with Node tests. Verify settings, previews, persistence, continuous and
manual playback, delayed/absent voices, keyboard access, contrast, and responsive
layout in Chromium. Inspect real rendered chapters in both themes. Browser
speech is substituted in automated tests; device-specific audible quality needs
a human preview. Run the repository gates and record their actual result.
