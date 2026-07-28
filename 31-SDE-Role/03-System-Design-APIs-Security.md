---
section: SDE Role
category: Interview
tags: [concept]
---

# System Design, APIs & Security (Phases 16–19)

---

# Phase 16: System Design

> **Why It Matters:** System design is the most important interview round for SDE II+ roles. It tests your ability to architect scalable, reliable, and maintainable systems. You'll typically have 45 minutes to design a complex system from scratch.

## System Design Framework

### The 4-Step Framework (Alex Xu's Method)

```text

Step 1: Requirements Clarification (5-10 min)
├── Functional Requirements
│   └── What should the system do?
├── Non-Functional Requirements
│   ├── Scalability (how many users/requests?)
│   ├── Availability (uptime requirements?)
│   ├── Latency (response time?)
│   ├── Consistency (eventual vs strong?)
│   └── Durability (data loss tolerance?)
└── Capacity Estimation
    ├── Traffic estimates (QPS, bandwidth)
    ├── Storage estimates
    └── Memory/cache estimates

Step 2: High-Level Design (10-15 min)
├── Draw main components
├── Show data flow
├── Identify APIs
└── Choose database type

Step 3: Detailed Design (15-20 min)
├── Deep dive into core components
├── Database schema
├── API design
├── Algorithms for specific problems
└── Caching strategy

Step 4: Wrap Up (5-10 min)
├── Bottlenecks and trade-offs
├── Monitoring and metrics
├── Future improvements
└── Handle follow-up questions

```

### Back-of-Envelope Calculations

```text

Common Numbers to Memorize:
- 1 day = 86,400 seconds ≈ 100,000 seconds
- 1 million requests/day ≈ 12 QPS
- 1 billion requests/day ≈ 12,000 QPS
- 1 KB = 1,000 bytes
- 1 MB = 1,000 KB = 1,000,000 bytes
- 1 GB = 1,000 MB
- 1 TB = 1,000 GB
- 1 PB = 1,000 TB

Typical Numbers:
- User → DB: 100 bytes per user
- Tweet: 300 bytes
- Photo: 200 KB
- Video: 50 MB
- Message: 100 bytes
- URL: 50 bytes

```

## Common System Design Problems

### 1. Design a URL Shortener (TinyURL)

**Requirements:**
- Given a long URL, generate a short URL
- Given a short URL, redirect to original
- Custom aliases (optional)
- Analytics (click count, etc.)

**High-Level Design:**

```text

Client → Load Balancer → Web Server → Cache → Database
                                ↓
                          URL Generation Service
                                ↓
                          Hash/Encode Service

```

**Key Decisions:**
- **Short URL Generation:** Base62 encoding of auto-increment ID or hash
  - MD5/SHA256 hash → take first 7 chars → Base62 encode
  - Auto-increment ID → Base62 encode
- **Database:** Key-value store (DynamoDB, Redis)
- **Caching:** Redis for hot URLs (LRU eviction)
- **Read-heavy:** 90% reads, 10% writes → optimize for reads

**Database Schema:**

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_urls_short_code ON urls(short_code);

```

**API Design:**

```text

POST /api/shorten
Body: { "url": "https://very-long-url.com/path", "custom_alias": "mylink" }
Response: { "short_url": "https://short.ly/abc123" }

GET /{short_code}
Response: 301/302 Redirect to original URL

GET /api/analytics/{short_code}
Response: { "clicks": 1234, "unique_visitors": 890 }

```

**Scaling:**
- **Write:** 100M URLs/day → 1,160 QPS → single DB can handle
- **Read:** 10B reads/day → 115,000 QPS → need caching + multiple replicas
- **Cache:** Redis cluster, 20% cache hit rate reduction → 80% fewer DB reads

---

### 2. Design a Chat System (WhatsApp/Messenger)

**Requirements:**
- 1:1 messaging and group chat
- Online/offline status
- Message delivery status (sent, delivered, read)
- Media sharing
- Push notifications

**High-Level Design:**

```text

Client ←→ WebSocket ←→ Chat Server ←→ Message Queue ←→ Storage
                     ↓
              Presence Service
              Notification Service
              Media Service

```

**Key Decisions:**
- **Connection:** WebSocket for real-time bidirectional communication
- **Storage:** Cassandra/DynamoDB for messages (write-heavy, append-only)
- **User Data:** PostgreSQL for user profiles
- **Message Queue:** Kafka for message routing and persistence
- **Push Notifications:** APNs (iOS), FCM (Android)

**Message Flow:**

```text

