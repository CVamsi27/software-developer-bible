{% raw %}
# Site Deployment — Cloudflare Pages builds straight from git

> Cloudflare Pages is connected to this repo and builds +
> publishes on every push to `main`. GitHub Actions runs only the
> render/safety gate (`site-build.yml`); there is no deploy job, no API
> token, and no secret to rotate.

The production host is private by design. Cloudflare Pages Functions run the
access gate before a static file can be served: Google OAuth is brokered by
Supabase Auth, and only the case-insensitive address `cvamsik99@gmail.com`
(including German/EU `@googlemail.com` aliases) receives a short-lived
`HttpOnly` session cookie. An unauthenticated visitor sees `/auth/login.html`;
a signed-in visitor with a different address is sent to
`https://personal.buildora.work/?study=access-denied` (with stale/invalid cookies
purged so the browser never enters an access-denied redirect loop). The gate is
server-side, so copying a static file URL does not bypass it.

|  |  |
| --------------- | --------------------------------------------------------------------- |
| **Status** | Git integration (Connect to Git) · production branch `main` |
| **Pages build** | `bundle exec jekyll build` → `_site` (Ruby 3.1 via `.ruby-version`) |
| **CI gate** | `site-build.yml` → same render + lane-exclusion assertions |

## 1. How publishing works

Every push to `main` triggers two builds of the same command:

1. **Cloudflare Pages** — pulls git, runs `bundle exec jekyll build`,
   publishes `_site/` to the production domain `study.buildora.work`
   (`software-developer-bible.pages.dev` stays live as the fallback and
   verification URL). Other branches get preview deployments built the
   same way.
2. **GitHub Actions (`site-build`)** — the safety gate Pages lacks. It
   renders with the locked `Gemfile`, then asserts:

   ```bash
   test -z "$(find _site -path '*personal*' -print -quit)"
   test ! -e _site/80-lanes-abroad-full-stack/personal
   test ! -e _site/81-lanes-indian-sde-faang/personal
   test -s _site/index.html && test -s _site/search.html
   # plus: fails on any Liquid warning (a literal {{ }} that collided and
   # would otherwise render as empty text and ship silently)
   grep -E "Liquid (Warning|Exception)" /tmp/jekyll-build.log && exit 1 || true
   ```

   The `personal/` tree (CV, applications tracker, outreach playbook) and
   the entire `81-lanes-indian-sde-faang/` tree are excluded from every
   build via `exclude:` in `_config.yml` — Pages honors it exactly as CI
   does (same config, same command), and the gate fails if that ever stops
   being true. Generated artifacts (`search.html`, `api/index.json`) were
   audited: zero personal strings, zero lane chapters.

   If the gate goes red beside a green Pages build, that deployment is live
   without its guards — treat it as suspect: fix forward or roll back from
   the dashboard (Pages project → *Deployments* → select a prior
   deployment → *Rollback*), then re-push.

## 2. One-time Cloudflare setup (~10 minutes)

> One-way door: a Git-integrated Pages project cannot be switched back to
> Direct Upload later. (Automatic deployments can still be paused via
> branch control in §4.)

1. **Connect the repo** — Cloudflare dashboard → *Workers & Pages* →
   *Create* → *Pages* → *Connect to Git* → select
   `CVamsi27/software-developer-bible` → name the project exactly
   `software-developer-bible`
   (must match `wrangler.toml` for manual CLI use). It must be a **Pages**
   project: a Worker project (Workers Builds) shows a *Deploy command*
   field — typically prefilled with `npx wrangler deploy` — and does not match this repo's Pages Functions deployment contract. If you see that field, stop and check the project identity. Create the intended Pages project; remove a mistaken Worker only after confirming it serves no needed traffic.
2. **Build settings** — framework preset `Jekyll`, then override:
   | Setting | Value |
   | ------------------------- | ---------------------------- |
   | Build command | `bundle exec jekyll build` |
   | Build output directory | `_site` |
   | Production branch | `main` |
   (The preset's bare `jekyll build` skips bundler; the override builds
   against the locked `Gemfile`.)
