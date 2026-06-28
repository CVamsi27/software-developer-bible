# API Versioning

## Definition

API versioning is the practice of managing changes to an API by creating multiple versions that can coexist. It allows API providers to evolve their APIs without breaking existing clients, enabling backward compatibility while introducing new features or modifying existing behavior.

## Why Do We Need It?

As APIs evolve, changes can break existing client integrations:

1. **Backward compatibility** - Existing clients continue to work

2. **Gradual migration** - Clients can upgrade at their own pace

3. **Deprecation management** - Old versions can be retired gracefully

4. **Feature introduction** - New features can be added incrementally

5. **Contract stability** - Clients have predictable behavior

## How It Works

### Versioning Strategies

```text
API Versioning Strategies
═════════════════════════

1. URL Path Versioning
   GET /api/v1/users
   GET /api/v2/users

2. Query Parameter Versioning
   GET /api/users?version=1
   GET /api/users?version=2

3. Header Versioning
   GET /api/users
   Accept: application/vnd.myapi.v1+json

4. Content Negotiation (Media Type)
   GET /api/users
   Accept: application/json; version=1

```

### Strategy 1: URL Path Versioning

```text
URL Path Versioning
═══════════════════

Client                    API Gateway                 Services
  │                           │                         │
  │  GET /api/v1/users        │                         │
  │──────────────────────────►│                         │
  │                           │  Route to v1 service    │
  │                           │────────────────────────►│
  │                           │                         │
  │  GET /api/v2/users        │                         │
  │──────────────────────────►│                         │
  │                           │  Route to v2 service    │
  │                           │────────────────────────►│

```

```typescript
// Express.js implementation
import express from 'express';

const app = express();

// V1 Router
const v1Router = express.Router();

v1Router.get('/users', async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

v1Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  res.json({ data: user });
});

// V2 Router (with changes)
const v2Router = express.Router();

v2Router.get('/users', async (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const users = await UserService.findAll({ page, limit });
  const total = await UserService.count();

  // V2 includes pagination metadata
  res.json({
    data: users,
    pagination: {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      total,
      pages: Math.ceil(total / limit)
    }
  });
});

v2Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  // V2 includes HATEOAS links
  res.json({
    data: user,
    _links: {
      self: `/api/v2/users/${user.id}`,
      posts: `/api/v2/users/${user.id}/posts`
    }
  });
});

// Mount versioned routers
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

```

### Strategy 2: Query Parameter Versioning

```typescript
// Query parameter approach
app.get('/api/users', (req, res) => {
  const version = parseInt(req.query.version as string) || 1;

  if (version === 1) {
    // V1 response format
    const users = await UserService.findAll();
    res.json({ data: users });
  } else if (version === 2) {
    // V2 response format
    const users = await UserService.findAll();
    const total = await UserService.count();
    res.json({
      data: users,
      pagination: { total }
    });
  } else {
    res.status(400).json({ error: 'Invalid version' });
  }
});

```

### Strategy 3: Header Versioning

```typescript
// Custom header approach
app.get('/api/users', (req, res) => {
  const version = req.headers['api-version'] || '1';

  // Route based on header
  switch (version) {
    case '1':
      return handleV1Users(req, res);
    case '2':
      return handleV2Users(req, res);
    default:
      return res.status(400).json({ error: 'Invalid API version' });
  }
});

// Content negotiation approach
app.get('/api/users', (req, res) => {
  const accept = req.headers.accept || 'application/json';

  // Parse version from Accept header
  // Accept: application/vnd.myapi.v2+json
  const match = accept.match(/vnd\.myapi\.v(\d+)\+json/);
  const version = match ? parseInt(match[1]) : 1;

  if (version === 1) {
    return handleV1Users(req, res);
  } else if (version === 2) {
    return handleV2Users(req, res);
  }

  res.status(406).json({ error: 'Not Acceptable' });
});

```

### Strategy 4: Media Type Versioning

