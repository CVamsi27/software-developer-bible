# Chat System Design

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

 messaging (up to 10,000 members)
- Media sharing (images, videos, files, voice messages)
- Read receipts and delivery status
- Online/offline presence indicators
- Typing indicators
- Push notifications for offline users
- Message search across conversations
- Message reactions (emoji)
- Message editing and deletion
- End-to-end encryption for private conversations
- Message history with infinite scroll

### Non-Functional Requirements

- Real-time delivery with < 100ms latency
- High availability (99.99%)
- Exactly-once message delivery
- Message ordering per conversation
- Support 1B+ users
- Handle 100B+ messages per day
- Storage for 10+ years of messages
- Low bandwidth for mobile clients

## Capacity Estimation

```text
Storage Estimates:

- 1B users, 50 messages/day average = 50B messages/day
- Average message: 1 KB (text + metadata)
- Daily storage: 50B × 1 KB = 50 TB/day
- Yearly storage: 50 TB × 365 = ~18 PB/year
- Media storage: 10% messages with attachments
- Average attachment: 500 KB (images, voice)
- Daily media: 5B × 500 KB = 2.5 PB/day
- After compression + CDN: 250 TB/day

Bandwidth Estimates:

- Messages: 50B × 1 KB = 50 TB/day = ~580 MB/s
- Media: 250 TB/day = ~2.9 GB/s (CDN offloads most)
- WebSocket connections: 500M concurrent = 5 TB RAM
- Total: ~3.5 GB/s peak

WebSocket Estimates:

- 50% users online during peak = 500M concurrent
- Each connection: ~10 KB overhead
- Total connection memory: 500M × 10 KB = 5 TB
- Need 5000+ servers (100K connections each)

```

## API Design

```yaml
# Authentication
POST /api/v1/auth/register
  Request: { "phone": "+1234567890", "name": "John", "password": "***" }
  Response: { "user_id": "usr_123", "token": "jwt_token_here" }

POST /api/v1/auth/login
  Request: { "phone": "+1234567890", "password": "***" }
  Response: { "user_id": "usr_123", "token": "jwt_token_here" }

# Conversations
POST /api/v1/conversations
  Request: { "type": "direct"|"group", "participants": ["usr_456"], "name": "Project Chat" }
  Response: { "conversation_id": "conv_789", "type": "group", "created_at": "..." }

GET /api/v1/conversations?limit=20&before=cursor
  Response: { "conversations": [...], "next_cursor": "..." }

# Messages
POST /api/v1/conversations/{conv_id}/messages
  Request:
    {
      "content": "Hello!",
      "content_type": "text",  # text, image, video, file, voice
      "attachment_url": null,
      "reply_to_id": null,
      "encryption_key": null
    }
  Response:
    {
      "message_id": "msg_123",
      "conversation_id": "conv_789",
      "sender_id": "usr_123",
      "content": "Hello!",
      "created_at": "2025-01-15T10:30:00Z",
      "status": "sent"
    }

GET /api/v1/conversations/{conv_id}/messages?limit=50&before=msg_100
  Response: { "messages": [...], "has_more": true }

# Message actions
PUT /api/v1/messages/{msg_id}
  Request: { "content": "Updated message" }

DELETE /api/v1/messages/{msg_id}

POST /api/v1/messages/{msg_id}/reactions
  Request: { "reaction": "👍" }

# Presence
WebSocket: ws://chat.example.com/ws?token=jwt
  Events:
    {"type": "message", "data": {...}}
    {"type": "presence", "data": {"user_id": "usr_123", "status": "online"}}
    {"type": "typing", "data": {"conversation_id": "conv_789", "user_id": "usr_123"}}
    {"type": "read_receipt", "data": {"conversation_id": "conv_789", "message_id": "msg_123"}}
```

## Database Design
### Schema

