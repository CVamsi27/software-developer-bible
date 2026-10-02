<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)

# Objects, Prototypes & `this` — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## This

Source: [This](10.1.2.01-this.md)

**Definition**

1. **Q:** If `this` is "dynamic", what is it actually bound to — the function's source text or the call?
   **A:** For an ordinary function, the invocation supplies the receiver; one function can receive different receivers. An arrow has no own receiver binding and resolves the enclosing `this`, so its source context matters.

**How It Works**

2. **Q:** A method that was copied off its object is called plainly as `greet()` — what does `this` become, and how do the two modes differ?
   **A:** The default binding applies: the global object in sloppy code, `undefined` in strict code, where the first property read throws.

3. **Q:** When more than one binding rule could apply, which one wins?
   **A:** Inspect the actual invocation and function kind. A bound function preserves its receiver under ordinary calls, but construction of a constructible bound target ignores that saved receiver. Arrows resolve enclosing `this` and are not constructors; a universal precedence slogan hides these boundaries.

4. **Q:** What do `call`, `apply`, and `bind` share, and what sets them apart?
   **A:** For ordinary calls, `call` supplies a receiver and separate arguments, `apply` uses array-like arguments, and `bind` returns a function storing a receiver and optional leading arguments. They cannot replace an arrow's lexical `this`.

**Code Examples**

5. **Q:** Why does `const fn = obj.greet; fn()` behave differently from `obj.greet()`?
   **A:** Copying the function does not copy the receiver — with no `.` in front of the call, `this` falls back to the default binding.

6. **Q:** What breaks when an object literal declares `greet: () => console.log(this.name)`?
   **A:** The arrow froze the literal's surrounding `this` at creation time, so invoking `obj.greet()` still reads from the outer scope instead of `obj`.

**Common Mistakes**

7. **Q:** Inside `setInterval(function () { this.seconds++; })` on a `Timer`, which object does `this` refer to?
   **A:** The host supplies the receiver, not the owning Timer: browser timers supply the window/global receiver even for a strict callback, while Node has its own timer receiver behavior. A closure or bound callback can explicitly retain the Timer instance.

8. **Q:** Why does a plain `function inner()` nested inside a method ignore that method's `this`, and what is the fix?
   **A:** Nesting grants no inheritance: a directly-invoked function takes the default binding of its own call. Declare `inner` as an arrow, or pass the receiver explicitly.

## Prototypes

Source: [Prototypes](10.1.2.02-prototypes.md)

**Definition**

1. **Q:** What is a prototype, in the terms the engine actually uses?
   **A:** For an ordinary object, its internal `[[Prototype]]` link is another object or null. Missing own properties can delegate along those links; Object.prototype and null-prototype dictionaries terminate at null.

**How It Works**

2. **Q:** What happens when a key is missing everywhere along the chain?
   **A:** The walk ends at the `null` link, so the read yields `undefined` instead of throwing — the reason a missing method fails at the call site rather than at the lookup.

3. **Q:** What do `obj.__proto__` and `fn.prototype` each describe?
   **A:** `__proto__` is usually an inherited legacy accessor, which can be absent or shadowed. A constructible function's `.prototype` is an ordinary property used for default new instances; arrows are not constructors. Use Object.getPrototypeOf to inspect an object's actual link.

**Code Examples**

4. **Q:** Why does `Person.prototype = { greet() {} }` lose the constructor even though `alice.greet()` still runs?
   **A:** The assignment changes the prototype used for future default instances and omits the old own constructor property. Existing instances keep their old links; they do not automatically re-point. The constructor property itself is ordinary data, not an object-creation authority.

5. **Q:** What does `Object.create(null)` buy you?
   **A:** A chainless object — no inherited `toString`, `hasOwnProperty`, or `constructor` — so its keys are exactly the ones you put there.

**Common Mistakes**

6. **Q:** Why is adding a method to `Array.prototype` a hazard rather than a convenience?
   **A:** Every array in the page shares that object, so your method can collide with another library's and with a future native implementation of the same name.

7. **Q:** What breaks if a derived constructor writes to `this` before calling `super()`?
   **A:** The derived constructor's `this` binding is uninitialized before super() establishes it, so accessing it throws ReferenceError. Constructors that deliberately return an object have further rules; the ordinary field-initialization path must call super first.

**Best Practices**

8. **Q:** Two quick checks settle most "which object is on the chain?" questions — what are they?
   **A:** Object.getPrototypeOf reports the immediate link. Default instanceof checks for the constructor's prototype in the chain, but custom Symbol.hasInstance, altered chains and cross-realm values can change the interpretation.

## Proxy & Reflect

Source: [Proxy & Reflect](10.1.2.03-proxy-reflect.md)

**Definition**

1. **Q:** What does a Proxy sit between, and what does it leave untouched?
   **A:** A caller using the proxy can trigger its handler traps. A caller retaining the raw target bypasses them. Traps may forward or mutate the target, so wrapping does not promise unchanged target state or complete access control.

**How It Works**

2. **Q:** Why does `Reflect` exist alongside Proxy instead of traps calling `target[prop]` directly?
   **A:** It packages each default operation as a callable function with the right receiver and return value, so a trap forwards part of the work without re-deriving engine behavior — hand-rolled forwarding is where subtle bugs enter.

3. **Q:** What stops a `set` trap from writing a value a frozen target forbids?
   **A:** Engine invariants: the operation is re-checked against the target's own property attributes, and a trap that claims a result the target cannot back throws a TypeError.

**Code Examples**

4. **Q:** Why must a `set` trap end by returning something truthy?
   **A:** The result indicates whether the set operation succeeded. A falsy result makes strict assignment throw TypeError; a successful assignment expression still evaluates to its right-hand-side value, not the trap's boolean result.

5. **Q:** What happens to a proxy after `revoke()` runs?
   **A:** Further trapped object operations such as get/has throw TypeError, while the raw target remains usable. Values previously returned from the proxy are not recursively revoked.

**Common Mistakes**

6. **Q:** Why is `new Proxy(42, {})` rejected, and when is the `apply` trap consulted?
   **A:** The target must be an object or a function, never a primitive; `apply` is only checked when the target itself is callable, so it is dead code around a plain object of methods.

**Performance Considerations**

7. **Q:** Where should a proxy sit relative to a hot loop?
   **A:** Measure the workload before optimizing: overhead depends on engine, handler and operation, not a fixed multiplier. Raw-target access bypasses interception and must not skip required validation or tracking.

**Best Practices**

8. **Q:** What do you gain by writing `Reflect.set(target, prop, value, receiver)` inside the trap instead of `target[prop] = value`?
   **A:** The correct receiver reaches setters defined higher up the chain, and the call returns the boolean the trap is required to produce.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
