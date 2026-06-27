# Backend Cheat Sheet

## Quick Reference Table

| Concept | Key Point | Code/Example |
|---------|-----------|--------------|
| NestJS Module | `@Module({})` — organizes code by feature; imports/exports providers | `@Module({ imports: [TypeOrmModule.forFeature([User])], controllers: [UserController], providers: [UserService] })` |
| NestJS Controller | `@Controller('prefix')` — handles HTTP requests; defines routes | `@Controller('users') export class UserController { @Get() findAll() {} }` |
| NestJS Provider | Injectable services; DI container manages lifecycle | `@Injectable() export class UserService { constructor(private prisma: PrismaService) {} }` |
| NestJS Guard | `@UseGuards()` — runs before handler; auth, roles, rate limiting | `@Injectable() export class AuthGuard implements CanActivate { canActivate(ctx) {} }` |
| NestJS Pipe | Transform/validate data before handler; `ValidationPipe` | `@UsePipes(new ValidationPipe({ whitelist: true }))` |
| NestJS Interceptor | `@UseInterceptors()` — wrap handler; logging, caching, transforms | `@Injectable() export class LoggingInterceptor implements NestInterceptor { intercept(ctx, next) {} }` |
| NestJS Filter | Exception filter; custom error responses | `@Catch(HttpException) export class HttpExceptionFilter implements ExceptionFilter {}` |
| NestJS Middleware | `@Middleware()` — runs before guards; Express/Connect compatible | `app.use(cors())` or `consumer.apply(cors()).forRoutes('*')` |
| NestJS Lifecycle | OnModuleInit → OnApplicationBootstrap → OnApplicationShutdown | `onModuleInit() { await this.init(); }` |
| REST — Resources | Nouns, plural, hierarchical: `/users`, `/users/:id/posts` | `GET /users/123/posts` |
| REST — Methods | GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove) | `PATCH /users/123` — partial update |
| REST — Status Codes | 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Too Many Requests, 500 Internal | Return correct codes, not just 200 |
| REST — Versioning | URL (`/v1/users`), Header (`Accept-Version`), Query (`?version=1`) | URL versioning is simplest and most common |
| REST — Pagination | Offset (page/limit) or Cursor (after/first) | Cursor better for large datasets; `?cursor=abc&first=10` |
| REST — HATEOAS | Include links for discoverability | `{ "links": { "self": "/users/123", "posts": "/users/123/posts" } }` |
| PostgreSQL — Index | B-tree default; GIN for full-text/JSON; GiST for spatial; BRIN for large sorted | `CREATE INDEX idx_users_email ON users(email);` |
| PostgreSQL — Composite Index | Index on multiple columns; order matters for query patterns | `CREATE INDEX idx_posts_author_date ON posts(author_id, created_at DESC);` |
| PostgreSQL — Covering Index | INCLUDE columns to avoid table lookups | `CREATE INDEX idx_covering ON users(email) INCLUDE (name, avatar);` |
| PostgreSQL — EXPLAIN | Analyze query plans; Sequential Scan vs Index Scan | `EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'x';` |
| PostgreSQL — Transactions | ACID; BEGIN → COMMIT / ROLLBACK; savepoints for nested | `BEGIN; UPDATE accounts SET balance = balance - 100 WHERE id = 1; COMMIT;` |
| PostgreSQL — Isolation Levels | Read Uncommitted → Read Committed → Repeatable Read → Serializable | Default: Read Committed; Serializable for strict consistency |
| PostgreSQL — MVCC | Multi-Version Concurrency Control; readers don't block writers | Old row versions kept until vacuum removes them |
| PostgreSQL — VACUUM | Reclaim space from dead tuples; ANALYZE updates statistics | `VACUUM (VERBOSE, ANALYZE) users;` or autovacuum |
| PostgreSQL — Partitioning | Range, List, or Hash; split large tables for performance | `CREATE TABLE orders_2024 PARTITION OF orders FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');` |
| PostgreSQL — CTE | Common Table Expression; readable subqueries; materialized | `WITH active_users AS (SELECT * FROM users WHERE active = true) SELECT * FROM active_users;` |
| PostgreSQL — Window Functions | `OVER()` — aggregate without collapsing rows | `ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)` |
| PostgreSQL — JSONB | Binary JSON; indexed, queryable; `@>`, `?`, `->`, `->>` operators | `SELECT * FROM products WHERE metadata @> '{"color": "red"}';` |
| Prisma | Type-safe ORM; schema-first; migrations; auto-generated client | `const users = await prisma.user.findMany({ where: { active: true } });` |
| Prisma — Relations | `@relation`, include/select, nested writes | `await prisma.user.findUnique({ where: { id }, include: { posts: true } });` |
| Prisma — Transactions | Interactive (client-level) or batch (query-level) | `await prisma.$transaction([prisma.user.create({ data: ... }), prisma.post.create({ data: ... })]);` |
| Prisma — Raw SQL | `prisma.$queryRaw` for complex queries not supported by Prisma | `await prisma.$queryRaw\`SELECT * FROM users WHERE id = ${id}\`` |
| Prisma — Migrations | `prisma migrate dev` (dev), `prisma migrate deploy` (prod) | `npx prisma migrate dev --name add_posts_table` |
| JWT | Header.Payload.Signature; stateless; include in `Authorization: Bearer <token>` | `jwt.sign(payload, secret, { expiresIn: '1h' })` |
| JWT — Access + Refresh | Short-lived access (15m), long-lived refresh (7d); rotate refresh | Access for API calls; refresh to get new access without re-login |
| OAuth 2.0 | Authorization Code flow (web), PKCE (SPA/mobile), Client Credentials (server-to-server) | Auth code → exchange for token → use token → refresh |
| OAuth — Scopes | Request minimum permissions; display to user for consent | `scope: 'read:profile write:posts'` |
| XSS | Inject scripts via user input; sanitize output, CSP headers | Never use `innerHTML`; use DOMPurify; `Content-Security-Policy` header |
| CSRF | Forge requests from other sites; use SameSite cookies, CSRF tokens | `SameSite=Strict` or `SameSite=Lax`; custom header check |
| SQL Injection | Inject SQL via user input; use parameterized queries | `prisma.user.findMany({ where: { id } })` — Prisma parameterizes |
| Rate Limiting | Limit requests per IP/user; sliding window or token bucket | `@UseGuards(ThrottlerGuard)` in NestJS |
| CORS | Cross-Origin Resource Sharing; configure allowed origins/methods | `app.use(cors({ origin: 'https://example.com', methods: ['GET', 'POST'] }))` |
| Helmet | Security headers; X-Content-Type-Options, X-Frame-Options, etc. | `app.use(helmet())` in NestJS/Express |
| bcrypt / argon2 | Password hashing; bcrypt with salt rounds; argon2 for memory-hard | `const hash = await bcrypt.hash(password, 12);` |
| Input Validation | Validate and sanitize all user input; class-validator + class-transformer | `@IsEmail() @IsString() email: string;` |
| idempotency | Same request produces same result; use idempotency keys for POST | `X-Idempotency-Key: <uuid>` header |
| Circuit Breaker | Stop calling failing service; half-open after timeout | `@UseGuards(CircuitBreakerGuard)` or opossum library |
| Health Checks | `/health` endpoint; check DB, cache, external services | NestJS: `@nestjs/terminus` module |
| Logging | Structured JSON logs; request ID correlation; different levels | `nest build` + Winston or `@nestjs/common` Logger |
| OpenAPI/Swagger | Auto-generate API docs from decorators | `SwaggerModule.setup('api', app, document)` |

