import test from "node:test";
import assert from "node:assert/strict";
import {
  accessDeniedRedirect,
  decideAccess,
  fetchSupabaseUser,
  isAllowedStudyEmail,
  isPagesDevHost,
  isPublicAuthPath,
  normalizeEmail,
  probeTokenSession,
  readStudyToken,
  resolveSessionFromToken,
  resolveSupabaseConfig,
  respondTo,
  safeNextPath,
} from "./study-access.mjs";

const JWKS_URL = "https://example.supabase.co/auth/v1/.well-known/jwks.json";
const STUDY = { hostname: "study.buildora.work" };

/** A genuinely ES256-signed access token plus the JWKS that verifies it. */
async function signedToken({ email = "cvamsik99@gmail.com", expiresIn = 3600, kid = "study-key" } = {}) {
  const { privateKey, publicKey } = await crypto.subtle.generateKey(
    { name: "ECDSA", namedCurve: "P-256" },
    true,
    ["sign", "verify"],
  );
  const publicJwk = await crypto.subtle.exportKey("jwk", publicKey);
  publicJwk.kid = kid;
  publicJwk.alg = "ES256";

  const encode = (value) => Buffer.from(value).toString("base64url");
  const header = encode(JSON.stringify({ alg: "ES256", kid, typ: "JWT" }));
  const payload = encode(JSON.stringify({
    aud: "authenticated",
    email,
    exp: Math.floor(Date.now() / 1000) + expiresIn,
    iss: "https://example.supabase.co/auth/v1",
  }));
  const signingInput = new TextEncoder().encode(`${header}.${payload}`);
  const signature = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, privateKey, signingInput);

  return {
    token: `${header}.${payload}.${Buffer.from(signature).toString("base64url")}`,
    jwks: { keys: [publicJwk] },
  };
}

function stubJwks(jwks) {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify(jwks), { status: 200 });
  return () => {
    globalThis.fetch = originalFetch;
  };
}

test("allows only the exact study account, case-insensitively", () => {
  assert.equal(isAllowedStudyEmail("cvamsik99@gmail.com"), true);
  assert.equal(isAllowedStudyEmail("CVAMSIK99@GMAIL.COM"), true);
  assert.equal(isAllowedStudyEmail("other@example.com"), false);
  assert.equal(isAllowedStudyEmail("cvamsik99@gmail.com.evil.example"), false);
});

test("normalizes whitespace and casing without changing the identity", () => {
  assert.equal(normalizeEmail("  CVamsik99@Gmail.com  "), "cvamsik99@gmail.com");
  assert.equal(normalizeEmail(null), "");
});

test("accepts only local next paths", () => {
  assert.equal(safeNextPath("/00-strategy/INDEX.md"), "/00-strategy/INDEX.md");
  assert.equal(safeNextPath("https://evil.example"), "/");
  assert.equal(safeNextPath("//evil.example"), "/");
  assert.equal(safeNextPath("\\\\evil.example"), "/");
  assert.equal(safeNextPath(""), "/");
});

test("keeps only auth entry points public", () => {
  assert.equal(isPublicAuthPath("/auth/login.html"), true);
  assert.equal(isPublicAuthPath("/auth/login"), true);
  assert.equal(isPublicAuthPath("/auth/callback.html"), true);
  assert.equal(isPublicAuthPath("/auth/callback"), true);
  assert.equal(isPublicAuthPath("/auth/session"), true);
  assert.equal(isPublicAuthPath("/favicon.svg"), true);
  assert.equal(isPublicAuthPath("/00-strategy/INDEX.md"), false);
});

test("uses the personal host for a denied study session", () => {
  assert.equal(accessDeniedRedirect(), "https://personal.buildora.work/?study=access-denied");
});

test("recognizes the production Pages fallback host as non-canonical", () => {
  assert.equal(isPagesDevHost("software-developer-bible.pages.dev"), true);
  assert.equal(isPagesDevHost("SOFTWARE-DEVELOPER-BIBLE.PAGES.DEV"), true);
  assert.equal(isPagesDevHost("study.buildora.work"), false);
});

test("accepts the public Supabase variable names used by the personal app", () => {
  assert.deepEqual(
    resolveSupabaseConfig({
      NEXT_PUBLIC_SUPABASE_URL: "https://example.supabase.co",
      SUPABASE_PUBLISHABLE_KEY: "public-key",
    }),
    { url: "https://example.supabase.co", anonKey: "public-key", jwksUrl: "" },
  );
  assert.deepEqual(
    resolveSupabaseConfig({ SUPABASE_JWKS_URL: JWKS_URL }),
    { url: "https://example.supabase.co", anonKey: "", jwksUrl: JWKS_URL },
  );
});

test("verifies an asymmetric access token with the configured JWKS endpoint", async () => {
  const { token, jwks } = await signedToken();
  const restore = stubJwks(jwks);
  try {
    assert.deepEqual(
      await fetchSupabaseUser(token, { SUPABASE_JWKS_URL: JWKS_URL }),
      { email: "cvamsik99@gmail.com" },
    );
  } finally {
    restore();
  }
});