3. **Environment** — Pages project → *Settings* → *Environment variables*:
   `JEKYLL_ENV=production`. Ruby needs no variable: the `.ruby-version`
   file (`3.1`) in the repo root pins the build image — the locked
   `liquid 4.0.3` calls `Object#tainted?`, removed in Ruby 3.2, so the
   default 3.4.x image crashes every render. (If the image ever rejects
   the file, set `RUBY_VERSION=3.1` here instead.) Add these **production**
   variables for the Pages Functions auth gate: `SUPABASE_URL` and either
   `SUPABASE_ANON_KEY` or `SUPABASE_JWKS_URL`. They are read at request time
   and are intentionally not committed. With asymmetric Supabase signing,
   `SUPABASE_JWKS_URL` is automatically derived from `SUPABASE_URL` as
   `${SUPABASE_URL}/auth/v1/.well-known/jwks.json` if omitted; Study verifies
   the access token locally with ES256/RS256 asymmetric cryptographic checks
   and dual-strategy verification (falling back from `/auth/v1/user` to JWKS).
   The implementation also accepts the personal app's public aliases
   (`NEXT_PUBLIC_SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY`). If the project
   uses symmetric signing, provide the publishable/anon key instead of JWKS.
   In Supabase Auth → URL Configuration, allow the exact
   redirect URL `https://study.buildora.work/auth/callback.html` (and the
   Pages preview callback URL when testing a preview deployment). The page
   itself lives in `functions/_middleware.ts` and nowhere else: the adapter
   answers the callback directly because Pages canonicalizes a `.html` asset
   request with a 308 (`/auth/login.html` → `/auth/login`), which is where the
   callback's `#access_token` fragment was lost. Do not add a second copy as
   an asset or a route — each would be shadowed by the intercept and drift.
   **Optional, and the only way to cover the success path:** add
   `STUDY_PROBE_TOKEN` (generate with `openssl rand -hex 32`) as a
   **production** variable here, and the same value as a **repository secret**
   of the same name (GitHub → Settings → Secrets and variables → Actions),
   which is what `study-live.yml` passes to the probe. This token is a bearer credential with chapter-read access, not a harmless health-check flag; keep it secret and rotate both configured copies together. A request whose session
   cookie carries it is treated as the approved account, so the live probe can
   fetch one real chapter per stack and assert each answers 200 with its own
   title, instead of only proving the site is *blocked*. Leave it unset and the
   branch is inert: the probe reports a warning, not a failure, and the manual
   checklist in §3 is the only proof of the signed-in path.
4. **No GitHub token needed** — jekyll-github-metadata has no disable
   flag, so `_config.yml` neutralizes it by construction instead: `github:`
   is an Array (never merged into an API-backed drop) and
   url/title/description/baseurl are all set explicitly (so the plugin
   installs zero lazy Values). The Pages build therefore makes no GitHub
   API calls — no token, no `PAGES_REPO_NWO`. (The old failure mode was an
   unset `baseurl`: the plugin installed a lazy baseurl Value whose render
   died with "No repo name found", because in production builds the git
   remote is never consulted. See §4.)
5. **Remove the old Direct Upload wiring** — repo → *Settings* → *Secrets
   and variables* → *Actions*: delete secrets `CF_API_TOKEN` and
   `CF_ACCOUNT_ID` plus variable `DEPLOY_SITE_ENABLED` (the `deploy` job
   that consumed them is gone with `deploy-site.yml`).
6. **Verify** — push any `.md` change, then:

   ```bash
   curl -sI https://software-developer-bible.pages.dev | head -1   # expect: HTTP/2 308
   ```

7. **Attach the production domain** — Pages project → *Custom domains* →
   set up `study.buildora.work`. This is the production URL; the
   `.pages.dev` hostname is not an access path: the root Pages middleware
   redirects `software-developer-bible.pages.dev` to the canonical study
   host before auth/static handling. Also configure the account-level Pages
   redirect described below so the platform fallback cannot be used as a
   second public entry point. (The `CNAME` file in the repo root is a GitHub
   Pages leftover and does nothing here; the dashboard record is what serves
   the domain.) If `buildora.work` is a
   zone in the same Cloudflare account, the record is added for you;
   otherwise add this record at your DNS provider:

   ```text
   CNAME  study  →  software-developer-bible.pages.dev
   ```

   Then:

   ```bash
   curl -sI https://study.buildora.work | head -1   # expect: HTTP/2 302 to /auth/login.html
   ```

   In Cloudflare Pages, add a redirect from the production
   `software-developer-bible.pages.dev` hostname to
   `https://study.buildora.work` using the Pages custom-domain redirect flow
   (or an account-level Bulk Redirect). Verify the fallback returns a 308/301
   with no chapter content, while the canonical host returns the sign-in flow.

