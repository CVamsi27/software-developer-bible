# Live Betting System Design

## Requirements
### Functional Requirements
- Real-time odds updates
- Place bets on live events
- Cash out before event ends
- Multiple bet types (single, accumulator, system)
- Live event tracking
- Settlement and payout
- User wallet management
- Responsible gambling features
- Multi-sport support
- Live streaming integration

### Non-Functional Requirements
- Ultra-low latency (< 100ms for odds updates)
- High availability (99.99%)
- Handle 100K+ concurrent users
- Process 10K+ bets per second
- Real-time settlement
- Fraud detection
- Regulatory compliance
- Global deployment

## Capacity Estimation
```
User Estimates:
- 1M registered users
- 100K daily active users
- 50K concurrent users at peak

Betting Estimates:
- 10K bets per second at peak
- Average bet: $20
- Daily volume: 1M bets × $20 = $20M
- Yearly volume: $7.3B

Event Estimates:
- 1K live events per day
- Average 100 markets per event
- 100K odds updates per minute

Storage Estimates:
- Bet data: 1M × 500 bytes = 500 MB/day
- Odds history: 100K × 100 bytes = 10 MB/minute
- User data: 1M × 1 KB = 1 GB
- Total: ~1.5 GB/day

Bandwidth Estimates:
- Odds updates: 100K × 100 bytes = 10 MB/s
- Bet placement: 10K × 500 bytes = 5 MB/s
- Live feeds: 1K × 10 KB = 10 MB/s
- Total: ~25 MB/s peak
```