1. User A sends message via WebSocket
2. Chat Server receives message
3. Chat Server stores message in database
4. Chat Server checks if User B is online
   a. If online: deliver via WebSocket
   b. If offline: send push notification
5. Update delivery status (sent → delivered → read)

```

**Database Schema:**

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20) UNIQUE,
    status TEXT, -- online, offline, last_seen
    created_at TIMESTAMP
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    type TEXT, -- 'direct' or 'group'
    created_at TIMESTAMP
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID,
    sender_id UUID,
    content TEXT,
    type TEXT, -- 'text', 'image', 'video'
    status TEXT, -- 'sent', 'delivered', 'read'
    created_at TIMESTAMP
);

-- Conversation Members
CREATE TABLE conversation_members (
    conversation_id UUID,
    user_id UUID,
    joined_at TIMESTAMP,
    PRIMARY KEY (conversation_id, user_id)
);

```

**Scaling:**
- **WebSocket:** Each server handles ~50K connections → 1M users need ~20 servers
- **Messages:** Cassandra for write-heavy workload, partition by conversation_id
- **Presence:** Redis for online status (TTL-based heartbeat)

---

### 3. Design a Notification System

**Requirements:**
- Send push notifications, SMS, email
- Support different notification types
- User preferences (opt-in/opt-out)
- Rate limiting
- Analytics (delivery rate, open rate)

**High-Level Design:**

```text

Service A → Notification API → Message Queue → Notification Service → Push/SMS/Email
                                    ↓
                              Preference Service
                              Rate Limiter
                              Analytics Service

```

**Key Decisions:**
- **Message Queue:** Kafka for reliability and ordering
- **Priority:** Separate queues for critical vs non-critical
- **Rate Limiting:** Token bucket per user
- **Templates:** Stored in database, rendered before sending
- **Deduplication:** Check for duplicate notifications

**Notification Flow:**

```text

1. Service sends notification request to API
2. API validates request and enqueues to Kafka
3. Preference Service checks user preferences
4. Rate Limiter checks limits
5. Notification Service dequeues and renders template
6. Notification Service sends via appropriate channel
7. Analytics Service tracks delivery status

```

---

### 4. Design a Rate Limiter

**Requirements:**
- Limit requests per user/IP per time window
- Return 429 Too Many Requests when exceeded
- Support different limits per API
- Distributed (works across multiple servers)

**Algorithms:**

```java
// Token Bucket
class TokenBucket {
    private final int capacity;
    private final int refillRate; // tokens per second
    private double tokens;
    private long lastRefillTime;

    TokenBucket(int capacity, int refillRate) {
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.tokens = capacity;
        this.lastRefillTime = System.currentTimeMillis();
    }

    synchronized boolean allowRequest() {
        refill();
        if (tokens >= 1) {
            tokens--;
            return true;
        }
        return false;
    }

    private void refill() {
        long now = System.currentTimeMillis();
        double elapsed = (now - lastRefillTime) / 1000.0;
        tokens = Math.min(capacity, tokens + elapsed * refillRate);
        lastRefillTime = now;
    }
}

// Sliding Window Log
class SlidingWindowLog {
    private final Map<String, LinkedList<Long>> userLogs = new HashMap<>();
    private final int maxRequests;
    private final long windowSizeMs;

    SlidingWindowLog(int maxRequests, long windowSizeMs) {
        this.maxRequests = maxRequests;
        this.windowSizeMs = windowSizeMs;
    }

    synchronized boolean allowRequest(String userId) {
        long now = System.currentTimeMillis();
        userLogs.putIfAbsent(userId, new LinkedList<>());
        LinkedList<Long> logs = userLogs.get(userId);

        // Remove old entries
        while (!logs.isEmpty() && logs.getFirst() <= now - windowSizeMs) {
            logs.removeFirst();
        }

        if (logs.size() < maxRequests) {
            logs.addLast(now);
            return true;
        }
        return false;
    }
}

```

**Distributed Rate Limiting:**
- Redis for shared state across servers
- Lua scripts for atomic operations
- Consistent hashing for partitioning by user ID

---

### 5. Design a Web Crawler

