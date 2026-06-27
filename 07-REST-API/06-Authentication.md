# API Authentication

## Definition

API authentication is the process of verifying the identity of a client making requests to an API. It ensures that only authorized users and applications can access protected resources. Authentication answers "Who are you?" while authorization answers "What can you do?"

## Why Do We Need It?

Without authentication:

1. **Data breaches** - Unauthorized access to sensitive data
2. **Abuse** - Uncontrolled API usage, rate limit bypass
3. **Compliance violations** - GDPR, HIPAA, SOC2 requirements
4. **Revenue loss** - Unauthorized access to paid features
5. **Trust issues** - Users won't share data with unsecured APIs

## How It Works

### Authentication Methods Overview

```
Authentication Methods
══════════════════════

1. API Keys
   Simple token-based authentication
   ✅ Easy to implement
   ❌ Less secure (can be leaked)

2. JWT (JSON Web Tokens)
   Stateless token with claims
   ✅ Scalable, no server state
   ❌ Cannot be revoked easily

3. OAuth 2.0
   Delegated authorization framework
   ✅ Industry standard, flexible
   ❌ Complex implementation

4. Session-Based
   Server-side session storage
   ✅ Easy to revoke
   ❌ Not scalable, stateful

5. Basic Auth
   Username:password in header
   ✅ Simple
   ❌ Insecure without HTTPS
```

### API Key Authentication

```
API Key Flow
════════════

Client                          Server
  │                               │
  │  GET /api/data                │
  │  X-API-Key: abc123def456      │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "data": "..." }           │
  │◄──────────────────────────────│
```

```typescript
// API Key middleware
function apiKeyAuth(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  const validKey = await ApiKeyService.validate(apiKey);
  
  if (!validKey) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  
  req.apiKey = validKey;
  next();
}

// Usage
app.use('/api', apiKeyAuth);

// Or per route
app.get('/api/data', apiKeyAuth, async (req, res) => {
  res.json({ data: 'secret' });
});

// API Key with rate limiting
app.get('/api/data', apiKeyAuth, rateLimiter({
  keyGenerator: (req) => req.apiKey.id,
  max: 100,
  windowMs: 15 * 60 * 1000
}), async (req, res) => {
  res.json({ data: 'secret' });
});
```

### JWT Authentication

```
JWT Token Structure
═══════════════════

Header.Payload.Signature

Header: { "alg": "HS256", "typ": "JWT" }
Payload: { "sub": "123", "role": "admin", "exp": 1735689600 }
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)

JWT Flow
════════

Client                          Server
  │                               │
  │  POST /api/auth/login         │
  │  { email, password }         │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "token": "eyJhbG..." }    │
  │◄──────────────────────────────│
  │                               │
  │  GET /api/users               │
  │  Authorization: Bearer eyJhbG...│
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "data": [...] }           │
  │◄──────────────────────────────│
```

```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

const JWT_SECRET = process.env.JWT_SECRET;
const JWT_EXPIRY = '1h';
const REFRESH_TOKEN_EXPIRY = '7d';

// Login endpoint
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }
  
  const user = await UserService.findByEmail(email);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const isValid = await bcrypt.compare(password, user.password);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = jwt.sign(
    { sub: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRY }
  );
  
  const refreshToken = jwt.sign(
    { sub: user.id, type: 'refresh' },
    JWT_SECRET,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );
  
  await RefreshTokenService.create({ userId: user.id, token: refreshToken });
  
  res.json({
    data: {
      token,
      refreshToken,
      expiresIn: 3600
    }
  });
});

// JWT middleware
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  const token = authHeader.split(' ')[1];
  
  try {
    const payload = jwt.verify(token, JWT_SECRET);
    req.user = payload;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Role-based authorization
function authorize(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// Usage
app.get('/api/admin/users', authenticate, authorize('admin'), async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});
```

### Token Refresh Flow