## API Design
```yaml
# Get Live Events
GET /api/v1/events/live
  Query: ?sport=football&page=1
  Response:
    {
      "events": [
        {
          "id": "evt_123",
          "sport": "football",
          "teams": ["Team A", "Team B"],
          "score": "2-1",
          "minute": 65,
          "markets": [...],
          "status": "live"
        }
      ]
    }

# Get Odds
GET /api/v1/events/{id}/odds
  Response:
    {
      "event_id": "evt_123",
      "markets": [
        {
          "id": "mkt_456",
          "name": "Match Winner",
          "outcomes": [
            {"id": "out_789", "name": "Team A", "odds": 1.50},
            {"id": "out_012", "name": "Team B", "odds": 2.50},
            {"id": "out_345", "name": "Draw", "odds": 3.20}
          ]
        }
      ],
      "last_updated": "2025-01-15T10:30:00Z"
    }

# Place Bet
POST /api/v1/bets
  Request:
    {
      "event_id": "evt_123",
      "market_id": "mkt_456",
      "outcome_id": "out_789",
      "amount": 20.00,
      "bet_type": "single"
    }
  Response:
    {
      "bet_id": "bet_345",
      "status": "accepted",
      "potential_payout": 30.00,
      "odds_at_placement": 1.50
    }

# Cash Out
POST /api/v1/bets/{id}/cashout
  Request:
    {
      "amount": 25.00  # cash out amount offered
    }
  Response:
    {
      "bet_id": "bet_345",
      "cashout_amount": 25.00,
      "status": "cashed_out"
    }

# Get User Bets
GET /api/v1/users/{id}/bets
  Query: ?status=open&limit=50
  Response:
    {
      "bets": [...],
      "total_open_bets": 5
    }

# User Wallet
GET /api/v1/users/{id}/wallet
  Response:
    {
      "balance": 150.00,
      "currency": "USD",
      "pending_bets": 20.00
    }

# Deposit
POST /api/v1/users/{id}/wallet/deposit
  Request:
    {
      "amount": 100.00,
      "payment_method": "card",
      "card_token": "tok_abc"
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
    country VARCHAR(2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'active',
    kyc_status VARCHAR(20) DEFAULT 'pending',
    responsible_gambling_limits JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User wallet
CREATE TABLE wallets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) UNIQUE,
    balance DECIMAL(12,2) DEFAULT 0,
    pending_balance DECIMAL(12,2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wallet transactions
CREATE TABLE wallet_transactions (
    id BIGSERIAL PRIMARY KEY,
    wallet_id BIGINT REFERENCES wallets(id),
    type VARCHAR(20) NOT NULL, -- 'deposit', 'withdrawal', 'bet', 'payout', 'cashout'
    amount DECIMAL(12,2) NOT NULL,
    balance_after DECIMAL(12,2) NOT NULL,
    reference_id BIGINT,
    reference_type VARCHAR(20),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Sports table
CREATE TABLE sports (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0
);

-- Events table
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    sport_id BIGINT REFERENCES sports(id),
    name VARCHAR(255) NOT NULL,
    league VARCHAR(255),
    teams JSONB,
    start_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'upcoming',
    score JSONB,
    minute INT,
    is_live BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_sport ON events(sport_id);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_live ON events(is_live) WHERE is_live = TRUE;

-- Markets table
CREATE TABLE markets (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    settlement_value VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_markets_event ON markets(event_id);

-- Outcomes table
CREATE TABLE outcomes (
    id BIGSERIAL PRIMARY KEY,
    market_id BIGINT REFERENCES markets(id),
    name VARCHAR(100) NOT NULL,
    odds DECIMAL(8,4) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    is_winner BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_outcomes_market ON outcomes(market_id);

-- Odds history (for analytics)
CREATE TABLE odds_history (
    id BIGSERIAL PRIMARY KEY,
    outcome_id BIGINT REFERENCES outcomes(id),
    odds DECIMAL(8,4) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (recorded_at);

-- Bets table
CREATE TABLE bets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    event_id BIGINT REFERENCES events(id),
    market_id BIGINT REFERENCES markets(id),
    outcome_id BIGINT REFERENCES outcomes(id),
    amount DECIMAL(12,2) NOT NULL,
    odds DECIMAL(8,4) NOT NULL,
    potential_payout DECIMAL(12,2) NOT NULL,
    bet_type VARCHAR(20) NOT NULL, -- 'single', 'accumulator', 'system'
    status VARCHAR(20) DEFAULT 'open',
    settled_at TIMESTAMP,
    payout_amount DECIMAL(12,2),
    cashout_amount DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_bets_user ON bets(user_id);
CREATE INDEX idx_bets_event ON bets(event_id);
CREATE INDEX idx_bets_status ON bets(status);

-- Bet settlements
CREATE TABLE bet_settlements (
    id BIGSERIAL PRIMARY KEY,
    bet_id BIGINT REFERENCES bets(id),
    settlement_type VARCHAR(20) NOT NULL, -- 'win', 'loss', 'void', 'cashout'
    amount DECIMAL(12,2) NOT NULL,
    settled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Live event feeds
CREATE TABLE live_feeds (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    feed_type VARCHAR(50) NOT NULL,
    feed_url TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ER Diagram (ASCII)
```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users    │     │    events       │     │    sports       │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │     │ id (PK)         │     │ id (PK)         │
│ email       │     │ sport_id (FK)───│────►│ name            │
│ name        │     │ name            │     │ slug            │
│ country     │     │ league          │     │ is_active       │
│ currency    │     │ teams           │     └─────────────────┘
│ status      │     │ start_time      │
│ kyc_status  │     │ status          │
└─────────────┘     │ score           │
        │           │ is_live         │
        │           └─────────────────┘
        │                    │
        ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│    wallets      │  │    markets      │
├─────────────────┤  ├─────────────────┤
│ id (PK)         │  │ id (PK)         │
│ user_id (FK)    │  │ event_id (FK)   │
│ balance         │  │ name            │
│ pending_balance │  │ status          │
│ currency        │  │ settlement_value│
└─────────────────┘  └─────────────────┘
        │                    │
        ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│wallet_transactions│ │    outcomes     │
├─────────────────┤  ├─────────────────┤
│ id (PK)         │  │ id (PK)         │
│ wallet_id (FK)  │  │ market_id (FK)  │
│ type            │  │ name            │
│ amount          │  │ odds            │
│ balance_after   │  │ status          │
│ reference_id    │  │ is_winner       │
│ status          │  └─────────────────┘
└─────────────────┘           │
                              ▼
                    ┌─────────────────┐
                    │      bets       │
                    ├─────────────────┤
                    │ id (PK)         │
                    │ user_id (FK)    │
                    │ event_id (FK)   │
                    │ market_id (FK)  │
                    │ outcome_id (FK) │
                    │ amount          │
                    │ odds            │
                    │ potential_payout│
                    │ bet_type        │
                    │ status          │
                    │ settled_at      │
                    │ payout_amount   │
                    └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│         (Web App, Mobile App, Live Streaming)                    │
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
│  Odds           │  │  Betting        │  │  Settlement     │
│  Service        │  │  Service        │  │  Service        │
│  (Real-time     │  │  (Place Bets,   │  │  (Payouts,      │
│   Updates)      │  │   Cash Out)     │  │   Cash Out)     │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (Bets,      │  │  (Odds,     │  │  (Events,   │
     │   Wallets)   │  │   Sessions) │  │   Settlement)│
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  WebSocket      │
     │  Service        │
     │  (Real-time     │
     │   Updates)      │
     └─────────────────┘
