const ALLOWED_STUDY_EMAIL = "cvamsik99@gmail.com";
const PERSONAL_ACCESS_DENIED_URL = "https://personal.buildora.work/?study=access-denied";
const PRODUCTION_PAGES_HOST = "software-developer-bible.pages.dev";
export const STUDY_CANONICAL_ORIGIN = "https://study.buildora.work";
// The paths the middleware answers itself, before the asset layer runs: the
// OAuth callback has no file behind it, and Pages canonicalizes a `.html`
// request with a 308 that would drop the #access_token fragment. One
// declaration on purpose: `_middleware.ts` consumes it for the intercept,
// `PUBLIC_AUTH_PATHS` spreads it, and the live probe resolves it
// (scripts/check_study_live.py) so the callback URLs cannot silently drop out
// of the must-answer-200 set.
export const INTERCEPTED_PATHS = ["/auth/callback.html", "/auth/callback"];
const PUBLIC_AUTH_PATHS = new Set([
  "/auth/login.html",
  "/auth/login",
  ...INTERCEPTED_PATHS,
  "/auth/start",
  "/auth/session",
  "/auth/logout",
  "/favicon.svg",
]);

export function normalizeEmail(value) {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

export function isAllowedStudyEmail(value) {
  const norm = normalizeEmail(value);
  return (
    norm === ALLOWED_STUDY_EMAIL ||
    norm.replace(/@googlemail\.com$/, "@gmail.com") === ALLOWED_STUDY_EMAIL
  );
}

export function isPagesDevHost(value) {
  return typeof value === "string" && value.trim().toLowerCase() === PRODUCTION_PAGES_HOST;
}

const DEFAULT_SUPABASE_URL = "https://ejbghgpatpfubxltkpde.supabase.co";
const DEFAULT_SUPABASE_KEY = "sb_publishable_I42JurXGACj13HhJ1vmjdQ_lwTO8IK8";

export function resolveSupabaseConfig(env) {
  const jwksUrl = env?.SUPABASE_JWKS_URL || "";
  let url = env?.SUPABASE_URL || env?.NEXT_PUBLIC_SUPABASE_URL || "";
  if (!url && jwksUrl) {
    try {
      url = new URL(jwksUrl).origin;
    } catch {
      url = "";
    }
  }
  let anonKey =
    env?.SUPABASE_ANON_KEY ||
    env?.SUPABASE_PUBLISHABLE_KEY ||
    env?.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
    env?.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
    "";
  if (!anonKey && url && url.includes("ejbghgpatpfubxltkpde")) {
    anonKey = DEFAULT_SUPABASE_KEY;
  }
  return {
    url: url ? url.replace(/\/$/, "") : "",
    anonKey,
    jwksUrl,
  };
}

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(value.length / 4) * 4, "=");
  const binary = atob(normalized);
  return Uint8Array.from(binary, (character) => character.charCodeAt(0));
}

function decodeJsonSegment(value) {
  return JSON.parse(new TextDecoder().decode(decodeBase64Url(value)));
}

function parseAccessToken(token) {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    return {
      header: decodeJsonSegment(parts[0]),
      payload: decodeJsonSegment(parts[1]),
      signingInput: new TextEncoder().encode(`${parts[0]}.${parts[1]}`),
      signature: decodeBase64Url(parts[2]),
    };
  } catch {
    return null;
  }
}

