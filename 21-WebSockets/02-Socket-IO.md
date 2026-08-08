---
section: WebSockets
category: Real-Time
tags: [concept, reference, tool]
---

# Socket.io

## Definition

Socket.io is a **real-time, event-driven JavaScript library** that enables bidirectional communication between clients and servers. Built on top of WebSockets, it provides automatic fallbacks to HTTP long-polling and other transports, ensuring connectivity across different network environments.

Socket.io abstracts the complexity of WebSockets, offering features like **rooms, namespaces, automatic reconnection, multiplexing, and broadcasting** out of the box.

## Why Do We Need It?

| Raw WebSockets | Socket.io |
|---|---|
| Manual fallback handling | Automatic transport fallback |
| No built-in reconnection | Automatic reconnection with backoff |
| No message acknowledgment | Built-in ACK callbacks |
| No room/namespace concept | Native rooms and namespaces |
| Manual event handling | Event-based API |
| No binary support handling | Automatic binary detection |
| Connection state management | Built-in connection management |

### Transport Fallback

```text
Socket.io Transport Selection:

1. Try WebSocket (fastest)
   ↓ (if fails)

2. Try HTTP Long Polling
   ↓ (if fails)

3. Try HTTP Streaming
   ↓ (if fails)

4. Connection failed

Result: Best available transport selected automatically

```

## How It Works

### Architecture

```text
+-------------------+        +-------------------+        +-------------------+

|     Client        |        |      Server       |        |     Database      |
|   (Browser)       |        |   (Node.js)       |        |   (MongoDB)       |

+-------------------+        +-------------------+        +-------------------+

        |                             |                           |
        |  1. HTTP GET /socket.io/    |                           |
        |---------------------------> |                           |
        |                             |                           |
        |  2. 200 OK (polling)        |                           |
        | <---------------------------|                           |
        |                             |                           |
        |  3. POST /socket.io/        |                           |
        |---------------------------> |                           |
        |                             |                           |
        |  4. Upgrade to WebSocket    |                           |
        |---------------------------> |                           |
        |                             |                           |
        |  5. WebSocket Connection    |                           |
        |<===========================>|                           |
        |                             |                           |
        |  6. emit('event', data)     |                           |
        |---------------------------> |-------------------------->|
        |                             |                           |
        |  7. on('event', callback)   |                           |
        | <---------------------------| <--------------------------|

```

### Connection Lifecycle

```text
+-----------+     +-----------+     +-----------+     +-----------+

| CONNECTING| --> | CONNECTED | --> | RECONNECT | --> | DISCONNECT|

+-----------+     +-----------+     +-----------+     +-----------+

      |                |                 |                 |

      | Transport      | Events flow     | Auto-retry     | Max attempts
      | negotiation    | both ways       | with backoff   | reached

```

## Code Examples

### Basic Server Setup

```typescript
import { Server } from 'socket.io';
import { createServer } from 'http';
import express from 'express';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: ['http://localhost:3000', 'https://myapp.com'],
    methods: ['GET', 'POST'],
    credentials: true,
  },
  pingInterval: 25000,
  pingTimeout: 60000,
  maxHttpBufferSize: 1e6, // 1MB
  transports: ['websocket', 'polling'],
  allowUpgrades: true,
  perMessageDeflate: {
    threshold: 1024,
  },
});

// Connection handler
io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);

  // Send welcome message
  socket.emit('welcome', {
    message: 'Connected to server',
    socketId: socket.id,
    serverTime: Date.now(),
  });

  // Handle events
  socket.on('message', (data) => {
    console.log('Received message:', data);
    io.emit('broadcast', data); // Broadcast to all clients
  });

  // Handle disconnect
  socket.on('disconnect', (reason) => {
    console.log(`Client ${socket.id} disconnected: ${reason}`);
  });
});

httpServer.listen(3000);

```

### Basic Client Setup

```typescript
import { io, Socket } from 'socket.io-client';

const socket: Socket = io('http://localhost:3000', {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  timeout: 20000,
  transports: ['websocket', 'polling'],
});

// Connection events
socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('welcome', (data) => {
  console.log('Server says:', data);
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error.message);
});

socket.on('reconnect_attempt', (attempt) => {
  console.log('Reconnection attempt:', attempt);
});

socket.on('reconnect', (attempt) => {
  console.log('Reconnected after', attempt, 'attempts');
});

// Send messages
function sendMessage(message: string): void {
  socket.emit('message', {
    text: message,
    timestamp: Date.now(),
  });
}

// Emit with acknowledgment
function sendWithAck(data: unknown): void {
  socket.emit('message', data, (response: { success: boolean }) => {
    if (response.success) {
      console.log('Message delivered');
    } else {
      console.log('Failed to deliver message');
    }
  });
}

```

