<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Attacks And Defense Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## XSS (Cross-Site Scripting)

Source: [XSS (Cross-Site Scripting)](20.5.2.01-xss.md)

**Q:** How does attacker-controlled data become executable browser content?

**A:** An unsafe rendering or execution sink interprets untrusted content as code in the page's security context. Not every piece of inserted markup executes script; the dangerous context and browser behavior determine the exploit.

**Q:** Why must output protection depend on the HTML, URL or script context?

**A:** HTML text, attributes, URLs and JavaScript have different syntax rules. Prefer safe framework rendering and APIs; validate URL schemes and avoid script construction rather than assuming one escaping function covers everything.

**Q:** What protection can CSP add when an unsafe execution sink remains?

**A:** A restrictive policy can block classes of script execution and resource loading, but cannot repair every unsafe sink. HttpOnly protects direct cookie reads; it does not stop injected code from issuing authenticated requests.

**Q:** When should a strict CSP authorize scripts with a nonce versus a hash?

**A:** A nonce should be unpredictable and generated for each response, then added only to trusted script elements. A hash authorizes exact script content and changes when that content changes; it can fit static output more easily. Caching and template delivery must preserve the chosen contract.

Source: [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html) · [MDN CSP guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)

**Q:** What does Trusted Types enforce, and what responsibility remains with the application?

**A:** With enforcement enabled in a supporting browser, covered DOM injection sinks reject ordinary strings unless a configured policy provides trusted values. The policy must perform a safe transformation such as sanitization; Trusted Types do not make an unsafe policy safe or replace output protection elsewhere.

Source: [MDN Trusted Types API](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API)

## CSRF (Cross-Site Request Forgery)

Source: [CSRF (Cross-Site Request Forgery)](20.5.2.02-csrf.md)

**Q:** How can automatic browser credentials enable an unwanted cross-site request?

**A:** A malicious page can trigger a request to a target site while the browser attaches eligible credentials. The target must verify more than the presence of a valid session.

**Q:** What does SameSite restrict, and why is it not a complete CSRF policy?

**A:** SameSite restricts cookies according to site relationships and request conditions, not exact origin equality. Top-level navigations, unsafe GET handlers and same-site sibling origins require separate consideration.

**Q:** How does a validated anti-CSRF token help distinguish an authorized request?

**A:** Validate an unpredictable token bound to the session or signed double-submit contract. Origin checks can complement it; neither proves user intent after XSS compromises a trusted origin.

**Q:** Does a CSRF attacker need to steal the victim's cookie or read the response?

**A:** No. A browser can carry eligible credentials on the forged request even when the attacker cannot read the cookie or response. Session hijacking and CSRF are distinct paths; authentication checks alone do not distinguish a legitimate mutation from the forged one.

## SQL Injection

Source: [SQL Injection](20.5.2.03-sql-injection.md)

**Q:** Why can concatenating untrusted input change a SQL statement's meaning?

**A:** The SQL parser receives the assembled statement as executable syntax. Untrusted fragments can change predicates or add operations before the database knows which parts were intended as data.

**Q:** How does parameter binding separate values from SQL syntax?

**A:** Bind untrusted values rather than concatenate them into the statement. Parameters generally do not stand for identifiers or keywords; construct those from validated allowlists.

**Q:** What should a query do when a user can select its sort column or direction?

**A:** Keep the SQL grammar in application code and map each public choice to a fixed identifier or keyword. A placeholder binds values, not identifiers, and quoting a valid identifier does not authorize its use.

