---
section: System Design
category: Architecture
tags: [concept]
---

# Lyft / Ride-Sharing System Design

## TL;DR

Design a ride-sharing platform matching riders to drivers in real time, computing ETAs, handling trip state (requested → matched → in-progress → completed), pricing, and driver location streaming — at the scale of a major metro.

**Why it matters:** The classic "geospatial + real-time" system design. Tests geohashing / S2 / quadtree indexing, location-update stream processing, dispatch algorithms (nearest-driver matching), and consistency around trip state. Different from Uber's framing but very similar — interviewers will look for nuanced differences.

## Requirements

### Functional Requirements

- Riders request a ride from pickup A to dropoff B
- System matches the rider with the nearest available driver
- Driver and rider see each other's location in real time
- Driver can accept/reject a ride
- Trip state machine: requested → matched → driver_en_route → arrived → in_progress → completed → paid
- Dynamic pricing (surge multiplier in high-demand areas)
- ETA and fare estimate shown before booking
- Ride history, receipts
- Driver onboarding, background checks (out of scope for core)
- Scheduled rides (out of scope for v1)

### Non-Functional Requirements

- 30M+ monthly riders, 5M+ drivers (US, Canada)
- Match latency < 5s (p99) from request to driver notification
- Location update frequency: every 3s per active driver
- ETA recomputation: every 10s during the trip
- 99.95% availability for booking
- Strong consistency for the trip state machine (no double-booking a driver)
- 30s SLA from "trip requested" to "driver accepted or reassign"

## Capacity Estimation

```text
Users:
- 5M active drivers, 30M monthly riders
- 1M concurrent drivers (online at peak)
- 200K active trips at any given peak moment

Location Updates:
- 1M drivers × 1 update / 3s = 333K location events/sec
- 28B location events/day
- Each event: ~100 bytes → 2.8 TB/day raw location stream
- 7-day retention on hot store: 20 TB
- Older data → cold store / aggregated

Trip Requests:
- 1M ride requests/sec at global peak (across regions)
- ~50K requests/sec per major metro
- 200K active trips × state transitions × 5 per trip = 1M state events/sec

Storage:
- Trip records: 1B trips/day × 5 KB = 5 TB/day → 1.8 PB/year
- Driver profiles: 5M × 50 KB = 250 GB
- Rider profiles: 30M × 20 KB = 600 GB

```

## API Design

```yaml
# Request a ride
POST /v1/rides
  Body:
    {
      "rider_id": "u_42",
      "pickup":  { "lat": 37.7749, "lng": -122.4194 },
      "dropoff": { "lat": 37.7849, "lng": -122.4094 },
      "ride_type": "standard"  // 'standard' | 'xl' | 'shared' | 'lux'
    }
  Response:
    {
      "ride_id": "ride_abc",
      "status": "requested",
      "eta_seconds": 240,
      "fare_estimate_usd": 12.50,
      "surge_multiplier": 1.0
    }

# Cancel a ride
POST /v1/rides/{ride_id}/cancel
  Response: 200 { "status": "cancelled" }

# Driver location stream
POST /v1/drivers/{driver_id}/location
  Body: { "lat": 37.7749, "lng": -122.4194, "heading": 90, "speed_mps": 12.3, "ts": "2026-07-15T10:30:00Z" }
  Response: 204

# Driver accepts ride
POST /v1/rides/{ride_id}/accept
  Body: { "driver_id": "d_99" }
  Response: 200 { "ride_id": "ride_abc", "status": "matched", "driver_id": "d_99" }

# Trip state transition
POST /v1/rides/{ride_id}/transition
  Body: { "to_state": "in_progress", "ts": "..." }
  Response: 200

```

## Database Design

### Schema (PostgreSQL, sharded by region)

