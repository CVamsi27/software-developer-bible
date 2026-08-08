---
section: System Design
category: Architecture
tags: [concept]
---

# Instagram System Design

## TL;DR

Design a photo/video sharing social network supporting upload, fan-out feed, likes/comments, stories, and explore — at billions of users and petabytes of media.

**Why it matters:** Tests media handling at scale (S3-style object storage, CDN), the same fan-out problem as Twitter but with heavier media payloads, the social-graph model (follow/follower counts), and the "celebrity skew" problem (one user, millions of followers). Mirrors Instagram's actual architecture.

## Requirements

### Functional Requirements

- Users can upload photos and short videos (up to 60s for Reels)
- Follow / unfollow other users
- Home feed: see posts from people you follow, ranked by recency + engagement
- Like and comment on posts
- Stories (24-hour ephemeral content)
- Explore tab: discovery of new content based on interests
- Direct messages (out of scope — see chat-system design)
- Search by username, hashtag, location
- Notifications for likes, comments, follows, mentions

### Non-Functional Requirements

- 2B+ monthly active users
- 100M photos/videos uploaded per day
- 50B+ photos stored
- Sub-300ms feed-load latency (p99)
- 99.99% availability for reads; 99.9% for writes
- Read-your-writes for the user posting (they should see their own post immediately)
- Eventual consistency for everyone else (1–5 min skew is acceptable)
- Strong consistency for likes/comments counters
- GDPR-compliant: delete a user's data on request

## Capacity Estimation

```text
User & Media:
- 2B MAU, 500M DAU
- 100M media uploads/day = ~1,160 uploads/sec average, ~3,500 peak
- 50B photos × 200 KB avg = 10 PB raw storage
- 3 replicas: 30 PB total

Feed Read Path:
- 500M DAU × 20 feed loads/day = 10B feed reads/day
- 10B / 10^5 = 100K reads/sec average, 300K peak
- Each feed load: 20 posts × 50 KB (thumbnails) = 1 MB payload

Storage Mix:
- Hot (last 30 days) on S3 + CloudFront: 100M × 30 × 200 KB = 600 TB
- Cold (older) on S3 IA / Glacier: 50B × 200 KB = 10 PB
- Metadata (PostgreSQL sharded): 50B rows × 2 KB = 100 TB
- Feed cache (Redis): 500M users × 100 KB of recent posts = 50 TB

Bandwidth:
- Write: 1,160 × 200 KB = 230 MB/s
- Read: 100K × 1 MB = 100 GB/s (CDN-absorbing most of this)

```

## API Design

```yaml
# Post upload
POST /v1/media
  Headers: Authorization: Bearer <token>
  Body (multipart):
    media_file: binary
    caption: string (optional)
    location: { lat, lng } (optional)
    tags: [string] (optional)
  Response:
    {
      "post_id": "post_abc123",
      "url": "https://cdn.example.com/posts/abc123.jpg",
      "thumbnail_url": "https://cdn.example.com/posts/abc123_thumb.jpg",
      "created_at": "2026-07-15T10:30:00Z"
    }

# Home feed
GET /v1/feed?cursor=...&limit=20
  Response:
    {
      "items": [
        {
          "post_id": "post_abc123",
          "user": { "id": "u_42", "username": "alice", "avatar": "..." },
          "media_url": "https://cdn.example.com/posts/abc123.jpg",
          "caption": "Sunset 🌅",
          "likes": 1234,
          "liked_by_me": true,
          "comments_count": 12,
          "created_at": "2026-07-15T10:30:00Z"
        }
      ],
      "next_cursor": "..."
    }

# Like
POST /v1/posts/{post_id}/likes
  Response: 200 { "likes": 1235 }

# Follow
POST /v1/users/{user_id}/follow
  Response: 204

```

## Database Design

### Schema (PostgreSQL, sharded by user_id)

