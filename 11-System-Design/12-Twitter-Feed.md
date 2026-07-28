# Twitter Feed System Design

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

ers)
- Users can follow/unfollow other users
- Users see a timeline of tweets from followed users
- Timeline should show most recent tweets first (reverse chronological)
- Support for media attachments (images, videos)
- Like, retweet, and reply to tweets
- Hashtags and search functionality
- User profiles with tweet history
- Trending topics based on tweet velocity
- Notifications for interactions

### Non-Functional Requirements

- Low latency timeline loading (< 200ms)
- High availability (99.99%)
- Handle 500M daily active users
- Support 10K tweets/second at peak
- Fanout to millions of followers per tweet
- Timeline consistency within seconds
- Support both push (fanout-on-write) and pull (fanout-on-read) patterns

## Capacity Estimation

```text
Storage Estimates:

- 500M DAU, 50% tweet once per day = 250M tweets/day
- Average tweet: 280 bytes + 1 KB metadata = ~1.28 KB
- Daily storage: 250M × 1.28 KB = ~320 GB/day
- Yearly storage: 320 GB × 365 = ~117 TB/year
- Media storage: 10% tweets have images (200 KB avg) = 50 TB/day
- Total yearly: ~18 PB (media) + 117 TB (tweets)

Bandwidth Estimates:

- Write: 250M tweets/day = ~2,900 tweets/sec = ~3.7 MB/s
- Timeline reads: 500M DAU × 10 reads/day = 5B reads/day
- Read bandwidth: 5B × 1 KB = ~5 TB/day = ~58 MB/s
- Media CDN bandwidth: 50 TB/day = ~580 MB/s

Fanout Estimates:

- Average followers per user: 200
- Power users (celebrities): 10M+ followers
- Fanout writes: 250M tweets × 200 followers = 50B fanout writes/day
- For power users: single tweet to 10M followers = 10M writes

```

## API Design

```yaml
# Tweet Operations
POST /api/v1/tweets
  Request:
    {
      "content": "Hello World!",
      "media_ids": ["media_123", "media_456"],
      "in_reply_to_id": null
    }
  Response:
    {
      "tweet_id": "tweet_789",
      "content": "Hello World!",
      "author": {
        "id": "usr_123",
        "name": "John Doe",
        "handle": "@johndoe"
      },
      "created_at": "2025-01-15T10:30:00Z",
      "like_count": 0,
      "retweet_count": 0,
      "media_urls": ["https://media.twitter.com/..."],
      "liked": false,
      "retweeted": false
    }

# Timeline
GET /api/v1/timeline?limit=20&cursor=next_token
  Response:
    {
      "tweets": [...],
      "next_cursor": "next_token",
      "has_more": true
    }

GET /api/v1/home_timeline?limit=20
  Response:
    {
      "tweets": [
        {"tweet_id": "tweet_789", "author": {...}, "content": "...", ...}
      ],
      "meta": {"new_tweets_count": 5}
    }

# Follow/Unfollow
POST /api/v1/friendships/create
  Request: { "user_id": "usr_456" }

POST /api/v1/friendships/destroy
  Request: { "user_id": "usr_456" }

# Like/Retweet
POST /api/v1/tweets/{tweet_id}/like
POST /api/v1/tweets/{tweet_id}/retweet
POST /api/v1/tweets/{tweet_id}/reply
  Request: { "content": "Great post!" }

# Search
GET /api/v1/search?q=hashtag&count=20
```

## Database Design
### Schema

