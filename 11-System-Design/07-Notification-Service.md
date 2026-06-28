# Notification Service System Design

## Requirements
### Functional Requirements

- Send push notifications (iOS, Android)
- Send email notifications
- Send SMS notifications
- Support in-app notifications
- Template-based notifications
- User notification preferences
- Notification scheduling
- Delivery tracking and analytics
- Rate limiting per user
- A/B testing for notifications

### Non-Functional Requirements

- High availability (99.99%)
- Delivery latency < 5 seconds for push
- Support 100M+ users
- Handle 1B+ notifications per day
- At-least-once delivery guarantee
- Scalable template engine
- Multi-language support
- GDPR compliance

## Capacity Estimation

```text
Notification Estimates:

- 100M users × 10 notifications/day = 1B notifications/day
- Peak: 1B / 86400 = ~11.6K notifications/second
- Average notification size: 1 KB
- Daily data: 1B × 1 KB = 1 TB

Channel Distribution:

- Push: 60% = 600M/day
- Email: 30% = 300M/day
- SMS: 10% = 100M/day

Storage Estimates:

- Notification logs: 1 TB/day × 30 days = 30 TB/month
- User preferences: 100M × 1 KB = 100 GB
- Templates: 10K × 10 KB = 100 MB

Bandwidth Estimates:

- Outbound: 11.6K × 1 KB = 11.6 MB/s
- Peak: 5x = 58 MB/s
- SMS provider: 100M × 160 bytes = 16 GB/day

```

## API Design

```yaml
# Send Notification
POST /api/v1/notifications
  Request:
    {
      "user_id": "usr_123",
      "channel": "push",  # push, email, sms, in_app
      "template": "order_shipped",
      "data": {
        "order_id": "ord_456",
        "tracking_url": "https://..."
      },
      "schedule_at": "2025-01-15T10:00:00Z"  # optional
    }
  Response:
    {
      "notification_id": "ntf_789",
      "status": "queued",
      "estimated_delivery": "2025-01-15T10:00:05Z"
    }

# Send Bulk Notifications
POST /api/v1/notifications/bulk
  Request:
    {
      "user_ids": ["usr_123", "usr_456"],
      "channel": "email",
      "template": "weekly_digest",
      "data": {...}
    }
  Response:
    {
      "batch_id": "batch_012",
      "total": 2,
      "status": "queued"
    }

# Get Notification Status
GET /api/v1/notifications/{id}
  Response:
    {
      "id": "ntf_789",
      "status": "delivered",
      "channel": "push",
      "sent_at": "2025-01-15T10:00:02Z",
      "delivered_at": "2025-01-15T10:00:04Z",
      "opened_at": "2025-01-15T10:05:00Z"
    }

# Update User Preferences
PUT /api/v1/users/{id}/preferences
  Request:
    {
      "push_enabled": true,
      "email_enabled": true,
      "sms_enabled": false,
      "quiet_hours_start": "22:00",
      "quiet_hours_end": "08:00",
      "categories": {
        "marketing": false,
        "transactional": true
      }
    }

# Get Notification History
GET /api/v1/notifications/history
  Query: ?user_id=usr_123&channel=push&limit=50
  Response:
    {
      "notifications": [...],
      "has_more": true,
      "cursor": "cur_345"
    }

```

## Database Design
### Schema

```sql
-- Users notification preferences
CREATE TABLE user_preferences (
    user_id BIGINT PRIMARY KEY,
    push_enabled BOOLEAN DEFAULT TRUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT TRUE,
    in_app_enabled BOOLEAN DEFAULT TRUE,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    timezone VARCHAR(50) DEFAULT 'UTC',
    locale VARCHAR(10) DEFAULT 'en',
    categories JSONB DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification templates
CREATE TABLE templates (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    channel VARCHAR(20) NOT NULL,
    subject VARCHAR(255),
    body TEXT NOT NULL,
    variables JSONB,
    language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications log
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    channel VARCHAR(20) NOT NULL,
    template_id BIGINT REFERENCES templates(id),
    subject VARCHAR(255),
    body TEXT,
    data JSONB,
    status VARCHAR(20) NOT NULL, -- 'queued', 'sent', 'delivered', 'failed'
    priority VARCHAR(10) DEFAULT 'normal',
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    opened_at TIMESTAMP,
    failure_reason TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE notifications_2025_01 PARTITION OF notifications
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_scheduled ON notifications(scheduled_at)
    WHERE status = 'queued';

-- Device tokens for push notifications
CREATE TABLE device_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    device_type VARCHAR(20) NOT NULL, -- 'ios', 'android', 'web'
    token TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, device_type, token)
);

-- Email delivery tracking
CREATE TABLE email_deliveries (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT REFERENCES notifications(id),
    provider VARCHAR(50) NOT NULL, -- 'sendgrid', 'ses'
    provider_message_id VARCHAR(255),
    status VARCHAR(20) NOT NULL,
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP,
    bounced_at TIMESTAMP,
    bounce_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SMS delivery tracking
CREATE TABLE sms_deliveries (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT REFERENCES notifications(id),
    provider VARCHAR(50) NOT NULL, -- 'twilio', 'nexmo'
    provider_message_id VARCHAR(255),
    status VARCHAR(20) NOT NULL,
    cost DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification analytics
CREATE TABLE notification_analytics (
    id BIGSERIAL PRIMARY KEY,
    template_id BIGINT REFERENCES templates(id),
    channel VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    sent_count INT DEFAULT 0,
    delivered_count INT DEFAULT 0,
    opened_count INT DEFAULT 0,
    clicked_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    UNIQUE(template_id, channel, date)
);

```

