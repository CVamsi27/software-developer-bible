# Apollo Client

## Definition

**Apollo Client** is a comprehensive state management library for JavaScript that integrates with GraphQL. It manages the interaction between client and server by parsing, caching, and error handling GraphQL operations. It provides React hooks, Vue integration, and vanilla JS support for building data-driven applications.

```text
Apollo Client = GraphQL Client + Normalized Cache + React Hooks + DevTools

```

---

## Why Do We Need It?

### The Data Fetching Problem

```text
Without Apollo Client:
┌─────────────────────────────────────────────────────────────────┐
│  1. Manual fetch calls for every query                          │
│  2. No normalized cache                                         │
│  3. Manual loading/error state management                       │
│  4. No optimistic updates                                       │
│  5. No automatic re-rendering on data changes                   │
└─────────────────────────────────────────────────────────────────┘

With Apollo Client:
┌─────────────────────────────────────────────────────────────────┐
│  1. Declarative queries with hooks                              │
│  2. Normalized cache with automatic updates                     │
│  3. Built-in loading/error states                               │
│  4. Optimistic updates for instant feedback                     │
│  5. Automatic re-rendering on cache changes                     │
│  6. DevTools for debugging                                      │
└─────────────────────────────────────────────────────────────────┘

```

### Apollo Client vs Alternatives

| Feature | Apollo Client | urql | React Query (tRPC) |
|---------|---------------|------|---------------------|
| **Cache** | Normalized | Document | Normalized |
| **Bundle Size** | 33KB | 10KB | 25KB |
| **Learning Curve** | Medium | Low | Medium |
| **Ecosystem** | Apollo Server | Any server | tRPC server |
| **DevTools** | Yes | Yes | Yes |
| **Subscriptions** | Yes | Yes | No (use WebSocket) |

---

## How It Works

### Architecture Overview

```text
┌──────────────────────────────────────────────────────────────────┐
│                    APOLLO CLIENT ARCHITECTURE                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    React Components                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│   │
│  │  │ useQuery │  │ useMutation│  │ useSubscription│  │ useLazyQuery││   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│   │
│  └───────┼──────────────┼──────────────┼──────────────┼──────┘   │
│          │              │              │              │           │
│  ┌───────▼──────────────▼──────────────▼──────────────▼──────┐   │
│  │                    Apollo Client Core                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │   Query      │  │   Mutation   │  │ Subscription │   │   │
│  │  │   Manager    │  │   Manager    │  │   Manager    │   │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │   │
│  │         └─────────────────┼─────────────────┘            │   │
│  │                           │                               │   │
│  │  ┌────────────────────────▼──────────────────────────┐   │   │
│  │  │              Normalized Cache                      │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │   │
│  │  │  │ Query    │  │ Entity   │  │ Optimistic│       │   │   │
│  │  │  │ Store    │  │ Store    │  │ Updates  │       │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘       │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼─────────────────────────────┐   │
│  │                    Apollo Link Chain                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│   │
│  │  │ Auth     │  │ HTTP     │  │ Retry    │  │ Error    ││   │
│  │  │ Link     │  │ Link     │  │ Link     │  │ Link     ││   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘│   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │                                    │
│  ┌─────────────────────────▼───────────────────────────────┐   │
│  │                    HTTP Transport                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ Fetch    │  │ Axios    │  │ WebSocket│              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘

```

### Normalized Cache

```text
Query Response:
{
  user: {
    id: "1",
    name: "John",
    posts: [
      { id: "101", title: "Post 1", author: { id: "1" } },
      { id: "102", title: "Post 2", author: { id: "1" } }
    ]
  }
}

Normalized Cache (InMemoryCache):
┌─────────────────────────────────────────────────────────────────┐
│  ROOT_QUERY                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  user({id:"1"}): { __ref: "User:1" }                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  User:1                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  id: "1", name: "John",                                  │   │
│  │  posts: [                                                 │   │
│  │    { __ref: "Post:101" },                                 │   │
│  │    { __ref: "Post:102" }                                  │   │
│  │  ]                                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Post:101                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  id: "101", title: "Post 1",                             │   │
│  │  author: { __ref: "User:1" }                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Post:102                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  id: "102", title: "Post 2",                             │   │
│  │  author: { __ref: "User:1" }                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

Benefits:

- Single source of truth per entity
- Automatic cache updates when data changes
- Efficient re-renders (only affected components update)

```

