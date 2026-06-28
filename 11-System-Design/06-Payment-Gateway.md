# Payment Gateway System Design

## Requirements
### Functional Requirements
- Process credit/debit card payments
- Support multiple payment methods (cards, wallets, bank transfers)
- Handle refunds and chargebacks
- Idempotent payment operations
- Webhook notifications for payment events
- Payment reconciliation
- Merchant onboarding
- Recurring payments (subscriptions)
- Multi-currency support
- Fraud detection

### Non-Functional Requirements
- High availability (99.999% - five nines)
- PCI DSS Level 1 compliance
- Idempotency for all operations
- Sub-second payment processing
- Support 100K+ transactions per second
- Data encryption at rest and in transit
- Audit trail for all operations
- Global payment support

## Capacity Estimation
```
Transaction Estimates:
- 100K transactions per second (peak)
- 10M transactions per day
- Average transaction size: $50
- Daily volume: $500M
- Yearly volume: $182.5B

Storage Estimates:
- Transaction data: 1 KB per transaction
- Daily: 10M × 1 KB = 10 GB
- Yearly: 10 GB × 365 = 3.65 TB
- With 7 year retention: 25.55 TB

Bandwidth Estimates:
- Inbound: 100K × 1 KB = 100 MB/s
- Outbound: 100K × 500 bytes = 50 MB/s
- Total: 150 MB/s peak

Availability Requirements:
- 99.999% uptime = 5.26 minutes downtime per year
- Multi-region deployment
- Active-active across 3+ regions
```

## API Design
```yaml
# Create Payment Intent
POST /api/v1/payment-intents
  Request:
    {
      "amount": 5000,  # cents
      "currency": "usd",
      "customer_id": "cust_123",
      "payment_method": "card",
      "metadata": {
        "order_id": "ord_456",
        "description": "Product purchase"
      }
    }
  Response:
    {
      "id": "pi_789",
      "status": "requires_payment_method",
      "client_secret": "pi_789_secret_abc",
      "amount": 5000,
      "currency": "usd"
    }

# Confirm Payment
POST /api/v1/payment-intents/{id}/confirm
  Request:
    {
      "payment_method": {
        "type": "card",
        "card": {
          "number": "4242424242424242",
          "exp_month": 12,
          "exp_year": 2025,
          "cvc": "123"
        }
      }
    }
  Response:
    {
      "id": "pi_789",
      "status": "succeeded",
      "charge_id": "ch_012"
    }

# Create Refund
POST /api/v1/refunds
  Request:
    {
      "charge_id": "ch_012",
      "amount": 2500,  # partial refund
      "reason": "requested_by_customer"
    }
  Response:
    {
      "id": "ref_345",
      "status": "pending",
      "amount": 2500
    }

# Webhook Endpoint
POST /api/v1/webhooks
  Request:
    {
      "url": "https://merchant.example.com/webhook",
      "events": ["payment.succeeded", "payment.failed"],
      "secret": "whsec_abc123"
    }

# Get Transaction
GET /api/v1/transactions/{id}
  Response:
    {
      "id": "txn_678",
      "type": "charge",
      "amount": 5000,
      "currency": "usd",
      "status": "succeeded",
      "customer_id": "cust_123",
      "created_at": "2025-01-15T10:30:00Z"
    }
```