### ER Diagram (ASCII)

```text
┌─────────────────────┐     ┌─────────────────┐
│  user_preferences   │     │    templates     │
├─────────────────────┤     ├─────────────────┤
│ user_id (PK)        │     │ id (PK)         │
│ push_enabled        │     │ name            │
│ email_enabled       │     │ channel         │
│ sms_enabled         │     │ subject         │
│ quiet_hours_start   │     │ body            │
│ quiet_hours_end     │     │ variables       │
│ categories          │     │ language        │
└─────────────────────┘     │ is_active       │
        │                   └─────────────────┘
        │                            │
        │                            ▼
        │                   ┌─────────────────┐
        │                   │   notifications │
        │                   ├─────────────────┤
        │                   │ id (PK)         │
        │                   │ user_id (FK)    │
        │                   │ channel         │
        │                   │ template_id(FK) │
        │                   │ subject         │
        │                   │ body            │
        │                   │ status          │
        │                   │ scheduled_at    │
        │                   │ sent_at         │
        │                   │ delivered_at    │
        │                   └─────────────────┘
        │                            │
        │              ┌─────────────┼─────────────┐
        │              │             │             │
        │              ▼             ▼             ▼
        │     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │     │email_       │ │sms_         │ │notification_│
        │     │deliveries   │ │deliveries   │ │analytics    │
        │     ├─────────────┤ ├─────────────┤ ├─────────────┤
        │     │id (PK)      │ │id (PK)      │ │id (PK)      │
        │     │notification │ │notification │ │template_id  │
        │     │provider     │ │provider     │ │channel      │
        │     │status       │ │status       │ │date         │
        │     │opened_at    │ │cost         │ │sent_count   │
        │     └─────────────┘ └─────────────┘ │delivered_cnt│
        │                                     └─────────────┘
        ▼
┌─────────────────────┐
│   device_tokens     │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ device_type         │
│ token               │
│ is_active           │
│ last_used_at        │
└─────────────────────┘

```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│           (Mobile, Web, Backend Services)                        │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway        │
                    │   (Rate Limiting,    │
                    │    Authentication)   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Notification        │
                    │  Service             │
                    │  (Template Engine,   │
                    │   Preference Check)  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Message Queue      │
                    │   (Kafka Cluster)    │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Push Service   │  │  Email Service  │  │  SMS Service    │
│  (FCM, APNs)    │  │  (SendGrid,     │  │  (Twilio,       │
│                 │  │   SES)          │  │   Nexmo)        │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │   Analytics          │
                    │   Service            │
                    │   (Delivery Tracking,│
                    │    Metrics)          │
                    └──────────────────────┘

```

## Key Components

### Template Engine

```python
from jinja2 import Environment, BaseLoader
import json

class TemplateEngine:
    def __init__(self, db):
        self.db = db
        self.env = Environment(loader=BaseLoader())
        self.cache = {}

    async def render_template(self, template_name: str,
                              variables: dict,
                              language: str = 'en') -> dict:
        # Get template from cache or database
        cache_key = f"{template_name}:{language}"

        if cache_key not in self.cache:
            template = await self.db.get_template(
                template_name, language
            )
            self.cache[cache_key] = template

        template = self.cache[cache_key]

        # Render subject and body
        subject_template = self.env.from_string(
            template['subject'] or ''
        )
        body_template = self.env.from_string(template['body'])

        return {
            'subject': subject_template.render(**variables),
            'body': body_template.render(**variables),
            'template_id': template['id']
        }

    async def render_multichannel(self, template_name: str,
                                  variables: dict) -> dict:
        # Render for all channels
        channels = ['push', 'email', 'sms', 'in_app']
        results = {}

        for channel in channels:
            try:
                rendered = await self.render_template(
                    f"{template_name}_{channel}",
                    variables
                )
                results[channel] = rendered
            except TemplateNotFound:
                # Use default template
                results[channel] = await self.render_template(
                    template_name, variables
                )

        return results

