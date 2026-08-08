---
section: NestJS
category: Backend
tags: [concept]
---

# Configuration & Validation in NestJS

> **TL;DR:** `ConfigModule` reads env vars (or files) into a typed, injectable `ConfigService`; `class-validator` + `ValidationPipe` validates DTOs at the request boundary. The senior test is the full config lifecycle: schema validation at boot (`Joi` / `class-validator`), namespacing by feature, env-specific files, and keeping secrets out of code.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**Configuration** in NestJS is the `ConfigModule` from `@nestjs/config` — a wrapper around `dotenv` that loads env vars (or YAML/JSON files) and exposes them as a `ConfigService` for injection. **Validation** in NestJS is the `ValidationPipe` from `@nestjs/common` plus `class-validator` decorators on DTOs — when applied globally (`useGlobalPipes`) it intercepts every request body/query/param and rejects invalid input with a 400 before it ever reaches a controller method.

## Why Do We Need It?

1. **Boot-time fail-fast** — Validate env vars at boot, not at first request, so a missing `DATABASE_URL` crashes the deploy, not the user.
2. **Type safety** — DTOs with `class-validator` give you runtime validation and TS types from one source of truth.
3. **Centralization** — One place to read config, one place to override it in tests, one place to namespace by feature.
4. **Security** — Strip unknown properties (`whitelist: true`) and forbid prototype pollution (`forbidNonWhitelisted: true`).
5. **Env-specific overrides** — `.env.development`, `.env.production`, `.env.test`; no manual swapping in CI.
6. **Avoid `process.env` sprawl** — Greppable `configService.get(...)` is better than 200 `process.env.X` reads.
7. **Transformation** — `class-transformer` turns plain JSON into a typed DTO instance so handlers receive a class, not a bag of properties.

## How It Works

### Config Flow

```text
.env file  ──▶  ConfigModule.forRoot({...})
                  │
                  ├── validationSchema (Joi / class-validator)
                  │     └─ fails boot if env is invalid
                  │
                  ├── load: [fileLoader, fileLoader({ env: NODE_ENV })]
                  │
                  └── ConfigService (injectable)
                        │
                        ▼
                  configService.get<string>('DB.host')
                  configService.getOrThrow('JWT_SECRET')   // throws if missing
```

### Validation Flow

```text
HTTP Request Body (plain JSON)
   │
   ▼
ValidationPipe (global)
   │
   ├── class-transformer: plainToInstance(CreateUserDto, body, { excludeExtraneousValues: true })
   │
   ├── class-validator: validate(instance) → errors[]
   │
   ├── if errors.length > 0 → throw BadRequestException(errors)
   │
   └── otherwise → instance passed to handler
```

## Code Examples

### ConfigModule with Joi Schema Validation at Boot

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import * as Joi from 'joi';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,                  // available everywhere without re-import
      cache: true,                     // read once, not per call
      envFilePath: [
        `.env.${process.env.NODE_ENV}.local`,
        `.env.${process.env.NODE_ENV}`,
        '.env.local',
        '.env',
      ],
      validationSchema: Joi.object({
        NODE_ENV: Joi.string().valid('development', 'test', 'production').default('development'),
        PORT: Joi.number().default(3000),
        DATABASE_URL: Joi.string().uri().required(),
        JWT_SECRET: Joi.string().min(32).required(),
        REDIS_URL: Joi.string().uri().optional(),
        LOG_LEVEL: Joi.string().valid('debug', 'info', 'warn', 'error').default('info'),
      }),
      validationOptions: { abortEarly: true },
    }),
    // feature modules...
  ],
})
export class AppModule {}
```

### Namespaced Config for One Feature

```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  url: process.env.DATABASE_URL,
  poolSize: parseInt(process.env.DB_POOL_SIZE ?? '10', 10),
  ssl: process.env.NODE_ENV === 'production',
}));

