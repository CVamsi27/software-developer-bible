# Web Crawler System Design

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

## Requirements
### Functional Requirements

- Crawl web pages starting from a seed set of URLs
- Extract and follow links to discover new pages
- Store crawled pages for indexing and analysis
- Respect robots.txt and crawl-delay directives
- Deduplicate content (avoid crawling same URL twice)
- Handle different content types (HTML, PDF, images)
- Schedule recrawling for content freshness
- Prioritize high-quality and frequently updated pages
- Support politeness policy (not overwhelm servers)
- Provide crawl statistics and monitoring

### Non-Functional Requirements

- Crawl 10B+ pages per month
- Scalable to thousands of crawling nodes
- Fault-tolerant (hardware failures are common)
- Distributed across multiple data centers
- Respectful crawling (no DoS)
- Storage for 100PB+ of raw HTML and metadata
- Bandwidth: 10+ Gbps per crawling node

## Capacity Estimation

```text
Crawl Estimates:

- 10B pages crawled per month = ~4,000 pages/second
- Average page size: 500 KB (HTML + resources)
- Daily download: 4,000 × 500 KB × 86400 = ~173 TB/day
- Monthly storage: 173 TB × 30 = ~5.2 PB/month
- After compression (5:1 ratio): ~1 PB/month

Link Discovery Estimates:

- Average links per page: 50
- Total links discovered: 4,000 × 50 = 200K/sec
- Total unique URLs: ~100B (over time)

Bandwidth Estimates:

- Per node: 10 Gbps = ~1.25 GB/s
- Total nodes needed: 173 TB/day = ~2 GB/s = ~2 nodes (bandwidth-limited)
- With redundancy: 10-20 nodes minimum

Storage Estimates:

- Raw HTML: 5.2 PB/month × 12 = 62.4 PB/year
- Metadata + index: ~10% of raw = 6.2 PB/year
- After compression + dedup: ~15 PB/year

```

## API Design

```yaml
# Submit URLs to crawl (internal service)
POST /api/v1/crawler/submit
  Request:
    {
      "urls": [
        {"url": "https://example.com/page1", "priority": 10},
        {"url": "https://example.com/page2", "priority": 5}
      ],
      "callback_url": "https://callback.service/notify",
      "max_depth": 3,
      "respect_robots": true
    }
  Response:
    {
      "job_id": "crawl_job_123",
      "urls_accepted": 2,
      "estimated_completion": "2025-01-15T11:00:00Z"
    }

# Get crawl status
GET /api/v1/crawler/status/{job_id}
  Response:
    {
      "job_id": "crawl_job_123",
      "status": "in_progress",
      "urls_crawled": 50,
      "urls_queued": 150,
      "urls_failed": 2,
      "progress_percentage": 25,
      "estimated_remaining_seconds": 3600
    }

# Get page metadata
GET /api/v1/crawler/page?url=https://example.com/page1
  Response:
    {
      "url": "https://example.com/page1",
      "canonical_url": "https://example.com/page1",
      "title": "Example Page",
      "content_type": "text/html",
      "content_length": 24500,
      "crawl_timestamp": "2025-01-15T10:30:00Z",
      "http_status": 200,
      "outgoing_links": 45,
      "checksum": "sha256:abc123...",
      "last_modified": "2025-01-14T10:00:00Z"
    }

# Crawler management (admin)
POST /api/v1/crawler/pause
POST /api/v1/crawler/resume
PUT /api/v1/crawler/config
  Request:
    {
      "max_concurrent_requests": 1000,
      "request_timeout_ms": 10000,
      "max_redirects": 5,
      "user_agent": "MyCrawler/1.0"
    }

GET /api/v1/crawler/stats
  Response:
    {
      "pages_crawled_total": 5000000000,
      "pages_per_second": 4000,
      "active_workers": 500,
      "queue_size": 5000000,
      "error_rate": 0.02,
      "bandwidth_usage_gbps": 8.5
    }
```

## Database Design
### Schema

