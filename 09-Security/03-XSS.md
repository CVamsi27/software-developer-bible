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

```
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

```
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

## Interview Questions

### Beginner (5-10)

**Q1: What is XSS and why is it dangerous?**
A: Cross-Site Scripting allows attackers to inject malicious scripts into web pages viewed by other users. It's dangerous because it can steal session cookies, personal data, and perform actions on behalf of users.

**Q2: What are the three types of XSS?**
A: Stored XSS (malicious script saved on server), Reflected XSS (script in URL parameter reflected back), and DOM-based XSS (script executes entirely in the browser via DOM manipulation).

**Q3: How do you prevent XSS?**
A: Validate and sanitize all input, encode output, use textContent instead of innerHTML, implement Content Security Policy (CSP), use frameworks with auto-escaping, and use DOMPurify for HTML sanitization.

**Q4: What is Content Security Policy (CSP)?**
A: CSP is a security header that restricts which resources (scripts, styles, images) can be loaded and executed on a page. It helps prevent XSS by blocking unauthorized scripts.

**Q5: What is DOMPurify?**
A: DOMPurify is a DOM-only XSS sanitizer for HTML. It removes untrusted content and keeps only safe HTML elements and attributes based on a whitelist.

**Q6: Why is innerHTML dangerous?**
A: innerHTML parses and executes any HTML/JavaScript in the string. If the string contains user input, malicious scripts will execute in the browser.

**Q7: What is the difference between stored and reflected XSS?**
A: Stored XSS is persistent — the malicious script is saved on the server and affects all users who view the page. Reflected XSS is temporary — the script is in the URL and only affects users who click the link.

**Q8: Can XSS steal cookies?**
A: Yes, if cookies are not HttpOnly. An attacker can use `document.cookie` to steal session tokens and impersonate users.

**Q9: What is the `escape()` function used for in XSS prevention?**
A: The escape() function converts special characters to their HTML entities (< becomes &lt;, > becomes &gt;), preventing them from being interpreted as HTML/JavaScript.

**Q10: How does React prevent XSS?**
A: React automatically escapes all values rendered in JSX. It converts special characters to HTML entities, preventing XSS in most cases. However, dangerouslySetInnerHTML bypasses this protection.

### Intermediate (5-10)

**Q11: How would you implement CSP for a Next.js application?**
A: Use the `next.config.js` headers configuration. Define strict CSP policies with nonce-based script loading. Example: `Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-${nonce}'`

**Q12: How do you handle XSS in rich text editors?**
A: Use a whitelist-based sanitizer like DOMPurify. Allow only specific tags (p, b, i, ul, ol, li) and attributes. Never allow script, event handlers, or URLs with javascript: protocol.

**Q13: What is the difference between encoding and sanitization?**
A: Encoding converts special characters to HTML entities (prevent interpretation). Sanitization removes or modifies potentially dangerous content while preserving safe content.

**Q14: How do you prevent DOM-based XSS?**
A: Avoid using document.write(), innerHTML, and eval() with untrusted data. Use textContent or safe DOM APIs. Implement CSP. Use libraries like DOMPurify for sanitization.

**Q15: How do you handle XSS in a single-page application?**
A: Use a framework with auto-escaping (React, Vue, Angular). Implement CSP headers. Sanitize any user-generated HTML. Avoid using dangerouslySetInnerHTML/v-html.

**Q16: What is a nonce in CSP context?**
A: A nonce (number used once) is a random value added to CSP headers and script tags. Only scripts with the correct nonce can execute, preventing injected scripts from running.

**Q17: How do you test for XSS vulnerabilities?**
A: Use automated scanners (OWASP ZAP, Burp Suite), manual testing with payloads (<script>alert(1)</script>), and code review. Test all input fields, URL parameters, and HTTP headers.

**Q18: How do you handle XSS in user-generated content displayed in admin panels?**
A: Use sandboxed iframes to isolate untrusted content. Apply strict CSP. Sanitize content before display. Never execute user content as code.

**Q19: What is the httpOnly cookie flag and how does it prevent XSS impact?**
A: httpOnly prevents JavaScript from accessing the cookie via document.cookie. Even if XSS occurs, session tokens in httpOnly cookies cannot be stolen.

**Q20: How do you handle XSS in email content?**
A: Use plain text or strict HTML sanitization. Avoid inline scripts. Use CSP in web-based email clients. Strip all JavaScript and event handlers.

### Senior (10-15)

**Q21: Design a comprehensive XSS defense strategy for a large application.**
A: Layer 1: Input validation and sanitization. Layer 2: Output encoding. Layer 3: CSP with nonce-based scripts. Layer 4: Framework auto-escaping. Layer 5: Security monitoring and logging. Layer 6: Regular security audits.

**Q22: How would you implement XSS protection for a user-generated HTML content system?**
A: Use a whitelist-based sanitizer. Define allowed tags and attributes. Sanitize on both input and output. Use DOMPurify with custom configuration. Implement CSP. Use sandboxed iframes for rendering.

