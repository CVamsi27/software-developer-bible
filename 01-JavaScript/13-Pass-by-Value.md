---
section: JavaScript
category: Core
tags: [concept]
---

# Pass by Value vs Pass by Reference

## Definition

JavaScript uses **pass by value** for all parameters. However, when passing objects, the "value" being passed is a reference to the object, not the object itself. This creates the illusion of pass by reference, but it's actually pass by value of the reference.

## Why Do We Need It?

- **Understanding Mutation**: Know when changes affect original objects
- **Function Design**: Predict how functions modify arguments
- **Bug Prevention**: Avoid unintended side effects
- **Performance**: Understand when copying occurs
- **Interview Questions**: Common topic in technical interviews

## How It Works

### Pass by Value vs Pass by Reference

```text
┌─────────────────────────────────────────────────────────────┐
│              PASS BY VALUE vs PASS BY REFERENCE               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PASS BY VALUE (Primitives):                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let x = 10;                                       │    │
│  │  function change(value) {                          │    │
│  │    value = 20;  // Changes local copy             │    │
│  │  }                                                  │    │
│  │  change(x);                                        │    │
│  │  console.log(x);  // 10 (unchanged)               │    │
│  │                                                      │    │
│  │  MEMORY:                                           │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │  x: [10] ←── Original                       │   │    │
│  │  │  value: [10] ←── Copy                       │   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  PASS BY REFERENCE VALUE (Objects):                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let obj = { value: 10 };                         │    │
│  │  function change(o) {                             │    │
│  │    o.value = 20;  // Changes original!            │    │
│  │  }                                                  │    │
│  │  change(obj);                                      │    │
│  │  console.log(obj.value);  // 20 (changed!)        │    │
│  │                                                      │    │
│  │  MEMORY:                                           │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │  obj: [ref] ─────┐                          │   │    │
│  │  │                   ▼                          │   │    │
│  │  │  o: [ref] ─────→ { value: 10 }             │   │    │
│  │  │                   (same object)              │   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  REASSIGNMENT (Objects):                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let obj = { value: 10 };                         │    │
│  │  function reassign(o) {                           │    │
│  │    o = { value: 20 };  // Creates new object!    │    │
│  │  }                                                  │    │
│  │  reassign(obj);                                    │    │
│  │  console.log(obj.value);  // 10 (unchanged!)     │    │
│  │                                                      │    │
│  │  MEMORY:                                           │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │  obj: [ref] ─────┐                          │   │    │
│  │  │                   ▼                          │   │    │
│  │  │  { value: 10 } ←── Original                 │   │    │
│  │  │                                              │   │    │
│  │  │  o: [ref] ─────→ { value: 20 } ←── New!    │   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Primitive Types

```text
┌─────────────────────────────────────────────────────────────┐
│                     PRIMITIVE TYPES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  All primitives are passed by value:                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  • Number:     42, 3.14, NaN                       │    │
│  │  • String:     'hello', "world"                    │    │
│  │  • Boolean:    true, false                         │    │
│  │  • null:       null                                │    │
│  │  • undefined:  undefined                           │    │
│  │  • Symbol:     Symbol('id')                        │    │
│  │  • BigInt:     9007199254740991n                   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  When passed to function:                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let x = 10;                                       │    │
│  │                                                      │    │
│  │  function double(num) {                           │    │
│  │    num = num * 2;  // Local copy modified         │    │
│  │    return num;                                     │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  let result = double(x);                          │    │
│  │  console.log(x);      // 10 (unchanged)          │    │
│  │  console.log(result);  // 20 (new value)          │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Reference Types

```text
┌─────────────────────────────────────────────────────────────┐
│                     REFERENCE TYPES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  All objects (including arrays, functions) are passed by    │
│  value of the reference:                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  • Object:     { name: 'Alice' }                  │    │
│  │  • Array:      [1, 2, 3]                          │    │
│  │  • Function:   () => {}                           │    │
│  │  • Date:       new Date()                         │    │
│  │  • RegExp:     /pattern/                          │    │
│  │  • Map:        new Map()                          │    │
│  │  • Set:        new Set()                          │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  When passed to function:                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let obj = { value: 10 };                         │    │
│  │                                                      │    │
│  │  function modify(o) {                             │    │
│  │    o.value = 20;  // Modifies original!           │    │
│  │    return o;                                       │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  let result = modify(obj);                        │    │
│  │  console.log(obj.value);  // 20 (modified!)       │    │
│  │  console.log(result.value);  // 20 (same object)  │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Primitive Pass by Value

```typescript
let primitive = 10;

function modifyPrimitive(value: number) {
  value = value * 2;  // Changes local copy
  console.log('Inside function:', value);  // 20
}

modifyPrimitive(primitive);
console.log('Outside function:', primitive);  // 10 (unchanged)

// Primitive values are copied
// Original is not affected

```

### Object Pass by Reference Value

```typescript
let obj = { value: 10 };

function modifyObject(o: { value: number }) {
  o.value = 20;  // Modifies original!
  console.log('Inside function:', o.value);  // 20
}

modifyObject(obj);
console.log('Outside function:', obj.value);  // 20 (modified!)

// Object reference is copied
// Both point to same object

```

### Reassignment vs Mutation

```typescript
// Mutation: Changes the original object
let obj1 = { value: 10 };

function mutate(o: { value: number }) {
  o.value = 20;  // Mutation!
}

mutate(obj1);
console.log(obj1.value);  // 20 (changed)

// Reassignment: Creates new object, original unchanged
let obj2 = { value: 10 };

function reassign(o: { value: number }) {
  o = { value: 20 };  // Reassignment!
}

reassign(obj2);
console.log(obj2.value);  // 10 (unchanged)

```

### Array Examples

```typescript
// Array mutation
let arr = [1, 2, 3];

function pushItem(a: number[]) {
  a.push(4);  // Mutates original
}

pushItem(arr);
console.log(arr);  // [1, 2, 3, 4]

// Array reassignment
let arr2 = [1, 2, 3];

function replaceArray(a: number[]) {
  a = [4, 5, 6];  // Reassignment
}

replaceArray(arr2);
console.log(arr2);  // [1, 2, 3] (unchanged)

```

### String Immutability

```typescript
// Strings are primitives, but have methods
let str = 'hello';

function appendWorld(s: string) {
  s = s + ' world';  // Creates new string
}

appendWorld(str);
console.log(str);  // 'hello' (unchanged)

// String methods return new strings
let str2 = 'hello';
str2.toUpperCase();  // Returns 'HELLO', doesn't modify
console.log(str2);  // 'hello' (unchanged)

str2 = str2.toUpperCase();  // Reassignment required
console.log(str2);  // 'HELLO'

```

### Function Parameters

```typescript
// Passing primitives
function increment(num: number) {
  num++;
  return num;
}

let x = 5;
let y = increment(x);
console.log(x);  // 5 (unchanged)
console.log(y);  // 6 (new value)

// Passing objects
function addObject(arr: number[], value: number) {
  arr.push(value);
  return arr;
}

let a = [1, 2, 3];
let b = addObject(a, 4);
console.log(a);  // [1, 2, 3, 4] (modified!)
console.log(b);  // [1, 2, 3, 4] (same array)

```

### Destructuring

```typescript
// Destructuring creates new variables
let obj = { a: 1, b: 2, c: 3 };

let { a, b } = obj;
a = 10;  // Changes local 'a', not obj.a
console.log(obj.a);  // 1 (unchanged)

// Array destructuring
let arr = [1, 2, 3];
let [first, second] = arr;
first = 10;  // Changes local 'first', not arr[0]
console.log(arr[0]);  // 1 (unchanged)

```

## Real-World Use Cases

### 1. Immutable State Updates

```typescript
// React state updates
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'UPDATE':
      // Bad: Mutates state
      // state.value = action.payload;
      // return state;

      // Good: Returns new state
      return { ...state, value: action.payload };

    default:
      return state;
  }
}

