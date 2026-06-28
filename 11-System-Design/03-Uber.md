# Uber System Design

## Requirements
### Functional Requirements

- Request a ride from current location to destination
- Match riders with nearby drivers
- Real-time driver tracking on map
- ETA calculation for pickup and dropoff
- fare estimation before booking
- Surge pricing during high demand
- Payment processing (card, cash, wallet)
- Rating system for riders and drivers
- Trip history and receipts
- Driver availability management

### Non-Functional Requirements

- Low latency matching (< 30 seconds)
- High availability (99.99%)
- Real-time location updates (every 4 seconds)
- Support 20M daily active users
- Handle 1M ride requests per hour at peak
- Location accuracy within 10 meters
- Secure payment processing (PCI compliant)

## Capacity Estimation

```text
Storage Estimates:

- 20M DAU × 2 rides/day = 40M rides/day
- Average ride data: 5 KB
- Daily storage: 40M × 5 KB = 200 GB/day
- Location updates: 1M drivers × 4 sec = 250K updates/sec
- Location storage: 250K × 200 bytes = 50 MB/sec

Bandwidth Estimates:

- Ride requests: 40M × 5 KB = 200 GB/day = ~2.3 MB/s
- Location updates: 50 MB/s = 50 MB/s
- Total: ~52.3 MB/s average, ~260 MB/s peak

Driver Estimates:

- 5M drivers globally
- 1M concurrent during peak
- Location updates every 4 seconds
- Need 1000+ location processing servers

```

## API Design

```yaml
# Ride Request
POST /api/v1/rides
  Request:
    {
      "rider_id": "usr_123",
      "pickup_location": {
        "lat": 37.7749,
        "lng": -122.4194
      },
      "destination": {
        "lat": 37.7849,
        "lng": -122.4094
      },
      "ride_type": "uberx"
    }
  Response:
    {
      "ride_id": "ride_456",
      "driver": {
        "id": "drv_789",
        "name": "John",
        "vehicle": "Toyota Camry",
        "rating": 4.8,
        "location": {"lat": 37.7750, "lng": -122.4190}
      },
      "eta_pickup": 5,
      "fare_estimate": 15.50
    }

# Driver Location Update
PUT /api/v1/drivers/{driver_id}/location
  Request:
    {
      "lat": 37.7750,
      "lng": -122.4190,
      "heading": 45,
      "speed": 30
    }

# Accept Ride
POST /api/v1/rides/{ride_id}/accept
  Request: { "driver_id": "drv_789" }

# Complete Ride
POST /api/v1/rides/{ride_id}/complete
  Request:
    {
      "fare": 15.50,
      "distance": 5.2,
      "duration": 1200
    }

# Get ETA
GET /api/v1/eta?pickup_lat=37.7749&pickup_lng=-122.4194&destination_lat=37.7849&destination_lng=-122.4094
  Response: { "eta_seconds": 1800, "distance_km": 5.2 }

```

## Database Design
### Schema

