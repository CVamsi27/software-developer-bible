# CQRS & Dependency Injection Patterns

## Definition

### CQRS (Command Query Responsibility Segregation)

CQRS is an architectural pattern that separates read and write operations into different models. Commands update the state and return void, while Queries return data without modifying state. This separation allows for independent optimization, scaling, and evolution of read and write sides.

### Dependency Injection (DI)

Dependency Injection is a design pattern where an object receives its dependencies from external sources rather than creating them itself. It's a form of Inversion of Control (IoC) that promotes loose coupling and testability.

## Why Do We Need Them?

### CQRS Benefits:
1. **Independent Scaling**: Read and write sides can be scaled independently
2. **Optimized Models**: Different models for reads and writes
3. **Flexibility**: Different storage technologies for different needs
4. **Performance**: Optimized queries without affecting write operations

### DI Benefits:
1. **Loose Coupling**: Classes don't create their dependencies
2. **Testability**: Easy to mock dependencies for testing
3. **Flexibility**: Easy to swap implementations
4. **Maintainability**: Changes in dependencies don't affect dependents

## How They Work

### CQRS Architecture:

```
┌─────────────────────────────────────────────────┐
│              CQRS Pattern                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐      ┌──────────────┐         │
│  │   Command     │      │   Query      │         │
│  │   Side        │      │   Side       │         │
│  └──────────────┘      └──────────────┘         │
│         │                       │                │
│         ▼                       ▼                │
│  ┌──────────────┐      ┌──────────────┐         │
│  │   Write       │      │   Read       │         │
│  │   Database    │      │   Database   │         │
│  └──────────────┘      └──────────────┘         │
│         │                       │                │
│         └───────────┬───────────┘                │
│                     │                            │
│                     ▼                            │
│  ┌──────────────────────────────────────────┐   │
│  │         Event Bus / Synchronization      │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### DI Container:

```
┌─────────────────────────────────────────────────┐
│           Dependency Injection                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │◄── Receives dependencies      │
│  └──────────────┘                               │
│         │                                       │
│         │ Constructor injection                  │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         DI Container                     │   │
│  │    + register<T>(token, factory): void   │   │
│  │    + resolve<T>(token): T                │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Dependencies                     │   │
│  │    - ServiceA: IServiceA                 │   │
│  │    - ServiceB: IServiceB                 │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## Code Examples

### CQRS Implementation