```

### 2. Pure Functions

```typescript
// Bad: Mutates input
function addToArray(arr: number[], value: number) {
  arr.push(value);
  return arr;
}

// Good: Returns new array
function addToArrayPure(arr: number[], value: number) {
  return [...arr, value];
}

```

### 3. Object Cloning

```typescript
// Shallow clone
const original = { a: 1, b: { c: 2 } };
const shallow = { ...original };

// Deep clone
const deep = JSON.parse(JSON.stringify(original));
// Or
const deep2 = structuredClone(original);

```

### 4. Event Handler Context

```typescript
class Component {
  private data = { value: 0 };

  // Problem: 'this' context lost
  handleClick() {
    console.log(this.data.value);
  }

  // Solution: Arrow function or bind
  handleClickFixed = () => {
    console.log(this.data.value);
  };
}

```

### 5. Higher-Order Functions

```typescript
// Function that returns a function
function createMultiplier(multiplier: number) {
  return function(number: number) {
    return number * multiplier;
  };
}

const double = createMultiplier(2);
console.log(double(5));  // 10

// Closure captures 'multiplier' by value

```

## Common Mistakes

### 1. Assuming Pass by Reference

```typescript
// Mistake: Thinking objects are passed by reference
function modifyObject(obj: { value: number }) {
  obj = { value: 20 };  // Reassignment!
}

let obj = { value: 10 };
modifyObject(obj);
console.log(obj.value);  // 10 (not 20!)

```

### 2. Mutating Arguments

```typescript
// Bad: Mutating the original array
function sortArray(arr: number[]) {
  return arr.sort((a, b) => a - b);  // Mutates original!
}

let arr = [3, 1, 2];
sortArray(arr);
console.log(arr);  // [1, 2, 3] (mutated!)

// Good: Create copy first
function sortArraySafe(arr: number[]) {
  return [...arr].sort((a, b) => a - b);
}

