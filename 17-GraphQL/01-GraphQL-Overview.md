# GraphQL Overview

## Definition

GraphQL is a **query language for APIs** and a **runtime for executing those queries** against your data. Developed by Facebook in 2012 and open-sourced in 2015, it provides a complete and understandable description of the data in your API, giving clients the power to ask for exactly what they need—nothing more, nothing less.

```text
GraphQL = Query Language + Type System + Execution Engine + Introspection

```

Unlike REST, which exposes data through multiple endpoints with fixed response structures, GraphQL exposes a **single endpoint** where clients specify exactly what data they want.

---

## Why Do We Need It?

### Problems with REST

```text
REST Pain Points:
┌─────────────────────────────────────────────────────────────────┐
│  1. Over-fetching    → Getting more data than needed            │
│  2. Under-fetching   → Needing multiple requests for one view   │
│  3. Multiple endpoints → /users, /users/:id/posts, /posts/:id  │
│  4. Versioning pain  → /api/v1/, /api/v2/                      │
│  5. Fixed structures → Server dictates response shape           │
└─────────────────────────────────────────────────────────────────┘

```

**Example: Mobile app needing user profile + posts**

REST approach:

```typescript
// 3 separate requests needed
const user = await fetch('/api/users/1');          // Request 1
const posts = await fetch('/api/users/1/posts');   // Request 2
const comments = await fetch('/api/posts/1/comments'); // Request 3

```

GraphQL approach:

```typescript
// 1 single request
const result = await fetch('/graphql', {
  method: 'POST',
  body: JSON.stringify({
    query: `{
      user(id: 1) {
        name
        email
        posts {
          title
          comments { body }
        }
      }
    }`
  })
});

```

### Benefits of GraphQL

| Benefit | Description |
|---------|-------------|
| **Client-driven** | Clients request exactly what they need |
| **Single endpoint** | One URL for all operations |
| **Strongly typed** | Schema defines the contract |
| **Introspective** | Self-documenting API |
| **No over/under-fetching** | Precise data retrieval |
| **Real-time** | Built-in subscriptions |
| **No versioning** | Schema evolves without breaking changes |

---

## How It Works

### The GraphQL Ecosystem

```text
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Web App     │  │  Mobile App  │  │  Desktop App │          │
│  │  (React)     │  │  (React      │  │  (Electron)  │          │
│  │              │  │   Native)    │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           │                                      │
│                    GraphQL Queries                               │
│                    { user { name email } }                       │
│                           │                                      │
├───────────────────────────┼──────────────────────────────────────┤
│                     SERVER LAYER                                 │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              GraphQL Server                           │       │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │       │
│  │  │  Schema    │  │  Resolvers │  │  Context   │    │       │
│  │  │  (Types)   │  │  (Logic)   │  │  (State)   │    │       │
│  │  └────────────┘  └────────────┘  └────────────┘    │       │
│  └──────────────────────────┬───────────────────────────┘       │
│                             │                                    │
├─────────────────────────────┼────────────────────────────────────┤
│                       DATA LAYER                                  │
│                             ▼                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Database │  │ REST API │  │ Micro-   │  │ External │       │
│  │ (SQL/    │  │          │  │ service  │  │ API      │       │
│  │  NoSQL)  │  │          │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└──────────────────────────────────────────────────────────────────┘

```

### Request Lifecycle

```text

1. Client sends query
        │
        ▼

2. Query hits GraphQL endpoint
        │
        ▼

3. Schema validation (is query valid?)
        │
        ├── No → Return validation error
        │
        ▼ Yes

4. Query parsing + AST generation
        │
        ▼

5. Resolver execution
        │
        ├── Root resolvers execute
        │
        ├── Field resolvers chain
        │
        └── DataLoader batching (if configured)
        │
        ▼

6. Response assembled matching query shape
        │
        ▼

7. Client receives exactly what was requested

```

---

## Type System

GraphQL's type system is the foundation of the schema:

```graphql
# Scalar Types (leaf nodes)
scalar String
scalar Int
scalar Float
scalar Boolean
scalar ID

# Object Types
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

# Enum Types
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

# Input Types
input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

# Interface Types
interface Node {
  id: ID!
}

# Union Types
union SearchResult = User | Post | Comment

```

### Type Relationships Diagram

```text
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │    Post     │       │   Comment   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id: ID!     │  1:N  │ id: ID!     │  1:N  │ id: ID!     │
│ name: String│◄─────│ title: Str  │◄─────│ body: Str   │
│ email: Str  │       │ content: Str│       │ author: User│
│ posts: [Post]│      │ author: User│       │ post: Post  │
└─────────────┘       │ comments:   │       └─────────────┘
                      │  [Comment]  │
                      │ status:     │
                      │  PostStatus │
                      └─────────────┘

```

