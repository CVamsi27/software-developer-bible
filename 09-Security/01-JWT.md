# JWT (JSON Web Tokens)

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

## Interview Questions

### Beginner (5-10)

**Q1: What is a JWT and why is it used?**
A: JWT (JSON Web Token) is a compact, URL-safe token format used for authentication and authorization. It contains a header, payload, and signature, enabling stateless authentication where the server doesn't need to store session data.

**Q2: What are the three parts of a JWT?**
A: Header (algorithm and token type), Payload (claims and user data), and Signature (cryptographic signature to verify integrity).

**Q3: What is the difference between HS256 and RS256?**
A: HS256 uses a shared secret for signing and verification (symmetric). RS256 uses a private key to sign and a public key to verify (asymmetric). RS256 is better for distributed systems.

**Q4: How do you store JWTs on the client?**
A: The most secure method is httpOnly cookies. Alternatives include memory (JavaScript variables) or sessionStorage. localStorage is discouraged due to XSS vulnerability.

**Q5: What is a refresh token?**
A: A refresh token is a long-lived token used to obtain new access tokens without re-authenticating the user. It's typically stored more securely than access tokens.

**Q6: Why shouldn't you store JWTs in localStorage?**
A: localStorage is accessible via JavaScript, making it vulnerable to XSS attacks. An attacker who injects malicious script can steal the token.

**Q7: How do you verify a JWT?**
A: The server uses the signing algorithm and key to recompute the signature from the header and payload, then compares it with the token's signature.

**Q8: What happens when a JWT expires?**
A: The token is rejected by the server, and the client must either re-authenticate or use a refresh token to get a new access token.

**Q9: Can a JWT be revoked?**
A: JWTs are inherently non-revocable. To implement revocation, maintain a server-side blacklist (e.g., in Redis) and check it during validation.

**Q10: What is the `iss` claim?**
A: The `iss` (issuer) claim identifies who created the token. It's used to ensure tokens from untrusted sources are rejected.

### Intermediate (5-10)

**Q11: How would you implement token revocation?**
A: Maintain a blacklist in Redis or a database. When a user logs out, store the token's JTI (unique ID) in the blacklist with an expiration matching the token's lifetime. Check the blacklist on each request.

**Q12: What is token rotation and why is it important?**
A: Token rotation means issuing a new refresh token each time one is used. This limits the window of opportunity if a refresh token is compromised, as each token can only be used once.

**Q13: How do you handle JWT in microservices?**
A: Use RS256 with the auth server signing tokens and services verifying with the public key. Each service validates the token independently without calling the auth server.

**Q14: What are impersonation attacks and how do you prevent them?**
A: An attacker uses a stolen token to impersonate a user. Prevent with short expiration times, refresh token rotation, and token binding to specific devices/IPs.

**Q15: How do you validate JWT claims?**
A: Always validate: `iss` (issuer), `aud` (audience), `exp` (expiration), `nbf` (not before), and `iat` (issued at). Also validate custom claims like roles.

**Q16: What is a JWT jti claim?**
A: The `jti` (JWT ID) is a unique identifier for the token. It's used for token revocation and to prevent replay attacks.

**Q17: How do you handle JWT in server-side rendering?**
A: In SSR, you can store JWT in httpOnly cookies and have the server read the cookie directly. The browser sends the cookie automatically with requests.

**Q18: What is the difference between authentication and authorization in JWT context?**
A: Authentication is proving identity (validating the token and its signature). Authorization is checking if the authenticated user has permission for a specific action (checking roles/permissions in claims).

**Q19: How do you handle JWT across multiple domains?**
A: Use a centralized auth server that issues tokens. Services across domains validate the token using the public key. CORS must be configured to allow cross-origin requests.

**Q20: What are the security implications of JWT payload being base64-encoded?**
A: Base64 encoding is not encryption. Anyone can decode the payload and read the claims. Never store sensitive data like passwords, SSNs, or private information in JWT payloads.

### Senior (10-15)

**Q21: Design a token revocation system for a distributed system with 100+ microservices.**
A: Use a centralized blacklist stored in Redis Cluster. When a token is revoked, publish the JTI to all services. Each service maintains a local cache of recently revoked tokens (with TTL). For real-time revocation, use Redis Pub/Sub or a message queue.

**Q22: How would you implement device-bound tokens?**
A: Bind tokens to device fingerprints (derived from User-Agent, IP, device characteristics). During validation, recompute the fingerprint and compare. For higher security, use hardware-bound keys (WebAuthn, TPM).

**Q23: Explain the trade-offs between short-lived tokens with refresh tokens vs long-lived tokens with revocation.**
A: Short-lived tokens are more secure (limited exposure if stolen) but increase network overhead. Long-lived tokens with revocation reduce network overhead but require infrastructure for revocation checks. The refresh token approach is generally preferred for web applications.