## 3. Private entry-flow verification

The pure policy gate runs in CI and locally:

```bash
node --test functions/_lib/study-access.test.mjs
node --experimental-strip-types --test functions/_middleware.test.mjs
```

The first is the policy (who may read, and under what session); the second is
the Pages adapter that turns that policy into a Response — URL parse, cookie
read, `next()` hand-off. The adapter had no coverage anywhere until it did: it
was exercised only by requests to production, where a broken `Location` header
looks exactly like a working one from the dashboard.

### Machine-checked contract

Everything below except the signed-in steps is probed automatically:

```bash
python3 scripts/check_study_live.py --verbose   # exits 1 on a contract violation
```

`study-live.yml` runs the offline half (`test_study_live.py`, which drives the
real CLI against stub hosts and pins every exit code) on any change to its own
inputs, and the live probe on anything that changes what production should serve
(the corpus, `_config.yml`, `api/**`, the edge) as well as weekly on Mondays and
on manual *Run workflow*.

The probe used to be scheduled-only, because Pages builds from git in parallel
with this repo's CI and a push-time probe would measure the *previous* build.
That safety cost a week of detection latency, so the probe waits instead: with
`--await-fresh` it polls the deployed corpus digest until the deploy lands
(bounded, then it judges). Waiting is what makes the push trigger safe — without
it the probe would fail on a deployment that is merely in flight. Only one state
is waited for, because only one is a build in flight: a **valid digest from an
older build**. A body that is not the dump at all (`/api/index.json` answering
an HTML page, or JSON with no `corpus_digest` field) is misconfiguration, cannot
be waited out, and fails on the first read naming that cause instead of blaming
an old commit — so the run cannot stall for its whole budget before reporting a
state the first read already settled. The wait is also cheap when nothing has
changed: the digest covers content files, so a push touching only `scripts/` or
`docs/` matches immediately and does not poll. Scheduled runs can start hours
late (GitHub queues them; this repo's `job-board-watch` has fired as late as
11:19 for an 06:00 cron), so the push trigger is the fast path and Monday is the
backstop.


The probe list is not repeated here: each probe in
`scripts/check_study_live.py` owns the expectation it enforces, and
`--print-contract` renders the whole set — a copy in this runbook could only
drift from it.

Warnings never change the exit code: they describe environment state (unset
Supabase variables, a dead denial host) that only an operator can change —
including when that host does not answer at all. A zero exit with warnings proves only the paths actually exercised; unconfigured or unprobed paths remain unverified. Failures mean the live host
contradicts the checked contract.

**The signed-in path** is probed only when `STUDY_PROBE_TOKEN` is set (see
§2 step 3): the probe then fetches one real chapter per top-level stack with
that credential and asserts each response is 200 *and* contains that chapter's
own title — the two halves that no amount of policy testing can join, because
the middleware letting a valid session through and the edge serving that file
are different machines. One chapter per stack exists because each stack is its
own render class; a marker is a full plain-prose run from the chapter's title,
never a single word, because "Testing" or "WebSockets" appears in the
navigation of every page in its section and would make the assertion vacuous.
It also checks that no two chapters return identical bodies, which catches an
edge serving one cached response for every path, and that the deployed
`api/index.json` carries the same `corpus_digest` as this checkout — the one
check that separates "the site is up" from "the site is this commit". That
distinction is not academic: on 2026-09-22 production served a bundle a commit
behind HEAD for fifteen hours while every gate was green, because a stale
deployment is still a *working* site. It needs the credential, since
`/api/index.json` sits behind the gate.

Without the credential the probe says so in a warning, and only the policy
suite (`node --test`, 27 cases) plus the artifact assertions in
`site-build.yml` stand behind that path.

Either way, verify by hand in a private window after any auth change — it is
the only check that also exercises Google's consent screen and the callback:

1. `https://study.buildora.work/` opens the Google sign-in screen rather than
   returning a chapter file.
