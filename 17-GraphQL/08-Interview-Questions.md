# GraphQL Interview Questions

## Definition

This comprehensive guide covers the **30 most frequently asked GraphQL interview questions** with detailed answers, code examples, and explanations. Questions range from beginner to FAANG-level and cover schema design, resolvers, performance, security, and architecture.

---

## Why Do We Need It?

### Interview Preparation Strategy

```text
GraphQL Interview Focus Areas:
┌─────────────────────────────────────────────────────────────────┐
│  1. Core Concepts    → Schema, types, queries, mutations        │
│  2. Design Patterns  → Schema-first, pagination, error handling│
│  3. Performance      → N+1, DataLoader, caching, complexity    │
│  4. Security         → Auth, authorization, query validation   │
│  5. Architecture     → Federation, gateways, microservices     │
│  6. Tooling          → Apollo Server/Client, codegen, testing  │
└─────────────────────────────────────────────────────────────────┘

```

---

## Questions & Answers

### Beginner (5-10)

#### 1. What is GraphQL?

**Answer:** GraphQL is a query language for APIs and a runtime for executing those queries. It allows clients to request exactly the data they need from a single endpoint, eliminating over-fetching and under-fetching.

**Key Points:**

- Single endpoint (unlike REST's multiple endpoints)
- Client specifies response shape
- Strongly typed schema
- Introspective (self-documenting)

```graphql
# Client gets exactly what it asks for
query {
  user(id: "1") {
    name
    email
  }
}

```

---

#### 2. How does GraphQL differ from REST?

**Answer:**

| Aspect | GraphQL | REST |
|--------|---------|------|
| **Endpoints** | Single `/graphql` | Multiple `/users`, `/posts` |
| **Data Fetching** | Client specifies | Server determines |
| **Versioning** | Schema evolution | URL versioning |
| **Over-fetching** | No | Yes |
| **Under-fetching** | No | Yes |
| **Caching** | HTTP-level | Built-in HTTP caching |

**REST Example (3 requests):**

```typescript
GET /api/users/1
GET /api/users/1/posts
GET /api/posts/1/comments

```

**GraphQL Example (1 request):**

```graphql
query {
  user(id: "1") {
    name
    posts {
      title
      comments { body }
    }
  }
}

```

---

#### 3. What is a GraphQL schema?

**Answer:** A schema is a contract between client and server that defines the types, relationships, and operations available in the API. It's written in Schema Definition Language (SDL).

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

type Mutation {
  createUser(name: String!, email: String!): User!
}

```

---

#### 4. What are the three root operation types?

**Answer:**

- **Query**: Read operations (idempotent, parallel execution)
- **Mutation**: Write operations (sequential, side effects allowed)
- **Subscription**: Real-time operations (WebSocket-based)

```graphql
query { ... }     # Read
mutation { ... }  # Write
subscription { ... }  # Real-time

```

---

#### 5. What are scalar types in GraphQL?

**Answer:** Built-in leaf types that hold values:

- `String` - Text
- `Int` - 32-bit integer
- `Float` - Double-precision floating point
- `Boolean` - true/false
- `ID` - Unique identifier

Custom scalars can be defined:

```graphql
scalar DateTime
scalar JSON
scalar URL
scalar Email

```

---

#### 6. What is the `!` (non-null) modifier?

**Answer:** The `!` indicates a field is non-null. Without `!`, fields can return `null`.

```graphql
type User {
  id: ID!        # Never null
  name: String!  # Never null
  email: String  # Can be null
  bio: String    # Can be null
}

```

---

#### 7. What are arguments in GraphQL?

**Answer:** Arguments allow passing parameters to fields.

```graphql
type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
}

# Usage
query {
  user(id: "1") {
    name
  }
}

```

---

#### 8. What is introspection?

**Answer:** GraphQL's ability to query the schema itself. Useful for tools like GraphiQL and code generators.

```graphql
# Query the schema
query {
  __schema {
    types {
      name
      kind
    }
  }
}

# Query a specific type
query {
  __type(name: "User") {
    name
    fields {
      name
      type { name }
    }
  }
}

```

---

#### 9. What is the difference between `[String]` and `[String!]`?

**Answer:**

- `[String]` - List can be null, items can be null
- `[String!]` - List can be null, items cannot be null
- `[String!]!` - List cannot be null, items cannot be null

```graphql
type User {
  tags: [String]        # ["a", null, "b"] or null
  friends: [String!]    # ["a", "b"] or null
  posts: [Post!]!       # Never null, items never null
}

