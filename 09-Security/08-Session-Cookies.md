---
section: Security
category: Architecture
tags: [concept]
---

# Sessions and Cookies

## Definition

**Sessions** are server-side storage mechanisms that maintain user state across multiple HTTP requests. A session stores user data on the server and associates it with a unique session ID sent to the client.

**Cookies** are small pieces of data stored on the client side (browser) that are sent with every HTTP request to the server. They can store session IDs, user preferences, authentication tokens, and other state information.

Sessions and cookies work together: cookies typically store the session ID, while the session data lives on the server. This combination enables stateful interactions in the stateless HTTP protocol.

## Why Do We Need It?

- **State Maintenance**: HTTP is stateless; sessions/cookies maintain user state
- **Authentication**: Keep users logged in across requests
- **Personalization**: Store user preferences and settings
- **Shopping Carts**: Maintain cart contents across page loads
- **CSRF Protection**: Session-based CSRF tokens
- **Analytics**: Track user behavior across sessions

## How It Works

### Session Flow

```text
┌──────────┐                    ┌──────────┐
│  Client  │                    │  Server  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. POST /login               │
     │     {email, password}         │
     │──────────────────────────────>│
     │                               │
     │                    2. Validate credentials
     │                    3. Create session
     │                    4. Generate session ID
     │                    5. Store session data
     │                               │
     │  6. Set-Cookie:               │
     │     sessionId=abc123;         │
     │     HttpOnly; Secure;         │
     │     SameSite=Strict           │
     │<──────────────────────────────│
     │                               │
     │  7. GET /dashboard            │
     │     Cookie: sessionId=abc123  │
     │──────────────────────────────>│
     │                               │
     │                    8. Lookup session
     │                    9. Return user data
     │                               │
     │  10. Response with dashboard  │
     │<──────────────────────────────│

```

### Cookie Attributes

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Cookie Attributes                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Set-Cookie: sessionId=abc123;                                 │
│              Domain=.example.com;                               │
│              Path=/;                                            │
│              Expires=Thu, 01 Jan 2025 00:00:00 GMT;             │
│              Max-Age=3600;                                      │
│              Secure;                                            │
│              HttpOnly;                                          │
│              SameSite=Strict                                    │
│                                                                 │
│  Attributes:                                                    │
│  - Domain: Which domain can access the cookie                   │
│  - Path: Which paths can access the cookie                      │
│  - Expires/Max-Age: When the cookie expires                     │
│  - Secure: Only send over HTTPS                                 │
│  - HttpOnly: Not accessible via JavaScript                      │
│  - SameSite: Control cross-site cookie sending                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### Session vs JWT

```text
┌─────────────────────────────────────────────────────────────────┐
│              Session vs JWT Comparison                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SESSION-BASED:                                                 │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │  Client  │─────>│  Server  │─────>│ Session  │              │
│  │ (Cookie) │      │          │      │  Store   │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│  - Server-side storage                                         │
│  - Session ID in cookie                                        │
│  - Easy to revoke                                              │
│  - Scalability challenge                                       │
│                                                                 │
│  JWT-BASED:                                                     │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │  Client  │─────>│  Server  │─────>│  Token   │              │
│  │ (Token)  │      │          │      │(Self-contained)         │
│  └──────────┘      └──────────┘      └──────────┘              │
│  - Client-side storage                                         │
│  - Self-contained token                                        │
│  - Harder to revoke                                            │
│  - Highly scalable                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Express Session Configuration

```typescript
import express from "express";
import session from "express-session";
import RedisStore from "connect-redis";
import Redis from "ioredis";

const app = express();
const redis = new Redis();

// Redis session store
const redisStore = new RedisStore({
  client: redis,
  prefix: "myapp:sessions:",
});

app.use(
  session({
    store: redisStore,
    secret: process.env.SESSION_SECRET!,
    name: "sessionId",
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === "production", // HTTPS only
      httpOnly: true, // Prevent XSS access
      maxAge: 15 * 60 * 1000, // 15 minutes
      sameSite: "strict", // CSRF protection
      domain: ".example.com",
      path: "/",
    },
  })
);

// Session-based authentication
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await authenticateUser(email, password);

  if (user) {
    req.session.userId = user.id;
    req.session.roles = user.roles;
    res.json({ success: true });
  } else {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

// Protected route
app.get("/profile", (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }
  res.json({ userId: req.session.userId });
});

// Logout
app.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: "Logout failed" });
    }
    res.clearCookie("sessionId");
    res.json({ success: true });
  });
});

```

### Cookie Configuration

```typescript
// Set cookie
app.get("/preferences", (req, res) => {
  res.cookie("theme", "dark", {
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    domain: ".example.com",
    path: "/",
  });

  res.cookie("language", "en", {
    maxAge: 30 * 24 * 60 * 60 * 1000,
    httpOnly: true,
    secure: true,
    sameSite: "strict",
  });

  res.json({ success: true });
});

// Clear cookie
app.post("/clear-preferences", (req, res) => {
  res.clearCookie("theme");
  res.clearCookie("language");
  res.json({ success: true });
});

// Signed cookies
import cookieParser from "cookie-parser";
app.use(cookieParser(process.env.COOKIE_SECRET));

