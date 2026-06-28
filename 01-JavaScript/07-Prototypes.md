# Prototypes

## Definition

A **Prototype** is an object from which other objects inherit properties and methods. In JavaScript, every object has a hidden `[[Prototype]]` property that references another object. This creates a **prototype chain** that enables inheritance and property sharing.

## Why Do We Need It?

- **Code Reusability**: Share methods across multiple objects
- **Memory Efficiency**: Methods are defined once, shared by all instances
- **Inheritance**: Create object hierarchies
- **Dynamic Behavior**: Add or modify properties at runtime
- **JavaScript Foundation**: Core of object-oriented programming in JS

## How It Works

### Prototype Chain

```
┌─────────────────────────────────────────────────────────────┐
│                    PROTOTYPE CHAIN                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  OBJECT STRUCTURE:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  const obj = { name: 'Alice' };                    │    │
│  │                                                      │    │
│  │  obj ──────┐                                        │    │
│  │            ▼                                         │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Object.prototype   │                            │    │
│  │  │  • toString()       │                            │    │
│  │  │  • hasOwnProperty() │                            │    │
│  │  │  • valueOf()        │                            │    │
│  │  └─────────────────────┘                            │    │
│  │            │                                         │    │
│  │            ▼                                         │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  null               │                            │    │
│  │  └─────────────────────┘                            │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  PROTOTYPE CHAIN RESOLUTION:                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  1. Check object's own properties                  │    │
│  │  2. Check object's prototype                       │    │
│  │  3. Check prototype's prototype                    │    │
│  │  4. Continue until null (end of chain)             │    │
│  │                                                      │    │
│  │  Example:                                           │    │
│  │  obj.toString()  // Not on obj                     │    │
│  │  → Check obj.__proto__ (Object.prototype)          │    │
│  │  → Found on Object.prototype                       │    │
│  │  → Call Object.prototype.toString()                │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### __proto__ vs prototype

```
┌─────────────────────────────────────────────────────────────┐
│                 __proto__ vs prototype                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  __proto__ (instance property):                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const obj = {};                                    │    │
│  │  console.log(obj.__proto__);  // Object.prototype  │    │
│  │                                                      │    │
│  │  // Every object has __proto__                     │    │
│  │  // It points to the object's prototype            │    │
│  │  // Deprecated, use Object.getPrototypeOf()        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  prototype (function property):                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function Person(name) {                           │    │
│  │    this.name = name;                               │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  console.log(Person.prototype);                    │    │
│  │  // { constructor: Person }                        │    │
│  │                                                      │    │
│  │  // All functions have a prototype property        │    │
│  │  // It's used when creating objects with new       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  RELATIONSHIP:                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  function Person(name) {                           │    │
│  │    this.name = name;                               │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  Person.prototype.greet = function() {             │    │
│  │    return `Hello, ${this.name}`;                   │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  const alice = new Person('Alice');                │    │
│  │                                                      │    │
│  │  alice.__proto__ === Person.prototype  // true     │    │
│  │                                                      │    │
│  │  alice ──────┐                                      │    │
│  │              ▼                                       │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Person.prototype   │                            │    │
│  │  │  • greet()          │                            │    │
│  │  │  • constructor      │                            │    │
│  │  └─────────────────────┘                            │    │
│  │              │                                       │    │
│  │              ▼                                       │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Object.prototype   │                            │    │
│  │  │  • toString()       │                            │    │
│  │  │  • hasOwnProperty() │                            │    │
│  │  └─────────────────────┘                            │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Constructor Functions

```
┌─────────────────────────────────────────────────────────────┐
│                  CONSTRUCTOR FUNCTIONS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  function Person(name, age) {                              │
│    this.name = name;  // Instance property                  │
│    this.age = age;     // Instance property                  │
│  }                                                          │
│                                                              │
│  Person.prototype.greet = function() {                     │
│    return `Hello, I'm ${this.name}`;                       │
│  };                                                          │
│                                                              │
│  const alice = new Person('Alice', 30);                     │
│  const bob = new Person('Bob', 25);                         │
│                                                              │
│  OBJECTS CREATED:                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  alice                    bob                       │    │
│  │  ├─ name: 'Alice'        ├─ name: 'Bob'            │    │
│  │  ├─ age: 30              ├─ age: 25                 │    │
│  │  └─ __proto__ ─────┐     └─ __proto__ ─────┐       │    │
│  │                    ▼                       ▼       │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │           Person.prototype                  │   │    │
│  │  │  • greet()  (shared by all instances)       │   │    │
│  │  │  • constructor: Person                      │   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  MEMORY EFFICIENCY:                                          │
│  • name, age: Stored in each instance                      │
│  • greet(): Stored once in Person.prototype                │
│  • All instances share the same greet() method             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Class-Based Inheritance

