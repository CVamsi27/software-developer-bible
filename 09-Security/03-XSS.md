---
section: Security
category: Architecture
tags: [concept]
---

# Cross-Site Scripting (XSS)

## Definition

Cross-Site Scripting (XSS) is a security vulnerability that allows attackers to inject malicious client-side scripts into web pages viewed by other users. When a victim views the affected page, the malicious script executes in their browser, enabling the attacker to steal data, hijack sessions, or perform actions on behalf of the user. XSS is one of the most common web vulnerabilities, consistently appearing in the OWASP Top 10.

## Why Do We Need It?

- **Data Theft**: Attackers can steal cookies, session tokens, and personal information
- **Session Hijacking**: Stolen session cookies allow impersonation of users
- **Malware Distribution**: Injected scripts can redirect users to malicious sites
- **Phishing**: Modified pages can present fake login forms
- **Defacement**: Attackers can alter the appearance of web pages
- **Keylogging**: Injected scripts can record user keystrokes

## How It Works

### Types of XSS

```text
┌─────────────────────────────────────────────────────────────────┐
│                        XSS Attack Types                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Stored XSS (Persistent)                                     │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│     │ Attacker │─────>│  Server  │─────>│  Victim  │           │
│     │          │      │  (Store) │      │          │           │
│     └──────────┘      └──────────┘      └──────────┘           │
│     Malicious script saved in database, served to all users     │
│                                                                 │
│  2. Reflected XSS (Non-persistent)                              │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│     │ Attacker │─────>│  Server  │─────>│  Victim  │           │
│     │          │      │(Reflect) │      │          │           │
│     └──────────┘      └──────────┘      └──────────┘           │
│     Script in URL, reflected back in response                   │
│                                                                 │
│  3. DOM-based XSS                                               │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│     │ Attacker │─────>│  Browser │─────>│  Victim  │           │
│     │          │      │  (DOM)   │      │          │           │
│     └──────────┘      └──────────┘      └──────────┘           │
│     Script executes entirely in the browser                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### Attack Flow

```text
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│ Attacker │                    │  Server  │                    │  Victim  │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Inject malicious script   │                               │
     │     (form, URL parameter)     │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                    2. Script stored/reflected                 │
     │                               │                               │
     │                               │  3. Victim requests page      │
     │                               │<──────────────────────────────│
     │                               │                               │
     │                               │  4. Page with malicious       │
     │                               │     script served             │
     │                               │──────────────────────────────>│
     │                               │                               │
     │                               │     5. Malicious script       │
     │                               │         executes              │
     │                               │                               │
     │  6. Stolen data sent to       │                               │
     │     attacker                  │                               │
     │<──────────────────────────────────────────────────────────────│

```

## Code Examples

### Vulnerable Code Examples

```typescript
// ❌ VULNERABLE: Direct innerHTML with user input
app.get("/search", (req, res) => {
  const query = req.query.q as string;
  res.send(`
    <div>
      <p>Search results for: ${query}</p>
    </div>
  `);
});

// ❌ VULNERABLE: Template literal injection
app.get("/profile", (req, res) => {
  const name = req.query.name as string;
  res.send(`<h1>Welcome, ${name}!</h1>`);
});

// ❌ VULNERABLE: eval() with user input
app.get("/calculate", (req, res) => {
  const expression = req.query.expr as string;
  const result = eval(expression); // Never do this!
  res.send(`Result: ${result}`);
});

// ❌ VULNERABLE: innerHTML in frontend JavaScript
function displayComment(comment: string) {
  const div = document.getElementById("comments");
  div.innerHTML += `<p>${comment}</p>`; // XSS vulnerability
}

```

### Secure Code Examples

```typescript
import DOMPurify from "dompurify";
import { JSDOM } from "jsdom";

// ✅ SECURE: HTML encoding
function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
    "/": "&#x2F;",
  };
  return text.replace(/[&<>"'/]/g, (char) => map[char]);
}

// ✅ SECURE: Using escaped output in server response
app.get("/search", (req, res) => {
  const query = req.query.q as string;
  const safeQuery = escapeHtml(query);
  res.send(`
    <div>
      <p>Search results for: ${safeQuery}</p>
    </div>
  `);
});

// ✅ SECURE: Using DOMPurify for client-side sanitization
function displayComment(comment: string) {
  const div = document.getElementById("comments");
  const window = new JSDOM("").window;
  const purify = DOMPurify(window);
  div.innerHTML += `<p>${purify.sanitize(comment)}</p>`;
}

// ✅ SECURE: Using textContent instead of innerHTML
function displayCommentSecure(comment: string) {
  const div = document.getElementById("comments");
  const p = document.createElement("p");
  p.textContent = comment;
  div.appendChild(p);
}

// ✅ SECURE: React (automatically escapes JSX)
function Comment({ text }: { text: string }) {
  return <p>{text}</p>; // React escapes this automatically
}

// ✅ SECURE: Content Security Policy middleware
const cspMiddleware = (req, res, next) => {
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );
  next();
};

