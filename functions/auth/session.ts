import { accessDeniedRedirect, fetchSupabaseUser, isAllowedStudyEmail, resolveSupabaseConfig, safeNextPath } from "../_lib/study-access.mjs";
import type { StudyEnv } from "../_lib/env.ts";

function json(body: unknown, init?: ResponseInit) {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...(init?.headers ?? {}) },
  });
}

export const onRequestPost = async ({ request, env }: { request: Request; env: StudyEnv }) => {
  let payload: { access_token?: unknown; code?: unknown };
  try {
    payload = await request.json() as { access_token?: unknown; code?: unknown };
  } catch {
    return json({ ok: false, reason: "invalid-request" }, { status: 400 });
  }

  let token = typeof payload.access_token === "string" ? payload.access_token : "";
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
  if (!user || !isAllowedStudyEmail(user.email)) {
    return json({ ok: false, reason: "not-allowed", redirect: accessDeniedRedirect() }, { status: 403 });
  }

  const next = safeNextPath(new URL(request.url).searchParams.get("next"));
  return json(
    { ok: true, email: user.email, next },
    {
      headers: {
        "Set-Cookie": `study_access_token=${encodeURIComponent(token)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=3600`,
      },
    },
  );
};