```
Token Refresh Flow
══════════════════

Client                          Server
  │                               │
  │  GET /api/data                │
  │  Authorization: Bearer <expired>│
  │──────────────────────────────►│
  │                               │
  │  401 Token Expired            │
  │◄──────────────────────────────│
  │                               │
  │  POST /api/auth/refresh       │
  │  { refreshToken }            │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "token": "new..." }       │
  │◄──────────────────────────────│
  │                               │
  │  GET /api/data                │
  │  Authorization: Bearer <new>  │
  │──────────────────────────────►│
```

```typescript
// Refresh token endpoint
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(400).json({ error: 'Refresh token required' });
  }
  
  try {
    const payload = jwt.verify(refreshToken, JWT_SECRET);
    
    if (payload.type !== 'refresh') {
      return res.status(401).json({ error: 'Invalid token type' });
    }
    
    const storedToken = await RefreshTokenService.findByToken(refreshToken);
    if (!storedToken || storedToken.used) {
      return res.status(401).json({ error: 'Invalid refresh token' });
    }
    
    // Mark old token as used
    await RefreshTokenService.markAsUsed(refreshToken);
    
    // Generate new tokens
    const user = await UserService.findById(payload.sub);
    const newToken = jwt.sign(
      { sub: user.id, email: user.email, role: user.role },
      JWT_SECRET,
      { expiresIn: JWT_EXPIRY }
    );
    
    const newRefreshToken = jwt.sign(
      { sub: user.id, type: 'refresh' },
      JWT_SECRET,
      { expiresIn: REFRESH_TOKEN_EXPIRY }
    );
    
    await RefreshTokenService.create({ userId: user.id, token: newRefreshToken });
    
    res.json({
      data: {
        token: newToken,
        refreshToken: newRefreshToken,
        expiresIn: 3600
      }
    });
  } catch (err) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

### OAuth 2.0 Flow

```
OAuth 2.0 Authorization Code Flow
══════════════════════════════════

User        Client          Auth Server       Resource Server
  │            │                  │                  │
  │  1. Login  │                  │                  │
  │───────────►│                  │                  │
  │            │  2. Redirect to  │                  │
  │◄───────────│  auth server     │                  │
  │            │                  │                  │
  │  3. Authorize                │                  │
  │──────────────────────────────►│                  │
  │            │                  │                  │
  │  4. Authorization Code       │                  │
  │◄──────────────────────────────│                  │
  │            │                  │                  │
  │  5. Send code to client      │                  │
  │───────────►│                  │                  │
  │            │  6. Exchange     │                  │
  │            │  code for token  │                  │
  │            │─────────────────►│                  │
  │            │                  │                  │
  │            │  7. Access Token │                  │
  │            │◄─────────────────│                  │
  │            │                  │                  │
  │            │  8. API Request  │                  │
  │            │──────────────────────────────────►│
  │            │                  │                  │
  │            │  9. Response     │                  │
  │            │◄──────────────────────────────────│
```

```typescript
// OAuth 2.0 implementation
app.get('/api/auth/google', (req, res) => {
  const url = `https://accounts.google.com/o/oauth2/v2/auth?` +
    `client_id=${GOOGLE_CLIENT_ID}&` +
    `redirect_uri=${GOOGLE_REDIRECT_URI}&` +
    `response_type=code&` +
    `scope=openid email profile`;
  
  res.redirect(url);
});

app.get('/api/auth/google/callback', async (req, res) => {
  const { code } = req.query;
  
  // Exchange code for tokens
  const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      redirect_uri: GOOGLE_REDIRECT_URI,
      grant_type: 'authorization_code'
    })
  });
  
  const { access_token, id_token } = await tokenResponse.json();
  
  // Get user info
  const userInfoResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
    headers: { Authorization: `Bearer ${access_token}` }
  });
  
  const userInfo = await userInfoResponse.json();
  
  // Find or create user
  let user = await UserService.findByEmail(userInfo.email);
  if (!user) {
    user = await UserService.create({
      email: userInfo.email,
      name: userInfo.name,
      provider: 'google',
      providerId: userInfo.id
    });
  }
  
  // Generate JWT
  const token = jwt.sign(
    { sub: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRY }
  );
  
  res.json({ data: { token, user } });
});
```

## Code Examples

### Complete Authentication System

```typescript
import express from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import { v4 as uuidv4 } from 'uuid';

