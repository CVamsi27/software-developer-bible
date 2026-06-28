# Generators

## Definition

**Generators** are special functions that can be paused and resumed. They use `function*` syntax and `yield` keyword to produce a sequence of values lazily (on-demand), implementing the iterator protocol.

## Why Do We Need It?

- **Lazy Evaluation**: Produce values only when needed
- **Memory Efficiency**: Don't compute entire sequence upfront
- **Async Flows**: Implement async/await patterns
- **Iterators**: Custom iteration behavior
- **State Machines**: Manage complex state transitions

## How It Works

### Generator Basics

```
┌─────────────────────────────────────────────────────────────┐
│                    GENERATOR BASICS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FUNCTION DECLARATION:                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function* myGenerator() {                         │    │
│  │    yield 1;                                         │    │
│  │    yield 2;                                         │    │
│  │    yield 3;                                         │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  CREATING GENERATOR:                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const gen = myGenerator();                        │    │
│  │                                                      │    │
│  │  // gen is an iterator object                      │    │
│  │  // Code doesn't run until .next() is called       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ITERATOR PROTOCOL:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  gen.next()  → { value: 1, done: false }          │    │
│  │  gen.next()  → { value: 2, done: false }          │    │
│  │  gen.next()  → { value: 3, done: false }          │    │
│  │  gen.next()  → { value: undefined, done: true }   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  VISUALIZATION:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  function* gen() {                                 │    │
│  │    console.log('Start');                           │    │
│  │    yield 1;  ←── Pauses here                      │    │
│  │    console.log('After 1');                         │    │
│  │    yield 2;  ←── Pauses here                      │    │
│  │    console.log('After 2');                         │    │
│  │    yield 3;  ←── Pauses here                      │    │
│  │    console.log('End');                             │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const g = gen();                                  │    │
│  │  g.next();  // Logs 'Start', returns { value: 1 } │    │
│  │  g.next();  // Logs 'After 1', returns { value: 2}│    │
│  │  g.next();  // Logs 'After 2', returns { value: 3}│    │
│  │  g.next();  // Logs 'End', returns { done: true } │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Generator Methods

```
┌─────────────────────────────────────────────────────────────┐
│                   GENERATOR METHODS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  next():                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Resumes execution until next yield              │    │
│  │  • Returns { value, done }                         │    │
│  │  • Can pass value to yield expression              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  return():                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Terminates generator                            │    │
│  │  • Returns { value, done: true }                   │    │
│  │  • Can pass final value                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  throw():                                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Throws error inside generator                   │    │
│  │  • Can be caught with try/catch                    │    │
│  │  • Resumes after catch if not re-thrown            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  USAGE:                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const gen = myGenerator();                        │    │
│  │                                                      │    │
│  │  gen.next();        // Resume                      │    │
│  │  gen.next(value);   // Pass value to yield         │    │
│  │  gen.return(value); // Terminate with value        │    │
│  │  gen.throw(error);  // Throw error inside          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Generator

```typescript
function* countTo(n: number): Generator<number> {
  for (let i = 1; i <= n; i++) {
    yield i;
  }
}

const counter = countTo(5);
console.log(counter.next());  // { value: 1, done: false }
console.log(counter.next());  // { value: 2, done: false }
console.log(counter.next());  // { value: 3, done: false }
console.log(counter.next());  // { value: 4, done: false }
console.log(counter.next());  // { value: 5, done: false }
console.log(counter.next());  // { value: undefined, done: true }
```

### Generator with Return Value

```typescript
function* fibonacci(): Generator<number> {
  let a = 0, b = 1;

  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

const fib = fibonacci();
console.log(fib.next().value);  // 0
console.log(fib.next().value);  // 1
console.log(fib.next().value);  // 1
console.log(fib.next().value);  // 2
console.log(fib.next().value);  // 3

// Get first 10 fibonacci numbers
function* take<T>(gen: Generator<T>, count: number): Generator<T> {
  for (let i = 0; i < count; i++) {
    const { value, done } = gen.next();
    if (done) break;
    yield value;
  }
}

const first10 = [...take(fibonacci(), 10)];
console.log(first10);  // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Passing Values to Generators

```typescript
function* inputProcessor(): Generator<string, string, string> {
  let name = yield "What is your name?";
  let age = yield `Hello ${name}, what is your age?`;
  return `${name} is ${age} years old`;
}