```sql
-- Users
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts (sharded by user_id)
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    media_url TEXT NOT NULL,
    thumbnail_url TEXT,
    media_type VARCHAR(20) NOT NULL,  -- 'photo' | 'video' | 'reel' | 'story'
    caption TEXT,
    location_id BIGINT,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    view_count BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,           -- for stories
    deleted_at TIMESTAMPTZ,
    INDEX idx_user_created (user_id, created_at DESC)
);

-- Follows (sharded by follower_id)
CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (follower_id, followee_id)
);

-- Likes (sharded by post_id)
CREATE TABLE likes (
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, post_id)
);

-- Feed cache (separate Redis cluster, not SQL)

-- Comments (sharded by post_id)
CREATE TABLE comments (
    comment_id BIGINT PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    parent_comment_id BIGINT,
    like_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Architecture

### ASCII Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                        INSTAGRAM-TYPE STACK                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Client (Mobile/Web)                                                │
│       │                                                             │
│       ▼                                                             │
│  CDN (CloudFront / Fastly) — media + thumb delivery                 │
│       │                                                             │
│       ▼                                                             │
│  Load Balancer → API Gateway (rate limit, auth, routing)            │
│       │                                                             │
│       ├──▶ Feed Service ──▶ Redis (precomputed feed cache)          │
│       │              │                                              │
│       │              └─▶ Fan-out Service (write path) ──▶ Kafka      │
│       │                                                                 │
│       ├──▶ Post Service ──▶ PostgreSQL (sharded by user_id)          │
│       │              │                                              │
│       │              └─▶ Object Store (S3) + Image Pipeline          │
│       │                                                                 │
│       ├──▶ Follow Service ──▶ PostgreSQL (graph shard)               │
│       │                                                                 │
│       ├──▶ Like / Comment Service ──▶ Cassandra (counter shard)      │
│       │                                                                 │
│       ├──▶ Notification Service ──▶ Kafka ──▶ APNs / FCM            │
│       │                                                                 │
│       └──▶ Search Service ──▶ Elasticsearch / OpenSearch            │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Media Upload Pipeline

1. Client requests a **pre-signed S3 URL** with an upload policy (max size, content-type).
2. Client uploads directly to S3 (bypasses app servers — saves bandwidth and CPU).
3. Client calls `POST /v1/media` with the S3 object key.
4. Post Service writes the metadata row and enqueues a Kafka event `post.created`.
5. Image Pipeline worker picks up the event, generates thumbnails (multiple sizes) and probes metadata (EXIF, dimensions).
6. On success, post metadata is updated with thumbnail URLs.

### Feed Generation (Hybrid Push/Pull)

- **Push (fan-out on write)**: When user A with 1M followers posts, we enqueue a fan-out job that pushes the post ID into the feed cache (Redis) of each follower.
- **Pull (for celebrities)**: For users with >100K followers, do not fan out. Instead, merge at read time by querying the celebrity's recent posts and inserting them at the top of the feed.

```text
Read path:
  1. Read precomputed feed from Redis (last 500 post IDs)
  2. Hydrate with full post objects from post cache (Memcached)
  3. For each followed celebrity, fetch their latest N posts and merge
  4. Apply ranking model (recency × engagement × affinity)
  5. Return top 20

Write path:
  1. Post created → write to PostgreSQL (strong)
  2. Publish to Kafka `post.created`
  3. Fan-out worker:
     a. If user has <100K followers → push post ID to each follower's feed cache
     b. If user has >=100K followers → mark as "celebrity" in their profile; read path merges
  4. Update post_count, increment counters
