# WhatsApp System Design

## Requirements
### Functional Requirements

- 1:1 text messaging between users
- Group messaging (up to 1024 members)
- Media sharing (images, videos, documents)
- Online/offline presence indicators
- Read receipts (blue ticks)
- End-to-end encryption for messages
- Push notifications for offline users
- Message search functionality
- Voice and video calls (simplified)
- User profile management

### Non-Functional Requirements

- Low latency message delivery (< 100ms)
- High availability (99.99%)
- Message ordering guaranteed
- Exactly-once delivery
- Support 500M daily active users
- Handle 100B messages per day
- Messages persist until deleted
- End-to-end encryption for privacy

## Capacity Estimation

```text
Storage Estimates:

- 500M DAU × 40 messages/day = 20B messages/day
- Average message: 100 bytes
- Daily storage: 20B × 100 bytes = 2 TB/day
- Yearly storage: 2 TB × 365 = 730 TB
- Media storage: 10x messages = 7.3 PB/year

Bandwidth Estimates:

- Messages: 20B × 100 bytes = 2 TB/day = ~23 MB/s
- Media: 7.3 PB/day = ~84.5 GB/s (peak: 5x)
- Total: ~425 GB/s peak bandwidth

Connection Estimates:

- 500M DAU, 30% online = 150M concurrent connections
- WebSocket memory: 150M × 10 KB = 1.5 TB RAM
- Need 1500+ WebSocket servers (100K connections each)

```

## API Design

```yaml
# Authentication
POST /api/v1/auth/login
  Request:
    { "phone": "+1234567890", "otp": "123456" }
  Response:
    { "user_id": "usr_123", "token": "jwt_token" }

# Messaging
POST /api/v1/messages
  Request:
    {
      "conversation_id": "conv_456",
      "content": "Hello!",
      "type": "text",
      "media_url": null
    }
  Response:
    {
      "message_id": "msg_789",
      "timestamp": "2025-01-15T10:30:00Z",
      "status": "sent"
    }

GET /api/v1/messages/{conversation_id}?limit=50&before=msg_789
  Response:
    {
      "messages": [...],
      "has_more": true,
      "cursor": "msg_100"
    }

# Presence
PUT /api/v1/presence
  Request: { "status": "online", "last_seen": "2025-01-15T10:30:00Z" }

# Groups
POST /api/v1/groups
  Request:
    {
      "name": "Project Team",
      "members": ["usr_123", "usr_456"],
      " admins": ["usr_123"]
    }
  Response: { "group_id": "grp_001", "created_at": "..." }

```

## Database Design
### Schema

```sql
-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    profile_picture_url TEXT,
    about TEXT,
    last_seen TIMESTAMP,
    is_online BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(10) NOT NULL, -- 'direct' or 'group'
    name VARCHAR(255),        -- group name
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table (partitioned by conversation)
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL,
    sender_id BIGINT NOT NULL,
    content TEXT,
    type VARCHAR(20) NOT NULL, -- 'text', 'image', 'video', 'document'
    media_url TEXT,
    encryption_key TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
) PARTITION BY HASH (conversation_id);

-- Create 16 partitions
CREATE TABLE messages_p0 PARTITION OF messages FOR VALUES WITH (MODULUS 16, REMAINDER 0);
CREATE TABLE messages_p1 PARTITION OF messages FOR VALUES WITH (MODULUS 16, REMAINDER 1);
-- ... etc

-- Conversation participants
CREATE TABLE conversation_participants (
    conversation_id BIGINT REFERENCES conversations(id),
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member', -- 'admin', 'member'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_message_id BIGINT,
    muted BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (conversation_id, user_id)
);

-- Message status (delivery and read receipts)
CREATE TABLE message_status (
    message_id BIGINT REFERENCES messages(id),
    user_id BIGINT REFERENCES users(id),
    status VARCHAR(20) NOT NULL, -- 'sent', 'delivered', 'read'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (message_id, user_id)
);

-- Indexes
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_conversation_participants_user ON conversation_participants(user_id);

```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌────────────────────────┐     ┌─────────────────┐
│    users    │     │    conversations       │     │    messages     │
├─────────────┤     ├────────────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ created_by (FK)        │     │ id (PK)         │
│ phone       │     │ id (PK)                │◄────│ conversation_id │
│ name        │     │ type                   │     │ sender_id (FK)  │
│ profile_url │     │ name                   │     │ content         │
│ about       │     │ created_at             │     │ type            │
│ last_seen   │     │ updated_at             │     │ media_url       │
│ is_online   │     └────────────────────────┘     │ encryption_key  │
└─────────────┘              │                      │ created_at      │
        ▲                    │                      │ is_deleted      │
        │                    ▼                      └─────────────────┘
        │     ┌────────────────────────┐                 ▲
        │     │conversation_participants│                 │
        │     ├────────────────────────┤                 │
        └─────│ user_id (FK)           │                 │
              │ conversation_id (FK)   │                 │
              │ role                   │                 │
              │ last_read_message_id   │─────────────────┘
              │ muted                  │
              └────────────────────────┘
                              ▲
                              │
              ┌────────────────────────┐
              │    message_status      │
              ├────────────────────────┤
              │ message_id (FK)        │
              │ user_id (FK)           │
              │ status                 │
              │ updated_at             │
              └────────────────────────┘

