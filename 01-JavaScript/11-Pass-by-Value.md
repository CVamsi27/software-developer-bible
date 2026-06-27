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

```
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

```
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

```
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
 * Sorts the array in place (mutates original)
 */
function sortInPlace(arr: number[]): number[] {
  return arr.sort((a, b) => a - b);
}

/**
 * Returns sorted copy (original unchanged)
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

## Interview Questions

### Beginner (5-10 questions)

**Q1: Does JavaScript pass by value or pass by reference?**

A: JavaScript passes by value. For primitives, the value itself is copied. For objects, the reference (address) is copied, but it's still pass by value of the reference.

**Q2: What happens when you pass a primitive to a function?**

A: The primitive value is copied. Changes to the parameter inside the function don't affect the original value.

**Q3: What happens when you pass an object to a function?**

A: A copy of the reference is passed. Both the original and the parameter point to the same object. Changes to the object's properties affect the original.

**Q4: What is the difference between mutation and reassignment?**

A: 
- **Mutation**: Modifies the object's properties (affects original)
- **Reassignment**: Changes what the variable points to (doesn't affect original)

**Q5: How do you create a copy of an object?**

A: Use spread operator, Object.assign, or structuredClone:
```typescript
const copy = { ...original };
const copy2 = Object.assign({}, original);
const copy3 = structuredClone(original);
```

### Intermediate (5-10 questions)

**Q6: Why does this code output 10 instead of 20?**

```typescript
function change(x: number) {
  x = 20;
}
let a = 10;
change(a);
console.log(a);  // 10
```

A: Because `a` is a primitive (number). When passed to `change`, its value is copied. Changing `x` inside the function only changes the local copy.

**Q7: Why does this code output 20?**

```typescript
function change(obj: { value: number }) {
  obj.value = 20;
}
let a = { value: 10 };
change(a);
console.log(a.value);  // 20
```

A: Because `a` is an object. When passed to `change`, its reference is copied. Both `a` and `obj` point to the same object, so changing `obj.value` affects `a`.

**Q8: How do you prevent mutation of an object?**

A: Use Object.freeze:
```typescript
const frozen = Object.freeze({ value: 10 });
frozen.value = 20;  // Silently fails
```

**Q9: What is the difference between shallow and deep copy?**

A: 
- **Shallow copy**: Copies object properties, but nested objects are still references
- **Deep copy**: Copies everything, including nested objects

**Q10: How do you create a deep copy?**

A: Use JSON.parse(JSON.stringify()) or structuredClone:
```typescript
const deep = JSON.parse(JSON.stringify(original));
// Or
const deep2 = structuredClone(original);
```

### Senior (10-15 questions)

**Q11: Explain the memory model for object references.**

A: When an object is created, it's stored in heap memory. Variables hold references (pointers) to this memory. When passed to functions, the reference is copied, not the object.

**Q12: What are the performance implications of copying vs referencing?**

A: 
- Referencing: O(1), just copies pointer
- Shallow copy: O(n), copies n properties
- Deep copy: O(n*m), copies all nested objects

**Q13: How do you implement immutable data structures?**

A: Use libraries like Immutable.js, or implement persistent data structures that share structure between versions.

**Q14: What is structural sharing?**

A: Structural sharing is when immutable data structures share parts of their structure with previous versions, reducing memory usage while maintaining immutability.

**Q15: How do you handle large objects efficiently?**

A: 
1. Use references when possible
2. Lazy loading for large properties
3. WeakMap/WeakRef for caching
4. Streams for large data processing

### FAANG-style (5-10 questions)

**Q16: Design an immutable state management system.**

A: 
```typescript
class ImmutableState<T> {
  private history: T[] = [];
  private currentIndex = 0;
  
  constructor(initialState: T) {
    this.history.push(structuredClone(initialState));
  }
  
  get state(): T {
    return this.history[this.currentIndex];
  }
  
  update(updater: (state: T) => T): void {
    const newState = updater(structuredClone(this.state));
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(newState);
    this.currentIndex++;
  }
  
  undo(): void {
    if (this.currentIndex > 0) {
      this.currentIndex--;
    }
  }
  
  redo(): void {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
    }
  }
}
```

**Q17: How would you implement a deep freeze function?**

A: 
```typescript
function deepFreeze(obj: any): any {
  Object.freeze(obj);
  
  Object.getOwnPropertyNames(obj).forEach(prop => {
    if (obj[prop] !== null && 
        (typeof obj[prop] === 'object' || typeof obj[prop] === 'function') &&
        !Object.isFrozen(obj[prop])) {
      deepFreeze(obj[prop]);
    }
  });
  
  return obj;
}
```

**Q18: Analyze the memory implications of different cloning strategies.**

A: 
- **Shallow copy**: Low memory, but shared nested objects
- **Deep copy**: High memory, fully independent
- **Structural sharing**: Balanced memory, immutable
- **Lazy copying**: Copy on write, efficient for large objects

**Q19: How do you optimize object copying for performance?**

A: 
1. Copy only needed properties
2. Use typed arrays for numeric data
3. Implement copy-on-write
4. Use object pools for frequent allocation
5. Profile and measure actual usage

**Q20: What are the security implications of object references?**

A: 
1. **Prototype pollution**: Modifying shared prototypes affects all objects
2. **Information leakage**: References can expose internal state
3. **Privilege escalation**: Malicious code can modify shared objects
4. **Mitigation**: Use Object.freeze, input validation

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a bug caused by reference confusion?**

A: Common bug:
```typescript
// Bug: Array mutation
function addItem(items: string[], item: string) {
  items.push(item);
  return items;
}

let cart = ['apple', 'banana'];
let updatedCart = addItem(cart, 'orange');
console.log(cart);  // ['apple', 'banana', 'orange'] (mutated!)
console.log(updatedCart);  // ['apple', 'banana', 'orange']

// Fix: Create copy
function addItemSafe(items: string[], item: string) {
  return [...items, item];
}
```

**Q22: How do you handle deep cloning efficiently?**

A: 
1. Use structuredClone (modern browsers)
2. JSON.parse(JSON.stringify()) for simple objects
3. Custom deep clone with circular reference handling
4. Libraries like lodash for complex cases

**Q23: What is the relationship between references and garbage collection?**

A: Objects are garbage collected when no references point to them. If you copy a reference, the object stays alive. If you delete all references, it becomes eligible for GC.

**Q24: How do different languages handle this differently?**

A: 
- **Java**: Primitives by value, objects by reference
- **Python**: Everything by reference
- **C++**: Can choose by value or by reference
- **JavaScript**: Everything by value (including object references)

**Q25: What are best practices for working with object references?**

A: 
1. Document mutation behavior
2. Use pure functions when possible
3. Create copies before modification
4. Use Object.freeze for immutability
5. Be careful with shared state
6. Use TypeScript for type safety
7. Test for unintended mutations
8. Use immutable data structures when needed

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

```
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

## References & Learn More

- [MDN: Passing Arguments](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function)
- [JavaScript.info: Copying by Reference](https://javascript.info/object-copy)
- [FreeCodeCamp: Pass by Value vs Pass by Reference](https://www.freecodecamp.org/news/js-pass-by-value-or-reference-explained/)
- [ECMAScript Specification: Copy Data Blocks](https://tc39.es/ecma262/#sec-copydatablockbytes)