```typescript
// Media type with version parameter
app.get('/api/users', (req, res) => {
  const accept = req.headers.accept || 'application/json';

  // Parse: application/json; version=2
  const match = accept.match(/version=(\d+)/);
  const version = match ? parseInt(match[1]) : 1;

  // Set response Content-Type with version
  res.set('Content-Type', `application/json; version=${version}`);

  if (version === 1) {
    return handleV1Users(req, res);
  } else if (version === 2) {
    return handleV2Users(req, res);
  }
});

```

### Deprecation Management

```typescript
// Deprecation middleware
const deprecationMiddleware = (req, res, next) => {
  const version = getVersionFromRequest(req);

  if (version === '1') {
    res.set({
      'Deprecation': 'true',
      'Sunset': '2024-12-31',
      'Link': '</api/v2/docs>; rel="successor-version"'
    });
  }

  next();
};

// Warning header for deprecated versions
app.use('/api/v1', deprecationMiddleware, v1Router);

```

### Version Migration Strategy

```text
Version Migration Flow
══════════════════════

Phase 1: Support Both Versions
────────────────────────────────
  GET /api/v1/users  ──────► V1 Response
  GET /api/v2/users  ──────► V2 Response

Phase 2: Deprecate V1
────────────────────────────
  GET /api/v1/users  ──────► V1 Response + Deprecation Headers
  GET /api/v2/users  ──────► V2 Response

Phase 3: Remove V1
────────────────────────────
  GET /api/v1/users  ──────► 404 Not Found
  GET /api/v2/users  ──────► V2 Response

```

## Code Examples

### Complete Versioning System

```typescript
import express, { Request, Response, NextFunction } from 'express';

// Version detection middleware
function detectVersion(req: Request): string {
  // Priority: URL path > Query param > Header > Media type

  // 1. Check URL path (/api/v1/ or /api/v2/)
  const pathMatch = req.path.match(/^\/api\/v(\d+)\//);
  if (pathMatch) return pathMatch[1];

  // 2. Check query parameter
  if (req.query.version) return req.query.version as string;

  // 3. Check custom header
  if (req.headers['api-version']) return req.headers['api-version'] as string;

  // 4. Check Accept header media type
  const accept = req.headers.accept || '';
  const mediaMatch = accept.match(/vnd\.api\.v(\d+)\+json/);
  if (mediaMatch) return mediaMatch[1];

  return '1'; // Default version
}

// Version-aware router
class VersionedRouter {
  private versions: Map<string, express.Router> = new Map();

  addVersion(version: string, router: express.Router) {
    this.versions.set(version, router);
  }

  handle(req: Request, res: Response, next: NextFunction) {
    const version = detectVersion(req);
    const router = this.versions.get(version);

    if (!router) {
      return res.status(400).json({
        error: 'Unsupported API version',
        supportedVersions: Array.from(this.versions.keys())
      });
    }

    // Add version to request for handlers
    req.apiVersion = version;

    return router(req, res, next);
  }
}

// V1 Implementation
const v1Router = express.Router();

v1Router.get('/users', async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

v1Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json({ data: user });
});

v1Router.post('/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201).json({ data: user });
});

// V2 Implementation (enhanced)
const v2Router = express.Router();

v2Router.get('/users', async (req, res) => {
  const { page = 1, limit = 10, sort = 'createdAt' } = req.query;
  const users = await UserService.findAll({ page, limit, sort });
  const total = await UserService.count();

  res.json({
    data: users,
    pagination: {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      total,
      pages: Math.ceil(total / limit)
    },
    _links: {
      self: `/api/v2/users?page=${page}&limit=${limit}`,
      next: parseInt(page as string) < Math.ceil(total / parseInt(limit as string))
        ? `/api/v2/users?page=${parseInt(page as string) + 1}&limit=${limit}`
        : null
    }
  });
});

v2Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });

  res.json({
    data: user,
    _links: {
      self: `/api/v2/users/${user.id}`,
      posts: `/api/v2/users/${user.id}/posts`
    }
  });
});

v2Router.post('/users', async (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(422).json({
      error: 'Validation failed',
      details: {
        ...(!name && { name: 'Required' }),
        ...(!email && { email: 'Required' })
      }
    });
  }

  const user = await UserService.create({ name, email });
  res.status(201)
    .header('Location', `/api/v2/users/${user.id}`)
    .json({ data: user });
});

// Setup versioned routing
const versionedRouter = new VersionedRouter();
versionedRouter.addVersion('1', v1Router);
versionedRouter.addVersion('2', v2Router);

app.use('/api', versionedRouter.handle.bind(versionedRouter));

```

