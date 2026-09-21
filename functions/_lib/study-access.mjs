const ALLOWED_STUDY_EMAIL = "cvamsik99@gmail.com";
const PERSONAL_ACCESS_DENIED_URL = "https://personal.buildora.work/?study=access-denied";
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

export async function fetchSupabaseUser(accessToken, env) {
  if (!accessToken || !env?.SUPABASE_URL || !env?.SUPABASE_ANON_KEY) return null;

  const response = await fetch(`${env.SUPABASE_URL.replace(/\/$/, "")}/auth/v1/user`, {
    headers: {
      apikey: env.SUPABASE_ANON_KEY,
      Authorization: `Bearer ${accessToken}`,
    },
  });
  if (!response.ok) return null;

  const user = await response.json();
  return user && typeof user === "object" && typeof user.email === "string" ? user : null;
}
