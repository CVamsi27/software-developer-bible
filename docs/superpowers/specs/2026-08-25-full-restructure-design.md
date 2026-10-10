# Design - Bible Restructure: Unified Numbering, Category Subfolders, Full Topic Coverage

> **Historical design record:** requirements, example paths and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md) and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; TL;DR and inline chapter cheat/revision sections are retired.

Date: 2026-08-25
Status: Approved (user approved all sections including design-patterns scheme conversion)
Scope: Everything at once - structure, numbering, auth completion, and ~80 new chapters across all stacks.

---

## 1. Problem statement

1. **Numbering gaps everywhere**: `20.5-security` starts at `.03` (gaps .01-.02, .07-.08), `20.4-database` (.16/.21), `20.8-caching` (.02/.04/.05), `30.3-infra-patterns` (.08-.10/.12), `70.1-behavioral` (starts at .03). The entire `auth/` subfolder is unnumbered.
2. **Subfolders missing**: only design-patterns and system-design have category subfolders; ~19 larger flat stacks do not.
3. **Incomplete topics**: e.g., the auth track lacks Basic/Digest Auth, API Keys, MFA/Passkeys, and a dedicated SSO/SAML stage (ref: "7 Authentication Concepts Every Developer Should Know", Hayk Simonyan). Similar verified gaps exist across all stacks.

## 2. Unified convention (single source of truth)

| Level | Pattern | Example |
| ---------------- | --------------------------------------------------------------------- | ------------------------------------------ |
| Stack | `NN.N-slug/` | `20.5-security/` |
| Category folder | `NN-slug/` (2-digit study order) | `01-auth/`, `03-hardening-and-operations/` |
| File in category | `stack.cat.seq-slug.md`, seq contiguous from 01 | `20.5.1.01-auth-fundamentals.md` |
| Flat-stack file | `stack.seq-slug.md`, seq contiguous from 01, interview-questions LAST | `40.1.10-interview-questions.md` |

- `cat` segment in filenames = folder number without leading zero (folder `02-attacks-and-defense/` holds files `20.5.2.xx-*`).
- Interview-questions files always sort last within their scope.
- `AGENTS.md` and `contributing.md` updated to document exactly this convention (replacing the old concatenated design-patterns rule).
- Root `INDEX.md` / `README.md` / `ROADMAP.md` counts refreshed at the end.

## 3. Structural moves (per stack)

Legend: `slug -> NewID-seq` inside each target category. Existing files keep their slugs unless noted. NEW = new chapter (see sections 4-5).

### 10.1-javascript -> 6 categories
- `01-execution-and-scope/`: execution-context->10.1.1.01, call-stack->.02, hoisting->.03, closures->.04, scope->.05, lexical-environment->.06
- `02-objects-prototypes-this/`: this->10.1.2.01, prototypes->.02, proxy-reflect->.03
- `03-async-concurrency/`: event-loop->10.1.3.01, promises->.02, async-await->.03, error-handling->.04
- `04-memory-and-data/`: pass-by-value->10.1.4.01, map-set-weakmap-weakset->.02, shallow-vs-deep-copy->.03, debounce->.04, throttle->.05, memory-leaks->.06, garbage-collection->.07
- `05-functional-patterns/`: modules->10.1.5.01, memoization->.02, generators->.03, currying-composition->.04, recursion-tail-call->.05
- `06-modern-and-interview/`: es2024-features->10.1.6.01, web-workers->.02, dom-events-delegation(NEW)->.03, cross-tab-communication(NEW)->.04, interview-questions->.05

### 10.2-typescript -> 5 categories
- `01-foundations/`: types-vs-interfaces->10.2.1.01, keyof-typeof->.02, type-narrowing->.03, tsconfig-compiler-options(NEW)->.04
- `02-generics-and-inference/`: generics->10.2.2.01, infer->.02, advanced-generics->.03, type-variance(NEW)->.04
- `03-type-transformations/`: utility-types->10.2.3.01, conditional-types->.02, mapped-types->.03, template-literal-types->.04
- `04-advanced-patterns/`: satisfies-operator->10.2.4.01, branded-types->.02, decorators->.03, declaration-files->.04, advanced-patterns->.05
- `05-interview-prep/`: interview-questions->10.2.5.01