---

## Code Examples

### Basic Setup

```typescript
import { ApolloClient, InMemoryCache, HttpLink, gql } from '@apollo/client';

// Create Apollo Client
const client = new ApolloClient({
  link: new HttpLink({ uri: 'http://localhost:4000/graphql' }),
  cache: new InMemoryCache({
    typePolicies: {
      User: {
        keyFields: ['id'],  // Use 'id' for cache normalization
      },
      Post: {
        keyFields: ['id'],
      },
    },
  }),
});

// Execute query
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

const { data } = await client.query({
  query: GET_USER,
  variables: { id: '1' },
});

console.log(data.user.name);  // "John"

```

### React Provider Setup

```typescript
import { ApolloProvider } from '@apollo/client';
import { ApolloClient, InMemoryCache } from '@apollo/client';
import App from './App';

const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql',
  cache: new InMemoryCache(),
});

function Root() {
  return (
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  );
}

export default Root;

```

### useQuery Hook

```typescript
import { gql, useQuery } from '@apollo/client';

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
            excerpt
            createdAt
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
  }
`;

function UserPosts({ userId }: { userId: string }) {
  const { loading, error, data, fetchMore, refetch } = useQuery(GET_USER_POSTS, {
    variables: {
      userId,
      first: 10,
      after: null,
    },
    // Polling for real-time updates
    pollInterval: 30000,  // 30 seconds

    // Fetch policy
    fetchPolicy: 'cache-and-network',  // Return cache, also fetch

    // Error policy
    errorPolicy: 'all',  // Return partial data with errors

    // Skip query if no userId
    skip: !userId,

    // Notify on network status change
    notifyOnNetworkStatusChange: true,
  });

  const loadMore = () => {
    fetchMore({
      variables: {
        after: data.user.posts.pageInfo.endCursor,
      },
    });
  };

  if (loading && !data) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <h2>{data.user.name}'s Posts ({data.user.posts.totalCount})</h2>

      {data.user.posts.edges.map(({ node, cursor }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {data.user.posts.pageInfo.hasNextPage && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}

```

### useMutation Hook

```typescript
import { gql, useMutation } from '@apollo/client';

const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      post {
        id
        title
        content
        createdAt
      }
      errors {
        field
        message
        code
      }
    }
  }
`;

function CreatePostForm() {
  const [createPost, { loading, error }] = useMutation(CREATE_POST, {
    // Update cache after mutation
    update(cache, { data }) {
      if (data.createPost.post) {
        // Option 1: Refetch queries
        // refetchQueries: [{ query: GET_POSTS }]

        // Option 2: Update cache manually
        cache.modify({
          fields: {
            posts(existingPosts = []) {
              const newPostRef = cache.writeFragment({
                data: data.createPost.post,
                fragment: gql`
                  fragment NewPost on Post {
                    id
                    title
                    content
                    createdAt
                  }
                `,
              });
              return [newPostRef, ...existingPosts];
            },
          },
        });
      }
    },

    // Optimistic response
    optimisticResponse: {
      createPost: {
        __typename: 'CreatePostPayload',
        post: {
          __typename: 'Post',
          id: 'temp-id',
          title: 'Optimistic Title',
          content: 'Optimistic content',
          createdAt: new Date().toISOString(),
        },
        errors: [],
      },
    },

    // On completed
    onCompleted: (data) => {
      if (data.createPost.post) {
        showToast('Post created successfully!');
        router.push(`/posts/${data.createPost.post.id}`);
      }
    },

    // On error
    onError: (error) => {
      showToast('Failed to create post', 'error');
    },
  });

  const handleSubmit = async (title: string, content: string) => {
    await createPost({
      variables: {
        input: { title, content, status: 'DRAFT' },
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Post'}
      </button>
      {error && <ErrorMessage error={error} />}
    </form>
  );
}

```

### useLazyQuery Hook

```typescript
import { gql, useLazyQuery } from '@apollo/client';

const SEARCH_USERS = gql`
  query SearchUsers($query: String!) {
    users(search: $query) {
      id
      name
      email
      avatar
    }
  }
`;

function UserSearch() {
  const [searchUsers, { loading, data }] = useLazyQuery(SEARCH_USERS, {
    // Debounce requests
    fetchPolicy: 'network-only',
  });

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    if (query.length >= 2) {
      searchUsers({ variables: { query } });
    }
  };

  return (
    <div>
      <input
        type="search"
        placeholder="Search users..."
        onChange={handleSearch}
      />

      {loading && <Spinner />}

      {data?.users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

```

### useSubscription Hook

```typescript
import { gql, useSubscription } from '@apollo/client';

const NEW_COMMENT = gql`
  subscription OnNewComment($postId: ID!) {
    commentAdded(postId: $postId) {
      id
      body
      author {
        id
        name
        avatar
      }
      createdAt
    }
  }
`;

function PostComments({ postId }: { postId: string }) {
  const { data, loading } = useSubscription(NEW_COMMENT, {
    variables: { postId },
    onData: ({ data }) => {
      // Handle new comment
      const newComment = data.data.commentAdded;
      showToast(`New comment from ${newComment.author.name}`);
    },
  });

  // ... render comments
}

```

### Cache Updates

```typescript
// 1. Update cache after mutation
const [deletePost] = useMutation(DELETE_POST, {
  update(cache, { data }) {
    if (data.deletePost.deletedPostId) {
      cache.modify({
        fields: {
          posts(existingPosts, { readField }) {
            return existingPosts.filter(
              (postRef) => readField('id', postRef) !== data.deletePost.deletedPostId
            );
          },
        },
      });
    }
  },
});

// 2. Write to cache directly
client.writeQuery({
  query: GET_USER,
  variables: { id: '1' },
  data: {
    user: {
      id: '1',
      name: 'Updated Name',
      __typename: 'User',
    },
  },
});

// 3. Read from cache
const { user } = client.readQuery({
  query: GET_USER,
  variables: { id: '1' },
});

// 4. Modify cache with optimistic updates
const [updateUser] = useMutation(UPDATE_USER, {
  optimisticResponse: {
    updateUser: {
      __typename: 'UpdateUserPayload',
      user: {
        __typename: 'User',
        id: userId,
        ...input,
      },
    },
  },
  update(cache, { data }) {
    cache.modify({
      id: cache.identify({ __typename: 'User', id: userId }),
      fields: {
        name() { return data.updateUser.user.name; },
        email() { return data.updateUser.user.email; },
      },
    });
  },
});

```

### Apollo Client with TypeScript

```typescript
import { gql, useQuery, TypedDocumentNode } from '@apollo/client';

// Define query type
const GET_USER: TypedDocumentNode<{
  user: {
    id: string;
    name: string;
    email: string;
  };
}, { id: string }> = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

// Typed hook
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useQuery(GET_USER, {
    variables: { id: userId },
  });

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  // data.user is fully typed
  return (
    <div>
      <h1>{data.user.name}</h1>
      <p>{data.user.email}</p>
    </div>
  );
}

```

---

## Real-World Use Cases

### 1. Infinite Scroll with Cache

```typescript
import { gql, useQuery } from '@apollo/client';

const GET_POSTS = gql`
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
    }
  }