```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                        Mobile Clients                            │
│                    (iOS, Android, Web)                           │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway/LB      │
                    │   (Rate Limiting,     │
                    │    SSL Termination)   │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  WebSocket      │  │  REST API       │  │  Push Notification│
│  Servers        │  │  Servers        │  │  Service          │
│  (1500+)        │  │  (50+)          │  │  (FCM/APNs)       │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Message Queue   │
                    │   (Kafka Cluster) │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │  Message    │ │  Media      │ │  Analytics  │
     │  Service    │ │  Service    │ │  Service    │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │               │               │
            ▼               ▼               ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │  Cassandra  │ │  S3/CDN     │ │  ClickHouse │
     │  Cluster    │ │             │ │             │
     └─────────────┘ └─────────────┘ └─────────────┘

```

## Key Components

### WebSocket Connection Manager

```python
import asyncio
import websockets
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        # user_id -> set of (websocket, device_type) tuples
        self.connections: Dict[str, Set] = {}
        self.redis = None

    async def connect(self, websocket, user_id: str, device_type: str):
        if user_id not in self.connections:
            self.connections[user_id] = set()

        self.connections[user_id].add((websocket, device_type))

        # Update presence in Redis
        await self.redis.hset(f"presence:{user_id}", device_type, "online")
        await self.redis.expire(f"presence:{user_id}", 300)  # 5 min TTL

        # Notify contacts about online status
        await self.broadcast_presence(user_id, "online")

    async def disconnect(self, websocket, user_id: str, device_type: str):
        if user_id in self.connections:
            self.connections[user_id].discard((websocket, device_type))

            if not self.connections[user_id]:
                del self.connections[user_id]
                await self.redis.hdel(f"presence:{user_id}", device_type)
                await self.broadcast_presence(user_id, "offline")

    async def send_to_user(self, user_id: str, message: dict):
        if user_id not in self.connections:
            return False

        for ws, device_type in self.connections[user_id]:
            try:
                await ws.send(json.dumps(message))
            except websockets.ConnectionClosed:
                await self.disconnect(ws, user_id, device_type)

        return True

    async def broadcast_presence(self, user_id: str, status: str):
        contacts = await self.get_contacts(user_id)
        for contact_id in contacts:
            await self.send_to_user(contact_id, {
                "type": "presence",
                "user_id": user_id,
                "status": status
            })

```

### Message Queue Producer