```sql
-- Riders table
CREATE TABLE riders (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_rides INT DEFAULT 0,
    payment_method_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drivers table
CREATE TABLE drivers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    vehicle_plate VARCHAR(20) NOT NULL,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_rides INT DEFAULT 0,
    is_available BOOLEAN DEFAULT FALSE,
    current_location GEOGRAPHY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drivers_location ON drivers USING GIST(current_location);
CREATE INDEX idx_drivers_available ON drivers(is_available);

-- Rides table
CREATE TABLE rides (
    id BIGSERIAL PRIMARY KEY,
    rider_id BIGINT REFERENCES riders(id),
    driver_id BIGINT REFERENCES drivers(id),
    status VARCHAR(20) NOT NULL, -- 'requested', 'accepted', 'in_progress', 'completed', 'cancelled'
    pickup_location GEOGRAPHY(POINT, 4326) NOT NULL,
    destination GEOGRAPHY(POINT, 4326) NOT NULL,
    pickup_address TEXT,
    destination_address TEXT,
    fare DECIMAL(10,2),
    distance_km DECIMAL(8,2),
    duration_seconds INT,
    surge_multiplier DECIMAL(3,2) DEFAULT 1.00,
    payment_method VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_rides_rider ON rides(rider_id);
CREATE INDEX idx_rides_driver ON rides(driver_id);
CREATE INDEX idx_rides_status ON rides(status);

-- Driver location history (partitioned by time)
CREATE TABLE driver_locations (
    driver_id BIGINT NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    heading INT,
    speed INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (recorded_at);

-- Surge pricing table
CREATE TABLE surge_pricing (
    id BIGSERIAL PRIMARY KEY,
    region GEOGRAPHY(POLYGON, 4326) NOT NULL,
    multiplier DECIMAL(3,2) NOT NULL,
    demand_score INT NOT NULL,
    supply_score INT NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    ride_id BIGINT REFERENCES rides(id),
    rider_id BIGINT REFERENCES riders(id),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   riders    │     │     rides       │     │    drivers      │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ rider_id (FK)   │     │ id (PK)         │
│ name        │     │ id (PK)         │────►│ name            │
│ email       │     │ driver_id (FK)  │     │ phone           │
│ phone       │     │ status          │     │ vehicle_type    │
│ rating      │     │ pickup_location │     │ vehicle_plate   │
│ total_rides │     │ destination     │     │ rating          │
│ payment_id  │     │ fare            │     │ is_available    │
└─────────────┘     │ distance_km     │     │ current_location│
                    │ duration        │     └─────────────────┘
                    │ surge_multiplier│              │
                    │ payment_method  │              │
                    │ created_at      │              ▼
                    │ started_at      │     ┌─────────────────┐
                    │ completed_at    │     │driver_locations │
                    └─────────────────┘     ├─────────────────┤
                             │              │ driver_id (FK)  │
                             ▼              │ location        │
                    ┌─────────────────┐     │ heading         │
                    │    payments     │     │ speed           │
                    ├─────────────────┤     │ recorded_at     │
                    │ id (PK)         │     └─────────────────┘
                    │ ride_id (FK)    │
                    │ rider_id (FK)   │
                    │ amount          │
                    │ currency        │
                    │ method          │
                    │ status          │
                    │ transaction_id  │
                    └─────────────────┘

```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Mobile Apps (Rider/Driver)                     │
└──────────────────────────────────────────────────────────────────┘
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
│  Ride Service   │  │  Location       │  │  Payment        │
│  (Request,      │  │  Service        │  │  Service        │
│   Matching)     │  │  (Tracking)     │  │  (Processing)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │   Redis     │  │   Kafka     │
     │  (Rides,     │  │  (Location, │  │  (Events)   │
     │   Payments)  │  │   Sessions) │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  PostGIS/Geo    │
     │  (Spatial       │
     │   Queries)      │
     └─────────────────┘

```

## Key Components

### Geospatial Indexing Service

```python
from sqlalchemy import create_engine
from geoalchemy2 import Geography
import redis
import json

class GeospatialService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def find_nearby_drivers(self, lat: float, lng: float,
                                  radius_km: int = 5) -> list:
        # Redis GEORADIUS for fast lookup
        nearby = self.redis.georadius(
            'driver_locations',
            lng, lat,
            radius_km,
            unit='km',
            withdist=True,
            withcoord=True,
            sort='ASC'  # nearest first
        )

        # Filter for available drivers
        available_drivers = []
        for driver_id, distance, location in nearby:
            if self.redis.hget(f"driver:{driver_id}", 'available'):
                available_drivers.append({
                    'driver_id': driver_id,
                    'distance': distance,
                    'location': location
                })

        return available_drivers

    async def update_driver_location(self, driver_id: str,
                                     lat: float, lng: float):
        # Update in Redis for real-time queries
        self.redis.geoadd(
            'driver_locations',
            (lng, lat, driver_id)
        )

        # Store in database for historical analysis
        await self.db.execute(
            "INSERT INTO driver_locations (driver_id, location, recorded_at) "
            "VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), NOW())",
            (driver_id, lng, lat)
        )

    async def calculate_eta(self, pickup_lat: float, pickup_lng: float,
                           destination_lat: float, destination_lng: float) -> dict:
        # Use routing service (Google Maps API or OSRM)
        route = await self.routing_service.get_route(
            (pickup_lng, pickup_lat),
            (destination_lng, destination_lat)
        )

        return {
            'eta_seconds': route['duration'],
            'distance_km': route['distance'] / 1000
        }

```

### Ride Matching Service

```python
from typing import Optional
import asyncio