## Database Design
### Schema
```sql
-- Merchants table
CREATE TABLE merchants (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    webhook_url TEXT,
    webhook_secret VARCHAR(255),
    settlement_currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    merchant_id BIGINT REFERENCES merchants(id),
    email VARCHAR(255),
    name VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment methods (tokenized)
CREATE TABLE payment_methods (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(id),
    type VARCHAR(20) NOT NULL, -- 'card', 'bank_account', 'wallet'
    card_last4 VARCHAR(4),
    card_brand VARCHAR(20),
    card_exp_month INT,
    card_exp_year INT,
    fingerprint VARCHAR(255),  # unique card identifier
    token VARCHAR(255) NOT NULL,  # tokenized by payment processor
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment intents
CREATE TABLE payment_intents (
    id VARCHAR(255) PRIMARY KEY,  # idempotency key
    merchant_id BIGINT REFERENCES merchants(id),
    customer_id BIGINT REFERENCES customers(id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(30) NOT NULL,
    payment_method_id BIGINT,
    client_secret VARCHAR(255),
    metadata JSONB,
    idempotency_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_intents_merchant ON payment_intents(merchant_id);
CREATE INDEX idx_payment_intents_customer ON payment_intents(customer_id);
CREATE INDEX idx_payment_intents_status ON payment_intents(status);

-- Charges
CREATE TABLE charges (
    id VARCHAR(255) PRIMARY KEY,
    payment_intent_id VARCHAR(255) REFERENCES payment_intents(id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    failure_code VARCHAR(50),
    failure_message TEXT,
    processor_response_code VARCHAR(20),
    receipt_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refunds
CREATE TABLE refunds (
    id VARCHAR(255) PRIMARY KEY,
    charge_id VARCHAR(255) REFERENCES charges(id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    reason VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Settlements
CREATE TABLE settlements (
    id BIGSERIAL PRIMARY KEY,
    merchant_id BIGINT REFERENCES merchants(id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    settlement_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhook events
CREATE TABLE webhook_events (
    id BIGSERIAL PRIMARY KEY,
    merchant_id BIGINT REFERENCES merchants(id),
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'pending', 'sent', 'failed'
    attempts INT DEFAULT 0,
    last_attempt_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_webhook_events_merchant ON webhook_events(merchant_id);
CREATE INDEX idx_webhook_events_status ON webhook_events(status);

-- Audit log
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    actor_id BIGINT,
    actor_type VARCHAR(20),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Fraud signals
CREATE TABLE fraud_signals (
    id BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(255) NOT NULL,
    signal_type VARCHAR(50) NOT NULL,
    score DECIMAL(5,4),
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ER Diagram (ASCII)
```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  merchants  │     │   customers     │     │ payment_methods │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ merchant_id(FK) │◄────│ customer_id(FK) │
│ name        │     │ id (PK)         │     │ id (PK)         │
│ email       │     │ email           │     │ type            │
│ api_key     │     │ name            │     │ card_last4      │
│ webhook_url │     │ metadata        │     │ card_brand      │
│ status      │     └─────────────────┘     │ token           │
└─────────────┘              │              │ is_default       │
        │                    │              └─────────────────┘
        │                    │                       │
        │                    ▼                       │
        │           ┌─────────────────┐              │
        │           │payment_intents  │◄─────────────┘
        │           ├─────────────────┤
        │           │ id (PK)         │
        │           │ merchant_id(FK) │
        │           │ customer_id(FK) │
        │           │ amount          │
        │           │ currency        │
        │           │ status          │
        │           │ idempotency_key │
        │           └─────────────────┘
        │                    │
        │                    ▼
        │           ┌─────────────────┐     ┌─────────────────┐
        │           │    charges      │     │    refunds      │
        │           ├─────────────────┤     ├─────────────────┤
        │           │ id (PK)         │◄────│ charge_id (FK)  │
        │           │ payment_intent  │     │ id (PK)         │
        │           │ amount          │     │ amount          │
        │           │ status          │     │ reason          │
        │           │ failure_code    │     │ status          │
        │           └─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│  settlements    │     │ webhook_events  │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ merchant_id(FK) │     │ merchant_id(FK) │
│ amount          │     │ event_type      │
│ status          │     │ payload         │
│ settlement_date │     │ status          │
└─────────────────┘     │ attempts        │
                        └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│              (E-commerce, SaaS, Marketplaces)                    │
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
│  Payment        │  │  Fraud          │  │  Webhook        │
│  Service        │  │  Detection      │  │  Service        │
│  (Processing)   │  │  Service        │  │  (Notifications)│
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (ACID,      │  │  (Idempotency│  │  (Events)   │
     │   Ledger)    │  │   Cache)    │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Payment        │
     │  Processors     │
     │  (Stripe,       │
     │   Adyen, etc.)  │
     └─────────────────┘
