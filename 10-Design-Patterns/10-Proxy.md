# Proxy Pattern

## Definition

The Proxy pattern is a structural design pattern that provides a surrogate or placeholder for another object to control access to it. It creates a representative object that controls access to the original object, adding a layer of indirection.

The pattern is particularly useful for lazy loading, access control, logging, caching, and remote resource management.

## Why Do We Need It?

Without the Proxy pattern, direct object access leads to:

1. **Security issues**: No access control or validation

2. **Performance problems**: Loading expensive resources upfront

3. **Tight coupling**: Direct dependency on concrete implementations

4. **Difficult monitoring**: No logging or audit trails

## How It Works

The Proxy pattern works by:

1. Defining a common interface for the real object and proxy

2. Creating a proxy class that wraps the real object

3. The proxy controls access to the real object

4. The proxy can add behavior before/after delegating to the real object

```text
┌─────────────────────────────────────────────────┐
│              Proxy Pattern                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │◄── Uses interface             │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Subject Interface                │   │
│  │    + request(): void                     │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┐                                 │
│    ▼         ▼                                 │
│ ┌──────┐ ┌──────┐                             │
│ │Real  │ │Proxy │                             │
│ │Subj. │ │      │                             │
│ └──────┘ │- real: RealSubject │               │
│          │+ request(): void   │               │
│          └──────────────┘                     │
└─────────────────────────────────────────────────┘

```

## Code Examples

### Basic Proxy Pattern

```typescript
// Subject interface
interface Image {
  display(): void;
  getInfo(): string;
}

// Real subject
class RealImage implements Image {
  private filename: string;

  constructor(filename: string) {
    this.filename = filename;
    this.loadFromDisk();
  }

  private loadFromDisk(): void {
    console.log(`Loading image from disk: ${this.filename}`);
  }

  display(): void {
    console.log(`Displaying image: ${this.filename}`);
  }

  getInfo(): string {
    return `Image: ${this.filename}`;
  }
}

// Proxy
class ImageProxy implements Image {
  private realImage: RealImage | null = null;
  private filename: string;

  constructor(filename: string) {
    this.filename = filename;
  }

  display(): void {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename);
    }
    this.realImage.display();
  }

  getInfo(): string {
    return `Proxy for: ${this.filename}`;
  }
}

// Client code
function renderImage(image: Image): void {
  console.log(image.getInfo());
  image.display();
}

// Usage
console.log('Creating proxy (no image loaded yet):');
const proxy = new ImageProxy('photo.jpg');

console.log('\nFirst display (loads image):');
proxy.display();

console.log('\nSecond display (uses cached image):');
proxy.display();

```

### Virtual Proxy (Lazy Loading)

```typescript
// Subject interface
interface DatabaseConnection {
  query<T>(sql: string): Promise<T[]>;
  close(): Promise<void>;
  isConnected(): boolean;
}

// Real subject
class RealDatabaseConnection implements DatabaseConnection {
  private connected: boolean = false;

  constructor(private config: any) {
    this.connect();
  }

  private async connect(): Promise<void> {
    console.log('Connecting to database...');
    // Simulate connection delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.connected = true;
    console.log('Connected to database');
  }

  async query<T>(sql: string): Promise<T[]> {
    if (!this.connected) {
      throw new Error('Not connected');
    }
    console.log(`Executing query: ${sql}`);
    return [] as T[];
  }

  async close(): Promise<void> {
    this.connected = false;
    console.log('Database connection closed');
  }

  isConnected(): boolean {
    return this.connected;
  }
}

// Virtual proxy
class DatabaseProxy implements DatabaseConnection {
  private realConnection: RealDatabaseConnection | null = null;
  private connectionPromise: Promise<RealDatabaseConnection> | null = null;

  constructor(private config: any) {}

  private async getConnection(): Promise<RealDatabaseConnection> {
    if (!this.realConnection) {
      if (!this.connectionPromise) {
        this.connectionPromise = this.createConnection();
      }
      this.realConnection = await this.connectionPromise;
    }
    return this.realConnection;
  }

  private async createConnection(): Promise<RealDatabaseConnection> {
    return new RealDatabaseConnection(this.config);
  }

  async query<T>(sql: string): Promise<T[]> {
    const connection = await this.getConnection();
    return connection.query<T>(sql);
  }

  async close(): Promise<void> {
    if (this.realConnection) {
      await this.realConnection.close();
      this.realConnection = null;
      this.connectionPromise = null;
    }
  }

  isConnected(): boolean {
    return this.realConnection?.isConnected() || false;
  }
}

// Client code
const db = new DatabaseProxy({ host: 'localhost', port: 5432 });

// Connection is not established yet
console.log('Database created (not connected):');
console.log(`Connected: ${db.isConnected()}`);

// First query triggers connection
console.log('\nFirst query (connects to database):');
await db.query('SELECT * FROM users');

// Subsequent queries use existing connection
console.log('\nSecond query (uses existing connection):');
await db.query('SELECT * FROM orders');

```