```typescript
// Commands
interface Command {
  execute(): Promise<void>;
}

interface CommandHandler<T extends Command> {
  handle(command: T): Promise<void>;
}

// Queries
interface Query<TResult> {
  execute(): Promise<TResult>;
}

interface QueryHandler<T extends Query<TResult>, TResult> {
  handle(query: T): Promise<TResult>;
}

// Domain Events
interface DomainEvent {
  type: string;
  timestamp: Date;
  payload: any;
}

// Event Store
class EventStore {
  private events: DomainEvent[] = [];

  append(event: DomainEvent): void {
    this.events.push(event);
  }

  getEvents(aggregateId: string): DomainEvent[] {
    return this.events.filter(e => e.payload.aggregateId === aggregateId);
  }

  getAllEvents(): DomainEvent[] {
    return [...this.events];
  }
}

// Write Model
class User {
  constructor(
    public id: string,
    public name: string,
    public email: string,
    public isActive: boolean = true,
    public version: number = 0
  ) {}

  static create(id: string, name: string, email: string): User {
    return new User(id, name, email);
  }

  deactivate(): void {
    this.isActive = false;
    this.version++;
  }

  updateProfile(name: string, email: string): void {
    this.name = name;
    this.email = email;
    this.version++;
  }
}

// Write Repository
class UserWriteRepository {
  private users: Map<string, User> = new Map();

  save(user: User): void {
    this.users.set(user.id, user);
  }

  findById(id: string): User | undefined {
    return this.users.get(id);
  }
}

// Read Model
interface UserReadModel {
  id: string;
  name: string;
  email: string;
  isActive: boolean;
  lastUpdated: Date;
}

// Read Repository
class UserReadRepository {
  private users: Map<string, UserReadModel> = new Map();

  findById(id: string): UserReadModel | undefined {
    return this.users.get(id);
  }

  findAll(): UserReadModel[] {
    return Array.from(this.users.values());
  }

  findByEmail(email: string): UserReadModel | undefined {
    return Array.from(this.users.values()).find(u => u.email === email);
  }

  update(user: UserReadModel): void {
    this.users.set(user.id, user);
  }

  delete(id: string): void {
    this.users.delete(id);
  }
}

// Command Handlers
class CreateUserCommand implements Command {
  constructor(
    public id: string,
    public name: string,
    public email: string
  ) {}

  execute(): Promise<void> {
    return Promise.resolve();
  }
}

class CreateUserCommandHandler implements CommandHandler<CreateUserCommand> {
  constructor(
    private writeRepository: UserWriteRepository,
    private readRepository: UserReadRepository,
    private eventStore: EventStore
  ) {}

  async handle(command: CreateUserCommand): Promise<void> {
    // Create user in write model
    const user = User.create(command.id, command.name, command.email);
    this.writeRepository.save(user);

    // Update read model
    this.readRepository.update({
      id: user.id,
      name: user.name,
      email: user.email,
      isActive: user.isActive,
      lastUpdated: new Date()
    });

    // Store event
    this.eventStore.append({
      type: 'UserCreated',
      timestamp: new Date(),
      payload: {
        aggregateId: user.id,
        name: user.name,
        email: user.email
      }
    });

    console.log(`User created: ${user.id}`);
  }
}

class DeactivateUserCommand implements Command {
  constructor(public userId: string) {}

  execute(): Promise<void> {
    return Promise.resolve();
  }
}

class DeactivateUserCommandHandler implements CommandHandler<DeactivateUserCommand> {
  constructor(
    private writeRepository: UserWriteRepository,
    private readRepository: UserReadRepository,
    private eventStore: EventStore
  ) {}

  async handle(command: DeactivateUserCommand): Promise<void> {
    const user = this.writeRepository.findById(command.userId);

    if (!user) {
      throw new Error(`User ${command.userId} not found`);
    }

    user.deactivate();
    this.writeRepository.save(user);

    // Update read model
    const readModel = this.readRepository.findById(command.userId);
    if (readModel) {
      this.readRepository.update({
        ...readModel,
        isActive: false,
        lastUpdated: new Date()
      });
    }

    // Store event
    this.eventStore.append({
      type: 'UserDeactivated',
      timestamp: new Date(),
      payload: {
        aggregateId: user.id
      }
    });

    console.log(`User deactivated: ${user.id}`);
  }
}

// Query Handlers
class GetUserQuery implements Query<UserReadModel | undefined> {
  constructor(public userId: string) {}

  execute(): Promise<UserReadModel | undefined> {
    return Promise.resolve(undefined);
  }
}

class GetUserQueryHandler implements QueryHandler<GetUserQuery, UserReadModel | undefined> {
  constructor(private readRepository: UserReadRepository) {}

  async handle(query: GetUserQuery): Promise<UserReadModel | undefined> {
    return this.readRepository.findById(query.userId);
  }
}

class GetAllUsersQuery implements Query<UserReadModel[]> {
  execute(): Promise<UserReadModel[]> {
    return Promise.resolve([]);
  }
}

class GetAllUsersQueryHandler implements QueryHandler<GetAllUsersQuery, UserReadModel[]> {
  constructor(private readRepository: UserReadRepository) {}

  async handle(query: GetAllUsersQuery): Promise<UserReadModel[]> {
    return this.readRepository.findAll();
  }
}

// CQRS Bus
class CommandBus {
  private handlers: Map<string, CommandHandler<any>> = new Map();

  registerHandler<T extends Command>(
    commandType: string,
    handler: CommandHandler<T>
  ): void {
    this.handlers.set(commandType, handler);
  }

  async dispatch<T extends Command>(command: T): Promise<void> {
    const handler = this.handlers.get(command.constructor.name);

    if (!handler) {
      throw new Error(`No handler for command: ${command.constructor.name}`);
    }

    await handler.handle(command);
  }
}

class QueryBus {
  private handlers: Map<string, QueryHandler<any, any>> = new Map();

  registerHandler<T extends Query<TResult>, TResult>(
    queryType: string,
    handler: QueryHandler<T, TResult>
  ): void {
    this.handlers.set(queryType, handler);
  }

  async dispatch<T extends Query<TResult>, TResult>(query: T): Promise<TResult> {
    const handler = this.handlers.get(query.constructor.name);

    if (!handler) {
      throw new Error(`No handler for query: ${query.constructor.name}`);
    }

    return handler.handle(query);
  }
}

// Client code
async function main() {
  // Setup
  const eventStore = new EventStore();
  const writeRepository = new UserWriteRepository();
  const readRepository = new UserReadRepository();

  const commandBus = new CommandBus();
  const queryBus = new QueryBus();

  // Register handlers
  commandBus.registerHandler(
    'CreateUserCommand',
    new CreateUserCommandHandler(writeRepository, readRepository, eventStore)
  );

  commandBus.registerHandler(
    'DeactivateUserCommand',
    new DeactivateUserCommandHandler(writeRepository, readRepository, eventStore)
  );

  queryBus.registerHandler(
    'GetUserQuery',
    new GetUserQueryHandler(readRepository)
  );

  queryBus.registerHandler(
    'GetAllUsersQuery',
    new GetAllUsersQueryHandler(readRepository)
  );

  // Execute commands
  await commandBus.dispatch(new CreateUserCommand('1', 'John', 'john@example.com'));
  await commandBus.dispatch(new CreateUserCommand('2', 'Jane', 'jane@example.com'));

  // Execute queries
  const user = await queryBus.dispatch(new GetUserQuery('1'));
  console.log('User:', user);

  const allUsers = await queryBus.dispatch(new GetAllUsersQuery());
  console.log('All users:', allUsers);

  // Deactivate user
  await commandBus.dispatch(new DeactivateUserCommand('1'));

  const deactivatedUser = await queryBus.dispatch(new GetUserQuery('1'));
  console.log('Deactivated user:', deactivatedUser);
}

main();
```