```

### 3. Sharing References

```typescript
// Problem: Multiple variables reference same object
let original = { value: 10 };
let copy = original;

copy.value = 20;
console.log(original.value);  // 20 (shared!)

// Solution: Create actual copy
let actualCopy = { ...original };

```

### 4. Forgetting Immutability

```typescript
// Bad: Direct mutation
function updateItem(items: any[], index: number, value: any) {
  items[index] = value;  // Mutates original!
  return items;
}

// Good: Immutable update
function updateItemSafe(items: any[], index: number, value: any) {
  return items.map((item, i) => i === index ? value : item);
}

```

## Best Practices

### 1. Use Spread Operator for Shallow Copies

```typescript
// Shallow copy
const original = { a: 1, b: 2 };
const copy = { ...original };

// Array shallow copy
const arr = [1, 2, 3];
const arrCopy = [...arr];

```

### 2. Use Object.freeze for Immutability

```typescript
const frozen = Object.freeze({ value: 10 });
frozen.value = 20;  // Silently fails (or throws in strict mode)
console.log(frozen.value);  // 10

```

### 3. Prefer Pure Functions

```typescript
// Pure function: No side effects
function add(a: number, b: number): number {
  return a + b;
}

// Impure function: Has side effects
let total = 0;
function addToTotal(value: number) {
  total += value;  // Modifies external state
}

```

### 4. Document Mutation Behavior

```typescript
/**

 - Sorts the array in place (mutates original)
 */
function sortInPlace(arr: number[]): number[] {
  return arr.sort((a, b) => a - b);
}

/**

 - Returns sorted copy (original unchanged)
 */
function sorted(arr: number[]): number[] {
  return [...arr].sort((a, b) => a - b);
}

```

## Performance Considerations

### Copying vs Referencing

```typescript
// Referencing is faster (no copy)
const obj = { large: 'data' };
function process(o: typeof obj) {
  // Just uses reference, no copy
}

// Copying has overhead
function processCopy(o: typeof obj) {
  const copy = { ...o };  // Creates copy
  // Process copy
}

// For large objects, prefer referencing when possible
// But be careful about mutations

```

### Immutability Libraries

```typescript
// Immutable.js (efficient immutable data structures)
import { Map } from 'immutable';

const original = Map({ a: 1, b: 2 });
const updated = original.set('c', 3);

// original is unchanged
// updated is new Map

```

## Summary

Understanding pass by value vs reference is crucial:

1. **Primitives**: Passed by value (copied)

2. **Objects**: Passed by value of reference (shared)

3. **Mutation**: Changes affect original

4. **Reassignment**: Doesn't affect original

5. **Copying**: Use spread, Object.assign, or structuredClone

6. **Immutability**: Use Object.freeze or immutable libraries

7. **Best practices**: Document mutation, use pure functions

Understanding this prevents bugs and enables better code design.

## Cheat Sheet
```text
PASS BY VALUE VS REFERENCE CHEAT SHEET
═══════════════════════════════════════════════════════════════

PRIMITIVES (Pass by Value):
• Number, String, Boolean, null, undefined, Symbol, BigInt
• Copied when passed to functions
• Changes don't affect original

OBJECTS (Pass by Value of Reference):
• Object, Array, Function, Date, RegExp, Map, Set
• Reference copied, not object
• Changes to properties affect original
• Reassignment doesn't affect original

MEMORY MODEL:
Primitive: variable → [value]
Object: variable → [reference] → [object in heap]

MUTATION vs REASSIGNMENT:
Mutation: obj.value = 20  (affects original)
Reassignment: obj = { value: 20 }  (doesn't affect original)

COPYING:
Shallow: { ...obj }, Object.assign({}, obj)
Deep: JSON.parse(JSON.stringify(obj)), structuredClone(obj)

BEST PRACTICES:
• Document mutation behavior
• Use pure functions
• Create copies before modification
• Use Object.freeze for immutability
• Use TypeScript for type safety

COMMON MISTAKES:
• Assuming pass by reference
• Mutating arguments
• Sharing references unintentionally
• Forgetting shallow vs deep copy

PERFORMANCE:
• Referencing: O(1)
• Shallow copy: O(n)
• Deep copy: O(n*m)
• Choose based on needs

DEBUGGING:
• console.log before/after
• Object.isFrozen() check
• Memory profiling
• Mutation testing

SECURITY:
• Prototype pollution
• Information leakage
• Privilege escalation
• Mitigation: freeze, validation

```

---

## See Also
- [TypeScript](../02-TypeScript/)
- [Node.js](../05-NodeJS/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- [MDN: Passing Arguments](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function)
- [JavaScript.info: Copying by Reference](https://javascript.info/object-copy)
- [FreeCodeCamp: Pass by Value vs Pass by Reference](https://www.freecodecamp.org/news/js-pass-by-value-or-reference-explained/)
- [ECMAScript Specification: Copy Data Blocks](https://tc39.es/ecma262/#sec-copydatablockbytes)
