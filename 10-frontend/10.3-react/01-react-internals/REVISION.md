<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# React Internals — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Virtual DOM

Source: [Virtual DOM](10.3.1.01-virtual-dom.md)

**Q:** What does React keep in memory in addition to the live DOM?

**A:** Element descriptions express desired output, while fibers retain identities, state and pending work. The browser still owns the actual document nodes.

**Q:** Why can a component run again without its DOM changing?

**A:** React compares the newly described output with the existing tree. If the output matches, the render needs no corresponding DOM mutation.

**Q:** Does a heuristic diff guarantee the fewest possible DOM operations?

**A:** No. Type and key matching avoid a costly search for an optimal edit sequence while preserving the identities React recognizes.

**Q:** Which problem do keys solve for a reordered list?

**A:** They associate each sibling with the same record across updates, preserving its instance and state. They do not independently prevent that component from rendering.

**Q:** What still runs when one dashboard metric changes?

**A:** The dashboard and ordinary child component functions may execute again. Reconciliation can nevertheless keep the DOM writes limited to changed output.

**Q:** Why can stable callback props fail to eliminate child renders?

**A:** An ordinary child renders with its parent; stable references matter when an identity-sensitive boundary such as memo checks them. They cannot substitute for that boundary.

**Q:** How should you compare direct DOM code with declarative rendering?

**A:** Measure the same interaction on comparable hardware, separating React computation, commit work and browser layout or paint. Fixed universal timings hide differences in workload.

## React Fiber

Source: [React Fiber](10.3.1.02-fiber.md)

**Q:** Why does a fiber contain more information than a React element?

**A:** A fiber persists a component identity together with its state, pending updates and scheduling metadata. An element only describes what should be rendered.

**Q:** What makes the current tree usable while another render is being prepared?

**A:** React builds a work-in-progress representation linked to current fibers through alternate pointers. It can discard unfinished work without publishing that partial tree.

**Q:** Can React interrupt an expensive synchronous loop inside a component?

**A:** It cannot preempt JavaScript midway through that loop. Cooperative yielding happens between work units, so expensive computation may need smaller units or a worker.

**Q:** Which phase changes the displayed DOM?

**A:** Commit publishes prepared changes and runs layout work. Render may prepare detached nodes and flags without mutating the displayed tree.

**Q:** Does fetching in an Effect activate a surrounding Suspense fallback?

**A:** No. Suspense responds to work that suspends during render, such as lazy code or a supported framework/data source. Fetching in an Effect does not suspend the render.

**Q:** Why does filtering data inside a transition callback still delay typing?

**A:** The callback runs immediately; transition marks setters rather than moving arbitrary computation off the main thread. Put the result-driving state update there and schedule the consuming render separately.

**Q:** Why should the controlled input value remain outside a transition?

**A:** An input must reflect its current event promptly. Deferred state can drive the expensive results view while the input itself stays urgent.

**Q:** Why are lane bitmasks and fiber sizes poor application contracts?

**A:** They are internal details that depend on React versions, build settings and runtimes. Supported scheduling APIs express intent without depending on those layouts.

## Reconciliation

Source: [Reconciliation](10.3.1.03-reconciliation.md)

**Q:** How does reconciliation avoid solving a general optimal tree-edit problem?

**A:** React uses element type and sibling identity to restrict matching. This makes updates practical while foregoing a guarantee of the optimal edit sequence.

**Q:** What identifies a keyed component strongly enough to preserve its state?

**A:** Its type and key must match within the same parent position. A key is scoped to siblings, so it does not carry state across different parents.

**Q:** Why must a replacement with an existing key still mark the old node for deletion?

**A:** Matching keys alone do not permit reuse when types differ. The new fiber must mount and the incompatible old fiber must be removed at commit.

**Q:** What does changing a tab panel key deliberately accomplish?

**A:** It removes the old panel instance and creates a new one, resetting its local state. Shared state kept above the panel can survive.

**Q:** What happens to item state when a reordered list uses indices as keys?

**A:** State remains attached to the position whose key matches, potentially becoming associated with another record. The issue is incorrect identity, not merely extra rendering.

**Q:** Why must a memo wrapper be declared outside its parent render?

**A:** Recreating the wrapper produces a different component type and can reset the child. A single stable wrapper lets prop comparisons determine whether parent-driven execution is skippable.

**Q:** What costs are outside the heuristic linear-diff description?

**A:** Component calculations, sorting, repeated render attempts and browser layout or paint can dominate total time. Linear matching alone does not bound the entire interaction.