### Dependency Injection Container

```typescript
// DI Container implementation
type Factory<T> = () => T;
type Token = string | symbol | Function;

class DIContainer {
  private factories: Map<Token, Factory<any>> = new Map();
  private singletons: Map<Token, any> = new Map();

  register<T>(token: Token, factory: Factory<T>, singleton: boolean = false): void {
    this.factories.set(token, factory);

    if (singleton) {
      const instance = factory();
      this.singletons.set(token, instance);
    }
  }

  resolve<T>(token: Token): T {
    // Check for singleton first
    if (this.singletons.has(token)) {
      return this.singletons.get(token) as T;
    }

    const factory = this.factories.get(token);

    if (!factory) {
      throw new Error(`No registration for token: ${String(token)}`);
    }

    return factory() as T;
  }

  has(token: Token): boolean {
    return this.factories.has(token) || this.singletons.has(token);
  }

  clear(): void {
    this.factories.clear();
    this.singletons.clear();
  }
}

// Service interfaces
interface ILogger {
  log(message: string): void;
  error(message: string): void;
  warn(message: string): void;
}

interface IConfig {
  get(key: string): string;
  getAll(): Record<string, string>;
}

interface IDatabase {
  query<T>(sql: string): Promise<T[]>;
  execute(sql: string): Promise<void>;
}

interface IUserService {
  getUser(id: string): Promise<any>;
  createUser(data: any): Promise<any>;
}

// Concrete implementations
class ConsoleLogger implements ILogger {
  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }

  error(message: string): void {
    console.error(`[ERROR] ${message}`);
  }

  warn(message: string): void {
    console.warn(`[WARN] ${message}`);
  }
}

class EnvironmentConfig implements IConfig {
  private config: Record<string, string>;

  constructor() {
    this.config = {
      DATABASE_URL: process.env.DATABASE_URL || 'localhost',
      PORT: process.env.PORT || '3000',
      NODE_ENV: process.env.NODE_ENV || 'development'
    };
  }

  get(key: string): string {
    return this.config[key] || '';
  }

  getAll(): Record<string, string> {
    return { ...this.config };
  }
}

class PostgreSQLDatabase implements IDatabase {
  constructor(private config: IConfig) {}

  async query<T>(sql: string): Promise<T[]> {
    console.log(`Executing query: ${sql}`);
    return [] as T[];
  }

  async execute(sql: string): Promise<void> {
    console.log(`Executing: ${sql}`);
  }
}

class UserService implements IUserService {
  constructor(
    private database: IDatabase,
    private logger: ILogger
  ) {}

  async getUser(id: string): Promise<any> {
    this.logger.log(`Getting user ${id}`);
    const results = await this.database.query('SELECT * FROM users WHERE id = $1');
    return results[0];
  }

  async createUser(data: any): Promise<any> {
    this.logger.log('Creating user');
    await this.database.execute('INSERT INTO users ...');
    return { id: '1', ...data };
  }
}

// Setup DI Container
function setupDI(): DIContainer {
  const container = new DIContainer();

  // Register services
  container.register<ILogger>('Logger', () => new ConsoleLogger(), true);
  container.register<IConfig>('Config', () => new EnvironmentConfig(), true);

  container.register<IDatabase>('Database', () => {
    const config = container.resolve<IConfig>('Config');
    return new PostgreSQLDatabase(config);
  }, true);

  container.register<IUserService>('UserService', () => {
    const database = container.resolve<IDatabase>('Database');
    const logger = container.resolve<ILogger>('Logger');
    return new UserService(database, logger);
  }, true);

  return container;
}

// Client code
async function main() {
  const container = setupDI();

  const userService = container.resolve<IUserService>('UserService');

  await userService.getUser('1');
  await userService.createUser({ name: 'John' });
}

main();
```

