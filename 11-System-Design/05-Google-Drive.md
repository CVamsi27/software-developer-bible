# Google Drive System Design

## Requirements
### Functional Requirements
- Upload and download files
- File synchronization across devices
- Real-time collaboration on documents
- File sharing with permissions (view, edit, comment)
- Version history and rollback
- File search (name, content, metadata)
- Offline access with sync
- File organization (folders, labels)
- Trash and recovery
- Storage quota management

### Non-Functional Requirements
- Strong consistency for file operations
- High availability (99.99%)
- Support 1B+ files
- Handle 10M concurrent sync operations
- Real-time collaboration latency < 100ms
- Data durability (11 9s)
- End-to-end encryption option
- Cross-platform compatibility

## Capacity Estimation
```text
Storage Estimates:
- 1B files × 1 MB average = 1 PB
- With versions: 1 PB × 10 versions = 10 PB
- Metadata: 1B × 1 KB = 1 TB
- Total: ~11 PB

Bandwidth Estimates:
- 100M DAU × 10 MB sync/day = 1 PB/day = ~11.6 TB/s
- Peak: 5x = 58 TB/s
- Upload/download ratio: 30/70

File Operations:
- 10M concurrent sync operations
- 100K operations/second
- Average file size: 1 MB
- Throughput: 100 GB/s
```

## API Design
```yaml
# File Operations
POST /api/v1/files/upload
  Request: multipart/form-data
    file: binary
    parent_id: "folder_123"
    name: "document.pdf"
  Response:
    {
      "file_id": "file_456",
      "name": "document.pdf",
      "size": 1048576,
      "mime_type": "application/pdf",
      "version": 1,
      "created_at": "2025-01-15T10:30:00Z"
    }

GET /api/v1/files/{file_id}/download
  Response: binary stream with Content-Disposition

# File Listing
GET /api/v1/files
  Query: ?parent_id=folder_123&limit=100&cursor=abc
  Response:
    {
      "files": [...],
      "next_cursor": "def",
      "has_more": true
    }

# File Metadata
PUT /api/v1/files/{file_id}
  Request:
    {
      "name": "renamed_document.pdf",
      "starred": true
    }

# Sharing
POST /api/v1/files/{file_id}/permissions
  Request:
    {
      "type": "user",
      "email": "user@example.com",
      "role": "writer"
    }

# Version History
GET /api/v1/files/{file_id}/versions
  Response:
    {
      "versions": [
        {"version": 3, "size": 1048576, "modified_at": "..."},
        {"version": 2, "size": 1048500, "modified_at": "..."},
        {"version": 1, "size": 1048000, "modified_at": "..."}
      ]
    }

# Real-time Collaboration
WebSocket /api/v1/files/{file_id}/collaborate
  Messages:
    {
      "type": "operation",
      "user_id": "usr_123",
      "operations": [
        {"type": "insert", "position": 10, "text": "Hello"},
        {"type": "delete", "position": 20, "length": 5}
      ],
      "version": 123
    }
```