async function verifyAsymmetricToken(token, config) {
  const parsed = parseAccessToken(token);
  if (!parsed) return null;
  const jwksUrl = config.jwksUrl || (config.url ? `${config.url.replace(/\/$/, "")}/auth/v1/.well-known/jwks.json` : "");
  if (!jwksUrl) return null;

  const algorithm = parsed.header.alg;
  const keyAlgorithm =
    algorithm === "ES256"
      ? { name: "ECDSA", namedCurve: "P-256" }
      : algorithm === "RS256"
        ? { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }
        : null;
  if (!keyAlgorithm || typeof parsed.header.kid !== "string") return null;

  try {
    const jwksResponse = await fetch(jwksUrl);
    if (!jwksResponse.ok) return null;
    const jwks = await jwksResponse.json();
    const jwk = Array.isArray(jwks?.keys)
      ? jwks.keys.find((key) => key?.kid === parsed.header.kid && (key?.alg === algorithm || !key?.alg))
      : null;
    if (!jwk) return null;

    const cryptoKey = await crypto.subtle.importKey("jwk", jwk, keyAlgorithm, false, ["verify"]);
    const verifyAlgorithm = algorithm === "ES256" ? { name: "ECDSA", hash: "SHA-256" } : keyAlgorithm;
    const valid = await crypto.subtle.verify(verifyAlgorithm, cryptoKey, parsed.signature, parsed.signingInput);
    if (!valid) return null;

    const now = Math.floor(Date.now() / 1000);
    const { exp, nbf, iss, aud, email, user_metadata } = parsed.payload ?? {};
    const expectedIssuer = config.url ? `${config.url.replace(/\/$/, "")}/auth/v1` : "";
    const cleanUrl = config.url ? config.url.replace(/\/$/, "") : "";
    const cleanIss = typeof iss === "string" ? iss.replace(/\/$/, "") : "";
    const validIssuer = !iss || cleanIss === expectedIssuer || cleanIss === cleanUrl || cleanIss === "supabase" || cleanIss.includes("supabase.co");
    const validAudience = !aud || (Array.isArray(aud) ? aud.includes("authenticated") : aud === "authenticated");

    const resolvedEmail =
      (typeof email === "string" && email) ||
      (typeof user_metadata?.email === "string" && user_metadata.email) ||
      null;

    if (!resolvedEmail || typeof exp !== "number" || exp <= now || (typeof nbf === "number" && nbf > (now + 60)) || !validIssuer || !validAudience) return null;

    return { email: resolvedEmail };
  } catch {
    return null;
  }
}

export function safeNextPath(value) {
  if (typeof value !== "string" || !value.startsWith("/") || value.startsWith("//") || value.includes("\\")) {
    return "/";
  }
  return value;
}

export function isPublicAuthPath(pathname) {
  return PUBLIC_AUTH_PATHS.has(pathname);
}

export function accessDeniedRedirect() {
  return PERSONAL_ACCESS_DENIED_URL;
}

/** The session cookie's value, or "" when absent or not decodable. */
export function readStudyToken(cookieHeader) {
  const match = (cookieHeader ?? "").match(/(?:^|;\s*)study_access_token=([^;]+)/);
  if (!match) return "";
  try {
    return decodeURIComponent(match[1]);
  } catch {
    return "";
  }
}

/**
 * The optional probe credential: a machine-checkable identity for the success
 * path.
 *
 * Every other probe in `scripts/check_study_live.py` proves the site is
 * correctly *blocked*; the branch that serves a chapter needs the owner's
 * Google session, so it was verified by unit tests alone — which leaves the
 * join (the middleware letting a valid session through and the edge serving
 * that file) unprobed, and that join is the only reason the site exists.
 *
 * With `STUDY_PROBE_TOKEN` set, a request whose cookie matches it is the
 * approved identity, so the live probe can assert 200 + the chapter's own
 * title in CI. Unset, this returns null for every input: the branch is inert
 * until an operator opts in, so shipping it changes no behaviour.
 *
 * The comparison is constant-time over padded byte arrays, length difference
 * included, because a secret compared with `===` leaks its prefix to timing.
 */
export function probeTokenSession(token, env) {
  const expected = env?.STUDY_PROBE_TOKEN;
  if (typeof expected !== "string" || expected.length === 0) return null;
  if (typeof token !== "string" || token.length === 0) return null;
  if (!matchesSecret(token, expected)) return null;
  return { email: ALLOWED_STUDY_EMAIL };
}

function matchesSecret(presented, expected) {
  const left = new TextEncoder().encode(presented);
  const right = new TextEncoder().encode(expected);
  let diff = left.length ^ right.length;
  const width = Math.max(left.length, right.length);
  for (let index = 0; index < width; index += 1) {
    diff |= (left[index] ?? 0) ^ (right[index] ?? 0);
  }
  return diff === 0;
}

