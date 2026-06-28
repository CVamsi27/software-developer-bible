# Apollo Server

## Definition

**Apollo Server** is the reference implementation of a GraphQL server in JavaScript/TypeScript. It's a production-ready, spec-compliant GraphQL server that integrates with any Node.js HTTP framework (Express, Fastify, Koa, etc.) or runs standalone. It provides built-in features for query validation, execution, error handling, caching, and monitoring.

```
Apollo Server = GraphQL Spec + HTTP Transport + Middleware + Tooling + Studio
```

---

## Why Do We Need It?

### Building GraphQL Servers Without Apollo

```
Without Apollo Server:
┌─────────────────────────────────────────────────────────────────┐
│  1. Implement HTTP server from scratch                          │
│  2. Parse and validate GraphQL queries                          │
│  3. Execute resolvers manually                                  │
│  4. Handle CORS, error formatting, etc.                         │
│  5. No built-in tooling (Playground, tracing, etc.)             │
└─────────────────────────────────────────────────────────────────┘

With Apollo Server:
┌─────────────────────────────────────────────────────────────────┐
│  1. Single configuration                                       │
│  2. Automatic query validation and execution                    │
│  3. Built-in CORS, error handling, caching                     │
│  4. GraphiQL/Apollo Sandbox for development                     │
│  5. Apollo Studio for production monitoring                     │
│  6. Plugin system for extensibility                             │
└─────────────────────────────────────────────────────────────────┘
```

### Apollo Server vs Alternatives

| Feature | Apollo Server | Yoga Server | Mercurius |
|---------|---------------|-------------|-----------|
| **Maintained by** | Apollo | The Guild | Fastify |
| **Ecosystem** | Apollo Client, Studio | GraphQL.js | Fastify |
| **File uploads** | Yes (via plugin) | Built-in | Built-in |
| **Subscriptions** | WebSocket | WebSocket | WebSocket |
| **Federation** | Yes | Yes | Limited |
| **Performance** | Good | Better | Good |

---

## How It Works

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                       APOLLO SERVER ARCHITECTURE                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    HTTP Layer                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│   │
│  │  │ Express  │  │ Fastify  │  │  Koa     │  │ Standalone││   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│   │
│  │       └──────────────┴──────────────┴──────────────┘      │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│  ┌─────────────────────────▼────────────────────────────────┐   │
│  │                  Apollo Server Core                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │    Parser    │  │   Validator  │  │   Executor   │  │   │
│  │  │              │  │              │  │              │  │   │
│  │  │  Query → AST │  │  AST → Valid │  │  Valid → Data│  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│  ┌─────────────────────────▼────────────────────────────────┐   │
│  │                  Plugin System                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│   │
│  │  │  Usage   │  │ Response │  │ Cache    │  │ Custom   ││   │
│  │  │ Reporting│  │  Cache   │  │ Control  │  │ Plugins  ││   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘│   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Request Lifecycle

```
1. HTTP Request arrives
        │
        ▼
2. HTTP Framework (Express/Fastify) receives
        │
        ▼
3. Apollo Server middleware processes
        │
        ├── Parse request body
        │
        ├── Extract query, variables, operationName
        │
        ▼
4. Query parsing (query string → AST)
        │
        ├── Invalid syntax → 400 error
        │
        ▼
5. Schema validation (AST against schema)
        │
        ├── Invalid query → 400 error
        │
        ▼
6. Plugin hooks execute
        │
        ├── requestDidStart
        │
        ▼
7. Context creation
        │
        ├── context(req) → { dataSources, loaders, etc. }
        │
        ▼
8. Resolver execution
        │
        ├── Root resolvers
        │
        ├── Field resolvers (with DataLoader)
        │
        ▼
9. Response formatting
        │
        ├── Format success response
        │
        ├── Format error response
        │
        ▼
10. Plugin hooks execute
        │
        ├── willSendResponse
        │
        ▼
11. HTTP Response sent
```

---

## Code Examples

