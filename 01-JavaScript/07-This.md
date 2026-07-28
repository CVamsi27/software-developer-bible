# This

[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

 is currently executing the code. Its value depends on how a function is called (execution context), not where it's defined. This is called **dynamic binding** or **dynamic scoping** of `this`.

## Why Do We Need It?

- **Object Methods**: Reference the object a method belongs to
- **Constructor Functions**: Initialize object properties
- **Event Handlers**: Access the element that triggered the event
- **Function Reusability**: Same function can work with different objects
- **OOP Patterns**: Enable object-oriented programming in JavaScript

## How It Works

### Binding Rules

```text
┌─────────────────────────────────────────────────────────────┐
│                    THIS BINDING RULES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  RULE 1: DEFAULT BINDING                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function greet() {                                │    │
│  │    console.log(this);                              │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  greet();  // window (non-strict) or undefined     │    │
│  │                                                      │    │
│  │  // When function is called without context        │    │
│  │  // 'this' defaults to global object               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  RULE 2: IMPLICIT BINDING                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const obj = {                                     │    │
│  │    name: 'Alice',                                  │    │
│  │    greet() {                                       │    │
│  │      console.log(this.name);                       │    │
│  │    }                                                │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  obj.greet();  // 'Alice' (this = obj)            │    │
│  │                                                      │    │
│  │  // When method is called on object               │    │
│  │  // 'this' refers to the object                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  RULE 3: EXPLICIT BINDING                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function greet() {                                │    │
│  │    console.log(this.name);                         │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const obj = { name: 'Alice' };                   │    │
│  │                                                      │    │
│  │  greet.call(obj);   // 'Alice'                     │    │
│  │  greet.apply(obj);  // 'Alice'                     │    │
│  │  const bound = greet.bind(obj);                    │    │
│  │  bound();           // 'Alice'                     │    │
│  │                                                      │    │
│  │  // call, apply, bind explicitly set 'this'        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  RULE 4: ARROW FUNCTION                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const obj = {                                     │    │
│  │    name: 'Alice',                                  │    │
│  │    greet: () => {                                  │    │
│  │      console.log(this.name);                       │    │
│  │    }                                                │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  obj.greet();  // undefined (this = window)       │    │
│  │                                                      │    │
│  │  // Arrow functions inherit 'this' from parent    │    │
│  │  // They don't have their own 'this'              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### this in Different Contexts

```text
┌─────────────────────────────────────────────────────────────┐
│                  THIS IN DIFFERENT CONTEXTS                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GLOBAL CONTEXT:                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  console.log(this);  // window (browser)           │    │
│  │  console.log(this);  // global (Node.js)           │    │
│  │                                                      │    │
│  │  // In strict mode:                                │    │
│  │  'use strict';                                     │    │
│  │  console.log(this);  // undefined                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  FUNCTION CONTEXT:                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function standalone() {                           │    │
│  │    console.log(this);                              │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  standalone();  // window (non-strict)             │    │
│  │                                                      │    │
│  │  'use strict';                                     │    │
│  │  function strict() {                               │    │
│  │    console.log(this);  // undefined                │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  OBJECT METHOD:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const obj = {                                     │    │
│  │    name: 'Alice',                                  │    │
│  │    greet() {                                       │    │
│  │      console.log(this);  // obj                    │    │
│  │    }                                                │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  obj.greet();  // obj                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  CONSTRUCTOR:                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function Person(name) {                           │    │
│  │    this.name = name;                               │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const alice = new Person('Alice');                │    │
│  │  console.log(alice.name);  // 'Alice'             │    │
│  │                                                      │    │
│  │  // 'this' refers to new object being created     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  EVENT HANDLER:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  button.addEventListener('click', function() {    │    │
│  │    console.log(this);  // button element           │    │
│  │  });                                                │    │
│  │                                                      │    │
│  │  button.addEventListener('click', () => {         │    │
│  │    console.log(this);  // window (arrow function) │    │
│  │  });                                                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### call, apply, bind

