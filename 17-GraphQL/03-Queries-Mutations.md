# Queries & Mutations

## Definition

**Queries** and **Mutations** are the two primary read and write operations in GraphQL. Queries retrieve data without side effects, while mutations modify data and return the updated state. Both follow the same syntax rules but differ in execution guarantees.

```
Query   → Read operations (idempotent, side-effect free)
Mutation → Write operations (sequential execution, side effects allowed)
```

---

## Why Do We Need It?

### The Problem with REST Operations

```
REST Approach:
┌─────────────────────────────────────────────────────────────────┐
│  GET    /api/users/1          → Fetch user                      │
│  POST   /api/users            → Create user                     │
│  PUT    /api/users/1          → Update user                     │
│  DELETE /api/users/1          → Delete user                     │
│                                                                  │
│  Problems:                                                       │
│  1. Fixed HTTP methods for all operations                       │
│  2. No standardized error response                              │
│  3. Multiple endpoints to manage                                │
│  4. Client can't specify response shape                         │
└─────────────────────────────────────────────────────────────────┘

GraphQL Approach:
┌─────────────────────────────────────────────────────────────────┐
│  POST /graphql (Query)                                          │
│  { user(id: 1) { name email posts { title } } }                │
│                                                                  │
│  POST /graphql (Mutation)                                       │
│  { createUser(input: { name: "John" }) { id name } }           │
│                                                                  │
│  Benefits:                                                       │
│  1. Single endpoint for all operations                          │
│  2. Standardized error handling                                 │
│  3. Client controls response shape                              │
│  4. Type-safe operations                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Execution Guarantees

| Operation | Execution Order | Side Effects | Idempotent |
|-----------|-----------------|--------------|------------|
| Query | Parallel | Not allowed | Yes |
| Mutation | Sequential | Allowed | No |
| Subscription | Persistent | Allowed | No |

---

## How It Works

### Query Execution Flow

```
Query: { user(id: 1) { name posts { title } } }

1. Parse query into AST
        │
        ▼
2. Validate against schema
        │
        ├── User type exists? ✓
        ├── name field exists? ✓
        ├── posts field exists? ✓
        │
        ▼
3. Execute resolvers (parallel where possible)
        │
        ├── user(id: 1) ─────┐
        │                     │
        ├── User.name ───────┤ (parallel)
        │                     │
        └── User.posts ──────┘
        │
        ▼
4. Assemble response matching query shape
        │
        ▼
5. Return { data: { user: { name: "...", posts: [...] } } }
```

### Mutation Execution Flow

```
Mutation: { createUser(input: { name: "John" }) { id name } }

1. Parse mutation into AST
        │
        ▼
2. Validate against schema
        │
        ├── CreateUserInput type valid? ✓
        ├── CreateUserPayload type valid? ✓
        │
        ▼
3. Execute resolvers (SEQUENTIAL)
        │
        ├── Mutation.createUser(input: { name: "John" })
        │   └── Execute one at a time, wait for completion
        │
        ├── User.id (after mutation completes)
        │
        └── User.name (after mutation completes)
        │
        ▼
4. Return { data: { createUser: { id: "...", name: "John" } } }
```

---

## Code Examples

### Basic Queries

```graphql
# Simple query
query {
  user(id: "1") {
    id
    name
    email
  }
}

# Named query (recommended)
query GetUser {
  user(id: "1") {
    id
    name
    email
  }
}

# Query with variables
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      id
      title
      createdAt
    }
  }
}