Source: [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) · [Prisma ORM v6 raw queries](https://www.prisma.io/docs/orm/v6/prisma-client/using-raw-sql/raw-queries)

**Q:** How does least privilege reduce the impact of a SQL injection flaw?

**A:** An injected statement runs with the database role's authority. Restrict role permissions and data reach, but do not treat RLS or low privilege as a replacement for removing the injection flaw.

## API Security Best Practices & OWASP API Top 10

Source: [API Security Best Practices & OWASP API Top 10](20.5.2.04-api-security-best-practices.md)

**Q:** Which identity, input and access claims must an API validate?

**A:** Verify the credential, then authorize the principal for this operation and object using trusted tenant and state context. Independently allowlist writable fields and project only readable response properties. A valid identity is not permission to every row or field.

Source: [OWASP API1 — Broken Object Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/) · [OWASP API3 — Broken Object Property Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/)

**Q:** Why should a tenant-scoped read include the tenant in its data-access predicate?

**A:** The tenant identifier from a route or header is only a request value. Verify current membership, then constrain the resource lookup by the verified tenant and its access policy; a guessed identifier must not widen the query.

Source: [OWASP API1 — Broken Object Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)

**Q:** Why are request-rate limits insufficient as the only resource budget?

**A:** A permitted request can still contain too many records, trigger an expensive query, run too long, fan out concurrently or incur a paid downstream call. Bound the cost dimensions at their respective boundaries and test them separately.

Source: [OWASP API4 — Unrestricted Resource Consumption](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/)

**Q:** How does abuse of a sensitive business flow differ from resource exhaustion?

**A:** Resource exhaustion consumes infrastructure or paid capacity; business-flow abuse follows valid operations in a way that harms domain outcomes, such as reserving all inventory. Apply domain quotas, state transitions and idempotency in addition to technical budgets.

Source: [OWASP API6 — Unrestricted Access to Sensitive Business Flows](https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)

**Q:** How can an API return useful errors without exposing sensitive details?

**A:** Use documented safe errors and correlation identifiers, retaining stack traces and sensitive diagnostics in protected logs. Keep behavior useful without allowing account or object enumeration through inconsistent responses.

**Q:** Why do APIs need object and operation checks even behind a trusted network boundary?

**A:** Network placement can reduce exposure but does not establish which workload or user sent a request, nor which record it may change. Authenticate the caller and apply resource-specific policy at the service that owns the operation.

**Q:** Why does an outbound host allowlist need connection-time and redirect controls?

**A:** DNS can resolve differently between validation and connection, and a permitted host can redirect the client elsewhere. Enforce destination policy through the actual connector for each hop, disable redirects or revalidate them, and restrict network egress.

Source: [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

**Q:** What must an API do before trusting a response from a third-party service?

**A:** Use authenticated TLS, apply explicit time and size limits, validate the response schema, and constrain redirects and downstream effects. A reputable provider's data is still external input.

Source: [OWASP API10 — Unsafe Consumption of APIs](https://api-security.owasp.org/editions/2023/en/0xaa-unsafe-consumption-of-apis/)

**Q:** What information belongs in a client-facing problem response versus a diagnostic log?

**A:** Return stable, documented interface details that let the client respond; keep stack traces, query text, secrets and sensitive internal context in protected diagnostics. A problem-details format describes the HTTP interface and is not a debugging channel.

Source: [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)

## Trace the boundary that changed

Source: [XSS](20.5.2.01-xss.md), [CSRF](20.5.2.02-csrf.md), [SQL injection](20.5.2.03-sql-injection.md), [API security](20.5.2.04-api-security-best-practices.md).

**Q:** Can HTML text escaping make an attacker-controlled `javascript:` link safe?

**A:** No. URL scheme validation is a separate policy; prefer a safe text sink for plain content and validated destinations for links.

**Q:** Why does a signed double-submit token include the current session identifier in its MAC?

**A:** An attacker may inject a cookie/token pair they obtained for their own session. Session binding prevents that pair from verifying for the victim's session.

**Q:** Does parameterizing a search term make `%` a literal character in `LIKE`?

**A:** No. Binding separates SQL syntax from data, while `LIKE` still interprets pattern characters inside the value. Escape pattern characters when the feature promises a literal substring search.

Source: [PostgreSQL 18 pattern matching](https://www.postgresql.org/docs/18/functions-matching.html)

**Q:** Why does resolving an allowed hostname before `fetch` leave an SSRF gap?

**A:** The connection may use another DNS answer or follow a redirect. The actual connector and every redirect must obey destination policy.

**Q:** If a user can read an order, can the response include every stored order property?

**A:** No. Object access and property access are separate decisions. Project only fields authorized for that caller and operation.

## Summary

Use these prompts after the reading pass to recall the attacks and defense mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for attacker-controlled input and browser/server defenses

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
