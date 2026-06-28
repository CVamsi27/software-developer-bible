# Pagination

## Definition

Pagination is the practice of dividing large datasets into smaller, manageable chunks (pages) that can be retrieved incrementally. It's essential for REST APIs to avoid returning excessive data, improve performance, reduce memory usage, and provide a better user experience.

## Why Do We Need It?

Without pagination, APIs would face:

1. **Memory exhaustion** - Loading millions of records at once

2. **Network overhead** - Transferring massive payloads

3. **Slow responses** - Long query times for large datasets

4. **Poor UX** - Users waiting for complete data loads

5. **Resource waste** - Client and server processing unnecessary data

## How It Works

### Pagination Strategies

```text
Pagination Strategies
═════════════════════

1. Offset-Based (Traditional)
   GET /api/users?page=3&limit=10
   OFFSET 20 LIMIT 10

2. Cursor-Based
   GET /api/users?cursor=abc123&limit=10
   WHERE id > 'abc123' LIMIT 10

3. Keyset-Based
   GET /api/users?createdAfter=2024-01-01&limit=10
   WHERE created_at > '2024-01-01' LIMIT 10

4. Time-Based
   GET /api/events?since=2024-01-01T00:00:00Z&limit=10
   WHERE timestamp > '2024-01-01' LIMIT 10

```

### Offset-Based Pagination

```text
Offset Pagination
═════════════════

Request: GET /api/users?page=3&limit=10

Total Records: 100

Page 1:  Records 1-10   (OFFSET 0,  LIMIT 10)
Page 2:  Records 11-20  (OFFSET 10, LIMIT 10)
Page 3:  Records 21-30  (OFFSET 20, LIMIT 10)  ◄── Current
Page 4:  Records 31-40  (OFFSET 30, LIMIT 10)
...
Page 10: Records 91-100 (OFFSET 90, LIMIT 10)

Response:
{
  "data": [...],
  "pagination": {
    "page": 3,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}

```

```typescript
// Offset-based pagination implementation
app.get('/api/users', async (req, res) => {
  const { page = '1', limit = '10' } = req.query;

  const pageNum = Math.max(1, parseInt(page as string));
  const limitNum = Math.min(100, Math.max(1, parseInt(limit as string)));
  const offset = (pageNum - 1) * limitNum;

  const [users, total] = await Promise.all([
    UserService.findAll({ offset, limit: limitNum }),
    UserService.count()
  ]);

  res.json({
    data: users,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      pages: Math.ceil(total / limitNum)
    },
    _links: {
      self: `/api/users?page=${pageNum}&limit=${limitNum}`,
      first: `/api/users?page=1&limit=${limitNum}`,
      last: `/api/users?page=${Math.ceil(total / limitNum)}&limit=${limitNum}`,
      next: pageNum < Math.ceil(total / limitNum)
        ? `/api/users?page=${pageNum + 1}&limit=${limitNum}`
        : null,
      prev: pageNum > 1
        ? `/api/users?page=${pageNum - 1}&limit=${limitNum}`
        : null
    }
  });
});

```

### Cursor-Based Pagination

```text
Cursor Pagination
═════════════════

Request: GET /api/users?cursor=eyJpZCI6MTB9&limit=10

Cursor = Base64 encoded last item ID
Cursor "eyJpZCI6MTB9" = { "id": 10 }

First Request:
  GET /api/users?limit=10
  Returns: users 1-10, cursor: "eyJpZCI6MTB9"

Second Request:
  GET /api/users?cursor=eyJpZCI6MTB9&limit=10
  Returns: users 11-20, cursor: "eyJpZCI6MjB9"

Third Request:
  GET /api/users?cursor=eyJpZCI6MjB9&limit=10
  Returns: users 21-30, cursor: "eyJpZCI6MzB9"

Response:
{
  "data": [...],
  "pagination": {
    "hasMore": true,
    "nextCursor": "eyJpZCI6MjB9"
  }
}

```