```
┌─────────────────────────────────────────────────────────────┐
│                 CLASS-BASED INHERITANCE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  class Animal {                                             │
│    constructor(name: string) {                             │
│      this.name = name;                                     │
│    }                                                        │
│                                                            │
│    speak() {                                               │
│      return `${this.name} makes a sound`;                  │
│    }                                                        │
│  }                                                          │
│                                                              │
│  class Dog extends Animal {                                │
│    speak() {                                               │
│      return `${this.name} barks`;                          │
│    }                                                        │
│  }                                                          │
│                                                              │
│  INHERITANCE CHAIN:                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  const dog = new Dog('Rex');                       │    │
│  │                                                      │    │
│  │  dog ──────┐                                        │    │
│  │            ▼                                         │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Dog.prototype      │                            │    │
│  │  │  • speak()          │                            │    │
│  │  └─────────────────────┘                            │    │
│  │            │                                         │    │
│  │            ▼                                         │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Animal.prototype   │                            │    │
│  │  │  • speak()          │                            │    │
│  │  │  • constructor      │                            │    │
│  │  └─────────────────────┘                            │    │
│  │            │                                         │    │
│  │            ▼                                         │    │
│  │  ┌─────────────────────┐                            │    │
│  │  │  Object.prototype   │                            │    │
│  │  │  • toString()       │                            │    │
│  │  │  • hasOwnProperty() │                            │    │
│  │  └─────────────────────┘                            │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Prototype

```typescript
// Object literal with prototype
const animal = {
  name: 'Animal',
  speak() {
    return `${this.name} makes a sound`;
  }
};

const dog = Object.create(animal);
dog.name = 'Rex';
console.log(dog.speak());  // "Rex makes a sound"

// dog inherits from animal via prototype chain
```

### Constructor Function

```typescript
function Car(brand: string, model: string) {
  this.brand = brand;
  this.model = model;
}

Car.prototype.drive = function() {
  return `${this.brand} ${this.model} is driving`;
};

Car.prototype.toString = function() {
  return `${this.brand} ${this.model}`;
};

const tesla = new Car('Tesla', 'Model 3');
const ford = new Car('Ford', 'Mustang');

console.log(tesla.drive());  // "Tesla Model 3 is driving"
console.log(ford.drive());   // "Ford Mustang is driving"

// Shared method via prototype
console.log(tesla.drive === ford.drive);  // true
```

### hasOwnProperty

```typescript
const person = { name: 'Alice', age: 30 };

console.log(person.hasOwnProperty('name'));     // true
console.log(person.hasOwnProperty('toString')); // false

// hasOwnProperty is on Object.prototype
console.log(Object.prototype.hasOwnProperty.call(person, 'name'));  // true

// Useful for checking own properties
for (const key in person) {
  if (person.hasOwnProperty(key)) {
    console.log(`${key}: ${person[key]}`);
  }
}
```

### Object.create

```typescript
// Create object with specific prototype
const personPrototype = {
  greet() {
    return `Hello, I'm ${this.name}`;
  },
  toString() {
    return `${this.name}`;
  }
};