class RideMatchingService:
    def __init__(self, geo_service, db, notification_service):
        self.geo = geo_service
        self.db = db
        self.notifications = notification_service
        self.max_search_radius = 10  # km
        self.search_expansion_rate = 2  # km per attempt

    async def match_ride(self, ride_request: dict) -> Optional[dict]:
        pickup_lat = ride_request['pickup_location']['lat']
        pickup_lng = ride_request['pickup_location']['lng']

        # Progressive search - start small, expand
        radius = 2  # Start with 2km

        while radius <= self.max_search_radius:
            # Find nearby available drivers
            drivers = await self.geo.find_nearby_drivers(
                pickup_lat, pickup_lng, radius
            )

            if drivers:
                # Score drivers based on multiple factors
                scored_drivers = await self.score_drivers(
                    drivers, ride_request
                )

                # Try to match with best driver
                for driver in scored_drivers:
                    success = await self.offer_ride_to_driver(
                        ride_request, driver
                    )
                    if success:
                        return driver

            # Expand search radius
            radius += self.search_expansion_rate
            await asyncio.sleep(0.5)  # Brief wait before expanding

        # No driver found
        return None

    async def score_drivers(self, drivers: list,
                           ride_request: dict) -> list:
        scored = []
        for driver in drivers:
            # Calculate score based on:
            # 1. Distance to pickup (40%)
            # 2. Driver rating (30%)
            # 3. Acceptance rate (20%)
            # 4. Vehicle type match (10%)

            distance_score = 1 - (driver['distance'] / self.max_search_radius)
            rating_score = driver['rating'] / 5.0
            acceptance_score = driver['acceptance_rate']
            vehicle_match = 1.0 if driver['vehicle_type'] == ride_request['ride_type'] else 0.5

            total_score = (
                distance_score * 0.4 +
                rating_score * 0.3 +
                acceptance_score * 0.2 +
                vehicle_match * 0.1
            )

            scored.append({**driver, 'score': total_score})

        return sorted(scored, key=lambda x: x['score'], reverse=True)

    async def offer_ride_to_driver(self, ride_request: dict,
                                   driver: dict) -> bool:
        # Send offer to driver
        offer = {
            'ride_id': ride_request['ride_id'],
            'pickup': ride_request['pickup_location'],
            'destination': ride_request['destination'],
            'estimated_fare': ride_request['fare_estimate'],
            'expires_in': 15  # seconds to accept
        }

        accepted = await self.notifications.send_ride_offer(
            driver['driver_id'], offer
        )

        if accepted:
            # Update ride status
            await self.db.update_ride(
                ride_request['ride_id'],
                driver_id=driver['driver_id'],
                status='accepted'
            )

            # Mark driver as unavailable
            await self.geo.set_driver_unavailable(driver['driver_id'])

            return True

        return False

```

### Surge Pricing Service

```python
from datetime import datetime, timedelta
import math

class SurgePricingService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def calculate_surge(self, lat: float, lng: float) -> float:
        # Get demand and supply in the area
        demand = await self.get_demand_score(lat, lng)
        supply = await self.get_supply_score(lat, lng)

        # Calculate surge multiplier
        if supply == 0:
            return 3.0  # Max surge when no drivers

        ratio = demand / supply

        # Surge pricing algorithm
        if ratio < 0.8:
            return 1.0  # No surge
        elif ratio < 1.2:
            return 1.25
        elif ratio < 1.5:
            return 1.5
        elif ratio < 2.0:
            return 2.0
        else:
            return min(3.0, 1.0 + (ratio - 1.0) * 0.5)

    async def get_demand_score(self, lat: float, lng: float) -> int:
        # Count ride requests in last 15 minutes
        key = f"demand:{lat:.3f}:{lng:.3f}"
        count = self.redis.get(key)
        if count:
            return int(count)

        # Query database
        result = await self.db.execute(
            "SELECT COUNT(*) FROM rides "
            "WHERE ST_DWithin(pickup_location, "
            "ST_SetSRID(ST_MakePoint(%s, %s), 4326), 1000) "
            "AND created_at > NOW() - INTERVAL '15 minutes'",
            (lng, lat)
        )

        return result[0][0]

    async def get_supply_score(self, lat: float, lng: float) -> int:
        # Count available drivers in area
        nearby_drivers = await self.geo.find_nearby_drivers(lat, lng, 5)
        return len([d for d in nearby_drivers if d['available']])