### 10.3-react -> 5 categories
- `01-react-internals/`: virtual-dom->10.3.1.01, fiber->.02, reconciliation->.03, rendering->.04, lifecycle->.05
- `02-core-hooks/`: usestate->10.3.2.01, useeffect->.02, usememo-usecallback->.03, useref->.04, context-api->.05
- `03-advanced-hooks-and-patterns/`: suspense->10.3.3.01, error-boundary->.02, custom-hooks->.03, usesyncexternalstore(NEW)->.04, performance->.05, state-management->.06
- `04-modern-react/`: modern-hooks-react18-19->10.3.4.01, web-components->.02, react-router(NEW)->.03
- `05-patterns-and-interview/`: portals->10.3.5.01, compound-components->.02, interview-questions->.03

### 10.4-next.js -> 5 categories
- `01-rendering-fundamentals/`: ssr-csr-ssg-isr->10.4.1.01, app-router->.02, server-components->.03, client-components->.04
- `02-routing-and-middleware/`: middleware->10.4.2.01, route-handlers->.02, metadata->.03
- `03-data-and-caching/`: data-fetching-patterns->10.4.3.01, server-actions->.02, caching->.03, streaming->.04, incremental-static-regeneration->.05, static-exports->.06
- `04-production/`: authentication->10.4.4.01, image-optimization->.02, deploying-nextjs(NEW)->.03
- `05-interview-prep/`: interview-questions->10.4.5.01

### 10.5-form-handling - stays flat + 1 NEW
react-hook-form->10.5.01, zod->.02, formik->.03, tanstack-form->.04, server-actions-and-form-patterns->.05, autosave-draft-recovery(NEW)->.06, interview-questions->.07

### 10.6-animation - stays flat + 1 NEW
css-animations->10.6.01, framer-motion->.02, gsap->.03, react-spring->.04, web-animations-api->.05, view-transitions-and-scroll-driven-animations->.06, canvas-svg-animation(NEW)->.07, interview-questions->.08

### 10.7-html-css - stays flat + 2 NEW
html-fundamentals->10.7.01, css-fundamentals->.02, browser-rendering->.03, seo->.04, pwa->.05, css-architecture-styling-approaches(NEW)->.06, theming-design-tokens(NEW)->.07

### 10.8-mobile - stays flat + 2 NEW
react-native-cross-platform->10.8.01, deep-linking-universal-links(NEW)->10.8.02, testing-react-native-apps(NEW)->10.8.03

### 20.1-node.js -> 4 categories
- `01-runtime-and-async/`: event-loop->20.1.1.01, web-streams-and-test-runner->.02
- `02-io-and-data/`: streams->20.1.2.01, buffers->.02, file-system->.03, http-module->.04
- `03-processes-and-concurrency/`: clustering->20.1.3.01, child-processes-workers->.02, process-environment->.03
- `04-security-and-operations/`: node-security->20.1.4.01, debugging-profiling-nodejs(NEW)->.02, express-fastify-internals(NEW)->.03, interview-questions->.04

### 20.2-nestjs -> 5 categories
- `01-core-architecture/`: modules->20.2.1.01, controllers->.02, providers->.03, dependency-injection->.04
- `02-request-lifecycle/`: middleware->20.2.2.01, guards->.02, pipes->.03, interceptors->.04, exception-filters->.05
- `03-patterns/`: cqrs->20.2.3.01, microservices->.02
- `04-quality-and-operations/`: configuration-validation->20.2.4.01, testing->.02, lifecycle-hooks-graceful-shutdown(NEW)->.03, scheduling-background-jobs(NEW)->.04, swagger-openapi-nestjs(NEW)->.05
- `05-advanced-and-interview/`: custom-decorators->20.2.5.01, interview-questions->.02

### 20.3-rest-apis -> 5 categories
- `01-design-and-contract/`: api-design-patterns->20.3.1.01, rest-principles->.02, versioning->.03, rest-maturity-model->.04, openapi-swagger->.05
- `02-http-mechanics/`: http-methods->20.3.2.01, status-codes->.02, cors->.03, http-caching->.04
- `03-payloads-errors-integration/`: pagination->20.3.3.01, error-handling-design->.02, long-running-api-operations(NEW)->.03, file-upload-apis(NEW)->.04, webhooks->.05
- `04-edge-and-scale/`: rate-limiting->20.3.4.01, api-gateway->.02, bff->.03, authentication->.04
- `05-interview-drills/`: interview-questions->20.3.5.01