```

---

#### 10. What is a fragment?

**Answer:** A reusable piece of query logic that can be spread into multiple queries.

```graphql
fragment UserFields on User {
  id
  name
  email
}

query {
  user(id: "1") {
    ...UserFields
    posts {
      title
      author {
        ...UserFields
      }
    }
  }
}

```

---

### Intermediate (5-10)

#### 11. What is the N+1 problem in GraphQL?

**Answer:** When resolving nested fields, each parent item triggers a separate database query.

```typescript
// BAD: 1 query for users + N queries for posts
const resolvers = {
  Query: { users: () => db.user.findMany() },
  User: {
    posts: (parent) => db.post.findMany({ where: { authorId: parent.id } }),
  },
};

```

**Solution:** Use DataLoader to batch queries:

```typescript
const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.post.findMany({ where: { authorId: { in: userIds } } });
  return userIds.map(id => posts.filter(p => p.authorId === id));
});

const resolvers = {
  User: {
    posts: (parent, _, { loaders }) => loaders.post.load(parent.id),
  },
};

```

---

#### 12. What is DataLoader?

**Answer:** A utility that batches and caches database queries within a single execution cycle.

```typescript
const userLoader = new DataLoader(async (ids) => {
  const users = await db.user.findMany({ where: { id: { in: ids } } });
  const userMap = new Map(users.map(u => [u.id, u]));
  return ids.map(id => userMap.get(id));
});

// In resolver
User: {
  author: (parent, _, { loaders }) => loaders.user.load(parent.authorId),
}