```sql
-- URLs discovered (the frontier)
CREATE TABLE url_frontier (
    id BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    domain VARCHAR(255) NOT NULL,
    priority INT DEFAULT 10,       -- 1-10, higher = more important
    depth INT DEFAULT 0,
    crawl_status VARCHAR(20) DEFAULT 'pending',
    -- 'pending', 'queued', 'crawling', 'completed', 'failed'
    discover_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_crawled TIMESTAMP,
    next_crawl TIMESTAMP,
    crawl_frequency INT DEFAULT 86400,  -- seconds (24h default)
    http_status INT,
    checksum VARCHAR(64),           -- SHA-256 of content
    is_seed BOOLEAN DEFAULT FALSE,
    retry_count INT DEFAULT 0
);

CREATE INDEX idx_frontier_status ON url_frontier(crawl_status, next_crawl);
CREATE INDEX idx_frontier_domain ON url_frontier(domain);
CREATE INDEX idx_frontier_priority ON url_frontier(priority DESC);

-- Crawled pages
CREATE TABLE crawled_pages (
    id BIGSERIAL PRIMARY KEY,
    url_id BIGINT REFERENCES url_frontier(id),
    url TEXT NOT NULL,
    canonical_url TEXT,
    title TEXT,
    content TEXT,                    -- Compressed HTML body
    content_type VARCHAR(100),
    content_length BIGINT,
    http_status INT,
    response_headers JSONB,
    outgoing_links JSONB,           -- Array of extracted links
    anchor_text TEXT[],             -- Anchor text for each link
    metadata JSONB,                 -- Meta tags, Open Graph, etc.
    crawl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    download_time_ms INT,
    checksum VARCHAR(64)
) PARTITION BY RANGE (crawl_timestamp);

CREATE INDEX idx_crawled_url ON crawled_pages(url);
CREATE INDEX idx_crawled_checksum ON crawled_pages(checksum);

-- Domain crawl rules
CREATE TABLE domain_rules (
    id BIGSERIAL PRIMARY KEY,
    domain VARCHAR(255) PRIMARY KEY,
    robots_txt TEXT,
    crawl_delay INT DEFAULT 1,      -- seconds between requests
    allowed_paths TEXT[],           -- patterns from robots.txt
    disallowed_paths TEXT[],         -- patterns from robots.txt
    sitemap_urls TEXT[],
    max_crawl_depth INT DEFAULT 10,
    respect_robots BOOLEAN DEFAULT TRUE,
    last_robots_check TIMESTAMP,
    last_sitemap_fetch TIMESTAMP
);

-- Crawl errors
CREATE TABLE crawl_errors (
    id BIGSERIAL PRIMARY KEY,
    url_id BIGINT REFERENCES url_frontier(id),
    url TEXT NOT NULL,
    error_type VARCHAR(50) NOT NULL,
    -- 'timeout', 'dns_failure', 'connection_refused', 'http_error', 'parse_error'
    error_message TEXT,
    http_status INT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_crawl_errors_type ON crawl_errors(error_type);
```

### ER Diagram (ASCII)

```text
┌──────────────────┐     ┌──────────────────────┐
│   url_frontier   │     │    crawled_pages      │
├──────────────────┤     ├──────────────────────┤
│ id (PK)          │◄────│ url_id (FK)           │
│ url (UK)         │     │ id (PK)               │
│ domain           │     │ url                   │
│ priority         │     │ canonical_url         │
│ depth            │     │ title                 │
│ crawl_status     │     │ content (compressed)  │
│ discover_time    │     │ content_type          │
│ last_crawled     │     │ content_length        │
│ next_crawl       │     │ http_status           │
│ crawl_frequency  │     │ outgoing_links        │
│ checksum         │     │ anchor_text           │
│ retry_count      │     │ metadata              │
└──────────────────┘     │ crawl_timestamp       │
        │                │ checksum              │
        │                └──────────────────────┘
        │                           ▲
        │                           │
        │                ┌──────────┴──────────┐
        │                │                     │
        ▼                ▼                     │
┌──────────────────┐  ┌──────────────────┐    │
│   domain_rules   │  │  crawl_errors    │    │
├──────────────────┤  ├──────────────────┤    │
│ domain (PK)      │  │ id (PK)          │    │
│ robots_txt       │  │ url_id (FK)──────┘    │
│ crawl_delay      │  │ url                   │
│ allowed_paths    │  │ error_type            │
│ disallowed_paths │  │ error_message         │
│ sitemap_urls     │  │ http_status           │
│ max_crawl_depth  │  │ retry_count           │
│ respect_robots   │  │ created_at            │
└──────────────────┘  └──────────────────────┘
```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                     Seed URLs (Initial input)                     │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   URL Frontier        │
                    │   (Priority Queue)    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   URL Dispatcher      │
                    │   (Domain-aware)      │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Downloader     │  │  Downloader     │  │  Downloader     │