```

## Key Components

### Real-time Odds Service
```python
import asyncio
import json
from datetime import datetime

class OddsService:
    def __init__(self, db, redis_client, websocket_manager):
        self.db = db
        self.redis = redis_client
        self.websocket = websocket_manager
        self.odds_update_interval = 1  # seconds
    
    async def start_odds_updates(self):
        # Background task to update odds
        while True:
            try:
                # Get all live events
                live_events = await self.db.get_live_events()
                
                for event in live_events:
                    # Calculate new odds
                    new_odds = await self.calculate_odds(event)
                    
                    # Update in database
                    await self.update_odds(event['id'], new_odds)
                    
                    # Broadcast to connected clients
                    await self.broadcast_odds(event['id'], new_odds)
                
                await asyncio.sleep(self.odds_update_interval)
                
            except Exception as e:
                logger.error(f"Odds update error: {e}")
    
    async def calculate_odds(self, event: dict) -> dict:
        # Get current market data
        markets = await self.db.get_event_markets(event['id'])
        
        # Apply margin (bookmaker's edge)
        margin = 0.05  # 5% margin
        
        for market in markets:
            for outcome in market['outcomes']:
                # Adjust odds based on:
                # 1. Current score
                # 2. Time remaining
                # 3. Team form
                # 4. Market liquidity
                
                base_odds = await self.get_base_odds(outcome)
                adjusted = base_odds * (1 - margin)
                
                outcome['odds'] = round(adjusted, 2)
        
        return markets
    
    async def broadcast_odds(self, event_id: int, markets: dict):
        # Get all connected clients watching this event
        clients = await self.websocket.get_event_clients(event_id)
        
        message = {
            'type': 'odds_update',
            'event_id': event_id,
            'markets': markets,
            'timestamp': datetime.now().isoformat()
        }
        
        for client in clients:
            await client.send(json.dumps(message))
```

### Betting Service
```python
class BettingService:
    def __init__(self, db, redis_client, odds_service,
                 wallet_service, fraud_service):
        self.db = db
        self.redis = redis_client
        self.odds = odds_service
        self.wallet = wallet_service
        self.fraud = fraud_service
    
    async def place_bet(self, user_id: int, bet_data: dict) -> dict:
        # Validate bet
        await self.validate_bet(user_id, bet_data)
        
        # Check responsible gambling limits
        await self.check_gambling_limits(user_id, bet_data['amount'])
        
        # Fraud check
        fraud_result = await self.fraud.check_bet(user_id, bet_data)
        if fraud_result['action'] == 'block':
            raise FraudDetectedError("Bet blocked")
        
        # Get current odds
        current_odds = await self.odds.get_odds(
            bet_data['outcome_id']
        )
        
        # Lock odds for this bet
        locked_odds = await self.lock_odds(
            bet_data['outcome_id'], bet_data['amount']
        )
        
        # Debit wallet
        await self.wallet.debit(
            user_id, 
            bet_data['amount'],
            reference_type='bet'
        )
        
        # Create bet
        bet = await self.db.create_bet(
            user_id=user_id,
            event_id=bet_data['event_id'],
            market_id=bet_data['market_id'],
            outcome_id=bet_data['outcome_id'],
            amount=bet_data['amount'],
            odds=locked_odds,
            potential_payout=bet_data['amount'] * locked_odds,
            bet_type=bet_data.get('bet_type', 'single')
        )
        
        return {
            'bet_id': bet['id'],
            'status': 'accepted',
            'odds': locked_odds,
            'potential_payout': bet['potential_payout']
        }
    
    async def validate_bet(self, user_id: int, bet_data: dict):
        # Check event is live
        event = await self.db.get_event(bet_data['event_id'])
        if not event['is_live']:
            raise InvalidBetError("Event is not live")
        
        # Check market is open
        market = await self.db.get_market(bet_data['market_id'])
        if market['status'] != 'open':
            raise InvalidBetError("Market is closed")
        
        # Check outcome is active
        outcome = await self.db.get_outcome(bet_data['outcome_id'])
        if outcome['status'] != 'active':
            raise InvalidBetError("Outcome is not active")
        
        # Check minimum/maximum bet
        min_bet = 1.00
        max_bet = 10000.00
        
        if bet_data['amount'] < min_bet:
            raise InvalidBetError(f"Minimum bet is {min_bet}")
        
        if bet_data['amount'] > max_bet:
            raise InvalidBetError(f"Maximum bet is {max_bet}")
    
    async def cash_out(self, bet_id: int, user_id: int) -> dict:
        bet = await self.db.get_bet(bet_id)
        
        if bet['user_id'] != user_id:
            raise PermissionError("Not your bet")
        
        if bet['status'] != 'open':
            raise InvalidBetError("Bet is not open")
        
        # Calculate cash out value
        cashout_value = await self.calculate_cashout(bet)
        
        # Credit wallet
        await self.wallet.credit(
            user_id,
            cashout_value,
            reference_type='cashout'
        )
        
        # Update bet status
        await self.db.update_bet_status(
            bet_id, 'cashed_out', cashout_value
        )
        
        return {
            'bet_id': bet_id,
            'cashout_amount': cashout_value,
            'status': 'cashed_out'
        }
    
    async def calculate_cashout(self, bet: dict) -> float:
        # Get current odds
        current_odds = await self.odds.get_odds(bet['outcome_id'])
        
        # Calculate implied probability
        implied_prob = 1 / current_odds
        
        # Cash out value = original stake × (current odds / original odds)
        cashout = bet['amount'] * (current_odds / bet['odds'])
        
        # Apply cash out margin
        cashout_margin = 0.90  # 10% margin
        return round(cashout * cashout_margin, 2)