test("rejects an expired access token", async () => {
  const { token, jwks } = await signedToken({ expiresIn: -60 });
  const restore = stubJwks(jwks);
  try {
    assert.equal(await fetchSupabaseUser(token, { SUPABASE_JWKS_URL: JWKS_URL }), null);
  } finally {
    restore();
  }
});

test("reads the session cookie out of a cookie header", () => {
  assert.equal(readStudyToken("study_access_token=abc.def.ghi"), "abc.def.ghi");
  assert.equal(readStudyToken("other=1; study_access_token=tok; more=2"), "tok");
  assert.equal(readStudyToken("study_access_token=a%20b"), "a b");
  assert.equal(readStudyToken("study_access_token=%E0%A4%A"), "");
  assert.equal(readStudyToken("other=1"), "");
  assert.equal(readStudyToken(undefined), "");
});

test("an absent cookie is anonymous and never calls the verifier", async () => {
  let verifications = 0;
  const session = await resolveSessionFromToken({
    token: "",
    verifyToken: async () => {
      verifications += 1;
      return { email: "cvamsik99@gmail.com" };
    },
  });
  assert.deepEqual(session, { email: null, hasToken: false });
  assert.equal(verifications, 0);
});

test("forwards the verified account's email", async () => {
  const session = await resolveSessionFromToken({
    token: "tok",
    verifyToken: async () => ({ email: "cvamsik99@gmail.com" }),
  });
  assert.deepEqual(session, { email: "cvamsik99@gmail.com", hasToken: true });
});

test("a rejected token and a thrown verification are both presented sessions", async () => {
  for (const verifyToken of [
    async () => null,
    async () => {
      throw new Error("supabase unreachable");
    },
  ]) {
    assert.deepEqual(await resolveSessionFromToken({ token: "tok", verifyToken }), {
      email: null,
      hasToken: true,
    });
  }
});

// ---------------------------------------------------------------------------
// The probe credential: the one thing that lets the *success* path be verified
// against the real edge instead of only here. It must be inert when unset.
// ---------------------------------------------------------------------------

const PROBE = "a-long-random-probe-secret-value";

test("an unset probe credential grants nothing", () => {
  for (const env of [{}, { STUDY_PROBE_TOKEN: "" }, null]) {
    assert.equal(probeTokenSession(PROBE, env), null);
  }
});

test("the probe credential admits only an exact match", () => {
  assert.deepEqual(probeTokenSession(PROBE, { STUDY_PROBE_TOKEN: PROBE }), {
    email: "cvamsik99@gmail.com",
  });
  for (const wrong of [
    "",
    "a-long-random-probe-secret-valu",
    "a-long-random-probe-secret-value-",
    "A-LONG-RANDOM-PROBE-SECRET-VALUE",
    "a-long-random-probe-secret-valueX",
  ]) {
    assert.equal(probeTokenSession(wrong, { STUDY_PROBE_TOKEN: PROBE }), null, wrong);
  }
});

test("a cookie that is not the probe credential still goes to Supabase", async () => {
  const calls = [];
  const session = await resolveSessionFromToken({
    token: "an-ordinary-session-cookie",
    verifyToken: async (token) => {
      calls.push(token);
      return probeTokenSession(token, { STUDY_PROBE_TOKEN: PROBE })
        ?? { email: "cvamsik99@gmail.com" };
    },
  });
  assert.deepEqual(calls, ["an-ordinary-session-cookie"]);
  assert.deepEqual(session, { email: "cvamsik99@gmail.com", hasToken: true });
});

// ---------------------------------------------------------------------------
// The gate decision. These are the branches a live probe cannot reach: the one
// that serves content needs the owner's Google account, so it is proven here or
// nowhere.
// ---------------------------------------------------------------------------

const verified = (email) => async () => ({ email, hasToken: true });
const anonymous = async () => ({ email: null, hasToken: false });

test("sends the fallback host to the study origin before anything else", async () => {
  const decision = await decideAccess({
    hostname: "software-developer-bible.pages.dev",
    pathname: "/INDEX.html",
    search: "?q=1",
    resolveSession: async () => {
      throw new Error("the fallback host must not resolve a session");
    },
  });
  assert.deepEqual(decision, {
    action: "canonical",
    status: 308,
    location: "https://study.buildora.work/INDEX.html?q=1",
  });
});

test("keeps auth entry points public without resolving a session", async () => {
  let resolutions = 0;
  for (const pathname of [
    "/auth/login",
    "/auth/login.html",
    "/auth/callback",
    "/auth/callback.html",
    "/auth/start",
    "/auth/session",
    "/auth/logout",
    "/favicon.svg",
  ]) {
    const decision = await decideAccess({
      ...STUDY,
      pathname,
      resolveSession: async () => {
        resolutions += 1;
        return { email: null, hasToken: false };
      },
    });
    assert.equal(decision.action, "public", pathname);
  }
  assert.equal(resolutions, 0, "a public path must not pay for a token verification");
});

test("serves content to a verified session for the approved account", async () => {
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/10-frontend/10.1-javascript/INDEX.html",
    resolveSession: verified("cvamsik99@gmail.com"),
  });
  assert.deepEqual(decision, { action: "allow", status: 200, location: "" });
});

