# Facade Pattern

## Definition

The Facade pattern is a structural design pattern that provides a simplified interface to a library, a framework, or any other complex set of classes. It hides the complexity of the subsystem and provides a unified interface to the client.

The pattern is particularly useful when you need to provide a simple interface to a complex subsystem, when you want to layer your subsystems, or when you need to define entry points to each level of a layered software.

## Why Do We Need It?

Without the Facade pattern, clients interact directly with complex subsystems, leading to:

1. **Tight coupling**: Clients depend on many subsystem classes
2. **Complex code**: Clients need to understand subsystem internals
3. **Difficult maintenance**: Changes in subsystems affect clients
4. **Code duplication**: Common operations repeated everywhere

## How It Works

The Facade pattern works by:

1. Defining a facade class that provides simplified methods
2. The facade delegates calls to appropriate subsystem classes
3. Clients interact only with the facade
4. The facade handles subsystem coordination

```
┌─────────────────────────────────────────────────┐
│              Facade Pattern                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │◄── Uses simplified interface  │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Facade                           │   │
│  │    + simpleMethod(): void                │   │
│  │    - subsystem1: Subsystem1              │   │
│  │    - subsystem2: Subsystem2              │   │
│  │    - subsystem3: Subsystem3              │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┬────────────┐                    │
│    ▼         ▼            ▼                    │
│ ┌──────┐ ┌──────┐   ┌──────┐                  │
│ │Sub 1 │ │Sub 2 │   │Sub 3 │                  │
│ └──────┘ └──────┘   └──────┘                  │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Facade Pattern

```typescript
// Complex subsystem classes
class CPU {
  freeze(): void {
    console.log('CPU: Freezing processor');
  }

  jump(address: number): void {
    console.log(`CPU: Jumping to address ${address}`);
  }

  execute(): void {
    console.log('CPU: Executing instructions');
  }
}

class Memory {
  load(address: number, data: string): void {
    console.log(`Memory: Loading data at address ${address}`);
  }

  free(address: number): void {
    console.log(`Memory: Freeing address ${address}`);
  }
}

class HardDrive {
  read(sector: number, size: number): string {
    console.log(`HardDrive: Reading ${size} bytes from sector ${sector}`);
    return 'data';
  }

  write(sector: number, data: string): void {
    console.log(`HardDrive: Writing data to sector ${sector}`);
  }
}

// Facade
class ComputerFacade {
  private cpu: CPU;
  private memory: Memory;
  private hardDrive: HardDrive;

  constructor() {
    this.cpu = new CPU();
    this.memory = new Memory();
    this.hardDrive = new HardDrive();
  }

  startComputer(): void {
    console.log('Starting computer...');

    // Complex startup sequence
    this.cpu.freeze();
    this.memory.load(0, 'boot sector');
    this.hardDrive.read(0, 512);
    this.cpu.jump(0);
    this.cpu.execute();

    console.log('Computer started successfully');
  }

  shutdownComputer(): void {
    console.log('Shutting down computer...');

    // Complex shutdown sequence
    this.cpu.freeze();
    this.memory.free(0);

    console.log('Computer shut down successfully');
  }
}

// Client code
const computer = new ComputerFacade();
computer.startComputer();
// No need to know about CPU, Memory, HardDrive details
```

### API Facade

```typescript
// Complex subsystems
class AuthenticationService {
  async authenticate(username: string, password: string): Promise<string> {
    console.log(`Authenticating user: ${username}`);
    return 'auth_token_' + Date.now();
  }

  async validateToken(token: string): Promise<boolean> {
    console.log('Validating token...');
    return true;
  }

  async refreshToken(token: string): Promise<string> {
    console.log('Refreshing token...');
    return 'new_token_' + Date.now();
  }
}

class UserService {
  async getUser(userId: string): Promise<any> {
    console.log(`Getting user ${userId}`);
    return { id: userId, name: 'John' };
  }

