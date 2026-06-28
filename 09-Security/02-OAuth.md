# OAuth 2.0

## Definition

OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user resources on a third-party service without exposing the user's credentials. It is defined by RFC 6749 and provides a standardized protocol for delegated authorization. OAuth 2.0 separates the roles of resource owner, client, authorization server, and resource server, enabling secure delegated access.

OAuth 2.0 is NOT an authentication protocol — it's an authorization protocol. OpenID Connect (OIDC) extends OAuth 2.0 to provide authentication.

## Why Do We Need It?

- **Credential Separation**: Users never share passwords with third-party applications
- **Granular Access Control**: Users can grant limited permissions (scopes)
- **Revocable Access**: Users can revoke access without changing passwords
- **Standard Protocol**: Universal standard supported by all major platforms
- **Delegated Authorization**: Applications can act on behalf of users
- **Mobile/SPA Support**: Designed for modern application architectures

## How It Works

### OAuth 2.0 Roles

```text
┌─────────────────────────────────────────────────────────────┐
│                    OAuth 2.0 Roles                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Resource Owner ──────> Client ──────> Authorization Server │
│  (User)           (App)              (Issues Tokens)        │
│                        │                                     │
│                        v                                     │
│                  Resource Server                             │
│                  (Stores Resources)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Authorization Code Flow

```text
┌──────────┐          ┌──────────┐          ┌──────────────────┐
│  User    │          │  Client  │          │ Authorization    │
│  (RO)    │          │  (App)   │          │ Server           │
└────┬─────┘          └────┬─────┘          └────────┬─────────┘
     │                     │                         │
     │  1. Click "Login    │                         │
     │     with Provider"  │                         │
     │────────────────────>│                         │
     │                     │                         │
     │                     │  2. Redirect to         │
     │                     │     authorization       │
     │                     │     endpoint            │
     │  3. Login &         │                         │
     │     consent screen  │                         │
     │<────────────────────│────────────────────────>│
     │                     │                         │
     │  4. User approves   │                         │
     │──────────────────────────────────────────────>│
     │                     │                         │
     │                     │  5. Authorization code  │
     │                     │     returned            │
     │                     │<────────────────────────│
     │                     │                         │
     │                     │  6. Exchange code for   │
     │                     │     tokens              │
     │                     │────────────────────────>│
     │                     │                         │
     │                     │  7. Access + Refresh    │
     │                     │     tokens              │
     │                     │<────────────────────────│
     │                     │                         │
     │                     │  8. Use token to        │
     │                     │     access resource     │
     │                     │────────────────────>│
     │                     │                    │
     │                     │  9. Protected      │
     │                     │     resource       │
     │                     │<───────────────────│
```

### PKCE Flow (for Public Clients)

```text
┌──────────┐          ┌──────────┐          ┌──────────────────┐
│  User    │          │  Client  │          │ Authorization    │
│          │          │  (SPA)   │          │ Server           │
└────┬─────┘          └────┬─────┘          └────────┬─────────┘
     │                     │                         │
     │                     │  1. Generate code_verifier
     │                     │     & code_challenge     │
     │                     │                         │
     │                     │  2. /authorize?          │
     │                     │     code_challenge=xxx   │
     │                     │     code_challenge_      │
     │                     │     method=S256          │
     │                     │────────────────────────>│
     │                     │                         │
     │                     │  3. Authorization code   │
     │                     │<────────────────────────│
     │                     │                         │
     │                     │  4. /token               │
     │                     │     code=xxx             │
     │                     │     code_verifier=yyy    │
     │                     │────────────────────────>│
     │                     │                         │
     │                     │  5. Access token         │
     │                     │<────────────────────────│
```

## Code Examples

### Authorization Code Flow Implementation (TypeScript)

```typescript
import crypto from "crypto";

interface OAuthConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  authorizationEndpoint: string;
  tokenEndpoint: string;
  scopes: string[];
}

interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  scope?: string;
}

interface PKCEChallenge {
  codeVerifier: string;
  codeChallenge: string;
}

// PKCE Helper Functions
const generatePKCEChallenge = (): PKCEChallenge => {
  const codeVerifier = crypto.randomBytes(32).toString("base64url");
  const codeChallenge = crypto
    .createHash("sha256")
    .update(codeVerifier)
    .digest("base64url");

  return { codeVerifier, codeChallenge };
};

// Build Authorization URL
const buildAuthorizationUrl = (
  config: OAuthConfig,
  state: string,
  pkce?: PKCEChallenge
): string => {
  const params = new URLSearchParams({
    response_type: "code",
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    scope: config.scopes.join(" "),
    state,
  });

  if (pkce) {
    params.set("code_challenge", pkce.codeChallenge);
    params.set("code_challenge_method", "S256");
  }

  return `${config.authorizationEndpoint}?${params.toString()}`;
};

// Exchange Authorization Code for Tokens
const exchangeCodeForTokens = async (
  config: OAuthConfig,
  code: string,
  codeVerifier?: string
): Promise<TokenResponse> => {
  const body: Record<string, string> = {
    grant_type: "authorization_code",
    code,
    redirect_uri: config.redirectUri,
    client_id: config.clientId,
  };

  if (config.clientSecret) {
    body.client_secret = config.clientSecret;
  }

  if (codeVerifier) {
    body.code_verifier = codeVerifier;
  }

  const response = await fetch(config.tokenEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams(body).toString(),
  });

  if (!response.ok) {
    throw new Error(`Token exchange failed: ${response.statusText}`);
  }

  return response.json();
};

// Refresh Access Token
const refreshAccessToken = async (
  config: OAuthConfig,
  refreshToken: string
): Promise<TokenResponse> => {
  const response = await fetch(config.tokenEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: refreshToken,
      client_id: config.clientId,
      client_secret: config.clientSecret,
    }).toString(),
  });

  if (!response.ok) {
    throw new Error(`Token refresh failed: ${response.statusText}`);
  }

  return response.json();
};
```

### OAuth 2.0 Express Middleware

```typescript
import { Request, Response, NextFunction } from "express";

interface OAuthSession {
  accessToken: string;
  refreshToken?: string;
  expiresAt: number;
  scopes: string[];
}

class OAuthMiddleware {
  private sessions: Map<string, OAuthSession> = new Map();