```typescript
// Cursor-based pagination implementation
app.get('/api/users', async (req, res) => {
  const { cursor, limit = '10' } = req.query;

  const limitNum = Math.min(100, Math.max(1, parseInt(limit as string)));

  let whereClause = {};
  if (cursor) {
    const decodedCursor = JSON.parse(Buffer.from(cursor as string, 'base64').toString());
    whereClause = { id: { $gt: decodedCursor.id } };
  }

  const users = await UserService.findAll({
    where: whereClause,
    limit: limitNum + 1, // Fetch one extra to check if there are more
    order: [['id', 'ASC']]
  });

  const hasMore = users.length > limitNum;
  const data = hasMore ? users.slice(0, limitNum) : users;
  const nextCursor = hasMore
    ? Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64')
    : null;

  res.json({
    data,
    pagination: {
      hasMore,
      nextCursor
    }
  });
});

```

### Keyset-Based Pagination

```text
Keyset Pagination
═════════════════

Request: GET /api/users?createdAfter=2024-01-01&limit=10

First Request:
  GET /api/users?limit=10&sort=created_at
  Returns: users 1-10 (created 2024-01-01 to 2024-01-10)
  Response includes: lastCreated: "2024-01-10"

Second Request:
  GET /api/users?createdAfter=2024-01-10&limit=10&sort=created_at
  Returns: users 11-20 (created 2024-01-11 to 2024-01-20)

Response:
{
  "data": [...],
  "pagination": {
    "hasMore": true,
    "filters": {
      "createdAfter": "2024-01-20"
    }
  }
}

```

```typescript
// Keyset pagination implementation
app.get('/api/users', async (req, res) => {
  const { createdAfter, createdBefore, limit = '10', sort = 'created_at' } = req.query;

  const limitNum = Math.min(100, Math.max(1, parseInt(limit as string)));

  const whereClause: any = {};

  if (createdAfter) {
    whereClause.created_at = { $gt: new Date(createdAfter as string) };
  }
  if (createdBefore) {
    whereClause.created_at = { ...whereClause.created_at, $lt: new Date(createdBefore as string) };
  }

  const users = await UserService.findAll({
    where: whereClause,
    limit: limitNum + 1,
    order: [[sort, 'ASC']]
  });

  const hasMore = users.length > limitNum;
  const data = hasMore ? users.slice(0, limitNum) : users;
  const lastItem = data[data.length - 1];

  res.json({
    data,
    pagination: {
      hasMore,
      filters: {
        createdAfter: lastItem?.created_at?.toISOString()
      }
    }
  });
});

```

### Infinite Scroll Implementation

```typescript
// Infinite scroll backend
app.get('/api/feed', authenticate, async (req, res) => {
  const { cursor, limit = '20' } = req.query;
  const limitNum = parseInt(limit as string);

  const feed = await FeedService.getForUser(req.user.id, {
    cursor,
    limit: limitNum + 1
  });

  const hasMore = feed.length > limitNum;
  const posts = hasMore ? feed.slice(0, limitNum) : feed;
  const nextCursor = hasMore ? posts[posts.length - 1].id : null;

  // Prefetch indicator
  const shouldPrefetch = posts.length <= limitNum * 0.7;

  res.json({
    data: posts,
    pagination: {
      hasMore,
      nextCursor,
      shouldPrefetch
    }
  });
});

```

### Pagination Response Formats

```typescript
// Format 1: Page-based with links
interface PagePaginationResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
  _links: {
    self: string;
    first: string;
    last: string;
    next: string | null;
    prev: string | null;
  };
}

// Format 2: Cursor-based
interface CursorPaginationResponse<T> {
  data: T[];
  pagination: {
    hasMore: boolean;
    nextCursor: string | null;
  };
}

// Format 3: Keyset-based
interface KeysetPaginationResponse<T> {
  data: T[];
  pagination: {
    hasMore: boolean;
    filters: Record<string, any>;
  };
}

```

## Code Examples

### Complete Pagination System

