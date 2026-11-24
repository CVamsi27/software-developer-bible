# Listening Experience

## Goal

Make chapter listening easy to configure, follow, and control using voices
already available on the device. This supersedes the voice shortlist and
playback defaults in the November 2 read-aloud design.

## Interaction

Use a fixed, compact player with the chapter title, visible playback status, passage count, progress bar, previous and next passage buttons, `Listen`, `Pause` or `Resume`, and `Stop`. An Audio settings disclosure is available before playback while keeping existing paragraph selection and start-from-view behavior; the chapter continues by default, and a `One passage at a time` mode preserves deliberate study pauses.

Settings contain voice, a sample preview, speed, playback mode, and a follow-text checkbox, remembering choices locally. Offer every tenth from `0.2` through `2.0`, retaining `0.75` and `1.25`, and show the current speed in the collapsed player. Changing speed or voice applies at the latest reported word boundary; without boundary events, replay only the current short chunk.

Pause cancels the current utterance and retains its position, while resume creates a fresh utterance so playback avoids depending on inconsistent native pause behavior. Preview pauses chapter speech and leaves it paused afterward without advancing the chapter, and completion, error, and cancellation handlers ignore obsolete speech events.

## Spoken word and paragraph

Keep the source paragraph highlighted and give the word currently being spoken a stronger accent background and contrasting text. Use speech word-boundary events and their character offsets; when word length is unavailable, identify the word from chunk text while preserving offsets after pause, resume, and live voice or speed changes.

Map normalized speech characters back to source text nodes, including whitespace between adjacent inline elements and words split by emphasis or inline code. Use a Cascading Style Sheets (CSS) Custom Highlight range without rewriting the chapter or changing the reader's selection; if that API is unavailable, draw non-interactive range rectangles and refresh them on scrolling or reflow. Follow the current word when follow-text is enabled, freeze the word on pause, clear obsolete word highlights on new chunks, navigation, passage completion, stop, error, and departure, and retain paragraph highlights for voices without word-boundary events.

## Voice selection

Use only English voices returned by `SpeechSynthesis` with `localService` enabled. Prefer Samantha, including premium and enhanced variants, then voices whose names indicate `premium`, `enhanced`, `natural`, or `neural` variants; filter known novelty and robot voices, deduplicate voice Uniform Resource Identifiers (URIs), and sort ties deterministically.

Show up to five suggestions with remaining eligible installed voices in a separate option group. Keep an explicit saved choice when available, migrating the old saved choice only if it remains a suggested voice.

Because voice metadata cannot prove perceived quality, label suggestions honestly and provide a preview. Refresh selection when voices arrive asynchronously without overriding a manual choice, and with no eligible local English voice, disable playback and explain how to enable a device voice rather than falling back to an unspecified system or network voice.

## Presentation and verification

Keep the reader's type and theme tokens, using a quiet, rounded dock with a slim passage-progress line and a settings panel above the transport. On small screens, stack settings and retain 44-pixel controls; in short viewports, scroll the settings panel internally, let `Escape` close settings and restore focus, ensure follow-text respects reduced motion and can be disabled, and reserve page-bottom space for the actual dock height.

Verify engine sequencing, rates, boundary bookmarks, cancellation, and voice ranking with Node tests. Verify settings, previews, persistence, continuous and manual playback, delayed and absent voices, keyboard access, contrast, and responsive layout in Chromium, inspecting rendered chapters in both themes; browser speech is substituted in automated tests, so device-specific audible quality needs a human preview alongside running repository gates and recording actual results.