```

## Caching Strategy

| Cache | Stores | TTL | Invalidation |
|---|---|---|---|
| Redis feed cache | `user_id → [post_id, ...]` | 7 days, LRU on overflow | New post event-driven push |
| Memcached post cache | `post_id → post object` | 24 hours | Delete on post update/delete |
| CDN | Media + thumbnails | Edge TTL (30 days) | Versioned URLs (purge via /thumb_v2.jpg) |
| Local in-process (LRU) | Hottest 1K posts per app server | 60s | Time-based |
| Browser cache | Media + UI bundle | 1 year (content-hashed) | N/A — content-hash in URL |

## Message Queue

Kafka is the right pick here because:

- High throughput (millions of events/sec)
- Replay for backfill (e.g., when feed ranking model changes, replay `post.created`)
- Multi-consumer (fan-out, search indexer, analytics, notifications)

Topics:
- `post.created` → fan-out, search, notification
- `user.followed` → timeline generation, notification
- `post.liked` → counter update, notification
- `post.commented` → counter update, notification
- `media.uploaded` → image pipeline

## Scaling Strategy

| Bottleneck | Solution |
|---|---|
| Hot user (celebrity with 1B followers) | Pull-side merge instead of push |
| Feed cache too large | Shard by user_id; LRU eviction for inactive users |
| Image processing latency | Parallel pipeline workers; precompute on upload |
| Database write contention on `posts` table | Shard by user_id; consider Cassandra for the timeline side |
| Counter updates (likes) on hot posts | Async counter via Kafka; eventual consistency |
| Search index rebuild on schema change | Dual-write Elasticsearch; switch readers after verified |

## Failure Handling

| Failure | Mitigation |
|---|---|
| Feed cache Redis down | Fall back to DB + celebrity merge; degraded but functional |
| Kafka down | Buffer write events in a local write-ahead log; replay on recovery |
| Image pipeline worker dies | Re-queue; idempotent retries on `media.processed` event |
| Celebrity user posts | Detect on write; do NOT push to followers; read-time merge |
| Hot post (1M likes/sec) | Async counter updates batched; counter reconciled nightly |
| S3 region outage | Multi-region active-passive for hot media; serve stale OK |

## Monitoring

- **Business metrics**: posts/sec, likes/sec, DAU/MAU ratio, feed CTR
- **Latency**: feed load p50/p95/p99, upload ack, image processing duration
- **Cache hit rate**: feed cache, post cache, CDN cache
- **Queue health**: Kafka consumer lag per topic, DLQ size
- **Storage**: S3 object count, PG row counts, shard skew
- **Errors**: 5xx rate, partial-failure rate from image pipeline

Alerts: feed load p99 > 1s, image pipeline lag > 5 min, fan-out lag > 1 min, Redis memory > 80%.

## Trade-offs

| Decision | Option A | Option B | Choice |
|---|---|---|---|
| Feed generation | Push (write-heavy) | Pull (read-heavy) | Hybrid (push for normal users, pull for celebrities) |
| Counter store | PostgreSQL (strong) | Cassandra (fast) | Cassandra (eventual OK, hot-path tolerant) |
| Media metadata | PostgreSQL | DynamoDB | PostgreSQL (joins + transactions needed) |
| Search | Elasticsearch (own infra) | Algolia (managed) | Elasticsearch (cost + control at scale) |
| Direct messages | Custom WebSocket | Third-party (Sendbird) | Custom (sticky feature, control UX) |
| Story expiry | Cron deletion | TTL on row + lazy expiry | TTL + lazy (lower write amplification) |

## Summary

- **Storage**: PostgreSQL for relational data, S3 for media, Cassandra for counters, Redis for feed cache, Elasticsearch for search.
- **Feed**: Hybrid push/pull handles the celebrity skew problem — the single most important design decision.
- **Media pipeline**: Client uploads directly to S3 via pre-signed URL; app servers never touch the bytes.
- **Async everything**: Fan-out, search indexing, notifications, and counter updates are all Kafka-driven to keep the write path sub-100ms.
- **GDPR**: Soft-delete users; hard-delete media + scrub S3 + scrub search index via tombstone event.

---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [Object Storage & CDN](../08-Database/) (database section)
- [System Design Interview Questions](16-Interview-Questions.md)
- [Twitter Feed](12-Twitter-Feed.md)
- [URL Shortener](01-URL-Shortener.md)

## References & Learn More

- [Instagram Engineering Blog](https://instagram-engineering.com/)
- [What Powers Instagram — Hundreds of Instances, Dozens of Technologies](https://instagram-engineering.com/what-powers-instagram-hundreds-of-instances-dozens-of-technologies-62c0a4f5579f)
- [System Design Primer — Instagram](https://github.com/donnemartin/system-design-primer#design-instagram)
- [Alex Xu — System Design Vol 2 (Instagram chapter)](https://bytebytego.com/)
- [How Instagram Really Works — High Scalability](http://highscalability.com/blog/2012/4/9/the-instagram-architecture-facebook-bought-for-1-billion.html)
