# Cross-Site Request Forgery (CSRF)

## Definition

Cross-Site Request Forgery (CSRF) is a web security vulnerability that forces an authenticated user to execute unwanted actions on a web application in which they're authenticated. Unlike XSS, which injects malicious scripts, CSRF tricks the user's browser into making unintended requests using the user's existing session. The attacker exploits the trust that a site has in the user's browser.

CSRF attacks target state-changing operations (not data retrieval) and rely on the fact that browsers automatically include credentials (cookies, HTTP auth) with cross-origin requests.

## Why Do We Need It?

- **Session Hijacking**: Attackers can perform actions using the victim's authenticated session
- **State Changes**: CSRF can trigger unwanted state changes (transfers, password changes, account modifications)
- **Financial Impact**: Can lead to unauthorized transactions or purchases
- **Reputation Damage**: Users may lose trust in the application
- **Compliance Violations**: May violate security standards (PCI DSS, GDPR)

## How It Works

### Attack Flow

```text
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│ Attacker │                    │  Victim  │                    │  Server  │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Victim logs into bank.com │                               │
     │                               │──────────────────────────────>│
     │                               │                               │
     │                    2. Session cookie set                       │
     │                               │<──────────────────────────────│
     │                               │                               │
     │  3. Victim visits attacker's  │                               │
     │     malicious page            │                               │
     │                               │                               │
     │  4. Malicious page contains:  │                               │
     │     <form action="bank.com/   │                               │
     │       transfer" method="POST">│                               │
     │     <input name="to" value=   │                               │
     │       "attacker">             │                               │
     │     <input name="amount"      │                               │
     │       value="10000">          │                               │
     │     </form>                   │                               │
     │     <script>form.submit()     │                               │
     │     </script>                 │                               │
     │                               │                               │
     │  5. Browser sends POST        │                               │
     │     with session cookie       │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                    6. Server validates session                 │
     │                    7. Transfer executes                        │
     │                               │                               │

```

### Same-Origin Policy and CSRF

```text
┌─────────────────────────────────────────────────────────────────┐
│              Same-Origin Policy & CSRF                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Origin: https://bank.com                                       │
│                                                                 │
│  ✅ Same Origin:                                               │
│     https://bank.com/dashboard                                  │
│     https://bank.com/api/transfer                               │
│                                                                 │
│  ❌ Cross Origin:                                              │
│     https://evil.com/steal                                      │
│     http://bank.com (different scheme)                          │
│     https://sub.bank.com (different host)                       │
│                                                                 │
│  CSRF Exploits:                                                 │
│     - Cookies are sent with cross-origin requests               │
│     - Forms can submit to any origin                            │
│     - Images can trigger GET requests                           │
│     - JavaScript can make cross-origin requests (with CORS)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Vulnerable Code

```typescript
// ❌ VULNERABLE: No CSRF protection on state-changing endpoint
app.post("/api/transfer", async (req, res) => {
  const { to, amount } = req.body;
  const userId = req.session.userId;

  // Attacker can force user to make this transfer
  await db.transfer(userId, to, amount);
  res.json({ success: true });
});

// ❌ VULNERABLE: GET request for state-changing operation
app.get("/api/delete-account", async (req, res) => {
  const userId = req.session.userId;
  await db.deleteUser(userId);
  res.json({ success: true });
});

```

### CSRF Protection Implementation

```typescript
import crypto from "crypto";
import express from "express";

// 1. CSRF Token Generation and Validation
class CSRFProtection {
  private secret: string;

  constructor(secret: string) {
    this.secret = secret;
  }

  generateToken(sessionId: string): string {
    const timestamp = Date.now().toString();
    const data = `${sessionId}:${timestamp}`;
    const signature = crypto
      .createHmac("sha256", this.secret)
      .update(data)
      .digest("hex");
    return Buffer.from(`${timestamp}:${signature}`).toString("base64url");
  }

