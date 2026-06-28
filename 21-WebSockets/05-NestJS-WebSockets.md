# NestJS WebSockets

## Definition

NestJS provides first-class support for WebSockets through its **WebSocket Gateway** system. Built on top of Socket.io, NestJS WebSockets integrate seamlessly with the NestJS ecosystem, supporting **decorators, dependency injection, guards, interceptors, pipes, and filters** just like HTTP controllers.

The WebSocket Gateway acts as a bridge between clients and the NestJS application, enabling real-time bidirectional communication while maintaining the modular, testable architecture NestJS is known for.

## Why Do We Need It?

| Feature | Raw Socket.io | NestJS WebSockets |
|---|---|---|
| Architecture | Manual setup | Module-based |
| Dependency Injection | Not available | Full DI support |
| Guards | Manual implementation | Decorator-based |
| Interceptors | Manual implementation | Built-in support |
| Pipes | Manual validation | Request validation |
| Filters | Manual error handling | Exception filters |
| Testing | Difficult | Unit testable |
| Type Safety | Manual | Decorator-based |

## How It Works

### NestJS WebSocket Architecture

```text
+------------------+     +------------------+     +------------------+

|     Client       |     |   WebSocket      |     |    NestJS        |
|    (Browser)     | --> |   Gateway        | --> |   Application    |

+------------------+     +------------------+     +------------------+

                              |                         |

                              | Guards                  | Services
                              | Interceptors           | Controllers
                              | Pipes                  | Modules

                              | Filters                |

```

### Gateway Lifecycle

```text
+-----------+     +-----------+     +-----------+     +-----------+

|  Module   | --> |  Gateway  | --> |  Handle   | --> |  Cleanup  |
|  Init     |     |  Listen   |     |  Events   |     |  OnModule |
|           |     |           |     |           |     |  Destroy  |

+-----------+     +-----------+     +-----------+     +-----------+

```

## Code Examples

### Basic WebSocket Gateway

```typescript
import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
  OnGatewayInit,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';

@WebSocketGateway({
  cors: {
    origin: '*',
  },
  namespace: '/',
})
export class AppGateway
  implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect
{
  @WebSocketServer()
  server: Server;

  private logger = new Logger('AppGateway');

  afterInit(server: Server) {
    this.logger.log('WebSocket Gateway initialized');
  }

  handleConnection(client: Socket, ...args: any[]) {
    this.logger.log(`Client connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    this.logger.log(`Client disconnected: ${client.id}`);
  }

  @SubscribeMessage('message')
  handleMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() payload: { text: string; room: string }
  ): void {
    this.logger.log(`Message from ${client.id}: ${payload.text}`);

    // Broadcast to all clients
    this.server.emit('message', {
      userId: client.id,
      text: payload.text,
      timestamp: Date.now(),
    });

    // Or send to specific room
    this.server.to(payload.room).emit('room-message', {
      userId: client.id,
      text: payload.text,
    });
  }
}

```

### Gateway with DI Services

```typescript
import { WebSocketGateway, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Inject } from '@nestjs/common';
import { ChatService } from './chat.service';
import { NotificationService } from './notification.service';

@WebSocketGateway({ cors: true })
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  constructor(
    @Inject(ChatService) private chatService: ChatService,
    @Inject(NotificationService) private notificationService: NotificationService,
  ) {}

  @SubscribeMessage('join-room')
  async handleJoinRoom(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; userId: string }
  ): Promise<void> {
    client.join(data.roomId);

    const room = await this.chatService.getRoom(data.roomId);
    client.emit('room-joined', {
      roomId: data.roomId,
      roomName: room.name,
      members: room.members,
    });

    client.to(data.roomId).emit('user-joined', {
      userId: data.userId,
      roomId: data.roomId,
    });
  }

  @SubscribeMessage('send-message')
  async handleSendMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; content: string; userId: string }
  ): Promise<void> {
    const message = await this.chatService.saveMessage({
      roomId: data.roomId,
      userId: data.userId,
      content: data.content,
    });

    this.server.to(data.roomId).emit('new-message', message);

    // Notify offline users
    await this.notificationService.notifyRoomMembers(data.roomId, {
      type: 'new-message',
      messageId: message.id,
      roomId: data.roomId,
    });
  }
}

