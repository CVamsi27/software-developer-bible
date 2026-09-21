{% raw %}
# Site Deployment — Cloudflare Pages builds straight from git

> **TL;DR:** Cloudflare Pages is connected to this repo and builds +
> publishes on every push to `main`. GitHub Actions runs only the
> render/safety gate (`site-build.yml`); there is no deploy job, no API
> token, and no secret to rotate.

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
> branch control in §3.)

1. **Connect the repo** — Cloudflare dashboard → *Workers & Pages* →
   *Create* → *Pages* → *Connect to Git* → select
   `CVamsi27/software-developer-bible` → name the project exactly
   `software-developer-bible`
   (must match `wrangler.toml` for manual CLI use). It must be a **Pages**
   project: a Worker project (Workers Builds) shows a *Deploy command*
   field — typically prefilled with `npx wrangler deploy` — and can never
   serve this site. If you see that field, delete the project and restart
   this step.
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
   the file, set `RUBY_VERSION=3.1` here instead.)
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
   curl -sI https://software-developer-bible.pages.dev | head -1   # expect: HTTP/2 200
   ```

7. **Attach the production domain** — Pages project → *Custom domains* →
   set up `study.buildora.work`. This is the production URL; the
   `.pages.dev` hostname is only the fallback. (The `CNAME` file in the
   repo root is a GitHub Pages leftover and does nothing here; the
   dashboard record is what serves the domain.) If `buildora.work` is a
   zone in the same Cloudflare account, the record is added for you;
   otherwise add this record at your DNS provider:

   ```text
   CNAME  study  →  software-developer-bible.pages.dev
   ```

   Then:

   ```bash
   curl -sI https://study.buildora.work | head -1   # expect: HTTP/2 200
   ```

## 3. Conventions

- **Never publish `personal/`.** The `exclude:` entries in `_config.yml`
  and the CI assertions are the mechanism; do not "clean up" either.
- **The pause switch is branch control**, not a repo variable. To pause
  publishing temporarily: Pages project → *Settings* → *Builds* → *Branch
  control* → turn off automatic production-branch deployments. The CI gate
  keeps running; re-enable to resume.
- **Local preview** parity with CI is unavailable on this machine (native-gem
  build failure); the CI gate plus Pages preview URLs are the render gates
  of record.
- Rollbacks are a dashboard action: Pages project → *Deployments* → select a
  prior deployment → *Rollback*.

## 4. Troubleshooting

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
suspect, fix forward or *Rollback* per §3, then re-push.

## See Also

- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)
- [Build image (language versions)](https://developers.cloudflare.com/pages/configuration/build-image/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
{% endraw %}
