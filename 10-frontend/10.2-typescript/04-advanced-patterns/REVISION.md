<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)

# Advanced Patterns — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## The `satisfies` Operator

Source: [The `satisfies` Operator](10.2.4.01-satisfies-operator.md)

**Definition**

1. **Q:** Which type does a checked expression retain after `satisfies`?
   **A:** It keeps the type inferred for that contextually typed expression rather than adopting the whole target. The target can still influence how literal values or tuples are inferred.

**How It Works**

2. **Q:** Why do route-table keys remain available to `keyof` after a `satisfies Record` check?
   **A:** The result still has the specific properties written in the expression. A variable annotated with the Record contract instead exposes its open index signature.

3. **Q:** Can a discriminated-union annotation also identify a literal's current branch?
   **A:** Yes; control-flow analysis can narrow the annotated variable after initialization. The distinction is its wider declared contract, not an absence of narrowing.

**Code Examples**

4. **Q:** Why use `as const` for feature-flag names declared as strings in the target?
   **A:** A plain string context allows the names to widen to string. Pinning the literals first lets the derived key union reject names outside the listed flags.

5. **Q:** What does `satisfies` prove about an untrusted JSON result at runtime?
   **A:** Nothing; the operator emits no validation code. Parse the result as unknown and run a validator before relying on a domain type.

**Common Mistakes**

6. **Q:** Why might a flag initialized with `true satisfies boolean` reject a later false value?
   **A:** Contextual typing can preserve the true literal. Annotate the variable or property with boolean when future assignments should admit both values.

7. **Q:** Does checking an existing object with `satisfies` guarantee it has no extra fields?
   **A:** Structural assignability allows extra fields on an existing compatible value. The excess-property checks that catch literal typos do not make arbitrary objects exact.

**Best Practices**

8. **Q:** When is an explicit annotation useful for an exported value?
   **A:** It supplies a stable public contract instead of exposing implementation-specific inference. That can allow an internal refactor without changing the types consumers compile against.

## Branded Types

Source: [Branded Types](10.2.4.02-branded-types.md)

**How It Works**

1. **Q:** Why can an ordinary string not satisfy a required brand field?
   **A:** Structural compatibility checks the intersection as well as its base primitive. The extra required member makes the untagged string insufficient, even though the runtime representation stays a string.

2. **Q:** What isolation does a module-private `unique symbol` add?
   **A:** Its identity makes the phantom key distinct from independently declared symbols, avoiding accidental agreement on a common property name. It still creates no runtime property when used only in a type.

**Code Examples**

3. **Q:** Why must callers inspect a `Price | Error` result instead of asserting `Price`?
   **A:** The validator can actually return an Error object. A cast hides that branch and can let arithmetic operate on a failure instead of a price.

4. **Q:** How does `NoInfer` prevent accidental cross-currency addition in the example?
   **A:** It keeps the second argument from helping choose the currency parameter. A USD first argument therefore requires the second argument to satisfy USD rather than inferring a USD-or-EUR union.

5. **Q:** Which unit must the second operand of `force` carry?
   **A:** Acceleration in meters per second squared. Multiplying mass by speed produces momentum, so a speed brand cannot justify a Newtons result.

**Common Mistakes**

6. **Q:** Can checking `value.__brand` identify a cast-branded primitive at runtime?
   **A:** No property was installed by the assertion. Runtime recognition must use the underlying data or an explicitly stored tag.

**Best Practices**

7. **Q:** What happens to the brand when a value passes through JSON?
   **A:** Only its ordinary data is serialized. A parser must validate the incoming value again before returning the branded type.

8. **Q:** Why does a type named `JWT` fail to prove a token is trustworthy?
   **A:** A phantom name cannot authenticate bytes or check claims. Signature and claim verification must happen before the program treats the token as trusted.

## Decorators

Source: [Decorators](10.2.4.03-decorators.md)

**Definition**

1. **Q:** Which compiler choice determines the decorator calling convention?
   **A:** Enabling `experimentalDecorators` selects the legacy convention. With it disabled, TypeScript 5.0 and later use the Stage 3 convention for supported class decorators.

**How It Works**

2. **Q:** Why does registering a parameter token not inject a value by itself?
   **A:** Registration records which argument position needs which dependency. A container must read that record and construct the class with resolved arguments.

3. **Q:** How does Stage 3 `bound` preserve a receiver for detached calls?
   **A:** It schedules an instance initializer that replaces the public method with a bound function. Each new instance therefore receives its own function linked to that instance.

**Code Examples**

4. **Q:** Why does `Min` wrap an accessor instead of a legacy field decorator?
   **A:** Accessor descriptors expose the setter that receives assignments. Legacy field decorators have no initializer hook, and a prototype setter can be shadowed by an own field.

