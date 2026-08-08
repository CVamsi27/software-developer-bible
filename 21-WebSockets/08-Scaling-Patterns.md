---
section: WebSockets
category: Real-Time
tags: [concept, guide, reference]
---

# Scaling WebSockets

## Definition

A single WebSocket server hits its connection ceiling at roughly 10,000-50,000 concurrent connections (depending on memory, file descriptors, and CPU). To support more, you need to scale **horizontally** across multiple nodes. But WebSocket connections are stateful (the socket lives on one node), so load balancing requires strategies that preserve the session, and cross-node messaging requires a shared pub/sub layer.

Scaling WebSockets is fundamentally a stateful load-balancing problem combined with a pub/sub fanout problem.

## Why Do We Need It?

1. **Connection limits**: A single Node.js process caps at ~10K WebSockets (event loop + memory).
2. **High availability**: One node crash = all its connections drop. Multi-node + reconnection mitigates.
3. **Geographic distribution**: Route users to the nearest region for lower latency.
4. **Burst handling**: A 10x traffic spike (viral moment) requires elastic scale-out, not vertical scale-up.

## How It Works

### The Core Problem

```text
Without scaling:
Client A ─┐
Client B ─┼──▶ WebSocket Server (1 node, 10K cap)
Client C ─┘   - state in-memory
              - if node dies, all clients disconnect

With scaling:
Client A ─┐
Client B ─┼──▶ Load Balancer ──┬──▶ WS Node 1 (clients: A, D)
Client C ─┤                   ├──▶ WS Node 2 (clients: B, E)
Client D ─┤                   └──▶ WS Node 3 (clients: C, F)
Client E ─┘                          │
Client F ─┐                          ▼
         (Reconnect to                 ┌────────────────┐
          another node)                 │ Redis Pub/Sub │
         (or same via                   │ (cross-node   │
          sticky session)               │  fanout)      │
                                        └────────────────┘
```

### Two Problems to Solve

1. **Connection routing**: How does a client land on the same node every reconnect? → **Sticky sessions**
2. **Cross-node messaging**: How does Node 1 send a message to a client connected to Node 2? → **Shared pub/sub**

## Scaling Strategies

### 1. Sticky Sessions (Connection Affinity)

The load balancer routes a client to a specific backend node based on a hash of session ID, IP, or a cookie. The client always reconnects to the same node.

```text
AWS ALB:
  - Stickiness: enabled, duration 1 day
  - Cookie: AWSALBAPP-0

Nginx:
  upstream backend {
    hash $cookie_session_id consistent;
    server ws1.example.com:8080;
    server ws2.example.com:8080;
  }
```

**Pros**: Simple, stateful sessions work without cross-node sync.
**Cons**: Uneven load (hot users on one node), node failure = client reconnect.

### 2. Redis Pub/Sub Adapter (Cross-Node Fanout)

The canonical pattern: each WS node subscribes to Redis pub/sub. When Node 1 wants to broadcast, it publishes to Redis; all nodes receive and deliver to their local clients.

```typescript
// Socket.io with Redis adapter
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const io = new Server(httpServer);
const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));

// io.emit() now works across all nodes
io.to('room:42').emit('message', { text: 'Hello' });
```

**Pros**: No sticky sessions needed, even load.
**Cons**: Redis is a single point of failure; pub/sub is fire-and-forget (no replay).

### 3. Sharded Sockets (Hash by User)

Each user is assigned to a specific node via `hash(userId) % nodeCount`. Broadcasts query the right node.

```typescript
class ShardedSocketManager {
  private nodes = new Map<string, WebSocketServer>();
  private userShards = new Map<string, string>(); // userId -> nodeId

  getNodeForUser(userId: string): WebSocketServer {
    const hash = parseInt(createHash('md5').update(userId).digest('hex').slice(0, 8), 16);
    const nodeId = `node-${hash % this.nodes.size}`;
    return this.nodes.get(nodeId)!;
  }

  // To send to all users, iterate all nodes
  broadcast(event: string, data: unknown): void {
    this.nodes.forEach((server) => {
      server.emit(event, data);
    });
  }
}
```

