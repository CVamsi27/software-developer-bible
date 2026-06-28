# Performance & Security

## Definition

**GraphQL Performance & Security** encompasses strategies and techniques to optimize query execution, prevent abuse, protect against attacks, and ensure reliable operation of GraphQL APIs in production environments.

```
Performance = Query Optimization + Caching + Rate Limiting + Monitoring
Security    = Authentication + Authorization + Input Validation + Attack Prevention
```

---

## Why Do We Need It?

### The Production Challenge

```
Without Performance & Security:
┌─────────────────────────────────────────────────────────────────┐
│  1. Denial of Service via complex queries                       │
│  2. N+1 query problems degrading performance                    │
│  3. Unbounded queries exhausting resources                      │
│  4. Missing authentication exposing sensitive data              │
│  5. No rate limiting allowing abuse                             │
│  6. Unmonitored queries hiding performance issues               │
└─────────────────────────────────────────────────────────────────┘

With Performance & Security:
┌─────────────────────────────────────────────────────────────────┐
│  1. Query complexity analysis prevents abuse                    │
│  2. DataLoader prevents N+1 queries                             │
│  3. Depth limiting stops deeply nested queries                  │
│  4. Authentication ensures only authorized access               │
│  5. Rate limiting prevents abuse                                │
│  6. Monitoring provides visibility                              │
└─────────────────────────────────────────────────────────────────┘
```

### Common Attacks

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Query Complexity** | Expensive queries exhaust resources | Complexity limits |
| **Denial of Service** | Malicious queries crash server | Rate limiting, timeouts |
| **Introspection Leak** | Schema exposed to attackers | Disable introspection |
| **Injection** | Malicious input executes code | Input validation |
| **Unauthorized Access** | Data exposed without auth | Field-level auth |

---

## How It Works

### Security Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Layer 1: HTTP Security                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  CORS    │  │  HTTPS   │  │ Headers  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Layer 2: Query Validation                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Depth   │  │Complexity│  │  Persisted│              │   │
│  │  │  Limit   │  │ Analysis │  │  Queries  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Layer 3: Authentication                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  JWT     │  │  OAuth   │  │ Session  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Layer 4: Authorization                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Role    │  │  Field   │  │ Directive│              │   │
│  │  │  Based   │  │  Level   │  │  Based   │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Layer 5: Input Validation                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Schema  │  │  Custom  │  │ Sanitize │              │   │
│  │  │  Valid   │  │  Valid   │  │  Input   │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Performance Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE OPTIMIZATION                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Caching Layers                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  CDN     │  │  HTTP    │  │  Query   │              │   │
│  │  │  Cache   │  │  Cache   │  │  Cache   │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  │  ┌──────────┐  ┌──────────┐                             │   │
│  │  │  Client  │  │  Redis   │                             │   │
│  │  │  Cache   │  │  Cache   │                             │   │
│  │  └──────────┘  └──────────┘                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Query Optimization                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Data    │  │  Batch   │  │  Query   │              │   │
│  │  │  Loader  │  │  ing     │  │  Persist │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Monitoring                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Tracing │  │  Metrics │  │  Alerts  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Query Complexity Analysis

```typescript
import { getComplexity, simpleEstimator, fieldExtensionsEstimator } from 'graphql-query-complexity';
import { ValidationRule } from 'graphql';

const complexityRule = (maximumComplexity: number): ValidationRule => {
  return (context) => ({
    Document(node) {
      const complexity = getComplexity({
        schema: context.getSchema(),
        operationName: context.getOperationName()?.value,
        query: node,
        variables: {},
        estimators: [
          fieldExtensionsEstimator(),
          simpleEstimator({ defaultComplexity: 1 })
        ],
      });

      if (complexity > maximumComplexity) {
        context.reportError(
          new GraphQLError(
            `Query too complex: ${complexity}. Maximum allowed: ${maximumComplexity}`,
            { extensions: { code: 'QUERY_TOO_COMPLEX', complexity, maximumComplexity } }
          )
        );
      }
    },
  });
};

// Usage
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityRule(1000)],
});
```

### Schema-Level Complexity Scoring