### 20.4-database -> 5 categories
- `01-postgresql-foundations/`: postgresql->20.4.1.01, normalization->.02, mvcc->.03, nosql-vs-sql->.04, postgresql-performance->.05
- `02-querying-and-optimization/`: indexes->20.4.2.01, joins->.02, execution-plans->.03, window-functions->.04, jsonb->.05
- `03-transactions-and-replication/`: transactions->20.4.3.01, deadlocks->.02, optimistic-pessimistic-locking->.03, database-replication->.04
- `04-orm-and-access/`: prisma->20.4.4.01, prisma-advanced->.02, orm-query-builder-landscape(NEW)->.03
- `05-operations-and-scaling/`: connection-pooling->20.4.5.01, migration-strategies->.02, soft-delete-and-tombstones->.03, backups-pitr-recovery(NEW)->.04, search-infrastructure-at-scale(NEW)->.05, interview-questions->.06

### 20.5-security -> 4 categories (auth/ renamed to 01-auth/, files numbered)
- `01-auth/`: auth-fundamentals->20.5.1.01, http-basic-digest-auth(NEW)->.02, api-keys(NEW)->.03, sessions-cookies->.04, jwt->.05, oauth2-oidc->.06, sso-saml-federation(NEW)->.07, mfa-passkeys-webauthn(NEW)->.08, rbac-abac->.09, interview-questions->.10
- `02-attacks-and-defense/`: xss->20.5.2.01, csrf->.02, sql-injection->.03, api-security-best-practices->.04
- `03-hardening-and-operations/`: encryption->20.5.3.01, web-security->.02, threat-modeling-stride->.03, secrets-management->.04, vulnerability-management-patch-governance(NEW)->.05
- `04-interview-drills/`: interview-questions->20.5.4.01

oauth2-oidc.md gets slimmed: SSO/SAML/passkey content moves to new chapters 07/08 with links left behind.

### 20.6-microservices -> 5 categories
- `01-service-topology/`: service-discovery->20.6.1.01, api-gateway->.02, service-mesh->.03, strangler-fig->.04
- `02-communication-and-messaging/`: grpc->20.6.2.01, grpc-streaming->.02, kafka->.03, rabbitmq->.04, message-brokers->.05, event-driven-architecture->.06
- `03-data-and-consistency/`: saga-pattern->20.6.3.01, distributed-transactions->.02, event-sourcing->.03, cqrs->.04, decomposing-monolith-database(NEW)->.05
- `04-resilience/`: circuit-breaker->20.6.4.01, bulkhead-pattern->.02
- `05-interview-drills/`: interview-questions->20.6.5.01

### 20.7-graphql -> 4 categories
- `01-fundamentals/`: graphql-overview->20.7.1.01, schema-design->.02, queries-mutations->.03
- `02-execution/`: resolvers->20.7.2.01, apollo-server->.02
- `03-clients-and-production/`: apollo-client->20.7.3.01, performance-security->.02, codegen-schema-safety-ci(NEW)->.03
- `04-interview-prep/`: interview-questions->20.7.4.01

### 20.8-caching - stays flat, compacted
caching-deep-dive->20.8.01, redis-fundamentals->.02, advanced-redis-patterns->.03

### 20.12-ai-engineering - stays flat + 3 NEW
llm-app-architecture->20.12.01, prompts-context-evals->.02, retrieval-quality-hybrid-search-reranking(NEW)->.03, agent-orchestration-patterns(NEW)->.04, serving-models-hosted-vs-self-hosted(NEW)->.05, safety-cost-governance->.06, interview-questions->.07

