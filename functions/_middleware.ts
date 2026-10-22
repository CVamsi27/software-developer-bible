import {
  INTERCEPTED_PATHS,
  decideAccess,
  fetchSupabaseUser,
  probeTokenSession,
  readStudyToken,
  resolveSessionFromToken,
  respondTo,
} from "./_lib/study-access.mjs";
import type { StudyEnv } from "./_lib/env.ts";

type PagesContext = {
  request: Request;
  env: StudyEnv;
  next: () => Promise<Response>;
};

// Raw HTML for the OAuth callback page — the only copy. It used to exist twice
// more (an asset at `auth/callback.html`, a route at
// `functions/auth/callback.ts`), the same page duplicated, and both unreachable:
// this intercept answers first, so neither could ever have run. Do not
// reintroduce one. It is served here, not as an asset, because Pages
// canonicalizes a `.html` request with a 308 (`/auth/login.html` ->
// `/auth/login`), and that redirect is where the #access_token=... fragment
// was lost. It is styled with the same neutral tokens as `auth/login.html` —
// this page is shown mid-sign-in, directly after that one — and loads the same
// pre-paint theme script and Roboto face (both listed as public in
// `_lib/study-access.mjs`, because a signed-out visitor reads this page).
const CALLBACK_HTML = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">
    <meta name="theme-color" content="#ffffff">
    <title>Signing in // Buildora Study</title>
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="preload" href="/assets/fonts/Roboto-Variable.woff2" as="font" type="font/woff2" crossorigin>
    <script src="/assets/theme.js"></script>
    <style>
      @font-face {
        font-family: "Roboto";
        src: url("/assets/fonts/Roboto-Variable.woff2") format("woff2");
        font-style: normal;
        font-weight: 100 900;
        font-display: swap;
      }
      :root {
        color-scheme: light;
        --bg: #ffffff;
        --text: #1f1f1f;
        --muted: #5f6368;
        --heading: #1f1f1f;
        --border: #dadce0;
        --card: #ffffff;
        --link: #1a73e8;
        --action: #1a73e8;
        --action-text: #ffffff;
        --error: #d93025;
        --shadow: 0 24px 80px rgba(32, 33, 36, 0.08);
        font-family: "Roboto", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
        background: var(--bg);
        color: var(--text);
      }
      @media (prefers-color-scheme: dark) {
        :root:not([data-theme="light"]) {
          color-scheme: dark;
          --bg: #131314;
          --text: #e3e3e3;
          --muted: #9aa0a6;
          --heading: #f8f9fa;
          --border: #2b2c2e;
          --card: #1b1c1d;
          --link: #8ab4f8;
          --action: #8ab4f8;
          --action-text: #202124;
          --error: #f28b82;
          --shadow: 0 24px 80px rgba(0, 0, 0, 0.5);
        }
      }
      html[data-theme="dark"] {
        color-scheme: dark;
        --bg: #131314;
        --text: #e3e3e3;
        --muted: #9aa0a6;
        --heading: #f8f9fa;
        --border: #2b2c2e;
        --card: #1b1c1d;
        --link: #8ab4f8;
        --action: #8ab4f8;
        --action-text: #202124;
        --error: #f28b82;
        --shadow: 0 24px 80px rgba(0, 0, 0, 0.5);
      }
      html[data-theme="light"] { color-scheme: light; }
      * { box-sizing: border-box; }
      body { min-height: 100svh; margin: 0; display: grid; place-items: center; padding: 24px; background: var(--bg); }
      main {
        position: relative;
        width: min(100%, 480px);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: clamp(24px, 7vw, 48px);
        background: var(--card);
        box-shadow: var(--shadow);
      }
      .theme-slot { position: absolute; top: 10px; right: 10px; }
      .theme-toggle-btn {
        display: inline-flex; align-items: center; justify-content: center;
        width: 44px; height: 44px; padding: 0; border: 0; border-radius: 999px;
        background: transparent; color: var(--muted); cursor: pointer;
      }
      .theme-toggle-btn:hover { background: var(--border); color: var(--heading); }
      .theme-toggle-btn:focus-visible { outline: 3px solid var(--link); outline-offset: 3px; }
      .theme-toggle-btn svg { display: block; width: 18px; height: 18px; }
      h1 { margin: 0 0 12px; font-size: clamp(28px, 7vw, 38px); letter-spacing: -.02em; line-height: 1.1; color: var(--heading); }
      p { color: var(--muted); line-height: 1.6; }
      .error { color: var(--error); }
      .actions { margin-top: 24px; display: flex; flex-wrap: wrap; gap: 12px; }
      a.btn { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 18px; border: 1px solid var(--action); border-radius: 999px; background: var(--action); color: var(--action-text); font-weight: 600; font-size: 13px; text-decoration: none; }
      a.btn:hover { filter: brightness(0.94); }
      a.btn:focus-visible { outline: 3px solid var(--link); outline-offset: 3px; }
      a.btn-secondary { background: transparent; color: var(--muted); border: 1px solid var(--border); }
    </style>
  </head>
  <body>
    <main>
      <div class="theme-slot" data-theme-toggle-slot></div>
      <h1>Checking access…</h1>
      <p id="status">Securing your private study session.</p>
      <div id="actions" class="actions" style="display:none;">
        <a class="btn" href="/auth/login.html">Try signing in again</a>
        <a class="btn btn-secondary" href="https://personal.buildora.work/?study=access-denied">Go to Personal</a>
      </div>
    </main>
    <script>
      const query = new URLSearchParams(window.location.search);
      const rawHash = window.location.hash.startsWith("#") ? window.location.hash.slice(1) : window.location.hash;
      const fragment = new URLSearchParams(rawHash);
      const accessToken = fragment.get("access_token") || query.get("access_token");
      const code = query.get("code") || fragment.get("code");

      const getCookie = (name) => {
        const match = (document.cookie || "").match(new RegExp("(?:^|;\\\\s*)" + name + "=([^;]*)"));
        return match ? decodeURIComponent(match[1]) : "";
      };

      let storedNext = "";
      try {
        storedNext = sessionStorage.getItem("study_next_url") || localStorage.getItem("study_next_url") || "";
      } catch (e) {}

      const candidateNext =
        query.get("next") ||
        fragment.get("next") ||
        query.get("state") ||
        fragment.get("state") ||
        storedNext ||
        getCookie("study_next_url") ||
        "/";

      const isValidLocalPath = (val) =>
        typeof val === "string" && val.startsWith("/") && !val.startsWith("//") && !val.includes("\\\\");
      const resolvedNext = isValidLocalPath(candidateNext) ? candidateNext : "/";

      try {
        sessionStorage.removeItem("study_next_url");
        localStorage.removeItem("study_next_url");
      } catch (e) {}

      const status = document.getElementById("status");
      const actions = document.getElementById("actions");
      const denied = (message, autoRedirect = true) => {
        status.className = "error";
        status.textContent = message;
        if (actions) actions.style.display = "flex";
        if (autoRedirect) {
          window.setTimeout(() => { window.location.href = "https://personal.buildora.work/?study=access-denied"; }, 3500);
        }
      };
      const errorDesc = fragment.get("error_description") || query.get("error_description") || fragment.get("error") || query.get("error");
      if (errorDesc) {
        console.error("Auth error:", errorDesc);
        denied("Google authorization error: " + errorDesc + ". Redirecting.", true);
      } else if (!accessToken && !code) {
        console.error("No access token or auth code found in callback URL:", window.location.href);
        denied("No Google session was returned in the callback. Please try signing in again.", false);
      } else {
        fetch("/auth/session?next=" + encodeURIComponent(resolvedNext), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ access_token: accessToken, code: code, next: resolvedNext })
        }).then(async (response) => {
          const result = await response.json().catch(() => ({}));
          if (!response.ok || !result.ok) {
            console.error("Session exchange refused:", response.status, result);
            const isNotAllowed = result && result.reason === "not-allowed";
            const msg = isNotAllowed
              ? "Account " + (result.email || "this Google account") + " is not authorized for Study."
              : "Session verification failed: " + (result?.error || result?.reason || response.status) + ".";
            return denied(msg, isNotAllowed);
          }
          window.location.replace(result.next || resolvedNext || "/");
        }).catch((err) => {
          console.error("Network error exchanging session:", err);
          denied("The study session could not be secured due to a network error. Please try again.", false);
        });
      }
    </script>
  </body>
</html>`;

/**
 * The Cloudflare Pages adapter: parse the URL, hand the request to the policy,
 * send what it decides.
 */
export const onRequest = async ({ request, env, next }: PagesContext) => {
  const url = new URL(request.url);

  // Directly serve callback HTML to guarantee 0 redirects and preserve
  // #access_token=... The interception list lives once, in
  // `_lib/study-access.mjs` (`INTERCEPTED_PATHS`) — the live probe resolves
  // that declaration, so re-inlining the check here would detach it.
  if (INTERCEPTED_PATHS.includes(url.pathname)) {
    return new Response(CALLBACK_HTML, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store, no-cache, must-revalidate",
      },
    });
  }

  const decision = await decideAccess({
    hostname: url.hostname,
    pathname: url.pathname,
    search: url.search,
    allowedEmail: env.STUDY_ALLOWED_EMAIL,
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