**Pros**: Predictable routing, no Redis needed for direct messaging.
**Cons**: Broadcasts require touching every node; rebalancing is hard.

### 4. Sticky + Pub/Sub (Most Common)

Production setup: **Sticky sessions for connection affinity** + **Redis pub/sub for broadcasts**. This is what Socket.io, NestJS WebSockets, and most production deployments use.

```text
Client → ALB (sticky by cookie) → WS Node (reconnect lands on same node)
WS Node 1 → Redis Pub/Sub ──┐
WS Node 2 → Redis Pub/Sub ──┼── broadcast reaches all nodes
WS Node 3 → Redis Pub/Sub ──┘
```

### 5. Serverless / Edge (Cloudflare Durable Objects, etc.)

Hand off the WebSocket state to an edge platform. Each "room" or "user" becomes a Durable Object. No infra to manage.

```typescript
// Cloudflare Durable Object (WebSocket hibernation API)
export class ChatRoom implements DurableObject {
  state: DurableObjectState;
  sessions: WebSocket[] = [];

  async fetch(request: Request): Promise<Response> {
    const pair = new WebSocketPair();
    this.sessions.push(pair[0]);
    pair[0].accept();
    pair[0].addEventListener('message', (msg) => {
      this.sessions.forEach((s) => s.send(msg.data));
    });
    return new Response(null, { status: 101, webSocket: pair[1] });
  }
}
```

**Pros**: No ops, scales to zero, global low latency.
**Cons**: Vendor lock-in, hibernation limits, cost at scale.

## Code Examples

### Nginx Sticky Load Balancing

```nginx
upstream websocket_backend {
    # Sticky by client IP
    ip_hash;
    server ws1.internal:8080;
    server ws2.internal:8080;
    server ws3.internal:8080;
}

server {
    listen 443 ssl;
    server_name ws.example.com;

    # WebSocket upgrade
    location / {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;  # 24h
    }
}
```

### Health Checks for WebSocket Nodes

```typescript
// Express health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    connections: io.engine.clientsCount,
    uptime: process.uptime(),
    nodeId: process.env.NODE_ID,
  });
});

// ALB checks this every 30s
```

### Graceful Shutdown

```typescript
process.on('SIGTERM', async () => {
  console.log('Shutting down...');

  // Stop accepting new connections
  io.close(async () => {
    // Drain existing connections
    io.engine.clientsCount === 0
      ? process.exit(0)
      : setTimeout(() => process.exit(0), 30000); // 30s drain
  });
});
```

## Real-World Use Cases

### 1. Slack-Scale Chat (Billions of Messages)

Slack uses a sharded architecture where each channel/team is hosted on specific nodes. Cross-channel messages route through Kafka. WebSocket fanout is per-node.

### 2. Trading Platform (Sub-10ms Latency)

Direct connection (no LB) to a single co-located node. Vertical scaling (more RAM/CPU) beats horizontal scale when latency matters more than throughput.

### 3. Multiplayer Game (1M+ Concurrent)

Sharded by region + game session. Use Cloudflare Durable Objects or a custom sharded architecture. Edge termination at the CDN.

## Common Mistakes

### 1. Using Round-Robin Load Balancing

```text
❌ Bad: round-robin across WebSocket nodes — connection lands on a different node each reconnect
✅ Good: sticky session (cookie, IP hash, or session ID)
```

### 2. Storing Session State In-Memory

```typescript
// ❌ Bad: in-memory session
const userSessions = new Map<string, Session>();  // lost on node restart

// ✅ Good: in Redis
await redis.hset(`session:${userId}`, JSON.stringify(session));
```

### 3. No Graceful Shutdown

Killing a node drops all its connections. ALB takes the node out of rotation, but in-flight messages are lost. Implement drain: stop accepting, send close frame, wait for clients to reconnect.

### 4. Forgetting Heartbeats in Horizontal Setup