  async updateUser(userId: string, data: any): Promise<any> {
    console.log(`Updating user ${userId}`);
    return { id: userId, ...data };
  }

  async deleteUser(userId: string): Promise<boolean> {
    console.log(`Deleting user ${userId}`);
    return true;
  }
}

class OrderService {
  async getOrders(userId: string): Promise<any[]> {
    console.log(`Getting orders for user ${userId}`);
    return [{ id: '1', total: 100 }];
  }

  async createOrder(userId: string, items: any[]): Promise<any> {
    console.log(`Creating order for user ${userId}`);
    return { id: '2', items, total: items.length * 10 };
  }
}

class PaymentService {
  async processPayment(orderId: string, amount: number): Promise<boolean> {
    console.log(`Processing payment for order ${orderId}: $${amount}`);
    return true;
  }

  async getPaymentHistory(userId: string): Promise<any[]> {
    console.log(`Getting payment history for user ${userId}`);
    return [];
  }
}

// Facade
class ECommerceFacade {
  private auth: AuthenticationService;
  private users: UserService;
  private orders: OrderService;
  private payments: PaymentService;

  constructor() {
    this.auth = new AuthenticationService();
    this.users = new UserService();
    this.orders = new OrderService();
    this.payments = new PaymentService();
  }

  async login(username: string, password: string): Promise<string> {
    const token = await this.auth.authenticate(username, password);
    console.log('Login successful');
    return token;
  }

  async placeOrder(token: string, userId: string, items: any[]): Promise<any> {
    // Validate token
    const isValid = await this.auth.validateToken(token);
    if (!isValid) {
      throw new Error('Invalid token');
    }

    // Create order
    const order = await this.orders.createOrder(userId, items);

    // Process payment
    const paymentSuccess = await this.payments.processPayment(order.id, order.total);

    if (!paymentSuccess) {
      throw new Error('Payment failed');
    }

    console.log('Order placed successfully');
    return order;
  }

  async getUserProfile(token: string, userId: string): Promise<any> {
    const isValid = await this.auth.validateToken(token);
    if (!isValid) {
      throw new Error('Invalid token');
    }

    const user = await this.users.getUser(userId);
    const orders = await this.orders.getOrders(userId);
    const payments = await this.payments.getPaymentHistory(userId);

    return { user, orders, payments };
  }
}

// Client code
const ecommerce = new ECommerceFacade();
const token = await ecommerce.login('john', 'password');
const order = await ecommerce.placeOrder(token, 'user1', [{ id: '1', quantity: 2 }]);
```

### Database Facade

```typescript
// Complex subsystems
class ConnectionPool {
  private connections: any[] = [];

  async getConnection(): Promise<any> {
    console.log('Getting connection from pool');
    return { id: Math.random() };
  }

  async releaseConnection(connection: any): Promise<void> {
    console.log('Releasing connection to pool');
  }
}

class QueryBuilder {
  select(table: string, fields: string[]): string {
    return `SELECT ${fields.join(', ')} FROM ${table}`;
  }

  insert(table: string, data: Record<string, any>): { sql: string; values: any[] } {
    const fields = Object.keys(data);
    const values = Object.values(data);
    return {
      sql: `INSERT INTO ${table} (${fields.join(', ')}) VALUES (${fields.map(() => '?').join(', ')})`,
      values
    };
  }

  update(table: string, data: Record<string, any>, where: string): { sql: string; values: any[] } {
    const fields = Object.keys(data);
    const values = Object.values(data);
    return {
      sql: `UPDATE ${table} SET ${fields.map(f => `${f} = ?`).join(', ')} WHERE ${where}`,
      values
    };
  }

  delete(table: string, where: string): string {
    return `DELETE FROM ${table} WHERE ${where}`;
  }
}

class MigrationRunner {
  async runMigrations(): Promise<void> {
    console.log('Running migrations...');
  }

  async rollback(): Promise<void> {
    console.log('Rolling back migrations...');
  }
}

