<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Generics & Inference — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Generics

Source: [Generics](10.2.2.01-generics.md)

**Definition**

1. **Q:** What does a type parameter actually represent, and when is it bound?
   **A:** A named unknown the *caller* decides — `<T>(x: T): T` is a contract that works for any type, and each call site resolves `T` at compile time; nothing about it exists at runtime.

2. **Q:** What do `T extends X` and `T = X` each do?
   **A:** `extends` *constrains* the parameter to types assignable to `X`, which is what lets the body use `X`'s members; `=` sets a *default* used when the caller omits the argument.

**How It Works**

3. **Q:** Why is `identity("hello")` enough — when would you ever write `identity<string>("hello")`?
   **A:** Inference binds `T` from the argument's type. Explicit arguments are the fallback where inference has nothing to work from — a parameter that appears only in the return type (`function create<T>(): T` must be called `create<User>()`) — or where you deliberately pin a wider type than inference would pick.

**Code Examples**

4. **Q:** What is the result type of `merge({ name: "Alice" }, { age: 30 })` where `merge<T, U>(a: T, b: U): T & U`?
   **A:** `{ name: string; } & { age: number; }` — the intersection carries both member sets, so `merged.name` and `merged.age` are both available.

**Common Mistakes**

5. **Q:** Why does `function add<T>(a: T, b: T): T { return a + b; }` fail, and does `T extends number | string` fix it?
   **A:** The operator is checked against the unresolved `T`, so it errors (TS2365) — and no, the constraint doesn't help: `a + b` still errors (TS2365). If the body needs one specific type, the function isn't generic.

6. **Q:** What goes wrong with `function first<T>(arr: T[]): any`?
   **A:** The call site gets `any`, so every downstream use is unchecked — the parameter bought nothing. Return `T | undefined` and the type flows through.

**Best Practices**

