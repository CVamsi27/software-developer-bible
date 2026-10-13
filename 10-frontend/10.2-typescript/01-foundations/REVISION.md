<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Foundations — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Types vs Interfaces

Source: [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md)

**Definition**

1. **Q:** What can `type` declare that `interface` cannot, and vice versa?
   **A:** `type` covers unions, intersections, tuples, mapped/conditional types and primitive aliases; `interface` adds declaration merging and the `extends` form libraries use for augmentation. Their common object shapes are often mutually assignable; merging and conflict handling still differ.

2. **Q:** Why do two declarations with the same name collide for `type` but merge for `interface`?
   **A:** A type alias is a one-shot binding to a single type — a second one is a duplicate identifier. An interface is an open contract: each declaration contributes members to the same growing shape.

**How It Works**

3. **Q:** Does `interface Dog extends Animal` do something `type Dog = Animal & { … }` cannot?
   **A:** Compatible members can describe the same shape, but conflicting extension members report an error at the interface; an intersection instead requires both and may produce an impossible never property. An interface also supports merging.

4. **Q:** What does structural typing imply about a `type Point` and an identically-shaped `interface PointInterface`?
   **A:** They are interchangeable: a value typed one is assignable to the other, because these plain object contracts compare their members. Private/protected class members and brands impose additional compatibility conditions.

**Code Examples**

5. **Q:** Why does `const p: Point = { x: 1, y: 2, z: 3 }` fail while assigning an object literal *variable* with an extra `z` succeeds?
   **A:** Object literals get an excess-property check against the target type; a variable already typed elsewhere is only checked structurally, and a compatible existing value can have extra members. This is not an exact runtime schema, and other contexts/index signatures/weak targets have their own checks.

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

4. **Q:** In `function get<T, K extends keyof T>(obj: T, key: K): T[K]`, what does the `keyof T` constraint buy you, and what can it not prove for a dictionary?
   **A:** It restricts the key to the static contract and preserves the declared property type; it does not prove runtime ownership or presence. For `Record<string, V>`, arbitrary keys are allowed even when absent, so a generic `T[K]` return can overstate a lookup. Model dictionary results as `V | undefined` and check the intended presence boundary.

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

4. **Q:** What must a function return for `if (isCat(x))` to narrow `x`, and when can the compiler infer that result?
   **A:** An explicit `x is Cat` return type is trusted by the checker, so its implementation must validate the claim. Since TypeScript 5.5, some unannotated Boolean functions infer predicates when they have one return path, do not mutate the parameter, and return an expression that refines it on both true and false outcomes. Annotating the return as `boolean` prevents that predicate inference.

**Code Examples**

5. **Q:** In `default: assertNever(shape)`, what breaks when a new union member is added?
   **A:** The `shape` in that branch is no longer `never`, so the call fails to type-check and the error lands directly on the switch that is missing a case.

**Common Mistakes**

6. **Q:** Why is a `void` handler with an uncovered union member dangerous compared to a value-returning one?
   **A:** A value-returning function with a non-undefined return type and strict null checking can fail for the missing return, but the `void` handler compiles cleanly and silently drops the event.

7. **Q:** After `x = x.trim()` inside a branch that had already narrowed `x`, is the narrowed type kept?
   **A:** Yes. `trim()` returns a string, so this assignment leaves the current flow type as `string`. An assignment updates the flow type according to the assigned value; assigning a value that may be `null` can broaden it again. The declared type still limits which assignments are allowed.

## tsconfig & Compiler Options

Source: [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md)

**Definition**

1. **Q:** What does a `tsconfig` guarantee, and where does that guarantee stop?
   **A:** It selects source files and sets the compiler’s checking, resolution and optional emit behavior. Strict checks can expose issues represented in the types, but explicit `any`, assertions, unvalidated input and the actual bundler/runtime remain outside that guarantee.

**How It Works**