```

### ETA Calculation Service

```python
class ETACalculationService:
    def __init__(self, traffic_service, routing_service):
        self.traffic = traffic_service
        self.routing = routing_service

    async def calculate_eta(self, origin: tuple, destination: tuple,
                           departure_time: datetime = None) -> dict:
        if departure_time is None:
            departure_time = datetime.now()

        # Get route options
        routes = await self.routing.get_routes(
            origin, destination, alternatives=3
        )

        results = []
        for route in routes:
            # Adjust for current traffic conditions
            traffic_factor = await self.traffic.get_traffic_factor(
                route, departure_time
            )

            adjusted_duration = route['duration'] * traffic_factor

            results.append({
                'route_id': route['id'],
                'distance_km': route['distance'] / 1000,
                'duration_seconds': int(adjusted_duration),
                'traffic_level': self.get_traffic_level(traffic_factor)
            })

        # Return best route (shortest time)
        best = min(results, key=lambda x: x['duration_seconds'])

        return {
            'eta_seconds': best['duration_seconds'],
            'distance_km': best['distance_km'],
            'traffic_level': best['traffic_level'],
            'all_routes': results
        }

    def get_traffic_level(self, factor: float) -> str:
        if factor < 1.2:
            return 'light'
        elif factor < 1.5:
            return 'moderate'
        elif factor < 2.0:
            return 'heavy'
        else:
            return 'severe'

```

## Caching Strategy (Redis)

### Location Cache

```python
class LocationCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def update_driver_location(self, driver_id: str,
                                     lat: float, lng: float,
                                     heading: int, speed: int):
        # Update geo index
        self.redis.geoadd(
            'driver_locations',
            (lng, lat, driver_id)
        )

        # Update driver details
        self.redis.hset(f"driver:{driver_id}", mapping={
            'lat': lat,
            'lng': lng,
            'heading': heading,
            'speed': speed,
            'updated_at': datetime.now().isoformat()
        })
        self.redis.expire(f"driver:{driver_id}", 30)  # 30 sec TTL

    async def get_nearby_drivers(self, lat: float, lng: float,
                                 radius_km: float = 5) -> list:
        return self.redis.georadius(
            'driver_locations',
            lng, lat,
            radius_km,
            unit='km',
            withdist=True,
            withcoord=True
        )

    async def remove_driver(self, driver_id: str):
        self.redis.zrem('driver_locations', driver_id)
        self.redis.delete(f"driver:{driver_id}")

```

### Surge Pricing Cache

```python
class SurgeCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def update_surge(self, region_id: str, multiplier: float):
        self.redis.hset(f"surge:{region_id}", mapping={
            'multiplier': multiplier,
            'updated_at': datetime.now().isoformat()
        })
        self.redis.expire(f"surge:{region_id}", 300)  # 5 min TTL

    async def get_surge(self, lat: float, lng: float) -> float:
        region_id = self.get_region_id(lat, lng)
        result = self.redis.hget(f"surge:{region_id}", 'multiplier')
        return float(result) if result else 1.0

    def get_region_id(self, lat: float, lng: float) -> str:
        # Round to 0.01 degree grid (~1km)
        return f"{lat:.2f}:{lng:.2f}"

```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── ride.requested        (new ride requests)
├── ride.accepted         (driver accepted ride)
├── ride.started          (ride in progress)
├── ride.completed        (ride finished)
├── ride.cancelled        (ride cancelled)
├── driver.location       (driver location updates)
├── payment.processed     (payment events)
└── surge.calculated      (surge pricing updates)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "ride.requested",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "ride_id": "ride_456",
    "rider_id": "usr_123",
    "pickup": {"lat": 37.7749, "lng": -122.4194},
    "destination": {"lat": 37.7849, "lng": -122.4094}
  }
}

```

### Event Processing

