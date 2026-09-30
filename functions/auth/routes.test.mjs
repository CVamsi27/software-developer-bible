import test from "node:test";
import assert from "node:assert/strict";
import * as sessionModule from "./session.ts";
import { onRequestPost as session } from "./session.ts";
import { onRequestGet as start } from "./start.ts";
import { onRequestGet as logout } from "./logout.ts";

/**
 * The auth routes, offline.
 *
 * `session.ts` is the one that matters: it exchanges a Supabase access token for
 * the session cookie the whole gate reads, so it decides both who gets in and
 * what gets stored. It had no test in this repository and was exercised only by
 * a real Google sign-in — the one flow that cannot be driven from CI. The
 * verification itself (JWKS/ES256, claims, expiry) is covered in
 * `_lib/study-access.test.mjs`; what is tested here is what the route *does*
 * with a verification result: allowlist, cookie shape, and `next`.
 *
 * Run with type stripping:
 *
 *     node --experimental-strip-types --test functions/auth/routes.test.mjs
 */
const ALLOWED = "cvamsik99@gmail.com";
const SUPABASE = "https://example.supabase.co";
const ENV = { SUPABASE_URL: SUPABASE, SUPABASE_ANON_KEY: "publishable-key" };

/** Stub Supabase's /auth/v1/user, capturing the request the route makes. */
function stubUser(user, { status = 200, throws = false } = {}) {
  const originalFetch = globalThis.fetch;
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url: String(url), authorization: init?.headers?.Authorization ?? "" });
    if (throws) throw new Error("supabase unreachable");
    return new Response(JSON.stringify(user), { status });
  };
  return {
    calls,
    restore: () => {
      globalThis.fetch = originalFetch;
    },
  };
}

function post({ body, url = "https://study.buildora.work/auth/session", env = ENV, headers = {} } = {}) {
  const request = new Request(url, {
    method: "POST",
    body: typeof body === "string" ? body : JSON.stringify(body),
    headers: { "Content-Type": "application/json", ...headers },
  });
  return session({ request, env });
}

test("the session route exports no GET handler", () => {
  // Pages answers a GET with 405, which is what the live probe relies on: the
  // path must be public, and a public path must never serve a chapter. Adding
  // an onRequestGet here would change what production does with a GET, so the
  // absence is asserted rather than assumed.
  assert.equal(typeof session, "function");
  assert.equal("onRequestGet" in sessionModule, false);
});

test("a body that is not JSON is rejected as a bad request", async () => {
  const response = await post({ body: "not json" });
  assert.equal(response.status, 400);
  assert.deepEqual(await response.json(), { ok: false, reason: "invalid-request" });
});

test("a missing or non-string token is never exchanged", async () => {
  const stub = stubUser({ email: ALLOWED });
  try {
    for (const body of [{}, { access_token: 42 }, { access_token: null }]) {
      const response = await post({ body });
      assert.equal(response.status, 403, JSON.stringify(body));
      const payload = await response.json();
      assert.equal(payload.ok, false);
      assert.equal(payload.reason, "not-allowed");
    }
    assert.deepEqual(stub.calls, []);
  } finally {
    stub.restore();
  }
});

test("the token is forwarded to Supabase, and the allowed account gets a session cookie", async () => {
  const stub = stubUser({ email: ALLOWED });
  try {
    const response = await post({ body: { access_token: "a.b.c" } });
    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), { ok: true, email: ALLOWED, next: "/" });
    assert.deepEqual(stub.calls, [
      { url: `${SUPABASE}/auth/v1/user`, authorization: "Bearer a.b.c" },
    ]);
    const cookie = response.headers.get("Set-Cookie") ?? "";
    assert.match(cookie, /^study_access_token=a\.b\.c;/);
    for (const attribute of ["Path=/", "HttpOnly", "Secure", "SameSite=Lax", "Max-Age=3600"]) {
      assert.ok(cookie.includes(attribute), `${attribute} missing from ${cookie}`);
    }
    assert.equal(response.headers.get("Cache-Control"), "no-store");
  } finally {
    stub.restore();
  }
});

test("a token that needs encoding is stored encoded", async () => {
  const stub = stubUser({ email: ALLOWED });
  try {
    const response = await post({ body: { access_token: "a+b/c=d" } });
    assert.match(response.headers.get("Set-Cookie") ?? "", /study_access_token=a%2Bb%2Fc%3Dd;/);
  } finally {
    stub.restore();
  }
});

