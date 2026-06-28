# CORS (Cross-Origin Resource Sharing)

## Definition

CORS (Cross-Origin Resource Sharing) is a security mechanism implemented in web browsers that restricts how web pages from one origin can request resources from a different origin. It allows servers to specify who can access their resources and how, using HTTP headers.

## Why Do We Need It?

Without CORS:

1. **Security risks** - Malicious sites could access sensitive data from other origins
2. **API limitations** - Legitimate cross-origin requests would be blocked
3. **Development issues** - Frontend and backend on different origins can't communicate
4. **Third-party integrations** - External services can't access your API
5. **Microservices** - Services on different domains can't communicate

## How It Works

### Same-Origin Policy

```
Same-Origin Policy
══════════════════

Origin = Protocol + Domain + Port

Same Origin:
  https://api.example.com  ✅ Same as itself
  https://api.example.com:443  ✅ Same (443 is default for HTTPS)

Different Origins:
  https://api.example.com  vs  http://api.example.com  ❌ (different protocol)
  https://api.example.com  vs  https://www.example.com  ❌ (different domain)
  https://api.example.com  vs  https://api.example.com:8080  ❌ (different port)
  https://api.example.com  vs  https://api.other.com  ❌ (different domain)
```

### CORS Request Flow

```
CORS Preflight Request
══════════════════════

Browser                          Server
  │                               │
  │  OPTIONS /api/data            │
  │  Origin: https://app.com     │
  │  Access-Control-Request-Method: POST
  │  Access-Control-Request-Headers: Content-Type, Authorization
  │──────────────────────────────►│
  │                               │
  │  204 No Content               │
  │  Access-Control-Allow-Origin: https://app.com
  │  Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  │  Access-Control-Allow-Headers: Content-Type, Authorization
  │  Access-Control-Max-Age: 86400
  │◄──────────────────────────────│
  │                               │
  │  POST /api/data               │
  │  Origin: https://app.com     │
  │  Content-Type: application/json
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  Access-Control-Allow-Origin: https://app.com
  │◄──────────────────────────────│
```

### CORS Headers

```
CORS Response Headers
═════════════════════

Access-Control-Allow-Origin: https://app.com
  - Which origins can access the resource
  - Can be * for public APIs or specific origin

Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  - Which HTTP methods are allowed

Access-Control-Allow-Headers: Content-Type, Authorization
  - Which headers can be sent in request

Access-Control-Allow-Credentials: true
  - Whether cookies/credentials can be sent

Access-Control-Expose-Headers: X-Custom-Header
  - Which headers can be read by JavaScript

Access-Control-Max-Age: 86400
  - How long preflight response can be cached (seconds)

Access-Control-Max-Age: 86400
  - How long preflight can be cached (seconds)
```

```typescript
// CORS middleware implementation
import cors from 'cors';

// Basic CORS
app.use(cors());

// CORS with options
const corsOptions = {
  origin: 'https://app.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400
};

app.use(cors(corsOptions));

// Dynamic origin
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = ['https://app.com', 'https://admin.com'];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));

// Per-route CORS
app.get('/api/public', cors(), (req, res) => {
  res.json({ data: 'public data' });
});

app.get('/api/private', cors({ origin: 'https://app.com' }), (req, res) => {
  res.json({ data: 'private data' });
});
```

### Preflight Requests

```
Preflight Request Requirements
══════════════════════════════

Browser sends preflight when:
  1. Method is not GET, HEAD, or POST
  2. POST with Content-Type other than:
     - application/x-www-form-urlencoded
     - multipart/form-data
     - text/plain
  3. Custom headers are sent (e.g., Authorization)
  4. Credentials are included

Example preflight:
OPTIONS /api/data HTTP/1.1
Host: api.example.com
Origin: https://app.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Content-Type, Authorization
```

