# Builder Pattern

## Definition

The Builder pattern is a creational design pattern that separates the construction of a complex object from its representation. It allows you to produce different types and representations of an object using the same construction code.

The pattern is particularly useful when you need to create an object with many optional parameters or when the construction process involves multiple steps.

## Why Do We Need It?

Without the Builder pattern, object creation can be problematic:

1. **Telescoping constructors**: Too many constructor parameters

2. **Complex initialization**: Multiple steps needed to create an object

3. **Immutable objects**: Difficult to create immutable objects with many fields

4. **Readability**: Constructor calls with many parameters are hard to read

## How It Works

The Builder pattern works by:

1. Creating a separate builder class for constructing objects

2. Providing step-by-step methods for building the object

3. Allowing the same construction process to create different representations

4. Providing a final build method that returns the constructed object

```text
┌─────────────────────────────────────────────────┐
│              Builder Pattern                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │                               │
│  └──────────────┘                               │
│         │                                       │
│         │ uses                                  │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Builder Interface                │   │
│  │    + setPartA(): Builder                 │   │
│  │    + setPartB(): Builder                 │   │
│  │    + build(): Product                    │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┐                                 │
│    ▼         ▼                                 │
│ ┌──────┐ ┌──────┐                             │
│ │Build1│ │Build2│                             │
│ └──────┘ └──────┘                             │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Product                          │   │
│  │    Complex object with many parts        │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘

```

## Code Examples

### Basic Builder Pattern

```typescript
// Product
class House {
  constructor(
    public foundation: string,
    public structure: string,
    public roof: string,
    public interior: string,
    public garden: string,
    public garage: string
  ) {}

  toString(): string {
    return `
House:
  Foundation: ${this.foundation}
  Structure: ${this.structure}
  Roof: ${this.roof}
  Interior: ${this.interior}
  Garden: ${this.garden}
  Garage: ${this.garage}
    `.trim();
  }
}

// Builder interface
interface HouseBuilder {
  buildFoundation(): HouseBuilder;
  buildStructure(): HouseBuilder;
  buildRoof(): HouseBuilder;
  buildInterior(): HouseBuilder;
  buildGarden(): HouseBuilder;
  buildGarage(): HouseBuilder;
  getResult(): House;
}

// Concrete builder
class ConcreteHouseBuilder implements HouseBuilder {
  private house: House;

  constructor() {
    this.house = new House('', '', '', '', '', '');
  }

  reset(): void {
    this.house = new House('', '', '', '', '', '');
  }

  buildFoundation(): HouseBuilder {
    this.house.foundation = 'Concrete foundation';
    return this;
  }

  buildStructure(): HouseBuilder {
    this.house.structure = 'Wooden structure';
    return this;
  }

  buildRoof(): HouseBuilder {
    this.house.roof = 'Tile roof';
    return this;
  }

  buildInterior(): HouseBuilder {
    this.house.interior = 'Modern interior';
    return this;
  }

  buildGarden(): HouseBuilder {
    this.house.garden = 'Landscaped garden';
    return this;
  }

  buildGarage(): HouseBuilder {
    this.house.garage = 'Two-car garage';
    return this;
  }

  getResult(): House {
    const result = this.house;
    this.reset();
    return result;
  }
}

// Director
class HouseDirector {
  private builder: HouseBuilder;

  constructor(builder: HouseBuilder) {
    this.builder = builder;
  }

  setBuilder(builder: HouseBuilder): void {
    this.builder = builder;
  }

  buildSimpleHouse(): House {
    return this.builder
      .buildFoundation()
      .buildStructure()
      .buildRoof()
      .getResult();
  }

  buildFullHouse(): House {
    return this.builder
      .buildFoundation()
      .buildStructure()
      .buildRoof()
      .buildInterior()
      .buildGarden()
      .buildGarage()
      .getResult();
  }
}

// Usage
const builder = new ConcreteHouseBuilder();
const director = new HouseDirector(builder);

const simpleHouse = director.buildSimpleHouse();
console.log(simpleHouse.toString());

const fullHouse = director.buildFullHouse();
console.log(fullHouse.toString());

// Without director
const customHouse = builder
  .buildFoundation()
  .buildStructure()
  .buildRoof()
  .buildInterior()
  .getResult();

console.log(customHouse.toString());

```

### Fluent Builder with Type Safety

