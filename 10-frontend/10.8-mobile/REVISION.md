<!-- section: Frontend | category: Reference | tags: revision, retrieval-practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Frontend-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Mobile — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## React Native & Cross-Platform

Source: [React Native & Cross-Platform](10.8.01-react-native-cross-platform.md)

**Q:** Why does React Native's newer architecture not guarantee a smooth interface?

**A:** It removes or changes particular bridge costs. Expensive JavaScript, rendering, lists, image work and native code can still exceed the frame budget.

## Deep Linking, Universal Links & App Links

Source: [Deep Linking, Universal Links & App Links](10.8.02-deep-linking-universal-links.md)

**Q:** What should happen when a deep link targets a protected screen while logged out?

**A:** Preserve and validate the intended destination, authenticate, then authorize and navigate. Never treat the link's object ID as proof of access.

## Testing React Native Apps

Source: [Testing React Native Apps](10.8.03-testing-react-native-apps.md)

**Q:** Why do JavaScript component tests not prove native navigation works?

**A:** They often mock native modules and run outside the device runtime. Use focused native integration/end-to-end checks for platform behavior and release-critical journeys.

## Expo EAS Build — Cloud Builds, Profiles & Submitting

Source: [Expo EAS Build — Cloud Builds, Profiles & Submitting](10.8.04-expo-eas-builds.md)

**Q:** What distinguishes an EAS build from a submission or release?

**A:** Build produces the native artifact; submission uploads it to a store path; review and rollout determine user availability. A successful upload is not a live release.

**Q:** Why can an internally distributed preview not simply be submitted to TestFlight?

**A:** Direct internal installation and store testing use different signing/distribution targets. An iOS ad hoc preview is not an App Store-signed artifact; build a store-compatible version for TestFlight. Simulator output is another separate target.

**Q:** With remote version management, why can `app.json` still show an old build number?

**A:** EAS increments its remotely stored build version and applies it to the native build rather than rewriting the local configuration. Record the effective version with the artifact.

## Over-the-Air Updates — EAS Update, CodePush & the JS/Native Boundary

Source: [Over-the-Air Updates — EAS Update, CodePush & the JS/Native Boundary](10.8.05-codepush-ota-updates.md)

**Q:** Why must an OTA update match the installed runtime version?

**A:** Its JavaScript may depend on native capabilities in that binary. The version label is a compatibility contract and must change when native requirements change.

## App-Store Release Automation — Release Trains, Store Review & Rollout Safety

Source: [App-Store Release Automation — Release Trains, Store Review & Rollout Safety](10.8.06-app-store-release-automation.md)

**Q:** Why can stopping a phased release not undo every user's installed version?

**A:** Users who already installed retain that binary. Recovery may require a compatible OTA update or a new store build, with adoption and review delays.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
