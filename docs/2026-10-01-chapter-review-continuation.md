# Chapter Review Continuation

> **Dated review record:** counts, test results, and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-25-fullstack-coverage-review.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

The shared OpenCode conversation established four linked requirements: correct
technical inaccuracies, explain missing mechanisms, remove repeated teaching,
and end concept chapters with Summary → Revision Questions → See Also.

That initial contract was superseded by the user's later 2026-10-01 request:
remove `TL;DR`, improve the reading flow, and move practice into separate
section revision companions. The core frontend wave below ran before the wider
reading-flow pass; active review now covers all Markdown sections, including
indexes and companion guides.

## Scope and remaining work

The earlier core wave covered JavaScript bounded concurrency, TypeScript
transformation, advanced, and interview material, React internals, hooks, and
composition, and Next.js. Its findings and validation describe that wave's
scope rather than a completed corpus audit.

**The corpus-wide editorial audit is still incomplete.** Reviewers maintain
path-level ledgers of actual prose reads, corrections, and example probes;
mechanical template migration, generated metadata, and passing structural gates
do not establish that every explanation has been reviewed.

The updated contract removes `TL;DR`, keeps one opening definition, and moves
questions into one separate `REVISION.md` per category. Category indexes end
their learning stages with revision while interview banks remain distinct
drills, introducing new terms in plain language before listing variants. The
lexical-environment complaint prompted a full rewrite: a name-lookup trace
precedes `"Inside a lexical environment: what the Environment Record stores"`,
and its three JavaScript examples ran successfully.

Remaining work includes unread chapters and indexes across the corpus,
revision-companion coverage, technical-source checks, and final integration. Do
not manufacture questions from headings or mark files reviewed merely because a
format checker passes.

## Findings addressed

| Area | Corrections and missing mechanisms |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JavaScript concurrency | Promise aggregation versus task starts; request versus socket count; rate versus concurrency limits; rejection versus cancellation; invalid budgets; complete outcomes for queued tasks after abort |
| TypeScript | Actual compiler behavior for type extraction, brands, inference, and decorators; declaration-file scope and emission; working state transitions and runtime parsing at API boundaries |
| React rendering and hooks | Removed fabricated timing claims; corrected keys, synchronous transition callbacks, hydration API, update queues, effect timing, callback identity, and context contracts |
| React composition | React 19 custom-event and property support; safe literal custom-element text; real lazy Data Mode exports and concurrent loader guards; portal target lifetime, inside-click detection, reactive option registries, and typed component factories |
| Next.js | Client Component prerendering; async request APIs; version-scoped middleware and proxy behavior; cache identity and invalidation; valid rendering, data, and deployment examples |

Repeated full examples now point to their canonical sections, unique facts from
retired cheat sheets live in the body, and concept questions test mechanisms
and failure cases in fresh wording without adding a second question section to
interview banks.

## Evidence and regression protection

Chapter examples were checked against official framework documentation and
local compilers and runtimes. Executable probes cover React 19 custom events
and properties, the controlled select's initial label, portal inside/outside
clicks, custom-element literal text, promise-pool concurrency, order, error, and
abort behavior, and the generic compound-component factory under strict
TypeScript checking.

Independent reruns also cover React update queues and effect cleanup, seven
strictly typechecked custom hooks, storage replay safety, latest-request wins,
fetch cancellation, shared-store subscribers, and WebSocket teardown. All 57
TypeScript compiler and runtime fixtures pass; Next.js source-extracted probes
verify JavaScript Object Notation for Linked Data (JSON-LD) escaping, experiment
cookies, and role-based access control (RBAC) route specificity (there is no
standalone Next.js build in this repository).

The link scanner now inventories headings and navigation inside whole-document
Liquid raw wrappers (previously it skipped real chapters and rejected valid
cross-chapter anchors), with a regression case preserving exclusion of inline
raw examples.

The [freshness gate](verification-gates.md) rejects nonexistent `hydrateRoot`
`onHydrated` options and removed `NextRequest.geo` usage in Next.js code fences.
Defect and clean cases in `scripts/test_gates.py` prove detection and keep
unrelated custom callbacks, legacy API names in prose, or geolocation code
outside Next.js valid.

Final integration runs the full repository verification suite after regenerating
reading times, navigation and search data, and measured counts; commit and push
occur only after full review and required gates pass.
