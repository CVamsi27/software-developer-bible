# Web Security

## Definition

Web security encompasses the practices, technologies, and policies designed to protect web applications and their users from security threats. It includes a wide range of defenses such as Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), Cross-Origin Resource Sharing (CORS), and various security headers. Web security aims to prevent attacks like XSS, CSRF, clickjacking, open redirects, SSRF, and XXE.

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

## Interview Questions

### Beginner (5-10)

**Q1: What is Content Security Policy (CSP)?**
A: CSP is a security header that restricts which resources (scripts, styles, images) can be loaded and executed on a page. It helps prevent XSS by blocking unauthorized scripts.

**Q2: What is HSTS?**
A: HTTP Strict Transport Security forces browsers to use HTTPS for all connections to a domain. It prevents SSL stripping attacks and ensures secure communication.

**Q3: What is CORS?**
A: Cross-Origin Resource Sharing controls which domains can access resources on your server. It's a browser security feature that prevents unauthorized cross-origin requests.

**Q4: What is clickjacking?**
A: Clickjacking tricks users into clicking on hidden elements on a web page. Attackers overlay transparent iframes to trick users into performing unintended actions.

**Q5: What is an open redirect?**
A: An open redirect vulnerability allows attackers to redirect users to malicious sites by manipulating URL parameters. It can be used for phishing attacks.

**Q6: What is SSRF?**
A: Server-Side Request Forgery allows attackers to make requests from the server to internal or external resources. It can be used to access internal services or scan networks.

**Q7: What is XXE?**
A: XML External Entity injection allows attackers to include external entities in XML documents, potentially accessing sensitive data or causing denial of service.

**Q8: What security headers should every web application have?**
A: CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, and X-XSS-Protection.

**Q9: How do you prevent clickjacking?**
A: Use X-Frame-Options header (DENY or SAMEORIGIN) and CSP frame-ancestors directive.

**Q10: What is the difference between X-Frame-Options and CSP frame-ancestors?**
A: X-Frame-Options is older and limited. CSP frame-ancestors is more flexible and supports multiple domains. Use both for compatibility.

### Intermediate (5-10)

**Q11: How would you implement CSP for a React application?**
A: Use nonce-based CSP. Generate nonce per request. Add nonce to script tags. Configure CSP header with nonce. Use webpack to inject nonces in build.

**Q12: How do you configure CORS for a microservices architecture?**
A: Configure CORS at API gateway. Use specific allowed origins. Implement CORS for each service if needed. Use credentials carefully.

**Q13: How do you prevent SSRF in a web application?**
A: Validate and sanitize URLs. Block private IP ranges. Use allowlists for domains. Implement network segmentation. Monitor outbound requests.

**Q14: How do you implement XXE prevention in XML parsing?**
A: Disable external entities and DTDs. Use safe XML parsers. Prefer JSON over XML. Validate XML input. Use parser configurations that prevent XXE.

**Q15: How do you handle security headers in a server-side rendered application?**
A: Use middleware to set headers. Configure CSP for server-rendered content. Handle dynamic content in CSP. Test headers thoroughly.

**Q16: How do you implement security headers in a CDN?**
A: Configure headers at CDN level. Use CDN-specific configurations. Implement header overrides. Test header propagation.

**Q17: How do you handle CSP violations?**
A: Implement CSP reporting. Monitor violation reports. Adjust CSP rules as needed. Use report-uri or report-to directives.

**Q18: How do you implement HSTS preloading?**
A: Submit domain to HSTS preload list. Ensure includeSubDomains is set. Use long max-age. Test preloading in staging.

**Q19: How do you handle security headers in a microservices architecture?**
A: Implement headers at gateway level. Use service mesh for internal headers. Test header propagation. Monitor header compliance.

**Q20: How do you audit security headers?**
A: Use tools like securityheaders.com. Implement automated testing. Monitor header compliance. Regular security audits.

### Senior (10-15)

