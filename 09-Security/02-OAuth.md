[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

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

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OAuth 2.0 - RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [OAuth 2.0 for Browser-Based Apps](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-browser-based-apps)
- [OpenID Connect Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 Simplified - Aaron Parecki](https://aaronparecki.com/oauth-2-simplified/)
- [Auth0 OAuth Documentation](https://auth0.com/docs/authenticate/protocols/oauth)