## Top 10 Things to Remember

1. **NestJS is modular and DI-based**. Everything is a module. Providers are injectable services. Controllers handle HTTP. Guards, pipes, interceptors, and filters cross-cut concerns.

2. **REST: resources are nouns, HTTP methods are verbs**. `GET /users` not `GET /getUsers`. Use proper status codes (201 for create, 204 for delete).

3. **PostgreSQL indexes are B-tree by default**. Composite indexes: column order matters. Use `EXPLAIN ANALYZE` to verify index usage. Missing indexes = slow queries.

4. **ACID transactions are not optional for financial data**. Use `BEGIN`, check constraints, handle deadlocks, and always have a rollback strategy.

5. **MVCC means readers don't block writers** but old versions accumulate. `VACUUM` reclaims space. Monitor `pg_stat_user_tables` for dead tuple counts.

6. **Prisma generates type-safe client from schema**. Use `include`/`select` for relations. Batch transactions for atomic operations. Migrations in dev, deploy in prod.

7. **JWT is stateless — no server-side revocation by default**. Short access tokens (15m), long refresh tokens (7d). Rotate refresh tokens. Store securely (httpOnly cookie, not localStorage).

8. **OAuth 2.0 Authorization Code + PKCE** is the standard for SPAs and mobile apps. Never use Implicit flow. Always validate state parameter.

9. **Sanitize all input, encode all output**. Prevent XSS with CSP headers. Use parameterized queries (Prisma does this). CSRF tokens or SameSite cookies.

10. **Rate limiting is a must**. Sliding window or token bucket. Per-IP for public APIs, per-user for authenticated. Return 429 with `Retry-After` header.

## Common Patterns

