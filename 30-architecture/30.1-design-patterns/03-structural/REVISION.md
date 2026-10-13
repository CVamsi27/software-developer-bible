<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Structural — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Adapter Pattern

Source: [Adapter Pattern](30.1.3.01-adapter.md)

**Q:** When does a wrapper qualify as an Adapter rather than merely a forwarding helper?

**A:** It translates an existing interface into the interface the client expects, including any required data or semantic conversion.

**Q:** Trace the old player's 1,250-millisecond playback position through the target interface.

**A:** The adapter calls `getPlaybackPosition` and divides by 1,000, returning 1.25 target seconds. The method-name translation alone would leave an incorrect unit.

**Q:** How does the profile adapter handle a blank display name, a null email, and an impossible UTC date such as February 30?

**A:** A blank display name falls back to the required handle, a null email stays `null`, and the timestamp round-trip check rejects February 30 instead of allowing JavaScript to normalize it into March. Shape validation does not verify authentication or email ownership, and production code must follow the provider's documented timestamp format.

## Facade Pattern

Source: [Facade Pattern](30.1.3.02-facade.md)

**Q:** Does a Facade prevent callers from using the underlying subsystem directly?

**A:** Not necessarily. It offers a simpler entry point; access restrictions require a separate encapsulation or permission boundary.

**Q:** Trace the computer facade's disk and memory calls. Which result feeds which input?

**A:** After freezing, it reads the boot sector and passes the returned data to memory loading, then jumps and executes. Discarding the disk result would omit that dependency. The console classes simulate this sequence.

**Q:** What changes if a facade's payment call succeeds but its order-finalization call fails?

**A:** The facade cannot undo the payment. Persist workflow state and an operation ID; a durable workflow or Saga records progress and drives forward or compensating actions, while the payment owner reconciles an uncertain result. The facade may invoke that workflow, but it is not itself a transaction; use idempotency to prevent a duplicate charge.

## Decorator Pattern

Source: [Decorator Pattern](30.1.3.03-decorator.md)

**Q:** What invariant lets multiple decorators compose around one component?

**A:** Each exposes the component's expected contract while delegating and adding behavior. A wrapper may propagate, transform or handle errors, but must keep the service's promises; ordering can change semantics and should be explicit.

**Q:** Trace a base price 10 through discount 20% then fee 2, and through the reversed wrappers.

**A:** Discount then fee returns 10 × 0.8 + 2 = 10. Fee then discount returns (10 + 2) × 0.8 = 9.6. Calls go inward, while returned results are transformed outward. This is illustrative arithmetic, not a currency rounding policy.

**Q:** What if a cache wrapper sits outside an authorization wrapper and returns a hit without delegation?

**A:** The inner authorization check is bypassed. Place authoritative permission checking on a path that covers hits and misses, and scope cached data/permissions appropriately. Matching interfaces alone does not establish safe substitution.

## Proxy Pattern

Source: [Proxy Pattern](30.1.3.04-proxy.md)

**Q:** What distinguishes a Proxy's intent from a Decorator's intent?

**A:** A Proxy controls access, identity, location or lifecycle of a subject. A Decorator adds responsibilities through composition; similar wrapper structures can serve different intentions.

**Q:** Trace proxy creation and two displays. When is the subject created?

**A:** Construction stores a filename; the first display constructs and caches the real image before delegation. The second display reuses it. Metadata can be returned without loading under the common subject contract.

**Q:** Why is a permission check inside an optional in-process proxy not a complete security boundary?

**A:** A caller may bypass that proxy and reach the server operation directly. Enforce authorization at the authoritative boundary and ensure a cache hit cannot return protected data before permission is checked.

**Q:** What happens if the synchronous subject constructor throws on first display?

**A:** Assignment does not complete, so the subject remains absent and a later display attempts construction again. Define whether that retry is permitted; async initialization instead needs a shared pending attempt and lifecycle policy.

## Module Pattern

Source: [Module Pattern](30.1.3.05-module-pattern.md)

**Q:** What does module privacy fail to provide in an application that serves many tenants?

**A:** It hides implementation bindings, but does not create per-tenant data isolation. Shared mutable module state can still mix requests unless scoped correctly.

**Q:** Trace `area(5)` through the barrel to private state. Which bindings can the consumer import?

**A:** The barrel re-exports `area` from the circle module; that function calls private `computeArea`, which uses private `PI`. The consumer gets the exported contract, not those hidden bindings. Resolution of the emitted files still follows the runtime's module rules.

**Q:** A cache hides its `Map` but returns an object stored inside it. What can the caller still change?

**A:** The caller can mutate the returned object through its shared reference even though it cannot name the map. Copy or freeze values when that is the contract; module privacy alone provides neither deep immutability nor tenant isolation.

**Q:** Why will a TypeScript `paths` alias not necessarily work in the emitted application?

**A:** `paths` guides TypeScript resolution but does not rewrite emitted import specifiers. The runtime or bundler must resolve the alias too, or use a `package.json` `imports` entry where the runtime supports it.

## Composite Pattern

Source: [Composite Pattern](30.1.3.06-composite.md)

**Q:** What advantage does Composite provide to a tree-processing client?

**A:** The client can use a shared component contract for leaves and containers. The design still must decide how to expose operations that only containers support.

**Q:** Trace root size through home/user files and the root config file.

**A:** User sums 1,024 + 500,000, home delegates that sum, and root adds 256 for 501,280. Both leaves and containers satisfy `size`; only the container recursively asks children.

**Q:** Why does the example put `add` on `Container` instead of `Component`?

**A:** A file can report its size but cannot accept children. The safe interface keeps that invalid operation off leaves; a transparent Composite can share child-management methods only if leaf behavior is clearly defined.

**Q:** What if a directory adds an ancestor, or one leaf appears under two different parents?

**A:** The supplied `add` rejects self/ancestor cycles and duplicate children within a container. It does not enforce one parent globally; shared placements can therefore be counted per edge. Enforce exclusive ownership for a strict tree or define graph traversal/counting explicitly.

## Bridge Pattern

Source: [Bridge Pattern](30.1.3.07-bridge.md)

**Q:** How does Bridge avoid a hierarchy growing for every combination of two dimensions?

**A:** It separates the abstraction hierarchy from its implementation hierarchy and connects them through composition, so each dimension can vary independently.

**Q:** Trace two circles with the same radius and different renderers.

**A:** Each circle owns its radius and delegates draw to its chosen renderer. Vector and raster implementations return different descriptions while the circle API stays stable. Neither description creates a real image.

**Q:** What if this Renderer contract gains a triangle shape operation?

**A:** Add the triangle class, change Renderer, and implement the operation in every renderer. Reducing combination classes does not remove this shared-contract cost. A primitive path interface could trade that cost for a more complex geometry contract.

## Flyweight Pattern

Source: [Flyweight Pattern](30.1.3.08-flyweight.md)

**Q:** Which state belongs outside a shared Flyweight?

**A:** Keep usage-specific state, called extrinsic state, outside the shared object—for example, a glyph’s position. State shared by every use, called intrinsic state, must be safely reusable and is usually immutable.

**Q:** Trace two oak lookups with the same appearance tuple and two different positions.

**A:** The factory returns one shared TreeType for the same name/color/texture version. Each Tree owns its coordinates and passes them to that type during drawing. Shared type identity does not merge logical placement identity.

**Q:** What if texture version changes but the cache key omits it, or the factory clears while trees remain alive?

**A:** An incomplete key can return the wrong appearance. Clearing removes factory references, while the trees still retain their types; it neither destroys the types nor disposes an external texture. Identity and resource lifetime need their own contract.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
