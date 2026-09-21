import { accessDeniedRedirect, fetchSupabaseUser, isAllowedStudyEmail, isPagesDevHost, isPublicAuthPath, safeNextPath } from "./_lib/study-access.mjs";

type StudyEnv = {
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  NEXT_PUBLIC_SUPABASE_URL?: string;
  SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_ANON_KEY?: string;
  SUPABASE_JWKS_URL?: string;
};

type PagesContext = {
  request: Request;
  env: StudyEnv;
  next: () => Promise<Response>;
};

function redirect(location: string, status = 302) {
  return new Response(null, { status, headers: { Location: location, "Cache-Control": "no-store" } });
}

function readAccessToken(request: Request) {
  const cookieHeader = request.headers.get("Cookie") ?? "";
  const match = cookieHeader.match(/(?:^|;\s*)study_access_token=([^;]+)/);
  if (!match) return "";
  try {
    return decodeURIComponent(match[1]);
  } catch {
    return "";
  }
}

async function currentEmail(request: Request, env: StudyEnv) {
  const token = readAccessToken(request);
  const user = await fetchSupabaseUser(token, env);
  return user && typeof user.email === "string" ? user.email : null;
}

export const onRequest = async ({ request, env, next }: PagesContext) => {
  const url = new URL(request.url);
  if (isPagesDevHost(url.hostname)) {
    const canonical = new URL(`${url.pathname}${url.search}`, "https://study.buildora.work");
    return redirect(canonical.toString(), 308);
  }
  if (isPublicAuthPath(url.pathname)) return next();

  let email: string | null = null;
  try {
    email = await currentEmail(request, env);
  } catch {
    email = null;
  }

  if (email && isAllowedStudyEmail(email)) return next();
  if (readAccessToken(request)) return redirect(accessDeniedRedirect());

  const requestedPath = safeNextPath(`${url.pathname}${url.search}`);
  return redirect(`/auth/login.html?next=${encodeURIComponent(requestedPath)}`);
};