```graphql
# Assign complexity scores to fields
type Query {
  # Simple query: complexity 1
  user(id: ID!): User @complexity(value: 1)

  # List query: complexity 2 + multiplier
  users(first: Int): [User!]! @complexity(value: 2, multipliers: ["first"])

  # Expensive query: complexity 10
  analytics(dateRange: DateRange!): Analytics! @complexity(value: 10)
}

type User {
  # Simple field: no additional complexity
  id: ID!
  name: String!

  # List field with multiplier
  posts(first: Int): [Post!]! @complexity(value: 2, multipliers: ["first"])

  # Expensive computed field
  recommendations: [Post!]! @complexity(value: 5)
}
```

### Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(7)  // Maximum depth of 7
  ],
});

// Custom depth limit with field-specific rules
const customDepthLimit = (maxDepth: number) => {
  return (context) => ({
    Document(node) {
      const depth = calculateDepth(node);
      if (depth > maxDepth) {
        context.reportError(
          new GraphQLError(
            `Query depth ${depth} exceeds maximum ${maxDepth}`,
            { extensions: { code: 'QUERY_TOO_DEEP' } }
          )
        );
      }
    },
  });
};
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import { RedisStore } from 'rate-limit-redis';

// HTTP-level rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    sendCommand: (...args) => redis.call(...args),
  }),
  keyGenerator: (req) => {
    return req.headers.authorization || req.ip;
  },
  handler: (req, res) => {
    res.status(429).json({
      errors: [{
        message: 'Too many requests',
        extensions: { code: 'RATE_LIMIT_EXCEEDED' }
      }]
    });
  },
});

app.use('/graphql', limiter);

// Query-level rate limiting
const queryRateLimit = new Map<string, number>();

const queryLimiter = (maxQueries: number, windowMs: number) => {
  return (req, res, next) => {
    const userId = req.headers.authorization || req.ip;
    const now = Date.now();

    const userQueries = queryRateLimit.get(userId) || [];
    const recentQueries = userQueries.filter(time => now - time < windowMs);

    if (recentQueries.length >= maxQueries) {
      return res.status(429).json({
        errors: [{
          message: 'Query rate limit exceeded',
          extensions: { code: 'QUERY_RATE_LIMIT_EXCEEDED' }
        }]
      });
    }

    recentQueries.push(now);
    queryRateLimit.set(userId, recentQueries);
    next();
  };
};
```

### Persisted Queries

```typescript
import {
  ApolloServerPluginAutomaticPersistedQueries
} from '@apollo/server/plugin/automaticPersistedQueries';

// Server-side
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginAutomaticPersistedQueries({
      cache: new RedisCache(redis),
    }),
  ],
});

// Client-side
const client = new ApolloClient({
  link: createPersistedQueryLink({
    sha256,
    useGETForHashedQueries: true,
  }).concat(httpLink),
  cache: new InMemoryCache(),
});
```

### Authentication

```typescript
import jwt from 'jsonwebtoken';

// Context-based authentication
const createContext = async ({ req }) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return { currentUser: null };
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await db.user.findById(decoded.userId);

    if (!user || user.status !== 'ACTIVE') {
      return { currentUser: null };
    }

    return { currentUser: user };
  } catch (error) {
    return { currentUser: null };
  }
};

// Middleware authentication
const authenticate = async (resolve, parent, args, context, info) => {
  if (!context.currentUser) {
    throw new GraphQLError('Not authenticated', {
      extensions: { code: 'UNAUTHENTICATED' }
    });
  }
  return resolve(parent, args, context, info);
};
```

### Authorization

```typescript
// Field-level authorization
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      // Only admins can view other users
      if (context.currentUser?.role !== 'ADMIN' &&
          context.currentUser?.id !== id) {
        throw new GraphQLError('Not authorized', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
      return context.dataSources.userAPI.getUser(id);
    },
  },

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

// Directive-based authorization
const typeDefs = `
  directive @auth(requires: Role = USER) on FIELD_DEFINITION | OBJECT

  enum Role {
    ADMIN
    MODERATOR
    USER
  }

  type Query {
    adminOnly: String! @auth(requires: ADMIN)
    userOnly: String! @auth(requires: USER)
  }
`;

