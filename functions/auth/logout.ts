export const onRequestGet = async ({ request }: { request: Request }) => {
  const login = new URL("/auth/login.html", request.url);
  return new Response(null, {
    status: 302,
    headers: {
      Location: login.toString(),
      "Cache-Control": "no-store",
      "Set-Cookie": "study_access_token=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0",
    },
  });
};
