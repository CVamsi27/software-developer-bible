# Security Interview Questions

## Definition

This comprehensive guide covers the 40 most frequently asked security interview questions for Senior Full Stack Developer positions. Questions are categorized by difficulty level with detailed answers, examples, and follow-up discussions. These questions span authentication, authorization, encryption, web vulnerabilities, and security architecture.

## Why Do We Need It?

- **Interview Preparation**: Master the most common security questions
- **Knowledge Consolidation**: Review and reinforce security concepts
- **Practical Application**: Understand how to apply security in real-world scenarios
- **Career Advancement**: Demonstrate security expertise to employers
- **Architecture Skills**: Show ability to design secure systems

## How It Works

### Question Categories

```text
┌─────────────────────────────────────────────────────────────────┐
│                Interview Question Categories                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Beginner (10 Questions)                                        │
│  ├─ Basic security concepts                                     │
│  ├─ Common vulnerabilities                                      │
│  └─ Fundamental defense mechanisms                              │
│                                                                 │
│  Intermediate (10 Questions)                                    │
│  ├─ Implementation strategies                                   │
│  ├─ Security architecture                                       │
│  └─ Real-world scenarios                                        │
│                                                                 │
│  Senior (12 Questions)                                          │
│  ├─ System design for security                                  │
│  ├─ Advanced attack prevention                                  │
│  └─ Security architecture decisions                             │
│                                                                 │
│  FAANG-style (8 Questions)                                      │
│  ├─ Large-scale security systems                                │
│  ├─ Performance and security trade-offs                         │
│  └─ Novel security challenges                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Example Answer Format

When answering security interview questions, use this structure:

```text

1. Definition: What is it?

2. Why: Why is it important?

3. How: How does it work?

4. Code: Show implementation

5. Trade-offs: Discuss alternatives

6. Real-world: Give examples

```

## Beginner Questions (10)

### Q1: What is XSS and how do you prevent it?

**Answer:**

Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. There are three types:

- **Stored XSS**: Malicious script saved on server
- **Reflected XSS**: Script reflected in URL/response
- **DOM-based XSS**: Script executes in browser via DOM

**Prevention:**

```typescript
// 1. Output encoding
function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#039;", "/": "&#x2F;",
  };
  return text.replace(/[&<>"'/]/g, (char) => map[char]);
}

// 2. Use textContent instead of innerHTML
element.textContent = userInput;

// 3. Implement CSP
res.setHeader("Content-Security-Policy", "script-src 'self' 'nonce-xxx'");

// 4. Use DOMPurify for HTML sanitization
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(dirtyHtml);

```

**Follow-up**: "How would you handle XSS in a React application?"

- React auto-escapes JSX
- Avoid dangerouslySetInnerHTML
- Use DOMPurify for user-generated HTML
- Implement CSP headers

---

### Q2: What is CSRF and how do you prevent it?

**Answer:**

Cross-Site Request Forgery forces authenticated users to execute unwanted actions. The attacker exploits the trust between the user's browser and the application.

**Attack Flow:**

1. User logs into bank.com (session cookie set)

2. User visits attacker's site

3. Attacker's site sends request to bank.com

4. Browser includes session cookie automatically

5. Bank processes the request as legitimate

**Prevention:**

```typescript
// 1. SameSite cookies
cookie: {
  sameSite: "strict", // or "lax"
  secure: true,
  httpOnly: true
}

// 2. CSRF tokens
const csrfToken = crypto.randomBytes(32).toString("hex");
req.session.csrfToken = csrfToken;
// Include in forms and validate on submission

// 3. Double Submit Cookie
// Set cookie with random token, require same token in header
res.cookie("csrf_token", token, { httpOnly: false });
// Client reads cookie and sends as header

```

---

### Q3: What is SQL injection and how do you prevent it?

**Answer:**

SQL injection inserts malicious SQL code into queries, allowing attackers to access, modify, or delete data.

**Prevention:**

```typescript
// 1. Parameterized queries
const query = "SELECT * FROM users WHERE id = $1";
const result = await db.query(query, [userId]);

// 2. Use ORM (Prisma)
const user = await prisma.user.findUnique({
  where: { id: userId }
});

// 3. Input validation
import { z } from "zod";
const schema = z.object({
  id: z.string().regex(/^\d+$/)
});

```

---

### Q4: What is the difference between authentication and authorization?

**Answer:**

- **Authentication**: Verifying identity (who are you?)
- **Authorization**: Checking permissions (what can you do?)

**Example:**

```typescript
// Authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization;
  const user = verifyJWT(token);
  req.user = user;
  next();
};

// Authorization middleware
const authorize = (roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res.status(403).json({ error: "Forbidden" });
  }
  next();
};

// Usage
app.get("/admin", authenticate, authorize(["admin"]), adminHandler);

```

---

### Q5: What is HTTPS and why is it important?

**Answer:**

HTTPS is HTTP over TLS/SSL, encrypting all data in transit. It prevents:

- Eavesdropping (man-in-the-middle attacks)
- Data tampering
- Impersonation

**Implementation:**

```typescript
// Express with HTTPS
import https from "https";
import fs from "fs";

