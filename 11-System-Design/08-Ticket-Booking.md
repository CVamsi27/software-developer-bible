# Ticket Booking System Design

## Requirements
### Functional Requirements

- Browse available events/shows
- View seating charts
- Select seats
- Reserve seats temporarily
- Process payments
- Generate tickets (QR codes)
- Handle cancellations and refunds
- Support multiple payment methods
- Send booking confirmations
- Support for different event types (movies, concerts, sports)

### Non-Functional Requirements

- High availability (99.99%)
- Strong consistency for seat reservations
- Handle flash sales (high concurrency)
- Prevent double booking
- Support 100K+ concurrent users
- Ticket generation < 1 second
- Real-time seat availability
- Mobile-first design

## Capacity Estimation

```text
Booking Estimates:

- 100K concurrent users during flash sales
- 10K bookings per minute at peak
- 1M bookings per day
- Average booking: 2 tickets
- Daily tickets: 2M

Event Estimates:

- 10K events per day
- Average venue: 500 seats
- Total seats: 5M per day
- Seat reservation timeout: 10 minutes

Storage Estimates:

- Booking data: 1 KB per booking
- Daily: 1M × 1 KB = 1 GB
- Event metadata: 10K × 10 KB = 100 MB
- Total: ~1.1 GB/day

Bandwidth Estimates:

- Booking requests: 10K × 1 KB = 10 MB/s
- Seat availability checks: 100K × 100 bytes = 10 MB/s
- Total: 20 MB/s peak

```

## API Design

```yaml
# Browse Events
GET /api/v1/events
  Query: ?city=mumbai&date=2025-01-15&category=movie&page=1
  Response:
    {
      "events": [...],
      "total": 1000,
      "has_more": true
    }

# Get Event Details
GET /api/v1/events/{event_id}
  Response:
    {
      "id": "evt_123",
      "title": "Movie Show",
      "venue": "PVR Cinema",
      "date": "2025-01-15",
      "time": "19:00",
      "seating_chart": {...},
      "pricing": {
        "silver": 200,
        "gold": 350,
        "platinum": 500
      }
    }

# Get Seat Availability
GET /api/v1/events/{event_id}/seats
  Response:
    {
      "sections": [
        {
          "name": "Silver",
          "rows": [
            {
              "row": "A",
              "seats": [
                {"number": 1, "status": "available", "price": 200},
                {"number": 2, "status": "reserved", "price": 200}
              ]
            }
          ]
        }
      ]
    }

# Reserve Seats
POST /api/v1/reservations
  Request:
    {
      "event_id": "evt_123",
      "seats": [
        {"section": "gold", "row": "B", "number": 5},
        {"section": "gold", "row": "B", "number": 6}
      ],
      "user_id": "usr_456"
    }
  Response:
    {
      "reservation_id": "rsv_789",
      "expires_at": "2025-01-15T10:10:00Z",
      "total_amount": 700
    }

# Confirm Booking
POST /api/v1/bookings
  Request:
    {
      "reservation_id": "rsv_789",
      "payment_method": "card",
      "card_token": "tok_012"
    }
  Response:
    {
      "booking_id": "bkg_345",
      "tickets": [
        {
          "ticket_id": "tkt_678",
          "qr_code": "https://...",
          "seat": {"section": "gold", "row": "B", "number": 5}
        }
      ],
      "total_amount": 700
    }

# Cancel Booking
POST /api/v1/bookings/{id}/cancel
  Response:
    {
      "refund_amount": 630,  # after cancellation fee
      "refund_status": "processing"
    }

```

## Database Design
### Schema

