# Mobile & Cross-Platform — Index

> **3 files** — React Native fluency for studio/agency loops (MVST-class): the architecture and platform-choice primer, plus deep linking and testing chapters covering what production mobile work actually adds.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories

The concepts classify into 6 groups across the three files — the way to recall them in a "would you pick RN or native?" or "how does deep linking actually work?" question.

| Category | What it covers | The one-line exam answer |
|----------|----------------|--------------------------|
| **RN Architecture** | Bridge → JSI/Fabric evolution, new renderer, why perf changed | Old bridge = serialization bottleneck; JSI = direct synchronous calls |
| **Tooling Decision** | Expo vs bare workflow | Expo first unless you need native modules day one |
| **Cross-Platform Choice** | RN vs native vs PWA decision matrix | Match to team skills + UI customness + platform-API depth |
| **Web/Mobile Code Sharing** | TS monorepo, shared types/logic/hooks | RN maximizes sharing when web is already TypeScript |
| **Deep Linking** | URI schemes vs Universal Links vs App Links, deferred linking, fallbacks | https links verified via hosted JSON beat schemes: ownership proof + free web fallback |
| **Mobile Testing** | Jest/RNTL units, Detox vs Maestro E2E, mocking native modules, macOS CI | Same pyramid as web; the mobile deltas are native-module mocks and mac runners |

---

## Files

| # | File | Topics |
|---|------|--------|
| 1 | [React Native & Cross-Platform](10.8.01-react-native-cross-platform.md) | RN architecture (bridge → JSI/Fabric), Expo vs bare, RN vs native vs PWA decision matrix, code-sharing with web (your TS monorepo), mobile-specific concerns |
| 2 | [Deep Linking & Universal Links](10.8.02-deep-linking-universal-links.md) | URI schemes vs Universal Links (AASA) vs App Links (assetlinks.json), cold/warm start capture, deferred deep linking, React Navigation `linking` config, testing with simctl/adb/Detox, web fallback |
| 3 | [Testing React Native Apps](10.8.03-testing-react-native-apps.md) | Jest units, React Native Testing Library components, Detox vs Maestro comparison, mocking native modules, device farms + macOS runners in CI, React Native DevTools, visual regression options |

## The 30-Second Version

```text
Web team shipping mobile fast, mostly-standard UI? → React Native (Expo first)
Deep platform APIs / perf-critical animations? → Native (Swift/Kotlin) or RN + native modules
Content/product surface needing reach + instant use? → PWA
Already a TS monorepo? → RN maximizes shared types/logic/hooks
```

---

**Cross-references:** [React](../10.3-react/INDEX.md) · [Next.js/PWA](../10.7-html-css/INDEX.md) · [MVST prep sheet](../../80-lanes-abroad-full-stack/80.32-company-prep-sheets.md)

---

## Navigation

[← Previous: HTML/CSS & PWA](../10.7-html-css/INDEX.md) · [ Back to Index](../../INDEX.md)
