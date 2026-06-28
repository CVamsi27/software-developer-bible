# Pipes

## Definition

**Pipes** in NestJS are classes that implement the `PipeTransform` interface. They are used to transform input data and validate it before it reaches the route handler. Pipes can transform data (e.g., string to number) or validate data against constraints (e.g., email format, required fields).

Pipes execute after guards and before the route handler, operating on individual parameters, the request body, or the entire request.

## Why Do We Need It?

1. **Input Validation**: Ensure incoming data meets expected format and constraints.
2. **Data Transformation**: Convert data types (string to number, plain object to class instance).
3. **Sanitization**: Clean and sanitize user input.
4. **Error Handling**: Return meaningful validation errors to clients.
5. **Separation of Concerns**: Keep validation logic out of controllers and services.
6. **Reusability**: Apply the same validation logic across multiple endpoints.
7. **DTO Integration**: Work seamlessly with class-validator and DTOs.

## How It Works

Pipes have two responsibilities:
1. **Validation**: Check if input data is valid
2. **Transformation**: Transform the data to the desired type

### Pipe Execution Flow

```text
┌──────────────────────────────────────────────────────────┐
│                  Pipe Execution Flow                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Request Parameter / Body                                │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────────────────┐│
│  │              Pipe Transform                          ││
│  │                                                      ││
│  │  1. Receive raw input data                           ││
│  │  2. Validate against constraints                     ││
│  │  3. Transform to desired type                        ││
│  │  4. Return transformed data or throw exception       ││
│  │                                                      ││
│  └──────────────────────────────────────────────────────┘│
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────┐                                        │
│  │  Controller  │  Receives validated/transformed data   │
│  │   Handler    │                                        │
│  └──────────────┘                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Built-in Pipes

```text
┌─────────────────────────────────────────────────────────┐
│                  Built-in Pipes                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ValidationPipe          ParseIntPipe                    │
│  ┌─────────────┐        ┌─────────────┐                 │
│  │ class-val   │        │ string →    │                 │
│  │ DTO validat │        │ number      │                 │
│  └─────────────┘        └─────────────┘                 │
│                                                         │
│  ParseBoolPipe           ParseArrayPipe                  │
│  ┌─────────────┐        ┌─────────────┐                 │
│  │ string →    │        │ string →    │                 │
│  │ boolean     │        │ array       │                 │
│  └─────────────┘        └─────────────┘                 │
│                                                         │
│  ParseUUIDPipe           ParseEnumPipe                   │
│  ┌─────────────┐        ┌─────────────┐                 │
│  │ validate    │        │ validate    │                 │
│  │ UUID format │        │ enum value  │                 │
│  └─────────────┘        └─────────────┘                 │
│                                                         │
│  DefaultValuePipe        ParseFloatPipe                  │
│  ┌─────────────┐        ┌─────────────┐                 │
│  │ set default │        │ string →    │                 │
│  │ value       │        │ float       │                 │
│  └─────────────┘        └─────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic ValidationPipe

```typescript
// create-user.dto.ts
import {
  IsString,
  IsEmail,
  IsNumber,
  IsOptional,
  MinLength,
  MaxLength,
  Min,
  Max,
  IsEnum,
  IsBoolean,
  ValidateNested,
  IsArray,
  ArrayMinSize,
} from 'class-validator';
import { Type } from 'class-transformer';

enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
}

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  @MaxLength(50)
  name: string;

  @IsEmail()
  email: string;

  @IsNumber()
  @Min(0)
  @Max(150)
  age: number;

  @IsEnum(UserRole)
  role: UserRole;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean;

  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  interests: string[];
}
```

### Global ValidationPipe

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,           // Strip non-whitelisted properties
      forbidNonWhitelisted: true, // Throw error for non-whitelisted properties
      transform: true,           // Auto-transform payloads to DTO instances
      transformOptions: {
        enableImplicitConversion: true, // Auto-convert types
      },
    }),
  );

  await app.listen(3000);
}
bootstrap();
```

### ParseIntPipe

```typescript
// user.controller.ts
import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';

@Controller('users')
export class UserController {
  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    // id is guaranteed to be a number
    return this.userService.findOne(id);
  }

  @Get()
  findAll(
    @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
    @Query('limit', new DefaultValuePipe(10), ParseIntPipe) limit: number,
  ) {
    return this.userService.findAll(page, limit);
  }
}
```

### Custom Pipe

```typescript
// parse-objectid.pipe.ts
import {
  PipeTransform,
  Injectable,
  BadRequestException,
} from '@nestjs/common';