### 30.1-design-patterns - converted to unified dotted scheme
Folders renamed: `30.1.0-foundations`->`01-foundations`, `30.1.1-creational`->`02-creational`, `30.1.2-structural`->`03-structural`, `30.1.3-behavioral`->`04-behavioral`, `30.1.4-architectural`->`05-architectural`, `30.1.5-interview-prep`->`06-interview-prep`.
- foundations: solid-principles->30.1.1.01, dry-kiss-yagni->.02, oop-concepts->.03, uml-basics->.04
- creational: singleton->30.1.2.01, factory-method->.02, builder->.03, abstract-factory->.04, prototype->.05
- structural: adapter->30.1.3.01, facade->.02, decorator->.03, proxy->.04, module-pattern->.05, composite->.06, bridge->.07, flyweight->.08
- behavioral: strategy->30.1.4.01, observer->.02, chain-of-responsibility->.03, state->.04, template-method->.05, iterator->.06, mediator->.07, memento->.08, command->.09, visitor->.10, interpreter->.11, null-object(NEW)->.12
- architectural: repository->30.1.5.01, cqrs-di->.02, event-sourcing->.03, saga->.04, ddd-tactical-patterns-aggregates-value-objects(NEW)->.05, anti-corruption-layer(NEW)->.06, service-locator-vs-dependency-injection(NEW)->.07, presentation-patterns-mvc-mvp-mvvm(NEW)->.08
- interview-prep: interview-questions->30.1.6.01

### 30.2-system-design - folders renamed to match convention
`00-theory`->`01-theory`, `10-case-studies`->`02-case-studies`. Files already conform (`30.2.1.xx`, `30.2.2.xx`) - unchanged.
NEW case studies (append in 02-case-studies): typeahead-autocomplete->30.2.2.23, metrics-monitoring-pipeline->.24, distributed-job-scheduler->.25, distributed-id-generator->.26, ad-click-aggregator->.27

### 30.3-infra-patterns -> 5 categories (compacted)
- `01-liveness-lifecycle/`: health-checks-graceful-shutdown->30.3.1.01
- `02-failure-and-recovery/`: resilience-patterns->30.3.2.01, retry-patterns->.02, idempotency-keys->.03, feature-flags-kill-switches(NEW)->.04, backup-strategy-restore-drills(NEW)->.05
- `03-coordination/`: leader-election-consensus->30.3.3.01
- `04-data-at-scale/`: database-scaling->30.3.4.01, data-pipelines->.02, cdn-architecture->.03
- `05-shipping-and-evolution/`: zero-downtime-deployments->30.3.5.01, technical-debt->.02, cost-engineering-finops(NEW)->.03, data-retention-archival(NEW)->.04

Dedup rules: PostgreSQL backup mechanics (WAL, pgBackRest, PITR how-to) live in 20.4.5.04; operational drill cadence/game-days live here. 50.4 does NOT get its own DR chapter (cross-links instead).

### 40.1-docker - flat + 3 NEW (compacted, IQ last)
images-containers->40.1.01, volumes-networks->.02, compose->.03, multi-stage-builds->.04, dockerfile-best-practices->.05, production-patterns->.06, container-runtime-internals-namespaces-cgroups(NEW)->.07, image-signing-sbom-supply-chain(NEW)->.08, rootless-sandboxed-runtimes(NEW)->.09, interview-questions->.10

### 40.2-kubernetes -> 6 categories
- `01-core-workloads/`: pods-replicasets->40.2.1.01, deployments->.02, statefulsets-daemonsets->.03, jobs-cronjobs->.04
- `02-networking-and-config/`: services-ingress->40.2.2.01, configmaps-secrets->.02, podpresets->.03
- `03-scaling/`: hpa-scaling->40.2.3.01, node-autoscaling-cluster-capacity(NEW)->.02
- `04-production-hardening/`: health-checks->40.2.4.01, pod-disruption-budgets->.02, rbac-network-policies->.03, resource-quotas->.04
- `05-packaging-and-extensibility/`: helm->40.2.5.01, kustomize-overlays-packaging-tradeoffs(NEW)->.02, crds-operators-controller-patterns(NEW)->.03
- `06-interview-prep/`: interview-questions->40.2.6.01

### 40.3-ci-cd -> 4 categories (+ delete stray `.DS_Store`)
- `01-ci-platforms/`: github-actions->40.3.1.01, gitlab-ci->.02, jenkins->.03, argocd->.04
- `02-build-and-deploy/`: docker-build-deploy->40.3.2.01, pipeline-patterns->.02, artifact-registries-release-promotion(NEW)->.03, pipeline-supply-chain-security-slsa(NEW)->.04
- `03-releases-and-metrics/`: blue-green-canary->40.3.3.01, dora-metrics-delivery-performance(NEW)->.02
- `04-interview-prep/`: interview-questions->40.3.4.01