### Basic Setup (v4)

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `
  type Query {
    hello: String!
    user(id: ID!): User
  }

  type User {
    id: ID!
    name: String!
    email: String!
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello, World!',
    user: async (_, { id }, context) => {
      return context.dataSources.userAPI.getUser(id);
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => ({
    dataSources: {
      userAPI: new UserAPI(),
    },
  }),
});

console.log(`Server ready at ${url}`);
```

### Express Integration

```typescript
import express from 'express';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import cors from 'cors';

const app = express();
const server = new ApolloServer({ typeDefs, resolvers });

await server.start();

app.use(
  '/graphql',
  cors<cors.Request>(),
  express.json(),
  expressMiddleware(server, {
    context: async ({ req }) => ({
      token: req.headers.authorization,
      dataSources: {
        userAPI: new UserAPI(),
        postAPI: new PostAPI(),
      },
    }),
  })
);

app.listen(4000, () => {
  console.log('Server running at http://localhost:4000/graphql');
});
```

### Fastify Integration

```typescript
import Fastify from 'fastify';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { ApolloServer } from '@apollo/server';
import { fastifyApolloDrainPlugin } from '@as-integrations/fastify';

const app = Fastify();
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [fastifyApolloDrainPlugin(app)],
});

await server.start();

app.register(server.createHandler({ path: '/graphql' }));

app.listen({ port: 4000 }, () => {
  console.log('Server running at http://localhost:4000/graphql');
});
```

### Context with Authentication

```typescript
import jwt from 'jsonwebtoken';

const createContext = async ({ req }) => {
  const token = req.headers.authorization?.replace('Bearer ', '') || '';
  let currentUser = null;

  try {
    if (token) {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      currentUser = await db.user.findById(decoded.userId);
    }
  } catch (error) {
    // Invalid token - user remains null
  }

  return {
    currentUser,
    dataSources: {
      userAPI: new UserAPI(),
      postAPI: new PostAPI(),
    },
    loaders: {
      user: createUserLoader(),
      post: createPostLoader(),
    },
    pubsub: new PubSub(),
  };
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: createContext,
});
```

### Plugin System

```typescript
import { ApolloServerPlugin } from '@apollo/server';

// Custom logging plugin
const loggingPlugin: ApolloServerPlugin = {
  async requestDidStart(requestContext) {
    const start = Date.now();
    
    console.log(`Request started: ${requestContext.request.query}`);

    return {
      async willSendResponse(requestContext) {
        const duration = Date.now() - start;
        console.log(`Request completed in ${duration}ms`);
      },

      async didEncounterErrors(requestContext) {
        for (const error of requestContext.errors) {
          console.error('GraphQL Error:', error.message);
        }
      },
    };
  },
};

// Usage reporting plugin
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    loggingPlugin,
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },  // Don't send sensitive data
    }),
  ],
});
```

### Schema-First with SDL File

```typescript
import { readFileSync } from 'fs';
import { makeExecutableSchema } from '@graphql-tools/schema';

const typeDefs = readFileSync('./schema.graphql', 'utf-8');

const schema = makeExecutableSchema({
  typeDefs,
  resolvers,
});

const server = new ApolloServer({
  schema,
  resolvers,  // Can also pass resolvers here
});
```

### Code-First with TypeGraphQL

```typescript
import 'reflect-metadata';
import { buildSchema } from 'type-graphql';
import { UserResolver } from './resolvers/UserResolver';
import { PostResolver } from './resolvers/PostResolver';

const schema = await buildSchema({
  resolvers: [UserResolver, PostResolver],
  validate: true,
});

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginLandingPageLocalDefault({ embed: true }),
  ],
});
```

### File Uploads

```typescript
import { GraphQLUpload, graphqlUploadExpress } from 'graphql-upload';
import { createWriteStream } from 'fs';

const typeDefs = `
  scalar Upload

  type Mutation {
    uploadFile(file: Upload!): File!
  }

  type File {
    filename: String!
    mimetype: String!
    encoding: String!
    url: String!
  }
