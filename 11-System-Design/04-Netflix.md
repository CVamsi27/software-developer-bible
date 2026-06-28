# Netflix System Design

## Requirements
### Functional Requirements
- Stream video content on demand
- Personalized content recommendations
- Multiple user profiles per account
- Watch history and resume playback
- Content search and browsing
- Download for offline viewing
- Parental controls
- Multiple device support (TV, mobile, web)
- Subtitles and audio tracks
- 4K/HDR streaming support

### Non-Functional Requirements
- High availability (99.99%)
- Global content delivery (< 50ms latency)
- Adaptive streaming quality
- Support 200M+ subscribers
- Handle 15M concurrent streams
- Minimal buffering (< 1% rebuffer rate)
- Content protection (DRM)
- Cross-device synchronization

## Capacity Estimation
```
Storage Estimates:
- 15M concurrent streams × 5 Mbps = 75 Tbps bandwidth
- 200M users × 2 hours/day × 100 MB/hour = 40 PB/month viewing
- Content library: 100K hours × 1 GB/hour = 100 TB raw
- With multiple qualities: 100 TB × 10 = 1 PB

Bandwidth Estimates:
- Peak: 15M × 5 Mbps = 75 Tbps (global CDN)
- Average: 50 Tbps
- CDN edge servers: 10,000+ globally

Encoding Estimates:
- Each title encoded in 10+ formats (4K, 1080p, 720p, etc.)
- 100K titles × 10 formats × 50 GB = 50 PB storage
- Encoding time: 1 hour of content × 10 formats × 1000 parallel = 10K hours
```

## API Design
```yaml
# Content Discovery
GET /api/v1/browse
  Query: ?genre=action&language=en&page=1
  Response:
    {
      "categories": [
        {
          "name": "Trending Now",
          "items": [...]
        },
        {
          "name": "Continue Watching",
          "items": [...]
        }
      ]
    }

GET /api/v1/content/{content_id}
  Response:
    {
      "id": "cnt_123",
      "title": "Stranger Things",
      "description": "...",
      "genres": ["sci-fi", "horror"],
      "rating": "TV-14",
      "seasons": 4,
      "episodes": [...],
      "thumbnail": "https://cdn.example.com/thumb.jpg",
      "trailer": "https://cdn.example.com/trailer.mp4"
    }

# Playback
GET /api/v1/play/{content_id}
  Response:
    {
      "manifest_url": "https://manifest.example.com/manifest.mpd",
      "drm_token": "...",
      "playback_session_id": "sess_456",
      "bitrate_options": [1000, 2500, 5000, 8000, 15000]
    }

# User Profile
GET /api/v1/profile/{profile_id}
  Response:
    {
      "id": "prof_789",
      "name": "John",
      "avatar": "...",
      "maturity_rating": "R",
      "language": "en",
      "autoplay_next": true
    }

# Watch History
POST /api/v1/watch/{content_id}/progress
  Request:
    {
      "progress_seconds": 1200,
      "duration_seconds": 2700,
      "bitrate": 5000
    }
```

