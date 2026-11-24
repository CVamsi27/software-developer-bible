# Reader and Discovery Refinement Plan

**Goal:** Make reading controls coherent and remove confirmed navigation and information gaps while preserving the current product and publication boundary.

**Implementation:** Existing vanilla JavaScript, Cascading Style Sheets (CSS), and Jekyll. Use exact source ranges for highlighting and the current `Back to top` control, keep publication exclusions, make repository-only references explicit, and validate generated HTML after rendering as well as source Markdown before rendering.

1. Capture the current product flows and record confirmed issues and scope.
2. Add failing regression tests, then implement responsive arrow ownership and calmer paragraph, word, and callout styling.
3. Repair badge and repository-only links, testing their source validation and index completeness without weakening unrelated checks.
4. Add a rendered-link checker with controlled fixtures, wire it into `site-build`, and document its scope in the script map.
5. Rebuild, walk important flows across both themes and narrow screens, inspect screenshots and record residual limits, restamp counts and generated search metadata with their owning tools, and refresh scoped Markdown review hashes.
6. Run final gates and tests, following the previously authorized commit, push, and merge workflow once changes are concrete and verified.