class CacheManager {
  private cache: Map<string, any> = new Map();

  async get(key: string): Promise<any> {
    return this.cache.get(key);
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    this.cache.set(key, value);
  }

  async invalidate(pattern: string): Promise<void> {
    // Invalidate cache entries matching pattern
  }
}

// Facade
class DatabaseFacade {
  private pool: ConnectionPool;
  private queryBuilder: QueryBuilder;
  private migrations: MigrationRunner;
  private cache: CacheManager;

  constructor() {
    this.pool = new ConnectionPool();
    this.queryBuilder = new QueryBuilder();
    this.migrations = new MigrationRunner();
    this.cache = new CacheManager();
  }

  async query<T>(sql: string, params?: any[]): Promise<T[]> {
    const connection = await this.pool.getConnection();

    try {
      // Check cache first
      const cacheKey = `query:${sql}:${JSON.stringify(params)}`;
      const cached = await this.cache.get(cacheKey);
      if (cached) {
        return cached;
      }

      // Execute query
      console.log(`Executing query: ${sql}`);
      const result: T[] = [];

      // Cache result
      await this.cache.set(cacheKey, result, 300); // 5 minutes TTL

      return result;
    } finally {
      await this.pool.releaseConnection(connection);
    }
  }

  async insert<T>(table: string, data: Record<string, any>): Promise<T> {
    const { sql, values } = this.queryBuilder.insert(table, data);
    console.log(`Inserting into ${table}`);

    // Invalidate cache for this table
    await this.cache.invalidate(`${table}:*`);

    return {} as T;
  }

  async update<T>(table: string, id: string, data: Record<string, any>): Promise<T> {
    const { sql, values } = this.queryBuilder.update(table, data, `id = '${id}'`);
    console.log(`Updating ${table} where id = ${id}`);

    // Invalidate cache
    await this.cache.invalidate(`${table}:*`);

    return {} as T;
  }

  async delete(table: string, id: string): Promise<boolean> {
    const sql = this.queryBuilder.delete(table, `id = '${id}'`);
    console.log(`Deleting from ${table} where id = ${id}`);

    // Invalidate cache
    await this.cache.invalidate(`${table}:*`);

    return true;
  }

  async initialize(): Promise<void> {
    await this.migrations.runMigrations();
    console.log('Database initialized');
  }

  async shutdown(): Promise<void> {
    console.log('Database shutdown');
  }
}

// Client code
const db = new DatabaseFacade();
await db.initialize();

const users = await db.query('SELECT * FROM users');
await db.insert('users', { name: 'John', email: 'john@example.com' });
await db.update('users', '1', { name: 'Jane' });
await db.delete('users', '1');

await db.shutdown();
```

### File System Facade

```typescript
// Complex subsystems
class FileReader {
  async read(path: string): Promise<string> {
    console.log(`Reading file: ${path}`);
    return 'file content';
  }

  async readBuffer(path: string): Promise<Buffer> {
    console.log(`Reading file as buffer: ${path}`);
    return Buffer.from('file content');
  }
}

class FileWriter {
  async write(path: string, content: string): Promise<void> {
    console.log(`Writing file: ${path}`);
  }

  async append(path: string, content: string): Promise<void> {
    console.log(`Appending to file: ${path}`);
  }
}

class FileSearcher {
  async search(directory: string, pattern: string): Promise<string[]> {
    console.log(`Searching for ${pattern} in ${directory}`);
    return ['file1.txt', 'file2.txt'];
  }

  async searchContent(directory: string, content: string): Promise<string[]> {
    console.log(`Searching for content "${content}" in ${directory}`);
    return ['file1.txt'];
  }
}

class FileCompressor {
  async compress(path: string): Promise<string> {
    console.log(`Compressing: ${path}`);
    return `${path}.gz`;
  }

  async decompress(path: string): Promise<string> {
    console.log(`Decompressing: ${path}`);
    return path.replace('.gz', '');
  }
}

