import { safeNextPath } from "../_lib/study-access.mjs";

type Env = { SUPABASE_URL?: string };

export const onRequestGet = async ({ request, env }: { request: Request; env: Env }) => {
  if (!env.SUPABASE_URL) return new Response("Study sign-in is not configured.", { status: 503 });

  const requestUrl = new URL(request.url);
  const next = safeNextPath(requestUrl.searchParams.get("next"));
  const callback = new URL("/auth/callback.html", requestUrl.origin);

  const authorize = new URL(`${env.SUPABASE_URL.replace(/\/$/, "")}/auth/v1/authorize`);
  authorize.searchParams.set("provider", "google");
  authorize.searchParams.set("redirect_to", callback.toString());
  authorize.searchParams.set("state", next);
  return Response.redirect(authorize.toString(), 302);
};