const options = {
  key: fs.readFileSync("private-key.pem"),
  cert: fs.readFileSync("certificate.pem"),
};

https.createServer(options, app).listen(443);

// HSTS header
app.use((req, res, next) => {
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload"
  );
  next();
});

```

---

### Q6: What is the difference between symmetric and asymmetric encryption?

**Answer:**

| Aspect | Symmetric | Asymmetric |
|--------|-----------|------------|
| Keys | Same key for encrypt/decrypt | Key pair (public/private) |
| Speed | Fast | Slower |
| Use Case | Bulk data encryption | Key exchange, signatures |
| Examples | AES-256, ChaCha20 | RSA, ECC |

```typescript
// Symmetric (AES)
const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
const encrypted = cipher.update(text, "utf8", "hex");

// Asymmetric (RSA)
const encrypted = crypto.publicEncrypt(publicKey, buffer);
const decrypted = crypto.privateDecrypt(privateKey, encrypted);

```

---

### Q7: What is a security header?

**Answer:**

Security headers are HTTP response headers that instruct browsers on how to behave securely. Essential headers:

- **CSP**: Controls resource loading
- **HSTS**: Forces HTTPS
- **X-Content-Type-Options**: Prevents MIME sniffing
- **X-Frame-Options**: Prevents clickjacking
- **Referrer-Policy**: Controls referrer information

```typescript
import helmet from "helmet";
app.use(helmet());

```

---

### Q8: What is the principle of least privilege?

**Answer:**

Users and systems should only have the minimum permissions necessary for their function.

**Implementation:**

```typescript
// Database user with limited permissions
// Grant only SELECT, INSERT, UPDATE on specific tables
// Don't grant DROP, ALTER, or admin permissions

// API with scoped permissions
app.get("/api/users", authenticate, requireScope("users:read"), handler);
app.post("/api/users", authenticate, requireScope("users:write"), handler);

```

---

### Q9: What is input validation?

**Answer:**

Input validation checks user input against expected formats before processing.

```typescript
import { z } from "zod";

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  age: z.number().int().min(0).max(150),
});

const result = userSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({ errors: result.error.errors });
}

```

---

### Q10: What is a JWT?

**Answer:**

JSON Web Token is a compact, URL-safe token for transmitting claims. It consists of:

- Header (algorithm, type)
- Payload (claims, user data)
- Signature (integrity verification)

```typescript
import jwt from "jsonwebtoken";

// Sign
const token = jwt.sign({ userId: "123" }, secret, { expiresIn: "1h" });

// Verify
const decoded = jwt.verify(token, secret);

```

---

## Intermediate Questions (10)

### Q11: How would you implement OAuth 2.0 for a single-page application?

**Answer:**

Use Authorization Code flow with PKCE:

```typescript
// 1. Generate PKCE challenge
const codeVerifier = crypto.randomBytes(32).toString("base64url");
const codeChallenge = crypto
  .createHash("sha256")
  .update(codeVerifier)
  .digest("base64url");

// 2. Redirect to authorization server
const authUrl = new URL("https://auth.example.com/authorize");
authUrl.searchParams.set("response_type", "code");
authUrl.searchParams.set("client_id", clientId);
authUrl.searchParams.set("redirect_uri", redirectUri);
authUrl.searchParams.set("code_challenge", codeChallenge);
authUrl.searchParams.set("code_challenge_method", "S256");

// 3. Exchange code for tokens
const response = await fetch("https://auth.example.com/token", {
  method: "POST",
  body: JSON.stringify({
    grant_type: "authorization_code",
    code,
    code_verifier: codeVerifier,
  }),
});

```

---

### Q12: How do you handle session security in a microservices architecture?

**Answer:**

```typescript
// 1. Use centralized session store (Redis Cluster)
const redis = new Redis.Cluster([
  { host: "redis-1", port: 6379 },
  { host: "redis-2", port: 6379 },
]);

// 2. Share session across services
const sessionStore = new RedisStore({ client: redis });

// 3. Validate session at API gateway
const validateSession = async (req, res, next) => {
  const sessionId = req.cookies.sessionId;
  const session = await redis.get(`session:${sessionId}`);
  if (!session) {
    return res.status(401).json({ error: "Invalid session" });
  }
  req.session = JSON.parse(session);
  next();
};

```

---

### Q13: How do you implement RBAC in a NestJS application?

**Answer:**

```typescript
// 1. Create roles guard
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      "roles",
      context.getHandler()
    );
    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles.includes(role));
  }
}

// 2. Create roles decorator
export const Roles = (...roles: string[]) =>
  SetMetadata("roles", roles);

// 3. Use in controller
@Controller("users")
@UseGuards(AuthGuard, RolesGuard)
export class UsersController {
  @Get()
  @Roles("admin")
  findAll() {
    return this.userService.findAll();
  }
}

```

---

### Q14: How do you prevent open redirects?

**Answer:**

```typescript
// 1. Validate redirect URLs
const validateRedirect = (url: string): boolean => {
  try {
    const parsed = new URL(url);
    const allowed = ["example.com", "www.example.com"];
    return allowed.includes(parsed.hostname);
  } catch {
    return false;
  }
};

