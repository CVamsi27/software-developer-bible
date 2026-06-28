# NestJS Interview Questions

## 40 Most Asked NestJS Interview Questions with Detailed Answers

---

## Beginner Level (Questions 1-10)

### Q1: What is NestJS and why would you use it?

**Answer:** NestJS is a progressive Node.js framework for building efficient, scalable server-side applications. It uses TypeScript and combines OOP (Object-Oriented Programming), FP (Functional Programming), and FRP (Functional Reactive Programming).

**Why use it:**
- Built-in dependency injection
- Modular architecture
- TypeScript-first
- Excellent testing support
- Microservices ready
- Wide ecosystem (TypeORM, GraphQL, WebSockets)
- Strong community and documentation

### Q2: What are the main components of a NestJS application?

**Answer:**
- **Modules**: Organize code into related capabilities
- **Controllers**: Handle HTTP requests and define routes
- **Providers/Services**: Business logic and data access
- **Middleware**: Execute logic before route handlers
- **Guards**: Authorization and access control
- **Interceptors**: Cross-cutting concerns (logging, caching)
- **Pipes**: Data validation and transformation
- **Exception Filters**: Error handling

### Q3: What is the difference between NestJS and Express?

**Answer:**
| Feature | NestJS | Express |
|---------|--------|---------|
| Architecture | Opinionated, modular | Unopinionated, minimal |
| TypeScript | First-class support | Optional |
| DI | Built-in | Manual |
| Testing | Integrated | Manual setup |
| Structure | Enforced patterns | Flexible |
| Microservices | Built-in support | Requires additional libraries |

NestJS uses Express (or Fastify) under the hood but adds structure and features.

### Q4: What is a module in NestJS?

**Answer:** A module is a class decorated with `@Module()` that organizes closely related set of capabilities. Every NestJS app has at least one module (root module).

Properties:
- `providers`: Services available within the module
- `controllers`: Request handlers
- `imports`: Other modules whose exports are needed
- `exports`: Providers available to importing modules

### Q5: What is dependency injection in NestJS?

**Answer:** DI is a design pattern where NestJS's IoC container manages and injects dependencies into components through constructor parameters.

```typescript
@Injectable()
export class UserService {
  constructor(
    private readonly userRepo: UserRepository, // Injected
    private readonly cacheService: CacheService, // Injected
  ) {}
}
```

Benefits: Loose coupling, testability, reusability.

### Q6: What is the difference between `@Injectable()` and `@Inject()`?

**Answer:**
- `@Injectable()`: Marks a class as a provider that can be managed by DI container
- `@Inject()`: Used to inject dependencies using custom tokens when type alone isn't sufficient

```typescript
@Injectable() // Class is injectable
export class UserService {}

constructor(
  @Inject('CUSTOM_TOKEN') // Custom token injection
  private custom: any,
) {}
```

### Q7: What are the different HTTP method decorators in NestJS?

**Answer:**
- `@Get()` - GET requests
- `@Post()` - POST requests
- `@Put()` - PUT requests (full update)
- `@Patch()` - PATCH requests (partial update)
- `@Delete()` - DELETE requests
- `@Options()` - OPTIONS requests
- `@Head()` - HEAD requests
- `@All()` - All HTTP methods

### Q8: How do you validate request data in NestJS?

**Answer:** Use DTOs with class-validator and the global ValidationPipe:

```typescript
// DTO
class CreateUserDto {
  @IsString()
  name: string;

  @IsEmail()
  email: string;
}

// Global validation
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  transform: true,
}));

// Controller
@Post()
create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto);
}
```

### Q9: What is the purpose of `@Controller()` decorator?

**Answer:** `@Controller()` marks a class as a controller that handles HTTP requests. It accepts an optional route prefix:

```typescript
@Controller('users') // All routes start with /users
export class UserController {
  @Get() // GET /users
  findAll() {}

  @Get(':id') // GET /users/:id
  findOne(@Param('id') id: string) {}
}
```

### Q10: How do you run a NestJS application?

**Answer:**
```bash
# Development
npm run start:dev

# Production
npm run build
npm run start:prod

# With debugging
npm run start:debug
```

The entry point is `main.ts`:
```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
```

---