// Facade
class FileSystemFacade {
  private reader: FileReader;
  private writer: FileWriter;
  private searcher: FileSearcher;
  private compressor: FileCompressor;

  constructor() {
    this.reader = new FileReader();
    this.writer = new FileWriter();
    this.searcher = new FileSearcher();
    this.compressor = new FileCompressor();
  }

  async readAndProcess(path: string, processor: (content: string) => string): Promise<string> {
    const content = await this.reader.read(path);
    const processed = processor(content);
    await this.writer.write(path, processed);
    return processed;
  }

  async backupAndCompress(path: string): Promise<string> {
    const content = await this.reader.read(path);
    const backupPath = `${path}.backup`;
    await this.writer.write(backupPath, content);
    const compressed = await this.compressor.compress(backupPath);
    return compressed;
  }

  async searchAndReplace(directory: string, search: string, replace: string): Promise<number> {
    const files = await this.searcher.searchContent(directory, search);

    for (const file of files) {
      const content = await this.reader.read(file);
      const newContent = content.replace(new RegExp(search, 'g'), replace);
      await this.writer.write(file, newContent);
    }

    return files.length;
  }

  async batchProcess(paths: string[], processor: (content: string) => string): Promise<void> {
    for (const path of paths) {
      await this.readAndProcess(path, processor);
    }
  }
}

// Client code
const fs = new FileSystemFacade();
await fs.readAndProcess('file.txt', content => content.toUpperCase());
await fs.backupAndCompress('important.txt');
await fs.searchAndReplace('./src', 'oldFunction', 'newFunction');
```

## Real-World Use Cases

### 1. E-commerce Checkout Facade

```typescript
class InventoryChecker {
  async checkStock(productId: string, quantity: number): Promise<boolean> {
    console.log(`Checking stock for ${productId}: ${quantity} units`);
    return true;
  }

  async reserveStock(productId: string, quantity: number): Promise<string> {
    console.log(`Reserving stock for ${productId}`);
    return 'reservation_' + Date.now();
  }
}

class PriceCalculator {
  async calculatePrice(items: any[]): Promise<number> {
    console.log('Calculating total price');
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  async applyDiscount(price: number, code: string): Promise<number> {
    console.log(`Applying discount code: ${code}`);
    return price * 0.9; // 10% discount
  }
}

class ShippingCalculator {
  async calculateShipping(address: any, weight: number): Promise<number> {
    console.log(`Calculating shipping to ${address.city}`);
    return 9.99;
  }

  async getDeliveryEstimate(address: any): Promise<string> {
    return '3-5 business days';
  }
}

class OrderProcessor {
  async createOrder(data: any): Promise<string> {
    console.log('Creating order');
    return 'order_' + Date.now();
  }

  async processPayment(orderId: string, amount: number): Promise<boolean> {
    console.log(`Processing payment for order ${orderId}: $${amount}`);
    return true;
  }
}

// Facade
class CheckoutFacade {
  private inventory: InventoryChecker;
  private pricing: PriceCalculator;
  private shipping: ShippingCalculator;
  private orders: OrderProcessor;

  constructor() {
    this.inventory = new InventoryChecker();
    this.pricing = new PriceCalculator();
    this.shipping = new ShippingCalculator();
    this.orders = new OrderProcessor();
  }