### NestJS CRUD Controller
```ts
@Controller('users')
@UseGuards(AuthGuard)
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  @UseInterceptors(CacheInterceptor)
  findAll(@Query() query: PaginationDto) {
    return this.userService.findAll(query);
  }

  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.userService.findOne(id);
  }

  @Post()
  @HttpCode(201)
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateUserDto) {
    return this.userService.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(204)
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.userService.remove(id);
  }
}
```

### PostgreSQL Index Strategy
```sql
-- Single column lookup
CREATE INDEX idx_users_email ON users(email);

-- Composite for common query pattern (equality + range)
CREATE INDEX idx_posts_author_date ON posts(author_id, created_at DESC);

-- Partial index (only active users)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Covering index (avoids table lookup)
CREATE INDEX idx_user_covering ON users(id) INCLUDE (name, email, avatar_url);

-- GIN for JSONB queries
CREATE INDEX idx_products_metadata ON products USING GIN(metadata);

-- GIN for full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || content));

-- BRIN for naturally ordered data (timestamps)
CREATE INDEX idx_logs_created ON logs USING BRIN(created_at);

-- EXPLAIN to verify
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM posts WHERE author_id = 123 AND created_at > '2024-01-01';
```

### Prisma Schema with Relations
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@index([createdAt])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]

  @@index([authorId, createdAt(sort: Desc)])
  @@index([published])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]
}
```

### JWT Auth Flow
```ts
// Token generation
async generateTokens(user: User) {
  const payload = { sub: user.id, email: user.email };

  const [accessToken, refreshToken] = await Promise.all([
    this.jwtService.signAsync(payload, { expiresIn: '15m' }),
    this.jwtService.signAsync(payload, { expiresIn: '7d', secret: this.config.get('REFRESH_SECRET') }),
  ]);

  // Store refresh token hash
  await this.prisma.refreshToken.create({
    data: {
      token: await bcrypt.hash(refreshToken, 10),
      userId: user.id,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    },
  });

  return { accessToken, refreshToken };
}

// Token refresh
async refresh(refreshToken: string) {
  const payload = this.jwtService.verify(refreshToken, {
    secret: this.config.get('REFRESH_SECRET'),
  });

  const stored = await this.prisma.refreshToken.findFirst({
    where: { userId: payload.sub, revoked: false },
  });

  if (!stored || !(await bcrypt.compare(refreshToken, stored.token))) {
    throw new UnauthorizedException('Invalid refresh token');
  }

  // Rotate: revoke old, issue new
  await this.prisma.refreshToken.update({
    where: { id: stored.id },
    data: { revoked: true },
  });

  return this.generateTokens({ id: payload.sub, email: payload.email });
}
```

### Rate Limiting (NestJS)
```ts
// throttler.module.ts
@Module({
  imports: [
    ThrottlerModule.forRoot([
      { name: 'short', ttl: 1000, limit: 3 },
      { name: 'medium', ttl: 10000, limit: 20 },
      { name: 'long', ttl: 60000, limit: 100 },
    ]),
  ],
})
export class ThrottlerConfigModule {}

// Custom throttle decorator
export const SkipThrottle = () => SetMetadata('skipThrottle', true);

// Per-user throttle
export const UserThrottle = (ttl: number, limit: number) =>
  SetMetadata('throttle', { [`${limit}-${ttl}`]: { ttl, limit } });
```

### Input Validation (DTOs)
```ts
// create-user.dto.ts
export class CreateUserDto {
  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsString()
  @MinLength(8)
  @MaxLength(128)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase, and number',
  })
  password: string;

  @IsOptional()
  @IsString()
  @MaxLength(100)
  name?: string;

  @IsEnum(Role)
  @IsOptional()
  role?: Role;
}