```sql
-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    handle VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    bio TEXT,
    profile_image_url TEXT,
    follower_count BIGINT DEFAULT 0,
    following_count BIGINT DEFAULT 0,
    tweet_count BIGINT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_handle ON users(handle);
CREATE INDEX idx_users_created ON users(created_at);

-- Tweets table (partitioned by created_at)
CREATE TABLE tweets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    content VARCHAR(280) NOT NULL,
    media_urls TEXT[],          -- Array of URLs
    in_reply_to_id BIGINT,
    retweet_of_id BIGINT REFERENCES tweets(id),
    like_count BIGINT DEFAULT 0,
    retweet_count BIGINT DEFAULT 0,
    reply_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_tweets_user ON tweets(user_id, created_at DESC);
CREATE INDEX idx_tweets_reply ON tweets(in_reply_to_id);
CREATE INDEX idx_tweets_retweet ON tweets(retweet_of_id);

-- Follows table
CREATE TABLE follows (
    follower_id BIGINT NOT NULL REFERENCES users(id),
    followee_id BIGINT NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_follows_followee ON follows(followee_id);

-- Likes table
CREATE TABLE likes (
    user_id BIGINT NOT NULL REFERENCES users(id),
    tweet_id BIGINT NOT NULL REFERENCES tweets(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tweet_id)
);

CREATE INDEX idx_likes_tweet ON likes(tweet_id);

-- Timeline (fanout cache - Redis primary, DB backup)
CREATE TABLE timeline_entries (
    user_id BIGINT NOT NULL,
    tweet_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, tweet_id)
) PARTITION BY HASH (user_id);

-- Hashtags
CREATE TABLE hashtags (
    id BIGSERIAL PRIMARY KEY,
    hashtag VARCHAR(100) UNIQUE NOT NULL,
    last_tweeted_at TIMESTAMP,
    tweet_count BIGINT DEFAULT 0
);

CREATE INDEX idx_hashtags_name ON hashtags(hashtag);

-- Tweet-hashtag mapping
CREATE TABLE tweet_hashtags (
    tweet_id BIGINT REFERENCES tweets(id),
    hashtag_id BIGINT REFERENCES hashtags(id),
    PRIMARY KEY (tweet_id, hashtag_id)
);
```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users    │     │    tweets       │     │    hashtags     │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ user_id (FK)    │     │ id (PK)         │
│ handle (UK) │     │ id (PK)         │◄────│ hashtag (UK)    │
│ name        │     │ content         │     │ last_tweeted_at │
│ email (UK)  │     │ media_urls      │     └─────────────────┘
│ follower_cnt│     │ in_reply_to_id  │              │
│ following_cnt│    │ retweet_of_id   │              │
│ tweet_count │     │ like_count      │              ▼
│ is_verified │     │ retweet_count   │     ┌─────────────────┐
│ created_at  │     │ reply_count     │     │ tweet_hashtags  │
└─────────────┘     │ created_at      │     ├─────────────────┤
        │           └─────────────────┘     │ tweet_id (FK)   │
        │                    │              │ hashtag_id (FK) │
        ▼                    ▼              └─────────────────┘
┌─────────────────┐  ┌─────────────────┐
│    follows      │  │    likes        │
├─────────────────┤  ├─────────────────┤
│ follower_id(FK) │  │ user_id (FK)    │
│ followee_id(FK) │  │ tweet_id (FK)   │
│ created_at      │  │ created_at      │
└─────────────────┘  └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                     Clients (Web/Mobile)                          │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway         │
                    │   (Rate Limiting,     │
                    │    Authentication)    │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Tweet Service  │  │  Timeline       │  │  Social Graph   │
│  (CRUD tweets)  │  │  Service        │  │  Service        │
└────────┬────────┘  │  (Fanout/Read)  │  │  (Follow/Unfollow)
         │           └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Kafka Cluster  │
                    │ (Async Fanout)   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ PostgreSQL  │  │   Redis     │  │  Media CDN  │
     │  (Tweets,   │  │ (Timeline,  │  │ (Images,    │
     │   Users)    │  │  Trending)  │  │  Videos)    │
     └─────────────┘  └─────────────┘  └─────────────┘
              │              │
              │              ▼
              │     ┌─────────────────┐
              └────►│  Elasticsearch  │
                    │  (Search/Trend) │
                    └─────────────────┘
```

## Key Components

### Timeline Fanout Service

The core challenge is efficiently distributing tweets to followers. Two approaches are used depending on user type:

```python
import asyncio
from enum import Enum

class FanoutStrategy(Enum):
    PUSH = "fanout_on_write"   # Pre-compute timeline
    PULL = "fanout_on_read"    # Compute on demand

