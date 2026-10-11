# Study Flow Design QA

**Final result:** passed for the approved local study-flow design.

**Repository verification:** all 30 verification gates pass, including the refreshed citation baseline.

**Source visual truth:** [Refined reader](docs/superpowers/specs/assets/2026-10-11-study-flow/focused-reader-final.png), supported by the [approved behavior specification](docs/superpowers/specs/2026-10-11-study-flow-uiux-design.md).

**Implementation:** Existing Jekyll site built locally at `http://127.0.0.1:4340/`. The separately rendered home preview is `http://127.0.0.1:4340/home-preview.html` because the macOS filesystem cannot distinguish index.html from INDEX.html. The temporary local review server maps Home to that rendered preview and serves Library separately, so the complete local journey works. Production routes remain unchanged.

**Comparison state:** Lexical Environment, chapter start, dark theme, Wide selected, desktop outline open. Requested CSS viewport: 1440 × 1024. Source raster: 1487 × 1058. In-app browser capture: 1432 × 1018. The source is resized proportionally to the capture dimensions for comparison only; original assets are retained. Browser chrome is excluded. This is a comparison of the approved structure and visual direction, not a claim of pixel-exact reproduction of an abbreviated generated lesson.

## Findings and refinement

1. **[P2, fixed] Small section headings weakened the reading hierarchy.** The first combined comparison showed 24 px section headings against the target’s larger hierarchy. Desktop section headings now use 30 px, prose uses 18 px with the existing line spacing, and mobile retains 24 px headings. The chapter title remains 44 px at the desktop viewport.
2. **[P2, fixed] Copy controls were small and appeared only on hover.** Copy now has a visible 44 px target. Language labels come from the existing fence language class; code text and clipboard behavior are preserved.
3. **[P2, fixed] The mobile outline preceded the chapter context.** Below 1200 px the outline now follows the title and metadata as a closed disclosure. Desktop retains the adjacent, sticky outline. Long breadcrumbs use their immediate stack/category links on narrow screens.
4. **[P2, fixed] The mobile search input competed with Clear search.** The query now occupies a full mobile row, with its clear action below. Stack and Material remain directly available.
5. **[P2, fixed] Returning-home actions competed with Resume.** Resume is now the primary action when a valid position exists. The generic intro becomes compact, search becomes secondary, and the inherited home heading is hidden. Clearing restores the first-visit state; Undo restores the returning state.
6. **[P2, fixed] The desktop mobile-menu label remained a zero-sized keyboard target.** An explicit desktop display rule removes it; the mobile 44 px control remains available.
7. **[Correctness, fixed] Lesson badges could be mistaken for header metadata.** Only badges before the authored title move into Chapter details. A failing regression test reproduced the issue; the fix preserves body-badge paragraphs in their original position.

Full-view evidence: [combined reader comparison](docs/superpowers/specs/assets/2026-10-11-study-flow/reader-comparison.png). Focused evidence: [chapter header comparison](docs/superpowers/specs/assets/2026-10-11-study-flow/reader-header-comparison.png). The post-fix comparison was captured and reviewed after the fixes above; no actionable P0/P1/P2 differences remain within the approved scope. Post-fix implementation: [desktop reader](docs/superpowers/specs/assets/2026-10-11-study-flow/implemented-reader-desktop.png), [mobile light](docs/superpowers/specs/assets/2026-10-11-study-flow/implemented-reader-mobile-light.png), [mobile dark](docs/superpowers/specs/assets/2026-10-11-study-flow/implemented-reader-mobile-dark.png).

## Fidelity surfaces