```typescript
// Handle preflight requests
app.options('/api/data', cors());

// Or manually
app.options('/api/data', (req, res) => {
  res.set({
    'Access-Control-Allow-Origin': 'https://app.com',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
  });
  res.status(204).end();
});

// With credentials
app.use(cors({
  origin: 'https://app.com',
  credentials: true
}));
```

## Code Examples

### Complete CORS Implementation

```typescript
import express from 'express';
import cors from 'cors';

const app = express();

// CORS configuration
const corsConfig = {
  origin: function (origin, callback) {
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com',
      'http://localhost:3000' // Development
    ];

    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);

    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'X-Idempotency-Key'],
  exposedHeaders: ['X-Total-Count', 'X-Page-Count', 'Link'],
  credentials: true,
  preflightContinue: false,
  optionsSuccessStatus: 204,
  maxAge: 86400 // 24 hours
};

// Apply CORS globally
app.use(cors(corsConfig));

// Handle preflight for all routes
app.options('*', cors(corsConfig));

// Or specific routes
app.get('/api/public', cors({ origin: '*' }), (req, res) => {
  res.json({ data: 'public' });
});

app.get('/api/private', cors(corsConfig), (req, res) => {
  res.json({ data: 'private' });
});

// Custom CORS headers
app.use('/api', (req, res, next) => {
  const origin = req.headers.origin;

  if (isAllowedOrigin(origin)) {
    res.set('Access-Control-Allow-Origin', origin);
    res.set('Access-Control-Allow-Credentials', 'true');
  }

  next();
});

// CORS error handler
app.use((err, req, res, next) => {
  if (err.message === 'Not allowed by CORS') {
    return res.status(403).json({
      error: 'CORS Error',
      message: 'Origin not allowed'
    });
  }
  next(err);
});
```

### CORS for Microservices

```typescript
// API Gateway CORS handling
const gatewayCors = {
  origin: function (origin, callback) {
    // Allow all internal service origins
    if (origin && origin.endsWith('.internal')) {
      callback(null, true);
    }
    // Allow external origins from whitelist
    else if (isExternalAllowedOrigin(origin)) {
      callback(null, true);
    }
    else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
};

app.use(cors(gatewayCors));

// Service-specific CORS
app.use('/api/users', cors({
  origin: ['https://app.com', 'https://admin.com'],
  methods: ['GET', 'POST', 'PUT'],
  allowedHeaders: ['Authorization', 'Content-Type']
}));

app.use('/api/public', cors({
  origin: '*',
  methods: ['GET'],
  allowedHeaders: []
}));
```

### CORS with Credentials

```typescript
// CORS with credentials (cookies, authorization headers)
app.use(cors({
  origin: 'https://app.com',
  credentials: true
}));

// Client must include credentials
fetch('https://api.example.com/data', {
  method: 'GET',
  credentials: 'include', // Important for cookies
  headers: {
    'Authorization': 'Bearer token'
  }
});

// Axios with credentials
axios.get('https://api.example.com/data', {
  withCredentials: true,
  headers: {
    'Authorization': 'Bearer token'
  }
});
```

### Dynamic CORS Configuration

```typescript
// Dynamic CORS based on request
app.use((req, res, next) => {
  const origin = req.headers.origin;
  const path = req.path;

  // Different CORS for different endpoints
  if (path.startsWith('/api/public')) {
    res.set('Access-Control-Allow-Origin', '*');
  } else if (path.startsWith('/api/admin')) {
    if (origin === 'https://admin.example.com') {
      res.set('Access-Control-Allow-Origin', origin);
      res.set('Access-Control-Allow-Credentials', 'true');
    }
  } else if (path.startsWith('/api')) {
    if (isAllowedOrigin(origin)) {
      res.set('Access-Control-Allow-Origin', origin);
      res.set('Access-Control-Allow-Credentials', 'true');
    }
  }

  next();
});
```

## Real-World Use Cases

### 1. Single Page Application (SPA)