class TimelineFanoutService:
    def __init__(self, redis_client, db, kafka_producer):
        self.redis = redis_client
        self.db = db
        self.kafka = kafka_producer
        self.fanout_threshold = 100_000  # Users with >100K followers use pull

    async def fanout_tweet(self, tweet: dict, author_id: str):
        """Fanout a new tweet to all followers' timelines."""
        follower_count = await self.get_follower_count(author_id)

        if follower_count > self.fanout_threshold:
            # Celebrity: Use fanout-on-read (pull model)
            await self.fanout_celebrity(tweet, author_id)
        else:
            # Regular user: Use fanout-on-write (push model)
            await self.fanout_regular(tweet, author_id)

    async def fanout_regular(self, tweet: dict, author_id: str):
        """Push tweet to all followers' timeline caches."""
        # Get followers from social graph service
        followers = await self.get_followers(author_id)

        # Batch fanout via Redis pipeline
        pipeline = self.redis.pipeline()
        for follower_id in followers:
            timeline_key = f"timeline:{follower_id}"
            pipeline.lpush(timeline_key, tweet['id'])
            pipeline.ltrim(timeline_key, 0, 800)  # Keep last 800 tweets

        await pipeline.execute()

        # Also fanout to Kafka for persistent storage
        await self.kafka.send('timeline.fanout', {
            'tweet_id': tweet['id'],
            'author_id': author_id,
            'follower_ids': followers
        })

    async def fanout_celebrity(self, tweet: dict, author_id: str):
        """For celebrities, just store the tweet. Pull on read."""
        # Store celebrity tweet metadata in cache
        await self.redis.zadd(
            f"celebrity_tweets:{author_id}",
            {tweet['id']: tweet['created_at']},
            nx=True
        )
        await self.redis.zremrangebyrank(
            f"celebrity_tweets:{author_id}",
            0, -1000  # Keep last 1000 tweets
        )

    async def get_timeline(self, user_id: str, limit: int = 20) -> list:
        """Get user's home timeline, merging push + pull sources."""
        timeline = []

        # 1. Get pre-computed timeline from Redis (push-based)
        timeline_key = f"timeline:{user_id}"
        tweet_ids = await self.redis.lrange(timeline_key, 0, limit - 1)
        timeline.extend(tweet_ids)

        # 2. Get IDs of users with pull-based fanout
        pull_followees = await self.get_pull_followees(user_id)

        # 3. Merge celebrity tweets (pull-based)
        for celeb_id in pull_followees:
            celeb_tweets = await self.redis.zrevrange(
                f"celebrity_tweets:{celeb_id}",
                0, limit - 1
            )
            timeline.extend(celeb_tweets)

        # 4. Sort by timestamp, limit, and hydrate
        return await self.hydrate_tweets(sorted(
            set(timeline),
            key=lambda x: x['created_at'],
            reverse=True
        )[:limit])

```

### Tweet Hydration Service

```python
class TweetHydrationService:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db

    async def hydrate_tweets(self, tweet_ids: list,
                             current_user_id: str = None) -> list:
        """Fetch full tweet objects with user context."""
        hydrated = []
        pipeline = self.redis.pipeline()

        # Batch fetch from cache
        for tweet_id in tweet_ids:
            pipeline.hgetall(f"tweet:{tweet_id}")

        cached = await pipeline.execute()

        for i, tweet_data in enumerate(cached):
            if tweet_data:
                tweet = self.parse_tweet_data(tweet_data, tweet_ids[i])
            else:
                # Cache miss - fetch from DB
                tweet = await self.db.get_tweet(tweet_ids[i])
                # Cache for future
                await self.cache_tweet(tweet)

            if tweet and not tweet.get('is_deleted'):
                hydrated.append(tweet)

        return hydrated

    async def cache_tweet(self, tweet: dict):
        """Cache tweet in Redis with TTL."""
        key = f"tweet:{tweet['id']}"
        self.redis.hset(key, mapping={
            'id': tweet['id'],
            'user_id': tweet['user_id'],
            'content': tweet['content'],
            'created_at': tweet['created_at'].isoformat(),
            'like_count': tweet['like_count'],
            'retweet_count': tweet['retweet_count'],
            'reply_count': tweet['reply_count'],
        })
        self.redis.expire(key, 3600)  # 1 hour TTL
