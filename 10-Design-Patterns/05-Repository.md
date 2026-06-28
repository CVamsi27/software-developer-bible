# Repository Pattern

## Definition

The Repository pattern is a structural design pattern that provides an abstraction over the data access layer, separating the business logic from the persistence logic. It acts as a collection-like interface for accessing domain objects, hiding the details of data storage and retrieval.

The pattern is particularly useful in Domain-Driven Design (DDD) and Clean Architecture, where it mediates between the domain and data mapping layers.

## Why Do We Need It?

Without the Repository pattern, business logic is tightly coupled to data access, leading to:

1. **Tight coupling**: Business logic depends on specific database implementations
2. **Code duplication**: Data access logic repeated throughout the codebase
3. **Difficult testing**: Hard to mock database operations for unit tests
4. **Hard to change databases**: Switching from PostgreSQL to MongoDB requires rewriting many files

## How It Works

The Repository pattern works by:

1. Defining an interface for data access operations
2. Implementing the interface for specific data stores
3. Business logic depends only on the interface, not implementations
4. Dependency injection provides the concrete implementation

```text
┌─────────────────────────────────────────────────┐
│             Repository Pattern                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Service     │◄── Business logic             │
│  └──────────────┘                               │
│         │                                       │
│         │ depends on                            │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Repository Interface             │   │
│  │    + findById(id): Entity                │   │
│  │    + findAll(): Entity[]                 │   │
│  │    + save(entity): Entity                │   │
│  │    + delete(id): void                    │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┬────────────┐                    │
│    ▼         ▼            ▼                    │
│ ┌──────┐ ┌──────┐   ┌──────┐                  │
│ │Postgr│ │Mongo │   │File  │                  │
│ │SQL   │ │DB    │   │System│                  │
│ └──────┘ └──────┘   └──────┘                  │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Repository Interface

```typescript
// Entity base class
abstract class Entity {
  abstract getId(): string;
  abstract createdAt: Date;
  abstract updatedAt: Date;
}

// Repository interface
interface Repository<T extends Entity> {
  findById(id: string): Promise<T | null>;
  findAll(options?: FindOptions): Promise<T[]>;
  save(entity: T): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T | null>;
  delete(id: string): Promise<boolean>;
  count(): Promise<number>;
}

interface FindOptions {
  limit?: number;
  offset?: number;
  orderBy?: string;
  order?: 'asc' | 'desc';
}
```

### User Repository Implementation

```typescript
// User entity
class User extends Entity {
  constructor(
    public id: string,
    public name: string,
    public email: string,
    public password: string,
    public role: 'admin' | 'user' | 'moderator',
    public isActive: boolean = true,
    public createdAt: Date = new Date(),
    public updatedAt: Date = new Date()
  ) {
    super();
  }

  getId(): string {
    return this.id;
  }
}

// In-memory repository implementation
class InMemoryUserRepository implements Repository<User> {
  private users: Map<string, User> = new Map();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  async findAll(options?: FindOptions): Promise<User[]> {
    let users = Array.from(this.users.values());

    if (options?.orderBy) {
      users.sort((a, b) => {
        const aVal = (a as any)[options.orderBy!];
        const bVal = (b as any)[options.orderBy!];
        const order = options.order === 'desc' ? -1 : 1;
        return aVal > bVal ? order : -order;
      });
    }

    if (options?.offset) {
      users = users.slice(options.offset);
    }

    if (options?.limit) {
      users = users.slice(0, options.limit);
    }

    return users;
  }

  async save(user: User): Promise<User> {
    user.updatedAt = new Date();
    this.users.set(user.id, user);
    return user;
  }

  async update(id: string, data: Partial<User>): Promise<User | null> {
    const user = this.users.get(id);
    if (!user) return null;

    const updatedUser = { ...user, ...data, updatedAt: new Date() };
    this.users.set(id, updatedUser);
    return updatedUser;
  }

  async delete(id: string): Promise<boolean> {
    return this.users.delete(id);
  }

  async count(): Promise<number> {
    return this.users.size;
  }

  // Custom repository methods
  async findByEmail(email: string): Promise<User | null> {
    return Array.from(this.users.values()).find(u => u.email === email) || null;
  }

