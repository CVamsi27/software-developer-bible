<!-- section: Mobile | category: Reference | tags: revision, retrieval-practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Mobile-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Mobile — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## React Native & Cross-Platform

Source: [React Native & Cross-Platform](10.8.01-react-native-cross-platform.md)

**Q:** Why does React Native's newer architecture not guarantee a smooth interface?

**A:** It removes or changes particular bridge costs. Expensive JavaScript, rendering, lists, image work, and native code can still exceed the frame budget.

**Q:** A card is halfway through expanding when tapped again. Which value should determine its next target?

**A:** The logical expanded state, not the intermediate spring value. Flip intent, assign the new target, and let the animation continue from its current progress. UI-thread execution still does not guarantee a frame budget.

## Deep Linking, Universal Links & App Links

Source: [Deep Linking, Universal Links & App Links](10.8.02-deep-linking-universal-links.md)

**Q:** What should happen when a deep link targets a protected screen while logged out?

**A:** Preserve and validate the intended destination, authenticate, then authorize and navigate. Never treat the link's object ID as proof of access.

**Q:** A warm link arrives before `getInitialURL` resolves. How do you keep the late initial link from replacing it?

**A:** Subscribe during bootstrap, record that an event arrived, and ignore the older initial completion. Cleanup must also disable pending completions. Validate the route and wait for session and navigation readiness before accessing data.

**Q:** Why can a verified Universal Link still open Safari despite a valid AASA file, and what open-redirect check belongs in inbound link parsing?

**A:** Apple's CDN caches the AASA file and re-checks roughly weekly (use `?mode=developer` with iOS Developer Mode during staging QA), and iOS ignores Universal Links on same-domain taps, programmatic redirects, and many embedded WebViews. On arrival, reject protocol-relative paths (`//evil.com`) and arbitrary return URLs before forwarding links into navigation or `WebView` components.

## Testing React Native Apps

Source: [Testing React Native Apps](10.8.03-testing-react-native-apps.md)

**Q:** Why do JavaScript component tests not prove native navigation works?

**A:** They often mock native modules and run outside the device runtime. Use focused native integration and end-to-end checks for platform behavior and release-critical journeys.

**Q:** A permission mock always returns granted. Which failure is hidden, and what evidence is still missing after fixing it?

**A:** Denial and recovery behavior is hidden. Configure a denial case and assert the React response; device tests must still verify the actual OS prompt, settings, and lifecycle behavior.

**Q:** A React Native screen test passes, but a cold-start link fails on a device. What boundary was missing from the test evidence?

**A:** The component test only exercised JavaScript-rendered host components. Add an installed-app test for the OS link handoff, app bootstrap, and navigation readiness, then verify the HTTPS association on the target platform.

## Expo EAS Build — Cloud Builds, Profiles & Submission

Source: [Expo EAS Build — Cloud Builds, Profiles & Submission](10.8.04-expo-eas-builds.md)

**Q:** What distinguishes an EAS build from a submission or release?

**A:** Build produces the native artifact; submission uploads it to a store path; review and rollout determine user availability. A successful upload is not a live release.

**Q:** Why can an internally distributed preview not simply be submitted to TestFlight?

**A:** Direct internal installation and store testing use different signing and distribution targets. An iOS ad hoc preview is not an App Store-signed artifact; build a store-compatible version for TestFlight. Simulator output is another separate target.

**Q:** With remote version management, why can `app.json` still show an old build number?

**A:** EAS increments its remotely stored build version and applies it to the native build rather than rewriting the local configuration. Record the effective version with the artifact.

**Q:** A preview runs on an enrolled iPhone but cannot be submitted to TestFlight. Why is renaming its profile insufficient?

**A:** The existing artifact carries its signing and distribution contract. Produce a store-compatible build from reviewed source, record its effective version, and submit that exact artifact ID.

**Q:** A CI log says an artifact was submitted successfully. Which identities should you retain before promoting it?

**A:** Retain the source revision, build profile, platform build ID, and effective store version, then confirm the store is reviewing that same artifact. Keep matching symbols and source maps so later crash reports can be diagnosed.

**Q:** Why must API secrets or signing keys never be placed in `EXPO_PUBLIC_*` environment variables?

**A:** Only `EXPO_PUBLIC_*` values are inlined in plaintext directly into the shipped JavaScript bundle inside `.ipa` and `.aab` artifacts, where anyone can inspect them. Keep private credentials server-side or restricted to build-time-only EAS environment variables used strictly by native build hooks.

## Over-the-Air Updates — EAS Update, CodePush & the JS/Native Boundary

Source: [Over-the-Air Updates — EAS Update, CodePush & the JS/Native Boundary](10.8.05-codepush-ota-updates.md)

**Q:** Why must an OTA update match the installed runtime version?

**A:** Its JavaScript may depend on native capabilities in that binary. The version label is a compatibility contract and must change when native requirements change.

**Q:** A device is offline when an OTA revert is published. What code can it run?

**A:** It retains an eligible cached update or embedded fallback under its update policy; publication cannot immediately repair an offline device. Monitor actual uptake and test crash recovery for each supported runtime.

**Q:** A JavaScript bundle matches the installed runtime. Is that enough to publish it through an OTA service?

**A:** No. Runtime matching is a technical compatibility condition, not store approval. Review the platform's downloaded-code rules and the provider's release guidance for the specific change; Apple restricts downloaded code that introduces or changes app features, and Google Play restricts self-updating and external executable downloads.

**Q:** Can a deployed CodePush client move to EAS Update by changing the update URL?

**A:** No. The installed binary needs the `expo-updates` client and native configuration. Replace the integration, build a new binary, and distribute it through the stores; older installed clients continue using their existing provider until they upgrade.

**Q:** What is the trade-off between blocking cold launch on an update download vs. applying on the next restart, and how does `expo-updates` survive a crash on boot?

**A:** Blocking launch during splash speeds fix adoption at the cost of slower startup on poor networks, whereas background download with next-restart activation preserves fast startup while delaying uptake. If a newly applied bundle crashes before rendering, `expo-updates` detects the failed launch and automatically rolls back to the last working cached or embedded bundle.

## App-Store Release Automation — Release Trains, Store Review & Rollout Safety

Source: [App-Store Release Automation — Release Trains, Store Review & Rollout Safety](10.8.06-app-store-release-automation.md)

**Q:** Why can stopping a phased release not undo every user's installed version?

**A:** Users who already installed retain that binary. Recovery may require a compatible OTA update or a new store build, with adoption and review delays.

**Q:** You pause an iOS phased release after a crash spike. Can you assume only the configured percentage has the binary?

**A:** No. Apple's phased schedule governs automatic updates; anyone can manually download it. Existing installations remain. Contain the feature and deliver a compatible repair or corrective binary, with adoption evidence.

**Q:** Does a store's staged percentage tell you what share of active devices is running the release?

**A:** No. Apple phases automatic updates while allowing manual downloads; Google staged rollout controls eligibility for an update. Measure installed-version adoption separately, and remember that halting distribution does not downgrade devices already updated.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