const person = Object.create(personPrototype);
person.name = 'Alice';

console.log(person.greet());  // "Hello, I'm Alice"
console.log(person.toString());  // "Alice"

// Create object with null prototype
const empty = Object.create(null);
console.log(empty.toString);  // undefined (no Object.prototype)
```

### Inheritance Patterns

```typescript
// Pattern 1: Prototype chaining
function Animal(name: string) {
  this.name = name;
}

Animal.prototype.speak = function() {
  return `${this.name} makes a sound`;
};

function Dog(name: string, breed: string) {
  Animal.call(this, name);  // Call parent constructor
  this.breed = breed;
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
  return `${this.name} barks`;
};

const rex = new Dog('Rex', 'German Shepherd');
console.log(rex.speak());  // "Rex makes a sound" (inherited)
console.log(rex.bark());   // "Rex barks" (own method)

// Pattern 2: Class syntax (syntactic sugar)
class Animal2 {
  constructor(public name: string) {}

  speak() {
    return `${this.name} makes a sound`;
  }
}

class Dog2 extends Animal2 {
  constructor(name: string, public breed: string) {
    super(name);
  }

  bark() {
    return `${this.name} barks`;
  }
}
```

### Prototype Method Override

```typescript
class Rectangle {
  constructor(public width: number, public height: number) {}

  area() {
    return this.width * this.height;
  }

  toString() {
    return `Rectangle(${this.width}x${this.height})`;
  }
}

class Square extends Rectangle {
  constructor(size: number) {
    super(size, size);
  }

  // Override toString
  toString() {
    return `Square(${this.width})`;
  }
}

const rect = new Rectangle(5, 10);
const square = new Square(5);

console.log(rect.toString());    // "Rectangle(5x10)"
console.log(square.toString());  // "Square(5)"
console.log(rect.area());        // 50
console.log(square.area());      // 25
```

### Prototype Inspection

```typescript
const obj = { name: 'Alice' };

// Get prototype
const proto = Object.getPrototypeOf(obj);
console.log(proto === Object.prototype);  // true

// Check prototype chain
console.log(obj instanceof Object);  // true
console.log(obj.__proto__ === Object.prototype);  // true

// List all methods in prototype chain
function getPrototypeMethods(obj: any): string[] {
  const methods: string[] = [];
  let current = obj;

  while (current !== null) {
    methods.push(...Object.getOwnPropertyNames(current)
      .filter(name => typeof current[name] === 'function'));
    current = Object.getPrototypeOf(current);
  }

  return methods;
}

console.log(getPrototypeMethods(obj));
// ['constructor', 'toString', 'valueOf', 'hasOwnProperty', ...]
```

## Real-World Use Cases

### 1. Array Methods via Prototype

```typescript
// Custom array-like object with prototype methods
function createArrayList() {
  const list: any[] = [];

  // Add array methods via prototype
  list.push = Array.prototype.push;
  list.pop = Array.prototype.pop;
  list.forEach = Array.prototype.forEach;
  list.map = Array.prototype.map;

  return list;
}

const myList = createArrayList();
myList.push(1);
myList.push(2);
myList.push(3);

console.log(myList.map((x: number) => x * 2));  // [2, 4, 6]
```

### 2. Mixin Pattern

```typescript
// Mixin for loggable objects
const Loggable = {
  log(message: string) {
    console.log(`[${this.constructor.name}] ${message}`);
  },

  warn(message: string) {
    console.warn(`[${this.constructor.name}] ${message}`);
  },

  error(message: string) {
    console.error(`[${this.constructor.name}] ${message}`);
  }
};

// Mixin for serializable objects
const Serializable = {
  serialize() {
    return JSON.stringify(this);
  },

  deserialize(json: string) {
    return Object.assign(this, JSON.parse(json));
  }
};