## Database Design
### Schema
```sql
-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    subscription_tier VARCHAR(20) NOT NULL,
    country VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Profiles table (multiple per user)
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    maturity_rating VARCHAR(10) DEFAULT 'ALL',
    language VARCHAR(10) DEFAULT 'en',
    autoplay_next BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content table
CREATE TABLE content (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(10) NOT NULL, -- 'movie' or 'series'
    title VARCHAR(500) NOT NULL,
    description TEXT,
    release_year INT,
    rating VARCHAR(10),
    duration_minutes INT,
    thumbnail_url TEXT,
    poster_url TEXT,
    trailer_url TEXT,
    genres TEXT[],
    languages TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_content_genres ON content USING GIN(genres);
CREATE INDEX idx_content_release ON content(release_year);

-- Episodes table (for series)
CREATE TABLE episodes (
    id BIGSERIAL PRIMARY KEY,
    content_id BIGINT REFERENCES content(id),
    season_number INT NOT NULL,
    episode_number INT NOT NULL,
    title VARCHAR(500),
    description TEXT,
    duration_minutes INT,
    thumbnail_url TEXT,
    UNIQUE(content_id, season_number, episode_number)
);

-- Watch history
CREATE TABLE watch_history (
    id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT REFERENCES profiles(id),
    content_id BIGINT REFERENCES content(id),
    episode_id BIGINT,
    progress_seconds INT DEFAULT 0,
    duration_seconds INT,
    last_watched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    device_type VARCHAR(20)
);

CREATE INDEX idx_watch_history_profile ON watch_history(profile_id);
CREATE INDEX idx_watch_history_content ON watch_history(content_id);

-- Viewing preferences (for recommendations)
CREATE TABLE viewing_preferences (
    profile_id BIGINT REFERENCES profiles(id),
    genre VARCHAR(50),
    watch_count INT DEFAULT 0,
    total_watch_time INT DEFAULT 0,
    last_watched TIMESTAMP,
    PRIMARY KEY (profile_id, genre)
);

-- Subscriptions
CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    tier VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    payment_method VARCHAR(20)
);

-- Content metadata (for search)
CREATE TABLE content_metadata (
    content_id BIGINT PRIMARY KEY REFERENCES content(id),
    cast_members TEXT[],
    director VARCHAR(255),
    production_company VARCHAR(255),
    awards TEXT[],
    imdb_rating DECIMAL(3,1),
    search_vector tsvector
);

CREATE INDEX idx_content_search ON content_metadata USING GIN(search_vector);
```

### ER Diagram (ASCII)
```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users    │     │    profiles     │     │  watch_history  │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ user_id (FK)    │     │ id (PK)         │
│ email       │     │ id (PK)         │◄────│ profile_id (FK) │
│ password    │     │ name            │     │ content_id (FK) │──┐
│ subscription│     │ avatar_url      │     │ episode_id      │  │
│ country     │     │ maturity_rating │     │ progress_seconds│  │
└─────────────┘     │ language        │     │ last_watched    │  │
        │           └─────────────────┘     │ completed       │  │
        │                   │               └─────────────────┘  │
        ▼                   ▼                                  │
┌─────────────────┐ ┌─────────────────┐                        │
│  subscriptions  │ │viewing_prefs    │                        │
├─────────────────┤ ├─────────────────┤                        │
│ id (PK)         │ │ profile_id (FK) │                        │
│ user_id (FK)    │ │ genre           │                        │
│ tier            │ │ watch_count     │                        │
│ status          │ │ total_watch_time│                        │
│ start_date      │ └─────────────────┘                        │
│ end_date        │                                            │
└─────────────────┘                                            │
                                                               │
┌─────────────────┐     ┌─────────────────┐                    │
│    content      │     │    episodes     │                    │
├─────────────────┤     ├─────────────────┤                    │
│ id (PK)         │◄────│ content_id (FK) │                    │
│ type            │     │ id (PK)         │                    │
│ title           │     │ season_number   │                    │
│ description     │     │ episode_number  │                    │
│ release_year    │     │ title           │                    │
│ rating          │     │ duration        │                    │
│ genres[]        │     │ thumbnail_url   │                    │
│ languages[]     │     └─────────────────┘                    │
└─────────────────┘                                            │
        │                                                      │
        ▼                                                      │
┌─────────────────┐                                            │
│content_metadata │                                            │
├─────────────────┤                                            │
│ content_id (PK) │◄───────────────────────────────────────────┘
│ cast_members[]  │
│ director        │
│ search_vector   │
└─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│         (Smart TV, Mobile, Web, Gaming Console)                  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   Global CDN         │
                    │   (10,000+ edge      │
                    │    servers)          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   API Gateway        │
                    │   (Rate Limiting,    │
                    │    Authentication)   │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Content        │  │  User           │  │  Streaming      │
│  Service        │  │  Service        │  │  Service        │
│  (Discovery,    │  │  (Profiles,     │  │  (Playback,     │
│   Search)       │  │   History)      │  │   DRM)          │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Cassandra  │  │  Elasticsearch│
     │  (Users,     │  │  (Watch     │  │  (Content    │
     │   Content)   │  │   History)  │  │   Search)    │
     └─────────────┘  └─────────────┘  └─────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │  Recommendation      │
                    │  Engine (ML)         │
                    └──────────────────────┘
```