```sql
-- Drivers (active in current region; hot)
CREATE TABLE drivers (
    driver_id      BIGINT PRIMARY KEY,
    home_region    VARCHAR(8) NOT NULL,
    current_loc    GEOGRAPHY(POINT, 4326),
    status         VARCHAR(20) NOT NULL,  -- 'offline' | 'available' | 'en_route' | 'on_trip'
    rating         DECIMAL(3,2),
    vehicle_type   VARCHAR(20),
    last_seen      TIMESTAMPTZ,
    INDEX idx_status_loc (status, current_loc)  -- GIST index for spatial queries
);

-- Rides (sharded by region)
CREATE TABLE rides (
    ride_id        UUID PRIMARY KEY,
    rider_id       BIGINT NOT NULL,
    driver_id      BIGINT,
    region         VARCHAR(8) NOT NULL,
    pickup         GEOGRAPHY(POINT) NOT NULL,
    dropoff        GEOGRAPHY(POINT) NOT NULL,
    status         VARCHAR(20) NOT NULL,  -- see state machine
    ride_type      VARCHAR(20),
    fare_quote     DECIMAL(8,2),
    surge          DECIMAL(3,2),
    requested_at   TIMESTAMPTZ,
    matched_at     TIMESTAMPTZ,
    pickup_at      TIMESTAMPTZ,
    dropoff_at     TIMESTAMPTZ,
    INDEX idx_status_region (region, status)
);

-- Trip state transitions (audit log; append-only)
CREATE TABLE trip_events (
    ride_id        UUID,
    from_state     VARCHAR(20),
    to_state       VARCHAR(20),
    ts             TIMESTAMPTZ,
    actor          VARCHAR(20),  -- 'rider' | 'driver' | 'system'
    PRIMARY KEY (ride_id, ts)
);
```

## Architecture

### ASCII Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                   RIDE-SHARING-TYPE STACK                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Rider App ─┐                                                       │
│             ├──▶ API Gateway (region-routed, auth)                  │
│  Driver App ┘              │                                       │
│                            ▼                                       │
│                  ┌────────────────────┐                            │
│                  │  Dispatch Service  │  (per-region)               │
│                  │  (the brain)       │                            │
│                  │  ├── Geospatial    │                            │
│                  │  │   index (Redis  │                            │
│                  │  │   S2 / H3)      │                            │
│                  │  ├── ETA service   │                            │
│                  │  ├── Pricing svc   │                            │
│                  │  └── State machine │                            │
│                  └─────────┬──────────┘                            │
│                            │                                       │
│         ┌──────────────────┼──────────────────┐                    │
│         ▼                  ▼                  ▼                    │
│  Location Stream    Trip Store         Notification               │
│  (Kafka)            (PostgreSQL)       (APNs/FCM)                 │
│         │                  │                                       │
│         ▼                  ▼                                       │
│  Location Indexer    Trip Analytics                                  │
│  (Redis / S2 grid)   (Kafka → DW)                                   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Driver Location Pipeline

1. Driver app sends location every 3s (or 5–10s when stationary) over HTTPS to a regional load balancer.
2. LB routes to the **Location Ingest Service**, which validates, deduplicates, and publishes to Kafka `driver.location`.
3. **Location Indexer** consumes the stream and updates a per-region Redis cluster keyed by S2 cell ID.
4. The Dispatch Service queries this index to find nearby drivers in O(log N) or O(1) per cell.

```text
Driver location flow:
  App ──> Ingest LB ──> Kafka ──> Indexer ──> Redis (S2 cell → driver set)
                                                       │
                                                       ▼
                                          Dispatch Service (geo query)
```

### Geospatial Indexing (S2 / H3)

- Divide the world into **S2 cells** (~3 km² at level 14) or **H3 hexagons** at resolution 9.
- Each driver is added to a Redis sorted set keyed by cell ID: `ZADD s2:cell:abc123 <driver_id> <timestamp>`.
- For a ride request at (lat, lng), compute the pickup's S2 cell + neighbors, then `ZRANGEBYSCORE` to find drivers in those cells whose last-update is < 10s ago.
- Redis cluster is sharded by S2 cell, so each cell has bounded key size.

### Dispatch Algorithm (Nearest Driver)