```python
from kafka import KafkaProducer
import json
import uuid

class MessageProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Ensure message durability
            retries=3
        )

    async def send_message(self, message: dict):
        # Generate unique message ID for exactly-once semantics
        message_id = str(uuid.uuid4())
        message['id'] = message_id

        # Determine partition based on conversation_id for ordering
        partition_key = str(message['conversation_id']).encode()

        self.producer.send(
            topic='messages',
            key=partition_key,
            value=message,
            callback=self.on_send_success
        )

        return message_id

    def on_send_success(self, record_metadata):
        print(f"Message sent to {record_metadata.topic} "
              f"partition {record_metadata.partition} "
              f"offset {record_metadata.offset}")

```

### Encryption Service

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EncryptionService:
    def __init__(self):
        self.key_registry = {}  # In production, use secure key management

    def generate_conversation_key(self, conversation_id: str) -> bytes:
        # Generate unique key for each conversation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=conversation_id.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(conversation_id.encode())
        )
        self.key_registry[conversation_id] = key
        return key

    def encrypt_message(self, message: str, conversation_id: str) -> str:
        key = self.key_registry.get(conversation_id)
        if not key:
            key = self.generate_conversation_key(conversation_id)

        f = Fernet(key)
        encrypted = f.encrypt(message.encode())
        return encrypted.decode()

    def decrypt_message(self, encrypted_message: str,
                       conversation_id: str) -> str:
        key = self.key_registry.get(conversation_id)
        if not key:
            raise ValueError("Encryption key not found")

        f = Fernet(key)
        decrypted = f.decrypt(encrypted_message.encode())
        return decrypted.decode()

```

### Message Delivery Service

```python
class MessageDeliveryService:
    def __init__(self, connection_manager, db, notification_service):
        self.connections = connection_manager
        self.db = db
        self.notifications = notification_service

    async def deliver_message(self, message: dict):
        conversation_id = message['conversation_id']
        sender_id = message['sender_id']

        # Get all participants in conversation
        participants = await self.db.get_participants(conversation_id)

        for participant_id in participants:
            if participant_id == sender_id:
                continue

            # Try online delivery first
            delivered = await self.connections.send_to_user(
                participant_id,
                {
                    "type": "message",
                    "message": message
                }
            )

            if delivered:
                # Update status to delivered
                await self.db.update_message_status(
                    message['id'], participant_id, 'delivered'
                )
            else:
                # User offline, queue for push notification
                await self.notifications.send_push(
                    participant_id,
                    message
                )
                # Store in offline message queue
                await self.db.queue_offline_message(
                    participant_id, message
                )

```

## Caching Strategy (Redis)

### Presence Cache

```python
class PresenceCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def set_online(self, user_id: str, device_type: str):
        await self.redis.hset(f"presence:{user_id}", device_type, "1")
        await self.redis.expire(f"presence:{user_id}", 300)

    async def set_offline(self, user_id: str, device_type: str):
        await self.redis.hdel(f"presence:{user_id}", device_type)
        if await self.redis.hlen(f"presence:{user_id}") == 0:
            await self.redis.delete(f"presence:{user_id}")

    async def is_online(self, user_id: str) -> bool:
        return await self.redis.exists(f"presence:{user_id}")

    async def get_last_seen(self, user_id: str) -> str:
        return await self.redis.get(f"last_seen:{user_id}")

```

### Message Cache

```python
class MessageCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_cached_messages = 100

    async def cache_conversation(self, conversation_id: str,
                                 messages: list):
        key = f"conversation:{conversation_id}"
        await self.redis.delete(key)

        for msg in messages[:self.max_cached_messages]:
            await self.redis.rpush(key, json.dumps(msg))

        await self.redis.expire(key, 3600)  # 1 hour

    async def get_cached_messages(self, conversation_id: str,
                                  limit: int = 50) -> list:
        key = f"conversation:{conversation_id}"
        messages = await self.redis.lrange(key, -limit, -1)
        return [json.loads(msg) for msg in messages]

```

## Message Queue (Kafka)

### Topic Architecture

```text
Topics:
├── messages.new           (incoming messages)
├── messages.delivered     (delivery confirmations)
├── messages.read          (read receipts)
├── presence.updates       (online/offline status)
├── media.upload           (media processing events)
└── notifications.push     (push notification requests)

