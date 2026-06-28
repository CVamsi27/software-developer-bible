# Resolvers

## Definition

**Resolvers** are functions that populate the data for each field in your GraphQL schema. They are the execution layer that connects your schema to your data sources (databases, APIs, microservices, etc.). Each field in the schema can have a corresponding resolver that determines how that field's value is computed.

```text
Resolver = Function(Schema Field) → Data Source
```

---

## Why Do We Need It?

### The Data Fetching Problem

```text
Without Resolvers:
┌─────────────────────────────────────────────────────────────────┐
│  Schema defines WHAT data is available                          │
│  But HOW to fetch it?  ← No mechanism defined                  │
└─────────────────────────────────────────────────────────────────┘

With Resolvers:
┌─────────────────────────────────────────────────────────────────┐
│  Schema defines WHAT data is available                          │
│  Resolvers define HOW to fetch each field                       │
│                                                                 │
│  type Query { user(id: ID!): User }                            │
│  Query.user = (parent, { id }) => db.user.findById(id)         │
└─────────────────────────────────────────────────────────────────┘
```

### Resolver Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Data Fetching** | Query databases, call APIs, etc. |
| **Transformation** | Convert data to schema types |
| **Authorization** | Check permissions |
| **Validation** | Validate inputs |
| **Error Handling** | Handle failures gracefully |
| **Caching** | Cache expensive operations |

---

## How It Works

### Resolver Function Signature

```typescript
// Standard resolver signature
(
  parent: any,           // Result from parent resolver
  args: any,             // Arguments passed to this field
  context: any,          // Shared context (auth, data sources, etc.)
  info: any              // Query AST, field name, path, etc.
) => any | Promise<any>
```

### Resolver Chain Execution

```text
Query: { user(id: 1) { name posts { title author { name } } } }

Execution Chain:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. Query.user(id: 1)                                          │
│     │                                                           │
│     ▼ parent = undefined, args = { id: 1 }                     │
│     │                                                           │
│     ▼ Returns: { id: 1, name: "John", ... }                    │
│                                                                 │
│  2. User.name                                                  │
│     │                                                           │
│     ▼ parent = { id: 1, name: "John", ... }                    │
│     │                                                           │
│     ▼ Returns: "John"                                           │
│                                                                 │
│  3. User.posts                                                 │
│     │                                                           │
│     ▼ parent = { id: 1, ... }                                  │
│     │                                                           │
│     ▼ Returns: [{ id: 1, title: "Post 1", authorId: 1 }, ...]  │
│                                                                 │
│  4. Post.title                                                 │
│     │                                                           │
│     ▼ parent = { id: 1, title: "Post 1", authorId: 1 }        │
│     │                                                           │
│     ▼ Returns: "Post 1"                                         │
│                                                                 │
│  5. Post.author                                                │
│     │                                                           │
│     ▼ parent = { id: 1, authorId: 1 }                          │
│     │                                                           │
│     ▼ Returns: { id: 1, name: "John" }                         │
│                                                                 │
│  6. User.name (nested)                                          │
│     │                                                           │
│     ▼ parent = { id: 1, name: "John" }                         │
│     │                                                           │
│     ▼ Returns: "John"                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Resolver Field Mapping

```text
Schema Field                          Resolver Function
─────────────────────────────────────────────────────────────────
type Query {
  user(id: ID!): User           →  Query.user(parent, args, ctx, info)
}

type User {
  id: ID!                       →  User.id(parent, args, ctx, info)
  name: String!                 →  User.name(parent, args, ctx, info)
  posts(first: Int): [Post!]!   →  User.posts(parent, args, ctx, info)
}

type Post {
  id: ID!                       →  Post.id(parent, args, ctx, info)
  title: String!                →  Post.title(parent, args, ctx, info)
  author: User!                 →  Post.author(parent, args, ctx, info)
}
```

---

## Code Examples

### Basic Resolver Setup

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `
  type Query {
    user(id: ID!): User
    users(limit: Int): [User!]!
  }

  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }
`;

// Root resolvers
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      return await context.dataSources.userAPI.getUser(id);
    },
    users: async (parent, { limit = 10 }, context) => {
      return await context.dataSources.userAPI.getUsers(limit);
    },
  },

  // Field resolvers
  User: {
    posts: async (parent, args, context) => {
      return await context.dataSources.postAPI.getPostsByAuthor(parent.id);
    },
  },

  Post: {
    author: async (parent, args, context) => {
      return await context.dataSources.userAPI.getUser(parent.authorId);
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    dataSources: {
      userAPI: new UserAPI(),
      postAPI: new PostAPI(),
    },
    currentUser: await authenticateUser(req.headers.authorization),
  }),
});
```

### TypeScript Typed Resolvers

```typescript
import { Resolvers } from './generated/graphql';

export const resolvers: Resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      const user = await context.dataSources.userAPI.getUser(id);
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND', id }
        });
      }
      return user;
    },

    users: async (_, { limit }, context) => {
      return context.dataSources.userAPI.getUsers(limit ?? 10);
    },
  },

  User: {
    posts: async (parent, { first, after }, context) => {
      return context.dataSources.postAPI.getPostsByAuthor(parent.id, {
        first,
        after
      });
    },

    // Default resolver (resolves to parent field)
    name: (parent) => parent.name,
    email: (parent) => parent.email,
  },

  Post: {
    author: async (parent, _, context) => {
      return context.dataSources.userAPI.getUser(parent.authorId);
    },

    // Computed field
    excerpt: (parent) => {
      return parent.content.substring(0, 200) + '...';
    },

    // Async computed field
    commentCount: async (parent, _, context) => {
      return context.dataSources.commentAPI.getCountByPost(parent.id);
    },
  },
};
```

### DataLoader Implementation

```typescript
import DataLoader from 'dataloader';

// DataLoader for User
const createUserLoader = (userAPI: UserAPI) => {
  return new DataLoader<string, User>(async (ids) => {
    const users = await userAPI.getUsersByIds(ids as string[]);
    const userMap = new Map(users.map(user => [user.id, user]));
    return ids.map(id => userMap.get(id as string) || new Error(`User ${id} not found`));
  });
};

// DataLoader for Posts by Author
const createPostsByAuthorLoader = (postAPI: PostAPI) => {
  return new DataLoader<string, Post[]>(async (authorIds) => {
    const posts = await postAPI.getPostsByAuthorIds(authorIds as string[]);
    const postsByAuthor = new Map<string, Post[]>();

    for (const post of posts) {
      const existing = postsByAuthor.get(post.authorId) || [];
      postsByAuthor.set(post.authorId, [...existing, post]);
    }

    return authorIds.map(id => postsByAuthor.get(id as string) || []);
  });
};

// DataLoader for Comment Count
const createCommentCountLoader = (commentAPI: CommentAPI) => {
  return new DataLoader<string, number>(async (postIds) => {
    const counts = await commentAPI.getCountsByPostIds(postIds as string[]);
    const countMap = new Map(counts.map(c => [c.postId, c.count]));
    return postIds.map(id => countMap.get(id as string) || 0);
  });
};

// Context creation with DataLoaders
const createContext = ({ req }) => {
  const userAPI = new UserAPI();
  const postAPI = new PostAPI();
  const commentAPI = new CommentAPI();

  return {
    dataSources: { userAPI, postAPI, commentAPI },
    loaders: {
      user: createUserLoader(userAPI),
      postsByAuthor: createPostsByAuthorLoader(postAPI),
      commentCount: createCommentCountLoader(commentAPI),
    },
    currentUser: await authenticateUser(req.headers.authorization),
  };
};

// Resolvers using DataLoaders
const resolvers: Resolvers = {
  User: {
    posts: async (parent, _, context) => {
      // Uses DataLoader - batches all user.posts calls
      return context.loaders.postsByAuthor.load(parent.id);
    },
  },

  Post: {
    author: async (parent, _, context) => {
      // Uses DataLoader - batches all post.author calls
      return context.loaders.user.load(parent.authorId);
    },

    commentCount: async (parent, _, context) => {
      return context.loaders.commentCount.load(parent.id);
    },
  },
};
```

### Advanced Resolver Patterns