### Rooms

```typescript
// Server-side room management
io.on('connection', (socket) => {
  // Join a room
  socket.on('join-room', (roomId: string) => {
    socket.join(roomId);
    console.log(`Socket ${socket.id} joined room ${roomId}`);

    // Notify room members
    socket.to(roomId).emit('user-joined', {
      userId: socket.id,
      roomId,
    });

    // Send room state to joining user
    const roomSockets = io.sockets.adapter.rooms.get(roomId);
    socket.emit('room-state', {
      roomId,
      members: Array.from(roomSockets || []),
      memberCount: roomSockets?.size || 0,
    });
  });

  // Leave a room
  socket.on('leave-room', (roomId: string) => {
    socket.leave(roomId);
    socket.to(roomId).emit('user-left', {
      userId: socket.id,
      roomId,
    });
  });

  // Send message to room
  socket.on('room-message', ({ roomId, message }) => {
    io.to(roomId).emit('new-message', {
      from: socket.id,
      message,
      timestamp: Date.now(),
    });
  });

  // Join multiple rooms
  socket.on('join-channels', (channels: string[]) => {
    channels.forEach((channel) => {
      socket.join(`channel:${channel}`);
    });
  });
});

// Room utilities
class RoomManager {
  // Get all rooms a socket is in
  getSocketRooms(socketId: string): string[] {
    const socket = io.sockets.sockets.get(socketId);
    if (!socket) return [];
    return Array.from(socket.rooms).filter((room) => room !== socketId);
  }

  // Get all sockets in a room
  getRoomMembers(roomId: string): string[] {
    const room = io.sockets.adapter.rooms.get(roomId);
    return room ? Array.from(room) : [];
  }

  // Get total connected sockets
  getConnectedCount(): number {
    return io.engine.clientsCount;
  }

  // Broadcast to all except sender
  broadcastExcept(senderId: string, event: string, data: unknown): void {
    socket.broadcast.emit(event, data);
  }
}

```

### Namespaces

```typescript
// Create namespaces
const chatNamespace = io.of('/chat');
const adminNamespace = io.of('/admin');
const notificationsNamespace = io.of('/notifications');

// Chat namespace
chatNamespace.on('connection', (socket) => {
  console.log('User connected to chat');

  socket.on('send-message', (data) => {
    chatNamespace.emit('new-message', {
      user: data.user,
      message: data.message,
      timestamp: Date.now(),
    });
  });
});

// Admin namespace with middleware
adminNamespace.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (verifyAdminToken(token)) {
    socket.data.isAdmin = true;
    next();
  } else {
    next(new Error('Authentication error'));
  }
});

adminNamespace.on('connection', (socket) => {
  console.log('Admin connected');

  socket.on('get-stats', async () => {
    const stats = await getSystemStats();
    socket.emit('stats', stats);
  });
});

// Notifications namespace
notificationsNamespace.on('connection', (socket) => {
  const userId = socket.handshake.query.userId as string;
  socket.join(`user:${userId}`);

  socket.on('subscribe', (topics: string[]) => {
    topics.forEach((topic) => {
      socket.join(`topic:${topic}`);
    });
  });
});

// Send notification to specific user
function sendNotification(userId: string, notification: Notification): void {
  notificationsNamespace.to(`user:${userId}`).emit('notification', notification);
}

// Send notification to topic subscribers
function broadcastToTopic(topic: string, data: unknown): void {
  notificationsNamespace.to(`topic:${topic}`).emit('topic-update', data);
}

```

### Events & Broadcasting

```typescript
// Custom events with types
interface ChatMessage {
  id: string;
  userId: string;
  content: string;
  timestamp: number;
}

interface UserPresence {
  userId: string;
  status: 'online' | 'away' | 'offline';
  lastSeen: number;
}

// Type-safe event handlers
chatNamespace.on('connection', (socket) => {
  // Emit with type safety
  socket.emit('message', {
    id: '123',
    userId: 'user1',
    content: 'Hello',
    timestamp: Date.now(),
  } as ChatMessage);

  // Listen with type safety
  socket.on('send-message', (message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const fullMessage: ChatMessage = {
      ...message,
      id: generateId(),
      timestamp: Date.now(),
    };

    // Broadcast to all
    chatNamespace.emit('new-message', fullMessage);
  });

  // Broadcast patterns
  socket.on('announce', (data) => {
    // To all connected clients
    io.emit('announcement', data);

    // To all except sender
    socket.broadcast.emit('announcement', data);

    // To specific room
    io.to('general').emit('room-message', data);

    // To all rooms sender is in, except sender
    socket.broadcast.emit('room-update', data);
  });
});

```