```

## Key Components

### Idempotency Service
```python
import hashlib
import json
from redis import Redis

class IdempotencyService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.ttl = 86400  # 24 hours

    def generate_idempotency_key(self, request: dict) -> str:
        # Create deterministic key from request
        key_data = {
            'merchant_id': request['merchant_id'],
            'amount': request['amount'],
            'currency': request['currency'],
            'customer_id': request.get('customer_id'),
            'idempotency_key': request.get('idempotency_key')
        }

        return hashlib.sha256(
            json.dumps(key_data, sort_keys=True).encode()
        ).hexdigest()

    async def check_idempotency(self, key: str) -> dict:
        # Check if request was already processed
        result = await self.redis.get(f"idempotency:{key}")

        if result:
            return json.loads(result)

        # Lock to prevent concurrent processing
        locked = await self.redis.set(
            f"idempotency_lock:{key}",
            "1",
            nx=True,
            ex=30  # 30 second lock
        )

        if not locked:
            raise ConcurrentModificationError("Request in progress")

        return None

    async def store_result(self, key: str, result: dict):
        await self.redis.setex(
            f"idempotency:{key}",
            self.ttl,
            json.dumps(result)
        )
        await self.redis.delete(f"idempotency_lock:{key}")
```

### Payment Processing Service
```python
class PaymentProcessor:
    def __init__(self, db, idempotency_service, fraud_service):
        self.db = db
        self.idempotency = idempotency_service
        self.fraud = fraud_service
        self.processors = {
            'stripe': StripeProcessor(),
            'adyen': AdyenProcessor(),
            'paypal': PayPalProcessor()
        }

    async def process_payment(self, payment_intent: dict) -> dict:
        # Check idempotency
        idempotency_key = self.idempotency.generate_idempotency_key(
            payment_intent
        )

        existing = await self.idempotency.check_idempotency(
            idempotency_key
        )
        if existing:
            return existing

        # Fraud check
        fraud_result = await self.fraud.check_transaction(
            payment_intent
        )

        if fraud_result['action'] == 'block':
            return await self.handle_fraud_block(payment_intent)

        # Route to appropriate processor
        processor = self.select_processor(payment_intent)

        try:
            result = await processor.charge(
                amount=payment_intent['amount'],
                currency=payment_intent['currency'],
                payment_method=payment_intent['payment_method'],
                idempotency_key=idempotency_key
            )

            # Store successful result
            await self.store_payment_result(
                payment_intent, result, 'succeeded'
            )

            # Store idempotency result
            await self.idempotency.store_result(
                idempotency_key, result
            )

            return result

        except PaymentProcessorError as e:
            # Store failed result
            await self.store_payment_result(
                payment_intent,
                {'error': str(e)},
                'failed'
            )
            raise

    def select_processor(self, payment_intent: dict) -> str:
        # Route based on currency, region, or card type
        currency = payment_intent['currency']

        if currency == 'eur':
            return self.processors['adyen']
        elif payment_intent.get('payment_method', {}).get('type') == 'paypal':
            return self.processors['paypal']
        else:
            return self.processors['stripe']
