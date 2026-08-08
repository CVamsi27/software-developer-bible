---
section: System Design
category: Architecture
tags: [concept]
---

# Dropbox System Design

## TL;DR

Design a file synchronization service (Dropbox / iCloud Drive / OneDrive) supporting cross-device sync, offline edits, conflict resolution, file versioning, and share links — at petabyte scale.

**Why it matters:** The canonical file-sync problem. Tests **block-level deduplication**, **content-addressable storage**, **notification-based sync**, and **conflict resolution** (CRDT vs server-wins vs three-way merge). The architecture diverges sharply from "just upload to S3" because of the offline-first nature.

## Requirements

### Functional Requirements

- Upload / download files (up to 2 TB per file in modern Dropbox)
- Sync across multiple devices (desktop, mobile, web)
- Offline edits queued and replayed on reconnect
- Conflict resolution when same file edited on two devices
- Version history (30 days free, 1 year on paid plans)
- Share files / folders with permissions (view / edit)
- Public share links
- Selective sync (don't download all folders on a device)
- Deleted file recovery
- Bandwidth-efficient updates (only sync deltas)

### Non-Functional Requirements

- 700M+ registered users
- Sync completion < 5s for small edits on broadband
- File metadata visible < 1s after upload
- 99.9% availability
- Eventually consistent across devices
- Strong consistency per user for file ordering
- Idempotent sync operations (replay-safe)

## Capacity Estimation

```text
User & Files:
- 700M users
- Average user: 50 GB stored, 200 files
- Total files: 700M × 200 = 140B file metadata rows
- Total storage (with dedup): ~1 EB raw user data → ~600 PB on storage after dedup

Upload / Sync:
- 1B syncs/day = 11.5K events/sec average
- Average file: 1 MB → 11.5 GB/s aggregate upload
- Block-level updates: only changed blocks, often < 1% of file

Storage Mix:
- Block store (content-addressable): 600 PB
- Metadata (sharded PostgreSQL): 140B rows × 1 KB = 140 TB
- Version history: extra 50% storage multiplier
- Notification stream (Redis pub/sub): ephemeral, ~1M concurrent subscribers

```

## API Design

```yaml
# Get upload session (block-level)
POST /v2/files/upload_session/start
  Body: { "close": false }
  Response: { "session_id": "us_abc" }

PUT /v2/files/upload_session/append_v2
  Headers: X-Dropbox-Api-Arg: { "cursor": { "session_id": "...", "offset": 0 } }
  Body: binary block (4 MB)

POST /v2/files/upload_session/finish
  Body: { "cursor": { "session_id": "...", "offset": 4194304 }, "commit": { "path": "/file.pdf", "mode": "overwrite" } }
  Response: { "metadata": { "id": "id:abc", "path": "/file.pdf", "size": 4194304, "rev": "016..." } }

# List folder
POST /v2/files/list_folder
  Body: { "path": "/Photos", "recursive": false }
  Response: { "entries": [...], "cursor": "AAE..." }

# Long-poll for changes
POST /v2/files/list_folder/continue
  Body: { "cursor": "AAE..." }
  Response: { "entries": [...], "cursor": "AAE..." (with changes) }

# Download
POST /v2/files/download
  Body: { "path": "/file.pdf" }
  Response: binary (or 307 redirect to signed URL)

# Share
POST /v2/sharing/create_shared_link_with_settings
  Body: { "path": "/file.pdf", "settings": { "link_password": "...", "expires": "2026-12-31" } }
  Response: { "url": "https://db.tt/xyz", "expires": "2026-12-31" }

```

## Database Design

### Schema

```sql
-- File metadata (sharded by namespace_id, which is the user/team)
CREATE TABLE file_metadata (
    file_id        UUID PRIMARY KEY,
    namespace_id   BIGINT NOT NULL,       -- user_id or team_id
    path           TEXT NOT NULL,
    size_bytes     BIGINT,
    content_hash   CHAR(64) NOT NULL,     -- SHA-256 of file content
    block_hashes   BYTEA NOT NULL,        -- ordered list of block hashes
    revision       BIGINT NOT NULL,
    server_modified TIMESTAMPTZ NOT NULL,
    client_modified TIMESTAMPTZ NOT NULL,
    is_deleted     BOOLEAN DEFAULT FALSE,
    UNIQUE (namespace_id, path, server_modified DESC)
);

-- Blocks (content-addressable, dedup)
CREATE TABLE blocks (
    block_hash     CHAR(64) PRIMARY KEY,  -- SHA-256 of block contents
    size_bytes     INT NOT NULL,
    storage_path   TEXT NOT NULL,         -- S3 key
    ref_count      INT DEFAULT 1,         -- dedup accounting
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- File versions (history)
CREATE TABLE file_versions (
    file_id        UUID,
    revision       BIGINT,
    content_hash   CHAR(64),
    block_hashes   BYTEA,
    server_modified TIMESTAMPTZ,
    size_bytes     BIGINT,
    PRIMARY KEY (file_id, revision)
);

-- Changes stream (per-user cursor)
CREATE TABLE cursors (
    cursor_id      VARCHAR(64) PRIMARY KEY,
    namespace_id   BIGINT NOT NULL,
    last_revision  BIGINT NOT NULL
);
```

## Architecture

### ASCII Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                      DROPBOX-TYPE STACK                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Client (Desktop / Mobile / Web)                                    │
│  ┌────────────────────────────────────────────────────┐             │
│  │ Sync Agent (per device)                             │             │
│  │ ├── Local block store (chunked files)              │             │
│  │ ├── Local SQLite index (mirrors server metadata)   │             │
│  │ ├── Block-level diff engine (rsync-style)          │             │
│  │ └── Long-poll / websocket for change notifications │             │
│  └────────────────────────────────────────────────────┘             │
│       │                                                             │
│       ▼                                                             │
│  API Gateway (rate limit, auth, routing)                            │
│       │                                                             │
│       ├──▶ Block Service ──▶ S3 (content-addressable)              │
│       │         │                                                  │
│       │         └─▶ Metadata DB (sharded PostgreSQL)               │
│       │                                                                 │
│       ├──▶ Sync / Cursor Service ──▶ Redis pub/sub                  │
│       │                                                                 │
│       ├──▶ Share Service ──▶ Link DB + signed-URL service           │
│       │                                                                 │
│       ├──▶ Versioning Service ──▶ Cold storage (S3 IA)              │
│       │                                                                 │
│       └──▶ Notification Service ──▶ WebSocket / long-poll fleet     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Block-Level Chunking (4 MB blocks)

Files are split into **4 MB blocks** (the last block may be smaller). Each block is hashed with SHA-256. The file's `content_hash` is the Merkle tree root of the block hashes.

```python
BLOCK_SIZE = 4 * 1024 * 1024  # 4 MB

def chunk_file(file_path: str) -> List[Block]:
    blocks = []
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BLOCK_SIZE)
            if not data:
                break
            h = sha256(data).hexdigest()
            blocks.append(Block(hash=h, data=data))
    return blocks
```

The block hash is the **content address**: storage is keyed by hash, so identical blocks (across users, even) are deduplicated automatically.

### Block-Level Diff (Rsync-Style)

When a file is modified and re-synced:

1. Client computes the new list of block hashes.
2. Client sends the list to the server (`/upload_session/append_v2` with `content_hash` of each block).
3. Server checks which hashes it already has. **Missing blocks are uploaded; existing ones are skipped** — saving bandwidth.
4. If a 4 MB block is partially modified, the *entire block* is re-uploaded. (4 MB granularity is the standard trade-off; smaller blocks = more dedup but more metadata.)

```text
File v1:  [A][B][C][D][E]  (20 MB, 5 blocks)
File v2:  [A][B][X][D][E]  (20 MB, 5 blocks; block C changed → X)
                        ↑ re-upload only this 4 MB
```

### Content-Addressable Storage

```python
async def upload_block_if_missing(block_hash: str, data: bytes):
    exists = await s3_client.head_object(Bucket='blocks', Key=block_hash)
    if exists.status == 200:
        # Block already on S3 — no upload needed
        return False
    await s3_client.put_object(Bucket='blocks', Key=block_hash, Body=data)
    return True
```

When `ref_count` drops to zero (no file references the block), it's deleted by a GC job.

### Sync Algorithm (Cursor + Long-Poll)

1. Client maintains a `cursor` for its namespace.
2. Client calls `list_folder/continue` with the cursor — long-polls for changes (up to 90s).
3. Server holds the request open. When a change happens (write, delete, move), it wakes up all waiting clients for that namespace and returns the new entries.
4. Client applies the changes locally and updates its cursor.
5. If the client has been offline, it replays all changes since its last cursor.

### Conflict Resolution

Three cases when the same file changes on two devices while offline:

| Scenario | Resolution |
|---|---|
| Two devices edit **different files** | Both apply; no conflict |
| Two devices edit **same file**, no overlapping changes | Three-way merge (rare in Dropbox; usually only one survives) |
| Two devices edit **same file**, conflicting changes | Server-wins, original stored as a "conflicted copy" on the loser; user prompted |

Dropbox originally used server-wins. Modern file sync services (Notion, Linear) use **operational transforms** for true collaborative merging — but Dropbox's per-file model doesn't need OT.

## Caching Strategy

| Cache | Stores | TTL | Invalidation |
|---|---|---|---|
| CDN | Public share-link downloads | 1 hour | Signed URL expiration |
| Redis | File metadata, change cursors | 1 hour | DB write invalidation |
| Local client cache | Block data, metadata SQLite | Persistent | On-disk LRU + hash compare |
| Memcached | Hot block hashes (popular files) | 1 day | LRU |

## Message Queue

Kafka topics:
- `file.modified` → notification fan-out, version backup, share-link invalidation
- `block.uploaded` → dedup reference counter update
- `share.created` → share-link DB write, CDN warm

## Scaling Strategy

| Bottleneck | Solution |
|---|---|
| Block store grows unbounded | GC deletes orphaned blocks (ref_count = 0 and > 30 days old) |
| Metadata DB write contention | Shard by namespace_id; use read replicas for cursor reads |
| Long-poll fleet connection count | Use WebSocket with sticky routing; cap per-server connections |
| Sync notification fan-out | Pub/sub keyed by namespace_id; 1M concurrent subscribers per region |
| Mobile app on flaky network | Client-side exponential backoff + request queue + resume tokens |
| S3 LIST cost on block store | Use S3 Inventory + Athena for batch analysis, not real-time |

## Failure Handling

| Failure | Mitigation |
|---|---|
| Server misses a change event | Client detects divergence on next sync (hash compare); pulls diff |
| Long-poll request times out | Client immediately re-issues — at-least-once delivery |
| Two devices edit same file | Conflicted copy saved; user picks winner |
| Block GC deletes a referenced block | Reference count is incremented transactionally before commit; rollback on failure |
| S3 region outage | Cross-region replication for new blocks; old blocks eventually re-replicated |
| Client clock skew | Server-modified time is authoritative; client-modified time is informational only |

## Monitoring

- **Sync latency**: time from server commit to client apply (p50, p95, p99)
- **Long-poll health**: connection count, idle-timeout rate
- **Block dedup ratio**: dedup / total — drives effective storage cost
- **Conflict rate**: conflicted copies per 1K writes
- **Storage**: S3 object count, ref-count distribution, orphan-block count
- **Client**: app crashes, sync stalls, version-skew (server vs client metadata)

Alerts: sync p99 > 30s, long-poll fleet saturation, dedup ratio dropping, GC backlog > 1M blocks.

## Trade-offs

| Decision | Option A | Option B | Choice |
|---|---|---|---|
| Block size | 4 MB (Dropbox) | 128 KB (smaller) | 4 MB (less metadata, more dedup granularity cost) |
| Conflict resolution | Server-wins | CRDT / OT | Server-wins (per-file model doesn't need OT) |
| Notification transport | Long-poll | WebSocket | Both — long-poll for legacy, WS for new clients |
| Storage backend | S3 | HDFS / Ceph | S3 (managed, cost-effective) |
| Block dedup scope | Cross-user | Per-user only | Cross-user (huge savings on common files) |
| Versioning | Keep all versions | Keep last N | Configurable (30 days / 1 year / forever) |
| Mobile strategy | Full sync | On-demand | On-demand (selective sync) to save bandwidth |

## Summary

- **Block-level chunking** is the core innovation — turns "file sync" into a content-addressable dedup problem.
- **Content-addressable storage** deduplicates across users (a public PDF in 100K folders = 1 block on S3).
- **Cursor + long-poll** for change notifications — at-least-once delivery with client-side idempotency.
- **Server-wins conflict** is fine for per-file semantics; CRDTs only matter for collaborative editing.
- **Client is offline-first**: local SQLite index + persistent block cache + on-reconnect sync.
- **Cost levers**: dedup ratio, block size, version retention, cold-storage tiering.

---

## See Also
- [Database](../08-Database/)
- [Google Drive](05-Google-Drive.md) (related but different: collaborative editing model)
- [Microservices](../12-Microservices/)
- [System Design Interview Questions](16-Interview-Questions.md)
- [WhatsApp](02-WhatsApp.md)

## References & Learn More

- [How Dropbox Really Works — High Scalability](http://highscalability.com/blog/2011/3/14/tech-talk-dropbox-architecture.html)
- [Dropbox Tech Blog](https://dropbox.tech/)
- [Dropbox API Documentation](https://www.dropbox.com/developers/documentation)
- [System Design Primer — Dropbox](https://github.com/donnemartin/system-design-primer#design-dropbox)
- [Alex Xu — System Design Vol 2 (Dropbox chapter)](https://bytebytego.com/)
- [rsync algorithm (the foundation of block-level diff)](https://rsync.samba.org/tech_report.html)