```sql
-- Events table
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    venue_id BIGINT REFERENCES venues(id),
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    category VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Venues table
CREATE TABLE venues (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    address TEXT,
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seating sections
CREATE TABLE seating_sections (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total_rows INT,
    seats_per_row INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seats table
CREATE TABLE seats (
    id BIGSERIAL PRIMARY KEY,
    section_id BIGINT REFERENCES seating_sections(id),
    row_number VARCHAR(5) NOT NULL,
    seat_number INT NOT NULL,
    status VARCHAR(20) DEFAULT 'available', -- 'available', 'reserved', 'booked', 'blocked'
    reservation_id BIGINT,
    booking_id BIGINT,
    reserved_at TIMESTAMP,
    UNIQUE(section_id, row_number, seat_number)
);

CREATE INDEX idx_seats_status ON seats(status);
CREATE INDEX idx_seats_section ON seats(section_id);

-- Reservations (temporary holds)
CREATE TABLE reservations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_id BIGINT REFERENCES events(id),
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'expired', 'converted'
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reservations_user ON reservations(user_id);
CREATE INDEX idx_reservations_expires ON reservations(expires_at)
    WHERE status = 'active';

-- Bookings table
CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_id BIGINT REFERENCES events(id),
    reservation_id BIGINT REFERENCES reservations(id),
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'confirmed', -- 'confirmed', 'cancelled', 'refunded'
    payment_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table
CREATE TABLE tickets (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT REFERENCES bookings(id),
    seat_id BIGINT REFERENCES seats(id),
    ticket_code VARCHAR(50) UNIQUE NOT NULL,
    qr_code TEXT,
    status VARCHAR(20) DEFAULT 'valid', -- 'valid', 'used', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT REFERENCES bookings(id),
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cancellations/Refunds
CREATE TABLE refunds (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT REFERENCES bookings(id),
    amount DECIMAL(10,2) NOT NULL,
    reason TEXT,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   venues    │     │     events      │     │seating_sections │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ venue_id (FK)   │     │ id (PK)         │
│ name        │     │ id (PK)         │◄────│ event_id (FK)   │
│ city        │     │ title           │     │ name            │
│ address     │     │ event_date      │     │ price           │
│ capacity    │     │ event_time      │     │ total_rows      │
└─────────────┘     │ category        │     │ seats_per_row   │
                    └─────────────────┘     └─────────────────┘
                             │                      │
                             │                      ▼
                             │             ┌─────────────────┐
                             │             │     seats       │
                             │             ├─────────────────┤
                             │             │ id (PK)         │
                             │             │ section_id (FK) │
                             │             │ row_number      │
                             │             │ seat_number     │
                             │             │ status          │
                             │             │ reservation_id  │
                             │             │ booking_id      │
                             │             └─────────────────┘
                             │                      │
                             ▼                      ▼
                    ┌─────────────────┐     ┌─────────────────┐
                    │  reservations   │     │    bookings     │
                    ├─────────────────┤     ├─────────────────┤
                    │ id (PK)         │◄────│ reservation_id  │
                    │ user_id         │     │ id (PK)         │
                    │ event_id (FK)   │     │ user_id         │
                    │ total_amount    │     │ event_id (FK)   │
                    │ status          │     │ total_amount    │
                    │ expires_at      │     │ status          │
                    └─────────────────┘     │ payment_id      │
                                            └─────────────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │    tickets      │
                                            ├─────────────────┤
                                            │ id (PK)         │
                                            │ booking_id (FK) │
                                            │ seat_id (FK)    │
                                            │ ticket_code     │
                                            │ qr_code         │
                                            │ status          │
                                            └─────────────────┘

```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│              (Mobile App, Web App, Box Office)                   │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway        │
                    │   (Rate Limiting,    │
                    │    Load Balancing)   │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Event Service  │  │  Booking        │  │  Payment        │
│  (Browse,       │  │  Service        │  │  Service        │
│   Search)       │  │  (Reserve,      │  │  (Process)      │
└────────┬────────┘  │   Confirm)      │  └────────┬────────┘
         │           └────────┬────────┘           │
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (Events,    │  │  (Seat      │  │  (Events)   │
     │   Bookings)  │  │   Locks)    │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Ticket         │
     │  Generator      │
     │  (QR Codes)     │
     └─────────────────┘

```

## Key Components

### Seat Reservation Service

```python
import redis
from datetime import datetime, timedelta

class SeatReservationService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
        self.reservation_timeout = 600  # 10 minutes

    async def reserve_seats(self, event_id: int, user_id: int,
                           seats: list) -> dict:
        # Use Redis for atomic seat locking
        lock_keys = []

        for seat in seats:
            lock_key = f"seat:{event_id}:{seat['section']}:{seat['row']}:{seat['number']}"
            lock_keys.append(lock_key)

        # Try to acquire all locks atomically
        pipe = self.redis.pipeline()
        for key in lock_keys:
            pipe.set(key, user_id, nx=True, ex=self.reservation_timeout)

        results = pipe.execute()

        # Check if all locks acquired
        if not all(results):
            # Release any acquired locks
            for key, acquired in zip(lock_keys, results):
                if acquired:
                    self.redis.delete(key)

            raise SeatUnavailableError("Some seats are no longer available")

        # Create reservation in database
        reservation = await self.db.create_reservation(
            user_id=user_id,
            event_id=event_id,
            seats=seats,
            expires_at=datetime.now() + timedelta(seconds=self.reservation_timeout)
        )

        return {
            'reservation_id': reservation['id'],
            'expires_at': reservation['expires_at'],
            'total_amount': sum(s['price'] for s in seats)
        }

    async def release_expired_reservations(self):
        # Find expired reservations
        expired = await self.db.get_expired_reservations()

        for reservation in expired:
            # Release seat locks in Redis
            for seat in reservation['seats']:
                lock_key = f"seat:{reservation['event_id']}:{seat['section']}:{seat['row']}:{seat['number']}"
                self.redis.delete(lock_key)

            # Update reservation status
            await self.db.update_reservation_status(
                reservation['id'], 'expired'
            )