```sql
-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    profile_picture_url TEXT,
    bio TEXT,
    password_hash VARCHAR(255) NOT NULL,
    public_key TEXT,                    -- For E2E encryption
    is_online BOOLEAN DEFAULT FALSE,
    last_seen_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_username ON users(username);

-- Conversations
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(10) NOT NULL,          -- 'direct', 'group'
    name VARCHAR(255),                  -- Group name
    avatar_url TEXT,
    created_by BIGINT REFERENCES users(id),
    last_message_id BIGINT,
    last_message_at TIMESTAMP,
    message_count BIGINT DEFAULT 0,
    is_encrypted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation participants
CREATE TABLE conversation_participants (
    conversation_id BIGINT REFERENCES conversations(id),
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member',  -- 'admin', 'member'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP,
    last_read_message_id BIGINT,
    is_muted BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (conversation_id, user_id)
);

CREATE INDEX idx_cp_user ON conversation_participants(user_id);
CREATE INDEX idx_cp_conversation ON conversation_participants(conversation_id);

-- Messages (partitioned by conversation_id hash)
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL REFERENCES conversations(id),
    sender_id BIGINT NOT NULL REFERENCES users(id),
    content TEXT,
    content_type VARCHAR(20) NOT NULL DEFAULT 'text',
    -- 'text', 'image', 'video', 'file', 'voice', 'system'
    attachment_url TEXT,
    attachment_metadata JSONB,          -- {width, height, duration, size, ...}
    reply_to_id BIGINT REFERENCES messages(id),
    encryption_key TEXT,                -- Encrypted per-recipient
    is_edited BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    reactions JSONB DEFAULT '{}',       -- {"👍": ["usr_123"], "❤️": ["usr_456"]}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY HASH (conversation_id);

CREATE INDEX idx_messages_conv ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_messages_sender ON messages(sender_id);

-- Message delivery status
CREATE TABLE message_delivery (
    message_id BIGINT REFERENCES messages(id),
    user_id BIGINT REFERENCES users(id),
    status VARCHAR(20) NOT NULL,        -- 'sent', 'delivered', 'read'
    read_at TIMESTAMP,
    delivered_at TIMESTAMP,
    PRIMARY KEY (message_id, user_id)
);

-- Message reactions (denormalized, also stored in messages.reactions JSONB)
CREATE TABLE message_reactions (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT REFERENCES messages(id),
    user_id BIGINT REFERENCES users(id),
    reaction VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (message_id, user_id, reaction)
);

CREATE INDEX idx_reactions_message ON message_reactions(message_id);
```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    users    │     │  conversations   │     │   messages      │
├─────────────┤     ├──────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ created_by (FK)  │     │ id (PK)         │
│ phone (UK)  │     │ id (PK)          │◄────│ conversation_id │
│ username    │     │ type             │     │ sender_id (FK)  │
│ display_name│     │ name             │────►│ content         │
│ profile_pic │     │ last_message_id  │     │ content_type    │
│ public_key  │     │ last_message_at  │     │ attachment_url  │
│ is_online   │     │ is_encrypted     │     │ reply_to_id     │
│ last_seen   │     └──────────────────┘     │ reactions       │
└─────────────┘              │              │ is_deleted      │
        │                    │              │ created_at      │
        │                    ▼              └─────────────────┘
        │     ┌──────────────────┐                 ▲
        │     │conv_participants │                 │
        │     ├──────────────────┤                 │
        │     │ conversation_id │─────────────────┘
        └─────│ user_id (FK)    │
              │ role            │         ┌─────────────────┐
              │ last_read_msg   │         │message_delivery │
              │ is_muted        │         ├─────────────────┤
              └──────────────────┘         │ message_id (FK)│
                                           │ user_id (FK)   │
                                           │ status         │
                                           │ read_at        │
                                           └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                      Clients (Web/Mobile)                         │
│             WebSocket + HTTP REST (for history)                   │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   Load Balancer L4    │
                    │  (TCP/WebSocket LB)  │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  WebSocket      │  │  WebSocket      │  │  WebSocket      │