`;

const resolvers = {
  Upload: GraphQLUpload,
  Mutation: {
    uploadFile: async (_, { file }) => {
      const { createReadStream, filename, mimetype, encoding } = await file;
      
      const stream = createReadStream();
      const path = `./uploads/${filename}`;
      
      await new Promise((resolve, reject) => {
        stream
          .pipe(createWriteStream(path))
          .on('finish', resolve)
          .on('error', reject);
      });

      return {
        filename,
        mimetype,
        encoding,
        url: `/uploads/${filename}`,
      };
    },
  },
};

// Add middleware for Express
app.use(graphqlUploadExpress({ maxFileSize: 10000000, maxFiles: 10 }));
```

### Subscriptions

```typescript
import { WebSocketServer } from 'ws';
import { useServer } from 'ws.use/server';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const typeDefs = `
  type Subscription {
    postAdded: Post!
    commentAdded(postId: ID!): Comment!
  }
`;

const resolvers = {
  Subscription: {
    postAdded: {
      subscribe: () => pubsub.asyncIterator(['POST_ADDED']),
    },
    commentAdded: {
      subscribe: (_, { postId }) => {
        return pubsub.asyncIterator(`COMMENT_ADDED_${postId}`);
      },
    },
  },
};

// WebSocket server
const httpServer = createServer(app);
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});
```

### Health Check and Liveness Probes

```typescript
// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Readiness probe
app.get('/ready', async (req, res) => {
  try {
    // Check database connection
    await db.raw('SELECT 1');
    
    // Check Redis connection
    await redis.ping();
    
    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// GraphQL introspection check
app.get('/graphql/introspection', async (req, res) => {
  const result = await server.executeOperation({
    query: '{ __schema { queryType { name } } }',
  });
  
  res.status(200).json(result);
});
```

---

## Real-World Use Cases

### 1. Production Server Configuration

```typescript
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { ApolloServerPluginLandingPageProductionDefault } from '@apollo/server/plugin/landingPage/default';
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    ApolloServerPluginCacheControl({ defaultMaxAge: 5 }),
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },
      sendReportsImmediately: true,
    }),
    ApolloServerPluginLandingPageProductionDefault({
      graphRef: 'my-graph@production',
      embed: true,
    }),
  ],
  introspection: process.env.NODE_ENV !== 'production',
  includeStacktraceInErrorMessages: process.env.NODE_ENV !== 'production',
  formatError: (error) => {
    console.error('GraphQL Error:', error);
    return {
      message: error.message,
      code: error.extensions?.code,
      path: error.path,
    };
  },
});
```

### 2. Multi-Tenant Server

```typescript
const createContext = async ({ req }) => {
  const tenantId = req.headers['x-tenant-id'] || 'default';
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  let currentUser = null;
  if (token) {
    currentUser = await verifyToken(token, tenantId);
  }

  return {
    tenantId,
    currentUser,
    dataSources: createTenantDataSources(tenantId),
    loaders: createTenantLoaders(tenantId),
  };
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: createContext,
});
```

### 3. GraphQL Gateway

```typescript
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://users-service:4001/graphql' },
      { name: 'posts', url: 'http://posts-service:4002/graphql' },
      { name: 'comments', url: 'http://comments-service:4003/graphql' },
    ],
  },
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        request.http.headers.set('x-tenant-id', context.tenantId);
        request.http.headers.set('authorization', context.token);
      },
    });
  },
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
});
```

---

## Common Mistakes

### 1. Not Using Apollo Server Plugins

```typescript
// BAD: No plugins configured
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

// GOOD: Production plugins
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    ApolloServerPluginUsageReporting({ enabled: true }),
    ApolloServerPluginCacheControl(),
    ApolloServerPluginLandingPageProductionDefault(),
  ],
});
```

### 2. Missing Error Handling

```typescript
// BAD: Generic error handling
const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => error,
});

// GOOD: Proper error handling
const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    // Log error
    logger.error('GraphQL Error', {
      message: error.message,
      stack: error.stack,
      path: formattedError.path,
    });

    // Don't expose internal errors in production
    if (process.env.NODE_ENV === 'production') {
      if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
        return {
          message: 'Internal server error',
          code: 'INTERNAL_SERVER_ERROR',
        };
      }
    }

    return formattedError;
  },
});
```