```

### Booking Service

```python
class BookingService:
    def __init__(self, db, reservation_service, payment_service,
                 ticket_service, notification_service):
        self.db = db
        self.reservations = reservation_service
        self.payments = payment_service
        self.tickets = ticket_service
        self.notifications = notification_service

    async def confirm_booking(self, reservation_id: int,
                             user_id: int, payment_method: dict) -> dict:
        # Get reservation
        reservation = await self.db.get_reservation(reservation_id)

        if not reservation or reservation['user_id'] != user_id:
            raise InvalidReservationError("Invalid reservation")

        if reservation['status'] != 'active':
            raise ReservationExpiredError("Reservation expired")

        # Process payment
        payment = await self.payments.process_payment(
            amount=reservation['total_amount'],
            method=payment_method,
            reference=f"booking_{reservation_id}"
        )

        if payment['status'] != 'success':
            raise PaymentFailedError("Payment failed")

        # Create booking
        booking = await self.db.create_booking(
            user_id=user_id,
            event_id=reservation['event_id'],
            reservation_id=reservation_id,
            total_amount=reservation['total_amount'],
            payment_id=payment['id']
        )

        # Update seat status to booked
        for seat in reservation['seats']:
            await self.db.book_seat(
                seat['id'], booking['id']
            )

        # Generate tickets
        tickets = await self.tickets.generate_tickets(
            booking['id'], reservation['seats']
        )

        # Send confirmation
        await self.notifications.send_booking_confirmation(
            user_id, booking, tickets
        )

        # Update reservation status
        await self.db.update_reservation_status(
            reservation_id, 'converted'
        )

        return {
            'booking_id': booking['id'],
            'tickets': tickets,
            'total_amount': reservation['total_amount']
        }

```

### Ticket Generator Service

```python
import qrcode
import uuid
from io import BytesIO

class TicketGeneratorService:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage

    async def generate_tickets(self, booking_id: int,
                               seats: list) -> list:
        tickets = []

        for seat in seats:
            # Generate unique ticket code
            ticket_code = self.generate_ticket_code()

            # Generate QR code
            qr_code_url = await self.generate_qr_code(ticket_code)

            # Create ticket record
            ticket = await self.db.create_ticket(
                booking_id=booking_id,
                seat_id=seat['id'],
                ticket_code=ticket_code,
                qr_code=qr_code_url
            )

            tickets.append({
                'ticket_id': ticket['id'],
                'ticket_code': ticket_code,
                'qr_code': qr_code_url,
                'seat': seat
            })

        return tickets

    def generate_ticket_code(self) -> str:
        # Generate unique, short ticket code
        return f"TKT{uuid.uuid4().hex[:8].upper()}"

    async def generate_qr_code(self, ticket_code: str) -> str:
        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(ticket_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to storage
        buffer = BytesIO()
        img.save(buffer, format='PNG')

        url = await self.storage.upload(
            f"tickets/{ticket_code}.png",
            buffer.getvalue()
        )

        return url

```

### Flash Sale Handler

```python
class FlashSaleHandler:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def handle_flash_sale(self, event_id: int,
                               total_seats: int):
        # Pre-load seat data into Redis
        seats = await self.db.get_event_seats(event_id)

        # Create seat availability map in Redis
        for seat in seats:
            key = f"seat:{event_id}:{seat['section']}:{seat['row']}:{seat['number']}"
            self.redis.hset(key, mapping={
                'status': 'available',
                'price': seat['price']
            })

        # Set sale start time
        self.redis.set(f"sale_start:{event_id}", "active")

        # Monitor and handle high concurrency
        await self.process_concurrent_bookings(event_id, total_seats)

    async def process_concurrent_bookings(self, event_id: int,
                                         total_seats: int):
        # Use Redis pipeline for atomic operations
        pipe = self.redis.pipeline()

        # Track total bookings
        bookings_key = f"bookings:{event_id}"

        while True:
            try:
                # Check if sale is still active
                if not self.redis.get(f"sale_start:{event_id}"):
                    break

                # Process booking requests
                await self.process_booking_queue(event_id)

                # Check if sold out
                booked_count = await self.db.get_booked_count(event_id)
                if booked_count >= total_seats:
                    self.redis.delete(f"sale_start:{event_id}")
                    break

                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Flash sale error: {e}")

```

## Caching Strategy (Redis)

### Seat Availability Cache

```python
class SeatCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get_seat_status(self, event_id: int,
                             section: str, row: str,
                             seat_number: int) -> str:
        key = f"seat:{event_id}:{section}:{row}:{seat_number}"
        return await self.redis.hget(key, 'status')

    async def reserve_seat(self, event_id: int,
                          section: str, row: str,
                          seat_number: int, user_id: int,
                          timeout: int = 600) -> bool:
        key = f"seat:{event_id}:{section}:{row}:{seat_number}"

        # Atomic reserve
        result = await self.redis.hsetnx(key, 'status', 'reserved')

        if result:
            await self.redis.hset(key, 'reserved_by', user_id)
            await self.redis.expire(key, timeout)
            return True

        return False

    async def release_seat(self, event_id: int,
                          section: str, row: str,
                          seat_number: int):
        key = f"seat:{event_id}:{section}:{row}:{seat_number}"
        await self.redis.hset(key, 'status', 'available')
        await self.redis.hdel(key, 'reserved_by')

```

### Event Cache

```python
class EventCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 300  # 5 minutes

    async def get_event(self, event_id: int) -> dict:
        key = f"event:{event_id}"
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)

        return None

    async def set_event(self, event_id: int, event: dict):
        key = f"event:{event_id}"
        await self.redis.setex(key, self.ttl, json.dumps(event))

    async def invalidate_event(self, event_id: int):
        await self.redis.delete(f"event:{event_id}")

