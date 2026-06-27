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

```
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

```
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

```
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

## Interview Questions

### Beginner (5-10)

**Q1: What is the difference between a session and a cookie?**
A: A session stores data on the server, identified by a session ID. A cookie stores data on the client (browser) and is sent with every request. Sessions are more secure; cookies are simpler.

**Q2: What is the HttpOnly cookie flag?**
A: HttpOnly prevents JavaScript from accessing the cookie via document.cookie. This protects session cookies from XSS attacks, as malicious scripts cannot steal them.

**Q3: What is the Secure cookie flag?**
A: Secure ensures cookies are only sent over HTTPS connections. This prevents cookies from being transmitted over unencrypted HTTP, protecting against eavesdropping.

**Q4: What is SameSite cookie attribute?**
A: SameSite controls when cookies are sent with cross-site requests. Strict: never sent cross-site. Lax: sent for top-level navigation. None: sent with all requests.

**Q5: Why should you regenerate session ID after login?**
A: Prevents session fixation attacks. If an attacker sets a session ID before login, regenerating ensures the attacker's ID is invalidated after successful authentication.

**Q6: What is session expiration?**
A: Sessions should expire after a period of inactivity or a maximum lifetime. This limits the window of opportunity for attackers if a session is compromised.

**Q7: Where should session data be stored?**
A: Server-side in secure stores like Redis, PostgreSQL, or MongoDB. Never store sensitive session data in cookies (they're client-side and can be tampered with).

**Q8: What is a session store?**
A: A backend for storing session data. Options include in-memory (development), Redis (production), PostgreSQL, MongoDB, or file systems. Production should use persistent, scalable stores.

**Q9: What is the difference between session-based and token-based authentication?**
A: Session-based stores data server-side; session ID in cookie. Token-based (JWT) stores data in the token itself; stateless. Sessions are easier to revoke; tokens are more scalable.

**Q10: What is session fixation?**
A: An attack where an attacker sets a victim's session ID before authentication. After login, the attacker uses the known session ID to hijack the session.

### Intermediate (5-10)

**Q11: How would you implement session management for a microservices architecture?**
A: Use centralized session store (Redis Cluster). Implement session sharing across services. Use API gateway for session validation. Implement session stickiness or shared sessions.

**Q12: How do you handle session security in a multi-tenant application?**
A: Use tenant-specific session namespaces. Implement tenant isolation in session store. Validate tenant context on each request. Audit cross-tenant session access.

**Q13: How do you implement session revocation for logout?**
A: Destroy session on server. Clear session cookie on client. If using Redis, delete session key. Implement immediate session invalidation.

**Q14: How do you handle session persistence across devices?**
A: Implement device tracking in session. Use device-specific sessions. Sync session data across devices. Implement device management UI.

**Q15: How do you monitor session activity?**
A: Log session creation, access, and destruction. Monitor for unusual patterns (multiple IPs, rapid requests). Implement session anomaly detection. Use SIEM for monitoring.

**Q16: How do you handle session data serialization?**
A: Use efficient formats (JSON, MessagePack). Implement compression for large sessions. Use schema validation. Handle versioning for session structure changes.

**Q17: How do you implement session-based CSRF protection?**
A: Store CSRF token in session. Validate token on state-changing requests. Regenerate token periodically. Use double-submit cookie pattern for SPAs.

**Q18: How do you handle session security in server-side rendering?**
A: Use httpOnly cookies for session ID. Implement CSP headers. Validate session on each render. Use secure session stores.

**Q19: How do you implement session analytics?**
A: Track session duration, page views, user actions. Implement funnel analysis. Use session replay for debugging. Respect user privacy.

**Q20: How do you handle session migration?**
A: Implement session versioning. Migrate old sessions gracefully. Use backward compatibility. Implement rollback procedures.

### Senior (10-15)

**Q21: Design a session management system for a global application with 100 million users.**
A: Use distributed Redis Cluster. Implement session sharding by user ID. Use read replicas for session reads. Implement session caching at edge. Monitor session latency.

**Q22: How would you implement session security for a financial application?**
A: Implement step-up authentication for sensitive operations. Use session binding to device/IP. Implement session anomaly detection. Audit all session activity.

**Q23: Design a session system that supports both web and mobile clients.**
A: Use different session stores per platform. Implement platform-specific session lifetimes. Use secure storage on mobile (Keychain/Keystore). Implement cross-platform session management.

**Q24: How would you handle session security in a zero-trust environment?**
A: Validate sessions on every request. Implement continuous authentication. Use session attestation. Monitor for session hijacking.

**Q25: Design a session system for a real-time collaboration platform.**
A: Use WebSocket sessions. Implement session-based presence. Handle concurrent session access. Implement session-based conflict resolution.

**Q26: How would you implement session management for a system with strict compliance requirements?**
A: Implement comprehensive session logging. Use tamper-evident session storage. Implement session audit trails. Meet regulatory requirements (SOX, HIPAA).

**Q27: Design a session system that supports session failover.**
A: Use multi-region Redis replication. Implement session replication. Use sticky sessions or shared sessions. Implement failover procedures.

**Q28: How would you handle session security for a healthcare application?**
A: Implement patient-specific sessions. Use session-based access controls. Audit all session activity. Meet HIPAA requirements.

**Q29: Design a session system for a high-traffic event (e.g., ticket sales).**
A: Use distributed session stores. Implement session caching. Use optimistic locking for concurrent access. Implement queue-based session processing.

**Q30: How would you implement session management for a system with anonymous users?**
A: Use anonymous sessions with limited lifetime. Implement session-to-account merging. Use fingerprinting for anonymous tracking. Respect privacy regulations.

### FAANG-style (5-10)

**Q31: Design a session management system handling 1 billion active sessions.**
A: Use globally distributed Redis. Implement session sharding. Use edge caching. Implement session compression. Monitor session metrics at scale.

**Q32: How would you implement session security for a system with nation-state adversaries?**
A: Use hardware security modules. Implement session attestation. Use quantum-resistant algorithms. Implement air-gapped session stores.

**Q33: Design a session system for a system with 99.999% uptime requirements.**
A: Use multi-region replication. Implement automatic failover. Use session caching. Implement circuit breakers. Monitor session health.

**Q34: How would you implement session management for a system with strict latency requirements (< 1ms)?**
A: Use in-memory session stores. Implement session caching at application level. Use efficient serialization. Optimize session lookups.

**Q35: Design a session system that supports real-time session analytics.**
A: Use event streaming for session events. Implement real-time dashboards. Use machine learning for anomaly detection. Implement automated response.

### Follow-ups (5-10)

**Q36: How would your session design change if cookies were not available?**
A: Use URL-based sessions (less secure). Implement token-based authentication (JWT). Use local storage with manual token management. Implement device binding.

**Q37: If Redis was experiencing high latency, how would you optimize session lookups?**
A: Implement session caching at application level. Use connection pooling. Implement read replicas. Use session compression. Optimize data structures.

**Q38: How would you implement session management for a system with regulatory data retention requirements?**
A: Implement session logging with retention policies. Use encrypted session archives. Implement secure deletion. Maintain audit trails.

**Q39: How would your approach change for a system handling classified information?**
A: Use hardware security modules. Implement session attestation. Use air-gapped session stores. Implement strict access controls.

**Q40: If you discovered session hijacking in production, what would be your incident response?**
A: Immediately invalidate compromised sessions. Force re-authentication. Implement additional monitoring. Rotate session secrets. Notify affected users.

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

## References & Learn More

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Session Management](https://owasp.org/www-community/attacks/Session_hijacking_attack)
- [MDN Set-Cookie Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)
- [SameSite Cookies Explained - web.dev](https://web.dev/samesite-cookies-explained/)
- [Redis Session Store Best Practices](https://redis.io/docs/manual/patterns/)
- [OWASP Cookie Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cookie-Based_Session_Management_Cheat_Sheet.html)
