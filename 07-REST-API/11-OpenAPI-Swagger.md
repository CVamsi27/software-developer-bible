---
section: REST API
category: Backend
tags: [concept]
---

# OpenAPI / Swagger Documentation

> **TL;DR:** OpenAPI is a machine-readable contract for your HTTP API; Swagger is the tooling that renders it. In NestJS the `@nestjs/swagger` package generates the spec from decorators on controllers and DTOs, so the spec and code stay in sync. The senior test is treating the spec as a contract, versioning it, and using it to drive client SDKs and contract tests.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**OpenAPI** (formerly Swagger Specification) is a vendor-neutral, JSON/YAML description format for HTTP APIs. It defines every endpoint, request body, response shape, status code, and authentication scheme in a single document. **Swagger** is the umbrella term for the tooling around OpenAPI: Swagger UI (interactive docs), Swagger Editor (spec authoring), Swagger Codegen (client/server generation). In NestJS, `@nestjs/swagger` scans your controllers and DTOs at boot to auto-generate the spec, and serves Swagger UI at a configurable path.

## Why Do We Need It?

1. **Single source of truth** — The spec is the contract; client SDKs, mocks, contract tests, and docs all derive from it.
2. **Discoverability** — New team members explore the API in Swagger UI instead of asking Slack.
3. **Client generation** — Generate TypeScript, Java, Python, Go clients from the spec; no hand-written wrappers.
4. **Contract testing** — Run `schemathesis` or `Dredd` against the spec to verify the implementation matches the contract.
5. **Mock servers** — `prism` or `swagger-api-mock` can serve a fake API from the spec, so frontends don't block on backends.
6. **Onboarding & QA** — QA writes tests against Swagger UI without reading code.
7. **Governance** — Reviewing the diff of an OpenAPI PR is a real API review — much higher signal than reviewing controller code.

## How It Works

```text
Code (Controllers, DTOs, decorators)
   │
   ▼
@nestjs/swagger scans at boot
   │
   ├── @ApiOperation, @ApiResponse, @ApiParam, @ApiQuery, @ApiBody
   ├── @ApiProperty on DTO fields
   ├── @ApiTags for grouping
   ├── @ApiBearerAuth, @ApiOAuth2 for security
   │
   ▼
OpenAPI 3.x JSON document  (exposed at /api-json)
   │
   ├── Swagger UI       (interactive docs at /api)
   ├── ReDoc            (clean reference at /redoc)
   ├── Client SDKs      (openapi-generator, orval, openapi-typescript)
   ├── Mock server      (prism mock)
   └── Contract tests   (schemathesis, Dredd)
```

## Code Examples

### Bootstrapping Swagger in a NestJS App

```typescript
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('Orders API')
    .setDescription('Public orders & payments API')
    .setVersion('2.0.0')
    .addBearerAuth({ type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }, 'access-token')
    .addOAuth2(
      {
        type: 'oauth2',
        flows: {
          authorizationCode: {
            authorizationUrl: 'https://auth.example.com/oauth/authorize',
            tokenUrl: 'https://auth.example.com/oauth/token',
            scopes: { 'orders:read': 'Read orders', 'orders:write': 'Write orders' },
          },
        },
      },
      'oauth2',
    )
    .addTag('orders', 'Customer order lifecycle')
    .addServer('https://api.example.com')
    .build();

  const document = SwaggerModule.createDocument(app, config, {
    operationIdFactory: (ctrl, method) => `${ctrl}-${method}`,  // stable for client gen
  });
  SwaggerModule.setup('api', app, document, {
    swaggerOptions: { persistAuthorization: true },
  });

  await app.listen(3000);
}
```

### Decorating a Controller

```typescript
// orders.controller.ts
import { ApiOperation, ApiResponse, ApiTags, ApiBearerAuth, ApiParam } from '@nestjs/swagger';

@ApiTags('orders')
@ApiBearerAuth('access-token')
@Controller('orders')
export class OrdersController {
  @Get(':id')
  @ApiOperation({ summary: 'Get an order by id', operationId: 'getOrder' })
  @ApiParam({ name: 'id', type: 'string', format: 'uuid' })
  @ApiResponse({ status: 200, type: OrderDto })
  @ApiResponse({ status: 404, description: 'Order not found' })
  @ApiResponse({ status: 401, description: 'Unauthenticated' })
  async getOne(@Param('id') id: string): Promise<OrderDto> {
    return this.ordersService.getById(id);
  }
}
```

### Decorating a DTO

```typescript
// dto/order.dto.ts
import { ApiProperty } from '@nestjs/swagger';

export class OrderDto {
  @ApiProperty({ example: 'ord_01HXYZ', description: 'Unique order id' })
  id!: string;

  @ApiProperty({ example: 'cus_01HABC', description: 'Customer who placed the order' })
  customerId!: string;

  @ApiProperty({ enum: ['pending', 'paid', 'shipped', 'cancelled'], example: 'pending' })
  status!: 'pending' | 'paid' | 'shipped' | 'cancelled';

  @ApiProperty({ type: () => [LineItemDto] })
  items!: LineItemDto[];

  @ApiProperty({ example: '2025-01-15T10:00:00Z', format: 'date-time' })
  createdAt!: Date;
}
```

### Generating a TypeScript Client (orval)

```bash
# Save the live spec
curl -s http://localhost:3000/api-json > openapi.json

# Generate a typed client
npx orval --input openapi.json --output src/api/orders.ts
```