## Intermediate Level (Questions 11-20)

### Q11: What is middleware and how does it differ from guards?

**Answer:**
- **Middleware**: Executes before routing, handles cross-cutting concerns (logging, CORS)
- **Guard**: Executes after routing, handles authorization

```text
Request → Middleware → Guard → Interceptor → Pipe → Controller
```

Middleware:
```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log('Request...');
    next();
  }
}
```

### Q12: What is the difference between `@Put()` and `@Patch()`?

**Answer:**
- `@Put()`: Full replacement of the resource
- `@Patch()`: Partial update of specific fields

```typescript
@Put(':id')
replace(@Body() dto: FullUserDto) {
  // Replaces entire user
}

@Patch(':id')
update(@Body() dto: PartialUserDto) {
  // Updates only provided fields
}
```

### Q13: What is a DTO and why is it important?

**Answer:** DTO (Data Transfer Object) defines the shape of data for requests/responses. It enables:
- Input validation
- Type safety
- API documentation (Swagger)
- Data transformation

```typescript
export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;
}
```

### Q14: How do you implement authentication in NestJS?

**Answer:**
1. Use `@nestjs/jwt` for JWT tokens
2. Create an AuthGuard
3. Apply guard to protected routes

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

@Controller('users')
@UseGuards(JwtAuthGuard)
export class UserController {
  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }
}
```

### Q15: What is the difference between a Guard and an Interceptor?

**Answer:**
| Feature | Guard | Interceptor |
|---------|-------|-------------|
| Purpose | Authorization | Cross-cutting concerns |
| Executes | Before handler | Before/after handler |
| Can modify response | No | Yes |
| Has access to handler | No | Yes |
| Can be async | Yes | Yes |

### Q16: How do you handle errors in NestJS?

**Answer:**
1. Throw HTTP exceptions:
```typescript
throw new NotFoundException('User not found');
```

2. Use exception filters:
```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse();
    response.status(exception.getStatus()).json({
      statusCode: exception.getStatus(),
      message: exception.message,
    });
  }
}
```

### Q17: What is the difference between `useClass`, `useFactory`, `useValue`, and `useExisting`?

**Answer:**
```typescript
// useClass: Instantiate a class
{ provide: 'SERVICE', useClass: MyService }

// useFactory: Use factory function
{ provide: 'SERVICE', useFactory: (config) => new MyService(config), inject: [Config] }

// useValue: Use static value
{ provide: 'CONFIG', useValue: { host: 'localhost' } }

// useExisting: Alias to existing provider
{ provide: 'Alias', useExisting: MyService }
```

### Q18: What is the purpose of `@nestjs/config`?

**Answer:** It provides Type-safe configuration management:
```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
  ],
})
export class AppModule {}

// Usage
@Injectable()
export class AppService {
  constructor(private config: ConfigService) {}

  getDbHost() {
    return this.config.get<string>('DB_HOST');
  }
}
```

### Q19: How do you test a NestJS service?

**Answer:**
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: Partial<UserRepository>;

  beforeEach(async () => {
    mockRepo = { findAll: jest.fn().mockResolvedValue([]) };

    const module = await Test.createTestingModule({
      providers: [
        UserService,
        { provide: UserRepository, useValue: mockRepo },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  it('should return empty array', async () => {
    expect(await service.findAll()).toEqual([]);
  });
});
```

### Q20: What is Swagger and how do you integrate it?

**Answer:** Swagger provides API documentation:
```typescript
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  await app.listen(3000);
}
```

Controller:
```typescript
@ApiTags('users')
@Controller('users')
export class UserController {
  @ApiOperation({ summary: 'Get all users' })
  @ApiResponse({ status: 200, description: 'Success' })
  @Get()
  findAll() {}
}
```

---

## Senior Level (Questions 21-30)

### Q21: How would you design a scalable NestJS application?

**Answer:**
1. **Modular Architecture**: Group by feature
2. **CQRS**: Separate read/write models
3. **Event-Driven**: Use message brokers for async communication
4. **Caching**: Redis for response caching
5. **Database**: Read replicas, connection pooling
6. **Microservices**: Split by bounded context
7. **Load Balancing**: Multiple instances behind load balancer
8. **Monitoring**: Logging, metrics, tracing