### Deprecation Handler

```typescript
// Deprecation configuration
const deprecationConfig = {
  '1': {
    deprecated: true,
    sunset: new Date('2024-12-31'),
    successor: '2'
  }
};

// Deprecation middleware
app.use('/api', (req: Request, res: Response, next: NextFunction) => {
  const version = detectVersion(req);
  const config = deprecationConfig[version];

  if (config?.deprecated) {
    res.set({
      'Deprecation': 'true',
      'Sunset': config.sunset.toUTCString(),
      'Link': `</api/v${config.successor}/docs>; rel="successor-version"`,
      'Warning': `299 - "API version ${version} is deprecated. Use version ${config.successor} instead."`
    });
  }

  next();
});

```

### URL Rewriting for Migration

```typescript
// Redirect old URLs to new versions
app.get('/api/users', (req, res) => {
  // Redirect to current version
  res.redirect(301, '/api/v2/users');
});

app.get('/api/users/:id', (req, res) => {
  res.redirect(301, `/api/v2/users/${req.params.id}`);
});

// Or use middleware to rewrite
app.use('/api/users', (req, res, next) => {
  // Rewrite URL to include version
  req.url = `/api/v2${req.url}`;
  next();
});

```

## Real-World Use Cases

### 1. E-commerce API Evolution

```typescript
// V1: Basic product listing
v1Router.get('/products', async (req, res) => {
  const products = await ProductService.findAll();
  res.json({ data: products });
});

// V2: Added filtering and pagination
v2Router.get('/products', async (req, res) => {
  const { category, minPrice, maxPrice, page, limit } = req.query;
  const products = await ProductService.findAll({
    category,
    minPrice: minPrice ? parseFloat(minPrice as string) : undefined,
    maxPrice: maxPrice ? parseFloat(maxPrice as string) : undefined,
    page: parseInt(page as string) || 1,
    limit: parseInt(limit as string) || 10
  });
  res.json({ data: products, pagination: { page, limit } });
});

// V3: Added search and recommendations
v3Router.get('/products', async (req, res) => {
  const { q, ...filters } = req.query;
  let products;

  if (q) {
    products = await ProductService.search(q as string, filters);
  } else {
    products = await ProductService.findAll(filters);
  }

  // Add recommendations
  const recommendations = await RecommendationService.getForProducts(
    products.map(p => p.id)
  );

  res.json({
    data: products,
    recommendations,
    pagination: calculatePagination(req.query)
  });
});

```

### 2. Authentication System Migration

```typescript
// V1: Basic token auth
v1Router.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await UserService.authenticate(email, password);
  const token = generateToken(user);
  res.json({ token });
});

// V2: Added refresh tokens and scopes
v2Router.post('/auth/login', async (req, res) => {
  const { email, password, scope } = req.body;
  const user = await UserService.authenticate(email, password);
  const accessToken = generateAccessToken(user, scope);
  const refreshToken = await generateRefreshToken(user);

  res.json({
    access_token: accessToken,
    refresh_token: refreshToken,
    token_type: 'Bearer',
    expires_in: 3600
  });
});

// V3: Added OAuth2 support
v3Router.post('/auth/token', async (req, res) => {
  const { grant_type, ...params } = req.body;

  switch (grant_type) {
    case 'authorization_code':
      return handleAuthorizationCode(req, res);
    case 'refresh_token':
      return handleRefreshToken(req, res);
    case 'client_credentials':
      return handleClientCredentials(req, res);
    default:
      return res.status(400).json({ error: 'unsupported_grant_type' });
  }
});

```

### 3. Webhook System Evolution