const authDirectiveTransformer = (schema) =>
  mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, 'auth')?.[0];
      if (authDirective) {
        const requires = authDirective.requires || 'USER';
        const originalResolve = fieldConfig.resolve;

        fieldConfig.resolve = async (parent, args, context, info) => {
          if (!context.currentUser) {
            throw new GraphQLError('Not authenticated', {
              extensions: { code: 'UNAUTHENTICATED' }
            });
          }

          if (requires === 'ADMIN' && context.currentUser.role !== 'ADMIN') {
            throw new GraphQLError('Not authorized', {
              extensions: { code: 'FORBIDDEN' }
            });
          }

          return originalResolve(parent, args, context, info);
        };
      }
      return fieldConfig;
    },
  });
```

### Input Validation

```typescript
import { z } from 'zod';

// Zod schema for validation
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  password: z.string().min(8).max(128),
  age: z.number().int().min(13).max(150).optional(),
});

// Resolver with validation
const resolvers = {
  Mutation: {
    createUser: async (_, { input }, context) => {
      // Validate input
      const result = CreateUserSchema.safeParse(input);

      if (!result.success) {
        const errors = result.error.issues.map(issue => ({
          field: issue.path.join('.'),
          message: issue.message,
          code: 'VALIDATION_ERROR',
        }));

        return { user: null, errors };
      }

      // Create user with validated data
      const user = await context.dataSources.userAPI.create(result.data);
      return { user, errors: [] };
    },
  },
};
```

### CORS Configuration

```typescript
import cors from 'cors';

// Production CORS
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com',
    ];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400,  // 24 hours
};

app.use('/graphql', cors(corsOptions));
```

### Response Caching

```typescript
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginCacheControl({ defaultMaxAge: 5 }),
    responseCachePlugin({
      sessionId: (requestContext) => {
        // Don't cache for authenticated users
        return requestContext.request.http?.headers.get('authorization') || null;
      },
      extraCacheKeyData: (requestContext) => {
        return requestContext.request.variables;
      },
    }),
  ],
});

// Schema with cache hints
const typeDefs = `
  type Query {
    # Cache for 1 minute, publicly
    popularPosts: [Post!]! @cacheControl(maxAge: 60, scope: PUBLIC)

    # No caching for personalized data
    currentUser: User @cacheControl(maxAge: 0, scope: PRIVATE)
  }
`;
```

---

## Real-World Use Cases

### 1. Production Security Configuration

```typescript
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginLandingPageProductionDefault } from '@apollo/server/plugin/landingPage/default';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    // Disable introspection in production
    ApolloServerPluginLandingPageProductionDefault({
      embed: true,
    }),
  ],
  introspection: process.env.NODE_ENV !== 'production',
  includeStacktraceInErrorMessages: process.env.NODE_ENV !== 'production',
  formatError: (formattedError, error) => {
    // Log error
    logger.error('GraphQL Error', {
      message: error.message,
      stack: error.stack,
      path: formattedError.path,
    });

    // Don't expose internal errors
    if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
      return {
        message: 'Internal server error',
        code: 'INTERNAL_SERVER_ERROR',
      };
    }

    return formattedError;
  },
});
```

### 2. Query Whitelisting

```typescript
import { createHash } from 'crypto';

// Client: Send persisted query
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

// Generate hash
const queryHash = createHash('sha256')
  .update(print(GET_USER))
  .digest('hex');

// Server: Allow only persisted queries
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginPersistedQueries({
      cache: new RedisCache(redis),
      allowArbitraryOperations: false,
    }),
  ],
});
```

### 3. Monitoring and Alerting

```typescript
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },
      sendReportsImmediately: process.env.NODE_ENV !== 'production',
      generateClientInfo: ({ request }) => ({
        clientName: request.http?.headers.get('apollographql-client-name') || 'unknown',
        clientVersion: request.http?.headers.get('apollographql-client-version') || 'unknown',
      }),
    }),
  ],
});

// Custom metrics plugin
const metricsPlugin = {
  requestDidStart() {
    const start = Date.now();

    return {
      willSendResponse({ operationName, response }) {
        const duration = Date.now() - start;

        // Send to metrics service
        metrics.histogram('graphql.request.duration', duration, {
          operationName,
          status: response.errors ? 'error' : 'success',
        });

        // Alert on slow queries
        if (duration > 1000) {
          alerting.warn('Slow GraphQL query', {
            operationName,
            duration,
          });
        }
      },
    };
  },
};
```

---

## Common Mistakes

### 1. Not Implementing Query Complexity Limits

```typescript
// BAD: No complexity limits
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