Partitioning Strategy:

- messages.new: partition by conversation_id (ordering)
- presence.updates: partition by user_id
- media.upload: partition by media_type

```

### Consumer Groups

```python
class MessageConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'messages.new',
            bootstrap_servers=['kafka1:9092'],
            group_id='message-delivery-service',
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )

    async def consume_messages(self):
        for message in self.consumer:
            try:
                await self.process_message(message.value)
                self.consumer.commit()
            except Exception as e:
                # Log error, don't commit (will retry)
                logger.error(f"Failed to process message: {e}")

    async def process_message(self, message: dict):
        # 1. Store in database
        await self.db.store_message(message)

        # 2. Deliver to online users
        await self.delivery_service.deliver_message(message)

        # 3. Update conversation metadata
        await self.db.update_conversation(
            message['conversation_id'],
            message['created_at']
        )

```

## Scaling Strategy

### Connection Scaling

```text
WebSocket Server Cluster:
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (L4)                    │
│              (IP Hash for sticky connections)            │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  WS Server   │   │  WS Server   │   │  WS Server   │
│  (100K conn) │   │  (100K conn) │   │  (100K conn) │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴───────┐
                    │  Redis Cluster │
                    │ (Connection    │
                    │  Mapping)      │
                    └───────────────┘

```

### Database Scaling

```python
class ShardRouter:
    def __init__(self, num_shards: int = 16):
        self.num_shards = num_shards

    def get_shard(self, conversation_id: int) -> int:
        return conversation_id % self.num_shards

    def get_user_shard(self, user_id: int) -> int:
        # Different sharding for user data
        return (user_id * 7) % self.num_shards

```

### Geographic Distribution

```text
Global Deployment:
┌─────────────────────────────────────────────────────────┐
│                    Global CDN                           │
└─────────────────────────────────────────────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  US Region   │   │  EU Region   │   │  APAC Region │
│  ──────────  │   │  ──────────  │   │  ──────────  │
│  WS Servers  │   │  WS Servers  │   │  WS Servers  │
│  DB Shards   │   │  DB Shards   │   │  DB Shards   │
│  Redis       │   │  Redis       │   │  Redis       │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴───────┐
                    │  Kafka Mirror  │
                    │  (Cross-DC)    │
                    └───────────────┘

```

## Failure Handling

### Message Delivery Guarantees

```python
class ReliableDelivery:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [1, 5, 15]  # seconds

    async def deliver_with_retry(self, message: dict,
                                 recipient_id: str):
        for attempt in range(self.max_retries):
            try:
                success = await self.send_message(
                    message, recipient_id
                )
                if success:
                    return True

                # Exponential backoff
                await asyncio.sleep(
                    self.retry_delays[attempt]
                )
            except Exception as e:
                logger.error(
                    f"Delivery attempt {attempt} failed: {e}"
                )

        # All attempts failed, queue for later delivery
        await self.queue_for_later(message, recipient_id)
        return False

```

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| WebSocket server crash | Client auto-reconnects, message queue preserves order |
| Kafka broker failure | Replication factor 3, ISR required |
| Database node failure | Automatic failover to replica |
| Redis failure | Fall back to database for presence |
| Network partition | Store messages locally, sync when reconnected |

### Offline Message Handling

```python
class OfflineMessageHandler:
    def __init__(self, db, notification_service):
        self.db = db
        self.notifications = notification_service

    async def handle_offline_user(self, user_id: str,
                                  message: dict):
        # Store in offline queue
        await self.db.store_offline_message(user_id, message)

        # Send push notification (one per conversation)
        await self.notifications.send_push_notification(
            user_id,
            {
                "title": "New message",
                "body": message['content'][:50],
                "data": {
                    "conversation_id": message['conversation_id'],
                    "message_id": message['id']
                }
            }
        )

    async def sync_offline_messages(self, user_id: str):
        messages = await self.db.get_offline_messages(user_id)
        for message in messages:
            await self.send_message(user_id, message)
            await self.db.mark_message_synced(message['id'])