```text
┌─────────────────────────────────────────────────────────────┐
│                   CALL, APPLY, BIND                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CALL:                                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function greet(greeting) {                        │    │
│  │    return `${greeting}, ${this.name}!`;            │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const alice = { name: 'Alice' };                 │    │
│  │  const bob = { name: 'Bob' };                     │    │
│  │                                                      │    │
│  │  greet.call(alice, 'Hello');  // 'Hello, Alice!'  │    │
│  │  greet.call(bob, 'Hi');       // 'Hi, Bob!'       │    │
│  │                                                      │    │
│  │  // Arguments passed individually                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  APPLY:                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function greet(greeting, punctuation) {           │    │
│  │    return `${greeting}, ${this.name}${punctuation}`│    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const alice = { name: 'Alice' };                 │    │
│  │                                                      │    │
│  │  greet.apply(alice, ['Hello', '!']);               │    │
│  │  // 'Hello, Alice!'                                │    │
│  │                                                      │    │
│  │  // Arguments passed as array                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  BIND:                                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function greet() {                                │    │
│  │    return `Hello, ${this.name}!`;                  │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const alice = { name: 'Alice' };                 │    │
│  │  const greetAlice = greet.bind(alice);             │    │
│  │                                                      │    │
│  │  greetAlice();  // 'Hello, Alice!'                │    │
│  │                                                      │    │
│  │  // Returns new function with 'this' bound        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic this Usage

```typescript
const person = {
  name: 'Alice',
  greet() {
    console.log(`Hello, ${this.name}`);
  }
};

person.greet();  // "Hello, Alice"

// 'this' refers to 'person' object
// because greet() is called on person

```

### this in Constructor

```typescript
class Person {
  name: string;

  constructor(name: string) {
    this.name = name;  // 'this' = new object
  }

  greet() {
    console.log(`Hello, ${this.name}`);
  }
}

const alice = new Person('Alice');
alice.greet();  // "Hello, Alice"

```

### Arrow Function this

```typescript
const obj = {
  name: 'Alice',

  // Regular function: 'this' = obj
  greetRegular() {
    console.log(this.name);  // 'Alice'
  },

  // Arrow function: 'this' = parent scope
  greetArrow: () => {
    console.log(this.name);  // undefined (window)
  }
};

obj.greetRegular();  // 'Alice'
obj.greetArrow();    // undefined

// Arrow functions don't have their own 'this'
// They inherit from enclosing lexical scope

```

### Event Handler this

```typescript
const button = document.getElementById('myButton');

// Regular function: 'this' = button element
button?.addEventListener('click', function() {
  console.log(this);  // <button id="myButton">
  this.style.color = 'red';  // Works!
});

// Arrow function: 'this' = parent scope (window)
button?.addEventListener('click', () => {
  console.log(this);  // window
  // this.style.color = 'red';  // Error!
});

```

### call, apply, bind Examples

```typescript
function greet(greeting: string, punctuation: string) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const alice = { name: 'Alice' };
const bob = { name: 'Bob' };

// call: pass arguments individually
console.log(greet.call(alice, 'Hello', '!'));  // "Hello, Alice!"

// apply: pass arguments as array
console.log(greet.apply(bob, ['Hi', '.']));  // "Hi, Bob."

// bind: return new function with 'this' bound
const greetAlice = greet.bind(alice);
console.log(greetAlice('Hey', '?'));  // "Hey, Alice?"

// bind with partial application
const greetAliceHey = greet.bind(alice, 'Hey');
console.log(greetAliceHey('!'));  // "Hey, Alice!"

```

### this in Loops

```typescript
const obj = {
  name: 'Alice',
  items: [1, 2, 3],

  // Problem: 'this' lost in callback
  processItemsBad() {
    this.items.forEach(function(item) {
      console.log(this.name);  // undefined (window)
    });
  },

  // Solution 1: Arrow function
  processItemsGood1() {
    this.items.forEach((item) => {
      console.log(this.name);  // 'Alice'
    });
  },

  // Solution 2: bind
  processItemsGood2() {
    this.items.forEach(function(item) {
      console.log(this.name);  // 'Alice'
    }.bind(this));
  }
};

```

### this in Class Methods

```typescript
class Counter {
  private count = 0;

  increment() {
    this.count++;
    return this;  // Enable chaining
  }

  decrement() {
    this.count--;
    return this;
  }

  getCount() {
    return this.count;
  }
}

const counter = new Counter();
counter.increment().increment().increment();
console.log(counter.getCount());  // 3

```

### this in React

```typescript
import React, { Component } from 'react';

