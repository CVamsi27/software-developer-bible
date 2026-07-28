# Cross-Site Request Forgery (CSRF)

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

ces an authenticated user to execute unwanted actions on a web application in which they're authenticated. Unlike XSS, which injects malicious scripts, CSRF tricks the user's browser into making unintended requests using the user's existing session. The attacker exploits the trust that a site has in the user's browser.

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

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Cross-Site Request Forgery](https://owasp.org/www-community/attacks/csrf)
- [SameSite Cookie Explained - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)
- [CSRF Tokens - OWASP](https://owasp.org/www-community/attacks/csrf)
- [Double Submit Cookie Pattern - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [RFC 7235 - Hypertext Transfer Protocol (HTTP/1.1): Authentication](https://tools.ietf.org/html/rfc7235)