  validateToken(token: string, sessionId: string): boolean {
    try {
      const decoded = Buffer.from(token, "base64url").toString();
      const [timestamp, signature] = decoded.split(":");

      // Check token age (5 minutes)
      const tokenAge = Date.now() - parseInt(timestamp);
      if (tokenAge > 5 * 60 * 1000) {
        return false;
      }

      // Verify signature
      const data = `${sessionId}:${timestamp}`;
      const expectedSignature = crypto
        .createHmac("sha256", this.secret)
        .update(data)
        .digest("hex");

      return signature === expectedSignature;
    } catch {
      return false;
    }
  }
}

// 2. CSRF Middleware
const csrfProtection = new CSRFProtection(process.env.CSRF_SECRET!);

const csrfMiddleware = (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): void => {
  if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method)) {
    const token =
      req.headers["x-csrf-token"] as string ||
      req.body?._csrf as string;

    if (!token || !csrfProtection.validateToken(token, req.session.id)) {
      res.status(403).json({ error: "Invalid CSRF token" });
      return;
    }
  }
  next();
};

// 3. Double Submit Cookie Pattern
class DoubleSubmitCSRF {
  generateToken(): string {
    return crypto.randomBytes(32).toString("hex");
  }

  setCookie(res: express.Response, token: string): void {
    res.cookie("csrf_token", token, {
      httpOnly: false, // JavaScript needs to read this
      secure: true,
      sameSite: "strict",
    });
  }

  validate(req: express.Request): boolean {
    const cookieToken = req.cookies?.csrf_token;
    const headerToken = req.headers["x-csrf-token"] as string;

    if (!cookieToken || !headerToken) {
      return false;
    }

    // Timing-safe comparison
    return crypto.timingSafeEqual(
      Buffer.from(cookieToken),
      Buffer.from(headerToken)
    );
  }
}

// 4. Usage
const app = express();
const doubleSubmit = new DoubleSubmitCSRF();

app.get("/api/csrf-token", (req, res) => {
  const token = doubleSubmit.generateToken();
  doubleSubmit.setCookie(res, token);
  res.json({ csrfToken: token });
});

app.post("/api/transfer", csrfMiddleware, async (req, res) => {
  // Transfer logic
  res.json({ success: true });
});

// 5. SameSite Cookie Configuration
app.use(
  express-session({
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      sameSite: "strict", // Prevents CSRF
      maxAge: 15 * 60 * 1000, // 15 minutes
    },
  })
);

```

### React CSRF Implementation

```typescript
// Frontend: CSRF Token Fetcher
import { useEffect, useState } from "react";

function useCSRFToken() {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/csrf-token", { credentials: "include" })
      .then((res) => res.json())
      .then((data) => setCsrfToken(data.csrfToken));
  }, []);

  return csrfToken;
}

// API client with CSRF protection
const apiClient = {
  async post(url: string, data: any) {
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrf_token="))
      ?.split("=")[1];

    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfToken || "",
      },
      credentials: "include",
      body: JSON.stringify(data),
    });
  },
};

// Usage in component
function TransferForm() {
  const csrfToken = useCSRFToken();

  const handleSubmit = async (data: TransferData) => {
    const response = await apiClient.post("/api/transfer", {
      ...data,
      _csrf: csrfToken,
    });
  };
}