```typescript
// 1. Conditional resolvers based on arguments
const resolvers = {
  Query: {
    posts: async (parent, args, context) => {
      const { first, after, filter, sort } = args;

      // Build query based on arguments
      let query = context.db.post;

      if (filter?.status) {
        query = query.where({ status: filter.status });
      }

      if (filter?.authorId) {
        query = query.where({ authorId: filter.authorId });
      }

      if (sort) {
        query = query.orderBy(sort.field, sort.order);
      }

      // Cursor-based pagination
      if (after) {
        const cursor = decodeCursor(after);
        query = query.where('createdAt', '<', cursor);
      }

      const posts = await query.take(first + 1).many();

      return {
        edges: posts.slice(0, first).map(post => ({
          node: post,
          cursor: encodeCursor(post.createdAt),
        })),
        pageInfo: {
          hasNextPage: posts.length > first,
          endCursor: posts.length > first
            ? encodeCursor(posts[first - 1].createdAt)
            : null,
        },
      };
    },
  },
};

// 2. Union type resolvers
const resolvers = {
  SearchResult: {
    __resolveType(obj) {
      if (obj.__typename === 'User') return 'User';
      if (obj.__typename === 'Post') return 'Post';
      if (obj.__typename === 'Tag') return 'Tag';
      return null;
    },
  },
};

// 3. Interface type resolvers
const resolvers = {
  Node: {
    __resolveType(obj) {
      if (obj.name && obj.email) return 'User';
      if (obj.title && obj.content) return 'Post';
      return null;
    },
  },
};

// 4. Custom scalar resolvers
import { GraphQLScalarType, Kind } from 'graphql';

const DateTimeScalar = new GraphQLScalarType({
  name: 'DateTime',
  description: 'ISO 8601 date-time string',
  serialize(value) {
    if (value instanceof Date) {
      return value.toISOString();
    }
    throw new Error('DateTime serializer expected a Date object');
  },
  parseValue(value) {
    const date = new Date(value);
    if (isNaN(date.getTime())) {
      throw new Error('Invalid DateTime string');
    }
    return date;
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.STRING) {
      const date = new Date(ast.value);
      if (isNaN(date.getTime())) {
        throw new Error('Invalid DateTime string');
      }
      return date;
    }
    throw new Error('DateTime can only be parsed from strings');
  },
});

// 5. Subscription resolvers
const resolvers = {
  Subscription: {
    postPublished: {
      subscribe: (_, { authorId }, context) => {
        return context.pubsub.asyncIterator('POST_PUBLISHED');
      },
      resolve: (payload, _, context) => {
        // Filter by author if specified
        if (payload.authorId && payload.authorId !== authorId) {
          return null;
        }
        return payload;
      },
    },
  },
};
```

---

## Real-World Use Cases

### 1. E-Commerce Product Resolver

```typescript
const resolvers = {
  Product: {
    // Resolve price with currency formatting
    price: async (parent, _, context) => {
      const product = await context.loaders.product.load(parent.id);
      return {
        amount: product.priceAmount,
        currency: product.priceCurrency,
        formatted: formatMoney(product.priceAmount, product.priceCurrency),
      };
    },

    // Resolve inventory status
    inStock: async (parent, _, context) => {
      const inventory = await context.loaders.inventory.load(parent.id);
      return inventory.quantity > 0;
    },

    // Resolve average rating
    rating: async (parent, _, context) => {
      const reviews = await context.loaders.reviews.load(parent.id);
      if (reviews.length === 0) return null;
      const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
      return sum / reviews.length;
    },

    // Resolve related products
    relatedProducts: async (parent, { limit = 4 }, context) => {
      return context.dataSources.productAPI.getRelated(parent.id, limit);
    },
  },
};
```

### 2. Social Media Feed Resolver

```typescript
const resolvers = {
  Query: {
    feed: async (_, { first, after }, context) => {
      const userId = context.currentUser.id;

      // Get followed users
      const following = await context.loaders.following.load(userId);

      // Get posts from followed users
      const posts = await context.dataSources.postAPI.getFeed(
        userId,
        following.map(f => f.followingId),
        { first: first + 1, after }
      );

      return {
        edges: posts.slice(0, first).map(post => ({
          node: post,
          cursor: encodeCursor(post.createdAt),
        })),
        pageInfo: {
          hasNextPage: posts.length > first,
          endCursor: posts.length > first
            ? encodeCursor(posts[first - 1].createdAt)
            : null,
        },
      };
    },
  },

  FeedItem: {
    // Resolve post content
    post: async (parent, _, context) => {
      return context.loaders.post.load(parent.postId);
    },

    // Resolve engagement metrics
    metrics: async (parent, _, context) => {
      const [likes, comments, shares] = await Promise.all([
        context.loaders.likeCount.load(parent.postId),
        context.loaders.commentCount.load(parent.postId),
        context.loaders.shareCount.load(parent.postId),
      ]);
      return { likes, comments, shares };
    },
  },
};
```