// 2. Use relative URLs
const redirect = (path: string) => {
  if (path.startsWith("/") && !path.startsWith("//")) {
    return path;
  }
  return "/dashboard";
};

// 3. Use whitelist
const allowedRedirects = ["/dashboard", "/profile", "/settings"];
if (allowedRedirects.includes(req.query.redirect)) {
  res.redirect(req.query.redirect);
}

```

---

### Q15: How do you implement CSP for a React application?

**Answer:**

```typescript
// 1. Generate nonce per request
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString("base64");
  next();
});

// 2. Configure CSP
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'nonce-${res.locals.nonce}'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    },
  })
);

// 3. Use nonce in React
// In index.html or template:
// <script nonce="${nonce}">...</script>

```

---

### Q16: How do you handle password security?

**Answer:**

```typescript
// 1. Use Argon2id (recommended) or bcrypt
import argon2 from "argon2";

const hashPassword = async (password: string): Promise<string> => {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,
    timeCost: 3,
    parallelism: 4,
  });
};

// 2. Verify password
const verifyPassword = async (
  hash: string,
  password: string
): Promise<boolean> => {
  return argon2.verify(hash, password);
};

// 3. Enforce password policy
const passwordSchema = z.string()
  .min(8)
  .max(100)
  .regex(/[A-Z]/, "Must contain uppercase")
  .regex(/[a-z]/, "Must contain lowercase")
  .regex(/[0-9]/, "Must contain number")
  .regex(/[^A-Za-z0-9]/, "Must contain special character");

```

---

### Q17: How do you implement rate limiting?

**Answer:**

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";

// 1. Basic rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests",
});

app.use(limiter);

// 2. Redis-backed rate limiting
const redisLimiter = rateLimit({
  store: new RedisStore({
    sendCommand: (...args) => redis.call(...args),
  }),
  windowMs: 15 * 60 * 1000,
  max: 100,
});

// 3. Different limits for different routes
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 login attempts per 15 minutes
  skipSuccessfulRequests: true,
});

app.use("/login", authLimiter);

```

---

### Q18: How do you implement CORS correctly?

**Answer:**

```typescript
import cors from "cors";

const corsOptions = {
  origin: (origin, callback) => {
    const allowed = ["https://example.com", "https://www.example.com"];
    if (!origin || allowed.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error("Not allowed by CORS"));
    }
  },
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
  maxAge: 86400,
};

app.use(cors(corsOptions));

```

---

### Q19: How do you handle security in server-side rendering?

**Answer:**

```typescript
// 1. CSP with nonce for inline scripts
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString("base64");
  next();
});

// 2. Set security headers
app.use(helmet());

// 3. Sanitize user data before rendering
const sanitize = (data: any) => {
  if (typeof data === "string") {
    return escapeHtml(data);
  }
  return data;
};

// 4. Use httpOnly cookies for session
app.use(
  session({
    cookie: {
      httpOnly: true,
      secure: true,
      sameSite: "strict",
    },
  })
);

```

---

### Q20: How do you implement security logging?

**Answer:**

```typescript
import winston from "winston";

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "security.log" }),
  ],
});

// Log security events
const logSecurityEvent = (event: string, details: any) => {
  logger.warn({
    event,
    timestamp: new Date().toISOString(),
    ...details,
  });
};

// Log authentication attempts
app.post("/login", async (req, res) => {
  try {
    const user = await authenticate(req.body);
    logSecurityEvent("LOGIN_SUCCESS", { userId: user.id });
    res.json({ success: true });
  } catch (error) {
    logSecurityEvent("LOGIN_FAILURE", { email: req.body.email });
    res.status(401).json({ error: "Invalid credentials" });
  }
});

```

---

## Senior Questions (12)

### Q21: Design a secure authentication system for a financial application.

**Answer:**

```typescript
// 1. Multi-factor authentication
const loginWithMFA = async (email: string, password: string, mfaCode: string) => {
  // Verify password
  const user = await verifyPassword(email, password);
  if (!user) throw new Error("Invalid credentials");

  // Verify MFA
  const mfaValid = await verifyMFA(user.mfaSecret, mfaCode);
  if (!mfaValid) throw new Error("Invalid MFA code");

  // Generate tokens
  const accessToken = generateAccessToken(user);
  const refreshToken = generateRefreshToken(user);

  // Log security event
  logSecurityEvent("LOGIN_SUCCESS", { userId: user.id, mfa: true });

  return { accessToken, refreshToken };
};

// 2. Step-up authentication for sensitive operations
const sensitiveOperation = async (req, res, next) => {
  const { userId, action } = req.body;

  // Check if step-up auth is required
  if (requiresStepUp(action)) {
    const recentAuth = await getRecentAuth(userId);
    if (!recentAuth || Date.now() - recentAuth.timestamp > 5 * 60 * 1000) {
      return res.status(401).json({ error: "Step-up authentication required" });
    }
  }

  next();
};

// 3. Session binding to device
const bindSession = (req, res, next) => {
  const deviceFingerprint = generateDeviceFingerprint(req);
  req.session.deviceFingerprint = deviceFingerprint;
  next();
};

const validateDevice = (req, res, next) => {
  const currentFingerprint = generateDeviceFingerprint(req);
  if (currentFingerprint !== req.session.deviceFingerprint) {
    return res.status(401).json({ error: "Device mismatch" });
  }
  next();
};

```

