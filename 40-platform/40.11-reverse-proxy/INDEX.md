# Reverse Proxy — Index

> **Study time:** ≈ 28 min of reading (2 files, ~14 min average).
> **1 file** — Nginx as the production front door: the C10K origin story, the master–worker event-loop model, config context hierarchy, upstream load balancing, TLS termination, buffering, rate limiting, caching, and zero-downtime reloads.

[![Files](https://img.shields.io/badge/files-2-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Reverse Proxy:** Almost every real deployment puts a reverse proxy between browsers and app servers — Kubernetes ingress is nginx, Docker tutorials are nginx, and "why is prod slow" often lives in a proxy buffer or rate limit. One chapter covers the internals interviewers actually probe: why event loops beat thread-per-connection, what `proxy_pass` really does, and how SIGHUP gives zero-downtime deploys.

---

## The File

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Nginx Reverse Proxy Internals](40.11.01-nginx-reverse-proxy-internals.md) | Forward vs reverse proxy, C10K, master–worker model, epoll/kqueue event loop vs Apache threads, blocking-is-poison (aio threads), main/events/http/server/location contexts, sendfile vs proxy_pass, upstream LB algorithms (round robin, least_conn, ip_hash, weights), passive/active health checks, TLS termination, gzip/brotli, proxy buffering, limit_req burst nodelay, proxy_cache, SIGHUP zero-downtime reload, nginx vs HAProxy vs Envoy vs cloud ALB | 23 min |
| 02 | [Nginx Reverse Proxy Interview Questions](40.11.02-interview-questions.md) | 18 senior-depth Q&A: event-loop failure modes, reload semantics, buffering/keepalive defaults that bite, health checks, rate limiting, the nginx-vs-alternatives decision, scenario drills (502 diagnosis, outage story, "is nginx still relevant?") | 5 min |

---

## When to read

- **Before any deployment/platform interview** — pairs with [Load Balancing](../../30-architecture/30.2-system-design/01-theory/30.2.1.04-load-balancing.md)
- 26 min read
- Then reference back when debugging ingress controllers, TLS chains, or rate-limit configs

## Common interview questions

The full bank with model answers: → [40.11.02 Interview Questions](40.11.02-interview-questions.md). The headlines:
- "What does a reverse proxy do that a load balancer doesn't?" (and vice versa)
- "How does nginx handle 10K concurrent connections with a handful of workers?"
- "One worker stalls and thousands of connections freeze — what happened?"
- "Walk me through a zero-downtime nginx reload."
- "When would you pick HAProxy or Envoy over nginx?"

---

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