```typescript
// V1: Basic webhooks
v1Router.post('/webhooks', async (req, res) => {
  const webhook = await WebhookService.create(req.body);
  res.status(201).json({ data: webhook });
});

// V2: Added retry logic and event filtering
v2Router.post('/webhooks', async (req, res) => {
  const { url, events, secret } = req.body;
  const webhook = await WebhookService.create({
    url,
    events,
    secret,
    retryPolicy: { maxRetries: 3, backoff: 'exponential' }
  });
  res.status(201).json({ data: webhook });
});

// V3: Added webhook management and testing
v3Router.post('/webhooks', async (req, res) => {
  const webhook = await WebhookService.create({
    ...req.body,
    status: 'active',
    metadata: { createdBy: req.user.id }
  });

  // Send test event
  await WebhookService.sendTestEvent(webhook.id);

  res.status(201).json({ data: webhook });
});

v3Router.post('/webhooks/:id/test', async (req, res) => {
  const result = await WebhookService.sendTestEvent(req.params.id);
  res.json({ data: result });
});

```

## Common Mistakes

### 1. Breaking Changes Without Versioning

```typescript
// ❌ Bad: Changed response format without versioning
// Old: { "name": "John" }
// New: { "fullName": "John Doe" }

// ✅ Good: New version with backward compatibility
v2Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  res.json({
    data: {
      id: user.id,
      name: user.name,      // Keep for backward compatibility
      fullName: user.fullName // Add new field
    }
  });
});

```

### 2. Using Headers Only

```typescript
// ❌ Bad: Only header versioning (hard to test/debug)
app.get('/api/users', (req, res) => {
  const version = req.headers['api-version'];
  // Hard to test with curl/browser
});

// ✅ Good: Support multiple strategies
app.get('/api/v1/users', ...);  // URL path (easy to test)
app.get('/api/users', (req, res) => {
  const version = req.headers['api-version'] || '1';  // Fallback to header
});

```

### 3. Not Deprecating Gracefully

```typescript
// ❌ Bad: Immediate removal
app.delete('/api/v1/users', (req, res) => {
  res.status(404).json({ error: 'API v1 removed' });
});

// ✅ Good: Deprecation period with warnings
app.use('/api/v1', (req, res, next) => {
  res.set({
    'Deprecation': 'true',
    'Sunset': '2024-12-31',
    'Link': '</api/v2/docs>; rel="successor-version"'
  });
  next();
});

```

### 4. Versioning Every Small Change

```typescript
// ❌ Bad: New version for minor changes
// V1: GET /api/v1/users
// V2: GET /api/v2/users (added one field)

// ✅ Good: Only version for breaking changes
// Keep V1, add field to V1 response (non-breaking)
v1Router.get('/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  res.json({
    data: user,
    // New field doesn't break existing clients
    metadata: { createdAt: user.createdAt }
  });
});

```

### 5. Not Documenting Versions

```typescript
// ❌ Bad: No version documentation
// ✅ Good: Clear documentation
app.get('/api/docs', (req, res) => {
  res.json({
    versions: {
      v1: { status: 'deprecated', sunset: '2024-12-31', docs: '/api/v1/docs' },
      v2: { status: 'current', docs: '/api/v2/docs' }
    }
  });
});

```

## Best Practices

1. **Use URL path versioning** - Most visible and easiest to test

2. **Version only breaking changes** - Non-breaking changes don't need versions

3. **Deprecate gracefully** - Provide Sunset dates and migration guides

4. **Support multiple versions** - But limit to 2-3 active versions

5. **Document all versions** - Clear API documentation for each version

6. **Use semantic versioning** - Major.Minor.Patch format

7. **Add deprecation headers** - Inform clients about upcoming removals

8. **Provide migration guides** - Help clients upgrade between versions

9. **Monitor version usage** - Track which versions are being used
10. **Automate version management** - Use middleware and configuration

## Performance Considerations

- **Caching** - Version-specific cache keys to avoid conflicts
- **CDN routing** - Route cached responses by version
- **Database migrations** - Handle schema changes across versions
- **Monitoring** - Track performance per version
- **Load testing** - Test each version independently