```

## Real-World Use Cases

### 1. Banking Applications

- Transfer requests must be protected against CSRF
- Password changes require CSRF tokens
- Account modifications need verification

### 2. E-commerce Sites

- Purchase orders must be CSRF-protected
- Cart modifications require protection
- Address and payment changes need CSRF tokens

### 3. Social Media Platforms

- Posting, liking, and sharing require CSRF protection
- Profile updates need CSRF tokens
- Account settings changes must be protected

### 4. Admin Dashboards

- All state-changing operations require CSRF protection
- User management operations need CSRF tokens
- Configuration changes must be protected

## Common Mistakes

1. **Using GET for state-changing operations**: GET requests should be idempotent; use POST for state changes

2. **Not implementing CSRF protection**: Every state-changing endpoint needs protection

3. **Using SameSite=None without CSRF tokens**: SameSite cookies don't protect all scenarios

4. **Not validating CSRF tokens**: Must validate on every state-changing request

5. **Storing CSRF tokens in localStorage**: Tokens should be in httpOnly cookies or session

6. **Not protecting API endpoints**: APIs need CSRF protection too

7. **Using predictable CSRF tokens**: Always use cryptographically random tokens

8. **Not invalidating CSRF tokens after use**: Single-use tokens are more secure

## Best Practices

1. **Use SameSite cookies** (Strict or Lax) as first line of defense

2. **Implement CSRF tokens** for all state-changing operations

3. **Use Double Submit Cookie** pattern for SPAs

4. **Validate CSRF tokens** with timing-safe comparison

5. **Use POST** for all state-changing operations

6. **Set CSRF token expiration** (5-15 minutes)

7. **Rotate CSRF tokens** after login/logout

8. **Implement Content Security Policy** to limit script execution

9. **Use HTTPS** to prevent token interception
10. **Validate Origin and Referer headers** as additional protection

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Token Generation | Minimal overhead (HMAC operation) |
| Token Validation | Fast operation, can be cached |
| Cookie Overhead | Negligible additional cookie size |
| Network Overhead | Extra header per request |
| Memory Usage | Token storage is minimal |

## Interview Questions

### Beginner (5-10)

**Q1: What is CSRF and how does it work?**
A: CSRF forces an authenticated user to perform unwanted actions on a web application. Attackers trick users into making requests using their existing session cookies. The browser automatically includes cookies with requests, so the server can't distinguish between legitimate and forged requests.

**Q2: What is the difference between XSS and CSRF?**
A: XSS injects malicious scripts that execute in the user's browser. CSRF tricks the user's browser into making unintended requests. XSS steals data; CSRF performs actions. XSS doesn't require the user to be authenticated; CSRF does.

**Q3: How do you prevent CSRF?**
A: Use SameSite cookies (Strict or Lax), implement CSRF tokens, use Double Submit Cookie pattern, validate Origin/Referer headers, and use POST for state-changing operations.

**Q4: What is a CSRF token?**
A: A CSRF token is a unique, unpredictable value generated by the server and embedded in forms or headers. The server validates this token on state-changing requests to ensure they originated from the application.

**Q5: What is SameSite cookie attribute?**
A: SameSite controls when cookies are sent with cross-site requests. Strict: never sent cross-site. Lax: sent for top-level navigation. None: sent with all requests (requires Secure flag).

**Q6: What is the Double Submit Cookie pattern?**
A: A CSRF protection technique where the server sets a random token in a cookie and requires the same token in a request header or parameter. The server compares both values to validate the request.

**Q7: Can GET requests cause CSRF?**
A: Yes, but they shouldn't be used for state-changing operations. GET requests should be idempotent. CSRF attacks typically target POST, PUT, PATCH, and DELETE operations.

**Q8: Why are APIs vulnerable to CSRF?**
A: If APIs accept cookies for authentication and don't validate CSRF tokens, they're vulnerable. Even with CORS, browsers may send cookies with cross-origin requests if credentials are included.

**Q9: What is Origin header validation?**
A: The Origin header indicates where a request originated. Validating it ensures requests come from expected domains. However, Origin header can be absent in some legitimate requests (e.g., same-origin).

**Q10: How does CSRF relate to session management?**
A: CSRF exploits the trust the server has in the user's session. Strong session management (short expiration, rotation) limits CSRF impact but doesn't prevent it.

### Intermediate (5-10)

**Q11: How would you implement CSRF protection for a REST API?**
A: Use SameSite cookies, validate Origin/Referer headers, implement CSRF tokens for state-changing operations, use Bearer tokens instead of cookies for API authentication, or implement mutual TLS.

**Q12: How do you handle CSRF in a microservices architecture?**
A: Use an API gateway to validate CSRF tokens. Services trust the gateway. Implement token-based authentication (JWT) instead of session cookies. Use client credentials for service-to-service communication.

**Q13: What is synchronizer token pattern?**
A: A CSRF protection technique where the server generates a unique token tied to the user's session. The token is embedded in forms and validated on submission. The token is different from the session ID.

**Q14: How do you handle CSRF for mobile applications?**
A: Mobile apps don't use cookies, so CSRF is less of a concern. Use token-based authentication (JWT) in headers. Implement certificate pinning. Use device binding for additional security.

**Q15: What is the difference between CSRF tokens and anti-forgery tokens?**
A: They're the same concept. Anti-forgery tokens are the ASP.NET term for CSRF tokens. Both prevent cross-site request forgery by validating request origin.

**Q16: How do you handle CSRF in GraphQL?**
A: Use GET for queries (idempotent), POST for mutations with CSRF tokens. Validate Origin headers. Use persisted queries. Implement query depth limiting.

**Q17: What is the Referer header and how does it help with CSRF?**
A: The Referer header indicates the URL of the page that initiated the request. Validating it ensures requests come from expected origins. However, it can be absent or spoofed in some cases.

**Q18: How do you handle CSRF when using JWT?**
A: JWT in headers (not cookies) is not vulnerable to CSRF. If using cookies with JWT, implement CSRF tokens. Use SameSite cookies. Consider using Bearer tokens for API authentication.

**Q19: What is the CSRF vulnerability in OAuth 2.0?**
A: OAuth 2.0 authorization code flow can be vulnerable to CSRF if the state parameter isn't validated. Attackers can initiate OAuth flows and trick users into completing them.

**Q20: How do you test for CSRF vulnerabilities?**
A: Use tools like Burp Suite, OWASP ZAP. Test state-changing operations without CSRF tokens. Verify SameSite cookie settings. Test cross-origin form submissions.

### Senior (10-15)

**Q21: Design a comprehensive CSRF defense strategy for a large application.**
A: Layer 1: SameSite cookies (Strict). Layer 2: CSRF tokens for all forms. Layer 3: Origin/Referer validation. Layer 4: Content Security Policy. Layer 5: Custom headers for AJAX. Layer 6: Rate limiting on sensitive operations.

**Q22: How would you implement CSRF protection for a single-page application with a separate API?**
A: Use Double Submit Cookie pattern. Implement CSRF token in a cookie, read it via JavaScript, and send as custom header. Validate both on server. Consider using Bearer tokens instead of cookies.

**Q23: Explain the CSRF implications of using Subresource Integrity (SRI).**
A: SRI ensures external resources haven't been tampered with, but doesn't prevent CSRF directly. However, it prevents attackers from injecting malicious scripts via compromised CDNs that could bypass CSRF protections.

**Q24: How would you handle CSRF in a server-side rendered application with forms?**
A: Implement synchronizer token pattern. Embed CSRF tokens in hidden form fields. Validate tokens on form submission. Rotate tokens after login. Use httpOnly cookies for session management.

**Q25: Design a system for CSRF protection that works across multiple domains.**
A: Implement centralized CSRF token service. Use cryptographically signed tokens. Validate tokens across domains. Implement token exchange for cross-domain operations. Use CORS with strict policies.

**Q26: How would you handle CSRF in a WebSocket-based application?**
A: Validate origin header during WebSocket handshake. Use authentication tokens in messages. Implement rate limiting. Monitor for suspicious patterns. Use wss:// (secure WebSocket).

**Q27: Explain the security implications of SameSite=Lax vs SameSite=Strict.**
A: Lax allows cookies with top-level navigations (GET requests from external links). Strict never sends cookies cross-site. Lax is more compatible but slightly less secure. Strict is recommended for sensitive applications.

**Q28: How would you implement CSRF protection for a file upload system?**
A: Use multipart/form-data with CSRF tokens. Validate Content-Type headers. Implement virus scanning. Use separate tokens for upload endpoints. Rate limit upload requests.

**Q29: Design a CSRF protection system for a multi-tenant application.**
A: Generate tenant-specific CSRF tokens. Validate tenant context on each request. Implement tenant isolation. Use separate signing keys per tenant. Audit CSRF validation failures.

**Q30: How would you handle CSRF in a serverless architecture?**
A: Use JWT in headers instead of cookies. Implement API Gateway-level CSRF validation. Use Lambda authorizers for token validation. Implement rate limiting at the gateway level.

### FAANG-style (5-10)

**Q31: Design a CSRF protection system handling 1 million requests per second.**
A: Use Redis for distributed token validation. Implement token caching at edge. Use async validation for non-critical paths. Implement circuit breakers. Monitor validation latency.

**Q32: How would you implement CSRF protection for a real-time collaboration platform?**
A: Use WebSocket authentication tokens. Implement session binding. Validate origin on connection. Use message-level authentication. Monitor for session hijacking.

**Q33: Design a system that prevents CSRF while supporting cross-origin requests.**
A: Use CORS with strict origin validation. Implement custom headers for AJAX requests. Use credentials mode carefully. Validate CSRF tokens in headers. Implement rate limiting per origin.

**Q34: How would you handle CSRF in a system with multiple authentication methods?**
A: Implement per-authentication CSRF protection. Use different token formats for different auth methods. Validate context-specific tokens. Implement authentication method binding.

**Q35: Design a CSRF detection and prevention system for a financial platform.**
A: Implement behavioral analysis for request patterns. Use machine learning for anomaly detection. Implement step-up authentication for high-risk operations. Build automated response system.

### Follow-ups (5-10)

**Q36: How would your CSRF defense change if cookies were not an option?**
A: Use token-based authentication (JWT) in headers. Implement mutual TLS. Use client certificates. Implement API keys. These methods don't rely on cookies and are not vulnerable to CSRF.

**Q37: If SameSite cookies were not supported by browsers, how would you implement CSRF protection?**
A: Use synchronizer token pattern. Implement Double Submit Cookie. Validate Origin/Referer headers. Use custom headers for AJAX requests. Implement additional validation layers.

**Q38: How would you handle CSRF in a system with legacy components that can't be modified?**
A: Implement CSRF protection at the reverse proxy level. Use WAF rules. Implement network-level segmentation. Monitor for attacks. Plan for component upgrades.

**Q39: How would your approach change for a government or healthcare application?**
A: Implement multi-factor authentication for sensitive operations. Use hardware security modules for token generation. Implement comprehensive audit logging. Follow regulatory requirements (FIPS, HIPAA).

**Q40: If you discovered a CSRF vulnerability in production, what would be your incident response?**
A: Immediately enable SameSite cookies. Deploy CSRF tokens. Rotate all active sessions. Audit for exploitation. Notify affected users. Implement additional monitoring.

## Summary

CSRF is a serious web security vulnerability that exploits the trust between a user's browser and web application. Key takeaways:

- Always use SameSite cookies as first line of defense
- Implement CSRF tokens for all state-changing operations
- Use POST for all state-changing operations
- Validate Origin and Referer headers
- Use Double Submit Cookie pattern for SPAs
- Rotate and expire CSRF tokens
- Test for CSRF vulnerabilities regularly

## Cheat Sheet

| Defense | Implementation |
|---------|---------------|
| SameSite Cookies | Set to Strict or Lax |
| CSRF Tokens | Random tokens in forms/headers |
| Double Submit Cookie | Cookie + header comparison |
| Origin Validation | Check Origin/Referer headers |
| Custom Headers | X-Requested-With for AJAX |
| Content-Type | Validate content type |
| State-Changing Ops | Use POST, not GET |
| Token Expiration | 5-15 minutes |

## References & Learn More

- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Cross-Site Request Forgery](https://owasp.org/www-community/attacks/csrf)
- [SameSite Cookie Explained - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)
- [CSRF Tokens - OWASP](https://owasp.org/www-community/attacks/csrf)
- [Double Submit Cookie Pattern - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [RFC 7235 - Hypertext Transfer Protocol (HTTP/1.1): Authentication](https://tools.ietf.org/html/rfc7235)
