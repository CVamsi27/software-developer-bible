<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Modern React — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Modern React: Scheduling, Actions, and DOM APIs

Source: [Modern React: Scheduling, Actions, and DOM APIs](10.3.4.01-modern-hooks-react18-19.md)

**First Principles**

1. **Q:** What single theme connects React 18's hooks and React 19's APIs?
   **A:** They give React explicit scheduling and resource lifetimes. Transitions and deferred values distinguish urgent feedback from eligible background rendering; Actions coordinate async mutations, while optimistic state supplies a temporary proposal over a confirmed base. Error presentation, stable resource ownership and persistence remain application responsibilities.

2. **Q:** When do you reach for `useTransition` versus `useDeferredValue`?
   **A:** Transition when you own the setter — you wrap the slow `setState` yourself and `isPending` reports on it. Deferred value when the slow input arrives as a prop or from elsewhere — you can't wrap its producer, so `useDeferredValue` hands back a lagging copy for the expensive render.

**How It Works**

3. **Q:** What does `startTransition` actually mark as non-urgent, and what is the async caveat?
   **A:** Only updates scheduled *synchronously* inside the callback are marked as Transitions; work awaited inside is included, but a `set()` called after an `await` currently is not — React documents wrapping that call in a second `startTransition` as a known limitation. Interrupting typing restarts the transition rather than blocking input.

4. **Q:** How does `useOptimistic` decide what is displayed once the Action ends?
   **A:** The value passed as its base remains the confirmed state. When the Action ends, React drops the temporary overlay; the owner should update the base after a successful write, while a failure leaves the previous base visible. The optional reducer recomputes the optimistic view against the latest base when that value changes during the Action.

**Code Examples**

5. **Q:** What keeps an optimistic value visible for the lifetime of an asynchronous write?
   **A:** The optimistic setter must run inside an Action, such as a form Action or Transition. Outside an Action, the temporary value has no pending lifetime and React warns before reverting it.

6. **Q:** What makes a promise safe to hand to `use(promise)`?
   **A:** Stability across renders — a cached or deduped promise (React Query, SWR, a framework loader). A promise created fresh during render is uncached: React can warn and discard or retry render work, with repeated requests or unstable loading behavior.

**Common Mistakes**

7. **Q:** Why is wrapping the input's own setter in a transition a mistake?
   **A:** The input must paint every keystroke immediately — keeping it *urgent* lets React prioritize that update without promising a frame rate. The transition belongs around the expensive derived update that follows, not around the value the user is currently typing.

**Best Practices**

8. **Q:** What does ref-as-prop actually eliminate in React 19?
   **A:** The `forwardRef` wrapper — function components now read `ref` straight from props (and `forwardRef` is slated for eventual deprecation). `useImperativeHandle` stays: only the *forwarding* boilerplate goes away, not imperative handles for exposing focus/scroll APIs.

9. **Q:** Which `use` reads are supported in a Server Component, and what does that mean for a promise passed to a Client Component?
   **A:** `use(promise)` is supported in a Server Component, but `use(context)` is not. A Server Component can pass a promise to a Client Component for `use` to read; its resolved value must be serializable.

10. **Q:** What is the React 19.3 purpose of a Fragment ref?
   **A:** It exposes a limited FragmentInstance over a group of DOM children, allowing focus, observation or scrolling without inserting a wrapper that could alter layout or semantics.

11. **Q:** When should a component call use(browser())?
   **A:** Only when it cannot produce meaningful server output. It suspends that component during server rendering and continues in the browser; ordinary renderable data should still be loaded by the framework or server path.

12. **Q:** What does Activity mode="hidden" preserve, and what happens to Effects?
   **A:** It preserves the subtree’s component state while hiding it, disconnecting its Effects and deferring updates until it becomes visible again. Use it when that retention behavior is useful, not as a generic loading state.

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

6. **Q:** How do you listen for the booking-confirmed custom event in React 19 JSX?
   **A:** Use the on-prefixed prop with the event name’s exact case and dashes: onbooking-confirmed. Type the custom element’s intrinsic JSX props separately.

7. **Q:** Why does interpolating user text into shadow-root `innerHTML` remain unsafe?
   **A:** A shadow tree does not sanitize markup or isolate script privileges. Insert untrusted text with `textContent`, and treat intentional HTML insertion as a separate sanitization problem.

**Best Practices**

