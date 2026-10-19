<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Type Transformations — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Utility Types

Source: [Utility Types](10.2.3.01-utility-types.md)

**Q:** How does `Pick` behave when the source model gains an unrelated field?

**A:** The selected view stays limited to its chosen keys. An `Omit` view instead admits new fields unless they are explicitly excluded.

**Q:** What is still mutable inside a `Readonly` object containing nested settings?

**A:** Fields inside the nested settings object remain writable. The shallow utility blocks replacing the top-level property, not mutation through its stored reference.

**Q:** Why must a `fetch` wrapper parse JSON before returning a DTO?

**A:** `fetch` resolves to a Response object, not the payload. Reading JSON and validating the resulting unknown data are separate steps needed to earn the DTO type.

**Q:** How do `ReturnType` and `Awaited` answer different questions about an async function?

**A:** The first reports the function's declared promise return type. Applying the second reveals the value available after promise-like resolution.

**Q:** Which utility composition keeps `label` mandatory while relaxing other button props?

**A:** Combine `Pick<Props, 'label'>` with `Partial<Omit<Props, 'label'>>`. Making the picked label partial would relax the wrong side.

**Q:** Why separate an update ID from optional changes?

**A:** A partial entity permits the identifier to be absent. A separate required ID identifies the target; an explicit Pick allowlist prevents optional changes from also granting writes to IDs, secrets or server-controlled fields.

**Q:** Does `Omit<User, 'password'>` remove a password from an actual object?

**A:** It only changes which properties the static view exposes. Runtime projection must create a value without the password before serialization.

**Q:** Which overload does `Parameters` or `ReturnType` extract from an overloaded function?

**A:** It uses the last declared signature. It does not perform overload selection from hypothetical call arguments.

## Conditional Types

Source: [Conditional Types](10.2.3.02-conditional-types.md)

**Q:** Which part of a conditional determines whether a union is tested member by member?

**A:** The checked side must be a naked type parameter. A concrete union expression or a tuple-wrapped parameter instead undergoes one whole-type test.

**Q:** Why does a distributive test of `never` produce no true or false result?

**A:** `never` has no union members to visit. Distribution therefore produces an empty union, which is itself `never`.

**Q:** What does tuple wrapping change in an array-producing conditional?

**A:** It prevents separate branch evaluation for each member. A string-or-number input can then become one array of the union instead of a union of homogeneous arrays.

**Q:** Why infer an argument tuple before selecting its first member?

**A:** The tuple reveals whether an argument exists. A direct one-parameter function pattern can also match a zero-parameter function and infer `unknown`.

**Q:** Why does the nullable-key map remove optional modifiers before indexing it?

**A:** Otherwise an optional mapped property contributes `undefined` when read. Removing optionality leaves only the selected key names in the result union.

**Q:** Why is a conditional returning `any` less useful than one capturing the return type?

**A:** It erases the result information that callers need. Capturing with `infer` preserves the type already present in the function signature.

**Q:** Can a type alias that computes `true` or `false` act as a runtime guard?

**A:** No JavaScript is emitted for the alias. A runtime guard needs a function that tests the actual value and communicates narrowing through its signature.

**Q:** What contract does `OptionalExcept<T, K>` need to enforce?

**A:** Keys in K remain required while other keys may be omitted. Making only K partial implements the opposite policy.

## Mapped Types

Source: [Mapped Types](10.2.3.03-mapped-types.md)

**Q:** What information does `T[K]` preserve while a map iterates keys?

**A:** It retrieves the source value type for the current key. Replacing it with a fixed type intentionally discards field-specific information.

**Q:** How do you remove optionality while retaining the original values?

**A:** Use `-?` on the mapped property and keep `T[K]` as its value. Adding or removing a modifier is separate from selecting a new value type.

**Q:** What does mapping a key to `never` accomplish in an `as` clause?

**A:** It omits that property from the resulting object type. It does not delete a property from a runtime object.

**Q:** Why does `mapValues` enumerate with `Reflect.ownKeys`?

**A:** Its declared key space may include symbols, which a `for...in` loop skips. Reflection reports numeric property keys as strings, so the callback receives the actual `string | symbol` key. The helper still assumes the declared fields are the own fields of a closed plain record; descriptors are not preserved, getters execute during reads, and extra runtime fields can violate the result type claim.

**Q:** What extra operation does a deep partial perform when a database object is supplied?

