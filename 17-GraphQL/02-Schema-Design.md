# Schema Design

## Definition

GraphQL Schema Design is the process of defining the **type system**, **operations**, and **relationships** that form your API contract. A well-designed schema serves as documentation, enables tooling, and ensures type safety across your entire stack.

```
Schema = Type Definitions + Type Relationships + Operations + Directives
```

The schema is written in the **Schema Definition Language (SDL)**, a declarative syntax that describes what operations are possible and what data can be returned.

---

## Why Do We Need It?

### The Schema-First Advantage

```
Without Schema-First:
┌──────────────────────────────────────────────────────┐
│  1. Implementation varies across teams               │
│  2. No single source of truth                        │
│  3. Frontend/Backend misalignment                     │
│  4. Difficult to generate types automatically         │
│  5. No contract validation                            │
└──────────────────────────────────────────────────────┘

With Schema-First:
┌──────────────────────────────────────────────────────┐
│  1. Schema IS the contract                           │
│  2. Auto-generated TypeScript types                  │
│  3. Mock server for frontend development             │
│  4. Breaking change detection                        │
│  5. Self-documenting API                             │
└──────────────────────────────────────────────────────┘
```

### Schema Design Principles

| Principle | Description |
|-----------|-------------|
| **Discoverability** | Easy to explore and understand |
| **Consistency** | Uniform naming and patterns |
| **Evolvability** | Can grow without breaking changes |
| **Performance** | Designed to avoid expensive queries |
| **Security** | No unintentional data exposure |

---

## How It Works

### Core Type System

```
┌──────────────────────────────────────────────────────────────────┐
│                     GRAPHQL TYPE SYSTEM                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │   Scalars   │   │   Objects   │   │   Enums     │          │
│  │             │   │             │   │             │          │
│  │  String     │   │  User       │   │  STATUS     │          │
│  │  Int        │   │  Post       │   │  ACTIVE     │          │
│  │  Float      │   │  Comment    │   │  INACTIVE   │          │
│  │  Boolean    │   │             │   │             │          │
│  │  ID         │   │             │   │             │          │
│  └─────────────┘   └─────────────┘   └─────────────┘          │
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │  Input      │   │ Interface   │   │   Union     │          │
│  │  Types      │   │   Types     │   │   Types     │          │
│  │             │   │             │   │             │          │
│  │ CreateUser  │   │  Node       │   │ SearchResult│          │
│  │ UpdatePost  │   │  Timestamped│   │ User|Post   │          │
│  │             │   │             │   │             │          │
│  └─────────────┘   └─────────────┘   └─────────────┘          │
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐                             │
│  │  Lists      │   │  Non-Null   │                             │
│  │  [User!]!   │   │  String!    │                             │
│  │  [Post]     │   │  ID!        │                             │
│  └─────────────┘   └─────────────┘                             │
└──────────────────────────────────────────────────────────────────┘
```

### Type Relationships Diagram

```
                    ┌─────────────────┐
                    │     Node        │  (Interface)
                    │─────────────────│
                    │ id: ID!         │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │   User   │   │   Post   │   │ Comment  │
        │──────────│   │──────────│   │──────────│
        │ name     │   │ title    │   │ body     │
        │ email    │   │ content  │   │ author   │
        │ posts    │   │ author   │   │ post     │
        └──────────┘   └──────────┘   └──────────┘
              │              │              │
              │    1:N       │    1:N       │
              └──────────────┴──────────────┘
```

---

## Code Examples

### Complete Schema Definition

