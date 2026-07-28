# Web Security

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

d to protect web applications and their users from security threats. It includes a wide range of defenses such as Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), Cross-Origin Resource Sharing (CORS), and various security headers. Web security aims to prevent attacks like XSS, CSRF, clickjacking, open redirects, SSRF, and XXE.

## Why Do We Need It?

- **Attack Prevention**: Protect against common web vulnerabilities
- **Data Protection**: Safeguard user data from theft and manipulation
- **Compliance**: Meet regulatory requirements (GDPR, PCI DSS, HIPAA)
- **Trust**: Build user confidence in application security
- **Reputation**: Avoid security incidents that damage brand reputation
- **Legal**: Prevent lawsuits from security breaches

## How It Works

### Security Layers

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Web Security Layers                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 1: Network                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  HTTPS/TLS, DDoS Protection, WAF                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Layer 2: Application                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  CSP, HSTS, CORS, Security Headers                      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Layer 3: Code                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Input Validation, Output Encoding, Authentication      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Layer 4: Data                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Encryption, Access Control, Audit Logging              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### Security Headers Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Security Headers                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Content-Security-Policy (CSP)                                  │
│  ├─ Controls which resources can be loaded                      │
│  ├─ Prevents XSS attacks                                        │
│  └─ Specifies allowed scripts, styles, images                   │
│                                                                 │
│  Strict-Transport-Security (HSTS)                               │
│  ├─ Forces HTTPS connections                                    │
│  ├─ Prevents SSL stripping attacks                              │
│  └─ Includes subdomains option                                  │
│                                                                 │
│  X-Content-Type-Options                                         │
│  ├─ Prevents MIME type sniffing                                 │
│  └─ Value: nosniff                                              │
│                                                                 │
│  X-Frame-Options                                                │
│  ├─ Prevents clickjacking                                       │
│  └─ Values: DENY, SAMEORIGIN                                   │
│                                                                 │
│  X-XSS-Protection                                               │
│  ├─ Enables browser XSS filter                                  │
│  └─ Value: 1; mode=block                                        │
│                                                                 │
│  Referrer-Policy                                                 │
│  ├─ Controls referrer information                               │
│  └─ Values: no-referrer, strict-origin                         │
│                                                                 │
│  Permissions-Policy                                              │
│  ├─ Controls browser features                                   │
│  └─ Controls camera, microphone, geolocation                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Content Security Policy (CSP)

```typescript
// Express CSP middleware
import helmet from "helmet";

// Basic CSP configuration
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'nonce-abc123'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      connectSrc: ["'self'", "https://api.example.com"],
      frameSrc: ["'none'"],
      objectSrc: ["'none'"],
      baseUri: ["'self'"],
      formAction: ["'self'"],
      frameAncestors: ["'none'"],
      upgradeInsecureRequests: [],
    },
  })
);

// Dynamic CSP with nonce
const generateNonce = (): string => {
  return require("crypto").randomBytes(16).toString("base64");
};

app.use((req, res, next) => {
  const nonce = generateNonce();
  res.locals.nonce = nonce;

  res.setHeader(
    "Content-Security-Policy",
    `default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline'`
  );

  next();
});

// CSP reporting
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      reportUri: "/csp-report",
      reportTo: "csp-endpoint",
    },
  })
);

app.post("/csp-report", express.json({ type: "application/csp-report" }), (req, res) => {
  console.error("CSP Violation:", req.body);
  res.status(204).end();
});

```

### HSTS Configuration

```typescript
// Helmet HSTS
app.use(
  helmet.hsts({
    maxAge: 31536000, // 1 year in seconds
    includeSubDomains: true,
    preload: true,
  })
);

// Manual HSTS header
app.use((req, res, next) => {
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload"
  );
  next();
});

```

### CORS Configuration

```typescript
import cors from "cors";

// Basic CORS
app.use(cors());

// Custom CORS configuration
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      "https://example.com",
      "https://www.example.com",
    ];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error("Not allowed by CORS"));
    }
  },
  methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
  credentials: true,
  maxAge: 86400, // 24 hours
};

app.use(cors(corsOptions));

// CORS for specific routes
app.use("/api", cors(corsOptions));

// Preflight handler
app.options("*", cors(corsOptions));