│  Server         │  │  Server         │  │  Server         │
│  (100K conn)    │  │  (100K conn)    │  │  (100K conn)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Kafka Cluster  │
                    │  (Message Queue) │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ Message     │  │ Presence    │  │ Push        │
     │ Service     │  │ Service     │  │ Notification│
     └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
            │               │               │
            ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ PostgreSQL  │  │  Redis      │  │ Firebase    │
     │  Cluster    │  │ (Presence,  │  │ FCM/APNs    │
     │  (Messages) │  │  Sessions)  │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
            │
            ▼
     ┌─────────────────┐
     │  Elasticsearch  │
     │ (Message Search)│
     └─────────────────┘
```

## Key Components

### WebSocket Connection Manager

```python
import asyncio
import json
import time
from typing import Dict, Set

class ConnectionManager:
    """Manages WebSocket connections for real-time messaging."""

    def __init__(self, redis_client):
        self.redis = redis_client
        # Local mapping: user_id -> {device_id: websocket}
        self.connections: Dict[str, Dict[str, any]] = {}

    async def register_connection(self, user_id: str,
                                   device_id: str,
                                   websocket):
        """Register a new WebSocket connection."""
        if user_id not in self.connections:
            self.connections[user_id] = {}

        self.connections[user_id][device_id] = {
            'ws': websocket,
            'connected_at': time.time(),
            'device_type': self.get_device_type(device_id)
        }

        # Update presence in Redis
        await self.update_presence(user_id, 'online')
        await self.broadcast_presence(user_id, 'online')

    async def remove_connection(self, user_id: str,
                                 device_id: str):
        """Remove a WebSocket connection."""
        if user_id in self.connections:
            self.connections[user_id].pop(device_id, None)
            if not self.connections[user_id]:
                del self.connections[user_id]
                await self.update_presence(user_id, 'offline', offline_at=time.time())
                await self.broadcast_presence(user_id, 'offline')

    def get_user_connections(self, user_id: str) -> list:
        """Get all active connections for a user."""
        if user_id not in self.connections:
            return []
        return [
            info['ws'] for info in self.connections[user_id].values()
        ]

    async def send_to_user(self, user_id: str, event: dict):
        """Send event to all devices of a user."""
        sent = False
        for ws in self.get_user_connections(user_id):
            try:
                await ws.send_json(event)
                sent = True
            except Exception:
                pass
        return sent

    async def send_to_conversation(self, conversation_id: str,
                                    event: dict,
                                    exclude_user_id: str = None):
        """Send event to all participants in a conversation."""
        participants = await self.get_conversation_participants(
            conversation_id
        )
        for user_id in participants:
            if user_id == exclude_user_id:
                continue
            await self.send_to_user(user_id, event)

    async def broadcast_presence(self, user_id: str, status: str):
        """Broadcast presence change to user's contacts."""
        contacts = await self.get_user_contacts(user_id)
        for contact_id in contacts:
            await self.send_to_user(contact_id, {
                'type': 'presence',
                'user_id': user_id,
                'status': status,
                'timestamp': time.time()
            })

    async def update_presence(self, user_id: str, status: str,
                              offline_at: float = None):
        key = f"presence:{user_id}"
        if status == 'online':
            self.redis.hset(key, mapping={
                'status': 'online',
                'updated_at': time.time()
            })
            self.redis.expire(key, 300)  # 5 min heartbeat
        else:
            self.redis.hset(key, mapping={
                'status': 'offline',
                'last_seen': offline_at or time.time()
            })
            self.redis.expire(key, 86400)

    def get_device_type(self, device_id: str) -> str:
        if 'ios' in device_id.lower():
            return 'ios'
        elif 'android' in device_id.lower():
            return 'android'
        return 'web'

    async def get_conversation_participants(self,
                                            conv_id: str) -> list:
        return await self.redis.smembers(f"conv:{conv_id}:members")

    async def get_user_contacts(self, user_id: str) -> list:
        return await self.redis.smembers(f"contacts:{user_id}")
```

### Message Service

```python
from kafka import KafkaProducer
import json
import uuid