### TypeScript Decorator-based DI

```typescript
// Metadata keys
const INJECTABLE_TOKEN = Symbol('injectable');
const INJECT_TOKEN = Symbol('inject');

// Injectable decorator
function Injectable() {
  return function (constructor: Function) {
    Reflect.defineMetadata(INJECTABLE_TOKEN, true, constructor);
  };
}

// Inject decorator
function Inject(token: symbol) {
  return function (target: any, propertyKey: string, parameterIndex: number) {
    const existingTokens = Reflect.getMetadata(INJECT_TOKEN, target, propertyKey) || [];
    existingTokens[parameterIndex] = token;
    Reflect.defineMetadata(INJECT_TOKEN, existingTokens, target, propertyKey);
  };
}

// DI Container with decorators
class Container {
  private static bindings: Map<symbol, any> = new Map();

  static bind<T>(token: symbol, implementation: new (...args: any[]) => T): void {
    this.bindings.set(token, implementation);
  }

  static resolve<T>(token: symbol): T {
    const implementation = this.bindings.get(token);

    if (!implementation) {
      throw new Error(`No binding for token: ${token.toString()}`);
    }

    // Get constructor parameter types
    const paramTypes = Reflect.getMetadata('design:paramtypes', implementation) || [];
    const injectTokens = Reflect.getMetadata(INJECT_TOKEN, implementation) || [];

    // Resolve dependencies
    const dependencies = paramTypes.map((type: any, index: number) => {
      const token = injectTokens[index];
      if (token) {
        return this.resolve(token);
      }
      return this.resolve(type);
    });

    return new implementation(...dependencies);
  }
}

// Usage
const LOGGER_TOKEN = Symbol('Logger');
const CONFIG_TOKEN = Symbol('Config');
const DATABASE_TOKEN = Symbol('Database');
const USER_SERVICE_TOKEN = Symbol('UserService');

class Logger {
  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }
}

class Config {
  get(key: string): string {
    return process.env[key] || '';
  }
}

class Database {
  constructor(
    @Inject(CONFIG_TOKEN) private config: Config,
    @Inject(LOGGER_TOKEN) private logger: Logger
  ) {}

  query<T>(sql: string): Promise<T[]> {
    this.logger.log(`Executing: ${sql}`);
    return Promise.resolve([] as T[]);
  }
}

class UserService {
  constructor(
    @Inject(DATABASE_TOKEN) private database: Database,
    @Inject(LOGGER_TOKEN) private logger: Logger
  ) {}

  async getUser(id: string): Promise<any> {
    this.logger.log(`Getting user ${id}`);
    return this.database.query('SELECT * FROM users WHERE id = $1');
  }
}

// Register and resolve
Container.bind(LOGGER_TOKEN, Logger);
Container.bind(CONFIG_TOKEN, Config);
Container.bind(DATABASE_TOKEN, Database);
Container.bind(USER_SERVICE_TOKEN, UserService);

const userService = Container.resolve<UserService>(USER_SERVICE_TOKEN);
```

