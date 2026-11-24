# Final Performance and Reader UX Pass

## Goal

Make the site's page-weight check measure a real delivery concern, reduce repeated HTML payload, and improve the search page's failure and loading behavior without changing authored study content, anchors, IDs, navigation ownership, or publication rules.

The work happens in two phases:

1. Correct the performance measurement and remove avoidable repeated payload.
2. Verify the reader UI and make only concrete, evidence-backed user experience (UX) corrections.

## Diagnosis

The current production Jekyll build has nine pages above the 120,000-byte raw HTML threshold, with gzip sizes between 20.1 KB and 62.7 KB. The largest pages are legitimate interview, revision, project, and internal-plan documents, so splitting or deleting authored content solely to satisfy raw HTML size would damage the learning corpus without improving delivered transfer proportionally.

Every normal page also repeats approximately 24.8 KB of inline Cascading Style Sheets (CSS) and 13.6 KB of inline reader JavaScript, while the search page embeds approximately 120.7 KB of search metadata in its HTML. These are avoidable delivery and caching costs.

Existing browser UI checks cannot currently run in this checkout because `jsdom` and Playwright are not installed. The repository's static, rendered, and source gates remain available and will run after implementation.

## Phase 1 — performance and measurement

### Shared reader assets

Extract the existing inline reader stylesheet and reader behavior into versioned, cacheable assets and load them from the shared head in their existing order, preserving:

- theme initialization and visual behavior;
- reading progress, back-to-top, table overflow, code-copy, alerts, anchors, and keyboard search behavior;
- deferred reader script ordering;
- relative URL behavior under the configured Jekyll base URL.

This is a delivery refactor rather than a visual redesign: existing CSS and JavaScript remain the source of behavior, with only their transport location changing.

### Search data

Extend the master-index generator to emit a relative, cacheable search data script so the generated search page loads that script rather than embedding the full metadata array in an inline JavaScript Object Notation (JSON) element. The script must work from both HTTP and `file://` previews without requiring a network API or a personal binding.

Update the search client to:

- render a polite loading status while the data is unavailable;
- render the existing results once the generated data is present;
- render an actionable failure state linking to the full library if the data cannot load;
- preserve query, filter, Back-state, keyboard shortcut, and roadmap-context behavior.

### Page-weight check

Keep raw HTML, gzip bytes, and asset counts in `page-weight.json` for diagnosis and review evidence. Change the default enforcement check to use the portable gzip transport budget — the user-facing transfer metric — so legitimate long-form content is not treated as a defect, while naming the enforced metric and retaining raw-size reporting in command output and existing ledger fast evidence.

## Phase 2 — reader UX verification

Run available rendered-page and source checks against representative:

- home, library, search, and roadmap pages;
- chapter, revision, and interview pages;
- desktop and narrow mobile widths;
- light, dark, and system theme paths;
- keyboard navigation, search loading and error states, code-copy controls, outlines, anchors, and responsive tables.

Make a UI change only when a check exposes a concrete usability, accessibility, responsive-layout, or state-management defect. Do not add discretionary visual restyling or duplicate existing controls.

## Invariants and non-goals

- Preserve all authored prose, question-and-answer (Q&A) pairs, code, heading IDs, anchors, and file identities.
- Do not split or renumber long pages merely to lower raw HTML bytes.
- Do not expose private lane or personal data in generated search assets.
- Do not claim browser coverage when the browser dependency is unavailable.
- Do not change authentication, deployment, or Cloudflare behavior.
- Keep generated files synchronized through repository-owned writers.

## Validation and delivery

After both phases:

1. Generate search and API metadata and build with the pinned Ruby and Jekyll bundle.
2. Measure page weight and confirm the enforced gzip budget.
3. Run source, rendered-link, heading, prose, freshness, structure, and verification gates.
4. Run available Document Object Model (DOM) and browser tests, explicitly record unavailable optional dependencies, and run focused generated-page assertions.
5. Inspect the final diff and run `git diff --check`.
6. Create one implementation commit, push the working branch, merge it into `main`, push `main`, and verify the remote commit.
