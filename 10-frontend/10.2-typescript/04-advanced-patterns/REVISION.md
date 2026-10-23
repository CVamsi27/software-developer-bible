<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Advanced Patterns — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## The `satisfies` Operator

Source: [The `satisfies` Operator](10.2.4.01-satisfies-operator.md)

**Q:** Which type does a checked expression retain after `satisfies`?

**A:** It keeps the type inferred for that contextually typed expression rather than adopting the whole target. The target can still influence how literal values or tuples are inferred.

**Q:** How do finite and open route keys change the check?

**A:** A finite key union checks required and excess literal keys. Record<string, Route> accepts any declared key, while the inferred object still exposes only the keys it contains.

**Q:** When should a route table use an annotation instead of satisfies?

**A:** Use an annotation when later code needs the wider declared contract or must assign other values allowed by it. Use satisfies when callers should retain the entries and narrower values written in the object.

**Q:** When does as const add something to a satisfies check?

**A:** Use it when downstream code needs literal values or readonly properties. A target whose property is string or number can still widen a mutable property.

**Q:** What does `satisfies` prove about an untrusted JSON result at runtime?

**A:** Nothing; the operator emits no validation code. Parse the result as unknown and run a validator before relying on a domain type.

**Q:** Why can a property declared as string still widen after satisfies?

**A:** The target context gives that property the type string, so a mutable initializer such as one path literal widens to string. satisfies preserves the useful expression shape without forcing every member to stay literal.

**Q:** Does an open Record<string, Route> catch a misspelled route name?

**A:** No; every string key is allowed. Use a finite key union when the route set is fixed.

**Q:** When is an explicit annotation useful for an exported value?

**A:** It supplies a stable public contract instead of exposing implementation-specific inference. That can allow an internal refactor without changing the types consumers compile against.

**Q:** Does an open route record catch an admni key at declaration time?

**A:** No. Its string index signature accepts that entry if the value has the required shape. A finite key union catches a typo in the table; retained inferred keys catch a typo in later property access.

## Branded Types

Source: [Branded Types](10.2.4.02-branded-types.md)

**Q:** Why can an ordinary string not satisfy a required brand field?

**A:** Structural compatibility checks the intersection as well as its base primitive. The extra required member makes the untagged string insufficient, even though the runtime representation stays a string.

**Q:** What isolation does a module-private `unique symbol` add?

**A:** Its identity makes the phantom key distinct from independently declared symbols, avoiding accidental agreement on a common property name. It still creates no runtime property when used only in a type.

**Q:** What justifies returning a branded ID from a parser?

**A:** The parser first checks the unknown input against the runtime invariant, then keeps the assertion in that constructor. The marker alone does not inspect the input.

**Q:** How does `NoInfer` prevent accidental cross-currency addition in the example?

**A:** It keeps the second argument from helping choose the currency parameter. A USD first argument therefore requires the second argument to satisfy USD rather than inferring a USD-or-EUR union.

**Q:** What does a unit brand guarantee about arithmetic?

**A:** It can reject passing seconds to an operation that requires meters, but it does not derive multiplication or division dimensions. Those operations need explicit domain rules and result brands.

**Q:** Can checking `value.__brand` identify a cast-branded primitive at runtime?

**A:** No property was installed by the assertion. Runtime recognition must use the underlying data or an explicitly stored tag.

**Q:** What happens to the brand when a value passes through JSON?

**A:** Only its ordinary data is serialized. A parser must validate the incoming value again before returning the branded type.

**Q:** Why does a type named `JWT` fail to prove a token is trustworthy?

**A:** A phantom name cannot authenticate bytes or check claims. Signature and claim verification must happen before the program treats the token as trusted.

**Q:** Why check numeric bounds before asserting a unit brand?

**A:** The assertion adds no numeric safety. The constructor or operation must reject non-finite, out-of-range or overflowed results before returning the branded value.

**Q:** How can a parser reject an invalid canonical date such as February 30?

**A:** Parse the YYYY-MM-DD value as UTC and format it back; require the canonical string to equal the input. Also keep calendar dates distinct from instants and local-day calculations.

## Decorators

Source: [Decorators](10.2.4.03-decorators.md)

