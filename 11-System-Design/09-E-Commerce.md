# E-Commerce System Design

## Requirements
### Functional Requirements
- Product catalog with search and filtering
- Shopping cart management
- Checkout process
- Inventory management
- Order management
- User accounts and profiles
- Payment processing
- Shipping and delivery tracking
- Reviews and ratings
- Wishlist functionality
- Promotions and discounts

### Non-Functional Requirements
- High availability (99.99%)
- Support 100K+ concurrent users
- Handle 10K+ orders per minute
- Real-time inventory updates
- Sub-second search results
- PCI compliance for payments
- Mobile-first responsive design
- Global shipping support

## Capacity Estimation
```
User Estimates:
- 10M registered users
- 1M daily active users
- 100K concurrent users at peak

Product Estimates:
- 10M products
- 100K new products per day
- 1M product images
- Average product data: 5 KB

Order Estimates:
- 100K orders per day
- Average order: 3 items
- Daily items: 300K
- Average order value: $50
- Daily GMV: $5M

Storage Estimates:
- Product catalog: 10M × 5 KB = 50 GB
- Product images: 1M × 500 KB = 500 GB
- Order data: 100K × 2 KB = 200 MB/day
- User data: 10M × 1 KB = 10 GB
- Total: ~560 GB + 200 MB/day

Bandwidth Estimates:
- Product browsing: 1M × 50 KB = 50 GB/day = ~580 KB/s
- Order placement: 100K × 2 KB = 200 MB/day = ~2.3 KB/s
- Image loading: 10M × 500 KB = 5 TB/day = ~58 MB/s
- Total: ~59 MB/s peak
```

## API Design
```yaml
# Product Catalog
GET /api/v1/products
  Query: ?category=electronics&price_min=100&price_max=500&sort=rating&page=1
  Response:
    {
      "products": [...],
      "total": 10000,
      "has_more": true,
      "filters": {...}
    }

GET /api/v1/products/{id}
  Response:
    {
      "id": "prod_123",
      "name": "Smartphone",
      "description": "...",
      "price": 499.99,
      "category": "electronics",
      "images": [...],
      "stock": 50,
      "rating": 4.5,
      "reviews_count": 1234
    }

# Search
GET /api/v1/search
  Query: ?q=smartphone&category=electronics&sort=price_asc
  Response:
    {
      "products": [...],
      "total": 500,
      "facets": {...}
    }

# Shopping Cart
GET /api/v1/cart
  Response:
    {
      "items": [
        {"product_id": "prod_123", "quantity": 2, "price": 499.99}
      ],
      "total": 999.98
    }

POST /api/v1/cart/items
  Request:
    {
      "product_id": "prod_123",
      "quantity": 2
    }

# Checkout
POST /api/v1/checkout
  Request:
    {
      "shipping_address": {...},
      "payment_method": "card",
      "card_token": "tok_456"
    }
  Response:
    {
      "order_id": "ord_789",
      "status": "confirmed",
      "total": 1050.98,
      "estimated_delivery": "2025-01-20"
    }

# Orders
GET /api/v1/orders
  Response:
    {
      "orders": [...],
      "total": 50
    }

GET /api/v1/orders/{id}
  Response:
    {
      "id": "ord_789",
      "status": "shipped",
      "items": [...],
      "tracking": {...}
    }

# Inventory
GET /api/v1/inventory/{product_id}
  Response:
    {
      "product_id": "prod_123",
      "stock": 50,
      "available": 45,
      "reserved": 5
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
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);

-- User addresses
CREATE TABLE user_addresses (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    type VARCHAR(20) NOT NULL, -- 'billing', 'shipping'
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(2) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE
);

-- Products table
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT REFERENCES categories(id),
    price DECIMAL(10,2) NOT NULL,
    compare_at_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    low_stock_threshold INT DEFAULT 10,
    weight DECIMAL(8,2),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_price ON products(price);

-- Product images
CREATE TABLE product_images (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id),
    url TEXT NOT NULL,
    alt_text VARCHAR(255),
    sort_order INT DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE
);

-- Categories
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id BIGINT REFERENCES categories(id),
    slug VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shopping cart
CREATE TABLE carts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_items (
    id BIGSERIAL PRIMARY KEY,
    cart_id BIGINT REFERENCES carts(id),
    product_id BIGINT REFERENCES products(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id)
);

-- Orders table
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(10,2) DEFAULT 0,
    discount DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    shipping_address_id BIGINT REFERENCES user_addresses(id),
    billing_address_id BIGINT REFERENCES user_addresses(id),
    payment_method VARCHAR(20),
    payment_id BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Order items
CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id),
    product_id BIGINT REFERENCES products(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL
);

-- Payments
CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id),
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory tracking
CREATE TABLE inventory_transactions (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id),
    transaction_type VARCHAR(20) NOT NULL, -- 'sale', 'restock', 'adjustment'
    quantity INT NOT NULL,
    reference_id BIGINT, -- order_id for sales
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews
CREATE TABLE reviews (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id),
    user_id BIGINT REFERENCES users(id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    body TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, user_id)
);

-- Wishlist
CREATE TABLE wishlist_items (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    product_id BIGINT REFERENCES products(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

-- Promotions
CREATE TABLE promotions (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL, -- 'percentage', 'fixed', 'free_shipping'
    value DECIMAL(10,2) NOT NULL,
    min_order_amount DECIMAL(10,2),
    max_uses INT,
    used_count INT DEFAULT 0,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
```

