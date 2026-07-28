[![Category: Backend](https://img.shields.io/badge/category-Backend-2ea44f)](.)

# Controllers

## Definition

**Controllers** in NestJS are classes decorated with `@Controller()` that handle incoming HTTP requests and return responses. They act as the presentation layer of the application, receiving requests from clients, processing them (often by delegating to services), and returning appropriate responses.

Controllers are responsible for:

- Defining route endpoints using method-level decorators
- Parsing request parameters, body, query strings, and headers
- Validating incoming data
- Calling appropriate services for business logic
- Returning responses to clients

## Why Do We Need It?

1. **Separation of Concerns**: Controllers handle HTTP-specific logic, keeping business logic in services.

2. **Route Definition**: Clean, decorator-based route declaration.

3. **Request/Response Handling**: Built-in support for HTTP methods, status codes, headers, and streaming.

4. **Validation**: Integration with pipes for automatic request validation.

5. **Error Handling**: Consistent error handling through exception filters.

6. **Documentation**: Swagger/OpenAPI integration for API documentation.

7. **Testing**: Easy to test in isolation with mocked services.

## How It Works

When an HTTP request arrives at NestJS:

1. The framework matches the URL to a registered route

2. The appropriate controller method is invoked

3. Any middleware, guards, interceptors, and pipes run in order

4. The controller method processes the request

5. The response is returned to the client

### Request Lifecycle

```text
┌─────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  Client  │───▶│ Middleware │───▶│   Guard    │───▶│ Interceptor│
│ Request  │    │            │    │            │    │ (Before)   │
└─────────┘    └────────────┘    └────────────┘    └─────┬──────┘
                                                         │
                                                         ▼
┌─────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  Client  │◀──│ Interceptor│◀──│   Filter   │◀──│ Controller │
│ Response │    │ (After)    │    │ (if error) │    │  Method    │
└─────────┘    └────────────┘    └────────────┘    └────────────┘

```

### Route Resolution

```text
HTTP Request
    │
    ▼
┌──────────────────────┐
│  Global Middleware    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Route Matching     │
│  GET /users/:id      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Controller Method    │
│  @Get(':id')         │
│  findOne(@Param())   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Pipe Validation   │
│  ParseIntPipe        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Execute Method     │
│   Return Response    │
└──────────────────────┘

```

## Code Examples

### Basic Controller

```typescript
// user.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { UserService } from './user.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  findAll() {
    return this.userService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.userService.findOne(id);
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.userService.update(id, updateUserDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.userService.remove(id);
  }
}

```

### HTTP Method Decorators

```typescript
// resource.controller.ts
import {
  Controller, Get, Post, Put, Patch, Delete,
  Head, Options,
  Req, Res, Body, Param, Query, Headers,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Controller('resources')
export class ResourceController {
  @Get()
  findAll(@Query() query: any) {
    return { data: [], query };
  }

  @Post()
  @HttpCode(201)
  create(@Body() body: any) {
    return { id: 1, ...body };
  }

  @Put(':id')
  replace(@Param('id') id: string, @Body() body: any) {
    return { id, ...body };
  }

  @Patch(':id')
  partialUpdate(@Param('id') id: string, @Body() body: any) {
    return { id, ...body };
  }

  @Delete(':id')
  @HttpCode(204)
  remove(@Param('id') id: string) {
    return null;
  }

  @Head(':id')
  checkExists(@Param('id') id: string, @Res() res: Response) {
    res.header('X-Exists', 'true');
    res.end();
  }

  @Options()
  options(@Res() res: Response) {
    res.header('Allow', 'GET, POST, PUT, PATCH, DELETE');
    res.end();
  }
}

```

### Request Parameters and Body

```typescript
// advanced.controller.ts
import {
  Controller, Get, Post,
  Param, Body, Query, Headers,
  Req, Session,
} from '@nestjs/common';
import { Request } from 'express';
import { IsString, IsEmail, IsNumber, IsOptional } from 'class-validator';

class CreateUserDto {
  @IsString()
  name: string;

  @IsEmail()
  email: string;

  @IsNumber()
  @IsOptional()
  age?: number;
}

@Controller('advanced')
export class AdvancedController {
  // Route parameters
  @Get('users/:userId/posts/:postId')
  getPost(
    @Param('userId') userId: string,
    @Param('postId') postId: string,
  ) {
    return { userId, postId };
  }

  // Multiple parameters with object destructuring
  @Get('items/:id')
  getItem(@Param() params: { id: string }) {
    return { id: params.id };
  }

  // Query strings
  @Get('search')
  search(@Query('q') query: string, @Query('page') page: number) {
    return { query, page };
  }

  // Headers
  @Get('auth')
  getAuth(@Headers('authorization') auth: string) {
    return { token: auth };
  }

  // Full request object
  @Get('full-request')
  getFullRequest(@Req() req: Request) {
    return {
      url: req.url,
      method: req.method,
      headers: req.headers,
      ip: req.ip,
    };
  }

  // Session
  @Get('session')
  getSession(@Session() session: any) {
    session.views = (session.views || 0) + 1;
    return { views: session.views };
  }

  // Body with validation
  @Post('users')
  createUser(@Body() createUserDto: CreateUserDto) {
    return createUserDto;
  }
}

```

### Status Codes and Headers

```typescript
// status.controller.ts
import {
  Controller, Post, Get,
  HttpCode, HttpStatus, Header,
} from '@nestjs/common';

@Controller('status')
export class StatusController {
  @Post()
  @HttpCode(201)
  create() {
    return { created: true };
  }

  @Post('accepted')
  @HttpCode(HttpStatus.ACCEPTED)
  accepted() {
    return { accepted: true };
  }

  @Get('custom-headers')
  @Header('X-Custom-Header', 'custom-value')
  @Header('Cache-Control', 'none')
  withHeaders() {
    return { data: 'with custom headers' };
  }

  @Get('stream')
  stream(@Res() res: Response) {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const data = { message: 'Hello' };
    res.write(`data: ${JSON.stringify(data)}\n\n`);
    res.end();
  }
}

```

### DTOs with Validation

```typescript
// dto/create-user.dto.ts
import {
  IsString, IsEmail, IsNumber, IsOptional,
  MinLength, MaxLength, Min, Max,
  IsEnum, IsBoolean, ValidateNested,
  ArrayMinSize,
} from 'class-validator';
import { Type } from 'class-transformer';

enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
}

class AddressDto {
  @IsString()
  street: string;

  @IsString()
  city: string;

  @IsString()
  zipCode: string;
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

  @ValidateNested()
  @Type(() => AddressDto)
  address: AddressDto;

  @IsString({ each: true })
  @ArrayMinSize(1)
  interests: string[];
}

```

### Versioned Controllers

```typescript
// versioned.controller.ts
import { Controller, Get, Version } from '@nestjs/common';

@Controller('users')
export class VersionedController {
  @Version('1')
  @Get()
  findAllV1() {
    return { version: 1, users: [] };
  }

  @Version('2')
  @Get()
  findAllV2() {
    return { version: 2, users: [], metadata: {} };
  }
}

```

### Sub-Controllers and Resource Nesting

```typescript
// posts.controller.ts
import { Controller, Get, Post, Param, Body } from '@nestjs/common';

@Controller('users/:userId/posts')
export class PostsController {
  @Get()
  findAll(@Param('userId') userId: string) {
    return { userId, posts: [] };
  }

  @Get(':postId')
  findOne(
    @Param('userId') userId: string,
    @Param('postId') postId: string,
  ) {
    return { userId, postId };
  }

  @Post()
  create(
    @Param('userId') userId: string,
    @Body() body: any,
  ) {
    return { userId, ...body };
  }
}

```

### Controller Inheritance

```typescript
// base.controller.ts
import { Get, Param, NotFoundException } from '@nestjs/common';

export abstract class BaseEntityController<T> {
  protected abstract readonly serviceName: string;

  constructor(protected readonly service: any) {}

  @Get()
  findAll() {
    return this.service.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const entity = await this.service.findOne(id);
    if (!entity) {
      throw new NotFoundException(`${this.serviceName} with id ${id} not found`);
    }
    return entity;
  }
}

// user.controller.ts
@Controller('users')
export class UserController extends BaseEntityController<User> {
  protected readonly serviceName = 'User';

  constructor(private readonly userService: UserService) {
    super(userService);
  }
}

```

## Real-World Use Cases

### 1. RESTful API Controller

```typescript
@Controller('api/v1/products')
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
    @Query('category') category?: string,
  ) {
    return this.productService.findAll({ page, limit, category });
  }

  @Get(':id')
  async findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.productService.findOne(id);
  }

  @Post()
  @Roles('admin')
  async create(@Body() dto: CreateProductDto) {
    return this.productService.create(dto);
  }

  @Put(':id')
  @Roles('admin')
  async update(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: UpdateProductDto,
  ) {
    return this.productService.update(id, dto);
  }

  @Delete(':id')
  @Roles('admin')
  @HttpCode(204)
  async remove(@Param('id', ParseUUIDPipe) id: string) {
    await this.productService.remove(id);
  }
}

```

### 2. GraphQL Resolver (Alternative to REST)

```typescript
// @Resolver decorator instead of @Controller
@Resolver(() => User)
export class UserResolver {
  constructor(private userService: UserService) {}

  @Query(() => [User])
  async users() {
    return this.userService.findAll();
  }

  @Mutation(() => User)
  async createUser(@Args('input') input: CreateUserInput) {
    return this.userService.create(input);
  }
}

```

### 3. File Upload Controller

```typescript
@Controller('upload')
export class UploadController {
  @Post('single')
  @UseInterceptors(FileInterceptor('file'))
  uploadSingle(
    @UploadedFile(
      new ParseFilePipe({
        validators: [
          new FileTypeValidator({ fileType: 'image/(jpeg|png|gif)' }),
          new MaxFileSizeValidator({ maxSize: 1024 * 1024 * 5 }),
        ],
      }),
    )
    file: Express.Multer.File,
  ) {
    return { filename: file.originalname, size: file.size };
  }

  @Post('multiple')
  @UseInterceptors(FilesInterceptor('files', 10))
  uploadMultiple(
    @UploadedFiles() files: Express.Multer.File[],
  ) {
    return files.map(f => ({ filename: f.originalname, size: f.size }));
  }
}

```

### 4. Streaming Response Controller

```typescript
@Controller('stream')
export class StreamController {
  @Sse('events')
  sendEvents(): Observable<MessageEvent> {
    return interval(1000).pipe(
      map((count) => ({
        data: { count, timestamp: new Date().toISOString() },
      })),
    );
  }

  @Get('file')
  streamFile(@Res() res: Response) {
    const fileStream = createReadStream('large-file.zip');
    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', 'attachment; filename="file.zip"');
    fileStream.pipe(res);
  }
}

```

## Common Mistakes

### 1. Putting Business Logic in Controllers

```typescript
// ❌ BAD: Business logic in controller
@Controller('users')
export class UserController {
  @Post()
  async create(@Body() dto: CreateUserDto) {
    // Business logic shouldn't be here
    const hashedPassword = await bcrypt.hash(dto.password, 10);
    const user = await this.userRepository.create({
      ...dto,
      password: hashedPassword,
    });
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}

// ✅ GOOD: Delegate to service
@Controller('users')
export class UserController {
  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }
}

```

### 2. Not Validating Input

```typescript
// ❌ BAD: No validation
@Post()
create(@Body() body: any) {
  return this.userService.create(body);
}

// ✅ GOOD: Use DTOs with validation
@Post()
create(@Body() createUserDto: CreateUserDto) {
  return this.userService.create(createUserDto);
}

```

### 3. Using @Res() Without @Body()

```typescript
// ❌ BAD: Using @Res() breaks NestJS response handling
@Get()
findAll(@Res() res: Response) {
  res.json({ data: [] }); // NestJS can't intercept this
}

// ✅ GOOD: Use @Res({ passthrough: true }) if you need Response object
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.header('X-Custom', 'value');
  return { data: [] }; // NestJS can still intercept
}

// OR: Don't use @Res at all
@Get()
findAll() {
  return { data: [] }; // NestJS handles serialization
}

```

### 4. Not Using Proper Status Codes

```typescript
// ❌ BAD: Always returning 200
@Post()
create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto); // Returns 200
}

// ✅ GOOD: Use proper status codes
@Post()
@HttpCode(201)
create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto); // Returns 201
}

```

### 5. Over-Fetching Data

```typescript
// ❌ BAD: Returning entire entity with sensitive data
@Get(':id')
async findOne(@Param('id') id: string) {
  return this.userService.findOne(id); // Returns password hash, etc.
}

// ✅ GOOD: Use serialization groups or DTOs
@Get(':id')
async findOne(@Param('id') id: string) {
  const user = await this.userService.findOne(id);
  return plainToInstance(UserResponseDto, user);
}

```

## Best Practices

1. **Thin Controllers**: Keep controllers thin — delegate business logic to services.

2. **Use DTOs**: Always validate incoming data with DTOs and class-validator.

3. **Proper HTTP Methods**: Use the correct HTTP methods (GET, POST, PUT, PATCH, DELETE).

4. **Status Codes**: Return appropriate HTTP status codes.

5. **Error Handling**: Let exception filters handle errors, don't try-catch everything.

6. **Documentation**: Use Swagger decorators for API documentation.

7. **Input Sanitization**: Sanitize all user input to prevent injection attacks.

8. **Response Transformation**: Use class-transformer to shape responses.

9. **Rate Limiting**: Implement rate limiting on sensitive endpoints.
10. **Versioning**: Use API versioning for breaking changes.

## Performance Considerations

1. **Response Caching**: Use `@CacheTTL()` and `@CacheKey()` for caching responses.

2. **Pagination**: Always implement pagination for list endpoints.

3. **Compression**: Enable response compression for large payloads.

4. **Async Operations**: Use async/await for I/O operations to avoid blocking.

5. **Response Streaming**: Stream large files instead of loading them entirely in memory.

6. **Connection Pooling**: Use connection pooling for database operations.

## Summary

Controllers are NestJS's HTTP handling layer that define routes, validate input, and delegate business logic to services. They provide decorator-based route definition, built-in validation support, and seamless integration with guards, interceptors, and pipes. Proper controller design follows thin controller principles, uses DTOs for validation, and returns appropriate HTTP responses.

## Cheat Sheet
| Decorator | Purpose |
|-----------|---------|
| `@Controller('path')` | Define a controller with base route |
| `@Get()`, `@Post()`, `@Put()`, `@Patch()`, `@Delete()` | HTTP method decorators |
| `@Param()` | Access route parameters |
| `@Body()` | Access request body |
| `@Query()` | Access query string parameters |
| `@Headers()` | Access request headers |
| `@Req()`, `@Res()` | Access raw Request/Response objects |
| `@HttpCode()` | Set HTTP status code |
| `@Header()` | Set response header |
| `@Redirect()` | Redirect to URL |
| `@UseInterceptors()` | Apply interceptors |
| `@UseGuards()` | Apply guards |
| `@UsePipes()` | Apply pipes |
| `@Version()` | API versioning |
| `@SetMetadata()` | Set custom metadata |

---

## See Also
- [Design Patterns](../10-Design-Patterns/)
- [Microservices](../12-Microservices/)
- [Node.js](../05-NodeJS/)
- [REST APIs](../07-REST-API/)

## References & Learn More

- [NestJS Controllers Official Docs](https://docs.nestjs.com/controllers)
- [NestJS Pipes](https://docs.nestjs.com/pipes)
- [NestJS Guards](https://docs.nestjs.com/guards)
- [NestJS Intercept](https://docs.nestjs.com/interceptors)