app.use(cspMiddleware);

```

### Input Validation and Sanitization

```typescript
import validator from "validator";
import xss from "xss";

// Input validation
const validateInput = (input: string): string => {
  if (!validator.isLength(input, { min: 1, max: 1000 })) {
    throw new Error("Input too long");
  }
  return validator.escape(input);
};

// XSS sanitization
const sanitizeInput = (input: string): string => {
  return xss(input, {
    whiteList: {}, // No tags allowed
    stripIgnoreTag: true,
    stripIgnoreTagBody: ["script", "style"],
  });
};

// URL validation to prevent XSS via URLs
const validateUrl = (url: string): string => {
  if (!validator.isURL(url, { protocols: ["http", "https"] })) {
    throw new Error("Invalid URL");
  }
  return validator.escape(url);
};

// Content Security Policy nonce generation
const generateNonce = (): string => {
  return require("crypto").randomBytes(16).toString("base64");
};

```

## Real-World Use Cases

### 1. Comment Systems

- User-submitted comments can contain malicious scripts
- Must sanitize before storing and when displaying
- Use DOMPurify or similar libraries for sanitization

### 2. User Profiles

- Usernames, bios, and profile fields can contain XSS
- Sanitize all user-generated content
- Use CSP to prevent script execution

### 3. Search Functionality

- Search queries reflected in results pages
- Always encode user input in output
- Avoid using search terms in HTML attributes

### 4. Rich Text Editors

- Allow limited HTML tags for formatting
- Whitelist allowed tags and attributes
- Sanitize before storing and when displaying

### 5. Admin Dashboards

- Display user-generated content in admin panels
- Use sandboxed iframes for untrusted content
- Implement strict CSP policies

## Common Mistakes

1. **Trusting user input**: Never assume input is safe; always validate and sanitize

2. **Using innerHTML without sanitization**: Always sanitize or use textContent

3. **Not implementing CSP**: CSP is a critical defense layer

4. **Sanitizing on input only**: Must also sanitize on output (stored XSS)

5. **Using eval()**: Never use eval() with user input

6. **Not encoding output**: Always encode user data in HTML responses

7. **Using document.write()**: Avoid document.write() with dynamic content

8. **Ignoring DOM-based XSS**: Client-side scripts can be vulnerable too

## Best Practices

1. **Validate all input** on both client and server

2. **Sanitize output** before rendering in HTML

3. **Implement Content Security Policy (CSP)** with strict rules

4. **Use textContent** instead of innerHTML

5. **Use DOMPurify** for HTML sanitization

6. **Encode special characters** in HTML, CSS, JavaScript, and URLs

7. **Use frameworks** that auto-escape (React, Angular, Vue)

8. **Implement rate limiting** to prevent mass injection

9. **Use HTTPOnly cookies** for session tokens (limits XSS impact)
10. **Regular security audits** and penetration testing

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| DOMPurify | Adds ~50ms overhead for large documents |
| HTML Encoding | Negligible performance impact |
| CSP | First load may be slower due to policy evaluation |
| Input Validation | Minimal overhead for most validators |
| Sanitization Libraries | Lightweight libraries have minimal impact |


## Summary

XSS is a critical web security vulnerability that allows attackers to inject malicious scripts. Key takeaways:

- Never trust user input — always validate and sanitize
- Use output encoding to prevent script execution
- Implement Content Security Policy (CSP)
- Use textContent instead of innerHTML
- Use DOMPurify for HTML sanitization
- Use frameworks with auto-escaping (React, Vue, Angular)
- Implement httpOnly cookies to limit XSS impact
- Regular security audits and penetration testing

## Cheat Sheet
| Defense | Implementation |
|---------|---------------|
| Input Validation | Validate type, length, format on server |
| Output Encoding | HTML entity encoding for all user data |
| CSP | Strict policy with nonce-based scripts |
| DOMPurify | Sanitize all user-generated HTML |
| textContent | Use instead of innerHTML |
| httpOnly Cookies | Prevent JavaScript access to session tokens |
| Framework Auto-escaping | React, Vue, Angular escape JSX |
| Security Headers | X-XSS-Protection, X-Content-Type-Options |

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Cross-Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [DOMPurify - HTML Sanitizer](https://github.com/cure53/DOMPurify)
- [Content Security Policy (CSP) - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [XSS Game - Google](https://xss-game.appspot.com/)
- [PortSwigger XSS Tutorials](https://portswigger.net/web-security/cross-site-scripting)
