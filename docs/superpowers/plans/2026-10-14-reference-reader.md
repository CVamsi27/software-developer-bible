# Reference Reader Implementation Plan

> Execute inline in the isolated study-ui-restoration worktree. The user supplied the visual reference and explicitly requested planning and implementation.

**Goal:** Match the supplied dark reader screenshot while preserving canonical chapters.

**Architecture:** Keep Jekyll, the shared header and vanilla reader enhancements. Add a focused stylesheet loaded last; enrich metadata and code presentation without changing authored prose or clipboard text.

**Tech Stack:** Liquid, CSS, vanilla JavaScript, jsdom, Jekyll.

## Global constraints

- Retain clean URL activation, narration, revision and deliberate resume.
- Use screenshot layout and colors: dark background #0d1720, utility surfaces #1c2935, borders #2b3d4c, text #dce5ee, heading #f6f8fb, accent #4ab0ff.
- Desktop content uses a 920px article and 225px outline within a centered 1175px region; scale fluidly at smaller widths.
- Preserve real chapter text, headings and read times; never replace teaching content with mockup copy.
- Keep mobile controls usable, visible focus and light theme. Do not merge or deploy.

## Tasks

- [x] Test code text and copy preservation when adding line numbers, colored metadata and header search semantics.
- [x] Add header search form targeting the existing search page; keep Library and Roadmap navigation and theme control.
- [x] Build metadata as separate semantic tokens, omit root Library from the breadcrumb, add decorative line numbers outside code and narration.
- [x] Load a focused final stylesheet for screenshot geometry, typography, controls, outline, dividers and code syntax colors.
- [x] Run focused tests, render actual clean chapter URL at desktop and mobile sizes, capture screenshot, refine visible differences.
- [x] Run repository gates, generated metadata/count checks, and Jekyll build. Keep the result in the isolated branch for later review and merge.


## Full refinement pass

The user requested refinement of all elements including mobile views. Keep the approved reference and canonical content.

- [x] Consolidate the reference stylesheet, including light/dark tokens, tablet sizing, mobile header/toolbar, metadata wrapping, disclosure and continuation targets.
- [x] Give code panels named keyboard scroll regions; close mobile outline only after deliberate section selection; make the search shortcut focus the visible field.
- [x] Replace placeholder icons, refine syntax, and keep copied/narrated code unchanged.
- [x] Check 320, 390, 768, 1024 and 1487px layouts; inspect both themes, metadata expansion, outline navigation, search, copy and keyboard access.
- [x] Capture desktop and mobile evidence, run focused tests, pinned build and repository gates, then commit on the isolated branch.


## Measured visual fidelity correction

The user clarified that the complete authored lesson must remain unchanged. Use a temporary content-matched fixture only to isolate CSS geometry; it is not the delivered chapter.

- [x] Compare at 1487 by 1058 with settled fonts, preserving actual lesson content in the delivered page.
- [x] Bundle the Inter font and its OFL license; remove the inherited clearfix flex item and heading bottom padding.
- [x] Correct header/search coordinates, article and outline widths, title tracking, metadata baseline, section spacing and toolbar alignment.
- [x] Verify actual chapter and responsive breakpoints with the locally bundled font; capture real-page evidence and rerun tests, build and repository gates.


## Final detail pass

- [x] Inspect visual anchors, font loading, metadata expansion, light/dark contrast and copy accuracy.
- [x] Add live copy success/failure feedback and exclude that feedback from narration; verify with DOM tests.
- [x] Align theme-button DOM order with desktop/mobile visual order and preserve focus across the breakpoint.
- [x] Version the theme script through its existing config owner so cached clients receive updated behavior.
- [x] Reproduce and fix final-section outline highlighting at the document bottom.
- [x] Verify real tab order, keyboard code scrolling, end-of-chapter focus/highlighting and both themes; run focused tests, build and repository verification.