```

### Trending Topics Service

```python
from datetime import datetime, timedelta
import re
from collections import Counter

class TrendingTopicsService:
    def __init__(self, redis_client, kafka_consumer):
        self.redis = redis_client
        self.trending_window = 3600  # 1 hour window

    async def process_tweet_for_trends(self, tweet: dict):
        """Extract hashtags and update trending scores."""
        hashtags = re.findall(r'#(\w+)', tweet['content'])

        for tag in hashtags:
            # Increment score in trending sorted set
            self.redis.zincrby(
                'trending',
                1,
                tag.lower()
            )

            # Store tweet ID for context
            self.redis.sadd(f"trending:tweets:{tag.lower()}",
                           tweet['id'])

    async def get_trending(self, limit: int = 10) -> list:
        """Get top trending topics globally or by location."""
        # Decay scores over time (exponential decay)
        # ZINCRBY with weight based on recency
        trending = self.redis.zrevrange(
            'trending',
            0, limit - 1,
            withscores=True
        )

        return [
            {
                'hashtag': f"#{tag}",
                'tweet_count': int(score),
                'category': self.categorize_hashtag(tag)
            }
            for tag, score in trending
        ]

    async def decay_trends(self):
        """Periodically decay old trends (run every 15 min)."""
        # Decay all scores by 5% every 15 minutes
        pipeline = self.redis.pipeline()
        for tag in self.redis.zrange('trending', 0, -1):
            pipeline.zincrby('trending', -0.05, tag)
        pipeline.execute()

        # Remove trends below threshold
        self.redis.zremrangebyscore('trending', 0, 1)
```

### Search Service

```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

class TweetSearchService:
    def __init__(self):
        self.es = Elasticsearch(['http://search-cluster:9200'])
        self.index = 'tweets'

    async def index_tweet(self, tweet: dict):
        """Index a tweet for search."""
        doc = {
            'content': tweet['content'],
            'user_id': tweet['user_id'],
            'user_handle': tweet['user_handle'],
            'user_name': tweet['user_name'],
            'hashtags': self.extract_hashtags(tweet['content']),
            'mentions': self.extract_mentions(tweet['content']),
            'like_count': tweet['like_count'],
            'retweet_count': tweet['retweet_count'],
            'created_at': tweet['created_at']
        }

        self.es.index(
            index=self.index,
            id=tweet['id'],
            body=doc,
            refresh='wait_for'  # Ensure real-time search
        )

    async def search(self, query: str, limit: int = 20,
                     cursor: dict = None) -> dict:
        """Search tweets with relevance scoring."""
        s = Search(using=self.es, index=self.index)

        # Build query
        must_queries = [
            Q('multi_match', query=query,
              fields=['content^3', 'hashtags^2', 'user_name'])
        ]

        if cursor:
            must_queries.append(
                Q('range', created_at={'lt': cursor['created_at']})
            )

        s = s.query(Q('bool', must=must_queries))
        s = s.sort({'_score': 'desc'}, {'created_at': 'desc'})
        s = s.extra(size=limit)

        response = s.execute()

        return {
            'results': [hit.to_dict() for hit in response],
            'total': response.hits.total.value,
            'next_cursor': self.get_next_cursor(response)
        }

    def extract_hashtags(self, content: str) -> list:
        return re.findall(r'#(\w+)', content)

    def extract_mentions(self, content: str) -> list:
        return re.findall(r'@(\w+)', content)
```

## Caching Strategy (Redis)

### Timeline Cache

```python
class TimelineCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_timeline_size = 800  # tweets per user

    async def add_to_timeline(self, user_id: str, tweet_id: str):
        key = f"timeline:{user_id}"
        self.redis.lpush(key, tweet_id)
        self.redis.ltrim(key, 0, self.max_timeline_size - 1)
        self.redis.expire(key, 86400)  # 24 hour TTL

    async def get_timeline(self, user_id: str, start: int = 0,
                           end: int = 19) -> list:
        key = f"timeline:{user_id}"
        return self.redis.lrange(key, start, end)

    async def merge_timelines(self, user_id: str,
                              celeb_tweets: list) -> list:
        """Merge regular timeline with celebrity pull tweets."""
        key = f"timeline:{user_id}"
        regular_ids = self.redis.lrange(key, 0, -1)
        all_ids = set(regular_ids) | set(celeb_tweets)
        return sorted(all_ids, reverse=True)[:20]
