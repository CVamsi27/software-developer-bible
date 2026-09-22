const ALLOWED_STUDY_EMAIL = "cvamsik99@gmail.com";
const PERSONAL_ACCESS_DENIED_URL = "https://personal.buildora.work/?study=access-denied";
const PRODUCTION_PAGES_HOST = "software-developer-bible.pages.dev";
export const STUDY_CANONICAL_ORIGIN = "https://study.buildora.work";
const PUBLIC_AUTH_PATHS = new Set([
  "/auth/login.html",
  "/auth/login",
  "/auth/callback.html",
  "/auth/callback",
  "/auth/start",
  "/auth/session",
  "/auth/logout",
  "/favicon.svg",
]);

export function normalizeEmail(value) {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

export function isAllowedStudyEmail(value) {
  return normalizeEmail(value) === ALLOWED_STUDY_EMAIL;
}

export function isPagesDevHost(value) {
  return typeof value === "string" && value.trim().toLowerCase() === PRODUCTION_PAGES_HOST;
}

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
  return {
    url,
    anonKey:
      env?.SUPABASE_ANON_KEY ||
      env?.SUPABASE_PUBLISHABLE_KEY ||
      env?.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
      env?.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
      "",
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
  if (!parsed || !config.jwksUrl) return null;

  const algorithm = parsed.header.alg;
  const keyAlgorithm =
    algorithm === "ES256"
      ? { name: "ECDSA", namedCurve: "P-256" }
      : algorithm === "RS256"
        ? { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }
        : null;
  if (!keyAlgorithm || typeof parsed.header.kid !== "string") return null;

  const jwksResponse = await fetch(config.jwksUrl);
  if (!jwksResponse.ok) return null;
  const jwks = await jwksResponse.json();
  const jwk = Array.isArray(jwks?.keys)
    ? jwks.keys.find((key) => key?.kid === parsed.header.kid && key?.alg === algorithm)
    : null;
  if (!jwk) return null;

  const cryptoKey = await crypto.subtle.importKey("jwk", jwk, keyAlgorithm, false, ["verify"]);
  const verifyAlgorithm = algorithm === "ES256" ? { name: "ECDSA", hash: "SHA-256" } : keyAlgorithm;
  const valid = await crypto.subtle.verify(verifyAlgorithm, cryptoKey, parsed.signature, parsed.signingInput);
  if (!valid) return null;

  const now = Math.floor(Date.now() / 1000);
  const { exp, nbf, iss, aud, email } = parsed.payload ?? {};
  const expectedIssuer = `${config.url.replace(/\/$/, "")}/auth/v1`;
  const validAudience = Array.isArray(aud) ? aud.includes("authenticated") : aud === "authenticated";
  if (typeof email !== "string" || typeof exp !== "number" || exp <= now || (typeof nbf === "number" && nbf > now) || iss !== expectedIssuer || !validAudience) return null;

  return { email };
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
  return new Response(null, {
    status: decision.status,
    headers: { Location: decision.location, "Cache-Control": "no-store" },
  });
}

export async function fetchSupabaseUser(accessToken, env) {
  const config = resolveSupabaseConfig(env);
  if (!accessToken || !config.url) return null;

  if (!config.anonKey) return verifyAsymmetricToken(accessToken, config);

  const response = await fetch(`${config.url.replace(/\/$/, "")}/auth/v1/user`, {
    headers: {
      apikey: config.anonKey,
      Authorization: `Bearer ${accessToken}`,
    },
  });
  if (!response.ok) return null;

  const user = await response.json();
  return user && typeof user === "object" && typeof user.email === "string" ? user : null;
}