## Database Design
### Schema
```sql
-- Files table
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    size BIGINT DEFAULT 0,
    owner_id BIGINT REFERENCES users(id),
    parent_id BIGINT REFERENCES files(id),
    is_folder BOOLEAN DEFAULT FALSE,
    is_trashed BOOLEAN DEFAULT FALSE,
    is_starred BOOLEAN DEFAULT FALSE,
    version INT DEFAULT 1,
    checksum VARCHAR(64),
    content_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trashed_at TIMESTAMP,
    UNIQUE(owner_id, parent_id, name)
);

CREATE INDEX idx_files_parent ON files(parent_id);
CREATE INDEX idx_files_owner ON files(owner_id);
CREATE INDEX idx_files_name ON files USING GIN(to_tsvector('english', name));

-- File versions
CREATE TABLE file_versions (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES files(id),
    version INT NOT NULL,
    size BIGINT,
    checksum VARCHAR(64),
    storage_path TEXT NOT NULL,
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_id, version)
);

-- File permissions
CREATE TABLE file_permissions (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES files(id),
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(20) NOT NULL, -- 'owner', 'writer', 'commenter', 'reader'
    type VARCHAR(20) NOT NULL, -- 'user', 'group', 'domain'
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_id, user_id)
);

CREATE INDEX idx_permissions_file ON file_permissions(file_id);
CREATE INDEX idx_permissions_user ON file_permissions(user_id);

-- File shares
CREATE TABLE file_shares (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES files(id),
    share_link VARCHAR(255) UNIQUE,
    permission VARCHAR(20) NOT NULL,
    expires_at TIMESTAMP,
    password_hash VARCHAR(255),
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Collaborative editing operations
CREATE TABLE collaboration_operations (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES files(id),
    user_id BIGINT REFERENCES users(id),
    operation_type VARCHAR(20) NOT NULL,
    position INT,
    content TEXT,
    length INT,
    version INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_operations_file ON collaboration_operations(file_id, version);

-- Sync status per device
CREATE TABLE device_sync_status (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    device_id VARCHAR(255) NOT NULL,
    file_id BIGINT REFERENCES files(id),
    sync_status VARCHAR(20) NOT NULL, -- 'synced', 'pending', 'conflict'
    last_synced_at TIMESTAMP,
    UNIQUE(user_id, device_id, file_id)
);

-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    storage_quota BIGINT DEFAULT 15 * 1024 * 1024 * 1024, -- 15 GB
    storage_used BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ER Diagram (ASCII)
```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users    │     │     files       │     │ file_versions   │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ owner_id (FK)   │     │ id (PK)         │
│ email       │     │ id (PK)         │◄────│ file_id (FK)    │
│ name        │     │ name            │     │ version         │
│ storage_quota│    │ mime_type       │     │ size            │
│ storage_used│     │ size            │     │ checksum        │
└─────────────┘     │ parent_id (FK)──│──┐  │ storage_path    │
        │           │ is_folder       │  │  │ created_by (FK) │
        │           │ is_trashed      │  │  │ created_at      │
        │           │ is_starred      │  │  └─────────────────┘
        │           │ version         │  │
        │           │ checksum        │  │
        │           │ content_hash    │  │
        │           │ created_at      │  │
        │           │ modified_at     │  │
        │           └─────────────────┘  │
        │                   │            │
        │                   ▼            │
        │           ┌─────────────────┐  │
        │           │file_permissions │  │
        │           ├─────────────────┤  │
        │           │ id (PK)         │  │
        │           │ file_id (FK)    │  │
        └───────────│ user_id (FK)    │  │
                    │ role            │  │
                    │ type            │  │
                    │ email           │  │
                    └─────────────────┘  │
                                         │
                    ┌─────────────────┐  │
                    │  file_shares    │  │
                    ├─────────────────┤  │
                    │ id (PK)         │  │
                    │ file_id (FK)    │  │
                    │ share_link      │  │
                    │ permission      │  │
                    │ expires_at      │  │
                    └─────────────────┘  │
                                         │
                    ┌─────────────────┐  │
                    │device_sync_status│◄┘
                    ├─────────────────┤
                    │ id (PK)         │
                    │ user_id (FK)    │
                    │ device_id       │
                    │ file_id (FK)    │
                    │ sync_status     │
                    │ last_synced_at  │
                    └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```text
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│         (Desktop, Mobile, Web, API)                              │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway        │
                    │   (Auth, Rate        │
                    │    Limiting)         │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  File Service   │  │  Sync Service   │  │  Collaboration  │
│  (CRUD,         │  │  (Delta Sync,   │  │  Service        │
│   Metadata)     │  │   Conflict)     │  │  (Real-time)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (Metadata,  │  │  (Sync      │  │  (Events)   │
     │   Permissions│  │   Status)   │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Object Storage │
     │  (S3/GCS)       │
     │  (File Content) │
     └─────────────────┘
```

## Key Components