```typescript
import express, { Request, Response } from 'express';

// Generic pagination middleware
function paginate(schema: any) {
  return async (req: Request, res: Response, next: Function) => {
    const { page, limit, cursor, sort, order } = req.query;

    const paginationType = cursor ? 'cursor' : 'offset';

    if (paginationType === 'offset') {
      const pageNum = Math.max(1, parseInt(page as string) || 1);
      const limitNum = Math.min(100, Math.max(1, parseInt(limit as string) || 10));

      req.pagination = {
        type: 'offset',
        page: pageNum,
        limit: limitNum,
        offset: (pageNum - 1) * limitNum
      };
    } else {
      const limitNum = Math.min(100, Math.max(1, parseInt(limit as string) || 10));

      req.pagination = {
        type: 'cursor',
        cursor: cursor as string,
        limit: limitNum
      };
    }

    req.sort = {
      field: (sort as string) || 'createdAt',
      order: (order as string) || 'desc'
    };

    next();
  };
}

// User routes with pagination
app.get('/api/users', paginate(UserSchema), async (req: Request, res: Response) => {
  const { pagination, sort } = req;

  let users;
  let paginationResponse;

  if (pagination.type === 'offset') {
    const [data, total] = await Promise.all([
      UserService.findAll({
        offset: pagination.offset,
        limit: pagination.limit,
        sort: sort.field,
        order: sort.order
      }),
      UserService.count()
    ]);

    users = data;
    paginationResponse = {
      page: pagination.page,
      limit: pagination.limit,
      total,
      pages: Math.ceil(total / pagination.limit)
    };
  } else {
    const data = await UserService.findAll({
      cursor: pagination.cursor,
      limit: pagination.limit,
      sort: sort.field,
      order: sort.order
    });

    users = data;
    paginationResponse = {
      hasMore: data.length === pagination.limit,
      nextCursor: data.length === pagination.limit
        ? data[data.length - 1].id
        : null
    };
  }

  res.json({
    data: users,
    pagination: paginationResponse
  });
});

// Cursor helper functions
function encodeCursor(data: any): string {
  return Buffer.from(JSON.stringify(data)).toString('base64');
}

function decodeCursor(cursor: string): any {
  return JSON.parse(Buffer.from(cursor, 'base64').toString());
}

```

### Search with Pagination

```typescript
app.get('/api/search', async (req, res) => {
  const { q, page = '1', limit = '10' } = req.query;

  if (!q) {
    return res.status(400).json({ error: 'Query parameter required' });
  }

  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);
  const offset = (pageNum - 1) * limitNum;

  const [results, total] = await Promise.all([
    SearchService.search(q as string, { offset, limit: limitNum }),
    SearchService.count(q as string)
  ]);

  res.json({
    data: results,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      pages: Math.ceil(total / limitNum)
    },
    query: q
  });
});

```

### Sorting with Pagination

```typescript
app.get('/api/products', async (req, res) => {
  const { page = '1', limit = '10', sort = 'createdAt', order = 'desc' } = req.query;

  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);

  // Validate sort field
  const allowedSortFields = ['createdAt', 'price', 'name', 'rating'];
  const sortField = allowedSortFields.includes(sort as string) ? sort : 'createdAt';
  const sortOrder = order === 'asc' ? 'ASC' : 'DESC';

  const [products, total] = await Promise.all([
    ProductService.findAll({
      offset: (pageNum - 1) * limitNum,
      limit: limitNum,
      sort: sortField,
      order: sortOrder
    }),
    ProductService.count()
  ]);

  res.json({
    data: products,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      pages: Math.ceil(total / limitNum)
    },
    sort: {
      field: sortField,
      order: sortOrder
    }
  });
});

```

## Real-World Use Cases

### 1. Social Media Feed

```typescript
// Infinite scroll feed
app.get('/api/feed', authenticate, async (req, res) => {
  const { cursor, limit = '20' } = req.query;

  const feed = await FeedService.getPersonalized(req.user.id, {
    cursor,
    limit: parseInt(limit as string)
  });

  res.json({
    data: feed,
    pagination: {
      hasMore: feed.length === parseInt(limit as string),
      nextCursor: feed.length === parseInt(limit as string)
        ? feed[feed.length - 1].id
        : null
    }
  });
});

```

### 2. E-commerce Product Catalog

```typescript
// Product listing with filters
app.get('/api/products', async (req, res) => {
  const { page = '1', limit = '24', category, minPrice, maxPrice, sort } = req.query;

  const filters: ProductFilters = {};
  if (category) filters.category = category as string;
  if (minPrice) filters.minPrice = parseFloat(minPrice as string);
  if (maxPrice) filters.maxPrice = parseFloat(maxPrice as string);

  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);

  const [products, total] = await Promise.all([
    ProductService.findAll({
      filters,
      offset: (pageNum - 1) * limitNum,
      limit: limitNum,
      sort: sort as string
    }),
    ProductService.count(filters)
  ]);

  res.json({
    data: products,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      pages: Math.ceil(total / limitNum)
    },
    filters
  });
});

```

