# Reading and senior interview quality review — 2026-10-07

> **Dated review record:** counts, test results, and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-25-fullstack-coverage-review.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

This pass preserves the practical introductions, adds original formal definitions, corrects misleading teaching claims, and repairs the shared reader. Paragraphs now fill the article width on desktop, while mobile gutters and local code and table scrolling remain responsive.

## Review coverage

The inventory enumerated 1,014 Markdown documents, including navigation, operational documentation, and private career material. Corpus-wide scans cover structure, links, prose conventions, metadata, stale signatures, and repeated content. Definition-bearing learning introductions received a topic-specific formal counterpart. Deep semantic verification focused on the mechanisms and examples identified below; this is not a claim that every sentence or code sample in the corpus was independently proofread or executed.

The enforced teaching scope contains 482 concept chapters, 32 case-study chapters, 40 interview banks, and 117 reference or revision documents. Every required concept `Definition` section has exactly one nonempty textbook definition outside code fences. Interview banks, revision companions, cheat sheets, and operational records keep their respective formats.

These definitions are original textbook-style explanations, not invented quotations attributed to books or standards. The existing practical explanation remains the entry point; only incorrect or misleading wording was changed.

| Area | Markdown documents outside personal data | Documents with a textbook definition |
| ---------------------------- | ---------------------------------------- | ------------------------------------ |
| `00-strategy` | 6 | 4 |
| `10-frontend` | 175 | 114 |
| `20-backend` | 223 | 135 |
| `30-architecture` | 139 | 106 |
| `40-platform` | 150 | 83 |
| `50-quality` | 63 | 34 |
| `60-realtime` | 20 | 10 |
| `70-interview-toolkit` | 50 | 27 |
| `80-lanes-abroad-full-stack` | 38 | 0 |
| `81-lanes-indian-sde-faang` | 25 | 12 |
| `projects` | 30 | 25 |

The count difference reflects genres: INDEX documents teach study order; revision companions and interview banks test knowledge; guides and historical records do not need a repeated formal definition. Architecture case studies receive a concise formal problem statement even when their template has no Definition heading.

## Reading and theme repairs

- Removed both prose width caps, which had left paragraphs about 814 pixels wide inside a 1,140-pixel article. Browser assertions now compare actual paragraph and article widths at desktop and wide desktop sizes.
- Prevented duplicate Copy buttons caused by processing both a code wrapper and its nested `<pre>` element.
- Overrode the theme's static light table-header and striped-row fills with theme-aware surfaces and borders. Table text, links, and hovered cells now retain readable contrast in dark mode, and visited links use the theme palette instead of Minima's static dark-blue color.
- Gave filled action controls a separate contrast-safe color rather than using the brighter dark-mode link color behind white text. Copy success and navigation hover states use readable fills too.
- Kept the theme toggle and browser theme color synchronized when the operating-system preference changes; a saved explicit preference still takes precedence.
- Kept theme switching functional when browser preference storage is unavailable.
- Hid an inferred theme title only when it duplicates the authored chapter title, and gave the root README an explicit rendered route. Navigation pages now have one visible title, and the README link resolves.
- Repaired blank-line boundaries before and after tables. Missing separation made roadmap tables and project-evidence tables render as wide paragraphs; the alignment fixer now handles that defect outside code fences.
- Separated the mobile theme and menu controls and gave both 44-pixel touch targets. The dropdown opens below them, leaving the theme control accessible. Navigation supports `Enter` and `Space`, `Escape` closes it and returns focus, and assistive technology receives the expanded state.

## Content and interview improvements