```typescript
// Type-safe builder with chaining
class QueryBuilder {
  private table: string = '';
  private conditions: string[] = [];
  private selectFields: string[] = ['*'];
  private orderByField: string = '';
  private orderDirection: 'ASC' | 'DESC' = 'ASC';
  private limitValue: number = 0;
  private offsetValue: number = 0;

  from(table: string): this {
    this.table = table;
    return this;
  }

  select(...fields: string[]): this {
    this.selectFields = fields;
    return this;
  }

  where(condition: string): this {
    this.conditions.push(condition);
    return this;
  }

  andWhere(condition: string): this {
    this.conditions.push(`AND ${condition}`);
    return this;
  }

  orWhere(condition: string): this {
    this.conditions.push(`OR ${condition}`);
    return this;
  }

  orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.orderByField = field;
    this.orderDirection = direction;
    return this;
  }

  limit(limit: number): this {
    this.limitValue = limit;
    return this;
  }

  offset(offset: number): this {
    this.offsetValue = offset;
    return this;
  }

  build(): string {
    if (!this.table) {
      throw new Error('Table is required');
    }

    let query = `SELECT ${this.selectFields.join(', ')} FROM ${this.table}`;

    if (this.conditions.length > 0) {
      query += ` WHERE ${this.conditions.join(' ')}`;
    }

    if (this.orderByField) {
      query += ` ORDER BY ${this.orderByField} ${this.orderDirection}`;
    }

    if (this.limitValue) {
      query += ` LIMIT ${this.limitValue}`;
    }

    if (this.offsetValue) {
      query += ` OFFSET ${this.offsetValue}`;
    }

    return query;
  }
}

// Usage
const query = new QueryBuilder()
  .select('id', 'name', 'email')
  .from('users')
  .where('age > 18')
  .andWhere('status = "active"')
  .orderBy('name', 'ASC')
  .limit(10)
  .offset(20)
  .build();

console.log(query);
// SELECT id, name, email FROM users WHERE age > 18 AND status = "active" ORDER BY name ASC LIMIT 10 OFFSET 20

```

### HTTP Request Builder

```typescript
interface HttpRequest {
  method: string;
  url: string;
  headers: Record<string, string>;
  body: any;
  timeout: number;
  retries: number;
}

class HttpRequestBuilder {
  private request: HttpRequest;

  constructor() {
    this.request = {
      method: 'GET',
      url: '',
      headers: {},
      body: null,
      timeout: 30000,
      retries: 0
    };
  }

  reset(): this {
    this.request = {
      method: 'GET',
      url: '',
      headers: {},
      body: null,
      timeout: 30000,
      retries: 0
    };
    return this;
  }

  method(method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'): this {
    this.request.method = method;
    return this;
  }

  url(url: string): this {
    this.request.url = url;
    return this;
  }

  header(key: string, value: string): this {
    this.request.headers[key] = value;
    return this;
  }

  headers(headers: Record<string, string>): this {
    Object.assign(this.request.headers, headers);
    return this;
  }

  body(body: any): this {
    this.request.body = body;
    return this;
  }

  json(data: any): this {
    this.request.body = JSON.stringify(data);
    this.request.headers['Content-Type'] = 'application/json';
    return this;
  }

  timeout(timeout: number): this {
    this.request.timeout = timeout;
    return this;
  }

  retries(retries: number): this {
    this.request.retries = retries;
    return this;
  }

  bearerToken(token: string): this {
    this.request.headers['Authorization'] = `Bearer ${token}`;
    return this;
  }

  build(): HttpRequest {
    if (!this.request.url) {
      throw new Error('URL is required');
    }
    return { ...this.request };
  }
}

// Usage
const request = new HttpRequestBuilder()
  .method('POST')
  .url('https://api.example.com/users')
  .header('Accept', 'application/json')
  .json({ name: 'John', email: 'john@example.com' })
  .bearerToken('my-token')
  .timeout(5000)
  .retries(3)
  .build();

console.log(request);

```

### Configuration Builder