### 40.4-observability -> 5 categories
- `01-pillars/`: logging->40.4.1.01, monitoring->.02, tracing->.03
- `02-errors-and-health/`: error-tracking->40.4.2.01, health-checks->.02
- `03-sre-targets/`: sli-slo-sla->40.4.3.01, alerting->.02
- `04-advanced-telemetry/`: opentelemetry->40.4.4.01, continuous-profiling(NEW)->.02, ebpf-observability(NEW)->.03
- `05-interview-prep/`: interview-questions->40.4.5.01

### 40.5-build-tools -> 4 categories
- `01-bundlers/`: webpack->40.5.1.01, vite->.02, turbopack->.03, rspack->.04
- `02-compilers/`: babel->40.5.2.01, esbuild-swc->.02
- `03-optimization-and-comparison/`: build-optimization->40.5.3.01, asset-pipelines-css-images-fonts(NEW)->.02, build-tool-comparison->.03
- `04-interview-prep/`: interview-questions->40.5.4.01

### 40.6-git-advanced - flat + 3 NEW (compacted, IQ last)
git-internals-objects-refs-packfiles(NEW)->40.6.01, branching-strategies->.02, rebase-cherry-pick->.03, git-hooks->.04, git-advanced-commands->.05, patch-and-bundle->.06, code-archaeology->.07, git-at-scale-lfs-partial-clones(NEW)->.08, signed-commits-repository-security(NEW)->.09, interview-questions->.10

### 40.7-serverless-edge - flat + 1 NEW (IQ last)
serverless-overview->40.7.01, aws-lambda->.02, vercel-deployments->.03, edge-functions->.04, serverless-patterns->.05, serverless-frameworks->.06, durable-execution-temporal-inngest(NEW)->.07, interview-questions->.08

### 40.8-monorepo - flat + 1 NEW (IQ last)
monorepo-overview->40.8.01, turborepo->.02, nx->.03, monorepo-tools->.04, versioning-publishing-strategies(NEW)->.05, interview-questions->.06

### 40.9-twelve-factor - unchanged (single-chapter by design)

### 40.10-cdn - flat + 2 NEW
cdn-architecture->40.10.01, multi-cdn-traffic-steering(NEW)->.02, media-optimization-at-the-edge(NEW)->.03

### 50.1-testing -> 6 categories
- `01-foundations/`: testing-overview->50.1.1.01, test-data-management-anonymization(NEW)->.02
- `02-frameworks/`: jest->50.1.2.01, vitest->.02, react-testing-library->.03, testing-frameworks-comparison->.04
- `03-test-levels/`: unit-testing->50.1.3.01, integration-testing->.02, e2e-testing->.03
- `04-mocking-and-patterns/`: mocking->50.1.4.01, test-patterns->.02
- `05-advanced/`: performance-load-testing->50.1.5.01, chaos-engineering->.02
- `06-interview-prep/`: interview-questions->50.1.6.01

### 50.2-accessibility - flat + 2 NEW (IQ last)
wcag-overview->50.2.01, aria->.02, keyboard-navigation->.03, color-and-contrast->.04, forms-and-labels->.05, accessible-charts-data-viz(NEW)->.06, accessibility-design-systems(NEW)->.07, testing-a11y->.08, interview-questions->.09

### 50.3-performance-monitoring -> 4 categories
- `01-core-metrics/`: core-web-vitals->50.3.1.01
- `02-measurement/`: performance-apis->50.3.2.01, profiling-tools->.02, lighthouse-ci->.03, real-user-monitoring->.04, http2-http3-performance-effects(NEW)->.05
- `03-optimization-and-governance/`: bundle-analysis->50.3.3.01, performance-budgets->.02
- `04-interview-prep/`: interview-questions->50.3.4.01

### 50.4-production-engineering - flat + 2 NEW
incident-response->50.4.01, sli-slo-error-budgets->.02, chaos-engineering->.03, production-readiness-reviews(NEW)->.04, on-call-without-burnout(NEW)->.05

### 60.1-websockets -> 4 categories
- `01-transports/`: websockets-overview->60.1.1.01, server-sent-events->.02, socket-io->.03, webtransport->.04
- `02-architecture-and-scaling/`: real-time-architecture->60.1.2.01, scaling-patterns->.02
- `03-frameworks-and-paradigms/`: nestjs-websockets->60.1.3.01, graphql-subscriptions-live-queries(NEW)->.02, webrtc-peer-to-peer(NEW)->.03, testing-realtime-systems(NEW)->.04
- `04-interview-prep/`: interview-questions->60.1.4.01