`;

function InfiniteScrollFeed() {
  const { data, loading, fetchMore } = useQuery(GET_POSTS, {
    variables: { first: 10 },
  });

  const loadMore = () => {
    if (!data?.posts.pageInfo.hasNextPage) return;

    fetchMore({
      variables: {
        after: data.posts.pageInfo.endCursor,
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult) return previousResult;

        return {
          posts: {
            ...fetchMoreResult.posts,
            edges: [
              ...previousResult.posts.edges,
              ...fetchMoreResult.posts.edges,
            ],
          },
        };
      },
    });
  };

  return (
    <InfiniteScroll
      loadMore={loadMore}
      hasMore={data?.posts.pageInfo.hasNextPage}
      loader={<Spinner key={0} />}
    >
      {data?.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}
    </InfiniteScroll>
  );
}

```

### 2. Optimistic UI with Undo

```typescript
import { gql, useMutation } from '@apollo/client';

const DELETE_POST = gql`
  mutation DeletePost($id: ID!) {
    deletePost(id: $id) {
      deletedPostId
    }
  }
`;

const RESTORE_POST = gql`
  mutation RestorePost($input: RestorePostInput!) {
    restorePost(input: $input) {
      post {
        id
        title
      }
    }
  }
`;

function PostCard({ post }: { post: Post }) {
  const [deletePost] = useMutation(DELETE_POST, {
    optimisticResponse: {
      deletePost: {
        __typename: 'DeletePostPayload',
        deletedPostId: post.id,
      },
    },
    update(cache) {
      cache.modify({
        fields: {
          posts(existingPosts, { readField }) {
            return existingPosts.filter(
              (ref) => readField('id', ref) !== post.id
            );
          },
        },
      });
    },
  });

  const [restorePost] = useMutation(RESTORE_POST);

  const handleDelete = async () => {
    await deletePost({ variables: { id: post.id } });

    // Show undo toast
    showToast('Post deleted', {
      action: {
        label: 'Undo',
        onClick: () => restorePost({
          variables: { input: { postId: post.id } }
        }),
      },
      duration: 5000,
    });
  };

  return (
    <div>
      <h3>{post.title}</h3>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}

```

