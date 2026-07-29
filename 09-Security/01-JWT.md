# JWT (JSON Web Tokens)

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

## Definition

A JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties. JWTs are defined by the RFC 7519 standard and consist of a JSON-encoded payload signed with a cryptographic algorithm. They are self-contained tokens that carry all the information needed for authentication and authorization, eliminating the need for server-side session storage.

A JWT is essentially a digitally signed token that proves identity and carries authorized claims between systems.

## Why Do We Need It?

- **Stateless Authentication**: No server-side session storage required; the token itself contains all needed information
- **Scalability**: Horizontal scaling is trivial because authentication state lives in the token, not on the server
- **Interoperability**: Standard format understood across languages, frameworks, and services
- **Microservices**: Ideal for service-to-service authentication in distributed architectures
- **Performance**: Token validation is fast and doesn't require database lookups
- **Decoupled Authorization**: The token carries claims, allowing services to make authorization decisions independently

## How It Works

### JWT Structure

A JWT consists of three Base64URL-encoded parts separated by dots:

```text
xxxxx.yyyyy.zzzzz

|       |       |

Header  Payload Signature

```

**Header**: Contains metadata about the token (algorithm, token type)
**Payload**: Contains the claims (user data, permissions, expiration)
**Signature**: Cryptographic signature ensuring token integrity

### Authentication Flow

```text
┌─────────────┐                                    ┌─────────────┐
│   Client    │                                    │   Server    │
└──────┬──────┘                                    └──────┬──────┘
       │                                                   │
       │  1. POST /login {email, password}                 │
       │──────────────────────────────────────────────────>│
       │                                                   │
       │                    2. Validate credentials         │
       │                    3. Generate JWT                 │
       │                    4. Sign with secret/key         │
       │                                                   │
       │  5. Return { accessToken, refreshToken }          │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  6. GET /resource                                 │
       │     Authorization: Bearer <jwt>                   │
       │──────────────────────────────────────────────────>│
       │                                                   │
       │                    7. Verify signature             │
       │                    8. Check expiration             │
       │                    9. Extract claims               │
       │                    10. Return resource             │
       │                                                   │
       │  11. Response with data                           │
       │<──────────────────────────────────────────────────│

```

### Token Expiration and Refresh Flow

```text
┌─────────────┐                              ┌─────────────┐
│   Client    │                              │   Server    │
└──────┬──────┘                              └──────┬──────┘
       │                                             │
       │  Access token expires (15 min)              │
       │                                             │
       │  POST /refresh { refreshToken }             │
       │────────────────────────────────────────────>│
       │                                             │
       │              Validate refresh token         │
       │              Check if revoked               │
       │              Generate new pair              │
       │                                             │
       │  Return { accessToken, refreshToken }       │
       │<────────────────────────────────────────────│

```

## Code Examples

### Basic JWT Generation and Verification (TypeScript)

```typescript
import jwt from "jsonwebtoken";

interface TokenPayload {
  userId: string;
  email: string;
  roles: string[];
}

interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;

const generateTokenPair = (payload: TokenPayload): TokenPair => {
  const accessToken = jwt.sign(payload, ACCESS_SECRET, {
    expiresIn: "15m",
    issuer: "myapp",
    audience: "myapp-api",
  });

  const refreshToken = jwt.sign({ userId: payload.userId }, REFRESH_SECRET, {
    expiresIn: "7d",
    issuer: "myapp",
  });

  return { accessToken, refreshToken };
};

const verifyAccessToken = (token: string): TokenPayload => {
  return jwt.verify(token, ACCESS_SECRET, {
    issuer: "myapp",
    audience: "myapp-api",
  }) as TokenPayload;
};

const verifyRefreshToken = (token: string): { userId: string } => {
  return jwt.verify(token, REFRESH_SECRET, {
    issuer: "myapp",
  }) as { userId: string };
};

```

### JWT Middleware (Express)

```typescript
import { Request, Response, NextFunction } from "express";

interface AuthRequest extends Request {
  user?: TokenPayload;
}

const authenticateToken = (
  req: AuthRequest,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader?.startsWith("Bearer ")
    ? authHeader.slice(7)
    : null;

  if (!token) {
    res.status(401).json({ error: "Access token required" });
    return;
  }

  try {
    const decoded = verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      res.status(401).json({ error: "Token expired" });
    } else {
      res.status(403).json({ error: "Invalid token" });
    }
  }
};

const authorizeRole = (roles: string[]) => {
  return (req: AuthRequest, res: Response, next: NextFunction): void => {
    if (!req.user || !roles.includes(req.user.roles[0])) {
      res.status(403).json({ error: "Insufficient permissions" });
      return;
    }
    next();
  };
};

// Usage
app.get("/admin", authenticateToken, authorizeRole(["admin"]), adminHandler);

```

### JWT with RS256 (Asymmetric Keys)