// app.module.ts
ConfigModule.forRoot({
  isGlobal: true,
  load: [databaseConfig],     // merged under 'database' namespace
});

// usage in a service
@Injectable()
export class UsersService {
  constructor(private readonly config: ConfigService) {}

  getPoolSize() {
    return this.config.get<number>('database.poolSize');   // 10
  }
}
```

### Typed Config Service Wrapper

```typescript
// config/typed-config.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class TypedConfigService {
  constructor(private readonly cs: ConfigService) {}

  get databaseUrl(): string {
    return this.cs.getOrThrow<string>('DATABASE_URL');
  }
  get jwtSecret(): string {
    return this.cs.getOrThrow<string>('JWT_SECRET');
  }
  get isProd(): boolean {
    return this.cs.get<string>('NODE_ENV') === 'production';
  }
}

// module
@Module({
  providers: [
    { provide: TypedConfigService, useFactory: (cs) => new TypedConfigService(cs), inject: [ConfigService] },
  ],
  exports: [TypedConfigService],
})
export class ConfigTypedModule {}
```

### Global ValidationPipe + DTO

```typescript
// main.ts
import { ValidationPipe } from '@nestjs/common';
import { useContainer } from 'class-validator';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,                    // strip unknown properties
      forbidNonWhitelisted: true,         // 400 if unknown property sent
      transform: true,                    // plainToInstance before validation
      transformOptions: { enableImplicitConversion: true },
    }),
  );
  await app.listen(process.env.PORT ?? 3000);
}

// users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional, IsEnum } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(2)
  name!: string;

  @IsOptional()
  @IsEnum(['admin', 'member'] as const)
  role?: 'admin' | 'member';
}

// users.controller.ts
@Post()
create(@Body() dto: CreateUserDto) {   // already validated + transformed
  return this.usersService.create(dto);
}
```

### Custom Validator Constraint

```typescript
// validators/is-strong-password.validator.ts
import { registerDecorator, ValidationOptions } from 'class-validator';

