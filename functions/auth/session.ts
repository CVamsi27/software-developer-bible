import { accessDeniedRedirect, fetchSupabaseUser, isAllowedStudyEmail, safeNextPath } from "../_lib/study-access.mjs";
import type { StudyEnv } from "../_lib/env.ts";

function json(body: unknown, init?: ResponseInit) {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...(init?.headers ?? {}) },
  });
}

export const onRequestPost = async ({ request, env }: { request: Request; env: StudyEnv }) => {
  let payload: { access_token?: unknown };
  try {
    payload = await request.json() as { access_token?: unknown };
  } catch {
    return json({ ok: false, reason: "invalid-request" }, { status: 400 });
  }

  const token = typeof payload.access_token === "string" ? payload.access_token : "";
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
