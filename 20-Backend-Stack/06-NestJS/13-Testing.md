---
section: NestJS
category: Backend
tags: [concept]
---

# Testing NestJS Applications

> **TL;DR:** NestJS testing is built on Jest with a TestingModule that creates a sandboxed DI container per test — unit tests override providers with mocks, e2e tests boot the full HTTP app with `supertest`. The senior test is knowing the difference between isolated provider mocking, integration over a real DB, and contract testing, plus how to keep test suites fast.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

Testing in NestJS is layered: **unit tests** instantiate a single class with all its dependencies mocked via `Test.createTestingModule({ providers: [...] })`; **integration tests** boot a slice of the app (e.g. one module wired against a real DB or a Testcontainers PostgreSQL); and **end-to-end tests** boot the full `NestFactory.create` HTTP application and drive it with `supertest`. NestJS ships first-class Jest support and the `TestingModule` abstraction that mirrors the production DI container.

## Why Do We Need It?

1. **Refactor Confidence** — A 200-service monorepo without tests is a refactor that cannot happen.
2. **Contract Protection** — API contract tests catch breaking changes in serializers, DTOs, and guards.
3. **DI Verification** — `TestingModule` proves your DI graph is correct (missing providers, circular deps) at test time, not boot time.
4. **Regression Prevention** — Especially for guards, pipes, and interceptors that wire the request lifecycle.
5. **Documentation** — Well-written tests document how a service is supposed to be used and what it returns on edge cases.
6. **Safe Migrations** — DB-touching integration tests with real schema migrations catch SQL errors that mocks hide.
7. **CI Pipeline** — Senior teams gate merges on `pnpm test` plus the lint/type/boundary checks; the test layer must be reliable.

## How It Works

### Test Layers

```text
┌────────────────────────────────────────────────────────────────┐
│                       Test Pyramid                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│                          ╱╲                                     │
│                         ╱  ╲         E2E (slow, few)            │
│                        ╱    ╲       Boot full app + supertest   │
│                       ╱──────╲                                  │
│                      ╱        ╲     Integration (medium)        │
│                     ╱          ╲    Real DB (Testcontainers)    │
│                    ╱────────────╲   One module wired            │
│                   ╱              ╲                              │
│                  ╱   Unit (many)  ╲  Pure class + mocked deps   │
│                 ╱                  ╲ Test.createTestingModule   │
│                ╱────────────────────╲                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### TestingModule Lifecycle

```text
Test.createTestingModule({...})
  .useValue / useMock / useClass
  .overrideProvider(RealService).useValue(mockService)
  .compile()
        │
        ▼
   module.get<Service>(Service)  // resolved from sandbox container
        │
        ▼
   await module.close()          // teardown for afterEach
```

## Code Examples

### Unit Test with a Mocked Provider

```typescript
// users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';
import { NotFoundException } from '@nestjs/common';

describe('UsersService', () => {
  let service: UsersService;
  let repo: jest.Mocked<UsersRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UsersRepository,
          useValue: {
            findById: jest.fn(),
            save: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(UsersService);
    repo = module.get(UsersRepository);
  });

  afterEach(() => jest.clearAllMocks());

  it('throws NotFoundException when user is missing', async () => {
    repo.findById.mockResolvedValue(null);
    await expect(service.getById('nope')).rejects.toBeInstanceOf(NotFoundException);
  });

  it('returns the user when found', async () => {
    const user = { id: '1', email: 'a@b.com' };
    repo.findById.mockResolvedValue(user);
    await expect(service.getById('1')).resolves.toEqual(user);
    expect(repo.findById).toHaveBeenCalledWith('1');
  });
});
```

### E2E Test with Supertest

```typescript
// test/app.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('Users API (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleRef: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('rejects invalid email with 400', async () => {
    const res = await request(app.getHttpServer())
      .post('/users')
      .send({ email: 'not-an-email' })
      .expect(400);
    expect(res.body.message).toEqual(expect.arrayContaining([expect.stringMatching(/email/i)]));
  });

  it('creates a user and returns 201 with id', async () => {
    const res = await request(app.getHttpServer())
      .post('/users')
      .send({ email: 'a@b.com', name: 'Alice' })
      .expect(201);
    expect(res.body.id).toBeDefined();
  });
});
```

### Integration Test with Testcontainers (PostgreSQL)

```typescript
// test/users.integration-spec.ts
import { Test } from '@nestjs/testing';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersModule } from '../src/users/users.module';
import { UsersService } from '../src/users/users.service';

describe('UsersService (integration)', () => {
  let container: StartedPostgreSqlContainer;
  let app: any;
  let service: UsersService;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:16-alpine').start();

    const moduleRef = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'postgres',
          url: container.getConnectionUri(),
          autoLoadEntities: true,
          synchronize: true,
        }),
        UsersModule,
      ],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
    service = app.get(UsersService);
  }, 60_000);

  afterAll(async () => {
    await app?.close();
    await container?.stop();
  });

  it('persists and fetches a user', async () => {
    const created = await service.create({ email: 'a@b.com', name: 'A' });
    const fetched = await service.getById(created.id);
    expect(fetched.email).toBe('a@b.com');
  });
});
```

### Overriding a Provider Globally for a Test Suite

```typescript
// When you only want to swap one dep without rebuilding the whole module
const moduleRef = await Test.createTestingModule({
  imports: [AppModule],
})
  .overrideProvider(ConfigService)
  .useValue({ get: () => 'test-value' })
  .overrideGuard(JwtAuthGuard)
  .useValue({ canActivate: () => true })   // bypass auth in tests
  .compile();