### Q22: Explain the NestJS request lifecycle

**Answer:**
```text
Request
  → Global Middleware
    → Route Matching
      → Controller Guards
        → Interceptor (before)
          → Pipe (validation)
            → Controller Handler
          ← Interceptor (after)
      ← Exception Filter (if error)
  ← Response
```

### Q23: What is the difference between Singleton, Transient, and Request scope?

**Answer:**
- **Singleton (Default)**: One instance per module
- **Transient**: New instance per consumer
- **Request**: New instance per HTTP request

```typescript
@Injectable() // Singleton
class SingletonService {}

@Injectable({ scope: Scope.TRANSIENT })
class TransientService {}

@Injectable({ scope: Scope.REQUEST })
class RequestService {
  constructor(private request: Request) {}
}
```

### Q24: How do you implement CQRS in NestJS?

**Answer:**
```typescript
// Command
export class CreateUserCommand {
  constructor(public name: string, public email: string) {}
}

// Command Handler
@CommandHandler(CreateUserCommand)
export class CreateUserHandler implements ICommandHandler<CreateUserCommand> {
  async execute(command: CreateUserCommand) {
    const user = await this.userRepo.create(command);
    this.eventBus.publish(new UserCreatedEvent(user));
    return user;
  }
}

// Controller
@Post()
async create(@Body() dto: CreateUserDto) {
  return this.commandBus.execute(new CreateUserCommand(dto.name, dto.email));
}
```

### Q25: What is the difference between `ClientProxy.send()` and `ClientProxy.emit()`?

**Answer:**
- `send()`: Request-response pattern, expects response
- `emit()`: Event pattern, fire-and-forget

```typescript
// Request-response
const user = await this.client.send({ cmd: 'get_user' }, { id }).toPromise();

// Event
this.client.emit('user_created', userData);
```

### Q26: How do you implement rate limiting in NestJS?

**Answer:**
Using `@nestjs/throttler`:
```typescript
@Module({
  imports: [
    ThrottlerModule.forRoot([
      { name: 'short', ttl: 1000, limit: 3 },
      { name: 'medium', ttl: 10000, limit: 20 },
      { name: 'long', ttl: 60000, limit: 100 },
    ]),
  ],
})
export class AppModule {}

// Or with guard
@UseGuards(ThrottlerGuard)
@Get('expensive')
expensiveEndpoint() {}
```

### Q27: How do you implement file uploads in NestJS?

**Answer:**
```typescript
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';

@Controller('upload')
export class UploadController {
  @Post('single')
  @UseInterceptors(FileInterceptor('file'))
  uploadFile(@UploadedFile() file: Express.Multer.File) {
    return { filename: file.originalname, size: file.size };
  }

  @Post('multiple')
  @UseInterceptors(FilesInterceptor('files', 10))
  uploadFiles(@UploadedFiles() files: Express.Multer.File[]) {
    return files.map(f => ({ filename: f.originalname }));
  }
}
```

### Q28: How do you implement WebSocket in NestJS?

**Answer:**
```typescript
// Gateway
@WebSocketGateway()
export class EventsGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('message')
  handleMessage(client: Socket, payload: string): void {
    this.server.emit('message', payload);
  }
}

// Module
@Module({
  imports: [ClientsModule.register([
    { name: 'WEBSOCKET', transport: Transport.TCP },
  ])],
  providers: [EventsGateway],
})
export class EventsModule {}
```

### Q29: How do you handle database transactions in NestJS?

**Answer:**
Using TypeORM:
```typescript
@Injectable()
export class UserService {
  constructor(private dataSource: DataSource) {}

  async createUserWithProfile(dto: CreateUserDto) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      const user = await queryRunner.manager.save(User, dto);
      const profile = await queryRunner.manager.save(Profile, { userId: user.id });
      await queryRunner.commitTransaction();
      return { user, profile };
    } catch (err) {
      await queryRunner.rollbackTransaction();
      throw err;
    } finally {
      await queryRunner.release();
    }
  }
}
```

### Q30: What is the purpose of `OnModuleInit` and `OnApplicationShutdown`?