@Injectable()
export class ParseObjectIdPipe implements PipeTransform<string> {
  transform(value: string): string {
    if (!isValidObjectId(value)) {
      throw new BadRequestException(`${value} is not a valid ObjectId`);
    }
    return value;
  }
}

// Usage
@Get(':id')
findOne(@Param('id', ParseObjectIdPipe) id: string) {
  return this.userService.findOne(id);
}
```

### Transformation Pipe

```typescript
// trim.pipe.ts
import { PipeTransform, Injectable } from '@nestjs/common';

@Injectable()
export class TrimPipe implements PipeTransform {
  transform(value: any): any {
    if (typeof value === 'string') {
      return value.trim();
    }
    if (typeof value === 'object' && value !== null) {
      return Object.keys(value).reduce((acc, key) => {
        acc[key] = typeof value[key] === 'string' ? value[key].trim() : value[key];
        return acc;
      }, {});
    }
    return value;
  }
}
```

### Validation with Class-Validator

```typescript
// create-order.dto.ts
import {
  IsString,
  IsNumber,
  IsArray,
  ValidateNested,
  IsOptional,
  Min,
  ArrayMinSize,
  IsEnum,
  IsDateString,
} from 'class-validator';
import { Type } from 'class-transformer';

enum OrderStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  SHIPPED = 'shipped',
}

class OrderItemDto {
  @IsString()
  productId: string;

  @IsNumber()
  @Min(1)
  quantity: number;

  @IsNumber()
  @Min(0)
  price: number;
}

export class CreateOrderDto {
  @IsString()
  customerId: string;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  @ArrayMinSize(1)
  items: OrderItemDto[];

  @IsOptional()
  @IsString()
  notes?: string;

  @IsOptional()
  @IsDateString()
  deliveryDate?: string;
}
```

### Custom Validation Pipe

```typescript
// unique-email.pipe.ts
import {
  PipeTransform,
  Injectable,
  ConflictException,
} from '@nestjs/common';
import { UserService } from '../user.service';

@Injectable()
export class UniqueEmailPipe implements PipeTransform<string> {
  constructor(private readonly userService: UserService) {}

  async transform(email: string): Promise<string> {
    const existingUser = await this.userService.findByEmail(email);
    if (existingUser) {
      throw new ConflictException('Email already exists');
    }
    return email;
  }
}

// Usage
@Post()
create(
  @Body('email', UniqueEmailPipe) email: string,
  @Body('name') name: string,
) {
  return this.userService.create({ email, name });
}
```

### Schema Validation Pipe (Joi)

```typescript
// joi-validation.pipe.ts
import {
  PipeTransform,
  Injectable,
  BadRequestException,
} from '@nestjs/common';
import * as Joi from 'joi';

@Injectable()
export class JoiValidationPipe implements PipeTransform {
  constructor(private schema: Joi.ObjectSchema) {}

  transform(value: any): any {
    const { error, value: validatedValue } = this.schema.validate(value, {
      abortEarly: false,
    });

    if (error) {
      const messages = error.details.map((d) => d.message).join(', ');
      throw new BadRequestException(messages);
    }

    return validatedValue;
  }
}

// Usage with schema
const createUserSchema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  age: Joi.number().min(0).max(150).required(),
});

@Post()
@UsePipes(new JoiValidationPipe(createUserSchema))
create(@Body() body: any) {
  return this.userService.create(body);
}
```

### Zod Validation Pipe

```typescript
// zod-validation.pipe.ts
import {
  PipeTransform,
  Injectable,
  BadRequestException,
} from '@nestjs/common';
import { ZodSchema, ZodError } from 'zod';

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any): any {
    try {
      return this.schema.parse(value);
    } catch (error) {
      if (error instanceof ZodError) {
        const messages = error.errors.map((e) => e.message).join(', ');
        throw new BadRequestException(messages);
      }
      throw error;
    }
  }
}

// Usage
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(0).max(150),
});

@Post()
@UsePipes(new ZodValidationPipe(createUserSchema))
create(@Body() body: any) {
  return this.userService.create(body);
}
```

### Nested Validation

```typescript
// address.dto.ts
import { IsString, IsOptional } from 'class-validator';

export class AddressDto {
  @IsString()
  street: string;

  @IsString()
  city: string;

  @IsString()
  state: string;

  @IsString()
  zipCode: string;
}

