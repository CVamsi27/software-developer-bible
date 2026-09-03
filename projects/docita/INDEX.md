# Docita — Architecture Decision Deep Dives

> Every major decision in Docita, explained with context, alternatives considered, trade-offs, what worked, what failed, and what could be better.

---

## How to Read This Section

Each file follows a consistent structure:

| Section | What It Answers |
| --------------------------- | ------------------------------------------- |
| **Context** | What problem were we solving? |
| **Decision** | What did we choose? |
| **Alternatives Considered** | What else was on the table? |
| **Why This Was Chosen** | The real reasoning (not just "it's better") |
| **Trade-offs** | What we gave up |
| **What Worked** | What exceeded expectations |
| **What Failed** | What broke in production |
| **What Could Be Better** | Known tech debt and improvements |
| **Code Evidence** | Exact file paths proving every claim |
| **Interview Script** | How to explain it in 60 seconds |

---

## Files

| # | File | Topic | Why It Matters |
| --- | -------------------------------------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| 01 | [Architecture Decisions](01-architecture-decisions.md) | DDD, Zod-first, NestJS modules, monorepo | Foundation choices that shaped everything |
| 02 | [Multi-Tenancy & RLS](02-multi-tenancy-rls.md) | 7-layer defense, AsyncLocalStorage, RLS | The hardest problem — data isolation in healthcare |
| 03 | [Async Processing](03-async-processing.md) | Postgres queue, transactional outbox, worker | How we process jobs without Redis |
| 04 | [Payment Flows](04-payment-flows.md) | Three rails, Razorpay, idempotency | Financial compliance — never mix payment flows |
| 05 | [Clinic Workflows](05-clinic-workflows.md) | Scheduling, queue, follow-ups, OPD | The core product — how clinics actually use Docita |
| 06 | [WhatsApp Integration](06-whatsapp-integration.md) | Templates, responses, rate limits | WhatsApp-first means it must work perfectly |
| 07 | [Prescription Safety](07-prescription-safety.md) | Allergy checks, controlled substances, PDFs | Clinical safety — wrong prescriptions harm patients |
| 08 | [Billing & Invoicing](08-billing-invoicing.md) | GST, tax calculation, invoice lifecycle | Indian healthcare billing complexity |
| 09 | [Subscription System](09-subscription-system.md) | Tier gating, overage, referrals | SaaS monetization — how clinics pay Docita |
| 10 | [Deployment & Infrastructure](10-deployment-infrastructure.md) | Fly.io, Cloudflare, migrations, cold starts | Production reliability at small-team scale |
| 11 | [What I'd Do Differently](11-what-id-do-differently.md) | Retrospective, tech debt, future improvements | Honest assessment — what's not perfect |

---

## Cross-References

- **Interview defense guide:** [80.36-docita-complete-interview-defense.md](80.36-docita-complete-interview-defense.md)
- **Resume evidence pack:** [80.17-docita-interview-evidence-pack.md](80.17-docita-interview-evidence-pack.md)
- **Tech topic mapping:** [80.22-docita-tech-topic-mapping.md](80.22-docita-tech-topic-mapping.md)
- **Google-level prep:** [80.21-docita-google-level-prep.md](80.21-docita-google-level-prep.md)

---

## Key Numbers to Remember

| Metric | Number |
| --------------- | ------------------------------------------------------------------------- |
| Active clinics | 25+ |
| Workflows/month | 1,000+ |
| Domain modules | 28 |
| Prisma models | 149 |
| ADRs | 14 |
| Tech stack | TypeScript, React 19, NestJS 11, Prisma 7, PostgreSQL, Fly.io, Cloudflare |