### 3. Form with Auto-Save

```typescript
import { gql, useMutation, useQuery } from '@apollo/client';
import { debounce } from 'lodash';

const GET_DRAFT = gql`
  query GetDraft($id: ID!) {
    draft(id: $id) {
      id
      title
      content
      lastSavedAt
    }
  }
`;

const SAVE_DRAFT = gql`
  mutation SaveDraft($input: SaveDraftInput!) {
    saveDraft(input: $input) {
      draft {
        id
        lastSavedAt
      }
    }
  }
`;

function AutoSaveEditor({ draftId }: { draftId: string }) {
  const { data } = useQuery(GET_DRAFT, { variables: { id: draftId } });
  const [saveDraft] = useMutation(SAVE_DRAFT);

  const autoSave = debounce(async (title: string, content: string) => {
    await saveDraft({
      variables: {
        input: { id: draftId, title, content }
      }
    });
  }, 2000);

  const handleChange = (field: string, value: string) => {
    autoSave(
      field === 'title' ? value : data.draft.title,
      field === 'content' ? value : data.draft.content
    );
  };

  return (
    <div>
      <input
        defaultValue={data?.draft.title}
        onChange={(e) => handleChange('title', e.target.value)}
      />
      <textarea
        defaultValue={data?.draft.content}
        onChange={(e) => handleChange('content', e.target.value)}
      />
      {data?.draft.lastSavedAt && (
        <span>Last saved: {new Date(data.draft.lastSavedAt).toLocaleTimeString()}</span>
      )}
    </div>
  );
}

```

---

## Common Mistakes

### 1. Not Handling Loading States

```typescript
// BAD: No loading state
function UserProfile({ userId }) {
  const { data } = useQuery(GET_USER, { variables: { id: userId } });
  return <h1>{data.user.name}</h1>;  // Crashes during loading
}

// GOOD: Handle all states
function UserProfile({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId },
  });

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return <h1>{data.user.name}</h1>;
}

```

### 2. Not Using Cache Properly

```typescript
// BAD: Always refetches
const { data } = useQuery(GET_USER, {
  variables: { id: userId },
  fetchPolicy: 'network-only',  // Never uses cache
});

// GOOD: Use appropriate fetch policy
const { data } = useQuery(GET_USER, {
  variables: { id: userId },
  fetchPolicy: 'cache-first',  // Default: use cache, fetch if missing
});

```