```

### Tweet Cache

```python
class TweetCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600

    async def cache_tweet(self, tweet: dict):
        self.redis.hset(f"tweet:{tweet['id']}", mapping={
            'id': str(tweet['id']),
            'user_id': str(tweet['user_id']),
            'content': tweet['content'],
            'like_count': str(tweet['like_count']),
            'retweet_count': str(tweet['retweet_count']),
            'reply_count': str(tweet['reply_count']),
            'created_at': tweet['created_at'].isoformat()
        })
        self.redis.expire(f"tweet:{tweet['id']}", self.default_ttl)

    async def get_tweet(self, tweet_id: str) -> dict:
        data = self.redis.hgetall(f"tweet:{tweet_id}")
        return data if data else None

    async def update_like_count(self, tweet_id: str,
                                increment: int = 1):
        self.redis.hincrby(f"tweet:{tweet_id}", 'like_count', increment)

    async def update_retweet_count(self, tweet_id: str,
                                   increment: int = 1):
        self.redis.hincrby(f"tweet:{tweet_id}",
                          'retweet_count', increment)
```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── tweet.created          (new tweet events)
├── tweet.deleted          (tweet deletion events)
├── timeline.fanout        (fanout write tasks)
├── like.created           (like events)
├── retweet.created        (retweet events)
├── follow.created         (new follows)
├── search.index           (tweet indexing for search)
├── trending.update        (trending recalculation triggers)
├── notification.send      (push notifications)

Partitioning Strategy:

- tweet.created: partition by user_id hash (ordering per user)
- timeline.fanout: partition by follower_id (balanced load)
- notification.send: partition by recipient_id
```

### Fanout Consumer

```python
from kafka import KafkaConsumer, KafkaProducer
import json

class FanoutConsumer:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
        self.batch_size = 100

        self.consumer = KafkaConsumer(
            'timeline.fanout',
            bootstrap_servers=['kafka1:9092'],
            group_id='timeline-fanout-worker',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_records=self.batch_size
        )

    async def process_batch(self):
        for message in self.consumer:
            data = json.loads(message.value.decode())
            tweet_id = data['tweet_id']
            author_id = data['author_id']
            follower_ids = data['follower_ids']

            # Batch write timeline entries to DB
            await self.db.batch_insert_timeline(
                [(fid, tweet_id, author_id)
                 for fid in follower_ids]
            )

            self.consumer.commit()
```

## Scaling Strategy

### Fanout Scaling

```text
Fanout Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Tweet Service                         │
│         (Receives tweet, publishes to Kafka)             │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Kafka Topic  │
                    │ tweet.created  │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │  Fanout      │ │  Fanout      │ │  Fanout      │
     │  Worker 1    │ │  Worker 2    │ │  Worker N    │
     │  (100K/s)    │ │  (100K/s)    │ │  (100K/s)    │
     └──────────────┘ └──────────────┘ └──────────────┘
              │             │             │
              └─────────────┼─────────────┘
                            │
                    ┌───────┴───────┐
                    │  Redis Cluster │
                    │ (Timeline      │
                    │  Caches)       │
                    └───────────────┘
```

### Database Scaling

```python
class TweetShardRouter:
    def __init__(self, num_shards: int = 64):
        self.num_shards = num_shards

    def get_tweet_shard(self, tweet_id: int) -> int:
        return tweet_id % self.num_shards

    def get_user_shard(self, user_id: int) -> int:
        # Consistent hashing for user data
        return (user_id * 7 + 3) % self.num_shards
```

## Failure Handling

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| Redis timeline cache down | Fall back to DB timeline, serve slightly stale data |
| Kafka broker failure | Buffer tweets locally, replay when available |
| Database primary down | Promote read replica, read-only mode during failover |
| Search cluster degraded | Return tweets sorted by time as fallback |
| Media CDN failure | Serve placeholder images, retry with alternative CDN |