---

### Q22: Design a zero-trust security architecture.

**Answer:**

```typescript
// 1. Verify every request
const zeroTrustMiddleware = async (req, res, next) => {
  // Verify identity
  const user = await verifyToken(req.headers.authorization);
  if (!user) return res.status(401).json({ error: "Unauthorized" });

  // Verify device
  const device = await verifyDevice(req.headers["x-device-id"]);
  if (!device) return res.status(401).json({ error: "Unverified device" });

  // Verify context
  const context = await verifyContext(req.ip, req.headers["user-agent"]);
  if (!context.trusted) return res.status(403).json({ error: "Untrusted context" });

  // Check permissions
  const hasPermission = await checkPermission(user, req.path, req.method);
  if (!hasPermission) return res.status(403).json({ error: "Forbidden" });

  // Log for audit
  await logAccess(user, req.path, req.method);

  next();
};

// 2. Microsegmentation
const microsegmentation = (req, res, next) => {
  const service = getServiceName(req.path);
  const allowedServices = getAllowedServices(req.user);

  if (!allowedServices.includes(service)) {
    return res.status(403).json({ error: "Service not allowed" });
  }

  next();
};

// 3. Continuous authentication
const continuousAuth = async (req, res, next) => {
  const session = req.session;

  // Check session age
  if (Date.now() - session.lastAuth > 5 * 60 * 1000) {
    return res.status(401).json({ error: "Re-authentication required" });
  }

  // Check for anomalies
  const anomalies = await detectAnomalies(session);
  if (anomalies.length > 0) {
    return res.status(403).json({ error: "Anomalous behavior detected" });
  }

  next();
};

```

---

### Q23: How would you implement encryption at scale?

**Answer:**

```typescript
// 1. Envelope encryption
class EnvelopeEncryption {
  private kms: AWS.KMS;

  async encrypt(data: Buffer): Promise<{ encryptedData: Buffer; encryptedKey: Buffer }> {
    // Generate data encryption key
    const dek = crypto.randomBytes(32);

    // Encrypt data with DEK
    const cipher = crypto.createCipheriv("aes-256-gcm", dek, iv);
    const encryptedData = Buffer.concat([cipher.update(data), cipher.final()]);

    // Encrypt DEK with KMS
    const encryptedKey = await this.kms.encrypt({
      KeyId: "alias/my-key",
      Plaintext: dek,
    }).promise();

    return { encryptedData, encryptedKey: Buffer.from(encryptedKey.CiphertextBlob) };
  }

  async decrypt(encryptedData: Buffer, encryptedKey: Buffer): Promise<Buffer> {
    // Decrypt DEK with KMS
    const decryptedKey = await this.kms.decrypt({
      CiphertextBlob: encryptedKey,
    }).promise();

    // Decrypt data with DEK
    const decipher = crypto.createDecipheriv("aes-256-gcm", decryptedKey.Plaintext, iv);
    return Buffer.concat([decipher.update(encryptedData), decipher.final()]);
  }
}

// 2. Key rotation
const rotateKeys = async () => {
  // Generate new key version
  const newKey = await generateNewKey();

  // Re-encrypt data with new key
  await reEncryptAllData(newKey);

  // Archive old key
  await archiveOldKey(currentKey);
};

```

---

### Q24: How do you handle security in a microservices architecture?

**Answer:**

```typescript
// 1. Service-to-service authentication
const serviceAuth = async (req, res, next) => {
  const serviceToken = req.headers["x-service-token"];
  const service = await verifyServiceToken(serviceToken);

  if (!service) {
    return res.status(401).json({ error: "Invalid service token" });
  }

  req.service = service;
  next();
};

// 2. API gateway security
const gatewaySecurity = async (req, res, next) => {
  // Validate JWT
  const user = await validateJWT(req.headers.authorization);

  // Check rate limits
  const rateLimitOk = await checkRateLimit(user.id);
  if (!rateLimitOk) {
    return res.status(429).json({ error: "Rate limit exceeded" });
  }

  // Validate request
  const requestValid = await validateRequest(req);
  if (!requestValid) {
    return res.status(400).json({ error: "Invalid request" });
  }

  // Forward to service
  next();
};

// 3. Service mesh (Istio)
// Configure mTLS between services
// Implement authorization policies
// Enable distributed tracing

```

---

### Q25: How do you implement security monitoring and incident response?

**Answer:**