### ER Diagram (ASCII)
```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users    │     │    products     │     │   categories    │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │     │ id (PK)         │     │ id (PK)         │
│ email       │     │ sku             │     │ name            │
│ password    │     │ name            │     │ parent_id (FK)  │
│ name        │     │ price           │     │ slug            │
│ phone       │     │ category_id(FK) │────►│                 │
└─────────────┘     │ stock_quantity  │     └─────────────────┘
        │           │ status          │
        │           └─────────────────┘
        │                    │
        │                    ▼
        │           ┌─────────────────┐
        │           │ product_images  │
        │           ├─────────────────┤
        │           │ id (PK)         │
        │           │ product_id (FK) │
        │           │ url             │
        │           │ alt_text        │
        │           │ sort_order      │
        │           └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│     carts       │     │     orders      │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ user_id (FK)    │     │ user_id (FK)    │
│ session_id      │     │ order_number    │
│ created_at      │     │ status          │
│ updated_at      │     │ subtotal        │
└─────────────────┘     │ tax             │
        │               │ total           │
        ▼               │ payment_id      │
┌─────────────────┐     └─────────────────┘
│   cart_items    │              │
├─────────────────┤              ▼
│ id (PK)         │     ┌─────────────────┐
│ cart_id (FK)    │     │  order_items    │
│ product_id (FK) │     ├─────────────────┤
│ quantity        │     │ id (PK)         │
│ price           │     │ order_id (FK)   │
└─────────────────┘     │ product_id (FK) │
                        │ quantity        │
                        │ price           │
                        │ total           │
                        └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    payments     │
                        ├─────────────────┤
                        │ id (PK)         │
                        │ order_id (FK)   │
                        │ amount          │
                        │ method          │
                        │ status          │
                        │ transaction_id  │
                        └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│              (Web, Mobile, Admin Panel)                          │
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
│  Product        │  │  Cart &         │  │  Order          │
│  Service        │  │  Checkout       │  │  Service        │
│  (Catalog,      │  │  Service        │  │  (Processing,   │
│   Search)       │  │                 │  │   Management)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (Products,  │  │  (Cart,     │  │  (Events)   │
     │   Orders)    │  │   Cache)    │  │             │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Elasticsearch  │
     │  (Product       │
     │   Search)       │
     └─────────────────┘
```

## Key Components

