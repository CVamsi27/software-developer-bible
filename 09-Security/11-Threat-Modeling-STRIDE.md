---
section: Security
category: Architecture
tags: [concept]
---

# Threat Modeling — STRIDE & Attack Surfaces

> **TL;DR:** Threat modeling is the practice of systematically enumerating what can go wrong, before the code ships. STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation) is the classic framework; the senior test is doing it during design, not after the incident, and producing concrete mitigations tied to data flows, not generic checklists.
>
> **Why it matters:** This is an Architecture interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**Threat modeling** is a structured analysis of a system's data flows, trust boundaries, and assets to identify, prioritize, and mitigate threats before they are exploited. The two dominant approaches are **STRIDE** (a per-element checklist of threat categories) and **attack trees** (decomposed attack paths from a goal). Senior engineers integrate threat modeling into design reviews and architecture decisions, treat it as a reusable artifact (a living document), and tie each threat to a concrete mitigation and owner.

## Why Do We Need It?

1. **Shift left** — A vulnerability found in design is cheap; the same finding in production costs an incident.
2. **Coverage** — You can't secure what you haven't enumerated; "I added auth" misses the new microservice.
3. **Prioritization** — Not all threats are equal; threat modeling gives you a risk-ranked backlog.
4. **Shared mental model** — Security stops being "the security team's problem" and becomes everyone's.
5. **Audit & compliance** — SOC 2, ISO 27001, and PCI-DSS all require some form of threat modeling.
6. **Reduce blast radius** — Trust boundaries explicit at design time mean a breach doesn't propagate.
7. **Better code** — A clear data flow is good engineering; threat modeling forces you to draw it.

## How It Works

### STRIDE Per Element

| Threat | Question | Example |
|--------|----------|---------|
| **S**poofing | Can an attacker pretend to be a user / service? | Forged JWT, stolen API key |
| **T**ampering | Can an attacker modify data in transit or at rest? | Modified request body, SQL injection |
| **R**epudiation | Can a user deny an action they took? | Missing audit log, no idempotency key |
| **I**nformation Disclosure | Can an attacker see data they shouldn't? | Verbose error, log leak, IDOR |
| **D**enial of Service | Can an attacker make the system unavailable? | Slowloris, expensive query, large payload |
| **E**levation of Privilege | Can an attacker gain more access than allowed? | Role escalation, missing authz check |

### Data Flow Diagram

```text
┌────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────┐
│  Browser   │───▶│  API GW     │───▶│  Auth Svc   │───▶│  IdP    │
│  (User)    │    │  (rate-lim) │    │ (JWT issue) │    │ (OAuth) │
└────┬───────┘    └──────┬──────┘    └──────┬──────┘    └─────────┘
     │                   │                  │
     │       Trust       │      Trust       │
     │     Boundary 1    │   Boundary 2     │
     │                   │                  │
     │                   ▼                  ▼
     │            ┌─────────────┐    ┌─────────────┐
     │            │  Orders API │───▶│  Postgres   │
     │            │  (business  │    │  (truth)    │
     │            │   logic)    │    └──────┬──────┘
     │            └──────┬──────┘           │
     │                   │                  │
     │                   ▼                  ▼
     │            ┌─────────────┐    ┌─────────────┐
     │            │  Kafka      │    │  S3         │
     │            │  (events)   │    │  (assets)   │
     │            └─────────────┘    └─────────────┘
     │
     └──────▶ (public internet, untrusted)
```

For every arrow crossing a trust boundary, ask each STRIDE question.

## Code Examples

### Threat Record

```yaml
# threats/ORD-2025-01.yaml
id: THREAT-ORD-001
title: IDOR on /orders/:id allows reading other users' orders
stride: I      # Information Disclosure
asset: Order
dataflow: Browser -> API GW -> Orders API -> Postgres
likelihood: High
impact: High
risk: High
mitigations:
  - Enforce ownership check in OrdersService.getById (compare userId to JWT.sub)
  - Add integration test: GET /orders/<other-user-id> returns 404
  - Add structured log on 403/404 for monitoring
owner: orders-team
status: Open
```

### Authentication Threat Catalogue (sample)

```text
STRIDE-AUTH-001  Spoofing:    Forged JWT (alg=none / weak key)
  Mitigation:  Pin RS256 / ES256; reject 'none'; rotate keys via JWKS

STRIDE-AUTH-002  Spoofing:    Stolen refresh token
  Mitigation:  Refresh-token rotation; family revocation; device fingerprinting

STRIDE-AUTH-003  Repudiation: User denies placing an order
  Mitigation:  Append-only audit log with user_id, ip, ua, action, payload hash

STRIDE-AUTH-004  Info Disc.:  Verbose login error reveals user enumeration
  Mitigation:  Generic 'invalid credentials' message; constant-time response

STRIDE-AUTH-005  DoS:         Brute-force login
  Mitigation:  Rate limit per IP + per account; CAPTCHA after N failures; lockout

STRIDE-AUTH-006  Elev. Priv.: Admin role mis-assigned in token
  Mitigation:  Server-side role lookup; never trust role claim for authorization
```

### Trust Boundary Checklist (used during design review)

```text
[ ] Public internet -> API gateway
    - TLS only, HSTS, valid cert
    - Rate limit per IP
    - Body size limit
    - JWT/session validation

[ ] API gateway -> service mesh
    - mTLS between services
    - Service identity via SPIFFE/SPIRE
    - Per-route authz (e.g. OPA)

[ ] Service -> database
    - TLS to DB
    - Least-privilege role per service
    - Parameterized queries
    - Audit log of writes

[ ] Service -> object store
    - Pre-signed URLs with short TTL
    - Server-side encryption
    - Per-tenant prefix
    - Lifecycle policies for old data
```