```typescript
// SPA frontend on different domain than API
app.use(cors({
  origin: 'https://app.example.com',
  credentials: true,
  allowedHeaders: ['Authorization', 'Content-Type', 'X-Request-ID']
}));

// Handle preflight
app.options('/api/*', cors());
```

### 2. Third-Party API Access

```typescript
// Public API with CORS for third-party developers
app.use(cors({
  origin: '*', // Public API
  methods: ['GET'],
  allowedHeaders: ['Authorization', 'X-API-Key']
}));

// Private endpoints without CORS
app.use('/api/internal', (req, res, next) => {
  const origin = req.headers.origin;
  if (!origin || !isTrustedOrigin(origin)) {
    return res.status(403).json({ error: 'CORS not allowed' });
  }
  next();
});
```

### 3. Mobile App Backend

```typescript
// Mobile apps don't send Origin header
app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);

    // Allow web app origins
    if (isWebAppOrigin(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
```

### 4. Development Environment

```typescript
// Allow all origins in development
if (process.env.NODE_ENV === 'development') {
  app.use(cors({
    origin: true,
    credentials: true
  }));
} else {
  app.use(cors(corsConfig));
}
```

## Common Mistakes

### 1. Using Wildcard Origin with Credentials

```typescript
// ❌ Bad: Can't use * with credentials
app.use(cors({
  origin: '*',
  credentials: true
}));

// ✅ Good: Specify allowed origins
app.use(cors({
  origin: ['https://app.com', 'https://admin.com'],
  credentials: true
}));
```

### 2. Not Handling Preflight Requests

```typescript
// ❌ Bad: No preflight handling
app.put('/api/data', (req, res) => {
  res.json({ data: 'updated' });
});

// ✅ Good: Handle preflight
app.options('/api/data', cors());
app.put('/api/data', (req, res) => {
  res.json({ data: 'updated' });
});
```

### 3. Not Including Required Headers

```typescript
// ❌ Bad: Missing allowed headers
app.use(cors({
  origin: 'https://app.com',
  allowedHeaders: ['Content-Type']
}));

// ✅ Good: Include all needed headers
app.use(cors({
  origin: 'https://app.com',
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));
```

### 4. Not Setting Max-Age

```typescript
// ❌ Bad: No preflight caching
app.use(cors({
  origin: 'https://app.com'
}));

// ✅ Good: Cache preflight
app.use(cors({
  origin: 'https://app.com',
  maxAge: 86400 // 24 hours
}));
```

### 5. Exposing Wrong Headers

```typescript
// ❌ Bad: Not exposing custom headers
app.use(cors({
  origin: 'https://app.com'
}));

// ✅ Good: Expose custom headers
app.use(cors({
  origin: 'https://app.com',
  exposedHeaders: ['X-Total-Count', 'X-Page-Count', 'Link']
}));
```

## Best Practices

1. **Never use wildcard with credentials** - Specify allowed origins
2. **Handle preflight requests** - OPTIONS endpoint for all routes
3. **Set maxAge** - Cache preflight for 24 hours
4. **Expose custom headers** - Let JavaScript read them
5. **Validate origin** - Check against whitelist
6. **Use HTTPS** - CORS over HTTP is insecure
7. **Document CORS** - Clear API documentation
8. **Test CORS** - Verify in browser developer tools
9. **Monitor CORS errors** - Track blocked requests
10. **Consider CSP** - Content Security Policy for additional security

## Performance Considerations

- **Preflight caching** - Use maxAge to reduce preflight requests
- **CDN caching** - Cache CORS headers at CDN level
- **Minimal headers** - Only include necessary headers
- **Avoid wildcard** - More processing for origin validation
- **Async origin checking** - Don't block on origin validation

## Interview Questions

### Beginner (5)

1. **What is CORS?** - Cross-Origin Resource Sharing; a security mechanism for cross-origin HTTP requests.

2. **Why do we need CORS?** - Browsers block cross-origin requests by default for security.

3. **What is a preflight request?** - OPTIONS request sent by browser to check if cross-origin request is allowed.