5. **Q:** Why is the cache stored per instance?
   **A:** Two receivers can produce different results for the same arguments. Sharing one argument-only cache across them would return another instance's result.

**Common Mistakes**

6. **Q:** Is returning a descriptor mandatory after mutating it in legacy mode?
   **A:** No; the supplied descriptor remains in use when the decorator returns nothing. Returning is needed when supplying a replacement descriptor.

**Best Practices**

7. **Q:** In what order are two stacked decorators evaluated and applied?
   **A:** Their expressions evaluate in source order, then the resulting functions apply from the bottom upward. The resulting wrappers may therefore execute in the opposite order from application.

8. **Q:** How many attempts does `Retry(3)` allow?
   **A:** Four: the first attempt plus three retries. Its loop and log denominator must include that initial attempt.

## Declaration Files (.d.ts)

Source: [Declaration Files (.d.ts)](10.2.4.04-declaration-files.md)

**Definition**

1. **Q:** What does a function signature in a `.d.ts` promise about runtime code?
   **A:** It tells the checker how existing JavaScript can be used. It does not supply a function body or ensure the implementation fulfills that promise.

**How It Works**

2. **Q:** Why are imports and exports useful in declarations?
   **A:** They connect the types and values exposed by modules, just as they identify an implementation's public surface. Their presence also changes the file from global script scope to module scope.

**Code Examples**

3. **Q:** Why does the Express example augment `express-serve-static-core`?
   **A:** That package declares the core Request and Response interfaces used by handler types. Extending those interfaces makes custom fields visible through those signatures.

4. **Q:** What decides whether an SVG import should be typed as a URL or a component?
   **A:** The configured loader determines the runtime export. The declaration must describe that export rather than choosing a convenient type independently.

5. **Q:** Where must triple-slash directives appear to be recognized?
   **A:** Before statements and declarations at the beginning of the file. Moving them into a later example leaves ordinary comments rather than dependency directives.

**Common Mistakes**

6. **Q:** Does declaration generation copy manual source `.d.ts` files into `dist`?
   **A:** No; those files are compiler input. A packaging step must include them when generated declarations or the public entry point depend on them.

7. **Q:** How does a file declare globals after adding `export {}`?
   **A:** It places the global additions inside `declare global`. Top-level declarations now stay in the module's own scope.

**Best Practices**

8. **Q:** Why should a library test a consumer as well as checking its own declarations?
   **A:** A consumer exercises the published entry path, imports and inferred types together. A valid declaration file can still be absent from the package or describe behavior the JavaScript never implements.

## TypeScript Advanced Patterns — Decorators, Middleware, Advanced Generics

Source: [TypeScript Advanced Patterns — Decorators, Middleware, Advanced Generics](10.2.4.05-advanced-patterns.md)

**Definition**

1. **Q:** What makes a type pattern a composition rather than a new language feature?
   **A:** It relates existing generic parameters, key lookups and conditional transforms to enforce an API contract. The runtime implementation must still maintain that relationship.

**Advanced Generics**

2. **Q:** How does the emitter select the listener's payload type?
   **A:** Its event argument determines a key parameter, and indexing the event map with that key yields the payload. Reusing the parameter couples both arguments.

**Parameter Decorators**

3. **Q:** Which runtime step connects a recorded parameter index to a request value?
   **A:** A framework consumer resolves the metadata and builds the invocation arguments. The decorator only registers that information.

**Mapped Types**

4. **Q:** Why is recursively mapping every `object` too broad for general data transforms?
   **A:** Dates, functions and arrays are objects too, but their API members are not ordinary nested data fields. A useful transform needs leaf rules matching the application's domain.

**Template Literal Types**

5. **Q:** What limitation remains after extracting `clinicId` from a path type?
   **A:** The type-level result cannot parse a runtime URL. The router must implement the same path grammar and provide the extracted strings.

**Branded Types**

6. **Q:** Why should an API layer export branded constructors as well as branded aliases?
   **A:** Callers need a controlled way to turn external values into accepted IDs. A constructor keeps validation and the necessary assertion in one place.

**Common Mistakes**

7. **Q:** Does replacing `Record<string, any>` with `Record<string, unknown>` always accept an interface event map?
   **A:** No; an interface can lack the required string index signature. Constrain its known keys or use an object constraint while retaining precise key lookup types.

**Best Practices**

8. **Q:** Which evidence makes a complicated composed type worth keeping?
   **A:** It should reject a meaningful invalid call and give useful inference for valid calls. If assertions bypass both benefits, simplifying the API often provides stronger checking.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