**Q24: How do you prevent token replay attacks?**
A: Use the `jti` claim to track used tokens, enforce short expiration times, implement nonce-based validation, and use token binding to specific clients or sessions.

**Q25: What are the security considerations when implementing JWT in a multi-tenant system?**
A: Ensure tenant isolation through claims, validate tenant context on every request, implement tenant-specific signing keys if needed, and audit token usage per tenant.

**Q26: How would you migrate from session-based auth to JWT without downtime?**
A: Run both systems in parallel. Validate tokens against both the session store and JWT. Gradually migrate services to JWT-first validation. Finally, remove session-based code once all services are migrated.

**Q27: Explain how to implement JWT for machine-to-machine authentication.**
A: Use OAuth 2.0 client credentials flow. The client authenticates with client_id and client_secret, receives a JWT with machine identity claims. Services validate the JWT and check machine-level permissions.

**Q28: How do you audit and monitor JWT usage?**
A: Log token issuance, validation, and revocation events. Monitor for anomalies (unusual IP patterns, multiple token usage). Implement alerting for suspicious patterns. Use centralized logging with correlation IDs.

**Q29: What is token introspection and when should you use it?**
A: Token introspection (RFC 7662) is an endpoint that validates a token by querying the authorization server. Use it when the token format is opaque or when real-time revocation checking is required.

**Q30: How do you handle JWT in environments where HTTPS is not guaranteed?**
A: Don't use JWT in untrusted networks. If HTTPS is unavailable, use additional payload encryption (JWE), implement channel binding, and ensure the signing algorithm provides integrity protection.

### FAANG-style (5-10)

**Q31: Design a JWT system that supports real-time revocation across 10,000 servers with < 100ms latency.**
A: Use a Redis Cluster with consistent hashing for JTI storage. Implement a local cache with 30-second TTL on each server. Use Redis Pub/Sub for real-time revocation propagation. For 99.999% availability, replicate across multiple regions.

**Q32: How would you implement a secure JWT-based API gateway handling 1 million requests per second?**
A: Cache public keys in memory (RS256). Use asynchronous verification for non-critical paths. Implement circuit breakers for downstream services. Use connection pooling and keep-alive for token introspection endpoints.

**Q33: Explain how to design a JWT system that's resistant to quantum computing attacks.**
A: Use post-quantum cryptographic algorithms for signing (e.g., CRYSTALS-Dilithium). Implement hybrid signatures (classical + post-quantum). Plan for algorithm agility to migrate as standards evolve.

**Q34: How would you handle JWT in a zero-trust architecture?**
A: Validate tokens on every request, not just at the perimeter. Implement token binding to mTLS sessions. Use short-lived tokens with continuous validation. Implement just-in-time access with token scoping.

**Q35: Design a system where JWT tokens can be shared between organizations while maintaining security.**
A: Implement cross-organization trust chains using JWT federation. Use JWKS (JSON Web Key Set) endpoints for key discovery. Implement consent-based sharing with granular scopes. Audit all cross-org token usage.

### Follow-ups (5-10)

**Q36: What would you do differently if JWT tokens needed to carry user preferences and settings?**
A: Store only essential claims (userId, roles, tenantId) in the JWT. Fetch preferences from a dedicated service or cache (Redis). JWTs should be minimal for security and performance.

**Q37: How would your design change if you needed to support both web and IoT devices?**
A: Implement different token types: standard JWT for web, hardware-bound JWT for IoT. Use different signing algorithms (RS256 for web, ECDSA for IoT). Implement device registration and binding.

**Q38: If the security team required all tokens to be encrypted, how would you implement JWE?**
A: Use JWE (JSON Web Encryption) for the payload. Encrypt with the recipient's public key. The header contains the encrypted key, IV, and ciphertext. This adds computational overhead but protects sensitive claims.

**Q39: How would you handle JWT in a Kubernetes environment with service mesh?**
A: Use SPIFFE/SPIRE for workload identity. Implement JWT validation at the sidecar proxy level. Use mTLS between services with JWT for user context. Rotate signing keys using Kubernetes Secrets.

**Q40: If performance metrics showed JWT verification was a bottleneck, what optimizations would you apply?**
A: Cache public keys in-memory. Use HMAC for internal services where asymmetric isn't needed. Implement token pre-validation at the edge. Use hardware acceleration for cryptographic operations. Consider token introspection caching.

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

## References & Learn More

- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [JWT.io - Introduction to JSON Web Tokens](https://jwt.io/introduction/)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [Auth0 JWT Documentation](https://auth0.com/docs/secure/tokens/json-web-tokens)
- [RFC 7517 - JSON Web Key (JWK)](https://datatracker.ietf.org/doc/html/rfc7517)
- [Understanding JWT Security - Auth0 Blog](https://auth0.com/blog/json-web-token-security-what-you-need-to-know/)