  async findByRole(role: User['role']): Promise<User[]> {
    return Array.from(this.users.values()).filter(u => u.role === role);
  }

  async findActiveUsers(): Promise<User[]> {
    return Array.from(this.users.values()).filter(u => u.isActive);
  }
}
```

### Repository with Prisma

```typescript
import { PrismaClient, User as PrismaUser } from '@prisma/client';

// Prisma repository implementation
class PrismaUserRepository implements Repository<User> {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = new PrismaClient();
  }

  private toDomain(prismaUser: PrismaUser): User {
    return new User(
      prismaUser.id,
      prismaUser.name,
      prismaUser.email,
      prismaUser.password,
      prismaUser.role as User['role'],
      prismaUser.isActive,
      prismaUser.createdAt,
      prismaUser.updatedAt
    );
  }

  private toPrisma(user: User): Omit<PrismaUser, 'id' | 'createdAt' | 'updatedAt'> {
    return {
      name: user.name,
      email: user.email,
      password: user.password,
      role: user.role,
      isActive: user.isActive
    };
  }

  async findById(id: string): Promise<User | null> {
    const prismaUser = await this.prisma.user.findUnique({
      where: { id }
    });

    return prismaUser ? this.toDomain(prismaUser) : null;
  }

  async findAll(options?: FindOptions): Promise<User[]> {
    const prismaUsers = await this.prisma.user.findMany({
      take: options?.limit,
      skip: options?.offset,
      orderBy: options?.orderBy ? {
        [options.orderBy]: options.order || 'asc'
      } : undefined
    });

    return prismaUsers.map(u => this.toDomain(u));
  }

  async save(user: User): Promise<User> {
    const prismaData = this.toPrisma(user);

    const prismaUser = await this.prisma.user.upsert({
      where: { id: user.id },
      update: prismaData,
      create: {
        id: user.id,
        ...prismaData
      }
    });

    return this.toDomain(prismaUser);
  }

  async update(id: string, data: Partial<User>): Promise<User | null> {
    try {
      const prismaUser = await this.prisma.user.update({
        where: { id },
        data: this.toPrisma(data as User)
      });

      return this.toDomain(prismaUser);
    } catch {
      return null;
    }
  }

  async delete(id: string): Promise<boolean> {
    try {
      await this.prisma.user.delete({
        where: { id }
      });
      return true;
    } catch {
      return false;
    }
  }

  async count(): Promise<number> {
    return this.prisma.user.count();
  }

  // Custom methods
  async findByEmail(email: string): Promise<User | null> {
    const prismaUser = await this.prisma.user.findUnique({
      where: { email }
    });

    return prismaUser ? this.toDomain(prismaUser) : null;
  }

  async findByRole(role: User['role']): Promise<User[]> {
    const prismaUsers = await this.prisma.user.findMany({
      where: { role }
    });

    return prismaUsers.map(u => this.toDomain(u));
  }
}
```

### Generic Repository with Specifications

```typescript
// Specification pattern for complex queries
interface Specification<T> {
  isSatisfiedBy(entity: T): boolean;
  toQuery(): Record<string, any>;
}

// Base specifications
class AndSpecification<T> implements Specification<T> {
  constructor(
    private left: Specification<T>,
    private right: Specification<T>
  ) {}

  isSatisfiedBy(entity: T): boolean {
    return this.left.isSatisfiedBy(entity) && this.right.isSatisfiedBy(entity);
  }

  toQuery() {
    return {
      AND: [this.left.toQuery(), this.right.toQuery()]
    };
  }
}

class OrSpecification<T> implements Specification<T> {
  constructor(
    private left: Specification<T>,
    private right: Specification<T>
  ) {}

  isSatisfiedBy(entity: T): boolean {
    return this.left.isSatisfiedBy(entity) || this.right.isSatisfiedBy(entity);
  }

  toQuery() {
    return {
      OR: [this.left.toQuery(), this.right.toQuery()]
    };
  }
}

// User specifications
class IsActiveUserSpecification implements Specification<User> {
  isSatisfiedBy(user: User): boolean {
    return user.isActive;
  }

  toQuery() {
    return { isActive: true };
  }
}

class HasRoleSpecification implements Specification<User> {
  constructor(private role: User['role']) {}