```typescript
interface DatabaseConfig {
  host: string;
  port: number;
  username: string;
  password: string;
  database: string;
  ssl: boolean;
  poolSize: number;
  timeout: number;
}

interface AppConfig {
  database: DatabaseConfig;
  redis: { host: string; port: number };
  jwt: { secret: string; expiresIn: string };
  cors: { origin: string[]; credentials: boolean };
}

class DatabaseConfigBuilder {
  private config: Partial<DatabaseConfig> = {};

  host(host: string): this {
    this.config.host = host;
    return this;
  }

  port(port: number): this {
    this.config.port = port;
    return this;
  }

  credentials(username: string, password: string): this {
    this.config.username = username;
    this.config.password = password;
    return this;
  }

  database(database: string): this {
    this.config.database = database;
    return this;
  }

  ssl(ssl: boolean): this {
    this.config.ssl = ssl;
    return this;
  }

  poolSize(size: number): this {
    this.config.poolSize = size;
    return this;
  }

  timeout(timeout: number): this {
    this.config.timeout = timeout;
    return this;
  }

  build(): DatabaseConfig {
    if (!this.config.host || !this.config.database) {
      throw new Error('Host and database are required');
    }

    return {
      host: this.config.host,
      port: this.config.port || 5432,
      username: this.config.username || '',
      password: this.config.password || '',
      database: this.config.database,
      ssl: this.config.ssl || false,
      poolSize: this.config.poolSize || 10,
      timeout: this.config.timeout || 30000
    };
  }
}

// Usage
const dbConfig = new DatabaseConfigBuilder()
  .host('localhost')
  .port(5432)
  .credentials('admin', 'password')
  .database('myapp')
  .ssl(true)
  .poolSize(20)
  .build();

console.log(dbConfig);

```

### Email Builder

```typescript
interface Email {
  to: string[];
  cc: string[];
  bcc: string[];
  subject: string;
  html: string;
  text: string;
  attachments: Array<{ filename: string; content: Buffer }>;
  replyTo: string;
  from: string;
}

class EmailBuilder {
  private email: Email;

  constructor() {
    this.email = {
      to: [],
      cc: [],
      bcc: [],
      subject: '',
      html: '',
      text: '',
      attachments: [],
      replyTo: '',
      from: ''
    };
  }

  from(address: string): this {
    this.email.from = address;
    return this;
  }

  to(address: string): this {
    this.email.to.push(address);
    return this;
  }

  cc(address: string): this {
    this.email.cc.push(address);
    return this;
  }

  bcc(address: string): this {
    this.email.bcc.push(address);
    return this;
  }

  subject(subject: string): this {
    this.email.subject = subject;
    return this;
  }

  html(content: string): this {
    this.email.html = content;
    return this;
  }

  text(content: string): this {
    this.email.text = content;
    return this;
  }

  replyTo(address: string): this {
    this.email.replyTo = address;
    return this;
  }

  attach(filename: string, content: Buffer): this {
    this.email.attachments.push({ filename, content });
    return this;
  }

  build(): Email {
    if (this.email.to.length === 0) {
      throw new Error('At least one recipient is required');
    }

    if (!this.email.subject) {
      throw new Error('Subject is required');
    }

    return { ...this.email };
  }
}

// Usage
const email = new EmailBuilder()
  .from('sender@example.com')
  .to('recipient1@example.com')
  .to('recipient2@example.com')
  .cc('cc@example.com')
  .subject('Hello!')
  .html('<h1>Hello!</h1><p>This is a test email.</p>')
  .text('Hello! This is a test email.')
  .build();

console.log(email);

```

## Real-World Use Cases

### 1. Component Builder (React-style)

```typescript
interface Component {
  type: string;
  props: Record<string, any>;
  children: Component[];
  className: string;
  id: string;
}

class ComponentBuilder {
  private component: Component;

  constructor(type: string) {
    this.component = {
      type,
      props: {},
      children: [],
      className: '',
      id: ''
    };
  }

  id(id: string): this {
    this.component.id = id;
    return this;
  }

  className(className: string): this {
    this.component.className = className;
    return this;
  }

  prop(key: string, value: any): this {
    this.component.props[key] = value;
    return this;
  }

  props(props: Record<string, any>): this {
    Object.assign(this.component.props, props);
    return this;
  }

  child(component: Component): this {
    this.component.children.push(component);
    return this;
  }

  children(components: Component[]): this {
    this.component.children.push(...components);
    return this;
  }

  text(content: string): this {
    this.component.children.push({
      type: 'text',
      props: { content },
      children: [],
      className: '',
      id: ''
    });
    return this;
  }

  build(): Component {
    return { ...this.component };
  }
}

// Usage
const button = new ComponentBuilder('button')
  .id('submit-btn')
  .className('btn btn-primary')
  .prop('onClick', () => console.log('clicked'))
  .text('Submit')
  .build();

const form = new ComponentBuilder('form')
  .className('login-form')
  .child(button)
  .build();

```

### 2. Test Data Builder

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'user' | 'moderator';
  isActive: boolean;
  createdAt: Date;
}

class UserTestBuilder {
  private user: Partial<User> = {};

