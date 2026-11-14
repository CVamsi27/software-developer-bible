# Reader and Discovery Refinement

## Goal

Align Back to top with the listening dock, improve simultaneous word/paragraph
emphasis, and repair important problems found while walking the learning flow.
Keep the existing Wide reader, local voice engine, theme, and publication rules.

## Reading controls

On wide screens, the up-arrow sits alongside the dock at its vertical center.
On phones and tablets it sits in the dock's information row, leaving the
transport row's 44-pixel targets intact. Preserve its existing scroll behavior
and visibility threshold. An expanded settings panel must not overlap it.

Use a quieter paragraph tint and a distinct warm word marker with clear text
contrast. A paragraph inside a callout uses the callout's existing rail rather
than adding a second one. Highlighting must not move the text or change its
selection, markup, speech timing, or pause/resume behavior.

## Discovery and information

Capture the current home, library, roadmap, search, stack/category index, chapter,
revision, interview, and sign-in states. Check narrow screens and both themes.
Scan all rendered pages for internal destinations and review the topic metadata
and learning-stage navigation. A complete semantic re-review of every teaching
paragraph is outside this product-flow pass; record that limit explicitly.

The SDE lane remains excluded from the site. Links to its already-public source
guides must point to the repository and say that they do. Preserve the source
folder's index completeness. Fix priority-badge destinations and make the source
link checker understand image links. References to excluded audit artifacts
should be described as repository artifacts rather than broken site links.

Resolve legacy Markdown badge destinations through the existing published-path
catalog before converting badges to chips. Preserve source links, queries and
fragments; never invent a route for an excluded file. Revision search results
show and search their category context so repeated titles remain distinguishable.
Suppress the browser's duplicate clear icon using separate vendor selectors.
Keep heading names concise for assistive technology while preserving separately
named permalink links. Interview banks receive the reader outline, metadata and
listening controls, while retaining their authored practice and resume exclusions.

Remove the legacy and character voice names observed in the device list. Keep
Samantha first and the existing local-only quality ordering. Correct sub-stack
badges through the count owner and separate prose from unintended Setext headings.

## Verification

Add regression checks for attached up-arrow ownership, source badge links,
repository-source index links, and rendered links. The rendered check must catch
missing files and fragments, allow existing Pages Function endpoints, and fail
on an empty site. Recognize catalog-backed client resolution separately from
actual raw repository documents. Local Home/Library aliases are an explicit test
option for case-insensitive filesystems; CI checks the native Linux artifact.
Wire it into the site build and script map. Recheck the flows
in the in-app browser, preserve screenshots and audit notes, and run the source
gates, related Node tests, production build, and rendered checks.