const gen = inputProcessor();
console.log(gen.next());           // { value: "What is your name?", done: false }
console.log(gen.next("Alice"));    // { value: "Hello Alice, what is your age?", done: false }
console.log(gen.next("30"));       // { value: "Alice is 30 years old", done: true }
```

### Generator for Iteration

```typescript
class Range {
  constructor(private start: number, private end: number) {}

  *[Symbol.iterator](): Generator<number> {
    for (let i = this.start; i <= this.end; i++) {
      yield i;
    }
  }
}

const range = new Range(1, 5);
for (const num of range) {
  console.log(num);  // 1, 2, 3, 4, 5
}

// Convert to array
const numbers = [...new Range(1, 5)];
console.log(numbers);  // [1, 2, 3, 4, 5]
```

### Async Generator

```typescript
async function* fetchPages(url: string): AsyncGenerator<any> {
  let page = 1;

  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();

    if (data.length === 0) break;

    yield data;
    page++;
  }
}

// Usage
async function getAllData() {
  const allData = [];

  for await (const page of fetchPages('https://api.example.com/data')) {
    allData.push(...page);
  }

  return allData;
}
```

### Generator Composition

```typescript
function* generator1() {
  yield 1;
  yield 2;
}

function* generator2() {
  yield 3;
  yield 4;
}

function* combined() {
  yield* generator1();
  yield* generator2();
}

const gen = combined();
console.log([...gen]);  // [1, 2, 3, 4]
```

### Generator for State Machine

```typescript
function* stateMachine() {
  let state = 'idle';

  while (true) {
    const action = yield state;

    switch (state) {
      case 'idle':
        if (action === 'START') state = 'running';
        break;
      case 'running':
        if (action === 'PAUSE') state = 'paused';
        if (action === 'STOP') state = 'idle';
        break;
      case 'paused':
        if (action === 'START') state = 'running';
        if (action === 'STOP') state = 'idle';
        break;
    }
  }
}

const machine = stateMachine();
machine.next();           // { value: 'idle', done: false }
machine.next('START');    // { value: 'running', done: false }
machine.next('PAUSE');    // { value: 'paused', done: false }
machine.next('START');    // { value: 'running', done: false }
machine.next('STOP');     // { value: 'idle', done: false }
```

## Real-World Use Cases

### 1. Lazy Data Loading

```typescript
function* loadLargeDataset(): Generator<DataChunk> {
  let offset = 0;
  const batchSize = 1000;

  while (true) {
    const response = await fetch(`/api/data?offset=${offset}&limit=${batchSize}`);
    const data = await response.json();

    if (data.length === 0) break;

    yield data;
    offset += batchSize;
  }
}

// Process data lazily
for (const chunk of loadLargeDataset()) {
  processChunk(chunk);
}
```

### 2. Infinite Sequences

```typescript
function* infiniteCounter(): Generator<number> {
  let i = 0;
  while (true) {
    yield i++;
  }
}

// Use with take
const counter = infiniteCounter();
const first100 = [...take(counter, 100)];
```

### 3. Async/Await Implementation

```typescript
// Generators can implement async/await
async function asyncFn() {
  const data = await fetchData();
  return data;
}

// Equivalent with generators
function* asyncFn() {
  const data = yield fetchData();
  return data;
}

function runGenerator(gen: Generator) {
  return new Promise((resolve, reject) => {
    function step(value?: any) {
      let result: IteratorResult<any>;
      try {
        result = gen.next(value);
      } catch (error) {
        return reject(error);
      }

      if (result.done) {
        return resolve(result.value);
      }

      Promise.resolve(result.value).then(
        (value) => step(value),
        (error) => gen.throw(error)
      );
    }

    step();
  });
}
```

### 4. Custom Iterators

```typescript
class FileSystem {
  *walk(dir: string): Generator<string> {
    const entries = readdirSync(dir);

    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        yield* this.walk(fullPath);
      } else {
        yield fullPath;
      }
    }
  }
}

// Usage
const fs = new FileSystem();
for (const file of fs.walk('/path/to/dir')) {
  console.log(file);
}
```

### 5. Pipeline Processing

```typescript
function* pipeline<T>(
  source: Generator<T>,
  ...transforms: Array<(item: T) => T>
): Generator<T> {
  for (const item of source) {
    let result = item;
    for (const transform of transforms) {
      result = transform(result);
    }
    yield result;
  }
}

// Usage
function* numbers() {
  for (let i = 0; i < 10; i++) {
    yield i;
  }
}

const processed = pipeline(
  numbers(),
  x => x * 2,
  x => x + 1
);

console.log([...processed]);  // [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
```

## Common Mistakes

### 1. Forgetting to Iterate

```typescript
function* myGen() {
  yield 1;
  yield 2;
}

