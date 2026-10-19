<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Patterns & Interview Prep — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Portals

Source: [Portals](10.3.5.01-portals.md)

**Q:** Which tree changes when a component uses a portal?

**A:** The content's DOM parent changes. Its position in React's tree continues to determine context and React event propagation.

**Q:** Can a native DOM listener on the original parent see a portal click by bubbling?

**A:** Only if that parent also lies on the actual DOM event path. React's synthetic propagation does not rewrite the native browser path.

**Q:** Why can portal roots declared as sibling JSX be unavailable during the same initial render?

**A:** JSX describes future DOM; those nodes exist only after commit. Put targets in the host HTML or wait until a ref/effect has obtained the committed element.

**Q:** Which nodes must a dropdown's outside-click check include?

**A:** Both its trigger and its portaled menu. Otherwise a menu interaction looks external and may unmount the item before its click handler runs.

**Q:** Why create and remove an owned portal container in an effect?

**A:** DOM mutation belongs after commit, and cleanup must undo the owned insertion. An abandoned render must not leave an attached container behind.

**Q:** Does `document.querySelector` skip portal content?

**A:** No; it searches the document's DOM normally. A query scoped to the original parent cannot reach content placed outside that subtree.

**Q:** What does a modal still need after being portaled and marked with `aria-modal`?

**A:** Focus entry, trapping and restoration, background interaction control, and an accessible name. A portal supplies placement rather than modal behavior.

**Q:** What happens if the portal receives a different container node on an update?

**A:** React recreates its content in the new target. Keep the container stable when preserving the subtree's state and avoiding extra work matters.

## Compound Components

Source: [Compound Components](10.3.5.02-compound-components.md)

**Q:** What does the parent own in a compound-component API?

**A:** It owns shared state and actions; child components consume that contract through context. Namespacing children is a public API convention, not the state-sharing mechanism.

**Q:** Can a consumer insert an extra wrapper between `<Tabs>` and `<Tabs.Tab>`?

**A:** Yes, context follows the React ancestry through ordinary wrappers. Direct-child cloning instead only inspects the elements supplied at that particular children boundary.

**Q:** Why does the select example register and unregister each option through immutable state updates?

**A:** Registration makes the selected label available to the trigger; cleanup removes a label when an option unmounts. A mutated Map keeps the same identity and schedules no render, so added or removed choices can leave the displayed label stale.

**Q:** Why can generic JSX on a parent fail to type its namespaced children?

**A:** Separate JSX elements do not inherit the parent's type parameter through context. A typed component factory creates one context and child API bound to a concrete item type.

**Q:** Why must a field's label, input, and error share generated IDs?

**A:** Matching `htmlFor`, `id`, and `aria-describedby` connects the displayed label and error to the same control. Each field instance needs distinct identifiers.

**Q:** Does `cloneElement` mutate the supplied child?

**A:** No; it returns a new element. Its trade-off is fragile prop injection and direct-child assumptions, rather than mutation of the original object.

**Q:** Does using `ReactNode` for children reject unrelated components at compile time?

**A:** No; it accepts arbitrary renderable nodes. Context guards can detect misplaced consumers at runtime, while stronger API-specific types require additional design.

**Q:** Which updates can memoizing a context value avoid?

**A:** It avoids context notifications caused solely by rebuilding an equivalent provider value. Changes to shared state still notify consumers, and parent rendering can independently render children.

**Q:** Why does the example require a controlled `value` prop instead of implying an uncontrolled mode?

**A:** The root owns only open/closed state; the caller owns the selected value. Making `value` required keeps that data contract explicit instead of suggesting a mode the implementation does not support.

## Changed identity and display contracts

Source: [Portals](10.3.5.01-portals.md), [Compound Components](10.3.5.02-compound-components.md)

**Q:** What log sequence does one portaled button click request in the bubbling example?

**A:** Its own handler queues the portal entry, then the logical React ancestor queues the outer entry. Native propagation follows the actual DOM path separately.

**Q:** Does setting z-index without checking the destination guarantee an overlay stays above the page?

**A:** No. Stacking contexts, positioning and the browser top layer still govern visibility. A portal changes ancestry rather than granting global priority.

**Q:** What happens to a form draft if an inactive tab panel returns `null`?

**A:** React unmounts the panel’s children, so their local state is discarded. Keep the panel mounted or move the draft state to an owner that survives the tab switch; account for Effects that remain active in a hidden mounted panel.

**Q:** What must change if compound tab children can be reordered?

**A:** Use stable values instead of positional selection and define removal/reset behavior; otherwise the same selected index can identify a different tab.

**Q:** Why can selected object state become obsolete in a generic list?

**A:** Replacing the input item objects does not replace the stored selected object. A key-owned selection can derive the current item or detect its removal.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