### Product Catalog Service
```python
class ProductCatalogService:
    def __init__(self, db, cache, search_engine):
        self.db = db
        self.cache = cache
        self.search = search_engine
    
    async def get_product(self, product_id: int) -> dict:
        # Check cache first
        cached = await self.cache.get_product(product_id)
        if cached:
            return cached
        
        # Fetch from database
        product = await self.db.get_product(product_id)
        
        if product:
            # Cache for future requests
            await self.cache.set_product(product_id, product)
        
        return product
    
    async def search_products(self, query: str, 
                             filters: dict = None,
                             sort: str = 'relevance',
                             page: int = 1,
                             limit: int = 20) -> dict:
        # Use Elasticsearch for full-text search
        results = await self.search.search(
            index='products',
            query=query,
            filters=filters,
            sort=sort,
            from_=(page - 1) * limit,
            size=limit
        )
        
        return {
            'products': results['hits'],
            'total': results['total'],
            'facets': results.get('facets', {})
        }
    
    async def update_stock(self, product_id: int, 
                          quantity_change: int) -> bool:
        # Atomic stock update
        result = await self.db.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity + %s,
                updated_at = NOW()
            WHERE id = %s AND stock_quantity + %s >= 0
            RETURNING stock_quantity
        """, (quantity_change, product_id, quantity_change))
        
        if result:
            # Invalidate cache
            await self.cache.invalidate_product(product_id)
            
            # Check for low stock
            if result[0]['stock_quantity'] < 10:
                await self.send_low_stock_alert(product_id)
            
            return True
        
        return False
```

### Shopping Cart Service
```python
class CartService:
    def __init__(self, db, redis_client, product_service):
        self.db = db
        self.redis = redis_client
        self.products = product_service
    
    async def get_cart(self, user_id: int = None,
                       session_id: str = None) -> dict:
        # Get cart from Redis
        cart_key = self.get_cart_key(user_id, session_id)
        cart_data = await self.redis.get(cart_key)
        
        if cart_data:
            return json.loads(cart_data)
        
        # Initialize empty cart
        return {'items': [], 'total': 0}
    
    async def add_to_cart(self, user_id: int = None,
                         session_id: str = None,
                         product_id: int = None,
                         quantity: int = 1) -> dict:
        # Validate product
        product = await self.products.get_product(product_id)
        if not product:
            raise ProductNotFoundError("Product not found")
        
        # Check stock
        if product['stock_quantity'] < quantity:
            raise InsufficientStockError("Insufficient stock")
        
        # Get current cart
        cart = await self.get_cart(user_id, session_id)
        
        # Check if product already in cart
        existing_item = next(
            (item for item in cart['items'] 
             if item['product_id'] == product_id),
            None
        )
        
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            cart['items'].append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })
        
        # Calculate total
        cart['total'] = sum(
            item['price'] * item['quantity'] 
            for item in cart['items']
        )
        
        # Save to Redis
        cart_key = self.get_cart_key(user_id, session_id)
        await self.redis.setex(
            cart_key, 86400, json.dumps(cart)  # 24 hours TTL
        )
        
        return cart
    
    async def remove_from_cart(self, user_id: int = None,
                              session_id: str = None,
                              product_id: int = None) -> dict:
        cart = await self.get_cart(user_id, session_id)
        
        cart['items'] = [
            item for item in cart['items'] 
            if item['product_id'] != product_id
        ]
        
        # Recalculate total
        cart['total'] = sum(
            item['price'] * item['quantity'] 
            for item in cart['items']
        )
        
        # Save to Redis
        cart_key = self.get_cart_key(user_id, session_id)
        await self.redis.setex(
            cart_key, 86400, json.dumps(cart)
        )
        
        return cart
    
    def get_cart_key(self, user_id: int = None,
                    session_id: str = None) -> str:
        if user_id:
            return f"cart:user:{user_id}"
        return f"cart:session:{session_id}"
```