```typescript
// 1. Security event logging
const securityLogger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "security.log" }),
    new winston.transports.Http({ host: "siem.example.com" }),
  ],
});

// 2. Anomaly detection
const detectAnomalies = async (userId: string, action: string) => {
  const history = await getUserHistory(userId);
  const anomalies = [];

  // Check for unusual time
  if (isUnusualTime(history)) {
    anomalies.push({ type: "unusual_time", severity: "medium" });
  }

  // Check for unusual location
  if (isUnusualLocation(history)) {
    anomalies.push({ type: "unusual_location", severity: "high" });
  }

  // Check for unusual action
  if (isUnusualAction(history, action)) {
    anomalies.push({ type: "unusual_action", severity: "high" });
  }

  return anomalies;
};

// 3. Automated response
const automatedResponse = async (anomaly: Anomaly) => {
  if (anomaly.severity === "high") {
    // Block user
    await blockUser(anomaly.userId);

    // Notify security team
    await notifySecurityTeam(anomaly);

    // Create incident
    await createIncident(anomaly);
  }
};

```

---

### Q26: How do you handle security compliance (GDPR, HIPAA, PCI DSS)?

**Answer:**

```typescript
// 1. Data encryption
const encryptSensitiveData = (data: any) => {
  const sensitiveFields = ["ssn", "creditCard", "healthInfo"];
  const encrypted = { ...data };

  for (const field of sensitiveFields) {
    if (encrypted[field]) {
      encrypted[field] = encrypt(encrypted[field]);
    }
  }

  return encrypted;
};

// 2. Access audit logging
const auditAccess = async (userId: string, resource: string, action: string) => {
  await db.auditLog.create({
    data: {
      userId,
      resource,
      action,
      timestamp: new Date(),
      ipAddress: req.ip,
      userAgent: req.headers["user-agent"],
    },
  });
};

// 3. Data retention policies
const enforceRetentionPolicy = async () => {
  const cutoffDate = new Date();
  cutoffDate.setFullYear(cutoffDate.getFullYear() - 7); // 7 years

  await db.record.deleteMany({
    where: {
      createdAt: { lt: cutoffDate },
      retentionRequired: false,
    },
  });
};

// 4. Consent management
const manageConsent = async (userId: string, consentType: string, granted: boolean) => {
  await db.consent.upsert({
    where: { userId_type: { userId, type: consentType } },
    update: { granted, updatedAt: new Date() },
    create: { userId, type: consentType, granted },
  });
};

```

---

### Q27: How do you implement security testing?

**Answer:**

```typescript
// 1. SAST (Static Application Security Testing)
// Use ESLint security plugins
// Run security scans in CI/CD

// 2. DAST (Dynamic Application Security Testing)
// Use OWASP ZAP or Burp Suite
// Automated security scanning

// 3. Dependency scanning
import snyk from "snyk";

const checkDependencies = async () => {
  const result = await snyk.test("npm://my-project");
  if (result.vulnerabilities.length > 0) {
    throw new Error(`Found ${result.vulnerabilities.length} vulnerabilities`);
  }
};

// 4. Security unit tests
describe("Security", () => {
  it("should prevent SQL injection", async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    const result = await UserService.findByName(maliciousInput);
    expect(result).toBeNull();
  });

  it("should prevent XSS", () => {
    const maliciousInput = "<script>alert('xss')</script>";
    const escaped = escapeHtml(maliciousInput);
    expect(escaped).not.toContain("<script>");
  });
});

```

---

### Q28: How do you handle security in a serverless architecture?

**Answer:**

```typescript
// 1. IAM roles and policies
// Grant minimal permissions to Lambda functions
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:*:*:table/Users"
}

// 2. API Gateway security
// Implement WAF rules
// Use API keys and usage plans
// Enable request validation

// 3. Environment variable encryption
// Use AWS Secrets Manager or Parameter Store
// Never hardcode secrets

// 4. Function-level security
export const handler = async (event: APIGatewayEvent) => {
  // Validate input
  const validated = validateInput(event.body);

  // Check authorization
  const user = await authorize(event.headers.authorization);

  // Process request
  const result = await processRequest(validated, user);

  return {
    statusCode: 200,
    body: JSON.stringify(result),
  };
};

```

---

### Q29: How do you handle security for real-time applications?

**Answer:**

```typescript
// 1. WebSocket authentication
const wsAuth = (ws, req) => {
  const token = new URL(req.url, "http://localhost").searchParams.get("token");
  const user = verifyJWT(token);

  if (!user) {
    ws.close(1008, "Unauthorized");
    return;
  }

  ws.user = user;
};

// 2. Rate limiting for WebSocket
const wsRateLimit = new Map();

const checkWsRateLimit = (userId: string) => {
  const now = Date.now();
  const userLimit = wsRateLimit.get(userId) || { count: 0, resetTime: now };

  if (now > userLimit.resetTime) {
    userLimit.count = 0;
    userLimit.resetTime = now + 60000; // 1 minute
  }

  userLimit.count++;
  wsRateLimit.set(userId, userLimit);

  return userLimit.count <= 100; // 100 messages per minute
};

// 3. Message validation
const validateMessage = (message: any) => {
  const schema = z.object({
    type: z.string(),
    data: z.any(),
  });

  return schema.safeParse(message);
};

```

---

### Q30: How do you handle security for file uploads?

**Answer:**