```

### Fraud Detection Service
```python
class FraudDetectionService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
        self.rules = [
            self.check_velocity,
            self.check_amount_limits,
            self.check地理位置,
            self.check_fingerprint
        ]

    async def check_transaction(self, transaction: dict) -> dict:
        signals = []

        # Run all fraud rules
        for rule in self.rules:
            signal = await rule(transaction)
            if signal:
                signals.append(signal)

        # Calculate overall score
        score = self.calculate_fraud_score(signals)

        # Determine action
        if score > 0.8:
            action = 'block'
        elif score > 0.5:
            action = 'review'
        else:
            action = 'approve'

        return {
            'score': score,
            'action': action,
            'signals': signals
        }

    async def check_velocity(self, transaction: dict) -> dict:
        # Check transaction velocity
        customer_id = transaction.get('customer_id')

        # Count transactions in last hour
        key = f"velocity:{customer_id}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 3600)

        if count > 10:  # More than 10 transactions per hour
            return {
                'type': 'velocity',
                'score': 0.3,
                'details': f'{count} transactions in last hour'
            }

        return None

    async def check_amount_limits(self, transaction: dict) -> dict:
        amount = transaction['amount']
        customer_id = transaction.get('customer_id')

        # Get customer's average transaction amount
        avg_amount = await self.db.get_customer_avg_amount(customer_id)

        if amount > avg_amount * 3:  # 3x average
            return {
                'type': 'amount_anomaly',
                'score': 0.2,
                'details': f'Amount {amount} > 3x average {avg_amount}'
            }

        return None
```

### Webhook Service
```python
import hmac
import hashlib
import json
from datetime import datetime, timedelta

class WebhookService:
    def __init__(self, db, http_client):
        self.db = db
        self.http = http_client
        self.max_retries = 5
        self.retry_delays = [1, 5, 30, 300, 3600]  # seconds

    async def send_webhook(self, merchant_id: int, event_type: str,
                          payload: dict):
        # Get merchant webhook config
        merchant = await self.db.get_merchant(merchant_id)

        if not merchant['webhook_url']:
            return

        # Create webhook event
        event = await self.db.create_webhook_event(
            merchant_id=merchant_id,
            event_type=event_type,
            payload=payload
        )

        # Sign payload
        signature = self.sign_payload(
            payload, merchant['webhook_secret']
        )

        # Send with retry
        await self.send_with_retry(
            event['id'],
            merchant['webhook_url'],
            payload,
            signature
        )

    async def send_with_retry(self, event_id: int, url: str,
                             payload: dict, signature: str):
        for attempt in range(self.max_retries):
            try:
                response = await self.http.post(
                    url,
                    json=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'X-Webhook-Signature': signature,
                        'X-Webhook-Attempt': str(attempt + 1)
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    await self.db.update_webhook_event(
                        event_id, status='sent'
                    )
                    return

            except Exception as e:
                pass

            # Wait before retry
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delays[attempt])

        # All retries failed
        await self.db.update_webhook_event(
            event_id, status='failed'
        )

    def sign_payload(self, payload: dict, secret: str) -> str:
        # HMAC-SHA256 signature
        payload_str = json.dumps(payload, sort_keys=True)
        return hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
```

### Reconciliation Service
```python
class ReconciliationService:
    def __init__(self, db, processor_client):
        self.db = db
        self.processor = processor_client

    async def reconcile_daily(self, date: date):
        # Get all transactions for the day
        transactions = await self.db.get_transactions_by_date(date)

        # Get processor settlement report
        processor_report = await self.processor.get_settlement_report(
            date
        )

        # Compare
        discrepancies = []

        for txn in transactions:
            processor_txn = processor_report.get(txn['processor_id'])

            if not processor_txn:
                discrepancies.append({
                    'type': 'missing_in_processor',
                    'transaction_id': txn['id'],
                    'amount': txn['amount']
                })
            elif txn['amount'] != processor_txn['amount']:
                discrepancies.append({
                    'type': 'amount_mismatch',
                    'transaction_id': txn['id'],
                    'our_amount': txn['amount'],
                    'processor_amount': processor_txn['amount']
                })

        # Handle discrepancies
        for discrepancy in discrepancies:
            await self.handle_discrepancy(discrepancy)

        return discrepancies

    async def handle_discrepancy(self, discrepancy: dict):
        # Log for manual review
        await self.db.log_discrepancy(discrepancy)

        # Auto-resolve small discrepancies
        if discrepancy['type'] == 'amount_mismatch':
            diff = abs(discrepancy['our_amount'] -
                      discrepancy['processor_amount'])
            if diff < 100:  # Less than $1
                await self.auto_resolve(discrepancy)