// Types
interface User {
  id: string;
  email: string;
  password: string;
  role: 'user' | 'admin';
}

interface JWTPayload {
  sub: string;
  email: string;
  role: string;
  iat: number;
  exp: number;
}

// Token storage (in production, use Redis)
const refreshTokens = new Map<string, { userId: string; used: boolean }>();
const passwordResetTokens = new Map<string, { userId: string; expires: Date }>();

// Auth middleware
const authenticate = async (req, res, next) => {
  const token = extractToken(req);
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const payload = jwt.verify(token, JWT_SECRET) as JWTPayload;
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
};

// Role authorization
const authorize = (...roles: string[]) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};

// Permission-based authorization
const requirePermission = (...permissions: string[]) => {
  return async (req, res, next) => {
    const userPermissions = await PermissionService.getUserPermissions(req.user.sub);
    
    const hasPermission = permissions.every(p => userPermissions.includes(p));
    
    if (!hasPermission) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};

// Routes
app.post('/api/auth/register', async (req, res) => {
  const { email, password, name } = req.body;
  
  if (!email || !password || !name) {
    return res.status(400).json({ error: 'All fields required' });
  }
  
  const existing = await UserService.findByEmail(email);
  if (existing) {
    return res.status(409).json({ error: 'Email already exists' });
  }
  
  const hashedPassword = await bcrypt.hash(password, 12);
  const user = await UserService.create({ email, password: hashedPassword, name });
  
  const token = generateToken(user);
  const refreshToken = await generateRefreshToken(user.id);
  
  res.status(201).json({
    data: {
      user: { id: user.id, email: user.email, name: user.name },
      token,
      refreshToken
    }
  });
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }
  
  const user = await UserService.findByEmail(email);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = generateToken(user);
  const refreshToken = await generateRefreshToken(user.id);
  
  res.json({
    data: {
      user: { id: user.id, email: user.email },
      token,
      refreshToken
    }
  });
});

app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(400).json({ error: 'Refresh token required' });
  }
  
  const stored = refreshTokens.get(refreshToken);
  if (!stored || stored.used) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }
  
  // Mark as used (rotation)
  stored.used = true;
  
  const user = await UserService.findById(stored.userId);
  const newToken = generateToken(user);
  const newRefreshToken = await generateRefreshToken(user.id);
  
  res.json({
    data: {
      token: newToken,
      refreshToken: newRefreshToken
    }
  });
});

app.post('/api/auth/logout', authenticate, async (req, res) => {
  const { refreshToken } = req.body;
  
  if (refreshToken) {
    refreshTokens.delete(refreshToken);
  }
  
  res.json({ message: 'Logged out' });
});

