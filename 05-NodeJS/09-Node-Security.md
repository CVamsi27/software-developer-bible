---
section: Node.js
category: Backend
tags: [concept]
---

# Node.js Security

Node.js applications face unique security challenges due to their asynchronous nature, event-driven architecture, and ecosystem of third-party packages. This covers authentication, input validation, secure configuration, dependency management, and common vulnerability prevention.

## Definition

**Node.js Security** encompasses the practices, tools, and configurations to protect Node.js applications from attacks. Key areas include:

- **Input validation**: Preventing injection attacks through request data
- **Authentication & authorization**: Secure user identification and access control
- **Dependency security**: Managing third-party package vulnerabilities
- **Secure configuration**: Environment variables, secrets management, HTTPS
- **Output encoding**: Preventing XSS in server-rendered responses
- **Rate limiting & DoS protection**: Preventing resource exhaustion
- **Logging & monitoring**: Detecting security incidents

## Why Do We Need It?

1. **Supply chain attacks**: npm packages can contain malicious code or vulnerabilities

2. **Injection attacks**: SQL injection, NoSQL injection, command injection through unsanitized input

3. **Data breaches**: Leaked secrets, exposed environment variables, insecure storage

4. **Denial of Service**: Event loop blocking, memory exhaustion, infinite JSON parsing

5. **Authentication bypass**: Weak sessions, JWT vulnerabilities, insecure password handling

6. **Compliance**: GDPR, HIPAA, PCI-DSS require security practices

## How It Works

### Threat Model

```text
┌─────────────────────────────────────────────────────────────┐
│                  NODE.JS THREAT SURFACE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  External Threats:                                           │
│  ├── HTTP Attacks (XSS, CSRF, Injection)                    │
│  ├── DoS (Slow loris, Regex DoS, Memory exhaustion)          │
│  └── Supply Chain (Malicious packages, Typosquatting)        │
│                                                              │
│  Internal Threats:                                           │
│  ├── Secrets Exposure (env vars, config files, .git)         │
│  ├── Injection (Command injection in child_process)          │
│  └── Prototype Pollution (unsafe object merging)             │
│                                                              │
│  Operational:                                                │
│  ├── Unpatched Dependencies (known CVEs)                    │
│  ├── Insecure Defaults (Express.js defaults)                │
│  └── Data Exposure (verbose error messages)                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples (Node.js)

### Input Validation & Sanitization

```javascript
// Validation middleware
function validateInput(schema) {
  return (req, res, next) => {
    const { error } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.details.map((d) => d.message),
      });
    }
    next();
  };
}

// Prevent NoSQL injection
function sanitizeMongoQuery(obj) {
  if (typeof obj !== 'object' || obj === null) return obj;

  const sanitized = {};
  for (const [key, value] of Object.entries(obj)) {
    // Block dangerous operators
    if (key.startsWith('$')) {
      throw new Error('Dangerous operator detected');
    }
    sanitized[key] = sanitizeMongoQuery(value);
  }
  return sanitized;
}

// Prevent command injection
const { spawn } = require('child_process');
const path = require('path');