```

---

#### 13. How do you implement pagination in GraphQL?

**Answer:** Use the Relay Connection pattern:

```graphql
type Query {
  posts(first: Int, after: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}

```

---

#### 14. What are Input types?

**Answer:** Special object types used exclusively for mutation arguments.

```graphql
input CreateUserInput {
  name: String!
  email: String!
  password: String!
  age: Int
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

```

---

#### 15. How do you handle errors in GraphQL?

**Answer:** Return errors in the `errors` array with custom extensions:

```typescript
throw new GraphQLError('User not found', {
  extensions: { code: 'NOT_FOUND', id }
});

```

Response:

```json
{
  "data": { "user": null },
  "errors": [{
    "message": "User not found",
    "extensions": { "code": "NOT_FOUND", "id": "1" }
  }]
}

```

---

#### 16. What is schema-first vs code-first?

**Answer:**

**Schema-first:** Write SDL first, implement resolvers second.

```graphql
type User { id: ID!, name: String! }

```

**Code-first:** Define types in code, generate schema.

```typescript
@ObjectType()
class User {
  @Field(() => ID)
  id: string;

  @Field()
  name: string;
}

```

---

#### 17. What are Enums in GraphQL?

**Answer:** Enum types represent a fixed set of values.

```graphql
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type Post {
  status: PostStatus!
}

```

---

#### 18. What are Interfaces and Unions?

**Answer:**

**Interface:** Defines a set of fields that implementing types must have.

```graphql
interface Node { id: ID! }
type User implements Node { id: ID!, name: String! }

```

**Union:** A type that can be one of several types.

```graphql
union SearchResult = User | Post | Tag

```

---

#### 19. How do you handle file uploads in GraphQL?

**Answer:** Use multipart form data specification or separate REST endpoints.

```typescript
import { GraphQLUpload } from 'graphql-upload';

const resolvers = {
  Upload: GraphQLUpload,
  Mutation: {
    uploadFile: async (_, { file }) => {
      const { createReadStream, filename } = await file;
      // Handle stream
    },
  },
};

```

---

#### 20. What is the `__typename` field?

**Answer:** Returns the actual type name of an object. Used for:

- Client-side type resolution
- Cache normalization
- Union/interface handling

```graphql
query {
  search(query: "test") {
    ... on User { __typename, name }
    ... on Post { __typename, title }
  }
}

```

---

### Senior (10-15)

#### 21. How would you design a schema for a multi-tenant SaaS?

**Answer:**

```graphql
type Query {
  # Tenant-scoped queries
  me: User!
  team(id: ID!): Team
  projects(first: Int, after: String): ProjectConnection!
}

type User {
  id: ID!
  tenant: Tenant!
  role: Role!
  # Field-level authorization
  email: String  # Only visible to self/admins
}

# Middleware for tenant isolation
const createContext = ({ req }) => {
  const tenantId = extractTenant(req);
  return {
    tenantId,
    dataSources: createTenantDataSources(tenantId),
  };
};

```

---

#### 22. Explain your approach to schema governance.

**Answer:**

```text

1. Schema Review Process

   - PR-based schema changes
   - Breaking change detection (GraphQL Inspector)
   - Compatibility testing

2. Deprecation Policy

   - @deprecated directive
   - 6-month minimum deprecation period
   - Client migration tracking

3. Schema Registry

   - Version control
   - Schema stitching coordination
   - Breaking change alerts

```

---

#### 23. How do you handle real-time collaboration with GraphQL?

**Answer:**

```graphql
# Optimistic updates
mutation UpdateDocument($id: ID!, $content: String!) {
  updateDocument(id: $id, content: $content) {
    document {
      id
      content
      version  # For conflict detection
    }
  }
}

# Subscription for live updates
subscription OnDocumentUpdate($id: ID!) {
  documentUpdated(id: $id) {
    id
    content
    version
    updatedBy
  }
}

```

Conflict resolution using OT or CRDTs in resolvers.

---

#### 24. How would you migrate a REST API to GraphQL?

**Answer:**

```text
Phase 1: Gateway

- GraphQL gateway over existing REST
- No changes to backend services
- Start with high-value endpoints

Phase 2: Incremental

- Add GraphQL resolvers for new features
- Maintain REST compatibility
- Client-side migration

Phase 3: Complete

- Decommission REST endpoints
- Unified GraphQL API
- Performance optimization

```

---

#### 25. Design a schema for a social media feed.

**Answer:**

```graphql
type FeedItem {
  id: ID!
  type: FeedItemType!
  post: Post
  story: Story
  ad: Ad
  metrics: FeedMetrics!
}

union FeedContent = Post | Story | Ad

type FeedMetrics {
  likes: Int!
  comments: Int!
  shares: Int!
}

# Cursor-based pagination
type FeedConnection {
  edges: [FeedEdge!]!
  pageInfo: PageInfo!
}

# Subscriptions for real-time updates
subscription NewFeedItem {
  feedItemAdded {
    ... on FeedItem { id type }
  }
}

```

---

#### 26. How do you optimize GraphQL for mobile clients?

**Answer:**

```graphql
# Persisted queries
query GetUserProfile($id: ID!) @persisted {
  user(id: $id) {
    name
    avatar(size: THUMBNAIL)  # Size-specific fields
  }
}

# Query whitelisting
const ALLOWED_QUERIES = new Map([
  ['hash123', GetUserQuery],
]);

```

Strategies:

- Persisted queries for smaller payloads
- Field-level caching
- Query complexity limits
- Mobile-specific schemas

---

#### 27. How do you implement GraphQL in microservices?

**Answer:**

```typescript
// Apollo Federation
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://users-service/graphql' },
      { name: 'posts', url: 'http://posts-service/graphql' },
    ],
  }),
});

// Schema Stitching
const gatewaySchema = stitchSchemas({
  subschemas: [usersSchema, postsSchema],
  typeDefs: `
    extend type User { posts: [Post!]! }
    extend type Post { author: User! }
  `,
});

```

---

#### 28. How do you handle GraphQL in serverless environments?

**Answer:**

```typescript
// Lambda handler
import { ApolloServer } from '@apollo/server';
import { startServerAndCreateLambdaHandler } from '@as-integrations/aws-lambda';

const server = new ApolloServer({ typeDefs, resolvers });

export const handler = startServerAndCreateLambdaHandler(
  server,
  {
    context: async ({ event }) => ({
      // Extract from event
      userId: event.requestContext?.authorizer?.userId,
    }),
  }
);

```

Considerations:

- Cold start optimization
- Stateless context
- Connection pooling
- Query complexity limits

---

#### 29. Design a monitoring system for GraphQL.

**Answer:**

```typescript
// Metrics to track
const metrics = {
  // Performance
  'graphql.query.duration': Histogram,
  'graphql.resolver.duration': Histogram,
  'graphql.complexity.score': Gauge,

  // Errors
  'graphql.errors.count': Counter,
  'graphql.errors.type': Counter,

  // Usage
  'graphql.queries.count': Counter,
  'graphql.mutations.count': Counter,
  'graphql.subscriptions.active': Gauge,

  // Cache
  'graphql.cache.hit': Counter,
  'graphql.cache.miss': Counter,
};