### 3. GraphQL Gateway with Multiple Services

```typescript
// Schema stitching resolvers
const resolvers = {
  User: {
    // Delegate to users service
    profile: {
      selectionSet: '{ id }',
      resolve(user, args, context, info) {
        return delegateToSchema({
          schema: usersServiceSchema,
          operation: 'query',
          fieldName: 'getUserProfile',
          args: { userId: user.id },
          context,
          info,
        });
      },
    },

    // Delegate to posts service
    posts: {
      selectionSet: '{ id }',
      resolve(user, args, context, info) {
        return delegateToSchema({
          schema: postsServiceSchema,
          operation: 'query',
          fieldName: 'getPostsByAuthor',
          args: { authorId: user.id, ...args },
          context,
          info,
        });
      },
    },
  },
};
```

---

## Common Mistakes

### 1. N+1 Query Problem

```typescript
// BAD: N+1 queries
const resolvers = {
  Query: {
    users: () => db.user.findMany(), // 1 query
  },
  User: {
    posts: (parent) => db.post.findMany({ // N queries (one per user)
      where: { authorId: parent.id }
    }),
  },
};

// GOOD: Use DataLoader
const resolvers = {
  User: {
    posts: (parent, _, { loaders }) => loaders.postsByAuthor.load(parent.id),
  },
};
```

### 2. Missing Null Checks

```typescript
// BAD: No null checks
const resolvers = {
  User: {
    posts: async (parent) => {
      const posts = await db.post.findMany({
        where: { authorId: parent.id }
      });
      return posts; // Could be null if user doesn't exist
    },
  },
};

// GOOD: Proper null handling
const resolvers = {
  User: {
    posts: async (parent, _, context) => {
      if (!parent?.id) {
        return [];
      }
      return context.loaders.postsByAuthor.load(parent.id);
    },
  },
};
```

### 3. Exposing Sensitive Data

```typescript
// BAD: Returning sensitive fields
const resolvers = {
  User: {
    email: (parent) => parent.email,  // Exposed to everyone
    passwordHash: (parent) => parent.passwordHash,  // NEVER expose
  },
};

// GOOD: Field-level authorization
const resolvers = {
  User: {
    email: (parent, _, context) => {
      // Only show email to self or admins
      if (context.currentUser?.id === parent.id ||
          context.currentUser?.role === 'ADMIN') {
        return parent.email;
      }
      return null;
    },
  },
};
```

### 4. Blocking the Event Loop

```typescript
// BAD: Synchronous heavy computation
const resolvers = {
  Query: {
    analytics: (_, { dateRange }) => {
      // Blocks event loop!
      return computeAnalytics(dateRange);
    },
  },
};

// GOOD: Async computation
const resolvers = {
  Query: {
    analytics: async (_, { dateRange }, context) => {
      // Check cache first
      const cached = await context.cache.get(`analytics:${dateRange}`);
      if (cached) return cached;

      // Offload heavy computation
      const result = await context.dataSources.analyticsAPI.compute(dateRange);
      await context.cache.set(`analytics:${dateRange}`, result, { ttl: 3600 });
      return result;
    },
  },
};
```

### 5. Not Using Context Properly

```typescript
// BAD: Creating new instances per resolver
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const db = new Database();  // New instance every time!
      return db.user.findById(id);
    },
  },
};

// GOOD: Share instances via context
const createContext = () => ({
  db: new Database(),
  redis: new Redis(),
  dataSources: {
    userAPI: new UserAPI(),
    postAPI: new PostAPI(),
  },
});

const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.dataSources.userAPI.getUser(id);
    },
  },
};
```

### 6. Resolver Side Effects

```typescript
// BAD: Unexpected side effects in query resolver
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      // Don't modify data in query resolvers!
      await context.db.user.update({
        where: { id },
        data: { lastAccessedAt: new Date() }
      });
      return context.db.user.findById(id);
    },
  },
};

// GOOD: Use mutations for side effects
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.db.user.findById(id);
    },
  },
  Mutation: {
    trackUserAccess: async (_, { id }, context) => {
      await context.db.user.update({
        where: { id },
        data: { lastAccessedAt: new Date() }
      });
      return context.db.user.findById(id);
    },
  },
};
```