```

## Caching Strategy (Redis)

### Idempotency Cache
```python
class IdempotencyCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 86400  # 24 hours

    async def check_and_lock(self, key: str) -> bool:
        # Atomic check and lock
        result = await self.redis.set(
            f"idempotency:{key}",
            "processing",
            nx=True,
            ex=30
        )
        return result is not None

    async def store_result(self, key: str, result: dict):
        await self.redis.setex(
            f"idempotency:{key}",
            self.ttl,
            json.dumps(result)
        )

    async def get_result(self, key: str) -> dict:
        result = await self.redis.get(f"idempotency:{key}")
        return json.loads(result) if result else None
```

### Rate Limiting Cache
```python
class PaymentRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def check_rate_limit(self, merchant_id: int,
                               limit: int = 1000,
                               window: int = 60) -> bool:
        key = f"rate_limit:{merchant_id}"

        current = await self.redis.get(key)
        if current and int(current) >= limit:
            return False

        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        pipe.execute()

        return True
```

## Message Queue (Kafka)

### Topics and Events
```
Topics:
├── payment.initiated        (payment starts)
├── payment.succeeded        (payment completed)
├── payment.failed           (payment failed)
├── refund.initiated         (refund starts)
├── refund.completed         (refund completed)
├── chargeback.received      (chargeback received)
├── settlement.completed     (settlement processed)
└── webhook.delivered        (webhook sent)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "payment.succeeded",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "payment_intent_id": "pi_456",
    "charge_id": "ch_789",
    "amount": 5000,
    "currency": "usd",
    "merchant_id": "mer_012"
  }
}
```

### Event Processing
```python
class PaymentEventProcessor:
    def __init__(self, kafka_consumer, webhook_service):
        self.consumer = kafka_consumer
        self.webhooks = webhook_service

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'payment.succeeded':
                await self.handle_payment_succeeded(event)
            elif event['event_type'] == 'payment.failed':
                await self.handle_payment_failed(event)

    async def handle_payment_succeeded(self, event: dict):
        # Send webhook to merchant
        await self.webhooks.send_webhook(
            event['data']['merchant_id'],
            'payment.succeeded',
            event['data']
        )

        # Update analytics
        await self.update_analytics(event)
```

## Scaling Strategy

### Horizontal Scaling
```
Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│              (Health checks, SSL termination)            │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Payment     │   │  Payment     │   │  Payment     │
│  Service     │   │  Service     │   │  Service     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Database Scaling
```python
class PaymentDatabaseScaler:
    def __init__(self):
        self.master = None
        self.read_replicas = []

    async def route_query(self, query: str, params: dict):
        if query.startswith('SELECT'):
            # Route to read replica
            replica = self.get_least_loaded_replica()
            return await replica.execute(query, params)
        else:
            # Route to master
            return await self.master.execute(query, params)
```

### Global Deployment
```
Global Architecture:
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
│  Payment Svc │   │  Payment Svc │   │  Payment Svc │
│  DB Primary  │   │  DB Primary  │   │  DB Primary  │
│  Processor   │   │  Processor   │   │  Processor   │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴───────┐
                    │  Kafka Mirror  │
                    │  (Cross-DC)    │
                    └───────────────┘
```

## Failure Handling

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.failure_threshold = 5
        self.reset_timeout = 60
        self.state = 'CLOSED'
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if self.should_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()

        try:
            result = await func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| Payment processor down | Failover to backup processor |
| Database failover | Read from replica, queue writes |
| Redis down | Fall back to database for idempotency |
| Kafka down | Buffer events locally |
| Network partition | Store locally, sync when reconnected |