## Key Components

### Adaptive Bitrate Streaming
```python
class AdaptiveBitrateService:
    def __init__(self):
        self.bitrate_profiles = {
            '4K': {'bitrate': 15000, 'resolution': '3840x2160'},
            '1080p': {'bitrate': 8000, 'resolution': '1920x1080'},
            '720p': {'bitrate': 5000, 'resolution': '1280x720'},
            '480p': {'bitrate': 2500, 'resolution': '854x480'},
            '360p': {'bitrate': 1000, 'resolution': '640x360'}
        }

    def select_bitrate(self, bandwidth_bps: float,
                       device_capability: dict) -> str:
        # Select highest quality that fits bandwidth
        for quality, profile in self.bitrate_profiles.items():
            if (profile['bitrate'] * 1000 <= bandwidth_bps and
                self.meets_device_capability(profile, device_capability)):
                return quality

        return '360p'  # Fallback to lowest quality

    def generate_manifest(self, content_id: str,
                         qualities: list) -> dict:
        # Generate DASH/HLS manifest with multiple quality levels
        manifest = {
            'versions': ['DASH', 'HLS'],
            'qualities': []
        }

        for quality in qualities:
            profile = self.bitrate_profiles[quality]
            manifest['qualities'].append({
                'quality': quality,
                'bitrate': profile['bitrate'],
                'resolution': profile['resolution'],
                'url': f'https://manifests.example.com/{content_id}/{quality}/manifest.mpd'
            })

        return manifest
```

### Content Delivery Network (CDN)
```python
class CDNService:
    def __init__(self):
        self.edge_servers = {}  # region -> edge_server
        self.origin_servers = {}  # region -> origin_server

    async def get_content_url(self, content_id: str,
                              user_region: str) -> str:
        # Check if content is cached at edge
        edge_server = self.get_nearest_edge(user_region)

        if await self.is_cached(edge_server, content_id):
            return f"https://{edge_server}/content/{content_id}"

        # Cache miss - fetch from origin and cache
        origin_url = await self.fetch_from_origin(content_id)
        await self.cache_at_edge(edge_server, content_id, origin_url)

        return origin_url

    def get_nearest_edge(self, region: str) -> str:
        # Use GeoDNS to route to nearest edge
        return self.edge_servers.get(region, 'us-east.edge')

    async def prefetch_content(self, content_ids: list,
                               region: str):
        # Predictive prefetching based on popularity
        for content_id in content_ids:
            await self.cache_at_edge(
                self.get_nearest_edge(region),
                content_id
            )
```

### Video Transcoding Pipeline
```python
class TranscodingPipeline:
    def __init__(self):
        self.formats = [
            {'codec': 'h264', 'quality': '4K', 'bitrate': 15000},
            {'codec': 'h264', 'quality': '1080p', 'bitrate': 8000},
            {'codec': 'h264', 'quality': '720p', 'bitrate': 5000},
            {'codec': 'h264', 'quality': '480p', 'bitrate': 2500},
            {'codec': 'h264', 'quality': '360p', 'bitrate': 1000},
        ]

    async def transcode_content(self, source_url: str,
                                content_id: str) -> dict:
        tasks = []
        for fmt in self.formats:
            task = asyncio.create_task(
                self.transcode_single(source_url, content_id, fmt)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return {r['quality']: r['url'] for r in results}

    async def transcode_single(self, source_url: str,
                               content_id: str, format: dict) -> dict:
        # Use FFmpeg or cloud transcoding service
        output_url = f"s3://content/{content_id}/{format['quality']}/"

        await self.ffmpeg.transcode(
            input=source_url,
            output=output_url,
            codec=format['codec'],
            bitrate=f"{format['bitrate']}k",
            preset='medium'
        )

        return {
            'quality': format['quality'],
            'url': output_url,
            'codec': format['codec'],
            'bitrate': format['bitrate']
        }
```