- **Frontend:** replaced unsupported animation popularity and performance guarantees; corrected GreenSock Animation Platform (GSAP) timeline positions, `CustomEase`, plugin registration, and ownership cleanup; and distinguished compositing opportunities from graphics processing unit (GPU) guarantees. Clarified React effect timing and ref ownership, corrected Expo build, distribution, and update boundaries, and repaired clipped cross-reference explanations.
- **Backend:** clarified normalization and multiversion concurrency control (MVCC) boundaries, authentication versus authorization, Digest algorithms and credential handling, signed versus encrypted JSON Web Tokens (JWTs), GraphQL mutation ordering, Kafka delivery limits, and outbox duplicates. Reworded malformed generated revision prompts while retaining their subject coverage. Subscription examples now use current built-in PubSub APIs, the documented WebSocket transport export, and server-side filtering rather than returning unauthorized payloads or nulls.
- **Architecture and platform:** corrected the Horizontal Pod Autoscaler (HPA) scaling ratio, Deployment progress-deadline behavior, Git reference and object storage descriptions, container isolation absolutes, Temporal replay and Activity examples, and provider-specific edge-runtime restrictions.
- **Quality and real-time systems:** distinguished Cumulative Layout Shift (CLS) session windows from lifetime sums, ranking signals from ranking guarantees, reusable accessibility primitives from whole-page conformance, scheduled k6 iterations from achieved request throughput, Socket.IO reconnection from replay, and Web Real-Time Communication (WebRTC) transport encryption from application-level end-to-end encryption. Removed unsourced testing-cost and Traversal Using Relays around NAT (TURN) rate figures.
- **Senior preparation:** added observable readiness criteria for mechanism, implementation, failure analysis, judgment, and ownership to the brush-up roadmap. Added changed-constraint exercises for frontend, backend, and full-stack roles, plus source-linked revision questions about lost acknowledgments, duplicate effects, and CLS windows. The rubric is a self-assessment tool, not an employer's scoring system.
- **Metadata:** restored clipped tag names from complete badges or the pre-truncation Git version. The gate rejects disagreement between the metadata comment and Tags badge, and search and API outputs are regenerated from that corrected source.

## Continued final pass

Read and consolidated the complete error-boundary, pagination, transactional-outbox, and distributed-transactions chapters; reviewed Node streams and advanced Redis; and corrected the Redis cross-reference about payment deduplication. The focused chapters build one mechanism and example before comparing recovery and consistency boundaries.

- React recovery distinguishes resetting a boundary from repairing a rejected external resource. The class handles unknown thrown values, retains neighboring UI, and explains the loss of child state on remount.
- Pagination traces tied timestamps with a unique tie-breaker, preserves timestamp and identifier precision, validates complete bounded inputs, and separates cursor integrity from authorization and snapshots.
- Distributed-transaction teaching distinguishes atomic commit from isolation, prepared-state recovery from a local timeout, and durable saga progress from an in-memory callback list. Its interview answer and broker, idempotency, and email cross-references follow the same contracts, and repeated outbox and relay snippets point to the canonical chapter.
- Outbox teaching makes only the business mutation and publication intent atomic. Relay acknowledgment, duplicate delivery, database-local effects, and external provider actions have explicit, separate recovery contracts. A cache marker around email sending is no longer presented as exactly-once processing.
- Revision companions add source-linked questions about those boundaries while retaining authored prompts. The Backend for Frontend (BFF) decision table has one header and accepts a serverless deployment when runtime and operating constraints fit.
- The main roadmap, homepage, lane selector, master-index entry, and Software Development Engineer (SDE) lane entry pages now choose work from the confirmed assessment. Removed unsupported interview percentages, pass guarantees, universal hiring rounds and salary bands, obsolete phase plans, and an unsupported AI experience story. Forms, HTML, CSS, and accessibility remain core frontend preparation.

The table repair was verified with planted heading and rule boundary defects, exact fixer output, and repeat-run idempotence; nested fenced examples remain untouched. A rendered-output scan found no remaining plain-paragraph table candidates across 930 HTML outputs in the preview, including its temporary homepage alias. A broader browser sweep covered 34 navigation, chapter, and large-content routes at 375 and 1,280 pixels in both themes, including opened mobile menus, with no overflow failures.

The authored pagination helpers ran against valid, absent, malformed, and excessive limits, plus empty, full, and look-ahead pages and lossless cursor keys. The authored React class ran in Chromium with React 19.2: `null` and string throws, persistent failures, neighboring interaction, and recovered child-state remount all passed.

SQLite mechanism fixtures confirmed tied-key traversal with tenant filtering, mutation and intent rollback, projection and marker rollback, and consumer-scoped duplicate suppression. These are focused mechanism checks; PostgreSQL query plans, Prisma models, and broker or provider integrations were not executed.

## Resume alignment