### Trust Boundary in Code (Example: BFF)

```typescript
// bff/orders.controller.ts — sits at the trust boundary between
// the public internet and the internal services.
// Every request here is untrusted; everything past here is internal.

@UseGuards(AuthGuard, RateLimitGuard)   // 1. authenticate
@Controller('orders')
export class OrdersBffController {
  @Get(':id')
  async getOne(@Req() req: AuthedRequest, @Param('id') id: string) {
    // 2. authorize — does the JWT subject own this order?
    const order = await this.ordersService.getById(id);
    if (order.userId !== req.user.sub) {
      throw new NotFoundException();   // 404 (not 403) to avoid existence leak
    }
    return order;
  }
}
```

## Real-World Use Cases

1. **New microservice design** — Threat model in the design doc; review in PR; revisit on every authn/authz change.
2. **Public API launch** — STRIDE the API surface; map OWASP API Top 10; produce a customer-facing security page.
3. **PCI-DSS scope** — Threat model the card-data flow; reduce scope by tokenization.
4. **M&A integration** — Threat model the merged system from scratch; both legacy teams had different assumptions.
5. **Annual review** — Re-walk the data flow diagram; re-score risks; close anything that drifted.
6. **Bug-bounty triage** — Use the threat model to classify reports: in-scope, out-of-scope, or new threat.
7. **Compliance audit** — SOC 2 / ISO 27001 evidence; threat model + mitigations + owners = auditable artifact.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Threat modeling only after launch | Do it in the design phase, before code |
| One giant document nobody reads | Per-system living document; update on every change |
| Generic checklists without data flow | STRIDE per arrow in the data flow, not generic |
| Threat = bug | A threat is a *category*; the bug is one instance; model categories |
| No owner / no status | Each threat has an owner, status, and due date |
| Mitigation = "use TLS" | Concrete: TLS 1.2+, valid cert, HSTS, cipher restrictions |
| Confusing STRIDE with compliance | STRIDE finds risks; controls are the mitigations; compliance is the audit |
| Skipping the data flow diagram | The diagram is the threat model; without it you are guessing |

## Best Practices

1. **Draw the data flow first** — Every box, every arrow, every trust boundary. This is the threat model.
2. **STRIDE per arrow, not per system** — Each crossing of a trust boundary has 6 threat questions.
3. **Risk score every threat** — Likelihood × impact; prioritize the top quartile.
4. **Tie each threat to a concrete mitigation** — "Add auth" is not a mitigation; "Validate JWT with `jwks-rsa` and `aud` claim check" is.
5. **Own every threat** — A threat without an owner is a threat that won't be fixed.
6. **Revisit on every change** — Adding a new microservice? Re-walk the data flow. New auth flow? Re-STRIDE.
7. **Use the framework as a checklist, not a script** — STRIDE helps you enumerate; your judgment ranks them.
8. **Pair threat modeling with abuse cases** — For each feature, write 1–2 abuse cases (e.g., "user creates 1M accounts to harvest emails").
9. **Capture decisions in the design doc** — "We chose mTLS over JWT for service-to-service because …" — future readers will thank you.
10. **Integrate with the SDLC** — Threat model at design review; security review in CI; pen test before launch; ongoing bug bounty.

## Performance Considerations

- Threat modeling is a design-time activity; it has no runtime cost.
- The mitigations it produces (mTLS, validation, rate limiting) each have a small runtime cost — measure before declaring "overhead".
- A good threat model is faster than a security incident; the ROI is asymmetric.

## Summary

- Threat modeling is structured enumeration of what can go wrong, before code ships.
- STRIDE gives you a per-element checklist; data flow diagrams give you the elements.
- Every threat gets a risk score, a concrete mitigation, and an owner.
- It is a living artifact, not a one-time document.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| STRIDE | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege |
| Trust boundary | A line where the trust level changes (public internet → service, etc.) |
| Data flow diagram | Boxes (processes / data stores) + arrows (data flow) + trust boundaries |
| Risk score | Likelihood × impact; prioritize the top quartile |
| Mitigation | A concrete technical control (e.g., "validate JWT aud claim") |
| Owner | The person/team responsible for closing the threat |
| DFD | Data Flow Diagram — the foundation of the threat model |
| Asset | What you are protecting (data, system, reputation) |
| STRIDE per arrow | Apply STRIDE at each crossing of a trust boundary |
| Living document | Updated on every change to the system |
| OWASP API Top 10 | Industry-standard API threat catalog (BOLA, BFLA, etc.) |
| mTLS | Mutual TLS — both client and server authenticate; used at service-to-service trust boundaries |

---

## See Also
- [Microservices](../12-Microservices/) (trust boundaries in service mesh)
- [REST APIs](../07-REST-API/) (API threat catalog)
- [System Design](../11-System-Design/) (security in system design)
- [Web Security](./09-Web-Security.md) (OWASP Top 10)

## References & Learn More

- [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [Adam Shostack — Threat Modeling: Designing for Security](https://shostack.org/books/threat-modeling-book)
- [Tactical Edge — Practical Threat Modeling](https://tacticaledge.co/practical-threat-modeling/)
- [Elevation of Privilege (EoP) Card Game](https://shostack.org/games/eop)