# Multiple queries in one request
query {
  currentUser {
    id
    name
  }
  popularPosts(limit: 5) {
    id
    title
    views
  }
}
```

### Query with Arguments and Filtering

```graphql
# Pagination
query GetPosts($first: Int!, $after: String) {
  posts(first: $first, after: $after) {
    edges {
      node {
        id
        title
        excerpt
        author {
          name
          avatar
        }
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}

# Filtering
query SearchPosts($query: String!, $status: PostStatus) {
  posts(filter: { search: $query, status: $status }) {
    edges {
      node {
        id
        title
        content
      }
    }
  }
}

# Sorting
query GetPostsSorted($sort: SortInput!) {
  posts(sort: $sort) {
    edges {
      node {
        id
        title
        createdAt
      }
    }
  }
}
```

### Query with Fragments

```graphql
# Fragment definition
fragment UserFields on User {
  id
  name
  email
  avatar
}

fragment PostFields on Post {
  id
  title
  excerpt
  createdAt
  author {
    ...UserFields
  }
}

# Using fragments
query GetUserWithPosts($id: ID!) {
  user(id: $id) {
    ...UserFields
    posts {
      ...PostFields
    }
  }
}

# Inline fragments for polymorphic types
query Search($query: String!) {
  search(query: $query) {
    ... on User {
      id
      name
      email
    }
    ... on Post {
      id
      title
      content
    }
    ... on Tag {
      id
      name
    }
  }
}
```

### Basic Mutations

```graphql
# Simple mutation
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    createdAt
  }
}

# Mutation with variables
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    content
    updatedAt
  }
}

# Delete mutation
mutation DeletePost($id: ID!) {
  deletePost(id: $id) {
    deletedPostId
  }
}
```

### Mutations with Error Handling

```graphql
# Using payload types
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
    errors {
      field
      message
      code
    }
  }
}

# Response when successful
{
  "data": {
    "createUser": {
      "user": {
        "id": "1",
        "name": "John Doe",
        "email": "john@example.com"
      },
      "errors": []
    }
  }
}

# Response with validation errors
{
  "data": {
    "createUser": {
      "user": null,
      "errors": [
        {
          "field": "email",
          "message": "Email already exists",
          "code": "CONFLICT"
        }
      ]
    }
  }
}
```

### Mutations with Input Validation

```graphql
# Complex input types
input CreatePostInput {
  title: String!
  content: String!
  excerpt: String
  status: PostStatus = DRAFT
  tagIds: [ID!]
  metadata: PostMetadataInput
}

input PostMetadataInput {
  seoTitle: String
  seoDescription: String
  featuredImage: String
  allowComments: Boolean = true
}

# Nested mutations
mutation CreatePostWithTags($input: CreatePostInput!) {
  createPost(input: $input) {
    post {
      id
      title
      tags {
        id
        name
      }
      metadata {
        seoTitle
        featuredImage
      }
    }
    errors {
      field
      message
      code
    }
  }
}
```

### Optimistic Updates

```typescript
import { gql, useMutation } from '@apollo/client';

const UPDATE_POST = gql`
  mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
    updatePost(id: $id, input: $input) {
      id
      title
      content
      updatedAt
    }
  }
`;