### Protection Proxy (Access Control)

```typescript
// Subject interface
interface Document {
  read(): string;
  write(content: string): void;
  delete(): void;
  getInfo(): DocumentInfo;
}

interface DocumentInfo {
  id: string;
  owner: string;
  lastModified: Date;
  size: number;
}

// Real subject
class RealDocument implements Document {
  private content: string = '';
  private lastModified: Date = new Date();

  constructor(
    public id: string,
    public owner: string,
    initialContent: string = ''
  ) {
    this.content = initialContent;
  }

  read(): string {
    return this.content;
  }

  write(content: string): void {
    this.content = content;
    this.lastModified = new Date();
  }

  delete(): void {
    console.log(`Document ${this.id} deleted`);
  }

  getInfo(): DocumentInfo {
    return {
      id: this.id,
      owner: this.owner,
      lastModified: this.lastModified,
      size: this.content.length
    };
  }
}

// Protection proxy
class DocumentProxy implements Document {
  private realDocument: RealDocument;

  constructor(
    realDocument: RealDocument,
    private currentUser: string,
    private userRole: 'admin' | 'editor' | 'viewer'
  ) {
    this.realDocument = realDocument;
  }

  read(): string {
    console.log(`User ${this.currentUser} reading document`);
    return this.realDocument.read();
  }

  write(content: string): void {
    if (!this.canWrite()) {
      throw new Error('Permission denied: Cannot write to document');
    }

    console.log(`User ${this.currentUser} writing to document`);
    this.realDocument.write(content);
  }

  delete(): void {
    if (!this.canDelete()) {
      throw new Error('Permission denied: Cannot delete document');
    }

    console.log(`User ${this.currentUser} deleting document`);
    this.realDocument.delete();
  }

  getInfo(): DocumentInfo {
    return this.realDocument.getInfo();
  }

  private canWrite(): boolean {
    return this.userRole === 'admin' || this.userRole === 'editor';
  }

  private canDelete(): boolean {
    return this.userRole === 'admin';
  }
}

// Client code
const document = new RealDocument('doc1', 'john', 'Hello World');

const adminProxy = new DocumentProxy(document, 'admin', 'admin');
const editorProxy = new DocumentProxy(document, 'jane', 'editor');
const viewerProxy = new DocumentProxy(document, 'bob', 'viewer');

console.log('Admin can write:');
adminProxy.write('Updated by admin');

console.log('\nEditor can write:');
editorProxy.write('Updated by editor');

console.log('\nViewer cannot write:');
try {
  viewerProxy.write('Attempted update');
} catch (error) {
  console.log(error.message);
}

console.log('\nViewer can read:');
console.log(viewerProxy.read());

```

### Caching Proxy