### Graceful Degradation

```python
class TimelineFallback:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def get_timeline_with_fallback(self, user_id: str,
                                         limit: int = 20) -> list:
        # Try Redis first
        try:
            tweet_ids = self.redis.lrange(
                f"timeline:{user_id}", 0, limit - 1
            )
            if tweet_ids:
                return await self.hydrate(tweet_ids)
        except RedisConnectionError:
            pass  # Fall through to DB

        # Fallback to database
        tweets = await self.db.get_timeline_from_db(
            user_id, limit
        )
        return tweets
```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - tweets_per_second
  - timeline_load_latency_p50_p95_p99
  - fanout_latency_per_tweet
  - like_to_tweet_ratio
  - trending_topic_velocity

System Metrics:

  - fanout_worker_throughput
  - redis_timeline_hit_ratio
  - kafka_consumer_lag_per_partition
  - database_connection_pool_usage
  - cache_miss_rate

Infrastructure Metrics:

  - fanout_latency_by_user_type (regular vs celebrity)
  - timeline_merge_latency
  - search_query_latency
  - media_upload_throughput
```

### Alerting

```yaml
alerts:

  - name: Timeline Latency High
    condition: p95_timeline_latency > 500ms for 5 minutes
    severity: critical

  - name: Fanout Backlog
    condition: kafka_lag > 50000 for 2 minutes
    severity: warning

  - name: Cache Hit Ratio Low
    condition: timeline_cache_hit_ratio < 70%
    severity: warning

  - name: Tweet Rate Spike
    condition: tweets_per_second > 15000
    severity: info (autoscale trigger)
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Fanout Strategy | Push (fast reads, heavy writes) | Pull (slow reads, light writes) | Hybrid: push for regular, pull for celebrities |
| Timeline Storage | Redis (fast, volatile) | PostgreSQL (durable, slower) | Redis cache + DB persistence |
| Search | Elasticsearch (feature-rich) | PostgreSQL full-text (simpler) | Elasticsearch for search, PG for basic |
| Tweet ID Generation | Snowflake (ordered, unique) | UUID (unique, unordered) | Snowflake for time-ordered IDs |
| Real-time Updates | WebSocket (persistent) | Long-polling (simpler) | WebSocket for streaming, HTTP for API |

## Summary

The Twitter Feed system design covers:

- **Fanout at Scale**: Hybrid push/pull strategy for 500M DAU
- **Real-time Timeline**: Redis caching with celebrity tweet merging
- **Social Graph**: Efficient follow/unfollow with graph traversal
- **Trending**: Real-time hashtag velocity tracking with decay
- **Search**: Elasticsearch-powered full-text search with relevance

Key takeaways:

1. Use hybrid fanout: push for regular users, pull for celebrities

2. Cache aggressively with Redis (timeline, tweet hydration)

3. Process fanout asynchronously via Kafka for resilience

4. Use Snowflake for ordered, scalable tweet ID generation

5. Implement graceful degradation for timeline serving

This design handles 500M DAU with 10K tweets/second and sub-200ms timeline loading.

---

---

## Cheat Sheet
```text
TWITTER FEED SYSTEM DESIGN CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  The core challenge is efficiently distributing tweets to followers. Two approaches are used depending on user type:
```
```
  | Failure | Mitigation |
  |---------|------------|
  | Redis timeline cache down | Fall back to DB timeline, serve slightly stale data |
  | Kafka broker failure | Buffer tweets locally, replay when available |
  | Database primary down | Promote read replica, read-only mode during failover |
  | Search cluster degraded | Return tweets sorted by time as fallback |
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
- [REST APIs](../07-REST-API/)
- [WebSockets](../21-WebSockets/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [Designing Data-Intensive Applications](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321)
- [Twitter Engineering Blog](https://blog.twitter.com/engineering/en_us)
- [High Scalability - Twitter](http://highscalability.com/blog/2013/7/8/the-architecture-twitter-uses-to-process-over-100000-tweets-p.html)