  static create(): UserTestBuilder {
    return new UserTestBuilder()
      .id(Math.random().toString(36).substr(2, 9))
      .name('Test User')
      .email('test@example.com')
      .age(25)
      .role('user')
      .isActive(true)
      .createdAt(new Date());
  }

  id(id: string): this {
    this.user.id = id;
    return this;
  }

  name(name: string): this {
    this.user.name = name;
    return this;
  }

  email(email: string): this {
    this.user.email = email;
    return this;
  }

  age(age: number): this {
    this.user.age = age;
    return this;
  }

  role(role: User['role']): this {
    this.user.role = role;
    return this;
  }

  isActive(isActive: boolean): this {
    this.user.isActive = isActive;
    return this;
  }

  createdAt(date: Date): this {
    this.user.createdAt = date;
    return this;
  }

  build(): User {
    return this.user as User;
  }

  buildMany(count: number): User[] {
    return Array.from({ length: count }, (_, index) => {
      return new UserTestBuilder()
        .id(`user-${index}`)
        .name(`User ${index}`)
        .email(`user${index}@example.com`)
        .age(20 + index)
        .build();
    });
  }
}

// Usage
const user = UserTestBuilder.create()
  .name('John Doe')
  .email('john@example.com')
  .role('admin')
  .build();

const users = UserTestBuilder.create().buildMany(10);

```

### 3. URL Builder

```typescript
class URLBuilder {
  private protocol: string = 'https';
  private host: string = '';
  private port: number = 0;
  private path: string = '';
  private queryParams: Record<string, string> = {};
  private fragment: string = '';

  protocol(protocol: string): this {
    this.protocol = protocol;
    return this;
  }

  host(host: string): this {
    this.host = host;
    return this;
  }

  port(port: number): this {
    this.port = port;
    return this;
  }

  path(path: string): this {
    this.path = path.startsWith('/') ? path : `/${path}`;
    return this;
  }

  query(key: string, value: string): this {
    this.queryParams[key] = value;
    return this;
  }

  queries(params: Record<string, string>): this {
    Object.assign(this.queryParams, params);
    return this;
  }

  fragment(fragment: string): this {
    this.fragment = fragment;
    return this;
  }

  build(): string {
    if (!this.host) {
      throw new Error('Host is required');
    }

    let url = `${this.protocol}://${this.host}`;

    if (this.port) {
      url += `:${this.port}`;
    }

    url += this.path;

    const queryString = Object.entries(this.queryParams)
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&');

    if (queryString) {
      url += `?${queryString}`;
    }

    if (this.fragment) {
      url += `#${this.fragment}`;
    }

    return url;
  }
}

// Usage
const url = new URLBuilder()
  .protocol('https')
  .host('api.example.com')
  .port(443)
  .path('/users')
  .query('page', '1')
  .query('limit', '10')
  .fragment('section1')
  .build();

console.log(url);
// https://api.example.com:443/users?page=1&limit=10#section1

```

## Common Mistakes

### 1. Too Many Builder Methods

```typescript
// ❌ BAD - Builder with too many methods
class BadBuilder {
  setPartA(): this { ... }
  setPartB(): this { ... }
  setPartC(): this { ... }
  setPartD(): this { ... }
  setPartE(): this { ... }
  setPartF(): this { ... }
  setPartG(): this { ... }
  setPartH(): this { ... }
  // Hard to use and maintain
}

```

### 2. Builder Without Interface

```typescript
// ❌ BAD - No common interface
class HouseBuilder {
  buildFoundation(): this { ... }
  buildStructure(): this { ... }
}

class CarBuilder {
  buildEngine(): this { ... }
  buildWheels(): this { ... }
}

// These builders have no common interface

```

### 3. Builder with Mutable State

```typescript
// ❌ BAD - Builder with complex state
class BadBuilder {
  private state: any;
  private dependencies: any[];

  // Hard to test and use
}

```

### 4. Not Providing Default Values

```typescript
// ❌ BAD - No defaults
class BadBuilder {
  build(): Product {
    if (!this.field1) {
      throw new Error('field1 is required');
    }
    // Should have sensible defaults
  }
}

```

## Best Practices

### 1. Use Interface for Builders

```typescript
// ✅ GOOD - Common interface
interface Builder<T> {
  reset(): this;
  build(): T;
}

```

### 2. Provide Sensible Defaults

```typescript
// ✅ GOOD - Defaults
class GoodBuilder {
  private config: Config = {
    timeout: 30000,
    retries: 3,
    verbose: false
  };
}