### File Sync Service
```python
import hashlib
from typing import List, Dict

class FileSyncService:
    def __init__(self, db, storage, cache):
        self.db = db
        self.storage = storage
        self.cache = cache

    async def upload_file(self, user_id: int, file_data: bytes,
                         parent_id: int, filename: str) -> dict:
        # Calculate checksum for deduplication
        checksum = hashlib.sha256(file_data).hexdigest()

        # Check for duplicate
        existing = await self.db.find_by_checksum(checksum)
        if existing:
            # Create reference instead of uploading
            return await self.create_file_reference(
                user_id, existing['id'], parent_id, filename
            )

        # Upload to object storage
        storage_path = f"users/{user_id}/{checksum}/{filename}"
        await self.storage.upload(storage_path, file_data)

        # Create file record
        file_record = await self.db.create_file(
            name=filename,
            owner_id=user_id,
            parent_id=parent_id,
            size=len(file_data),
            checksum=checksum,
            storage_path=storage_path
        )

        # Create initial version
        await self.db.create_version(
            file_id=file_record['id'],
            version=1,
            size=len(file_data),
            checksum=checksum,
            storage_path=storage_path,
            created_by=user_id
        )

        # Update storage quota
        await self.db.update_storage_usage(user_id, len(file_data))

        return file_record

    async def sync_device(self, user_id: int, device_id: str,
                         last_sync_timestamp: str) -> dict:
        # Get files modified since last sync
        modified_files = await self.db.get_modified_files(
            user_id, last_sync_timestamp
        )

        # Get sync status for this device
        sync_status = await self.db.get_device_sync_status(
            user_id, device_id
        )

        # Calculate delta
        delta = self.calculate_delta(modified_files, sync_status)

        return {
            'files_to_download': delta['new'],
            'files_to_upload': delta['pending'],
            'conflicts': delta['conflicts'],
            'sync_timestamp': datetime.now().isoformat()
        }
```

### Delta Sync Engine
```python
class DeltaSyncEngine:
    def __init__(self):
        self.chunk_size = 1024 * 1024  # 1MB chunks

    async def calculate_file_delta(self, old_version: bytes,
                                   new_version: bytes) -> List[dict]:
        # Use rsync-like algorithm for efficient delta calculation
        operations = []

        # Split into chunks and compute rolling checksums
        old_chunks = self.compute_chunks(old_version)
        new_chunks = self.compute_chunks(new_version)

        # Find matching blocks
        matching_blocks = self.find_matching_blocks(old_chunks, new_chunks)

        # Generate delta operations
        for i, chunk in enumerate(new_chunks):
            if i not in matching_blocks:
                operations.append({
                    'type': 'insert',
                    'position': i * self.chunk_size,
                    'data': chunk
                })

        return operations

    async def apply_delta(self, base_version: bytes,
                          operations: List[dict]) -> bytes:
        result = bytearray(base_version)

        # Sort operations by position in reverse
        sorted_ops = sorted(operations,
                           key=lambda x: x['position'],
                           reverse=True)

        for op in sorted_ops:
            if op['type'] == 'insert':
                result[op['position']:op['position']] = op['data']
            elif op['type'] == 'delete':
                result[op['position']:op['position'] + op['length']] = b''

        return bytes(result)
```