```typescript
// Subject interface
interface DataFetcher {
  fetch(url: string): Promise<any>;
  postData(url: string, data: any): Promise<any>;
}

// Real subject
class RealDataFetcher implements DataFetcher {
  async fetch(url: string): Promise<any> {
    console.log(`Fetching data from: ${url}`);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { data: `Data from ${url}`, timestamp: Date.now() };
  }

  async postData(url: string, data: any): Promise<any> {
    console.log(`Posting data to: ${url}`);
    return { success: true };
  }
}

// Caching proxy
class CachingProxy implements DataFetcher {
  private cache: Map<string, { data: any; expiry: number }> = new Map();
  private defaultTTL: number;

  constructor(
    private realFetcher: DataFetcher,
    defaultTTL: number = 5 * 60 * 1000 // 5 minutes
  ) {
    this.defaultTTL = defaultTTL;
  }

  async fetch(url: string): Promise<any> {
    const cached = this.cache.get(url);

    if (cached && Date.now() < cached.expiry) {
      console.log(`Cache hit for: ${url}`);
      return cached.data;
    }

    console.log(`Cache miss for: ${url}`);
    const data = await this.realFetcher.fetch(url);

    this.cache.set(url, {
      data,
      expiry: Date.now() + this.defaultTTL
    });

    return data;
  }

  async postData(url: string, data: any): Promise<any> {
    // Invalidate cache for this URL
    this.cache.delete(url);

    return this.realFetcher.postData(url, data);
  }

  clearCache(): void {
    this.cache.clear();
  }

  getCacheSize(): number {
    return this.cache.size;
  }
}

// Client code
const fetcher = new CachingProxy(new RealDataFetcher());

console.log('First fetch (cache miss):');
await fetcher.fetch('https://api.example.com/data');

console.log('\nSecond fetch (cache hit):');
await fetcher.fetch('https://api.example.com/data');

console.log('\nCache size:', fetcher.getCacheSize());

```

### Logging Proxy

```typescript
// Subject interface
interface UserService {
  getUser(id: string): Promise<any>;
  createUser(data: any): Promise<any>;
  updateUser(id: string, data: any): Promise<any>;
  deleteUser(id: string): Promise<boolean>;
}

// Real subject
class RealUserService implements UserService {
  async getUser(id: string): Promise<any> {
    return { id, name: 'John' };
  }

  async createUser(data: any): Promise<any> {
    return { id: '1', ...data };
  }

  async updateUser(id: string, data: any): Promise<any> {
    return { id, ...data };
  }

  async deleteUser(id: string): Promise<boolean> {
    return true;
  }
}

// Logging proxy
class LoggingProxy implements UserService {
  private logs: Array<{ timestamp: Date; method: string; args: any[]; result: any }> = [];

  constructor(private realService: UserService) {}

  async getUser(id: string): Promise<any> {
    const start = Date.now();
    const result = await this.realService.getUser(id);
    const duration = Date.now() - start;

    this.log('getUser', [id], result, duration);
    return result;
  }

  async createUser(data: any): Promise<any> {
    const start = Date.now();
    const result = await this.realService.createUser(data);
    const duration = Date.now() - start;

    this.log('createUser', [data], result, duration);
    return result;
  }

  async updateUser(id: string, data: any): Promise<any> {
    const start = Date.now();
    const result = await this.realService.updateUser(id, data);
    const duration = Date.now() - start;

    this.log('updateUser', [id, data], result, duration);
    return result;
  }

  async deleteUser(id: string): Promise<boolean> {
    const start = Date.now();
    const result = await this.realService.deleteUser(id);
    const duration = Date.now() - start;

    this.log('deleteUser', [id], result, duration);
    return result;
  }

  private log(method: string, args: any[], result: any, duration: number): void {
    const entry = {
      timestamp: new Date(),
      method,
      args,
      result,
      duration
    };

    this.logs.push(entry);
    console.log(`[${method}] Duration: ${duration}ms`, { args, result });
  }

  getLogs(): Array<{ timestamp: Date; method: string; args: any[]; result: any }> {
    return [...this.logs];
  }
}

// Client code
const service = new LoggingProxy(new RealUserService());

await service.getUser('1');
await service.createUser({ name: 'Jane' });
await service.updateUser('1', { name: 'John Updated' });

console.log('\nAll logs:', service.getLogs());

```