│  Worker 1       │  │  Worker 2       │  │  Worker N       │
│  (Async HTTP)   │  │  (Async HTTP)   │  │  (Async HTTP)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Parser /        │
                    │   Link Extractor  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ Content     │  │ URL         │  │ URL Filter  │
     │ Dedup       │  │ Filter (robots,│ (already     │
     │ (Checksum)  │  │  allowed)   │  │  crawled)   │
     └─────────────┘  └─────────────┘  └─────────────┘
              │              │              │
              │              ▼              │
              │      ┌─────────────┐        │
              │      │  New URLs   │────────┘
              │      │  (Back to   │
              │      │  Frontier)  │
              │      └─────────────┘
              ▼
     ┌─────────────────┐
     │  Storage Service │
     │  (Object Store)  │
     └─────────────────┘
```

## Key Components

### URL Frontier (Priority Queue)

```python
import asyncio
from heapq import heappush, heappop
from urllib.parse import urlparse
import time

class URLFrontier:
    """Distributed priority queue for URLs to crawl."""

    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
        self.queue_key = "crawler:frontier"
        self.domain_queue_key = "crawler:frontier:domains"

    async def add_urls(self, urls: list, source_depth: int = 0):
        """Add URLs to the frontier with deduplication."""
        pipeline = self.redis.pipeline()

        for url_info in urls:
            url = url_info['url']
            priority = url_info.get('priority', 10)
            depth = url_info.get('depth', source_depth + 1)

            # Check if URL already known
            if not await self.is_url_known(url):
                # Add to Redis sorted set (priority score)
                pipeline.zadd(self.queue_key, {
                    self.serialize_url(url, priority, depth): priority
                })

                # Track by domain for politeness control
                domain = urlparse(url).netloc
                pipeline.sadd(f"domain:{domain}:urls", url)

        await pipeline.execute()

    async def get_next_batch(self, batch_size: int = 100) -> list:
        """Get next batch of URLs to crawl, respecting domain politeness."""
        urls = []
        domains_being_crawled = set()

        # Get highest priority URLs
        candidates = self.redis.zrevrange(
            self.queue_key, 0, batch_size * 5
        )

        for candidate in candidates:
            if len(urls) >= batch_size:
                break

            url, priority, depth = self.deserialize_url(candidate)
            domain = urlparse(url).netloc

            # Politeness check: not crawling this domain too aggressively
            if domain in domains_being_crawled:
                continue

            # Check crawl delay for this domain
            if await self.is_domain_cooldown(domain):
                continue

            urls.append({
                'url': url,
                'priority': priority,
                'depth': depth
            })
            domains_being_crawled.add(domain)

            # Remove from frontier
            self.redis.zrem(self.queue_key, candidate)

        return urls

    async def is_url_known(self, url: str) -> bool:
        """Check if URL has been seen before (bloom filter)."""
        # Use Bloom filter for O(1) check with small false positive rate
        return self.redis.sismember('crawler:seen_urls', self.hash_url(url))

    async def mark_url_crawled(self, url: str, success: bool):
        """Mark URL as crawled and schedule recrawl if needed."""
        if success:
            # Add to bloom filter
            self.redis.sadd('crawler:seen_urls', self.hash_url(url))

            # Schedule recrawl (default: 24 hours)
            self.redis.zadd('crawler:recrawl_queue', {
                url: time.time() + 86400
            })
        else:
            # Re-queue with lower priority
            self.redis.zadd(self.queue_key, {
                self.serialize_url(url, 1, 0): 1
            })

    def is_domain_cooldown(self, domain: str) -> bool:
        """Check if we need to wait before crawling this domain."""
        key = f"domain:{domain}:last_crawl"
        last_crawl = self.redis.get(key)
        if not last_crawl:
            return False

        delay = self.redis.get(f"domain:{domain}:delay") or 1
        return (time.time() - float(last_crawl)) < int(delay)

    def serialize_url(self, url: str, priority: int, depth: int) -> str:
        return f"{url}|{priority}|{depth}"

    def deserialize_url(self, data: str) -> tuple:
        parts = data.split('|', 2)
        return parts[0], int(parts[1]), int(parts[2])

    def hash_url(self, url: str) -> str:
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()
```

### Downloader Service

```python
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import hashlib