---

## Queries vs Mutations vs Subscriptions

### Queries (Read Operations)

```graphql
# Fetch a single user
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      title
      createdAt
    }
  }
}

# Fetch multiple users with filtering
query SearchUsers($query: String!, $limit: Int) {
  users(search: $query, limit: $limit) {
    edges {
      node {
        id
        name
        avatar
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

```

### Mutations (Write Operations)

```graphql
# Create a new user
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    createdAt
  }
}

# Update with optimistic response
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    content
    updatedAt
  }
}

```

### Subscriptions (Real-time)

```graphql
# Subscribe to new comments
subscription OnNewComment($postId: ID!) {
  commentAdded(postId: $postId) {
    id
    body
    author {
      name
      avatar
    }
    createdAt
  }
}

# Subscribe to live updates
subscription OnPostUpdate($postId: ID!) {
  postUpdated(postId: $postId) {
    id
    title
    content
    status
    updatedAt
  }
}

```

---

## Code Examples

### TypeScript Schema Definition (Nexus / TypeGraphQL)

```typescript
import { ObjectType, Field, ID, Int, Resolver, Query, Arg, Mutation } from 'type-graphql';

@ObjectType()
class User {
  @Field(() => ID)
  id: string;

  @Field()
  name: string;

  @Field()
  email: string;

  @Field(() => Int, { nullable: true })
  age?: number;

  @Field(() => [Post])
  posts: Post[];
}

@Resolver(User)
class UserResolver {
  @Query(() => User)
  async user(@Arg('id') id: string): Promise<User> {
    return await db.user.findById(id);
  }

  @Query(() => [User])
  async users(
    @Arg('search', { nullable: true }) search?: string
  ): Promise<User[]> {
    return await db.user.findMany({
      where: search ? { name: { contains: search } } : undefined
    });
  }

  @Mutation(() => User)
  async createUser(
    @Arg('input') input: CreateUserInput
  ): Promise<User> {
    return await db.user.create({ data: input });
  }
}

```

### Apollo Server Setup

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
    author: User!
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
  }
`;

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      return await db.user.findById(id);
    },
    users: async (_, { limit = 10 }) => {
      return await db.user.findMany({ take: limit });
    },
  },
  User: {
    posts: async (parent) => {
      return await db.post.findMany({
        where: { authorId: parent.id }
      });
    },
  },
  Mutation: {
    createUser: async (_, { name, email }) => {
      return await db.user.create({
        data: { name, email }
      });
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Server ready at ${url}`);

```

### Client Query (Apollo Client)

```typescript
import { gql, useQuery, useMutation } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      posts {
        id
        title
      }
    }
  }
`;

const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
    }
  }
`;

function UserProfile({ userId }: { userId: string }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId }
  });

  const [createUser] = useMutation(CREATE_USER);

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (
    <div>
      <h1>{data.user.name}</h1>
      <p>{data.user.email}</p>
      <ul>
        {data.user.posts.map((post: any) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}

```

---

## Real-World Use Cases

### 1. Social Media Platform

```graphql
# Facebook/Instagram-style feed
query NewsFeed($cursor: String) {
  feed(first: 20, after: $cursor) {
    edges {
      node {
        ... on Post {
          id
          author { name avatar }
          content
          likes { count }
          comments(first: 3) {
            edges { node { body author { name } } }
          }
        }
        ... on Photo {
          id
          url
          author { name avatar }
          likes { count }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}

```

### 2. E-Commerce Platform

```graphql
# Product catalog with filtering
query ProductCatalog($filters: ProductFilters!) {
  products(filters: $filters) {
    edges {
      node {
        id
        name
        price
        images
        rating
        reviews(first: 5) {
          edges { node { rating body author { name } } }
        }
        variants {
          id
          name
          price
          inStock
        }
      }
    }
    totalCount
  }
}

```

### 3. Content Management System

```graphql
# Flexible content types
union ContentBlock = Paragraph | Image | Video | CodeBlock | Quote

type Page {
  id: ID!
  title: String!
  slug: String!
  blocks: [ContentBlock!]!
  author: User!
  publishedAt: DateTime
  seo: SEOFields
}

type SEOFields {
  title: String
  description: String
  ogImage: String
}

```

### 4. Real-time Dashboard

```graphql
# Live metrics
subscription DashboardMetrics {
  metricsUpdated {
    timestamp
    activeUsers
    revenue
    conversions
    errors {
      message
      count
      lastSeen
    }
  }
}

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
    posts: (parent) => db.post.findMany({ // N queries
      where: { authorId: parent.id }
    }),
  },
};

// GOOD: Use DataLoader
const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.post.findMany({
    where: { authorId: { in: userIds } }
  });
  return userIds.map(id => posts.filter(p => p.authorId === id));
});

```

### 2. Missing Error Handling

```typescript
// BAD: No error handling
const resolvers = {
  Query: {
    user: (_, { id }) => db.user.findById(id),
  },
};

// GOOD: Proper error handling
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      try {
        const user = await db.user.findById(id);
        if (!user) {
          throw new GraphQLError('User not found', {
            extensions: { code: 'NOT_FOUND', id }
          });
        }
        return user;
      } catch (error) {
        if (error instanceof GraphQLError) throw error;
        throw new GraphQLError('Internal server error', {
          extensions: { code: 'INTERNAL_ERROR' }
        });
      }
    },
  },
};