```

### Guards for WebSocket Authentication

```typescript
import { CanActivate, ExecutionContext, Injectable, Logger } from '@nestjs/common';
import { WsException } from '@nestjs/websockets';
import { JwtService } from '@nestjs/jwt';
import { Socket } from 'socket.io';

@Injectable()
export class WsJwtGuard implements CanActivate {
  private logger = new Logger('WsJwtGuard');

  constructor(private jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    try {
      const client: Socket = context.switchToWs().getClient();
      const token = this.extractTokenFromHandshake(client);

      if (!token) {
        throw new WsException('Unauthorized');
      }

      const payload = await this.jwtService.verifyAsync(token);
      client.data.user = payload;

      return true;
    } catch (error) {
      this.logger.error('WebSocket authentication failed:', error);
      throw new WsException('Unauthorized');
    }
  }

  private extractTokenFromHandshake(client: Socket): string | undefined {
    const auth = client.handshake.auth;
    return auth?.token || client.handshake.query?.token as string;
  }
}

// Apply guard to gateway
@UseGuards(WsJwtGuard)
@WebSocketGateway({ cors: true })
export class ProtectedGateway {
  @SubscribeMessage('protected-event')
  handleProtectedEvent(@ConnectedSocket() client: Socket): void {
    const user = client.data.user;
    client.emit('response', { message: `Hello ${user.username}` });
  }
}

```

### Interceptors

```typescript
import { CallHandler, ExecutionContext, Injectable, Logger, NestInterceptor } from '@nestjs/common';
import { Observable, tap } from 'rxjs';
import { WsResponse } from '@nestjs/websockets';

@Injectable()
export class WsLoggingInterceptor implements NestInterceptor {
  private logger = new Logger('WsLoggingInterceptor');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const client = context.switchToWs().getClient();
    const data = context.switchToWs().getData();
    const startTime = Date.now();

    this.logger.log(`Client ${client.id} sending: ${JSON.stringify(data)}`);

    return next.handle().pipe(
      tap((response) => {
        const duration = Date.now() - startTime;
        this.logger.log(
          `Client ${client.id} response sent in ${duration}ms`
        );
      }),
    );
  }
}

// Apply interceptor to gateway
@UseInterceptors(WsLoggingInterceptor)
@WebSocketGateway({ cors: true })
export class LoggedGateway {
  @SubscribeMessage('event')
  handleEvent(): WsResponse<{ message: string }> {
    return { event: 'event-response', data: { message: 'Handled' } };
  }
}

```

### Pipes for Validation

```typescript
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';
import { plainToInstance } from 'class-transformer';
import { IsString, IsNumber, Min, Max } from 'class-validator';

class CreateMessageDto {
  @IsString()
  roomId: string;

  @IsString()
  @Min(1)
  @Max(1000)
  content: string;

  @IsNumber()
  @Min(0)
  @Max(100)
  priority: number;
}

@Injectable()
export class WsValidationPipe implements PipeTransform {
  async transform(value: any, metadata: ArgumentMetadata) {
    const dto = plainToInstance(CreateMessageDto, value);
    const errors = await validate(dto);

    if (errors.length > 0) {
      const message = errors
        .map((err) => Object.values(err.constraints || {}).join(', '))
        .join('; ');
      throw new BadRequestException(message);
    }

    return dto;
  }
}

// Use in gateway
@WebSocketGateway({ cors: true })
export class ValidatedGateway {
  @SubscribeMessage('create-message')
  handleMessage(
    @MessageBody(new WsValidationPipe()) data: CreateMessageDto
  ): void {
    // data is validated and typed
    console.log(data.roomId, data.content, data.priority);
  }
}

```

### Rooms Management

```typescript
import { WebSocketGateway, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Injectable } from '@nestjs/common';

@WebSocketGateway({ cors: true })
export class RoomGateway {
  @WebSocketServer()
  server: Server;

  private rooms = new Map<string, Set<string>>();