```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── booking.created        (new booking)
├── booking.confirmed     (payment successful)
├── booking.cancelled     (booking cancelled)
├── seat.reserved         (seat temporarily held)
├── seat.booked           (seat permanently booked)
├── payment.processed     (payment completed)
├── ticket.generated      (ticket created)
└── notification.sent     (notification delivered)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "booking.confirmed",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "booking_id": "bkg_456",
    "user_id": "usr_789",
    "event_id": "evt_012",
    "seats": [...],
    "total_amount": 700
  }
}

```

### Event Processing

```python
class BookingEventProcessor:
    def __init__(self, kafka_consumer, notification_service):
        self.consumer = kafka_consumer
        self.notifications = notification_service

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'booking.confirmed':
                await self.handle_booking_confirmed(event)
            elif event['event_type'] == 'booking.cancelled':
                await self.handle_booking_cancelled(event)

    async def handle_booking_confirmed(self, event: dict):
        # Send confirmation email
        await self.notifications.send_email(
            event['data']['user_id'],
            'booking_confirmation',
            event['data']
        )

        # Send SMS with ticket details
        await self.notifications.send_sms(
            event['data']['user_id'],
            'booking_sms',
            event['data']
        )

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
│  Booking     │   │  Booking     │   │  Booking     │
│  Service     │   │  Service     │   │  Service     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘

```

### Database Scaling

```python
class BookingDatabaseScaler:
    def __init__(self):
        self.shards = 16

    def get_shard(self, event_id: int) -> int:
        return event_id % self.shards

    async def get_event_seats(self, event_id: int) -> list:
        shard = self.get_shard(event_id)
        return await self.shards[shard].execute(
            "SELECT * FROM seats WHERE section_id IN "
            "(SELECT id FROM seating_sections WHERE event_id = %s)",
            (event_id,)
        )

```

### Seat Lock Scaling

```python
class SeatLockScaler:
    def __init__(self):
        self.redis_clusters = []  # Multiple Redis clusters

    def get_cluster(self, event_id: int) -> int:
        return event_id % len(self.redis_clusters)

    async def reserve_seat(self, event_id: int,
                          seat: dict, user_id: int) -> bool:
        cluster = self.get_cluster(event_id)
        redis_client = self.redis_clusters[cluster]

        key = f"seat:{event_id}:{seat['section']}:{seat['row']}:{seat['number']}"

        return await redis_client.hsetnx(key, 'status', 'reserved')

```

## Failure Handling

### Reservation Timeout Handler

```python
class ReservationTimeoutHandler:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def start_timeout_processor(self):
        while True:
            try:
                # Find expired reservations
                expired = await self.db.get_expired_reservations()

                for reservation in expired:
                    await self.release_reservation(reservation)

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Timeout processor error: {e}")

    async def release_reservation(self, reservation: dict):
        # Release seats in Redis
        for seat in reservation['seats']:
            key = f"seat:{reservation['event_id']}:{seat['section']}:{seat['row']}:{seat['number']}"
            self.redis.delete(key)

        # Update database
        await self.db.update_reservation_status(
            reservation['id'], 'expired'
        )

```

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| Redis down | Fall back to database locks |
| Payment fails | Release reserved seats |
| Database failover | Read from replica |
| Network partition | Queue operations locally |
| Seat lock timeout | Automatic release |