```

### Security Headers Middleware

```typescript
// Comprehensive security headers
const securityHeaders = (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): void => {
  // HSTS
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload"
  );

  // Prevent MIME type sniffing
  res.setHeader("X-Content-Type-Options", "nosniff");

  // Prevent clickjacking
  res.setHeader("X-Frame-Options", "DENY");

  // XSS protection
  res.setHeader("X-XSS-Protection", "1; mode=block");

  // Referrer policy
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");

  // Permissions policy
  res.setHeader(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), payment=()"
  );

  // Content security policy (handled by helmet)
  // res.setHeader('Content-Security-Policy', csp);

  // Remove server header
  res.removeHeader("X-Powered-By");

  next();
};

app.use(securityHeaders);

```

### Clickjacking Protection

```typescript
// X-Frame-Options
app.use((req, res, next) => {
  res.setHeader("X-Frame-Options", "DENY");
  // Or for same-origin iframes:
  // res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  next();
});

// CSP frame-ancestors
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      frameAncestors: ["'none'"],
      // Or for specific domains:
      // frameAncestors: ["'self'", "https://trusted.com"],
    },
  })
);

// Frame busting (client-side, less reliable)
// <script>
//   if (window.top !== window.self) {
//     window.top.location = window.self.location;
//   }
// </script>

```

### Open Redirect Prevention

```typescript
// ❌ VULNERABLE: Unvalidated redirect
app.get("/redirect", (req, res) => {
  const url = req.query.url as string;
  res.redirect(url); // Can redirect to malicious sites
});

// ✅ SECURE: Validated redirect
const validateRedirectUrl = (url: string): boolean => {
  try {
    const parsed = new URL(url);
    const allowedDomains = ["example.com", "www.example.com"];
    return allowedDomains.includes(parsed.hostname);
  } catch {
    return false;
  }
};

app.get("/redirect", (req, res) => {
  const url = req.query.url as string;

  if (!validateRedirectUrl(url)) {
    return res.status(400).json({ error: "Invalid redirect URL" });
  }

  res.redirect(url);
});

// ✅ SECURE: Use relative URLs
app.get("/redirect", (req, res) => {
  const path = req.query.path as string;

  // Only allow relative paths
  if (path.startsWith("/") && !path.startsWith("//")) {
    res.redirect(path);
  } else {
    res.redirect("/dashboard");
  }
});

```

### SSRF Prevention

```typescript
import dns from "dns";
import { URL } from "url";

// SSRF prevention middleware
const preventSSRF = async (
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
): Promise<void> => {
  const url = req.body.url || req.query.url;

  if (!url) {
    return next();
  }

  try {
    const parsed = new URL(url);

    // Block private IPs
    const hostname = parsed.hostname;
    const ip = await dns.promises.resolve4(hostname);

    for (const address of ip) {
      if (isPrivateIP(address)) {
        res.status(400).json({ error: "Private IP addresses not allowed" });
        return;
      }
    }

    // Block dangerous protocols
    if (!["http:", "https:"].includes(parsed.protocol)) {
      res.status(400).json({ error: "Only HTTP/HTTPS protocols allowed" });
      return;
    }

    next();
  } catch (error) {
    res.status(400).json({ error: "Invalid URL" });
  }
};

const isPrivateIP = (ip: string): boolean => {
  const parts = ip.split(".").map(Number);

  // 10.x.x.x
  if (parts[0] === 10) return true;

  // 172.16.x.x - 172.31.x.x
  if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;

  // 192.168.x.x
  if (parts[0] === 192 && parts[1] === 168) return true;

  // 127.x.x.x (loopback)
  if (parts[0] === 127) return true;

  // 0.0.0.0
  if (ip === "0.0.0.0") return true;

  return false;
};

// Usage
app.post("/fetch-url", preventSSRF, async (req, res) => {
  const { url } = req.body;
  const response = await fetch(url);
  const data = await response.json();
  res.json(data);
});

```

### XXE Prevention

```typescript
// ❌ VULNERABLE: XML parsing without disabling external entities
import xml2js from "xml2js";

// ✅ SECURE: Disable external entities
import libxmljs from "libxmljs2";