```

### 3. Exposing Sensitive Data

```graphql
# BAD: Exposing internal fields
type User {
  id: ID!
  name: String!
  passwordHash: String!  # Never expose!
  internalNotes: String!  # Never expose!
}

# GOOD: Use @omit or separate types
type User {
  id: ID!
  name: String!
  email: String!
  # passwordHash and internalNotes are not in the schema
}

```

### 4. Over-fetching in Nested Queries

```graphql
# BAD: Fetching everything
query {
  users {
    id
    name
    email
    posts {
      id
      title
      content
      author { id name email }  # Circular!
    }
  }
}

# GOOD: Request only what you need
query {
  users {
    id
    name
    posts {
      id
      title
    }
  }
}

```

### 5. Ignoring Pagination

```typescript
// BAD: No pagination - returns everything
const resolvers = {
  Query: {
    posts: () => db.post.findMany(),
  },
};

// GOOD: Implement pagination
const resolvers = {
  Query: {
    posts: async (_, { first, after }) => {
      const cursor = after ? { id: after } : undefined;
      const posts = await db.post.findMany({
        take: first + 1,
        skip: cursor ? 1 : 0,
        cursor,
        orderBy: { createdAt: 'desc' }
      });
      return {
        edges: posts.slice(0, first).map(post => ({
          node: post,
          cursor: post.id,
        })),
        pageInfo: {
          hasNextPage: posts.length > first,
          endCursor: posts[first - 1]?.id,
        },
      };
    },
  },
};

```

---

## Best Practices

### Schema Design

```text

1. Design schema-first, implementation-second

2. Use descriptive names (getUser, not fetchUserData)

3. Return type-safe errors with extensions

4. Use Input types for mutations

5. Implement proper pagination (Relay-style)

6. Use enums for fixed sets of values

7. Keep schema versionless (add fields, don't remove)

```

### Resolver Implementation

```text

1. Keep resolvers thin - delegate to service layer

2. Use DataLoader for N+1 prevention

3. Implement proper authorization

4. Cache resolved data appropriately

5. Use async/await consistently

6. Handle null cases explicitly

```

### Client Best Practices

```text

1. Use fragments for reusable selections

2. Implement query polling for non-critical data

3. Use optimistic updates for mutations

4. Implement proper loading/error states

5. Cache normalized data

6. Use variables instead of string interpolation

```

---

## Performance Considerations

### Query Complexity Analysis

```typescript
import { getComplexity, simpleEstimator, fieldExtensionsEstimator } from 'graphql-query-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    queryComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        fieldExtensionsEstimator(),
        simpleEstimator({ defaultComplexity: 1 })
      ],
      onComplete: (complexity) => {
        console.log('Query complexity:', complexity);
      }
    })
  ]
});

```

### Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)]
});

```

### Response Caching

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, { cache }) => {
      const cached = await cache.get(`user:${id}`);
      if (cached) return cached;

      const user = await db.user.findById(id);
      await cache.set(`user:${id}`, user, { ttl: 300 });
      return user;
    },
  },
};