class PageDownloader:
    """Asynchronous HTTP downloader with politeness controls."""

    def __init__(self, frontier, storage_service):
        self.frontier = frontier
        self.storage = storage_service
        self.robots_cache = {}
        self.download_semaphore = asyncio.Semaphore(1000)  # Max concurrent
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def download_page(self, url_info: dict) -> dict:
        """Download a single page with retries and politeness."""
        url = url_info['url']
        domain = urlparse(url).netloc

        async with self.download_semaphore:
            # Check robots.txt
            if not await self.is_allowed_by_robots(domain, url):
                return {'url': url, 'status': 'blocked_by_robots'}

            # Respect crawl delay
            await self.enforce_crawl_delay(domain)

            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    headers = {
                        'User-Agent': 'MyCrawler/1.0 (Educational)',
                        'Accept': 'text/html,application/xhtml+xml',
                        'Accept-Language': 'en-US,en;q=0.5'
                    }

                    async with session.get(url, headers=headers,
                                           allow_redirects=True) as response:
                        content = await response.read()
                        content_type = response.headers.get(
                            'Content-Type', ''
                        )

                        result = {
                            'url': url,
                            'final_url': str(response.url),
                            'status': 'success',
                            'http_status': response.status,
                            'content': content,
                            'content_type': content_type,
                            'content_length': len(content),
                            'response_headers': dict(response.headers),
                            'download_time_ms': 0,
                            'checksum': hashlib.sha256(content).hexdigest()
                        }

                        return result

            except asyncio.TimeoutError:
                return {'url': url, 'status': 'timeout'}
            except aiohttp.ClientError as e:
                return {'url': url, 'status': 'error',
                        'error_message': str(e)}

    async def is_allowed_by_robots(self, domain: str, url: str) -> bool:
        """Check robots.txt rules."""
        if domain not in self.robots_cache:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            try:
                rp.read()
            except Exception:
                # If we can't read robots.txt, be permissive
                return True
            self.robots_cache[domain] = rp

        return self.robots_cache[domain].can_fetch('MyCrawler/1.0', url)

    async def enforce_crawl_delay(self, domain: str):
        """Ensure we respect crawl-delay between requests to same domain."""
        last_crawl = self.frontier.redis.get(f"domain:{domain}:last_crawl")
        delay = int(
            self.frontier.redis.get(f"domain:{domain}:delay") or 1
        )

        if last_crawl:
            elapsed = time.time() - float(last_crawl)
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)

        # Update last crawl time
        self.frontier.redis.set(
            f"domain:{domain}:last_crawl", time.time()
        )
```

### Parser and Link Extractor

```python
from urllib.parse import urljoin, urlparse
import re