### Recommendation Engine
```python
class RecommendationEngine:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def get_recommendations(self, profile_id: str,
                                  limit: int = 20) -> list:
        # Get user preferences
        preferences = await self.get_user_preferences(profile_id)

        # Get collaborative filtering results
        cf_results = await self.collaborative_filtering(profile_id)

        # Get content-based results
        cb_results = await self.content_based_filtering(preferences)

        # Combine and rank
        combined = self.merge_results(cf_results, cb_results)

        # Apply business rules (diversity, freshness)
        final = self.apply_business_rules(combined, profile_id)

        return final[:limit]

    async def collaborative_filtering(self, profile_id: str) -> list:
        # Find users with similar viewing patterns
        similar_users = await self.db.execute("""
            SELECT similar_profile_id, similarity
            FROM user_similarity
            WHERE profile_id = %s
            ORDER BY similarity DESC
            LIMIT 100
        """, (profile_id,))

        # Get content watched by similar users
        recommendations = await self.db.execute("""
            SELECT content_id, COUNT(*) as watch_count
            FROM watch_history
            WHERE profile_id IN (
                SELECT similar_profile_id FROM user_similarity
                WHERE profile_id = %s
            )
            AND content_id NOT IN (
                SELECT content_id FROM watch_history
                WHERE profile_id = %s
            )
            GROUP BY content_id
            ORDER BY watch_count DESC
            LIMIT 50
        """, (profile_id, profile_id))

        return recommendations

    async def content_based_filtering(self, preferences: dict) -> list:
        # Recommend content similar to what user likes
        genres = preferences.get('favorite_genres', [])

        recommendations = await self.db.execute("""
            SELECT id, title, genres
            FROM content
            WHERE genres && %s
            AND id NOT IN (
                SELECT content_id FROM watch_history
                WHERE profile_id = %s
            )
            ORDER BY release_year DESC, imdb_rating DESC
            LIMIT 50
        """, (genres, preferences['profile_id']))

        return recommendations
```

## Caching Strategy (Redis)

### Content Cache
```python
class ContentCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def cache_content_metadata(self, content_id: str,
                                     metadata: dict):
        key = f"content:{content_id}"
        await self.redis.hset(key, mapping=metadata)
        await self.redis.expire(key, 86400)  # 24 hours

    async def get_content_metadata(self, content_id: str) -> dict:
        key = f"content:{content_id}"
        return await self.redis.hgetall(key)

    async def cache_trending(self, region: str, content_ids: list):
        key = f"trending:{region}"
        await self.redis.delete(key)
        for i, content_id in enumerate(content_ids):
            await self.redis.zadd(key, {content_id: -i})  # Score by rank
        await self.redis.expire(key, 3600)  # 1 hour

    async def get_trending(self, region: str, limit: int = 20) -> list:
        key = f"trending:{region}"
        return await self.redis.zrange(key, 0, limit - 1)
```

### Session Cache
```python
class SessionCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def create_session(self, session_id: str,
                             user_data: dict):
        key = f"session:{session_id}"
        await self.redis.hset(key, mapping=user_data)
        await self.redis.expire(key, 1800)  # 30 minutes

    async def get_session(self, session_id: str) -> dict:
        key = f"session:{session_id}"
        return await self.redis.hgetall(key)

    async def update_watch_progress(self, session_id: str,
                                    content_id: str,
                                    progress: int):
        key = f"watch_progress:{session_id}:{content_id}"
        await self.redis.setex(key, 86400, progress)  # 24 hours
```

## Message Queue (Kafka)

### Topics and Events
```
Topics:
├── content.viewed          (playback events)
├── content.completed       (watch completion)
├── content.rated           (user ratings)
├── search.queries          (search analytics)
├── encoding.completed      (transcoding events)
└── recommendation.clicked  (recommendation clicks)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "content.viewed",
  "timestamp": "2025-01-15T10:30:00Z",
  "user_id": "usr_456",
  "profile_id": "prof_789",
  "content_id": "cnt_012",
  "data": {
    "progress_seconds": 1200,
    "duration_seconds": 2700,
    "bitrate": 5000,
    "device_type": "smart_tv"
  }
}
```