### Conflict Resolution Service
```python
class ConflictResolver:
    def __init__(self):
        self.conflict_strategies = {
            'document': 'operational_transform',
            'spreadsheet': 'last_writer_wins',
            'image': 'manual',
            'default': 'manual'
        }

    async def resolve_conflict(self, file_id: int,
                              local_version: dict,
                              remote_version: dict) -> dict:
        file_type = await self.get_file_type(file_id)
        strategy = self.conflict_strategies.get(
            file_type, self.conflict_strategies['default']
        )

        if strategy == 'operational_transform':
            return await self.operational_transform(
                local_version, remote_version
            )
        elif strategy == 'last_writer_wins':
            return self.last_writer_wins(local_version, remote_version)
        else:
            return await self.create_conflict_copy(
                file_id, local_version, remote_version
            )

    async def operational_transform(self, local: dict,
                                   remote: dict) -> dict:
        # Transform concurrent operations
        local_ops = local['operations']
        remote_ops = remote['operations']

        transformed_ops = []
        for op in local_ops:
            transformed = self.transform_operation(op, remote_ops)
            transformed_ops.append(transformed)

        # Merge operations
        merged_ops = transformed_ops + remote_ops

        return {
            'merged_content': self.apply_operations(
                local['base_content'], merged_ops
            ),
            'operations': merged_ops,
            'version': max(local['version'], remote['version']) + 1
        }

    def last_writer_wins(self, local: dict, remote: dict) -> dict:
        if local['modified_at'] > remote['modified_at']:
            return local
        return remote

    async def create_conflict_copy(self, file_id: int,
                                   local: dict, remote: dict) -> dict:
        # Create a copy with "(conflict)" suffix
        conflict_name = f"{local['name']} (conflict {local['device_id']})"

        await self.db.create_file(
            name=conflict_name,
            owner_id=local['owner_id'],
            parent_id=local['parent_id'],
            content=local['content']
        )

        return {
            'resolution': 'conflict_copy_created',
            'conflict_file_name': conflict_name
        }
```

### Version Control Service
```python
class VersionControlService:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage

    async def create_version(self, file_id: int, user_id: int,
                            content: bytes) -> dict:
        # Get current version
        current = await self.db.get_latest_version(file_id)
        new_version = (current['version'] + 1) if current else 1

        # Calculate checksum
        checksum = hashlib.sha256(content).hexdigest()

        # Store in object storage
        storage_path = f"versions/{file_id}/v{new_version}"
        await self.storage.upload(storage_path, content)

        # Create version record
        version = await self.db.create_version(
            file_id=file_id,
            version=new_version,
            size=len(content),
            checksum=checksum,
            storage_path=storage_path,
            created_by=user_id
        )

        # Update file metadata
        await self.db.update_file(
            file_id,
            version=new_version,
            size=len(content),
            checksum=checksum
        )

        return version

    async def rollback_version(self, file_id: int,
                              target_version: int) -> dict:
        # Get target version
        version = await self.db.get_version(file_id, target_version)

        # Download content
        content = await self.storage.download(version['storage_path'])

        # Create new version with rolled back content
        new_version = await self.create_version(
            file_id,
            system_user_id,
            content
        )

        return new_version

    async def get_version_history(self, file_id: int,
                                  limit: int = 50) -> list:
        return await self.db.get_versions(file_id, limit)
```

## Caching Strategy (Redis)

### File Metadata Cache
```python
class FileMetadataCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def cache_file_metadata(self, file_id: str,
                                  metadata: dict):
        key = f"file:{file_id}"
        await self.redis.hset(key, mapping=metadata)
        await self.redis.expire(key, 3600)  # 1 hour

    async def get_file_metadata(self, file_id: str) -> dict:
        key = f"file:{file_id}"
        return await self.redis.hgetall(key)

    async def invalidate_file(self, file_id: str):
        await self.redis.delete(f"file:{file_id}")

    async def cache_folder_contents(self, folder_id: str,
                                    files: list):
        key = f"folder:{folder_id}:contents"
        await self.redis.delete(key)
        for file in files:
            await self.redis.rpush(key, json.dumps(file))
        await self.redis.expire(key, 300)  # 5 minutes
```

### Sync Status Cache
```python
class SyncStatusCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def update_sync_status(self, user_id: int,
                                 device_id: str, file_id: int,
                                 status: str):
        key = f"sync:{user_id}:{device_id}"
        await self.redis.hset(key, file_id, status)
        await self.redis.expire(key, 86400)  # 24 hours

    async def get_sync_status(self, user_id: int,
                              device_id: str) -> dict:
        key = f"sync:{user_id}:{device_id}"
        return await self.redis.hgetall(key)

    async def get_pending_syncs(self, user_id: int,
                                device_id: str) -> list:
        key = f"sync:{user_id}:{device_id}"
        all_status = await self.redis.hgetall(key)
        return [fid for fid, status in all_status.items()
                if status == 'pending']
```

## Message Queue (Kafka)