```python
async def find_nearest_driver(pickup: LatLng, ride_type: str) -> Optional[Driver]:
    # 1. Find S2 cells at the pickup point + expanding ring of neighbors
    cells = s2.covering_cells(pickup, level=14)
    for radius in [0, 1, 2, 4, 8, 16]:  # expanding ring
        ring = s2.expand_ring(cells, radius)
        # 2. For each cell, query Redis sorted set of (driver_id, last_seen)
        candidates = []
        for cell in ring:
            members = await redis.zrangebyscore(
                f"s2:{cell}",
                min=now_ts - 10,  # last 10 seconds
                max=now_ts
            )
            candidates.extend(members)
        if not candidates:
            continue
        # 3. Filter by ride_type, status='available', rating threshold
        filtered = [d for d in candidates if d.matches(ride_type)]
        if not filtered:
            continue
        # 4. Compute road-network ETA (not straight-line distance) and sort
        return await eta_service.pick_best(filtered, pickup)
    return None
```

### ETA Service

Naive: Haversine distance → multiply by average speed. **Wrong** — doesn't account for roads, traffic, one-way streets, bridges.

Production: Use a **road-network routing engine**:
- OpenStreetMap graph + a routing library (OSRM, Valhalla)
- Real-time traffic overlay
- Cached precomputed travel-time matrices per cell pair, refreshed every 1–5 min

```text
ETA pipeline:
  Pickup + Driver pos ──> OSRM / Valhalla ──> Travel time (sec)
                                                 │
                                                 ▼
                                        Precomputed matrices (Redis)
                                                 │
                                                 ▼
                                        Rank drivers by ETA
```

### Pricing (Surge)

- Per cell, compute the **demand : supply ratio** in real time.
- If ratio > threshold (e.g., 2.0), apply surge multiplier: 1.5×, 2×, 3×, capped at 4× or 5×.
- Surge is **always visible to the rider before they commit** (regulatory requirement in many jurisdictions).
- Pricing recomputes every 60–120s.

### Trip State Machine

```text
        ┌───────────┐
        │ requested │
        └─────┬─────┘
              │ matched
              ▼
        ┌───────────┐     driver_cancel
        │  matched  │──────────────────────┐
        └─────┬─────┘                      │
              │ driver_en_route            │
              ▼                             │
        ┌──────────────────┐               │
        │ driver_en_route  │               │
        └─────┬────────────┘               │
              │ arrived                     │
              ▼                             │
        ┌───────────┐                      │
        │  arrived  │                      │
        └─────┬─────┘                      │
              │ trip_start                 │
              ▼                             ▼
        ┌─────────────┐              ┌─────────────┐
        │ in_progress │              │  cancelled  │
        └─────┬───────┘              └─────────────┘
              │ trip_complete
              ▼
        ┌────────────┐
        │  completed │  ──> payment ──> closed
        └────────────┘
```

Strong consistency on the state machine is enforced by an **optimistic-concurrency update**:

```sql
UPDATE rides
   SET status = 'matched', driver_id = $1, matched_at = NOW()
 WHERE ride_id = $2 AND status = 'requested';
-- Affected rows: 1 = success, 0 = lost the race
```

If 0, the second writer (Dispatch trying to assign another driver) backs off and reassigns.

## Caching Strategy

| Cache | Stores | TTL | Invalidation |
|---|---|---|---|
| Redis (per region) | S2 cell → driver set, ETA matrices, surge | 5–60s | TTL + event-driven update |
| Memcached | Driver profiles, rider profiles | 5 min | DB write invalidation |
| Client (mobile) | Recent locations, surge map, last 5 trips | Persistent | On logout / clear |
| Edge CDN | Static assets, app config | 1 hour | Versioned URL |

## Message Queue

Kafka topics:
- `driver.location` — location updates, 333K events/sec
- `ride.requested` — match triggers
- `ride.state.changed` — analytics, notifications, billing
- `pricing.tick` — surge recalculation
- `driver.status` — online/offline/trip events

Use **partition by region** to keep dispatch work local.

## Scaling Strategy

