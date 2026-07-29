# Vercel Deployments

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

## Definition

**Vercel** is a deployment platform optimized for frontend frameworks (Next.js, SvelteKit, Nuxt). It provides global edge network, serverless functions, automatic HTTPS, preview deployments, and Git integration. Vercel pioneered the **Edge Runtime** and **Serverless Functions** for Jamstack applications.

## Why Do We Need It?

1. **Git-integrated**: Auto-deploy on push; preview deployments for every branch/PR
2. **Edge Functions**: Run code at 100+ global locations for near-zero latency
3. **Serverless Functions**: Auto-scaling Node.js/Python/Go API endpoints
4. **Next.js native**: Optimal monorepo support, ISR, SSR, Edge Middleware

## Key Features

| Feature | Description |
|---------|-------------|
| Preview Deployments | Unique URL per branch/PR with comments |
| Edge Config | Globally replicated KV store (5ms reads) |
| Edge Middleware | Run before request hits serverless function |
| Image Optimization | Automatic WebP/AVIF, CDN-cached |
| Analytics | Real-time Web Vitals, usage insights |

## Summary

- Vercel provides serverless deployment for frontend frameworks with automatic HTTPS and CDN distribution
- Edge Functions run at the network edge for sub-50ms response times using the V8 runtime
- Serverless Functions (Node.js, Python, Go, Ruby) auto-scale and support region selection for data locality
- Preview deployments for every git branch enable instant collaboration and review environments
- Analytics dashboard provides real-time insights into performance, bandwidth, and error rates

---

## Cheat Sheet
```text
VERCEL DEPLOYMENTS CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [AWS Lambda](05-AWS-Lambda.md)
- [Docker](../13-Docker/)

## References & Learn More

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Edge Runtime](https://vercel.com/docs/functions/edge-functions)