```

### Notification Dispatcher

```python
class NotificationDispatcher:
    def __init__(self, preference_service, template_engine,
                 push_service, email_service, sms_service):
        self.preferences = preference_service
        self.templates = template_engine
        self.push = push_service
        self.email = email_service
        self.sms = sms_service

    async def dispatch(self, notification: dict) -> dict:
        user_id = notification['user_id']
        channel = notification['channel']

        # Check user preferences
        if not await self.preferences.is_channel_enabled(
            user_id, channel
        ):
            return {'status': 'skipped', 'reason': 'channel_disabled'}

        # Check quiet hours
        if await self.preferences.is_quiet_hours(user_id):
            return {'status': 'scheduled', 'reason': 'quiet_hours'}

        # Render template
        rendered = await self.templates.render_template(
            notification['template'],
            notification['data']
        )

        # Send via appropriate channel
        if channel == 'push':
            result = await self.push.send(user_id, rendered)
        elif channel == 'email':
            result = await self.email.send(user_id, rendered)
        elif channel == 'sms':
            result = await self.sms.send(user_id, rendered)

        return result

```

### Rate Limiter

```python
from redis import Redis
from datetime import datetime, timedelta

class NotificationRateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.limits = {
            'push': {'count': 100, 'window': 3600},  # 100/hour
            'email': {'count': 50, 'window': 3600},   # 50/hour
            'sms': {'count': 10, 'window': 86400},    # 10/day
            'in_app': {'count': 200, 'window': 3600}  # 200/hour
        }

    async def is_allowed(self, user_id: str, channel: str) -> bool:
        limit_config = self.limits.get(channel)
        if not limit_config:
            return True

        key = f"rate_limit:{user_id}:{channel}"

        # Get current count
        current = await self.redis.get(key)
        if current and int(current) >= limit_config['count']:
            return False

        # Increment counter
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, limit_config['window'])
        pipe.execute()

        return True

    async def get_remaining(self, user_id: str,
                           channel: str) -> int:
        limit_config = self.limits.get(channel)
        if not limit_config:
            return float('inf')

        key = f"rate_limit:{user_id}:{channel}"
        current = await self.redis.get(key)

        if current:
            return max(0, limit_config['count'] - int(current))

        return limit_config['count']

```

### Push Notification Service

```python
from firebase_admin import messaging
import aiohttp

class PushNotificationService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def send(self, user_id: str, notification: dict) -> dict:
        # Get device tokens
        tokens = await self.db.get_device_tokens(user_id)

        if not tokens:
            return {'status': 'no_devices'}

        # Send to all devices
        results = []
        for token_info in tokens:
            try:
                if token_info['device_type'] == 'ios':
                    result = await self.send_apns(
                        token_info['token'], notification
                    )
                elif token_info['device_type'] == 'android':
                    result = await self.send_fcm(
                        token_info['token'], notification
                    )

                results.append(result)
            except Exception as e:
                # Log failure but continue with other devices
                logger.error(f"Push failed for {token_info}: {e}")

        return {'status': 'sent', 'results': results}

    async def send_fcm(self, token: str, notification: dict) -> dict:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.get('subject', ''),
                body=notification.get('body', '')
            ),
            data=notification.get('data', {}),
            token=token
        )

        response = messaging.send(message)
        return {'message_id': response}

    async def send_apns(self, token: str, notification: dict) -> dict:
        # Use HTTP/2 APNs API
        async with aiohttp.ClientSession() as session:
            payload = {
                'aps': {
                    'alert': {
                        'title': notification.get('subject', ''),
                        'body': notification.get('body', '')
                    },
                    'badge': 1,
                    'sound': 'default'
                },
                'data': notification.get('data', {})
            }

            async with session.post(
                'https://api.push.apple.com/3/device/' + token,
                json=payload,
                headers=self.get_apns_headers()
            ) as response:
                return await response.json()

```

### Email Service

```python
import sendgrid
from sendgrid.helpers.mail import Mail