2. **Q:** How do bundled, fixed Node and current Node module settings differ, and how should a team choose?
   **A:** Use `module: "preserve"` or `"esnext"` with `moduleResolution: "bundler"` when a bundler loads the application. For a fixed Node 16/18/20 contract, use the matching `module` mode with `moduleResolution: "node16"`; the `node20` module mode models `require(ESM)` support available in newer Node 20 releases. Use `nodenext` for both settings when following current Node rules. Node ESM relative imports need runtime-valid extensions such as `.js`; package `exports` conditions and the actual loader must agree with the checker.

3. **Q:** Which type/value boundary errors does `isolatedModules` catch, and what must a project still verify?
   **A:** It reports constructs that a file-at-a-time transform cannot interpret safely, including a type-only re-export written as a value export and ambient const-enum access. Ordinary const-enum emission depends on the tool; run `tsc --noEmit` and inspect the actual transform output.

4. **Q:** How does `verbatimModuleSyntax` go further than `isolatedModules`?
   **A:** It requires `import type`/`export type` for every type-only import (not just re-exports) and prevents the emitter from rewriting module syntax, while explicitly type-only imports/exports and annotations are erased. It does not preserve every source byte.

**Code Examples**

5. **Q:** What happens if you set `composite: true, declaration: false`, and why?
   **A:** It fails to build (TS6304) — `composite` implies `declaration`, so the two flags contradict each other; declare intent with `declarationMap` instead.

**Common Mistakes**

6. **Q:** What class of bugs does `skipLibCheck` actually skip, and what does it never skip?
   **A:** It skips type checking inside `.d.ts` declaration files, including both dependency declarations and your own. Your ordinary source files are still checked against those declarations. An incorrect declaration can therefore escape checking and give source code a misleading description of the runtime behavior.

**Best Practices**

7. **Q:** An upgrade to TypeScript 6 or 7 changes a project's checking or rejects its config. What should you inspect?
   **A:** Pin and record the compiler version, inspect `tsc --showConfig`, and compare defaults and removed options with the [TypeScript 6 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html) and [TypeScript 7.0 announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/). TS 6 defaults `strict` to true and `types` to an empty list; TS 7 removes deprecated options such as `baseUrl` and `node10` resolution. Validate the application's actual build and runtime after migrating.

## Changed-condition checks

Source: [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md)

**Q:** A contract requires value:string, then a second contract requires value:number. Does intersection choose the later member?
**A:** No. It requires both, producing an impossible string-and-number property. An interface extension instead reports the incompatible member at its declaration.

Source: [Keyof and Typeof](10.2.1.02-keyof-typeof.md)

**Q:** Trace settings.port through typeof, keyof and indexed access. What changes when the property is optional?
**A:** typeof settings gives the object type, keyof selects names, and indexed access selects port's value type. An optional port read also admits undefined; the key union does not prove the runtime value is present.

Source: [Type Narrowing](10.2.1.03-type-narrowing.md)

**Q:** JSON parsing returns {name:42,email:"a@example.com"}. Why does parseUser reject it despite valid JSON?
**A:** Syntax parsing yields unknown data. isUser checks the actual required string fields; an as User cast would falsely claim them without changing the value.

Source: [Compiler Options](10.2.1.04-tsconfig-compiler-options.md)

**Q:** With noUncheckedIndexedAccess enabled, why must labels[0] be guarded, and what happens if paths is configured only in tsc?
**A:** The array type admits an empty array, so the index can be undefined. paths helps static resolution but does not rewrite emitted imports; the bundler/loader needs the matching alias contract.

Source: [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md)

**Q:** A Vite app checks `vite.config.ts` with TypeScript 6 but gets missing `process` and Vite-client globals. What should its config provide?
**A:** Install `@types/node` and include the required ambient packages, for example `"types": ["vite/client", "node"]`. With TypeScript 6, ambient packages are not automatically included just because they are installed.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
