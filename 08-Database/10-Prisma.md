# Prisma

## Definition

Prisma is a next-generation Node.js and TypeScript ORM (Object-Relational Mapping) that provides a type-safe database client, schema management, and migration tooling. It replaces traditional ORMs with a schema-first approach, generating a fully typed client from your database schema.

## Why Do We Need It?

- **Type Safety**: Compile-time error detection for database queries
- **Schema Management**: Declarative schema with migrations
- **Auto-generated Client**: TypeScript types from schema
- **Developer Experience**: IntelliSense, autocompletion, refactoring
- **Database Agnostic**: Supports PostgreSQL, MySQL, SQLite, MongoDB
- **Query Optimization**: Automatic query building and optimization
- **Connection Pooling**: Built-in connection management

## How It Works

### Prisma Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Prisma Architecture                        │
│                                                             │
│  Application Code (TypeScript/JavaScript)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  import { PrismaClient } from '@prisma/client'      │   │
│  │                                                     │   │
│  │  const prisma = new PrismaClient()                  │   │
│  │  const users = await prisma.user.findMany()         │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Prisma Client (Generated)               │   │
│  │  • Type-safe queries                                │   │
│  │  • Query building                                   │   │
│  │  • Connection pooling                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Prisma Engine (Rust)                    │   │
│  │  • SQL generation                                   │   │
│  │  • Connection management                            │   │
│  │  • Query optimization                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Database (PostgreSQL, MySQL, etc.)      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Schema → Client Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Prisma Workflow                            │
│                                                             │
│  1. Define Schema (schema.prisma)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  model User {                                        │   │
│  │    id    Int      @id @default(autoincrement())     │   │
│  │    email String   @unique                            │   │
│  │    name  String?                                     │   │
│  │    posts Post[]                                      │   │
│  │  }                                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  2. Generate Client (npx prisma generate)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • TypeScript types for models                       │   │
│  │  • CRUD operations                                  │   │
│  │  • Query filters                                    │   │
│  │  • Relation loaders                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  3. Use Client in Application                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  await prisma.user.findMany({                       │   │
│  │    where: { email: 'test@example.com' }             │   │
│  │  })                                                 │   │
│  │  // TypeScript knows return type is User[]          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Schema Definition

```prisma
// schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [uuid_ossp, pgcrypto]
}

model User {
  id        String   @id @default(uuid()) @db.Uuid
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  tags      String[] @default([])
  metadata  Json?    @default("{}")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}

model Post {
  id        String   @id @default(uuid()) @db.Uuid
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String   @map("author_id") @db.Uuid
  tags      String[] @default([])
  metadata  Json?    @default("{}")

  @@index([authorId])
  @@index([published, createdAt])
  @@map("posts")
}

model Profile {
  id     String  @id @default(uuid()) @db.Uuid
  bio    String? @db.Text
  avatar String?
  user   User    @relation(fields: [userId], references: [id])
  userId String  @unique @map("user_id") @db.Uuid

  @@map("profiles")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### CRUD Operations

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Create
async function createUser() {
  const user = await prisma.user.create({
    data: {
      email: 'john@example.com',
      name: 'John Doe',
      role: 'USER',
    },
  });
  return user;
}

// Read
async function findUser(email: string) {
  const user = await prisma.user.findUnique({
    where: { email },
    include: {
      posts: true,
      profile: true,
    },
  });
  return user;
}

// Update
async function updateUser(id: string, data: { name?: string; email?: string }) {
  const user = await prisma.user.update({
    where: { id },
    data,
  });
  return user;
}

// Delete
async function deleteUser(id: string) {
  await prisma.user.delete({
    where: { id },
  });
}

// Upsert
async function upsertUser(email: string, name: string) {
  const user = await prisma.user.upsert({
    where: { email },
    update: { name },
    create: { email, name },
  });
  return user;
}

// Find many with filters
async function findPublishedPosts() {
  const posts = await prisma.post.findMany({
    where: {
      published: true,
      createdAt: {
        gte: new Date('2024-01-01'),
      },
    },
    orderBy: {
      createdAt: 'desc',
    },
    take: 10,
  });
  return posts;
}
```

### Relations