export function IsStrongPassword(opts?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      name: 'isStrongPassword',
      target: object.constructor,
      propertyName,
      options: opts,
      validator: {
        validate(value: any) {
          return (
            typeof value === 'string' &&
            value.length >= 12 &&
            /[A-Z]/.test(value) &&
            /[a-z]/.test(value) &&
            /[0-9]/.test(value)
          );
        },
      },
    });
  };
}
```

## Real-World Use Cases

1. **12-factor config** — All config from env, validated at boot, no `if (env === 'prod')` branches scattered through code.
2. **Multi-tenant** — One env file per tenant, mounted as a secret in K8s; `ConfigService` reads the active tenant from a header.
3. **Feature flags** — A `featureFlag` namespace in config; `ConfigService.get('featureFlags.newCheckout')` returns a boolean.
4. **Request validation** — `ValidationPipe` rejects malformed bodies before they reach the service, so services can trust their inputs.
5. **Migration safety** — `Joi` schema with `abortEarly: true` and required fields means a missing `STRIPE_SECRET` cannot ship.
6. **Test override** — `ConfigModule.forRoot({ ignoreEnvFile: true, load: [() => testConfig] })` gives tests full control.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `process.env.X` in 200 places | Inject `ConfigService` or a typed wrapper |
| Validating env vars only at first read | Use `validationSchema` so boot fails fast |
| Skipping `whitelist: true` | Always set `whitelist: true` and `forbidNonWhitelisted: true` |
| Plain DTOs without `class-validator` | Every `@Body()` DTO must have decorators |
| Hardcoding `PORT` or URLs | Always read from `ConfigService` |
| Putting secrets in `.env` checked into git | Use `.env.example` for shape; real secrets from a secret manager |
| `transform: false` on `ValidationPipe` | DTO fields stay `string`; set `transform: true` and decorate with `@Type(() => Number)` |
| Loading `.env` in production | `ignoreEnvFile: process.env.NODE_ENV === 'production'` |

## Best Practices

1. **Validate at boot** — `Joi` or `class-validator` schema; missing required env crashes the deploy, not the first request.
2. **Namespace by feature** — `registerAs('feature', ...)` keeps config organized and makes per-feature overrides trivial.
3. **Global ValidationPipe** — Set `whitelist`, `forbidNonWhitelisted`, `transform`, `enableImplicitConversion` once in `main.ts`.
4. **Type your config** — A `TypedConfigService` with `getOrThrow` for required keys makes missing config a 500 at first call, not a silent `undefined`.
5. **Cache the config** — `ConfigModule.forRoot({ cache: true })` reads once; without it, every `configService.get()` re-parses.
6. **Env files per environment** — `.env.development`, `.env.test`, `.env.production`; in prod, use real secret stores and `ignoreEnvFile: true`.
7. **DTOs at the boundary only** — Don't validate inside services; trust that `ValidationPipe` already did.
8. **Custom validators for domain rules** — `IsStrongPassword`, `IsTenantMember`, etc. — declarative and reusable.
9. **Use `class-transformer` `@Type(() => Date)`** — `transform: true` alone doesn't convert nested fields; explicit `@Type` is required.
10. **Log validated config at boot (without secrets)** — Print the resolved env (DB host, port, feature flags) once at startup so you can verify what shipped.

## Performance Considerations

- `ConfigService` is fast (in-memory after `cache: true`); it's never a hotspot.
- `ValidationPipe` adds ~0.1–0.5ms per request — negligible. Most cost is in `class-transformer` reflection.
- DTO classes are compiled at boot, not per request.
- `cache: true` is on by default in v3+ but be explicit for older versions.
- For very large bodies, `class-transformer` can be slow; consider `transform: false` for read-only DTOs.

## Summary

- `ConfigModule` loads env vars (or files), validates them at boot, and exposes them as `ConfigService` for injection.
- `ValidationPipe` + `class-validator` + `class-transformer` validates and transforms DTOs at the request boundary.
- Namespace by feature, type your config (`getOrThrow`), set `whitelist + forbidNonWhitelisted + transform` on the global pipe.
- Validate env at boot so missing config crashes the deploy, not the first request.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `ConfigModule.forRoot({ isGlobal: true })` | Module-wide access to `ConfigService` |
| `validationSchema: Joi.object({...})` | Validates env at boot; aborts deploy if invalid |
| `registerAs('feature', () => ({...}))` | Namespace config by feature |
| `configService.getOrThrow('X')` | Returns the value or throws if missing |
| `cache: true` | Read env once at boot, not per call |
| `useGlobalPipes(new ValidationPipe({ whitelist, forbidNonWhitelisted, transform }))` | Validate every `@Body()` / `@Query()` DTO |
| `@IsEmail()`, `@IsString()`, `@MinLength()` | `class-validator` decorators |
| `@Type(() => Date)` | Tell `class-transformer` how to convert nested fields |
| Custom `@IsStrongPassword()` | Domain-specific reusable validator |
| `ignoreEnvFile: NODE_ENV === 'production'` | Don't load `.env` in prod; use real secret store |

---

## See Also
- [Design Patterns](../10-Design-Patterns/) (DI for ConfigService)
- [Microservices](../12-Microservices/) (config across services)
- [Node.js](../05-NodeJS/) (env, dotenv, process management)
- [REST APIs](../07-REST-API/) (validating API request bodies)

## References & Learn More

- [NestJS Configuration Docs](https://docs.nestjs.com/techniques/configuration)
- [NestJS Validation Docs](https://docs.nestjs.com/techniques/validation)
- [class-validator](https://github.com/typestack/class-validator)
- [class-transformer](https://github.com/typestack/class-transformer)
- [Joi](https://joi.dev/)
- [12-Factor App: Config](https://12factor.net/config)
