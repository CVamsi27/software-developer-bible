<!-- section: Security | category: Reference | tags: revision| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
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

**Q:** What core constraint explains why data and code share a channel. governs xss (cross-site scripting)?

**A:** HTML mixes both by design; when untrusted input re-enters the page as markup, the browser *must* execute it — it cannot know your intent. Every XSS is this boundary crossed: input → stored/transmitted → rendered as code.

**Q:** What core constraint explains why context determines escaping, so one escape function is never enough. governs xss (cross-site scripting)?

**A:** HTML body, attribute, JS string, URL, CSS each have different dangerous characters — the senior insight is *context-aware output encoding* and letting frameworks auto-escape (React), escaping only the gaps.

**Q:** What core constraint explains why csp is the seatbelt for when the boundary fails. governs xss (cross-site scripting)?

**A:** It cannot fix injection; it limits what injected code *reaches* (no inline, script allowlists) — defense in depth, not primary control. HttpOnly cookies cap the blast radius (token theft) the same way.

## CSRF (Cross-Site Request Forgery)

Source: [CSRF (Cross-Site Request Forgery)](20.5.2.02-csrf.md)

**Q:** What core constraint explains why the browser attaches cookies automatically. governs csrf (cross-site request forgery)?

**A:** evil.com's form POSTing to your-bank.com rides the user's session — the server sees a perfectly authenticated request it never should have honored. The vulnerability is *ambient authority*: who-sent-this is unproven.

**Q:** What core constraint explains why samesite cookies restore origin-awareness. governs csrf (cross-site request forgery)?

**A:** Lax/Strict simply stop sending cookies on cross-site posts — one line, closes most of the attack; the residuals (top-level GET navigations, old browsers) are why tokens still matter.

**Q:** What core constraint explains why anti-csrf tokens prove intent governs csrf (cross-site request forgery)?

**A:** the attacker cannot read your page's token (SOP, → 20.5.2.01), so requiring a random per-session value restores "the user's page initiated this." Origin/Referer checking is the same proof, cheaper. Defense is layered because the vulnerability is structural.

## SQL Injection

Source: [SQL Injection](20.5.2.03-sql-injection.md)

**Q:** What core constraint explains why string-concatenated queries make user input executable. governs sql injection?

**A:** The query planner receives `... WHERE name = '' OR '1'='1'` as *SQL* — it cannot distinguish your intent from attacker syntax. This is structural, not sloppiness: interpolation *is* the vulnerability.

**Q:** What core constraint explains why parameterized queries fix it by construction. governs sql injection?

**A:** Values travel as typed parameters the parser never reinterprets — data cannot become code. This is why "use prepared statements" is not one mitigation among many but *the* fix; escaping is the fallback for the few places parameters can't reach (identifiers, ORDER BY direction — validate against allowlists).

**Q:** What core constraint explains why the blast radius is capped by privilege design. governs sql injection?

**A:** An injected statement executes with the app's DB user's powers — least privilege, no superuser, RLS  mean even a successful injection hits a walled garden.

## API Security Best Practices & OWASP API Top 10

Source: [API Security Best Practices & OWASP API Top 10](20.5.2.04-api-security-best-practices.md)

**Q:** What core constraint explains why every request is untrusted input plus a claim. governs api security best practices & owasp api top 10?

**A:** AuthN  establishes the claim; authZ  checks it against the resource; input validation assumes the payload is hostile. An API that skips any one layer trusts something it shouldn't.

**Q:** What core constraint explains why fail predictably and leak nothing. governs api security best practices & owasp api top 10?

**A:** Error responses are attacker reconnaissance — uniform error shapes, no stack traces, rate limiting to slow enumeration, logging with correlation IDs for forensics. Security logging exists because attacks are campaigns, not single requests.

**Q:** What core constraint explains why the perimeter is the api itself. governs api security best practices & owasp api top 10?

**A:** There is no "internal" network to trust (zero trust) — every caller authenticates, every input validates, every response minimizes (over-fetching leaks data by volume).

## Summary

Use these prompts after the reading pass to recall the attacks and defense mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