```python
class RideEventProcessor:
    def __init__(self, kafka_consumer, db, cache):
        self.consumer = kafka_consumer
        self.db = db
        self.cache = cache

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'ride.requested':
                await self.handle_ride_requested(event['data'])
            elif event['event_type'] == 'ride.completed':
                await self.handle_ride_completed(event['data'])
            elif event['event_type'] == 'driver.location':
                await self.handle_driver_location(event['data'])

    async def handle_ride_requested(self, data: dict):
        # Update demand metrics
        region_id = self.get_region_id(
            data['pickup']['lat'],
            data['pickup']['lng']
        )
        await self.cache.increment_demand(region_id)

        # Trigger surge pricing recalculation
        await self.calculate_surge_for_region(region_id)

    async def handle_ride_completed(self, data: dict):
        # Update driver availability
        await self.cache.set_driver_available(data['driver_id'])

        # Update supply metrics
        region_id = self.get_region_id(
            data['dropoff']['lat'],
            data['dropoff']['lng']
        )
        await self.cache.increment_supply(region_id)

        # Process payment
        await self.process_payment(data)

```

## Scaling Strategy

### Geographic Sharding

```text
Global Deployment:
┌─────────────────────────────────────────────────────────┐
│                    Global Router                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  US Region   │   │  EU Region   │   │  APAC Region │
│  ──────────  │   │  ──────────  │   │  ──────────  │
│  Ride Service│   │  Ride Service│   │  Ride Service│
│  Location    │   │  Location    │   │  Location    │
│  DB Shards   │   │  DB Shards   │   │  DB Shards   │
└──────────────┘   └──────────────┘   └──────────────┘

```

### Location Service Scaling

```python
class LocationServiceScaler:
    def __init__(self):
        self.grid_size = 0.01  # ~1km grid cells
        self.shards_per_region = 16

    def get_shard(self, lat: float, lng: float) -> int:
        # Consistent hashing based on grid cell
        grid_id = f"{lat:.2f}:{lng:.2f}"
        return hash(grid_id) % self.shards_per_region

    def get_region(self, lat: float, lng: float) -> str:
        # Map to region based on geography
        if -180 <= lng <= -30:
            return 'us-east'
        elif -30 < lng <= 60:
            return 'eu-west'
        else:
            return 'apac'

```

### Database Scaling

```text
Database Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Primary (Write)                       │
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

```

## Failure Handling

### Driver Offline Detection

```python
class DriverOfflineDetector:
    def __init__(self, redis_client, notification_service):
        self.redis = redis_client
        self.notifications = notification_service
        self.timeout = 30  # seconds

    async def start_monitoring(self):
        while True:
            # Check for drivers that haven't updated location
            drivers = await self.redis.smembers('active_drivers')

            for driver_id in drivers:
                last_update = await self.redis.hget(
                    f"driver:{driver_id}", 'updated_at'
                )

                if last_update:
                    elapsed = (datetime.now() -
                              datetime.fromisoformat(last_update)).seconds

                    if elapsed > self.timeout:
                        await self.handle_driver_offline(driver_id)

            await asyncio.sleep(10)  # Check every 10 seconds

    async def handle_driver_offline(self, driver_id: str):
        # Check if driver has active ride
        active_ride = await self.db.get_active_ride(driver_id)

        if active_ride:
            # Notify rider and find replacement driver
            await self.notifications.notify_rider(
                active_ride['rider_id'],
                'Driver went offline, finding replacement...'
            )
            await self.find_replacement_driver(active_ride)

        # Mark driver as offline
        await self.redis.srem('active_drivers', driver_id)
        await self.geo.remove_driver(driver_id)

```

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| Location service down | Use cached locations, degrade ETA accuracy |
| Matching service down | Queue requests, process when recovered |
| Payment service down | Allow cash rides, process cards later |
| Driver GPS failure | Use cell tower triangulation as fallback |
| Network partition | Store location locally, sync when reconnected |

### Ride Cancellation Handling

```python
class CancellationHandler:
    def __init__(self, db, notification_service, refund_service):
        self.db = db
        self.notifications = notification_service
        self.refunds = refund_service

    async def handle_cancellation(self, ride_id: str,
                                  cancelled_by: str, reason: str):
        ride = await self.db.get_ride(ride_id)

        # Update ride status
        await self.db.update_ride(ride_id, status='cancelled')

        # Handle based on when cancellation occurred
        if ride['status'] == 'requested':
            # No driver assigned, just notify
            await self.notifications.notify_rider(
                ride['rider_id'], 'Ride cancelled'
            )

        elif ride['status'] == 'accepted':
            # Driver assigned, handle cancellation fee
            if cancelled_by == ride['rider_id']:
                # Rider cancelled after driver accepted
                cancellation_fee = self.calculate_cancellation_fee(ride)
                await self.refunds.charge_cancellation_fee(
                    ride['rider_id'], cancellation_fee
                )

            # Notify driver
            await self.notifications.notify_driver(
                ride['driver_id'], 'Ride cancelled by rider'
            )

            # Make driver available again
            await self.geo.set_driver_available(ride['driver_id'])

        # Log cancellation for analytics
        await self.db.log_cancellation(ride_id, cancelled_by, reason)

```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - rides_per_minute
  - average_wait_time
  - ride_completion_rate
  - surge_pricing_frequency
  - driver_utilization_rate