class LinkExtractor:
    """Extract and normalize links from HTML content."""

    def __init__(self, url_filter):
        self.url_filter = url_filter

    def extract_links(self, html_content: str, base_url: str) -> dict:
        """Extract all links from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []

        # Extract from <a> tags
        for anchor in soup.find_all('a', href=True):
            href = anchor['href'].strip()
            text = anchor.get_text(strip=True)

            # Normalize URL
            absolute_url = urljoin(base_url, href)
            normalized = self.normalize_url(absolute_url)

            if normalized and self.url_filter.is_valid(normalized):
                links.append({
                    'url': normalized,
                    'anchor_text': text[:100] if text else '',
                    'tag': 'a',
                    'rel': anchor.get('rel', []),
                    'nofollow': 'nofollow' in anchor.get('rel', [])
                })

        # Extract from <img>, <script>, <link> tags
        for tag in ['img', 'script', 'link']:
            for element in soup.find_all(tag, src=True):
                src = element['src'].strip()
                absolute_url = urljoin(base_url, src)
                normalized = self.normalize_url(absolute_url)
                if normalized:
                    links.append({
                        'url': normalized,
                        'tag': tag,
                        'anchor_text': ''
                    })

        return {
            'links': links,
            'internal_links': [l for l in links
                               if self.is_same_domain(l['url'], base_url)],
            'external_links': [l for l in links
                               if not self.is_same_domain(l['url'], base_url)],
            'link_count': len(links)
        }

    def extract_metadata(self, html_content: str) -> dict:
        """Extract page metadata."""
        soup = BeautifulSoup(html_content, 'html.parser')

        metadata = {
            'title': self.get_title(soup),
            'description': self.get_meta_content(soup, 'description'),
            'keywords': self.get_meta_content(soup, 'keywords'),
            'og_title': self.get_meta_property(soup, 'og:title'),
            'og_description': self.get_meta_property(soup, 'og:description'),
            'og_image': self.get_meta_property(soup, 'og:image'),
            'canonical': self.get_canonical(soup),
            'lang': soup.html.get('lang', '') if soup.html else '',
            'h1_tags': [h.get_text(strip=True) for h in soup.find_all('h1')],
            'word_count': len(soup.get_text().split()),
        }

        return metadata

    def normalize_url(self, url: str) -> str:
        """Normalize URL: lowercase, remove fragments, trailing slashes."""
        if not url or url.startswith('data:') or url.startswith('javascript:'):
            return None

        parsed = urlparse(url)

        # Remove fragments
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # Remove default ports
        normalized = re.sub(r':(80|443)(?=/|$)', '', normalized)

        # Remove trailing slash for non-root paths
        if len(normalized) > 1 and normalized.endswith('/'):
            normalized = normalized.rstrip('/')

        # Lowercase domain and path
        parts = urlparse(normalized)
        normalized = f"{parts.scheme}://{parts.netloc.lower()}{parts.path}"

        # Keep query parameters if they exist
        if parsed.query:
            normalized += f"?{parsed.query}"

        return normalized if len(normalized) < 2048 else None

    def is_same_domain(self, url1: str, url2: str) -> bool:
        return urlparse(url1).netloc == urlparse(url2).netloc

    def get_title(self, soup) -> str:
        return soup.title.string.strip()[:200] if soup.title and soup.title.string else ''

    def get_meta_content(self, soup, name: str) -> str:
        tag = soup.find('meta', attrs={'name': name})
        return tag['content'][:300] if tag and tag.get('content') else ''

    def get_meta_property(self, soup, prop: str) -> str:
        tag = soup.find('meta', attrs={'property': prop})
        return tag['content'][:300] if tag and tag.get('content') else ''

    def get_canonical(self, soup) -> str:
        tag = soup.find('link', rel='canonical')
        return tag['href'][:500] if tag and tag.get('href') else ''


class URLFilter:
    """Filter URLs based on crawl policies."""

    def __init__(self):
        self.excluded_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.mp3', '.mp4', '.avi', '.mov',
            '.zip', '.tar', '.gz', '.rar',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.css', '.js', '.json', '.xml'
        }

        self.excluded_patterns = [
            r'^mailto:', r'^tel:', r'^javascript:',
            r'/logout', r'/login\?', r'action=edit',
            r'#.*',  # Fragments
        ]

    def is_valid(self, url: str) -> bool:
        """Check if URL should be crawled."""
        if not url:
            return False

        # Check scheme
        if not url.startswith(('http://', 'https://')):
            return False

        # Check file extension
        path = urlparse(url).path.lower()
        if any(path.endswith(ext) for ext in self.excluded_extensions):
            return False

        # Check excluded patterns
        for pattern in self.excluded_patterns:
            if re.search(pattern, url):
                return False

        return True
```

### Content Deduplication

```python
class ContentDedupService:
    """Detect and skip duplicate content (near-exact match via simhash)."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.simhash_bits = 64

    def is_duplicate(self, checksum: str, url: str, content: str) -> bool:
        """Check if content is a duplicate of already-crawled page."""
        # Exact dedup via checksum
        if self.redis.sismember('crawler:content_checksums', checksum):
            return True

        # Near-exact dedup via simhash
        simhash = self.compute_simhash(content)
        similar = self.find_similar(simhash)

        if similar:
            return True

        # Not duplicate - store checksum and simhash
        self.redis.sadd('crawler:content_checksums', checksum)
        self.redis.set(f"crawler:simhash:{url}", simhash)
        return False

    def compute_simhash(self, content: str) -> int:
        """Compute simhash for near-duplicate detection."""
        import hashlib

        words = re.findall(r'\w+', content.lower())
        v = [0] * self.simhash_bits

        for word in set(words):
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
            for i in range(self.simhash_bits):
                if hash_val & (1 << i):
                    v[i] += 1
                else:
                    v[i] -= 1

        fingerprint = 0
        for i in range(self.simhash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)

        return fingerprint

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """Compute Hamming distance between two simhashes."""
        xor = hash1 ^ hash2
        distance = 0
        while xor:
            distance += xor & 1
            xor >>= 1
        return distance
