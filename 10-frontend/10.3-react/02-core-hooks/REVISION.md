<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Core Hooks — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## useState

Source: [useState](10.3.2.01-usestate.md)

**Definition**

1. **Q:** What stays stable when a component receives its next state value?
   **A:** The setter function keeps its identity while the component receives a new state snapshot. Calling that setter does not mutate variables captured by an existing handler.

**How It Works**

2. **Q:** How does React associate two useState calls with the correct stored values?
   **A:** It follows the component Hook call order to select the corresponding records. Conditional calls can shift that order and associate later calls with the wrong records.

3. **Q:** Why do three replacement updates from one snapshot increment only once?
   **A:** Each queues the same replacement value calculated from that snapshot. Three updater functions instead compose against pending state and increment three times.

**Code Examples**

4. **Q:** Why must lazy initializers and functional updaters remain pure?
   **A:** React may invoke them more than once while checking or replaying work. Generate event-specific values outside the updater and let it calculate state without side effects.

**Real-World Use Cases**

5. **Q:** What must an update preserve when changing a nested form field?
   **A:** It must copy each changed level while retaining unaffected fields. A Hook setter replaces the supplied object instead of merging it like class setState.

**Common Mistakes**

6. **Q:** Why is doubleCount better derived than synchronized through another setter?
   **A:** Its value is completely determined by count. Storing a second copy creates another update and permits the copies to disagree.

**Performance Considerations**

7. **Q:** What behavior can a lazy initializer save on later renders?
   **A:** It avoids rerunning the initial calculation merely because the component updates. A remount initializes again, and prop changes alone do not reinitialize state.

## useEffect

Source: [useEffect](10.3.2.02-useeffect.md)

**Definition**

1. **Q:** Which kind of ongoing work belongs in an effect?
   **A:** Synchronizing with an external system as committed reactive inputs change belongs there. Pure derived values belong in render, and action-specific work belongs in the event path.

**How It Works**

2. **Q:** How does React decide whether an effect dependency changed?
   **A:** It compares each listed value with its preceding committed value using Object.is. A newly allocated object or function usually differs even when its contents appear equivalent.

3. **Q:** Which captured values does a cleanup function use?
   **A:** It closes over the setup render that created it, so it can undo that setup with the old inputs. Cleanup runs before a replacement setup and at unmount.

**Code Examples**

4. **Q:** Why must a stale fetch guard cover finally as well as success?
   **A:** An obsolete request can finish its cleanup path while a newer request is pending. Its loading update would otherwise incorrectly mark that newer request complete.

**Real-World Use Cases**

5. **Q:** Does debouncing search eliminate races between network responses?
   **A:** It delays when requests begin but does not dictate completion order. Ignore or cancel superseded requests so an older response cannot replace newer results.

**Common Mistakes**

6. **Q:** Why is an async effect setup function an invalid cleanup contract?
   **A:** An async function returns a Promise, whereas React expects no return or a teardown function. Invoke async work inside a synchronous setup and handle its result and cleanup separately.

**Performance Considerations**

7. **Q:** Does useEffect guarantee that its code never delays paint?
   **A:** No; passive effects may flush before paint, and their callbacks execute synchronously when called. Keep them small and use layout effects only for work that must precede paint.

## useMemo & useCallback

Source: [useMemo & useCallback](10.3.2.03-usememo-usecallback.md)

**Definition**

1. **Q:** Which result does each memoization Hook preserve between ordinary updates?
   **A:** useMemo retains the result of a calculation, while useCallback retains a function reference. Neither should determine whether application logic remains correct.

**How It Works**

2. **Q:** Does useCallback avoid creating the arrow passed to it?
   **A:** JavaScript still evaluates that argument. When dependencies match, React returns the previously stored function so the consumer observes a stable reference.

3. **Q:** Why does a memoized calculation still need all of its reactive inputs?
   **A:** The dependency list determines which cached result can be reused. Leaving out an input can return a result computed from obsolete props or state.

**Code Examples**

4. **Q:** Why should a cached sorting operation copy its input array first?
   **A:** Array sort mutates the array it receives. Copying prevents a render-time calculation from altering props or shared data.

**Real-World Use Cases**

5. **Q:** Can a stable callback alone stop a table row from rendering?
   **A:** It helps only if a consumer uses identity to skip work, such as a memoized row with otherwise matching props. An ordinary child still executes with its parent.

**Common Mistakes**

6. **Q:** What is wrong with mutating a memoized output after render?
   **A:** The mutation changes a cached object outside the calculation without scheduling an update. Update the source state immutably and derive a new output instead.