```typescript
import jwt from "jsonwebtoken";
import fs from "fs";

const privateKey = fs.readFileSync("private.pem", "utf8");
const publicKey = fs.readFileSync("public.pem", "utf8");

// Sign with private key (authentication server)
const generateToken = (payload: TokenPayload): string => {
  return jwt.sign(payload, privateKey, {
    algorithm: "RS256",
    expiresIn: "15m",
    issuer: "auth-server",
  });
};

// Verify with public key (resource server)
const verifyToken = (token: string): TokenPayload => {
  return jwt.verify(token, publicKey, {
    algorithms: ["RS256"],
    issuer: "auth-server",
  }) as TokenPayload;
};

```

### Token Blacklisting (for logout)

```typescript
import Redis from "ioredis";

const redis = new Redis();

const blacklistToken = async (token: string): Promise<void> => {
  const decoded = jwt.decode(token) as TokenPayload;
  if (!decoded) return;

  const expiresIn = decoded.exp
    ? decoded.exp - Math.floor(Date.now() / 1000)
    : 900;

  if (expiresIn > 0) {
    await redis.setex(`bl:${token}`, expiresIn, "1");
  }
};

const isTokenBlacklisted = async (token: string): Promise<boolean> => {
  const result = await redis.get(`bl:${token}`);
  return result !== null;
};

```

## Real-World Use Cases

### 1. Single Sign-On (SSO)

- User authenticates with a central identity provider
- JWT is issued and shared across multiple services
- Each service validates the JWT independently

### 2. API Gateway Authentication

- API gateway validates JWT before routing to microservices
- Claims are forwarded to downstream services
- No need for each service to authenticate independently

### 3. Mobile and SPA Authentication

- Tokens stored securely on client
- Short-lived access tokens minimize risk if compromised
- Refresh tokens enable seamless re-authentication

### 4. Third-Party API Access

- OAuth 2.0 flows issue JWTs for API access
- Scoped permissions encoded in token claims
- Time-limited access without sharing credentials

## Common Mistakes

1. **Storing sensitive data in payload**: JWT payload is base64-encoded, not encrypted. Never store passwords, SSNs, or secrets in the payload.

2. **Using weak signing secrets**: Using short or predictable secrets makes tokens forgeable. Use cryptographically strong secrets (256+ bits for HMAC).

3. **No token expiration**: Tokens without expiration remain valid forever if compromised.

4. **Storing JWT in localStorage**: Vulnerable to XSS attacks. Use httpOnly cookies or memory storage.

5. **Not validating the `iss` and `aud` claims**: Without validation, tokens from other issuers may be accepted.

6. **Using HS256 when RS256 is needed**: In microservices, multiple services need to verify tokens. Sharing a secret is risky; use asymmetric keys.

7. **Neglecting refresh token rotation**: Not rotating refresh tokens increases the window of opportunity for attackers.

8. **Leaking tokens in logs or URLs**: Tokens in URLs or logs can be captured by proxies or logging systems.

## Best Practices

1. **Use short-lived access tokens** (15 minutes or less)

2. **Implement refresh token rotation** with single-use refresh tokens

3. **Store tokens in httpOnly, Secure, SameSite=Strict cookies** for web apps

4. **Use RS256 for multi-service architectures** to avoid sharing secrets

5. **Validate all standard claims** (`iss`, `aud`, `exp`, `nbf`, `iat`)

6. **Implement token revocation** for logout and security incidents

7. **Never store sensitive data** in the JWT payload

8. **Use strong secrets** (minimum 256-bit for HMAC algorithms)

9. **Keep tokens small** to avoid HTTP header size issues
10. **Implement rate limiting** on token refresh endpoints

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Token Size | Larger tokens increase HTTP header overhead; keep payloads minimal |
| Signing Performance | RS256 signing is slower than HS256; cache when possible |
| Verification | Symmetric verification is fast; asymmetric requires public key operations |
| Memory Usage | Stateless tokens reduce server memory vs session stores |
| Network Overhead | Tokens in every request add ~500-1000 bytes per request |

## Summary

JWT is a powerful stateless authentication mechanism that enables scalable, decoupled authorization across distributed systems. Key takeaways:

- JWTs consist of header, payload, and signature
- Use RS256 for distributed systems, HS256 for single-server apps
- Always validate all standard claims
- Store tokens in httpOnly cookies, not localStorage
- Implement refresh token rotation for security
- Never store sensitive data in JWT payloads
- Plan for token revocation from the start

## Cheat Sheet
| Concept | Recommendation |
|---------|---------------|
| Algorithm (Single Server) | HS256 |
| Algorithm (Distributed) | RS256 |
| Access Token Lifetime | 15 minutes |
| Refresh Token Lifetime | 7 days |
| Storage (Web) | httpOnly cookie |
| Storage (Mobile) | Secure storage (Keychain/Keystore) |
| Secret Length | 256+ bits |
| Required Claims | `iss`, `aud`, `exp`, `iat` |
| Revocation | Redis blacklist with JTI |
| Refresh Strategy | Rotation with family tracking |

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [JWT.io - Introduction to JSON Web Tokens](https://jwt.io/introduction/)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet_for_Java.html)
- [Auth0 JWT Documentation](https://auth0.com/docs/secure/tokens/json-web-tokens)
- [RFC 7517 - JSON Web Key (JWK)](https://datatracker.ietf.org/doc/html/rfc7517)
- [Understanding JWT Security - Auth0 Blog](https://auth0.com/blog/json-web-tokens-and-security/)
