<!-- section: React | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)

# React Internals — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Virtual DOM

Source: [Virtual DOM](10.3.1.01-virtual-dom.md)

**Definition**

1. **Q:** What does React keep in memory in addition to the live DOM?
   **A:** Element descriptions express desired output, while fibers retain identities, state and pending work. The browser still owns the actual document nodes.

**How It Works**

2. **Q:** Why can a component run again without its DOM changing?
   **A:** React compares the newly described output with the existing tree. If the output matches, the render needs no corresponding DOM mutation.

3. **Q:** Does a heuristic diff guarantee the fewest possible DOM operations?
   **A:** No. Type and key matching avoid a costly search for an optimal edit sequence while preserving the identities React recognizes.

**Code Examples**

4. **Q:** Which problem do keys solve for a reordered list?
   **A:** They associate each sibling with the same record across updates, preserving its instance and state. They do not independently prevent that component from rendering.

**Real-World Use Cases**

5. **Q:** What still runs when one dashboard metric changes?
   **A:** The dashboard and ordinary child component functions may execute again. Reconciliation can nevertheless keep the DOM writes limited to changed output.

**Common Mistakes**

6. **Q:** Why can stable callback props fail to eliminate child renders?
   **A:** An ordinary child renders with its parent; stable references matter when an identity-sensitive boundary such as memo checks them. They cannot substitute for that boundary.

**Performance Considerations**

7. **Q:** How should you compare direct DOM code with declarative rendering?
   **A:** Measure the same interaction on comparable hardware, separating React computation, commit work and browser layout or paint. Fixed universal timings hide differences in workload.

## React Fiber

Source: [React Fiber](10.3.1.02-fiber.md)

**Definition**

1. **Q:** Why does a fiber contain more information than a React element?
   **A:** A fiber persists a component identity together with its state, pending updates and scheduling metadata. An element only describes what should be rendered.

**How It Works**

2. **Q:** What makes the current tree usable while another render is being prepared?
   **A:** React builds a work-in-progress representation linked to current fibers through alternate pointers. It can discard unfinished work without publishing that partial tree.

3. **Q:** Can React interrupt an expensive synchronous loop inside a component?
   **A:** It cannot preempt JavaScript midway through that loop. Cooperative yielding happens between work units, so expensive computation may need smaller units or a worker.

4. **Q:** Which phase changes the displayed DOM?
   **A:** Commit publishes prepared changes and runs layout work. Render may prepare detached nodes and flags without mutating the displayed tree.

**Code Examples**

5. **Q:** Why does filtering data inside a transition callback still delay typing?
   **A:** The callback runs immediately; transition marks setters rather than moving arbitrary computation off the main thread. Put the result-driving state update there and schedule the consuming render separately.

**Common Mistakes**

6. **Q:** Why should the controlled input value remain outside a transition?
   **A:** An input must reflect its current event promptly. Deferred state can drive the expensive results view while the input itself stays urgent.

**Performance Considerations**

7. **Q:** Why are lane bitmasks and fiber sizes poor application contracts?
   **A:** They are internal details that depend on React versions, build settings and runtimes. Supported scheduling APIs express intent without depending on those layouts.

## Reconciliation

Source: [Reconciliation](10.3.1.03-reconciliation.md)

**Definition**

1. **Q:** How does reconciliation avoid solving a general optimal tree-edit problem?
   **A:** React uses element type and sibling identity to restrict matching. This makes updates practical while foregoing a guarantee of the optimal edit sequence.

**How It Works**

2. **Q:** What identifies a keyed component strongly enough to preserve its state?
   **A:** Its type and key must match within the same parent position. A key is scoped to siblings, so it does not carry state across different parents.

3. **Q:** Why must a replacement with an existing key still mark the old node for deletion?
   **A:** Matching keys alone do not permit reuse when types differ. The new fiber must mount and the incompatible old fiber must be removed at commit.

**Code Examples**