```typescript
// One-to-Many: User has many Posts
async function getUserWithPosts(userId: string) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: {
      posts: {
        where: { published: true },
        orderBy: { createdAt: 'desc' },
      },
    },
  });
  return user;
}

// One-to-One: User has one Profile
async function getUserWithProfile(userId: string) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: {
      profile: true,
    },
  });
  return user;
}

// Create with relations
async function createPostWithAuthor(authorId: string) {
  const post = await prisma.post.create({
    data: {
      title: 'My Post',
      content: 'Content here',
      author: {
        connect: { id: authorId },
      },
    },
  });
  return post;
}

// Nested creates
async function createUserWithPosts() {
  const user = await prisma.user.create({
    data: {
      email: 'john@example.com',
      name: 'John Doe',
      posts: {
        create: [
          { title: 'Post 1', content: 'Content 1' },
          { title: 'Post 2', content: 'Content 2' },
        ],
      },
    },
    include: {
      posts: true,
    },
  });
  return user;
}
```

### Transactions

```typescript
// Interactive transaction
async function transferMoney(fromId: string, toId: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    const from = await tx.account.findUnique({ where: { id: fromId } });
    const to = await tx.account.findUnique({ where: { id: toId } });

    if (!from || !to || from.balance < amount) {
      throw new Error('Insufficient funds');
    }

    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });

    return { success: true };
  });
}

// Batch transaction (atomic)
async function createOrderWithItems(
  userId: string,
  items: Array<{ productId: string; quantity: number; price: number }>
) {
  return prisma.$transaction([
    prisma.order.create({
      data: {
        userId,
        total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
        items: {
          create: items.map((item) => ({
            productId: item.productId,
            quantity: item.quantity,
            unitPrice: item.price,
          })),
        },
      },
    }),
  ]);
}
```

### Raw Queries

```typescript
// Raw SQL query
async function findUsersRaw() {
  const users = await prisma.$queryRaw`
    SELECT u.*, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.author_id
    GROUP BY u.id
    ORDER BY post_count DESC
  `;
  return users;
}

// Parameterized raw query
async function findUsersByEmail(email: string) {
  const users = await prisma.$queryRaw`
    SELECT * FROM users WHERE email = ${email}
  `;
  return users;
}

// Raw query with Prisma model
async function rawWithModel() {
  const users = await prisma.$queryRaw`
    SELECT * FROM users WHERE email LIKE ${'%@example.com'}
  `;
  return users as any[];
}

// Execute raw SQL
async function executeRaw() {
  await prisma.$executeRaw`
    UPDATE users SET updated_at = NOW() WHERE id = ${userId}
  `;
}
```

### Connection Pooling

```typescript
// Prisma manages connection pool automatically
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
      // connection_limit: 20,  // Set in URL instead
    },
  },
});

// DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=20&pool_timeout=10"
```

## Real-World Use Cases

### E-commerce API

```typescript
// Product listing with pagination
async function getProducts(page: number, limit: number, category?: string) {
  const where = category ? { category: { name: category } } : {};

  const [products, total] = await Promise.all([
    prisma.product.findMany({
      where,
      include: {
        category: true,
        reviews: {
          select: {
            rating: true,
          },
        },
      },
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.product.count({ where }),
  ]);

  return {
    products,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  };
}

// Order creation
async function createOrder(userId: string, items: Array<{ productId: string; quantity: number }>) {
  return prisma.$transaction(async (tx) => {
    // Validate stock
    for (const item of items) {
      const product = await tx.product.findUnique({
        where: { id: item.productId },
      });

      if (!product || product.stock < item.quantity) {
        throw new Error(`Insufficient stock for ${product?.name}`);
      }
    }

    // Create order
    const order = await tx.order.create({
      data: {
        userId,
        total: 0,  // Will calculate
        items: {
          create: items.map((item) => ({
            productId: item.productId,
            quantity: item.quantity,
            unitPrice: 0,  // Will fetch price
          })),
        },
      },
      include: {
        items: {
          include: { product: true },
        },
      },
    });

    // Calculate total and update stock
    let total = 0;
    for (const item of order.items) {
      const price = item.product.price;
      total += price * item.quantity;

      await tx.product.update({
        where: { id: item.productId },
        data: { stock: { decrement: item.quantity } },
      });

      await tx.orderItem.update({
        where: { id: item.id },
        data: { unitPrice: price },
      });
    }

    await tx.order.update({
      where: { id: order.id },
      data: { total },
    });

    return order;
  });
}
```

