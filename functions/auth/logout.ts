import { clearStudySessionCookies } from "../_lib/study-access.mjs";

export const onRequestGet = async ({ request }: { request: Request }) => {
  const login = new URL("/auth/login.html", request.url);
  const headers = new Headers({
    Location: login.toString(),
    "Cache-Control": "no-store",
  });
  for (const cookie of clearStudySessionCookies()) headers.append("Set-Cookie", cookie);
  return new Response(null, {
    status: 302,
    headers,
  });
};
