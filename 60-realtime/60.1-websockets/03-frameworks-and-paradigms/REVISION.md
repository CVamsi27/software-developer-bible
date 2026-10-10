<!-- section: WebSockets | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-WebSockets-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# WebSockets — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## NestJS WebSockets

Source: [NestJS WebSockets](60.1.3.01-nestjs-websockets.md)

**Q:** Why apply message-level authorization after authenticating a Nest gateway connection?

**A:** A user can request another room/resource or retain a stale session. Verify the operation's permissions and payload, and plan session expiry/revocation.

## GraphQL Subscriptions & Live Queries

Source: [GraphQL Subscriptions & Live Queries](60.1.3.02-graphql-subscriptions-live-queries.md)

**Q:** What distinguishes a subscription from a live query?

**A:** A subscription emits responses from application events; a live query re-executes as relevant data changes. Transport connection alone does not provide invalidation or authorization.

## WebRTC Peer-to-Peer

Source: [WebRTC Peer-to-Peer](60.1.3.03-webrtc-peer-to-peer.md)

**Q:** Why does WebRTC still need a signaling service and TURN?

**A:** Peers need an authenticated path to exchange negotiation/candidate information. Direct connectivity can fail, so a reachable relay with controlled credentials is needed for the supported network population.

## Testing Real-Time Systems

Source: [Testing Real-Time Systems](60.1.3.04-testing-realtime-systems.md)

**Q:** What should a socket smoke test assert besides connection success?

**A:** Test a message and response with the correct permissions, any required ordering or resume-cursor rules, rejected requests, and cleanup after disconnecting. Completing a handshake does not show that application operations behave correctly.

**Q:** Why include slow consumers and reconnect churn in load scenarios?

**A:** Healthy fast clients miss backpressure, buffer growth, authentication spikes, retry storms, and leaks. Those scenarios can exhaust a system with modest average throughput.

## Gateway Pipeline and Response Contract

Source: [NestJS WebSockets](60.1.3.01-nestjs-websockets.md)

**Q:** In the Nest fixture, which stages distinguish a bad token from an unauthorized room?

**A:** Namespace middleware rejects the bad token. A message guard establishes current session state, the pipe validates payload and the snapshot service checks room access.

**Q:** Why can a WsException be observed while emitWithAck still times out?

**A:** The default filter emits an exception event rather than acknowledging the same command with an error. The application must implement a uniform acknowledgment contract if that is required.

**Q:** Does guarding incoming events stop every private room broadcast after permission is revoked?

**A:** No. Outgoing subscriptions/room membership need a revocation policy too. A message guard only protects handlers that run through it.

## Subscription Execution and Lifecycle

Source: [GraphQL Subscriptions](60.1.3.02-graphql-subscriptions-live-queries.md)

**Q:** Does context run only once when a graphql-ws connection opens?

**A:** No. Context construction is operation-related. Use the connection hook for acceptance and authorize the requested subscription plus continuing results.

**Q:** Why can one next result contain errors without becoming a protocol error message?

**A:** GraphQL execution results can contain their own errors array. Protocol operation errors and WebSocket close codes are separate paths that the client must handle.

**Q:** What does the finite fixture prove about a broker replay path?

**A:** Nothing about a broker: it yields simulated events from an async generator. It proves local subscription execution and permissions; replay requires another explicitly tested source and cursor contract.

## Peer Connection and Message Semantics

Source: [WebRTC Peer-to-Peer](60.1.3.03-webrtc-peer-to-peer.md)

**Q:** Why did waiting for the sender channel open not prove the receiver channel event had arrived?

**A:** They are separate asynchronous events. The fixture waits for the receiver’s datachannel event and open state as well before declaring the pair ready.

**Q:** A newer complete position is applied before an older position arrives. What prevents rollback?

**A:** The receiver compares sequence values and discards older snapshots. Unordered/no-retransmit settings permit stale arrival; they do not perform application deduplication.

**Q:** Why is a TURN relay different from an ordinary SFU encryption endpoint?

**A:** TURN forwards protected packets along a route. An ordinary SFU terminates peer transport sessions; additional end-to-end media protection must be designed if the SFU must not access media.

## Test Evidence and Measurement

Source: [Testing Real-Time Systems](60.1.3.04-testing-realtime-systems.md)

**Q:** What concurrency follows from ten arrivals per second with thirty-second sessions in a stable workload?

**A:** About 300 active clients, ignoring startup/end transients. A maxVusers setting of 20,000 does not create that many active clients by itself.

**Q:** Why does a server timestamp not eliminate cross-host latency error?

**A:** The client compares it using another clock. Skew remains unless synchronized/quantified or the measurement avoids unrelated clocks.

**Q:** What should a recovery test compare when duplicate packets are expected?

**A:** Compare final authoritative state and business effects under the contract. At-least-once attempts can repeat packets without repeating an effect.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
