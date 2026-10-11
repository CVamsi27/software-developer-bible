/**
 * The environment variables the study edge reads.
 *
 * One declaration, imported by the middleware and every auth route. Each used
 * to spell out its own copy, so adding a variable meant finding all of them —
 * and a route that forgot one would read `undefined` with no type error,
 * because the copies were structurally different types that happened to be
 * assignable.
 *
 * Note the two families: the `SUPABASE_*` names this project sets in Pages, and
 * the `NEXT_PUBLIC_*`/publishable aliases the personal app already uses, which
 * `resolveSupabaseConfig()` accepts so one dashboard configuration serves both.
 */
export type StudyEnv = {
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  NEXT_PUBLIC_SUPABASE_URL?: string;
  SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY?: string;
  NEXT_PUBLIC_SUPABASE_ANON_KEY?: string;
  SUPABASE_JWKS_URL?: string;
  /** Exact Google account authorized to read the study site. */
  STUDY_ALLOWED_EMAIL?: string;
  /** Optional credential that lets the live probe verify the success path. */
  STUDY_PROBE_TOKEN?: string;
};
