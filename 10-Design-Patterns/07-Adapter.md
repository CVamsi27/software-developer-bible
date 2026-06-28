# Adapter Pattern

## Definition

The Adapter pattern is a structural design pattern that allows objects with incompatible interfaces to collaborate. It acts as a wrapper between two objects, catching calls for one object and transforming them to format and interface recognizable by the second object.

Also known as Wrapper pattern, it's particularly useful when integrating third-party libraries, legacy systems, or APIs with different interfaces.

## Why Do We Need It?

Without the Adapter pattern, integrating incompatible interfaces leads to:

1. **Tight coupling**: Code depends on specific external interfaces

2. **Code duplication**: Conversion logic repeated everywhere

3. **Difficult maintenance**: Changes in external APIs require modifying multiple files

4. **Testing challenges**: Hard to mock external dependencies

## How It Works

The Adapter pattern works by:

1. Defining a target interface that the client expects

2. Creating an adapter class that implements the target interface

3. The adapter wraps the adaptee (existing class with incompatible interface)

4. Translating calls between the two interfaces

```text
┌─────────────────────────────────────────────────┐
│              Adapter Pattern                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │◄── Uses target interface      │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Target Interface                 │   │
│  │    + request(): string                   │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Adapter                         │   │
│  │    + request(): string                   │   │
│  │    - adaptee: Adaptee                    │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Adaptee (Incompatible)           │   │
│  │    + specificRequest(): string           │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘

```

## Code Examples

### Basic Adapter Pattern

```typescript
// Target interface (what the client expects)
interface MediaPlayer {
  play(filename: string): void;
  pause(): void;
  stop(): void;
  getCurrentTime(): number;
}

// Adaptee (existing class with incompatible interface)
class OldMediaPlayer {
  playMedia(file: string): void {
    console.log(`Playing media: ${file}`);
  }

  pauseMedia(): void {
    console.log('Pausing media');
  }

  stopMedia(): void {
    console.log('Stopping media');
  }

  getPlaybackPosition(): number {
    return 0;
  }
}

// Adapter
class OldMediaPlayerAdapter implements MediaPlayer {
  private adaptee: OldMediaPlayer;

  constructor(adaptee: OldMediaPlayer) {
    this.adaptee = adaptee;
  }

  play(filename: string): void {
    this.adaptee.playMedia(filename);
  }

  pause(): void {
    this.adaptee.pauseMedia();
  }

  stop(): void {
    this.adaptee.stopMedia();
  }

  getCurrentTime(): number {
    return this.adaptee.getPlaybackPosition();
  }
}

// Client code
function playMusic(player: MediaPlayer, filename: string): void {
  player.play(filename);
  // ... do something
  player.stop();
}

// Usage
const oldPlayer = new OldMediaPlayer();
const adapter = new OldMediaPlayerAdapter(oldPlayer);

playMusic(adapter, 'song.mp3'); // Works with the adapter

```

### API Response Adapter

```typescript
// Target interface
interface NormalizedUser {
  id: string;
  name: string;
  email: string;
  avatar: string;
  createdAt: Date;
}

// Different API responses
interface GitHubUser {
  login: string;
  name: string;
  email: string;
  avatar_url: string;
  created_at: string;
}

interface GoogleUser {
  id: string;
  displayName: string;
  emails: Array<{ value: string }>;
  image: { url: string };
  created: string;
}

interface FacebookUser {
  id: string;
  name: string;
  email: string;
  picture: { data: { url: string } };
  created_time: string;
}

// Adapters
class GitHubUserAdapter {
  static adapt(githubUser: GitHubUser): NormalizedUser {
    return {
      id: githubUser.login,
      name: githubUser.name || githubUser.login,
      email: githubUser.email || '',
      avatar: githubUser.avatar_url,
      createdAt: new Date(githubUser.created_at)
    };
  }
}

class GoogleUserAdapter {
  static adapt(googleUser: GoogleUser): NormalizedUser {
    return {
      id: googleUser.id,
      name: googleUser.displayName,
      email: googleUser.emails[0]?.value || '',
      avatar: googleUser.image.url,
      createdAt: new Date(googleUser.created)
    };
  }
}

class FacebookUserAdapter {
  static adapt(facebookUser: FacebookUser): NormalizedUser {
    return {
      id: facebookUser.id,
      name: facebookUser.name,
      email: facebookUser.email,
      avatar: facebookUser.picture.data.url,
      createdAt: new Date(facebookUser.created_time)
    };
  }
}

// Client code
class UserService {
  async handleOAuthUser(provider: string, rawData: any): Promise<NormalizedUser> {
    let normalizedUser: NormalizedUser;

    switch (provider) {
      case 'github':
        normalizedUser = GitHubUserAdapter.adapt(rawData);
        break;
      case 'google':
        normalizedUser = GoogleUserAdapter.adapt(rawData);
        break;
      case 'facebook':
        normalizedUser = FacebookUserAdapter.adapt(rawData);
        break;
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }

    // Now we can use the normalized user
    return this.processUser(normalizedUser);
  }

  private async processUser(user: NormalizedUser): Promise<NormalizedUser> {
    // Process user with consistent interface
    return user;
  }
}

```

