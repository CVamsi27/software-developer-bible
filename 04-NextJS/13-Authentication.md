---
section: Next.js
category: Frontend
tags: [concept]
---

# Authentication in Next.js

## TL;DR

Next.js authentication spans middleware (edge auth checks), Server Components (server-side session validation), Client Components (auth state), and Route Handlers (token endpoints). Use sessions (server-stored) for web apps, JWTs for cross-domain APIs.

## Why It Matters

Senior engineers design auth that works across SSR, RSC, and CSR. They use middleware for redirects, server components for protected data fetching, and libraries like Auth.js (NextAuth), Clerk, or custom JWT. They know to never trust client-side auth checks and to use HTTP-only cookies for sessions.

## Definition

**Authentication** in Next.js involves verifying user identity and managing access to protected resources across different rendering strategies (SSR, SSG, CSR, ISR). Next.js supports authentication through middleware for edge-based route protection, server components for server-side session validation, client components for client-side auth state, and API route handlers for token issuance and verification.

## Why Do We Need It?

1. **Route protection** — Prevent unauthorized access to pages and API routes
2. **Role-based access** — Control what authenticated users can see and do
3. **Mixed rendering** — Auth must work across SSR, SSG, CSR, and ISR
4. **Security** — Protect against CSRF, XSS, and session hijacking
5. **UX** — Seamless login/logout, persistent sessions, redirect handling

## How It Works

### Auth Architecture in Next.js

```text
Next.js Auth Architecture:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                      AUTH FLOW DIAGRAM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Browser Request                                                 │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  1. Middleware (Edge Runtime)                             │   │
│  │     ├── Check session cookie / JWT token                  │   │
│  │     ├── Validate against protected routes list            │   │
│  │     ├── Redirect to login if unauthenticated              │   │
│  │     ├── Rewrite based on user role                        │   │
│  │     └── Set user headers for downstream consumption       │   │
│  └──────────────────────────────────────────────────────────┘   │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  2. Server Components (React Server Components)           │   │
│  │     ├── Read cookies/headers for session                  │   │
│  │     ├── Validate session server-side                      │   │
│  │     ├── Fetch user data from database                     │   │
│  │     ├── Render user-specific content                      │   │
│  │     └── Fetch data on behalf of the authenticated user    │   │
│  └──────────────────────────────────────────────────────────┘   │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  3. Client Components ('use client')                      │   │
│  │     ├── Auth context provider wraps the app               │   │
│  │     ├── useSession / useUser hooks for auth state         │   │
│  │     ├── Protected client-side navigation                  │   │
│  │     └── Token refresh and session management              │   │
│  └──────────────────────────────────────────────────────────┘   │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  4. Route Handlers (API Routes)                           │   │
│  │     ├── Login endpoint → issue token/session              │   │
│  │     ├── Logout endpoint → clear session                   │   │
│  │     ├── Register endpoint → create user                   │   │
│  │     ├── Verify endpoint → validate token                  │   │
│  │     └── Refresh endpoint → rotate tokens                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### Session vs JWT

```text
Session-Based Auth:
═══════════════════════════════════════════════════════════════

├── Server stores session in DB/Redis
├── Client gets httpOnly cookie with session ID
├── Pros: Easy to revoke, no token size limits
├── Cons: Requires server-side storage, scales less
└── Best for: Server-rendered apps, traditional web apps

JWT-Based Auth:
═══════════════════════════════════════════════════════════════

├── Token contains user info + claims (signed)
├── Client stores token in httpOnly cookie or memory
├── Pros: Stateless, no server storage needed
├── Cons: Hard to revoke, token size, expiry management
└── Best for: APIs, SPAs, mobile apps

Next.js Recommendation:
├── Use httpOnly cookies (XSS-safe) for token storage
├── Use middleware for edge-based validation
├── Use NextAuth.js/Auth.js for production apps
└── Avoid localStorage (vulnerable to XSS)

