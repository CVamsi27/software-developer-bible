<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
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

**Q:** How does least privilege reduce the impact of a SQL injection flaw?

**A:** An injected statement runs with the database role's authority. Restrict role permissions and data reach, but do not treat RLS or low privilege as a replacement for removing the injection flaw.

## API Security Best Practices & OWASP API Top 10

Source: [API Security Best Practices & OWASP API Top 10](20.5.2.04-api-security-best-practices.md)

**Q:** Which identity, input and access claims must an API validate?

**A:** Verify credential evidence, authorize the specific object and operation, and validate expected payload fields. Mass assignment, tenant scope and response-property access need explicit checks too.

**Q:** How can an API return useful errors without exposing sensitive details?

**A:** Use documented safe errors and correlation identifiers, retaining stack traces and sensitive diagnostics in protected logs. Keep behavior useful without allowing account or object enumeration through inconsistent responses.

**Q:** Why do APIs need object and operation checks even behind a trusted network boundary?

**A:** Compromised internal workloads and routing mistakes can cross a perimeter. Enforce identity and resource-specific policy at the application boundary, with trusted service context rather than network location alone.

## Trace the boundary that changed

Source: [XSS](20.5.2.01-xss.md), [CSRF](20.5.2.02-csrf.md), [SQL injection](20.5.2.03-sql-injection.md), [API security](20.5.2.04-api-security-best-practices.md).

**Q:** Can HTML text escaping make an attacker-controlled `javascript:` link safe?

**A:** No. URL scheme validation is a separate policy; prefer a safe text sink for plain content and validated destinations for links.

**Q:** Why does a signed double-submit token include the current session identifier in its MAC?

**A:** An attacker may inject a cookie/token pair they obtained for their own session. Session binding prevents that pair from verifying for the victim's session.

**Q:** Does parameterizing a search term make `%` a literal character in `LIKE`?

**A:** No. Binding separates SQL syntax from data, while `LIKE` still interprets pattern characters inside the value. Escape pattern characters when the feature promises a literal substring search.

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