System Metrics:

  - matching_latency_p95
  - location_update_frequency
  - api_response_time
  - error_rate_by_endpoint
  - database_query_latency

Infrastructure Metrics:

  - server_cpu_usage
  - memory_usage
  - network_latency_between_regions
  - redis_memory_usage
  - kafka_consumer_lag

```

### Alerting Rules

```yaml
alerts:

  - name: High Matching Latency
    condition: p95_matching_latency > 30s
    severity: critical

  - name: Driver Supply Low
    condition: available_drivers < 10% of demand
    severity: warning

  - name: Surge Pricing Anomaly
    condition: surge_multiplier > 3.0 for > 30 minutes
    severity: warning

  - name: Payment Processing Failures
    condition: payment_failure_rate > 5%
    severity: critical

```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Location Storage | Redis (fast, volatile) | PostgreSQL+PostGIS (persistent) | Redis for real-time, PG for history |
| Matching Algorithm | Nearest driver (simple) | Multi-factor scoring (complex) | Multi-factor for better UX |
| Surge Pricing | Static rules | ML-based dynamic | Static rules (simpler, predictable) |
| ETA Calculation | Direct API call | Cached + real-time hybrid | Hybrid for accuracy + speed |

## Interview Questions

### Design Questions

1. **How would you match riders with drivers efficiently?**

   - Use geospatial indexing (Redis GEO)
   - Progressive search radius expansion
   - Multi-factor scoring (distance, rating, acceptance)
   - Real-time availability tracking

2. **How do you handle surge pricing?**

   - Real-time demand/supply analysis per region
   - Dynamic multiplier calculation
   - Price transparency before booking
   - Gradual surge increase/decrease

3. **How would you ensure accurate ETA?**

   - Integrate with traffic data APIs
   - Machine learning for historical patterns
   - Real-time route optimization
   - Confidence intervals for ETAs

### Scaling Questions

4. **How do you scale location updates for 1M drivers?**

   - Geohash-based sharding
   - Redis for real-time queries
   - Kafka for event processing
   - Write-optimized time-series storage

5. **How do you handle peak demand (New Year's Eve)?**

   - Predictive driver positioning
   - Gradual surge pricing increase
   - Rider incentives for flexibility
   - Driver supply incentives

### Trade-off Questions

6. **How do you balance rider wait time vs driver utilization?**

   - Optimize for rider experience primarily
   - Driver acceptance rate incentives
   - Fair distribution of rides
   - Avoid driver burnout

7. **How do you handle ride pooling (UberPool)?**

   - Graph-based route optimization
   - Real-time rerouting for new pickups
   - Fare splitting logic
   - Delivery time guarantees

### Senior-level Questions

8. **How would you implement safety features?**

   - Real-time ride tracking for contacts
   - Emergency button integration
   - Driver background check system
   - Trip anomaly detection

9. **How do you handle multi-city operations?**

   - Regional data residency
   - Cross-border ride handling
   - Currency conversion
   - Local regulation compliance

10. **How would you optimize for electric vehicles?**

    - Range-aware routing
    - Charging station integration
    - Battery level in matching
    - EV-specific pricing

## Summary

The Uber system design covers:

- **Real-time Location Tracking**: Redis GEO for sub-second queries
- **Intelligent Matching**: Multi-factor scoring algorithm
- **Dynamic Pricing**: Surge based on demand/supply
- **Global Scale**: Geographic sharding and replication
- **Reliability**: Circuit breakers, fallback mechanisms

Key takeaways:

1. Use Redis GEO for efficient geospatial queries

2. Implement progressive search radius for matching

3. Process location updates asynchronously via Kafka

4. Use PostGIS for complex spatial queries

5. Design for failure with graceful degradation

This design supports 20M DAU with < 30 second matching latency and 99.99% availability.

---

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