8. **Q:** When does a custom event need both `bubbles` and `composed`?
   **A:** When it originates inside a shadow tree and ancestor listeners outside that tree must receive it by propagation. Dispatching directly on the host does not need to cross its own shadow boundary.

## React Router

Source: [React Router](10.3.4.03-react-router.md)

**Definition**

1. **Q:** How does Data Mode differ from a declarative router or Framework Mode?
   **A:** Data Mode adds loaders, actions and navigation state to a route tree. Declarative Mode supplies matching/navigation; Framework Mode adds route modules, build conventions, code splitting and rendering strategies. This chapter's examples use v8 Data Mode.

**How It Works**

2. **Q:** Can a parent loader prevent a child loader from starting, and what does Data Mode middleware change?
   **A:** Matched loaders run concurrently, so a parent loader cannot gate a child loader. Data Mode middleware runs sequentially before route handlers and can coordinate a client redirect, but every protected API operation still authorizes on the server.

3. **Q:** What changed about deferred loader data between v6 and v7/v8?
   **A:** V6 used `defer`; v7 and v8 return an object containing an unresolved promise. Await critical data explicitly, then render the slower value with `<Await>` beneath Suspense.

4. **Q:** What can route.lazy supply, and which route fields must be known before matching?
   **A:** A lazy module can supply implementation fields such as Component, loader, action or ErrorBoundary. The router needs matching fields such as path and index before navigation; a route without a loader does not need to export one.

5. **Q:** What does `useFetcher` add when submitting an inline rename?
   **A:** It runs a route action and exposes its pending/data state while keeping the current location. A navigation form instead participates in a route navigation.

**Common Mistakes**

6. **Q:** Does an absolute child path escape its parent layout?
   **A:** No; it must include the parent's combined path to be valid and still belongs to that route branch. Relative child paths avoid that duplication.

7. **Q:** Is a browser-only `<Form>` sufficient to support disabled JavaScript?
   **A:** Only if the server independently handles its native submission target. Progressive enhancement in Framework Mode relies on server actions and rendered HTML; a client-only router cannot run without JavaScript.

**Performance Considerations**

8. **Q:** What is the v8 Data Mode default after a failed mutation, and what can `shouldRevalidate` change?
   **A:** A 4xx/5xx action response skips default loader revalidation; a successful-status `{ error }` result still triggers it. `shouldRevalidate` can override the default, so preserve `defaultShouldRevalidate` unless the route data is known to be unaffected.

9. **Q:** What should a v7 application check before moving to v8?
   **A:** Meet the Node 22.22+ and React/React DOM 19.2.7+ minimums; Framework Mode also requires Vite 7+. Replace `react-router-dom` imports: DOM provider APIs come from `react-router/dom` and other APIs from `react-router`. Review the official migration guide for flags and adapter-specific changes.

10. **Q:** Is a v8 Data Mode middleware session check a security boundary?
   **A:** No. It runs in the browser and can coordinate navigation and avoid unnecessary client loaders, but users can call an API directly. The API must authenticate and authorize each read and write.

11. **Q:** When should an inline rename use a fetcher instead of a navigation Form?
   **A:** Use a fetcher when the action should expose pending/result state without changing the current location. Use a navigation Form when the submission represents a route transition or should update browser history.

## API and lifetime boundaries

Source: [Modern Hooks](10.3.4.01-modern-hooks-react18-19.md), [Web Components](10.3.4.02-web-components.md), [React Router](10.3.4.03-react-router.md)

**Q:** When should a theme change reconnect a room?

**A:** Only if theme is a connection input. If it affects notification presentation alone, an Effect Event can read the latest theme from the effect's callback without replacing the room connection.

**Q:** Can an Effect Event be passed down as a normal button callback?

**A:** No. Keep it inside its effect/subscription lifecycle; it is not a general replacement for event handlers or required dependencies.

**Q:** Why is useId unsuitable for a database record's list key?

**A:** It identifies an accessibility relationship for a component instance. A list must use the stable domain identity of the record across reorder and mount changes.

**Q:** What can replacing all shadow markup lose even when the displayed text is correct?

**A:** It replaces inner node identity, potentially losing focus and control state. A stable-node update or renderer is required when that state must survive.

**Q:** Does aborting an obsolete navigation undo a mutation at the server?

**A:** No. The client may stop waiting while the server already accepted work. Use server-side version/idempotency rules for conflicting or retried writes.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