```

### Settlement Service
```python
class SettlementService:
    def __init__(self, db, wallet_service, notification_service):
        self.db = db
        self.wallet = wallet_service
        self.notifications = notification_service
    
    async def settle_event(self, event_id: int):
        # Get all open bets for this event
        bets = await self.db.get_open_bets(event_id)
        
        # Get event results
        event = await self.db.get_event(event_id)
        
        for bet in bets:
            try:
                await self.settle_bet(bet, event)
            except Exception as e:
                logger.error(f"Settlement failed for bet {bet['id']}: {e}")
    
    async def settle_bet(self, bet: dict, event: dict):
        # Determine if bet won
        outcome = await self.db.get_outcome(bet['outcome_id'])
        
        if outcome['is_winner']:
            # Calculate payout
            payout = bet['potential_payout']
            
            # Credit wallet
            await self.wallet.credit(
                bet['user_id'],
                payout,
                reference_type='payout'
            )
            
            # Update bet status
            await self.db.settle_bet(
                bet['id'], 'win', payout
            )
            
            # Notify user
            await self.notifications.send_win_notification(
                bet['user_id'], bet, payout
            )
        else:
            # Bet lost
            await self.db.settle_bet(
                bet['id'], 'loss', 0
            )
    
    async def void_bet(self, bet_id: int, reason: str):
        bet = await self.db.get_bet(bet_id)
        
        # Refund stake
        await self.wallet.credit(
            bet['user_id'],
            bet['amount'],
            reference_type='refund'
        )
        
        # Update bet status
        await self.db.settle_bet(bet_id, 'void', bet['amount'])
```

### WebSocket Manager
```python
import websockets
import json
from typing import Dict, Set

class WebSocketManager:
    def __init__(self):
        # event_id -> set of websockets
        self.connections: Dict[int, Set] = {}
    
    async def connect(self, websocket, event_id: int):
        if event_id not in self.connections:
            self.connections[event_id] = set()
        
        self.connections[event_id].add(websocket)
    
    async def disconnect(self, websocket, event_id: int):
        if event_id in self.connections:
            self.connections[event_id].discard(websocket)
            
            if not self.connections[event_id]:
                del self.connections[event_id]
    
    async def broadcast_odds(self, event_id: int, odds_data: dict):
        if event_id not in self.connections:
            return
        
        message = json.dumps({
            'type': 'odds_update',
            'event_id': event_id,
            'data': odds_data
        })
        
        for websocket in self.connections[event_id]:
            try:
                await websocket.send(message)
            except websockets.ConnectionClosed:
                await self.disconnect(websocket, event_id)
    
    async def broadcast_event_update(self, event_id: int, 
                                     event_data: dict):
        if event_id not in self.connections:
            return
        
        message = json.dumps({
            'type': 'event_update',
            'event_id': event_id,
            'data': event_data
        })
        
        for websocket in self.connections[event_id]:
            try:
                await websocket.send(message)
            except websockets.ConnectionClosed:
                await self.disconnect(websocket, event_id)