### 3. Chat Messages

```typescript
// Load older messages
app.get('/api/conversations/:id/messages', authenticate, async (req, res) => {
  const { cursor, limit = '50' } = req.query;

  const messages = await MessageService.getForConversation(req.params.id, {
    cursor,
    limit: parseInt(limit as string)
  });

  res.json({
    data: messages,
    pagination: {
      hasMore: messages.length === parseInt(limit as string),
      nextCursor: messages.length === parseInt(limit as string)
        ? messages[0].id // Oldest message in batch
        : null
    }
  });
});

```

### 4. Admin Dashboard Data

```typescript
// Admin user management with pagination
app.get('/api/admin/users', adminOnly, async (req, res) => {
  const { page = '1', limit = '50', status, role, search } = req.query;

  const filters: AdminUserFilters = {};
  if (status) filters.status = status as string;
  if (role) filters.role = role as string;
  if (search) filters.search = search as string;

  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);

  const [users, total] = await Promise.all([
    UserService.adminFindAll({
      filters,
      offset: (pageNum - 1) * limitNum,
      limit: limitNum
    }),
    UserService.adminCount(filters)
  ]);

  res.json({
    data: users,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      pages: Math.ceil(total / limitNum)
    },
    filters
  });
});

```

## Common Mistakes

### 1. No Maximum Limit

```typescript
// ❌ Bad: No limit on page size
const limit = parseInt(req.query.limit as string) || 10;
const users = await UserService.findAll({ limit });

// ✅ Good: Enforce maximum limit
const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 10));
const users = await UserService.findAll({ limit });

```

### 2. Not Including Total Count

```typescript
// ❌ Bad: Missing total
res.json({ data: users });

// ✅ Good: Include total for UI pagination
res.json({
  data: users,
  pagination: {
    page: pageNum,
    limit: limitNum,
    total,
    pages: Math.ceil(total / limitNum)
  }
});

```

### 3. Inconsistent Sort Order

```typescript
// ❌ Bad: Default sort not specified
const users = await UserService.findAll({ page, limit });

// ✅ Good: Always specify default sort
const sort = req.query.sort || 'createdAt';
const order = req.query.order || 'desc';
const users = await UserService.findAll({ page, limit, sort, order });

```

### 4. Not Handling Edge Cases

```typescript
// ❌ Bad: No validation
const page = parseInt(req.query.page);
const users = await UserService.findAll({ offset: (page - 1) * limit });

// ✅ Good: Validate inputs
const page = Math.max(1, parseInt(req.query.page as string) || 1);
const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 10));
const offset = (page - 1) * limit;

```

### 5. Not Providing Navigation Links

```typescript
// ❌ Bad: No links
res.json({ data: users, pagination: { page, total } });

// ✅ Good: Include navigation links
res.json({
  data: users,
  pagination: { page, total },
  _links: {
    self: `/api/users?page=${page}`,
    next: page < totalPages ? `/api/users?page=${page + 1}` : null,
    prev: page > 1 ? `/api/users?page=${page - 1}` : null
  }
});

```

## Best Practices

1. **Always paginate** - Never return unbounded results

2. **Set maximum limits** - Prevent abuse (e.g., max 100 items)

3. **Include total count** - For UI pagination displays

4. **Provide navigation links** - HATEOAS-style next/prev

5. **Use consistent defaults** - Page 1, limit 10-20

6. **Validate inputs** - Handle invalid page/limit values

7. **Document pagination** - Clear API documentation

8. **Consider cursor for large datasets** - More efficient than offset

9. **Cache pagination metadata** - Total counts can be cached
10. **Support filtering** - Combine with pagination

## Performance Considerations

- **Offset pagination** - Can be slow for large offsets (OFFSET 100000)
- **Cursor pagination** - More efficient for large datasets
- **Database indexes** - Essential for pagination performance
- **Count queries** - Can be expensive; consider caching
- **Partial responses** - Use field selection to reduce payload