Idle connections can be killed by NAT timeouts. Each node must send heartbeats and detect zombie connections independently.

## Best Practices

1. **Use sticky sessions** for connection affinity (ALB, Nginx, Envoy)
2. **Add Redis adapter** for cross-node pub/sub
3. **Implement health endpoints** that report connection count and uptime
4. **Graceful shutdown** with 30s drain
5. **Heartbeat every 30s** with 10s timeout
6. **Monitor per-node** connection counts for uneven load
7. **Use Server-Sent Events for read-only** paths to reduce WS count
8. **Consider edge platforms** (Cloudflare DO, Durable Objects) for greenfield
9. **Cap max connections per node** (e.g., 80% of file descriptors)
10. **Plan for reconnection** with exponential backoff on the client

## Performance Considerations

| Strategy | Latency | Throughput | Complexity | Best For |
|----------|---------|------------|------------|----------|
| Single node (vertical) | Best | Limited | Low | < 10K connections |
| Sticky + Pub/Sub | Good | High | Medium | Most production |
| Sharded by user | Good | Very High | High | Predictable routing |
| Serverless/Edge | Variable | High | Low (managed) | Variable scale |
| Multi-region | Best for users | Very High | Very High | Global apps |

### Capacity Planning

Per 10K WebSocket connections (Node.js):
- Memory: ~100-200 MB (state, buffers)
- File descriptors: 10K + overhead
- CPU: minimal at idle, scales with message rate
- Network: depends on message size and frequency

## Summary

- A single WS node caps at ~10-50K connections
- Two problems: connection routing (sticky sessions) + cross-node messaging (pub/sub)
- Production pattern: ALB sticky + Redis adapter (Socket.io / NestJS)
- Edge platforms (Cloudflare Durable Objects) remove infra overhead
- Plan for graceful shutdown, heartbeats, and reconnection
- Capacity plan: 100-200 MB per 10K connections

---

## Cheat Sheet
```text
SCALING WEBSOCKETS CHEAT SHEET
============================================================

CAPACITY (single Node.js node):
  • ~10K-50K concurrent connections
  • ~100-200 MB RAM per 10K connections
  • file descriptor limit (ulimit -n)
  • CPU scales with msg rate, not connection count

PATTERNS:
  • Sticky sessions: ALB cookie / Nginx ip_hash
  • Redis adapter: cross-node pub/sub (Socket.io, NestJS)
  • Sharded by user: hash(userId) % N
  • Edge: Cloudflare Durable Objects

LOAD BALANCER HEADERS:
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  proxy_read_timeout 86400;  # prevent idle timeout

RECONNECTION:
  • Exponential backoff: min(1000 * 2^n, 30000) ms
  • Add jitter: ±20% to avoid thundering herd
  • Server side: emit `welcome` with last-seen event ID

GRACEFUL SHUTDOWN:
  • SIGTERM -> stop accepting
  • Send close frame to clients
  • Wait 30s for reconnect to land on other nodes
  • Exit cleanly

INTERVIEW TIPS:
  • Draw the architecture: LB -> WS nodes -> Redis
  • Explain why sticky sessions + pub/sub
  • Discuss trade-off: edge platforms vs self-hosted
  • Know the reconnection protocol (backoff + jitter)
```
---

## See Also
- [NestJS](../06-NestJS/)
- [Observability](../22-Observability/)
- [Real-Time Architecture](04-Real-Time-Architecture.md)
- [System Design](../11-System-Design/)
- [WebSockets Overview](01-WebSockets-Overview.md)
- [WebTransport](07-WebTransport.md)

## References & Learn More

- [Socket.io Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
- [Nginx WebSocket Upgrade](https://nginx.org/en/docs/http/websocket.html)
- [AWS ALB Sticky Sessions](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html)
- [Cloudflare Durable Objects WebSockets](https://developers.cloudflare.com/durable-objects/best-practices/websockets/)
- [Designing Data-Intensive Applications - Ch. 5 (Replication)](https://dataintensive.net/)
