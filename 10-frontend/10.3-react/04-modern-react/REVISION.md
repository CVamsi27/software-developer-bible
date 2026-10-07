<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Modern React — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Modern React Hooks: useTransition, useDeferredValue, use, useOptimistic, and React 19 APIs

Source: [Modern React Hooks: useTransition, useDeferredValue, use, useOptimistic, and React 19 APIs](10.3.4.01-modern-hooks-react18-19.md)

**First Principles**

1. **Q:** What single theme connects React 18's hooks and React 19's APIs?
   **A:** They give React explicit scheduling and resource lifetimes. Transitions and deferred values distinguish urgent feedback from eligible background rendering; Actions coordinate async mutations, while optimistic state supplies a temporary proposal over a confirmed base. Error presentation, stable resource ownership and persistence remain application responsibilities.

2. **Q:** When do you reach for `useTransition` versus `useDeferredValue`?
   **A:** Transition when you own the setter — you wrap the slow `setState` yourself and `isPending` reports on it. Deferred value when the slow input arrives as a prop or from elsewhere — you can't wrap its producer, so `useDeferredValue` hands back a lagging copy for the expensive render.

**How It Works**

3. **Q:** What does `startTransition` actually mark as non-urgent, and what is the async caveat?
   **A:** Only updates scheduled *synchronously* inside the callback are marked as Transitions; work awaited inside is included, but a `set()` called after an `await` currently is not — React documents wrapping that call in a second `startTransition` as a known limitation. Interrupting typing restarts the transition rather than blocking input.

4. **Q:** How does `useOptimistic` decide what is displayed once the action ends?
   **A:** The `value` you pass in is post-action truth: on successful persistence the owner updates the base; on failure that base can remain unchanged, so React displays it again. Completion discards the temporary overlay in either case. The optional reducer recomputes the optimistic view against whatever the base is *now*, which keeps relative updates correct when the base changed mid-flight.

**Code Examples**

5. **Q:** Why must the optimistic setter run inside `startTransition`?
   **A:** Without an enclosing Action there is nothing to hold the optimistic state while the request runs — React warns (*"An optimistic state update occurred outside a Transition or Action"*) and the value renders briefly before snapping straight back.

6. **Q:** What makes a promise safe to hand to `use(promise)`?
   **A:** Stability across renders — a cached or deduped promise (React Query, SWR, a framework loader). A promise created fresh during render is uncached: React can warn and discard or retry render work, with repeated requests or unstable loading behavior.

**Common Mistakes**

7. **Q:** Why is wrapping the input's own setter in a transition a mistake?
   **A:** The input must paint every keystroke immediately — keeping it *urgent* lets React prioritize that update without promising a frame rate. The transition belongs around the expensive derived update that follows, not around the value the user is currently typing.

**Best Practices**

8. **Q:** What does ref-as-prop actually eliminate in React 19?
   **A:** The `forwardRef` wrapper — function components now read `ref` straight from props (and `forwardRef` is slated for eventual deprecation). `useImperativeHandle` stays: only the *forwarding* boilerplate goes away, not imperative handles for exposing focus/scroll APIs.

## Web Components

Source: [Web Components](10.3.4.02-web-components.md)

**Definition**

1. **Q:** Must a custom element attach a shadow root?
   **A:** No. Registration, shadow-tree encapsulation, and reusable templates are independent browser features; an element can render entirely into light DOM.

**Custom Elements**

2. **Q:** Why should attribute updates call a render method rather than invoke `connectedCallback` directly?
   **A:** Connection callbacks describe attachment to the document, including reconnection. Keeping rendering separate avoids repeating attachment-only work when an observed attribute changes.

**Shadow DOM**

3. **Q:** What styling can cross a shadow boundary even when ordinary selectors cannot?
   **A:** Inherited values, including custom properties, can reach shadow descendants. A component may also expose selected elements through `part` names for host `::part()` rules.

**HTML Templates**

4. **Q:** Does declaring a `<template>` display its contents?
   **A:** No; its fragment remains inert until code clones and inserts it into the document.

**Code Examples**

5. **Q:** What decides whether React 19 assigns `config` as an element property?
   **A:** The property must already exist on the custom-element instance when React initializes it. Otherwise React generally uses an attribute, losing the object's structure through serialization.

6. **Q:** How do you listen to a custom `booked` event in React 19 JSX?
   **A:** Pass an `onbooked` handler. The characters after `on` must match the dispatched event name, including its casing and dashes.

**Common Mistakes**

7. **Q:** Why does interpolating user text into shadow-root `innerHTML` remain unsafe?
   **A:** A shadow tree does not sanitize markup or isolate script privileges. Insert untrusted text with `textContent`, and treat intentional HTML insertion as a separate sanitization problem.

**Best Practices**

8. **Q:** When does a custom event need both `bubbles` and `composed`?
   **A:** When it originates inside a shadow tree and ancestor listeners outside that tree must receive it by propagation. Dispatching directly on the host does not need to cross its own shadow boundary.

## React Router

Source: [React Router](10.3.4.03-react-router.md)

**Definition**

1. **Q:** How does Data Mode differ from a declarative router or Framework Mode?
   **A:** Data Mode adds loaders, actions, and navigation state to a route tree. Declarative Mode supplies matching/navigation, while Framework Mode adds build and server-rendering conventions; this chapter's examples use v7 Data Mode.

**How It Works**

2. **Q:** Can a parent layout loader prevent a child loader from starting its request?
   **A:** No; matched loaders normally execute concurrently. Each protected data operation must check access itself, and the server API must authorize every request.

3. **Q:** What changed about deferred loader data between v6 and v7?
   **A:** V6 used `defer`; v7 returns an object containing an unresolved promise. Await critical data explicitly, then use `<Await>` beneath Suspense for the slower value.

4. **Q:** Why must a lazy Data Mode module export `Component` and `loader`?
   **A:** `route.lazy` supplies route-object fields from named exports. A default component with `clientLoader` belongs to different Framework Mode conventions and will not populate those fields here.

5. **Q:** What does `useFetcher` add when submitting an inline rename?
   **A:** It runs a route action and exposes its pending/data state while keeping the current location. A navigation form instead participates in a route navigation.

**Common Mistakes**

6. **Q:** Does an absolute child path escape its parent layout?
   **A:** No; it must include the parent's combined path to be valid and still belongs to that route branch. Relative child paths avoid that duplication.

7. **Q:** Is a browser-only `<Form>` sufficient to support disabled JavaScript?
   **A:** Only if the server independently handles its native submission target. Progressive enhancement in Framework Mode relies on server actions and rendered HTML; a client-only router cannot run without JavaScript.

**Performance Considerations**

8. **Q:** Why might `shouldRevalidate` improve performance but introduce stale data?
   **A:** It can skip a loader after a mutation, reducing requests. Skip only when the retained data is unaffected, and account for the error-response defaults of the installed router version.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