// user.dto.ts
import { ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { AddressDto } from './address.dto';

export class CreateUserDto {
  @IsString()
  name: string;

  @ValidateNested()
  @Type(() => AddressDto)
  address: AddressDto;
}
```

## Real-World Use Cases

### 1. File Upload Validation

```typescript
// validate-file.pipe.ts
import {
  PipeTransform,
  Injectable,
  BadRequestException,
} from '@nestjs/common';

@Injectable()
export class ValidateFilePipe implements PipeTransform {
  private readonly allowedMimeTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf',
  ];

  private readonly maxSize = 5 * 1024 * 1024; // 5MB

  transform(file: Express.Multer.File): Express.Multer.File {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    if (!this.allowedMimeTypes.includes(file.mimetype)) {
      throw new BadRequestException('Invalid file type');
    }

    if (file.size > this.maxSize) {
      throw new BadRequestException('File too large');
    }

    return file;
  }
}
```

### 2. Pagination Pipe

```typescript
// pagination.pipe.ts
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

export interface PaginationQuery {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'ASC' | 'DESC';
}

@Injectable()
export class PaginationPipe implements PipeTransform {
  transform(value: any): PaginationQuery {
    const page = Math.max(1, parseInt(value.page) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(value.limit) || 10));
    const sortOrder = (value.sortOrder?.toUpperCase() || 'ASC') as 'ASC' | 'DESC';

    return { page, limit, sortBy: value.sortBy, sortOrder };
  }
}
```

### 3. MongoId Pipe

```typescript
// parse-mongo-id.pipe.ts
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';
import { Types } from 'mongoose';

@Injectable()
export class ParseMongoIdPipe implements PipeTransform {
  transform(value: string): string {
    if (!Types.ObjectId.isValid(value)) {
      throw new BadRequestException(`${value} is not a valid MongoId`);
    }
    return value;
  }
}
```

## Common Mistakes

### 1. Not Using Whitelist

```typescript
// ❌ BAD: Allows extra properties
app.useGlobalPipes(new ValidationPipe());

// ✅ GOOD: Strip non-whitelisted properties
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
}));
```

### 2. Not Transforming Input

```typescript
// ❌ BAD: Params stay as strings
@Get(':id')
findOne(@Param('id') id: string) {
  return this.userService.findOne(id); // id is string
}

// ✅ GOOD: Use ParseIntPipe or transform option
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {
  return this.userService.findOne(id); // id is number
}
```

### 3. Validation Pipe Without DTO

```typescript
// ❌ BAD: No validation
@Post()
create(@Body() body: any) {
  return this.userService.create(body);
}

// ✅ GOOD: Use DTO with validation
@Post()
create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto);
}
```

### 4. Custom Pipe Without Injectable

```typescript
// ❌ BAD: Missing @Injectable
export class TrimPipe implements PipeTransform {
  transform(value: any) {
    return value.trim();
  }
}