```

### Crawler Orchestrator

```python
class CrawlerOrchestrator:
    """Orchestrates the entire crawl process."""

    def __init__(self, frontier, downloader, extractor,
                 dedup_service, storage, kafka_producer):
        self.frontier = frontier
        self.downloader = downloader
        self.extractor = extractor
        self.dedup = dedup_service
        self.storage = storage
        self.kafka = kafka_producer
        self.worker_count = 100
        self.is_running = False

    async def start_crawl(self):
        """Start the crawl loop."""
        self.is_running = True
        workers = [
            asyncio.create_task(self.crawl_worker(i))
            for i in range(self.worker_count)
        ]

        # Monitor progress
        asyncio.create_task(self.progress_monitor())

        await asyncio.gather(*workers)

    async def crawl_worker(self, worker_id: int):
        """Individual worker that processes URLs."""
        while self.is_running:
            # Get batch of URLs from frontier
            batch = await self.frontier.get_next_batch(batch_size=10)

            if not batch:
                await asyncio.sleep(1)
                continue

            for url_info in batch:
                try:
                    # Step 1: Download page
                    download_result = await self.downloader.download_page(url_info)

                    if download_result['status'] != 'success':
                        await self.handle_failure(url_info, download_result)
                        continue

                    # Step 2: Check for duplicate content
                    if self.dedup.is_duplicate(
                            download_result['checksum'],
                            url_info['url'],
                            download_result['content']):
                        # Skip duplicate, just record it
                        await self.frontier.mark_url_crawled(
                            url_info['url'], True
                        )
                        continue

                    # Step 3: Parse and extract links
                    html_content = download_result['content'].decode(
                        'utf-8', errors='ignore'
                    )
                    links = self.extractor.extract_links(
                        html_content, url_info['url']
                    )
                    metadata = self.extractor.extract_metadata(html_content)

                    # Step 4: Store page
                    page_data = {
                        'url': url_info['url'],
                        'content': download_result['content'],
                        'metadata': metadata,
                        'links': links,
                        'crawl_info': {
                            'worker_id': worker_id,
                            'timestamp': time.time(),
                            'http_status': download_result['http_status'],
                            'download_time_ms': 0
                        }
                    }
                    await self.storage.store_page(page_data)

                    # Step 5: Add new URLs to frontier
                    new_urls = [
                        {'url': l['url'], 'depth': url_info['depth'],
                         'priority': self.calculate_priority(l)}
                        for l in links['links']
                        if not l.get('nofollow', False)
                    ]
                    await self.frontier.add_urls(new_urls, url_info['depth'])

                    # Step 6: Mark original URL as crawled
                    await self.frontier.mark_url_crawled(
                        url_info['url'], True
                    )

                    # Step 7: Publish crawl event
                    await self.kafka.send('page.crawled', {
                        'url': url_info['url'],
                        'content_length': len(download_result['content']),
                        'links_found': links['link_count'],
                        'http_status': download_result['http_status']
                    })

                except Exception as e:
                    await self.handle_error(url_info, str(e))

    def calculate_priority(self, link: dict) -> int:
        """Calculate crawl priority for a discovered link."""
        priority = 5  # Default medium priority

        # Boost priority based on signals
        if link.get('tag') == 'a' and not link.get('nofollow'):
            priority += 2
        if link.get('anchor_text'):
            priority += 1

        # Boost for internal links
        if link.get('is_internal'):
            priority += 1

        return min(priority, 10)

    async def handle_failure(self, url_info: dict, result: dict):
        status = result.get('status', 'unknown')
        if status in ('timeout', 'error'):
            # Retry with backoff
            retry_count = await self.frontier.redis.incr(
                f"retry:{url_info['url']}"
            )
            if retry_count < 3:
                await asyncio.sleep(retry_count * 5)
                await self.frontier.add_urls([url_info], 0)

        await self.frontier.mark_url_crawled(url_info['url'], False)

    async def progress_monitor(self):
        """Monitor and log crawl progress."""
        while self.is_running:
            stats = {
                'queue_size': self.frontier.redis.zcard(
                    self.frontier.queue_key
                ),
                'recrawl_queue': self.frontier.redis.zcard(
                    'crawler:recrawl_queue'
                ),
                'seen_urls': self.frontier.redis.scard(
                    'crawler:seen_urls'
                ),
                'timestamp': time.time()
            }
            await self.kafka.send('crawler.stats', stats)
            await asyncio.sleep(60)  # Every minute