4. **What headers are used for CORS?** - Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers.

5. **What is the difference between same-origin and cross-origin?** - Same-origin: same protocol, domain, port; Cross-origin: different in any.

### Intermediate (5)

6. **When is a preflight request sent?** - For non-simple requests (PUT, DELETE, custom headers, credentials).

7. **What is Access-Control-Allow-Credentials?** - Header indicating if cookies/credentials can be sent.

8. **How do you handle CORS in Node.js?** - Use cors middleware or manual header setting.

9. **What is the maxAge header?** - How long preflight response can be cached (seconds).

10. **How do you expose custom headers to JavaScript?** - Use Access-Control-Expose-Headers header.

### Senior (10)

11. **Design CORS for a multi-tenant API** - Dynamic origin validation, tenant-specific rules.

12. **How do you handle CORS in microservices?** - API gateway handles CORS, services trust internal requests.

13. **Design CORS with authentication** - Credentials handling, secure cookie settings.

14. **How do you debug CORS issues?** - Browser dev tools, check preflight response, verify headers.

15. **Design CORS for WebSocket connections** - Origin validation during upgrade handshake.

16. **How do you handle CORS in serverless functions?** - Middleware, environment-based configuration.

17. **Design CORS for file uploads** - Expose progress headers, handle large payloads.

18. **How do you handle CORS with GraphQL?** - OPTIONS handling, custom headers for queries.

19. **Design CORS monitoring and analytics** - Track blocked requests, origin statistics.

20. **How do you handle CORS during incidents?** - Graceful degradation, fallback origins.

### FAANG-style (5)

21. **Design CORS for a global platform** - Regional origins, latency considerations, edge caching.

22. **How would you implement CORS for a service mesh?** - Sidecar proxy handling, distributed CORS.

23. **Design CORS with zero-trust security** - Verify every request, no implicit trust.

24. **How do you handle CORS for real-time applications?** - WebSocket origins, SSE headers.

25. **Design CORS for API marketplaces** - Third-party origins, dynamic whitelisting.

### Follow-ups (5)

26. **What are CORS security risks?** - Misconfigured origins, credential leakage, CSRF attacks.

27. **How does CORS relate to CSRF?** - CORS doesn't prevent CSRF; use CSRF tokens.

28. **Can CORS be bypassed?** - Server-side requests don't have CORS restrictions.

29. **How do you test CORS?** - Browser dev tools, curl, automated tests.

30. **What is the future of CORS?** - Potential changes with WebTransport, HTTP/3.

## Summary

CORS is essential for secure cross-origin communication. Always specify allowed origins instead of using wildcards, handle preflight requests, and set appropriate maxAge for caching. Test CORS thoroughly and monitor for issues. Remember that CORS is a browser mechanism; server-to-server requests don't have CORS restrictions.

## Cheat Sheet

| Header | Purpose | Example |
|--------|---------|---------|
| Access-Control-Allow-Origin | Allowed origins | https://app.com |
| Access-Control-Allow-Methods | Allowed HTTP methods | GET, POST, PUT |
| Access-Control-Allow-Headers | Allowed request headers | Content-Type, Authorization |
| Access-Control-Allow-Credentials | Allow credentials | true |
| Access-Control-Expose-Headers | Headers exposed to JS | X-Total-Count |
| Access-Control-Max-Age | Preflight cache duration | 86400 (24 hours) |
| Access-Control-Request-Method | Requested method (preflight) | PUT |
| Access-Control-Request-Headers | Requested headers (preflight) | Content-Type |

## References & Learn More

- [CORS - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Cross-Origin Resource Sharing (CORS) - W3C](https://www.w3.org/TR/cors/)
- [How to Use CORS in Express.js](https://expressjs.com/en/resources/middleware/cors.html)
- [CORS - A Practical Guide - DigitalOcean](https://www.digitalocean.com/community/tutorials/an-introduction-to-cors)
- [Can I Use CORS?](https://caniuse.com/cors)