### Checkout Service
```python
class CheckoutService:
    def __init__(self, db, cart_service, inventory_service,
                 payment_service, order_service, notification_service):
        self.db = db
        self.cart = cart_service
        self.inventory = inventory_service
        self.payments = payment_service
        self.orders = order_service
        self.notifications = notification_service
    
    async def checkout(self, user_id: int, 
                      shipping_address: dict,
                      payment_method: dict,
                      promotion_code: str = None) -> dict:
        # Get cart
        cart = await self.cart.get_cart(user_id=user_id)
        
        if not cart['items']:
            raise EmptyCartError("Cart is empty")
        
        # Validate inventory
        for item in cart['items']:
            available = await self.inventory.check_availability(
                item['product_id'], item['quantity']
            )
            if not available:
                raise InsufficientStockError(
                    f"Insufficient stock for {item['name']}"
                )
        
        # Apply promotion if provided
        discount = 0
        if promotion_code:
            discount = await self.apply_promotion(
                promotion_code, cart['total']
            )
        
        # Calculate totals
        subtotal = cart['total']
        tax = self.calculate_tax(subtotal, shipping_address['country'])
        shipping_cost = self.calculate_shipping(shipping_address)
        total = subtotal + tax + shipping_cost - discount
        
        # Reserve inventory
        for item in cart['items']:
            await self.inventory.reserve(
                item['product_id'], item['quantity']
            )
        
        # Process payment
        payment = await self.payments.process_payment(
            amount=total,
            method=payment_method,
            reference=f"checkout_{user_id}"
        )
        
        if payment['status'] != 'success':
            # Release reserved inventory
            for item in cart['items']:
                await self.inventory.release(
                    item['product_id'], item['quantity']
                )
            raise PaymentFailedError("Payment failed")
        
        # Create order
        order = await self.orders.create_order(
            user_id=user_id,
            items=cart['items'],
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            discount=discount,
            total=total,
            shipping_address=shipping_address,
            payment_id=payment['id']
        )
        
        # Update inventory (confirm reservation)
        for item in cart['items']:
            await self.inventory.confirm_reservation(
                item['product_id'], item['quantity']
            )
        
        # Clear cart
        await self.cart.clear_cart(user_id=user_id)
        
        # Send confirmation
        await self.notifications.send_order_confirmation(
            user_id, order
        )
        
        return order
    
    def calculate_tax(self, subtotal: float, country: str) -> float:
        tax_rates = {
            'US': 0.08,
            'UK': 0.20,
            'IN': 0.18,
            'DE': 0.19
        }
        rate = tax_rates.get(country, 0.10)
        return round(subtotal * rate, 2)
    
    def calculate_shipping(self, address: dict) -> float:
        # Simple shipping calculation
        if address['country'] == 'US':
            return 5.99
        return 15.99
```

### Inventory Management Service
```python
class InventoryService:
    def __init__(self, db, redis_client, notification_service):
        self.db = db
        self.redis = redis_client
        self.notifications = notification_service
    
    async def check_availability(self, product_id: int,
                                quantity: int) -> bool:
        # Check Redis cache first
        stock = await self.redis.get(f"stock:{product_id}")
        
        if stock is not None:
            return int(stock) >= quantity
        
        # Check database
        result = await self.db.execute("""
            SELECT stock_quantity FROM products
            WHERE id = %s
        """, (product_id,))
        
        if result:
            available = result[0]['stock_quantity']
            # Cache for 5 minutes
            await self.redis.setex(
                f"stock:{product_id}", 300, available
            )
            return available >= quantity
        
        return False
    
    async def reserve(self, product_id: int, quantity: int) -> bool:
        # Atomic reservation
        result = await self.db.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity - %s
            WHERE id = %s AND stock_quantity >= %s
            RETURNING stock_quantity
        """, (quantity, product_id, quantity))
        
        if result:
            # Update cache
            await self.redis.set(
                f"stock:{product_id}", 
                result[0]['stock_quantity']
            )
            
            # Log transaction
            await self.db.execute("""
                INSERT INTO inventory_transactions 
                (product_id, transaction_type, quantity)
                VALUES (%s, 'reservation', %s)
            """, (product_id, quantity))
            
            return True
        
        return False
    
    async def release(self, product_id: int, quantity: int):
        await self.db.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity + %s
            WHERE id = %s
        """, (quantity, product_id))
        
        # Update cache
        stock = await self.db.get_stock(product_id)
        await self.redis.set(f"stock:{product_id}", stock)
    
    async def confirm_reservation(self, product_id: int, 
                                 quantity: int):
        # Log sale
        await self.db.execute("""
            INSERT INTO inventory_transactions 
            (product_id, transaction_type, quantity)
            VALUES (%s, 'sale', %s)
        """, (product_id, quantity))
        
        # Check for low stock
        stock = await self.db.get_stock(product_id)
        if stock < 10:
            await self.send_low_stock_alert(product_id, stock)
```

## Caching Strategy (Redis)