```

## Code Examples

### 1. Auth Middleware (Route Protection)

```typescript
// middleware.ts — root of project
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const sessionToken = request.cookies.get('session-token')?.value;
  const { pathname } = request.nextUrl;

  // Public routes (no auth required)
  const publicRoutes = ['/login', '/register', '/forgot-password', '/api/auth'];
  const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route));

  // Static files and assets
  const isStaticAsset = pathname.startsWith('/_next') ||
    pathname.startsWith('/static') ||
    pathname === '/favicon.ico';

  // Allow access to public routes and static assets
  if (isPublicRoute || isStaticAsset) {
    // Redirect authenticated users away from login
    if (sessionToken && pathname === '/login') {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    return NextResponse.next();
  }

  // Protected routes — redirect to login
  if (!sessionToken) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### 2. JWT Token Based Auth

```typescript
// lib/auth.ts — JWT utilities
import { SignJWT, jwtVerify } from 'jose';

const JWT_SECRET = new TextEncoder().encode(
  process.env.JWT_SECRET || 'your-secret-key-min-32-chars'
);

export interface JWTPayload {
  userId: string;
  email: string;
  role: 'user' | 'admin';
}

export async function createToken(payload: JWTPayload): Promise<string> {
  return new SignJWT({ ...payload })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(JWT_SECRET);
}

export async function verifyToken(token: string): Promise<JWTPayload | null> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET);
    return payload as unknown as JWTPayload;
  } catch {
    return null;
  }
}

// app/api/auth/login/route.ts — Login API
import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { createToken } from '@/lib/auth';

export async function POST(request: Request) {
  const { email, password } = await request.json();

  // Verify credentials (replace with DB lookup)
  const user = await authenticateUser(email, password);
  if (!user) {
    return NextResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    );
  }

  // Create JWT
  const token = await createToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  // Set httpOnly cookie
  const response = NextResponse.json({ user: { id: user.id, email: user.email } });
  response.cookies.set('session-token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
    path: '/',
  });

  return response;
}

// app/api/auth/logout/route.ts — Logout
export async function POST() {
  const response = NextResponse.json({ success: true });
  response.cookies.delete('session-token');
  return response;
}
```

### 3. Server-Side Auth in Server Components

```typescript
// lib/server-auth.ts
import { cookies } from 'next/headers';
import { verifyToken, JWTPayload } from '@/lib/auth';

export async function getServerSession(): Promise<JWTPayload | null> {
  const cookieStore = await cookies();
  const token = cookieStore.get('session-token')?.value;

  if (!token) return null;
  return verifyToken(token);
}

// app/dashboard/page.tsx — Server Component
import { redirect } from 'next/navigation';
import { getServerSession } from '@/lib/server-auth';

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session) {
    redirect('/login');
  }

  // Fetch user-specific data
  const userData = await fetchUserData(session.userId);

  return (
    <div>
      <h1>Welcome back, {userData.name}!</h1>
      <p>Email: {session.email}</p>
      <p>Role: {session.role}</p>
      {/* Server-rendered dashboard content */}
      <UserDashboard data={userData} />
    </div>
  );
}

// app/admin/page.tsx — Role-based server component
export default async function AdminPage() {
  const session = await getServerSession();

  if (!session || session.role !== 'admin') {
    redirect('/unauthorized');
  }

  return <AdminPanel />;
}
```

### 4. Client-Side Auth with Context

```typescript
// lib/auth-context.tsx
'use client';

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check session on mount
  useEffect(() => {
    fetch('/api/auth/session')
      .then(res => res.json())
      .then(data => {
        if (data.user) setUser(data.user);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error);
    }

    const data = await res.json();
    setUser(data.user);
    router.push('/dashboard');
  }, [router]);

  const logout = useCallback(async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    setUser(null);
    router.push('/login');
  }, [router]);

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      login,
      logout,
      isAuthenticated: !!user,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// app/layout.tsx — Wrap app with AuthProvider
import { AuthProvider } from '@/lib/auth-context';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}

// Usage in client component
const ProtectedPage = () => {
  const { user, loading, logout } = useAuth();

  if (loading) return <Spinner />;
  if (!user) redirect('/login');

  return (
    <div>
      <p>Welcome, {user.name}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

### 5. NextAuth.js / Auth.js Integration

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import GithubProvider from 'next-auth/providers/github';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';

const handler = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });

        if (!user) return null;

        const isValid = await verifyPassword(credentials.password, user.password);
        if (!isValid) return null;

        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],
  session: { strategy: 'jwt', maxAge: 30 * 24 * 60 * 60 }, // 30 days
  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.role = token.role as string;
        session.user.id = token.id as string;
      }
      return session;
    },
  },
});

export { handler as GET, handler as POST };

// components/AuthButtons.tsx — Client component
'use client';
import { signIn, signOut, useSession } from 'next-auth/react';

export function AuthButtons() {
  const { data: session } = useSession();

  if (session) {
    return (
      <div>
        <p>Signed in as {session.user?.email}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => signIn('github')}>Sign in with GitHub</button>
      <button onClick={() => signIn('google')}>Sign in with Google</button>
    </div>
  );
}

// app/layout.tsx — Add SessionProvider
import { SessionProvider } from 'next-auth/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
```

### 6. Role-Based Access Control

```typescript
// lib/authorization.ts
import { getServerSession } from './server-auth';

type Role = 'user' | 'admin' | 'superadmin';

const roleHierarchy: Record<Role, number> = {
  user: 1,
  admin: 2,
  superadmin: 3,
};

export function hasRole(userRole: Role, requiredRole: Role): boolean {
  return roleHierarchy[userRole] >= roleHierarchy[requiredRole];
}

// Middleware-based RBAC
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { verifyToken } from '@/lib/auth';

const routePermissions: Record<string, Role[]> = {
  '/admin': ['admin', 'superadmin'],
  '/admin/users': ['superadmin'],
  '/dashboard': ['user', 'admin', 'superadmin'],
};

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('session-token')?.value;
  const { pathname } = request.nextUrl;

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  const payload = await verifyToken(token);
  if (!payload) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Check role-based access
  for (const [route, allowedRoles] of Object.entries(routePermissions)) {
    if (pathname.startsWith(route)) {
      if (!allowedRoles.includes(payload.role as Role)) {
        return NextResponse.redirect(new URL('/unauthorized', request.url));
      }
      break;
    }
  }

  return NextResponse.next();
}
```

### 7. API Route Protection

```typescript
// lib/api-auth.ts
import { NextResponse } from 'next/server';
import { verifyToken, JWTPayload } from '@/lib/auth';

export async function authenticateApi(
  request: Request
): Promise<{ payload: JWTPayload; response: null } | { payload: null; response: NextResponse }> {
  const token = request.headers.get('authorization')?.replace('Bearer ', '');

  if (!token) {
    return {
      payload: null,
      response: NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      ),
    };
  }

  const payload = await verifyToken(token);
  if (!payload) {
    return {
      payload: null,
      response: NextResponse.json(
        { error: 'Invalid or expired token' },
        { status: 401 }
      ),
    };
  }

  return { payload, response: null };
}

// app/api/users/route.ts — Protected API route
import { NextResponse } from 'next/server';
import { authenticateApi } from '@/lib/api-auth';

export async function GET(request: Request) {
  const { payload, response } = await authenticateApi(request);
  if (response) return response; // Unauthorized

  // Only admins can list all users
  if (payload.role !== 'admin') {
    return NextResponse.json(
      { error: 'Forbidden' },
      { status: 403 }
    );
  }

  const users = await fetchAllUsers();
  return NextResponse.json({ users });
}
```

### 8. CSRF Protection

```typescript
// lib/csrf.ts
import { createToken, verifyToken } from '@/lib/auth';

const CSRF_SECRET = process.env.CSRF_SECRET || 'csrf-secret';

export async function generateCsrfToken(): Promise<string> {
  return createToken({ userId: 'csrf', email: '', role: 'user' });
}

export async function validateCsrfToken(token: string): Promise<boolean> {
  const payload = await verifyToken(token);
  return payload !== null && payload.userId === 'csrf';
}

// middleware.ts — CSRF check for mutations
export async function middleware(request: NextRequest) {
  if (request.method === 'POST' || request.method === 'PUT' || request.method === 'DELETE') {
    const csrfToken = request.headers.get('x-csrf-token');
    if (!csrfToken || !(await validateCsrfToken(csrfToken))) {
      return NextResponse.json(
        { error: 'CSRF token validation failed' },
        { status: 403 }
      );
    }
  }
  return NextResponse.next();
}
```

## Real-World Use Cases

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **Simple Auth** | Small apps, prototypes | JWT in httpOnly cookie + middleware |
| **NextAuth.js** | Production apps, OAuth | Social login, credentials, database sessions |
| **Clerk/Auth0** | Enterprise, multi-tenant | Pre-built UI, MFA, SSO, user management |
| **Iron Session** | Server-rendered apps | Encrypted session cookies, no DB needed |
| **Custom JWT** | API-heavy apps | Stateless tokens, custom claims |

### NextAuth.js vs Custom vs Auth Provider

| Feature | NextAuth.js | Custom | Auth0 / Clerk |
|---------|:-----------:|:------:|:-------------:|
| Setup time | Fast | Slow | Fastest |
| Flexibility | Moderate | Full | Limited |
| OAuth providers | 80+ built-in | Manual | Built-in |
| Database | Required | Optional | Included |
| MFA | ❌ | Manual | ✅ |
| UI components | Basic | Custom | Complete |
| Cost | Free | Free | Paid tiers |
| Self-hosted | ✅ | ✅ | ❌ |

## Common Mistakes

### 1. Storing Tokens in localStorage

```typescript
// ❌ BAD: XSS vulnerable
localStorage.setItem('token', jwtToken);

// ✅ GOOD: httpOnly cookie (inaccessible to JavaScript)
// Server-side: Set cookie with httpOnly flag
response.cookies.set('session-token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'lax',
});
```

### 2. Not Validating on Server

```typescript
// ❌ BAD: Client-only check
'use client';
const Dashboard = () => {
  const { user } = useAuth();
  if (!user) return null; // Data is still in the HTML!
  return <SensitiveData />;
};

// ✅ GOOD: Server-side validation
// Server Component validates before rendering
const Dashboard = async () => {
  const session = await getServerSession();
  if (!session) redirect('/login');
  return <SensitiveData userId={session.userId} />;
};
```

### 3. Mixing Rendering Strategies Incorrectly

```typescript
// ❌ BAD: Assuming session in SSG
export async function getStaticProps() {
  // SSG runs at build time — no user session!
  const session = await getSession(); // ❌ Always null
  return { props: { session } };
}

// ✅ GOOD: Use client-side fetching for SSG
// The page is static, session is checked client-side
```

### 4. Exposing Protected Data in Client Bundle

```typescript
// ❌ BAD: Server action returns too much data
async function getUserData() {
  return {
    id: 1,
    name: 'Alice',
    ssn: 'XXX-XX-XXXX', // ❌ Exposed!
    creditCard: 'XXXX',  // ❌ Exposed!
  };
}

// ✅ GOOD: Only return what's needed
async function getUserProfile() {
  const user = await db.user.findUnique({ where: { id: userId } });
  return {
    name: user.name,
    email: user.email,
    // Only safe-to-expose fields
  };
}
```

## Best Practices

1. **Use httpOnly cookies** for token storage — prevents XSS token theft

2. **Validate on the server** — Always check auth in Server Components and API routes

3. **Use NextAuth.js for production** — Battle-tested, handles OAuth, sessions, CSRF

4. **Protect at the edge** — Use middleware for fast route protection

5. **Implement CSRF protection** — For mutations on cookie-based auth

6. **Handle token refresh** — Implement refresh token rotation for long sessions

7. **Rate limit auth endpoints** — Prevent brute force attacks

8. **Use secure headers** — Content-Security-Policy, Strict-Transport-Security

9. **Short session expiry** — 15-30 minutes for access tokens, 7 days for refresh

10. **Audit auth flows** — Log login attempts and suspicious activity

## Summary

Authentication in Next.js spans middleware (edge-based route protection), Server Components (server-side session validation), and Client Components (auth state and UX). The recommended approach is NextAuth.js for production apps with httpOnly cookies for token storage, middleware for route protection, and Server Components for data access control.

## Cheat Sheet

```text
Next.js Auth Key Points:
├── Middleware: Edge-based route protection
├── Server Components: Server-side session validation
├── Client Components: Auth context + UX
├── Route Handlers: Login/logout/register endpoints
├── Cookies: Use httpOnly, secure, sameSite
└── Never: Store tokens in localStorage

Recommended Stack:
├── NextAuth.js (Auth.js) → Full auth solution
├── httpOnly cookies → Token storage
├── Middleware → Route protection
├── Server Components → Data access control
├── Client Components → Auth UI state
└── Rate limiting → Brute force prevention

Security Checklist:
├── Token in httpOnly cookie?  [✅]
├── Server-side validation?    [✅]
├── CSRF protection?           [✅]
├── Rate limiting?             [✅]
├── Secure headers?            [✅]
├── Session expiry?            [✅]
└── Auth logging?              [✅]

Common Patterns:
├── JWT + Middleware → Simple, stateless
├── NextAuth.js + DB → Full featured
├── Iron Session → Encrypted cookies
├── Clerk/Auth0 → Enterprise, hosted
└── Custom + Prisma → Full control
```

---

## See Also
- [Caching in Next.js](09-Caching.md)
- [Client Components](04-Client-Components.md)
- [Middleware](05-Middleware.md)
- [Route Handlers](07-Route-Handlers.md)
- [Server Actions](06-Server-Actions.md)
- [Server Components](03-Server-Components.md)
- [Static Exports](15-Static-Exports.md)

## References & Learn More

- [Next.js Docs: Authentication](https://nextjs.org/docs/app/building-your-application/authentication)
- [NextAuth.js Documentation](https://next-auth.js.org/)
- [Auth.js Documentation](https://authjs.dev/)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Clerk Documentation](https://clerk.com/docs)