class MyComponent extends Component {
  state = { count: 0 };

  // Arrow function: 'this' = component instance
  handleClick = () => {
    this.setState({ count: this.state.count + 1 });
  };

  // Regular function: need to bind in constructor
  handleClickBound() {
    this.setState({ count: this.state.count + 1 });
  }

  constructor(props: any) {
    super(props);
    this.handleClickBound = this.handleClickBound.bind(this);
  }

  render() {
    return (
      <button onClick={this.handleClick}>
        Count: {this.state.count}
      </button>
    );
  }
}

```

## Real-World Use Cases

### 1. Method Chaining

```typescript
class QueryBuilder {
  private table: string = '';
  private conditions: string[] = [];
  private limitCount: number = 0;

  from(table: string) {
    this.table = table;
    return this;  // Return 'this' for chaining
  }

  where(condition: string) {
    this.conditions.push(condition);
    return this;
  }

  limit(count: number) {
    this.limitCount = count;
    return this;
  }

  build() {
    let query = `SELECT * FROM ${this.table}`;
    if (this.conditions.length) {
      query += ` WHERE ${this.conditions.join(' AND ')}`;
    }
    if (this.limitCount) {
      query += ` LIMIT ${this.limitCount}`;
    }
    return query;
  }
}

const query = new QueryBuilder()
  .from('users')
  .where('age > 18')
  .where('active = true')
  .limit(10)
  .build();

console.log(query);  // "SELECT * FROM users WHERE age > 18 AND active = true LIMIT 10"

```

### 2. Event Delegation

```typescript
function setupEventDelegation(container: HTMLElement) {
  container.addEventListener('click', function(event) {
    const target = event.target as HTMLElement;

    // 'this' = container element
    if (target.matches('.delete-btn')) {
      const id = target.dataset.id;
      deleteItem(id);
    } else if (target.matches('.edit-btn')) {
      const id = target.dataset.id;
      editItem(id);
    }
  });
}

```

### 3. Object Pool Pattern

```typescript
class ObjectPool<T> {
  private pool: T[] = [];
  private factory: () => T;

  constructor(factory: () => T, initialSize: number = 10) {
    this.factory = factory;
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(factory());
    }
  }

  acquire(): T {
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }
    return this.factory();
  }

  release(obj: T) {
    this.pool.push(obj);
  }
}

const pool = new ObjectPool(() => ({ x: 0, y: 0 }));
const obj = pool.acquire();
obj.x = 10;
pool.release(obj);

```

### 4. Decorator Pattern

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;

  return function(this: any, ...args: Parameters<T>) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

function handleSearch(query: string) {
  console.log(`Searching: ${query}`);
}

const debouncedSearch = debounce(handleSearch, 300);

```

## Common Mistakes

### 1. Losing this in Callbacks

```typescript
class Timer {
  seconds = 0;

  // Bad: 'this' lost in callback
  startBad() {
    setInterval(function() {
      this.seconds++;  // this = window, not Timer
    }, 1000);
  }

  // Good: Arrow function
  startGood() {
    setInterval(() => {
      this.seconds++;  // this = Timer instance
    }, 1000);
  }

  // Good: bind
  startBound() {
    setInterval(function() {
      this.seconds++;
    }.bind(this), 1000);
  }
}

```

### 2. Arrow Functions as Object Methods

```typescript
const obj = {
  name: 'Alice',

  // Bad: Arrow function doesn't have own 'this'
  greet: () => {
    console.log(this.name);  // undefined
  },

  // Good: Regular function
  greetGood() {
    console.log(this.name);  // 'Alice'
  }
};

obj.greet();      // undefined
obj.greetGood();  // 'Alice'

```

### 3. Forgetting to Bind in Constructor

```typescript
class Component {
  constructor() {
    // Bad: 'this' not bound
    // this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    console.log(this);
  }
}

// When passed as callback, 'this' is lost
const component = new Component();
button.addEventListener('click', component.handleClick);  // this = button

```

### 4. this in Nested Functions

```typescript
const obj = {
  name: 'Alice',
  outer() {
    // 'this' = obj
    function inner() {
      // 'this' = window (not obj!)
      console.log(this.name);
    }
    inner();
  }
};

obj.outer();  // undefined

// Fix: Use arrow function
const obj2 = {
  name: 'Alice',
  outer() {
    const inner = () => {
      console.log(this.name);  // 'Alice'
    };
    inner();
  }
};

```