function PostEditor({ post }: { post: Post }) {
  const [updatePost] = useMutation(UPDATE_POST, {
    optimisticResponse: {
      __typename: 'Mutation',
      updatePost: {
        __typename: 'UpdatePostPayload',
        id: post.id,
        title: 'Updated Title',  // Optimistic value
        content: 'Updated content',
        updatedAt: new Date().toISOString(),
      },
    },
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({ __typename: 'Post', id: post.id }),
        fields: {
          title() { return data.updatePost.title; },
          content() { return data.updatePost.content; },
          updatedAt() { return data.updatePost.updatedAt; },
        },
      });
    },
  });

  const handleSubmit = async (title: string, content: string) => {
    await updatePost({
      variables: {
        id: post.id,
        input: { title, content }
      }
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input defaultValue={post.title} />
      <textarea defaultValue={post.content} />
      <button type="submit">Save</button>
    </form>
  );
}
```

### Variables and Operation Names

```typescript
// TypeScript client code
import { gql, useQuery } from '@apollo/client';

// Query with operation name
const GET_USER_POSTS = gql`
  query GetUserPosts($userId: ID!, $first: Int, $after: String) {
    user(id: $userId) {
      id
      name
      posts(first: $first, after: $after) {
        edges {
          node {
            id
            title
            createdAt
          }
          cursor
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
`;

// Usage with variables
function UserPosts({ userId }: { userId: string }) {
  const { loading, error, data, fetchMore } = useQuery(GET_USER_POSTS, {
    variables: {
      userId,
      first: 10,
      after: null
    },
    notifyOnNetworkStatusChange: true,
  });

  const loadMore = () => {
    fetchMore({
      variables: {
        after: data.user.posts.pageInfo.endCursor,
      },
    });
  };

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (
    <div>
      <h2>{data.user.name}'s Posts</h2>
      {data.user.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}
      {data.user.posts.pageInfo.hasNextPage && (
        <button onClick={loadMore}>Load More</button>
      )}
    </div>
  );
}
```

### Server-Side Error Handling

```typescript
import { GraphQLError } from 'graphql';
import { Resolvers } from './generated/graphql';

export const resolvers: Resolvers = {
  Mutation: {
    createUser: async (_, { input }, context) => {
      // Validation
      if (!input.email.includes('@')) {
        return {
          user: null,
          errors: [{
            field: 'email',
            message: 'Invalid email format',
            code: 'VALIDATION_ERROR'
          }]
        };
      }

      // Check uniqueness
      const existingUser = await context.dataSources.userAPI.findByEmail(input.email);
      if (existingUser) {
        return {
          user: null,
          errors: [{
            field: 'email',
            message: 'Email already in use',
            code: 'CONFLICT'
          }]
        };
      }

      // Authorization
      if (!context.currentUser) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      if (context.currentUser.role !== 'ADMIN') {
        throw new GraphQLError('Not authorized', {
          extensions: { code: 'FORBIDDEN' }
        });
      }

      // Create user
      try {
        const user = await context.dataSources.userAPI.create(input);
        return { user, errors: [] };
      } catch (error) {
        throw new GraphQLError('Failed to create user', {
          extensions: { code: 'INTERNAL_ERROR' }
        });
      }
    },
  },
};
```

### Client-Side Error Handling

```typescript
import { ApolloError } from '@apollo/client';

function UserProfile({ userId }: { userId: string }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId },
    errorPolicy: 'all',  // Include partial data with errors
  });

  if (loading) return <Spinner />;

  if (error) {
    // Handle specific error codes
    if (error.graphQLErrors?.[0]?.extensions?.code === 'NOT_FOUND') {
      return <NotFound message="User not found" />;
    }

    if (error.graphQLErrors?.[0]?.extensions?.code === 'FORBIDDEN') {
      return <Unauthorized message="You don't have permission" />;
    }

    return <ErrorMessage error={error} />;
  }

  return (
    <div>
      <h1>{data.user.name}</h1>
      {error && (
        <div className="warnings">
          {error.graphQLErrors.map((err, i) => (
            <p key={i}>Warning: {err.message}</p>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## Real-World Use Cases

### 1. E-Commerce Product Listing

```graphql
# Complex query with multiple filters
query ProductCatalog(
  $category: String
  $minPrice: Int
  $maxPrice: Int
  $inStock: Boolean
  $sort: ProductSortInput
  $first: Int
  $after: String
) {
  products(
    filter: {
      category: $category
      price: { min: $minPrice, max: $maxPrice }
      inStock: $inStock
    }
    sort: $sort
    first: $first
    after: $after
  ) {
    edges {
      node {
        id
        name
        slug
        price
        compareAtPrice
        images {
          url
          alt
        }
        rating
        reviewCount
        inStock
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    filters {
      categories {
        name
        count
      }
      priceRange {
        min
        max
      }
    }
  }
}
```

### 2. User Registration Flow

```graphql
# Multi-step registration mutation
mutation RegisterUser($input: RegisterUserInput!) {
  registerUser(input: $input) {
    user {
      id
      name
      email
    }
    token
    errors {
      field
      message
      code
    }
  }
}

input RegisterUserInput {
  name: String!
  email: String!
  password: String!
  confirmPassword: String!
  acceptTerms: Boolean!
  referralCode: String
}

# Profile completion mutation
mutation CompleteProfile($input: CompleteProfileInput!) {
  completeProfile(input: $input) {
    user {
      id
      name
      avatar
      bio
      location
      website
    }
    errors {
      field
      message
      code
    }
  }
}

input CompleteProfileInput {
  avatar: Upload
  bio: String
  location: String
  website: URL
  interests: [String!]
}
```

### 3. Real-time Chat

```graphql
# Send message mutation
mutation SendMessage($conversationId: ID!, $content: String!) {
  sendMessage(conversationId: $conversationId, content: $content) {
    message {
      id
      content
      sender {
        id
        name
        avatar
      }
      createdAt
    }
    errors {
      field
      message
      code
    }
  }
}

# Subscribe to new messages
subscription OnNewMessage($conversationId: ID!) {
  messageReceived(conversationId: $conversationId) {
    id
    content
    sender {
      id
      name
      avatar
    }
    createdAt
  }
}
```

### 4. Content Management

```graphql
# Draft and publish workflow
mutation SaveDraft($input: SaveDraftInput!) {
  saveDraft(input: $input) {
    post {
      id
      title
      content
      status
      wordCount
      lastSavedAt
    }
    errors {
      field
      message
      code
    }
  }
}

mutation PublishPost($id: ID!, $publishOptions: PublishOptions) {
  publishPost(id: $id, options: $publishOptions) {
    post {
      id
      title
      slug
      status
      publishedAt
      url
    }
    errors {
      field
      message
      code
    }
  }
}

input SaveDraftInput {
  id: ID
  title: String!
  content: String!
  excerpt: String
  tags: [String!]
}

input PublishOptions {
  notifySubscribers: Boolean = true
  socialMedia: Boolean = false
  scheduleAt: DateTime
}
```

---

## Common Mistakes

### 1. Not Using Operation Names

```graphql
# BAD: Anonymous query
query {
  user(id: "1") {
    name
  }
}

# GOOD: Named operation
query GetUser {
  user(id: "1") {
    name
  }
}

# Why: Better debugging, logging, and error tracking
```

### 2. Over-fetching in Queries

```graphql
# BAD: Fetching everything
query {
  user(id: "1") {
    id
    name
    email
    password  # Never expose!
    internalNotes  # Never expose!
    posts {
      id
      title
      content
      comments {
        id
        body
        author {
          id
          name
          email
          posts {
            # ... too deep
          }
        }
      }
    }
  }
}

# GOOD: Fetch only what you need
query {
  user(id: "1") {
    id
    name
    posts {
      id
      title
    }
  }
}
```

### 3. Missing Error Handling in Mutations

```typescript
// BAD: No error handling
const [createUser] = useMutation(CREATE_USER);

const handleSubmit = async (input) => {
  await createUser({ variables: { input } });
};

// GOOD: Proper error handling
const [createUser, { loading, error }] = useMutation(CREATE_USER);

const handleSubmit = async (input) => {
  try {
    const { data } = await createUser({ variables: { input } });

    if (data.createUser.errors.length > 0) {
      // Handle business logic errors
      data.createUser.errors.forEach(err => {
        showToast(err.message, 'error');
      });
      return;
    }

    showToast('User created successfully', 'success');
    router.push(`/users/${data.createUser.user.id}`);
  } catch (error) {
    // Handle network/GraphQL errors
    showToast('An error occurred', 'error');
  }
};
```

### 4. Ignoring Query Variables

```typescript
// BAD: String interpolation (vulnerable to injection)
const query = gql`
  query {
    user(id: "${userId}") {
      name
    }
  }
`;

// GOOD: Use variables
const query = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      name
    }
  }
`;

const { data } = await client.query({
  query: GET_USER,
  variables: { id: userId }
});
```

### 5. Not Handling Loading States

```typescript
// BAD: No loading state
function UserProfile({ userId }) {
  const { data } = useQuery(GET_USER, {
    variables: { id: userId }
  });

  return <h1>{data.user.name}</h1>;  // Crashes during loading
}

// GOOD: Handle all states
function UserProfile({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId }
  });

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return <h1>{data.user.name}</h1>;
}
```

### 6. Not Using Fragments

```typescript
// BAD: Repeated field selections
const GET_USER_POSTS = gql`
  query GetUserPosts($id: ID!) {
    user(id: $id) {
      id
      name
      email
      avatar
      posts {
        id
        title
        author {
          id
          name
          email
          avatar
        }
      }
    }
  }
`;

// GOOD: Reusable fragments
const USER_FIELDS = gql`
  fragment UserFields on User {
    id
    name
    email
    avatar
  }
`;

const GET_USER_POSTS = gql`
  query GetUserPosts($id: ID!) {
    user(id: $id) {
      ...UserFields
      posts {
        id
        title
        author {
          ...UserFields
        }
      }
    }
  }
`;
```

---

## Best Practices

### Query Best Practices

```
1. Always name operations
   query GetUser { ... }

2. Use variables for dynamic values
   query GetUser($id: ID!) { user(id: $id) { ... } }

3. Request only needed fields
   { user { name } }  // Not { user { name email ... } }

4. Use fragments for reusable selections
   fragment UserFields on User { id name }

5. Implement pagination
   posts(first: 10, after: $cursor) { ... }

6. Use operation-level directives
   query GetUser @skip(if: $skipUser) { ... }
```

### Mutation Best Practices

```
1. Use Input types for mutation arguments
   mutation CreateUser(input: CreateUserInput!) { ... }

2. Return payload types with errors
   type CreateUserPayload { user: User, errors: [Error!]! }

3. Include success status in response
   { success: true, user: {...}, errors: [] }

4. Use optimistic updates for better UX
   optimisticResponse: { ... }

5. Handle partial failures
   { data: null, errors: [{ field: "email", message: "..." }] }

6. Validate input in resolvers, not client
   if (!input.email) return error;
```

### Error Handling Best Practices

```
1. Use error codes for programmatic handling
   code: NOT_FOUND, UNAUTHORIZED, VALIDATION_ERROR

2. Include field information for form errors
   { field: "email", message: "Invalid email" }

3. Distinguish between user and system errors
   - User errors: validation, not found, unauthorized
   - System errors: database, network, internal

4. Never expose internal errors to clients
   catch (error) { throw new GraphQLError("Internal error") }

5. Log errors for monitoring
   logger.error("Query failed", { query, error });
```

---

## Performance Considerations

### Query Optimization

```typescript
// 1. Use field-level caching
@ObjectType()
class Post {
  @Field(() => ID)
  id: string;

  @Field()
  title: string;

  @Field(() => Int)
  @CacheControl({ maxAge: 3600 })  // Cache for 1 hour
  viewCount: number;
}

// 2. Batch resolver execution
const postLoader = new DataLoader(async (ids) => {
  const posts = await db.post.findMany({ where: { id: { in: ids } } });
  return ids.map(id => posts.find(post => post.id === id));
});

// 3. Use query complexity limits
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(7),
    queryComplexityRule({ maximumComplexity: 1000 })
  ]
});
```

### Mutation Optimization

```typescript
// 1. Use transactions for related mutations
const resolvers = {
  Mutation: {
    transferMoney: async (_, { from, to, amount }, context) => {
      return context.db.transaction(async (tx) => {
        await tx.account.update({ where: { id: from }, data: { balance: { decrement: amount } } });
        await tx.account.update({ where: { id: to }, data: { balance: { increment: amount } } });
        return { success: true };
      });
    },
  },
};

// 2. Return minimal data after mutations
const resolvers = {
  Mutation: {
    updateUser: async (_, { id, input }, context) => {
      const user = await context.dataSources.userAPI.update(id, input);
      return {
        user: { id: user.id, name: user.name, email: user.email },  // Minimal fields
        errors: [],
      };
    },
  },
};
```

---

## Interview Questions

### Beginner

1. **What is the difference between a query and a mutation?**
   Queries are for reading data (idempotent, parallel execution). Mutations are for writing data (sequential execution, side effects allowed).

2. **What are GraphQL variables?**
   Variables allow passing dynamic values to queries/mutations without string interpolation. They're defined in the query and passed as a separate object.

3. **What is an operation name?**
   A named identifier for a query or mutation (e.g., `query GetUser { ... }`). It improves debugging, logging, and error tracking.

4. **What are fragments?**
   Reusable pieces of query logic that can be spread into multiple queries. They help avoid duplication and maintain consistency.

5. **How does GraphQL handle errors in mutations?**
   Through the `errors` array in the response. Business logic errors are returned in payload types, while system errors go to the top-level errors array.

### Intermediate

6. **What is the difference between `errorPolicy: 'none'` and `errorPolicy: 'all'`?**
   `none` (default) throws errors and doesn't return partial data. `all` returns both data and errors, allowing partial results.

7. **How do you implement pagination in GraphQL?**
   Use the Relay Connection pattern with edges, nodes, cursors, and pageInfo. This provides consistent cursor-based pagination.

8. **What are inline fragments?**
   Syntax for querying polymorphic types: `... on Type { fields }`. Used with unions and interfaces.

9. **How do you handle file uploads in mutations?**
   Use multipart form data specification or separate REST endpoints. Apollo Server supports this via the Upload scalar type.

10. **What is the difference between `fetchPolicy` options in Apollo Client?**
    - `cache-first`: Use cache, fetch if missing
    - `network-only`: Always fetch, update cache
    - `cache-and-network`: Return cache, also fetch
    - `no-cache`: Never use cache

### Senior

11. **How would you implement optimistic updates for a complex mutation?**
    ```typescript
    const [updatePost] = useMutation(UPDATE_POST, {
      optimisticResponse: {
        updatePost: {
          __typename: 'UpdatePostPayload',
          post: {
            __typename: 'Post',
            ...currentPost,
            ...input,
          },
          errors: [],
        },
      },
      update(cache, { data }) {
        cache.modify({
          id: cache.identify(currentPost),
          fields: {
            title() { return data.updatePost.post.title; },
          },
        });
      },
    });
    ```

12. **How do you handle mutations that affect multiple parts of the cache?**
    Use `cache.modify` or `cache.writeQuery` to update multiple entries. Consider refetching queries if cache updates are complex.

13. **Explain the trade-offs between `refetchQueries` and `update` function.**
    `refetchQueries`: Simple but causes loading states and extra network requests. `update`: Immediate UI update but more complex to implement.

14. **How do you implement mutation middleware?**
    Use Apollo Link chain, context-based middleware in resolvers, or custom hooks that wrap mutations.

15. **How would you handle rate limiting for mutations?**
    Client-side: debounce/throttle. Server-side: query complexity analysis, rate limiting middleware, persisted queries.

### FAANG-style

16. **Design a mutation for a social media "like" feature with optimistic updates.**
    Consider: immediate UI feedback, cache normalization, undo functionality, real-time updates via subscriptions, and handling concurrent likes.

17. **How would you implement a multi-step form using GraphQL mutations?**
    Use draft/save mutations, server-side validation at each step, and a final "submit" mutation that validates all steps atomically.

18. **Explain how you'd handle a mutation that triggers a long-running job.**
    Return job ID immediately, use subscriptions or polling for status updates, handle timeouts, and provide cancellation.

19. **How do you optimize mutations that touch many cache entries?**
    Batch cache updates, use `cache.writeFragment` for targeted updates, consider optimistic responses for complex mutations.

20. **Design a query/mutation strategy for offline-first applications.**
    Queue mutations, handle conflicts (OT/CRDT), sync when online, provide merge strategies, and handle partial failures.

### Follow-ups

21. **What happens if a mutation resolver throws an error?**
    The error is caught and added to the `errors` array. If the mutation was part of a transaction, it may rollback depending on implementation.

22. **How do you handle mutations in a microservices architecture?**
    Use saga pattern for distributed transactions, eventual consistency, idempotent mutations, and compensation logic.

23. **What is the difference between local state mutations and server mutations?**
    Local: Apollo Client cache updates only. Server: GraphQL mutations that persist data. They can be combined for optimistic updates.

24. **How do you test mutations?**
    Unit test resolvers with mocked context, integration test with test database, and end-to-end test with Apollo Server testing utilities.

25. **How do you handle batch mutations?**
    Use input arrays and return arrays of results/errors. Consider transactions and partial success handling.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Query** | Read operations, parallel, idempotent |
| **Mutation** | Write operations, sequential, side effects |
| **Variables** | Use for dynamic values, never interpolate |
| **Fragments** | Reusable query logic, avoid duplication |
| **Errors** | Use payload types with error arrays |
| **Optimism** | Use optimisticResponse for better UX |

---

## References & Learn More

- [GraphQL Queries and Mutations](https://graphql.org/learn/queries/)
- [Apollo Client Mutations](https://www.apollographql.com/docs/react/data/mutations/)
- [Relay Mutations](https://relay.dev/docs/guided-tutorial/mutations/)
- [GraphQL Error Handling](https://www.apollographql.com/docs/apollo-server/data/errors/)
- [Best Practices for GraphQL Mutations](https://blog.apollographql.com/graphql-basics-the-top-5-ways-to-use-mutations-efd51395cac3)