## Real-World Use Cases

### 1. Vue.js Reactivity Proxy

```typescript
// Simulating Vue.js reactivity system
type Watcher = (newValue: any, oldValue: any) => void;

class ReactiveObject {
  private data: any;
  private watchers: Map<string, Watcher[]> = new Map();

  constructor(data: any) {
    this.data = this.createProxy(data);
  }

  private createProxy(obj: any): any {
    if (typeof obj !== 'object' || obj === null) {
      return obj;
    }

    const self = this;

    return new Proxy(obj, {
      get(target, prop) {
        const value = target[prop];

        // Recursively proxy nested objects
        if (typeof value === 'object' && value !== null) {
          return self.createProxy(value);
        }

        return value;
      },

      set(target, prop, value) {
        const oldValue = target[prop];
        target[prop] = value;

        // Notify watchers
        self.notifyWatchers(prop as string, value, oldValue);

        return true;
      }
    });
  }

  watch(key: string, watcher: Watcher): () => void {
    if (!this.watchers.has(key)) {
      this.watchers.set(key, []);
    }

    this.watchers.get(key)!.push(watcher);

    // Return unwatch function
    return () => {
      const watchers = this.watchers.get(key);
      if (watchers) {
        const index = watchers.indexOf(watcher);
        if (index !== -1) {
          watchers.splice(index, 1);
        }
      }
    };
  }

  private notifyWatchers(key: string, newValue: any, oldValue: any): void {
    const watchers = this.watchers.get(key);
    if (watchers) {
      watchers.forEach(watcher => watcher(newValue, oldValue));
    }
  }

  getData(): any {
    return this.data;
  }
}

// Usage
const state = new ReactiveObject({ count: 0, user: { name: 'John' } });

state.watch('count', (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`);
});

state.watch('user.name', (newValue, oldValue) => {
  console.log(`Name changed from ${oldValue} to ${newValue}`);
});

state.getData().count = 1; // Logs: Count changed from 0 to 1
state.getData().user.name = 'Jane'; // Logs: Name changed from John to Jane

```

### 2. API Rate Limiting Proxy

```typescript
// Subject interface
interface APIClient {
  request(url: string, options?: any): Promise<any>;
}

// Real subject
class RealAPIClient implements APIClient {
  async request(url: string, options?: any): Promise<any> {
    console.log(`Making request to: ${url}`);
    return { data: 'response', status: 200 };
  }
}

// Rate limiting proxy
class RateLimitProxy implements APIClient {
  private requests: Map<string, number[]> = new Map();
  private limit: number;
  private windowMs: number;

  constructor(
    private realClient: APIClient,
    limit: number = 100,
    windowMs: number = 60000
  ) {
    this.limit = limit;
    this.windowMs = windowMs;
  }

  async request(url: string, options?: any): Promise<any> {
    const endpoint = this.getEndpoint(url);
    const now = Date.now();

    const requests = this.requests.get(endpoint) || [];
    const recentRequests = requests.filter(time => now - time < this.windowMs);

    if (recentRequests.length >= this.limit) {
      console.log(`Rate limit exceeded for ${endpoint}`);
      throw new Error('Rate limit exceeded');
    }

    recentRequests.push(now);
    this.requests.set(endpoint, recentRequests);

    return this.realClient.request(url, options);
  }

  private getEndpoint(url: string): string {
    // Extract endpoint from URL
    const urlObj = new URL(url);
    return urlObj.pathname;
  }

  getRemainingRequests(endpoint: string): number {
    const now = Date.now();
    const requests = this.requests.get(endpoint) || [];
    const recentRequests = requests.filter(time => now - time < this.windowMs);
    return Math.max(0, this.limit - recentRequests.length);
  }
}

// Client code
const apiClient = new RateLimitProxy(new RealAPIClient(), 5, 10000);

for (let i = 0; i < 7; i++) {
  try {
    await apiClient.request('https://api.example.com/data');
    console.log(`Request ${i + 1} successful`);
  } catch (error) {
    console.log(`Request ${i + 1} failed: ${error.message}`);
  }
}