### Acknowledgments

```typescript
// Server-side acknowledgments
io.on('connection', (socket) => {
  // Acknowledge message receipt
  socket.on('save-message', async (data, callback) => {
    try {
      const saved = await saveToDatabase(data);
      callback({ success: true, id: saved.id });
    } catch (error) {
      callback({ success: false, error: error.message });
    }
  });

  // Emit with acknowledgment
  socket.emit('important-event', { data: 'critical' }, (response: boolean) => {
    if (response) {
      console.log('Client confirmed receipt');
    }
  });
});

// Client-side acknowledgments
socket.emit(
  'save-message',
  { content: 'Hello' },
  (response: { success: boolean; id?: string; error?: string }) => {
    if (response.success) {
      console.log('Message saved with ID:', response.id);
    } else {
      console.error('Failed to save:', response.error);
    }
  }
);

// Promise-based acknowledgments
function emitWithAck<T>(event: string, data: unknown): Promise<T> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('Acknowledgment timeout'));
    }, 5000);

    socket.emit(event, data, (response: T) => {
      clearTimeout(timeout);
      resolve(response);
    });
  });
}

// Usage
const result = await emitWithAck<{ id: string }>('save-message', { content: 'Hello' });

```

### Reconnection Handling

```typescript
class ResilientSocketClient {
  private socket: Socket;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private eventQueue: Array<{ event: string; data: unknown }> = [];

  constructor(url: string) {
    this.socket = io(url, {
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 30000,
      randomizationFactor: 0.5,
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.socket.on('connect', () => {
      console.log('Connected:', this.socket.id);
      this.reconnectAttempts = 0;
      this.flushEventQueue();
    });

    this.socket.on('disconnect', (reason) => {
      console.log('Disconnected:', reason);
      if (reason === 'io server disconnect') {
        // Server forced disconnect, need to reconnect manually
        this.socket.connect();
      }
    });

    this.socket.on('reconnect_attempt', (attempt) => {
      this.reconnectAttempts = attempt;
      console.log(`Reconnection attempt ${attempt}/${this.maxReconnectAttempts}`);

      // Update transport on each attempt
      if (attempt % 2 === 0) {
        this.socket.io.opts.transports = ['polling', 'websocket'];
      } else {
        this.socket.io.opts.transports = ['websocket', 'polling'];
      }
    });

    this.socket.on('reconnect_failed', () => {
      console.error('Failed to reconnect after max attempts');
      this.handleReconnectFailure();
    });
  }

  // Queue events when disconnected
  send(event: string, data: unknown): void {
    if (this.socket.connected) {
      this.socket.emit(event, data);
    } else {
      this.eventQueue.push({ event, data });
      console.log('Event queued for later delivery');
    }
  }

  private flushEventQueue(): void {
    while (this.eventQueue.length > 0) {
      const { event, data } = this.eventQueue.shift()!;
      this.socket.emit(event, data);
    }
  }

  private handleReconnectFailure(): void {
    // Show user notification
    // Attempt alternative connection methods
    // Log for monitoring
  }
}

```

## Real-World Use Cases

### 1. Real-Time Chat Application

```typescript
// Server: Chat with rooms and direct messages
class ChatServer {
  private userSockets = new Map<string, Set<string>>();
  private typingUsers = new Map<string, Set<string>>();

  initialize(): void {
    io.on('connection', (socket) => {
      const userId = socket.handshake.auth.userId;
      this.userConnected(userId, socket.id);

      socket.on('join-room', (roomId) => this.handleJoinRoom(socket, roomId));
      socket.on('leave-room', (roomId) => this.handleLeaveRoom(socket, roomId));
      socket.on('message', (data) => this.handleMessage(socket, data));
      socket.on('typing', (data) => this.handleTyping(socket, data));
      socket.on('disconnect', () => this.handleDisconnect(userId, socket.id));
    });
  }

  private handleMessage(socket: Socket, data: { roomId: string; content: string }): void {
    const message = {
      id: generateId(),
      userId: socket.handshake.auth.userId,
      roomId: data.roomId,
      content: data.content,
      timestamp: Date.now(),
    };

    // Save to database
    this.saveMessage(message);

    // Broadcast to room
    io.to(data.roomId).emit('new-message', message);
  }

  private handleTyping(socket: Socket, data: { roomId: string; isTyping: boolean }): void {
    const userId = socket.handshake.auth.userId;
    const roomId = data.roomId;

    if (!this.typingUsers.has(roomId)) {
      this.typingUsers.set(roomId, new Set());
    }

    if (data.isTyping) {
      this.typingUsers.get(roomId)!.add(userId);
    } else {
      this.typingUsers.get(roomId)!.delete(userId);
    }

    socket.to(roomId).emit('typing-users', {
      roomId,
      typingUsers: Array.from(this.typingUsers.get(roomId) || []),
    });
  }
}

```