### Topics and Events
```text
Topics:
├── file.created          (new file uploads)
├── file.modified         (file updates)
├── file.deleted          (file deletions)
├── file.shared           (permission changes)
├── file.sync.completed   (sync operations)
├── collaboration.operation (real-time edits)
└── conflict.detected     (sync conflicts)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "file.modified",
  "timestamp": "2025-01-15T10:30:00Z",
  "user_id": "usr_456",
  "file_id": "file_789",
  "data": {
    "version": 5,
    "size": 1048576,
    "checksum": "abc123...",
    "device_id": "dev_012"
  }
}
```

### Event Processing
```python
class FileEventProcessor:
    def __init__(self, kafka_consumer, db, notification_service):
        self.consumer = kafka_consumer
        self.db = db
        self.notifications = notification_service

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'file.modified':
                await self.handle_file_modified(event)
            elif event['event_type'] == 'file.shared':
                await self.handle_file_shared(event)
            elif event['event_type'] == 'conflict.detected':
                await self.handle_conflict(event)

    async def handle_file_modified(self, event: dict):
        # Notify collaborators
        collaborators = await self.db.get_file_collaborators(
            event['file_id']
        )

        for collab in collaborators:
            if collab['user_id'] != event['user_id']:
                await self.notifications.notify(
                    collab['user_id'],
                    {
                        'type': 'file_modified',
                        'file_id': event['file_id'],
                        'modified_by': event['user_id']
                    }
                )

        # Update search index
        await self.update_search_index(event['file_id'])
```

## Scaling Strategy

### File Storage Scaling
```text
Storage Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │  Storage Router  │
                    │  (Consistent     │
                    │   Hashing)       │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Object      │   │  Object      │   │  Object      │
│  Storage     │   │  Storage     │   │  Storage     │
│  (US-East)   │   │  (EU-West)   │   │  (APAC)      │
└──────────────┘   └──────────────┘   └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  Replication    │
                    │  (3x copies)    │
                    └─────────────────┘
```

### Database Scaling
```python
class ShardRouter:
    def __init__(self, num_shards: int = 64):
        self.num_shards = num_shards

    def get_shard(self, user_id: int) -> int:
        return user_id % self.num_shards

    def get_file_shard(self, file_id: int) -> int:
        # Different sharding for file metadata
        return (file_id * 7) % self.num_shards
```

### Sync Service Scaling
```python
class SyncServiceScaler:
    def __init__(self):
        self.sync_workers = []  # Worker pool

    async def handle_sync_request(self, request: dict):
        # Partition sync requests by user
        partition = request['user_id'] % self.num_partitions

        # Route to appropriate worker
        worker = self.get_worker(partition)

        return await worker.process_sync(request)

    async def process_sync_batch(self, requests: list):
        # Batch sync operations for efficiency
        grouped = self.group_by_user(requests)

        for user_id, user_requests in grouped.items():
            # Process all requests for a user together
            await self.process_user_sync(user_id, user_requests)
```

## Failure Handling

### Sync Conflict Recovery
```python
class SyncConflictRecovery:
    def __init__(self, db, notification_service):
        self.db = db
        self.notifications = notification_service

    async def handle_sync_conflict(self, conflict: dict):
        # Detect conflict type
        conflict_type = self.detect_conflict_type(conflict)

        if conflict_type == 'concurrent_edit':
            # Use operational transform
            resolved = await self.resolve_concurrent_edit(conflict)
        elif conflict_type == 'file_renamed':
            # Apply both renames
            resolved = await self.resolve_rename_conflict(conflict)
        elif conflict_type == 'file_deleted':
            # Notify user of conflict
            await self.notify_conflict(conflict)
            return

        # Apply resolution
        await self.apply_resolution(resolved)

        # Notify affected users
        await self.notify_resolution(conflict, resolved)
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| Storage node down | Replication ensures availability |
| Database failover | Read from replica |
| Sync service down | Queue operations, retry later |
| Network partition | Store locally, sync when reconnected |
| Conflict resolution fails | Create conflict copy |

### Offline Support
```python
class OfflineSupport:
    def __init__(self, local_storage, sync_service):
        self.local = local_storage
        self.sync = sync_service

    async def go_offline(self):
        # Mark all files as available offline
        files = await self.local.get_all_files()
        for file in files:
            await self.local.mark_available_offline(file['id'])

    async def go_online(self):
        # Sync pending changes
        pending = await self.local.get_pending_changes()

        for change in pending:
            try:
                await self.sync.apply_change(change)
                await self.local.mark_synced(change['file_id'])
            except ConflictError as e:
                await self.handle_offline_conflict(change, e)