  @SubscribeMessage('create-room')
  handleCreateRoom(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomName: string; userId: string }
  ): { roomId: string } {
    const roomId = `room-${Date.now()}`;
    client.join(roomId);
    this.rooms.set(roomId, new Set([data.userId]));

    return { roomId };
  }

  @SubscribeMessage('join-room')
  handleJoinRoom(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; userId: string }
  ): void {
    client.join(data.roomId);
    this.rooms.get(data.roomId)?.add(data.userId);

    this.server.to(data.roomId).emit('user-joined', {
      userId: data.userId,
      roomId: data.roomId,
      members: Array.from(this.rooms.get(data.roomId) || []),
    });
  }

  @SubscribeMessage('leave-room')
  handleLeaveRoom(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; userId: string }
  ): void {
    client.leave(data.roomId);
    this.rooms.get(data.roomId)?.delete(data.userId);

    this.server.to(data.roomId).emit('user-left', {
      userId: data.userId,
      roomId: data.roomId,
    });
  }

  @SubscribeMessage('room-message')
  handleRoomMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; message: string }
  ): void {
    this.server.to(data.roomId).emit('new-message', {
      userId: client.data.user?.id,
      roomId: data.roomId,
      message: data.message,
      timestamp: Date.now(),
    });
  }

  handleDisconnect(client: Socket): void {
    // Remove user from all rooms
    this.rooms.forEach((members, roomId) => {
      if (members.has(client.data.user?.id)) {
        members.delete(client.data.user.id);
        this.server.to(roomId).emit('user-left', {
          userId: client.data.user.id,
          roomId,
        });
      }
    });
  }
}

```

### Namespaces

```typescript
import { WebSocketGateway, WebSocketServer, SubscribeMessage } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';

// Chat namespace
@WebSocketGateway({
  namespace: '/chat',
  cors: { origin: '*' },
})
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  private logger = new Logger('ChatGateway');

  @SubscribeMessage('message')
  handleMessage(client: Socket, data: { text: string; room: string }): void {
    this.server.to(data.room).emit('new-message', {
      userId: client.id,
      text: data.text,
    });
  }
}

// Admin namespace
@WebSocketGateway({
  namespace: '/admin',
  cors: { origin: '*' },
})
export class AdminGateway {
  @WebSocketServer()
  server: Server;

  private logger = new Logger('AdminGateway');

  @SubscribeMessage('get-stats')
  handleGetStats(client: Socket): void {
    const stats = {
      connectedUsers: this.server.engine.clientsCount,
      timestamp: Date.now(),
    };
    client.emit('stats', stats);
  }

  @SubscribeMessage('broadcast')
  handleBroadcast(client: Socket, data: { message: string }): void {
    this.server.emit('announcement', data.message);
  }
}

```

### Client-Side Integration

```typescript
// Socket.io client for NestJS
import { io, Socket } from 'socket.io-client';

class NestWebSocketClient {
  private socket: Socket;

  constructor(private url: string) {
    this.socket = io(url, {
      auth: {
        token: localStorage.getItem('token'),
      },
      transports: ['websocket', 'polling'],
    });

    this.setupListeners();
  }

  private setupListeners(): void {
    this.socket.on('connect', () => {
      console.log('Connected to NestJS WebSocket');
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error.message);
    });

    this.socket.on('new-message', (data) => {
      console.log('New message:', data);
    });

    this.socket.on('user-joined', (data) => {
      console.log('User joined:', data);
    });
  }

  joinRoom(roomId: string, userId: string): void {
    this.socket.emit('join-room', { roomId, userId });
  }

  sendMessage(roomId: string, message: string): void {
    this.socket.emit('send-message', { roomId, content: message });
  }

  leaveRoom(roomId: string, userId: string): void {
    this.socket.emit('leave-room', { roomId, userId });
  }

  disconnect(): void {
    this.socket.disconnect();
  }
}