### Double Booking Prevention

```python
class DoubleBookingPrevention:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def book_seat(self, seat_id: int, booking_id: int) -> bool:
        # Use distributed lock
        lock_key = f"seat_lock:{seat_id}"

        # Try to acquire lock
        lock_acquired = await self.redis.set(
            lock_key, booking_id, nx=True, ex=30
        )

        if not lock_acquired:
            return False

        try:
            # Check seat status
            seat = await self.db.get_seat(seat_id)

            if seat['status'] != 'reserved':
                return False

            # Update to booked
            await self.db.update_seat_status(
                seat_id, 'booked', booking_id
            )

            return True

        finally:
            # Release lock
            await self.redis.delete(lock_key)

```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - bookings_per_minute
  - seat_utilization_rate
  - average_booking_value
  - cancellation_rate

System Metrics:

  - reservation_latency_p95
  - seat_lock_acquisition_time
  - payment_processing_time
  - ticket_generation_time

Infrastructure Metrics:

  - server_cpu_usage
  - memory_usage
  - redis_memory_usage
  - database_connection_pool

```

### Alerting Rules

```yaml
alerts:

  - name: High Booking Rate
    condition: bookings_per_minute > 1000
    severity: info

  - name: Seat Lock Contention
    condition: lock_acquisition_time > 100ms
    severity: warning

  - name: Reservation Expiry Rate High
    condition: expiry_rate > 30%
    severity: warning

  - name: Payment Failure Rate
    condition: payment_failure_rate > 5%
    severity: critical

```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Seat Locking | Redis (fast) | Database (reliable) | Redis with fallback |
| Reservation | Optimistic | Pessimistic | Pessimistic (prevents double booking) |
| Ticket Storage | PDF | QR Code | QR Code (mobile-friendly) |
| Flash Sale | Queue-based | Lock-based | Lock-based (simpler) |

## Interview Questions

### Design Questions

1. **How would you prevent double booking?**

   - Use distributed locks (Redis)
   - Atomic seat status updates
   - Reservation timeout for cleanup
   - Database constraints as fallback

2. **How would you handle flash sales?**

   - Pre-load seat data into Redis
   - Use atomic operations
   - Monitor and scale dynamically
   - Queue overflow handling

3. **How would you implement seat reservations?**

   - Temporary holds with timeout
   - Redis for fast locks
   - Database for persistence
   - Automatic cleanup for expired reservations

### Scaling Questions

4. **How do you scale to 100K concurrent users?**

   - Horizontal scaling of services
   - Redis cluster for seat locks
   - Database sharding by event
   - CDN for static content

5. **How do you handle high concurrency during flash sales?**

   - Pre-warm Redis cache
   - Use atomic operations
   - Monitor and auto-scale
   - Queue overflow handling

### Trade-off Questions

6. **How do you balance consistency vs availability?**

   - Strong consistency for seat booking
   - Eventual consistency for availability checks
   - Reservation timeout for cleanup
   - Fallback to database locks

7. **How do you handle payment failures?**

   - Release reserved seats
   - Allow retry
   - Queue for later processing
   - Notify user

### Senior-level Questions

8. **How would you implement dynamic pricing?**

   - Real-time price calculation
   - A/B testing for pricing
   - Demand-based pricing
   - Price history tracking

9. **How do you handle event cancellations?**

   - Automatic refund processing
   - Notification to all ticket holders
   - Rescheduling options
   - Compensation logic

10. **How would you implement waitlist management?**

    - FIFO queue for waitlist
    - Notification when seats available
    - Time-limited offers
    - Automatic promotion

## Summary

The Ticket Booking system design covers:

- **Seat Management**: Redis-based atomic locking
- **Reservation System**: Temporary holds with timeout
- **Booking Flow**: Reservation → Payment → Confirmation
- **Flash Sale Support**: High concurrency handling
- **Ticket Generation**: QR codes for mobile

Key takeaways:

1. Use Redis for fast, atomic seat locking

2. Implement reservation timeout for cleanup

3. Handle flash sales with pre-warmed caches

4. Prevent double booking with distributed locks

5. Generate QR codes for mobile tickets

This design supports 100K+ concurrent users with strong consistency for seat bookings.

---

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