// Apply mixins to class
class UserService {
  users: any[] = [];

  constructor() {
    Object.assign(this, Loggable, Serializable);
  }

  addUser(user: any) {
    this.users.push(user);
    this.log(`Added user: ${user.name}`);
  }
}

const service = new UserService();
service.addUser({ name: 'Alice' });
console.log(service.serialize());
```

### 3. Plugin System

```typescript
// Base plugin class
class Plugin {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  init() {
    console.log(`Initializing ${this.name}`);
  }

  destroy() {
    console.log(`Destroying ${this.name}`);
  }
}

// Plugin manager uses prototype chain
class PluginManager {
  private plugins: Plugin[] = [];

  register(plugin: Plugin) {
    this.plugins.push(plugin);
    plugin.init();
  }

  unregister(name: string) {
    const index = this.plugins.findIndex(p => p.name === name);
    if (index > -1) {
      this.plugins[index].destroy();
      this.plugins.splice(index, 1);
    }
  }
}
```

### 4. Event Emitter

```typescript
class EventEmitter {
  private listeners: Map<string, Function[]> = new Map();

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
    return this;
  }

  off(event: string, callback: Function) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
    return this;
  }

  emit(event: string, ...args: any[]) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(cb => cb(...args));
    }
    return this;
  }
}

// Usage
class Logger extends EventEmitter {
  log(message: string) {
    console.log(message);
    this.emit('log', message);
  }
}

const logger = new Logger();
logger.on('log', (msg: string) => console.log(`Listener: ${msg}`));
logger.log('Hello');  // Triggers listener
```

## Common Mistakes

### 1. Overwriting Prototype

```typescript
// Bad: Overwrites entire prototype
function Person(name: string) {
  this.name = name;
}

Person.prototype = {
  greet() {
    return `Hello, ${this.name}`;
  }
};

// Loses constructor property!
console.log(Person.prototype.constructor === Person);  // false

// Good: Add methods individually
function PersonFixed(name: string) {
  this.name = name;
}

PersonFixed.prototype.greet = function() {
  return `Hello, ${this.name}`;
};

console.log(PersonFixed.prototype.constructor === PersonFixed);  // true
```

### 2. Modifying Built-in Prototypes

```typescript
// Bad: Modifying Array.prototype
Array.prototype.last = function() {
  return this[this.length - 1];
};

// Can break third-party code
// Can cause conflicts with future JS features

// Good: Use utility functions
function last<T>(arr: T[]): T | undefined {
  return arr[arr.length - 1];
}
```

### 3. Confusing __proto__ and prototype

```typescript
function Person(name: string) {
  this.name = name;
}

const alice = new Person('Alice');

// __proto__ is on instances
console.log(alice.__proto__ === Person.prototype);  // true

// prototype is on functions
console.log(Person.prototype);  // { constructor: Person }

// Don't use __proto__ directly
// Use Object.getPrototypeOf() instead
console.log(Object.getPrototypeOf(alice) === Person.prototype);  // true
```

### 4. Forgetting to Call super()

```typescript
class Animal {
  constructor(public name: string) {}
}

class Dog extends Animal {
  constructor(name: string, public breed: string) {
    // Bad: Forgetting super()
    // this.breed = breed;  // ReferenceError!

    // Good: Call super first
    super(name);
    this.breed = breed;
  }
}
```

## Best Practices

### 1. Use Class Syntax

```typescript
// Modern: Class syntax
class Person {
  constructor(public name: string) {}

  greet() {
    return `Hello, ${this.name}`;
  }
}

// Legacy: Constructor function
function PersonLegacy(name: string) {
  this.name = name;
}

PersonLegacy.prototype.greet = function() {
  return `Hello, ${this.name}`;
};
```

### 2. Prefer Composition Over Inheritance

```typescript
// Inheritance
class Animal {
  constructor(public name: string) {}
  speak() { return `${this.name} makes a sound`; }
}