The canonical private generator now names supported ownership in API design, tenant isolation, background-job recovery, operational dashboards, and release checks. Study topics were not converted into experience claims or fabricated metrics, and the Docita walkthrough matches the current resume bullet count.

All current application, EU, and public variants were regenerated together through the existing resume-generator symlinks. Generator and cover-letter tests, claim checks, PDF text, order, and page checks, and the personal symlink doctor passed. All three PDFs were rendered and visually inspected as one-page A4 documents, while private resume data remains excluded from the public site.

## Verification record

- `bash scripts/verify.sh`: all repository checks passed, including the planted-defect self-test.
- `python3 scripts/test_gates.py`: 72/72 cases detect their defect and accept clean content.
- `python3 scripts/check_template.py`: 671 teaching documents pass; all 482 required concepts have their formal definition.
- `python3 scripts/check_links.py`: 9,424 links checked, 166 anchors verified, and zero broken links, stale labels, or stale inline paths. External citations are handled separately by the baseline and probe workflow.
- `read_time.py --write`, `check_counts.py --write`, alignment repair, and `gen_master_index.py`: study estimates, navigation counts, search, and the API catalog regenerated.
- Production Jekyll build: passed with no Liquid warnings; required reader assets exist, and private trees are absent from the output.
- Reading UI browser suite: passed on the rendered chapter, including desktop and wide-desktop widths, mobile overflow, outline destinations, one Copy control, theme changes, saved preferences, unavailable storage, and text, control, and syntax contrast.
- Navigation-page browser suite: passed route responses, one visible title, responsive layouts at 320, 375, 600, and 1,280 pixels, separate mobile touch targets, pointer and keyboard menus, expanded state and focus return, all homepage actions, table-header, cell, and link contrast, hovered-cell contrast, and actual clipboard text. The new header assertions failed before the spacing and keyboard repair and passed afterward.
- `python3 scripts/test_fixers.py`: 11/11 exact-output and idempotence cases passed.
- Read-aloud browser suite: passed on the rendered chapter, including extraction order, pause, resume, and stop controls, speed, follow position, departure cancellation, and unsupported-browser behavior. Its old fixture-only assumption about the second spoken block was corrected to permit the real Definition heading.
- Resume tests: seven generator and cover-letter tests and four claim tests passed. Each regenerated PDF passed one-page A4, searchable-text, and section-order checks; all three renders were inspected.
- Desktop and mobile screenshots in both themes and code-surface screenshots were inspected, and `git diff --check` passed.

Five freshness regression checks cover static `ScrollTrigger` cleanup, raw CSS easing supplied to GSAP, the obsolete built-in PubSub iterator method, the fabricated WebSocket transport import, and Temporal replay called on a live Worker instance. Their planted defects failed before the gate changes and are detected afterward; clean current examples and the third-party Redis adapter API remain accepted.

Eighteen new primary-source citation URLs were checked before refreshing the external-link baseline: sixteen returned HTTP 200 in the scripted probe, and two Socket.IO pages hit a local Transport Layer Security (TLS) probe error and were verified through the web reader. No newly added citation returned DEAD.

## Scope and use

Start with the role lane, use the brush-up roadmap to choose weak areas, and answer a revision question before reopening its source. For senior practice, change a constraint, trace a failure, defend the recovery choice, and connect the answer to an actual project decision. Reading alone does not demonstrate those skills; the linked practice routes make that evidence observable.

The macOS preview filesystem is case-insensitive, so `INDEX.html` and `index.html` collide locally. The authored homepage was rendered to a temporary `home-preview.html` alias for browser verification, while production routes remain unchanged. Existing build exclusions still omit personal data and the SDE lane tree; internal source-link checks cover that lane, and the rendered-route sweep covers emitted pages.

Historical application records remain historical, and this pass does not publish the site or submit a resume. The review above records automated coverage separately from targeted semantic verification, so future work can extend it without mistaking passing structural gates for proof of every technical claim.

## Preparation routes

- [Senior readiness and topic brush-up](../80-lanes-abroad-full-stack/80.29-topic-brushup-roadmap.md)
- [The Senior Engineer Roadmap](../ROADMAP.md)
- [Resume claim walkthrough](../projects/docita/24-resume-claim-walkthrough.md)
- [Implementation plan](superpowers/plans/2026-10-07-reading-and-interview-quality.md)