app.get("/signed", (req, res) => {
  res.cookie("signedCookie", "value", {
    signed: true,
    httpOnly: true,
    secure: true,
  });
  res.json({ success: true });
});

```

### Session Store Implementations

```typescript
// PostgreSQL Session Store
import connectPgSimple from "connect-pg-simple";

const pgStore = connectPgSimple(session);

app.use(
  session({
    store: new pgStore({
      conString: process.env.DATABASE_URL,
      tableName: "user_sessions",
      createTableIfMissing: true,
    }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      maxAge: 15 * 60 * 1000,
      sameSite: "strict",
    },
  })
);

// MongoDB Session Store
import MongoStore from "connect-mongo";

app.use(
  session({
    store: MongoStore.create({
      mongoUrl: process.env.MONGODB_URI,
      ttl: 15 * 60, // 15 minutes in seconds
      autoRemove: "native",
    }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      maxAge: 15 * 60 * 1000,
      sameSite: "strict",
    },
  })
);

```

### Session Security Middleware

```typescript
// Session fixation prevention
const preventSessionFixation = (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): void => {
  if (!req.session.userId) {
    // New session - regenerate ID
    req.session.regenerate((err) => {
      if (err) {
        return next(err);
      }
      next();
    });
  } else {
    next();
  }
};

// Session timeout
const sessionTimeout = (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): void => {
  const timeout = 15 * 60 * 1000; // 15 minutes
  const now = Date.now();

  if (req.session.lastAccess) {
    const elapsed = now - req.session.lastAccess;
    if (elapsed > timeout) {
      req.session.destroy(() => {
        res.status(401).json({ error: "Session expired" });
      });
      return;
    }
  }

  req.session.lastAccess = now;
  next();
};

// CSRF token in session
const csrfProtection = (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): void => {
  if (!req.session.csrfToken) {
    req.session.csrfToken = require("crypto").randomBytes(32).toString("hex");
  }
  next();
};

// Use CSRF token
app.post("/transfer", (req, res) => {
  if (req.body._csrf !== req.session.csrfToken) {
    return res.status(403).json({ error: "Invalid CSRF token" });
  }
  // Process transfer
});

```

## Real-World Use Cases

### 1. E-commerce Shopping Carts

- Store cart contents in session
- Persist across page loads
- Handle guest vs authenticated carts

### 2. User Authentication

- Keep users logged in
- Session-based access control
- Automatic logout on inactivity

### 3. Multi-Step Forms

- Store form data across steps
- Prevent data loss on navigation
- Validate each step

### 4. A/B Testing

- Store user variant in cookie
- Consistent experience across requests
- Long-term tracking with cookies

### 5. Language/Theme Preferences

- Store preferences in cookies
- Persist across sessions
- Sync across devices

## Common Mistakes

1. **Not using Secure flag**: Cookies sent over HTTP can be intercepted

2. **Not using HttpOnly**: JavaScript can steal session cookies via XSS

3. **Storing sensitive data in cookies**: Cookies are client-side; don't store secrets

4. **Not regenerating session ID**: Session fixation attacks

5. **Using default session configuration**: Default settings are often insecure

6. **Not implementing session expiration**: Sessions should expire

7. **Storing session data in cookies**: Keep data server-side

8. **Not using SameSite**: Vulnerable to CSRF attacks

## Best Practices

1. **Use Secure flag** on all cookies in production

2. **Use HttpOnly** for session cookies

3. **Set SameSite=Strict** or **Lax** for CSRF protection

4. **Regenerate session ID** after login

5. **Implement session expiration** and timeout

6. **Use secure session stores** (Redis, PostgreSQL)

7. **Encrypt session data** if storing sensitive information

8. **Implement session revocation** for logout

9. **Monitor session activity** for anomalies
10. **Use short session lifetimes** for sensitive applications

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Redis Store | Fast, scalable, supports TTL |
| PostgreSQL Store | Persistent, ACID compliant |
| Cookie Size | Limit to 4KB |
| Session Data | Keep minimal for performance |
| Serialization | Use efficient formats (JSON, MessagePack) |

## Summary

Sessions and cookies are fundamental to maintaining state in web applications. Key takeaways:

- Use httpOnly, Secure, SameSite cookies for session IDs
- Store session data server-side (Redis, PostgreSQL)
- Regenerate session ID after login
- Implement session expiration and timeout
- Use secure session stores in production
- Monitor session activity for anomalies
- Implement session revocation for logout
- Never store sensitive data in cookies

## Cheat Sheet
| Attribute | Recommendation |
|-----------|---------------|
| HttpOnly | Always true for session cookies |
| Secure | Always true in production |
| SameSite | Strict or Lax |
| Session Store | Redis (production), PostgreSQL |
| Session Lifetime | 15 minutes (sensitive), 24 hours (general) |
| Session ID Length | 32+ bytes of randomness |
| Session Regeneration | After login, privilege escalation |
| Session Cleanup | Implement TTL and garbage collection |

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Session Management](https://owasp.org/www-community/attacks/Session_hijacking_attack)
- [MDN Set-Cookie Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)
- [SameSite Cookies Explained - web.dev](https://web.dev/samesite-cookies-explained/)
- [Redis Session Store Best Practices](https://redis.io/docs/manual/patterns/)
- [OWASP Cookie Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cookie-Based_Session_Management_Cheat_Sheet.html)