### Database Adapter

```typescript
// Target interface
interface Database {
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  query<T>(sql: string, params?: any[]): Promise<T[]>;
  insert(table: string, data: Record<string, any>): Promise<any>;
  update(table: string, id: string, data: Record<string, any>): Promise<any>;
  delete(table: string, id: string): Promise<boolean>;
}

// PostgreSQL implementation
class PostgreSQLDatabase {
  private pool: any;

  async connect(): Promise<void> {
    console.log('Connecting to PostgreSQL...');
    // PostgreSQL specific connection
  }

  async disconnect(): Promise<void> {
    console.log('Disconnecting from PostgreSQL...');
  }

  async queryPostgres<T>(sql: string, params?: any[]): Promise<T[]> {
    console.log(`PostgreSQL query: ${sql}`);
    return [];
  }

  async insertPostgres(table: string, data: Record<string, any>): Promise<any> {
    console.log(`PostgreSQL insert into ${table}`);
    return { id: 1 };
  }
}

// MongoDB implementation
class MongoDBDatabase {
  private client: any;

  async connect(): Promise<void> {
    console.log('Connecting to MongoDB...');
  }

  async disconnect(): Promise<void> {
    console.log('Disconnecting from MongoDB...');
  }

  async find<T>(collection: string, filter?: any): Promise<T[]> {
    console.log(`MongoDB find in ${collection}`);
    return [];
  }

  async insertOne(collection: string, document: any): Promise<any> {
    console.log(`MongoDB insert into ${collection}`);
    return { insertedId: '1' };
  }
}

// Adapters
class PostgreSQLAdapter implements Database {
  private db: PostgreSQLDatabase;

  constructor(db: PostgreSQLDatabase) {
    this.db = db;
  }

  async connect(): Promise<void> {
    return this.db.connect();
  }

  async disconnect(): Promise<void> {
    return this.db.disconnect();
  }

  async query<T>(sql: string, params?: any[]): Promise<T[]> {
    return this.db.queryPostgres<T>(sql, params);
  }

  async insert(table: string, data: Record<string, any>): Promise<any> {
    return this.db.insertPostgres(table, data);
  }

  async update(table: string, id: string, data: Record<string, any>): Promise<any> {
    const sql = `UPDATE ${table} SET ${Object.keys(data).map(k => `${k} = $${k}`).join(', ')} WHERE id = $id`;
    return this.db.queryPostgres(sql, { ...data, id });
  }

  async delete(table: string, id: string): Promise<boolean> {
    const sql = `DELETE FROM ${table} WHERE id = $id`;
    await this.db.queryPostgres(sql, { id });
    return true;
  }
}

class MongoDBAdapter implements Database {
  private db: MongoDBDatabase;

  constructor(db: MongoDBDatabase) {
    this.db = db;
  }

  async connect(): Promise<void> {
    return this.db.connect();
  }

  async disconnect(): Promise<void> {
    return this.db.disconnect();
  }

  async query<T>(sql: string, params?: any[]): Promise<T[]> {
    // Convert SQL-like query to MongoDB format
    console.log(`Converting query: ${sql}`);
    return this.db.find<T>('collection');
  }

  async insert(table: string, data: Record<string, any>): Promise<any> {
    return this.db.insertOne(table, data);
  }

  async update(table: string, id: string, data: Record<string, any>): Promise<any> {
    console.log(`MongoDB update ${table} where id = ${id}`);
    return { modifiedCount: 1 };
  }

  async delete(table: string, id: string): Promise<boolean> {
    console.log(`MongoDB delete ${table} where id = ${id}`);
    return true;
  }
}

// Client code
class UserRepository {
  constructor(private database: Database) {}

  async findById(id: string): Promise<any> {
    const results = await this.database.query('SELECT * FROM users WHERE id = $1', [id]);
    return results[0];
  }

  async create(data: Record<string, any>): Promise<any> {
    return this.database.insert('users', data);
  }
}

// Usage
const pgAdapter = new PostgreSQLAdapter(new PostgreSQLDatabase());
const mongoAdapter = new MongoDBAdapter(new MongoDBDatabase());

const pgRepo = new UserRepository(pgAdapter);
const mongoRepo = new UserRepository(mongoAdapter);

```