**Answer:** Lifecycle hooks:
```typescript
@Injectable()
export class AppService implements OnModuleInit, OnApplicationShutdown {
  async onModuleInit() {
    // Called once module is initialized
    await this.initializeConnection();
  }

  async onApplicationShutdown(signal?: string) {
    // Called when application shuts down
    await this.closeConnection();
  }
}
```

---

## FAANG-Level (Questions 31-40)

### Q31: Design a multi-tenant NestJS application

**Answer:**
```typescript
// Tenant middleware
@Injectable()
export class TenantMiddleware implements NestMiddleware {
  async use(req: Request, res: Response, next: NextFunction) {
    const tenantId = req.headers['x-tenant-id'];
    const config = await this.configService.getTenantConfig(tenantId);
    req.tenantConfig = config;
    next();
  }
}

// Tenant-aware service
@Injectable()
export class UserService {
  constructor(
    @Inject('TENANT_CONNECTION')
    private connection: Connection,
  ) {}

  async findAll() {
    return this.connection.getRepository(User).find();
  }
}
```

### Q32: How would you implement distributed caching?

**Answer:**
```typescript
// Redis cache module
@Module({
  imports: [
    CacheModule.registerAsync({
      useFactory: (config: ConfigService) => ({
        store: redisStore,
        host: config.get('REDIS_HOST'),
        port: config.get('REDIS_PORT'),
        ttl: 60,
      }),
      inject: [ConfigService],
    }),
  ],
})
export class CacheModule {}

// Service
@Injectable()
export class ProductService {
  constructor(@Inject(CACHE_MANAGER) private cache: Cache) {}

  async findAll(): Promise<Product[]> {
    const cached = await this.cache.get<Product[]>('products');
    if (cached) return cached;

    const products = await this.productRepo.find();
    await this.cache.set('products', products, 300);
    return products;
  }
}
```

### Q33: Design a circuit breaker pattern in NestJS

**Answer:**
```typescript
@Injectable()
export class CircuitBreakerService {
  private state = 'CLOSED';
  private failureCount = 0;
  private threshold = 5;
  private resetTimeout = 30000;

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      throw new ServiceUnavailableException('Circuit is open');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      setTimeout(() => { this.state = 'HALF_OPEN'; }, this.resetTimeout);
    }
  }
}
```

### Q34: How would you implement event sourcing in NestJS?

**Answer:**
```typescript
// Event store
@Injectable()
export class EventStore {
  async save(event: DomainEvent) {
    await this.eventTable.insert({
      aggregateId: event.aggregateId,
      eventType: event.eventType,
      payload: JSON.stringify(event),
      version: event.version,
      timestamp: new Date(),
    });
  }

  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    return this.eventTable.find({ where: { aggregateId } });
  }
}

// Aggregate
export class OrderAggregate {
  private events: DomainEvent[] = [];

  static fromEvents(events: DomainEvent[]): OrderAggregate {
    const aggregate = new OrderAggregate();
    events.forEach(event => aggregate.apply(event));
    return aggregate;
  }

  apply(event: DomainEvent) {
    this.events.push(event);
    this.applyEvent(event);
  }
}
```

### Q35: Design a real-time notification system

**Answer:**
```typescript
// Notification service
@Injectable()
export class NotificationService {
  constructor(
    @Inject('WEBSOCKET') private wsClient: ClientProxy,
    private emailService: EmailService,
    private pushService: PushService,
  ) {}

  async notify(userId: string, notification: NotificationDto) {
    // Real-time
    this.wsClient.emit('notification', { userId, ...notification });

    // Email
    if (notification.channels.includes('email')) {
      await this.emailService.send(notification);
    }

    // Push
    if (notification.channels.includes('push')) {
      await this.pushService.send(userId, notification);
    }
  }
}

// WebSocket gateway
@WebSocketGateway()
export class NotificationGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('subscribe')
  handleSubscribe(client: Socket, userId: string) {
    client.join(`user:${userId}`);
  }

  sendNotification(userId: string, notification: any) {
    this.server.to(`user:${userId}`).emit('notification', notification);
  }
}
```

### Q36: How would you implement API versioning?