const parseXMLSecure = (xml: string) => {
  return libxmljs.parseXml(xml, {
    noent: false, // Disable entity substitution
    dtdvalid: false,
    nonet: true, // Disable network access
  });
};

// ✅ SECURE: Use JSON instead of XML
app.post("/data", express.json(), (req, res) => {
  // Use JSON instead of XML
  const data = req.body;
  // Process data
  res.json({ success: true });
});

// ✅ SECURE: If XML is required, use a safe parser
import { XMLParser } from "fast-xml-parser";

const xmlParser = new XMLParser({
  processEntities: false,
  allowBooleanAttributes: false,
  parseAttributeValue: false,
  trimValues: true,
});

app.post("/xml-data", express.text({ type: "application/xml" }), (req, res) => {
  const parsed = xmlParser.parse(req.body);
  // Process parsed data
  res.json({ success: true });
});

```

## Real-World Use Cases

### 1. Financial Applications

- Strict CSP to prevent script injection
- HSTS for secure connections
- CORS for API access control
- Comprehensive security headers

### 2. E-commerce Platforms

- Clickjacking protection for checkout pages
- Open redirect prevention for payment redirects
- SSRF prevention for product image loading
- Security headers for user data protection

### 3. Social Media Platforms

- CSP for user-generated content
- CORS for API access
- Security headers for privacy
- XXE prevention for XML imports

### 4. Healthcare Applications

- HIPAA-compliant security headers
- CSP for PHI protection
- HSTS for secure connections
- Comprehensive audit logging

## Common Mistakes

1. **Not implementing CSP**: Critical for preventing XSS

2. **Using unsafe-inline in CSP**: Weakens CSP protection

3. **Not using HSTS**: Allows SSL stripping attacks

4. **Overly permissive CORS**: CORS bypasses security

5. **Not preventing clickjacking**: Users can be tricked

6. **Ignoring open redirects**: Can lead to phishing

7. **Not preventing SSRF**: Server can be used as proxy

8. **Not preventing XXE**: XML parsing vulnerabilities

## Best Practices

1. **Implement strict CSP** with nonce-based scripts

2. **Use HSTS** with long max-age and includeSubDomains

3. **Configure CORS** with specific allowed origins

4. **Prevent clickjacking** with X-Frame-Options and CSP

5. **Validate redirect URLs** to prevent open redirects

6. **Prevent SSRF** by blocking private IPs

7. **Prevent XXE** by disabling external entities

8. **Use security headers** (helmet.js makes this easy)

9. **Regular security audits** and penetration testing
10. **Monitor security headers** with tools like securityheaders.com

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| CSP | First load may be slower; caching helps |
| HSTS | Minimal overhead after first connection |
| CORS | Preflight adds one round-trip |
| Security Headers | Negligible performance impact |
| SSRF Prevention | DNS resolution adds latency |

## Summary

Web security is a comprehensive approach to protecting web applications from attacks. Key takeaways:

- Implement CSP with nonce-based scripts
- Use HSTS with long max-age
- Configure CORS with specific origins
- Prevent clickjacking with X-Frame-Options and CSP
- Validate redirect URLs to prevent open redirects
- Prevent SSRF by blocking private IPs
- Prevent XXE by disabling external entities
- Use security headers (helmet.js)
- Regular security audits and testing

## Cheat Sheet
| Header | Purpose | Value |
|--------|---------|-------|
| Content-Security-Policy | Prevent XSS | default-src 'self'; script-src 'self' 'nonce-xxx' |
| Strict-Transport-Security | Force HTTPS | max-age=31536000; includeSubDomains; preload |
| X-Content-Type-Options | Prevent MIME sniffing | nosniff |
| X-Frame-Options | Prevent clickjacking | DENY or SAMEORIGIN |
| X-XSS-Protection | XSS filter | 1; mode=block |
| Referrer-Policy | Control referrer | strict-origin-when-cross-origin |
| Permissions-Policy | Control features | camera=(), microphone=() |
| CORS | Control cross-origin | Access-Control-Allow-Origin |

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [Helmet.js - Express Security Headers](https://helmetjs.github.io/)
- [Mozilla Observatory - Security Headers](https://observatory.mozilla.org/)
- [SecurityHeaders.com - Security Header Scanning](https://securityheaders.com/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