```

### Error Handling

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, Logger } from '@nestjs/common';
import { WsException } from '@nestjs/websockets';
import { Socket } from 'socket.io';

@Catch()
export class WebSocketExceptionFilter implements ExceptionFilter {
  private logger = new Logger('WebSocketExceptionFilter');

  catch(exception: unknown, host: ArgumentsHost): void {
    const client = host.switchToWs().getClient<Socket>();
    const error = exception instanceof WsException ? exception.getError() : exception;

    const errorResponse = {
      status: 'error',
      message: error instanceof Error ? error.message : 'Internal server error',
      timestamp: Date.now(),
    };

    this.logger.error(`WebSocket error for ${client.id}:`, error);
    client.emit('error', errorResponse);
  }
}

// Apply to gateway
@UseFilters(WebSocketExceptionFilter)
@WebSocketGateway({ cors: true })
export class ErrorHandledGateway {
  @SubscribeMessage('risky-operation')
  async handleRiskyOperation(@ConnectedSocket() client: Socket): Promise<void> {
    try {
      const result = await this.performRiskyOperation();
      client.emit('result', { success: true, data: result });
    } catch (error) {
      throw new WsException('Operation failed');
    }
  }
}

```

### Module Configuration

```typescript
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { ChatGateway } from './chat.gateway';
import { RoomGateway } from './room.gateway';
import { WsJwtGuard } from './ws-jwt.guard';
import { ChatService } from './chat.service';
import { NotificationService } from './notification.service';

@Module({
  imports: [
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: { expiresIn: '1h' },
    }),
  ],
  providers: [
    ChatGateway,
    RoomGateway,
    WsJwtGuard,
    ChatService,
    NotificationService,
  ],
})
export class WebSocketModule {}

```

## Real-World Use Cases

### 1. Chat Application

```typescript
@WebSocketGateway({
  cors: { origin: '*' },
  namespace: '/chat',
})
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  constructor(
    private chatService: ChatService,
    private notificationService: NotificationService,
  ) {}

  @SubscribeMessage('send-message')
  async handleMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { roomId: string; content: string }
  ): Promise<void> {
    const user = client.data.user;

    const message = await this.chatService.saveMessage({
      roomId: data.roomId,
      userId: user.id,
      content: data.content,
    });

    this.server.to(data.roomId).emit('new-message', {
      id: message.id,
      userId: user.id,
      username: user.username,
      content: data.content,
      timestamp: message.createdAt,
    });

    // Typing indicator reset
    this.server.to(data.roomId).emit('user-stopped-typing', {
      userId: user.id,
      roomId: data.roomId,
    });
  }
}

```

### 2. Real-Time Notifications

```typescript
@WebSocketGateway({ cors: { origin: '*' } })
export class NotificationGateway {
  @WebSocketServer()
  server: Server;

  private userSockets = new Map<string, Set<string>>();

  handleConnection(client: Socket): void {
    const userId = client.data.user?.id;
    if (userId) {
      if (!this.userSockets.has(userId)) {
        this.userSockets.set(userId, new Set());
      }
      this.userSockets.get(userId)!.add(client.id);
    }
  }

  sendNotification(userId: string, notification: any): void {
    const sockets = this.userSockets.get(userId);
    sockets?.forEach((socketId) => {
      this.server.to(socketId).emit('notification', notification);
    });
  }
}

```

### 3. Live Collaboration

```typescript
@WebSocketGateway({ cors: { origin: '*' } })
export class CollaborationGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('cursor-move')
  handleCursorMove(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { documentId: string; position: { x: number; y: number } }
  ): void {
    client.to(data.documentId).emit('cursor-update', {
      userId: client.data.user.id,
      position: data.position,
    });
  }

  @SubscribeMessage('operation')
  handleOperation(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { documentId: string; operation: any }
  ): void {
    client.to(data.documentId).emit('remote-operation', {
      userId: client.data.user.id,
      operation: data.operation,
    });
  }
}

```

## Common Mistakes

### 1. Not Using Guards

```typescript
// ❌ Bad: No authentication
@WebSocketGateway({ cors: true })
export class InsecureGateway {
  @SubscribeMessage('sensitive-action')
  handleSensitiveAction(): void {
    // Anyone can call this
  }
}

// ✅ Good: Using guards
@UseGuards(WsJwtGuard)
@WebSocketGateway({ cors: true })
export class SecureGateway {
  @SubscribeMessage('sensitive-action')
  handleSensitiveAction(@ConnectedSocket() client: Socket): void {
    // Only authenticated users can call this
    const user = client.data.user;
  }
}

```

### 2. Not Handling Disconnects