  async checkout(cart: { items: any[]; address: any; discountCode?: string }): Promise<any> {
    // Check stock
    for (const item of cart.items) {
      const inStock = await this.inventory.checkStock(item.productId, item.quantity);
      if (!inStock) {
        throw new Error(`Out of stock: ${item.productId}`);
      }
    }

    // Calculate prices
    let total = await this.pricing.calculatePrice(cart.items);

    // Apply discount
    if (cart.discountCode) {
      total = await this.pricing.applyDiscount(total, cart.discountCode);
    }

    // Calculate shipping
    const shipping = await this.shipping.calculateShipping(cart.address, 10);
    total += shipping;

    // Create order
    const orderId = await this.orders.createOrder({
      items: cart.items,
      address: cart.address,
      total
    });

    // Process payment
    const paymentSuccess = await this.orders.processPayment(orderId, total);

    if (!paymentSuccess) {
      throw new Error('Payment failed');
    }

    // Reserve stock
    for (const item of cart.items) {
      await this.inventory.reserveStock(item.productId, item.quantity);
    }

    return {
      orderId,
      total,
      shipping,
      deliveryEstimate: await this.shipping.getDeliveryEstimate(cart.address)
    };
  }
}
```

### 2. Notification Facade

```typescript
class EmailSender {
  async send(to: string, subject: string, body: string): Promise<boolean> {
    console.log(`Sending email to ${to}`);
    return true;
  }
}

class SMSSender {
  async send(phone: string, message: string): Promise<boolean> {
    console.log(`Sending SMS to ${phone}`);
    return true;
  }
}

class PushNotificationSender {
  async send(userId: string, title: string, body: string): Promise<boolean> {
    console.log(`Sending push notification to ${userId}`);
    return true;
  }
}

class SlackNotifier {
  async send(channel: string, message: string): Promise<boolean> {
    console.log(`Sending Slack message to ${channel}`);
    return true;
  }
}

// Facade
class NotificationFacade {
  private email: EmailSender;
  private sms: SMSSender;
  private push: PushNotificationSender;
  private slack: SlackNotifier;

  constructor() {
    this.email = new EmailSender();
    this.sms = new SMSSender();
    this.push = new PushNotificationSender();
    this.slack = new SlackNotifier();
  }

  async sendNotification(
    recipient: { email?: string; phone?: string; userId?: string },
    channels: string[],
    title: string,
    message: string
  ): Promise<boolean[]> {
    const results: boolean[] = [];

    for (const channel of channels) {
      switch (channel) {
        case 'email':
          if (recipient.email) {
            results.push(await this.email.send(recipient.email, title, message));
          }
          break;
        case 'sms':
          if (recipient.phone) {
            results.push(await this.sms.send(recipient.phone, message));
          }
          break;
        case 'push':
          if (recipient.userId) {
            results.push(await this.push.send(recipient.userId, title, message));
          }
          break;
        case 'slack':
          results.push(await this.slack.send('general', message));
          break;
      }
    }

    return results;
  }

  async sendBulkNotification(
    recipients: Array<{ email?: string; phone?: string; userId?: string }>,
    channels: string[],
    title: string,
    message: string
  ): Promise<void> {
    for (const recipient of recipients) {
      await this.sendNotification(recipient, channels, title, message);
    }
  }
}
```

### 3. Deployment Facade

```typescript
class CodeBuilder {
  async build(project: string): Promise<string> {
    console.log(`Building project: ${project}`);
    return 'build_' + Date.now();
  }

  async test(project: string): Promise<boolean> {
    console.log(`Running tests for: ${project}`);
    return true;
  }
}

class DockerManager {
  async buildImage(project: string): Promise<string> {
    console.log(`Building Docker image: ${project}`);
    return 'image_' + Date.now();
  }

  async pushImage(image: string, registry: string): Promise<boolean> {
    console.log(`Pushing image to ${registry}`);
    return true;
  }

  async runContainer(image: string): Promise<string> {
    console.log(`Running container: ${image}`);
    return 'container_' + Date.now();
  }
}

class KubernetesManager {
  async deploy(image: string, replicas: number): Promise<string> {
    console.log(`Deploying ${image} with ${replicas} replicas`);
    return 'deployment_' + Date.now();
  }

  async scale(deployment: string, replicas: number): Promise<boolean> {
    console.log(`Scaling ${deployment} to ${replicas} replicas`);
    return true;
  }

  async getStatus(deployment: string): Promise<string> {
    return 'running';
  }
}

class Monitor {
  async setupMonitoring(deployment: string): Promise<void> {
    console.log(`Setting up monitoring for ${deployment}`);
  }

