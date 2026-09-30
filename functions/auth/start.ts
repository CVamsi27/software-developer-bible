import { readStudyNextCookie, resolveSupabaseConfig, safeNextPath } from "../_lib/study-access.mjs";
import type { StudyEnv } from "../_lib/env.ts";

export const onRequestGet = async ({ request, env }: { request: Request; env: StudyEnv }) => {
  const { url: supabaseUrl } = resolveSupabaseConfig(env);
  if (!supabaseUrl) return new Response("Study sign-in is not configured. Set the Supabase URL in Cloudflare Pages production variables.", { status: 503 });

  const requestUrl = new URL(request.url);
  const cookieNext = readStudyNextCookie(request.headers.get("Cookie"));
  const next = safeNextPath(requestUrl.searchParams.get("next") || cookieNext || "/");
  const callback = new URL("/auth/callback.html", requestUrl.origin);

  const authorize = new URL(`${supabaseUrl.replace(/\/$/, "")}/auth/v1/authorize`);
  authorize.searchParams.set("provider", "google");
  authorize.searchParams.set("redirect_to", callback.toString());
  authorize.searchParams.set("state", next);

  return new Response(null, {
    status: 302,
    headers: {
      Location: authorize.toString(),
      "Set-Cookie": `study_next_url=${encodeURIComponent(next)}; Path=/; SameSite=Lax; Max-Age=1800`,
    },
  });
};