### Payment Gateway Adapter

```typescript
// Target interface
interface PaymentProcessor {
  charge(amount: number, currency: string, cardToken: string): Promise<PaymentResult>;
  refund(transactionId: string, amount?: number): Promise<RefundResult>;
  getTransaction(transactionId: string): Promise<Transaction>;
}

interface PaymentResult {
  success: boolean;
  transactionId: string;
  error?: string;
}

interface RefundResult {
  success: boolean;
  refundId: string;
  error?: string;
}

interface Transaction {
  id: string;
  amount: number;
  currency: string;
  status: string;
  createdAt: Date;
}

// Different payment gateway APIs
class StripeAPI {
  async createCharge(params: {
    amount: number;
    currency: string;
    source: string;
  }): Promise<{ id: string; status: string }> {
    console.log(`Stripe: Charging ${params.amount} ${params.currency}`);
    return { id: 'stripe_' + Date.now(), status: 'succeeded' };
  }

  async createRefund(params: {
    charge: string;
    amount?: number;
  }): Promise<{ id: string; status: string }> {
    console.log(`Stripe: Refunding ${params.charge}`);
    return { id: 'refund_' + Date.now(), status: 'succeeded' };
  }

  async retrieveCharge(id: string): Promise<{
    id: string;
    amount: number;
    currency: string;
    status: string;
    created: number;
  }> {
    return {
      id,
      amount: 1000,
      currency: 'usd',
      status: 'succeeded',
      created: Date.now()
    };
  }
}

class PayPalAPI {
  async createPayment(params: {
    intent: string;
    amount: string;
    currency: string;
    payment_method: string;
  }): Promise<{ id: string; state: string }> {
    console.log(`PayPal: Creating payment ${params.amount} ${params.currency}`);
    return { id: 'paypal_' + Date.now(), state: 'approved' };
  }

  async executePayment(paymentId: string): Promise<{ id: string; state: string }> {
    console.log(`PayPal: Executing payment ${paymentId}`);
    return { id: paymentId, state: 'completed' };
  }

  async refundPayment(paymentId: string): Promise<{ id: string; state: string }> {
    console.log(`PayPal: Refunding payment ${paymentId}`);
    return { id: 'refund_' + Date.now(), state: 'completed' };
  }

  async getPaymentDetails(paymentId: string): Promise<{
    id: string;
    amount: { total: string; currency: string };
    state: string;
    create_time: string;
  }> {
    return {
      id: paymentId,
      amount: { total: '10.00', currency: 'USD' },
      state: 'completed',
      create_time: new Date().toISOString()
    };
  }
}

// Adapters
class StripeAdapter implements PaymentProcessor {
  private stripe: StripeAPI;

  constructor(stripe: StripeAPI) {
    this.stripe = stripe;
  }

  async charge(amount: number, currency: string, cardToken: string): Promise<PaymentResult> {
    try {
      const result = await this.stripe.createCharge({
        amount: Math.round(amount * 100), // Stripe uses cents
        currency: currency.toLowerCase(),
        source: cardToken
      });

      return {
        success: result.status === 'succeeded',
        transactionId: result.id
      };
    } catch (error) {
      return {
        success: false,
        transactionId: '',
        error: error.message
      };
    }
  }

  async refund(transactionId: string, amount?: number): Promise<RefundResult> {
    try {
      const result = await this.stripe.createRefund({
        charge: transactionId,
        amount: amount ? Math.round(amount * 100) : undefined
      });

      return {
        success: result.status === 'succeeded',
        refundId: result.id
      };
    } catch (error) {
      return {
        success: false,
        refundId: '',
        error: error.message
      };
    }
  }

  async getTransaction(transactionId: string): Promise<Transaction> {
    const result = await this.stripe.retrieveCharge(transactionId);

    return {
      id: result.id,
      amount: result.amount / 100, // Convert from cents
      currency: result.currency.toUpperCase(),
      status: result.status,
      createdAt: new Date(result.created * 1000)
    };
  }
}

class PayPalAdapter implements PaymentProcessor {
  private paypal: PayPalAPI;

  constructor(paypal: PayPalAPI) {
    this.paypal = paypal;
  }

  async charge(amount: number, currency: string, cardToken: string): Promise<PaymentResult> {
    try {
      const payment = await this.paypal.createPayment({
        intent: 'sale',
        amount: amount.toString(),
        currency: currency,
        payment_method: cardToken
      });

      const executed = await this.paypal.executePayment(payment.id);

      return {
        success: executed.state === 'completed',
        transactionId: executed.id
      };
    } catch (error) {
      return {
        success: false,
        transactionId: '',
        error: error.message
      };
    }
  }

  async refund(transactionId: string, amount?: number): Promise<RefundResult> {
    try {
      const result = await this.paypal.refundPayment(transactionId);

      return {
        success: result.state === 'completed',
        refundId: result.id
      };
    } catch (error) {
      return {
        success: false,
        refundId: '',
        error: error.message
      };
    }
  }

  async getTransaction(transactionId: string): Promise<Transaction> {
    const result = await this.paypal.getPaymentDetails(transactionId);

    return {
      id: result.id,
      amount: parseFloat(result.amount.total),
      currency: result.amount.currency,
      status: result.state,
      createdAt: new Date(result.create_time)
    };
  }
}

// Client code
class OrderService {
  constructor(private paymentProcessor: PaymentProcessor) {}

  async processPayment(orderId: string, amount: number, currency: string, cardToken: string): Promise<boolean> {
    const result = await this.paymentProcessor.charge(amount, currency, cardToken);

    if (result.success) {
      console.log(`Payment successful for order ${orderId}`);
      return true;
    } else {
      console.log(`Payment failed for order ${orderId}: ${result.error}`);
      return false;
    }
  }
}

// Usage
const stripe = new StripeAdapter(new StripeAPI());
const paypal = new PayPalAdapter(new PayPalAPI());

const orderService1 = new OrderService(stripe);
const orderService2 = new OrderService(paypal);

```