```

## Caching Strategy (Redis)

### Odds Cache
```python
class OddsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 5  # 5 seconds for live odds
    
    async def get_odds(self, outcome_id: int) -> float:
        key = f"odds:{outcome_id}"
        cached = await self.redis.get(key)
        
        if cached:
            return float(cached)
        
        return None
    
    async def set_odds(self, outcome_id: int, odds: float):
        key = f"odds:{outcome_id}"
        await self.redis.setex(key, self.ttl, odds)
    
    async def get_all_odds(self, event_id: int) -> dict:
        key = f"event_odds:{event_id}"
        cached = await self.redis.get(key)
        
        if cached:
            return json.loads(cached)
        
        return None
    
    async def set_all_odds(self, event_id: int, odds: dict):
        key = f"event_odds:{event_id}"
        await self.redis.setex(key, self.ttl, json.dumps(odds))
```

### Session Cache
```python
class BettingSessionCache:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def track_user_session(self, user_id: int, 
                                 event_id: int):
        key = f"session:{user_id}:{event_id}"
        await self.redis.setex(key, 3600, "1")  # 1 hour
    
    async def get_user_events(self, user_id: int) -> list:
        pattern = f"session:{user_id}:*"
        keys = await self.redis.keys(pattern)
        
        event_ids = []
        for key in keys:
            parts = key.split(':')
            if len(parts) == 3:
                event_ids.append(int(parts[2]))
        
        return event_ids
```

## Message Queue (Kafka)

### Topics and Events
```
Topics:
├── odds.updated           (odds changes)
├── bet.placed             (new bet)
├── bet.settled            (bet settlement)
├── event.started          (event begins)
├── event.ended            (event ends)
├── event.score_changed    (score update)
├── cashout.requested      (cash out request)
└── fraud.detected         (fraud alert)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "bet.placed",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "bet_id": "bet_456",
    "user_id": "usr_789",
    "event_id": "evt_012",
    "amount": 20.00,
    "odds": 1.50
  }
}
```

### Event Processing
```python
class BettingEventProcessor:
    def __init__(self, kafka_consumer, settlement_service,
                 notification_service):
        self.consumer = kafka_consumer
        self.settlement = settlement_service
        self.notifications = notification_service
    
    async def process_events(self):
        async for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'event.ended':
                await self.handle_event_ended(event)
            elif event['event_type'] == 'bet.placed':
                await self.handle_bet_placed(event)
    
    async def handle_event_ended(self, event: dict):
        # Settle all bets for this event
        await self.settlement.settle_event(event['data']['event_id'])
    
    async def handle_bet_placed(self, event: dict):
        # Notify user of bet confirmation
        await self.notifications.send_bet_confirmation(
            event['data']['user_id'],
            event['data']
        )
```

## Scaling Strategy

### Horizontal Scaling
```
Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Odds        │   │  Betting     │   │  Settlement  │
│  Service     │   │  Service     │   │  Service     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Database Sharding
```python
class BettingDatabaseScaler:
    def __init__(self):
        self.shards = 16
    
    def get_user_shard(self, user_id: int) -> int:
        return user_id % self.shards
    
    def get_event_shard(self, event_id: int) -> int:
        return event_id % self.shards
```

### WebSocket Scaling
```python
class WebSocketScaler:
    def __init__(self):
        self.servers = []  # Multiple WebSocket servers
    
    async def handle_connection(self, websocket, event_id):
        # Route to least loaded server
        server = self.get_least_loaded_server()
        
        # Register connection
        await server.register(websocket, event_id)
```

## Failure Handling

