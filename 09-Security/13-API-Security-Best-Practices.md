---
section: Security
category: Architecture
tags: [concept]
---

# API Security Best Practices & OWASP API Top 10

> **TL;DR:** The OWASP API Security Top 10 (2023) is the senior interview anchor for API security. The biggest risks are BOLA (broken object-level authorization), BFLA (broken function-level authz), and broken authentication — and the answer is almost always a deliberate, layered set of guards, DTOs, and tests. The senior test is producing a production API that is secure by default, not one that gets hardened after a breach.
>
> **Why it matters:** This is an Architecture interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

API security is the discipline of designing, building, and operating HTTP APIs that resist the OWASP API Security Top 10 (2023) — BOLA, broken authentication, broken object-property-level authorization, unrestricted resource consumption, broken function-level authorization, server-side request forgery, security misconfiguration, lack of protection from automated threats, improper asset management, and unsafe consumption of APIs. The senior approach is **secure by default** — authn/authz/validation are global middleware, not per-endpoint afterthoughts.

## Why Do We Need It?

1. **Public attack surface** — An API is a documented, machine-readable attack surface; bots and bug-bounty hunters find issues first.
2. **BOLA is the #1 cause of API breaches** — Reading someone else's resource by changing the id is shockingly common.
3. **Compliance** — PCI-DSS, HIPAA, SOC 2, GDPR all require API security controls.
4. **Data exposure** — One misconfigured S3 bucket or one missing scope check is a brand-damaging leak.
5. **Automated abuse** — Credential stuffing, scraping, and account creation are daily; rate limiting and bot detection are baseline.
6. **Supply chain** — Your API consumes other APIs; their compromise becomes yours.
7. **Cost** — A successful abuse (cryptojacking, large-query DoS) can run a 5-figure AWS bill in hours.

## How It Works

### The OWASP API Security Top 10 (2023)

| # | Risk | What it looks like in production |
|---|------|----------------------------------|
| API1 | **Broken Object Level Authorization (BOLA)** | `GET /orders/123` returns any user's order by changing the id |
| API2 | **Broken Authentication** | Weak JWT, no key rotation, brute-forceable passwords, alg=none |
| API3 | **Broken Object Property Level Authorization** | `PATCH /users/1` with `{ "isAdmin": true }` escalates role |
| API4 | **Unrestricted Resource Consumption** | No rate limit, no body size limit, no query result limit |
| API5 | **Broken Function Level Authorization** | `POST /admin/users` accessible to non-admin role |
| API6 | **Unrestricted Access to Sensitive Business Flows** | Scripted ticket scalping, mass account creation |
| API7 | **Server Side Request Forgery (SSRF)** | `POST /fetch { url: "http://169.254.169.254/..." }` |
| API8 | **Security Misconfiguration** | Verbose errors, default creds, permissive CORS, missing headers |
| API9 | **Improper Inventory Management** | `/v1/` deprecated but still public; staging env exposed |
| API10 | **Unsafe Consumption of APIs** | Trusting 3rd-party API responses without validation |

### Defense in Depth

```text
                ┌────────────────────────────┐
                │  Edge: WAF, DDoS, rate-limit│
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │  Auth: JWT validation, scope│
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │  Authz: ownership, role check│
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │  Validation: DTOs, schemas   │
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │  Business logic (trusted)    │
                └────────────────────────────┘
```

## Code Examples

### BOLA Prevention (Ownership Check)

```typescript
// orders.controller.ts
@Get(':id')
@UseGuards(JwtAuthGuard)
async getOne(@Req() req: AuthedRequest, @Param('id') id: string) {
  const order = await this.ordersService.getById(id);
  if (!order) throw new NotFoundException();
  if (order.userId !== req.user.sub) {   // BOLA check
    // Return 404 (not 403) to avoid leaking existence
    throw new NotFoundException();
  }
  return order;
}
```

### BOLA Prevention (Database-Row-Level)

```typescript
// Better: enforce at the query layer
async getByIdForUser(id: string, userId: string): Promise<Order> {
  const order = await this.ordersRepo.findOne({ where: { id, userId } });
  if (!order) throw new NotFoundException();
  return order;
}
```

### BFLA Prevention (Role Guard)

```typescript
// common/guards/roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(ctx: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<Role[]>('roles', [
      ctx.getHandler(),
      ctx.getClass(),
    ]);
    if (!required?.length) return true;
    const req = ctx.switchToHttp().getRequest();
    return required.includes(req.user.role);
  }
}

// admin.controller.ts
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
@Controller('admin')
export class AdminController {
  @Post('users')
  create(@Body() dto: CreateUserDto) { ... }
}
```