```

---

## Interview Questions

### Beginner

1. **What is GraphQL?**
   GraphQL is a query language for APIs that allows clients to request exactly the data they need from a single endpoint.

2. **How does GraphQL differ from REST?**
   GraphQL uses a single endpoint with flexible queries, while REST uses multiple endpoints with fixed response structures. GraphQL eliminates over-fetching and under-fetching.

3. **What are the three root operation types?**

   - **Query**: Read operations
   - **Mutation**: Write operations
   - **Subscription**: Real-time operations

4. **What is a GraphQL schema?**
   A schema is a contract between client and server that defines the types, queries, mutations, and subscriptions available.

5. **What are scalar types in GraphQL?**
   Built-in leaf types: String, Int, Float, Boolean, and ID.

### Intermediate

6. **What is schema-first design?**
   Defining the GraphQL schema before implementation. The schema serves as the API contract and guides server development.

7. **How does GraphQL handle versioning?**
   Through schema evolution: add new fields/types without removing old ones. Deprecate with `@deprecated` directive instead of version bumping.

8. **What is introspection?**
   GraphQL's ability to query the schema itself using `__schema` and `__type` meta-fields, enabling tools like GraphiQL.

9. **What are Input types?**
   Special object types used exclusively for mutation arguments, enabling structured input with validation.

10. **How do you handle errors in GraphQL?**
    Return errors in the `errors` array with `message`, `locations`, `path`, and custom `extensions` (like error codes).

### Senior

11. **Explain the N+1 problem in GraphQL and how to solve it.**
    When resolving nested fields, each parent item triggers a separate database query. DataLoader solves this by batching and caching requests within a single execution.

12. **How would you implement authorization?**
    Use directives (@auth), context-based middleware, or field-level authorization in resolvers. Consider role-based (RBAC) or attribute-based (ABAC) access control.

13. **Describe your approach to schema governance.**
    Schema review process, breaking change detection (using tools like GraphQL Inspector), compatibility testing, and deprecation policies.

14. **How do you optimize GraphQL queries for mobile?**
    Query whitelisting, persisted queries, response caching, query complexity limits, and field-level caching strategies.

15. **Explain the difference between schema stitching and federation.**
    Schema stitching combines multiple schemas into one. Federation distributes a schema across multiple services with @key, @requires, and @provides directives.

### FAANG-style

16. **Design a GraphQL API for a social media feed.**
    Discuss: pagination (cursor-based), edge/node pattern, polymorphic types (union/interface), subscription for real-time updates, query complexity management.

17. **How would you handle a GraphQL service that receives 10M requests/day?**
    Caching layers (CDN, application, database), query complexity analysis, rate limiting, persisted queries, horizontal scaling, DataLoader optimization, monitoring.

18. **Explain your approach to migrating a REST API to GraphQL.**
    Strangler fig pattern, starting with high-value endpoints, maintaining backward compatibility, incremental adoption, GraphQL gateway over existing REST services.

19. **How do you prevent GraphQL from becoming a performance bottleneck?**
    Query depth/complexity limits, rate limiting per client, persisted queries, response caching, monitoring, query batching, and efficient resolvers.

20. **Describe how you would implement real-time features with subscriptions.**
    WebSocket transport, subscription filtering, connection management, scaling with Redis pub/sub, handling disconnected clients, security considerations.

### Follow-ups

21. **What happens when a resolver throws an error?**
    The error is caught and added to the `errors` array. Partial data may still be returned if some fields resolved successfully.

22. **How does Apollo Client normalize cache?**
    Uses `__typename` and `id` to create unique keys. Normalizes nested objects into a flat map, enabling efficient cache updates.

23. **What are fragment collocation and fragment spreads?**
    Collocation: defining fragments where the data is used. Spreads: using `...FragmentName` to include fragments in queries, enabling composition.

24. **How do you handle file uploads in GraphQL?**
    Use multipart form data spec (graphql-multipart-request-spec) or separate REST endpoints for uploads. Apollo Server supports this via Upload scalar.

25. **Explain the concept of schema directives.**
    Custom directives that add metadata to schema elements: `@deprecated`, `@auth`, `@cacheControl`, etc. Used for authorization, caching, and validation.

26. **How do you test GraphQL resolvers?**
    Unit tests with mocked context, integration tests with test database, schema snapshot tests, and query testing with tools like Apollo Server testing utilities.

27. **What are the trade-offs of using GraphQL over REST?**
    GraphQL: flexible but complex, single endpoint but needs tooling, type-safe but steeper learning curve. REST: simpler but rigid, multiple endpoints but easier caching.

28. **How do you handle GraphQL in microservices?**
    Use Apollo Federation or Schema Stitching to compose a unified schema from multiple services. Consider API gateway patterns.

29. **What monitoring/metrics would you track for a GraphQL API?**
    Query complexity, resolver execution time, error rates, cache hit rates, subscription connections, N+1 query counts, and client-specific metrics.

30. **How do you secure a GraphQL API?**
    Authentication (JWT/session), authorization (field-level), query complexity limits, rate limiting, persisted queries, CORS, input validation, and query whitelisting.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Core Concept** | Client specifies exact data needs |
| **Schema** | Type system defines API contract |
| **Operations** | Queries (read), Mutations (write), Subscriptions (real-time) |
| **Key Benefit** | Eliminates over/under-fetching |
| **Main Challenge** | N+1 problem (solved with DataLoader) |
| **Best Practice** | Schema-first, type-safe, secure by default |

---

## References & Learn More

- [GraphQL Official Spec](https://spec.graphql.org/)
- [GraphQL.org - Learn](https://graphql.org/learn/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [How to GraphQL](https://www.howtographql.com/)
- [Prisma GraphQL Guides](https://www.prisma.io/docs/graphql)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Relay Documentation](https://relay.dev/)