  async setupAlerts(deployment: string): Promise<void> {
    console.log(`Setting up alerts for ${deployment}`);
  }
}

// Facade
class DeploymentFacade {
  private builder: CodeBuilder;
  private docker: DockerManager;
  private k8s: KubernetesManager;
  private monitor: Monitor;

  constructor() {
    this.builder = new CodeBuilder();
    this.docker = new DockerManager();
    this.k8s = new KubernetesManager();
    this.monitor = new Monitor();
  }

  async deploy(project: string, config: {
    registry: string;
    replicas: number;
    enableMonitoring: boolean;
  }): Promise<{ deployment: string; status: string }> {
    // Build and test
    const buildId = await this.builder.build(project);
    const testsPass = await this.builder.test(project);

    if (!testsPass) {
      throw new Error('Tests failed');
    }

    // Docker
    const image = await this.docker.buildImage(project);
    await this.docker.pushImage(image, config.registry);

    // Kubernetes
    const deployment = await this.k8s.deploy(image, config.replicas);

    // Monitoring
    if (config.enableMonitoring) {
      await this.monitor.setupMonitoring(deployment);
      await this.monitor.setupAlerts(deployment);
    }

    const status = await this.k8s.getStatus(deployment);

    return { deployment, status };
  }

  async rollback(deployment: string): Promise<boolean> {
    console.log(`Rolling back deployment: ${deployment}`);
    return true;
  }

