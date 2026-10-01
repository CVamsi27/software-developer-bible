# Chapter Review Continuation

The shared OpenCode conversation established four linked requirements: correct
technical inaccuracies, explain missing mechanisms, remove repeated teaching,
and end concept chapters with Summary → Revision Questions → See Also.
This continuation resumes that contract against the current checkout and
finishes the shared conversation's interrupted core frontend wave.

## Scope and remaining work

The current batch covers the outstanding JavaScript bounded-concurrency chapter,
TypeScript transformation/advanced/interview material, React internals/hooks and
composition material, and the Next.js stack. The neighboring TypeScript
inference example also uses a distinct utility name instead of redeclaring the
built-in `ReturnType`. Previously completed chapters are retained unless this
audit finds a concrete defect.

**The corpus-wide audit is still incomplete.** Remaining frontend stacks
(forms, animation, HTML/CSS, mobile), backend, architecture, platform, quality,
realtime, strategy and interview-toolkit chapters require their own editorial
review. Template compliance and a green verification suite do not prove every
claim is correct; the template gate still permits existing retired cheat sheets
in the unprocessed corpus. Do not bulk-generate revision answers or mark those
chapters reviewed merely because their structure passes.

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
reading times, navigation/search data, and measured counts. No commit or push is
part of this continuation.