// GOOD: With complexity analysis
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityRule(1000)],
});
```

### 2. Exposing Introspection in Production

```typescript
// BAD: Introspection enabled
const server = new ApolloServer({
  typeDefs,
  resolvers,
  // Introspection on by default!
});

// GOOD: Disable in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
});
```

### 3. Missing Authentication

```typescript
// BAD: No authentication
const resolvers = {
  Query: {
    user: (_, { id }) => db.user.findById(id),  // Anyone can query
  },
};

// GOOD: Authentication in context
const resolvers = {
  Query: {
    user: (_, { id }, context) => {
      if (!context.currentUser) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      return db.user.findById(id);
    },
  },
};
```

### 4. Not Using DataLoader

```typescript
// BAD: N+1 queries
const resolvers = {
  User: {
    posts: (parent) => db.post.findMany({ where: { authorId: parent.id } }),
  },
};

// GOOD: DataLoader
const resolvers = {
  User: {
    posts: (parent, _, { loaders }) => loaders.postsByAuthor.load(parent.id),
  },
};
```

### 5. Missing Rate Limiting

```typescript
// BAD: No rate limiting
app.use('/graphql', expressMiddleware(server));

// GOOD: With rate limiting
app.use('/graphql', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
}), expressMiddleware(server));
```

---

## Best Practices

### Security Checklist

```
□ Disable introspection in production
□ Enable CORS with specific origins
□ Use HTTPS only
□ Implement authentication (JWT/OAuth)
□ Add field-level authorization
□ Validate all inputs
□ Sanitize error messages
□ Implement rate limiting
□ Use persisted queries
□ Log security events
□ Monitor for attacks
□ Regular security audits
```

### Performance Checklist

```
□ Implement DataLoader
□ Add query complexity limits
□ Enable response caching
□ Use persisted queries
□ Monitor query performance
□ Optimize database queries
□ Use connection pooling
□ Implement pagination
□ Cache expensive operations
□ Profile resolver execution
```

### Query Optimization

```typescript
// 1. Use DataLoader for N+1 prevention
const loaders = {
  user: new DataLoader(batchFn),
  post: new DataLoader(batchFn),
};

// 2. Cache expensive operations
const resolvers = {
  Query: {
    analytics: async (_, { dateRange }, context) => {
      const cached = await context.cache.get(`analytics:${dateRange}`);
      if (cached) return cached;

      const result = await computeAnalytics(dateRange);
      await context.cache.set(`analytics:${dateRange}`, result, { ttl: 3600 });
      return result;
    },
  },
};

// 3. Use query complexity limits
const server = new ApolloServer({
  validationRules: [complexityRule(1000)],
});
```

---

## Performance Considerations

### Monitoring Metrics

```
Key Metrics to Track:
┌─────────────────────────────────────────────────────────────────┐
│  1. Query Complexity    - Average and max complexity            │
│  2. Response Time       - P50, P95, P99 latencies              │
│  3. Error Rate          - 4xx and 5xx error percentages        │
│  4. Cache Hit Rate      - Percentage of cached responses       │
│  5. N+1 Queries         - Count of batched vs unbatched        │
│  6. Active Subscriptions - WebSocket connection count          │
│  7. Query Throughput    - Requests per second                  │
│  8. Resolver Duration   - Time per resolver                    │
└─────────────────────────────────────────────────────────────────┘
```

### Caching Strategy

```
Cache Layers:
┌─────────────────────────────────────────────────────────────────┐
│  Client Cache (Apollo Client)                                   │
│  └─ Normalized cache, automatic updates                        │
│                                                                  │
│  CDN Cache (Cloudflare/CloudFront)                              │
│  └─ Static queries, persisted queries                          │
│                                                                  │
│  HTTP Cache (Browser)                                           │
│  └─ Cache-Control headers                                      │
│                                                                  │
│  Application Cache (Redis/Memcached)                            │
│  └─ Query results, computed data                               │
│                                                                  │
│  Database Cache                                                  │
│  └─ Query cache, connection pooling                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Interview Questions

### Beginner

1. **What is query complexity analysis?**
   A technique to calculate the "cost" of a GraphQL query based on field complexity scores. Prevents expensive queries from exhausting resources.

2. **What is depth limiting?**
   Restricting how deeply nested a query can be. Prevents queries like `user { posts { comments { author { ... } } } }`.

