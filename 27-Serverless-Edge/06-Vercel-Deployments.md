---
section: Serverless & Edge
category: DevOps
tags: [concept]
---

# Vercel Deployments

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

---

### See Also

- [Next.js Deployment](../../04-NextJS/)
- [Edge Functions](../02-Edge-Functions.md)
- [AWS Lambda](../05-AWS-Lambda.md)

### References

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Edge Runtime](https://vercel.com/docs/functions/edge-functions)