```

## Monitoring

### Key Metrics
```yaml
Business Metrics:
  - files_uploaded_per_hour
  - active_sync_operations
  - storage_usage_by_user
  - collaboration_sessions_active

System Metrics:
  - sync_latency_p95
  - file_download_time
  - conflict_resolution_rate
  - storage_utilization
  - api_response_time

Infrastructure Metrics:
  - server_cpu_usage
  - memory_usage
  - network_throughput
  - disk_io
  - storage_iops
```

### Alerting Rules
```yaml
alerts:
  - name: High Sync Latency
    condition: p95_sync_latency > 5s
    severity: warning

  - name: Conflict Rate High
    condition: conflict_rate > 1%
    severity: warning

  - name: Storage Utilization High
    condition: storage_used > 80%
    severity: critical

  - name: Sync Queue Backlog
    condition: sync_queue_size > 10000
    severity: warning
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | Block storage | Object storage | Object (S3/GCS) |
| Sync | Full file sync | Delta sync | Delta (efficient) |
| Conflict Resolution | Operational transform | Last writer wins | OT for documents |
| Consistency | Strong | Eventual | Strong for metadata |
| Versioning | Full copies | Deltas | Full copies (simpler) |

## Interview Questions

### Design Questions
1. **How would you implement real-time file sync?**
   - WebSocket for live updates
   - Delta sync for efficiency
   - Conflict detection and resolution
   - Offline support with queue

2. **How do you handle file versioning?**
   - Store each version in object storage
   - Metadata tracks version history
   - Rollback creates new version
   - Garbage collection for old versions

3. **How would you implement collaboration?**
   - Operational transform for concurrent edits
   - WebSocket for real-time updates
   - Conflict detection and resolution
   - User presence indicators

### Scaling Questions
4. **How do you scale to 1B+ files?**
   - Object storage for file content
   - Database sharding for metadata
   - CDN for frequent downloads
   - Caching for hot files

5. **How do you handle 10M concurrent sync operations?**
   - Partition sync requests by user
   - Batch operations for efficiency
   - Priority queues for important files
   - Connection pooling

### Trade-off Questions
6. **How do you balance consistency vs availability?**
   - Strong consistency for metadata
   - Eventual consistency for sync status
   - Conflict resolution for concurrent edits
   - Offline support with eventual sync

7. **How do you handle large file uploads?**
   - Chunked upload for reliability
   - Resumable uploads for large files
   - Parallel chunk upload
   - Checksum verification

### Senior-level Questions
8. **How would you implement end-to-end encryption?**
   - Client-side encryption keys
   - Key management service
   - Encrypted metadata
   - Secure sharing with keys

9. **How do you optimize for different file types?**
   - Preview generation for documents
   - Thumbnail creation for images
   - Video transcoding
   - Metadata extraction

10. **How would you implement file search?**
    - Full-text indexing with Elasticsearch
    - Metadata-based search
    - Content-based search for documents
    - Search result ranking

## Summary

The Google Drive system design covers:
- **File Sync**: Delta sync for efficiency
- **Conflict Resolution**: Operational transform for documents
- **Version Control**: Full version history with rollback
- **Scalability**: Object storage with database sharding
- **Collaboration**: Real-time editing with conflict detection

Key takeaways:
1. Use delta sync for efficient bandwidth usage
2. Implement operational transform for real-time collaboration
3. Store file content in object storage (S3/GCS)
4. Use database sharding for metadata scalability
5. Implement conflict resolution for concurrent edits

This design supports 1B+ files with 10M concurrent sync operations while maintaining strong consistency for metadata.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