**Requirements:**
- Crawl billions of web pages
- Respect robots.txt
- Handle duplicate URLs
- Politeness (don't overwhelm servers)
- Freshness (re-crawl periodically)

**High-Level Design:**

```text

URL Frontier → Fetcher → Parser → Content Processor
     ↓              ↓          ↓
  DNS Resolver   robots.txt  Dedup Service
                    Cache    URL Extractor

```

**Key Decisions:**
- **URL Frontier:** Priority queue with politeness constraints
- **Deduplication:** Bloom filter for URL dedup, SimHash for content dedup
- **Storage:** HDFS/S3 for raw content, metadata in database
- **Parallelism:** Multiple fetcher threads, distributed across machines

---

### 6. Design a Key-Value Store (Redis-like)

**Requirements:**
- put(key, value) and get(key)
- TTL (time-to-live) support
- Replication for high availability
- Partitioning for scalability

**Architecture:**

```text

Client → Proxy → Coordinator → Partition Servers
                                  ↓
                              Storage Engine (LSM-Tree)
                                  ↓
                              Write-Ahead Log

```

**Key Decisions:**
- **Partitioning:** Consistent hashing
- **Replication:** Leader-follower with async replication
- **Consistency:** Quorum reads/writes (W + R > N)
- **Conflict Resolution:** Vector clocks or last-write-wins

---

### 7. Design a Social Media Feed

**Requirements:**
- Users can post content
- Home feed shows posts from followed users
- Real-time updates
- Like, comment, share

**Architecture:**

```text

Post Service → Fan-out Service → Feed Service
                ↓
          User Graph Service
          Media Service
          Notification Service

```

**Fan-out Strategies:**
- **Fan-out on Write:** Pre-compute feeds when post is created
  - Pros: Fast read
  - Cons: Write amplification, celebrity problem
- **Fan-out on Read:** Compute feed when user opens app
  - Pros: No write amplification
  - Cons: Slow read
- **Hybrid:** Fan-out on write for regular users, fan-out on read for celebrities

---

### 8. Design a Search Autocomplete

**Requirements:**
- Type prefix → show top suggestions
- Real-time suggestions as user types
- Popular/trending suggestions
- Personalized suggestions

**Architecture:**

```text

Client → API Gateway → Autocomplete Service → Trie Service
                                                ↓
                                          Analytics Service
                                          Trending Service

```

**Key Decisions:**
- **Data Structure:** Trie with frequency counts
- **Ranking:** Frequency-based, time-decayed
- **Caching:** Redis for top queries per prefix
- **Update:** Batch updates to trie (not real-time)

---

## System Design Concepts Deep Dive

### CAP Theorem

```text

In a distributed system, you can only guarantee 2 of 3:
├── Consistency — every read gets the most recent write
├── Availability — every request gets a response
└── Partition Tolerance — system works despite network failures

Since network partitions are inevitable:
- CP Systems: Consistent but may be unavailable (e.g., HBase, MongoDB)
- AP Systems: Available but may be inconsistent (e.g., Cassandra, DynamoDB)

```

### Consistent Hashing

```text

- Maps both servers and keys to a hash ring
- Adding/removing server only affects nearby keys
- Virtual nodes: each server maps to multiple points on ring
- Reduces hotspots and improves distribution

```

### Database Scaling

```text

Read Scaling:
- Read replicas (primary-replica replication)
- Caching layer (Redis, Memcached)
- CDN for static content

Write Scaling:
- Sharding (horizontal partitioning)
- Write-ahead logging
- Event sourcing

Vertical Scaling:
- More CPU, RAM, storage
- Simpler but has limits

```

### Message Queues

```text

When to Use:
- Decouple services
- Buffer writes during traffic spikes
- Async processing
- Event-driven architecture

Popular Options:
├── Kafka — high throughput, durable, ordered
├── RabbitMQ — flexible routing, AMQP
├── SQS — managed, simple
└── Pulsar — multi-tenant, tiered storage

```

### Microservices vs Monolith

```text

Monolith:
├── Pros: Simple deployment, easy debugging, no network overhead
├── Cons: Scaling entire app, tight coupling, tech lock-in
└── When: Small team, early stage, simple domain

Microservices:
├── Pros: Independent scaling, tech flexibility, team autonomy
├── Cons: Distributed complexity, network latency, debugging hard
└── When: Large team, complex domain, multiple products

```

## System Design Problems to Practice

| Problem | Key Concepts | Company |
|---------|-------------|---------|
| Design URL Shortener | Hashing, Caching, Database | Google, Amazon |
| Design Twitter/News Feed | Fan-out, Social Graph, Caching | Twitter, Meta |
| Design WhatsApp/Messenger | WebSocket, Message Queue, Storage | Meta, Microsoft |
| Design YouTube/Netflix | CDN, Video Processing, Streaming | Netflix, Google |
| Design Uber/Lyft | Geospatial Indexing, Real-time | Uber, Lyft |
| Design Instagram | CDN, Image Processing, Feed | Meta |
| Design Dropbox/Google Drive | File Sync, Chunking, Conflict | Google, Dropbox |
| Design Rate Limiter | Token Bucket, Sliding Window | All |
| Design Notification System | Message Queue, Priority | All |
| Design Search Autocomplete | Trie, Ranking, Caching | Google, Amazon |
| Design Payment System | Idempotency, Consistency | Stripe, PayPal |
| Design Ticket Booking | Concurrency, Inventory | Booking, Uber |
| Design E-Commerce | Catalog, Cart, Orders | Amazon, Shopify |
| Design Google Maps | Graph Algorithms, Tile System | Google |
| Design Chat System | WebSocket, Message Queue | All |

### Resources for System Design

- 📘 **Book:** *System Design Interview (Vol 1 & 2)* by Alex Xu — **MUST READ**
- 📘 **Book:** *Designing Data-Intensive Applications* by Martin Kleppmann — **MUST READ**
- 📘 **Book:** *System Design at Google* — engineering insights
- 🎥 **YouTube:** [ByteByteGo](https://www.youtube.com/@ByteByteGo) — visual system design
- 🎥 **YouTube:** [Hello Interview](https://www.youtube.com/@HelloInterview) — structured approach
- 🎥 **YouTube:** [Gaurav Sen](https://www.youtube.com/@gauravsen) — foundational concepts
- 🎥 **YouTube:** [Hussein Nasser](https://www.youtube.com/@husseinnasser) — backend deep dives
- 🌐 **Website:** [System Design Primer](https://github.com/donnemartin/system-design-primer) — free GitHub resource
- 🌐 **Website:** [Exponent](https://www.tryexponent.com/) — mock interviews
- 🌐 **Website:** [Codemia.io](https://codemia.io/) — LeetCode for system design
- 🌐 **Website:** [IGotAnOffer](https://igotanoffer.com/) — 1-on-1 mock interviews with ex-FAANG

---

# Phase 17: REST API Design

> **Why It Matters:** REST APIs are the backbone of modern web applications. Designing clean, consistent, and well-documented APIs is a critical skill for any SDE.

## REST Principles

```text

1. Client-Server Architecture
   - Separation of concerns
   - Client handles UI, server handles data

2. Stateless
   - Each request contains all information needed
   - Server doesn't store client context

3. Cacheable
   - Responses must define themselves as cacheable or not
   - Improves performance and scalability

4. Uniform Interface
   - Resource-based URLs
   - Standard HTTP methods
   - HATEOAS (optional)
   - Resource representation (JSON, XML)

```

## URL Design

```text

Good:
GET    /api/v1/users           — list users
GET    /api/v1/users/123       — get user 123
POST   /api/v1/users           — create user
PUT    /api/v1/users/123       — update user 123
DELETE /api/v1/users/123       — delete user 123

Nested Resources:
GET    /api/v1/users/123/orders         — orders for user 123
GET    /api/v1/users/123/orders/456     — order 456 for user 123

Bad:
GET /api/getUser?id=123
POST /api/deleteUser
GET /api/user_list

```

## HTTP Methods

| Method | Purpose | Idempotent | Safe | Request Body | Response |
|--------|---------|-----------|------|--------------|----------|
| GET | Read resource | Yes | Yes | No | 200 OK |
| POST | Create resource | No | No | Yes | 201 Created |
| PUT | Replace resource | Yes | No | Yes | 200 OK |
| PATCH | Partial update | No | No | Yes | 200 OK |
| DELETE | Delete resource | Yes | No | No | 204 No Content |

## Status Codes

```java
// 2xx Success
200 OK                    — successful request
201 Created               — resource created
202 Accepted              — request accepted, processing async
204 No Content            — success, no response body

// 3xx Redirection
301 Moved Permanently     — resource moved permanently
304 Not Modified          — use cached version

// 4xx Client Error
400 Bad Request           — invalid request body/parameters
401 Unauthorized          — authentication required
403 Forbidden             — authenticated but not authorized
404 Not Found             — resource doesn't exist
405 Method Not Allowed    — HTTP method not supported
409 Conflict              — conflict with current state
422 Unprocessable Entity  — validation failed
429 Too Many Requests     — rate limit exceeded

// 5xx Server Error
500 Internal Server Error — unexpected error
502 Bad Gateway           — upstream service error
503 Service Unavailable   — service temporarily down
504 Gateway Timeout       — upstream service timeout

```

## Request/Response Design

```json
// GET /api/v1/users/123
// Response 200 OK
{
    "id": 123,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:00Z",
    "_links": {
        "self": "/api/v1/users/123",
        "orders": "/api/v1/users/123/orders"
    }
}

// POST /api/v1/users
// Request Body
{
    "name": "Bob Jones",
    "email": "bob@example.com",
    "password": "securepassword123"
}

// Response 201 Created
{
    "id": 124,
    "name": "Bob Jones",
    "email": "bob@example.com",
    "created_at": "2024-07-20T14:00:00Z"
}

// Error Response 422 Unprocessable Entity
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": [
            {
                "field": "email",
                "message": "Email already exists"
            },
            {
                "field": "password",
                "message": "Password must be at least 8 characters"
            }
        ]
    }
}

```

## Pagination

```java
// Offset-based pagination
GET /api/v1/users?page=1&limit=20
GET /api/v1/users?page=2&limit=20

// Response with pagination metadata
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 150,
        "total_pages": 8,
        "has_next": true,
        "has_prev": false
    }
}

// Cursor-based pagination (better for large datasets)
GET /api/v1/users?cursor=abc123&limit=20

// Response
{
    "data": [...],
    "pagination": {
        "next_cursor": "def456",
        "has_next": true
    }
}

```

## Filtering, Sorting, Searching

```java
// Filtering
GET /api/v1/users?status=active&role=admin
GET /api/v1/orders?created_after=2024-01-01&created_before=2024-12-31
GET /api/v1/products?price_min=10&price_max=100

// Sorting
GET /api/v1/users?sort=name          — ascending
GET /api/v1/users?sort=-name         — descending (prefix with -)
GET /api/v1/users?sort=-created_at,name  — multiple sort fields

// Searching
GET /api/v1/users?q=alice
GET /api/v1/products?q=laptop&category=electronics

```

## API Versioning

```text

# URL versioning (most common)
/api/v1/users
/api/v2/users

# Header versioning
Accept: application/vnd.myapp.v2+json

# Query parameter
/api/users?version=2

```

## Authentication & Authorization

```java
// JWT Token in Authorization header
GET /api/v1/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

// API Key in header
GET /api/v1/data
X-API-Key: your-api-key-here

// OAuth2 flow
POST /oauth/token
{
    "grant_type": "authorization_code",
    "code": "auth_code_here",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}

```

## Rate Limiting

```java
// Response headers
X-RateLimit-Limit: 100        // max requests per window
X-RateLimit-Remaining: 75     // remaining requests
X-RateLimit-Reset: 1625000000 // when window resets

// 429 Too Many Requests
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Too many requests. Try again in 60 seconds.",
        "retry_after": 60
    }
}

```

## API Best Practices

```text

1. Use nouns for resources, not verbs
   ✅ GET /users
   ❌ GET /getUsers

2. Use plural nouns
   ✅ /users/123
   ❌ /user/123

3. Use HTTP methods for actions
   ✅ DELETE /users/123
   ❌ POST /deleteUser

4. Version your APIs
   ✅ /api/v1/users
   ❌ /api/users

5. Use consistent naming (kebab-case for URLs)
   ✅ /order-items
   ❌ /orderItems

6. Return appropriate status codes

7. Use pagination for list endpoints

8. Provide useful error messages

9. Use HATEOAS for discoverability (optional)

10. Document your APIs (OpenAPI/Swagger)

```

### Resources for REST API Design

- 📘 **Book:** *RESTful Web APIs* by Leonard Richardson
- 📘 **Book:** *Designing Web APIs* by Brenda Jin
- 🌐 **Website:** [RESTful API Design](https://restfulapi.net/) — best practices
- 🌐 **Website:** [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- 🌐 **Website:** [Google API Design Guide](https://cloud.google.com/apis/design)
- 🌐 **Website:** [JSON:API](https://jsonapi.org/) — specification
- 🌐 **Website:** [OpenAPI/Swagger](https://swagger.io/) — API documentation

---

# Phase 18: Security

> **Why It Matters:** Security vulnerabilities can be catastrophic. Interviewers expect you to know common attack vectors and how to prevent them.

## Common Vulnerabilities

### 1. SQL Injection

```java
// BAD — vulnerable to SQL injection
String query = "SELECT * FROM users WHERE email = '" + email + "'";
// If email = "'; DROP TABLE users; --"
// Query becomes: SELECT * FROM users WHERE email = ''; DROP TABLE users; --'

// GOOD — use parameterized queries
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?"
);
stmt.setString(1, email);
ResultSet rs = stmt.executeQuery();

// GOOD — use ORM (Prisma, Hibernate)
User user = userRepository.findByEmail(email);

```

### 2. Cross-Site Scripting (XSS)

```text

Types:
1. Stored XSS — malicious script stored in database
2. Reflected XSS — script in URL parameter
3. DOM-based XSS — script executes in browser

Prevention:
- Escape output: & → &amp;, < → &lt;, > → &gt;
- Content Security Policy (CSP) headers
- Input validation and sanitization
- Use framework's built-in escaping (React escapes by default)

```

```java
// BAD — directly rendering user input
<div dangerouslySetInnerHTML={{__html: userComment}} />

// GOOD — React escapes automatically
<div>{userComment}</div>

// Server-side: sanitize HTML input
String sanitized = Jsoup.clean(userInput, Safelist.basic());

```

### 3. Cross-Site Request Forgery (CSRF)

```text

Attack: Malicious site makes requests to your site using user's cookies

Prevention:
- CSRF tokens — unique token per session
- SameSite cookie attribute
- Check Origin/Referer headers
- Require re-authentication for sensitive actions

```

```java
// Backend: generate and validate CSRF token
@PostMapping("/transfer")
public ResponseEntity<?> transfer(
        @RequestHeader("X-CSRF-Token") String csrfToken,
        @RequestBody TransferRequest request) {
    if (!csrfTokenService.validate(csrfToken)) {
        throw new ForbiddenException("Invalid CSRF token");
    }
    // process transfer
}

```

### 4. Authentication Attacks

```text

Brute Force:
- Rate limiting
- Account lockout after N failed attempts
- CAPTCHA after suspicious activity
- Use bcrypt/scrypt/argon2 for password hashing (NOT MD5/SHA)

Session Hijacking:
- Use secure, httpOnly cookies
- Regenerate session ID after login
- Set appropriate session timeout

Credential Stuffing:
- Require strong passwords
- Enable MFA (multi-factor authentication)
- Monitor for unusual login patterns

```

### 5. Insecure Direct Object References (IDOR)

```java
// BAD — user can access any resource by ID
@GetMapping("/api/orders/{id}")
public Order getOrder(@PathVariable Long id) {
    return orderRepository.findById(id); // no ownership check!
}

// GOOD — verify ownership
@GetMapping("/api/orders/{id}")
public Order getOrder(@PathVariable Long id) {
    Order order = orderRepository.findById(id);
    if (!order.getUserId().equals(currentUserId)) {
        throw new ForbiddenException("Access denied");
    }
    return order;
}

```

## Encryption

```java
// Symmetric Encryption (AES) — same key for encrypt/decrypt
// Use for: data at rest, file encryption
SecretKey key = new SecretKeySpec(keyBytes, "AES");
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
cipher.init(Cipher.ENCRYPT_MODE, key);
byte[] encrypted = cipher.doFinal(plaintext);

// Asymmetric Encryption (RSA) — public key encrypt, private key decrypt
// Use for: key exchange, digital signatures
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);
KeyPair keyPair = keyGen.generateKeyPair();

// Hashing (one-way)
// Use for: passwords, data integrity
String hashed = BCrypt.hashpw(password, BCrypt.gensalt(12));
boolean matches = BCrypt.checkpw(password, hashed);

```

## Password Storage

```java
// NEVER store plaintext passwords
// NEVER use MD5 or SHA for passwords (too fast)

// GOOD — use bcrypt, scrypt, or argon2
// bcrypt: slow, adaptive, includes salt
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));
// Verify
boolean valid = BCrypt.checkpw(password, hash);

// scrypt: memory-hard, ASIC-resistant
// argon2: winner of Password Hashing Competition

```

## CORS (Cross-Origin Resource Sharing)

```java
// Configure CORS properly
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://yourdomain.com")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}

```

## JWT Security

```text

JWT Structure: Header.Payload.Signature

Best Practices:
- Use RS256 (asymmetric) over HS256 (symmetric) for microservices
- Set short expiration (15 min for access tokens)
- Use refresh tokens for long-lived sessions
- Store tokens in httpOnly, secure cookies (not localStorage)
- Validate signature, expiration, issuer, audience
- Include token revocation mechanism

```

```java
// JWT validation
public Claims validateToken(String token) {
    return Jwts.parserBuilder()
        .setSigningKey(publicKey)
        .requireIssuer("your-app")
        .requireAudience("your-api")
        .build()
        .parseClaimsJws(token)
        .getBody();
}

// Token refresh flow
@PostMapping("/auth/refresh")
public ResponseEntity<?> refreshToken(@RequestBody RefreshTokenRequest request) {
    // validate refresh token
    // issue new access token
    // optionally issue new refresh token
}

```

## Security Checklist for Interviews

```text

Authentication:
✅ Use bcrypt/argon2 for password hashing
✅ Implement MFA
✅ Use JWT with short expiration + refresh tokens
✅ Rate limit login attempts
✅ Account lockout after failures

Authorization:
✅ RBAC (Role-Based Access Control)
✅ Validate ownership on every request
✅ Principle of least privilege

Data Protection:
✅ Encrypt sensitive data at rest and in transit
✅ Use HTTPS everywhere
✅ Sanitize all user input
✅ Parameterized queries (no SQL injection)

API Security:
✅ Rate limiting
✅ Input validation
✅ CORS properly configured
✅ Security headers (CSP, X-Frame-Options, etc.)
✅ API versioning

Monitoring:
✅ Log security events
✅ Alert on suspicious activity
✅ Regular security audits

```

### Resources for Security

- 📘 **Book:** *Web Application Hacker's Handbook* — comprehensive web security
- 📘 **Book:** *OWASP Top 10* — common vulnerabilities
- 🌐 **Website:** [OWASP](https://owasp.org/) — Open Web Application Security Project
- 🌐 **Website:** [PortSwigger Web Security Academy](https://portswigger.net/web-security) — free labs
- 🌐 **Website:** [CWE/SANS Top 25](https://cwe.mitre.org/top25/) — most dangerous software errors
- 🌐 **Website:** [Auth0 Blog](https://auth0.com/blog/) — authentication best practices

---

# Phase 19: Concurrency & Multithreading

> **Why It Matters:** Concurrency is essential for building high-performance systems. Interviewers test your ability to reason about parallel execution, synchronization, and common pitfalls.

## Thread Basics

```java
// Creating threads
// 1. Extend Thread
class Worker extends Thread {
    public void run() {
        System.out.println("Worker running in " + Thread.currentThread().getName());
    }
}
new Worker().start();

// 2. Implement Runnable (preferred)
Runnable task = () -> System.out.println("Running");
new Thread(task).start();

// 3. Callable (returns result)
Callable<Integer> callable = () -> {
    Thread.sleep(1000);
    return 42;
};
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(callable);
int result = future.get(); // blocks

// 4. Virtual Threads (Java 21+)
Thread.startVirtualThread(() -> System.out.println("Virtual thread"));

```

## Synchronization

```java
// synchronized keyword
class Counter {
    private int count = 0;

    // Method-level lock
    public synchronized void increment() {
        count++;
    }

    // Block-level lock
    public void decrement() {
        synchronized (this) {
            count--;
        }
    }
}

// ReentrantLock (more flexible)
class FlexibleLock {
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notEmpty = lock.newCondition();
    private final Queue<Integer> queue = new LinkedList<>();

    public void produce(int item) {
        lock.lock();
        try {
            while (queue.size() == 10) {
                notEmpty.await(); // wait for space
            }
            queue.add(item);
            notEmpty.signalAll(); // notify consumers
        } finally {
            lock.unlock();
        }
    }

    public int consume() {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                notEmpty.await(); // wait for items
            }
            return queue.poll();
        } finally {
            lock.unlock();
        }
    }
}

```

## Common Concurrency Problems

### Producer-Consumer

```java
class BoundedBuffer<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    BoundedBuffer(int capacity) { this.capacity = capacity; }

    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (queue.size() == capacity) notFull.await();
            queue.add(item);
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (queue.isEmpty()) notEmpty.await();
            T item = queue.poll();
            notFull.signal();
            return item;
        } finally {
            lock.unlock();
        }
    }
}

```

### Readers-Writers Problem

```java
class ReadWriteLock {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Lock readLock = rwLock.readLock();
    private final Lock writeLock = rwLock.writeLock();
    private int readers = 0;

    public void read() {
        readLock.lock();
        try {
            readers++;
            // read operation
        } finally {
            readers--;
            readLock.unlock();
        }
    }

    public void write() {
        writeLock.lock();
        try {
            // write operation
        } finally {
            writeLock.unlock();
        }
    }
}

```

### Dining Philosophers

```java
// Prevent deadlock by ordering forks
class Philosopher implements Runnable {
    private final int id;
    private final ReentrantLock leftFork;
    private final ReentrantLock rightFork;

    Philosopher(int id, ReentrantLock left, ReentrantLock right) {
        this.id = id;
        this.leftFork = left;
        this.fork = right;
    }

    public void run() {
        while (true) {
            think();
            // Always pick up lower-numbered fork first
            ReentrantLock first = Math.min(leftFork, rightFork) == leftFork ? leftFork : rightFork;
            ReentrantLock second = first == leftFork ? rightFork : leftFork;
            first.lock();
            second.lock();
            try {
                eat();
            } finally {
                second.unlock();
                first.unlock();
            }
        }
    }
}

```

## CompletableFuture

```java
// Sequential composition
CompletableFuture.supplyAsync(() -> fetchUser(userId))
    .thenApply(user -> fetchOrders(user.getId()))
    .thenApply(orders -> calculateTotal(orders))
    .thenAccept(total -> System.out.println("Total: " + total))
    .exceptionally(ex -> {
        System.out.println("Error: " + ex.getMessage());
        return null;
    });

// Parallel composition
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> callServiceA());
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> callServiceB());

// Wait for both
CompletableFuture<Void> both = CompletableFuture.allOf(future1, future2);
both.thenRun(() -> {
    String result1 = future1.join();
    String result2 = future2.join();
    System.out.println(result1 + result2);
});

// Wait for first (race)
CompletableFuture<Object> first = CompletableFuture.anyOf(future1, future2);
first.thenAccept(result -> System.out.println("Winner: " + result));

```

## Thread Safety Patterns

```java
// Immutable objects (inherently thread-safe)
final class ImmutablePoint {
    private final int x;
    private final int y;

    ImmutablePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }
}

// Thread-local storage
ThreadLocal<Integer> threadLocal = ThreadLocal.withInitial(() -> 0);
threadLocal.set(42);
int value = threadLocal.get();

// Atomic operations
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet(); // atomic increment
counter.compareAndSet(5, 10); // CAS operation

// ConcurrentHashMap
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.putIfAbsent("key", 1);
map.compute("key", (k, v) -> v == null ? 1 : v + 1);

```

## Concurrency Problems

| Problem | Difficulty | Topic |
|---------|-----------|-------|
| [Print in Order](https://leetcode.com/problems/print-in-order/) | Easy | Synchronization |
| [Print FooBar Alternately](https://leetcode.com/problems/print-foobar-alternately/) | Medium | Synchronization |
| [Print Zero Even Odd](https://leetcode.com/problems/print-zero-even-odd/) | Medium | Synchronization |
| [Fizz Buzz Multithreaded](https://leetcode.com/problems/fizz-buzz-multithreaded/) | Medium | Synchronization |
| [Building H2O](https://leetcode.com/problems/building-h2o/) | Medium | Semaphore |
| [The Dining Philosophers](https://leetcode.com/problems/the-dining-philosophers/) | Medium | Deadlock prevention |
| [Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded/) | Medium | Concurrency |
| [Design Bounded Blocking Queue](https://leetcode.com/problems/design-bounded-blocking-queue/) | Medium | Producer-Consumer |
| [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) | Medium | Concurrency |
| [Fetch Data Sequentially](https://leetcode.com/problems/fetch-data-sequentially/) | Medium | CompletableFuture |

### Resources for Concurrency

- 📘 **Book:** *Java Concurrency in Practice* by Brian Goetz — **MUST READ**
- 📘 **Book:** *Concurrent Programming in Java* by Doug Lea
- 🌐 **Website:** [Baeldung Java Concurrency](https://www.baeldung.com/java-concurrency)
- 🎥 **YouTube:** [Jakob Jenkov](https://www.youtube.com/@JakobJenkov) — Java concurrency

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
| [Core CS Fundamentals](02-Core-CS-Fundamentals.md) | Phases 9-16: CS Fundamentals, NoSQL |
| [System Design & APIs](03-System-Design-APIs-Security.md) | Phases 17-20: System Design, REST, Security |
| [DevOps & Career](04-DevOps-Behavioral-Career.md) | Phases 21-28: Git, Linux, Behavioral, Cloud |
| [Advanced Topics](05-Advanced-Topics.md) | Segment Tree, DI, Repository, MVC |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week intensive study plan |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
| [Microsoft Guide](16-Microsoft-Azure-Interview-Guide.md) | Microsoft Azure team-specific prep |
| [Progress Tracker](08-Progress-Tracker.md) | Track your weekly progress |
| [Mock Interview Bank](09-Mock-Interview-Question-Bank.md) | 90 questions (Coding + SD + Behavioral) |
| [Google Guide](17-Google-Interview-Guide.md) | Google-specific interview prep |
| [Amazon Guide](18-Amazon-Interview-Guide.md) | Amazon Leadership Principles prep |
| [Meta Guide](19-Meta-Interview-Guide.md) | Meta-specific interview prep |
| [Apple Guide](20-Apple-Interview-Guide.md) | Apple-specific interview prep |
---


## Summary

This guide covers system design concepts, API design principles, and security fundamentals for senior engineering interviews. Topics include distributed systems, architectural patterns, authentication, authorization, and secure coding practices.

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)

## See Also
- [JavaScript](../01-JavaScript/)
- [TypeScript](../02-TypeScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