**Q23: Explain the DOM clobbering vulnerability and how to prevent it.**
A: DOM clobbering uses HTML attributes (id, name) to override JavaScript variables, potentially bypassing security checks. Prevent by not using innerHTML with untrusted data, validating DOM elements, and using CSP.

**Q24: How would you handle XSS in a micro-frontend architecture?**
A: Each micro-frontend has its own CSP. Use iframe isolation for untrusted components. Implement shared security utilities. Sanitize data passed between micro-frontends.

**Q25: How do you detect and prevent XSS in server-side rendered (SSR) applications?**
A: Implement CSP with nonce for inline scripts. Sanitize all user input on the server. Use proper output encoding. Implement security headers. Monitor for XSS attempts in logs.

**Q26: Explain how to implement a secure HTML sanitizer from scratch.**
A: Parse HTML into DOM nodes. Traverse the tree and remove disallowed elements/attributes. Whitelist safe tags and attributes. Handle edge cases (encoded entities, nested scripts). Test against known XSS payloads.

**Q27: How would you implement XSS protection for a markdown renderer?**
A: Parse markdown to HTML using a safe library. Sanitize the resulting HTML with DOMPurify. Allow only safe HTML elements. Strip all JavaScript and event handlers. Use CSP.

**Q28: How do you handle XSS in WebSocket messages?**
A: Validate and sanitize all WebSocket messages. Use strict message schemas. Encode data before rendering in DOM. Implement CSP. Monitor for suspicious patterns.

**Q29: Explain how to implement XSS protection for a file upload system.**
A: Validate file types and content. Sanitize file metadata. Never serve user-uploaded files with HTML content type. Use Content-Disposition headers. Implement CSP.

**Q30: How would you handle XSS in a GraphQL API?**
A: Validate GraphQL queries against schema. Sanitize all user input. Use query whitelisting. Implement rate limiting. Monitor for suspicious query patterns.

### FAANG-style (5-10)

**Q31: Design an XSS detection system for a large-scale web application.**
A: Implement client-side monitoring with error tracking. Use CSP violation reporting. Deploy runtime application self-protection (RASP). Implement anomaly detection for DOM mutations. Build automated alerting.

**Q32: How would you implement XSS protection for a real-time collaboration tool?**
A: Use operational transformation with sanitization. Implement per-user CSP. Sanitize shared content in real-time. Use WebSockets with strict message validation. Implement audit logging.

**Q33: Design a CSP deployment strategy for a legacy application with inline scripts.**
A: Phase 1: Inventory all scripts and styles. Phase 2: Refactor to external files. Phase 3: Implement nonce-based CSP. Phase 4: Deploy with report-only mode. Phase 5: Enforce strict CSP.

**Q34: How would you handle XSS in a server-side rendering (SSR) React application?**
A: Use React's built-in escaping for JSX. Sanitize any dangerouslySetInnerHTML usage. Implement CSP with nonce for hydration. Use DOMPurify for server-rendered HTML. Monitor for XSS attempts.

**Q35: Design a system for automatic XSS payload detection in user input.**
A: Use machine learning models trained on XSS payloads. Implement regex patterns for known attacks. Deploy honeypots to detect attacks. Build automated response system. Implement user behavior analysis.

### Follow-ups (5-10)

**Q36: How would your XSS defense change for a headless CMS?**
A: Sanitize content on ingestion and output. Use strict CSP. Implement content security scanning. Use sandboxed iframes for rendering untrusted content. Implement version control for content changes.

**Q37: If CSP was causing issues with third-party scripts, how would you handle it?**
A: Use specific third-party domains in CSP. Implement script nonce for third-party scripts. Use Subresource Integrity (SRI) for third-party resources. Evaluate alternatives to problematic third-party scripts.

**Q38: How would you implement XSS protection for a browser extension?**
A: Use content script isolation. Implement strict CSP for extension pages. Validate messages between content scripts and background scripts. Sanitize any user-generated content.

**Q39: How would your approach change for a progressive web app (PWA)?**
A: Implement service worker-based CSP. Cache sanitized content. Validate offline content. Implement integrity checks for cached resources. Monitor for XSS in push notifications.

**Q40: If you discovered XSS in production, what would be your incident response?**
A: Immediately deploy CSP in report-only mode. Identify all affected endpoints. Patch vulnerabilities. Rotate session tokens. Notify affected users. Conduct post-mortem. Implement additional monitoring.

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

## References & Learn More

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Cross-Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [DOMPurify - HTML Sanitizer](https://github.com/cure53/DOMPurify)
- [Content Security Policy (CSP) - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [XSS Game - Google](https://xss-game.appspot.com/)
- [PortSwigger XSS Tutorials](https://portswigger.net/web-security/cross-site-scripting)