### 3. Not Using Apollo Studio

```typescript
// BAD: No monitoring
const server = new ApolloServer({ typeDefs, resolvers });

// GOOD: With Studio reporting
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },
      sendReportsImmediately: process.env.NODE_ENV !== 'production',
    }),
  ],
});
```

### 4. Forgetting to Drain HTTP Server

```typescript
// BAD: Server doesn't drain properly
const httpServer = createServer(app);
const server = new ApolloServer({ typeDefs, resolvers });
await server.start();
app.use('/graphql', expressMiddleware(server));

// GOOD: Drain HTTP server
const httpServer = createServer(app);
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [ApolloServerPluginDrainHttpServer({ httpServer })],
});
await server.start();
app.use('/graphql', expressMiddleware(server));
```

### 5. Exposing Introspection in Production

```typescript
// BAD: Introspection enabled in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  // Introspection enabled by default!
});

// GOOD: Disable introspection in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
});
```

---

## Best Practices

### Configuration

```
1. Use environment variables for configuration
   - API keys
   - Database connections
   - Feature flags

2. Enable plugins for production
   - Usage reporting
   - Cache control
   - Landing page
   - HTTP server drain

3. Configure error handling
   - Log errors
   - Don't expose internals
   - Use error codes

4. Disable introspection in production
   - Security through obscurity
   - Prevent schema discovery
```

### Context Creation

```
1. Keep context lightweight
   - Don't create heavy objects
   - Use DataLoader for batching

2. Handle authentication in context
   - Verify tokens
   - Set currentUser

3. Create per-request instances
   - DataSources
   - Loaders
   - Cache connections
```

### Development vs Production

```
Development:
  - Enable introspection
  - Enable Playground/Sandbox
  - Include stack traces
  - Enable CORS for localhost

Production:
  - Disable introspection
  - Disable Playground (or use embedded)
  - Don't include stack traces
  - Restrict CORS
  - Enable usage reporting
  - Enable response caching
```

---

## Performance Considerations

### Response Caching

```typescript
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginCacheControl({
      defaultMaxAge: 5,  // Default 5 second cache
    }),
  ],
});

// In schema
const typeDefs = `
  type Query {
    # Cache for 1 minute
    popularPosts: [Post!]! @cacheControl(maxAge: 60)
    
    # No caching
    currentUser: User @cacheControl(maxAge: 0, scope: PRIVATE)
  }

  type Post {
    # Cache for 1 hour
    content: String! @cacheControl(maxAge: 3600)
  }
`;
```

### Query Complexity Limits

```typescript
import { depthLimit } from 'graphql-depth-limit';
import { createComplexityRule } from 'graphql-query-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(7),
    createComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        fieldExtensionsEstimator(),
        simpleEstimator({ defaultComplexity: 1 })
      ],
      onComplete: (complexity) => {
        if (complexity > 1000) {
          throw new Error(`Query too complex: ${complexity}`);
        }
      }
    })
  ],
});
```

### Batched Queries

```typescript
// Apollo Server supports query batching
const server = new ApolloServer({
  typeDefs,
  resolvers,
  allowBatchedHttpRequests: true,
});
```

---

## Interview Questions

### Beginner

1. **What is Apollo Server?**
   Apollo Server is a reference implementation of a GraphQL server. It handles query parsing, validation, execution, and HTTP transport.

2. **How do you set up Apollo Server with Express?**
   Use `@apollo/server/express4` package. Create server, start it, and use `expressMiddleware` middleware.

3. **What is the context function?**
   The context function runs per request and returns an object that's available to all resolvers. It's used for authentication, data sources, and loaders.

4. **What are Apollo Server plugins?**
   Plugins extend Apollo Server's functionality. They hook into lifecycle events like request start, response send, etc.