class EmailService:
    def __init__(self, db):
        self.db = db
        self.sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY')
        )

    async def send(self, user_id: str, notification: dict) -> dict:
        # Get user email
        user = await self.db.get_user(user_id)

        # Create message
        message = Mail(
            from_email='noreply@example.com',
            to_emails=user['email'],
            subject=notification.get('subject', ''),
            html_content=notification.get('body', '')
        )

        # Send
        try:
            response = self.sg.send(message)
            return {
                'status': 'sent',
                'provider_message_id': response.headers.get(
                    'X-Message-Id'
                )
            }
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

```

### SMS Service

```python
from twilio.rest import Client

class SMSService:
    def __init__(self, db):
        self.db = db
        self.client = Client(
            os.environ.get('TWILIO_SID'),
            os.environ.get('TWILIO_AUTH_TOKEN')
        )

    async def send(self, user_id: str, notification: dict) -> dict:
        # Get user phone
        user = await self.db.get_user(user_id)

        # Send SMS
        try:
            message = self.client.messages.create(
                body=notification.get('body', ''),
                from_='+1234567890',
                to=user['phone']
            )

            return {
                'status': 'sent',
                'provider_message_id': message.sid,
                'cost': float(message.price) if message.price else 0
            }
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

```

## Caching Strategy (Redis)

### Template Cache

```python
class TemplateCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hour

    async def get_template(self, template_name: str,
                          language: str) -> dict:
        key = f"template:{template_name}:{language}"
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)

        return None

    async def set_template(self, template_name: str,
                          language: str, template: dict):
        key = f"template:{template_name}:{language}"
        await self.redis.setex(
            key, self.ttl, json.dumps(template)
        )

    async def invalidate(self, template_name: str):
        # Invalidate all language versions
        pattern = f"template:{template_name}:*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

```

### User Preferences Cache

```python
class PreferencesCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 300  # 5 minutes

    async def get_preferences(self, user_id: str) -> dict:
        key = f"preferences:{user_id}"
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)

        return None

    async def set_preferences(self, user_id: str,
                             preferences: dict):
        key = f"preferences:{user_id}"
        await self.redis.setex(
            key, self.ttl, json.dumps(preferences)
        )

```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── notification.created    (new notifications)
├── notification.sent       (sent to providers)
├── notification.delivered  (delivery confirmation)
├── notification.opened     (user opened notification)
├── notification.clicked    (user clicked notification)
└── notification.failed     (delivery failures)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "notification.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "notification_id": "ntf_456",
    "user_id": "usr_789",
    "channel": "push",
    "template": "order_shipped"
  }
}

```

### Event Processing

```python
class NotificationEventProcessor:
    def __init__(self, kafka_consumer, dispatcher, analytics):
        self.consumer = kafka_consumer
        self.dispatcher = dispatcher
        self.analytics = analytics

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'notification.created':
                await self.handle_created(event)
            elif event['event_type'] == 'notification.delivered':
                await self.handle_delivered(event)

    async def handle_created(self, event: dict):
        # Dispatch notification
        result = await self.dispatcher.dispatch(event['data'])

        # Update status
        await self.update_notification_status(
            event['data']['notification_id'],
            result['status']
        )

        # Track analytics
        await self.analytics.track_sent(event['data'])

```

## Scaling Strategy

### Horizontal Scaling

```text
Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Notification│   │  Notification│   │  Notification│
│  Service     │   │  Service     │   │  Service     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘

```

### Database Scaling

```python
class NotificationDatabaseScaler:
    def __init__(self):
        self.partitions = 12  # Monthly partitions

    def get_partition(self, date: date) -> str:
        return f"notifications_{date.year}_{date.month:02d}"

    async def insert_notification(self, notification: dict):
        partition = self.get_partition(notification['created_at'])
        # Insert into appropriate partition

```

### Queue Scaling

```python
class NotificationQueueScaler:
    def __init__(self):
        self.partitions = 16

    def get_partition(self, user_id: int) -> int:
        return user_id % self.partitions

```

## Failure Handling

### Retry Logic

```python
class NotificationRetry:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [60, 300, 900]  # seconds

    async def send_with_retry(self, notification: dict,
                              dispatcher):
        for attempt in range(self.max_retries):
            try:
                result = await dispatcher.dispatch(notification)

                if result['status'] == 'sent':
                    return result

            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {e}")

                if attempt < self.max_retries - 1:
                    await asyncio.sleep(
                        self.retry_delays[attempt]
                    )

        # All retries failed
        return {'status': 'failed', 'reason': 'max_retries'}

```

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| FCM/APNs down | Retry with exponential backoff |
| SendGrid down | Fallback to SES |
| Twilio down | Fallback to Nexmo |
| Database down | Queue notifications in Redis |
| Kafka down | Buffer locally, process later |