**Q:** Which compiler choice determines the decorator calling convention?

**A:** Enabling `experimentalDecorators` selects the legacy convention. With it disabled, TypeScript 5.0 and later use the newer TC39-proposal-based convention for supported class elements.

**Q:** Why does registering a parameter token not inject a value by itself?

**A:** Registration records which argument position needs which dependency. A container must read that record and construct the class with resolved arguments.

**Q:** How does a newer-convention `bound` decorator preserve a receiver for detached calls?

**A:** It schedules an instance initializer that replaces the public method with a bound function. Each new instance therefore receives its own function linked to that instance. Reading the final method by name also preserves replacements made by stacked decorators.

**Q:** Why validate through an auto-accessor rather than a plain field?

**A:** The accessor exposes initialization and set operations, so a decorator can check both initial and later values. A field decorator does not intercept ordinary later assignments.

**Q:** What happens when a synchronous logging wrapper decorates a promise-returning method?

**A:** It returns the original promise immediately; it does not await settlement or log the eventual result unless the wrapper explicitly handles the promise.

**Q:** Is returning a descriptor mandatory after mutating it in legacy mode?

**A:** No; the supplied descriptor remains in use when the decorator returns nothing. Returning is needed when supplying a replacement descriptor.

**Q:** In what order do stacked decorator factories, applications and wrappers run?

**A:** Factory expressions evaluate from top to bottom, decorators apply from bottom to top, and the outer replacement runs first when the method is called.

**Q:** How many attempts does a retry count of three allow, and what must a write policy decide?

**A:** Four attempts: one initial call and three retries. A write needs an idempotency policy because repeating it can duplicate effects.

**Q:** Why must a bound initializer read the final decorated member?

**A:** If it binds an earlier captured method, a wrapper applied outside it can be bypassed. Reading the final member preserves the composed wrapper before binding.

**Q:** Why does a trimmed field later accept an untrimmed assignment?