```typescript
import multer from "multer";
import fileType from "file-type";

// 1. Validate file type
const validateFileType = async (file: Express.Multer.File) => {
  const type = await fileType.fromBuffer(file.buffer);
  const allowedTypes = ["image/jpeg", "image/png", "application/pdf"];

  if (!type || !allowedTypes.includes(type.mime)) {
    throw new Error("Invalid file type");
  }
};

// 2. Validate file size
const validateFileSize = (file: Express.Multer.File, maxSize: number) => {
  if (file.size > maxSize) {
    throw new Error("File too large");
  }
};

// 3. Scan for malware
const scanForMalware = async (file: Express.Multer.File) => {
  const clean = await clamav.scanBuffer(file.buffer);
  if (!clean) {
    throw new Error("Malware detected");
  }
};

// 4. Store securely
const storage = multer.memoryStorage();
const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith("image/")) {
      cb(null, true);
    } else {
      cb(new Error("Only images allowed"));
    }
  },
});

// 5. Use in route
app.post("/upload", upload.single("file"), async (req, res) => {
  await validateFileType(req.file);
  await validateFileSize(req.file, 5 * 1024 * 1024);
  await scanForMalware(req.file);

  // Store securely
  const path = await storeFile(req.file);
  res.json({ path });
});

```

---

### Q31: How do you handle security for APIs?

**Answer:**

```typescript
// 1. Authentication
const authenticateAPI = async (req, res, next) => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) {
    return res.status(401).json({ error: "Token required" });
  }

  const user = await verifyJWT(token);
  if (!user) {
    return res.status(401).json({ error: "Invalid token" });
  }

  req.user = user;
  next();
};

// 2. Authorization
const authorizeAPI = (permissions: string[]) => {
  return (req, res, next) => {
    const hasPermission = permissions.every((p) =>
      req.user.permissions.includes(p)
    );

    if (!hasPermission) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }

    next();
  };
};

// 3. Input validation
const validateAPIInput = (schema: z.ZodSchema) => {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.errors });
    }
    req.body = result.data;
    next();
  };
};

// 4. Rate limiting
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many API requests",
});

// 5. API versioning
app.use("/api/v1", apiV1Router);
app.use("/api/v2", apiV2Router);

```

---

### Q32: How do you handle security for GraphQL APIs?

**Answer:**

```typescript
// 1. Query depth limiting
const depthLimit = require("graphql-depth-limit");
const depthLimitRule = depthLimit(10);

// 2. Query complexity analysis
const { createComplexityLimitRule } = require("graphql-validation-complexity");
const complexityRule = createComplexityLimitRule(1000);

// 3. Authentication
const apolloServer = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }) => {
    const token = req.headers.authorization;
    const user = await verifyJWT(token);
    return { user };
  },
});

// 4. Authorization
const resolvers = {
  Query: {
    users: async (parent, args, context) => {
      if (!context.user) throw new AuthenticationError("Not authenticated");
      if (!context.user.permissions.includes("users:read")) {
        throw new ForbiddenError("Insufficient permissions");
      }
      return UserService.findAll();
    },
  },
};

// 5. Input validation
const resolvers = {
  Mutation: {
    createUser: async (parent, { input }, context) => {
      const validated = createUserSchema.parse(input);
      return UserService.create(validated);
    },
  },
};

```

---

### Q33: How do you handle security for containerized applications?

**Answer:**

```typescript
// 1. Use minimal base images
// FROM alpine:latest
// FROM scratch (for Go binaries)

// 2. Run as non-root user
// USER appuser

// 3. Scan images for vulnerabilities
// Use Trivy, Snyk, or AWS ECR scanning

// 4. Implement network policies
// Kubernetes NetworkPolicy
{
  apiVersion: "networking.k8s.io/v1",
  kind: "NetworkPolicy",
  spec: {
    podSelector: { matchLabels: { app: "api" } },
    policyTypes: ["Ingress", "Egress"],
    ingress: [
      {
        from: [{ podSelector: { matchLabels: { app: "gateway" } } }],
        ports: [{ port: 3000 }],
      },
    ],
  },
}

// 5. Use secrets management
// Kubernetes Secrets or external vault
const getSecret = async (name: string) => {
  const secret = await k8sApi.readNamespacedSecret(name, "default");
  return Buffer.from(secret.data.value, "base64").toString();
};

```

---

### Q34: How do you handle security for CI/CD pipelines?

**Answer:**

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v3

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: "myapp:${{ github.sha }}"

      - name: Run SAST
        uses: github/codeql-action/analyze@v2

      - name: Run dependency check
        run: npm audit --audit-level=high

      - name: Run SLSA provenance
        uses: slsa-framework/slsa-github-generator@v1.4.0

```

---

### Q35: How do you handle security for edge computing?

**Answer:**

```typescript
// 1. Edge function security
export const handler = async (event: RequestEvent) => {
  // Validate input
  const validated = validateInput(event.request);

  // Authenticate at edge
  const user = await authenticateAtEdge(event.request);

  // Apply security headers
  const headers = {
    "Content-Security-Policy": "default-src 'self'",
    "Strict-Transport-Security": "max-age=31536000",
  };

  // Process request
  const response = await processRequest(validated, user);

  return new Response(response, { headers });
};

// 2. DDoS protection at edge
// Use Cloudflare, AWS CloudFront, or similar

// 3. WAF rules at edge
// Implement custom WAF rules for edge functions