```

---

#### 30. How do you secure a GraphQL API?

**Answer:**

```text

1. Authentication

   - JWT/OAuth verification in context
   - Session management

2. Authorization

   - Field-level permissions
   - Directive-based (@auth)
   - Role-based access control

3. Query Security

   - Depth limiting
   - Complexity analysis
   - Persisted queries
   - Introspection disabled

4. Input Security

   - Schema validation
   - Input sanitization
   - Rate limiting

5. Infrastructure

   - CORS configuration
   - HTTPS enforcement
   - WAF rules

```

---

### FAANG-style (5-10)

#### 31. Design a GraphQL API for a ride-sharing service (like Uber).

**Answer:**

```graphql
type Query {
  ride(id: ID!): Ride
  availableDrivers(location: LocationInput!): [Driver!]!
  rideHistory(first: Int, after: String): RideConnection!
}

type Mutation {
  requestRide(input: RequestRideInput!): Ride!
  acceptRide(rideId: ID!): Ride!
  completeRide(rideId: ID!, rating: Int): Ride!
  cancelRide(rideId: ID!, reason: String): Ride!
}

type Subscription {
  driverLocationUpdated(driverId: ID!): Location!
  rideStatusChanged(rideId: ID!): RideStatus!
  newRideRequest: RideRequest!
}

type Ride {
  id: ID!
  rider: User!
  driver: Driver
  status: RideStatus!
  pickup: Location!
  dropoff: Location!
  fare: FareEstimate!
  estimatedArrival: DateTime
  actualArrival: DateTime
  route: [Location!]!
}

```

Considerations:

- Real-time location tracking (subscriptions)
- Geospatial queries
- Fare calculation
- Rating system
- Driver matching algorithm

---

#### 32. How would you handle GraphQL at scale (10M+ requests/day)?

**Answer:**

```text
Architecture:
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    CDN (Cloudflare)                          │
│                    - Persisted queries                       │
│                    - Query caching                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  GraphQL Gateway                             │
│                  - Query complexity analysis                 │
│                  - Rate limiting                             │
│                  - Authentication                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              GraphQL Services (Horizontal)                   │
│              - Apollo Server instances                       │
│              - DataLoader for N+1 prevention                │
│              - Response caching                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Data Layer                                │
│                    - Redis cache                             │
│                    - Database replicas                       │
│                    - Read/write splitting                    │
└─────────────────────────────────────────────────────────────┘

```

---

#### 33. Design a real-time collaborative document editor with GraphQL.

**Answer:**

```graphql
type Document {
  id: ID!
  title: String!
  content: String!
  version: Int!
  collaborators: [Collaborator!]!
  lastEditedBy: User
  lastEditedAt: DateTime
}

type Collaborator {
  user: User!
  role: CollaboratorRole!
  cursor: CursorPosition
  lastActive: DateTime
}

type CursorPosition {
  line: Int!
  column: Int!
}

# Operations
mutation UpdateDocument($id: ID!, $input: UpdateDocumentInput!) {
  updateDocument(id: $id, input: $input) {
    document {
      id
      version
      content
    }
    conflicts {
      expectedVersion
      actualVersion
    }
  }
}

# Subscriptions
subscription OnDocumentUpdate($id: ID!) {
  documentUpdated(id: $id) {
    id
    content
    version
    updatedBy
    cursorPositions {
      userId
      position
    }
  }
}

```

Conflict resolution:

- Optimistic locking with version numbers
- Operational Transformation (OT) or CRDTs
- Last-write-wins for simple conflicts

---

#### 34. How would you implement a GraphQL API for a financial system?

**Answer:**

```graphql
# Strict typing for financial data
scalar Money

type Money {
  amount: Int!  # In cents
  currency: String!
}

type Account {
  id: ID!
  balance: Money!
  transactions(first: Int, after: String): TransactionConnection!
  # Never expose sensitive fields in certain contexts
  accountNumber: String  # Only to account holder
}

# Input validation
input TransferInput {
  fromAccountId: ID!
  toAccountId: ID!
  amount: MoneyInput!
  description: String
}

# Authorization
type Mutation {
  transfer(input: TransferInput!): TransferResult!
    @auth(requires: AUTHENTICATED)
}

