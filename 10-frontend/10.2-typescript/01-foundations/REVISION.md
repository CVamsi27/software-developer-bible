<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Foundations — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Types vs Interfaces

Source: [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md)

**Definition**

1. **Q:** What can `type` declare that `interface` cannot, and vice versa?
   **A:** `type` covers unions, intersections, tuples, mapped/conditional types and primitive aliases; `interface` adds declaration merging and the `extends` form libraries use for augmentation. Everything both can express is interchangeable.

2. **Q:** Why do two declarations with the same name collide for `type` but merge for `interface`?
   **A:** A type alias is a one-shot binding to a single type — a second one is a duplicate identifier. An interface is an open contract: each declaration contributes members to the same growing shape.

**How It Works**

3. **Q:** Does `interface Dog extends Animal` do something `type Dog = Animal & { … }` cannot?
   **A:** No for a single object shape — the intersection produces the same members. The differences are elsewhere: `extends` cannot express a union, and only the interface form is mergeable.

4. **Q:** What does structural typing imply about a `type Point` and an identically-shaped `interface PointInterface`?
   **A:** They are interchangeable: a value typed one is assignable to the other, because assignability compares members, never declared names.

**Code Examples**

5. **Q:** Why does `const p: Point = { x: 1, y: 2, z: 3 }` fail while assigning an object literal *variable* with an extra `z` succeeds?
   **A:** Object literals get an excess-property check against the target type; a variable already typed elsewhere is only checked structurally, and extra members never break assignability.

**Common Mistakes**

6. **Q:** What error do you get from `interface Status = "active" | "inactive"`, and what is the fix?
   **A:** It is a syntax error — `interface` only declares a body of members. Write `type Status = "active" | "inactive"` instead.

**Summary**

7. **Q:** When a shape must be extended later by consumers of your library, which keyword should you reach for and why?
   **A:** `interface` — declaration merging lets downstream code add members to the same contract without editing (or forking) your source.

## Keyof & Typeof

Source: [Keyof & Typeof](10.2.1.02-keyof-typeof.md)

**Definition**

1. **Q:** What does `keyof User` produce when `User` has `name` and `age`?
   **A:** The union of literal keys `"name" | "age"`, which you can then index (`User[K]`) or assign against — a typo becomes a compile error.

2. **Q:** What is the difference between `typeof config` and `keyof typeof config`?
   **A:** `typeof config` is the object's *value type* (its members), while `keyof typeof config` is the *union of its keys*.

**How It Works**

3. **Q:** Why does `type Status = typeof STATUS[keyof typeof STATUS]` need `as const` on `STATUS`?
   **A:** Without `as const` each member widens to `string`, so the union collapses to `string`; with it, members stay literals and the union is `"active" | "inactive"`.

4. **Q:** In `function get<T, K extends keyof T>(obj: T, key: K): T[K]`, what does the `keyof T` constraint buy you?
   **A:** It guarantees `key` names a real property (typos fail to compile) and gives the return type the precise `T[K]` instead of `any`.

**Code Examples**

5. **Q:** How does key remapping with `as` filter a type down to matching keys?
   **A:** `[K in keyof T as null extends T[K] ? K : never]` keeps only the keys whose value satisfies the test and maps the rest to `never`, dropping them from the result.

**Common Mistakes**

6. **Q:** What is wrong with deriving a type by hand from a runtime constant instead of using `typeof`?
   **A:** The hand-written copy is a second source of truth — edit the constant and the type silently rots; `typeof` re-derives it on every compile.

**Best Practices**

7. **Q:** What do you lose if you write `keyof typeof routes` on a route map that was *not* marked `as const`?
   **A:** Nothing for the keys — but the values widen to `string`, so `routes[route]` no longer pins you to the exact path literals; add `as const` when the values matter too.

## Type Narrowing

Source: [Type Narrowing](10.2.1.03-type-narrowing.md)

**Definition**