### React Context DI

```typescript
import React, { createContext, useContext, ReactNode } from 'react';

// Service interfaces
interface IThemeContext {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

interface IAuthContext {
  user: any | null;
  login: (credentials: any) => Promise<void>;
  logout: () => void;
}

// Service implementations
const ThemeContext = createContext<IThemeContext | undefined>(undefined);
const AuthContext = createContext<IAuthContext | undefined>(undefined);

// Providers
function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = React.useState<any | null>(null);

  const login = async (credentials: any) => {
    // Simulate API call
    setUser({ id: '1', name: 'John' });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hooks for DI
function useTheme(): IThemeContext {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }

  return context;
}

function useAuth(): IAuthContext {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

// Component using DI
function UserProfile() {
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();

  return (
    <div className={`profile ${theme}`}>
      <h1>{user?.name}</h1>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

// App with providers
function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <UserProfile />
      </AuthProvider>
    </ThemeProvider>
  );
}
```

## Real-World Use Cases

### 1. E-commerce CQRS System

```typescript
// Write side - Commands
class PlaceOrderCommand {
  constructor(
    public userId: string,
    public items: Array<{ productId: string; quantity: number }>,
    public shippingAddress: any
  ) {}
}

class UpdateOrderStatusCommand {
  constructor(
    public orderId: string,
    public status: 'pending' | 'processing' | 'shipped' | 'delivered'
  ) {}
}

// Read side - Queries
class GetOrderQuery {
  constructor(public orderId: string) {}
}

class GetUserOrdersQuery {
  constructor(
    public userId: string,
    public page: number = 1,
    public limit: number = 10
  ) {}
}

class GetOrderStatisticsQuery {
  constructor(
    public startDate: Date,
    public endDate: Date
  ) {}
}

// Implementation
class OrderAggregate {
  private items: Array<{ productId: string; quantity: number; price: number }> = [];
  private status: string = 'pending';
  private total: number = 0;

  constructor(
    public id: string,
    public userId: string,
    public shippingAddress: any
  ) {}

  addItem(productId: string, quantity: number, price: number): void {
    this.items.push({ productId, quantity, price });
    this.total += quantity * price;
  }

  updateStatus(status: string): void {
    this.status = status;
  }

  getOrder(): any {
    return {
      id: this.id,
      userId: this.userId,
      items: this.items,
      status: this.status,
      total: this.total,
      shippingAddress: this.shippingAddress
    };
  }
}

class OrderWriteRepository {
  private orders: Map<string, OrderAggregate> = new Map();

  save(order: OrderAggregate): void {
    this.orders.set(order.id, order);
  }

  findById(id: string): OrderAggregate | undefined {
    return this.orders.get(id);
  }
}

class OrderReadRepository {
  private orders: Map<string, any> = new Map();

  save(order: any): void {
    this.orders.set(order.id, order);
  }

  findById(id: string): any {
    return this.orders.get(id);
  }

  findByUserId(userId: string, page: number, limit: number): any[] {
    const userOrders = Array.from(this.orders.values())
      .filter(o => o.userId === userId);

    return userOrders.slice((page - 1) * limit, page * limit);
  }

  getStatistics(startDate: Date, endDate: Date): any {
    const orders = Array.from(this.orders.values())
      .filter(o => {
        const orderDate = new Date(o.createdAt);
        return orderDate >= startDate && orderDate <= endDate;
      });

    return {
      totalOrders: orders.length,
      totalRevenue: orders.reduce((sum, o) => sum + o.total, 0),
      averageOrderValue: orders.length > 0
        ? orders.reduce((sum, o) => sum + o.total, 0) / orders.length
        : 0
    };
  }
}

// Command Handlers
class PlaceOrderCommandHandler {
  constructor(
    private writeRepo: OrderWriteRepository,
    private readRepo: OrderReadRepository
  ) {}

  async handle(command: PlaceOrderCommand): Promise<string> {
    const orderId = 'order_' + Date.now();
    const order = new OrderAggregate(orderId, command.userId, command.shippingAddress);

    // Add items (would fetch prices from product service)
    for (const item of command.items) {
      order.addItem(item.productId, item.quantity, 10); // Simplified price
    }

    this.writeRepo.save(order);
    this.readRepo.save(order.getOrder());

    return orderId;
  }
}

class UpdateOrderStatusCommandHandler {
  constructor(
    private writeRepo: OrderWriteRepository,
    private readRepo: OrderReadRepository
  ) {}

  async handle(command: UpdateOrderStatusCommand): Promise<void> {
    const order = this.writeRepo.findById(command.orderId);

    if (!order) {
      throw new Error(`Order ${command.orderId} not found`);
    }

    order.updateStatus(command.status);
    this.writeRepo.save(order);
    this.readRepo.save(order.getOrder());
  }
}

// Query Handlers
class GetOrderQueryHandler {
  constructor(private readRepo: OrderReadRepository) {}

  async handle(query: GetOrderQuery): Promise<any> {
    return this.readRepo.findById(query.orderId);
  }
}

class GetUserOrdersQueryHandler {
  constructor(private readRepo: OrderReadRepository) {}

  async handle(query: GetUserOrdersQuery): Promise<any[]> {
    return this.readRepo.findByUserId(query.userId, query.page, query.limit);
  }
}

class GetOrderStatisticsQueryHandler {
  constructor(private readRepo: OrderReadRepository) {}

  async handle(query: GetOrderStatisticsQuery): Promise<any> {
    return this.readRepo.getStatistics(query.startDate, query.endDate);
  }
}

// Usage
async function main() {
  const writeRepo = new OrderWriteRepository();
  const readRepo = new OrderReadRepository();

  const placeOrderHandler = new PlaceOrderCommandHandler(writeRepo, readRepo);
  const updateStatusHandler = new UpdateOrderStatusCommandHandler(writeRepo, readRepo);
  const getOrderHandler = new GetOrderQueryHandler(readRepo);

  // Place order
  const orderId = await placeOrderHandler.handle(
    new PlaceOrderCommand(
      'user1',
      [{ productId: 'prod1', quantity: 2 }],
      { city: 'New York', street: '123 Main St' }
    )
  );

  console.log('Order placed:', orderId);

  // Get order
  const order = await getOrderHandler.handle(new GetOrderQuery(orderId));
  console.log('Order:', order);

  // Update status
  await updateStatusHandler.handle(
    new UpdateOrderStatusCommand(orderId, 'shipped')
  );

  // Get updated order
  const updatedOrder = await getOrderHandler.handle(new GetOrderQuery(orderId));
  console.log('Updated order:', updatedOrder);
}

main();
```