class Dog extends Animal {
  speak() { return `${this.name} barks`; }
}

// Composition
class Animal2 {
  constructor(public name: string, public sound: string) {}
  speak() { return `${this.name} ${this.sound}`; }
}

const dog = new Animal2('Rex', 'barks');
const cat = new Animal2('Whiskers', 'meows');
```

### 3. Freeze Prototypes When Needed

```typescript
// Prevent modifications
const frozenObj = Object.freeze({
  method() { return 'frozen'; }
});

// Or freeze entire prototype
Object.freeze(Array.prototype);
```

### 4. Use TypeScript Interfaces

```typescript
interface Speakable {
  speak(): string;
}

interface Nammable {
  name: string;
}

class Dog implements Speakable, Nammable {
  constructor(public name: string) {}

  speak() {
    return `${this.name} barks`;
  }
}
```

## Performance Considerations

### Prototype Lookup

```typescript
// Property lookup traverses prototype chain
const obj = { a: 1 };

// Add many prototype levels
let current = obj;
for (let i = 0; i < 100; i++) {
  current.__proto__ = { level: i };
}

// Lookup is slower with deep chains
console.log(current.level);  // Traverses 100 prototypes

// Better: Keep prototype chains shallow
```

### Method Sharing

```typescript
// Bad: Methods on instances (not shared)
function Person(name: string) {
  this.name = name;
  this.greet = function() {  // New function for each instance
    return `Hello, ${this.name}`;
  };
}

// Good: Methods on prototype (shared)
function PersonFixed(name: string) {
  this.name = name;
}

PersonFixed.prototype.greet = function() {  // Shared by all instances
  return `Hello, ${this.name}`;
};
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a prototype in JavaScript?**

A: A prototype is an object from which other objects inherit properties and methods. Every object has a hidden `[[Prototype]]` property that references another object, creating a prototype chain.

**Q2: What is the prototype chain?**

A: The prototype chain is a series of objects linked by their prototype references. When you access a property, JavaScript looks up the chain until it finds the property or reaches null.

**Q3: What is the difference between `__proto__` and `prototype`?**

A:
- `__proto__`: Property on every object that points to its prototype (deprecated, use `Object.getPrototypeOf()`)
- `prototype`: Property on functions that becomes the prototype of objects created with `new`

**Q4: What is `hasOwnProperty`?**

A: `hasOwnProperty` is a method on `Object.prototype` that checks if an object has a property directly (not inherited from prototype).

**Q5: What is `Object.create`?**

A: `Object.create` creates a new object with a specified prototype. It's used to create objects with custom prototypes without using constructors.

### Intermediate (5-10 questions)

**Q6: How do you implement inheritance in JavaScript?**

A: Several ways:
1. Prototype chaining: `Dog.prototype = Object.create(Animal.prototype)`
2. ES6 classes: `class Dog extends Animal`
3. Constructor stealing: `Animal.call(this, name)`
4. Mixins: `Object.assign(Dog.prototype, animalMethods)`

**Q7: What is the `constructor` property?**

A: The `constructor` property is a reference to the function that created the object. It's automatically added to the prototype when a function is created.

**Q8: How do you properly set up prototype inheritance?**

A:
```typescript
function Child() {
  Parent.call(this);  // Call parent constructor
}
Child.prototype = Object.create(Parent.prototype);
Child.prototype.constructor = Child;  // Fix constructor
```

**Q9: What is method overriding?**

A: Method overriding is when a child class provides a different implementation of a method that exists in its parent class. The child's method takes precedence in the prototype chain.

**Q10: How do you check if an object is an instance of a class?**

A: Use the `instanceof` operator:
```typescript
const dog = new Dog('Rex');
console.log(dog instanceof Dog);     // true
console.log(dog instanceof Animal);  // true
```

### Senior (10-15 questions)

**Q11: Explain the relationship between prototypes and closures.**