class MessageService:
    """Core message service for sending and receiving messages."""

    def __init__(self, db, redis_client, kafka_producer,
                 connection_manager):
        self.db = db
        self.redis = redis_client
        self.kafka = kafka_producer
        self.connections = connection_manager
        self.search_service = None  # Elasticsearch client, injected separately

    async def send_message(self, sender_id: str,
                           conversation_id: str,
                           content: dict) -> dict:
        """Send a message to a conversation."""
        # Validate sender is a participant
        if not await self.is_participant(conversation_id, sender_id):
            raise PermissionError("User is not a participant")

        # Create message
        message = {
            'id': self.generate_message_id(),
            'conversation_id': conversation_id,
            'sender_id': sender_id,
            'content': content.get('content', ''),
            'content_type': content.get('content_type', 'text'),
            'attachment_url': content.get('attachment_url'),
            'reply_to_id': content.get('reply_to_id'),
            'reactions': {},
            'created_at': time.time()
        }

        # Store in database (async via Kafka)
        await self.kafka.send('messages.new', message)

        # Cache for recent messages
        await self.cache_message(message)

        # Real-time delivery via WebSocket
        await self.deliver_to_online_participants(
            conversation_id, message, sender_id
        )

        # Update conversation metadata
        await self.update_conversation_metadata(
            conversation_id, message['id']
        )

        return message

    async def deliver_to_online_participants(self,
                                              conversation_id: str,
                                              message: dict,
                                              sender_id: str):
        """Deliver message to all online participants in real-time."""
        participants = await self.connections.get_conversation_participants(
            conversation_id
        )

        for participant_id in participants:
            if participant_id == sender_id:
                continue

            # Check if online
            online = await self.connections.send_to_user(
                participant_id,
                {
                    'type': 'message.new',
                    'data': message
                }
            )

            if online:
                # Update delivery status
                await self.track_delivery(
                    message['id'], participant_id, 'delivered'
                )
            else:
                # Queue for push notification
                await self.queue_offline_delivery(
                    participant_id, message
                )

    async def get_messages(self, conversation_id: str,
                           limit: int = 50,
                           before_id: str = None) -> dict:
        """Get messages with cursor-based pagination."""
        # Try cache first for recent messages
        cached = await self.get_cached_messages(
            conversation_id, limit
        )
        if cached and not before_id:
            return {'messages': cached, 'has_more': True}

        # Query database
        query = """
            SELECT * FROM messages
            WHERE conversation_id = $1
            AND ($2 IS NULL OR id < $2)
            AND is_deleted = FALSE
            ORDER BY created_at DESC
            LIMIT $3
        """
        messages = await self.db.query(
            query, conversation_id, before_id, limit + 1
        )

        has_more = len(messages) > limit
        if has_more:
            messages = messages[:limit]

        return {
            'messages': [dict(m) for m in messages],
            'has_more': has_more,
            'next_cursor': messages[-1]['id'] if messages else None
        }

    async def search_messages(self, user_id: str,
                              query: str,
                              limit: int = 20) -> list:
        """Search messages across user's conversations."""
        # Get user's conversation IDs
        conv_ids = await self.get_user_conversation_ids(user_id)

        # Search in Elasticsearch
        results = await self.search_service.search(
            index='messages',
            query={
                'bool': {
                    'must': [
                        {'match': {'content': query}},
                        {'terms': {'conversation_id': conv_ids}}
                    ]
                }
            },
            size=limit
        )

        return results['hits']['hits']

    def generate_message_id(self) -> str:
        """Generate unique, time-ordered message ID (Snowflake-like)."""
        return str(uuid.uuid4())

    async def is_participant(self, conv_id: str,
                             user_id: str) -> bool:
        return await self.redis.sismember(
            f"conv:{conv_id}:members", user_id
        )

    async def cache_message(self, message: dict):
        key = f"conv:messages:{message['conversation_id']}"
        self.redis.lpush(key, json.dumps(message))
        self.redis.ltrim(key, 0, 99)  # Keep last 100 messages
        self.redis.expire(key, 3600)

    async def get_cached_messages(self, conv_id: str,
                                  limit: int = 50) -> list:
        key = f"conv:messages:{conv_id}"
        messages = self.redis.lrange(key, 0, limit - 1)
        return [json.loads(m) for m in messages] if messages else []

    async def track_delivery(self, msg_id: str, user_id: str,
                             status: str):
        await self.db.execute(
            "INSERT INTO message_delivery (message_id, user_id, status, delivered_at) "
            "VALUES ($1, $2, $3, NOW()) "
            "ON CONFLICT (message_id, user_id) DO UPDATE SET status = $3",
            msg_id, user_id, status
        )

    async def queue_offline_delivery(self, user_id: str,
                                     message: dict):
        # Store in offline queue
        await self.redis.rpush(
            f"offline:{user_id}",
            json.dumps(message)
        )
        # Send push notification
        await self.send_push_notification(user_id, message)

    async def update_conversation_metadata(self, conv_id: str,
                                           last_msg_id: str):
        self.redis.hset(f"conv:{conv_id}", 'last_message_id', last_msg_id)