3. **What is rate limiting?**
   Restricting the number of requests a client can make in a given time period. Prevents abuse and DoS attacks.

4. **What is CORS?**
   Cross-Origin Resource Sharing. A mechanism that allows or restricts resources to be requested from another domain.

5. **Why disable introspection in production?**
   Introspection exposes the entire schema, allowing attackers to discover vulnerabilities and craft malicious queries.

### Intermediate

6. **How do you implement authentication in GraphQL?**
   Use context to verify tokens, set `currentUser`, and check in resolvers. Use directives for declarative auth.

7. **What is the difference between authentication and authorization?**
   Authentication: verifying identity. Authorization: verifying permissions. GraphQL needs both.

8. **How do you handle rate limiting for GraphQL?**
   HTTP-level (per request), query-level (per operation), and complexity-based (per query cost).

9. **What are persisted queries?**
   Pre-registered query hashes that allow clients to send only the hash instead of the full query. Improves security and performance.

10. **How do you implement field-level authorization?**
    Check permissions in resolvers, use directives, or implement middleware for declarative authorization.

### Senior

11. **Design a security architecture for a public GraphQL API.**
    Multiple layers: HTTP security, query validation, authentication, authorization, input validation, and monitoring.

12. **How would you handle a DDoS attack on a GraphQL API?**
    Rate limiting, query complexity limits, WAF rules, CDN caching, and auto-scaling.

13. **Explain your approach to GraphQL security auditing.**
    Schema review, dependency scanning, penetration testing, access control verification, and monitoring.

14. **How do you secure GraphQL in a microservices architecture?**
    Gateway authentication, service-to-service auth, token propagation, and centralized policy enforcement.

15. **Design a monitoring system for GraphQL performance.**
    Distributed tracing, metrics collection, alerting, dashboards, and anomaly detection.

### FAANG-style

16. **Design a rate limiting system for a multi-tenant GraphQL API.**
    Tenant-based quotas, query complexity limits, adaptive throttling, and usage analytics.

17. **How would you implement query whitelisting for a mobile app?**
    Persisted queries, client registration, version control, and fallback mechanisms.

18. **Explain your approach to GraphQL security in a regulated industry.**
    Compliance requirements, audit logging, data encryption, access controls, and regular assessments.

19. **How do you prevent information leakage in GraphQL errors?**
    Sanitize error messages, use error codes, log detailed errors server-side, and return generic messages to clients.

20. **Design a real-time monitoring system for GraphQL performance.**
    Streaming metrics, anomaly detection, automated alerting, and correlation with business metrics.

### Follow-ups

21. **What happens when a query exceeds complexity limits?**
    Server returns an error with `QUERY_TOO_COMPLEX` code. Client should retry with simpler query.

22. **How do you handle CORS preflight requests?**
    Configure `Access-Control-Allow-Origin`, `Methods`, and `Headers`. Use `maxAge` to cache preflight responses.

23. **What is the difference between JWT and session authentication?**
    JWT: stateless, token-based, scalable. Session: server-side storage, more secure, requires sticky sessions.

24. **How do you implement query batching?**
    Use `BatchHttpLink` on client, configure server to accept batches, and handle partial failures.

25. **What are the trade-offs of persisted queries?**
    Pros: better security, smaller payloads, caching. Cons: deployment complexity, versioning challenges.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Query Complexity** | Analyze and limit expensive queries |
| **Depth Limiting** | Prevent deeply nested queries |
| **Rate Limiting** | Prevent abuse at HTTP and query level |
| **Persisted Queries** | Whitelist allowed queries |
| **Authentication** | Verify identity via JWT/OAuth |
| **Authorization** | Verify permissions at field level |
| **Input Validation** | Validate and sanitize all inputs |
| **Caching** | Multiple layers for performance |
| **Monitoring** | Track metrics and alert on issues |

---

## References & Learn More

- [GraphQL Security Best Practices](https://www.apollographql.com/blog/graphql-security/5-ways-to-secure-your-graphql-api/)
- [Query Complexity Analysis](https://github.com/slicknode/graphql-query-complexity)
- [Depth Limiting](https://github.com/stems/graphql-depth-limit)
- [Apollo Server Security](https://www.apollographql.com/docs/apollo-server/security/security-probest/)
- [GraphQL Rate Limiting](https://github.com/ravener/graphql-rate-limit)
- [OWASP GraphQL Security](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