```graphql
# ============================================
# CUSTOM SCALARS
# ============================================
scalar DateTime
scalar JSON
scalar URL
scalar Email

# ============================================
# ENUMS
# ============================================
enum Role {
  ADMIN
  MODERATOR
  USER
  GUEST
}

enum PostStatus {
  DRAFT
  PENDING_REVIEW
  PUBLISHED
  ARCHIVED
}

enum SortOrder {
  ASC
  DESC
}

enum PostSortField {
  CREATED_AT
  UPDATED_AT
  TITLE
  VIEWS
}

# ============================================
# INTERFACES
# ============================================
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

interface Searchable {
  searchableText: String!
}

# ============================================
# OBJECT TYPES
# ============================================
type User implements Node & Timestamped {
  id: ID!
  name: String!
  email: Email!
  role: Role!
  avatar: URL
  bio: String
  posts(
    first: Int
    after: String
    status: PostStatus
  ): PostConnection!
  followers(
    first: Int
    after: String
  ): UserConnection!
  following(
    first: Int
    after: String
  ): UserConnection!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post implements Node & Timestamped {
  id: ID!
  title: String!
  slug: String!
  content: String!
  excerpt: String
  status: PostStatus!
  author: User!
  tags: [Tag!]!
  comments(
    first: Int
    after: String
  ): CommentConnection!
  views: Int!
  likes: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Comment implements Node & Timestamped {
  id: ID!
  body: String!
  author: User!
  post: Post!
  parent: Comment
  replies(
    first: Int
    after: String
  ): CommentConnection!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Tag implements Node {
  id: ID!
  name: String!
  posts(
    first: Int
    after: String
  ): PostConnection!
}

# ============================================
# CONNECTION TYPES (Relay-style Pagination)
# ============================================
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserEdge {
  node: User!
  cursor: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type CommentEdge {
  node: Comment!
  cursor: String!
}

type CommentConnection {
  edges: [CommentEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

# ============================================
# UNION TYPES
# ============================================
union SearchResult = User | Post | Tag

# ============================================
# INPUT TYPES
# ============================================
input CreateUserInput {
  name: String!
  email: Email!
  password: String!
  role: Role = USER
  bio: String
}

input UpdateUserInput {
  name: String
  email: Email
  bio: String
  avatar: URL
}

input CreatePostInput {
  title: String!
  content: String!
  excerpt: String
  status: PostStatus = DRAFT
  tagIds: [ID!]
}

input UpdatePostInput {
  title: String
  content: String
  excerpt: String
  status: PostStatus
  tagIds: [ID!]
}

input PostFilterInput {
  status: PostStatus
  authorId: ID
  tagId: ID
  search: String
  createdAfter: DateTime
  createdBefore: DateTime
}

input PaginationInput {
  first: Int
  after: String
  last: Int
  before: String
}

input SortInput {
  field: PostSortField!
  order: SortOrder = DESC
}

# ============================================
# SCHEMA DIRECTIVES
# ============================================
directive @auth(
  requires: Role = USER
) on FIELD_DEFINITION | OBJECT

directive @deprecated(
  reason: String = "No longer supported"
) on FIELD_DEFINITION | ENUM_VALUE

directive @cacheControl(
  maxAge: Int!
  scope: CacheScope = PUBLIC
) on FIELD_DEFINITION | OBJECT | SCHEMA

enum CacheScope {
  PUBLIC
  PRIVATE
}

# ============================================
# ROOT TYPES
# ============================================
type Query {
  # User queries
  me: User @auth(requires: USER)
  user(id: ID!): User
  users(
    first: Int
    after: String
    role: Role
  ): UserConnection!

  # Post queries
  post(id: ID!): Post
  postBySlug(slug: String!): Post
  posts(
    first: Int
    after: String
    filter: PostFilterInput
    sort: SortInput
  ): PostConnection!

  # Search
  search(
    query: String!
    first: Int
    after: String
  ): [SearchResult!]!

  # Tags
  tags(first: Int, after: String): [Tag!]!
  tag(id: ID!): Tag
}

type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  # Post mutations
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
  publishPost(id: ID!): PublishPostPayload!

  # Comment mutations
  createComment(
    postId: ID!
    body: String!
    parentId: ID
  ): CreateCommentPayload!

  # Social mutations
  followUser(userId: ID!): FollowUserPayload!
  unfollowUser(userId: ID!): UnfollowUserPayload!
  likePost(postId: ID!): LikePostPayload!
  unlikePost(postId: ID!): UnlikePostPayload!
}

type Subscription {
  postPublished(authorId: ID): Post!
  commentAdded(postId: ID!): Comment!
  userJoined: User!
}

# ============================================
# PAYLOAD TYPES
# ============================================
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UpdateUserPayload {
  user: User
  errors: [UserError!]
}

type DeleteUserPayload {
  deletedUserId: ID
  errors: [UserError!]
}

type CreatePostPayload {
  post: Post
  errors: [PostError!]
}

type UpdatePostPayload {
  post: Post
  errors: [PostError!]
}

type DeletePostPayload {
  deletedPostId: ID
  errors: [PostError!]
}

type PublishPostPayload {
  post: Post
  errors: [PostError!]
}

type CreateCommentPayload {
  comment: Comment
  errors: [CommentError!]
}

type FollowUserPayload {
  user: User
  errors: [UserError!]
}

type UnfollowUserPayload {
  user: User
  errors: [UserError!]
}

type LikePostPayload {
  post: Post
  errors: [PostError!]
}

type UnlikePostPayload {
  post: Post
  errors: [PostError!]
}

# ============================================
# ERROR TYPES
# ============================================
type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

type PostError {
  field: String
  message: String!
  code: ErrorCode!
}

type CommentError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  NOT_FOUND
  UNAUTHORIZED
  FORBIDDEN
  VALIDATION_ERROR
  CONFLICT
  INTERNAL_ERROR
}
```