### 2. Collaborative Document Editing

```typescript
// Server: Real-time document collaboration
class DocumentCollaboration {
  private documents = new Map<string, DocumentState>();
  private clientCursors = new Map<string, CursorPosition>();

  initialize(): void {
    io.on('connection', (socket) => {
      socket.on('join-document', (docId) => this.joinDocument(socket, docId));
      socket.on('operation', (data) => this.handleOperation(socket, data));
      socket.on('cursor-move', (data) => this.handleCursorMove(socket, data));
      socket.on('disconnect', () => this.handleDisconnect(socket));
    });
  }

  private handleOperation(socket: Socket, data: OperationData): void {
    const { docId, operation, revision } = data;
    const doc = this.documents.get(docId);

    if (!doc) return;

    // Transform operation against pending operations
    const transformed = this.transformOperation(operation, doc.pendingOps);

    // Apply to document
    this.applyOperation(doc, transformed);

    // Store in history
    doc.pendingOps.push(transformed);
    doc.revision++;

    // Broadcast to other clients in document
    socket.to(docId).emit('operation', {
      operation: transformed,
      revision: doc.revision,
      userId: socket.handshake.auth.userId,
    });
  }

  private transformOperation(op: Operation, pendingOps: Operation[]): Operation {
    return pendingOps.reduce(
      (transformed, pending) => Operation.transform(transformed, pending),
      op
    );
  }
}

```

### 3. Live Auction System

```typescript
// Server: Real-time bidding
class AuctionServer {
  private auctions = new Map<string, Auction>();
  private bidTimers = new Map<string, NodeJS.Timeout>();

  initialize(): void {
    io.on('connection', (socket) => {
      socket.on('join-auction', (auctionId) => this.joinAuction(socket, auctionId));
      socket.on('place-bid', (data) => this.handleBid(socket, data));
      socket.on('disconnect', () => this.handleDisconnect(socket));
    });
  }

  private handleBid(socket: Socket, data: { auctionId: string; amount: number }): void {
    const { auctionId, amount } = data;
    const auction = this.auctions.get(auctionId);

    if (!auction) {
      socket.emit('bid-error', { message: 'Auction not found' });
      return;
    }

    if (amount <= auction.currentBid) {
      socket.emit('bid-error', { message: 'Bid must be higher than current bid' });
      return;
    }

    // Update auction
    auction.currentBid = amount;
    auction.lastBidder = socket.handshake.auth.userId;
    auction.bidHistory.push({
      userId: socket.handshake.auth.userId,
      amount,
      timestamp: Date.now(),
    });

    // Reset timer (extend by 10 seconds)
    this.resetAuctionTimer(auctionId);

    // Broadcast new bid to all participants
    io.to(auctionId).emit('new-bid', {
      auctionId,
      amount,
      bidder: socket.handshake.auth.userId,
      timestamp: Date.now(),
      timeRemaining: auction.endTime - Date.now(),
    });
  }

  private resetAuctionTimer(auctionId: string): void {
    const existing = this.bidTimers.get(auctionId);
    if (existing) clearTimeout(existing);

    this.bidTimers.set(
      auctionId,
      setTimeout(() => this.endAuction(auctionId), 10000) // 10 seconds
    );
  }
}

```

### 4. Multiplayer Game