// Protected routes
app.get('/api/users', authenticate, async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

app.get('/api/admin/users', authenticate, authorize('admin'), async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

app.delete('/api/users/:id', authenticate, requirePermission('users:delete'), async (req, res) => {
  await UserService.delete(req.params.id);
  res.status(204).end();
});

// Helper functions
function generateToken(user: User): string {
  return jwt.sign(
    { sub: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: '1h' }
  );
}

async function generateRefreshToken(userId: string): Promise<string> {
  const token = jwt.sign(
    { sub: userId, type: 'refresh' },
    JWT_SECRET,
    { expiresIn: '7d' }
  );
  
  refreshTokens.set(token, { userId, used: false });
  
  // Cleanup old tokens
  setTimeout(() => {
    refreshTokens.delete(token);
  }, 7 * 24 * 60 * 60 * 1000);
  
  return token;
}

function extractToken(req): string | null {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.split(' ')[1];
  }
  return null;
}
```

## Real-World Use Cases

### 1. Multi-Tenant SaaS

```typescript
// Tenant-aware authentication
const authenticateTenant = async (req, res, next) => {
  const token = extractToken(req);
  const payload = jwt.verify(token, JWT_SECRET);
  
  const tenant = await TenantService.findById(payload.tenantId);
  if (!tenant) {
    return res.status(401).json({ error: 'Invalid tenant' });
  }
  
  req.user = payload;
  req.tenant = tenant;
  
  // Set tenant context for database queries
  await db.query(`SET app.tenant_id = '${tenant.id}'`);
  
  next();
};

app.get('/api/data', authenticateTenant, async (req, res) => {
  // Data is automatically scoped to tenant
  const data = await DataService.findAll();
  res.json({ data });
});
```

### 2. API Gateway Authentication

```typescript
// Centralized authentication at gateway
const gatewayAuth = async (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  const token = extractToken(req);
  
  if (apiKey) {
    // API key authentication
    const key = await ApiKeyService.validate(apiKey);
    if (!key) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
    req.auth = { type: 'apiKey', key };
  } else if (token) {
    // JWT authentication
    try {
      const payload = jwt.verify(token, JWT_SECRET);
      req.auth = { type: 'jwt', user: payload };
    } catch (err) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  } else {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  next();
};
```

### 3. Machine-to-Machine Authentication

```typescript
// Client credentials flow
app.post('/api/auth/token', async (req, res) => {
  const { grant_type, client_id, client_secret } = req.body;
  
  if (grant_type !== 'client_credentials') {
    return res.status(400).json({ error: 'Unsupported grant type' });
  }
  
  const client = await ClientService.validate(client_id, client_secret);
  if (!client) {
    return res.status(401).json({ error: 'Invalid client credentials' });
  }
  
  const token = jwt.sign(
    { sub: client.id, type: 'machine' },
    JWT_SECRET,
    { expiresIn: '1h' }
  );
  
  res.json({
    access_token: token,
    token_type: 'Bearer',
    expires_in: 3600
  });
});
```

## Common Mistakes

### 1. Not Validating Tokens

```typescript
// ❌ Bad: Not verifying token signature
const payload = jwt.decode(token);

// ✅ Good: Verify signature
const payload = jwt.verify(token, JWT_SECRET);
```

### 2. Storing Secrets in Code

```typescript
// ❌ Bad
const JWT_SECRET = 'my-secret-key';

// ✅ Good
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error('JWT_SECRET not configured');
```

### 3. Not Rotating Refresh Tokens

```typescript
// ❌ Bad: Same refresh token forever
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  const payload = jwt.verify(refreshToken, JWT_SECRET);
  const newToken = generateToken(payload.sub);
  res.json({ token: newToken });
});

// ✅ Good: Rotate refresh tokens
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  const stored = await getRefreshToken(refreshToken);
  
  if (stored.used) {
    return res.status(401).json({ error: 'Token reuse detected' });
  }
  
  await markAsUsed(refreshToken);
  const newToken = generateToken(stored.userId);
  const newRefreshToken = await createRefreshToken(stored.userId);
  
  res.json({ token: newToken, refreshToken: newRefreshToken });
});
```

### 4. Missing HTTPS

```typescript
// ❌ Bad: HTTP only
app.listen(3000);

// ✅ Good: HTTPS in production
if (process.env.NODE_ENV === 'production') {
  https.createServer(sslOptions, app).listen(443);
} else {
  app.listen(3000);
}
```

### 5. Not Handling Token Expiration

```typescript
// ❌ Bad: No expiration
const token = jwt.sign({ sub: user.id }, JWT_SECRET);