// Bad: Just calling the function
const gen = myGen();  // Returns generator object, doesn't execute

// Good: Iterate over it
for (const value of myGen()) {
  console.log(value);
}
```

### 2. Not Handling Generator Completion

```typescript
function* gen() {
  yield 1;
  yield 2;
  return 3;  // Return value is only available via .next() after last yield
}

const g = gen();
g.next();  // { value: 1, done: false }
g.next();  // { value: 2, done: false }
g.next();  // { value: 3, done: true }
```

### 3. Mixing yield and return

```typescript
// Bad: Confusing control flow
function* gen() {
  yield 1;
  return 2;  // Generator completes here
  yield 3;  // Never reached!
}

// Good: Clear control flow
function* gen() {
  yield 1;
  yield 2;
  yield 3;
}
```

### 4. Not Using yield*

```typescript
// Bad: Manual iteration
function* combined() {
  const gen1 = generator1();
  let result = gen1.next();
  while (!result.done) {
    yield result.value;
    result = gen1.next();
  }
  // Same for gen2
}

// Good: Use yield*
function* combined() {
  yield* generator1();
  yield* generator2();
}
```

## Best Practices

### 1. Use for...of Loop

```typescript
function* myGen() {
  yield 1;
  yield 2;
  yield 3;
}

// Good: for...of automatically handles completion
for (const value of myGen()) {
  console.log(value);
}

// Bad: Manual iteration
const gen = myGen();
let result = gen.next();
while (!result.done) {
  console.log(result.value);
  result = gen.next();
}
```

### 2. Combine Generators

```typescript
// Use yield* for composition
function* allData() {
  yield* fetchData1();
  yield* fetchData2();
  yield* fetchData3();
}
```

### 3. Use TypeScript Generics

```typescript
function* take<T>(gen: Generator<T>, count: number): Generator<T> {
  for (let i = 0; i < count; i++) {
    const { value, done } = gen.next();
    if (done) break;
    yield value;
  }
}
```

### 4. Document Generator Behavior

```typescript
/**
 * Generates fibonacci numbers infinitely
 * @yields Fibonacci numbers starting from 0
 */
function* fibonacci(): Generator<number> {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}
```

## Performance Considerations

### Memory Efficiency

```typescript
// Bad: Eager evaluation
function rangeArray(start: number, end: number): number[] {
  const result = [];
  for (let i = start; i <= end; i++) {
    result.push(i);
  }
  return result;
}