# Audit logging
const resolvers = {
  Mutation: {
    transfer: async (_, { input }, context) => {
      await auditLog.log('transfer', {
        userId: context.currentUser.id,
        input,
      });
      // Execute transfer with idempotency
    },
  },
};

```

Considerations:

- Idempotent mutations
- Audit logging
- Compliance (PCI DSS)
- Fraud detection
- Transaction atomicity

---

#### 35. Design a GraphQL API for a content management system.

**Answer:**

```graphql
# Polymorphic content types
union ContentBlock =

  | Paragraph
  | Heading
  | Image
  | Video
  | CodeBlock
  | Quote

type Paragraph {
  id: ID!
  text: String!
  formatting: [TextFormat!]
}

type Heading {
  id: ID!
  level: Int!
  text: String!
}

# Page with flexible content
type Page implements Node {
  id: ID!
  title: String!
  slug: String!
  content: [ContentBlock!]!
  author: User!
  status: PageStatus!
  seo: SEOFields
  publishedAt: DateTime
}

# Workflow
enum PageStatus {
  DRAFT
  IN_REVIEW
  APPROVED
  PUBLISHED
  ARCHIVED
}

# Mutation with workflow
mutation PublishPage($id: ID!) {
  publishPage(id: $id) {
    page {
      id
      status
      publishedAt
    }
    errors {
      message
      code
    }
  }
}

```

---

#### 36. How do you handle GraphQL in a micro-frontends architecture?

**Answer:**

```typescript
// Shared Apollo Client
const client = new ApolloClient({
  cache: new InMemoryCache({
    typePolicies: {
      // Namespace types to avoid conflicts
      User: { keyFields: ['id', '__typename'] },
    },
  }),
});

// Each micro-frontend
function MicroFrontend1() {
  return (
    <ApolloProvider client={client}>
      <ComponentA />
    </ApolloProvider>
  );
}

// Query isolation
const GET_USER = gql`
  query GetUser_MFE1($id: ID!) {
    user(id: $id) {
      # Only request fields needed by this MFE
      id
      name
      preferences
    }
  }
`;

```

Considerations:

- Shared Apollo Client instance
- Cache isolation per MFE
- Cross-frontend cache updates
- Query deduplication

---

#### 37. Design a GraphQL API for a multiplayer game.

**Answer:**

```graphql
type Game {
  id: ID!
  state: GameState!
  players: [Player!]!
  board: [[Cell!]!]!
  currentTurn: Player
  winner: Player
  createdAt: DateTime!
}

type Player {
  id: ID!
  user: User!
  symbol: PlayerSymbol!
  score: Int!
}

enum PlayerSymbol { X O }
enum GameState { WAITING IN_PROGRESS FINISHED }

# Mutations (idempotent)
mutation JoinGame($gameId: ID!) {
  joinGame(gameId: $gameId) {
    game {
      id
      state
      players
    }
    error {
      message
      code
    }
  }
}

mutation MakeMove($gameId: ID!, $position: MoveInput!) {
  makeMove(gameId: $gameId, position: $position) {
    game {
      id
      board
      state
      winner
    }
    error {
      message
      code
    }
  }
}

# Subscriptions
subscription GameUpdates($gameId: ID!) {
  gameUpdated(gameId: $gameId) {
    id
    board
    state
    currentTurn
    winner
  }
}

```

Considerations:

- Optimistic UI updates
- Conflict resolution
- Low-latency transport (WebSockets)
- Rate limiting for fair play

---

#### 38. How would you implement GraphQL search with relevance scoring?

**Answer:**

```graphql
type Query {
  search(
    query: String!
    type: SearchType
    first: Int
    after: String
    filters: SearchFilters
  ): SearchResultConnection!
}

union SearchResult = User | Post | Product | Page