### TypeScript Type Generation (typegen)

```typescript
// Generated types from schema (using graphql-codegen)
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: Date;
  JSON: Record<string, unknown>;
  URL: string;
  Email: string;
};

export enum Role {
  Admin = 'ADMIN',
  Moderator = 'MODERATOR',
  User = 'USER',
  Guest = 'GUEST',
}

export enum PostStatus {
  Draft = 'DRAFT',
  PendingReview = 'PENDING_REVIEW',
  Published = 'PUBLISHED',
  Archived = 'ARCHIVED',
}

export interface User {
  __typename: 'User';
  id: Scalars['ID'];
  name: Scalars['String'];
  email: Scalars['Email'];
  role: Role;
  avatar?: Maybe<Scalars['URL']>;
  bio?: Maybe<Scalars['String']>;
  posts: PostConnection;
  followers: UserConnection;
  following: UserConnection;
  createdAt: Scalars['DateTime'];
  updatedAt: Scalars['DateTime'];
}

export interface Post {
  __typename: 'Post';
  id: Scalars['ID'];
  title: Scalars['String'];
  slug: Scalars['String'];
  content: Scalars['String'];
  excerpt?: Maybe<Scalars['String']>;
  status: PostStatus;
  author: User;
  tags: Array<Tag>;
  comments: CommentConnection;
  views: Scalars['Int'];
  likes: Scalars['Int'];
  createdAt: Scalars['DateTime'];
  updatedAt: Scalars['DateTime'];
}

// ... more generated types
```