### 2. DI with NestJS-style

```typescript
// Service tokens
const USER_REPOSITORY = 'USER_REPOSITORY';
const EMAIL_SERVICE = 'EMAIL_SERVICE';
const CACHE_SERVICE = 'CACHE_SERVICE';
const USER_SERVICE = 'USER_SERVICE';

// Interfaces
interface UserRepository {
  findById(id: string): Promise<any>;
  findByEmail(email: string): Promise<any>;
  save(user: any): Promise<any>;
}

interface EmailService {
  send(to: string, subject: string, body: string): Promise<boolean>;
}

interface CacheService {
  get<T>(key: string): Promise<T | null>;
  set(key: string, value: any, ttl?: number): Promise<void>;
  delete(key: string): Promise<void>;
}

// Implementations
class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<any> {
    console.log(`PostgreSQL: Finding user ${id}`);
    return { id, name: 'John' };
  }

  async findByEmail(email: string): Promise<any> {
    console.log(`PostgreSQL: Finding user by email ${email}`);
    return { id: '1', email };
  }

  async save(user: any): Promise<any> {
    console.log(`PostgreSQL: Saving user`);
    return user;
  }
}

class SendGridEmailService implements EmailService {
  async send(to: string, subject: string, body: string): Promise<boolean> {
    console.log(`SendGrid: Sending email to ${to}`);
    return true;
  }
}

class RedisCacheService implements CacheService {
  async get<T>(key: string): Promise<T | null> {
    console.log(`Redis: Getting ${key}`);
    return null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    console.log(`Redis: Setting ${key}`);
  }

  async delete(key: string): Promise<void> {
    console.log(`Redis: Deleting ${key}`);
  }
}

// DI Container
class Container {
  private static providers = new Map<string, any>();

  static provide(token: string, implementation: any): void {
    this.providers.set(token, implementation);
  }

  static get<T>(token: string): T {
    const provider = this.providers.get(token);

    if (!provider) {
      throw new Error(`No provider for ${token}`);
    }

    return provider as T;
  }
}

// Service using DI
class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService,
    private cacheService: CacheService
  ) {}

  async getUser(id: string): Promise<any> {
    // Check cache first
    const cached = await this.cacheService.get(`user:${id}`);
    if (cached) {
      return cached;
    }

    // Fetch from database
    const user = await this.userRepository.findById(id);

    // Cache result
    await this.cacheService.set(`user:${id}`, user, 3600);

    return user;
  }

  async createUser(data: any): Promise<any> {
    const user = await this.userRepository.save(data);

    // Send welcome email
    await this.emailService.send(user.email, 'Welcome!', 'Hello!');

    return user;
  }
}

// Setup DI
Container.provide(USER_REPOSITORY, new PostgresUserRepository());
Container.provide(EMAIL_SERVICE, new SendGridEmailService());
Container.provide(CACHE_SERVICE, new RedisCacheService());

// Create service with DI
const userService = new UserService(
  Container.get<UserRepository>(USER_REPOSITORY),
  Container.get<EmailService>(EMAIL_SERVICE),
  Container.get<CacheService>(CACHE_SERVICE)
);

// Usage
async function main() {
  await userService.createUser({ name: 'John', email: 'john@example.com' });
  const user = await userService.getUser('1');
  console.log('User:', user);
}

main();
```