type SearchResultConnection {
  edges: [SearchResultEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
  aggregations: SearchAggregations
}

type SearchResultEdge {
  node: SearchResult!
  score: Float!  # Relevance score
  highlights: [Highlight!]
}

type Highlight {
  field: String!
  snippet: String!
}

# Resolvers with Elasticsearch
const resolvers = {
  Query: {
    search: async (_, args, context) => {
      const results = await elasticsearch.search({
        index: 'content',
        body: {
          query: {
            multi_match: {
              query: args.query,
              fields: ['title^3', 'content', 'author.name'],
              fuzziness: 'AUTO',
            },
          },
          highlight: {
            fields: { title: {}, content: {} },
          },
        },
      });

      return {
        edges: results.hits.hits.map(hit => ({
          node: hit._source,
          score: hit._score,
          highlights: Object.entries(hit.highlight || {}).map(([field, snippets]) => ({
            field,
            snippet: snippets[0],
          })),
        })),
        totalCount: results.hits.total.value,
      };
    },
  },
};

```

---

#### 39. Design a GraphQL API for IoT device management.

**Answer:**

```graphql
type Device {
  id: ID!
  name: String!
  type: DeviceType!
  status: DeviceStatus!
  telemetry: TelemetryData!
  lastSeen: DateTime!
  firmware: Firmware!
  commands: [Command!]!
}

type TelemetryData {
  timestamp: DateTime!
  temperature: Float
  humidity: Float
  batteryLevel: Int
  signalStrength: Int
}

enum DeviceStatus { ONLINE OFFLINE UPDATING ERROR }

type Query {
  device(id: ID!): Device
  devices(filter: DeviceFilter, first: Int, after: String): DeviceConnection!
  deviceTelemetry(deviceId: ID!, since: DateTime): [TelemetryData!]!
}

type Mutation {
  sendCommand(deviceId: ID!, command: CommandInput!): CommandResult!
  updateFirmware(deviceId: ID!, version: String!): UpdateResult!
  configureDevice(deviceId: ID!, config: DeviceConfigInput!): Device!
}

# High-frequency telemetry subscription
subscription DeviceTelemetry($deviceId: ID!) {
  telemetryUpdate(deviceId: $deviceId) {
    timestamp
    temperature
    humidity
    batteryLevel
  }
}

```

Considerations:

- High-frequency data ingestion
- Time-series database for telemetry
- Command queuing and retry
- Device authentication (certificates)
- Batch operations for bulk devices

---

#### 40. How do you implement GraphQL API versioning?

**Answer:**

```graphql
# Schema evolution (preferred)
type User {
  id: ID!
  name: String!
  email: String!
  # New field - no breaking change
  avatar: String
  # Deprecated field
  username: String @deprecated(reason: "Use name instead")
}

# Field-level deprecation
type User {
  oldField: String @deprecated(reason: "Use newField instead", since: "2.0.0")
  newField: String
}

# Query-level versioning (if needed)
type Query {
  # Version 1
  userV1(id: ID!): UserV1
  # Version 2
  userV2(id: ID!): UserV2
}

```

Best practices:

- Add fields, don't remove
- Deprecate with @deprecated
- Provide migration period
- Track usage of deprecated fields
- Never rename (add new, deprecate old)

---

### Follow-ups (5-10)

#### 41. What happens when a resolver returns null for a non-null field?

**Answer:** GraphQL propagates null to the parent. If the parent is also non-null, it continues up until finding a nullable field or reaching the root.

```graphql
type User {
  id: ID!
  name: String!  # Non-null
}

# If name resolver returns null:
# User becomes null (if User is non-null, error propagates to Query)

```

---

#### 42. How do you test GraphQL resolvers?

**Answer:**

```typescript
// Unit test
describe('UserResolver', () => {
  it('should return user by id', async () => {
    const mockDataSources = {
      userAPI: {
        getUser: jest.fn().mockResolvedValue({ id: '1', name: 'John' }),
      },
    };

    const result = await resolvers.Query.user(
      null,
      { id: '1' },
      { dataSources: mockDataSources }
    );

    expect(result).toEqual({ id: '1', name: 'John' });
  });
});

// Integration test
describe('User Query', () => {
  it('should fetch user', async () => {
    const { query } = createTestClient(server);
    const res = await query({
      query: GET_USER,
      variables: { id: '1' },
    });

    expect(res.data.user.name).toBe('John');
  });
});

```

---

#### 43. What is the difference between `@skip` and `@include`?

**Answer:** Both are query-time directives for conditional field selection.

```graphql
# @skip - Skip field when condition is true
query GetUser($skipEmail: Boolean!) {
  user(id: "1") {
    name
    email @skip(if: $skipEmail)
  }
}

# @include - Include field when condition is true
query GetUser($includeEmail: Boolean!) {
  user(id: "1") {
    name
    email @include(if: $includeEmail)
  }
}

```

---

#### 44. How do you handle batch mutations?

**Answer:**

```graphql
input BatchCreateUsersInput {
  users: [CreateUserInput!]!
}

type BatchCreateUsersPayload {
  users: [User!]!
  errors: [BatchError!]!
}

type BatchError {
  index: Int!
  message: String!
  code: ErrorCode!
}

mutation BatchCreateUsers($input: BatchCreateUsersInput!) {
  batchCreateUsers(input: $input) {
    users { id name }
    errors { index message code }
  }
}

```

---

#### 45. What is the purpose of the `info` argument?

**Answer:** Contains query AST, field name, return type, schema, and path.

```typescript
const resolvers = {
  Query: {
    user: (parent, args, context, info) => {
      // info.fieldName - "user"
      // info.returnType - GraphQLObjectType
      // info.fieldNodes - AST nodes
      // info.path - { prev: ..., key: "user" }
      // info.schema - GraphQL schema

      // Useful for:
      // - Query analysis
      // - Field-level logging
      // - Dynamic resolver behavior
    },
  },
};

```

---

#### 46. How do you handle GraphQL in a monorepo?

**Answer:**

```text
packages/
├── shared/           # Shared types, fragments
│   ├── fragments/
│   └── types/
├── server/           # Apollo Server
│   ├── resolvers/
│   └── schema/
├── client/           # Apollo Client
│   ├── hooks/
│   └── components/
└── codegen/          # GraphQL codegen config
    └── codegen.yml

```

Use:

- Shared fragments
- Codegen for type safety
- Workspace dependencies
- Unified schema packages

---

#### 47. What are the trade-offs of GraphQL over REST?

**Answer:**

**GraphQL Pros:**

- No over/under-fetching
- Single endpoint
- Strong typing
- Introspection
- No versioning

**GraphQL Cons:**

- Complex setup
- Caching harder
- File uploads tricky
- Learning curve
- Query complexity risks

**When to use GraphQL:**

- Complex data requirements
- Multiple client types
- Rapid iteration
- Real-time features

**When REST is better:**

- Simple CRUD
- File-heavy APIs
- HTTP caching critical
- Team unfamiliar with GraphQL

---

#### 48. How do you implement GraphQL in Next.js?

**Answer:**

```typescript
// pages/api/graphql.ts (API Route)
import { ApolloServer } from '@apollo/server';
import { startServerAndCreateNextHandler } from '@as-integrations/next';

const server = new ApolloServer({ typeDefs, resolvers });
const handler = startServerAndCreateNextHandler(server);

export default handler;

// pages/index.tsx (Page)
import { ApolloProvider, useQuery } from '@apollo/client';
import { client } from '../lib/apollo';

export default function Home() {
  return (
    <ApolloProvider client={client}>
      <MyComponent />
    </ApolloProvider>
  );
}

```

---

#### 49. How do you monitor GraphQL in production?

**Answer:**

```typescript
// Apollo Studio
const server = new ApolloServer({
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },
    }),
  ],
});

