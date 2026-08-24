# Mobile & Cross-Platform — Index

> **Primer depth, not a full stack** — enough React Native fluency to hold your own in studio/agency loops (MVST-class) and to answer "would you pick RN, native, or PWA?" like a senior engineer.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-blue)](../../INDEX.md)

---

## 🗂️ Concept Categories (within the chapter)

One primer file, but the concepts inside classify into 4 groups — the way to recall them in a "would you pick RN or native?" question.

| Category | What it covers | The one-line exam answer |
|----------|----------------|--------------------------|
| **RN Architecture** | Bridge → JSI/Fabric evolution, new renderer, why perf changed | Old bridge = serialization bottleneck; JSI = direct synchronous calls |
| **Tooling Decision** | Expo vs bare workflow | Expo first unless you need native modules day one |
| **Cross-Platform Choice** | RN vs native vs PWA decision matrix | Match to team skills + UI customness + platform-API depth |
| **Web/Mobile Code Sharing** | TS monorepo, shared types/logic/hooks | RN maximizes sharing when web is already TypeScript |

---

| # | File | Topics |
|---|------|--------|
| 1 | [React Native & Cross-Platform](10.8.01-react-native-cross-platform.md) | RN architecture (bridge → JSI/Fabric), Expo vs bare, RN vs native vs PWA decision matrix, code-sharing with web (your TS monorepo), mobile-specific concerns |

## The 30-Second Version

```text
Web team shipping mobile fast, mostly-standard UI?   → React Native (Expo first)
Deep platform APIs / perf-critical animations?       → Native (Swift/Kotlin) or RN + native modules
Content/product surface needing reach + instant use?  → PWA
Already a TS monorepo?                                → RN maximizes shared types/logic/hooks
```

---

**Cross-references:** [React](../10.3-react/INDEX.md) · [Next.js/PWA](../10.7-html-css/INDEX.md) · [MVST prep sheet](../../80-lanes-abroad-full-stack/80.32-company-prep-sheets.md)

---

## Navigation

[← Previous: HTML/CSS & PWA](../10.7-html-css/INDEX.md) · [🏠 Back to Index](../../INDEX.md)
