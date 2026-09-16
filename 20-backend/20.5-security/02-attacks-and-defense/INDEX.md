# Attacks & Defense - Security

> **Study time:** ≈ 49 min of reading (4 files, ~12 min average).
> **4 files.** What can go wrong and how to stop it: XSS, CSRF, SQL injection, and the OWASP API Top 10 — the most-asked attack questions in senior interviews.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Attacks%20%26%20Defense-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [XSS](20.5.2.01-xss.md) | Stored/reflected/DOM XSS, CSP, encoding, sanitization | 11 min |
| 02 | [CSRF](20.5.2.02-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking | 14 min |
| 03 | [SQL Injection](20.5.2.03-sql-injection.md) | Parameterized queries, ORM protection, input validation, WAF | 12 min |
| 04 | [API Security Best Practices](20.5.2.04-api-security-best-practices.md) | OWASP API Top 10, BOLA/BFLA, mass assignment, SSRF, helmet | 12 min |

---

[← Back to Security](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| CSRF | `apps/api/src/shared/common/interceptors/csrf.interceptor.ts` - double-submit cookie/header pair compared timing-safe |
| XSS / security headers | `apps/api/src/main.ts` - helmet() sets CSP and hardening headers on both deployables |
| SQL injection | `apps/api/src/shared/common/utils/postgres-advisory-lock.ts` - even raw SQL goes through parameterized `$queryRaw` tagged templates |
| BOLA / IDOR defense | `apps/api/src/shared/common/extensions/tenant.extension.ts` - auto-injects clinicId scoping on every query |
| Audit trail (API Top 10) | `apps/api/src/shared/common/interceptors/patient-audit.interceptor.ts` - PHI access auditing on patient reads |
---

[← Previous: ../01 Auth/index](../01-auth/INDEX.md) · [Next: ../03 Hardening And Operations/index →](../03-hardening-and-operations/INDEX.md)
