import test from "node:test";
import assert from "node:assert/strict";
import { onRequest } from "./_middleware.ts";

/**
 * The Cloudflare Pages adapter, as the edge calls it.
 *
 * `functions/_lib/study-access.mjs` holds the policy and has its own suite; this
 * file covers the glue around it — the URL parse, the cookie read, the
 * `next()` hand-off, and the Response mapping. That glue had no coverage in
 * this repository at all: a typo in it was invisible until a request hit the
 * deployed edge, because the only thing that exercised it was production.
 * The callback page is glue too: the adapter must answer it itself, before the
 * policy and without a redirect, or the `#access_token` fragment never reaches
 * the session exchange — so that ordering is pinned here.
 *
 * Run with type stripping (Node's built-in, no toolchain):
 *
 *     node --experimental-strip-types --test functions/_middleware.test.mjs
 */
const PROBE_TOKEN = "a-long-random-probe-secret-value";
const ALLOWED_EMAIL = "owner@example.test";
const CHAPTER = "/10-frontend/10.1-javascript/INDEX.html";

function call(path, { cookie = "", env = {}, host = "study.buildora.work" } = {}) {
  const headers = cookie ? { Cookie: cookie } : undefined;
  return onRequest({
    request: new Request(`https://${host}${path}`, { headers }),
    env,
    next: async () => new Response("CHAPTER", { status: 200 }),
  });
}

test("the fallback host is redirected before anything else, query preserved", async () => {
  const response = await call("/INDEX.html?q=cap", { host: "software-developer-bible.pages.dev" });
  assert.equal(response.status, 308);
  assert.equal(response.headers.get("Location"),
               "https://study.buildora.work/INDEX.html?q=cap");
  assert.equal(response.headers.get("Cache-Control"), "no-store");
});

test("a public auth path is handed to the asset pipeline", async () => {
  const response = await call("/auth/login");
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "CHAPTER");
});

test("the OAuth callback is answered directly, fragment intact", async () => {
  // The one page that must never be canonicalized or gated: Supabase returns
  // the Google session in the URL fragment, and the `.html` -> clean-URL 308
  // is where it was lost. Both spellings resolve here, query and all.
  for (const path of [
    "/auth/callback.html",
    "/auth/callback",
    "/auth/callback?code=abc&state=%2FINDEX.html",
  ]) {
    const response = await call(path);
    assert.equal(response.status, 200, path);
    assert.equal(response.headers.get("Content-Type"), "text/html; charset=utf-8", path);
    assert.equal(response.headers.get("Cache-Control"),
                 "no-store, no-cache, must-revalidate", path);
    const body = await response.text();
    // The page's contract with `/auth/session`: read the fragment, post it,
    // then follow the sanitized `next` the route answers with.
    assert.match(body, /window\.location\.hash/, path);
    assert.match(body, /fragment\.get\("refresh_token"\)/, path);
    assert.match(body, /refresh_token: refreshToken/, path);
    assert.match(body, /fetch\("\/auth\/session\?next="/, path);
  }
});

test("the callback intercept precedes the policy, even for a session that would be allowed", async () => {
  // On a fall-through this request would reach `next()` and serve the
  // chapter: the callback has to be the whole response, not a decision.
  const response = await call("/auth/callback.html?code=x", {
    cookie: `study_access_token=${PROBE_TOKEN}`,
    env: { STUDY_PROBE_TOKEN: PROBE_TOKEN, STUDY_ALLOWED_EMAIL: ALLOWED_EMAIL },
  });
  assert.equal(response.status, 200);
  const body = await response.text();
  assert.match(body, /id="status"/);
  assert.doesNotMatch(body, /CHAPTER/);
});

test("a visitor with no cookie lands on login with the deep link preserved", async () => {
  const response = await call(`${CHAPTER}?q=cap`);
  assert.equal(response.status, 302);
  assert.equal(response.headers.get("Location"),
               "/auth/login.html?next=%2F10-frontend%2F10.1-javascript%2FINDEX.html%3Fq%3Dcap");
});

test("the probe credential is read from the cookie and serves the chapter", async () => {
  const response = await call(CHAPTER, {
    cookie: `study_access_token=${PROBE_TOKEN}`,
    env: { STUDY_PROBE_TOKEN: PROBE_TOKEN, STUDY_ALLOWED_EMAIL: ALLOWED_EMAIL },
  });
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "CHAPTER");
});

test("a cookie beside others is still found", async () => {
  const response = await call(CHAPTER, {
    cookie: `theme=dark; study_access_token=${PROBE_TOKEN}; other=1`,
    env: { STUDY_PROBE_TOKEN: PROBE_TOKEN, STUDY_ALLOWED_EMAIL: ALLOWED_EMAIL },
  });
  assert.equal(response.status, 200);
});

test("an unset probe credential grants nothing", async () => {
  const response = await call(CHAPTER, { cookie: `study_access_token=${PROBE_TOKEN}` });
  assert.equal(response.status, 302);
  assert.equal(response.headers.get("Location"),
               "https://personal.buildora.work/?study=access-denied");
});