**A:** The field decorator replaces only its initial value. A decorated accessor setter can intercept later writes. [Field and accessor boundary](10.2.4.03-decorators.md#3-fields-and-accessors-have-different-write-behavior).

## Declaration Files (.d.ts)

Source: [Declaration Files (.d.ts)](10.2.4.04-declaration-files.md)

**Q:** What does a function signature in a `.d.ts` promise about runtime code?

**A:** It tells the checker how existing JavaScript can be used. It does not supply a function body or ensure the implementation fulfills that promise.

**Q:** Why are imports and exports useful in declarations?

**A:** They connect types and values to a module's public surface. A declaration file's script/module scope determines whether `declare module` declares a runtime-provided module or augments an existing one; its `.d.ts`, `.d.mts` or `.d.cts` module format is a separate Node resolution concern. [Scope and format](10.2.4.04-declaration-files.md#scope-determines-whether-a-declaration-adds-or-extends-names).

**Q:** Why does the Express example augment `express-serve-static-core`?

**A:** That package declares the core Request and Response interfaces used by handler types. Extending those interfaces makes custom fields visible through those signatures.

**Q:** What decides whether an SVG import should be typed as a URL or a component?

**A:** The configured loader determines the runtime export. The declaration must describe that export rather than choosing a convenient type independently.

**Q:** Where must triple-slash directives appear to be recognized?

**A:** Before statements and declarations at the beginning of the file. Moving them into a later example leaves ordinary comments rather than dependency directives.

**Q:** Does declaration generation copy manual source `.d.ts` files into `dist`?

**A:** No; those files are compiler input. A packaging step must include them when generated declarations or the public entry point depend on them.

**Q:** How does a file declare globals after adding `export {}`?

**A:** It places the global additions inside `declare global`. Top-level declarations now stay in the module's own scope.

**Q:** Why should a library test a consumer as well as checking its own declarations?

**A:** A consumer exercises the published entry path, imports and inferred types together. A valid declaration file can still be absent from the package or describe behavior the JavaScript never implements.

**Q:** Why keep a new ambient package declaration separate from its consumer import?

**A:** The top-level import turns the declaration file into a module. A declare module block then augments an existing resolved package instead of declaring a new ambient package.

**Q:** Can a consumer type check establish that `greet` returns a string at runtime?

**A:** It checks against the declaration's promise. Execute the exported JavaScript as well, and verify both entry paths in the package. [Two-path fixture](10.2.4.04-declaration-files.md#describe-existing-javascript).

## Composing Advanced TypeScript Patterns

Source: [Composing Advanced TypeScript Patterns](10.2.4.05-advanced-patterns.md)

**Q:** What makes a type pattern a composition rather than a new language feature?

**A:** It relates existing generic parameters, key lookups and conditional transforms to enforce an API contract. The runtime implementation must still maintain that relationship.

**Q:** How does the emitter select the listener's payload type?

**A:** Its event argument determines a key parameter, and indexing the event map with that key yields the payload. Reusing the parameter couples both arguments.

**Q:** Which runtime step connects a recorded parameter index to a request value?

**A:** A framework consumer resolves the metadata and builds the invocation arguments. The decorator only registers that information.

**Q:** Why can a type-level update not define patch behavior by itself?

**A:** The runtime update must decide which keys are allowed, whether omission preserves a field, and what explicit undefined means. The mapped type only describes a static shape.

**Q:** What can a template type derive from a route that runtime code still must do?

**A:** It can derive names from a string literal, but it cannot parse an incoming URL. A runtime router must implement the same grammar and provide the actual values.

**Q:** Why should an API layer export branded constructors as well as branded aliases?

**A:** Callers need a controlled way to turn external values into accepted IDs. A constructor keeps validation and the necessary assertion in one place.

**Q:** Why constrain an event map with object instead of Record<string, unknown>?

**A:** A named interface need not promise that every possible string key exists. The object constraint accepts its known event keys while the generic preserves their lookup types.

**Q:** Which evidence makes a complicated composed type worth keeping?

**A:** It should reject a meaningful invalid call and give useful inference for valid calls. If assertions bypass both benefits, simplifying the API often provides stronger checking.

**Q:** What changes if a listener unsubscribes another listener during one dispatch?

**A:** The copied list still invokes that listener in the current dispatch; removal changes the next emit. A thrown exception instead stops the remaining current calls. [Dispatch policy](10.2.4.05-advanced-patterns.md#dispatch-policy-is-part-of-the-api).

**Q:** Why build a union of event/payload tuples rather than two independent union parameters?

**A:** Each tuple retains a valid pairing. Independent unions could admit a name from one case with a payload from another. [Correlated contract](10.2.4.05-advanced-patterns.md#first-principles).

## TypeScript Compiler Pipeline

Source: [TypeScript Compiler Pipeline](10.2.4.06-typescript-compiler-pipeline.md)

**Q:** What belongs to a TypeScript `Program`?

**A:** Its configured root files, resolved dependencies, and compiler options. Inspect the selected project and file graph before assuming an editor or command-line invocation checked a particular file.

**Q:** How do the parser, binder, and checker contribute different information?

**A:** The parser creates syntax trees while dependency resolution grows the source graph. The binder connects declarations to symbols and scopes; the checker follows those relationships to determine types and report semantic diagnostics. Emission has its own output controls.

**Q:** Can a tool using the TypeScript 6 `CompilerHost` API simply switch its compiler dependency to TypeScript 7.0?

**A:** No. TypeScript 7.0 does not ship that JavaScript Compiler API. A tool that embeds it needs a compatible TypeScript 6 package or a deliberate integration with the newer versioned API; CLI compatibility does not imply API compatibility.

**Q:** Why might `tsc` report an error and still write JavaScript?

**A:** Diagnostics and emission have separate controls. `noEmit` suppresses output entirely, while `noEmitOnError` blocks output when errors exist. A release pipeline must set and enforce the intended policy.

**Q:** The import type-checks but Node cannot load the built package. What boundary should you compare?

**A:** Compare TypeScript's configured module resolution with the runtime's emitted files, package exports, extensions, and actual entry point. Type checking does not prove the runtime can load a module.

**Q:** Why can an editor show no error while a clean build fails?

**A:** The language service serves incremental editor requests and may use an inferred or different configured project. A clean build applies the selected project graph and build options; run it as a separate release gate.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md) — where this revision companion sits in the advanced-patterns path

## References & Learn More

The source chapters above contain the technical references for these answers.