A: Closures capture the lexical scope, which includes access to prototypes. Methods defined in constructors can access prototype methods through the scope chain.

**Q12: What are the performance implications of deep prototype chains?**

A: Deep chains increase property lookup time. Each level adds another reference to traverse. Keep chains shallow for better performance.

**Q13: How do JavaScript engines optimize prototype lookups?**

A: Engines use hidden classes, inline caching, and JIT compilation to speed up property access. They create hidden classes for objects with the same shape and cache property locations.

**Q14: What is the difference between prototypal and classical inheritance?**

A:
- **Prototypal**: Objects inherit directly from other objects via prototype chain
- **Classical**: Classes are blueprints, instances are created from classes

JavaScript uses prototypal inheritance, with classes as syntactic sugar.

**Q15: How do you implement multiple inheritance in JavaScript?**

A: JavaScript doesn't support multiple inheritance directly. Use mixins:
```typescript
const Serializable = { serialize() {} };
const Loggable = { log() {} };

class MyClass extends BaseClass {
  constructor() {
    super();
    Object.assign(this, Serializable, Loggable);
  }
}
```

### FAANG-style (5-10 questions)

**Q16: Design a prototype-based object system.**

A:
```typescript
class PrototypeSystem {
  private prototypes = new Map<string, any>();

  create(name: string, properties: any) {
    this.prototypes.set(name, properties);
  }

  clone(name: string) {
    const proto = this.prototypes.get(name);
    if (!proto) throw new Error(`Prototype ${name} not found`);

    const clone = Object.create(proto);
    Object.assign(clone, { _proto: name });
    return clone;
  }

  extend(name: string, parentName: string, extraProperties: any) {
    const parent = this.prototypes.get(parentName);
    if (!parent) throw new Error(`Parent ${parentName} not found`);

    const child = Object.create(parent);
    Object.assign(child, extraProperties);
    this.prototypes.set(name, child);
  }
}
```

**Q17: How would you implement a class system without using classes?**

A:
```typescript
function createClass(constructor: Function, methods: any) {
  const proto = Object.create(null);

  Object.keys(methods).forEach(key => {
    proto[key] = methods[key];
  });

  proto.constructor = constructor;

  return function(...args: any[]) {
    const instance = Object.create(proto);
    constructor.apply(instance, args);
    return instance;
  };
}

const Person = createClass(
  function(name: string) {
    this.name = name;
  },
  {
    greet() {
      return `Hello, ${this.name}`;
    }
  }
);

const alice = Person('Alice');
console.log(alice.greet());  // "Hello, Alice"
```

**Q18: Analyze the memory usage of prototype-based inheritance.**

A:
- **Shared methods**: One copy per prototype, not per instance
- **Instance properties**: One copy per instance
- **Prototype chain**: Each level adds a reference
- **Hidden classes**: Engines optimize by sharing class structures

Memory efficient: Methods are shared. Each instance only stores unique properties.

**Q19: How do you handle prototype pollution attacks?**

A:
1. Use `Object.freeze` to prevent modifications
2. Use `Object.create(null)` for objects without prototype
3. Validate input before adding to prototypes
4. Use hasOwnProperty checks
5. Avoid modifying built-in prototypes

**Q20: What are the security implications of prototype pollution?**

A:
1. **Prototype pollution**: Malicious code can modify Object.prototype
2. **Property injection**: Attackers can inject properties
3. **Privilege escalation**: Can modify security-related properties
4. **Mitigation**: Input validation, freezing prototypes, using null prototypes

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a prototype-related bug in production?**

A: Common bug:
```typescript
// Bug: Modifying Object.prototype
Object.prototype.isEmpty = function() {
  return Object.keys(this).length === 0;
};

// Third-party library breaks
const config = {};
console.log(config.isEmpty());  // true
console.log({ a: 1 }.isEmpty());  // false

// Fix: Don't modify built-in prototypes
// Use utility functions instead
```

