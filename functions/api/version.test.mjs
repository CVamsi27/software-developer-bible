import test from "node:test";
import assert from "node:assert/strict";
import * as versionModule from "./version.ts";
import { onRequestGet as version } from "./version.ts";

/**
 * The version route, offline.
 *
 * The live probe's freshness verdict has exactly one input — the commit this
 * route publishes — so a drift here silently re-points every "is production
 * this commit?" answer. Two states matter: a platform-injected commit is
 * served verbatim and uncached, and a runtime without one (local
 * `wrangler pages dev`) serves an empty identity rather than a guess, which
 * the probe classifies as misconfiguration instead of a deploy in flight.
 *
 * Run with type stripping:
 *
 *     node --experimental-strip-types --test functions/api/version.test.mjs
 */

test("the route exports no mutating handler", () => {
  // Pages answers every other method with 405, and the probe relies on GET.
  // Adding an onRequestPost here would change what production does with a
  // POST, so the absence is asserted rather than assumed.
  assert.equal(typeof version, "function");
  assert.equal("onRequestPost" in versionModule, false);
});

test("the deployment's commit is served verbatim, uncached", async () => {
  const response = await version({ env: { CF_PAGES_COMMIT_SHA: "0123456789abcdef" } });
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { commit: "0123456789abcdef" });
  assert.match(response.headers.get("Content-Type") ?? "", /^application\/json/);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
});

test("a runtime without the platform commit serves an empty identity, never a guess", async () => {
  const response = await version({ env: {} });
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { commit: "" });
});