4. **Q:** What does changing a tab panel key deliberately accomplish?
   **A:** It removes the old panel instance and creates a new one, resetting its local state. Shared state kept above the panel can survive.

**Common Mistakes**

5. **Q:** What happens to item state when a reordered list uses indices as keys?
   **A:** State remains attached to the position whose key matches, potentially becoming associated with another record. The issue is incorrect identity, not merely extra rendering.

6. **Q:** Why must a memo wrapper be declared outside its parent render?
   **A:** Recreating the wrapper produces a different component type and can reset the child. A single stable wrapper lets prop comparisons determine whether parent-driven execution is skippable.

**Performance Considerations**

7. **Q:** What costs are outside the heuristic linear-diff description?
   **A:** Component calculations, sorting, repeated render attempts and browser layout or paint can dominate total time. Linear matching alone does not bound the entire interaction.

## Rendering

Source: [Rendering](10.3.1.04-rendering.md)

**Definition**

1. **Q:** What is the difference between rendering a component and committing its output?
   **A:** Rendering computes the requested UI and reconciles it. Commit publishes DOM changes and performs layout work for the accepted result.

**How It Works**

2. **Q:** Does updating a child state force its ancestor functions to run again?
   **A:** The update belongs to the child; ancestors need not execute again. An ordinary parent render, conversely, normally visits its children.

3. **Q:** Does a custom Hook returning a fresh object schedule a render by itself?
   **A:** No. Hooks run within an already executing component, so a changed return reference is a result of rendering rather than an update source.

**Code Examples**

4. **Q:** Why must client components run during hydration even though the server produced HTML?
   **A:** The client needs their matching output and interactive behavior to attach React to the existing document. Server HTML does not contain executable client handlers.

**Real-World Use Cases**

5. **Q:** Why should form validation derived from current fields avoid another state setter?
   **A:** Computing errors directly makes them available in the same render. A second stored copy requires synchronization and another render attempt.

**Common Mistakes**

6. **Q:** When can flushSync help an external integration?
   **A:** It can ensure requested DOM changes are available before the next line in a callback that requires synchronous access. Its broader flushing and performance costs make it an escape hatch.

**Performance Considerations**

7. **Q:** Why is a render log count different from the number of visible updates?
   **A:** Strict Mode checks and concurrent restarts can execute components without separate commits. Profile committed work and browser activity alongside render attempts.

## Lifecycle

Source: [Lifecycle](10.3.1.05-lifecycle.md)

**Definition**

1. **Q:** What are the three broad stages in a component instance lifetime?
   **A:** An instance mounts, may update repeatedly, and eventually unmounts. Side-effect resources should follow the relevant committed synchronization cycles within that lifetime.

**How It Works**

2. **Q:** Why is a dependency-based effect not identical to componentDidUpdate?
   **A:** It is set up on initial mount as well as after dependency changes. The class update callback excludes the initial mount.

3. **Q:** Why cannot useLayoutEffect directly replace getSnapshotBeforeUpdate?
   **A:** The class snapshot method reads the old DOM before mutations. A layout effect sees the committed new DOM, so the observation point differs.

**Code Examples**

4. **Q:** Why should one effect own fetching a user rather than separate mount and update effects?
   **A:** Both effect setups would run on mount and issue duplicate requests. A single dependency-based effect can also own cancellation, loading and error updates.

**Real-World Use Cases**

5. **Q:** What keeps a subscription tied to the currently selected channel?
   **A:** Changing the channel triggers teardown of the old setup before a replacement setup. Unmount also releases the active resource.

**Common Mistakes**

6. **Q:** What does an extra Strict Mode setup and cleanup cycle test?
   **A:** It checks whether teardown reverses setup and whether a replacement setup behaves correctly. It does not promise that synchronization happens only once.

**Performance Considerations**

7. **Q:** When should DOM measurement use a layout effect?
   **A:** Use it when the measurement changes what must be displayed before paint. Ordinary external synchronization can use a passive effect after commit.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