### 70.1-behavioral - flat, compacted from 01 (INDEX notes STAR basics live in 00-strategy)
stakeholder-management-stories(NEW)->70.1.01, leadership-questions->.02, judgment-calls-ambiguity(NEW)->.03, system-design-behavioral->.04, behavioral-anti-patterns-checklist(NEW)->.05

### 70.2-coding-patterns -> 4 categories
- `01-linear-structures/`: sliding-window->70.2.1.01, two-pointers->.02, binary-search->.03, linked-list-manipulation-patterns(NEW)->.04, intervals->.05, greedy-prefix-sum->.06, string-search-kmp-rabin-karp->.07
- `02-graphs-trees-grids/`: dfs-bfs->70.2.2.01, shortest-paths-dijkstra-bellman-ford(NEW)->.02, union-find->.03, topological-sort->.04, trie->.05, matrix-traversal-simulation(NEW)->.06
- `03-recursion-and-optimization/`: backtracking->70.2.3.01, dynamic-programming->.02, bit-manipulation->.03
- `04-heaps-stacks-selection/`: heap->70.2.4.01, monotonic-stack->.02, stack-queue-patterns->.03, segment-tree->.04, quick-select-reservoir-sampling->.05

### 70.3-cheatsheets - flat + 2 NEW
javascript-cheat-sheet->70.3.01, typescript-cheat-sheet->.02, react-nextjs-cheat-sheet->.03, backend-cheat-sheet->.04, system-design-cheat-sheet->.05, docker-kubernetes-cicd-cheat-sheet(NEW)->.06, sql-data-modeling-cheat-sheet(NEW)->.07

Unchanged: `00-strategy/`, `80-lanes-abroad-full-stack/`, `81-lanes-indian-sde-faang/`, `lanes/`, root docs.

## 4. Auth completion spec (video parity)

Ref: https://www.youtube.com/watch?v=iX8g4LqF8p8 (Hayk Simonyan - Basic, Digest, API Keys, Sessions, Bearer/JWT + access/refresh, OAuth2, OIDC, SSO, SAML, Authorization).

New chapters in `20.5-security/01-auth/`:
1. **20.5.1.02-http-basic-digest-auth.md** - Authorization header mechanics, Base64 credentials over TLS, `WWW-Authenticate`/401 handshake, Digest challenge-response (MD5 legacy, why it died), browser/curl examples, when Basic is still OK (internal tools, machine endpoints), comparison table vs all other methods.
2. **20.5.1.03-api-keys.md** - key generation with CSPRNG, hashing keys at rest, prefix schemes (`sk_live_`), rotation & revocation, per-key scopes, rate-limit binding, leak response runbook, vs OAuth client-credentials decision table.
3. **20.5.1.07-sso-saml-federation.md** - extracted from oauth2-oidc.md: SAML 2.0 flows (SP-initiated / IdP-initiated), assertions/signing/cert exchange, SAML vs OIDC table, enterprise SSO + SCIM provisioning, JIT provisioning.
4. **20.5.1.08-mfa-passkeys-webauthn.md** - TOTP/HOTP mechanics, SMS weakness, WebAuthn registration/authentication ceremonies, passkey sync, assurance levels (AAL), account recovery as weakest link.

Plus edits: oauth2-oidc.md slimmed (grants/PKCE/OIDC remain; SSO/SAML/passkeys replaced by links to 07/08); auth INDEX rebuilt as a 10-stage flow; security stack INDEX updated; security interview bank cross-links fixed; REST authentication chapter cross-linked.

## 5. New chapters by wave (83 total - authoritative source: NEW markers in section 3)

Every chapter follows contributing.md template: TL;DR -> Definition -> Why -> How -> Code -> Real-world -> Mistakes -> Best practices -> Summary -> Cheat sheet -> See Also -> References. No emojis. Badges per contributing.md. Each new file also gets a category INDEX row and stack INDEX row.

**Wave A - Frontend (13):** dom-events-delegation, cross-tab-communication, tsconfig-compiler-options, type-variance, usesyncexternalstore, react-router, deploying-nextjs, autosave-draft-recovery, canvas-svg-animation, css-architecture-styling-approaches, theming-design-tokens, deep-linking-universal-links, testing-react-native-apps