**Q21: Design a comprehensive web security strategy for a large application.**
A: Layer 1: Network (WAF, DDoS protection). Layer 2: Application (CSP, HSTS, CORS). Layer 3: Code (input validation, output encoding). Layer 4: Data (encryption, access control).

**Q22: How would you implement CSP for a single-page application with dynamic content?**
A: Use nonce-based CSP. Implement dynamic nonce generation. Handle inline scripts carefully. Use CSP reporting. Test thoroughly.

**Q23: Design a security header strategy for a multi-tenant application.**
A: Implement tenant-specific CSP. Use tenant-aware CORS. Configure headers per tenant. Test tenant isolation.

**Q24: How would you handle security headers in a serverless architecture?**
A: Configure headers at API Gateway. Use Lambda@Edge for CloudFront. Implement headers in serverless functions. Test header propagation.

**Q25: Design a security monitoring system for web attacks.**
A: Implement real-time monitoring. Use SIEM for log analysis. Deploy WAF with custom rules. Implement anomaly detection. Build automated response.

**Q26: How would you implement security headers for a GraphQL API?**
A: Configure CSP for GraphQL playground. Implement CORS for GraphQL endpoints. Use security headers for mutations. Test GraphQL-specific attacks.

**Q27: Design a security header strategy for a global application.**
A: Implement regional compliance. Use CDN for header distribution. Test regional variations. Monitor global compliance.

**Q28: How would you handle security headers in a containerized environment?**
A: Configure headers in reverse proxy. Use service mesh for internal headers. Implement headers in container orchestration. Test container security.

**Q29: Design a security header testing strategy.**
A: Implement automated testing in CI/CD. Use security scanning tools. Test header combinations. Monitor header drift.

**Q30: How would you implement security headers for a progressive web app (PWA)?**
A: Configure headers for service workers. Implement offline security. Handle push notification security. Test PWA-specific security.

### FAANG-style (5-10)

**Q31: Design a security header system for a platform serving 1 billion requests per day.**
A: Use CDN for header distribution. Implement edge caching for headers. Use hardware acceleration. Monitor header performance. Implement global compliance.

**Q32: How would you implement CSP for a system with complex third-party integrations?**
A: Use specific third-party domains in CSP. Implement script nonce for third-party scripts. Use Subresource Integrity. Monitor third-party compliance.

**Q33: Design a security header strategy for a system with strict compliance requirements.**
A: Implement compliance-specific headers. Use automated compliance checking. Maintain audit trails. Implement compliance reporting.

**Q34: How would you handle security headers in a system with real-time collaboration?**
A: Configure headers for WebSocket connections. Implement real-time header updates. Handle dynamic content. Test collaboration-specific security.

**Q35: Design a security header system for a global financial platform.**
A: Implement strict CSP. Use HSTS preload. Configure strict CORS. Implement comprehensive monitoring. Meet regulatory requirements.

### Follow-ups (5-10)

**Q36: How would your security header strategy change if you needed to support legacy browsers?**
A: Implement fallback headers. Use compatible CSP versions. Test browser compatibility. Use progressive enhancement.

**Q37: If CSP was breaking third-party scripts, how would you handle it?**
A: Use specific third-party domains. Implement script nonce. Use Subresource Integrity. Evaluate alternatives to problematic scripts.

**Q38: How would you implement security headers for a system with strict performance requirements?**
A: Use CDN caching. Implement header compression. Optimize header delivery. Monitor performance impact.

**Q39: How would your approach change for a system handling classified information?**
A: Implement strict security headers. Use hardware security modules. Implement air-gapped deployment. Meet government security standards.

**Q40: If you discovered a security header bypass, what would be your incident response?**
A: Immediately patch the vulnerability. Update security headers. Monitor for exploitation. Conduct post-mortem. Implement additional monitoring.

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

## References & Learn More

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [Helmet.js - Express Security Headers](https://helmetjs.github.io/)
- [Mozilla Observatory - Security Headers](https://observatory.mozilla.org/)
- [SecurityHeaders.com - Security Header Scanning](https://securityheaders.com/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
