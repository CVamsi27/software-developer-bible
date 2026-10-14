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