## Interview Questions

### Beginner (5)

1. **What is pagination?** - Dividing large datasets into smaller chunks for efficient retrieval.

2. **Why do we need pagination?** - Reduce memory usage, improve performance, better user experience.

3. **What is the difference between page and limit?** - Page: which page to retrieve; Limit: items per page.

4. **What is offset-based pagination?** - Skip N records (offset) and return M records (limit).

5. **When should you use pagination?** - Whenever a collection could contain more items than can be efficiently returned.

### Intermediate (5)

6. **Explain cursor-based pagination** - Uses a cursor (usually ID) to fetch next set; more efficient than offset for large datasets.

7. **What are the tradeoffs between offset and cursor?** - Offset: simple, supports random access; Cursor: efficient, stable under changes.

8. **How do you calculate total pages?** - `Math.ceil(total / limit)`.

9. **How do you handle sorting with pagination?** - Apply sort before pagination, ensure consistent ordering.

10. **What is infinite scroll?** - UI pattern that loads more content as user scrolls; uses cursor pagination.

### Senior (10)

11. **Design pagination for a search engine** - Cursors, relevance scoring, facet counts, deep pagination.

12. **How do you handle pagination in distributed systems?** - Consistent cursors, conflict resolution, eventual consistency.

13. **Design cursor-based pagination with complex sorts** - Multi-field cursors, composite keys, tie-breaking.

14. **How do you cache pagination results?** - Cache keys with page/cursor, invalidation strategies.

15. **Design pagination for real-time data** - Stable cursors, handling insertions/deletions during pagination.

16. **How do you handle pagination with filters?** - Dynamic cursors based on filter state, filter-aware pagination.

17. **Design pagination for GraphQL connections** - Edge/cursor pattern, page info, connections.

18. **How do you optimize count queries?** - Estimated counts, cached counts, async updates.

19. **Design pagination for admin dashboards** - Large page sizes, export functionality, real-time updates.

20. **How do you handle pagination in microservices?** - Aggregated pagination, service-level pagination, API gateway.

### FAANG-style (5)

21. **Design pagination for a social network feed** - Real-time updates, ranking, cursor stability.

22. **Design pagination for e-commerce product search** - Faceted search, infinite scroll, preloading.

23. **Design pagination for a messaging system** - Message ordering, read receipts, unread counts.

24. **How would you migrate from offset to cursor pagination?** - Backward compatibility, gradual migration.

25. **Design pagination analytics system** - Track usage patterns, optimize page sizes, detect abuse.

### Follow-ups (5)

26. **What is the N+1 problem in pagination?** - Executing N queries for N items; solve with eager loading.

27. **How do you handle pagination with soft deletes?** - Exclude deleted records from counts and results.

28. **What is deep pagination?** - Requesting very high page numbers; inefficient with offset, fine with cursor.

29. **How do you handle concurrent modifications during pagination?** - Stable cursors, snapshot isolation.

30. **What is the default page size?** - Typically 10-20 items; depends on use case and screen size.

## Summary

Pagination is essential for efficient API design. Offset-based pagination is simple but can be inefficient for large datasets. Cursor-based pagination is more performant for large datasets and real-time data. Always include pagination metadata, navigation links, and validate inputs. Choose the pagination strategy based on your data size, access patterns, and consistency requirements.

## Cheat Sheet

| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| Offset | Small datasets, random access | Simple, supports page jumping | Slow for large offsets |
| Cursor | Large datasets, real-time | Efficient, stable | No random access |
| Keyset | Time-series data | Efficient, natural ordering | Complex implementation |
| Infinite Scroll | Mobile, social feeds | Good UX, lazy loading | No direct URL access |

## References & Learn More

- [Cursor Pagination - Prisma Docs](https://www.prisma.io/docs/concepts/components/prisma-client/pagination)
- [Zalando RESTful API Guidelines - Pagination](https://opensource.zalando.com/restful-api-guidelines/#pagination)
- [How to Design Pagination APIs - Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#pagination)
- [Efficient Pagination with Cursor - Brandur Leach](https://brandur.org/articles/mysql-pagination)
- [GraphQL Cursor Connections Specification](https://relay.dev/graphql/connections.htm)