```typescript
// Server: Game state synchronization
class GameServer {
  private gameRooms = new Map<string, GameRoom>();
  private gameLoops = new Map<string, NodeJS.Timeout>();

  initialize(): void {
    io.on('connection', (socket) => {
      socket.on('create-room', () => this.createRoom(socket));
      socket.on('join-room', (roomId) => this.joinRoom(socket, roomId));
      socket.on('player-action', (data) => this.handlePlayerAction(socket, data));
      socket.on('disconnect', () => this.handleDisconnect(socket));
    });
  }

  private startGameLoop(roomId: string): void {
    const TICK_RATE = 20; // 20 ticks per second
    const TICK_INTERVAL = 1000 / TICK_RATE;

    this.gameLoops.set(
      roomId,
      setInterval(() => {
        const room = this.gameRooms.get(roomId);
        if (!room || room.players.size < 2) return;

        // Update game state
        this.updateGameState(room);

        // Send state to all players
        const state = this.getGameState(room);
        io.to(roomId).emit('game-state', state);
      }, TICK_INTERVAL)
    );
  }

  private handlePlayerAction(socket: Socket, data: PlayerAction): void {
    const room = this.getRoomBySocket(socket.id);
    if (!room) return;

    // Validate action
    if (!this.isValidAction(room, data)) {
      socket.emit('action-error', { message: 'Invalid action' });
      return;
    }

    // Apply action to game state
    this.applyAction(room, data);

    // Broadcast action to other players
    socket.to(room.id).emit('player-action', {
      playerId: socket.handshake.auth.userId,
      action: data,
      timestamp: Date.now(),
    });
  }
}

```

## Common Mistakes

### 1. Not Handling Disconnects

```typescript
// ❌ Bad: No disconnect handling
io.on('connection', (socket) => {
  socket.on('message', (data) => {
    // Process message
  });
});

// ✅ Good: Proper disconnect handling
io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId;

  socket.on('disconnect', (reason) => {
    console.log(`User ${userId} disconnected: ${reason}`);

    // Clean up user data
    this.removeUserFromRooms(userId);

    // Update presence
    this.updatePresence(userId, 'offline');

    // Notify relevant users
    this.notifyFriends(userId, 'offline');
  });
});

```

### 2. Not Validating Data

```typescript
// ❌ Bad: No validation
socket.on('send-message', (data) => {
  // Could crash on malformed data
  const message = JSON.parse(data);
  saveToDatabase(message);
});

// ✅ Good: Schema validation
import { z } from 'zod';

const MessageSchema = z.object({
  roomId: z.string().uuid(),
  content: z.string().min(1).max(1000),
  type: z.enum(['text', 'image', 'file']),
});

socket.on('send-message', (data, callback) => {
  try {
    const validated = MessageSchema.parse(data);
    const message = saveToDatabase(validated);
    callback({ success: true, id: message.id });
  } catch (error) {
    callback({ success: false, error: error.message });
  }
});

```

### 3. Memory Leaks

```typescript
// ❌ Bad: Not cleaning up listeners
io.on('connection', (socket) => {
  const handler = (data) => {
    // This creates a closure that may leak
    processLargeData(data);
  };

  socket.on('data', handler);

  // No cleanup on disconnect
});

// ✅ Good: Cleanup listeners
io.on('connection', (socket) => {
  const handler = (data) => {
    processLargeData(data);
  };

  socket.on('data', handler);

  socket.on('disconnect', () => {
    socket.off('data', handler);
    // Clean up any other resources
  });
});

```

### 4. Not Using Rooms Properly

```typescript
// ❌ Bad: Broadcasting to all
socket.on('send-message', (data) => {
  io.emit('new-message', data); // Everyone receives it
});

// ✅ Good: Using rooms for scoped broadcasting
socket.on('send-message', (data) => {
  io.to(data.roomId).emit('new-message', {
    ...data,
    sender: socket.id,
  });
});

```

### 5. Missing Error Handling

```typescript
// ❌ Bad: No error handling
socket.on('save-data', async (data) => {
  await database.save(data); // Could throw
});

// ✅ Good: Comprehensive error handling
socket.on('save-data', async (data, callback) => {
  try {
    const validated = validateData(data);
    const saved = await database.save(validated);
    callback({ success: true, id: saved.id });
  } catch (error) {
    console.error('Save failed:', error);
    callback({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

```

## Best Practices

### 1. Authentication

```typescript
// Middleware for authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (!token) {
    return next(new Error('Authentication required'));
  }

  try {
    const user = verifyToken(token);
    socket.data.user = user;
    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
});

// Protected namespace
const adminNamespace = io.of('/admin');

adminNamespace.use((socket, next) => {
  if (socket.data.user?.role !== 'admin') {
    return next(new Error('Unauthorized'));
  }
  next();
});

```

### 2. Rate Limiting