## Real-World Use Cases

### 1. Third-Party Service Integration

```typescript
// Target interface
interface EmailService {
  send(to: string, subject: string, body: string): Promise<boolean>;
  sendBulk(recipients: string[], subject: string, body: string): Promise<boolean[]>;
}

// Different email services
class SendGridAPI {
  async sendEmail(params: {
    to: string;
    from: string;
    subject: string;
    html: string;
  }): Promise<{ statusCode: number; messageId: string }> {
    console.log(`SendGrid: Sending email to ${params.to}`);
    return { statusCode: 202, messageId: 'sg_' + Date.now() };
  }

  async sendBatchEmail(params: {
    personalizations: Array<{ to: Array<{ email: string }> }>;
    from: { email: string };
    subject: string;
    content: Array<{ type: string; value: string }>;
  }): Promise<{ statusCode: number }> {
    console.log(`SendGrid: Sending batch email`);
    return { statusCode: 202 };
  }
}

class MailgunAPI {
  async sendMailgun(params: {
    to: string;
    from: string;
    subject: string;
    text: string;
    html: string;
  }): Promise<{ id: string; message: string }> {
    console.log(`Mailgun: Sending email to ${params.to}`);
    return { id: 'mg_' + Date.now(), message: 'Queued' };
  }

  async sendMailgunBulk(params: {
    to: string[];
    from: string;
    subject: string;
    text: string;
    html: string;
  }): Promise<{ id: string; message: string }> {
    console.log(`Mailgun: Sending bulk email`);
    return { id: 'mg_bulk_' + Date.now(), message: 'Queued' };
  }
}

// Adapters
class SendGridAdapter implements EmailService {
  constructor(private sendgrid: SendGridAPI) {}

  async send(to: string, subject: string, body: string): Promise<boolean> {
    try {
      const result = await this.sendgrid.sendEmail({
        to,
        from: 'noreply@example.com',
        subject,
        html: body
      });
      return result.statusCode === 202;
    } catch {
      return false;
    }
  }

  async sendBulk(recipients: string[], subject: string, body: string): Promise<boolean[]> {
    try {
      await this.sendgrid.sendBatchEmail({
        personalizations: recipients.map(to => ({ to: [{ email: to }] })),
        from: { email: 'noreply@example.com' },
        subject,
        content: [{ type: 'text/html', value: body }]
      });
      return recipients.map(() => true);
    } catch {
      return recipients.map(() => false);
    }
  }
}

class MailgunAdapter implements EmailService {
  constructor(private mailgun: MailgunAPI) {}

  async send(to: string, subject: string, body: string): Promise<boolean> {
    try {
      const result = await this.mailgun.sendMailgun({
        to,
        from: 'noreply@example.com',
        subject,
        text: body,
        html: body
      });
      return result.id.startsWith('mg_');
    } catch {
      return false;
    }
  }

  async sendBulk(recipients: string[], subject: string, body: string): Promise<boolean[]> {
    try {
      await this.mailgun.sendMailgunBulk({
        to: recipients,
        from: 'noreply@example.com',
        subject,
        text: body,
        html: body
      });
      return recipients.map(() => true);
    } catch {
      return recipients.map(() => false);
    }
  }
}

```