// Custom metrics
const metricsPlugin = {
  requestDidStart() {
    const start = Date.now();
    return {
      willSendResponse({ operationName }) {
        const duration = Date.now() - start;
        metrics.histogram('graphql.duration', duration, { operationName });
      },
    };
  },
};

```

Key metrics:

- Query complexity
- Response time (P50, P95, P99)
- Error rate
- Cache hit rate
- N+1 query count

---

#### 50. What are the future trends in GraphQL?

**Answer:**

```text

1. Federation 2.0 - Better schema composition

2. Edge Computing - GraphQL at the edge

3. AI Integration - Schema generation, query optimization

4. Defer/Stream - Incremental delivery

5. Client-side GraphQL - Local-first with GraphQL

6. Type-safe APIs - Better codegen tooling

7. Real-time First - Subscriptions as primary concern

8. Security Focus - Standardized security practices

```

---

## Summary

| Level | Focus Areas |
|-------|-------------|
| **Beginner** | Schema, types, queries, mutations, arguments |
| **Intermediate** | N+1, DataLoader, pagination, error handling |
| **Senior** | Architecture, security, performance, governance |
| **FAANG** | System design, scale, real-time, complex domains |
| **Follow-ups** | Testing, Next.js, monitoring, trade-offs |

---

## References & Learn More

- [GraphQL Official Spec](https://spec.graphql.org/)
- [How to GraphQL](https://www.howtographql.com/)
- [Apollo Best Practices](https://www.apollographql.com/blog/graphql/best-practices/)
- [GraphQL Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [Real World GraphQL](https://github.com/APIs-guru/graphql-apis)