```typescript
class RateLimiter {
  private limits = new Map<string, { count: number; resetAt: number }>();

  isAllowed(socketId: string, limit: number, windowMs: number): boolean {
    const now = Date.now();
    const record = this.limits.get(socketId);

    if (!record || now > record.resetAt) {
      this.limits.set(socketId, { count: 1, resetAt: now + windowMs });
      return true;
    }

    if (record.count >= limit) {
      return false;
    }

    record.count++;
    return true;
  }
}

const limiter = new RateLimiter();

io.use((socket, next) => {
  if (!limiter.isAllowed(socket.id, 100, 60000)) {
    return next(new Error('Rate limit exceeded'));
  }
  next();
});

```

### 3. Graceful Shutdown

```typescript
// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');

  // Stop accepting new connections
  io.close(() => {
    console.log('All connections closed');
    process.exit(0);
  });

  // Force close after timeout
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
});

```

### 4. Monitoring & Logging

```typescript
// Connection metrics
io.engine.on('connection', (socket) => {
  metrics.increment('websocket.connections');
  metrics.gauge('websocket.total', io.engine.clientsCount);
});

io.engine.on('connection', (socket) => {
  socket.on('disconnect', () => {
    metrics.decrement('websocket.connections');
  });
});

// Message metrics
io.use((socket, next) => {
  const originalEmit = socket.emit;
  socket.emit = function (event, ...args) {
    metrics.increment(`websocket.messages.${event}`);
    return originalEmit.call(this, event, ...args);
  };
  next();
});

```

### 5. Security

```typescript
// Input sanitization
function sanitizeInput(data: unknown): unknown {
  if (typeof data === 'string') {
    return data
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }
  return data;
}

// CORS configuration
const io = new Server(httpServer, {
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
    methods: ['GET', 'POST'],
    credentials: true,
  },
});

// Max payload size
const io = new Server(httpServer, {
  maxHttpBufferSize: 1e6, // 1MB
});

```

## Summary

Socket.io simplifies real-time communication with:

- **Automatic fallback**: WebSocket → HTTP Long Polling
- **Rooms & Namespaces**: Scoped communication channels
- **Acknowledgments**: Built-in message confirmation
- **Reconnection**: Automatic retry with backoff
- **Middleware**: Authentication and validation
- **Binary support**: Automatic binary detection

Key best practices:

- Always authenticate connections
- Validate all incoming data
- Use rooms for scoped broadcasting
- Handle disconnects gracefully
- Monitor and log connection metrics
- Implement rate limiting

---

## Cheat Sheet
```text
SOCKET.IO CHEAT SHEET
============================================================

TRANSPORT FALLBACK ORDER:
  1. WebSocket (fastest, full-duplex)
  2. HTTP Long Polling (universal compatibility)
  3. HTTP Streaming (legacy fallback)
  Result: best available transport selected automatically

KEY CONCEPTS:
  • Rooms:   subset of sockets, broadcast via .to(roomId)
  • Namespaces: separate connection multiplex (/chat, /admin)
  • ACKs:    callback in emit for delivery confirmation
  • Middleware: io.use((socket, next) => { ... })

RECONNECTION:
  • reconnectionAttempts: 5 (default Infinity)
  • reconnectionDelay: 1000ms initial
  • reconnectionDelayMax: 5000ms cap
  • randomizationFactor: 0.5 (jitter to avoid thundering herd)
  • 'io server disconnect' requires manual socket.connect()

SCALING WITH REDIS ADAPTER:
  • io.adapter(createAdapter(redis, redisSub))
  • Cross-node broadcast: io.emit works across all nodes
  • Sticky sessions still required at LB for WebSocket upgrade
  • Use perMessageDeflate for compression

INTERVIEW TIPS:
  • Explain transport upgrade from polling -> WebSocket
  • Show how to scale Socket.io horizontally with Redis
  • Know the difference between socket.broadcast and io.emit
  • Discuss typed events with TypeScript generics
  • Mention perMessageDeflate and binary frame support
```
---

## See Also
- [NestJS](../06-NestJS/)
- [Observability](../22-Observability/)
- [System Design](../11-System-Design/)

## References & Learn More

- [Socket.io Official Documentation](https://socket.io/docs/v4/)
- [Socket.io GitHub Repository](https://github.com/socketio/socket.io)
- [Socket.io Client API](https://socket.io/docs/v4/client-api/)
- [Socket.io Server API](https://socket.io/docs/v4/server-api/)
- [Socket.io Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
- [Socket.io Rooms and Namespaces](https://socket.io/docs/v4/rooms/)