---

## Best Practices

### Resolver Organization

```text
1. Keep resolvers thin
   - Delegate business logic to services
   - Resolvers only handle data fetching and transformation

2. Use DataLoader for N+1 prevention
   - Create loaders in context
   - Use for any field that triggers DB queries

3. Implement proper error handling
   - Try-catch async operations
   - Throw GraphQLError with extensions
   - Handle null cases

4. Use context for shared state
   - Authentication
   - Data sources
   - Loaders
   - Cache

5. Cache expensive operations
   - Use Redis/Memcached
   - Cache at resolver level
   - Use query-level caching
```

### DataLoader Best Practices

```typescript
// 1. Create loaders per request (in context)
const createContext = ({ req }) => ({
  loaders: {
    user: new DataLoader(batchFn),
    post: new DataLoader(batchFn),
  },
});

// 2. Batch function should handle errors
const batchFn = async (ids) => {
  const items = await db.findMany({ where: { id: { in: ids } } });
  const itemMap = new Map(items.map(item => [item.id, item]));

  return ids.map(id => {
    const item = itemMap.get(id);
    if (!item) {
      return new Error(`Item ${id} not found`);
    }
    return item;
  });
};

// 3. Prime the cache when you already have data
loaders.user.prime(userId, userData);

// 4. Clear cache when data changes
await updateUser(id, data);
loaders.user.clear(id);
```

---

## Performance Considerations

### Resolver Execution Timing

```text
Query Execution Timeline:
┌─────────────────────────────────────────────────────────────────┐
│ T=0ms    Query.user(id: 1) starts                              │
│ T=50ms   Query.user(id: 1) completes → { id: 1, name: "John" } │
│ T=50ms   User.name starts (returns immediately - scalar)       │
│ T=50ms   User.email starts (returns immediately - scalar)      │
│ T=50ms   User.posts starts                                     │
│ T=100ms  User.posts completes → [post1, post2, post3]          │
│ T=100ms  Post1.title starts (returns immediately)              │
│ T=100ms  Post2.title starts (returns immediately)              │
│ T=100ms  Post3.title starts (returns immediately)              │
│ T=100ms  Post1.author starts                                   │
│ T=100ms  Post2.author starts                                   │
│ T=100ms  Post3.author starts                                   │
│ T=150ms  Post1.author completes → { id: 1, name: "John" }     │
│ T=150ms  Post2.author completes → { id: 1, name: "John" }     │
│ T=150ms  Post3.author completes → { id: 1, name: "John" }     │
│ T=150ms  Total: 150ms (without DataLoader)                    │
│                                                                 │
│ With DataLoader:                                                │
│ T=0ms    Query.user(id: 1) starts                              │
│ T=50ms   Query.user completes                                   │
│ T=50ms   User.posts starts                                     │
│ T=100ms  User.posts completes                                   │
│ T=100ms  Post1.author, Post2.author, Post3.author batched     │
│ T=120ms  All authors complete (1 query instead of 3)           │
│ T=120ms  Total: 120ms (with DataLoader)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Query Complexity Scoring

```typescript
import { getComplexity, simpleEstimator, fieldExtensionsEstimator } from 'graphql-query-complexity';

// Assign complexity scores
const typeDefs = `
  type Query {
    user(id: ID!): User @complexity(value: 1)
    users(first: Int): [User!]! @complexity(value: 2, multipliers: ["first"])
  }

  type User {
    id: ID! @complexity(value: 0)
    name: String! @complexity(value: 0)
    posts(first: Int): [Post!]! @complexity(value: 5, multipliers: ["first"])
  }
`;

// Calculate and enforce
const complexity = getComplexity({
  schema,
  query: parsedQuery,
  variables,
  estimators: [
    fieldExtensionsEstimator(),
    simpleEstimator({ defaultComplexity: 1 })
  ]
});