```

### Presence Service

```python
class PresenceService:
    """Manages user online/offline presence with heartbeat."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.heartbeat_interval = 60  # seconds

    async def heartbeat(self, user_id: str):
        """Update user heartbeat to keep presence alive."""
        key = f"presence:{user_id}"
        await self.redis.expire(key, self.heartbeat_interval * 3)

    async def get_presence(self, user_id: str) -> dict:
        """Get presence status for a user."""
        key = f"presence:{user_id}"
        data = await self.redis.hgetall(key)
        if data:
            return {
                'user_id': user_id,
                'status': 'online',
                'last_seen': float(data.get('updated_at', 0))
            }
        else:
            # User is offline - get last seen from DB cache
            last_seen = await self.redis.get(f"last_seen:{user_id}")
            return {
                'user_id': user_id,
                'status': 'offline',
                'last_seen': float(last_seen) if last_seen else 0
            }

    async def get_batch_presence(self, user_ids: list) -> dict:
        """Get presence for multiple users in batch."""
        pipeline = self.redis.pipeline()
        for uid in user_ids:
            pipeline.exists(f"presence:{uid}")

        results = await pipeline.execute()
        presence = {}
        for i, uid in enumerate(user_ids):
            presence[uid] = 'online' if results[i] else 'offline'
        return presence
```

### Push Notification Service

```python
class PushNotificationService:
    """Send push notifications to offline users."""

    def __init__(self, redis_client, fcm_client=None, apns_client=None):
        self.redis = redis_client
        self.fcm = fcm_client  # Firebase Cloud Messaging
        self.apns = apns_client  # Apple Push Notification Service

    async def send_push(self, user_id: str, message: dict):
        """Send push notification for new message."""
        # Get user's device tokens
        device_tokens = await self.get_device_tokens(user_id)

        notification = {
            'title': message.get('sender_name', 'New message'),
            'body': self.truncate_content(message.get('content', '')),
            'data': {
                'conversation_id': message['conversation_id'],
                'message_id': message['id'],
                'type': message['content_type']
            }
        }

        for token in device_tokens:
            if token['platform'] == 'ios':
                await self.send_apns(token['token'], notification)
            elif token['platform'] == 'android':
                await self.send_fcm(token['token'], notification)

    async def send_apns(self, device_token: str,
                        notification: dict):
        if not self.apns:
            return
        try:
            await self.apns.send_notification(
                device_token,
                alert={
                    'title': notification['title'],
                    'body': notification['body']
                },
                data=notification['data'],
                sound='default',
                badge='+1'
            )
        except Exception as e:
            print(f"APNS send failed: {e}")

    async def send_fcm(self, device_token: str,
                       notification: dict):
        if not self.fcm:
            return
        try:
            await self.fcm.send(
                device_token,
                notification={
                    'title': notification['title'],
                    'body': notification['body']
                },
                data=notification['data']
            )
        except Exception as e:
            print(f"FCM send failed: {e}")

    async def get_device_tokens(self, user_id: str) -> list:
        tokens = []
        # Get from Redis
        raw = await self.redis.smembers(f"devices:{user_id}")
        for token_str in raw:
            tokens.append(json.loads(token_str))
        return tokens

    def truncate_content(self, content: str, max_len: int = 100) -> str:
        return content[:max_len] + '...' if len(content) > max_len else content
```

### Typing Indicator Service

```python
class TypingIndicatorService:
    """Broadcast typing indicators in real-time."""

    def __init__(self, redis_client, connection_manager):
        self.redis = redis_client
        self.connections = connection_manager
        self.typing_timeout = 5  # seconds

    async def user_typing(self, user_id: str, conversation_id: str):
        """User started typing in a conversation."""
        key = f"typing:{conversation_id}:{user_id}"

        # Set typing indicator with TTL
        await self.redis.setex(key, self.typing_timeout, '1')

        # Broadcast to conversation
        await self.connections.send_to_conversation(
            conversation_id,
            {
                'type': 'typing',
                'user_id': user_id,
                'conversation_id': conversation_id,
                'is_typing': True
            },
            exclude_user_id=user_id
        )

    async def user_stopped_typing(self, user_id: str,
                                  conversation_id: str):
        """User stopped typing."""
        key = f"typing:{conversation_id}:{user_id}"
        await self.redis.delete(key)

        await self.connections.send_to_conversation(
            conversation_id,
            {
                'type': 'typing',
                'user_id': user_id,
                'conversation_id': conversation_id,
                'is_typing': False
            },
            exclude_user_id=user_id
        )

    async def get_users_typing(self, conversation_id: str) -> list:
        """Get users currently typing in a conversation."""
        pattern = f"typing:{conversation_id}:*"
        keys = await self.redis.keys(pattern)
        return [key.split(':')[-1] for key in keys]
```

### Read Receipt Service

```python
class ReadReceiptService:
    """Track and broadcast read receipts."""

    def __init__(self, db, redis_client, connection_manager):
        self.db = db
        self.redis = redis_client
        self.connections = connection_manager

    async def mark_as_read(self, user_id: str,
                           conversation_id: str,
                           message_id: str):
        """Mark messages as read up to the given message ID."""
        # Update last read in database
        await self.db.execute(
            "UPDATE conversation_participants "
            "SET last_read_message_id = $1, last_read_at = NOW() "
            "WHERE conversation_id = $2 AND user_id = $3",
            message_id, conversation_id, user_id
        )

        # Update cache
        await self.redis.hset(
            f"conv:{conversation_id}:read",
            user_id,
            message_id
        )

        # Get message sender to notify them
        message = await self.db.get(
            "SELECT sender_id FROM messages WHERE id = $1",
            message_id
        )

        if message:
            # Notify sender about read receipt
            await self.connections.send_to_user(
                message['sender_id'],
                {
                    'type': 'read_receipt',
                    'user_id': user_id,
                    'conversation_id': conversation_id,
                    'message_id': message_id
                }
            )

    async def get_last_read(self, conversation_id: str,
                            user_id: str) -> int:
        """Get last read message ID for a user."""
        cached = await self.redis.hget(
            f"conv:{conversation_id}:read", user_id
        )
        if cached:
            return int(cached)

        result = await self.db.get(
            "SELECT last_read_message_id FROM conversation_participants "
            "WHERE conversation_id = $1 AND user_id = $2",
            conversation_id, user_id
        )
        return result['last_read_message_id'] if result else 0
```

## Caching Strategy (Redis)

### Cache Layers

```python
class ChatCache:
    """Multi-layer caching for chat system."""

    def __init__(self, redis_client):
        self.redis = redis_client

    # Conversation cache
    async def cache_conversation(self, conv: dict):
        key = f"conv:{conv['id']}"
        self.redis.hset(key, mapping=conv)
        self.redis.expire(key, 3600)

    async def get_conversation(self, conv_id: str) -> dict:
        return await self.redis.hgetall(f"conv:{conv_id}")

    # Recent messages cache (per conversation, last 100)
    async def cache_recent_messages(self, conv_id: str,
                                    messages: list):
        key = f"conv:messages:{conv_id}"
        self.redis.delete(key)
        for msg in messages:
            self.redis.rpush(key, json.dumps(msg))
        self.redis.expire(key, 1800)

    async def get_recent_messages(self, conv_id: str,
                                  count: int = 50) -> list:
        key = f"conv:messages:{conv_id}"
        msgs = self.redis.lrange(key, -count, -1)
        return [json.loads(m) for m in msgs]

    # Offline messages queue
    async def queue_offline(self, user_id: str, message: dict):
        key = f"offline:{user_id}"
        self.redis.rpush(key, json.dumps(message))
        self.redis.expire(key, 86400 * 7)  # Keep 7 days

    async def get_offline_messages(self, user_id: str) -> list:
        key = f"offline:{user_id}"
        msgs = self.redis.lrange(key, 0, -1)
        self.redis.delete(key)
        return [json.loads(m) for m in msgs]
```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── messages.new             (new messages to persist)
├── messages.delivered       (delivery confirmations)
├── messages.read            (read receipts)
├── presence.update          (online/offline changes)
├── typing.indicator         (typing events)
├── notification.send        (push notification requests)
├── media.process            (media upload processing)
├── conversation.update      (conversation metadata updates)

Partitioning Strategy:

- messages.new: partition by conversation_id (message ordering)
- presence.update: partition by user_id
- notification.send: partition by user_id
```

### Message Persistence Consumer

```python
from kafka import KafkaConsumer
import json

class MessageConsumer:
    """Persist messages from Kafka to database."""

    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
        self.batch_size = 100
        self.batch = []

        self.consumer = KafkaConsumer(
            'messages.new',
            bootstrap_servers=['kafka1:9092'],
            group_id='message-persister',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_records=self.batch_size
        )

    async def process_batch(self):
        for message in self.consumer:
            data = json.loads(message.value.decode())

            # Batch insert
            self.batch.append(data)

            if len(self.batch) >= self.batch_size:
                await self.flush_batch()

    async def flush_batch(self):
        if not self.batch:
            return

        # Bulk insert messages
        values = [
            (m['id'], m['conversation_id'], m['sender_id'],
             m['content'], m['content_type'],
             m.get('attachment_url'), m.get('reply_to_id'),
             m.get('created_at'))
            for m in self.batch
        ]

        await self.db.executemany(
            "INSERT INTO messages (id, conversation_id, sender_id, "
            "content, content_type, attachment_url, reply_to_id, created_at) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7, to_timestamp($8)) "
            "ON CONFLICT (id) DO NOTHING",
            values
        )

        self.consumer.commit()
        self.batch = []
```

## Scaling Strategy

### WebSocket Connection Scaling

```text
┌─────────────────────────────────────────────────────────────┐
│                    Global Load Balancer                      │
│              (GeoDNS → Regional L4 Load Balancers)           │
└─────────────────────────────────────────────────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ US Region    │   │ EU Region    │   │ APAC Region  │
│ ──────────   │   │ ──────────   │   │ ──────────   │
│ WS Servers   │   │ WS Servers   │   │ WS Servers   │
│ (2000 nodes) │   │ (1500 nodes) │   │ (1500 nodes) │
│              │   │              │   │              │
│ Redis        │   │ Redis        │   │ Redis        │
│ Local        │   │ Local        │   │ Local        │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                  ┌───────┴───────┐
                  │  Global Redis │
                  │  (Cross-DC    │
                  │   Replication)│
                  └───────────────┘
```

## Failure Handling

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| WebSocket server crash | Client auto-reconnects to next available server |
| Kafka broker failure | Replication factor 3, ISR with min.in-sync.replicas=2 |
| Database node down | Automatic failover to replica in < 30 seconds |
| Redis cluster down | Fall back to direct DB reads for history, disable real-time |
| Network partition | Store messages in local queue, sync when reconnected |
| Push notification failure | Retry with backoff, queue for later delivery |

### Offline Message Sync

```python
class OfflineSyncService:
    """Sync offline messages when user comes online."""

    def __init__(self, redis_client, connection_manager):
        self.redis = redis_client
        self.connections = connection_manager

    async def sync_offline_messages(self, user_id: str):
        """Deliver queued offline messages to user."""
        offline_key = f"offline:{user_id}"
        message_count = 0

        while True:
            message_data = await self.redis.lpop(offline_key)
            if not message_data:
                break

            message = json.loads(message_data)
            await self.connections.send_to_user(user_id, {
                'type': 'message.new',
                'data': message,
                'is_offline_sync': True
            })
            message_count += 1

        return message_count
```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - messages_per_second
  - active_conversations
  - delivery_latency_p50_p95_p99
  - messages_per_user_per_day
  - attachment_upload_throughput

System Metrics:

  - websocket_connections_per_server
  - kafka_consumer_lag
  - database_write_throughput
  - redis_memory_usage
  - push_notification_success_rate

Infrastructure Metrics:

  - cpu_usage_per_ws_server
  - memory_usage_per_ws_server
  - network_bandwidth_per_server
  - connection_establishment_rate
  - error_rate_by_type
```

### Alerting

```yaml
alerts:

  - name: High Message Delivery Latency
    condition: p99_delivery_latency > 500ms for 5 minutes
    severity: critical

  - name: Connection Drop Spike
    condition: websocket_disconnects > 1000/min for 2 minutes
    severity: warning

  - name: Kafka Consumer Lag
    condition: kafka_lag > 50000 for 2 minutes
    severity: critical

  - name: Database Write Throughput Low
    condition: db_writes_per_second < expected * 0.5
    severity: warning

  - name: Push Notification Failure Rate
    condition: push_failure_rate > 10%
    severity: warning
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Message Ordering | Per-conversation (local ordering) | Global ordering (hard to scale) | Per-conversation ordering |
| Storage Engine | Cassandra (write-optimized) | PostgreSQL (ACID, familiar) | PostgreSQL with partitioning |
| Real-time Transport | WebSocket (bidirectional) | SSE (simpler, server→client) | WebSocket for full duplex |
| Message Delivery | At-least-once (reliable) | At-most-once (fast) | At-least-once with dedup |
| E2E Encryption | Signal Protocol (secure) | TLS-only (simpler) | Signal-like E2E for private chats |

## Summary

The Chat System design covers:

- **Real-time Messaging**: WebSocket-based instant delivery to 500M+ concurrent users
- **Message Persistence**: At-least-once delivery with exactly-once storage semantics
- **Offline Support**: Message queuing + push notifications for offline users
- **Presence & Typing**: Real-time indicators with heartbeat-based liveness
- **Scalability**: Geographic sharding, connection pooling, Kafka-based async processing

Key takeaways:

1. Use WebSocket with sticky sessions for real-time bidirectional communication

2. Implement at-least-once delivery with deduplication at the client level

3. Partition messages by conversation_id for ordering guarantees

4. Cache recent messages in Redis, persist full history in PostgreSQL

5. Use Kafka for async persistence and decoupling of services

This design handles 1B+ users with 100B+ messages/day while maintaining < 100ms delivery latency.

---

---

## Cheat Sheet
```text
CHAT SYSTEM DESIGN CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  | Failure | Mitigation |
  |---------|------------|
  | WebSocket server crash | Client auto-reconnects to next available server |
  | Kafka broker failure | Replication factor 3, ISR with min.in-sync.replicas=2 |
  | Database node down | Automatic failover to replica in < 30 seconds |
  | Redis cluster down | Fall back to direct DB reads for history, disable real-time |
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [WebSockets](../21-WebSockets/)
- [System Design - WhatsApp](../11-System-Design/02-WhatsApp.md)

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [WhatsApp Engineering Blog](https://engineering.fb.com/category/core-infra/)
- [Messenger Architecture (Facebook)](https://engineering.fb.com/2023/08/03/core-infra/messenger/)
- [Signal Protocol](https://signal.org/docs/)