- **Fonts and typography:** Existing system sans family and fallback are retained. Desktop title/section/body hierarchy is 44/30/18 px. Navigation, metadata and tools use smaller optical sizes. Mobile wraps without truncating chapter titles; navigation keeps its existing ellipsis behavior for the brand.
- **Spacing and layout rhythm:** Title, restrained metadata, outline and onward actions follow the refined direction. Wide remains the existing default, so the article is broader than the generated reference; Comfortable constrains prose to 72ch while code and tables keep their own region. All lesson paragraphs remain present, so the example and continuation appear lower than in the abbreviated mockup.
- **Colors and visual tokens:** Existing slate, blue, light/dark, border and syntax tokens remain the source of truth. Listening is a secondary surface. Active outline links have both a border and aria-current. Focus remains visibly outlined.
- **Image quality and asset fidelity:** No new raster assets are required by the implemented UI. Existing theme/menu icons are reused. Source metadata badges are preserved under Chapter details. Generated references are design evidence, not substituted content.
- **Copy and content:** Every authored lesson paragraph, example, source group, revision question and answer remains canonical. UI labels follow the specification. Header Search is a navigation link, consistent with the approved compact header, rather than the generated mockup’s embedded field. Resume represents a reading position, never completion or mastery.

## Behavior evidence

- Search: query + Revision returned the actual Execution & Scope companion; browser Back restored both query and material. Clear filters retained the query. No matches showed the recovery state. Native result links and filters remained usable at 320 px.
- Reader: explicit outline navigation focused the destination and marked it current. Width persisted after reload. Next and revision actions used actual authored, published destinations. Listen entered reading, Pause entered paused, and Stop returned to idle.
- Revision: the real companion created 30 disclosures. Show all opened all 30; Hide all closed them; individual reveal worked. Complete multi-paragraph/code/list answers are covered by DOM tests. Interview banks are untouched. Before/after print opens all answers then restores the disclosure state.
- Resume: outline activity saved the selected section. Home displayed the saved chapter. Resume returned to its section; reload retained width and the explicit fragment. Clear hid the card; Undo restored it. Unit/DOM tests cover denied storage, corrupt records, unknown versions, removed paths/anchors, explicit fragment precedence, query exclusion, non-learning pages and pagehide flushing.
- Accessibility: observed 44 × 44 mobile menu/theme controls with separate hit regions, visible labels, native details/selects/buttons, focus movement only on explicit navigation, and no whole-page overflow at 320 px in both themes. Reduced-motion rules are retained. This is not a screen-reader or WCAG certification.
- Browser console: no JavaScript errors observed during the inspected flow.

## Verification

Focused test command:

```bash
npm install --prefix /tmp/bible-study-ui-test --no-audit --no-fund jsdom@26.1.0
NODE_PATH=/tmp/bible-study-ui-test/node_modules node --test assets/study-ui.test.cjs assets/study-state.test.cjs assets/read-aloud.test.cjs scripts/roadmap-return.test.cjs
```

All 24 focused tests pass. CI is configured to run the DOM tests with the same development-only jsdom version, and the repository verification gate includes dependency-free study-state tests. The pinned Jekyll build passes. Search and the API metadata contract regenerate deterministically; the API corpus digest includes the current unrelated authored edits without changing the schema.

Final link validation reports zero broken links. The complete repository verification passes all 30 gates. Before committing, the NIST source added by the [auth interview edit](20-backend/20.5-security/01-auth/20.5.1.11-interview-questions.md) was verified live. Both dead CMU paper citations in the [probabilistic structures chapter](30-architecture/30.2-system-design/01-theory/30.2.1.17-probabilistic-data-structures.md) were replaced with the paper author’s live CMU copy; its title and PDF body were checked, and the repository probe returned HTTP 200. The citation baseline and API corpus digest were regenerated together with these edits. The QA report is explicitly excluded from chapter/template/read-time scope so it cannot become a study result or change reading estimates.

Dark-reader DOM samples measured body text at 13.16:1, metadata at 8.37:1, outline links at 7.03:1 and the title at 17.08:1 against the body surface. These samples do not certify every state or token.

Implementation checklist: search, reader, revision, resume, responsive inspection, combined comparison, focused tests and pinned build are complete. Production authentication and case-sensitive routing remain outside this local verification.

## Remaining limits

The authenticated production site was not inspected. Linux/case-sensitive root and Library routing still need the normal deployment check. No live deployment was performed. The user subsequently authorized committing and pushing the changes on the study-flow branch. Storage denied by the browser cannot provide cross-page or cross-session persistence; the controls remain usable in memory within the current page. No reading completion, cross-device sync, semantic search or analytics is implied.
