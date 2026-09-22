import {
  decideAccess,
  fetchSupabaseUser,
  probeTokenSession,
  readStudyToken,
  resolveSessionFromToken,
  respondTo,
} from "./_lib/study-access.mjs";

type StudyEnv = {
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  NEXT_PUBLIC_SUPABASE_URL?: string;
  SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_ANON_KEY?: string;
  SUPABASE_JWKS_URL?: string;
  STUDY_PROBE_TOKEN?: string;
};

type PagesContext = {
  request: Request;
  env: StudyEnv;
  next: () => Promise<Response>;
};

/**
 * The Cloudflare Pages adapter: parse the URL, hand the request to the policy,
 * send what it decides. There is no branch here to get wrong — every rule lives
 * in `_lib/study-access.mjs`, where the branch that serves content to a valid
 * session (unreachable by a live probe without the owner's account) is pinned
 * by tests. The cookie is read inside `resolveSession` so a public path or the
 * fallback host never pays for a token round trip.
 */
export const onRequest = async ({ request, env, next }: PagesContext) => {
  const url = new URL(request.url);

  const decision = await decideAccess({
    hostname: url.hostname,
    pathname: url.pathname,
    search: url.search,
    resolveSession: () =>
      resolveSessionFromToken({
        token: readStudyToken(request.headers.get("Cookie")),
        // The probe credential is checked first and only exists when the
        // operator sets it; otherwise this is the ordinary Supabase path.
        verifyToken: (token) =>
          probeTokenSession(token, env) ?? fetchSupabaseUser(token, env),
      }),
  });

  return respondTo(decision, next);
};