5. **What is Apollo Studio?**
   Apollo Studio is a cloud-based platform for monitoring, analyzing, and validating GraphQL operations.

### Intermediate

6. **How do you handle CORS in Apollo Server?**
   Use CORS middleware (like `cors` package) or configure Apollo Server's built-in CORS options.

7. **What is the difference between `formatError` and error plugins?**
   `formatError` transforms error responses. Plugins can intercept errors before formatting for logging, reporting, etc.

8. **How do you implement file uploads?**
   Use `graphql-upload` package with middleware. Configure `Upload` scalar and handle streams in resolvers.

9. **What is the Apollo Server landing page?**
   Built-in GraphQL IDE for development (Playground/Sandbox). Can be embedded or disabled in production.

10. **How do you handle subscriptions?**
    Use WebSocket server (ws) with `ws.use` package. Configure `useServer` for subscription handling.

### Senior

11. **How would you deploy Apollo Server to production?**
    Use Docker/Kubernetes, configure health checks, enable usage reporting, set up caching, and monitor with Apollo Studio.

12. **Explain Apollo Server's caching strategy.**
    Response caching (HTTP cache headers), field-level caching (`@cacheControl`), and query complexity analysis.

13. **How do you handle multi-tenancy?**
    Tenant ID in context, separate data sources per tenant, and tenant-aware resolvers.

14. **What is Apollo Federation?**
    Distributes a GraphQL schema across multiple services using `@key`, `@requires`, and `@provides` directives.

15. **How do you monitor Apollo Server in production?**
    Apollo Studio for metrics, custom plugins for logging, APM tools (New Relic, Datadog), and health checks.

### FAANG-style

16. **Design a production Apollo Server architecture for a high-traffic API.**
    Consider: horizontal scaling, caching layers, query complexity limits, rate limiting, monitoring, and disaster recovery.

17. **How would you migrate from Express to Fastify with Apollo Server?**
    Swap HTTP framework, update middleware, test compatibility, and benchmark performance.

18. **Explain your approach to Apollo Server security hardening.**
    Introspection off, CORS restricted, rate limiting, query depth/complexity limits, input validation, and authentication.

19. **How do you handle Apollo Server in a serverless environment?**
    Use `@apollo/server` with Lambda/Cloud Functions, configure cold starts, and handle stateless context.

20. **Design a monitoring dashboard for Apollo Server.**
    Metrics: query complexity, resolver time, error rates, cache hits. Visualization: Apollo Studio + custom dashboards.

### Follow-ups

21. **What happens when Apollo Server receives an invalid query?**
    Returns 400 Bad Request with validation errors in the `errors` array.

22. **How does Apollo Server handle CORS?**
    Uses HTTP framework's CORS middleware or built-in options. Configure allowed origins, methods, and headers.

23. **What is the difference between Apollo Server and Apollo Gateway?**
    Server: single GraphQL endpoint. Gateway: routes queries to multiple federated services.

24. **How do you handle Apollo Server in development vs production?**
    Development: introspection on, Sandbox enabled, stack traces. Production: introspection off, usage reporting, no stack traces.

25. **What are the limitations of Apollo Server?**
    Single language (Node.js), requires Apollo ecosystem for full features, subscription scaling challenges.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Setup** | Single configuration, multiple frameworks |
| **Context** | Per-request state for auth, data sources |
| **Plugins** | Extend functionality (logging, caching) |
| **Production** | Disable introspection, enable reporting |
| **Caching** | HTTP headers, field-level, query complexity |
| **Monitoring** | Apollo Studio + custom plugins |

---

## References & Learn More

- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [Apollo Server Plugins](https://www.apollographql.com/docs/apollo-server/integrations/plugins/)
- [Apollo Federation](https://www.apollographql.com/docs/federation/)
- [Apollo Studio](https://www.apollographql.com/studio/)
- [GraphQL Upload Spec](https://github.com/jaydenseric/graphql-multipart-request-spec)
- [WebSocket Subscriptions](https://www.apollographql.com/docs/apollo-server/data/subscriptions/)