7. **Q:** Your team writes `map<string, number>(arr, fn)` at most call sites. What does that signal?
   **A:** Either the signature is fighting inference (fix the signature or the callback's annotation) or it's cargo-cult verbosity — inference should resolve both parameters from the arguments, and explicit type arguments are the fallback, not the default.

## Infer

Source: [Infer](10.2.2.02-infer.md)

**Definition**

1. **Q:** Where is `infer` legal, and where does it become a compile error?
   **A:** Only inside the `extends` (pattern) clause of a conditional type — `T extends Promise<infer U> ? U : never` is fine, while `T extends string ? infer S : unknown` fails with TS1338.

2. **Q:** What does `type Id<T> = T extends infer U ? U : never` actually extract?
   **A:** Nothing useful — `U` captures the whole matched type, so the result is just `T`; `infer` earns its keep only when it sits inside a constructed pattern like `Promise<infer U>`.

**How It Works**

3. **Q:** Given `type Unwrap<T> = T extends Promise<infer U> ? Unwrap<U> : T`, what is `Unwrap<Promise<Promise<string>>>`?
   **A:** `string` — each pass captures the inner `Promise` and recurses until the base case hits a non-promise.

4. **Q:** Which captures produce parameter lists, and which produce instances?
   **A:** `(...args: infer P) => any` captures the parameter tuple (`P = [string, number]`), `new (...args: any[]) => infer I` captures the constructed instance type, and `(event: infer E) => void` captures a single parameter.

**Code Examples**

5. **Q:** What does `RouteParams<"users/:id/posts/:postId">` evaluate to, and which construct does the work?
   **A:** `{ id: string; postId: string }` — the template-literal pattern captures each `:param` with `infer`, and a recursive call on the remaining segment collects the rest.

**Common Mistakes**

6. **Q:** Why is `T extends string ? T : unknown` a worse false branch than `never`?
   **A:** A non-match contributes `unknown`, and `unknown` absorbs any union it joins; `never` contributes nothing, so non-matches fall out of the result entirely.

**Best Practices**

7. **Q:** What are the three parts of a healthy recursive `infer` type?
   **A:** The capture in the `extends` pattern, a transformation of what was captured, and a base case (`never` or the pass-through type) so recursion terminates instead of hitting TS2589.

## Advanced Generics

Source: [Advanced Generics](10.2.2.03-advanced-generics.md)

**Definition**

1. **Q:** What makes a generic "advanced" beyond ordinary type parameters?
   **A:** Multi-step type-level programs — HKT encodings, variadic tuple manipulation, recursive conditional/mapped types, and deep path-based constraints — where types are computed from other types rather than merely parameterized.

**How It Works**

2. **Q:** Why can't you write `interface Functor<F> { map: <A, B>(fa: F<A>, …): F<B> }`, and what is the workaround?
   **A:** `F` is not a type constructor, so `F<A>` fails with TS2315 ("Type 'F' is not generic"). The workaround is a keyed table (`URItoKind<A>`) plus `Kind<URI, A>` so container-ness lives in a lookup, not in a generic parameter.

3. **Q:** Why does `type Bad<T> = Bad<T> | T` fail while `type List<T> = { value: T; next: List<T> } | null` compiles?
   **A:** A bare alias cycle has no position for the checker to resolve lazily (TS2456 circular reference); recursion through an object member is resolved member-by-member on demand, so it's legal.

**Code Examples**

4. **Q:** In the curried `add(1)(2)(3)` example, why must the stop condition compare against `fn.length` rather than the wrapper's `length`?
   **A:** The wrapper uses rest parameters, so `wrapper.length` is 0 and the "last argument" branch never fires — you'd return another function forever. Accumulating arguments and comparing their count to the original function's declared arity stops at exactly the right call.

5. **Q:** What goes wrong if `PipeResult` lacks its `Rest extends []` base case?
   **A:** Recursion bottoms out at `PipeResult<[]> = never`, `never extends (arg) => infer C` still passes, and `C` infers as `unknown` — the pipeline types as `(arg: number) => unknown` instead of `(arg: number) => string`.

**Common Mistakes**

6. **Q:** Your constraint reads `T extends object & { id: string } & { name: string } & { email: string }`. What's the better form, and why?
   **A:** Extract it to a named `interface User` and write `T extends User` — identical checking, but readable error messages, a single edit point, and something callers can `implements`.

**Best Practices**

7. **Q:** When does `T extends HasId` genuinely beat `T extends { id: string }`?
   **A:** When the constraint is a reusable contract: a named interface can be implemented, extended, and documented once, and errors print `HasId` instead of expanding the full inline shape every time.

## Type Variance

Source: [Type Variance](10.2.2.04-type-variance.md)

**Definition**

1. **Q:** Why may a function accepting any Animal replace a Dog callback?
   **A:** Every Dog that the caller can supply is also an Animal. The broader input promise therefore covers the narrower callback slot.

**How It Works**

2. **Q:** Which syntax keeps callback parameters bivariant even with strict function checking?
   **A:** Method declarations keep the compatibility exception. Function-valued properties receive contravariant parameter checking instead.

3. **Q:** Why does the pushed object appear at index one in the array example?
   **A:** The original Rex object occupies index zero and retains its breed. The write through the Animal alias appends a different object lacking that field.

4. **Q:** Does a plain `{ value: T }` field make a TypeScript container invariant?
   **A:** The checker still permits covariant assignment of that shape. A function-property setter plus an output, or a deliberate variance annotation, is needed to express the stricter generic contract.

**Code Examples**

5. **Q:** Which event type is more specific: PointerEvent or MouseEvent?
   **A:** PointerEvent extends MouseEvent with extra information. A general MouseEvent handler can replace a PointerEvent handler, while the opposite substitution may receive missing fields.

6. **Q:** Why must an emitter's callback constraint avoid requiring unknown input for every handler?
   **A:** A specialized handler cannot process arbitrary unknown values. The constraint should recognize a callback shape while preserving each event's actual parameter type for registration.

**Common Mistakes**

7. **Q:** What protection does a readonly array view leave unprovided?
   **A:** It blocks array writes through that view, but other aliases can still mutate the original. Its elements are not automatically frozen either.

**Performance Considerations**

8. **Q:** When can explicit variance annotations improve compilation work?
   **A:** They can help comparisons of the same generic type when recursive variance inference is expensive or ambiguous. Profiling is needed to establish a benefit for the actual project.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
