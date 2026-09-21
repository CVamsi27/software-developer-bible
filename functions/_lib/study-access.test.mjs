import test from "node:test";
import assert from "node:assert/strict";
import {
  accessDeniedRedirect,
  fetchSupabaseUser,
  isAllowedStudyEmail,
  isPagesDevHost,
  isPublicAuthPath,
  normalizeEmail,
  resolveSupabaseConfig,
  safeNextPath,
} from "./study-access.mjs";

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
    resolveSupabaseConfig({
      SUPABASE_JWKS_URL: "https://example.supabase.co/auth/v1/.well-known/jwks.json",
    }),
    {
      url: "https://example.supabase.co",
      anonKey: "",
      jwksUrl: "https://example.supabase.co/auth/v1/.well-known/jwks.json",
    },
  );
});

test("verifies an asymmetric access token with the configured JWKS endpoint", async () => {
  const { privateKey, publicKey } = await crypto.subtle.generateKey(
    { name: "ECDSA", namedCurve: "P-256" },
    true,
    ["sign", "verify"],
  );
  const publicJwk = await crypto.subtle.exportKey("jwk", publicKey);
  publicJwk.kid = "study-key";
  publicJwk.alg = "ES256";

  const encode = (value) => Buffer.from(value).toString("base64url");
  const header = encode(JSON.stringify({ alg: "ES256", kid: "study-key", typ: "JWT" }));
  const payload = encode(JSON.stringify({
    aud: "authenticated",
    email: "cvamsik99@gmail.com",
    exp: Math.floor(Date.now() / 1000) + 3600,
    iss: "https://example.supabase.co/auth/v1",
  }));
  const signingInput = new TextEncoder().encode(`${header}.${payload}`);
  const signature = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, privateKey, signingInput);
  const token = `${header}.${payload}.${Buffer.from(signature).toString("base64url")}`;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify({ keys: [publicJwk] }), { status: 200 });

  try {
    assert.deepEqual(
      await fetchSupabaseUser(token, { SUPABASE_JWKS_URL: "https://example.supabase.co/auth/v1/.well-known/jwks.json" }),
      { email: "cvamsik99@gmail.com" },
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});