if (complexity > 1000) {
  throw new Error(`Query too complex: ${complexity}. Maximum: 1000`);
}
```

---

## Interview Questions

### Beginner

1. **What is a resolver?**
   A resolver is a function that populates the data for each field in a GraphQL schema. It's the execution layer that connects schema to data sources.

2. **What are the resolver function arguments?**
   - `parent`: Result from parent resolver
   - `args`: Arguments passed to this field
   - `context`: Shared context (auth, data sources)
   - `info`: Query AST, field name, path

3. **What is the difference between root resolvers and field resolvers?**
   Root resolvers (Query, Mutation, Subscription) handle top-level operations. Field resolvers handle individual fields on types.

4. **What is the N+1 problem?**
   When resolving nested fields, each parent item triggers a separate database query. Example: querying users and their posts creates 1 query for users + N queries for posts.

5. **What is DataLoader?**
   A utility that batches and caches database queries within a single execution cycle, solving the N+1 problem.

### Intermediate

6. **How do resolvers execute in GraphQL?**
   Resolvers execute in parallel at the same level. Parent resolvers complete before child resolvers start.

7. **What is the `info` argument used for?**
   Contains query AST, field name, return type, schema, and path. Used for advanced optimization and debugging.

8. **How do you handle authorization in resolvers?**
   Check `context.currentUser` and permissions in resolvers. Use directives for declarative authorization.

9. **What are custom scalars and how do you implement them?**
   User-defined scalar types with serialize, parseValue, and parseLiteral methods for custom data types.

10. **How do you resolve union and interface types?**
    Use `__resolveType` function to determine which concrete type to return.

### Senior

11. **How would you design a resolver architecture for a large application?**
    Layered approach: schema → resolvers → services → repositories → data sources. Use dependency injection and DataLoader.

12. **Explain your DataLoader strategy for a complex schema.**
    Create loaders per entity, prime cache when data is available, clear on mutations, and scope per request.

13. **How do you optimize resolver execution?**
    Parallel execution, DataLoader batching, query complexity limits, field-level caching, and avoiding blocking operations.

14. **How would you implement real-time updates with subscriptions?**
    WebSocket transport, pub/sub pattern (Redis), filtering, connection management, and scaling.

15. **How do you handle resolver errors in production?**
    Structured error handling, logging, monitoring, error boundaries, partial data, and client error recovery.

### FAANG-style

16. **Design a resolver architecture for a social media platform with 1B users.**
    Sharding, DataLoader with Redis caching, query complexity limits, CDN for static fields, and distributed tracing.

17. **How would you migrate a REST API to GraphQL resolvers?**
    Start with high-value endpoints, wrap existing services, maintain backward compatibility, and incrementally adopt.

18. **Explain your approach to resolver performance monitoring.**
    Distributed tracing (OpenTelemetry), resolver execution time, N+1 detection, cache hit rates, and query complexity.

19. **How do you handle resolver conflicts in a microservices architecture?**
    Schema federation, gateway pattern, distributed resolvers, and service discovery.

20. **Design a resolver for a real-time collaborative editor.**
    Optimistic updates, conflict resolution (OT/CRDT), WebSocket subscriptions, and offline support.

### Follow-ups

21. **What happens if a resolver returns null for a non-null field?**
    GraphQL propagates null to the parent. If the parent is also non-null, it continues up until finding a nullable field or reaching the root.

22. **How do you test resolvers?**
    Unit test with mocked context, integration test with test database, and end-to-end test with Apollo Server testing utilities.

23. **What is the difference between `@resolveType` and `__resolveType`?**
    `__resolveType` is the resolver function. `@resolveType` is a directive for declarative type resolution.

24. **How do you handle resolver middleware?**
    Use Apollo Link chain, context-based middleware, or custom resolver wrappers.

25. **What are the best practices for resolver naming?**
    Use descriptive names that match the schema field names. Avoid abbreviations and be consistent.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Resolver** | Function that populates field data |
| **Execution** | Parallel at same level, sequential parent→child |
| **N+1 Problem** | Use DataLoader to batch queries |
| **Context** | Share auth, data sources, loaders |
| **Error Handling** | Use GraphQLError with extensions |
| **Performance** | DataLoader, caching, complexity limits |

---

## References & Learn More

- [GraphQL Resolvers](https://www.apollographql.com/docs/apollo-server/schema/schema/#the-resolver-map)
- [DataLoader](https://github.com/graphql/dataloader)
- [Apollo Server Resolvers](https://www.apollographql.com/docs/apollo-server/data/resolvers/)
- [GraphQL Execution](https://spec.graphql.org/#sec-Execution)
- [N+1 Problem Solutions](https://blog.apollographql.com/fixing-the-n-1-problem-in-graphql-763e44d89572)
