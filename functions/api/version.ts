import type { StudyEnv } from "../_lib/env.ts";

/**
 * The deployment's own commit, published for the live probe.
 *
 * Every other fact this site serves sits behind the gate, `/api/index.json`
 * included, which made "is production this commit?" a question only a
 * credential could ask: with no `STUDY_PROBE_TOKEN` configured, the CI probe
 * could not read the digest and warned instead of judging, so a deployment
 * lagging HEAD stayed invisible (2026-09-22: fifteen hours of it).
 *
 * The commit SHA is safe to publish because it decides nothing: the repository
 * is public, so the SHA reveals nothing a reader of the repo does not already
 * know, and it separates "the site is up" from "the site is this commit" for a
 * probe holding no session. Cloudflare Pages injects `CF_PAGES_COMMIT_SHA`
 * into every Functions runtime; `scripts/check_study_live.py` compares it with
 * the checkout it built from. The public-path declaration lives once, in
 * `_lib/study-access.mjs`, and the probe resolves it from there.
 *
 * No-store: a cached copy would let a stale deployment answer as a current one,
 * which is the one distinction this endpoint exists to make.
 */
export const onRequestGet = async ({ env }: { env: StudyEnv }) => {
  return new Response(JSON.stringify({ commit: env.CF_PAGES_COMMIT_SHA ?? "" }), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
};
