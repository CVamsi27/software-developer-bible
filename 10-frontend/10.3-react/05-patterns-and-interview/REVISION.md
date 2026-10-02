<!-- section: React | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Patterns & Interview Prep — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Portals

Source: [Portals](10.3.5.01-portals.md)

**Definition**

1. **Q:** Which tree changes when a component uses a portal?
   **A:** The content's DOM parent changes. Its position in React's tree continues to determine context and React event propagation.

**How It Works**

2. **Q:** Can a native DOM listener on the original parent see a portal click by bubbling?
   **A:** Only if that parent also lies on the actual DOM event path. React's synthetic propagation does not rewrite the native browser path.

**Code Examples**

3. **Q:** Why can portal roots declared as sibling JSX be unavailable during the same initial render?
   **A:** JSX describes future DOM; those nodes exist only after commit. Put targets in the host HTML or wait until a ref/effect has obtained the committed element.

4. **Q:** Which nodes must a dropdown's outside-click check include?
   **A:** Both its trigger and its portaled menu. Otherwise a menu interaction looks external and may unmount the item before its click handler runs.

5. **Q:** Why create and remove an owned portal container in an effect?
   **A:** DOM mutation belongs after commit, and cleanup must undo the owned insertion. An abandoned render must not leave an attached container behind.

**Common Mistakes**

6. **Q:** Does `document.querySelector` skip portal content?
   **A:** No; it searches the document's DOM normally. A query scoped to the original parent cannot reach content placed outside that subtree.

**Best Practices**

7. **Q:** What does a modal still need after being portaled and marked with `aria-modal`?
   **A:** Focus entry, trapping and restoration, background interaction control, and an accessible name. A portal supplies placement rather than modal behavior.

**Performance Considerations**

8. **Q:** What happens if the portal receives a different container node on an update?
   **A:** React recreates its content in the new target. Keep the container stable when preserving the subtree's state and avoiding extra work matters.

## Compound Components

Source: [Compound Components](10.3.5.02-compound-components.md)

**Definition**

1. **Q:** What does the parent own in a compound-component API?
   **A:** It owns shared state and actions; child components consume that contract through context. Namespacing children is a public API convention, not the state-sharing mechanism.

**How It Works**

2. **Q:** Can a consumer insert an extra wrapper between `<Tabs>` and `<Tabs.Tab>`?
   **A:** Yes, context follows the React ancestry through ordinary wrappers. Direct-child cloning instead only inspects the elements supplied at that particular children boundary.

**Code Examples**

3. **Q:** Why must option registration update state rather than mutate a stored Map?
   **A:** Mutating the Map preserves its identity and schedules no render, so the selected label can remain stale. An immutable state update lets the trigger observe registered labels.

4. **Q:** Why can generic JSX on a parent fail to type its namespaced children?
   **A:** Separate JSX elements do not inherit the parent's type parameter through context. A typed component factory creates one context and child API bound to a concrete item type.

5. **Q:** Why must a field's label, input, and error share generated IDs?
   **A:** Matching `htmlFor`, `id`, and `aria-describedby` connects the displayed label and error to the same control. Each field instance needs distinct identifiers.

**Common Mistakes**

6. **Q:** Does `cloneElement` mutate the supplied child?
   **A:** No; it returns a new element. Its trade-off is fragile prop injection and direct-child assumptions, rather than mutation of the original object.

7. **Q:** Does using `ReactNode` for children reject unrelated components at compile time?
   **A:** No; it accepts arbitrary renderable nodes. Context guards can detect misplaced consumers at runtime, while stronger API-specific types require additional design.

**Performance Considerations**

8. **Q:** Which updates can memoizing a context value avoid?
   **A:** It avoids context notifications caused solely by rebuilding an equivalent provider value. Changes to shared state still notify consumers, and parent rendering can independently render children.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