  async authenticate(
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> {
    const sessionId = req.cookies?.sessionId;
    const session = sessionId ? this.sessions.get(sessionId) : null;

    if (!session) {
      res.status(401).json({ error: "Authentication required" });
      return;
    }

    // Check if token is expired
    if (Date.now() >= session.expiresAt) {
      // Try to refresh
      if (session.refreshToken) {
        try {
          const newTokens = await refreshAccessToken(
            oauthConfig,
            session.refreshToken
          );

          this.sessions.set(sessionId, {
            accessToken: newTokens.access_token,
            refreshToken: newTokens.refresh_token || session.refreshToken,
            expiresAt: Date.now() + newTokens.expires_in * 1000,
            scopes: newTokens.scope?.split(" ") || [],
          });

          req.oauthToken = newTokens.access_token;
          next();
          return;
        } catch (error) {
          this.sessions.delete(sessionId);
          res.status(401).json({ error: "Token refresh failed" });
          return;
        }
      }

      res.status(401).json({ error: "Token expired" });
      return;
    }

    req.oauthToken = session.accessToken;
    next();
  }

  requireScope(scope: string) {
    return (req: Request, res: Response, next: NextFunction): void => {
      const sessionId = req.cookies?.sessionId;
      const session = sessionId ? this.sessions.get(sessionId) : null;

      if (!session?.scopes.includes(scope)) {
        res.status(403).json({ error: `Scope '${scope}' required` });
        return;
      }

      next();
    };
  }
}

// Usage
const oauth = new OAuthMiddleware();

app.get(
  "/api/photos",
  oauth.authenticate,
  oauth.requireScope("photos:read"),
  (req, res) => {
    // Access photos with req.oauthToken
  }
);
```

### GitHub OAuth Integration Example

```typescript
import express from "express";

const GITHUB_CONFIG: OAuthConfig = {
  clientId: process.env.GITHUB_CLIENT_ID!,
  clientSecret: process.env.GITHUB_CLIENT_SECRET!,
  redirectUri: "http://localhost:3000/auth/github/callback",
  authorizationEndpoint: "https://github.com/login/oauth/authorize",
  tokenEndpoint: "https://github.com/login/oauth/access_token",
  scopes: ["user:email", "repo"],
};

const app = express();

// Step 1: Initiate OAuth flow
app.get("/auth/github", (req, res) => {
  const state = crypto.randomBytes(16).toString("hex");
  const { codeVerifier, codeChallenge } = generatePKCEChallenge();

  // Store state and codeVerifier in session
  req.session = { state, codeVerifier };

  const authUrl = buildAuthorizationUrl(GITHUB_CONFIG, state, { codeVerifier, codeChallenge });
  res.redirect(authUrl);
});

// Step 2: Handle callback
app.get("/auth/github/callback", async (req, res) => {
  const { code, state } = req.query;

  if (state !== req.session?.state) {
    return res.status(403).json({ error: "Invalid state parameter" });
  }

  try {
    const tokens = await exchangeCodeForTokens(
      GITHUB_CONFIG,
      code as string,
      req.session.codeVerifier
    );

    req.session.accessToken = tokens.access_token;
    req.session.expiresAt = Date.now() + tokens.expires_in * 1000;

    res.redirect("/dashboard");
  } catch (error) {
    res.status(500).json({ error: "OAuth authentication failed" });
  }
});
```

## Real-World Use Cases

### 1. Social Login
- "Sign in with Google/GitHub/Facebook"
- User grants access to basic profile information
- Application doesn't store or handle user passwords

### 2. API Access (Machine-to-Machine)
- Server-to-server communication using Client Credentials flow
- No user involvement; service authenticates directly
- Used for backend services, cron jobs, microservices

### 3. Third-Party Integrations
- Accessing user's Google Drive, Dropbox, or GitHub repos
- Granular scope-based permissions
- User can revoke access at any time

### 4. Mobile Applications
- Authorization Code flow with PKCE (no client secret on device)
- Tokens stored in secure storage (Keychain/Keystore)
- Refresh tokens for seamless session management

### 5. SPA + API Architecture
- Authorization Code flow with PKCE
- Tokens stored in httpOnly cookies or memory
- API validates tokens on each request

## Common Mistakes

1. **Using implicit flow**: Deprecated due to token exposure in URL fragments. Use Authorization Code with PKCE.

2. **Not validating the `state` parameter**: Enables CSRF attacks. Always generate, store, and validate state.

3. **Storing client_secret in frontend code**: Exposes the secret to attackers. Only use in server-side applications.

4. **Not requesting minimal scopes**: Request only the scopes needed. Excessive scopes violate the principle of least privilege.

5. **Ignoring token expiration**: Not checking token expiry leads to failed API calls and poor UX.

6. **Not using PKCE for public clients**: PKCE prevents authorization code interception attacks.

7. **Sharing tokens between users**: Each user should have their own token. Sharing tokens compromises audit trails and security.

8. **Not implementing token revocation**: Without revocation, compromised tokens remain valid until expiry.

## Best Practices

1. **Always use Authorization Code flow with PKCE** for public clients (SPA, mobile)
2. **Validate the `state` parameter** to prevent CSRF attacks
3. **Request minimal scopes** — only what's needed
4. **Store tokens securely**: httpOnly cookies for web, secure storage for mobile
5. **Implement refresh token rotation** with single-use tokens
6. **Validate all token claims** (issuer, audience, expiration)
7. **Use short-lived access tokens** (15 minutes or less)
8. **Implement token revocation** for logout
9. **Log and monitor** OAuth usage for anomaly detection
10. **Keep client secrets secure** — never expose in client-side code

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Token Exchange | Network round-trip to auth server adds latency |
| Token Caching | Cache tokens locally to reduce network calls |
| Token Validation | JWT validation is fast; introspection adds latency |
| PKCE | Slight overhead for challenge generation, negligible |
| Refresh Flow | Additional network request when tokens expire |

## Interview Questions

### Beginner (5-10)

**Q1: What is OAuth 2.0 and how does it differ from authentication?**
A: OAuth 2.0 is an authorization framework for delegated access. It lets users grant third-party apps limited access to their resources without sharing credentials. Authentication verifies identity; OAuth 2.0 grants permissions. OpenID Connect extends OAuth 2.0 for authentication.

**Q2: What are the four roles in OAuth 2.0?**
A: Resource Owner (user), Client (application), Authorization Server (issues tokens), and Resource Server (hosts protected resources).

**Q3: What is the Authorization Code flow?**
A: A flow where the client redirects the user to the authorization server, the user authenticates and consents, the server returns an authorization code, and the client exchanges the code for tokens on the server side.

**Q4: What is PKCE and why is it needed?**
A: Proof Key for Code Exchange (RFC 7636) prevents authorization code interception attacks. The client generates a code verifier, sends a challenge (hash), and proves possession during token exchange. Required for public clients.

**Q5: What is the difference between access and refresh tokens?**
A: Access tokens are short-lived credentials for API access. Refresh tokens are long-lived credentials used to obtain new access tokens without user interaction.

**Q6: What are scopes in OAuth 2.0?**
A: Scopes define the specific permissions a client is requesting. They allow fine-grained access control (e.g., "read:email", "write:repos").

**Q7: What is the `state` parameter used for?**
A: The `state` parameter is a random value used to prevent CSRF attacks. The client generates it, stores it, and verifies it when the authorization server redirects back.

**Q8: What is the Client Credentials flow?**
A: A machine-to-machine flow where the client authenticates with its own credentials (client_id + client_secret) and receives an access token without user involvement.

**Q9: What is the Implicit flow?**
A: A deprecated flow where the access token is returned directly in the URL fragment. It was used for SPAs but has been replaced by Authorization Code + PKCE due to security concerns.

**Q10: What is token introspection?**
A: An endpoint (RFC 7662) that validates a token by querying the authorization server. Useful for opaque tokens or when real-time revocation checking is needed.

### Intermediate (5-10)

**Q11: How would you implement OAuth 2.0 for a Single Page Application?**
A: Use Authorization Code flow with PKCE. Store tokens in httpOnly cookies (for API calls) or memory (for SPA access). Use refresh token rotation. Never store tokens in localStorage.

**Q12: How do you handle token refresh in a concurrent request scenario?**
A: Implement a token refresh queue. When a token expires, queue all pending requests, refresh the token once, and retry all queued requests with the new token.

**Q13: What is the difference between JWT and opaque tokens?**
A: JWTs are self-contained with claims; validation is local. Opaque tokens are random strings; validation requires a network call to the authorization server (introspection).

**Q14: How do you handle logout in OAuth 2.0?**
A: Revoke the refresh token (invalidates future access), clear tokens from the client, and optionally call the authorization server's revocation endpoint (RFC 7009).

**Q15: What are the security implications of the authorization code flow?**
A: The authorization code can be intercepted. PKCE mitigates this by ensuring only the client that initiated the flow can exchange the code. Always use PKCE for public clients.

**Q16: How do you handle multiple redirect URIs?**
A: The redirect URI must exactly match (case-sensitive) what's registered with the authorization server. Avoid wildcards. Use separate registrations for different environments.

**Q17: What is the difference between bearer and proof-of-possession tokens?**
A: Bearer tokens grant access to anyone who presents them. Proof-of-possession tokens require the client to prove possession of a cryptographic key, preventing token theft.

**Q18: How do you implement OAuth 2.0 for a microservices architecture?**
A: Use an API gateway to handle OAuth validation. Services receive validated user context from the gateway. Use client credentials flow for service-to-service communication.

**Q19: What is the OAuth 2.0 Token Revocation endpoint?**
A: An endpoint (RFC 7009) that allows clients to invalidate tokens. Supports revoking access tokens and/or refresh tokens. Essential for logout and security incidents.

**Q20: How do you handle OAuth errors?**
A: Follow RFC 6749 error format: return appropriate error codes (invalid_grant, unauthorized_client, etc.) with descriptive messages. Log errors for monitoring but don't expose internal details.

### Senior (10-15)

**Q21: Design an OAuth 2.0 system for a platform with 50+ microservices.**
A: Centralized authorization server issues JWTs. API gateway validates tokens. Services trust the gateway and receive user context via headers. Use RS256 for signing. Implement token introspection at the gateway. Use Redis for revocation lists.

**Q22: How would you implement OAuth 2.0 for a B2B platform with different tenant configurations?**
A: Implement tenant-aware authorization. Each tenant has its own OAuth client configuration, scopes, and policies. Use JWT claims to carry tenant context. Implement tenant-specific token signing if needed.

**Q23: Explain how to implement a secure OAuth 2.0 consent management system.**
A: Store consent records per user, per client, per scope. Implement consent revocation UI. On each authorization request, check existing consent. Request incremental consent for new scopes. Audit consent changes.

**Q24: How would you handle OAuth 2.0 in a zero-trust environment?**
A: Validate tokens on every request. Implement proof-of-possession tokens. Bind tokens to client certificates (mTLS). Use short-lived tokens. Implement continuous authorization (re-validate periodically).

**Q25: Design a system for cross-domain OAuth 2.0 with shared user base.**
A: Use centralized identity provider with OAuth 2.0 federation. Implement trust relationships between domains. Use JWT claims for domain context. Implement domain-specific authorization policies.

**Q26: How would you handle OAuth 2.0 for IoT devices with limited capabilities?**
A: Use device authorization flow for input-constrained devices. Implement device code grant. Use hardware security modules for key storage. Implement certificate-based client authentication.

**Q27: Explain how to implement OAuth 2.0 token binding for enhanced security.**
A: Bind tokens to TLS channel (DPoP - Demonstrating Proof of Possession). Bind tokens to client certificate (mTLS). Bind tokens to device fingerprint. Validate binding on each request.

**Q28: How would you implement OAuth 2.0 with just-in-time access provisioning?**
A: On authorization, check if user has required permissions. If not, trigger access request workflow. Implement approval chains. Grant temporary access with expiration. Implement access review cycles.

**Q29: Design an OAuth 2.0 system that supports both web and API access patterns.**
A: Use Authorization Code flow with PKCE for web. Use client credentials for API access. Issue different token types (JWT for API, opaque for web). Implement token exchange (RFC 8693) for delegation.

**Q30: How would you handle OAuth 2.0 in a multi-region deployment?**
A: Replicate authorization server across regions. Use global session management. Implement region-aware token validation. Handle cross-region token exchange. Ensure consistency of revocation lists.

### FAANG-style (5-10)

**Q31: Design an OAuth 2.0 system supporting 1 billion daily active users.**
A: Horizontally scale authorization servers. Use distributed token storage (Redis Cluster). Implement token caching at edge (CDN). Use async revocation propagation. Implement rate limiting per client. Monitor for abuse patterns.

**Q32: How would you implement OAuth 2.0 for a financial institution with regulatory requirements?**
A: Implement step-up authentication for sensitive operations. Use FIDO2/WebAuthn for strong client authentication. Implement transaction signing. Maintain comprehensive audit logs. Implement consent with legal requirements.

**Q33: Design a system for OAuth 2.0 token sharing between competing organizations.**
A: Implement trust federation with standardized metadata exchange. Use signed JWT assertions for cross-org authentication. Implement fine-grained scope negotiation. Audit all cross-org token usage.

**Q34: How would you migrate from OAuth 2.0 to a new protocol without breaking existing clients?**
A: Implement protocol versioning. Support both protocols simultaneously. Use token exchange to bridge old and new systems. Implement gradual client migration with feature flags.

**Q35: Design an OAuth 2.0 system that provides real-time access analytics across 100+ services.**
A: Implement centralized logging with correlation IDs. Use event streaming (Kafka) for token usage events. Implement real-time dashboards. Build anomaly detection models. Implement automated alerting.

### Follow-ups (5-10)

**Q36: How would your design change if you needed to support OAuth 2.0 for both B2C and B2B use cases?**
A: B2C: Authorization Code flow with social login support. B2B: Client credentials with SAML federation. Implement separate client registrations and policies per use case. Use consistent token format but different claim sets.

**Q37: If the security team required all tokens to be encrypted, how would you implement JWE?**
A: Use JWE for token payloads. Implement key management service for encryption keys. Handle key rotation. Ensure backward compatibility during migration. Performance impact: additional encryption/decryption overhead.

**Q38: How would you implement OAuth 2.0 for a system requiring audit trails for every access?**
A: Implement comprehensive logging of all token issuance and usage. Use JWT claims to carry audit context. Implement centralized audit storage. Build compliance reporting. Implement tamper-evident audit logs.

**Q39: If OAuth 2.0 token validation was a performance bottleneck, what optimizations would you apply?**
A: Cache public keys. Use JWT for self-contained validation. Implement token validation at edge. Use hardware acceleration. Implement async validation for non-critical paths.

**Q40: How would you handle OAuth 2.0 in environments where the authorization server is temporarily unavailable?**
A: Implement token caching with grace periods. Use last-valid token within acceptable window. Implement fallback authorization. Monitor authorization server health. Implement circuit breakers.

## Summary

OAuth 2.0 is the standard framework for delegated authorization, enabling secure third-party access without sharing credentials. Key takeaways:

- Authorization Code flow with PKCE is the gold standard for most use cases
- Always validate the `state` parameter to prevent CSRF
- Use short-lived access tokens with refresh token rotation
- Store tokens securely (httpOnly cookies, secure storage)
- Request minimal scopes
- Implement token revocation for security
- OAuth 2.0 is authorization, not authentication (use OIDC for auth)

## Cheat Sheet

| Concept | Recommendation |
|---------|---------------|
| Flow (Web App) | Authorization Code + PKCE |
| Flow (SPA) | Authorization Code + PKCE |
| Flow (Mobile) | Authorization Code + PKCE |
| Flow (M2M) | Client Credentials |
| Access Token Lifetime | 15 minutes |
| Refresh Token Lifetime | 7 days |
| State Parameter | Always use for CSRF prevention |
| PKCE | Always use for public clients |
| Scopes | Request minimal required scopes |
| Token Storage (Web) | httpOnly, Secure, SameSite cookies |
| Token Storage (Mobile) | Keychain (iOS) / Keystore (Android) |
| Logout | Revoke refresh token + clear client tokens |

## References & Learn More

- [OAuth 2.0 - RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [OAuth 2.0 for Browser-Based Apps](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-browser-based-apps)
- [OpenID Connect Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 Simplified - Aaron Parecki](https://aaronparecki.com/oauth-2-simplified/)
- [Auth0 OAuth Documentation](https://auth0.com/docs/get-started/auth0-overview/oauth)