```

### 3. Use Fluent Interface

```typescript
// ✅ GOOD - Method chaining
const result = new Builder()
  .setA('value')
  .setB('value')
  .build();

```

### 4. Keep Builders Focused

```typescript
// ✅ GOOD - Single responsibility
class DatabaseBuilder implements Builder<DatabaseConfig> { ... }
class ServerBuilder implements Builder<ServerConfig> { ... }

```

## Performance Considerations

1. **Object Creation**: Builders create intermediate objects; consider object pooling for heavy objects.

2. **Memory Usage**: Builders are lightweight; the built object consumes memory.

3. **Compilation Time**: TypeScript generics add compile-time safety with no runtime cost.

4. **Method Chaining**: Minimal overhead compared to direct object creation.

5. **Validation**: Validate in build method to catch errors early.

## Interview Questions

### Beginner

1. **What is the Builder pattern?**

   - A creational pattern that separates object construction from representation.

2. **When would you use Builder pattern?**

   - When you have many optional parameters or complex construction steps.

3. **What's the difference between Builder and Factory?**

   - Builder creates objects step by step; Factory creates objects in one step.

4. **How do you implement Builder in TypeScript?**

   - Create a builder class with fluent interface and a build method.

5. **What are the benefits of Builder pattern?**

   - Readability, flexibility, immutability, and testability.

### Intermediate

6. **What's the difference between Builder and Prototype?**

   - Builder creates new objects; Prototype clones existing objects.

7. **How do you handle validation in Builder?**

   - Validate in the build method and throw descriptive errors.

8. **Can Builder be used with immutable objects?**

   - Yes, Builder is ideal for creating immutable objects with many fields.

9. **How do you test Builder pattern?**

   - Test each method independently and verify the build output.

10. **What's the relationship between Builder and Fluent Interface?**

    - Builder often uses Fluent Interface for method chaining.

### Senior

11. **How does Builder pattern affect scalability?**

    - Builders are lightweight; the built objects can be optimized.

12. **What are the SOLID violations with Builder?**

    - Usually follows SOLID; watch for builders violating Single Responsibility.

13. **How do you handle Builder in microservices?**

    - Builders can be shared across services; keep them focused.

14. **What are the memory implications of Builder?**

    - Builders are temporary; the built object persists.

15. **How do you refactor Builder code?**

    - Extract common logic, use generics, and apply SOLID principles.

### FAANG-style

16. **Design a Builder for a complex API request.**

    - Consider validation, serialization, and error handling.

17. **How would you implement Builder for distributed systems?**

    - Consider serialization, versioning, and backward compatibility.

18. **What are the implications of Builder in cloud-native applications?**

    - Consider configuration, feature flags, and dynamic configuration.

19. **How do you handle Builder in event-driven architectures?**

    - Use builders for event construction and validation.

20. **Design a Builder that supports validation.**

    - Consider field-level and cross-field validation.

### Follow-ups

21. **Can Builder pattern be combined with other patterns?**

    - Yes, commonly with Factory, Singleton, and Fluent Interface patterns.

22. **How do you handle Builder in testing frameworks?**

    - Create test builders with sensible defaults.

23. **What are the memory implications of Builder pattern?**

    - Builders are temporary; the built object consumes memory.

24. **How do you handle Builder in serverless environments?**

    - Consider cold starts, stateless design, and configuration.

25. **What's the impact of Builder on code maintainability?**

    - Improves maintainability by making object creation readable and flexible.

## Summary

The Builder pattern is essential for creating complex objects with many optional parameters. It improves readability, flexibility, and testability. Use it when you need step-by-step construction, immutable objects, or many configuration options.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           BUILDER PATTERN                   │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Many optional parameters                  │
│ • Complex construction steps                │
│ • Immutable objects needed                  │
│ • Multiple representations                   │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple object creation                    │
│ • Few parameters                            │
│ • Builder adds unnecessary complexity       │
│ • Performance is critical                   │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Builder interface                         │
│ • Fluent interface                          │
│ • Build method                              │
│ • Director (optional)                       │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Too many builder methods                  │
│ • No validation in build                    │
│ • Mutable state                             │
│ • No sensible defaults                      │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Factory (creates objects)                 │
│ • Prototype (clones objects)                │
│ • Fluent Interface (method chaining)        │
└─────────────────────────────────────────────┘

```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Builder](https://refactoring.guru/design-patterns/builder)
- [Builder Pattern in TypeScript](https://www.patterns.dev/posts/builder-pattern/)