**Answer:**
```typescript
// main.ts
app.enableVersioning({
  type: VersioningType.URI,
});

// Controller
@Controller({ path: 'users', version: '1' })
export class UsersV1Controller {
  @Get()
  findAll() { return 'v1 users'; }
}

@Controller({ path: 'users', version: '2' })
export class UsersV2Controller {
  @Get()
  findAll() { return 'v2 users with new fields'; }
}
```

### Q37: Design a feature flag system

**Answer:**
```typescript
@Injectable()
export class FeatureFlagService {
  constructor(private config: ConfigService) {}

  async isEnabled(flag: string, context?: any): Promise<boolean> {
    const flags = await this.getFlags();
    const feature = flags[flag];

    if (!feature) return false;

    if (feature.percentage !== undefined) {
      const hash = this.hashContext(context);
      return (hash % 100) < feature.percentage;
    }

    return feature.enabled;
  }

  private hashContext(context: any): number {
    const str = JSON.stringify(context);
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
    }
    return Math.abs(hash) % 100;
  }
}

// Guard
@Injectable()
export class FeatureFlagGuard implements CanActivate {
  constructor(private featureService: FeatureFlagService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const flag = this.reflector.get<string>('feature', context.getHandler());
    if (!flag) return true;
    return this.featureService.isEnabled(flag);
  }
}
```

### Q38: How would you implement zero-downtime deployments?

**Answer:**
1. **Health Checks**: Ensure service is ready before accepting traffic
2. **Graceful Shutdown**: Complete in-flight requests before stopping
3. **Load Balancer**: Route traffic away from old instances

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Health check endpoint
  app.useLogger(['error', 'warn', 'log', 'debug', 'verbose']);

  // Graceful shutdown
  app.enableShutdownHooks();

  await app.listen(3000);
}

// OnApplicationShutdown hook
@Injectable()
export class AppService implements OnApplicationShutdown {
  async onApplicationShutdown() {
    // Close database connections
    await this.database.disconnect();
    // Finish in-flight requests
    await this.server.close();
  }
}
```

### Q39: Design a distributed tracing system

**Answer:**
```typescript
// Trace interceptor
@Injectable()
export class TraceInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const traceId = uuid();
    const spanId = uuid();

    // Add to request
    const request = context.switchToHttp().getRequest();
    request.traceId = traceId;
    request.spanId = spanId;

    // Add to response headers
    const response = context.switchToHttp().getResponse();
    response.setHeader('X-Trace-Id', traceId);

    const startTime = Date.now();

    return next.handle().pipe(
      tap({
        next: () => this.exportSpan(traceId, spanId, startTime, 'OK'),
        error: (err) => this.exportSpan(traceId, spanId, startTime, 'ERROR'),
      }),
    );
  }

  private exportSpan(traceId: string, spanId: string, startTime: number, status: string) {
    const duration = Date.now() - startTime;
    // Export to Jaeger/Zipkin
    this.tracer.export({ traceId, spanId, duration, status });
  }
}
```

### Q40: How would you optimize NestJS application performance?

**Answer:**
1. **Caching**: Redis for response caching
2. **Compression**: Enable gzip
3. **Connection Pooling**: Database connection pools
4. **Lazy Loading**: Defer non-critical modules
5. **Async Operations**: Non-blocking I/O
6. **Pagination**: Always paginate lists
7. **Response Compression**: Compress large payloads
8. **Rate Limiting**: Prevent abuse
9. **Load Balancing**: Multiple instances
10. **Monitoring**: Track and optimize slow queries

```typescript
// Enable compression
app.use(compression());

// Enable CORS
app.enableCors();

// Use Fastify instead of Express
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter(),
);
```

---

## Summary

These 40 questions cover NestJS from beginner to FAANG-level complexity. Key areas:
- **Beginner**: Core concepts, decorators, basic patterns
- **Intermediate**: Testing, authentication, validation, Swagger
- **Senior**: Architecture, CQRS, microservices, patterns
- **FAANG**: Distributed systems, event sourcing, performance optimization

## References & Learn More

- [NestJS Official Docs](https://docs.nestjs.com/)
- [NestJS GitHub Repository](https://github.com/nestjs/nest)
- [NestJS Blog - Tips & Tricks](https://trilon.io/blog)
- [Awesome NestJS - Curated Resources](https://github.com/nestjs/awesome-nestjs)