// ✅ GOOD: Always use @Injectable
@Injectable()
export class TrimPipe implements PipeTransform {
  transform(value: any) {
    return value.trim();
  }
}
```

## Best Practices

1. **Global ValidationPipe**: Use `ValidationPipe` globally with whitelist and transform.
2. **DTOs**: Always use DTOs with class-validator for request validation.
3. **Custom Pipes**: Create custom pipes for reusable validation logic.
4. **Error Messages**: Provide meaningful error messages in validation.
5. **Type Safety**: Use `ParseIntPipe`, `ParseBoolPipe`, etc. for type safety.
6. **Nested Validation**: Use `@ValidateNested()` for nested objects.
7. **Async Validation**: Use async pipes for database lookups.
8. **Testing**: Test pipes in isolation.

## Performance Considerations

1. **Validation Overhead**: Validation adds processing time — validate only what's necessary.
2. **Async Pipes**: Async pipes add latency — use caching when possible.
3. **Pipe Caching**: Pipes are instantiated once — keep them lightweight.
4. **Early Exit**: Return early in pipes for invalid data.
5. **Batch Validation**: Validate arrays efficiently with `{ each: true }`.

## Interview Questions

### Beginner

**Q1: What is a pipe in NestJS?**
A pipe is a class implementing `PipeTransform` that validates and transforms input data before it reaches the route handler.

**Q2: What is the difference between `ParseIntPipe` and `ValidationPipe`?**
- `ParseIntPipe`: Converts string to number
- `ValidationPipe`: Validates data against DTO constraints

**Q3: How do you apply a pipe globally?**
Use `app.useGlobalPipes()` in main.ts or register via module.

**Q4: What is `whitelist` in ValidationPipe?**
Strips properties not defined in the DTO.

**Q5: Can pipes be async?**
Yes, pipes can return Promises.

### Intermediate

**Q6: How do you create a custom validation pipe?**
Implement `PipeTransform` interface with `transform()` method, add `@Injectable()`, and throw `BadRequestException` for invalid data.

**Q7: What is the difference between `transform: true` and `ParseIntPipe`?**
- `transform: true`: Automatically transforms payloads to DTO instances
- `ParseIntPipe`: Explicitly converts string parameters to numbers

**Q8: How do you handle nested object validation?**
Use `@ValidateNested()` with `@Type(() => NestedDto)`.

**Q9: What is `forbidNonWhitelisted`?**
When true, throws an error if non-whitelisted properties are present (instead of silently stripping them).

**Q10: How do you validate query parameters?**
Use `@Query()` with DTO and ValidationPipe.

### Senior

**Q11: How would you implement a pipe that validates against a database?**
Create an async pipe that queries the database (e.g., check if email exists) and throws exceptions for invalid data.

**Q12: How do you handle internationalized error messages?**
Inject a localization service and use locale-specific error messages based on request headers.

**Q13: Design a comprehensive validation strategy.**
Layer validation: DTO validation (format), business rule validation (service layer), database validation (constraints).

**Q14: How do you handle file validation in pipes?**
Use `ParseFilePipe` with validators like `FileTypeValidator` and `MaxFileSizeValidator`.

**Q15: How would you implement conditional validation?**
Use class-validator's `@ValidateIf()` or create custom decorators with metadata.

### FAANG-Style

**Q16: Design a validation system for a GraphQL API.**
Implement pipes for GraphQL argument validation using `GqlExecutionContext`. Use class-validator with GraphQL decorators.

**Q17: How would you implement schema versioning in validation?**
Use different DTOs per API version, or add version-aware validation logic to pipes.

**Q18: Design a real-time validation system for streaming data.**
Implement pipes that validate chunks of streaming data, buffering and validating incrementally.

**Q19: How would you handle validation in distributed systems?**
Implement validation at the API gateway, propagate validation context, and use schema registry for message validation.

**Q20: Design a self-documenting validation system.**
Generate OpenAPI/Swagger documentation from validation pipes. Use class-validator metadata to generate schemas.

### Follow-ups

**Q21: How do you test custom pipes?**
Create a testing module, instantiate the pipe, and test transform with valid/invalid inputs.

**Q22: What happens when a pipe throws an exception?**
NestJS catches it and sends an appropriate error response (400 Bad Request by default).

**Q23: Can pipes access the request object?**
Yes, use `@Req()` decorator in the controller and pass to pipe, or use `ExecutionContext`.

**Q24: How do you chain multiple pipes?**
Apply multiple pipes with `@UsePipes()` or parameter-level pipes: `@Param('id', ParseIntPipe, AdditionalValidation)`.

**Q25: What is the order of pipe execution?**
Pipes execute in the order they're defined (parameter-level first, then method-level, then controller-level).

## Summary

Pipes are NestJS's data transformation and validation mechanism. They ensure incoming data is valid and properly typed before reaching route handlers. Built-in pipes handle common cases, while custom pipes implement specific validation logic. Integration with class-validator and class-transformer provides powerful DTO-based validation.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `PipeTransform` | Interface pipes implement |
| `transform()` | Method that validates/transforms data |
| `ValidationPipe` | Built-in validation with class-validator |
| `ParseIntPipe` | Converts string to number |
| `ParseBoolPipe` | Converts string to boolean |
| `ParseArrayPipe` | Converts string to array |
| `ParseUUIDPipe` | Validates UUID format |
| `ParseEnumPipe` | Validates enum value |
| `DefaultValuePipe` | Sets default value |
| `whitelist: true` | Strip non-DTO properties |
| `forbidNonWhitelisted` | Error for extra properties |
| `transform: true` | Auto-transform to DTO instances |
| `@ValidateNested()` | Validate nested objects |
| `@Type(() => Class)` | Transform nested objects |
| `BadRequestException` | Throw for validation errors |

## References & Learn More

- [NestJS Pipes Official Docs](https://docs.nestjs.com/pipes)
- [NestJS Validation](https://docs.nestjs.com/techniques/validation)
- [class-validator GitHub](https://github.com/typestack/class-validator)
- [class-transformer GitHub](https://github.com/typestack/class-transformer)