test("an account outside the allowlist is refused with the denial target", async () => {
  const stub = stubUser({ email: "someone.else@example.com" });
  try {
    const response = await post({ body: { access_token: "a.b.c" } });
    assert.equal(response.status, 403);
    assert.deepEqual(await response.json(), {
      ok: false,
      reason: "not-allowed",
      redirect: "https://personal.buildora.work/?study=access-denied",
    });
    assert.equal(response.headers.get("Set-Cookie"), null, "no cookie for a refused account");
  } finally {
    stub.restore();
  }
});

test("a rejected or unreachable verification is a refusal, not a crash", async () => {
  for (const options of [{ user: { email: ALLOWED }, status: 401 }, { user: null, throws: true }]) {
    const stub = stubUser(options.user, { status: options.status ?? 200, throws: options.throws });
    try {
      const response = await post({ body: { access_token: "stale" } });
      assert.equal(response.status, 403);
      assert.equal((await response.json()).reason, "not-allowed");
    } finally {
      stub.restore();
    }
  }
});

test("next is carried only when it is a local path", async () => {
  const stub = stubUser({ email: ALLOWED });
  try {
    const cases = [
      ["/10-frontend/INDEX.html", "/10-frontend/INDEX.html"],
      ["https://evil.example", "/"],
      ["//evil.example", "/"],
      [null, "/"],
    ];
    for (const [raw, expected] of cases) {
      const url = `https://study.buildora.work/auth/session${raw === null ? "" : `?next=${encodeURIComponent(raw)}`}`;
      const response = await post({ body: { access_token: "a.b.c" }, url });
      assert.equal((await response.json()).next, expected, String(raw));
    }
  } finally {
    stub.restore();
  }
});

test("next is resolved from body or cookie when query parameter is omitted", async () => {
  const stub = stubUser({ email: ALLOWED });
  try {
    const fromBody = await post({ body: { access_token: "good-token", next: "/70-interview-toolkit/foo.html" } });
    assert.equal((await fromBody.json()).next, "/70-interview-toolkit/foo.html");

    const fromCookie = await post({
      body: { access_token: "good-token" },
      headers: { Cookie: "study_next_url=%2F20-backend%2Fbar.html" },
    });
    assert.equal((await fromCookie.json()).next, "/20-backend/bar.html");
  } finally {
    stub.restore();
  }
});

test("the sign-in redirect points at Supabase with the callback and deep link", async () => {
  const response = await start({
    request: new Request("https://study.buildora.work/auth/start?next=%2FINDEX.html"),
    env: ENV,
  });
  assert.equal(response.status, 302);
  const location = new URL(response.headers.get("Location"));
  assert.equal(location.origin + location.pathname, `${SUPABASE}/auth/v1/authorize`);
  assert.equal(location.searchParams.get("provider"), "google");
  assert.equal(location.searchParams.get("redirect_to"), "https://study.buildora.work/auth/callback.html");
  assert.equal(location.searchParams.get("state"), "/INDEX.html");
});

test("an off-site deep link never becomes the OAuth state", async () => {
  const response = await start({
    request: new Request("https://study.buildora.work/auth/start?next=https%3A%2F%2Fevil.example"),
    env: ENV,
  });
  assert.equal(new URL(response.headers.get("Location")).searchParams.get("state"), "/");
});

test("sign-in without a Supabase URL is a 503, not a broken redirect", async () => {
  const response = await start({
    request: new Request("https://study.buildora.work/auth/start"),
    env: {},
  });
  assert.equal(response.status, 503);
  assert.match(await response.text(), /not configured/i);
});

test("a trailing slash in the project URL does not double up", async () => {
  const response = await start({
    request: new Request("https://study.buildora.work/auth/start"),
    env: { SUPABASE_URL: `${SUPABASE}/` },
  });
  assert.equal(new URL(response.headers.get("Location")).pathname, "/auth/v1/authorize");
});

test("logout clears the session cookie and returns to the login page", async () => {
  const response = await logout({
    request: new Request("https://study.buildora.work/auth/logout"),
  });
  assert.equal(response.status, 302);
  assert.equal(response.headers.get("Location"), "https://study.buildora.work/auth/login.html");
  const cookie = response.headers.get("Set-Cookie") ?? "";
  assert.match(cookie, /^study_access_token=;/);
  assert.ok(cookie.includes("Max-Age=0"), cookie);
  for (const attribute of ["Path=/", "HttpOnly", "Secure"]) {
    assert.ok(cookie.includes(attribute), `${attribute} missing from ${cookie}`);
  }
  assert.equal(response.headers.get("Cache-Control"), "no-store");
});