**Q22: How do you debug prototype-related issues?**

A:
1. **Chrome DevTools**: Inspect prototype chain in debugger
2. **console.log**: Log `Object.getPrototypeOf(obj)`
3. **instanceof**: Check prototype chain membership
4. **hasOwnProperty**: Distinguish own vs inherited properties
5. **TypeScript**: Type checking prevents many issues

**Q23: What is the relationship between prototypes and TypeScript?**

A: TypeScript compiles to JavaScript, using prototypes under the hood. Classes in TypeScript are syntactic sugar over prototype-based inheritance. TypeScript adds type checking but doesn't change runtime behavior.

**Q24: How do frameworks use prototypes?**

A:
- **React**: Class components use prototype methods
- **Vue**: Options API uses prototype for methods
- **Angular**: Dependency injection via prototypes
- **jQuery**: All methods defined on prototype

**Q25: What are best practices for working with prototypes?**

A:
1. Use class syntax for clarity
2. Prefer composition over inheritance
3. Keep prototype chains shallow
4. Don't modify built-in prototypes
5. Use TypeScript for type safety
6. Freeze prototypes when needed
7. Use Object.create(null) for dictionaries
8. Document prototype behavior

## Summary

Prototypes are fundamental to JavaScript:

1. **Definition**: Objects inherit from other objects via prototype chain
2. **__proto__ vs prototype**: Instance reference vs function property
3. **Constructor functions**: Create objects with shared methods
4. **Class syntax**: Modern way to work with prototypes
5. **Inheritance**: Enable code reuse and hierarchies
6. **Performance**: Shared methods, shallow chains preferred
7. **Best practices**: Use classes, prefer composition, freeze when needed

Understanding prototypes is essential for mastering JavaScript and answering interview questions.

## Cheat Sheet

```
PROTOTYPES CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT IS A PROTOTYPE?
• Object from which others inherit properties/methods
• Every object has [[Prototype]] reference
• Creates prototype chain for inheritance

__proto__ vs prototype:
• __proto__: On instances, points to prototype (deprecated)
• prototype: On functions, becomes prototype of new objects

PROTOTYPE CHAIN:
• Object → Object.prototype → null
• Property lookup traverses the chain
• Ends at null

CONSTRUCTOR FUNCTIONS:
function Person(name) { this.name = name; }
Person.prototype.greet = function() { return this.name; };
const p = new Person('Alice');

CLASS SYNTAX (modern):
class Person {
  constructor(name) { this.name = name; }
  greet() { return this.name; }
}

INHERITANCE:
class Dog extends Animal {
  constructor(name) {
    super(name);
  }
}

KEY METHODS:
• Object.create(proto): Create object with prototype
• Object.getPrototypeOf(obj): Get prototype
• hasOwnProperty(): Check own properties
• instanceof: Check prototype chain

MEMORY:
• Shared methods via prototype (efficient)
• Instance properties per object
• Keep chains shallow for performance

BEST PRACTICES:
• Use class syntax
• Prefer composition over inheritance
• Don't modify built-in prototypes
• Freeze prototypes when needed
• Use TypeScript for type safety

COMMON MISTAKES:
• Overwriting entire prototype
• Modifying Object.prototype
• Forgetting super() in constructors
• Confusing __proto__ and prototype

DEBUGGING:
• Chrome DevTools: Prototype chain inspection
• Object.getPrototypeOf(): Check prototype
• instanceof: Check chain membership
• hasOwnProperty(): Distinguish own vs inherited
```

## References & Learn More

- [MDN: Inheritance & the Prototype Chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
- [JavaScript.info: Prototypal Inheritance](https://javascript.info/prototype-inheritance)
- [Udacity: Prototypes & Inheritance](https://www.udacity.com/blog/prototypal-inheritance-in-javascript-object-oriented-programming--h1d45740e8bf)
- [MDN: Object.create()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create)