## Interview Questions

### Beginner (5)

1. **What is API versioning?** - Managing changes to APIs by creating multiple versions that coexist.

2. **Why do we need API versioning?** - Maintain backward compatibility while evolving APIs.

3. **What are the main versioning strategies?** - URL path, query parameter, header, and media type versioning.

4. **Which versioning strategy is most common?** - URL path versioning (`/api/v1/users`).

5. **What is a breaking change?** - A change that breaks existing client integrations.

### Intermediate (5)

6. **When should you create a new version?** - Only for breaking changes; non-breaking additions can be added to existing versions.

7. **How do you handle deprecation?** - Add Deprecation and Sunset headers, provide migration timeline and guides.

8. **What is semantic versioning?** - Major.Minor.Patch format; increment major for breaking changes.

9. **How do you route requests to different versions?** - Use middleware to detect version and route to appropriate handler.

10. **How do you handle version conflicts?** - Clear version precedence rules, fallback to default version.

### Senior (10)

11. **Design a version migration strategy** - Phased approach: support both, deprecate old, remove old.

12. **How do you handle database migrations across versions?** - Schema versioning, backward-compatible migrations, feature flags.

13. **Design a version-aware caching system** - Version-specific cache keys, invalidation strategies per version.

14. **How do you monitor API version usage?** - Track version in logs, dashboard for version adoption metrics.

15. **Design webhook versioning** - Version in webhook URL or payload, migration support.

16. **How do you handle versioning in microservices?** - Service-level versioning, API gateway routing, contract testing.

17. **Design a version rollback system** - Blue-green deployments, feature flags, instant rollback capability.

18. **How do you handle versioning for GraphQL?** - Schema evolution, deprecation directives, version field.

19. **Design a version-aware rate limiter** - Different limits per version, upgrade incentives.

20. **How do you test multiple versions?** - Contract testing, version-specific test suites, compatibility testing.

### FAANG-style (5)

21. **Design API versioning for a global platform** - Regional version support, A/B testing, gradual rollout.

22. **How do you handle versioning for real-time APIs?** - WebSocket versioning, protocol evolution, backward compatibility.

23. **Design a version migration automation system** - Automated code generation, compatibility checking, migration scripts.

24. **How do you handle versioning for API marketplaces?** - Version discovery, pricing per version, usage analytics.

25. **Design a zero-downtime version migration** - Traffic splitting, shadow testing, automatic client upgrades.

### Follow-ups (5)

26. **What are the tradeoffs of each versioning strategy?** - URL path: visible but pollutes URLs; Header: clean URLs but harder to test.

27. **How do you handle versioning for mobile apps?** - Bundle API version with app, support old versions, force upgrades.

28. **What is the maximum number of versions to support?** - Typically 2-3; depends on resources and adoption rates.

29. **How do you handle versioning for third-party integrations?** - Long deprecation periods, version discovery, migration support.

30. **How do you communicate version changes?** - Changelog, email notifications, dashboard alerts, developer portal.

## Summary

API versioning is essential for evolving APIs without breaking existing clients. URL path versioning is the most common and recommended approach. Always version only breaking changes, deprecate gracefully with clear timelines, and provide migration guides. Monitor version usage and retire old versions when adoption drops.

## Cheat Sheet

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL Path | `/api/v1/users` | Visible, easy to test | URL pollution |
| Query Param | `?version=1` | Easy to implement | Not RESTful |
| Header | `Accept: vnd.api.v1+json` | Clean URLs | Hard to test |
| Media Type | `application/json; v=1` | RESTful | Complex parsing |

## References & Learn More

- [Microsoft REST API Guidelines - Versioning](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7-versioning)
- [Zalando RESTful API Guidelines - API Evolution](https://opensource.zalando.com/restful-api-guidelines/#api-evolution)
- [Stripe API Versioning Strategy](https://stripe.com/blog/api-versioning)
- [API Versioning Best Practices - SmartBear](https://smartbear.com/blog/which-api-versioning-strategy/)
- [GitHub REST API - Versioning](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