### Resolver Implementation with Type Safety

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

    posts: async (_, { first, after, filter, sort }, context) => {
      return context.dataSources.postAPI.getPosts({
        first: first ?? 10,
        after,
        filter,
        sort
      });
    },

    search: async (_, { query, first, after }, context) => {
      return context.dataSources.searchAPI.search(query, first, after);
    },
  },

  User: {
    posts: async (parent, { first, after, status }, context) => {
      return context.dataSources.postAPI.getPostsByAuthor(parent.id, {
        first,
        after,
        status
      });
    },

    followers: async (parent, { first, after }, context) => {
      return context.dataSources.socialAPI.getFollowers(parent.id, {
        first,
        after
      });
    },
  },

  Post: {
    author: async (parent, _, context) => {
      return context.dataSources.userAPI.getUser(parent.authorId);
    },

    tags: async (parent, _, context) => {
      return context.dataSources.tagAPI.getTagsByPost(parent.id);
    },

    comments: async (parent, { first, after }, context) => {
      return context.dataSources.commentAPI.getCommentsByPost(parent.id, {
        first,
        after
      });
    },
  },

  Mutation: {
    createUser: async (_, { input }, context) => {
      try {
        const user = await context.dataSources.userAPI.createUser(input);
        return { user, errors: [] };
      } catch (error) {
        return {
          user: null,
          errors: [{
            field: 'email',
            message: error.message,
            code: 'CONFLICT'
          }]
        };
      }
    },

    createPost: async (_, { input }, context) => {
      const user = context.getCurrentUser();
      if (!user) {
        return {
          post: null,
          errors: [{
            field: 'authentication',
            message: 'Must be logged in to create posts',
            code: 'UNAUTHORIZED'
          }]
        };
      }

      const post = await context.dataSources.postAPI.createPost({
        ...input,
        authorId: user.id
      });

      return { post, errors: [] };
    },
  },
};
```

### Schema Stitching Example

```typescript
import { stitchSchemas } from '@graphql-tools/stitch';

// Remote schemas
const usersSchema = makeRemoteDataSource({
  url: 'http://users-service/graphql',
});

const postsSchema = makeRemoteDataSource({
  url: 'http://posts-service/graphql',
});

const commentsSchema = makeRemoteDataSource({
  url: 'http://comments-service/graphql',
});