### Odds Lock Mechanism
```python
class OddsLockManager:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def lock_odds(self, outcome_id: int, 
                       amount: float) -> float:
        lock_key = f"odds_lock:{outcome_id}"
        
        # Get current odds
        odds = await self.redis.get(f"odds:{outcome_id}")
        
        if not odds:
            raise OddsUnavailableError("Odds not available")
        
        # Lock odds for this bet
        locked = await self.redis.set(
            lock_key, amount, nx=True, ex=30
        )
        
        if not locked:
            # Someone else is betting on same outcome
            # Wait and retry
            await asyncio.sleep(0.1)
            return await self.lock_odds(outcome_id, amount)
        
        return float(odds)
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| Odds service down | Use last known odds with warning |
| Database failover | Read from replica |
| Redis down | Fall back to database |
| WebSocket disconnect | Auto-reconnect |
| Settlement delay | Queue for retry |

### Bet Conflict Resolution
```python
class BetConflictResolver:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
    
    async def resolve_conflict(self, bet_data: dict) -> dict:
        # Check for duplicate bet
        key = f"bet_dedup:{bet_data['user_id']}:{bet_data['outcome_id']}"
        
        exists = await self.redis.exists(key)
        if exists:
            raise DuplicateBetError("Duplicate bet detected")
        
        # Mark as processing
        await self.redis.setex(key, 10, "1")  # 10 second window
        
        # Process bet
        return await self.process_bet(bet_data)
```

## Monitoring

### Key Metrics
```yaml
Business Metrics:
  - bets_per_second
  - total_volume
  - average_bet_size
  - cashout_rate
  - win_rate

System Metrics:
  - odds_update_latency_p99
  - bet_placement_latency_p95
  - settlement_latency
  - websocket_connections
  - api_response_time

Infrastructure Metrics:
  - server_cpu_usage
  - memory_usage
  - redis_memory_usage
  - kafka_consumer_lag
```

### Alerting Rules
```yaml
alerts:
  - name: High Odds Update Latency
    condition: p99_odds_latency > 100ms
    severity: critical
    
  - name: Bet Processing Slow
    condition: p95_bet_latency > 500ms
    severity: warning
    
  - name: Settlement Backlog
    condition: settlement_queue > 1000
    severity: warning
    
  - name: Fraud Detection Spike
    condition: fraud_alerts > 100
    severity: critical
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Odds Storage | Redis (fast) | Database (reliable) | Redis with DB fallback |
| Bet Processing | Sync | Async | Sync for confirmation |
| WebSocket | Single server | Multiple servers | Multiple with load balancing |
| Settlement | Real-time | Batch | Real-time for UX |
| Cash Out | Pre-calculated | On-demand | On-demand |

## Interview Questions

### Design Questions
1. **How would you implement real-time odds updates?**
   - WebSocket for push updates
   - Redis for fast access
   - Background jobs for calculation
   - Event-driven architecture

2. **How do you handle high-concurrency betting?**
   - Atomic operations
   - Distributed locks
   - Queue overflow handling
   - Rate limiting

3. **How would you implement cash out?**
   - Dynamic calculation based on current odds
   - Atomic wallet operations
   - Real-time settlement
   - Fraud detection

### Scaling Questions
4. **How do you scale to 100K concurrent users?**
   - Horizontal scaling
   - WebSocket clustering
   - Database sharding
   - Redis clustering

5. **How do you handle peak betting volumes?**
   - Pre-warm caches
   - Queue-based processing
   - Auto-scaling
   - Rate limiting

### Trade-off Questions
6. **How do you balance speed vs accuracy?**
   - Fast odds updates with eventual accuracy
   - Bet validation with quick confirmation
   - Settlement with verification

7. **How do you handle odds changes during bet placement?**
   - Lock odds for bet duration
   - Accept/reject based on policy
   - Notify user of changes

### Senior-level Questions
8. **How would you implement responsible gambling?**
   - Deposit limits
   - Loss limits
   - Session time limits
   - Self-exclusion

9. **How do you detect and prevent fraud?**
   - Pattern detection
   - Velocity checks
   - Device fingerprinting
   - Account behavior analysis

10. **How would you implement live streaming integration?**
    - Low-latency video feed
    - Synchronized odds display
    - Watch and bet simultaneously
    - Multi-device support

## Summary

The Live Betting system design covers:
- **Real-time Odds**: WebSocket + Redis for < 100ms updates
- **Bet Placement**: Atomic operations with distributed locks
- **Cash Out**: Dynamic calculation with fraud detection
- **Settlement**: Real-time with wallet integration
- **Scalability**: Horizontal scaling with sharding

Key takeaways:
1. Use WebSocket for real-time odds updates
2. Implement atomic bet placement with locks
3. Calculate cash out dynamically based on current odds
4. Settle bets in real-time for better UX
5. Detect fraud with pattern analysis

This design supports 100K+ concurrent users with < 100ms odds updates and 10K+ bets per second.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