## Rendering

Source: [Rendering](10.3.1.04-rendering.md)

**Q:** What is the difference between rendering a component and committing its output?

**A:** Rendering computes the requested UI and reconciles it. Commit publishes DOM changes and performs layout work for the accepted result.

**Q:** Does updating a child state force its ancestor functions to run again?

**A:** The update belongs to the child; ancestors need not execute again. An ordinary parent render, conversely, normally visits its children.

**Q:** Does a custom Hook returning a fresh object schedule a render by itself?

**A:** No. Hooks run within an already executing component, so a changed return reference is a result of rendering rather than an update source.

**Q:** Why must client components run during hydration even though the server produced HTML?

**A:** The client needs their matching output and interactive behavior to attach React to the existing document. Server HTML does not contain executable client handlers.

**Q:** Why should form validation derived from current fields avoid another state setter?

**A:** Computing errors directly makes them available in the same render. A second stored copy requires synchronization and another render attempt.

**Q:** When can flushSync help an external integration?

**A:** It can ensure requested DOM changes are available before the next line in a callback that requires synchronous access. Its broader flushing and performance costs make it an escape hatch.

**Q:** Why is a render log count different from the number of visible updates?

**A:** Strict Mode checks and concurrent restarts can execute components without separate commits. Profile committed work and browser activity alongside render attempts.

## Lifecycle

Source: [Lifecycle](10.3.1.05-lifecycle.md)

**Q:** What are the three broad stages in a component instance lifetime?

**A:** An instance mounts, may update repeatedly, and eventually unmounts. Side-effect resources should follow the relevant committed synchronization cycles within that lifetime.

**Q:** Why is a dependency-based effect not identical to componentDidUpdate?

**A:** It is set up on initial mount as well as after dependency changes. The class update callback excludes the initial mount.

**Q:** Why cannot useLayoutEffect directly replace getSnapshotBeforeUpdate?

**A:** The class snapshot method reads the old DOM before mutations. A layout effect sees the committed new DOM, so the observation point differs.

**Q:** Why should one effect own fetching a user rather than separate mount and update effects?

**A:** Both effect setups would run on mount and issue duplicate requests. A single dependency-based effect can also own cancellation, loading and error updates.

**Q:** What keeps a subscription tied to the currently selected channel?

**A:** Changing the channel triggers teardown of the old setup before a replacement setup. Unmount also releases the active resource.

**Q:** What does an extra Strict Mode setup and cleanup cycle test?

**A:** It checks whether teardown reverses setup and whether a replacement setup behaves correctly. It does not promise that synchronization happens only once.

**Q:** When should DOM measurement use a layout effect?

**A:** Use it when the measurement changes what must be displayed before paint. Ordinary external synchronization can use a passive effect after commit.

## Editable-row identity

Source: [Learning chapter](10.3.1.03-reconciliation.md)

**Q:** A row is filtered out and later restored with the same key. Does its draft survive?

**A:** Not merely because the key matches. Unmount removes its local state; retain drafts above the row or in a keyed store when restoration is required.

**Q:** Why can an index key show the right name but the wrong input draft after sorting?

**A:** The positional component identity survives while its record prop changes. The draft remains attached to that position instead of the domain record.

## Update and ownership boundaries

Source: [Virtual DOM](10.3.1.01-virtual-dom.md), [Fiber](10.3.1.02-fiber.md), [Rendering](10.3.1.04-rendering.md), [Lifecycle](10.3.1.05-lifecycle.md)

**Q:** A paragraph's text changes from 0 to 1. Must React replace its element node?

**A:** A same-type host element at the same identity can be retained while its text changes. New description objects do not imply new DOM nodes.

**Q:** A fiber has no child and no sibling. How does traversal find the next work item?

**A:** Completion follows its parent link, completes that parent and seeks the parent's sibling, continuing upward if necessary. These links encode a tree, not one flat list.

**Q:** Why does a memoized results view help separate urgent input from deferred filtering?

**A:** It can skip the urgent parent render while its result-driving query prop remains unchanged. The transition schedules the changed query's render; one long filter still cannot be interrupted midway.

**Q:** Does act() automatically finish a fetch controlled by an unresolved promise?

**A:** No. The test must resolve or reject the promise and coordinate the resulting React work. act() is not a network, timer or elapsed-time guarantee.

**Q:** Why can cancellation alone fail to keep the right profile visible?

**A:** It may arrive too late, and the already stored old result can remain during the new prop's first commit. Guard result publication and tie the displayed data to the requested identity.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