test("a configured probe cannot grant access when the allowlist is missing", async () => {
  const response = await call(CHAPTER, {
    cookie: `study_access_token=${PROBE_TOKEN}`,
    env: { STUDY_PROBE_TOKEN: PROBE_TOKEN },
  });
  assert.equal(response.status, 302);
  assert.equal(response.headers.get("Location"),
               "https://personal.buildora.work/?study=access-denied");
});

test("a presented session that cannot be verified reaches the denial page", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    throw new Error("supabase unreachable");
  };
  try {
    const response = await call(CHAPTER, {
      cookie: "study_access_token=presented-but-unverifiable",
      env: { SUPABASE_URL: "https://example.supabase.co", SUPABASE_ANON_KEY: "key" },
    });
    assert.equal(response.status, 302);
    assert.equal(response.headers.get("Location"),
                 "https://personal.buildora.work/?study=access-denied");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("a stale refresh cookie is cleared and the visitor starts at login", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url) => {
    const target = String(url);
    if (target.includes("/auth/v1/token?grant_type=refresh_token")) {
      return new Response(JSON.stringify({ error: "invalid_grant" }), { status: 400 });
    }
    throw new Error("unexpected Supabase request: " + target);
  };
  try {
    const response = await call(CHAPTER, {
      cookie: "study_refresh_token=stale",
      env: { SUPABASE_URL: "https://example.supabase.co", SUPABASE_ANON_KEY: "key" },
    });
    assert.equal(response.status, 302);
    assert.equal(response.headers.get("Location"),
                 "/auth/login.html?next=%2F10-frontend%2F10.1-javascript%2FINDEX.html");
    const cookies = response.headers.getSetCookie();
    assert.equal(cookies.length, 2, "the unusable pair is dropped together");
    for (const cookie of cookies) assert.match(cookie, /Max-Age=0/);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("a refreshed account outside the allowlist is denied without storing the renewal", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url) => {
    const target = String(url);
    if (target.includes("/auth/v1/token?grant_type=refresh_token")) {
      return new Response(JSON.stringify({
        access_token: "other-access",
        refresh_token: "other-refresh",
        expires_in: 3600,
        user: { email: "someone.else@example.com" },
      }), { status: 200 });
    }
    throw new Error("unexpected Supabase request: " + target);
  };
  try {
    const response = await call(CHAPTER, {
      cookie: "study_refresh_token=refresh-token",
      env: {
        SUPABASE_URL: "https://example.supabase.co",
        SUPABASE_ANON_KEY: "key",
        STUDY_ALLOWED_EMAIL: ALLOWED_EMAIL,
      },
    });
    assert.equal(response.status, 302);
    assert.equal(response.headers.get("Location"),
                 "https://personal.buildora.work/?study=access-denied");
    const cookies = response.headers.getSetCookie();
    for (const cookie of cookies) {
      assert.match(cookie, /Max-Age=0/);
      assert.doesNotMatch(cookie, /other-access|other-refresh/);
    }
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("an expired access cookie refreshes from the refresh cookie instead of asking for Google again", async () => {
  const originalFetch = globalThis.fetch;
  const calls = [];
  globalThis.fetch = async (url, init = {}) => {
    const target = String(url);
    calls.push({ target, method: init.method ?? "GET", body: init.body });
    if (target.endsWith("/auth/v1/user")) return new Response("{}", { status: 401 });
    if (target.endsWith("/auth/v1/.well-known/jwks.json")) {
      return new Response(JSON.stringify({ keys: [] }), { status: 200 });
    }
    if (target.includes("/auth/v1/token?grant_type=refresh_token")) {
      return new Response(JSON.stringify({
        access_token: "new-access-token",
        refresh_token: "rotated-refresh-token",
        expires_in: 3600,
        user: { email: ALLOWED_EMAIL },
      }), { status: 200 });
    }
    throw new Error("unexpected Supabase request: " + target);
  };
  try {
    const response = await call(CHAPTER, {
      cookie: "study_access_token=expired-token; study_refresh_token=refresh-token",
      env: {
        SUPABASE_URL: "https://example.supabase.co",
        SUPABASE_ANON_KEY: "key",
        STUDY_ALLOWED_EMAIL: ALLOWED_EMAIL,
      },
    });
    assert.equal(response.status, 200, "the refreshed session serves the chapter");
    assert.equal(await response.text(), "CHAPTER");
    assert.equal(
      JSON.parse(calls.find((entry) => entry.target.includes("grant_type=refresh_token")).body).refresh_token,
      "refresh-token",
      "the refresh cookie is exchanged, not the access cookie",
    );
    const cookies = response.headers.getSetCookie();
    assert.match(cookies[0], /^study_access_token=new-access-token;/);
    assert.match(cookies[0], /Max-Age=3600/);
    assert.match(cookies[1], /^study_refresh_token=rotated-refresh-token;/);
    assert.match(cookies[1], /Max-Age=2592000/);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