```typescript
// ❌ Bad: No cleanup
@WebSocketGateway({ cors: true })
export class BadGateway {
  @SubscribeMessage('join-room')
  handleJoinRoom(client: Socket, data: { roomId: string }): void {
    client.join(data.roomId);
    // No cleanup on disconnect
  }
}

// ✅ Good: Proper cleanup
@WebSocketGateway({ cors: true })
export class GoodGateway {
  handleDisconnect(client: Socket): void {
    // Clean up user data
    this.removeUserFromRooms(client.id);
    this.updatePresence(client.data.user?.id, 'offline');
  }
}

```

### 3. Not Validating Data

```typescript
// ❌ Bad: No validation
@SubscribeMessage('send-message')
handleMessage(@MessageBody() data: any): void {
  // Could crash on malformed data
  saveToDatabase(data);
}

// ✅ Good: With validation pipe
@SubscribeMessage('send-message')
handleMessage(
  @MessageBody(new WsValidationPipe()) data: CreateMessageDto
): void {
  // data is validated and typed
  saveToDatabase(data);
}

```

## Best Practices

### 1. Use DTOs for Message Validation

```typescript
export class SendMessageDto {
  @IsString()
  @IsNotEmpty()
  roomId: string;

  @IsString()
  @MinLength(1)
  @MaxLength(1000)
  content: string;
}

@SubscribeMessage('send-message')
async handleMessage(
  @MessageBody(new WsValidationPipe()) data: SendMessageDto,
  @ConnectedSocket() client: Socket
): Promise<void> {
  // Process validated data
}

```

### 2. Implement Rate Limiting

```typescript
@Injectable()
export class WsThrottlerGuard implements CanActivate {
  private clients = new Map<string, { count: number; resetAt: number }>();

  canActivate(context: ExecutionContext): boolean {
    const client = context.switchToWs().getClient();
    const now = Date.now();
    const record = this.clients.get(client.id);

    if (!record || now > record.resetAt) {
      this.clients.set(client.id, { count: 1, resetAt: now + 60000 });
      return true;
    }

    if (record.count >= 100) {
      throw new WsException('Rate limit exceeded');
    }

    record.count++;
    return true;
  }
}

```

### 3. Use Namespace for Separation

```typescript
// Chat namespace
@WebSocketGateway({ namespace: '/chat' })
export class ChatGateway {}

// Notifications namespace
@WebSocketGateway({ namespace: '/notifications' })
export class NotificationGateway {}

// Admin namespace
@WebSocketGateway({ namespace: '/admin' })
export class AdminGateway {}

```

## Interview Questions

### Beginner (5)

1. **What is a WebSocket Gateway in NestJS?**

   - Bridge between clients and NestJS application
   - Handles WebSocket connections and events
   - Supports decorators, guards, interceptors
   - Built on top of Socket.io

2. **How do you create a WebSocket Gateway?**

   - Use `@WebSocketGateway()` decorator
   - Implement `OnGatewayInit`, `OnGatewayConnection`, `OnGatewayDisconnect`
   - Use `@SubscribeMessage()` for event handling
   - Inject services via constructor

3. **What are WebSocket Guards?**

   - Authentication/authorization for WebSocket connections
   - Implement `CanActivate` interface
   - Access client via `context.switchToWs().getClient()`
   - Throw `WsException` for rejection

4. **How do you handle WebSocket events?**

   - Use `@SubscribeMessage('event-name')` decorator
   - Access data with `@MessageBody()`
   - Access client with `@ConnectedSocket()`
   - Return response or emit event

5. **What is the difference between WebSocket and HTTP in NestJS?**

   - WebSocket is persistent connection
   - HTTP is request-response
   - WebSocket uses Gateway, HTTP uses Controller
   - WebSocket supports bidirectional communication

### Intermediate (5-8)

6. **How do you implement authentication in WebSocket Gateway?**

   - Use JWT guard
   - Extract token from handshake
   - Verify token and attach user to client
   - Use in all message handlers

7. **How do you handle rooms in NestJS WebSockets?**

   - Use `client.join(roomId)` to join
   - Use `client.leave(roomId)` to leave
   - Use `this.server.to(roomId).emit()` for room messages
   - Track room membership