  isSatisfiedBy(user: User): boolean {
    return user.role === this.role;
  }

  toQuery() {
    return { role: this.role };
  }
}

class EmailContainsSpecification implements Specification<User> {
  constructor(private domain: string) {}

  isSatisfiedBy(user: User): boolean {
    return user.email.includes(this.domain);
  }

  toQuery() {
    return { email: { contains: this.domain } };
  }
}

// Generic repository with specifications
interface GenericRepository<T extends Entity> {
  findById(id: string): Promise<T | null>;
  find(specification: Specification<T>): Promise<T[]>;
  findOne(specification: Specification<T>): Promise<T | null>;
  save(entity: T): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T | null>;
  delete(id: string): Promise<boolean>;
  count(specification?: Specification<T>): Promise<number>;
}

// Implementation
class SpecificationRepository<T extends Entity> implements GenericRepository<T> {
  private items: Map<string, T> = new Map();

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) || null;
  }

  async find(specification: Specification<T>): Promise<T[]> {
    return Array.from(this.items.values()).filter(item =>
      specification.isSatisfiedBy(item)
    );
  }

  async findOne(specification: Specification<T>): Promise<T | null> {
    const results = await this.find(specification);
    return results[0] || null;
  }

  async save(entity: T): Promise<T> {
    this.items.set(entity.getId(), entity);
    return entity;
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    const entity = this.items.get(id);
    if (!entity) return null;

    const updated = { ...entity, ...data };
    this.items.set(id, updated as T);
    return updated as T;
  }

  async delete(id: string): Promise<boolean> {
    return this.items.delete(id);
  }

  async count(specification?: Specification<T>): Promise<number> {
    if (!specification) {
      return this.items.size;
    }

    return Array.from(this.items.values()).filter(item =>
      specification.isSatisfiedBy(item)
    ).length;
  }
}

// Usage
const userRepo = new SpecificationRepository<User>();

const activeUsers = await userRepo.find(new IsActiveUserSpecification());
const adminUsers = await userRepo.find(new HasRoleSpecification('admin'));
const gmailUsers = await userRepo.find(new EmailContainsSpecification('@gmail.com'));

// Combine specifications
const activeAdmins = await userRepo.find(
  new AndSpecification(
    new IsActiveUserSpecification(),
    new HasRoleSpecification('admin')
  )
);
```

### Unit of Work Pattern

```typescript
// Unit of Work interface
interface UnitOfWork {
  getRepository<T extends Entity>(entityClass: new (...args: any[]) => T): Repository<T>;
  beginTransaction(): Promise<void>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
}

// Concrete implementation
class InMemoryUnitOfWork implements UnitOfWork {
  private repositories: Map<string, Repository<any>> = new Map();
  private transactionActive = false;
  private transactionData: Map<string, any[]> = new Map();

  getRepository<T extends Entity>(entityClass: new (...args: any[]) => T): Repository<T> {
    const entityName = entityClass.name;

    if (!this.repositories.has(entityName)) {
      this.repositories.set(entityName, new InMemoryRepository<any>());
    }

    return this.repositories.get(entityName) as Repository<T>;
  }

  async beginTransaction(): Promise<void> {
    this.transactionActive = true;
    this.transactionData.clear();
  }

  async commit(): Promise<void> {
    this.transactionActive = false;
    this.transactionData.clear();
  }

  async rollback(): Promise<void> {
    this.transactionActive = false;
    this.transactionData.clear();
  }
}

// Service using Unit of Work
class UserService {
  constructor(private unitOfWork: UnitOfWork) {}

  async createUser(data: { name: string; email: string }): Promise<User> {
    const userRepo = this.unitOfWork.getRepository(User);

    // Check if user exists
    const existingUser = await userRepo.findByEmail(data.email);
    if (existingUser) {
      throw new Error('User already exists');
    }

    const user = new User(
      Math.random().toString(36).substr(2, 9),
      data.name,
      data.email,
      'hashed_password',
      'user'
    );

    return userRepo.save(user);
  }