2. The approved account returns to the requested path after consent.
3. A different Google account is redirected to Personal Buildora.
4. Opening a deep link while signed out still lands on login and returns to
   that deep link after a successful session.

The current scope is an open-app/browser session. There is no background push
delivery, refresh-token store, or binary upload in this site.

## 4. Conventions

- **Never publish `personal/`.** The `exclude:` entries in `_config.yml`
  and the CI assertions are the mechanism; do not "clean up" either.
- **The pause switch is branch control**, not a repo variable. To pause
  publishing temporarily: Pages project → *Settings* → *Builds* → *Branch
  control* → turn off automatic production-branch deployments. The CI gate
  keeps running; re-enable to resume.
- **Local preview:** use the locked bundle and Ruby version to build with `JEKYLL_ENV=production bundle exec jekyll build`. A historical native-gem failure does not establish that preview is unavailable now. Serve the output on loopback and run the [rendered-page checks](scripts-map.md#rendered-page-checks). On case-insensitive filesystems, the authored homepage needs the documented temporary preview alias because `INDEX.html` and `index.html` collide. Local rendering does not prove edge auth or a deployed release.
- Rollbacks are a dashboard action: Pages project → *Deployments* → select a
  prior deployment → *Rollback*.

## 5. Troubleshooting

**`Missing entry-point to Worker script` after `npx wrangler deploy`, or
a *Deploy command* field in the project settings.** The repo was connected
as a *Worker* (Workers Builds) instead of a *Pages* project, and Workers
have no `_site` to serve. Fix: delete the Worker project and redo §2 with
*Pages* → *Connect to Git* — never set a deploy command to
`npx wrangler deploy` on this repo.

**`No repo name found` from GitHub Metadata during the Pages build.**
jekyll-github-metadata installed a lazy Value (historically: the unset
`baseurl`) whose render needs the GitHub API — and production builds never
consult the git remote, so without `PAGES_REPO_NWO` the render dies. Fixed
in-repo: `_config.yml` sets `baseurl: ""` plus url/title/description
explicitly and keeps `github:` an Array, so the plugin installs zero lazy
Values and makes zero API calls. If this error ever returns, that
short-circuit regressed — do not "fix" it with a token; restore the
`_config.yml` shape documented there.

**Pages build fails on Ruby or gems.** Check the build log's Ruby line: it
must read 3.1.x. The pin is the `.ruby-version` file; if the image ignores
it, set `RUBY_VERSION=3.1` under *Settings* → *Environment variables*. Do
not "fix" it by upgrading `liquid` — the version is locked by the
`github-pages` gem.

**Pages is green but CI (`site-build`) is red.** The deployment is live
without its safety guards (lane exclusion, Liquid warnings) — treat as
suspect, fix forward or *Rollback* per §4, then re-push.

**`check_study_live.py` reports `FAIL canonical` — `.pages.dev` serves the
site instead of redirecting to the study host.** The live Functions bundle is
older than the commit that added the host check, or the account-level
redirect from §2.7 was never created. Re-run the Pages build first (dashboard
→ *Deployments* → *Retry deployment*); if the fallback still answers 302 to
its own login, add the redirect. This is hygiene, not a leak: the fallback is
gated by the same Functions bundle.

**`check_study_live.py` warns `sign-in is NOT configured` and `/auth/start`
returns 503.** The Supabase variables are unset in production — §2.3. The
login page still renders, which is exactly why this is worth a probe: the
site looks deployed while nobody can sign in.

**A deploy looks correct but the live site behaves like an older commit.**
Check the Pages deployment list against the pushed commit SHA. When the
static build succeeds but the Functions bundle fails to compile, Pages can
publish new assets beside the previously deployed Functions — so a stale gate
and a fresh site appear together. Re-run the deployment; if it fails again,
the build log names the offending file under `functions/`.

## See Also

- [Cloudflare Pages](https://developers.cloudflare.com/pages/) — official platform documentation covering edge delivery, preview builds, and static hosting
- [Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/) — webhook triggers and automated branch deployments from GitHub repositories
- [Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/) — build commands, output directories, and environment variables for the Jekyll pipeline
- [Build image (language versions)](https://developers.cloudflare.com/pages/configuration/build-image/) — Ruby and Node runtime pins for reproducible build environments
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/) — apex domain mapping, CNAME records, and automated edge SSL certificate provisioning
{% endraw %}
