import { resolveSupabaseConfig, safeNextPath } from "../_lib/study-access.mjs";
import type { StudyEnv } from "../_lib/env.ts";

export const onRequestGet = async ({ request, env }: { request: Request; env: StudyEnv }) => {
  const { url: supabaseUrl } = resolveSupabaseConfig(env);
  if (!supabaseUrl) return new Response("Study sign-in is not configured. Set the Supabase URL in Cloudflare Pages production variables.", { status: 503 });

  const requestUrl = new URL(request.url);
  const next = safeNextPath(requestUrl.searchParams.get("next"));
  const callback = new URL("/auth/callback.html", requestUrl.origin);

  const authorize = new URL(`${supabaseUrl.replace(/\/$/, "")}/auth/v1/authorize`);
  authorize.searchParams.set("provider", "google");
  authorize.searchParams.set("redirect_to", callback.toString());
  authorize.searchParams.set("state", next);
  return Response.redirect(authorize.toString(), 302);
};
