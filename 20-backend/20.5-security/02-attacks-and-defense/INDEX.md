# Attacks & Defense - Security

> **Study time:** ≈ 33 min of reading (5 files, ~7 min average).
> **5 files.** Study browser injection, forged requests, SQL injection and API security, then recall their trust boundaries with the separate revision drill.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Attacks%20%26%20Defense-blue)](../INDEX.md)

---

## Learning flow

Start with where untrusted text becomes executable browser content. Then separate browser credential attachment from request intent, and SQL syntax from bound values. Read API security last to compose these controls with object permissions, resource limits and outbound requests.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [XSS](20.5.2.01-xss.md) | Stored/reflected/DOM flows, context encoding, HTML sanitization, CSP, Trusted Types | Essential | Foundational | 6 min |
| 02 | [CSRF](20.5.2.02-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking | Essential | Foundational | 7 min |
| 03 | [SQL Injection](20.5.2.03-sql-injection.md) | Bound values, allowlisted query grammar, TypedSQL/raw-query boundaries, LIKE patterns and least privilege | Essential | Foundational | 6 min |
| 04 | [API Security Best Practices](20.5.2.04-api-security-best-practices.md) | Object and property authorization, cost budgets, sensitive business flows, SSRF and dependency trust | Essential | Foundational | 10 min |

After these chapters, use [category revision](REVISION.md), then the [security interview bank](../04-interview-drills/20.5.4.01-interview-questions.md).

---

[← Back to Security](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) paths are review starting points. Verify current configuration and route coverage before treating them as deployed security evidence:

| Topic | Docita evidence |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| CSRF | `apps/api/src/shared/common/interceptors/csrf.interceptor.ts` - double-submit cookie/header pair compared timing-safe |
| XSS / security headers | `apps/api/src/main.ts` - `configureSecurityHeaders` applies Helmet/CSP to the HTTP API; `/docs` gets a development-specific policy override |
| SQL injection | `apps/api/src/shared/common/utils/postgres-advisory-lock.ts` - even raw SQL goes through parameterized `$queryRaw` tagged templates |
| BOLA / IDOR defense | `apps/api/src/shared/common/extensions/tenant.extension.ts` - tenant-scoping extension; inspect covered clients, models and raw-query bypasses |
| Audit trail (API Top 10) | `apps/api/src/shared/common/interceptors/patient-audit.interceptor.ts` - PHI access auditing on patient reads |

---

[← Previous: Auth](../01-auth/INDEX.md) · [Next: Hardening & Operations →](../03-hardening-and-operations/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