### Object-Property-Level Authz (Mass Assignment)

```typescript
// ❌ DTO echoes any field the client sends
class UpdateUserDto {
  email?: string;
  isAdmin?: boolean;   // ← DANGER
}

// ✅ Use whitelist + a separate admin-only DTO
class UpdateUserDto {
  @IsEmail() @IsOptional() email?: string;
  @IsString() @IsOptional() name?: string;
  // no isAdmin here
}

// For admin, require a separate endpoint / DTO
class AdminUpdateUserDto extends UpdateUserDto {
  @IsBoolean() isAdmin!: boolean;
}
```

### Server-Side Request Forgery (SSRF) Prevention

```typescript
// utils/safe-fetch.ts
import { lookup } from 'dns/promises';
import { isIP } from 'net';

const PRIVATE_RANGES = [
  /^10\./, /^172\.(1[6-9]|2\d|3[01])\./, /^192\.168\./, /^127\./,
  /^169\.254\./, /^::1$/, /^fc[0-9a-f]{2}:/i, /^fe[89ab][0-9a-f]:/i,
];

export async function safeFetch(url: string): Promise<Response> {
  const u = new URL(url);
  if (u.protocol !== 'https:') throw new Error('https only');
  const ips = await lookup(u.hostname, { all: true });
  for (const { address } of ips) {
    if (PRIVATE_RANGES.some((re) => re.test(address)) || isIP(address) === 0) {
      throw new Error('private ip blocked');
    }
  }
  return fetch(url);
}
```

### Rate Limiting Per Route (NestJS `@nestjs/throttler`)

```typescript
// app.module.ts
ThrottlerModule.forRoot([{ name: 'default', ttl: 60_000, limit: 100 }]),

// login.controller.ts
@Post('login')
@Throttle({ default: { limit: 5, ttl: 60_000 } })   // 5/min per IP
async login(@Body() dto: LoginDto) { ... }
```

### Body Size Limit (Express / Fastify)

```typescript
// main.ts
app.use(express.json({ limit: '100kb' }));   // reject > 100KB
// Or with Fastify: fastify.register(import('@fastify/express'), { ... })
```

### Strict Response Shape (No Leak via JSON)

```typescript
// ❌ returning the whole user object including password hash
return this.userRepo.findById(id);

// ✅ project to a DTO; never echo back secrets
return plainToInstance(UserDto, user, { excludeExtraneousValues: true });
```

### Security Headers (helmet)

```typescript
// main.ts
import helmet from 'helmet';
app.use(helmet());
```

### CORS Strict

```typescript
// main.ts
app.enableCors({
  origin: ['https://app.example.com'],   // explicit allowlist
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
});
```

### Dependency Scanning in CI

```bash
# npm audit (or pnpm audit)
pnpm audit --prod --audit-level=high

# Snyk or Trivy for deeper scans
snyk test
```

## Real-World Use Cases

1. **Public REST API** — Helmet, strict CORS, rate limit, JWT validation, ownership check, DTO validation, structured errors with no stack traces.
2. **Mobile app backend** — Short-lived JWT (15 min) + refresh token rotation, push notifications for new device login, rate limit on auth endpoints.
3. **B2B partner API** — Per-partner API key, mTLS optional, per-partner rate limit, scoped OAuth2.
4. **Internal microservice mesh** — mTLS via service mesh (Istio/Linkerd), service-to-service authn, no public internet ingress.
5. **Webhook receiver** — HMAC signature verification (`X-Signature: sha256=...`), replay protection (timestamp + nonce), idempotency keys.
6. **Public file upload** — Pre-signed URLs (5-min TTL), server-side virus scan, MIME sniff, max-size enforcement.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| BOLA — endpoint returns any resource by id | Always check `resource.userId === jwt.sub` |
| Mass assignment — DTO has `isAdmin` | Separate admin DTO; never trust client-supplied role |
| Verbose errors with stack trace | Catch-all filter returns a safe body; log the full thing server-side |
| `*` CORS | Explicit allowlist; never use `*` with credentials |
| No rate limit on `/login` | Strict limit per IP + per account; lockout after N failures |
| Default credentials / sample data in prod | Enforce strong, rotated secrets; no debug routes in prod |
| Internal endpoints exposed by accident | Inventory check in CI; staging/prod parity |
| 3rd-party API responses trusted | Validate every external response against a schema (Zod / io-ts) |
| SSRF — `fetch(userInput)` | URL allowlist; resolve and block private IPs |
| Verbose logs that include JWTs / API keys | Structured logger with a redact list |