function safeExecFile(userInput) {
  // Whitelist approach
  const allowedCommands = ['ls', 'cat', 'head'];
  const [cmd, ...args] = userInput.split(' ');

  if (!allowedCommands.includes(cmd)) {
    throw new Error('Command not allowed');
  }

  // Validate arguments
  const safeArgs = args.map((arg) => {
    // Remove shell metacharacters
    return arg.replace(/[;&|`$(){}[\]<>]/g, '');
  });

  return spawn(cmd, safeArgs);
}
```

### Secure Configuration

```javascript
// secrets.js — NEVER commit to version control
const crypto = require('crypto');

class SecretsManager {
  constructor() {
    this.secrets = new Map();
  }

  loadFromEnv() {
    const required = ['DB_PASSWORD', 'JWT_SECRET', 'API_KEY'];
    const missing = required.filter((key) => !process.env[key]);

    if (missing.length > 0) {
      throw new Error(`Missing required secrets: ${missing.join(', ')}`);
    }

    for (const key of required) {
      this.secrets.set(key, process.env[key]);
    }
  }

  get(key) {
    if (!this.secrets.has(key)) {
      throw new Error(`Secret '${key}' not found`);
    }
    return this.secrets.get(key);
  }

  // Never log secrets
  toJSON() {
    return '[REDACTED]';
  }
}

// Secure .env loading
function loadEnvFile() {
  const lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('.env'),
  });

  lineReader.on('line', (line) => {
    const trimmed = line.trim();
    if (trimmed.startsWith('#') || !trimmed.includes('=')) return;

    const separator = trimmed.indexOf('=');
    const key = trimmed.slice(0, separator).trim();

    // Prevent process.env pollution from .env in production
    if (process.env.NODE_ENV === 'production') return;

    const value = trimmed.slice(separator + 1).trim();
    process.env[key] = value;
  });
}
```

### Rate Limiting & DoS Protection

```javascript
const http = require('http');

class RateLimiter {
  constructor(windowMs = 60000, maxRequests = 100) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
    this.clients = new Map();
  }

  middleware(req, res, next) {
    const ip = req.socket.remoteAddress;
    const now = Date.now();

    if (!this.clients.has(ip)) {
      this.clients.set(ip, []);
    }

    const requests = this.clients.get(ip);
    // Clean old entries
    const windowStart = now - this.windowMs;
    while (requests.length > 0 && requests[0] < windowStart) {
      requests.shift();
    }

    if (requests.length >= this.maxRequests) {
      res.writeHead(429, { 'Retry-After': Math.ceil(this.windowMs / 1000) });
      res.end('Too Many Requests');
      return;
    }

    requests.push(now);
    next();
  }
}

// Prevent JSON body parsing DoS
function jsonBodyParser(maxSize = '100kb') {
  const maxBytes = parseBytes(maxSize);

  return (req, res, next) => {
    if (req.headers['content-length'] > maxBytes) {
      res.writeHead(413);
      res.end('Payload Too Large');
      return;
    }

    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
      if (Buffer.byteLength(body) > maxBytes) {
        // Abort oversized request
        req.destroy(new Error('Payload Too Large'));
      }
    });

    req.on('end', () => {
      try {
        req.body = JSON.parse(body);
        next();
      } catch {
        res.writeHead(400);
        res.end('Invalid JSON');
      }
    });
  };
}
```

### Secure HTTP Headers

```javascript
const http = require('http');

function secureHeaders(req, res, next) {
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Enable XSS filter
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Strict Transport Security
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains'
  );

  // Content Security Policy
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );

  // Referrer Policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Permissions Policy
  res.setHeader(
    'Permissions-Policy',
    'geolocation=(), microphone=(), camera=()'
  );

  // Remove X-Powered-By
  res.removeHeader('X-Powered-By');

  next();
}
```

### Dependency Security

```javascript
// npm audit in package.json
/*
{
  "scripts": {
    "preinstall": "npx npm-audit-resolver",
    "audit": "npm audit --audit-level=high",
    "outdated": "npm outdated --depth=0"
  }
}
*/

// Check for known vulnerabilities in dependencies
/*
  $ npm audit                    # Check vulnerabilities
  $ npm audit fix                # Auto-fix vulnerabilities
  $ npm audit --audit-level=high # Only report high/critical

  $ npx snyk test                # Snyk vulnerability scanner
  $ npx snyk monitor             # Continuous monitoring

  # Lock file integrity
  # Always commit package-lock.json or yarn.lock
  # Use npm ci for CI/CD (uses lock file, fails if mismatch)
*/

// Check for outdated packages
async function checkOutdated() {
  const { exec } = require('child_process');
  const util = require('util');
  const execPromise = util.promisify(exec);

  try {
    const { stdout } = await execPromise('npm outdated --json');
    const outdated = JSON.parse(stdout);
    for (const [pkg, info] of Object.entries(outdated)) {
      console.log(`${pkg}: ${info.current} → ${info.latest} (${info.type})`);
    }
  } catch (err) {
    // npm outdated exits with non-zero if outdated packages exist
    if (err.stdout) {
      console.log('Outdated packages:', err.stdout);
    }
  }
}
```

### Helmet.js Integration (Security Headers)

```javascript
// Helmet.js is the standard security header middleware for Express
// In a real app: const helmet = require('helmet');

// What Helmet sets by default:
const helmetDefaults = {
  'Content-Security-Policy': "default-src 'self';base-uri 'self';font-src 'self' https: data:;form-action 'self';frame-ancestors 'self';img-src 'self' data:;object-src 'none';script-src 'self';script-src-attr 'none';style-src 'self' https: 'unsafe-inline';upgrade-insecure-requests",
  'Cross-Origin-Embedder-Policy': 'require-corp',
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Resource-Policy': 'same-origin',
  'Expect-CT': 'max-age=0',
  'Origin-Agent-Cluster': '?1',
  'Referrer-Policy': 'no-referrer',
  'Strict-Transport-Security': 'max-age=15552000; includeSubDomains',
  'X-Content-Type-Options': 'nosniff',
  'X-DNS-Prefetch-Control': 'off',
  'X-Download-Options': 'noopen',
  'X-Frame-Options': 'SAMEORIGIN',
  'X-Permitted-Cross-Domain-Policies': 'none',
  'X-XSS-Protection': '0',
};
```

### Prototype Pollution Prevention

```javascript
// Prototype pollution attack
// ❌ Vulnerable merge
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object') {
      target[key] = merge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// Attack: merge({}, JSON.parse('{"__proto__": {"polluted": true}}'));
// This pollutes Object.prototype

// ✅ Safe merge
function safeMerge(target, source) {
  for (const key of Object.keys(source)) {
    // Block prototype keys
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue;
    }
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = safeMerge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// ✅ Use Object.create(null) for maps
const safeMap = Object.create(null);
safeMap.userInput = 'value';
// No prototype chain — immune to pollution
```

## Common Security Vulnerabilities

| Vulnerability | Risk | Prevention |
|--------------|:----:|------------|
| Command Injection | High | Use `spawn` not `exec`; validate/sanitize input |
| SQL/NoSQL Injection | High | Parameterized queries; input validation |
| Prototype Pollution | High | Use `Object.create(null)`; validate `__proto__` |
| Insecure Dependencies | High | Regular `npm audit`; Dependabot/Renovate |
| ReDoS (Regex DoS) | Medium | Use `re2` library; test regex performance |
| Timing Attacks | Medium | Constant-time comparison for sensitive data |
| Directory Traversal | High | Use `path.resolve()` and validate prefix |
| Insecure Randomness | Medium | Use `crypto.randomBytes()` not `Math.random()` |

## Best Practices

1. **Use Helmet.js** — set secure HTTP headers in every app
2. **Validate all input** — never trust user input (body, params, query, headers)
3. **Use parameterized queries** — never concatenate SQL/NoSQL queries
4. **Run `npm audit`** regularly — automate in CI/CD pipeline
5. **Use environment variables** for secrets — never hardcode credentials
6. **Rate limit endpoints** — prevent brute force and DoS
7. **Implement proper CORS** — don't use `Access-Control-Allow-Origin: *` in production
8. **Use HTTPS only** — redirect HTTP to HTTPS in production
9. **Set request size limits** — prevent memory exhaustion
10. **Log security events** — failed auth attempts, suspicious patterns

## Performance Considerations

- **Rate limiting adds overhead** — use in-memory cache for single process, Redis for distributed
- **Input validation is fast** — libraries like Joi/Zod are optimized
- **TLS/SSL handshake** — termination at load balancer reduces overhead
- **Encryption (bcrypt)** — bcrypt is intentionally slow; use appropriate cost factor
- **Security headers** — negligible overhead (just header bytes)

## Summary

Node.js security requires defense in depth: validate inputs, secure dependencies, protect secrets, set security headers, rate limit endpoints, and prevent injection attacks. Use Helmet.js for headers, parameterized queries for databases, and `crypto` for secure operations. Regular `npm audit` and dependency scanning are essential for supply chain security.

## Cheat Sheet

```text
NODE.JS SECURITY CHEAT SHEET
═══════════════════════════════════════

HEADERS (Helmet):
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000
  Content-Security-Policy: default-src 'self'

INPUT VALIDATION:
  const schema = z.object({ email: z.string().email() });
  schema.parse(req.body);

DEPENDENCIES:
  npm audit           # Check vulnerabilities
  npm audit fix       # Auto fix
  snyk test           # Deeper scan
  Dependabot          # Automated PRs

SECRETS:
  process.env.MY_SECRET
  .env (never commit)
  Vault / AWS Secrets Manager

ENCRYPTION:
  crypto.randomBytes(32)    # Secure random
  crypto.createHash('sha256')  # Hashing
  bcrypt.hash(password, 10)  # Password hashing

DOS PREVENTION:
  Rate limiting (express-rate-limit)
  Body size limits (express.json({ limit: '100kb' }))
  Timeout middleware
  --max-old-space-size (Node flag)

PROTOTYPE POLLUTION:
  Object.create(null)  // No prototype
  Avoid deep merge without checks
```

---

### See Also

- [Web Security](../../09-Security/) — browser-side security
- [HTTP Module](../07-HTTP-Module.md) — secure HTTP configuration
- [Process & Environment](../09-Process-Environment.md) — environment variables
- [REST API Authentication](../../07-REST-API/06-Authentication.md)

### References

- [OWASP Node.js Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)
- [Node.js Security Guide](https://nodejs.org/en/learn/getting-started/security-best-practices)
- [Snyk: Node.js Security](https://snyk.io/blog/node-js-security-best-practices/)
- [npm audit Documentation](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)