```

## Caching Strategy (Redis)

### Crawl State Cache

```python
class CrawlStateCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def mark_url_seen(self, url_hash: str):
        """Add URL hash to bloom filter."""
        self.redis.sadd('crawler:seen_urls', url_hash)

    def is_url_seen(self, url_hash: str) -> bool:
        """Check if URL was already seen."""
        return self.redis.sismember('crawler:seen_urls', url_hash)

    def get_domain_delay(self, domain: str) -> int:
        """Get crawl delay for a domain."""
        delay = self.redis.get(f"domain:{domain}:delay")
        return int(delay) if delay else 1

    def mark_crawl_time(self, domain: str, delay: int = 1):
        """Record when we last crawled this domain."""
        self.redis.setex(
            f"domain:{domain}:last_crawl",
            delay * 2,
            time.time()
        )
```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── url.discovered          (new URLs found)
├── page.crawled           (successful page crawl)
├── page.failed            (crawl failure events)
├── robots.updated          (robots.txt changes)
├── crawler.stats          (periodic statistics)
├── crawler.control        (start/stop/pause commands)

Consumer Groups:
├── url-filter-worker      (validate and enqueue new URLs)
├── crawl-analytics        (stats processing)
├── recrawl-scheduler      (manage recrawl scheduling)
```

## Scaling Strategy

### Horizontal Scaling

```text
┌─────────────────────────────────────────────────────────────┐
│                    Crawler Coordinator                        │
│  (Manages workers, distributes work, handles failures)       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Crawler Node │   │ Crawler Node │   │ Crawler Node │
│              │   │              │   │              │
│ 100 Workers  │   │ 100 Workers  │   │ 100 Workers  │
│ 10 Gbps      │   │ 10 Gbps      │   │ 10 Gbps      │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴───────┐
                    │  Redis Cluster │
                    │ (Frontier,     │
                    │  Dedup, State) │
                    └───────────────┘
```