### Event Processing
```python
class ViewingEventProcessor:
    def __init__(self, kafka_consumer, db, recommendation_engine):
        self.consumer = kafka_consumer
        self.db = db
        self.recommendations = recommendation_engine

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'content.viewed':
                await self.handle_viewing_event(event)
            elif event['event_type'] == 'content.completed':
                await self.handle_completion_event(event)

    async def handle_viewing_event(self, event: dict):
        # Update watch history
        await self.db.update_watch_progress(
            event['profile_id'],
            event['content_id'],
            event['data']['progress_seconds']
        )

        # Update recommendation model
        await self.recommendations.update_user_profile(
            event['profile_id'],
            event['content_id'],
            event['data']['progress_seconds']
        )
```

## Scaling Strategy

### Global CDN Architecture
```
CDN Topology:
┌─────────────────────────────────────────────────────────┐
│                    Origin Servers                        │
│                    (3 regions: US, EU, APAC)             │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Regional    │   │  Regional    │   │  Regional    │
│  CDN         │   │  CDN         │   │  CDN         │
│  (US-East)   │   │  (EU-West)   │   │  (APAC)      │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Edge PoPs   │   │  Edge PoPs   │   │  Edge PoPs   │
│  (100+)      │   │  (80+)       │   │  (60+)       │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Database Scaling
```
Database Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Write Primary                          │
│                    (US-East)                             │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │  Read       │ │  Read       │ │  Read       │
     │  Replica    │ │  Replica    │ │  Replica    │
     │  (US-East)  │ │  (EU-West)  │ │  (APAC)     │
     └─────────────┘ └─────────────┘ └─────────────┘

Content Metadata: PostgreSQL with read replicas
Watch History: Cassandra for write-heavy workload
Search: Elasticsearch cluster
```

### Streaming Service Scaling
```python
class StreamingServiceScaler:
    def __init__(self):
        self.sessions = {}  # session_id -> server_id

    async def handle_playback_request(self, request: dict):
        # Route to least loaded server
        server = await self.get_least_loaded_server()

        # Create streaming session
        session = await self.create_session(server, request)

        # Return CDN URL for content
        cdn_url = await self.cdn.get_content_url(
            request['content_id'],
            request['user_region']
        )

        return {
            'session_id': session['id'],
            'stream_url': cdn_url,
            'server': server
        }

    async def get_least_loaded_server(self) -> str:
        # Use load balancer with health checks
        servers = await self.get_healthy_servers()
        return min(servers, key=lambda s: s['active_sessions'])
```

## Failure Handling

### Playback Failure Recovery
```python
class PlaybackRecovery:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [1, 3, 5]

    async def handle_playback_error(self, session_id: str,
                                    error: Exception):
        # Log error
        logger.error(f"Playback error: {error}")

        # Determine error type
        if isinstance(error, CDNError):
            # Switch to backup CDN
            return await self.switch_to_backup_cdn(session_id)

        elif isinstance(error, DRMError):
            # Refresh DRM token
            return await self.refresh_drm_token(session_id)

        elif isinstance(error, BandwidthError):
            # Reduce quality
            return await self.reduce_quality(session_id)

        # Generic retry
        for attempt in range(self.max_retries):
            try:
                await asyncio.sleep(self.retry_delays[attempt])
                return await self.retry_playback(session_id)
            except Exception:
                continue

        # All retries failed
        return await self.graceful_degradation(session_id)
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| CDN node failure | Automatic failover to next closest edge |
| Origin server down | Serve from regional cache |
| DRM service unavailable | Temporary offline license |
| Database failover | Read from replica |
| Recommendation engine down | Serve popular content |

### Graceful Degradation
```python
class GracefulDegradation:
    def __init__(self):
        self.fallback_content = {}  # region -> popular content

    async def get_content_with_fallback(self, content_id: str,
                                       region: str) -> dict:
        try:
            # Try primary content service
            return await self.content_service.get_content(content_id)
        except ServiceUnavailable:
            # Fallback to cached content
            cached = await self.cache.get_content(content_id)
            if cached:
                return cached

            # Last resort: serve popular content
            return await self.get_popular_content(region)
```