```

---

## FAANG-style Questions (8)

### Q36: Design a security system for a platform with 1 billion users.

**Answer:**

```typescript
// 1. Distributed authentication
class DistributedAuth {
  private redisCluster: Redis.Cluster;
  private kms: AWS.KMS;

  async authenticate(token: string): Promise<User> {
    // Check token in Redis Cluster
    const cached = await this.redisCluster.get(`token:${token}`);
    if (cached) return JSON.parse(cached);

    // Verify with KMS
    const user = await this.verifyWithKMS(token);

    // Cache in Redis
    await this.redisCluster.setex(`token:${token}`, 3600, JSON.stringify(user));

    return user;
  }
}

// 2. Global rate limiting
class GlobalRateLimit {
  private redis: Redis.Cluster;

  async checkLimit(userId: string, limit: number): Promise<boolean> {
    const key = `ratelimit:${userId}`;
    const current = await this.redis.incr(key);

    if (current === 1) {
      await this.redis.expire(key, 60);
    }

    return current <= limit;
  }
}

// 3. Security monitoring at scale
class SecurityMonitor {
  private kafka: Kafka;
  private elasticsearch: Elasticsearch;

  async logSecurityEvent(event: SecurityEvent) {
    // Send to Kafka
    await this.kafka.send({
      topic: "security-events",
      messages: [{ value: JSON.stringify(event) }],
    });

    // Index in Elasticsearch
    await this.elasticsearch.index({
      index: "security-events",
      body: event,
    });
  }

  async detectAnomalies(userId: string) {
    // Use machine learning for anomaly detection
    const anomalies = await this.mlService.detect(userId);
    return anomalies;
  }
}

```

---

### Q37: How would you implement security for a real-time collaboration platform?

**Answer:**

```typescript
// 1. WebSocket security
const wsSecurity = async (ws, req) => {
  // Authenticate connection
  const token = req.headers.authorization;
  const user = await verifyJWT(token);

  if (!user) {
    ws.close(1008, "Unauthorized");
    return;
  }

  // Rate limit messages
  const rateLimiter = new RateLimiter(100, 60000); // 100 msgs/min
  ws.on("message", async (message) => {
    if (!rateLimiter.check(user.id)) {
      ws.close(1008, "Rate limit exceeded");
      return;
    }

    // Validate message
    const validated = validateMessage(message);
    if (!validated.valid) {
      ws.close(1008, "Invalid message");
      return;
    }

    // Process message
    await processMessage(user, validated.data);
  });
};

// 2. Document-level security
class DocumentSecurity {
  async checkAccess(userId: string, documentId: string, action: string) {
    const permissions = await this.getPermissions(userId, documentId);
    return permissions.includes(action);
  }

  async encryptDocument(document: Document, key: string) {
    // End-to-end encryption
    const encrypted = await this.encrypt(document.content, key);
    return { ...document, content: encrypted };
  }
}

// 3. Audit logging
class AuditLogger {
  async logAction(userId: string, documentId: string, action: string) {
    await this.db.auditLog.create({
      data: {
        userId,
        documentId,
        action,
        timestamp: new Date(),
        ipAddress: this.getIpAddress(),
      },
    });
  }
}

```

---

### Q38: How would you implement security for a financial trading platform?

**Answer:**

```typescript
// 1. Transaction signing
class TransactionSigner {
  private hsm: HSM;

  async signTransaction(transaction: Transaction): Promise<string> {
    // Hash transaction
    const hash = crypto
      .createHash("sha256")
      .update(JSON.stringify(transaction))
      .digest("hex");

    // Sign with HSM
    const signature = await this.hsm.sign(hash);
    return signature;
  }

  async verifySignature(
    transaction: Transaction,
    signature: string
  ): Promise<boolean> {
    const hash = crypto
      .createHash("sha256")
      .update(JSON.stringify(transaction))
      .digest("hex");

    return await this.hsm.verify(hash, signature);
  }
}

// 2. Real-time fraud detection
class FraudDetector {
  async analyzeTransaction(transaction: Transaction) {
    const features = this.extractFeatures(transaction);
    const prediction = await this.mlModel.predict(features);

    if (prediction.fraudProbability > 0.8) {
      await this.blockTransaction(transaction);
      await this.notifySecurityTeam(transaction);
    }
  }

  extractFeatures(transaction: Transaction) {
    return {
      amount: transaction.amount,
      frequency: this.getFrequency(transaction.userId),
      location: transaction.location,
      time: transaction.timestamp,
    };
  }
}

// 3. Compliance monitoring
class ComplianceMonitor {
  async monitorTrade(trade: Trade) {
    // Check for insider trading patterns
    const insiderTrading = await this.checkInsiderTrading(trade);
    if (insiderTrading) {
      await this.flagTrade(trade, "insider_trading");
    }

    // Check for market manipulation
    const manipulation = await this.checkMarketManipulation(trade);
    if (manipulation) {
      await this.flagTrade(trade, "market_manipulation");
    }

    // Log for regulatory reporting
    await this.logForReporting(trade);
  }
}

