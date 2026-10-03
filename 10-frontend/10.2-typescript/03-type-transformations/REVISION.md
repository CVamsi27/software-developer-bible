<!-- section: TypeScript | category: Reference | tags: revision, retrieval-practi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-TypeScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Type Transformations — TypeScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Utility Types

Source: [Utility Types](10.2.3.01-utility-types.md)

**How It Works**

1. **Q:** How does `Pick` behave when the source model gains an unrelated field?
   **A:** The selected view stays limited to its chosen keys. An `Omit` view instead admits new fields unless they are explicitly excluded.

2. **Q:** What is still mutable inside a `Readonly` object containing nested settings?
   **A:** Fields inside the nested settings object remain writable. The shallow utility blocks replacing the top-level property, not mutation through its stored reference.

3. **Q:** Why must a `fetch` wrapper parse JSON before returning a DTO?
   **A:** `fetch` resolves to a Response object, not the payload. Reading JSON and validating the resulting unknown data are separate steps needed to earn the DTO type.

4. **Q:** How do `ReturnType` and `Awaited` answer different questions about an async function?
   **A:** The first reports the function's declared promise return type. Applying the second reveals the value available after promise-like resolution.

**Code Examples**

5. **Q:** Which utility composition keeps `label` mandatory while relaxing other button props?
   **A:** Combine `Pick<Props, 'label'>` with `Partial<Omit<Props, 'label'>>`. Making the picked label partial would relax the wrong side.

**Common Mistakes**

6. **Q:** Why separate an update ID from optional changes?
   **A:** A partial entity permits the identifier to be absent. A separate required ID establishes which record is being changed before optional fields are considered.

**Best Practices**

7. **Q:** Does `Omit<User, 'password'>` remove a password from an actual object?
   **A:** It only changes which properties the static view exposes. Runtime projection must create a value without the password before serialization.

8. **Q:** Which overload does `Parameters` or `ReturnType` extract from an overloaded function?
   **A:** It uses the last declared signature. It does not perform overload selection from hypothetical call arguments.

## Conditional Types

Source: [Conditional Types](10.2.3.02-conditional-types.md)

**How It Works**

1. **Q:** Which part of a conditional determines whether a union is tested member by member?
   **A:** The checked side must be a naked type parameter. A concrete union expression or a tuple-wrapped parameter instead undergoes one whole-type test.

2. **Q:** Why does a distributive test of `never` produce no true or false result?
   **A:** `never` has no union members to visit. Distribution therefore produces an empty union, which is itself `never`.

3. **Q:** What does tuple wrapping change in an array-producing conditional?
   **A:** It prevents separate branch evaluation for each member. A string-or-number input can then become one array of the union instead of a union of homogeneous arrays.

**Code Examples**

4. **Q:** Why infer an argument tuple before selecting its first member?
   **A:** The tuple reveals whether an argument exists. A direct one-parameter function pattern can also match a zero-parameter function and infer `unknown`.

5. **Q:** Why does the nullable-key map remove optional modifiers before indexing it?
   **A:** Otherwise an optional mapped property contributes `undefined` when read. Removing optionality leaves only the selected key names in the result union.

**Common Mistakes**

6. **Q:** Why is a conditional returning `any` less useful than one capturing the return type?
   **A:** It erases the result information that callers need. Capturing with `infer` preserves the type already present in the function signature.

**Best Practices**

7. **Q:** Can a type alias that computes `true` or `false` act as a runtime guard?
   **A:** No JavaScript is emitted for the alias. A runtime guard needs a function that tests the actual value and communicates narrowing through its signature.

8. **Q:** What contract does `OptionalExcept<T, K>` need to enforce?
   **A:** Keys in K remain required while other keys may be omitted. Making only K partial implements the opposite policy.

## Mapped Types

Source: [Mapped Types](10.2.3.03-mapped-types.md)

**How It Works**

1. **Q:** What information does `T[K]` preserve while a map iterates keys?
   **A:** It retrieves the source value type for the current key. Replacing it with a fixed type intentionally discards field-specific information.

2. **Q:** How do you remove optionality while retaining the original values?
   **A:** Use `-?` on the mapped property and keep `T[K]` as its value. Adding or removing a modifier is separate from selecting a new value type.

3. **Q:** What does mapping a key to `never` accomplish in an `as` clause?
   **A:** It omits that property from the resulting object type. It does not delete a property from a runtime object.

**Code Examples**

4. **Q:** Why does `mapValues` enumerate with `Reflect.ownKeys`?
   **A:** Its declared key space may include symbols, which a `for...in` loop skips. The helper still assumes those keys are own properties of a plain record.

5. **Q:** What extra operation does a deep partial perform when a database object is supplied?
   **A:** It relaxes fields inside that object as well as the outer property. A shallow partial still requires the nested object's complete original shape.

**Common Mistakes**

6. **Q:** Why can a direct `T[K] extends object` test miss an optional nested record?
   **A:** Reading an optional property gives a union with `undefined`, and that union does not wholly extend object. A helper conditional over its own naked parameter can recurse per member.

**Best Practices**

7. **Q:** Does `field: string | undefined` permit omitting a required field?
   **A:** The field must still be present unless it has the optional modifier. Its union only allows an explicit undefined value.

8. **Q:** Why keep Date and functions as leaves in the deep transform example?
   **A:** Mapping their members as ordinary data can destroy their usable signatures. Keeping them as leaves preserves those APIs, while leaving runtime mutation behavior unchanged.

## Template Literal Types

Source: [Template Literal Types](10.2.3.04-template-literal-types.md)

**How It Works**

1. **Q:** How many combinations arise from three vertical and three horizontal positions?
   **A:** Each vertical member combines with every horizontal member, yielding nine strings. Adding another interpolated union multiplies the count again.

2. **Q:** Does `on${Capitalize<string>}` restrict names to known DOM events?
   **A:** It accepts a broad capitalization pattern. A finite source union is needed to whitelist particular event names.

**Code Examples**

3. **Q:** Why must route definitions retain `:id` rather than widen that segment to `${string}`?
   **A:** The named placeholder is the information used to derive the required parameter. A broad string segment allows arbitrary names and loses the finite route contract.

4. **Q:** Why does a key-remapping type apply `SnakeToCamel<K>` directly?
   **A:** A generic type alias cannot be passed as a first-class type function and invoked through another type parameter. The mapped type must apply a known alias or another explicitly modeled transformation.

5. **Q:** What prefix must be removed to undo `PrefixedKeys<User, 'user'>`?
   **A:** The exact lowercase prefix `user`. Template matching is case sensitive, so `User` leaves those generated keys unchanged.

6. **Q:** Why does `ReplaceAll` stop immediately for an empty search string?
   **A:** An empty pattern can keep matching without consuming input. The guard gives that case a defined result instead of relying on recursive progress.

**Common Mistakes**

7. **Q:** Do conditional and interpolation expansion obey the same distribution rule?
   **A:** Conditional distribution requires a naked checked type parameter. Interpolated unions expand as a Cartesian product independently of that rule.

**Performance Considerations**

8. **Q:** How should a team judge whether a recursive string helper is too expensive?
   **A:** Measure the consuming compilation and editor behavior with realistic inputs. Fixed millisecond estimates and a supposed configurable universal depth do not describe the checker's actual work.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