**Wave B - Backend (20):** debugging-profiling-nodejs, express-fastify-internals, lifecycle-hooks-graceful-shutdown, scheduling-background-jobs, swagger-openapi-nestjs, long-running-api-operations, file-upload-apis, orm-query-builder-landscape, backups-pitr-recovery, search-infrastructure-at-scale, http-basic-digest-auth, api-keys, sso-saml-federation, mfa-passkeys-webauthn, vulnerability-management-patch-governance, decomposing-monolith-database, codegen-schema-safety-ci, retrieval-quality-hybrid-search-reranking, agent-orchestration-patterns, serving-models-hosted-vs-self-hosted

**Wave C - Architecture (14):** null-object, ddd-tactical-patterns-aggregates-value-objects, anti-corruption-layer, service-locator-vs-dependency-injection, presentation-patterns-mvc-mvp-mvvm, typeahead-autocomplete, metrics-monitoring-pipeline, distributed-job-scheduler, distributed-id-generator, ad-click-aggregator, feature-flags-kill-switches, backup-strategy-restore-drills, cost-engineering-finops, data-retention-archival

**Wave D - Platform (19):** container-runtime-internals-namespaces-cgroups, image-signing-sbom-supply-chain, rootless-sandboxed-runtimes, node-autoscaling-cluster-capacity, kustomize-overlays-packaging-tradeoffs, crds-operators-controller-patterns, artifact-registries-release-promotion, pipeline-supply-chain-security-slsa, dora-metrics-delivery-performance, continuous-profiling, ebpf-observability, asset-pipelines-css-images-fonts, git-internals-objects-refs-packfiles, git-at-scale-lfs-partial-clones, signed-commits-repository-security, durable-execution-temporal-inngest, versioning-publishing-strategies, multi-cdn-traffic-steering, media-optimization-at-the-edge

**Wave E - Quality/Realtime/Toolkit (17):** test-data-management-anonymization, accessible-charts-data-viz, accessibility-design-systems, http2-http3-performance-effects, production-readiness-reviews, on-call-without-burnout, graphql-subscriptions-live-queries, webrtc-peer-to-peer, testing-realtime-systems, stakeholder-management-stories, judgment-calls-ambiguity, behavioral-anti-patterns-checklist, shortest-paths-dijkstra-bellman-ford, linked-list-manipulation-patterns, matrix-traversal-simulation, docker-kubernetes-cicd-cheat-sheet, sql-data-modeling-cheat-sheet

Total new chapters: 13 (A) + 20 (B) + 14 (C) + 19 (D) + 17 (E) = **83**. Section 3's NEW markers enumerate the identical set with final file IDs.

## 6. INDEX updates

Every affected stack INDEX rebuilt: badges (file counts), category tables, study-flow ASCII diagrams, per-file topic rows, suggested paths, cross-references, navigation footers. Category-level INDEX.md created for each new subfolder (like design-patterns has). Root `INDEX.md`, `README.md`, `ROADMAP.md`, `contributing.md`, `AGENTS.md` updated last.

## 7. Link integrity & verification

- After each move batch: repo-wide grep sweep for old paths; rewrite all references.
- Repo link check (per contributing.md) after every phase commit.
- Final verification script: zero broken relative links between md files, zero duplicate file IDs, contiguous sequences per folder, badge counts == actual counts.

## 8. Execution order (each numbered step = one commit)

1. This spec.
2. Phase 1 - Structural moves + compaction + renames (all stacks), link repair, category INDEXes, stack INDEX rebuilds, AGENTS/contributing convention update.
3. Phase 2 - Auth completion (section 4) + security INDEX refresh.
4. Phases 3-7 - Content Waves A-E via parallel authoring agents; after each wave: link check + INDEX counts + commit.
5. Phase 8 - Root docs (README/INDEX/ROADMAP/contributing/AGENTS) final counts + full link check + final commit.

## 9. Out of scope / constraints

- No changes inside `80-lanes-abroad-full-stack/personal/` content (symlinks respected).
- No commits or pushes anywhere outside this repo; never touch `~/repos/career-ops`.
- No emojis anywhere (repo style).
- Keep every existing chapter's substance; moves are moves, not rewrites.