test("denies a presented session that failed verification", async () => {
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/INDEX.html",
    resolveSession: verified(null),
  });
  assert.deepEqual(decision, {
    action: "denied",
    status: 302,
    location: "https://personal.buildora.work/?study=access-denied",
  });
});

test("denies a verified session for a different account", async () => {
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/INDEX.html",
    resolveSession: verified("someone.else@example.com"),
  });
  assert.equal(decision.action, "denied");
});

test("sends a visitor with no session to login with the deep link preserved", async () => {
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/10-frontend/INDEX.html",
    search: "?q=cap",
    resolveSession: anonymous,
  });
  assert.deepEqual(decision, {
    action: "login",
    status: 302,
    location: "/auth/login.html?next=%2F10-frontend%2FINDEX.html%3Fq%3Dcap",
  });
});

test("never carries an off-site next into the login redirect", async () => {
  const decision = await decideAccess({ ...STUDY, pathname: "//evil.example", resolveSession: anonymous });
  assert.equal(decision.location, "/auth/login.html?next=%2F");
});

test("serves the asset for allow and public, and redirects otherwise", async () => {
  const next = async () => new Response("CONTENT", { status: 200 });
  for (const action of ["allow", "public"]) {
    const response = await respondTo({ action, status: 200, location: "" }, next);
    assert.equal(response.status, 200);
    assert.equal(await response.text(), "CONTENT");
  }
  for (const [action, status, location] of [
    ["canonical", 308, "https://study.buildora.work/INDEX.html"],
    ["denied", 302, accessDeniedRedirect()],
    ["login", 302, "/auth/login.html?next=%2F"],
  ]) {
    const response = await respondTo({ action, status, location }, next);
    assert.equal(response.status, status, action);
    assert.equal(response.headers.get("Location"), location, action);
    assert.equal(response.headers.get("Cache-Control"), "no-store", action);
    assert.equal(await response.text(), "", action);
  }
});

test("the probe credential serves content to the live probe's session", async () => {
  const session = await resolveSessionFromToken({
    token: PROBE,
    verifyToken: (token) => probeTokenSession(token, { STUDY_PROBE_TOKEN: PROBE }),
  });
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/00-strategy/00.01-communication.html",
    resolveSession: async () => session,
  });
  assert.deepEqual(decision, { action: "allow", status: 200, location: "" });
});

test("a thrown verification reaches the denial page, not the login page", async () => {
  const decision = await decideAccess({
    ...STUDY,
    pathname: "/10-frontend/INDEX.html",
    resolveSession: () =>
      resolveSessionFromToken({
        token: "presented",
        verifyToken: async () => {
          throw new Error("supabase unreachable");
        },
      }),
  });
  assert.deepEqual(decision, {
    action: "denied",
    status: 302,
    location: accessDeniedRedirect(),
  });
});

test("a real signed token for the approved account is allowed end to end", async () => {
  const { token, jwks } = await signedToken();
  const restore = stubJwks(jwks);
  try {
    // The full path a signed-in visitor takes: cookie -> verification -> decision.
    const session = await fetchSupabaseUser(token, { SUPABASE_JWKS_URL: JWKS_URL });
    const decision = await decideAccess({
      ...STUDY,
      pathname: "/10-frontend/INDEX.html",
      resolveSession: async () => ({ email: session?.email ?? null, hasToken: true }),
    });
    assert.deepEqual(decision, { action: "allow", status: 200, location: "" });
  } finally {
    restore();
  }
});

test("a signed-out chapter keeps its dated roadmap context through the login destination",async()=>{
 const pathname="/10-frontend/scope.html",search="?roadmapDate=2026-10-12&roadmapTask=germany%3A2026%3Aday%3A2026-10-12";
 const result=await decideAccess({hostname:"study.buildora.work",pathname,search,resolveSession:async()=>({email:null,hasToken:false})});
 assert.equal(result.action,"login");
 assert.equal(new URL(result.location,"https://study.buildora.work").searchParams.get("next"),pathname+search);
});
test("legacy Markdown reading links go to rendered chapters without losing the dated task", async () => {
  const search = "?roadmapDate=2026-10-12&roadmapTask=germany%3A2026%3Aday%3A2026-10-12";
  let resolved = false;
  const result = await decideAccess({
    hostname: "study.buildora.work",
    pathname: "/10-frontend/scope.md",
    search,
    resolveSession: async () => {
      resolved = true;
      return { email: "cvamsik99@gmail.com", hasToken: true };
    },
  });
  assert.deepEqual(result, {
    action: "canonical",
    status: 308,
    location: "https://study.buildora.work/10-frontend/scope.html" + search,
  });
  assert.equal(resolved, false);
  const next = await decideAccess({
    hostname: "study.buildora.work",
    pathname: "/10-frontend/scope.html",
    search,
    resolveSession: async () => ({ email: null, hasToken: false }),
  });
  assert.equal(next.action, "login");
  assert.equal(new URL(next.location, "https://study.buildora.work").searchParams.get("next"), "/10-frontend/scope.html" + search);
});
