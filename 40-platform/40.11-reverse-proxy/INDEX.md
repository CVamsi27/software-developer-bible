# Reverse Proxy — Index

> **Study time:** ≈ 29 min of reading (3 files, ~10 min average).
> **1 file** — Nginx as the production front door: the C10K origin story, the master–worker event-loop model, config context hierarchy, upstream load balancing, TLS termination, buffering, rate limiting, caching, and zero-downtime reloads.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

A proxy separates client-facing HTTP policy from backend request handling. Read this section by tracing where a request waits and which layer owns each decision. NGINX is one implementation; Kubernetes Ingress does not imply NGINX, and the community ingress-nginx controller retired in March 2026.

---

## The File

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Nginx Reverse Proxy Internals](40.11.01-nginx-reverse-proxy-internals.md) | Forward vs reverse proxy, C10K, master–worker model, epoll/kqueue event loop vs Apache threads, blocking-is-poison (aio threads), main/events/http/server/location contexts, sendfile vs proxy_pass, upstream LB algorithms (round robin, least_conn, ip_hash, weights), passive/active health checks, TLS termination, gzip/brotli, proxy buffering, limit_req burst nodelay, proxy_cache, SIGHUP zero-downtime reload, nginx vs HAProxy vs Envoy vs cloud ALB | 20 min |
| 02 | [Nginx Reverse Proxy Interview Questions](40.11.02-interview-questions.md) | Focused Q&A: event-loop failure modes, reload semantics, buffering/keepalive defaults that bite, health checks, rate limiting, the nginx-vs-alternatives decision, scenario drills (502 diagnosis, outage story, "is nginx still relevant?") | 7 min |

---

## Reading Passes

1. **Follow the request:** identify the master/worker roles and trace a request through location selection, upstream forwarding and response delivery in [the chapter](40.11.01-nginx-reverse-proxy-internals.md).
2. **Explain a failure:** change one condition — slow client, unavailable upstream, wrong header inheritance or draining WebSocket — and predict which boundary needs configuration or measurement.
3. **Check recall, then practice:** finish [the separate revision](REVISION.md) before using [the interview bank](40.11.02-interview-questions.md). Use your own incident evidence for behavioral answers.

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

Where [docita](https://github.com/CVamsi27/docita) meets reverse proxies — plainly: **no self-managed nginx exists**; the proxy is consumed, not operated.

| Topic | Docita evidence |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| TLS termination (managed) | Twice: Cloudflare edge, then Fly's router (`http_service.force_https = true`) — zero nginx config owned by me |
| Trusting the proxy layer | `shared/common/http/cloudflare-ips.ts` + `client-ip.ts` recover real client IPs from CF headers; ADR 0014 restricts ingress to CF ranges |
| Proxy behaviors I still own | Timeouts/budgets at the app edge (`timeout.interceptor.ts`, `fetch-with-timeout.ts`) because the platform proxy's knobs are fixed |
| nginx/HAProxy/Envoy ops stories | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