```

---

### Q39: How would you implement security for a healthcare platform?

**Answer:**

```typescript
// 1. PHI encryption
class PHIEncryption {
  async encryptPHI(data: any): Promise<any> {
    const phiFields = ["ssn", "medicalRecordNumber", "diagnosis"];

    for (const field of phiFields) {
      if (data[field]) {
        data[field] = await this.encrypt(data[field]);
      }
    }

    return data;
  }

  async decryptPHI(data: any): Promise<any> {
    const phiFields = ["ssn", "medicalRecordNumber", "diagnosis"];

    for (const field of phiFields) {
      if (data[field]) {
        data[field] = await this.decrypt(data[field]);
      }
    }

    return data;
  }
}

// 2. Access controls
class HealthcareAccessControl {
  async checkAccess(
    userId: string,
    patientId: string,
    action: string
  ): Promise<boolean> {
    // Check role-based access
    const user = await this.getUser(userId);
    if (!this.hasRequiredRole(user, action)) {
      return false;
    }

    // Check patient consent
    const consent = await this.getConsent(patientId, userId);
    if (!consent || !consent.granted) {
      return false;
    }

    // Check minimum necessary principle
    if (!this.isMinimumNecessary(user, action)) {
      return false;
    }

    return true;
  }
}

// 3. Audit logging
class HIPAAAuditLogger {
  async logAccess(
    userId: string,
    patientId: string,
    action: string,
    resource: string
  ) {
    await this.db.auditLog.create({
      data: {
        userId,
        patientId,
        action,
        resource,
        timestamp: new Date(),
        ipAddress: this.getIpAddress(),
        userAgent: this.getUserAgent(),
      },
    });
  }

  async generateReport(startDate: Date, endDate: Date) {
    // Generate compliance report
    const logs = await this.db.auditLog.findMany({
      where: {
        timestamp: { gte: startDate, lte: endDate },
      },
    });

    return this.formatReport(logs);
  }
}

```

---

### Q40: How would you implement security for a global payment platform?

**Answer:**

```typescript
// 1. PCI DSS compliance
class PCIDSSCompliance {
  async encryptCardData(cardData: CardData): Promise<EncryptedCardData> {
    // Tokenize card number
    const token = await this.tokenize(cardData.number);

    // Store only last 4 digits
    return {
      token,
      last4: cardData.number.slice(-4),
      expiry: cardData.expiry,
    };
  }

  async processPayment(payment: Payment): Promise<PaymentResult> {
    // Validate PCI compliance
    await this.validatePCICompliance();

    // Process with tokenized card
    const result = await this.paymentGateway.charge({
      token: payment.cardToken,
      amount: payment.amount,
      currency: payment.currency,
    });

    return result;
  }
}

// 2. Fraud prevention
class FraudPrevention {
  async analyzeTransaction(transaction: Transaction) {
    const riskScore = await this.calculateRiskScore(transaction);

    if (riskScore > 0.8) {
      // Block transaction
      return { blocked: true, reason: "High risk" };
    }

    if (riskScore > 0.5) {
      // Require additional verification
      return { requireVerification: true };
    }

    return { approved: true };
  }

  async calculateRiskScore(transaction: Transaction): Promise<number> {
    const factors = [
      await this.checkVelocity(transaction),
      await this.checkLocation(transaction),
      await this.checkDevice(transaction),
      await this.checkAmount(transaction),
    ];

    return factors.reduce((a, b) => a + b, 0) / factors.length;
  }
}

// 3. Cross-border compliance
class CrossBorderCompliance {
  async validateCrossBorderPayment(payment: Payment) {
    // Check sanctions lists
    const sanctioned = await this.checkSanctions(payment);
    if (sanctioned) {
      throw new Error("Sanctioned recipient");
    }

    // Check AML requirements
    const amlCheck = await this.checkAML(payment);
    if (!amlCheck.passed) {
      throw new Error("AML check failed");
    }

    // Log for regulatory reporting
    await this.logForReporting(payment);
  }
}

```

---

## Summary

Mastering security interview questions requires understanding:

1. **Fundamentals**: Authentication, authorization, encryption

2. **Web Vulnerabilities**: XSS, CSRF, SQL injection, SSRF

3. **Security Architecture**: Zero-trust, defense in depth

4. **Compliance**: GDPR, HIPAA, PCI DSS

5. **Implementation**: Security headers, CORS, CSP

6. **Monitoring**: Logging, anomaly detection, incident response

## Cheat Sheet

| Category | Key Concepts |
|----------|--------------|
| Authentication | JWT, OAuth 2.0, MFA, Sessions |
| Authorization | RBAC, ABAC, Policy-based |
| Encryption | AES, RSA, TLS, HTTPS |
| Web Security | XSS, CSRF, SQLi, SSRF |
| Security Headers | CSP, HSTS, CORS, X-Frame-Options |
| Compliance | GDPR, HIPAA, PCI DSS |
| Monitoring | Logging, SIEM, Anomaly detection |
| Architecture | Zero-trust, Defense in depth |

## References & Learn More

- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox - Cybersecurity Training](https://www.hackthebox.com/)
- [Cybrary - Free Cybersecurity Training](https://www.cybrary.it/)