// Good: Lazy evaluation
function* range(start: number, end: number): Generator<number> {
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

// Array uses memory for all values
const arr = rangeArray(1, 1000000);  // Stores all 1M values

// Generator uses memory for one value at a time
const gen = range(1, 1000000);  // Stores nothing until iterated
```

### Time Complexity

```typescript
// Generators don't change time complexity
// But they can reduce space complexity from O(n) to O(1)

// Fibonacci with memoization: O(n) time, O(n) space
function* fibonacciMemo(): Generator<number> {
  const memo = new Map<number, number>();

  function fib(n: number): number {
    if (n <= 1) return n;
    if (memo.has(n)) return memo.get(n)!;
    const result = fib(n - 1) + fib(n - 2);
    memo.set(n, result);
    return result;
  }

  for (let i = 0; ; i++) {
    yield fib(i);
  }
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a generator in JavaScript?**

A: A generator is a special function that can be paused and resumed. It uses `function*` syntax and `yield` to produce values lazily.

**Q2: What is the `yield` keyword?**

A: `yield` pauses generator execution and returns a value. When `.next()` is called again, execution resumes after the `yield`.

**Q3: What does `.next()` return?**

A: `.next()` returns `{ value, done }` where `value` is the yielded value and `done` indicates if the generator is complete.

**Q4: How do you create a generator?**

A: Use `function*` syntax and call the function: `const gen = myGenerator();`

**Q5: What is lazy evaluation?**

A: Lazy evaluation means values are computed only when needed. Generators produce values one at a time on demand.

### Intermediate (5-10 questions)

**Q6: What is the iterator protocol?**

A: An object implements the iterator protocol if it has a `next()` method returning `{ value, done }`. Generators automatically implement this.

**Q7: How do you pass values to a generator?**

A: Pass values to `.next(value)`. The value becomes the result of the `yield` expression the generator is paused at.

**Q8: What is `yield*`?**

A: `yield*` delegates to another generator, iterating over its values and yielding them.

**Q9: How do you create infinite sequences?**

A: Use a `while(true)` loop in the generator, yielding values indefinitely.

**Q10: What is the return value of a generator?**

A: The `return` value is only available when `.next()` is called after the last `yield`, returning `{ value: returnValue, done: true }`.

### Senior (10-15 questions)

**Q11: How do you implement async/await with generators?**

A: Use a runner function that calls `.next()` with resolved promise values and handles `.throw()` for errors.

**Q12: What are async generators?**

A: Async generators use `async function*` and `yield` promises. They're iterated with `for await...of`.

**Q13: How do generators implement iterators?**

A: Generators automatically implement the iterator protocol with `next()`, `return()`, and `throw()` methods.

**Q14: How do you handle errors in generators?**

A: Use `try/catch` inside the generator or call `.throw(error)` to inject errors.

**Q15: What are generator use cases?**

A: Lazy evaluation, infinite sequences, async flows, state machines, custom iterators, pipeline processing.

### FAANG-style (5-10 questions)

**Q16: Design a generator-based task scheduler.**

A: Use generators to yield tasks, implement priority queues, and coordinate async operations.

**Q17: How would you implement coroutines with generators?**

A: Use two generators that pass values to each other via `.next()` and `yield`.

**Q18: Analyze the memory implications of generators vs arrays.**

A: Generators use O(1) space, arrays use O(n). Generators are better for large/infinite sequences.

**Q19: How do you debug generator issues?**

A: Add console.log before/after yields, use try/catch, step through with debugger.

**Q20: What are security implications of generators?**

A: Generators can be used to implement cooperative multitasking, potential for denial of service.

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a generator bug in production?**

A: Infinite generator without proper termination causing memory issues.

**Q22: How do you handle generators in a micro-frontend architecture?**

A: Each micro-frontend can expose generators for data streaming, coordinated via message passing.

**Q23: What is the relationship between generators and observables?**

A: Generators pull values, observables push values. Both represent streams of data.

**Q24: How do different frameworks handle generators?**

A: Redux-Saga uses generators for side effects. MobX uses generators for async actions.

**Q25: What are best practices for working with generators?**

A: Use for...of, combine with yield*, add TypeScript generics, document behavior.

## Summary

Generators are powerful for lazy evaluation:

1. **Syntax**: `function*` and `yield`
2. **Iterator protocol**: `next()`, `return()`, `throw()`
3. **Lazy evaluation**: Produce values on demand
4. **Memory efficient**: O(1) space complexity
5. **Use cases**: Infinite sequences, async flows, state machines
6. **Composition**: Use `yield*` for delegation
7. **Async generators**: `async function*` with `for await...of`

## Cheat Sheet

```
GENERATORS CHEAT SHEET
═══════════════════════════════════════════════════════════════

BASICS:
function* myGen() {
  yield 1;
  yield 2;
  yield 3;
}

const gen = myGen();
gen.next()  // { value: 1, done: false }
gen.next()  // { value: 2, done: false }
gen.next()  // { value: 3, done: false }
gen.next()  // { value: undefined, done: true }

METHODS:
• next(value): Resume, pass value to yield
• return(value): Terminate with value
• throw(error): Inject error

PASSING VALUES:
function* input() {
  const name = yield "What is your name?";
  yield `Hello ${name}`;
}

COMPOSITION:
function* combined() {
  yield* gen1();
  yield* gen2();
}

ITERATOR PROTOCOL:
class Range {
  *[Symbol.iterator]() {
    for (let i = this.start; i <= this.end; i++) {
      yield i;
    }
  }
}

ASYNC GENERATORS:
async function* fetchData() {
  const data = await fetch(url);
  yield data;
}

for await (const item of fetchData()) {
  console.log(item);
}

USE CASES:
• Lazy evaluation
• Infinite sequences
• Async flows
• State machines
• Custom iterators
• Pipeline processing

PERFORMANCE:
• O(1) space vs O(n) for arrays
• Values computed on demand
• Good for large sequences

BEST PRACTICES:
• Use for...of loop
• Combine with yield*
• Add TypeScript generics
• Document behavior
• Handle termination

COMMON MISTAKES:
• Forgetting to iterate
• Not handling completion
• Mixing yield and return
• Not using yield*
```

## References & Learn More

- [MDN: Generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator)
- [JavaScript.info: Generators](https://javascript.info/generators)
- [StackOverflow: Difference between Generators and Iterators](https://stackoverflow.com/questions/34314327/what-is-the-difference-between-iterators-and-generators)
- [TC39: Generators Proposal](https://tc39.es/ecma262/#sec-generator-function-definitions)