```typescript
// src/api/orders.ts (generated)
import { getOrder } from './api/orders';
const order = await getOrder({ id: 'ord_01HXYZ' });
//    ^? typed as OrderDto
```

### Contract Test with schemathesis

```bash
# schemathesis fuzz-tests the running API against the spec
pip install schemathesis
schemathesis run http://localhost:3000/api-json --checks all
```

## Real-World Use Cases

1. **Public API portal** — Host Swagger UI or ReDoc at `/docs` for external developers; version the spec alongside the API.
2. **Frontend / backend parallelization** — Generate a TS client, mock a server, and start frontend work before the backend is ready.
3. **Internal API registry** — Crawl all services, collect their specs, host a developer portal (Backstage, Stoplight, Mintlify).
4. **Contract testing in CI** — `schemathesis` runs in CI; if a controller change violates the spec, the build fails.
5. **SDK distribution** — Publish the generated client as an npm package for downstream teams.
6. **API governance** — Lint the spec in CI: required `operationId`, no `any` types, `200`/`4xx`/`5xx` responses on every endpoint.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Spec drifts from code because of hand-edit | Always generate from code (`@nestjs/swagger`); never hand-write |
| `any` types in DTOs | Use class-validator + `@ApiProperty({ type: X })` so the generator sees the shape |
| No `operationId` | Use `operationIdFactory` so client generation is stable across PRs |
| One giant spec for hundreds of services | Per-service spec + a stitched master spec, or a developer portal |
| Exposing Swagger UI in production without auth | Lock the docs path behind auth or an IP allowlist |
| Skipping `ApiResponse` for error codes | Document 400/401/403/404/422 — these are the ones clients will read |
| No versioning on the spec | Tag the spec with the API version (`info.version` + URL path) |

## Best Practices

1. **Generate, don't hand-write** — `@nestjs/swagger` reflects over the code; if a decorator is missing, fix the code, not the spec.
2. **Stable `operationId`** — Use `operationIdFactory: (ctrl, method) => \`${ctrl}-${method}\``; never let it default to method names that may collide.
3. **Document errors** — Add `@ApiResponse({ status: 4xx, type: ErrorResponseDto })` for every realistic client error.
4. **Version the spec** — `info.version` matches the API version; expose `/v2/api-json` and `/v2/api` alongside `/v1/...` during deprecation windows.
5. **Lint in CI** — Spectral or vacuum-cli catches missing descriptions, missing examples, and `any` types.
6. **Two UI options** — Swagger UI for "try it out", ReDoc for the clean reference; both from the same spec.
7. **Lock the docs in production** — Behind auth or an IP allowlist; leaking internal endpoints is a real risk.
8. **Generate the client** — Don't hand-write a TypeScript client; generate it and commit the diff so changes are reviewable.
9. **Mock for parallel work** — `prism mock openapi.json` runs the frontend against a fake backend, no waiting.
10. **Treat the spec as a contract** — Review the OpenAPI diff in every PR, not just the code diff.

## Performance Considerations

- Spec generation happens at boot; it is fast (reflect-metadata over controllers/DTOs) but it is not free. ~10–100ms on a large app.
- The `/api-json` endpoint serves a cached static file in production; never generate per-request.
- Swagger UI is a 2MB JS bundle — host it once, not per route.
- Generated clients add zero runtime cost; you only ship the spec once.

## Summary

- OpenAPI is the contract; Swagger is the tooling; `@nestjs/swagger` is the NestJS integration.
- Always generate the spec from code (decorators on controllers + DTOs) — never hand-write it.
- Document every realistic error code; provide stable `operationId`; lock the docs path in production.
- Use the spec to drive client generation, mock servers, and contract tests — that is where the ROI compounds.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| OpenAPI | Vendor-neutral JSON/YAML contract for HTTP APIs |
| Swagger | Tooling around OpenAPI (UI, Editor, Codegen) |
| `@nestjs/swagger` | NestJS module that auto-generates the spec from decorators |
| `DocumentBuilder` | Fluent API to build the `info`, `servers`, `security`, `tags` sections |
| `SwaggerModule.createDocument(app, config)` | Builds the OpenAPI document from the running app |
| `SwaggerModule.setup('api', app, doc)` | Serves Swagger UI at `/api` and the spec at `/api-json` |
| `@ApiTags`, `@ApiOperation`, `@ApiResponse` | Controller/handler decoration for the spec |
| `@ApiProperty({ example, type })` | DTO field decoration for the spec |
| `operationIdFactory` | Produces stable IDs for client generation |
| `schemathesis run` | Fuzz-tests the running API against the spec in CI |
| `orval` / `openapi-generator` | Generates typed clients (TS, Java, etc.) from the spec |

---

## See Also
- [Microservices](../12-Microservices/) (per-service specs, developer portals)
- [NestJS](../06-NestJS/) (where `@nestjs/swagger` lives)
- [Security](../09-Security/) (security schemes in the spec)
- [System Design](../11-System-Design/) (public API contracts)

## References & Learn More

- [OpenAPI Specification](https://swagger.io/specification/)
- [NestJS Swagger Docs](https://docs.nestjs.com/openapi/introduction)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc)
- [Spectral — OpenAPI linter](https://stoplight.io/open-source/spectral)
- [schemathesis — API fuzzing from OpenAPI](https://schemathesis.readthedocs.io/)
- [orval — TypeScript client generator](https://orval.dev/)
- [OpenAPI Generator](https://openapi-generator.tech/)
