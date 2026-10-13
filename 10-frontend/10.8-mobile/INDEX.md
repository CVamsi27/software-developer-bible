# Mobile & Cross-Platform — Index

> **Study time:** ≈ 55 min of reading (8 files, ~7 min average).
> **8 files** — React Native fluency for studio/agency loops (MVST-class): the architecture and platform-choice primer, plus deep linking, testing, release operations (EAS builds, OTA updates, store automation), and interview-question chapters covering what production mobile work actually adds.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

This is optional specialist depth for a web full-stack role. Read it when the target role includes native/mobile ownership; prioritize the core JavaScript, React and request/data boundaries first.

## Pass 1 — understand which runtime owns the feature

[React Native & Cross-Platform](10.8.01-react-native-cross-platform.md) follows JavaScript, Fabric's renderer and native modules. Decide which code can be shared with web and which platform capabilities need native ownership. Expo tooling and custom native modules can coexist.

## Pass 2 — reach and verify the feature

[Deep Linking & Universal Links](10.8.02-deep-linking-universal-links.md) traces a URL through OS verification and navigation readiness. [Testing React Native Apps](10.8.03-testing-react-native-apps.md) separates React-side behavior from the installed app's native behavior.

Show what happens when a link opens an authenticated screen on a cold start, and which test can observe each boundary.

## Pass 3 — follow a release to installed devices

[Expo EAS Build](10.8.04-expo-eas-builds.md) produces a signed native artifact. [EAS Update and legacy CodePush](10.8.05-codepush-ota-updates.md) targets compatible JavaScript/assets to an existing runtime and distinguishes the maintained Expo path from retired CodePush infrastructure. [App-Store Release Automation](10.8.06-app-store-release-automation.md) follows review, rollout and recovery.

Distinguish stopping new exposure from repairing devices already updated. Neither a cloud build nor a matching runtime version proves the feature behaves correctly; neither store nor OTA rollback is instant on every installed client.

## Finish with revision, then interview practice

Trace one feature from cold-link launch through testing, release and a failed rollout. Use [section revision](REVISION.md), then [interview questions](10.8.07-interview-questions.md) to defend the platform and operational choices.

**Cross-references:** [React](../10.3-react/INDEX.md) · [HTML/CSS & PWA](../10.7-html-css/INDEX.md) · [Company preparation](../../80-lanes-abroad-full-stack/80.32-company-prep-sheets.md)

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
