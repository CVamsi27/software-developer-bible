---
section: WebSockets
category: Real-Time
tags: [concept, reference]
---

# WebTransport

## Definition

**WebTransport** is a modern W3C-standardized API for low-latency, bidirectional, and potentially unreliable communication between a web client and server. It runs over HTTP/3 (QUIC) and supports both datagrams (unreliable, low-overhead) and streams (reliable, ordered). It is positioned as the successor to WebSockets for use cases that need either unreliable messaging or the multiplexing benefits of QUIC.

WebTransport is supported in all major browsers as of 2024 (Chrome, Edge, Firefox, Safari) but requires server-side support (typically Node.js with a QUIC library, or a CDN/edge platform).

## Why Do We Need It?

1. **Unreliable messaging**: WebSockets are reliable + ordered. For game state or live video, retransmitting old packets is wasteful.
2. **QUIC multiplexing**: Independent streams without head-of-line blocking (vs TCP/WS).
3. **Connection migration**: QUIC can survive network changes (WiFi → cellular) without dropping — TCP-based WS cannot.
4. **0-RTT handshake**: Faster connection setup than WebSocket's HTTP upgrade.
5. **Server push at QUIC level**: Native server-initiated streams without the WebSocket upgrade dance.

## WebTransport vs WebSocket vs SSE

| Feature | WebSocket | SSE | WebTransport |
|---------|-----------|-----|--------------|
| Direction | Bidirectional | Server→Client | Bidirectional |
| Reliability | Reliable, ordered | Reliable, ordered | Configurable (datagrams unreliable, streams reliable) |
| Transport | TCP (HTTP/1.1 upgrade) | HTTP/1.1+ | QUIC (HTTP/3) |
| Multiplexing | App-level (frames) | N/A | Native streams + datagrams |
| Connection migration | No (TCP breaks) | No | Yes (QUIC) |
| Browser support | Universal | Universal | Modern (2022+) |
| Server support | Trivial | Trivial | Requires QUIC stack |
| Best for | Chat, general real-time | Notifications, stock ticks | Gaming, video, low-latency |

## How It Works

### Connection Flow

```text
Client                                Server
  |                                      |
  |  1. QUIC handshake (0-RTT possible)  |
  | <==================================> |
  |                                      |
  |  2. HTTP/3 CONNECT request           |
  |------------------------------------->|
  |                                      |
  |  3. Session established              |
  |<------------------------------------|
  |                                      |
  |  4. Open bidirectional stream        |
  |====================================>|
  |  or send datagram (unreliable)       |
  |~~datagram~~>                         |
  |                                      |
```

### Stream Types

```text
┌─────────────────────────────────────────────────────────────┐
│                WebTransport Stream Types                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BIDIRECTIONAL STREAM (reliable, ordered)                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Client ────data───▶ Server                         │    │
│  │  Client ◀───data──── Server                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  UNIDIRECTIONAL STREAM (reliable, one-way)                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Client ────data───▶ Server (only)                  │    │
│  │  Server ────data───▶ Client (only)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  DATAGRAM (unreliable, no ordering, low overhead)          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Client ~~datagram~~▶ Server (no retransmit)        │    │
│  │  Bounded size (~1200 bytes typical)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Client API

```typescript
// Establish a WebTransport session
const transport = new WebTransport('https://example.com:443/webtransport');

await transport.ready;  // session established

// Open a bidirectional stream
const stream = await transport.createBidirectionalStream();
const writer = stream.writable.getWriter();
const reader = stream.readable.getReader();

await writer.write(new TextEncoder().encode('Hello from client'));
const { value, done } = await reader.read();
console.log('Server says:', new TextDecoder().decode(value));

// Send a datagram (unreliable, no ack)
const datagramWriter = transport.datagrams.writable.getWriter();
await datagramWriter.write(new TextEncoder().encode('position update'));

// Handle incoming bidirectional stream (server-initiated)
const incomingReader = transport.incomingBidirectionalStreams.getReader();
while (true) {
  const { value: streamPair, done } = await incomingReader.read();
  if (done) break;
  // handle streamPair.readable and streamPair.writable
}

// Cleanup
await transport.close({ closeCode: 0, reason: 'done' });
```

### Server with Node.js (experimental)

```typescript
// Using @fails-components/webtransport or similar
import { createServer } from 'http';
import { WebTransportServer } from './webtransport-server';

const wtServer = new WebTransportServer({
  port: 443,
  cert: fs.readFileSync('cert.pem'),
  key: fs.readFileSync('key.pem'),
});

wtServer.on('session', async (session) => {
  console.log('New WebTransport session');

  // Read bidirectional stream
  const streamReader = session.incomingBidirectionalStreams.getReader();
  const { value: bidir } = await streamReader.read();

  const writer = bidir.writable.getWriter();
  await writer.write(new TextEncoder().encode('Hello from server'));
});

// Or use a managed edge: Cloudflare, Vercel Edge, Fastly
```

### React Hook

```typescript
function useWebTransport(url: string) {
  const [transport, setTransport] = useState<WebTransport | null>(null);
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting');

  useEffect(() => {
    const t = new WebTransport(url);

    t.ready.then(() => {
      setTransport(t);
      setStatus('open');
    });

    t.closed.then(() => setStatus('closed'));

    return () => { t.close(); };
  }, [url]);

  return { transport, status };
}
```

## Real-World Use Cases

### 1. Multiplayer Game State Sync

For 60 FPS games, retransmitting lost position packets adds latency. Use **datagrams** for position updates, **streams** for chat and reliable game events:

```typescript
// Position updates: datagram (unreliable, latest wins)
const dgWriter = transport.datagrams.writable.getWriter();
setInterval(() => {
  dgWriter.write(new TextEncoder().encode(JSON.stringify({
    x: player.x, y: player.y, z: player.z
  })));
}, 16); // 60 FPS