## Common Mistakes

### 1. CQRS Over-engineering

```typescript
// ❌ BAD - Using CQRS for simple CRUD
class SimpleEntity {
  // Simple CRUD doesn't need CQRS
  // Use it only when read/write patterns differ significantly
}
```

### 2. DI Container Abuse

```typescript
// ❌ BAD - Overusing DI for everything
class SimpleService {
  // Simple service that doesn't need DI
  // DI is for external dependencies
}
```

### 3. Circular Dependencies

```typescript
// ❌ BAD - Circular dependency
class ServiceA {
  constructor(private serviceB: ServiceB) {}
}

class ServiceB {
  constructor(private serviceA: ServiceA) {} // Circular!
}
```

### 4. Not Using Interface

```typescript
// ❌ BAD - DI without interface
class Service {
  constructor(private dependency: ConcreteClass) {} // Should use interface
}
```

## Best Practices

### 1. Use CQRS When Appropriate

```typescript
// ✅ GOOD - CQRS for complex domains
// Use when:
// - Read and write patterns differ significantly
// - Different scaling needs
// - Complex business logic
// - Multiple read models
```

### 2. Constructor Injection

```typescript
// ✅ GOOD - Constructor injection
class Service {
  constructor(
    private dependency1: Interface1,
    private dependency2: Interface2
  ) {}
}
```

### 3. Interface-based Dependencies

```typescript
// ✅ GOOD - Interface-based
class Service {
  constructor(private repository: UserRepository) {} // Interface, not implementation
}
```

### 4. Composition Root

```typescript
// ✅ GOOD - Composition root for DI setup
function configureDI(): Container {
  const container = new Container();
  container.register('Repository', new ConcreteRepository());
  return container;
}
```

## Performance Considerations

1. **CQRS Overhead**: CQRS adds complexity; use only when benefits outweigh costs.

2. **DI Resolution**: DI container resolution has minimal overhead.

3. **Event Synchronization**: CQRS requires eventual consistency handling.

4. **Memory Usage**: DI containers store registrations; be mindful of memory.

5. **Lazy Loading**: Consider lazy loading for expensive dependencies.

## Interview Questions

### Beginner

