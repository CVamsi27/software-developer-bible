# Density pass — 22 October 2026

Companion record for the paragraph-level readability pass. The outline repair of
21 October fixed navigation; this pass addressed the remaining wall paragraph.
Rules are now part of the [readability standard](readability-standard.md#4-density-rules-added-2026-10-22).

## Measured problem

A fence-aware recount over tracked content Markdown found that the corpus's
sentences were already tight but its paragraphs were not:

| Defect | Before | After |
| ------------------------------------ | -----: | ----: |
| Paragraphs over 90 words | 423 | 335 |
| Paragraphs with 3+ semicolons | 184 | 112 |
| Bold-label enumerations of 70+ words | 164 | 125 |
| Summaries over 100 words | 2 | 0 |
| Sentences over 45 words | 108 | 81 |

The first three classes overlapped: a single 200-word paragraph often fused a
definition, a pros/cons pair, and an implementation note, with semicolons doing
the work that paragraphs and bullets should do.

## Scope and transforms

Seventy-six files and 107 flagged sites were processed in six disjoint batches
(frontend, backend, platform, system-design theory, case studies/infrastructure,
and interview/quality/realtime). Three moves were permitted:

1. Split a long paragraph at its topic seam — definition to consequence,
   mechanism to example, claim to boundary — into 2–4 short paragraphs.
2. Put an existing bold label (`**Pros:**`, `**Use when:**`, `**Cost:**`,
   `**Implement with:**`) on its own paragraph instead of burying it mid-block.
3. Convert a parallel list of three or more semicolon-separated items into
   bullets. Two-item lists and flowing comparisons stayed in prose.

Representative result, from the architecture-patterns chapter:

> **Pros:** independent deploys ...; independent scaling ...; **Cons:**
> distributed-systems complexity ...

became a `**Pros:**` header with five bullets, a `**Cons:**` header with its own
bullets, and a separate `**Use when**` paragraph.

Sites that already read as one argument were left alone. One flagged site was
skipped: a 73-word adapter code walkthrough whose semicolons join two-clause
contrasts rather than a parallel list. The other 106 were transformed.

## Invariants and side effects

- Every content word was preserved. Normalized word sequences were compared
  against `HEAD` for all 76 files: 74 are identical, and the other two differ
  only by a promoted structural label, which the rules permit.
- No paragraph, heading, link, table, quote, or code block was reordered.
- Three headings gained missing sequence numbers (lexical environment,
  decorators, singleton), and two incoming anchors were updated to match:
  `REVISION.md` for decorators and `30.1.3.04-proxy.md` for singleton.
- The structural blank lines pushed the corpus from 152K to 153K lines, so the
  generated count claims in `INDEX.md`, `contributing.md`, and
  `docs/verification-gates.md` were restamped from disk, and the search index
  was regenerated.

## Verification and limits

`bash scripts/verify.sh` passes all 31 gates after the count and search-index
refresh. `check_links.py` reports 10,417 links and 177 anchors checked with zero
broken links; `check_readability.py` reports 529 chapters with no retired
heading and no mechanism step left under one.

The remaining 335 paragraphs over 90 words are not one backlog. Eighty-five sit
in interview banks, 24 in indexes, revision companions, and meta documents, and
226 in teaching chapters. Seventy of the teaching paragraphs are in files this
pass touched, but at sites the flagging rules did not select — usually a
90–110-word paragraph that develops one calculation or trace; the other 156 are
in chapters outside this batch. Those unflagged paragraphs are the next density
frontier, not evidence that the transforms failed: the rules deliberately
targeted 120+ word walls and fused labeled blocks, and a 90–110 word paragraph
that develops one idea was left intact.

## Editorial follow-up — 23 October 2026

The density pass fixed paragraph shape. This follow-up reviewed the prose in the
same cohorts for wording, explanation and context: fragments, unresolved
pronouns, unexpanded acronyms, vague cross-references and code/prose
disagreements. It is an editorial pass, not a second density rewrite.

### Scope

The review covered the frontend cohort; the theory chapters from caching and
consistency through failure modes, resilience and multi-region; the backend data
core (transactions, locking, replication, pooling, MVCC, row-level security,
indexes, migrations, backups, PostgreSQL performance and Prisma); the security
stack (authentication, sessions, JWT, OAuth/OIDC, web attacks, API security,
encryption, web hardening, threat modeling and secrets); and selected design
patterns, case studies and infrastructure chapters. The files changed by the
density pass and the chapters those edits exposed were the priority; this was
not a complete reread of all 529 chapters. After the cohort edits, a final diff
audit covered the remaining modified chapters in AI engineering, REST webhooks,
transactional outbox, caching, Kafka and event-driven patterns, infrastructure,
platform, quality, realtime and the interview banks; no further claim-changing
edits were required.

### Editorial changes

- **Terms and acronyms:** expanded on first use where the expansion explains the
  mechanism rather than decorating it. Examples include CSP, HSTS, CORS, TLS,
  MIME, DTD, SSRF, PCI, DEK, KMS, IDNA, SNI, ETag, CSRF, B2B, OIDC, RBAC and
  ABAC.
- **Sentences and paragraphs:** replaced fragments and dangling comparisons
  with complete claims, split sentences carrying two decisions, and removed
  duplicated phrasing without deleting caveats or failure cases.
- **Cross-references:** replaced vague See Also labels with the specific
  contribution of the linked chapter. The payment-gateway, web-crawler,
  live-betting and Instagram case studies were the clearest examples.
- **Explanation:** added a boundary sentence only where the chapter's own
  mechanism already supported it, such as why a fast hash is appropriate for a
  high-entropy API key, why a successful restore can undo a deletion, or why a
  cached nonce and header must remain coherent.

### Verified repairs

These were content inconsistencies found while editing, not stylistic
preferences:

- Replaced the malformed Basic/Digest handshake diagram with a readable
  client-server trace.
- Added the `approve` action to the RBAC example's action type and validation
  set so the chapter's own `invoice:approve` example type-checks.
- Made the ABAC guard fetch duty status only for doctors, matching the policy
  that already exempted admins from the on-duty requirement.
- Clarified the web-crawler URL identity helper's IDNA boundary and expanded
  SNI/ETag at first use.
- Expanded PCI and SSRF in the payment-gateway chapter instead of leaving
  compliance and webhook-security terms unexplained.
- Corrected the web-security See Also claim that every REST endpoint inherits
  browser headers and cookie rules; the requirement applies to browser-facing
  endpoints.
- Removed the dangling "Common Mistakes #4" pointer from the API-keys chapter
  and replaced it with the actual design rule.

### Invariants

Headings, anchors, code blocks, tables and link targets stayed stable except for
the verified repairs above. No version, date, number, URL, product behavior or
benchmark claim was added. Existing caveats, security warnings and version
constraints were preserved.

### Verification

Targeted gates passed after the edits:

- `python3 scripts/check_alignment.py` — 0 misaligned boxes or tables.
- `python3 scripts/check_links.py` — 10,425 links checked, 177 anchors verified,
  0 broken.
- `python3 scripts/check_readability.py` — 529 chapters, no retired heading.
- `python3 scripts/prose_hygiene.py` — 973 Markdown files, no findings.
- `python3 scripts/check_freshness.py` — clean across 955 files and 35 rules.

The full 31-gate `bash scripts/verify.sh` run passed after refreshing counts,
study times and the generated search index. It reports 973 files, 153K lines,
10,425 links and a fixed point across all ten writers. All changes from this
follow-up remain uncommitted.
