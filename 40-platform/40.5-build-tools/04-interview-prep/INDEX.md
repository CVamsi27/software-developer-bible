# Interview Prep — Build Tools

> **1 file, 50+ curated questions with answers.** Tree shaking internals, code-splitting strategy, and tool-selection judgment.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview%20Prep-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

Questions across all three content categories:

- **Easy** — what is tree shaking, what does Babel do, Vite vs Webpack one-liner
- **Medium** — route vs component code splitting, debugging a bundle regression, loaders vs plugins
- **Hard** — migrating Webpack to Rspack, HMR implementation details, designing the build for a large monorepo

---

## File Index

### [Build Tools Interview Questions](40.5.4.01-interview-questions.md)

50+ curated questions with answers. Work them after the content categories.

---

## Navigation

[← Optimization & Comparison](../03-optimization-and-comparison/INDEX.md) · [↑ Build Tools Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — gives me true stories for these answers.

| Topic | Docita evidence |
|-------|-----------------|
| "Vite vs Webpack?" | Lived the migration: Next.js → Vite SPA (ADR 0012), with reasons recorded |
| "Monorepo build design?" | Turbo task graph + per-app env scoping + shared vitest config across 5 apps |
| "Keeping bundles honest?" | knip dead-code gate, jscpd zero-clone gate, file-size budget checks in CI |
| "Multi-target builds?" | Same repo ships NestJS API, Vite SPAs, Astro landing to Cloudflare, worker app |
| Turbopack/Rspack war stories | _No direct docita implementation yet._ |
