# Site Deployment — build gate now, publishing on your setup

> **TL;DR:** The Jekyll build runs in CI on every docs push and asserts the
> private lanes never enter `_site/`. The deploy step is written but
> self-disarmed: it activates only when you finish the ~10-minute Cloudflare
> setup in §2. Until then nothing is published anywhere.

|  |  |
| -------------- | --------------------------------------------------------------------- |
| **Status** | Build gate live · deploy armed-off · domain pending §2 |
| **Build job** | `deploy-site.yml` → `bundle exec jekyll build` + exclusion assertions |
| **Deploy job** | `cloudflare/wrangler-action@v3`, skipped until vars/secrets exist |

## 1. What already runs (no action needed)

Every push touching `**.md`, `_config.yml`, `search.html`, `api/**`, or this
workflow triggers:

1. `bundle exec jekyll build --trace` against the locked `Gemfile` — the only
   executable Jekyll-render gate this repo has (local Ruby lacks the
   `nokogiri` native gem; see `docs/verification-gates.md`).
2. **Publish-safety assertions** on the built output:

   ```bash
   test -z "$(find _site -path '*personal*' -print -quit)"
   test ! -e _site/80-lanes-abroad-full-stack/personal
   test ! -e _site/81-lanes-indian-sde-faang/personal
   test -s _site/index.html && test -s _site/search.html
   ```

   The `personal/` tree (CV, applications tracker, outreach playbook) and the
   entire `81-lanes-indian-sde-faang/` tree are excluded from the build via
   `exclude:` in `_config.yml`. The assertions fail the build if that ever
   stops being true. Generated artifacts (`search.html`, `api/index.json`)
   were audited: zero personal strings, zero lane chapters.

## 2. One-time Cloudflare setup (~10 minutes)

Cloudflare Pages serves static sites free from a private repo via direct
upload, which is exactly what `wrangler pages deploy` does.

1. **Create the Pages project** — Cloudflare dashboard → *Workers & Pages* →
   *Create* → *Pages* → *Direct Upload* → name it exactly `bible` (must match
   `wrangler.toml` and the workflow's `--project-name`). You can upload any
   dummy file to finish the wizard; the first CI deploy replaces it.
2. **Create an API token** — dashboard → *My Profile* → *API Tokens* →
   *Create Token* → use the **"Cloudflare Pages — Edit"** template (scopes the
   token to Pages edits only).
3. **Get your Account ID** — dashboard right sidebar on any domain's overview
   page (or run `npx wrangler whoami` after `npx wrangler login`).
4. **Feed GitHub Actions** — repo → *Settings* → *Secrets and variables* →
   *Actions*:
   - Repository **secret** `CF_API_TOKEN` ← step 2
   - Repository **secret** `CF_ACCOUNT_ID` ← step 3
   - Repository **variable** `DEPLOY_SITE_ENABLED` = `true`
5. **Trigger the deploy** — *Actions* → `deploy-site` → *Run workflow* on
   `main` (or push any `.md` change).
6. **Verify** — when the job goes green, the Pages project shows a
   `bible.pages.dev` URL:

   ```bash
   curl -sI https://bible.pages.dev | head -1   # expect: HTTP/2 200
   ```

7. **Attach the custom domain** — Pages project → *Custom domains* → set up
   `study.buildora.work`. If `buildora.work` is a zone in the same Cloudflare
   account, the CNAME is added for you; otherwise add this record at your DNS
   provider:

   ```text
   CNAME  study  →  bible.pages.dev
   ```

8. **De-aspirationalize the config** — once step 6 returns 200, remove the
   TODO comment above `url:` in `_config.yml` so the config states fact
   instead of intent.

## 3. Conventions

- **Never publish `personal/`.** The `exclude:` entries in `_config.yml` and
  the CI assertions are the mechanism; do not "clean up" either.
- **The deploy guard is the variable**, not code edits. To pause publishing
  temporarily, set `DEPLOY_SITE_ENABLED` to anything other than `true` — the
  build gate keeps running, the deploy job skips.
- **Local preview** parity with CI is unavailable on this machine (native-gem
  build failure); the CI build job is the render gate of record.
- Rollbacks are a dashboard action: Pages project → *Deployments* → select a
  prior deployment → *Rollback*.

## See Also

- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [GitHub Actions builds (official guide)](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/)
- [Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [wrangler-action](https://github.com/cloudflare/wrangler-action)
- [wrangler pages deploy](https://developers.cloudflare.com/workers/wrangler/commands/#pages-deploy)
