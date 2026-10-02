<!-- section: Platform | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Platform-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Platform — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Nginx Reverse Proxy Internals

Source: [Nginx Reverse Proxy Internals](40.11.01-nginx-reverse-proxy-internals.md)

**Q:** Why can one slow operation damage many Nginx requests?

**A:** A worker multiplexes many connections. Blocking work on that worker delays unrelated clients; use supported asynchronous/offloaded paths and move heavy application work downstream.

**Q:** Why validate before reloading Nginx?

**A:** Syntax/configuration validation prevents a malformed replacement configuration. A reload then starts new workers and drains old ones; runtime semantics still need probes.

**Q:** When is response buffering useful and when is it harmful?

**A:** It shields upstreams from slow clients for ordinary responses. For streaming/SSE it can delay delivery, so configure the relevant path deliberately.

**Q:** Why forward an explicit trusted client-address policy?

**A:** A client can forge forwarding headers. Only accepted proxy hops should establish the original address used for logging, rate limits, or security decisions.

**Q:** Why is upstream keepalive separate from client keepalive?

**A:** They are different connection pools on opposite sides of the proxy. Reusing a browser connection does not automatically reuse an upstream connection.

**Q:** Did the ingress-nginx retirement remove Kubernetes Ingress or every NGINX-based controller?

**A:** No. The community ingress-nginx controller retired in March 2026 and no longer receives fixes or security updates. Ingress remains an API, and other products have separate lifecycles. Select a maintained implementation and test policy translation during migration.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