```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - messages_per_second
  - active_users_by_region
  - delivery_success_rate
  - average_delivery_latency

System Metrics:

  - websocket_connections
  - kafka_consumer_lag
  - database_query_latency
  - redis_hit_ratio
  - error_rate_by_type

Infrastructure Metrics:

  - cpu_usage_per_server
  - memory_usage_per_server
  - network_throughput
  - disk_io_latency

```

### Alerting

```yaml
alerts:

  - name: High Delivery Latency
    condition: p99_latency > 500ms
    severity: critical

  - name: Message Queue Backlog
    condition: kafka_lag > 100000
    severity: warning

  - name: Connection Drop Rate
    condition: connection_drops > 5% per minute
    severity: warning

  - name: Database Replication Lag
    condition: replication_lag > 1s
    severity: critical

```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | Cassandra (write-heavy) | PostgreSQL (ACID) | Cassandra for messages |
| Real-time | WebSockets (persistent) | Long-polling (simpler) | WebSockets for UX |
| Encryption | E2E (secure, complex) | Server-side (simple, less secure) | E2E (WhatsApp-style) |
| Ordering | Per-conversation | Global | Per-conversation |
| Delivery | At-most-once | At-least-once | At-least-once |

## Interview Questions

### Design Questions

1. **How would you handle message ordering?**

   - Partition Kafka topics by conversation_id
   - Use sequence numbers per conversation
   - Client-side deduplication
   - Server-side ordering guarantees per partition

2. **How do you implement read receipts?**

   - Track last_read_message_id per user per conversation
   - Async update via Kafka
   - Batch updates to reduce write amplification
   - Client shows "delivered" vs "read" based on status

3. **How would you handle group messaging?**

   - Store group membership in separate table
   - Fan-out on write for small groups (< 100)
   - Fan-out on read for large groups (> 100)
   - Separate notification logic for group mentions

### Scaling Questions

4. **How do you scale to 500M DAU?**

   - Geographic sharding with data residency
   - WebSocket connection pooling
   - Read replicas for message queries
   - CDN for media delivery

5. **How do you handle viral group messages?**

   - Rate limit message sending
   - Implement message queue backpressure
   - Cache hot conversations
   - Use fan-out on read for large groups

### Trade-off Questions

6. **How do you balance encryption with features?**

   - E2E encryption for messages
   - Server can see metadata (sender, timestamp)
   - Search requires client-side indexing
   - Backup requires key escrow

7. **How do you handle message deletion?**

   - Soft delete with tombstone messages
   - Propagate deletion to all devices
   - Remove from caches and backups
   - Legal retention requirements

### Senior-level Questions

8. **How would you implement voice/video calls?**

   - WebRTC for peer-to-peer media
   - Signaling server via WebSocket
   - TURN servers for NAT traversal
   - SFU for group calls

9. **How do you prevent spam and abuse?**

   - Rate limiting per user
   - Message content analysis
   - Report and block functionality
   - Phone number verification

10. **How would you implement message search?**

    - Client-side encrypted search
    - Server-side metadata search
    - Elasticsearch for message content
    - Respect E2E encryption boundaries

## Summary

The WhatsApp system design covers:

- **Real-time Communication**: WebSocket-based messaging
- **Scalability**: Geographic sharding, connection pooling
- **Security**: End-to-end encryption, secure key management
- **Reliability**: Exactly-once delivery, offline message queue
- **Performance**: Multi-level caching, message ordering

Key takeaways:

1. Use WebSocket with connection pooling for real-time

2. Implement E2E encryption with proper key management

3. Partition by conversation_id for ordering guarantees

4. Handle offline users with push notifications and message queue

5. Scale geographically with data residency compliance

This design handles 500M DAU with 100B messages/day while maintaining < 100ms delivery latency.

---

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