## Best Practices

### 1. Use Arrow Functions for Callbacks

```typescript
class Component {
  items = [1, 2, 3];

  processItems() {
    // Arrow function inherits 'this'
    this.items.forEach(item => {
      console.log(this);  // Component instance
    });
  }
}

```

### 2. Bind Methods in Constructor

```typescript
class Component {
  constructor() {
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    console.log(this);
  }
}

```

### 3. Use Explicit Parameters Instead of this

```typescript
// Bad: Relies on 'this'
function processUser() {
  console.log(this.name);
}

// Good: Explicit parameter
function processUser(user: { name: string }) {
  console.log(user.name);
}

```

### 4. Document this Behavior

```typescript
/**

 - Processes the item.
 - @this {Product} The product being processed
 */
function processItem(this: Product, quantity: number) {
  this.stock -= quantity;
}

```

## Performance Considerations

### Method Binding

```typescript
// Bad: Binding in render (creates new function each time)
class Component extends React.Component {
  render() {
    return (
      <button onClick={this.handleClick.bind(this)}>
        Click
      </button>
    );
  }
}

// Good: Bind in constructor or use arrow function
class Component extends React.Component {
  constructor(props: any) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  render() {
    return (
      <button onClick={this.handleClick}>
        Click
      </button>
    );
  }
}

```

### Arrow Function Performance

```typescript
// Arrow functions are slightly slower than regular functions
// because they don't have their own 'this'
// Use regular functions for methods, arrows for callbacks

const obj = {
  // Regular function: faster
  method() { return this; },

  // Arrow function: slower, but useful for callbacks
  callback: () => this
};

```

## Summary

`this` is a powerful but confusing JavaScript feature:

1. **Dynamic binding**: Value depends on how function is called

2. **Four rules**: Default, implicit, explicit, arrow function

3. **call/apply/bind**: Explicit control over `this`

4. **Arrow functions**: Inherit `this` from lexical scope

5. **Common issues**: Lost `this` in callbacks

6. **Solutions**: Arrow functions, bind, explicit parameters

7. **Best practices**: Use arrows for callbacks, bind in constructor

Understanding `this` is essential for writing clean, maintainable JavaScript and answering interview questions.

## Cheat Sheet
```text
THIS CHEAT SHEET
═══════════════════════════════════════════════════════════════

BINDING RULES (in order):

1. new binding: new Foo() → this = new object

2. Explicit: call/apply/bind → this = specified

3. Implicit: obj.method() → this = obj

4. Default: func() → this = global/undefined

COMMON PATTERNS:

// Method (implicit binding)
const obj = { name: 'Alice', greet() { return this.name; } };
obj.greet();  // 'Alice'

// Constructor (new binding)
function Person(name) { this.name = name; }
const p = new Person('Alice');

// Explicit binding
greet.call(alice, 'Hello');
greet.apply(alice, ['Hello']);
const bound = greet.bind(alice);

// Arrow function (lexical this)
const obj = { greet: () => this.name };  // this = parent scope

LOST THIS FIXES:

// 1. Arrow function
button.addEventListener('click', () => this.handleClick());

// 2. bind
button.addEventListener('click', this.handleClick.bind(this));

// 3. Store reference
const self = this;
button.addEventListener('click', function() { self.handleClick(); });

// 4. call/apply
func.call(context, ...args);

BEST PRACTICES:
• Use arrow functions for callbacks
• Bind methods in constructor
• Use TypeScript this parameter
• Document this behavior
• Prefer functional components

COMMON MISTAKES:
• Arrow functions as object methods
• Forgetting to bind in constructor
• this in nested functions
• this in loops

DEBUGGING:
• console.log(this)
• Chrome DevTools Scope panel
• TypeScript this parameter
• ESLint rules

```

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Node.js](../05-NodeJS/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [MDN: this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)
- [JavaScript.info: Binding Functions](https://web.archive.org/web/20240701000000/https://javascript.info/bind-apply-call)
- [FreeCodeCamp: Understand the this Keyword](https://www.freecodecamp.org/news/what-is-this-in-javascript/)
- [JavaScript.info: Arrow Functions & this](https://javascript.info/arrow-functions)