// Game events: bidirectional stream (reliable)
const stream = await transport.createBidirectionalStream();
stream.writable.getWriter().write(encode('player-shot', { weaponId: 5 }));
```

### 2. Live Video/Audio Streaming

Low-latency live streams (sub-second glass-to-glass) work over WebTransport datagrams or streams. YouTube uses QUIC for low-latency streaming.

### 3. Real-Time Collaboration with CRDT

Yjs, Automerge, and Liveblocks can use WebTransport for the underlying transport. Datagrams for ephemeral state, streams for sync messages.

### 4. IoT and Telemetry

Send frequent, lossy-OK sensor readings as datagrams; send commands reliably via streams.

## Common Mistakes

### 1. Using Datagrams for Reliable Data

```text
❌ Bad: send important events as datagrams (they may be dropped)
✅ Good: use streams for reliability, datagrams for lossy-tolerable data
```

### 2. Assuming WebTransport = WebSocket Replacement

WebTransport requires server-side QUIC support. For simple chat apps, WebSocket is still the right choice (universal support, simpler ops).

### 3. Ignoring Connection Migration

QUIC survives network changes — handle `transport.ready` re-firing or `transport.closed` cleanly:

```typescript
transport.closed.then((closeInfo) => {
  if (closeInfo.reason !== 'user-initiated') {
    // Reconnect with backoff
    scheduleReconnect();
  }
});
```

### 4. Not Setting Datagram Size Limits

QUIC datagrams have a max size (~1200 bytes typical). Sending larger messages will throw. Chunk or use streams for large payloads.

## Best Practices

1. **Use streams for reliable data, datagrams for lossy-tolerable**
2. **Handle `transport.closed` with reconnection logic** (unlike WS, QUIC migration may not need it)
3. **Size-limit datagrams** to 1200 bytes to fit in QUIC packets
4. **Use HTTPS in production** (HTTP/3 requires TLS)
5. **Consider edge platforms** (Cloudflare, Fastly) for QUIC support without custom infra
6. **Benchmark before migrating** from WebSocket — most apps don't need QUIC
7. **Use WebTransport polyfills** (`webtransport-polyfill`) for older browsers if needed

## Performance Considerations

| Metric | WebSocket | WebTransport |
|--------|-----------|--------------|
| Handshake | 1-2 RTT (TCP+TLS+upgrade) | 0-1 RTT (QUIC) |
| Head-of-line blocking | Yes (TCP) | No (independent streams) |
| Network change | Connection drops | Seamless migration |
| Datagram overhead | N/A (no unreliable) | ~1-2% over UDP |
| Server memory per connection | ~2-5 KB | ~10-20 KB (QUIC state) |

## Summary

- WebTransport is the modern QUIC-based successor to WebSockets
- Supports reliable streams AND unreliable datagrams
- Solves head-of-line blocking, enables 0-RTT, survives network changes
- Requires HTTP/3 + QUIC on the server (or an edge platform)
- Use datagrams for game state / telemetry, streams for reliable events
- For simple chat or notifications, WebSocket remains the pragmatic choice

---

## Cheat Sheet
```text
WEBTRANSPORT CHEAT SHEET
============================================================

WHEN TO USE:
  • Multiplayer games (datagrams for state, streams for events)
  • Low-latency live video (sub-second)
  • Real-time collaboration (CRDT sync)
  • IoT telemetry (lossy OK)
  • Anywhere TCP head-of-line blocking hurts

WHEN TO STICK WITH WEBSOCKET:
  • Simple chat apps
  • Server-sent notifications
  • Universal server/browser support needed
  • Infra without QUIC support

KEY APIS:
  • new WebTransport(url)        - create session
  • transport.ready              - Promise: connected
  • transport.closed             - Promise: session ended
  • createBidirectionalStream()  - reliable 2-way
  • createUnidirectionalStream() - reliable 1-way
  • transport.datagrams.writable - unreliable send
  • transport.incomingBidirectionalStreams - server-initiated

COMPARED TO WEBSOCKET:
  • Pros: no HOL blocking, unreliable msgs, 0-RTT, migration
  • Cons: needs QUIC server, smaller browser support (2022+)

INTERVIEW TIPS:
  • Explain datagram vs stream trade-offs
  • Discuss connection migration (WiFi to cellular)
  • Know WebTransport is HTTP/3, WebSocket is HTTP/1.1
  • Mention use cases where WebSocket is still better
```
---

## See Also
- [NestJS](../06-NestJS/)
- [Observability](../22-Observability/)
- [Real-Time Architecture](04-Real-Time-Architecture.md)
- [System Design](../11-System-Design/)
- [WebSockets Overview](01-WebSockets-Overview.md)

## References & Learn More

- [WebTransport Specification (W3C)](https://w3c.github.io/webtransport/)
- [MDN WebTransport API](https://developer.mozilla.org/en-US/docs/Web/API/WebTransport)
- [WebTransport over HTTP/3 (RFC 9298)](https://www.rfc-editor.org/rfc/rfc9298)
- [QUIC Working Group](https://quicwg.org/)
- [Cloudflare WebTransport](https://blog.cloudflare.com/announcing-webtransport/)
