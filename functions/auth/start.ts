import { resolveSupabaseConfig, safeNextPath } from "../_lib/study-access.mjs";

type Env = {
  SUPABASE_URL?: string;
  NEXT_PUBLIC_SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_ANON_KEY?: string;
  SUPABASE_JWKS_URL?: string;
};

export const onRequestGet = async ({ request, env }: { request: Request; env: Env }) => {
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