  async transferAdminRole(fromId: string, toId: string): Promise<void> {
    await this.unitOfWork.beginTransaction();

    try {
      const userRepo = this.unitOfWork.getRepository(User);

      const fromUser = await userRepo.findById(fromId);
      const toUser = await userRepo.findById(toId);

      if (!fromUser || !toUser) {
        throw new Error('User not found');
      }

      if (fromUser.role !== 'admin') {
        throw new Error('Only admin can transfer role');
      }

      await userRepo.update(fromId, { role: 'user' });
      await userRepo.update(toId, { role: 'admin' });

      await this.unitOfWork.commit();
    } catch (error) {
      await this.unitOfWork.rollback();
      throw error;
    }
  }
}
```

## Real-World Use Cases

### 1. Product Repository with Caching

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  stock: number;
}

class ProductRepository {
  private cache: Map<string, { product: Product; expiry: number }> = new Map();
  private cacheTTL = 5 * 60 * 1000; // 5 minutes

  constructor(private db: Database) {}

  async findById(id: string): Promise<Product | null> {
    // Check cache first
    const cached = this.cache.get(id);
    if (cached && Date.now() < cached.expiry) {
      return cached.product;
    }

    // Fetch from database
    const product = await this.db.product.findUnique({ where: { id } });

    if (product) {
      this.cache.set(id, {
        product,
        expiry: Date.now() + this.cacheTTL
      });
    }

    return product;
  }

  async save(product: Product): Promise<Product> {
    const saved = await this.db.product.upsert({
      where: { id: product.id },
      update: product,
      create: product
    });

    // Invalidate cache
    this.cache.delete(product.id);

    return saved;
  }

  async findByCategory(category: string): Promise<Product[]> {
    const cacheKey = `category:${category}`;
    const cached = this.cache.get(cacheKey);

    if (cached && Date.now() < cached.expiry) {
      return cached.product as any;
    }

    const products = await this.db.product.findMany({
      where: { category }
    });

    this.cache.set(cacheKey, {
      product: products as any,
      expiry: Date.now() + this.cacheTTL
    });

    return products;
  }

  async updateStock(id: string, quantity: number): Promise<Product> {
    const product = await this.findById(id);
    if (!product) {
      throw new Error('Product not found');
    }

    return this.save({
      ...product,
      stock: product.stock + quantity
    });
  }
}
```

### 2. Order Repository with Relationships

```typescript
interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered';
  createdAt: Date;
}

interface OrderItem {
  productId: string;
  quantity: number;
  price: number;
}

class OrderRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<Order | null> {
    const order = await this.prisma.order.findUnique({
      where: { id },
      include: {
        items: true,
        user: true
      }
    });

    return order ? this.toDomain(order) : null;
  }

  async findByUserId(userId: string): Promise<Order[]> {
    const orders = await this.prisma.order.findMany({
      where: { userId },
      include: { items: true },
      orderBy: { createdAt: 'desc' }
    });

    return orders.map(o => this.toDomain(o));
  }

  async findPendingOrders(): Promise<Order[]> {
    const orders = await this.prisma.order.findMany({
      where: { status: 'pending' },
      include: { items: true },
      orderBy: { createdAt: 'asc' }
    });

    return orders.map(o => this.toDomain(o));
  }

  async save(order: Order): Promise<Order> {
    const { items, ...orderData } = order;

    const savedOrder = await this.prisma.order.upsert({
      where: { id: order.id },
      update: {
        ...orderData,
        items: {
          deleteMany: {},
          create: items
        }
      },
      create: {
        ...orderData,
        items: {
          create: items
        }
      },
      include: { items: true }
    });

    return this.toDomain(savedOrder);
  }

  async updateStatus(id: string, status: Order['status']): Promise<Order | null> {
    const order = await this.prisma.order.update({
      where: { id },
      data: { status },
      include: { items: true }
    });

    return this.toDomain(order);
  }

  private toDomain(prismaOrder: any): Order {
    return {
      id: prismaOrder.id,
      userId: prismaOrder.userId,
      items: prismaOrder.items,
      total: prismaOrder.total,
      status: prismaOrder.status,
      createdAt: prismaOrder.createdAt
    };
  }
}
```

### 3. Search Repository

