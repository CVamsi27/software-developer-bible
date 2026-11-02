import {
  accessDeniedRedirect,
  fetchSupabaseUser,
  isAllowedStudyEmail,
  readStudyNextCookie,
  resolveSupabaseConfig,
  safeNextPath,
  studyAccessCookie,
  studyRefreshCookie,
} from "../_lib/study-access.mjs";
import type { StudyEnv } from "../_lib/env.ts";

function json(body: unknown, init?: ResponseInit) {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...(init?.headers ?? {}) },
  });
}

export const onRequestPost = async ({ request, env }: { request: Request; env: StudyEnv }) => {
  let payload: { access_token?: unknown; refresh_token?: unknown; code?: unknown; next?: unknown };
  try {
    payload = await request.json() as { access_token?: unknown; refresh_token?: unknown; code?: unknown; next?: unknown };
  } catch {
    return json({ ok: false, reason: "invalid-request" }, { status: 400 });
  }

  let token = typeof payload.access_token === "string" ? payload.access_token : "";
  let refreshToken = typeof payload.refresh_token === "string" ? payload.refresh_token : "";
  const code = typeof payload.code === "string" ? payload.code : "";

  if (!token && code) {
    const { url: supabaseUrl, anonKey } = resolveSupabaseConfig(env);
    if (supabaseUrl && anonKey) {
      try {
        const tokenRes = await fetch(`${supabaseUrl}/auth/v1/token?grant_type=pkce`, {
          method: "POST",
          headers: { apikey: anonKey, "Content-Type": "application/json" },
          body: JSON.stringify({ auth_code: code }),
        });
        if (tokenRes.ok) {
          const tokenData = await tokenRes.json() as any;
          if (typeof tokenData?.access_token === "string") {
            token = tokenData.access_token;
          }
          if (typeof tokenData?.refresh_token === "string") {
            refreshToken = tokenData.refresh_token;
          }
        }
      } catch {
        // Fall through
      }
    }
  }

  let user: { email?: unknown } | null;
  try {
    user = await fetchSupabaseUser(token, env);
  } catch {
    user = null;
  }
  if (!user || !isAllowedStudyEmail(user.email, env.STUDY_ALLOWED_EMAIL)) {
    return json({ ok: false, reason: "not-allowed", redirect: accessDeniedRedirect() }, { status: 403 });
  }

  const queryNext = new URL(request.url).searchParams.get("next");
  const payloadNext = typeof payload?.next === "string" ? payload.next : null;
  const cookieNext = readStudyNextCookie(request.headers.get("Cookie"));
  const rawTarget = (queryNext && queryNext !== "/") ? queryNext : (payloadNext || cookieNext || queryNext || "/");
  const next = safeNextPath(rawTarget);

  const headers = new Headers({
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  headers.append("Set-Cookie", studyAccessCookie(token));
  if (refreshToken) headers.append("Set-Cookie", studyRefreshCookie(refreshToken));

  return new Response(JSON.stringify({ ok: true, email: user.email, next }), {
    status: 200,
    headers,
  });
};