### 3. Missing Cache Updates

```typescript
// BAD: Cache not updated after mutation
const [createPost] = useMutation(CREATE_POST);
// Cache still shows old list of posts

// GOOD: Update cache after mutation
const [createPost] = useMutation(CREATE_POST, {
  update(cache, { data }) {
    cache.modify({
      fields: {
        posts(existingPosts) {
          const newPostRef = cache.writeFragment({
            data: data.createPost.post,
            fragment: POST_FRAGMENT,
          });
          return [newPostRef, ...existingPosts];
        },
      },
    });
  },
});

```

### 4. Not Using Variables

```typescript
// BAD: String interpolation
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

const { data } = useQuery(query, { variables: { id: userId } });

```

### 5. Ignoring Error Policy

```typescript
// BAD: Default error policy (throws on errors)
const { data, error } = useQuery(GET_USER);
if (error) {
  // Error is thrown, data might be undefined
}

// GOOD: Use 'all' error policy for partial data
const { data, error } = useQuery(GET_USER, {
  errorPolicy: 'all',
});
if (data?.user) {
  // Data is available even with errors
}

```

---

## Best Practices

### Query Optimization

```text

1. Use fragments for reusable selections
   fragment UserFields on User { id name email }

2. Request only needed fields
   { user { name } }  // Not { user { name email ... } }

3. Use pagination
   posts(first: 10, after: $cursor) { ... }

4. Set appropriate fetch policies

   - cache-first (default): Use cache, fetch if missing
   - network-only: Always fetch, update cache
   - cache-and-network: Return cache, also fetch

5. Use polling for real-time data
   pollInterval: 30000

```

### Cache Management

```text

1. Define keyFields for normalization
   typePolicies: { User: { keyFields: ['id'] } }

2. Update cache after mutations
   Use update function or refetchQueries

3. Use optimistic responses
   optimisticResponse: { ... }

4. Handle cache eviction
   cache.evict({ id: 'User:1' })

5. Monitor cache size
   cache.gc()  // Garbage collect

```

### Performance

```text

1. Use skip option for conditional queries
   skip: !userId

2. Debounce search queries
   useLazyQuery with debounce

3. Use pagination for large lists

4. Avoid unnecessary re-renders
   Use React.memo for components

5. Use polling sparingly
   Prefer subscriptions for real-time

```

---

## Performance Considerations

### Bundle Size Optimization

```typescript
// Import only what you need
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

// Use tree-shaking
import { useQuery } from '@apollo/client/react/hooks';

// Avoid importing everything
// import * as Apollo from '@apollo/client';  // BAD

```

### Query Batching

```typescript
import { BatchHttpLink } from '@apollo/client/link/batch-http';

const link = new BatchHttpLink({
  uri: 'http://localhost:4000/graphql',
  batchMax: 10,
  batchInterval: 20,
});

const client = new ApolloClient({
  link,
  cache: new InMemoryCache(),
});

```

### Cache Pagination

```typescript
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        posts: {
          keyArgs: ['filter'],  // Cache separately for different filters
          merge(existing = { edges: [] }, incoming) {
            return {
              ...incoming,
              edges: [...existing.edges, ...incoming.edges],
            };
          },
        },
      },
    },
  },
});

```

---

## Interview Questions

### Beginner

1. **What is Apollo Client?**
   Apollo Client is a GraphQL client that manages data fetching, caching, and state management for JavaScript applications.

2. **How do you set up Apollo Client in React?**
   Create `ApolloClient` instance, wrap app with `ApolloProvider`, and use hooks like `useQuery` and `useMutation`.

3. **What is the difference between `useQuery` and `useLazyQuery`?**
   `useQuery` executes immediately on render. `useLazyQuery` executes only when you call the returned function.

4. **What is the Apollo Client cache?**
   A normalized in-memory cache that stores query results. It automatically updates when mutations modify cached data.