### Product Cache
```python
class ProductCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 300  # 5 minutes
    
    async def get_product(self, product_id: int) -> dict:
        key = f"product:{product_id}"
        cached = await self.redis.get(key)
        
        if cached:
            return json.loads(cached)
        
        return None
    
    async def set_product(self, product_id: int, product: dict):
        key = f"product:{product_id}"
        await self.redis.setex(key, self.ttl, json.dumps(product))
    
    async def invalidate_product(self, product_id: int):
        await self.redis.delete(f"product:{product_id}")
    
    async def cache_popular_products(self, category_id: int,
                                    products: list):
        key = f"popular:{category_id}"
        await self.redis.delete(key)
        
        for i, product in enumerate(products):
            await self.redis.zadd(key, {json.dumps(product): -i})
        
        await self.redis.expire(key, 3600)  # 1 hour
```

### Cart Cache
```python
class CartCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 86400  # 24 hours
    
    async def get_cart(self, user_id: int) -> dict:
        key = f"cart:{user_id}"
        cached = await self.redis.get(key)
        
        if cached:
            return json.loads(cached)
        
        return None
    
    async def set_cart(self, user_id: int, cart: dict):
        key = f"cart:{user_id}"
        await self.redis.setex(key, self.ttl, json.dumps(cart))
```

## Message Queue (Kafka)

### Topics and Events
```
Topics:
├── order.created          (new order)
├── order.confirmed        (payment successful)
├── order.shipped          (order shipped)
├── order.delivered        (order delivered)
├── inventory.updated      (stock changes)
├── product.created        (new product)
├── product.updated        (product changes)
└── review.created         (new review)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "order.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "order_id": "ord_456",
    "user_id": "usr_789",
    "items": [...],
    "total": 1050.98
  }
}
```

### Event Processing
```python
class OrderEventProcessor:
    def __init__(self, kafka_consumer, notification_service,
                 inventory_service):
        self.consumer = kafka_consumer
        self.notifications = notification_service
        self.inventory = inventory_service
    
    async def process_events(self):
        async for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'order.created':
                await self.handle_order_created(event)
            elif event['event_type'] == 'order.shipped':
                await self.handle_order_shipped(event)
    
    async def handle_order_created(self, event: dict):
        # Send confirmation email
        await self.notifications.send_order_confirmation(
            event['data']['user_id'],
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
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Product     │   │  Cart &      │   │  Order       │
│  Service     │   │  Checkout    │   │  Service     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Database Sharding
```python
class EcommerceDatabaseScaler:
    def __init__(self):
        self.shards = 16
    
    def get_product_shard(self, product_id: int) -> int:
        return product_id % self.shards
    
    def get_user_shard(self, user_id: int) -> int:
        return (user_id * 7) % self.shards
    
    def get_order_shard(self, order_id: int) -> int:
        return order_id % self.shards
```

### Search Scaling
```python
class SearchServiceScaler:
    def __init__(self):
        self.elasticsearch_cluster = [
            'es1:9200', 'es2:9200', 'es3:9200'
        ]
    
    async def search(self, query: str, index: str):
        # Use Elasticsearch with replicas
        client = self.get_client()
        
        results = await client.search(
            index=index,
            body={
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': ['name^3', 'description', 'category']
                    }
                }
            }
        )
        
        return results