## Failure Handling

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| DNS resolution failure | Retry with exponential backoff, skip after 3 attempts |
| HTTP timeout | Reduce timeout, mark URL for retry |
| Server returns 5xx | Retry with backoff, skip persistent errors |
| Crawler node crash | Other nodes pick up URLs from the shared frontier |
| Disk full on storage node | Route to alternative storage, alert operations |
| Redis cluster failure | Local in-memory queue with checkpoint to disk |

### Retry Logic

```python
class RetryHandler:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def should_retry(self, error: dict) -> bool:
        retry_count = error.get('retry_count', 0)
        if retry_count >= self.max_retries:
            return False

        error_type = error.get('type')
        retryable = [
            'timeout', 'connection_reset', 'dns_failure',
            'http_503', 'http_429'  # Rate limited
        ]
        return error_type in retryable

    def get_backoff(self, retry_count: int) -> int:
        return min(300, (2 ** retry_count) * 5)  # 5, 10, 20, 40... max 300s
```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - pages_crawled_per_second
  - urls_discovered_per_second
  - duplicate_content_percentage
  - average_page_size
  - domain_coverage

System Metrics:

  - download_success_rate
  - average_download_time
  - frontier_queue_size
  - link_extraction_latency
  - content_dedup_rate

Infrastructure Metrics:

  - bandwidth_usage_per_node
  - redis_memory_usage
  - storage_throughput
  - worker_utilization_percentage
  - error_rate_by_type
```

### Alerting

```yaml
alerts:

  - name: High Error Rate
    condition: error_rate > 5% for 5 minutes
    severity: warning

  - name: Crawl Rate Drop
    condition: pages_per_second < 1000 for 10 minutes
    severity: critical

  - name: Frontier Growth Stagnant
    condition: frontier_size < 1000 and pages_per_second > 0
    severity: warning (no new URLs being discovered)

  - name: Bandwidth Exceeded
    condition: bandwidth_usage > 9 Gbps per node
    severity: warning
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| URL Dedup | Bloom filter (O(1), false positives) | Hash set (O(1), memory intensive) | Bloom filter for memory efficiency |
| Frontier Ordering | Priority queue (freshness) | BFS (coverage) | Priority queue with BFS fallback |
| Politeness | Per-domain delay (respectful) | No delay (faster) | Per-domain delay |
| Content Storage | Object store (S3) (scalable) | HDFS (Hadoop-native) | S3-compatible object store |
| Dedup Method | Simhash (near-duplicate) | Exact checksum (exact only) | Both: exact + simhash for near-duplicate |

## Summary

The Web Crawler system design covers:

- **Distributed Crawling**: Hundreds of workers across multiple nodes
- **Politeness**: Per-domain crawl delay and robots.txt compliance
- **Content Dedup**: Exact + near-duplicate detection via simhash
- **URL Management**: Priority-based frontier with recrawl scheduling
- **Fault Tolerance**: Retry logic, error classification, graceful degradation

Key takeaways:

1. Use Bloom filter for O(1) URL deduplication with small memory footprint

2. Implement per-domain politeness with crawl-delay tracking

3. Extract and normalize links with URL filtering

4. Use simhash for near-duplicate content detection

5. Process crawl asynchronously with checkpointing for failure recovery

This design crawls 10B+ pages per month with thousands of distributed workers while respecting website crawling policies.

---

---

## Cheat Sheet
```text
WEB CRAWLER SYSTEM DESIGN CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  | Failure | Mitigation |
  |---------|------------|
  | DNS resolution failure | Retry with exponential backoff, skip after 3 attempts |
  | HTTP timeout | Reduce timeout, mark URL for retry |
  | Server returns 5xx | Retry with backoff, skip persistent errors |
  | Crawler node crash | Other nodes pick up URLs from the shared frontier |
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [REST APIs](../07-REST-API/)
- [System Design - Google Drive](../11-System-Design/05-Google-Drive.md)

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [How Google Web Crawler Works](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Building a Web Crawler (Mercator)](https://www.researchgate.net/publication/225076539_Mercator_A_scalable_extensible_web_crawler)
- [Scrapy Framework](https://scrapy.org/)