```

### 3. Authentication Proxy

```typescript
// Subject interface
interface SecureResource {
  getData(): Promise<any>;
  updateData(data: any): Promise<any>;
  deleteData(): Promise<boolean>;
}

// Real subject
class RealSecureResource implements SecureResource {
  async getData(): Promise<any> {
    return { sensitive: 'data' };
  }

  async updateData(data: any): Promise<any> {
    return { updated: true, ...data };
  }

  async deleteData(): Promise<boolean> {
    return true;
  }
}

// Authentication proxy
class AuthProxy implements SecureResource {
  private token: string | null = null;

  constructor(private realResource: SecureResource) {}

  async authenticate(username: string, password: string): Promise<boolean> {
    // Simulate authentication
    if (username === 'admin' && password === 'password') {
      this.token = 'valid_token_' + Date.now();
      console.log('Authentication successful');
      return true;
    }

    console.log('Authentication failed');
    return false;
  }

  private isAuthenticated(): boolean {
    return this.token !== null;
  }

  async getData(): Promise<any> {
    if (!this.isAuthenticated()) {
      throw new Error('Not authenticated');
    }

    console.log('Accessing data with token:', this.token);
    return this.realResource.getData();
  }

  async updateData(data: any): Promise<any> {
    if (!this.isAuthenticated()) {
      throw new Error('Not authenticated');
    }

    console.log('Updating data with token:', this.token);
    return this.realResource.updateData(data);
  }

  async deleteData(): Promise<boolean> {
    if (!this.isAuthenticated()) {
      throw new Error('Not authenticated');
    }

    console.log('Deleting data with token:', this.token);
    return this.realResource.deleteData();
  }

  logout(): void {
    this.token = null;
    console.log('Logged out');
  }
}

// Client code
const resource = new AuthProxy(new RealSecureResource());

try {
  await resource.getData();
} catch (error) {
  console.log(error.message);
}

await resource.authenticate('admin', 'password');
await resource.getData();

resource.logout();

try {
  await resource.getData();
} catch (error) {
  console.log(error.message);
}

```

## Common Mistakes

### 1. Proxy Adding Too Much Logic

```typescript
// ❌ BAD - Proxy with business logic
class BadProxy {
  async process(): Promise<any> {
    // Business logic should be in real subject
    if (condition) {
      return this.real.process();
    }
    return null;
  }
}

```

### 2. Not Implementing Interface

```typescript
// ❌ BAD - Proxy doesn't implement interface
class BadProxy {
  private real: RealSubject;

  // Missing interface methods
}

```

### 3. Circular Proxy

```typescript
// ❌ BAD - Proxy references itself
class CircularProxy {
  private proxy: CircularProxy;

  constructor() {
    this.proxy = this;
  }
}

```

### 4. Proxy with State

```typescript
// ❌ BAD - Proxy with complex state
class StatefulProxy {
  private state: any;
  private dependencies: any[];

  // Hard to reason about
}

```

## Best Practices

### 1. Implement Subject Interface

```typescript
// ✅ GOOD - Implements interface
class GoodProxy implements Subject {
  private real: RealSubject;

  request(): void {
    this.real.request();
  }
}

```

### 2. Keep Proxy Focused

```typescript
// ✅ GOOD - Single responsibility
class LoggingProxy implements Subject {
  // Only adds logging
}

```

### 3. Use Dependency Injection

```typescript
// ✅ GOOD - Injectable proxy
class Proxy {
  constructor(private real: Subject) {}
}

```

### 4. Document Proxy Behavior

```typescript
// ✅ GOOD - Clear documentation
/**

 - Logging proxy that logs all method calls
 */
class LoggingProxy implements Subject {
  // Implementation
}