### 2. Legacy System Integration

```typescript
// Target interface
interface ModernInventorySystem {
  getStock(productId: string): Promise<number>;
  updateStock(productId: string, quantity: number): Promise<boolean>;
  getAllProducts(): Promise<Product[]>;
}

interface Product {
  id: string;
  name: string;
  stock: number;
  price: number;
}

// Legacy system with different interface
class LegacyInventorySystem {
  private inventory: Map<string, { qty: number; desc: string; cost: number }> = new Map();

  async checkItemAvailability(itemId: string): Promise<string> {
    const item = this.inventory.get(itemId);
    return item ? `AVAILABLE:${item.qty}` : 'NOT_FOUND';
  }

  async modifyItemQuantity(itemId: string, newQty: number): Promise<string> {
    const item = this.inventory.get(itemId);
    if (item) {
      item.qty = newQty;
      return 'SUCCESS';
    }
    return 'ITEM_NOT_FOUND';
  }

  async listItemCatalog(): Promise<string> {
    const items = Array.from(this.inventory.entries())
      .map(([id, item]) => `${id}:${item.desc}:${item.qty}:${item.cost}`)
      .join('|');
    return items || 'EMPTY';
  }
}

// Adapter
class LegacyInventoryAdapter implements ModernInventorySystem {
  constructor(private legacySystem: LegacyInventorySystem) {}

  async getStock(productId: string): Promise<number> {
    const result = await this.legacySystem.checkItemAvailability(productId);

    if (result.startsWith('AVAILABLE:')) {
      return parseInt(result.split(':')[1]);
    }

    throw new Error(`Product ${productId} not found`);
  }

  async updateStock(productId: string, quantity: number): Promise<boolean> {
    const result = await this.legacySystem.modifyItemQuantity(productId, quantity);
    return result === 'SUCCESS';
  }

  async getAllProducts(): Promise<Product[]> {
    const catalogString = await this.legacySystem.listItemCatalog();

    if (catalogString === 'EMPTY') {
      return [];
    }

    return catalogString.split('|').map(item => {
      const [id, name, qty, cost] = item.split(':');
      return {
        id,
        name,
        stock: parseInt(qty),
        price: parseFloat(cost)
      };
    });
  }
}

// Client code
class InventoryService {
  constructor(private inventorySystem: ModernInventorySystem) {}

  async checkAndReorder(productId: string, threshold: number): Promise<boolean> {
    const stock = await this.inventorySystem.getStock(productId);

    if (stock < threshold) {
      console.log(`Low stock for ${productId}: ${stock}`);
      await this.inventorySystem.updateStock(productId, threshold * 2);
      return true;
    }

    return false;
  }
}

```