```typescript
interface SearchCriteria {
  query?: string;
  filters?: Record<string, any>;
  sort?: { field: string; order: 'asc' | 'desc' };
  pagination?: { page: number; limit: number };
}

interface SearchResult<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

class SearchableRepository<T extends Entity> {
  constructor(private items: T[] = []) {}

  async search(criteria: SearchCriteria): Promise<SearchResult<T>> {
    let results = [...this.items];

    // Apply text search
    if (criteria.query) {
      const query = criteria.query.toLowerCase();
      results = results.filter(item => {
        const searchableText = this.getSearchableText(item).toLowerCase();
        return searchableText.includes(query);
      });
    }

    // Apply filters
    if (criteria.filters) {
      Object.entries(criteria.filters).forEach(([key, value]) => {
        results = results.filter(item => {
          const itemValue = (item as any)[key];
          return itemValue === value;
        });
      });
    }

    // Apply sorting
    if (criteria.sort) {
      results.sort((a, b) => {
        const aVal = (a as any)[criteria.sort!.field];
        const bVal = (b as any)[criteria.sort!.field];
        const order = criteria.sort!.order === 'desc' ? -1 : 1;
        return aVal > bVal ? order : -order;
      });
    }

    const total = results.length;

    // Apply pagination
    if (criteria.pagination) {
      const { page, limit } = criteria.pagination;
      const offset = (page - 1) * limit;
      results = results.slice(offset, offset + limit);

      return {
        items: results,
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit)
      };
    }

    return {
      items: results,
      total,
      page: 1,
      limit: total,
      totalPages: 1
    };
  }

  protected getSearchableText(item: T): string {
    // Override in subclasses to define searchable fields
    return JSON.stringify(item);
  }

  async add(item: T): Promise<void> {
    this.items.push(item);
  }

  async remove(id: string): Promise<boolean> {
    const index = this.items.findIndex(item => item.getId() === id);
    if (index !== -1) {
      this.items.splice(index, 1);
      return true;
    }
    return false;
  }
}

// Usage
class ProductSearchRepository extends SearchableRepository<Product> {
  protected getSearchableText(product: Product): string {
    return `${product.name} ${product.category}`;
  }
}
```

## Common Mistakes

### 1. Anemic Repository

```typescript
// ❌ BAD - Repository is just a data mapper
class BadRepository {
  async findById(id: string): Promise<any> {
    return this.db.find(id);
  }

  async save(data: any): Promise<any> {
    return this.db.save(data);
  }

  // No business logic, no query methods
}
```

### 2. Repository with Business Logic

```typescript
// ❌ BAD - Repository has too much business logic
class BadRepository {
  async createUserWithOrder(userData: any, orderData: any) {
    // This belongs in a service, not repository
    const user = await this.createUser(userData);
    const order = await this.createOrder(orderData);
    await this.sendWelcomeEmail(user);
    return { user, order };
  }
}
```

### 3. Not Using Interface

```typescript
// ❌ BAD - No abstraction
class UserRepository {
  async findById(id: string): Promise<User> {
    // Direct database access without interface
  }
}
```

### 4. God Repository

```typescript
// ❌ BAD - One repository for everything
class Repository {
  async findUser(id: string): Promise<User> { ... }
  async findProduct(id: string): Promise<Product> { ... }
  async findOrder(id: string): Promise<Order> { ... }
  // Violates Single Responsibility Principle
}
```

## Best Practices

### 1. Use Interface for All Repositories

```typescript
// ✅ GOOD - Clear interface
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<boolean>;
}
```

### 2. Keep Repositories Focused

```typescript
// ✅ GOOD - Single responsibility
class UserRepository implements UserRepositoryInterface {
  // Only user-related operations
}

class OrderRepository implements OrderRepositoryInterface {
  // Only order-related operations
}
```

### 3. Use Specification Pattern for Complex Queries

```typescript
// ✅ GOOD - Reusable query logic
const activeUsers = await userRepo.find(new IsActiveUserSpecification());
const adminUsers = await userRepo.find(new HasRoleSpecification('admin'));
```

### 4. Implement Caching at Repository Level

```typescript
// ✅ GOOD - Transparent caching
class CachedUserRepository implements UserRepository {
  private cache: Map<string, User> = new Map();

  async findById(id: string): Promise<User | null> {
    if (this.cache.has(id)) {
      return this.cache.get(id)!;
    }

    const user = await this.db.user.findUnique({ where: { id } });
    if (user) {
      this.cache.set(id, user);
    }

    return user;
  }
}
```