```

## Performance Considerations

1. **Indirection Overhead**: Proxies add a layer of indirection; consider the cost.

2. **Lazy Loading**: Virtual proxies defer expensive operations until needed.

3. **Caching**: Caching proxies can improve performance for repeated operations.

4. **Connection Pooling**: Connection proxies can manage resource pooling.

5. **Async Operations**: Consider async proxies for non-blocking operations.

## Interview Questions

### Beginner

1. **What is the Proxy pattern?**

   - A structural pattern that provides a surrogate for another object to control access.

2. **When would you use Proxy pattern?**

   - For lazy loading, access control, logging, caching, and remote resources.

3. **What's the difference between Proxy and Decorator?**

   - Both wrap objects; Proxy controls access, Decorator adds behavior.

4. **How do you implement Proxy in TypeScript?**

   - Create a proxy class that implements the subject interface and wraps the real subject.

5. **What are the benefits of Proxy pattern?**

   - Access control, lazy loading, logging, caching, and security.

### Intermediate

6. **What are the different types of Proxies?**

   - Virtual (lazy loading), Protection (access control), Caching, Logging, Remote.

7. **How do you test Proxy pattern?**

   - Test proxy behavior independently, mock real subject.

8. **What's the relationship between Proxy and Facade?**

   - Proxy controls access; Facade simplifies interface.

9. **How do you handle proxy chaining?**

   - Each proxy wraps the next; order matters.

10. **Can Proxy change the interface?**

    - No, proxy must maintain the subject interface.

### Senior

11. **How does Proxy pattern affect scalability?**

    - Proxies are lightweight; consider connection pooling for scaling.

12. **What are the SOLID violations with Proxy?**

    - Usually follows SOLID; watch for proxies violating Single Responsibility.

13. **How do you handle Proxy in microservices?**

    - Use proxies for API gateways, service meshes, and load balancing.

14. **What are the memory implications of Proxy?**

    - Proxies are usually stateless; the real subject consumes memory.

15. **How do you refactor Proxy code?**

    - Extract common logic, use composition, and apply SOLID principles.

### FAANG-style

16. **Design a Proxy for a distributed system.**

    - Consider network transparency, fault tolerance, and load balancing.

17. **How would you implement Proxy for cloud-native applications?**

    - Consider serverless functions, API gateways, and service meshes.

18. **What are the implications of Proxy in event-driven architectures?**

    - Use proxies for event routing, filtering, and transformation.

19. **How do you handle Proxy in real-time systems?**

    - Consider latency, throughput, and resource management.

20. **Design a Proxy that supports A/B testing.**

    - Consider traffic splitting, metrics collection, and gradual rollout.

### Follow-ups

21. **Can Proxy pattern be combined with other patterns?**

    - Yes, commonly with Decorator, Adapter, and Factory patterns.

22. **How do you handle Proxy in testing frameworks?**

    - Use dependency injection, create test proxies, and mock implementations.

23. **What are the memory implications of Proxy pattern?**

    - Proxies are usually lightweight; the real subject consumes memory.

24. **How do you handle Proxy in serverless environments?**

    - Consider stateless proxies, API gateways, and function composition.

25. **What's the impact of Proxy on code maintainability?**

    - Improves maintainability by adding indirection and control.

## Summary

The Proxy pattern is essential for controlling access to objects. It enables lazy loading, access control, logging, caching, and remote resource management. Use it to add a layer of indirection without modifying the real subject.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           PROXY PATTERN                     │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Lazy loading                              │
│ • Access control                            │
│ • Logging and monitoring                    │
│ • Caching                                   │
│ • Remote resources                          │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple object access                      │
│ • Proxy adds unnecessary complexity         │
│ • Performance is critical                   │
│ • Proxy with too much state                 │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Subject interface                         │
│ • Real subject                              │
│ • Proxy controls access                     │
│ • Delegation to real subject                │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Proxy with business logic                 │
│ • Not implementing interface                │
│ • Circular proxies                          │
│ • Proxy with too much state                 │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Decorator (adds behavior)                 │
│ • Adapter (changes interface)               │
│ • Facade (simplifies interface)             │
└─────────────────────────────────────────────┘

```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Proxy](https://refactoring.guru/design-patterns/proxy)
- [MDN: Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