// ✅ Good: Always set expiration
const token = jwt.sign({ sub: user.id }, JWT_SECRET, { expiresIn: '1h' });
```

## Best Practices

1. **Use HTTPS always** - Encrypt tokens in transit
2. **Set short token expiry** - 15 min for access tokens
3. **Rotate refresh tokens** - Prevent token reuse attacks
4. **Store tokens securely** - HttpOnly cookies or secure storage
5. **Validate on every request** - Don't trust client-side validation
6. **Use strong secrets** - 256-bit minimum for HMAC
7. **Implement rate limiting** - Prevent brute force attacks
8. **Log authentication events** - Monitor for suspicious activity
9. **Support MFA** - Multi-factor authentication for sensitive operations
10. **Use industry standards** - OAuth 2.0, OpenID Connect

## Performance Considerations

- **JWT validation** - Stateless, no database lookup needed
- **Token refresh** - Batch refresh operations
- **Session storage** - Use Redis for fast session lookup
- **Certificate caching** - Cache JWKS for RSA tokens
- **Connection pooling** - Reuse database connections

## Interview Questions

### Beginner (5)

1. **What is the difference between authentication and authorization?** - Authentication: verifying identity; Authorization: verifying permissions.

2. **What is JWT?** - JSON Web Token; a compact, URL-safe token format for securely transmitting information.

3. **What are API keys?** - Simple tokens passed in headers to identify and authenticate clients.

4. **Why should we use HTTPS?** - Encrypts data in transit, prevents token interception.

5. **What is token expiration?** - Setting a time limit on token validity to reduce risk of stolen tokens.

### Intermediate (5)

6. **Explain OAuth 2.0 flow** - Delegated authorization framework with authorization code, implicit, and client credentials grants.

7. **What are refresh tokens?** - Long-lived tokens used to obtain new access tokens without re-authentication.

8. **How do you store JWT tokens securely?** - HttpOnly, Secure cookies for web; secure storage for mobile.

9. **What is token rotation?** - Issuing new refresh tokens on each use to prevent token reuse attacks.

10. **How do you handle token revocation?** - Use token blacklist, short expiry, or refresh token rotation.

### Senior (10)

11. **Design a scalable authentication system** - Stateless JWT, distributed session store, token introspection.

12. **Implement MFA with TOTP** - Time-based one-time passwords, QR code generation, backup codes.

13. **Design API key management** - Generation, rotation, scoping, usage tracking.

14. **How do you prevent token theft?** - Secure storage, short expiry, token binding, device fingerprinting.

15. **Design SSO for microservices** - Centralized auth, token propagation, session sharing.

16. **Implement passwordless authentication** - Magic links, WebAuthn, biometrics.

17. **Design rate limiting per user** - Token bucket, sliding window, distributed counters.

18. **How do you handle concurrent token refresh?** - Token families, reuse detection, graceful degradation.

19. **Design audit logging for auth events** - Login attempts, token usage, permission changes.

20. **Implement zero-trust authentication** - Verify every request, no implicit trust, continuous validation.

### FAANG-style (5)

21. **Design authentication for a global platform** - Multi-region, latency-aware, failover strategies.

22. **Design session management at scale** - Distributed sessions, sticky sessions, session affinity.

23. **Implement certificate-based authentication** - mTLS, certificate rotation, revocation lists.

24. **Design authentication for IoT devices** - Device provisioning, certificate management, secure boot.

25. **How would you migrate from sessions to JWT?** - Dual support, gradual migration, backward compatibility.

### Follow-ups (5)

26. **What are the security risks of JWT?** - Token theft, no revocation, payload exposure.

27. **How do you handle password reset securely?** - Time-limited tokens, rate limiting, notification.

28. **What is session fixation and how to prevent it?** - Attack where attacker sets session ID; regenerate on login.

29. **How do you implement remember-me functionality?** - Long-lived refresh tokens, secure cookie.

30. **What are the tradeoffs between JWT and sessions?** - JWT: scalable but can't revoke; Sessions: revocable but stateful.

## Summary

API authentication is critical for security. JWT is the most common choice for modern APIs due to its stateless nature. Always use HTTPS, implement token rotation, and handle expiration properly. For complex systems, consider OAuth 2.0 and multi-factor authentication. Regular security audits and monitoring are essential.

## Cheat Sheet

| Method | Security | Scalability | Use Case |
|--------|----------|-------------|----------|
| API Key | Medium | High | External APIs |
| JWT | High | High | User authentication |
| OAuth 2.0 | High | High | Third-party access |
| Session | Medium | Low | Traditional web |
| Basic Auth | Low | High | Simple internal APIs |

## References & Learn More

- [OAuth 2.0 - RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [JWT (JSON Web Token) - RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [Introduction to JWT - Auth0](https://jwt.io/introduction/)
- [OAuth 2.0 Simplified - Aaron Parecki](https://aaronparecki.com/oauth-2-simplified/)
- [OWASP API Security - Top 10](https://owasp.org/API-Security/)
