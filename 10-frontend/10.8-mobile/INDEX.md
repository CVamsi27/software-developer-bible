# Mobile & Cross-Platform — Index

> **Study time:** ≈ 1 h 8 m of reading (7 files, ~10 min average).
> **7 files** — React Native fluency for studio/agency loops (MVST-class): the architecture and platform-choice primer, plus deep linking, testing, release operations (EAS builds, OTA updates, store automation), and interview-question chapters covering what production mobile work actually adds.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories

The concepts classify into 8 groups across the seven files — the way to recall them in a "would you pick RN or native?" or "how does deep linking actually work?" or "how do you ship a release?" question.

| Category | What it covers | The one-line exam answer |
| --------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **RN Architecture** | Bridge → JSI/Fabric evolution, new renderer, why perf changed | Old bridge = serialization bottleneck; JSI = direct synchronous calls |
| **Tooling Decision** | Expo vs bare workflow | Expo first unless you need native modules day one |
| **Cross-Platform Choice** | RN vs native vs PWA decision matrix | Match to team skills + UI customness + platform-API depth |
| **Web/Mobile Code Sharing** | TS monorepo, shared types/logic/hooks | RN maximizes sharing when web is already TypeScript |
| **Deep Linking** | URI schemes vs Universal Links vs App Links, deferred linking, fallbacks | https links verified via hosted JSON beat schemes: ownership proof + free web fallback |
| **Mobile Testing** | Jest/RNTL units, Detox vs Maestro E2E, mocking native modules, macOS CI | Same pyramid as web; the mobile deltas are native-module mocks and mac runners |
| **Cloud Builds & Release** | EAS Build profiles, credentials, versioning, CI-triggered native builds | Cloud native builds = no macOS needed, reproducible, release policy in `eas.json` |
| **OTA & Store Ops** | EAS Update/CodePush JS fixes, runtime-version boundary, release trains, review, staged rollout | JS fixes go OTA in minutes; native changes ride the store train with staged rollout |

---

## Files

| # | File | Topics |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | [React Native & Cross-Platform](10.8.01-react-native-cross-platform.md) | RN architecture (bridge → JSI/Fabric), Expo vs bare, RN vs native vs PWA decision matrix, code-sharing with web (your TS monorepo), mobile-specific concerns |
| 2 | [Deep Linking & Universal Links](10.8.02-deep-linking-universal-links.md) | URI schemes vs Universal Links (AASA) vs App Links (assetlinks.json), cold/warm start capture, deferred deep linking, React Navigation `linking` config, testing with simctl/adb/Detox, web fallback |
| 3 | [Testing React Native Apps](10.8.03-testing-react-native-apps.md) | Jest units, React Native Testing Library components, Detox vs Maestro comparison, mocking native modules, device farms + macOS runners in CI, React Native DevTools, visual regression options |
| 4 | [Expo EAS Build](10.8.04-expo-eas-builds.md) | Cloud native builds (no macOS needed), dev/preview/production profiles in `eas.json`, credentials & signing, versioning/autoIncrement, local vs cloud, CI-triggered builds |
| 5 | [OTA Updates — EAS Update & CodePush](10.8.05-codepush-ota-updates.md) | JS-bundle over-the-air updates, runtimeVersion compatibility contract, channels & rollouts, rollback, what can/can't go OTA (the JS/native boundary) |
| 6 | [App-Store Release Automation](10.8.06-app-store-release-automation.md) | Release trains, CI build → submit → TestFlight/Play internal → review → staged/phased rollout, adoption lag, rollback paths, store-specific mechanics |
| 7 | [Interview Questions](10.8.07-interview-questions.md) | 30+ curated Qs: bridge → JSI/Fabric architecture, RN vs native vs PWA choice, deep linking end-to-end, mobile testing, EAS/OTA/release trains/staged rollouts |

## The 30-Second Version

```text
Web team shipping mobile fast, mostly-standard UI? → React Native (Expo first)
Deep platform APIs / perf-critical animations? → Native (Swift/Kotlin) or RN + native modules
Content/product surface needing reach + instant use? → PWA
Already a TS monorepo? → RN maximizes shared types/logic/hooks
Releasing? → EAS Build (native train) + EAS Update (JS hotfixes) + staged store rollout
```

---

**Cross-references:** [React](../10.3-react/INDEX.md) · [Next.js/PWA](../10.7-html-css/INDEX.md) · [MVST prep sheet](../../80-lanes-abroad-full-stack/80.32-company-prep-sheets.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Web/mobile code sharing (TS monorepo) | `pnpm-workspace.yaml` - `apps/*` + `packages/*` workspace sharing types/hooks/utils across all frontends |
| PWA as the cross-platform route | `apps/app/public/sw.js` - offline app-shell service worker behind `apps/app/src/components/pwa/pwa-register.tsx` |

_React Native, Expo, deep linking/universal links, and RN-specific testing: no direct docita implementation yet._

---

## Navigation

[← Previous: HTML/CSS & PWA](../10.7-html-css/INDEX.md) · [ Back to Index](../../INDEX.md)