## Monitoring

### Key Metrics
```yaml
Business Metrics:
  - streams_per_minute
  - unique_viewers
  - average_watch_time
  - content_completion_rate
  - recommendation_click_rate

System Metrics:
  - playback_start_time_p95
  - rebuffer_rate
  - cdn_hit_ratio
  - encoding_queue_depth
  - api_response_time

Infrastructure Metrics:
  - server_cpu_usage
  - memory_usage
  - network_throughput
  - disk_io
  - cdn_bandwidth_utilization
```

### Alerting Rules
```yaml
alerts:
  - name: High Rebuffer Rate
    condition: rebuffer_rate > 1%
    severity: critical

  - name: CDN Cache Hit Low
    condition: cache_hit_ratio < 95%
    severity: warning

  - name: Encoding Queue Backlog
    condition: encoding_queue > 1000
    severity: warning

  - name: Playback Start Slow
    condition: p95_start_time > 5s
    severity: critical
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | PostgreSQL (ACID) | Cassandra (write-scale) | Both (different use cases) |
| Streaming | HLS (Apple) | DASH (Standard) | Both (device compatibility) |
| CDN | Multi-CDN | Single CDN | Multi-CDN (redundancy) |
| Encoding | H.264 (compatible) | H.265 (efficient) | Both (device support) |
| Recommendations | Collaborative filtering | Content-based | Hybrid approach |

## Interview Questions

### Design Questions
1. **How would you design Netflix's video streaming?**
   - Adaptive bitrate streaming (HLS/DASH)
   - Multi-CDN for global delivery
   - Client-side manifest parsing
   - DRM for content protection

2. **How does the recommendation engine work?**
   - Collaborative filtering (similar users)
   - Content-based filtering (similar content)
   - Deep learning for feature extraction
   - A/B testing for algorithm optimization

3. **How would you handle 15M concurrent streams?**
   - Global CDN with 10,000+ edge servers
   - Origin shield for cache hierarchy
   - Connection pooling and keep-alive
   - Regional load balancing

### Scaling Questions
4. **How do you scale content encoding?**
   - Distributed transcoding workers
   - Parallel encoding for different qualities
   - Cloud-based elastic scaling
   - Progress tracking and retry logic

5. **How do you handle global content delivery?**
   - Multi-region deployment
   - GeoDNS for routing
   - Predictive prefetching
   - Edge caching for popular content

### Trade-off Questions
6. **How do you balance quality vs bandwidth?**
   - Adaptive bitrate based on network conditions
   - Quality caps based on subscription tier
   - Offline quality options
   - Bandwidth saving modes

7. **How do you handle content protection (DRM)?**
   - Multi-DRM support (Widevine, FairPlay)
   - License server integration
   - Offline license management
   - Forensic watermarking

### Senior-level Questions
8. **How would you implement offline viewing?**
   - Secure download with DRM
   - Storage management on device
   - Expiration and renewal
   - Sync watch progress when online

9. **How do you optimize for different devices?**
   - Device capability detection
   - Quality profile selection
   - UI/UX adaptation
   - Codec support detection

10. **How would you implement live streaming?**
    - Low-latency HLS/DASH
    - Real-time encoding
    - Chat and interaction
    - DVR functionality

## Summary

The Netflix system design covers:
- **Global CDN**: 10,000+ edge servers for < 50ms latency
- **Adaptive Streaming**: Dynamic quality based on bandwidth
- **Personalization**: ML-powered recommendations
- **Scalability**: Handles 200M+ subscribers globally
- **Reliability**: Multi-CDN, graceful degradation

Key takeaways:
1. Use multi-CDN for redundancy and performance
2. Implement adaptive bitrate for optimal quality
3. Leverage ML for personalized recommendations
4. Design for global scale with regional deployment
5. Ensure content protection with DRM

This design supports 200M+ subscribers with 15M concurrent streams while maintaining < 1% rebuffer rate.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