**A:** It relaxes fields inside that object as well as the outer property. A shallow partial still requires the nested object's complete original shape.

**Q:** Why can a direct `T[K] extends object` test miss an optional nested record?

**A:** Reading an optional property gives a union with `undefined`, and that union does not wholly extend object. A helper conditional over its own naked parameter can recurse per member.

**Q:** Does `field: string | undefined` permit omitting a required field?

**A:** The field must still be present unless it has the optional modifier. Its union only allows an explicit undefined value.

**Q:** Why keep Date and functions as leaves in the deep transform example?

**A:** Mapping their members as ordinary data can destroy their usable signatures. Keeping them as leaves preserves those APIs, while leaving runtime mutation behavior unchanged. Map/Set/host classes require additional domain-specific leaf or readonly-container rules.

## Template Literal Types

Source: [Template Literal Types](10.2.3.04-template-literal-types.md)

**Q:** How many strings can two color values combine with two size values to produce?

**A:** Four: each color combines once with each size, so the total is 2 × 2.

**Q:** Why does `on${Capitalize<string>}` still fail to whitelist known events?

**A:** `Capitalize<string>` widens to `string`, so this pattern accepts any string with the `on` prefix. A finite event-name union enumerates supported names and rejects other keys.

**Q:** Why must route definitions retain `:id` rather than widen that segment to `${string}`?

**A:** The named placeholder is the information used to derive the required parameter. A broad string segment allows arbitrary names and loses the finite route contract.

**Q:** Why does a key-remapping type apply `SnakeToCamel<K>` directly?

**A:** A generic type alias cannot be passed as a first-class type function and invoked through another type parameter. The mapped type must apply a known alias or another explicitly modeled transformation.

**Q:** Why does `CamelKeys<T>` preserve a key when it is not a string?

**A:** Its `as` branch maps non-string keys back to themselves. Mapping them to `never` would silently drop numeric and symbol properties from the derived type.

**Q:** Why does `ReplaceAll` stop immediately for an empty search string?

**A:** An empty pattern can keep matching without consuming input. The guard gives that case a defined result instead of relying on recursive progress.

**Q:** Do conditional and interpolation expansion obey the same distribution rule?

**A:** Conditional distribution requires a naked checked type parameter. Interpolated unions expand as a Cartesian product independently of that rule.

**Q:** How should a team judge whether a recursive string helper is too expensive?

**A:** Measure the consuming compilation and editor behavior with realistic inputs. Fixed millisecond estimates and a supposed configurable universal depth do not describe the checker's actual work.

## Changed-condition checks

Source: [Utility Types](10.2.3.01-utility-types.md)

**Q:** Trace a Bob-only profile patch, then assign the full secret-bearing entity to a public type. Which values actually change?

**A:** The patch helper creates a new outer object with Bob and retains the original Alice object. Assigning to a public static view does not remove stored secret fields; serialization needs a real selected-field projection.

Source: [Conditional Types](10.2.3.02-conditional-types.md)

**Q:** Is ["one",2] admitted by ToArray<string|number>, and what changes with tuple wrapping?

**A:** The distributive result is string[]|number[], so a mixed array fits neither member. Whole-input wrapping produces (string|number)[], which permits that mixed array. never has no members to distribute.

Source: [Mapped Types](10.2.3.03-mapped-types.md)

**Q:** What is created for name and age in Getters, and does that add functions to a real user?

**A:** Static members getName:()=>string and getAge:()=>number are derived from their corresponding values. No runtime functions are installed. Numeric/symbol keys omitted by the string template stay omitted from the type only.

Source: [Template Literal Types](10.2.3.04-template-literal-types.md)

**Q:** Build /users/:userId/posts/:postId with userId=a/b, then omit postId at runtime. What happens?

**A:** The builder substitutes whole segments and encodes a/b as a%2Fb. Missing or nonstring postId throws even if an unchecked caller bypassed the static contract; it cannot leave a trusted unresolved placeholder.

**Q:** What does `Split<'a,', ','>` produce, and what does the helper return for an empty delimiter?

**A:** It produces `['a']` under the stated trailing-delimiter policy. An empty delimiter returns `never`, so the helper rejects a case that cannot make recursive progress.

**Q:** What does `Join` return for a readonly tuple versus an open-ended `string[]`?

**A:** A finite readonly tuple preserves its exact joined literal, such as `"users/42"`; an open-ended array widens to `string` because its length and elements are unknown.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
