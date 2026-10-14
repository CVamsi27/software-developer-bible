<!-- section: Platform | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Platform-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Platform — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Nginx Reverse Proxy Internals

Source: [Nginx Reverse Proxy Internals](40.11.01-nginx-reverse-proxy-internals.md)

**Q:** When can one slow operation delay many requests assigned to the same NGINX worker?

**A:** A worker multiplexes many connections. A blocking file operation, CPU-heavy filter, or synchronous plugin occupies that worker and delays its other scheduled work. Supported file operations can use `aio threads`; CPU-heavy application logic belongs downstream. See [NGINX core I/O directives](https://nginx.org/en/docs/http/ngx_http_core_module.html).

**Q:** Why validate before reloading Nginx?

**A:** `nginx -t` catches configuration errors before the reload. A successful reload starts new workers and drains old ones, but valid syntax can still route to the wrong service. Probe the changed behavior after reload. See [NGINX process control](https://nginx.org/en/docs/control.html).

**Q:** When is response buffering useful and when is it harmful?

**A:** It shields upstreams from slow clients for ordinary responses. For streaming/SSE it can delay delivery, so configure the relevant path deliberately.

**Q:** Why forward an explicit trusted client-address policy?

**A:** A client can forge forwarding headers. Only accepted proxy hops should establish the original address used for logging, rate limits, or security decisions.

**Q:** Why is upstream keepalive separate from client keepalive?

**A:** They are separate connections on opposite sides of the proxy. NGINX 1.29.7 changed upstream proxying to HTTP/1.1 with keepalive by default; older releases commonly need explicit HTTP/1.1, cleared `Connection`, and an upstream `keepalive` cache. See the [upstream module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html).

**Q:** What must be configured before HTTPS upstream traffic is authenticated?

**A:** NGINX encrypts an HTTPS upstream connection, but certificate verification and SNI are off by default. Enable verification, trust the intended CA, and send the expected SNI/name so the certificate is checked for the intended service. See the [proxy TLS directives](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

**Q:** Why is `worker_connections` not a direct estimate of proxied request capacity?

**A:** It counts every connection opened by a worker, including client and upstream sockets, and the open-file limit can lower the actual ceiling. A typical proxied request uses two sockets; HTTP/2 can carry multiple streams on one client connection. See the [NGINX core module](https://nginx.org/en/docs/ngx_core_module.html).

**Q:** Did the ingress-nginx retirement remove Kubernetes Ingress or every NGINX-based controller?

**A:** No. The community ingress-nginx controller retired in March 2026 and no longer receives fixes or security updates. Ingress remains an API, and other products have separate lifecycles. Select a maintained implementation and test policy translation during migration.

**Q:** /api/users matches location /api/. How does a trailing slash on proxy_pass change the path?

**A:** A proxy_pass without a URI preserves /api/users. With a URI /, the ordinary prefix match is replaced, forwarding /users. Rewrites/variables/regex locations have further conditions.

**Q:** An upstream sends a byte every twenty seconds under proxy_read_timeout 30s. Must the response end at thirty seconds?

**A:** No. The setting measures the interval between upstream reads. A total application deadline needs a separate boundary.

**Q:** Does burst=20 nodelay hold twenty extra requests in a delay queue?

**A:** No. It admits excess immediately while rate accounting drains. Without nodelay, permitted excess may be delayed. Requests beyond the capacity are rejected under the configured response policy.

**Q:** Why pair proxy_cache_bypass with proxy_no_cache for an authenticated request?

**A:** One controls serving an existing entry; the other controls storing the response. Correct keys and upstream cache controls remain necessary; a public cache must not reuse personalized content across identities.

**Q:** Does successfully reloading workers prove a POST with a lost upstream reply is safe to repeat?

**A:** No. The upstream could have committed. Retrying needs stable application operation identity and outcome reconciliation, independently of worker replacement.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
