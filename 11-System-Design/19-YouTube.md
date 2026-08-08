---
section: System Design
category: Architecture
tags: [concept]
---

# YouTube System Design

## TL;DR

Design a video sharing and streaming platform supporting upload of multi-GB videos, transcoding to multiple formats/bitrates, delivery over CDN, recommendations, comments, and search — at YouTube-scale (500+ hours uploaded per minute, 2B+ users).

**Why it matters:** Tests the video processing pipeline (transcoding ladder, thumbnails, audio extraction), adaptive bitrate streaming (HLS/DASH), CDN economics, and the recommendation ML stack. The most important video-system-design question you'll see.

## Requirements

### Functional Requirements

- Upload videos up to 12 hours / 256 GB
- Transcode to multiple formats (240p, 360p, 480p, 720p, 1080p, 4K) and codecs (H.264, H.265, VP9, AV1)
- Stream with adaptive bitrate (ABR) over HLS / DASH
- Generate thumbnails (auto-pick frames at intervals)
- Search by title, description, tags
- View counts, likes, dislikes, comments
- Channel subscriptions and notifications
- Recommendations on home page and "Up next"
- Watch history and resume playback
- Live streaming (out of scope for core design, but mention)
- Embeddable player

### Non-Functional Requirements

- 2B+ monthly active users
- 500+ hours of video uploaded per minute (720K hours/day)
- 1B+ hours watched per day
- Time-to-first-byte (TTFB) < 200ms for hot content
- Rebuffer ratio < 0.5% (YouTube's own bar)
- 99.95% availability
- Multi-region with low-latency playback globally
- Content protection (DRM, signed URLs)

## Capacity Estimation

```text
Upload:
- 720K hours/day = 8.3 hours/sec
- Avg bitrate 8 Mbps → 8.3 hr × 3600 s × 8 Mbps = ~240 Gbps of raw upload bandwidth
- Storage: 720K hr/day × 1 GB/hr (compressed, avg) = 720 TB/day
- 5-year retention: 720 TB × 365 × 5 = 1.3 EB raw

Transcoding:
- Each video transcoded to 6 resolutions × 4 codecs = 24 output files
- Real-time factor 0.5× (transcode faster than playback)
- 8.3 hours/sec of source → 16.6 hours/sec of output across all formats
- Compute: ~50K–100K transcoding cores equivalent (FFmpeg clusters)

View Bandwidth:
- 1B hours watched/day × 5 Mbps avg = 5.7 Tbps average
- Peak: 4× = 23 Tbps (absorbed by CDN edge)

Storage Mix:
- Hot (last 30 days, 720K hr/day × 30 = 21.6M hr) on standard S3: 21.6 PB
- Cold (older) on Glacier-class storage: 1.3 EB minus hot = ~1.2 EB
- Metadata (PostgreSQL/Cassandra): 10B videos × 5 KB = 50 TB

```

## API Design

```yaml
# Upload (resumable)
POST /v1/videos/upload
  Headers:
    Authorization: Bearer <token>
    X-Upload-Token: <resumable_session_id>
    Content-Range: bytes 0-104857599/524288000
  Body: binary chunk
  Response: 200 { "received": "100MB", "video_id": "vid_abc", "status": "uploading" }

# Finalize upload
POST /v1/videos
  Body:
    {
      "upload_id": "upload_xyz",
      "title": "...",
      "description": "...",
      "tags": ["..."],
      "visibility": "public"
    }
  Response: { "video_id": "vid_abc", "status": "processing" }

# Get video metadata
GET /v1/videos/{video_id}
  Response:
    {
      "video_id": "vid_abc",
      "title": "...",
      "channel_id": "ch_42",
      "duration": 596,
      "thumbnail_urls": {
        "default": "https://i.ytimg.com/vi/vid_abc/default.jpg",
        "high": "https://i.ytimg.com/vi/vid_abc/hqdefault.jpg"
      },
      "playback_urls": {
        "hls": "https://manifest.example.com/vid_abc/master.m3u8",
        "dash": "https://manifest.example.com/vid_abc/manifest.mpd"
      },
      "view_count": 1234567
    }

# Stream manifest
GET /v1/videos/{video_id}/master.m3u8
  Response: HLS manifest (variant playlists for each rendition)

# Search
GET /v1/search?q=...&type=video
  Response: { "results": [...], "next_page": "..." }

```

## Database Design

### Schema (Cassandra or sharded PostgreSQL)

```sql
-- Videos (sharded by video_id)
CREATE TABLE videos (
    video_id        UUID PRIMARY KEY,
    channel_id      BIGINT NOT NULL,
    title           VARCHAR(100) NOT NULL,
    description     TEXT,
    tags            SET<TEXT>,
    duration_sec    INT,
    visibility      VARCHAR(20) NOT NULL,  -- 'public' | 'unlisted' | 'private'
    status          VARCHAR(20) NOT NULL,  -- 'uploading' | 'processing' | 'ready' | 'failed'
    view_count      BIGINT DEFAULT 0,
    like_count      INT DEFAULT 0,
    dislike_count   INT DEFAULT 0,
    comment_count   INT DEFAULT 0,
    upload_time     TIMESTAMP,
    publish_time    TIMESTAMP,
    manifest_url    TEXT,             -- HLS master manifest
    thumbnail_url   TEXT,
    encoding_done   BOOLEAN DEFAULT FALSE
);

-- Renditions (one row per output format)
CREATE TABLE renditions (
    video_id        UUID,
    resolution      VARCHAR(10),      -- '240p', '720p', etc.
    codec           VARCHAR(10),      -- 'h264', 'vp9', 'av1'
    bitrate_kbps    INT,
    storage_path    TEXT,
    PRIMARY KEY (video_id, resolution, codec)
);

-- Channels
CREATE TABLE channels (
    channel_id      BIGINT PRIMARY KEY,
    user_id         BIGINT,
    name            VARCHAR(100),
    subscriber_count BIGINT DEFAULT 0,
    video_count     INT DEFAULT 0
);

-- Views (write-heavy; append-only log → analytics; aggregated counter for display)
CREATE TABLE video_views (
    video_id        UUID,
    user_id         BIGINT,
    watched_at      TIMESTAMP,
    watch_duration  INT,
    PRIMARY KEY (video_id, user_id, watched_at)
);
```

## Architecture

### ASCII Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                      YOUTUBE-TYPE STACK                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Client (Mobile / Web / TV / Embed)                                 │
│       │                                                             │
│       ▼                                                             │
│  CDN Edge (multi-tenant, signed URLs)                              │
│       │                                                             │
│       ▼                                                             │
│  API Gateway (rate limit, auth, region routing)                     │
│       │                                                             │
│       ├──▶ Upload Service ──▶ Object Store (raw uploads)            │
│       │                                                                 │
│       ├──▶ Transcoding Pipeline (FFmpeg cluster / AWS MediaConvert)│
│       │              │                                              │
│       │              ├─▶ Multi-rendition output → Object Store     │
│       │              ├─▶ Thumbnail extractor → Image store         │
│       │              └─▶ Audio extraction (for transcripts)        │
│       │                                                                 │
│       ├──▶ Manifest Service (generates HLS/DASH manifests)         │
│       │                                                                 │
│       ├──▶ Metadata Service ──▶ Cassandra / sharded PG              │
│       │                                                                 │
│       ├──▶ Search Service ──▶ Elasticsearch (with custom ranking)  │
│       │                                                                 │
│       ├──▶ Recommendation Service (ML inference) ──▶ Vector store    │
│       │                                                                 │
│       ├──▶ Analytics Pipeline (Kafka → Spark / Flink → DW)         │
│       │                                                                 │
│       └──▶ Notification Service ──▶ APNs / FCM / Web Push          │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Upload Pipeline (Resumable + Chunked)

- Client requests a **resumable upload session**: `POST /v1/videos/upload` → returns `upload_id` and `X-Upload-URL`.
- Client PUTs the file in **5–10 MB chunks** directly to S3-compatible storage. Each chunk uses `Content-Range` headers so partial uploads can resume.
- On final chunk, S3 triggers an event (S3:ObjectCreated) → Upload Service finalizes and creates the `videos` row in `processing` status.

### Transcoding Pipeline

- On upload completion, enqueue a `transcode` job to Kafka.
- Worker pool (Kubernetes + autoscaling) consumes jobs and runs **FFmpeg** with a per-codec/per-resolution command:
  - x264/720p: `-c:v libx264 -preset medium -crf 23 -vf scale=-2:720 -c:a aac -b:a 128k`
  - VP9/720p: `-c:v libvpx-vp9 -b:v 1800k -vf scale=-2:720 -c:a libopus`
  - AV1/720p: `-c:v libaom-av1 -crf 32 -vf scale=-2:720`
- Each rendition output is written to S3; renditions are registered in the `renditions` table.
- Thumbnail extraction: `ffmpeg -i input -vf "select=eq(n\,30)" -vframes 1 thumb_30.jpg` at multiple intervals.
- On all renditions complete → set `encoding_done=true`, generate HLS manifest, update `videos.status=ready`.

### Adaptive Bitrate Streaming

HLS / DASH masters list multiple variant playlists (one per rendition). The player monitors bandwidth and re-fetches the variant playlist, swapping to a higher bitrate when buffer fills and lower when it empties.

```text
Master manifest (master.m3u8):
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-STREAM-INF:BANDWIDTH=400000,RESOLUTION=426x240
240p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360
360p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720
720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
1080p.m3u8

Variant playlist (e.g., 720p.m3u8) — points to 6-second segments:
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-TARGETDURATION:6
#EXTINF:6.0,
seg_001.ts
#EXTINF:6.0,
seg_002.ts
...
```

## Caching Strategy

| Cache | Stores | TTL | Invalidation |
|---|---|---|---|
| CDN edge | Video segments (HLS .ts/.mp4) | 30 days | Versioned URLs (manifest hash in path) |
| CDN edge | Master + variant manifests | 5 min | Event-driven purge on re-encode |
| Redis | Video metadata | 1 hour | Delete on update |
| Memcached | View counts, like counts | 30s | Counter reconciliation from Kafka |
| Browser | Player JS/CSS, poster images | 1 year | Content-hash in URL |

## Message Queue

Kafka topics:
- `video.uploaded` → triggers transcoding
- `video.transcoded` → triggers manifest generation + notification
- `video.viewed` → counter increment, recommendation pipeline, analytics
- `comment.created` → counter, notification, moderation
- `subscription.created` → notification fan-out

Use **partition by video_id** for ordered processing per video.

## Scaling Strategy

| Bottleneck | Solution |
|---|---|
| Upload bandwidth saturates app servers | Direct-to-S3 with pre-signed URLs |
| Transcoding backlog spikes | Auto-scale FFmpeg worker pool on queue depth |
| CDN egress cost | Negotiate commit; consider multi-CDN (CloudFront + Fastly + Akamai) |
| Hot video (1B views/day) | CDN absorbs; origin shield for cache miss |
| Search index freshness | Dual-write; use Kafka to stream `videos.ready` → Elasticsearch bulk indexer |
| Recommendation latency | Pre-compute top-K per user; refresh hourly |
| Comments deep pagination | Cursor-based; restrict to first 1000 in API |

## Failure Handling

| Failure | Mitigation |
|---|---|
| S3 region down | Multi-region replication for new uploads; degraded playback OK |
| Transcoding worker dies | Job re-queue; idempotent (rendition is keyed by video_id + format) |
| CDN cache miss for hot video | Origin shield with read-through cache; serve next-best edge |
| Recommendation service down | Fall back to "Popular in your country" or "Recently uploaded by subscriptions" |
| Elasticsearch down | Fall back to DB LIKE search (slow but available) |
| Live stream ingestion failure | Switch to redundant RTMP endpoint; alert on bitrate drop |

## Monitoring

- **CDN metrics**: hit rate, origin offload, egress bandwidth
- **Pipeline**: upload success rate, transcode queue lag, transcode failure rate
- **Playback**: rebuffer ratio, video startup time, average bitrate delivered
- **Storage**: S3 object count, transcoded output size
- **Engagement**: view-through rate, average view duration, like ratio
- **Search**: query latency, click-through rate, zero-result rate

Alerts: transcode lag > 5 min, CDN origin offload < 80%, rebuffer ratio > 1%, upload failure rate > 0.5%.

## Trade-offs

| Decision | Option A | Option B | Choice |
|---|---|---|---|
| Transcoding | Self-managed FFmpeg on K8s | AWS MediaConvert / GCP Transcoder API | Self-managed at scale, managed for small teams |
| Codec focus | H.264 only (universal) | H.264 + VP9 + AV1 | All three (saves 30% bandwidth at cost of compute) |
| Storage | All on standard S3 | Tiered (hot/warm/cold) | Tiered after 30 days |
| Search | Elasticsearch | Algolia / Typesense | Elasticsearch (cost + control) |
| Recommendation | Rule-based | ML (deep ranking) | ML (drives 70%+ of watch time) |
| Live streaming | Custom RTMP + HLS | Mux / Agora (managed) | Custom for scale, managed for SMB |
| DRM | Widevine / FairPlay | None | DRM (required by studios) |

## Summary

- **Upload**: Direct-to-S3 resumable; bypasses app servers.
- **Transcoding**: Async pipeline via Kafka + FFmpeg cluster; multiple renditions for ABR.
- **Streaming**: HLS/DASH with master + variant manifests; CDN-edge delivery.
- **Discovery**: Elasticsearch for text search; ML ranking for recommendations.
- **Scale**: 23 Tbps of peak playback is entirely CDN-absorbing; the origin is for cold-start only.
- **Cost**: The single biggest line item is CDN egress — multi-CDN and codec choice (AV1) are the main levers.

---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [Netflix](04-Netflix.md) (similar CDN + streaming focus)
- [System Design Interview Questions](16-Interview-Questions.md)
- [URL Shortener](01-URL-Shortener.md)

## References & Learn More

- [YouTube Engineering Blog](https://youtube-eng.googleblog.com/)
- [YouTube Architecture — High Scalability](http://highscalability.com/blog/2012/2/6/youtube-architecture-1-billion-viewsday.html)
- [HLS Specification (RFC 8216)](https://datatracker.ietf.org/doc/html/rfc8216)
- [DASH-IF Guidelines](https://dashif.org/)
- [Alex Xu — System Design Vol 2 (YouTube chapter)](https://bytebytego.com/)
- [FFmpeg Wiki — Encoding for Streaming](https://trac.ffmpeg.org/wiki/EncodingForStreamingSites)