```

## Real-World Use Cases

1. **API contract tests** — `supertest` against the booted app to ensure controllers, validation pipes, and exception filters all compose correctly. The test fails if any layer misbehaves.
2. **Microservice transport tests** — Mock the `ClientProxy` to verify `emit()` / `send()` payloads without standing up a broker.
3. **Database integration** — Testcontainers spins up a real PostgreSQL/MySQL so migrations and SQL queries run against the actual engine.
4. **Cron/Scheduled tasks** — Trigger `@Cron` handlers manually in tests using `SchedulerRegistry` to verify they read and write correctly.
5. **Authn/Authz** — Test guards and roles decorators with a real JWT fixture (and a fake signing key) to verify the full policy.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mocking the service under test instead of its dependencies | Mock collaborators (repo, external clients), not the SUT itself. |
| Using `synchronize: true` in e2e against shared DB | Use Testcontainers or per-test schema; never run migrations on a shared DB. |
| Not closing the `INestApplication` between tests | Always `await app.close()` in `afterAll` to release DB connections. |
| Asserting on implementation details (private methods) | Assert on observable behavior — return values, thrown exceptions, emitted events. |
| Reusing global state across tests (e.g., single PrismaClient) | Use a per-test container, or wrap each test in a transaction that rolls back. |
| E2E tests for trivial CRUD | Reserve e2e for the request lifecycle, auth, and validation; CRUD belongs in unit/integration. |

## Best Practices

1. **Use `Test.createTestingModule`** — It mirrors production DI, so the test fails if your wiring is broken.
2. **Mock at the boundary** — Replace repositories, HTTP clients, and brokers with `useValue` mocks; let real services talk to each other.
3. **Use Testcontainers for DB** — In-memory SQLite or mocked repos hide SQL errors; a real container in CI catches them.
4. **Cover guards, pipes, and interceptors explicitly** — They are the request lifecycle and they break silently otherwise.
5. **Test the failure path first** — `NotFoundException`, `UnauthorizedException`, and `BadRequestException` paths are the highest-value tests.
6. **Parallelize** — Jest workers + sharded test suites. If your e2e suite takes 5 min serial, shard it across 4 machines and gate merges on a 90-second run.
7. **Snapshot only stable output** — Avoid snapshotting the whole `app.getHttpServer()` response body; snapshot the parts that are stable.
8. **One assertion per concept** — Multiple `expect`s in one test are fine if they describe one behavior; don't bundle unrelated behaviors.
9. **CI cache for `node_modules` and Docker layers** — Testcontainers pulls images on every run unless cached.
10. **Tag slow tests** — Use Jest projects / `testPathIgnorePatterns` so a fast unit loop is sub-10-seconds.

## Performance Considerations

- **E2E is the bottleneck** — Every `Test.createTestingModule({ imports: [AppModule] })` boot costs 200ms–2s. Use partial imports (`UsersModule` only) for module tests.
- **Testcontainers is the second** — Image pull is the killer. Pre-pull in CI, or use a smaller image (alpine).
- **Jest worker count** — Default `cpu_count - 1`. For e2e with containers, drop to 1–2 workers to avoid port collisions.
- **Module compile per test** — `beforeAll` not `beforeEach` for the heavy compile; use `beforeEach` only for the cheap mock reset.
- **Avoid `useValue: actualHugeService`** — If you find yourself injecting a real heavy service into a unit test, that's an integration test, not a unit test — split it.

## Summary

- NestJS testing is built on `Test.createTestingModule` + Jest, with three layers: unit (mocked deps), integration (real DB via Testcontainers), and e2e (full app + supertest).
- Mock collaborators, not the system under test; cover the request lifecycle (guards, pipes, interceptors, filters) explicitly.
- Testcontainers + a real engine is the only way to catch real SQL bugs; in-memory mocks hide them.
- Boot cost dominates — boot the smallest module possible and shard the suite in CI.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `Test.createTestingModule` | Builds a sandboxed DI container for the test |
| `overrideProvider(X).useValue(...)` | Swap a provider with a mock globally for the module |
| `overrideGuard(X).useValue({ canActivate: () => true })` | Bypass auth in e2e |
| `module.get<T>(T)` | Resolve a provider from the compiled test module |
| `app.close()` | Release DB connections / app resources between tests |
| `Testcontainers` | Real PostgreSQL/MySQL/Redis inside the test runner |
| `supertest(app.getHttpServer())` | Drive the booted HTTP app without a real port |
| `Jest.Mocked<T>` | Type helper to type a `useValue` mock |
| `synchronize: true` | OK in tests, **never** in prod |
| `beforeAll` vs `beforeEach` | Compile in `beforeAll`; reset mocks in `beforeEach` |

---

## See Also
- [Design Patterns](../10-Design-Patterns/) (Repository, Dependency Injection)
- [Microservices](../12-Microservices/) (testing message-driven services)
- [Node.js](../05-NodeJS/) (Jest configuration, async testing)
- [REST APIs](../07-REST-API/) (API contract testing)

## References & Learn More

- [NestJS Testing Official Docs](https://docs.nestjs.com/fundamentals/testing)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Supertest GitHub](https://github.com/ladjs/supertest)
- [Testcontainers Node](https://node.testcontainers.org/)
- [Testing NestJS with Testcontainers — Trilon](https://trilon.io/blog/testing-nestjs-with-testcontainers)
- [Effective NestJS Testing Strategies](https://docs.nestjs.com/fundamentals/testing#testing-utilities)