### User Authentication

```typescript
// User registration
async function register(email: string, password: string, name: string) {
  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) {
    throw new Error('Email already registered');
  }

  const hashedPassword = await hash(password, 10);

  return prisma.user.create({
    data: {
      email,
      name,
      password: hashedPassword,
      profile: {
        create: {},
      },
    },
    include: {
      profile: true,
    },
  });
}

// User login
async function login(email: string, password: string) {
  const user = await prisma.user.findUnique({
    where: { email },
    include: { profile: true },
  });

  if (!user || !await compare(password, user.password)) {
    throw new Error('Invalid credentials');
  }

  return user;
}
```

## Common Mistakes

### 1. N+1 Query Problem

```typescript
// BAD: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  user.posts = await prisma.post.findMany({
    where: { authorId: user.id },
  });
}

// GOOD: Eager loading
const users = await prisma.user.findMany({
  include: {
    posts: true,
  },
});
```

### 2. Missing Indexes

```typescript
// BAD: No indexes on foreign keys
model Post {
  id       String @id
  authorId String  // No index!
}

// GOOD: Index foreign keys
model Post {
  id       String @id
  authorId String
  @@index([authorId])
}
```

### 3. Not Using Transactions

```typescript
// BAD: No transaction for multi-step operation
await prisma.account.update({
  where: { id: fromId },
  data: { balance: { decrement: amount } },
});
// If this fails, money is lost!
await prisma.account.update({
  where: { id: toId },
  data: { balance: { increment: amount } },
});

// GOOD: Use transaction
await prisma.$transaction([
  prisma.account.update({
    where: { id: fromId },
    data: { balance: { decrement: amount } },
  }),
  prisma.account.update({
    where: { id: toId },
    data: { balance: { increment: amount } },
  }),
]);
```

## Best Practices

```typescript
// 1. Use transactions for multi-step operations
await prisma.$transaction(async (tx) => {
  // All operations here
});

// 2. Index foreign keys
model Post {
  authorId String
  @@index([authorId])
}

// 3. Use include/select for related data
const user = await prisma.user.findUnique({
  where: { id },
  include: { posts: true },  // Or select: { posts: { select: { title: true } } }
});

// 4. Use cursor-based pagination for large datasets
const users = await prisma.user.findMany({
  take: 10,
  skip: 1,  // Skip the cursor
  cursor: { id: lastId },
});

// 5. Use raw queries for complex operations
const result = await prisma.$queryRaw`
  SELECT * FROM users WHERE created_at > ${date}
`;

// 6. Handle errors gracefully
try {
  await prisma.user.create({ data: { email: 'duplicate@example.com' } });
} catch (error) {
  if (error.code === 'P2002') {
    // Unique constraint violation
  }
}

// 7. Use Prisma Studio for data inspection
// npx prisma studio
```

## Performance Considerations

```typescript
// 1. Use select instead of include for specific fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
});

// 2. Use cursor-based pagination
const posts = await prisma.post.findMany({
  take: 10,
  cursor: { id: lastId },
});

// 3. Use aggregate functions
const count = await prisma.post.count({
  where: { published: true },
});

const avg = await prisma.review.aggregate({
  _avg: { rating: true },
  where: { productId },
});

// 4. Use raw queries for complex analytics
const result = await prisma.$queryRaw`
  SELECT
    date_trunc('day', created_at) AS day,
    COUNT(*) AS count
  FROM posts
  GROUP BY 1
  ORDER BY 1
`;
```

## Interview Questions

### Beginner (5)

1. **What is Prisma?**
   Next-generation TypeScript ORM with schema-first approach.

2. **What is schema.prisma?**
   Declarative schema file defining models, relations, and enums.

3. **What is the difference between include and select?**
   Include: fetch related records; Select: specify which fields to return.

4. **What is npx prisma generate?**
   Generates TypeScript client from schema.

5. **What is the difference between findUnique and findFirst?**
   findUnique: requires unique field; findFirst: returns first match.

### Intermediate (5)

6. **How do you handle transactions in Prisma?**
   Use $transaction for interactive or batch transactions.

7. **What is the N+1 query problem?**
   Multiple individual queries instead of one; solve with include.