1. **What is CQRS?**
   - An architectural pattern separating read and write operations into different models.

2. **What is Dependency Injection?**
   - A design pattern where objects receive dependencies from external sources.

3. **When would you use CQRS?**
   - When read and write patterns differ significantly, or different scaling needs.

4. **How do you implement DI in TypeScript?**
   - Use constructor injection, interfaces, and DI containers.

5. **What are the benefits of DI?**
   - Loose coupling, testability, flexibility, and maintainability.

### Intermediate

6. **What's the difference between CQRS and Event Sourcing?**
   - CQRS separates reads/writes; Event Sourcing stores state changes as events.

7. **How do you handle eventual consistency in CQRS?**
   - Use event handlers, sagas, or polling for synchronization.

8. **Can you use CQRS without Event Sourcing?**
   - Yes, CQRS can work with traditional databases.

9. **What's the difference between DI and Service Locator?**
   - DI is explicit; Service Locator is implicit dependency resolution.

10. **How do you test code with DI?**
    - Use mock implementations, inject test doubles.

### Senior

11. **How does CQRS affect scalability?**
    - Enables independent scaling of read and write sides.

12. **What are the SOLID violations with CQRS/DI?**
    - Usually follows SOLID; watch for violating Dependency Inversion.

13. **How do you handle CQRS in microservices?**
    - Use separate services for read/write, or separate databases.

14. **What are the memory implications of DI?**
    - DI containers store registrations; singleton instances persist.

15. **How do you refactor to CQRS/DI?**
    - Start with simple separation, gradually introduce complexity.

### FAANG-style

16. **Design a CQRS system for high availability.**
    - Consider replication, partitioning, and consistency guarantees.

17. **How would you implement DI for distributed systems?**
    - Use service discovery, configuration management, and health checks.

18. **What are the implications of CQRS in cloud-native applications?**
    - Consider serverless, auto-scaling, and cost optimization.

19. **How do you handle CQRS in event-driven architectures?**
    - Use event buses, message queues, and eventual consistency.

20. **Design a DI container that supports lifecycle management.**
    - Consider singleton, transient, and scoped lifetimes.

### Follow-ups

21. **Can CQRS/DI be combined with other patterns?**
    - Yes, commonly with Event Sourcing, Repository, and Factory patterns.

22. **How do you handle CQRS/DI in testing frameworks?**
    - Use dependency injection, create test containers, and mock implementations.

23. **What are the memory implications of CQRS/DI?**
    - CQRS requires separate models; DI containers store registrations.

24. **How do you handle CQRS/DI in serverless environments?**
    - Consider stateless design, function composition, and cold starts.

25. **What's the impact of CQRS/DI on code maintainability?**
    - Improves maintainability by separating concerns and promoting loose coupling.

## Summary

CQRS and DI are essential architectural patterns for complex applications. CQRS separates read and write operations for independent optimization, while DI promotes loose coupling and testability. Use them when complexity warrants the added overhead.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│        CQRS & DI PATTERNS                   │
├─────────────────────────────────────────────┤
│ CQRS:                                        │
│ ✅ USE WHEN:                                │
│ • Different read/write patterns              │
│ • Independent scaling needed                 │
│ • Complex business logic                     │
│ • Multiple read models                       │
├─────────────────────────────────────────────┤
│ DI:                                          │
│ ✅ USE WHEN:                                │
│ • Loose coupling needed                      │
│ • Testing is critical                        │
│ • Multiple implementations                   │
│ • Configuration management                   │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ CQRS:                                        │
│ • Commands vs Queries                        │
│ • Separate read/write models                 │
│ • Event synchronization                      │
├─────────────────────────────────────────────┤
│ DI:                                          │
│ • Constructor injection                      │
│ • Interface-based dependencies               │
│ • DI container                               │
│ • Composition root                           │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Over-engineering                           │
│ • Circular dependencies                      │
│ • Not using interfaces                       │
│ • Complexity overhead                        │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [Martin Fowler: CQRS](https://martinfowler.com/bliki/CQRS.html)
- [NestJS CQRS](https://docs.nestjs.com/recipes/cqrs)
- [Dependency Injection in TypeScript](https://inversify.io/)