1. **Q:** What does it mean to "narrow" a value, and where does the refinement live?
   **A:** You replace a union with the member(s) still possible on the current control-flow path; the refinement exists only in the checker's model of that branch — the runtime value never changes.

2. **Q:** Which everyday operators double as type guards?
   **A:** `typeof` (primitives), `instanceof` (classes), `in` (property presence), and equality against a literal discriminant (`x.status === "ok"`), plus user-defined predicates (`x is T`).

**How It Works**

3. **Q:** Why does `if (typeof user === "object")` still allow `null`?
   **A:** `typeof null` is `"object"`, so the null branch survives the guard — check `user !== null` (or `!= null`) explicitly instead.

4. **Q:** What must a function return for `if (isCat(x))` to narrow `x`?
   **A:** A type predicate — `x is Cat` in the signature — not a plain `boolean`; the boolean version only says yes/no, it claims nothing about the type.

**Code Examples**

5. **Q:** In `default: assertNever(shape)`, what breaks when a new union member is added?
   **A:** The `shape` in that branch is no longer `never`, so the call fails to type-check and the error lands directly on the switch that is missing a case.

**Common Mistakes**

6. **Q:** Why is a `void` handler with an uncovered union member dangerous compared to a value-returning one?
   **A:** The value-returning function fails with `TS2366 Function lacks ending return statement`, but the `void` handler compiles cleanly and silently drops the event.

7. **Q:** After `x = x.trim()` inside a branch that had already narrowed `x`, is the narrowed type kept?
   **A:** Yes. `trim()` returns a string, so this assignment leaves the current flow type as `string`. An assignment updates the flow type according to the assigned value; assigning a value that may be `null` can broaden it again. The declared type still limits which assignments are allowed.

## tsconfig & Compiler Options

Source: [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md)

**Definition**

1. **Q:** What four option families does a tsconfig organize into, and which family decides which bugs reach production?
   **A:** Strictness, modules/resolution, emit/build, and interop/lint-adjacent flags. Strictness is the one that decides bug classes: `strictNullChecks` and `noImplicitAny` catch null dereferences and silent `any` at compile time instead of at runtime.

**How It Works**

2. **Q:** App or published npm package — which `moduleResolution` does each need, and what breaks when they're swapped?
   **A:** Bundled apps use `bundler` (extensionless imports fine); packages consumed by Node use `nodenext` (relative ESM imports need `.js`, honors `exports` maps). Swapped, you get phantom "cannot find module" errors that appear only in some tools.

3. **Q:** What does `isolatedModules: true` actually reject, and what does it merely warn you about by behavior?
   **A:** It rejects type/value ambiguity a single-file transpiler can't resolve — chiefly type-only *re*-exports (`export { Foo }` → TS1205) and ambient const enum access (TS2748). Ordinary const enums still compile; they just never get inlined across files.

4. **Q:** How does `verbatimModuleSyntax` go further than `isolatedModules`?
   **A:** It requires `import type`/`export type` for every type-only import (not just re-exports) and prevents the emitter from rewriting module syntax, so the file you wrote is the file that ships.

**Code Examples**

5. **Q:** What happens if you set `composite: true, declaration: false`, and why?
   **A:** It fails to build (TS6304) — `composite` implies `declaration`, so the two flags contradict each other; declare intent with `declarationMap` instead.

**Common Mistakes**

6. **Q:** What class of bugs does `skipLibCheck` actually skip, and what does it never skip?
   **A:** It skips type checking inside `.d.ts` declaration files, including both dependency declarations and your own. Your ordinary source files are still checked against those declarations. An incorrect declaration can therefore escape checking and give source code a misleading description of the runtime behavior.

**Best Practices**

7. **Q:** Two engineers get different `tsc` results from the same commit — which tsconfig principle does that violate?
   **A:** The config is a project fingerprint: CI must type-check with the committed tsconfig, and local editor settings must not drift from it, or the same code means different things per machine.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