```

## Failure Handling

### Inventory Overselling Prevention
```python
class InventoryProtection:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
    
    async def safe_reserve(self, product_id: int, 
                          quantity: int) -> bool:
        # Use distributed lock
        lock_key = f"inventory_lock:{product_id}"
        
        # Try to acquire lock
        lock_acquired = await self.redis.set(
            lock_key, "1", nx=True, ex=10
        )
        
        if not lock_acquired:
            # Wait and retry
            await asyncio.sleep(0.1)
            return await self.safe_reserve(product_id, quantity)
        
        try:
            # Check and reserve atomically
            result = await self.db.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s AND stock_quantity >= %s
                RETURNING stock_quantity
            """, (quantity, product_id, quantity))
            
            return result is not None
            
        finally:
            await self.redis.delete(lock_key)
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| Database failover | Read from replica |
| Redis down | Fall back to database |
| Payment fails | Release inventory |
| Inventory service down | Queue operations |
| Network partition | Store locally, sync later |

### Order Processing Recovery
```python
class OrderRecovery:
    def __init__(self, db, kafka_client):
        self.db = db
        self.kafka = kafka_client
    
    async def recover_stuck_orders(self):
        # Find orders stuck in 'pending' state
        stuck_orders = await self.db.execute("""
            SELECT * FROM orders 
            WHERE status = 'pending' 
            AND created_at < NOW() - INTERVAL '5 minutes'
        """)
        
        for order in stuck_orders:
            await self.process_stuck_order(order)
    
    async def process_stuck_order(self, order: dict):
        # Check payment status
        payment = await self.db.get_payment(order['payment_id'])
        
        if payment['status'] == 'failed':
            # Cancel order
            await self.cancel_order(order['id'])
        elif payment['status'] == 'success':
            # Complete order
            await self.complete_order(order['id'])
```

## Monitoring

### Key Metrics
```yaml
Business Metrics:
  - orders_per_minute
  - average_order_value
  - cart_abandonment_rate
  - conversion_rate

System Metrics:
  - product_search_latency_p95
  - checkout_latency_p95
  - inventory_update_latency
  - api_response_time

Infrastructure Metrics:
  - server_cpu_usage
  - memory_usage
  - database_query_latency
  - redis_memory_usage
```

### Alerting Rules
```yaml
alerts:
  - name: High Cart Abandonment
    condition: cart_abandonment_rate > 70%
    severity: warning
    
  - name: Inventory Overselling
    condition: negative_stock_count > 0
    severity: critical
    
  - name: Checkout Failures High
    condition: checkout_failure_rate > 5%
    severity: critical
    
  - name: Search Latency High
    condition: p95_search_latency > 500ms
    severity: warning
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Search | Database LIKE | Elasticsearch | Elasticsearch |
| Cart Storage | Database | Redis | Redis (fast) |
| Inventory | Optimistic | Pessimistic | Pessimistic |
| Order Processing | Sync | Async | Async (Kafka) |
| Product Cache | Write-through | Cache-aside | Cache-aside |

## Interview Questions

### Design Questions
1. **How would you design an e-commerce product catalog?**
   - PostgreSQL for structured data
   - Elasticsearch for search
   - Redis for caching
   - CDN for images

2. **How do you handle shopping cart management?**
   - Redis for fast access
   - Merge carts on login
   - Session-based for guests
   - 24-hour expiration

3. **How would you implement checkout?**
   - Validate inventory
   - Reserve stock
   - Process payment
   - Create order
   - Send confirmation

### Scaling Questions
4. **How do you scale to 100K concurrent users?**
   - Horizontal scaling
   - Database sharding
   - Redis clustering
   - CDN for static content

5. **How do you handle flash sales?**
   - Pre-warm cache
   - Use atomic operations
   - Queue overflow
   - Monitor and auto-scale

### Trade-off Questions
6. **How do you balance consistency vs performance?**
   - Strong consistency for inventory
   - Eventual consistency for product data
   - Cache invalidation strategy
   - Transaction boundaries

7. **How do you prevent inventory overselling?**
   - Distributed locks
   - Atomic operations
   - Reservation system
   - Real-time monitoring

### Senior-level Questions
8. **How would you implement personalization?**
   - User behavior tracking
   - Recommendation engine
   - A/B testing
   - Real-time pricing

9. **How do you handle global shipping?**
   - Multi-region deployment
   - Local payment methods
   - Currency conversion
   - Customs calculation

10. **How would you implement multi-vendor support?**
    - Vendor management
    - Commission calculation
    - Split payments
    - Vendor analytics

## Summary

The E-Commerce system design covers:
- **Product Catalog**: PostgreSQL + Elasticsearch
- **Shopping Cart**: Redis-based with session support
- **Checkout**: Atomic inventory reservation
- **Order Management**: Async processing with Kafka
- **Search**: Full-text with faceted filtering

Key takeaways:
1. Use Redis for fast cart and cache operations
2. Implement atomic inventory updates to prevent overselling
3. Use Elasticsearch for product search
4. Process orders asynchronously with Kafka
5. Design for flash sales with pre-warmed caches

This design supports 100K+ concurrent users with 10K+ orders per minute.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