| Bottleneck | Solution |
|---|---|
| Location updates flood Kafka | Batch updates client-side; sample when stationary |
| Hot cell (Times Square, rush hour) | Sub-cell sharding; thousands of drivers per cell is OK if ZSET scan is fast |
| ETA recompute on every match | Precomputed matrices; refresh every 1–5 min |
| Trip store write contention | Shard by region; use connection pool sizing per region |
| Match spike (concert ending) | Surge pricing + virtual queue; cap dispatch rate per cell |
| Geospatial index drift | Periodic reconciliation job compares Redis to last-known locations |
| Driver app GPS noise | Kalman filter on client; server applies plausibility check (max speed 200 km/h) |

## Failure Handling

| Failure | Mitigation |
|---|---|
| Location stream stalled | Dispatch uses last-known position with TTL; alert if all drivers stale > 30s |
| Match service down | Trip requests buffered; client retries with exponential backoff |
| State transition race (two systems try to match) | Optimistic concurrency on rides.status; only one wins |
| Surge miscalculation | Cap surge at 4× or 5×; show rider the multiplier before commit |
| Driver GPS spoofing | Compare reported position to prior trail; detect teleports > 1 km / 3 s |
| Pricing service down | Fall back to last-known surge for that cell; ride proceeds with cached quote |
| Trip payment fails | Hold trip in "completed_unpaid" state; retry payment async for 24h |

## Monitoring

- **Match latency**: request → driver accepted, p50/p95/p99
- **Match success rate**: % of requests matched within 60s
- **Surge coverage**: distribution of multipliers across cells
- **Trip state machine**: transition counts per minute per state
- **Driver app health**: location update frequency, app version distribution
- **ETA accuracy**: predicted vs actual arrival time, drift
- **Location stream lag**: Kafka consumer lag for `driver.location`

Alerts: match latency p99 > 30s, location stream lag > 10s, surge spike across > 50% of cells, match failure rate > 5%.

## Trade-offs

| Decision | Option A | Option B | Choice |
|---|---|---|---|
| Geo index | Redis ZSET per S2 cell | Elasticsearch geo queries | Redis (latency, throughput) |
| Match algorithm | Nearest first | Best ETA (road network) | Best ETA (rider experience) |
| Pricing | Static + per-region | Dynamic per-cell | Per-cell (balances supply/demand) |
| Location frequency | Every 1s | Every 3–5s | 3–5s (battery + bandwidth vs accuracy) |
| Dispatch | Single global service | Per-region sharded | Per-region (latency, blast radius) |
| Trip state store | PostgreSQL | Event-sourced | PostgreSQL with audit log (simpler, queryable) |
| Ride sharing (pool) | Match in batches | Match in real time | Real time (UX) with greedy batching |

## Summary

- **Geo index** is the foundation — S2 cells in Redis, queryable in O(1) per cell.
- **Location pipeline** must handle 333K events/sec with bounded lag; batch and sample on the client.
- **Dispatch** is the heart: find best-ETA driver, atomic state transition, prompt re-dispatch on timeout.
- **ETA** is computed against the road network, not straight-line distance — precomputed travel-time matrices.
- **State machine** uses optimistic concurrency on the rides table to prevent double-booking.
- **Surge pricing** is visible to the rider before commit and capped at 4–5×.
- **Regional sharding** keeps latency low and blast radius small.

---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [System Design Interview Questions](16-Interview-Questions.md)
- [Uber](03-Uber.md) (sister problem with different framing)
- [WebSockets](../21-WebSockets/)

## References & Learn More

- [Lyft Engineering Blog](https://eng.lyft.com/)
- [Uber Engineering Blog — geospatial systems](https://www.uber.com/blog/engineering/)
- [Google S2 Geometry Library](https://s2geometry.io/)
- [Uber's H3 Hexagonal Grid](https://h3geo.org/)
- [OSRM — Open Source Routing Machine](http://project-osrm.org/)
- [Alex Xu — System Design Vol 2 (Ride-sharing chapter)](https://bytebytego.com/)
- [Designing Data-Intensive Applications — Kleppmann (Ch. 11: Stream Processing)](https://dataintensive.net/)
