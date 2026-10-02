# Chapter Review Continuation

The shared OpenCode conversation established four linked requirements: correct
technical inaccuracies, explain missing mechanisms, remove repeated teaching,
and end concept chapters with Summary → Revision Questions → See Also.
That initial contract is superseded by the user’s later 2026-10-01 request:
remove TL;DR, improve the reading flow, and move practice into separate section
revision companions. The corpus-wide work now follows that newer contract.
The core frontend wave below was completed before the wider reading-flow pass.
The active review now covers all Markdown sections, including indexes and companion guides.

## Scope and remaining work

The earlier core wave covered JavaScript bounded concurrency, TypeScript transformation/advanced/interview material, React internals/hooks/composition and Next.js. Its findings and validation below describe that wave’s scope, not a completed corpus audit.

**The corpus-wide editorial audit is still incomplete.** Reviewers maintain path-level ledgers of actual prose reads, corrections and example probes. Mechanical template migration, generated metadata and a passing structural gate do not establish that every explanation has been reviewed.

The current contract removes TL;DR, keeps one opening definition, and puts questions in one separate `REVISION.md` per category. Category indexes end their learning stages with revision; dedicated interview banks remain their own drills. New terms must be introduced in plain language and connected to their role in the whole before listing variants. The lexical-environment complaint prompted a complete chapter rewrite: a name-lookup trace precedes the explicit “Inside a lexical environment: what the Environment Record stores” section. Its three JavaScript examples were executed successfully.

Remaining work includes unread chapters and indexes across the corpus, revised-companion coverage, technical-source checks and final integration. Do not generate questions from headings or mark files reviewed merely because a format checker passes.

## Findings addressed

| Area | Corrections and missing mechanisms |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JavaScript concurrency | Promise aggregation versus task starts; request versus socket count; rate versus concurrency limits; rejection versus cancellation; invalid budgets; complete outcomes for queued tasks after abort |
| TypeScript | Actual compiler behavior for type extraction, brands, inference and decorators; declaration-file scope/emission; working state transitions and runtime parsing at API boundaries |
| React rendering and hooks | Removed fabricated timing claims; corrected keys, synchronous transition callbacks, hydration API, update queues, effect timing, callback identity and context contracts |
| React composition | React 19 custom-event/property support; safe literal custom-element text; real lazy Data Mode exports and concurrent loader guards; portal target lifetime, inside-click detection, reactive option registries and typed component factories |
| Next.js | Client Component prerendering; async request APIs; version-scoped middleware/proxy behavior; cache identity/invalidation; valid rendering, data and deployment examples |

Repeated full examples are replaced by short pointers to their canonical
sections. Unique facts from retired cheat sheets are explained in the body;
concept questions cover mechanisms and failure cases in fresh wording.
Interview banks retain their existing drill without a second question section.

## Evidence and regression protection

The chapter examples were checked against official framework documentation and
local compilers/runtimes. Executable probes cover React 19 custom events and
properties, the controlled select's initial label, portal inside/outside clicks,
custom-element literal text, promise-pool concurrency/order/error/abort behavior,
and the generic compound-component factory under strict TypeScript checking.
Independent reruns also cover React update queues and effect cleanup, seven
strictly typechecked custom hooks, storage replay safety, latest-request wins,
fetch cancellation, shared-store subscribers and WebSocket teardown. All 57
TypeScript compiler/runtime fixtures pass. Next.js source-extracted probes
verify JSON-LD escaping, experiment cookies and RBAC route specificity; there
is no standalone Next.js application build in this documentation repository.

The link scanner now inventories headings and navigation inside whole-document
Liquid raw wrappers. Previously it skipped real chapters and rejected valid
cross-chapter anchors; a regression case also preserves exclusion of inline
raw examples.

The [freshness gate](verification-gates.md) now rejects a nonexistent
`hydrateRoot` `onHydrated` option and removed `NextRequest.geo` usage in Next.js
code fences. Defect/clean cases in `scripts/test_gates.py` prove both detection
and legitimate alternatives. The rules do not reject unrelated custom callbacks,
legacy API names in prose, or geolocation code outside the Next.js stack.

Final integration runs the full repository verification suite after regenerating
reading times, navigation/search data, and measured counts. The user has authorized a commit and push after the full review and required gates pass. Neither has been performed for the ongoing corpus pass.