### Graceful Degradation

```python
class GracefulDegradation:
    def __init__(self):
        self.fallback_channels = {
            'push': 'email',
            'email': 'sms',
            'sms': 'in_app'
        }

    async def send_with_fallback(self, notification: dict,
                                 dispatcher):
        channel = notification['channel']

        try:
            result = await dispatcher.dispatch(notification)

            if result['status'] == 'failed':
                # Try fallback channel
                fallback = self.fallback_channels.get(channel)
                if fallback:
                    notification['channel'] = fallback
                    return await dispatcher.dispatch(notification)

            return result

        except Exception:
            # Use fallback channel
            fallback = self.fallback_channels.get(channel)
            if fallback:
                notification['channel'] = fallback
                return await dispatcher.dispatch(notification)

```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - notifications_per_second
  - delivery_rate_by_channel
  - open_rate_by_channel
  - click_rate_by_channel

System Metrics:

  - delivery_latency_p95
  - queue_depth
  - error_rate_by_provider
  - template_render_time

Infrastructure Metrics:

  - server_cpu_usage
  - memory_usage
  - kafka_consumer_lag
  - redis_memory_usage

```

### Alerting Rules

```yaml
alerts:

  - name: High Failure Rate
    condition: failure_rate > 5%
    severity: critical

  - name: Queue Backlog
    condition: queue_depth > 100000
    severity: warning

  - name: Delivery Latency High
    condition: p95_latency > 10s
    severity: warning

  - name: Provider Error Spike
    condition: provider_error_rate > 10%
    severity: critical

```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | PostgreSQL | Cassandra | PostgreSQL (ACID) |
| Queue | Kafka | RabbitMQ | Kafka (scalability) |
| Template | Jinja2 | Handlebars | Jinja2 (flexibility) |
| Caching | Redis | Memcached | Redis (rich data) |
| Delivery | Synchronous | Async | Async (scalability) |

## Interview Questions

### Design Questions

1. **How would you design a notification service?**

   - Template engine for customizable notifications
   - User preferences for channel selection
   - Rate limiting to prevent abuse
   - Delivery tracking and analytics

2. **How do you handle notification preferences?**

   - Store preferences in database
   - Cache in Redis for fast lookup
   - Check before sending
   - Respect quiet hours

3. **How would you implement A/B testing?**

   - Create multiple template variants
   - Random user assignment
   - Track open/click rates
   - Statistical significance testing

### Scaling Questions

4. **How do you scale to 1B notifications per day?**

   - Partition notifications by user
   - Horizontal scaling of services
   - Kafka for async processing
   - Database sharding by time

5. **How do you handle rate limiting?**

   - Redis-based rate limiting
   - Per-user and per-channel limits
   - Graceful degradation
   - Queue overflow handling

### Trade-off Questions

6. **How do you balance delivery speed vs cost?**

   - Priority queues for important notifications
   - Batch processing for non-urgent
   - Channel selection based on urgency
   - Cost optimization by provider

7. **How do you ensure delivery guarantees?**

   - At-least-once delivery
   - Idempotency for deduplication
   - Dead letter queue for failures
   - Retry with exponential backoff

### Senior-level Questions

8. **How would you implement multi-language support?**

   - Template versioning by language
   - User locale detection
   - Fallback to default language
   - Translation management

9. **How do you handle notification fatigue?**

   - Smart batching
   - Priority-based delivery
   - User engagement tracking
   - Frequency capping

10. **How would you implement real-time notifications?**

    - WebSocket for in-app
    - Push for mobile
    - SSE for web
    - Event-driven architecture

## Summary

The Notification Service system design covers:

- **Multi-channel**: Push, email, SMS, in-app
- **Template Engine**: Customizable notifications
- **Rate Limiting**: Per-user and per-channel
- **Delivery Tracking**: Full lifecycle visibility
- **Scalability**: Handles 1B+ notifications/day

Key takeaways:

1. Use template engine for customizable notifications

2. Implement user preferences for channel selection

3. Use rate limiting to prevent notification fatigue

4. Track delivery status for reliability

5. Design for graceful degradation

This design supports 100M+ users with 1B+ notifications per day while maintaining 99.99% availability.

---

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