### 3. XML to JSON Adapter

```typescript
// Target interface
interface DataParser {
  parse(data: string): any;
  stringify(data: any): string;
}

// XML Parser (incompatible interface)
class XMLParser {
  parseXML(xml: string): any {
    console.log('Parsing XML...');
    // Simulate XML parsing
    return { root: { item: 'value' } };
  }

  toXML(data: any): string {
    console.log('Converting to XML...');
    return '<root><item>value</item></root>';
  }
}

// JSON Parser
class JSONParser {
  parseJSON(json: string): any {
    return JSON.parse(json);
  }

  toJSON(data: any): string {
    return JSON.stringify(data, null, 2);
  }
}

// Adapter
class XMLtoJSONAdapter implements DataParser {
  private xmlParser: XMLParser;

  constructor(xmlParser: XMLParser) {
    this.xmlParser = xmlParser;
  }

  parse(data: string): any {
    // Check if data is XML
    if (data.trim().startsWith('<')) {
      return this.xmlParser.parseXML(data);
    }

    // If it's JSON, parse directly
    return JSON.parse(data);
  }

  stringify(data: any): string {
    // Convert to XML
    return this.xmlParser.toXML(data);
  }
}

// Client code
class ConfigurationManager {
  constructor(private parser: DataParser) {}

  loadConfig(configData: string): any {
    return this.parser.parse(configData);
  }

  saveConfig(config: any): string {
    return this.parser.stringify(config);
  }
}

// Usage
const xmlParser = new XMLParser();
const adapter = new XMLtoJSONAdapter(xmlParser);
const configManager = new ConfigurationManager(adapter);

const config = configManager.loadConfig('<config><db>localhost</db></config>');
console.log(config);

```

## Common Mistakes

### 1. Over-Adapting

```typescript
// ❌ BAD - Creating adapters for everything
class SimpleAdapter {
  // Adapting something that could be easily modified
}

```

### 2. Adapter with Too Much Logic

```typescript
// ❌ BAD - Adapter doing business logic
class BadAdapter {
  adapt(data: any): any {
    // Also validates, transforms, and saves
    // Should only adapt interface
  }
}

```

### 3. Not Using Interface

```typescript
// ❌ BAD - No common interface
class XMLAdapter {
  convert(data: string): any { ... }
}

class JSONAdapter {
  convert(data: string): any { ... }
}

// These adapters have no common interface

```

### 4. Tight Coupling

```typescript
// ❌ BAD - Adapter depends on concrete implementation
class BadAdapter {
  private specificImplementation: SpecificClass;

  constructor() {
    this.specificImplementation = new SpecificClass();
  }
}

```

## Best Practices

### 1. Use Interface for Adapters

```typescript
// ✅ GOOD - Common interface
interface Parser {
  parse(data: string): any;
  stringify(data: any): string;
}

class XMLParserAdapter implements Parser {
  parse(data: string): any { ... }
  stringify(data: any): string { ... }
}

class JSONParserAdapter implements Parser {
  parse(data: string): any { ... }
  stringify(data: any): string { ... }
}

```

### 2. Keep Adapters Focused

```typescript
// ✅ GOOD - Single responsibility
class UserAdapter {
  adaptUser(externalUser: ExternalUser): User {
    // Only adapts user data
  }
}

class OrderAdapter {
  adaptOrder(externalOrder: ExternalOrder): Order {
    // Only adapts order data
  }
}

```

### 3. Use Dependency Injection

```typescript
// ✅ GOOD - Injectable adapters
class Service {
  constructor(private adapter: Adapter) {}
}

// In dependency injection container
container.register('adapter', new SpecificAdapter());

```

### 4. Make Adapters Stateless

```typescript
// ✅ GOOD - Stateless adapters
class StatelessAdapter {
  static adapt(data: any): any {
    // Pure function, no state
  }
}

```

## Performance Considerations

1. **Conversion Overhead**: Adapters add conversion overhead; consider caching if conversion is expensive.

2. **Memory Usage**: Adapters are usually lightweight; the adapted objects consume memory.

3. **Batch Operations**: Implement batch adaptation for better performance.