// Stitched schema
const gatewaySchema = stitchSchemas({
  subschemas: [
    {
      schema: usersSchema,
      merge: {
        User: {
          fieldName: 'user',
          selectionSet: '{ id }',
          args: (originalObject) => ({ id: originalObject.id }),
        },
      },
    },
    {
      schema: postsSchema,
      merge: {
        Post: {
          fieldName: 'post',
          selectionSet: '{ id }',
          args: (originalObject) => ({ id: originalObject.id }),
        },
      },
    },
    {
      schema: commentsSchema,
    },
  ],
  typeDefs: `
    extend type User {
      posts: [Post!]!
    }
    extend type Post {
      author: User!
      comments: [Comment!]!
    }
    extend type Comment {
      author: User!
      post: Post!
    }
  `,
  resolvers: {
    User: {
      posts: {
        selectionSet: '{ id }',
        resolve(user, args, context, info) {
          return delegateToSchema({
            schema: postsSchema,
            operation: 'query',
            fieldName: 'postsByAuthor',
            args: { authorId: user.id },
            context,
            info,
          });
        },
      },
    },
    Post: {
      author: {
        selectionSet: '{ authorId }',
        resolve(post, args, context, info) {
          return delegateToSchema({
            schema: usersSchema,
            operation: 'query',
            fieldName: 'user',
            args: { id: post.authorId },
            context,
            info,
          });
        },
      },
    },
  },
});
```

---

## Real-World Use Cases

### 1. E-Commerce Schema

```graphql
type Product implements Node {
  id: ID!
  name: String!
  slug: String!
  description: String!
  price: Money!
  compareAtPrice: Money
  sku: String!
  inventory: Inventory!
  images: [ProductImage!]!
  variants: [ProductVariant!]!
  collections: [Collection!]!
  reviews: ReviewConnection!
  rating: Float
  reviewCount: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Money {
  amount: Int!  # In cents
  currency: String!
}

type Inventory {
  quantity: Int!
  trackInventory: Boolean!
  allowBackorder: Boolean!
}

type ProductVariant implements Node {
  id: ID!
  product: Product!
  name: String!
  sku: String!
  price: Money!
  inventory: Inventory!
  options: [VariantOption!]!
}

input ProductFilterInput {
  collectionId: ID
  minPrice: Int
  maxPrice: Int
  inStock: Boolean
  search: String
  tags: [String!]
  rating: Float
}
```

### 2. CMS Content Model

```graphql
union ContentBlock =
  | Paragraph
  | Heading
  | Image
  | Video
  | CodeBlock
  | Quote
  | List
  | Table

type Paragraph {
  text: String!
  formatting: [TextFormat!]
}

type Heading {
  level: Int!
  text: String!
}

type Image {
  url: URL!
  alt: String!
  caption: String
  width: Int
  height: Int
}

interface Block {
  id: ID!
}

type Page implements Node {
  id: ID!
  title: String!
  slug: String!
  content: [ContentBlock!]!
  author: User!
  publishedAt: DateTime
  seo: SEOFields
  template: PageTemplate
}

type SEOFields {
  title: String
  description: String
  ogImage: URL
  keywords: [String!]
}
```

### 3. Analytics Dashboard Schema

```graphql
type Dashboard implements Node {
  id: ID!
  name: String!
  widgets: [Widget!]!
  owner: User!
  sharedWith: [User!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

union Widget =
  | ChartWidget
  | MetricWidget
  | TableWidget
  | FilterWidget

type ChartWidget {
  id: ID!
  title: String!
  chartType: ChartType!
  dataSource: DataSource!
  data: ChartData!
}

enum ChartType {
  LINE
  BAR
  PIE
  AREA
  SCATTER
}

type MetricWidget {
  id: ID!
  title: String!
  value: Float!
  change: Float
  changePercent: Float
  sparkline: [DataPoint!]
}

type DataPoint {
  timestamp: DateTime!
  value: Float!
}
```

---

## Common Mistakes

### 1. Overloading Query Roots

```graphql
# BAD: Too many similar queries
type Query {
  user(id: ID!): User
  userById(id: ID!): User
  getUser(id: ID!): User
  fetchUser(id: ID!): User
  findUser(id: ID!): User
}

# GOOD: Single, clear query
type Query {
  user(id: ID!): User
}
```

### 2. Inconsistent Naming

```graphql
# BAD: Mixed naming conventions
type Query {
  get_user(id: ID!): User
  fetchPosts: [Post]
  commentsForPost(postId: ID!): [Comment]
  retrieve_tags: [Tag]
}

# GOOD: Consistent camelCase
type Query {
  user(id: ID!): User
  posts(first: Int, after: String): PostConnection!
  comments(postId: ID!, first: Int, after: String): CommentConnection!
  tags: [Tag!]!
}
```

### 3. Missing Pagination

```graphql
# BAD: No pagination
type Query {
  users: [User!]!  # Returns ALL users
  posts: [Post!]!  # Returns ALL posts
}

# GOOD: Always paginate
type Query {
  users(first: Int, after: String): UserConnection!
  posts(first: Int, after: String): PostConnection!
}
```

### 4. Exposing Internal IDs

```graphql
# BAD: Using database IDs
type User {
  id: ID!  # Could be auto-incremented database ID
  mongoId: String!  # Internal MongoDB ID
  uuid: String!  # Internal UUID
}

# GOOD: Use opaque IDs
type User {
  id: ID!  # Opaque, versioned ID (e.g., base64 encoded)
}
```

### 5. No Input Validation

```graphql
# BAD: No constraints
input CreateUserInput {
  name: String
  email: String
  age: Int
}

# GOOD: Use non-null and validation
input CreateUserInput {
  name: String!
  email: Email!  # Custom scalar with validation
  age: Int  # Validated in resolver
}
```

### 6. Circular References

```graphql
# BAD: Infinite recursion possible
type User {
  posts: [Post!]!
}

type Post {
  author: User!
  comments: [Comment!]!
}

type Comment {
  author: User!
  post: Post!
}

# GOOD: Limit depth in resolvers or use DataLoader
```

---

## Best Practices

### Naming Conventions

```
Types:       PascalCase  → User, PostConnection, CreatePostInput
Fields:      camelCase   → firstName, createdAt, totalCount
Enums:       SCREAMING   → POST_STATUS, USER_ROLE
Arguments:   camelCase   → first, after, search
Input types: PascalCase + Input suffix → CreateUserInput
```

### Schema Evolution

```
DO:
  ✓ Add new fields
  ✓ Add new types
  ✓ Add new arguments (with defaults)
  ✓ Deprecate with @deprecated
  ✓ Use feature flags

DON'T:
  ✗ Remove fields
  ✗ Rename fields
  ✗ Change field types
  ✗ Remove enum values
  ✗ Change argument types
```

### Pagination Pattern (Relay Connection)

```
Connection Pattern:
┌─────────────────────────────────────────────────────┐
│                    Connection                        │
│  ┌──────────┐                                       │
│  │  edges   │──→ [Edge] ──→ { node, cursor }       │
│  └──────────┘                                       │
│  ┌──────────┐                                       │
│  │ pageInfo │──→ { hasNext, hasPrev, start, end }   │
│  └──────────┘                                       │
│  ┌──────────┐                                       │
│  │ totalCount│                                      │
│  └──────────┘                                       │
└─────────────────────────────────────────────────────┘
```

### Error Handling Pattern

```graphql
# Use payload types for mutations
type CreateUserPayload {
  user: User  # Successful result
  errors: [UserError!]!  # Always include errors array
}

type UserError {
  field: String  # Which field caused the error
  message: String!  # Human-readable message
  code: ErrorCode!  # Machine-readable code
}
```

---

## Performance Considerations

### Query Complexity Scoring

```typescript
import { getComplexity, simpleEstimator, fieldExtensionsEstimator } from 'graphql-query-complexity';

// Assign complexity scores to fields
const typeDefs = `
  extend type Query {
    users(first: Int): [User!]! @complexity(value: 1)
    posts(first: Int): [Post!]! @complexity(value: 1)
  }

  type User {
    id: ID!
    name: String!
    posts(first: Int): [Post!]! @complexity(value: 2, multipliers: ["first"])
  }
`;

// Complexity calculation
const complexity = getComplexity({
  schema,
  operationName: 'GetUsers',
  query: parse(query),
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

### Schema-Level Caching

```graphql
type Query {
  # Cache for 5 minutes
  popularPosts: [Post!]! @cacheControl(maxAge: 300, scope: PUBLIC)

  # Cache for 1 hour
  staticData: StaticData! @cacheControl(maxAge: 3600, scope: PUBLIC)

  # No caching
  currentUser: User @cacheControl(maxAge: 0, scope: PRIVATE)
}

type Post {
  id: ID!
  title: String!
  content: String! @cacheControl(maxAge: 3600)
  author: User! @cacheControl(maxAge: 300)
  comments: [Comment!]! @cacheControl(maxAge: 60)
}
```

---

## Interview Questions

### Beginner

1. **What is a GraphQL schema?**
   A schema defines the types, relationships, and operations available in a GraphQL API. It's the contract between client and server.

2. **What is the difference between a scalar and an object type?**
   Scalars are leaf types (String, Int, Boolean, etc.) that hold values. Object types are composite types with fields that can be other types.

3. **What does `!` mean in GraphQL?**
   The `!` indicates non-null. `String!` means the field will never return null.

4. **What is an Input type?**
   A special object type used exclusively for mutation arguments, enabling structured and validated input.

5. **What are Enums used for?**
   Enums represent a fixed set of values (like statuses or types), providing type safety and documentation.

### Intermediate

6. **What is schema stitching?**
   Combining multiple GraphQL schemas into a single unified schema, allowing clients to query across multiple services.

7. **What is the Relay Connection specification?**
   A pagination pattern using edges, nodes, cursors, and pageInfo to provide consistent, cursor-based pagination.

8. **How do you handle file uploads in GraphQL?**
   Use multipart form data specification or separate REST endpoints. GraphQL spec doesn't natively support file uploads.

9. **What are custom scalars?**
   User-defined scalar types (like DateTime, JSON, Email) that extend GraphQL's built-in type system.

10. **How do you version a GraphQL API?**
    Through schema evolution: add new fields/types, deprecate old ones with @deprecated, never remove until no clients use them.

### Senior

11. **How would you design a schema for a multi-tenant SaaS?**
    Use tenant-scoped queries, field-level authorization, tenant context in resolvers, and possibly schema-per-tenant for strict isolation.

12. **Explain the trade-offs between schema-first and code-first approaches.**
    Schema-first: better for API contracts, mocking, documentation. Code-first: better for type safety, refactoring, developer experience.

13. **How do you handle schema governance at scale?**
    Schema review process, breaking change detection tools (GraphQL Inspector), compatibility testing, deprecation policies, and schema registry.

14. **Design a schema that supports real-time collaboration.**
    Use subscriptions for live updates, optimistic UI, conflict resolution (OT or CRDTs), and versioning for concurrent edits.

15. **How do you optimize schema for mobile clients?**
    Query whitelisting, persisted queries, field-level caching, response compression, and mobile-specific query complexity limits.

### FAANG-style

16. **Design a GraphQL schema for a social media platform with 1B users.**
    Consider: sharding strategy, cursor-based pagination, denormalization for read performance, CDN caching, and query complexity limits.

17. **How would you migrate a REST API with 100 endpoints to GraphQL?**
    Strangler fig pattern, GraphQL gateway over REST, incremental adoption, starting with high-value endpoints, maintaining backward compatibility.

18. **Explain how you'd implement a global search API with GraphQL.**
    Union types for polymorphic results, cursor-based pagination, relevance scoring, filtering, and query complexity management for deep searches.

19. **How do you handle schema composition in a microservices architecture?**
    Apollo Federation with @key, @requires, @provides directives. Schema registry for coordination. Breaking change detection across services.

20. **Design a GraphQL API for a real-time multiplayer game.**
    Subscriptions for game state, optimistic updates, conflict resolution, low-latency transport (WebSockets), and rate limiting for fair play.

### Follow-ups

21. **What happens when two fields return the same data?**
    This is generally fine (redundancy for convenience), but consider if one should reference the other or if you need a wrapper type.

22. **How do you handle circular dependencies in resolvers?**
    Use DataLoader, limit query depth, or restructure schema to break cycles.

23. **What is the difference between @skip and @include directives?**
    Both are query-time directives for conditional field selection. @skip(name: "field") omits when true. @include includes when true.

24. **How do you handle batch operations in mutations?**
    Use input arrays and return arrays of results/errors. Consider transactions and partial success handling.

25. **What is the purpose of the __typename meta-field?**
    Returns the actual type name of an object. Used for client-side type resolution, cache normalization, and union/interface handling.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Type System** | Foundation of the API contract |
| **Naming** | Consistent, discoverable, clear |
| **Pagination** | Always use Relay Connection pattern |
| **Evolution** | Add, don't remove; deprecate instead |
| **Errors** | Payload types with error arrays |
| **Performance** | Complexity limits, caching, depth limits |

---

## References & Learn More

- [GraphQL Schema Design](https://graphql.org/learn/schema/)
- [Relay Connection Specification](https://relay.dev/graphql/connections.htm)
- [Apollo Schema Design](https://www.apollographql.com/docs/federation/schema-design/)
- [Prisma Schema Design](https://www.prisma.io/docs/concepts/components/prisma-schema)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [GraphQL Schema Stitching](https://www.graphql-tools.com/docs/schema-stitching/)
- [Apollo Federation](https://www.apollographql.com/docs/federation/)