  async scale(deployment: string, replicas: number): Promise<boolean> {
    return this.k8s.scale(deployment, replicas);
  }
}
```

## Common Mistakes

### 1. God Facade

```typescript
// ❌ BAD - Facade with too many responsibilities
class GodFacade {
  async doEverything(): void {
    // Does too much, violates Single Responsibility
  }
}
```

### 2. Facade with Business Logic

```typescript
// ❌ BAD - Facade with business logic
class BadFacade {
  async processOrder(order: any): Promise<any> {
    // Business logic should be in services, not facade
    if (order.total > 100) {
      order.discount = 0.1;
    }
  }
}
```

### 3. Bypassing Facade

```typescript
// ❌ BAD - Client bypasses facade
const client = new Client();
const subsystem = new Subsystem();
client.directlyUseSubsystem(subsystem); // Should use facade
```

### 4. Not Providing All Needed Methods

```typescript
// ❌ BAD - Facade missing important operations
class IncompleteFacade {
  async create(): Promise<void> { ... }
  // Missing: read, update, delete
}
```

## Best Practices

### 1. Keep Facade Focused

```typescript
// ✅ GOOD - Single responsibility
class UserFacade {
  // Only user-related operations
}
```

### 2. Delegate to Appropriate Subsystems

```typescript
// ✅ GOOD - Proper delegation
class OrderFacade {
  async createOrder(data: any): Promise<any> {
    const order = await this.orderService.create(data);
    await this.paymentService.process(order.total);
    await this.inventoryService.reserve(order.items);
    return order;
  }
}
```

### 3. Use Dependency Injection

```typescript
// ✅ GOOD - Injectable facade
class Facade {
  constructor(
    private service1: Service1,
    private service2: Service2
  ) {}
}
```

### 4. Provide Comprehensive Interface

```typescript
// ✅ GOOD - Complete interface
class DatabaseFacade {
  async query<T>(sql: string): Promise<T[]> { ... }
  async insert<T>(table: string, data: any): Promise<T> { ... }
  async update<T>(table: string, id: string, data: any): Promise<T> { ... }
  async delete(table: string, id: string): Promise<boolean> { ... }
}
```

## Performance Considerations

1. **Delegation Overhead**: Facades add minimal overhead; the subsystem calls are the bottleneck.

2. **Batch Operations**: Implement batch operations in facade for better performance.

3. **Caching**: Add caching at facade level for frequently accessed data.

4. **Async Operations**: Use Promise.all for parallel subsystem calls when possible.

5. **Lazy Initialization**: Initialize subsystems only when needed.

## Interview Questions

### Beginner

1. **What is the Facade pattern?**
   - A structural pattern that provides a simplified interface to a complex subsystem.

2. **When would you use Facade pattern?**
   - When you need to simplify a complex system or provide a unified interface.

3. **What's the difference between Facade and Adapter?**
   - Facade simplifies interface; Adapter makes incompatible interfaces compatible.

4. **How do you implement Facade in TypeScript?**
   - Create a facade class that delegates to subsystem classes.

5. **What are the benefits of Facade pattern?**
   - Simplified interface, loose coupling, and improved readability.

### Intermediate

6. **Can Facade add functionality?**
   - Yes, but keep it focused on coordination, not business logic.

7. **How do you test Facade pattern?**
   - Mock subsystems, test facade's delegation logic.

8. **What's the relationship between Facade and Mediator?**
   - Facade simplifies; Mediator centralizes communication between objects.

9. **How do you handle Facade versioning?**
   - Use API versioning, backward compatibility, and deprecation warnings.

10. **Can Facade be used with microservices?**
    - Yes, as an API gateway or service facade.

### Senior

11. **How does Facade pattern affect scalability?**
    - Facades are lightweight; subsystems can be scaled independently.

12. **What are the SOLID violations with Facade?**
    - Usually follows SOLID; watch for facade violating Single Responsibility.

13. **How do you handle Facade in distributed systems?**
    - Use API gateways, service meshes, or backend for frontends.

14. **What are the memory implications of Facade?**
    - Facades are usually stateless; subsystems consume memory.

15. **How do you refactor Facade code?**
    - Extract common logic, use composition, and apply SOLID principles.

### FAANG-style

16. **Design a Facade for a microservices architecture.**
    - Consider API gateway, service discovery, and load balancing.

17. **How would you implement Facade for distributed systems?**
    - Consider network transparency, fault tolerance, and caching.

18. **What are the implications of Facade in cloud-native applications?**
    - Consider serverless facades, API gateways, and edge computing.

19. **How do you handle Facade in event-driven architectures?**
    - Use event facades, message brokers, and async operations.

20. **Design a Facade that supports multiple clients.**
    - Consider client-specific facades, API versioning, and authentication.

### Follow-ups

21. **Can Facade pattern be combined with other patterns?**
    - Yes, commonly with Adapter, Mediator, and Proxy patterns.

22. **How do you handle Facade in testing frameworks?**
    - Use dependency injection, create test facades, and mock subsystems.

23. **What are the memory implications of Facade pattern?**
    - Facades are usually lightweight; subsystems consume memory.

24. **How do you handle Facade in serverless environments?**
    - Consider stateless facades, API gateways, and function composition.

25. **What's the impact of Facade on code maintainability?**
    - Improves maintainability by simplifying complex systems.

## Summary

The Facade pattern is essential for simplifying complex systems and providing unified interfaces. It improves readability, reduces coupling, and makes systems easier to use. Use it to hide subsystem complexity, layer your system, or provide simplified APIs.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│           FACADE PATTERN                    │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Simplify complex systems                  │
│ • Provide unified interface                 │
│ • Layer your system                         │
│ • Hide subsystem complexity                 │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • System is already simple                  │
│ • Facade adds unnecessary complexity        │
│ • Performance is critical                   │
│ • Clients need subsystem access             │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Simplified interface                      │
│ • Delegation to subsystems                  │
│ • Unified access point                      │
│ • Subsystem coordination                    │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • God facades                               │
│ • Business logic in facade                  │
│ • Bypassing facade                          │
│ • Missing operations                        │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Adapter (interface conversion)            │
│ • Mediator (centralized communication)      │
│ • Proxy (controls access)                   │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Facade](https://refactoring.guru/design-patterns/facade)
- [Facade Pattern Examples](https://www.patterns.dev/posts/facade-pattern/)