8. **How do you do pagination in Prisma?**
   skip/take for offset, cursor for cursor-based.

9. **What are raw queries?**
   Direct SQL execution; use for complex operations.

10. **How does Prisma handle connection pooling?**
    Built-in pool; configure via DATABASE_URL parameters.

### Senior (10)

11. **How does Prisma generate TypeScript types?**
    From schema.prisma; types match model definitions.

12. **What is the Prisma engine?**
    Rust-based query engine; handles SQL generation and execution.

13. **How do you optimize Prisma queries?**
    Use select, avoid N+1, index foreign keys, use raw queries.

14. **What are Prisma migrations?**
    Schema versioning; auto-generate SQL from schema changes.

15. **How do you handle database-specific features?**
    Use previewFeatures, raw queries, or extensions.

16. **What is the difference between Prisma and traditional ORMs?**
    Schema-first, type-safe, no runtime reflection.

17. **How do you handle complex queries in Prisma?**
    Use raw queries, $queryRaw, or $executeRaw.

18. **What is Prisma Client?**
    Auto-generated, type-safe database client.

19. **How do you handle errors in Prisma?**
    Try-catch with error codes (P2002, P2025, etc.).

20. **What is the difference between Prisma and Drizzle?**
    Prisma: schema-first, generated client; Drizzle: SQL-like, lightweight.

### FAANG-style (5)

21. **Design a Prisma schema for a social media platform.**
    Users, posts, comments, likes with proper relations and indexes.

22. **How would you optimize Prisma for high traffic?**
    Connection pooling, read replicas, caching, query optimization.

23. **Design a multi-tenant Prisma schema.**
    Schema per tenant, row-level security, or database per tenant.

24. **How do you handle schema migrations in production?**
    Prisma Migrate, expand-contract pattern, zero-downtime strategies.

25. **Design a real-time system with Prisma.**
    Prisma + WebSocket, subscriptions, event-driven architecture.

### Follow-ups (5)

26. **What is the difference between Prisma Migrate and db push?**
    Migrate: version-controlled; db push: schema sync without migrations.

27. **How do you handle soft deletes in Prisma?**
    DeletedAt timestamp, custom middleware.

28. **What is Prisma Accelerate?**
    Connection pooling and caching service for Prisma.

29. **How do you test Prisma applications?**
    Use in-memory database, reset between tests.

30. **What is the future of Prisma?**
    Edge runtime, serverless optimization, more database support.

## Summary

Prisma provides a type-safe, schema-first approach to database access. Use schema.prisma to define models, generate a TypeScript client, and manage migrations. Leverage transactions, include/select, and raw queries for complex operations. Handle N+1 queries with eager loading and optimize with proper indexes.

## Cheat Sheet

```bash
# Prisma commands
npx prisma init          # Initialize project
npx prisma generate      # Generate client
npx prisma migrate dev   # Create migration
npx prisma migrate deploy  # Apply migrations
npx prisma studio        # Open Prisma Studio
npx prisma db push       # Sync schema to database
npx prisma db seed       # Seed database
```

```typescript
// Common operations
await prisma.user.findMany({ where: { email: 'test@example.com' } });
await prisma.user.findUnique({ where: { id: '123' } });
await prisma.user.create({ data: { email: 'test@example.com' } });
await prisma.user.update({ where: { id: '123' }, data: { name: 'New' } });
await prisma.user.delete({ where: { id: '123' } });
await prisma.user.upsert({ where: { id: '123' }, update: {}, create: {} });

// Transactions
await prisma.$transaction([prisma.user.create({ data: {} })]);
await prisma.$transaction(async (tx) => { /* ... */ });

// Raw queries
await prisma.$queryRaw`SELECT * FROM users`;
await prisma.$executeRaw`UPDATE users SET name = ${name}`;
```

## References & Learn More

- [Prisma Official Documentation](https://www.prisma.io/docs/)
- [Prisma GitHub Repository](https://github.com/prisma/prisma)
- [Prisma Examples - Type-Safe Database Access](https://github.com/prisma/prisma-examples)
- [Prisma Data Platform - Accelerate](https://www.prisma.io/data-platform/accelerate)
- [Prisma Blog - Tips and Best Practices](https://www.prisma.io/blog)