**Performance Considerations**

7. **Q:** How do you decide whether caching is worth its bookkeeping?
   **A:** Measure the cost and frequency of the work it actually skips. Dependency checks, retained data and complexity should earn a useful improvement.

## useRef

Source: [useRef](10.3.2.04-useref.md)

**Definition**

1. **Q:** Why does modifying a ref not refresh displayed content?
   **A:** A ref is a persistent mutable box without an update queue that schedules rendering. Put values that drive the displayed UI in state.

**How It Works**

2. **Q:** When does a DOM ref become usable and when is it cleared?
   **A:** React assigns the node during commit after mounting it, and clears the ref when that node is detached. Initial render cannot rely on a DOM node already being present.

3. **Q:** How does ref forwarding differ between React 18 and React 19?
   **A:** React 18 function components use forwardRef to receive the special ref. React 19 can receive it as a prop and explicitly pass it to a node or imperative handle.

**Code Examples**

4. **Q:** Why must a timer Start handler check whether a timer is already running?
   **A:** Starting twice can overwrite the stored ID while leaving the first interval active. A guard ensures the ref continues to identify the one resource cleanup must cancel.

**Real-World Use Cases**

5. **Q:** Why should a video control label follow media events?
   **A:** Playback can fail or change outside the button handler. Updating state from play, pause and ended events keeps the label aligned with the media element.

**Common Mistakes**

6. **Q:** Why can reading a previous-value ref during render violate purity?
   **A:** A ref is mutable shared storage rather than the render snapshot React is evaluating. Read committed history inside effects or handlers, and use state for rendered history.

**Performance Considerations**

7. **Q:** What does avoiding a ref-triggered render fail to guarantee?
   **A:** It does not remove browser layout costs or ensure an imperative update is faster. The retained ref data also has a memory cost and needs appropriate cleanup.

## Context API

Source: [Context API](10.3.2.05-context-api.md)

**Definition**

1. **Q:** What responsibility does context add to a local state owner?
   **A:** It transports the owner’s value to distant descendants. Updates and state transitions still belong to the owner’s state Hook, reducer or external store.

**How It Works**

2. **Q:** When is the value passed to createContext used?
   **A:** It is the static fallback when no matching provider exists above a reader. An explicit undefined provider value overrides it rather than restoring the fallback.

3. **Q:** Which provider wins when the same context is provided twice?
   **A:** The nearest matching provider above the consumer supplies its value. Its consumers are shielded from changes to a more distant provider of that context.

**Code Examples**

4. **Q:** Why must a required-provider Hook use a sentinel default?
   **A:** A sentinel such as null lets it distinguish absence from a valid value. A non-null fallback would be returned outside the provider and make an undefined check ineffective.

**Real-World Use Cases**

5. **Q:** Why should locale-loading effects ignore obsolete imports?
   **A:** An earlier language load can resolve after a later selection. Suppressing the old result prevents translations for that earlier locale from replacing the current ones.

**Common Mistakes**

6. **Q:** What can memoizing a provider object actually prevent?
   **A:** It avoids context propagation caused solely by allocating an equivalent new object. It does not stop parent-driven renders or updates from actual changes to the context fields.

**Performance Considerations**

7. **Q:** Why cannot React.memo block an update to context a component reads?
   **A:** Consumed context is a direct dependency independent of the prop comparison. Splitting contexts can reduce which readers are notified when one value changes.

## Changed contracts

Source: [useMemo/useCallback](10.3.2.03-usememo-usecallback.md), [useRef](10.3.2.04-useref.md), [Context](10.3.2.05-context-api.md)

**Q:** What happens to cached sorting when the parent allocates an equivalent new array?

**A:** Its dependency reference differs, so the calculation reruns. In-place mutation is worse: it can preserve identity while silently invalidating the cached contents.

**Q:** A condition replaces an observed node. Why might an effect depending on the ref object keep watching the old node?

**A:** The ref object remains stable; assigning `.current` does not schedule the effect. A callback ref can own the observer for each attached node.

**Q:** How does a React 19 callback ref release a ResizeObserver?

**A:** It returns cleanup from attachment. Detachment invokes that cleanup; stable callback identity avoids unnecessary detach/attach cycles.

**Q:** Can a component read a context provider it returns around its own children?

**A:** No. The reading call resolves providers above that component; its returned provider is below it. Move the reader under the owner.

**Q:** Why must the newest failed login settle loading after invalidating an initial session lookup?

**A:** The old lookup is correctly prohibited from publishing. Without a failure settlement in the current action, no remaining owner can clear the initial loading state.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
