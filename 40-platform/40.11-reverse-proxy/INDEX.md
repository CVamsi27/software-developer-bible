# Reverse Proxy — Index

> **Study time:** ≈ 19 min of reading (3 files, ~6 min average).
> **1 teaching chapter** — Follow a request from worker and route selection through upstream handling, backpressure, trust boundaries, and graceful reloads. Use the revision companion and interview bank to test the mechanisms afterward.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

A proxy separates client-facing HTTP policy from backend request handling. Read this section by tracing where a request waits and which layer owns each decision. NGINX is one implementation; Kubernetes Ingress does not imply NGINX, and the community ingress-nginx controller retired in March 2026.

---

## The File

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Nginx Reverse Proxy Internals](40.11.01-nginx-reverse-proxy-internals.md) | Request routing, worker capacity, upstream selection and version-specific connection reuse, timeout and retry boundaries, buffering, trusted client identity, TLS, rate limiting, caching, and graceful reloads | Important | Specialized | 11 min |
| — | [Revision questions](REVISION.md) | Recall checks for routing, keepalive versions, buffering, trusted identity, timeouts, caching, and safe retries | Important | Specialized | 2 min |
| 02 | [Nginx Reverse Proxy Interview Questions](40.11.02-interview-questions.md) | Scenario-driven practice for worker stalls, reloads, WebSockets, upstream health, rate limiting, 502 diagnosis, and proxy selection | Important | Specialized | 6 min |

---

## Reading Passes

1. **Follow the request:** trace a client through the worker, location, upstream, and response path in [the chapter](40.11.01-nginx-reverse-proxy-internals.md).
2. **Change one condition:** predict what changes for a slow client, unavailable upstream, untrusted forwarding header, or WebSocket held during reload.
3. **Retrieve, then practice:** complete [the revision questions](REVISION.md), then use [the interview bank](40.11.02-interview-questions.md). Support behavioral answers with your own evidence.

## Cross-References

- [CDN & Edge](../40.10-cdn/INDEX.md) — caching one layer further out
- [Docker](../40.1-docker/INDEX.md) — nginx as the containerized edge
- [Observability](../40.4-observability/INDEX.md) — `$request_time` vs `$upstream_response_time`
- [System Design Theory](../../30-architecture/30.2-system-design/01-theory/INDEX.md) — transport + LB fundamentals behind every proxy decision

---

## Navigation

[← Previous: Twelve-Factor](../40.9-twelve-factor/INDEX.md) · [< Back to Platform](../INDEX.md) · [Next: CDN & Edge →](../40.10-cdn/INDEX.md)

---

## Docita Anchor

These existing [Docita](https://github.com/CVamsi27/docita) pointers describe managed-proxy integration rather than a self-managed NGINX implementation. Inspect code and actual routing/credential policy before making a deployment claim.

| Topic | Docita evidence |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| TLS termination (managed) | Twice: Cloudflare edge, then Fly's router (`http_service.force_https = true`) — zero nginx config owned by me |
| Trusting the proxy layer | `shared/common/http/cloudflare-ips.ts` + `client-ip.ts` recover real client IPs from CF headers; ADR 0014 restricts ingress to CF ranges |
| Proxy behaviors I still own | Timeouts/budgets at the app edge (`timeout.interceptor.ts`, `fetch-with-timeout.ts`) because the platform proxy's knobs are fixed |
| nginx/HAProxy/Envoy ops stories | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