## Best Practices

1. **Default-deny authz** — Every endpoint requires auth unless explicitly public; every resource requires ownership.
2. **Whitelist DTOs** — `whitelist: true` + `forbidNonWhitelisted: true`; never accept fields you didn't ask for.
3. **Helmet + strict CORS** — At boot, always; never use `*` with credentials.
4. **Rate limit per route** — Aggressive on auth, write, and expensive-read endpoints.
5. **BOLA tests in CI** — A test that calls `GET /orders/<other-user-id>` and expects 404/403.
6. **Body size limit** — Reject > 100KB unless explicitly required; protect against log poisoning.
7. **Strict JSON response shape** — Project to DTOs; never echo the raw DB row.
8. **No secrets in error messages or logs** — Redact known keys; review log output in code review.
9. **SSRF allowlist + DNS resolution check** — Block private IP ranges for any user-supplied URL.
10. **Dependency scanning in CI** — `pnpm audit --audit-level=high` or Snyk; fail the build on criticals.
11. **API inventory** — Every endpoint documented in OpenAPI; staging and prod parity; deprecated endpoints are blocked, not "still there but 410".
12. **Webhook security** — HMAC signature + replay protection (timestamp window) + idempotency keys.

## Performance Considerations

- Auth/authz adds ~0.5–2ms per request; use connection pooling and JWT-cached key sets.
- Rate limiting with Redis is ~0.5ms; local in-memory is faster but not distributed.
- WAF (Cloudflare, AWS WAF) adds ~5–20ms p99; worth it for known-bad patterns.
- Dependency scanning in CI is slow; cache results, parallelize.

## Summary

- The OWASP API Top 10 (2023) is the senior anchor: BOLA, broken auth, mass assignment, unrestricted consumption, BFLA, SSRF, misconfig, sensitive flow, inventory, unsafe consumption.
- Defense in depth: edge (WAF, rate limit) → auth (JWT) → authz (ownership, role) → validation (DTOs) → business logic.
- BOLA is the #1 API breach pattern — always check `resource.userId === jwt.sub`.
- Mass assignment is #2 — whitelist DTOs; never let the client set `isAdmin`.

## Cheat Sheet

| Risk | Mitigation |
|------|------------|
| API1 BOLA | `resource.userId === jwt.sub` at the service layer |
| API2 Broken Auth | Strong JWT, RS256, key rotation, lockout, MFA |
| API3 Mass Assignment | Whitelist DTOs, `forbidNonWhitelisted`, separate admin DTOs |
| API4 Resource Consumption | Rate limit, body size, query result limits, timeouts |
| API5 BFLA | Role guard, server-side role lookup, no role from JWT claim alone |
| API6 Sensitive Flow | CAPTCHA, bot detection, per-account rate limit |
| API7 SSRF | URL allowlist, block private IPs, no user-supplied URLs to internal |
| API8 Misconfig | Helmet, strict CORS, no verbose errors, no defaults |
| API9 Inventory | OpenAPI per env, deprecated → 410, staging ≠ prod |
| API10 Unsafe Consumption | Validate every 3rd-party response (Zod), timeout, retry policy |

| Tool | Use |
|------|-----|
| Helmet | Security headers (HSTS, X-Frame-Options, etc.) |
| `@nestjs/throttler` | Rate limit per route |
| `class-validator` + `ValidationPipe` | Whitelist DTOs |
| `passport-jwt` / `jose` | JWT validation |
| `helmet-csp` | Content Security Policy |
| `gitleaks` / `trufflehog` | Secret scanning in CI |
| `snyk` / `pnpm audit` | Dependency scanning |
| `schemathesis` | OpenAPI contract fuzzing |
| OWASP ZAP | API DAST scanning |

---

## See Also
- [Microservices](../12-Microservices/) (mTLS in service mesh)
- [REST APIs](../07-REST-API/) (rate limiting, CORS, error handling)
- [System Design](../11-System-Design/) (security in design)
- [Threat Modeling](./11-Threat-Modeling-STRIDE.md) (per-system enumeration)
- [Web Security](./09-Web-Security.md) (HTTPS, headers, OWASP Top 10)

## References & Learn More

- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP API Security Checklist](https://github.com/OWASP/API-Security/blob/master/editions/2023/en/0x00-header.md)
- [helmet](https://helmetjs.github.io/)
- [NestJS Throttler](https://github.com/nestjs/throttler)
- [Auth0 — JWT Best Practices](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-best-practices)
- [PortSwigger — API Security Academy](https://portswigger.net/web-security/api-security)