5. **How do you handle loading states?**
   Use the `loading` boolean from `useQuery` to show spinners or skeleton UI.

### Intermediate

6. **What are fetch policies?**
   Strategies for how Apollo Client uses the cache:

   - `cache-first`: Use cache, fetch if missing
   - `network-only`: Always fetch, update cache
   - `cache-and-network`: Return cache, also fetch
   - `no-cache`: Never use cache

7. **How do you update cache after mutations?**
   Use the `update` function to modify cache, `refetchQueries` to refetch affected queries, or `optimisticResponse` for instant UI.

8. **What is optimistic UI?**
   Showing the expected result before the server responds. If the server fails, Apollo automatically rolls back.

9. **How do you handle pagination?**
   Use `fetchMore` with cursor-based pagination and `updateQuery` to merge results.

10. **What are fragments?**
    Reusable selections that can be spread into queries. They help avoid duplication and improve cache normalization.

### Senior

11. **How would you optimize Apollo Client for a large application?**
    Code splitting, query batching, cache pagination, optimistic updates, and monitoring with Apollo DevTools.

12. **Explain Apollo Client's normalized cache.**
    Entities are stored by `__typename:id`. Queries reference entities. Updates propagate automatically.

13. **How do you handle cache conflicts?**
    Use `keyFields` for proper normalization, `merge` functions for lists, and `optimisticResponse` for concurrent updates.

14. **How would you implement offline support?**
    Queue mutations, persist cache to localStorage/IndexedDB, and sync when online.

15. **How do you migrate from REST to Apollo Client?**
    Start with new features, use `@rest` link for gradual migration, and maintain backward compatibility.

### FAANG-style

16. **Design a caching strategy for a social media feed.**
    Normalized cache for entities, cursor-based pagination, optimistic updates for likes/comments, and TTL-based eviction.

17. **How would you handle Apollo Client in a micro-frontends architecture?**
    Shared Apollo Client instance, cache isolation per micro-frontend, and cross-frontend cache updates.

18. **Explain your approach to Apollo Client performance monitoring.**
    Track query execution time, cache hit rates, network requests, and bundle size impact.

19. **How do you handle real-time updates with Apollo Client?**
    Use subscriptions, optimistic updates, and cache normalization for instant UI updates.

20. **Design a global state management solution with Apollo Client.**
    Use `@client` directives for local state, cache policies for normalization, and reactive variables for fine-grained updates.

### Follow-ups

21. **What happens when Apollo Client loses network connection?**
    Queries fail, mutations queue (if configured), and cache remains available. Use `errorPolicy: 'all'` for offline-first.

22. **How does Apollo Client handle concurrent mutations?**
    Mutations execute in order. Optimistic updates are applied immediately. Cache updates are atomic.

23. **What is the difference between `update` and `refetchQueries`?**
    `update` modifies cache immediately. `refetchQueries` fetches fresh data from server. Use `update` for instant UI, `refetchQueries` for data consistency.

24. **How do you debug Apollo Client issues?**
    Use Apollo DevTools, enable logging, check cache state, and monitor network requests.

25. **What are the limitations of Apollo Client?**
    Bundle size, complexity for simple apps, learning curve, and dependency on Apollo ecosystem.

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Setup** | ApolloClient + ApolloProvider + Hooks |
| **Queries** | useQuery, useLazyQuery, useSubscription |
| **Mutations** | useMutation with update/optimisticResponse |
| **Cache** | Normalized, automatic updates |
| **Performance** | Batching, pagination, optimistic UI |
| **DevTools** | Essential for debugging |

---

## References & Learn More

- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [Apollo Client Hooks](https://www.apollographql.com/docs/react/data/hooks/)
- [Apollo Client Cache](https://www.apollographql.com/docs/react/caching/overview/)
- [Apollo Client DevTools](https://www.apollographql.com/docs/react/devtools/)
- [GraphQL Code Generator](https://www.graphql-code-generator.com/)
- [Apollo Client Examples](https://github.com/apollographql/apollo-client-integration-react)