8. **How do you use interceptors with WebSocket?**

   - Create class implementing `NestInterceptor`
   - Use `@UseInterceptors()` decorator
   - Log, transform, or handle errors
   - Apply globally or per gateway

9. **How do you test WebSocket Gateways?**

   - Mock Socket.io server
   - Test message handlers
   - Test guards and interceptors
   - Use `socket.io-client` for integration tests

10. **How do you handle errors in WebSocket Gateways?**

    - Use exception filters
    - Throw `WsException`
    - Catch errors in handlers
    - Emit error events to client

### Senior (8-12)

11. **Design a scalable WebSocket architecture with NestJS**

    - Use Redis adapter for scaling
    - Implement connection pooling
    - Use namespaces for separation
    - Monitor with metrics

12. **How do you handle WebSocket scaling across multiple servers?**

    - Use `@nestjs/platform-socket.io` with Redis adapter
    - Implement sticky sessions
    - Share state via Redis
    - Use message brokers for cross-server communication

13. **How do you implement WebSocket middleware?**

    - Use `@WebSocketGateway({ useMiddleware: ... })`
    - Implement `NestMiddleware`
    - Log, validate, or transform messages
    - Apply to all gateway events

14. **How do you handle WebSocket in microservices?**

    - Use WebSocket gateway in API gateway
    - Communicate via message broker
    - Implement service discovery
    - Handle connection state

15. **How do you monitor WebSocket connections?**

    - Track connection counts
    - Monitor message rates
    - Alert on errors
    - Dashboard for visibility

### FAANG-style (5-8)

16. **Design a real-time chat system with NestJS**

    - WebSocket gateway for connections
    - Redis for scaling
    - Message persistence
    - Presence tracking
    - Push notification fallback

17. **Design a collaborative editing system**

    - Operational Transform or CRDT
    - Cursor presence
    - Version history
    - Conflict resolution
    - Offline support

18. **Design a multiplayer game backend**

    - WebSocket gateway for connections
    - Game state management
    - Anti-cheat measures
    - Scaling across servers
    - Reconnection handling

19. **Design a live notification system**

    - WebSocket gateway for real-time
    - Redis for scaling
    - Message persistence
    - User preferences
    - Delivery guarantees

20. **Design a live dashboard system**

    - WebSocket for real-time updates
    - Data aggregation
    - Connection management
    - Caching strategies
    - Export functionality

### Follow-ups (5-8)

21. **How do you handle WebSocket reconnection in NestJS?**

    - Client-side reconnection logic
    - Server-side state preservation
    - Missed message recovery
    - Connection state tracking

22. **How do you secure WebSocket connections?**

    - Use WSS (WebSocket Secure)
    - Implement JWT authentication
    - Rate limit connections
    - Validate all messages

23. **How do you optimize WebSocket performance?**

    - Message compression
    - Binary protocol
    - Connection pooling
    - Message batching

24. **How do you handle WebSocket in production?**

    - Graceful shutdown
    - Health checks
    - Monitoring and alerting
    - Log aggregation

25. **How do you migrate to NestJS WebSockets?**

    - Start with simple gateway
    - Add authentication
    - Implement guards and interceptors
    - Scale with Redis

## Summary

NestJS WebSockets provide:

- **Gateway System**: Seamless integration with NestJS ecosystem
- **Decorators**: `@SubscribeMessage`, `@MessageBody`, `@ConnectedSocket`
- **Guards**: Authentication and authorization
- **Interceptors**: Logging, transformation, error handling
- **Pipes**: Message validation
- **Filters**: Exception handling
- **DI Support**: Full dependency injection

Key benefits:

- Maintainable, testable code
- Consistent architecture with HTTP
- Built-in security features
- Easy scaling with Redis adapter
- Production-ready patterns

## References & Learn More

- [NestJS WebSocket Documentation](https://docs.nestjs.com/websockets)
- [Socket.io Adapter](https://docs.nestjs.com/websockets/socketio-adapter)
- [Gateways](https://docs.nestjs.com/websockets/gateways)
- [Exception Filters](https://docs.nestjs.com/exception-filters)
- [Pipes](https://docs.nestjs.com/pipes)
- [Guards](https://docs.nestjs.com/guards)