## Performance Considerations

1. **N+1 Query Problem**: Use eager loading or joins to avoid multiple queries.

2. **Caching**: Implement caching at repository level for frequently accessed data.

3. **Connection Pooling**: Use connection pools for database connections.

4. **Batch Operations**: Implement batch insert/update for better performance.

5. **Lazy Loading**: Consider lazy loading for related entities when appropriate.

## Interview Questions

### Beginner

1. **What is the Repository pattern?**
   - An abstraction over data access that separates business logic from persistence.

2. **When would you use Repository pattern?**
   - When you need to decouple business logic from data access or switch databases easily.

3. **What's the difference between Repository and DAO?**
   - Repository is domain-focused; DAO is data-focused. Repository is an aggregate root.

4. **How do you implement Repository in TypeScript?**
   - Define an interface, implement for specific data stores, and use dependency injection.

5. **What are the benefits of Repository pattern?**
   - Loose coupling, easier testing, and database independence.

### Intermediate

6. **How do you handle complex queries in Repository?**
   - Use Specification pattern, query builders, or custom repository methods.

7. **Can Repository have business logic?**
   - No, keep business logic in services. Repository should only handle data access.

8. **How do you test Repository pattern?**
   - Use in-memory implementations, mock databases, or test doubles.

9. **What's the relationship between Repository and Unit of Work?**
   - Unit of Work coordinates multiple repositories and transactions.

10. **How do you handle caching in Repository?**
    - Implement caching at repository level with cache invalidation strategies.

### Senior

11. **How does Repository pattern affect scalability?**
    - Can implement different strategies for read/write separation and sharding.

12. **What are the SOLID violations with Repository?**
    - Usually follows SOLID; watch for violating Interface Segregation.

13. **How do you handle Repository in microservices?**
    - Each service has its own repositories; avoid shared repositories.

14. **What are the memory implications of Repository?**
    - Repositories are usually stateless; caching can consume memory.

15. **How do you refactor Repository code?**
    - Extract common logic, use generics, and apply SOLID principles.

### FAANG-style

16. **Design a Repository for a distributed database.**
    - Consider consistency, partition tolerance, and conflict resolution.

17. **How would you implement Repository for event sourcing?**
    - Use event store, projections, and snapshots.

18. **What are the implications of Repository in cloud-native applications?**
    - Consider serverless databases, connection limits, and scaling.

19. **How do you handle Repository in CQRS?**
    - Separate read and write repositories with different optimizations.

20. **Design a Repository that supports multi-tenancy.**
    - Consider tenant isolation, data partitioning, and security.

### Follow-ups

21. **Can Repository pattern be combined with other patterns?**
    - Yes, commonly with Unit of Work, Specification, and Factory patterns.

22. **How do you handle Repository in testing frameworks?**
    - Use in-memory implementations, mock databases, and test containers.

23. **What are the memory implications of Repository pattern?**
    - Repositories are usually lightweight; caching consumes memory.

24. **How do you handle Repository in serverless environments?**
    - Consider connection pooling, cold starts, and stateless design.

25. **What's the impact of Repository on code maintainability?**
    - Improves maintainability by centralizing data access and reducing duplication.

## Summary

The Repository pattern is essential for clean architecture and domain-driven design. It provides an abstraction over data access, making it easier to test, maintain, and switch between different data stores. Use it to separate business logic from persistence concerns.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           REPOSITORY PATTERN                │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Need database independence                │
│ • Complex queries                           │
│ • Domain-driven design                      │
│ • Testing is critical                       │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple CRUD operations                    │
│ • Direct database access is fine            │
│ • Repository adds unnecessary complexity    │
│ • Performance is critical                   │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Repository interface                      │
│ • Entity/Aggregate root                     │
│ • Specification pattern                     │
│ • Unit of Work                              │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Anemic repositories                       │
│ • Business logic in repository              │
│ • God repositories                          │
│ • N+1 query problems                        │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Unit of Work                              │
│ • Specification                             │
│ • Data Mapper                               │
│ • Active Record                             │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Jimmy Bogard: Repository Pattern](https://jimmybogard.com/who-needs-the-repository-pattern/)
- [Eric Evans: Domain-Driven Design](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