### Retry Logic
```python
class RetryLogic:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [0.1, 0.5, 1.0]  # seconds

    async def execute_with_retry(self, func, *args, **kwargs):
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except RetryableError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(
                        self.retry_delays[attempt]
                    )
            except NonRetryableError:
                raise

        raise last_exception
```

## Monitoring

### Key Metrics
```yaml
Business Metrics:
  - transactions_per_second
  - success_rate
  - average_transaction_amount
  - total_volume_by_currency

System Metrics:
  - payment_processing_latency_p95
  - api_response_time
  - error_rate_by_type
  - webhook_delivery_rate

Infrastructure Metrics:
  - server_cpu_usage
  - memory_usage
  - database_connection_pool
  - redis_memory_usage
```

### Alerting Rules
```yaml
alerts:
  - name: High Failure Rate
    condition: failure_rate > 5%
    severity: critical

  - name: Processing Latency High
    condition: p95_latency > 2s
    severity: warning

  - name: Webhook Delivery Failed
    condition: webhook_delivery_rate < 95%
    severity: warning

  - name: Reconciliation Discrepancies
    condition: discrepancy_count > 10
    severity: critical
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | PostgreSQL (ACID) | DynamoDB (scale) | PostgreSQL (ACID required) |
| Idempotency | Database | Redis | Redis (faster) |
| Fraud Detection | Rule-based | ML-based | Hybrid approach |
| Webhooks | Synchronous | Async with retry | Async with retry |
| Reconciliation | Real-time | Batch | Batch (daily) |

## Interview Questions

### Design Questions
1. **How would you ensure payment idempotency?**
   - Unique idempotency key per request
   - Redis for fast lookup with TTL
   - Database as source of truth
   - Atomic operations to prevent race conditions

2. **How do you handle payment failures?**
   - Retry with exponential backoff
   - Circuit breaker for processor failures
   - Graceful degradation with fallback processors
   - Clear error messages to merchants

3. **How would you implement fraud detection?**
   - Rule-based checks (velocity, amount limits)
   - Machine learning models
   - Real-time scoring
   - Manual review queue for suspicious transactions

### Scaling Questions
4. **How do you scale to 100K transactions per second?**
   - Horizontal scaling of payment service
   - Database sharding by merchant
   - Redis for hot data
   - Kafka for async processing

5. **How do you handle global payments?**
   - Regional deployment
   - Local payment method support
   - Currency conversion
   - Compliance with local regulations

### Trade-off Questions
6. **How do you balance speed vs security?**
   - Fast path for low-risk transactions
   - Enhanced verification for high-risk
   - Asynchronous fraud checks
   - Customer-initiated verification

7. **How do you handle chargebacks?**
   - Automated evidence collection
   - Merchant notification
   - Dispute resolution workflow
   - Financial impact tracking

### Senior-level Questions
8. **How would you implement PCI compliance?**
   - Tokenization of card data
   - Encrypted storage
   - Access controls
   - Audit logging

9. **How do you ensure data durability?**
   - Write-ahead logging
   - Replication across regions
   - Regular backups
   - Point-in-time recovery

10. **How would you implement multi-currency support?**
    - Real-time exchange rates
    - Settlement in merchant's currency
    - Cross-border fee handling
    - Currency conversion at settlement

## Summary

The Payment Gateway system design covers:
- **Idempotency**: Redis-based with database fallback
- **Fraud Detection**: Rule-based with ML enhancement
- **Webhook Delivery**: Async with retry logic
- **Reconciliation**: Daily batch processing
- **Compliance**: PCI DSS Level 1

Key takeaways:
1. Use idempotency keys for all payment operations
2. Implement circuit breakers for processor failures
3. Use Redis for fast idempotency checks
4. Process webhooks asynchronously with retries
5. Reconcile daily to catch discrepancies

This design supports 100K+ transactions per second with 99.999% availability and full PCI compliance.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
