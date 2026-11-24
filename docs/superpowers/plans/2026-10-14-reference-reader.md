# Reference Reader Implementation Plan

> Execute inline in the isolated `study-ui-restoration` worktree. The user supplied the visual reference and explicitly requested planning and implementation.

**Goal:** Match the supplied dark reader screenshot while preserving canonical chapters.

**Architecture:** Keep Jekyll, the shared header, and vanilla reader enhancements. Add a focused stylesheet loaded last, enriching metadata and code presentation without changing authored prose or clipboard text.

**Tech Stack:** Liquid, Cascading Style Sheets (CSS), vanilla JavaScript, `jsdom`, and Jekyll.

## Global constraints

- Retain clean URL activation, narration, revision, and deliberate resume.
- Use screenshot layout and colors: dark background `#0d1720`, utility surfaces `#1c2935`, borders `#2b3d4c`, text `#dce5ee`, heading `#f6f8fb`, and accent `#4ab0ff`.
- Desktop content uses a 920-pixel article and 225-pixel outline within a centered 1,175-pixel region, scaling fluidly at smaller widths.
- Preserve real chapter text, headings, and read times; never replace teaching content with mockup copy.
- Keep mobile controls usable alongside visible focus and light theme; do not merge or deploy.

## Tasks

- [x] Test code text and copy preservation when adding line numbers, colored metadata, and header search semantics.
- [x] Add a header search form targeting the existing search page while keeping Library and Roadmap navigation and the theme control.
- [x] Build metadata as separate semantic tokens, omit root Library from the breadcrumb, and add decorative line numbers outside code and narration.
- [x] Load a focused final stylesheet for screenshot geometry, typography, controls, outline, dividers, and code syntax colors.
- [x] Run focused tests, render an actual clean chapter URL at desktop and mobile sizes, capture screenshots, and refine visible differences.
- [x] Run repository gates, generated metadata and count checks, and the Jekyll build, keeping the result in the isolated branch for later review and merge.

## Full refinement pass

The user requested refinement of all elements including mobile views; keep the approved reference and canonical content.

- [x] Consolidate the reference stylesheet, including light and dark tokens, tablet sizing, mobile header and toolbar, metadata wrapping, disclosure, and continuation targets.
- [x] Give code panels named keyboard scroll regions, close the mobile outline only after deliberate section selection, and make the search shortcut focus the visible field.
- [x] Replace placeholder icons, refine syntax, and keep copied and narrated code unchanged.
- [x] Check `320`, `390`, `768`, `1,024`, and `1,487` pixel layouts; inspect both themes, metadata expansion, outline navigation, search, copy, and keyboard access.
- [x] Capture desktop and mobile evidence, run focused tests, pinned build, and repository gates, and commit on the isolated branch.

## Measured visual fidelity correction

The user clarified that the complete authored lesson must remain unchanged; use a temporary content-matched fixture only to isolate CSS geometry rather than as the delivered chapter.

- [x] Compare at `1,487` by `1,058` pixels with settled fonts while preserving actual lesson content in the delivered page.
- [x] Bundle the Inter font and its SIL Open Font License (OFL) license, and remove the inherited clearfix flex item and heading bottom padding.
- [x] Correct header and search coordinates, article and outline widths, title tracking, metadata baseline, section spacing, and toolbar alignment.
- [x] Verify the actual chapter and responsive breakpoints with the locally bundled font, capture real-page evidence, and rerun tests, build, and repository gates.

## Final detail pass

- [x] Inspect visual anchors, font loading, metadata expansion, light and dark contrast, and copy accuracy.
- [x] Add live copy success and failure feedback and exclude that feedback from narration; verify with Document Object Model (DOM) tests.
- [x] Align theme-button DOM order with desktop and mobile visual order and preserve focus across breakpoints.
- [x] Version the theme script through its config owner so cached clients receive updated behavior.
- [x] Reproduce and fix final-section outline highlighting at the document bottom.
- [x] Verify real tab order, keyboard code scrolling, end-of-chapter focus and highlighting, and both themes; run focused tests, build, and repository verification.

## Listen and width refinement

- [x] Align playback border joins, icons, typography, hover, and focus states.
- [x] Widen the width selector so `Comfortable` is visible in full while preserving native `<select>` behavior.
- [x] Wrap independent playback and width groups on phones; verify 44-pixel targets, both themes, and persisted settings.
- [x] Save desktop and mobile evidence, run tests, build, and repository gates, and commit in the isolated branch.