// Global validation pipe
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,        // Strip unknown properties
  forbidNonWhitelisted: true, // Throw on unknown properties
  transform: true,        // Auto-transform to DTO types
}));
```

### Health Check
```ts
// health.controller.ts
@Controller('health')
export class HealthController {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.prisma.$queryRaw`SELECT 1`,
      () => this.redis.ping(),
    ]);
  }
}
```

### Structured Logging
```ts
// logger.service.ts
@Injectable()
export class AppLogger implements LoggerService {
  private logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
      winston.format.timestamp(),
      winston.format.json(),
    ),
    defaultMeta: { service: 'my-api' },
    transports: [new winston.transports.Console()],
  });

  log(message: string, context?: string, requestId?: string) {
    this.logger.info(message, { context, requestId });
  }

  error(message: string, trace: string, context?: string, requestId?: string) {
    this.logger.error(message, { trace, context, requestId });
  }
}
```

### Database Transaction (Prisma)
```ts
// Interactive transaction
async transfer(fromId: string, toId: string, amount: number) {
  return this.prisma.$transaction(async (tx) => {
    const from = await tx.account.findUnique({ where: { id: fromId } });
    const to = await tx.account.findUnique({ where: { id: toId } });

    if (from.balance < amount) {
      throw new BadRequestException('Insufficient funds');
    }

    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });

    await tx.transaction.create({
      data: { fromId, toId, amount, type: 'TRANSFER' },
    });

    return { success: true };
  });
}
```

## Red Flags (Things NOT to Say)

- **"I return 200 for everything"** — Incorrect status codes confuse clients and monitoring. Use proper REST status codes.
- **"I don't use transactions"** — Leads to inconsistent data. Always use transactions for multi-step operations.
- **"I store JWT in localStorage"** — Vulnerable to XSS. Use httpOnly, secure, SameSite cookies.
- **"I use ORM for everything including complex reports"** — ORMs have limits. Use raw SQL for complex queries, reporting, and performance-critical paths.
- **"I don't validate input on the backend"** — Frontend validation is UX, backend is security. Always validate server-side.
- **"I use MD5 for passwords"** — Insecure. Use bcrypt (12+ rounds) or argon2.
- **"PostgreSQL and MySQL are basically the same"** — They differ significantly in features (JSONB, CTEs, MVCC, extensions).
- **"I skip EXPLAIN ANALYZE"** — You're guessing about performance. Always verify query plans.
- **"I don't need rate limiting"** — Every public API needs rate limiting. DDoS, brute force, and abuse are real.
- **"REST is better than GraphQL"** — They serve different purposes. Don't say one is universally better.

## Green Flags (Things TO Say)

- **"I use parameterized queries — Prisma does this by default, preventing SQL injection."** — Security-conscious.
- **"I store refresh tokens hashed in the database for revocation."** — Proper JWT architecture.
- **"I use EXPLAIN ANALYZE to verify index usage and optimize query plans."** — Performance-oriented.
- **"I use `SameSite=Strict` cookies for session tokens to prevent CSRF."** — Modern security practice.
- **"I validate input with class-validator DTOs and strip unknown properties with `whitelist: true`."** — Defense in depth.
- **"I use composite indexes in the right column order for my query patterns."** — Database optimization knowledge.
- **"I separate read and write models when CQRS makes sense."** — Architecture awareness.
- **"I use circuit breakers to prevent cascading failures in microservices."** — Resilience patterns.
- **"I implement idempotency keys for POST requests to handle retries safely."** — Distributed systems knowledge.
- **"I use structured JSON logging with request IDs for correlation."** — Observability best practice.

## 5-Minute Pre-Interview Review

- **NestJS Architecture**: Module → Controller → Service. Guards (auth), Pipes (validation), Interceptors (logging/caching), Filters (exception handling). DI everywhere.
- **REST Principles**: Resources as nouns, HTTP methods as verbs, proper status codes, pagination (cursor > offset), versioning, HATEOAS.
- **PostgreSQL Indexes**: B-tree (default), GIN (JSONB/full-text), GiST (spatial), BRIN (large sorted), partial (WHERE clause), covering (INCLUDE). Composite index order matters.
- **Transactions**: ACID. BEGIN → operations → COMMIT/ROLLBACK. Isolation levels: Read Committed (default), Serializable (strict). MVCC: readers don't block writers.
- **Prisma**: Schema-first ORM. `findMany`, `findUnique`, `create`, `update`, `delete`. `include`/`select` for relations. `$transaction` for multi-step. Migrations: `migrate dev` (dev), `migrate deploy` (prod).
- **JWT**: Access (short-lived, 15m) + Refresh (long-lived, 7d). Store in httpOnly cookie. Rotate refresh tokens. Stateless — no server-side revocation without blacklist.
- **OAuth 2.0**: Authorization Code + PKCE for SPAs/mobile. Client Credentials for server-to-server. Always validate `state` parameter. Request minimal scopes.
- **Security**: XSS (sanitize output, CSP headers), CSRF (SameSite cookies, tokens), SQL injection (parameterized queries), rate limiting, bcrypt/argon2 for passwords.
- **Validation**: class-validator decorators on DTOs. `ValidationPipe` with `whitelist: true` strips unknown fields. `forbidNonWhitelisted` throws on extra fields.
- **Monitoring**: Health checks (`/health`), structured JSON logging, request ID correlation, EXPLAIN ANALYZE for queries, circuit breakers for external services.

---

## References & Learn More
- [Cheat Sheet Collection](https://github.com/detailyang/awesome-cheatsheet)
- [DevHints](https://devhints.io/)
- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