/**
 * Turn a presented cookie into a session.
 *
 * A verification failure is still a *presented* session: the visitor holds a
 * cookie, so they reach the denial page rather than a login page that would
 * hand them another one. That rule lives here, not in the adapter, because it
 * is policy and the adapter's catch block was the only place it could hide.
 * Without a cookie the verifier is never called.
 */
export async function resolveSessionFromToken({ token, verifyToken }) {
  if (!token) return { email: null, hasToken: false };
  try {
    const user = await verifyToken(token);
    return { email: user && typeof user.email === "string" ? user.email : null, hasToken: true };
  } catch {
    return { email: null, hasToken: true };
  }
}

/**
 * The whole gate decision, as data, with the session resolved lazily.
 *
 * `_middleware.ts` only turns this into a Response. Keeping the decision out of
 * the TypeScript adapter is what makes the branch that matters testable: the
 * one that serves content to a valid session cannot be exercised by a live
 * probe without the owner's Google account, and it is the branch the site
 * exists for.
 *
 * `resolveSession` is called only when the answer depends on it, so a public
 * auth path never pays for a token verification round trip.
 */
export async function decideAccess({
  hostname,
  pathname,
  search = "",
  resolveSession,
  canonicalOrigin = STUDY_CANONICAL_ORIGIN,
}) {
  if (isPagesDevHost(hostname)) {
    return { action: "canonical", status: 308, location: `${canonicalOrigin}${pathname}${search}` };
  }
  if (isPublicAuthPath(pathname)) return { action: "public", status: 200, location: "" };

  const { email, hasToken } = await resolveSession();
  if (email && isAllowedStudyEmail(email)) return { action: "allow", status: 200, location: "" };
  if (hasToken) return { action: "denied", status: 302, location: accessDeniedRedirect() };

  const next = safeNextPath(`${pathname}${search}`);
  return { action: "login", status: 302, location: `/auth/login.html?next=${encodeURIComponent(next)}` };
}

/**
 * Turn a decision into the Response the edge sends.
 *
 * Kept here rather than in the middleware so the mapping is pinned by tests
 * too — the adapter should be glue, not policy.
 */
export function respondTo(decision, next) {
  if (decision.action === "public" || decision.action === "allow") return next();
  const headers = { Location: decision.location, "Cache-Control": "no-store" };
  if (decision.action === "denied") {
    headers["Set-Cookie"] = "study_access_token=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0";
  }
  return new Response(null, {
    status: decision.status,
    headers,
  });
}

export async function fetchSupabaseUser(accessToken, env) {
  const config = resolveSupabaseConfig(env);
  if (!accessToken || !config.url) return null;

  // Auto-populate JWKS URL if missing
  if (!config.jwksUrl && config.url) {
    config.jwksUrl = `${config.url.replace(/\/$/, "")}/auth/v1/.well-known/jwks.json`;
  }
  // If anonKey is missing and pointing to the known Buildora Supabase project, supply publishable key
  if (!config.anonKey && config.url.includes("ejbghgpatpfubxltkpde")) {
    config.anonKey = "sb_publishable_I42JurXGACj13HhJ1vmjdQ_lwTO8IK8";
  }

  // 1. Try Supabase /auth/v1/user endpoint first if anonKey is available
  if (config.anonKey) {
    try {
      const response = await fetch(`${config.url.replace(/\/$/, "")}/auth/v1/user`, {
        headers: {
          apikey: config.anonKey,
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (response.ok) {
        const user = await response.json();
        const email =
          (user && typeof user === "object" && typeof user.email === "string" && user.email) ||
          (user && typeof user === "object" && typeof user.user_metadata?.email === "string" && user.user_metadata.email) ||
          null;
        if (email) return { ...user, email };
      }
    } catch {
      // Fall through to verifyAsymmetricToken
    }
  }

  // 2. Cryptographic token verification against JWKS (local & offline-verifiable)
  return verifyAsymmetricToken(accessToken, config);
}