4. **Lazy Adaptation**: Consider lazy adaptation if adaptation is expensive.

5. **Caching**: Cache adapted results if the same data is adapted multiple times.

## Interview Questions

### Beginner

1. **What is the Adapter pattern?**

   - A structural pattern that allows objects with incompatible interfaces to collaborate.

2. **When would you use Adapter pattern?**

   - When integrating third-party libraries, legacy systems, or APIs with different interfaces.

3. **What's the difference between Adapter and Facade?**

   - Adapter makes one interface compatible; Facade simplifies a complex system.

4. **How do you implement Adapter in TypeScript?**

   - Create an adapter class that implements the target interface and wraps the adaptee.

5. **What are the benefits of Adapter pattern?**

   - Reusability, flexibility, and separation of concerns.

### Intermediate

6. **What's the difference between Object Adapter and Class Adapter?**

   - Object Adapter uses composition; Class Adapter uses inheritance.

7. **Can Adapter add functionality?**

   - Yes, but keep it focused on interface adaptation, not business logic.

8. **How do you test Adapter pattern?**

   - Mock the adaptee, test the adapter's interface implementation.

9. **What's the relationship between Adapter and Decorator?**

   - Adapter changes interface; Decorator adds behavior while keeping interface.

10. **How do you handle multiple adaptees?**

    - Create separate adapters for each adaptee or use a compound adapter.

### Senior

11. **How does Adapter pattern affect scalability?**

    - Adapters are lightweight; the adapted objects can be optimized.

12. **What are the SOLID violations with Adapter?**

    - Usually follows SOLID; watch for adapters violating Single Responsibility.

13. **How do you handle Adapter in microservices?**

    - Use adapters for API integration, protocol translation, and data transformation.

14. **What are the memory implications of Adapter?**

    - Adapters are usually stateless; the adapted objects consume memory.

15. **How do you refactor Adapter code?**

    - Extract common logic, use composition, and apply SOLID principles.

### FAANG-style

16. **Design an Adapter for a legacy system.**

    - Consider backward compatibility, error handling, and performance.

17. **How would you implement Adapter for distributed systems?**

    - Consider network transparency, serialization, and fault tolerance.

18. **What are the implications of Adapter in cloud-native applications?**

    - Consider serverless functions, API gateways, and protocol translation.

19. **How do you handle Adapter in event-driven architectures?**

    - Use adapters for event transformation and protocol translation.

20. **Design an Adapter that supports versioning.**

    - Consider backward compatibility, version negotiation, and migration.

### Follow-ups

21. **Can Adapter pattern be combined with other patterns?**

    - Yes, commonly with Factory, Decorator, and Proxy patterns.

22. **How do you handle Adapter in testing frameworks?**

    - Use dependency injection, create test adapters, and mock implementations.

23. **What are the memory implications of Adapter pattern?**

    - Adapters are usually lightweight; the adapted objects consume memory.

24. **How do you handle Adapter in serverless environments?**

    - Consider stateless design, cold starts, and protocol translation.

25. **What's the impact of Adapter on code maintainability?**

    - Improves maintainability by decoupling systems and centralizing adaptation logic.

## Summary

The Adapter pattern is essential for integrating incompatible interfaces. It allows you to reuse existing code, integrate third-party libraries, and maintain clean architecture. Use it when you need to bridge different interfaces without modifying existing code.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           ADAPTER PATTERN                   │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Integrating third-party libraries         │
│ • Legacy system integration                 │
│ • API translation                           │
│ • Protocol conversion                       │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Interfaces are compatible                 │
│ • Adapter adds unnecessary complexity       │
│ • Performance is critical                   │
│ • Simple conversion is enough               │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Target interface                          │
│ • Adaptee (incompatible interface)          │
│ • Adapter wraps adaptee                     │
│ • Interface translation                     │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Over-adapting                             │
│ • Adapter with too much logic               │
│ • Tight coupling                            │
│ • Not using interface                       │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Facade (simplifies interface)             │
│ • Decorator (adds behavior)                 │
│ • Proxy (controls access)                   │
└─────────────────────────────────────────────┘

```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Adapter](https://refactoring.guru/design-patterns/adapter)
- [Adapter Pattern Examples](https://www.patterns.dev/posts/adapter-pattern/)
