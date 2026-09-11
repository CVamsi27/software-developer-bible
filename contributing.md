# Contributing Guide

> **Formatting conventions and best practices** for the Senior Full Stack Interview Bible.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [File Naming](#file-naming)
- [File Metadata](#file-metadata-html-comment--shieldsio-badges)
- [Badges](#badges)
- [Content Structure](#content-structure)
- [INDEX.md Format](#indexmd-format)
- [Code Blocks](#code-blocks)
- [File Endings & Whitespace](#file-endings--whitespace)
- [Cross-References & Navigation](#cross-references--navigation)
- [Special File Types](#special-file-types)
- [Verification Checklist](#verification-checklist)

---

## Getting Started

This repository documents senior full-stack engineering interview topics across 7 study stacks (10-70), a strategy folder (00), two terminal interview lanes (80, 81), and project deep-dives (projects/docita). All content is written in **GitHub Flavored Markdown** (`.md`).

Before contributing, review the existing files in the relevant section to understand the established conventions before creating or modifying content.

---

## Directory Structure

```
.
├── README.md # Project overview
├── INDEX.md # Central navigation hub (pick your lane)
├── contributing.md # This file
│
├── 00-strategy/ # Cross-lane (everyone starts here)
│ ├── INDEX.md
│ ├── 00.01-communication.md
│ ├── 00.02-resume-tips.md
│ ├── 00.03-star-method.md
│ └── 00.04-hr-questions.md
│
├── 10-frontend/ # Frontend (JS → TS → React → Next.js → Mobile)
│ ├── 10.1-javascript/
│ ├── 10.2-typescript/
│ ├── 10.3-react/
│ ├── 10.4-next.js/
│ ├── 10.5-form-handling/
│ ├── 10.6-animation/
│ ├── 10.7-html-css/
│ └── 10.8-mobile/
│
├── 20-backend/ # Backend (Node → NestJS → REST → DB → Security → Distributed → AI → Java)
│ ├── 20.1-node.js/
│ ├── 20.2-nestjs/
│ ├── 20.3-rest-apis/
│ ├── 20.4-database/
│ ├── 20.5-security/
│ ├── 20.6-microservices/
│ ├── 20.7-graphql/
│ ├── 20.8-caching/
│ ├── 20.12-ai-engineering/
│ └── 20.13-java/
│
├── 30-architecture/ # Architecture (design patterns + system design + infra patterns)
│ ├── 30.1-design-patterns/
│ ├── 30.2-system-design/
│ └── 30.3-infra-patterns/
│
├── 40-platform/ # DevOps / Platform
│ ├── 40.1-docker/
│ ├── 40.2-kubernetes/
│ ├── 40.3-ci-cd/
│ ├── 40.4-observability/
│ ├── 40.5-build-tools/
│ ├── 40.6-git-advanced/
│ ├── 40.7-serverless-edge/
│ ├── 40.8-monorepo/
│ ├── 40.9-twelve-factor/
│ ├── 40.10-cdn/
│ ├── 40.11-reverse-proxy/
│ └── 40.12-iac/
│
├── 50-quality/ # Quality (testing, a11y, performance, production engineering)
│ ├── 50.1-testing/
│ ├── 50.2-accessibility/
│ ├── 50.3-performance-monitoring/
│ └── 50.4-production-engineering/
│
├── 60-realtime/ # Real-time (WebSockets)
│ └── 60.1-websockets/
│
├── 70-interview-toolkit/ # Interview toolkit (behavioral, coding patterns, cheatsheets)
│ ├── 70.1-behavioral/
│ ├── 70.2-coding-patterns/
│ └── 70.3-cheatsheets/
│
├── projects/ # Project deep-dives
│ └── docita/ # 22 numbered deep-dives (01-10 foundations, 11-21 domains, 22 retrospective) + 80.x prep docs
│
├── 80-lanes-abroad-full-stack/ # Abroad Full-Stack lane (EU/remote) — INDEX.md + numbered 80.x files
│
└── 81-lanes-indian-sde-faang/ # Indian SDE / FAANG lane (DSA-heavy) — INDEX.md + numbered 81.x files
```

> Repo scale (measured 2026-09-04): **806 `.md` files / 345K lines** across the stacks, lanes, and projects above — run `python3 scripts/check_counts.py` to verify the claim stays true.

- **The 7 study stacks** (`10-`, `20-`, `30-`, `40-`, `50-`, `60-`, `70-`) hold the technical material both interview lanes pull from.
- **00-strategy** is cross-lane (everyone starts here); **80-** and **81-lanes** are terminal interview plans that reference into the stacks, never the other way around; **projects/** holds the Docita deep-dive corpus.
- Stack directories are numbered `00-` through `81-` to make it easy to slot new sections in.
- Each section has an `INDEX.md` file
- Large stacks are grouped into category subfolders (`01-`, `02-`, ... study order) with a per-category `INDEX.md`; small stacks stay flat
- Content files carry hierarchical IDs (`<stack>.<cat>.<seq>-slug.md`) or flat IDs (`<stack>.<seq>-slug.md`), always contiguous

---

## File Naming

| File Type | Pattern | Example |
| --------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Stack folder | `NN.N-slug/` | `10.1-javascript/` |
| Category folder (stacks >= ~8 chapters) | `NN-slug/` (2-digit study order) | `20.5-security/01-auth/` |
| Category INDEX | `INDEX.md` inside category folder | `20-backend/20.5-security/01-auth/INDEX.md` |
| Content file in a category | `<stack>.<cat>.<seq>-slug.md`, seq contiguous from 01 | `20-backend/20.5-security/01-auth/20.5.1.04-sessions-cookies.md` (`cat` = folder number without leading zero) |
| Content file in a flat stack | `<stack>.<seq>-slug.md`, seq contiguous from 01 | `40-platform/40.1-docker/40.1.06-production-patterns.md` |
| Interview questions file | same rule, always LAST sequence number | `40-platform/40.1-docker/40.1.10-interview-questions.md` |

- Use **kebab-case** for slugs and directory names
- Numeric IDs are unique repo-wide and sort correctly lexicographically; sequences are contiguous (no gaps)
- Verify with: `python3 scripts/check_structure.py`
- Verify ASCII diagrams/tables are aligned with: `python3 scripts/check_alignment.py` (exit 1 on drift)
  — auto-fix with `python3 scripts/check_alignment.py --fix`
- Verify links with: `python3 scripts/check_links.py` (fence-aware broken-link scan — ignores code fences, external URLs, and anchor-only links)

---

## File Metadata (HTML comment + shields.io badges)

Every content file **must** begin with metadata in two forms:

1. **HTML comment** (preserved for tooling, hidden in markdown renderers)
2. **shields.io badges** (visual metadata that renders as colored pills)

```markdown
<!-- section: JavaScript | category: Core | tags: concept -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Core-blue)](#)
[![Tags](https://img.shields.io/badge/tags-concept-lightgrey)](#)

# File Title
```

### Rules

- **Required fields**: `section`, `category`, `tags`
- `tags` is a comma-separated list: `concept, lld, principles, theory`
- Metadata line goes BEFORE the title (H1)
- INDEX.md and README.md files do **not** have the HTML comment, but they have badges
- Badges are clickable — in content files they link to `#`; in INDEX files the Files badge links to the central repo-root `INDEX.md` and Category/Status link to `#`
- Files whose body contains Liquid/Jinja template snippets (`{{ }}`, `{% %}`) open with a `{% raw %}` line *above* the HTML comment so GitHub Pages renders them literally (44 files use this today)

### Category Values

| Category | Used For | Badge color |
| --------------- | ---------------------------------------------------------------- | ---------------------- |
| `Core` | JavaScript, TypeScript | blue |
| `Frontend` | React, Next.js, Animation, Form Handling | ff6b35 (orange) |
| `Backend` | Node.js, NestJS | success (green) |
| `API` | REST APIs, GraphQL | ff6b35 (orange) |
| `Data` | Database | 8b5cf6 (purple) |
| `Architecture` | System Design, Microservices, Security, Design Patterns | 800080 (dark purple) |
| `DevOps` | Docker, Kubernetes, CI/CD, Serverless | ff7f00 (devops orange) |
| `Observability` | Observability (logging, monitoring, tracing, SLI/SLO, alerting) | 0ea5e9 (sky) |
| `Tooling` | Build Tools, Git Advanced | 64748b (slate) |
| `Quality` | Testing, Accessibility, Performance Monitoring | 8b5cf6 (purple) |
| `Real-Time` | WebSockets | f59e0b (amber) |
| `Interview` | Behavioral, Interview Strategy, Coding Patterns, SDE Role, lanes | red |
| `Reference` | CheatSheets, Monorepo | lightgrey |
| `Execution` | Personal execution plans (e.g., Berlin plan) | ff6b35 (orange) |

> **14 categories** total. `API`, `Data`, `Observability`, and `Tooling` were split out of overloaded categories later (REST+GraphQL, Database, logs/metrics/traces, build+Git) — they are real categories, not sub-values. `Execution` is for personalized plans tied to a specific user. One-off categories (e.g., `Company`, `Infra`, `Mobile`, `Serverless`, `Testing`) appear only in 80-lane planning docs; keep them out of new content files.

---

## Badges

All content files and INDEX.md files use [shields.io](https://shields.io/) badges for visual metadata.

### Badge URL Format

```
https://img.shields.io/badge/<label>-<value>-<color>
```

URL-encode%20special characters:
- Spaces → `%20` (preferred over `_` for readability)
- `&` → `%26`

> **Note:** Every file type carries badges. Content files carry **Section / Category / Tags** badges (3) below their HTML-comment metadata; INDEX.md files carry **Files / Category / Status** badges (3). There is **no YAML frontmatter anywhere in this repo** — metadata lives in the HTML comment, never in `---` blocks.

### INDEX.md Badges (3 per file)

```text
[![Files](https://img.shields.io/badge/files-10-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
```

The Files badge links to the **central INDEX.md** at the repo root (relative path from the file's folder — e.g. `../INDEX.md` from `40-platform/`, `../../INDEX.md` from `40-platform/40.1-docker/`); some category INDEXes link it to an in-file anchor instead. Category and Status badges link to `#`. Root-level `INDEX.md` and this guide use the same format.

### Standard Badge Colors

Category badge colors follow the **Category Values** table above (one color per category, used on both content and INDEX category badges). The fixed labels use these colors:

| Badge label | Color | Notes |
| ------------------- | -------------------------------------- | ------------------------------------------------------------- |
| `section` (content) | `blue` | Always blue, whatever the section |
| `tags` (content) | `lightgrey` | Always lightgrey |
| `files` (INDEX) | `blue` | Always blue |
| `status` | `brightgreen` / `yellow` / `lightgrey` | `complete` / `in-progress` / `planned` (see below) |

### Status Badge Values

- `complete` → `brightgreen`
- `in-progress` → `yellow` (use when applicable)
- `planned` → `lightgrey` (use when applicable)

### Tags Badge Values (URL-encoded)

There is no separate "type" badge — the Tags badge carries the `tags:` values from the HTML comment, kebab-cased and joined with a `·` separator when there is more than one:

| Comment `tags:` | Tags badge URL value |
| ------------------------------- | ------------------------------------------------- |
| `concept` | `concept` |
| `concept, reference` | `concept%20%C2%B7%20reference` |
| `interview-questions, practice` | `interview-questions%20%C2%B7%20practice` |

---

## Content Structure

### Standard Concept Files

Every concept file follows this exact section order. Sections that are not applicable may be omitted, but the order below is the canonical structure:

```text
# Title

[badges]

## TL;DR

1-3 sentences distilling the concept.

## Definition

What is this concept? A clear, concise definition in 1-3 sentences. Follow with an ASCII diagram or bullet list for clarity.

## Why Do We Need It?

Numbered reasons explaining the importance and use cases.

## How It Works

Detailed explanation with ASCII diagrams inside `text` code blocks. Break down internal mechanics.

## Code Examples

Practical TypeScript code examples demonstrating the concept. Use `typescript` language tag.

## Real-World Use Cases

3-5 real-world scenarios where this concept is applied. Each with a code example.

## Common Mistakes

4-6 common mistakes with code examples showing the bad and good patterns.

## Best Practices

Numbered list of recommended practices.

## Performance Considerations

Optional section for performance implications, trade-offs, and optimization tips.

## Summary

Concise summary of key takeaways. 3-7 bullet points.

## Cheat Sheet

Either a `text` code block with `═══════` headers and `•` bullets, OR a markdown table with `| Concept | Description |` columns.

---

## See Also
- [Kubernetes](../40.2-kubernetes/INDEX.md)
- [Microservices](../../20-backend/20.6-microservices/INDEX.md)

## References & Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
```

### Section Rules

1. **`## TL;DR`** — Optional but standard (most concept files open with it); `## Definition` is required for all concept files and follows `TL;DR` when present.
2. **`## Summary`** — Required for all content files. Must appear near the end.
3. **`## Cheat Sheet`** — Present in ~78% of content files (measured 2026-09-03). Either as a **`text` code block** (detailed content) or a **markdown table** (quick reference pairs).
4. **`## See Also`** — Required for all content files. Relative links to related sections.
5. **`## References & Learn More`** — Required for all content files. External resource links.
6. **`## Code Examples`** — Required for all concept files. Uses `typescript` (or appropriate) language tag.
7. **`## Interview Questions`** — Optional. Can appear before `## Summary` in concept files that include inline Q&A.
8. **Separator**: The `---` horizontal rule goes **between** `## Cheat Sheet` and `## See Also`. All content sections (Definition → Cheat Sheet) come before `---`; cross-references and references come after `---`.

### Why and Common Mistakes Variants

Concept files typically use **numbered lists** or **bullet lists** for these sections. However, DevOps-focused files (Docker, Kubernetes, CI/CD) often use **table formats** for clarity:

**Table format for Why:**
```text
## Why Do We Need It?

| Problem               | Solution                          |
| --------------------- | --------------------------------- |
| "Works on my machine" | Consistent environment via images |
| Manual server setup   | Declarative configuration         |
```

**Table format for Common Mistakes:**
```text
## Common Mistakes

| Mistake            | Fix                   |
| ------------------ | --------------------- |
| Using `latest` tag | Pin specific versions |
| Running as root    | Use non-root user     |
```

Either format is acceptable — choose the one that best suits the content.

## Cheat Sheet Format

Two formats are used depending on content:

**Code-block format** (416 files, measured 2026-09-03) — for detailed textual summaries:

````text
## Cheat Sheet
```text
TOPIC CHEAT SHEET
═══════════════════════════════════════

SECTION:
• Item description
• Item description

BEST PRACTICES:
• Always do this
• Never do that
```
````

**Table format** (86 files, measured 2026-09-03) — for structured concept/definition pairs:

```text
## Cheat Sheet

| Concept | Description       |
| ------- | ----------------- |
| Name    | Short description |
| Name    | Short description |
```

---

## INDEX.md Format

Every section has an `INDEX.md` file. Format:

```text
# Docker — Index

> **10 files** — Docker fundamentals from images and containers to volumes, networks, Compose, multi-stage builds, runtime internals (namespaces/cgroups), supply chain security (signing/SBOM), rootless & sandboxed runtimes, production patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

| # | File | Topics | Read time |
| --: | -------------------------- | ----------------------------------------------------- | --------: |
| 01 | [Images & Containers](40.1.01-images-containers.md) | Dockerfile, layers, CMD vs ENTRYPOINT | 25 min |
| 02 | [Volumes & Networks](40.1.02-volumes-networks.md) | Bind mounts, volumes, bridge/host/overlay networks | 25 min |

---

**Cross-references:** [CI/CD](../40.3-ci-cd) | [Microservices](../../20-backend/20.6-microservices/INDEX.md)

---

## Navigation

[← Previous: Microservices](../../20-backend/20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Kubernetes →](../40.2-kubernetes/INDEX.md)
```

> The Files badge links to the **central INDEX.md** at the repo root (relative path from the file's folder, e.g. `../../INDEX.md`); Category/Status link to `#`. File rows link each chapter by its actual `<stack>.<seq>-slug.md` name.

### INDEX.md Rules

- **Badges**: Always 3 badges: Files (blue, links to the central repo-root INDEX.md), Category (section-specific color), Status (brightgreen)
- **Table**: 4 columns: `#`, `File` (linked), `Topics` (comma-separated keywords), `Read time` (most stack INDEXes include it; category INDEXes may drop it)
- **Cross-references**: Bold `**Cross-references:**` with pipe-separated links to related sections
- **Navigation**: Previous (sibling section), Back to Index, Next (sibling section). Use `·` as separator.
- The first/last section in a series may show `(start of series)` / `(end of series)` instead of a sibling link.

---

## Code Blocks

### Language Tags

All opening code blocks **must** have a language tag. Use the **full, official** tag name:

| Correct | Incorrect |
| ------------ | --------------- |
| `typescript` | `ts` |
| `javascript` | `js` |
| `python` | `py` |
| `bash` | `shell` or `sh` |
| `yaml` | `yml` |
| `graphql` | `gql` |

### Supported Language Tags

| Tag | Usage |
| ------------ | -------------------------------------------------- |
| `typescript` | TypeScript/JavaScript code examples |
| `javascript` | Vanilla JS examples |
| `python` | Python/backend examples |
| `java` | Java examples (SDE Role section) |
| `sql` | SQL queries and schema |
| `bash` | Shell commands |
| `yaml` | YAML config (Docker, K8s, CI/CD) |
| `json` | JSON payloads and responses |
| `text` | ASCII diagrams, plain text output, terminal output |
| `html` | HTML markup |
| `css` | CSS styles |
| `graphql` | GraphQL queries and schemas |
| `dockerfile` | Dockerfile syntax |
| `go` | Go examples |
| `rust` | Rust examples |
| `ruby` | Ruby examples |
| `scss` | SCSS styles |
| `protobuf` | Protocol Buffer definitions |
| `promql` | Prometheus query language |
| `groovy` | Groovy/Jenkins pipeline scripts |
| `ini` | INI configuration files |
| `markdown` | Markdown formatting examples |
| `tsx` | TypeScript/React JSX (use `typescript` instead) |
| `jsx` | JavaScript/React JSX (use `typescript` instead) |

### ASCII Diagrams

Use `text` code blocks for ASCII art diagrams:

````text
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT NAME                                                                                    │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                   │
│ ┌─────────────────────────────────────────────────────┐                                           │
│ │ Sub-component                                       │                                           │
│ └─────────────────────────────────────────────────────┘                                           │
│                                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```
````

### State Tracking

When doing batch operations on code blocks (e.g., fixing language tags), always use a **state-machine approach** (tracking `in_code_block` state line-by-line) rather than regex. This prevents corrupting closing ` ``` ` markers.

---

## File Endings & Whitespace

- **All files must end with a single newline** — no more, no less
- **No trailing whitespace** on any line
- Check with: `python3 scripts/check_alignment.py` (whitespace inside code blocks is part of the alignment gate) and a quick newline/trailing-whitespace sweep:

```bash
python3 - <<'EOF'
import os
issues = []
for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for f in files:
        if not f.endswith('.md'): continue
        fp = os.path.join(root, f)
        with open(fp, 'rb') as fh:
            content = fh.read()
        for i, line in enumerate(content.split(b'\n'), 1):
            if line != line.rstrip(b' \t'):
                issues.append(f'{fp}:{i} trailing whitespace')
        if len(content) > 1 and content[-1:] != b'\n':
            issues.append(f'{fp}: missing final newline')
        elif len(content) > 2 and content[-2:-1] == b'\n' and content[-3:-2] == b'\n':
            issues.append(f'{fp}: double trailing newline')
print('\n'.join(issues) if issues else 'All md files clean')
EOF
```

---

## Cross-References & Navigation

### In Content Files (`## See Also`)

```text
## See Also
- [Coding Patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md)
- [JavaScript](10-frontend/10.1-javascript/INDEX.md)
- [TypeScript](10-frontend/10.2-typescript/INDEX.md)
```

#### Rules

- **Heading level**: Use `## See Also` (level-2). Some new files use `### See Also` (level-3) — convert to `##` when encountered.
- **Alphabetization**: Links must be **alphabetized** by link text (case-insensitive). This is enforced project-wide.
- **Placement**: `## See Also` must come **before** `## References` / `## References & Learn More`.
- **Path style**: Always use repo-relative paths from the file's own directory, pointing at the target section's `INDEX.md` (e.g., `../../20-backend/20.6-microservices/INDEX.md`).
- **Cross-section links**: Point at the target section's `INDEX.md` (e.g., `[Microservices](../../20-backend/20.6-microservices/INDEX.md)`), not a bare directory.
- **Intra-section links**: When linking to another file within the same section, link to the specific file (e.g., `[HPA Scaling](../03-scaling/40.2.3.01-hpa-scaling.md)`). This is common — ~32% of all See Also links point to specific files (measured 2026-09-03); most of those are intra-section.

#### Accepted Link Formats

| Variant | Example | Usage |
| ----------------- | ------------------------------------------------------------------- | -------------------------------------- |
| Section INDEX | `- [Microservices](../../20-backend/20.6-microservices/INDEX.md)` | Cross-section links (64% of links) |
| Specific file | `- [HPA Scaling](../03-scaling/40.2.3.01-hpa-scaling.md)` | Intra-section links (32% of links) |
| Section directory | `- [CI/CD](../40.3-ci-cd)` | Same-section sibling dir (4% of links) |

### In Content Files (`## References & Learn More`)

```text
## References & Learn More

- [Resource Title](https://example.com/)
- [Another Resource](https://example.com/)
```

- **Preferred heading**: `## References & Learn More` (used by ~96% of files, measured 2026-09-03)
- **Accepted variant**: `## References` (~4% of files — acceptable when referencing fewer external resources)
- Links should point to high-quality, authoritative resources
- Official documentation, books, and well-known tutorials are preferred

### In INDEX.md (`**Cross-references:**`)

```text
**Cross-references:** [JavaScript](10-frontend/10.1-javascript/INDEX.md) | [TypeScript](10-frontend/10.2-typescript/INDEX.md) | [Coding Patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md)
```

- Pipe-separated links
- Bold prefix: `**Cross-references:**`
- Links point to section directories

### In INDEX.md (`## Navigation`)

```text
## Navigation

[← Previous: Microservices](../../20-backend/20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Kubernetes →](../40.2-kubernetes/INDEX.md)
```

- Three links: Previous (left arrow), Home (house icon), Next (right arrow)
- Use `·` as separator
- Study order follows the numbering (`40.1` → `40.2` → ... → `40.12`)
- A stack INDEX links to its sibling stacks; a category INDEX links back to its stack (`../INDEX.md`) and on to the next category

---

## Special File Types

### Interview Questions

These files (e.g., `10-frontend/10.6-animation/10.6.08-interview-questions.md`) follow a different structure:

```text
# Section Interview Questions

[badges]

## N Most Asked [Section] Interview Questions

### Beginner Level (10 Questions)

**Q1: What is a closure?**

A: A closure is...

**Q2: ...**

### Intermediate Level (10 Questions)

### Senior Level (15 Questions)

### FAANG-style (10 Questions)

**Q36: Design X from scratch.**

```typescript
// Implementation
```

### Follow-up Questions (5 Questions)

## Summary

## Cheat Sheet

```text
...
```

---

## See Also
- ...

## References & Learn More
- ...
```

- Uses `## See Also` and `## References & Learn More` like concept files
- **Bottom section**: Uses `## Cheat Sheet` as the bottom section (standardized project-wide). Both `## Quick Reference` and `### Quick Reference` have been migrated.
- Questions are grouped by difficulty level with H3 headings

### System Design Case Studies

These files (e.g., `30-architecture/30.2-system-design/02-case-studies/30.2.2.01-url-shortener.md`) follow a case-study structure:

```text
# Title System Design

[badges]

## Requirements
### Functional Requirements
### Non-Functional Requirements

## Capacity Estimation

## API Design

## Database Design
### Schema

## Architecture
### ASCII Architecture Diagram

## Key Components

## Caching Strategy

## Message Queue

## Scaling Strategy

## Failure Handling

## Monitoring

## Trade-offs

## Summary

---

## See Also
- ...

## References & Learn More
- ...
```

- The Requirements section serves as the "Definition" equivalent
- Has `## Summary`, `## See Also`, `## References & Learn More` like other files
- Uses `text` code blocks for architecture diagrams
- Uses `sql`, `yaml`, `python`, `typescript` as appropriate for code

### CheatSheet Files

These files (e.g., `70-interview-toolkit/70.3-cheatsheets/70.3.05-system-design-cheat-sheet.md`) start with:

```text
# Title Cheat Sheet

[badges]

## Quick Reference Table

| Concept | Key Point | Code/Example |
| ------- | --------- | ------------ |
```

- No `## Definition`, `## Why Do We Need It?`, etc.
- `## Quick Reference Table` is the first content section
- Has `## Top 10 Things to Remember`, `## Common Patterns`, and similar section-specific content
- Has `## Summary`, `## References & Learn More` at the end

### Behavioral Guides

These files (in `70-interview-toolkit/70.1-behavioral/`) start with a `## Table of Contents` rather than `## Definition`:

```text
# Title

[badges]

## Table of Contents

- [Section](#section)
```

- Narrative/storytelling style rather than reference style
- Has `## Summary` and `## References & Learn More` at the end

### Coding Pattern Guides

These files (in `70-interview-toolkit/70.2-coding-patterns/`) describe algorithmic patterns for interview preparation. They have a unique structure optimized for problem-solving:

```text
# Pattern Name

[badges]

## Definition

## When to Use

Identifying criteria for when this pattern applies.

## Template

Code skeleton showing the core pattern structure (usually 1-2 variants).

## How It Works

ASCII diagram showing the pattern in action, with step-by-step visual walkthrough.

## Code Examples (TypeScript)

3-6 problems from easy to hard, each with:
- Problem statement
- TypeScript implementation
- Example usage with expected output

## Common Mistakes

## Time/Space Complexity

Table format showing complexity for different problem variants:

| Complexity | Variant A | Variant B |
| ---------- | --------- | --------- |
| Time | O(n) | O(n²) |
| Space | O(1) | O(n) |

## Interview Problems

Grouped by difficulty (Easy / Medium / Hard), each with LeetCode number:

### Easy

1. **Problem Name** (LeetCode N)

### Medium

### Hard

## Summary

## Cheat Sheet
```text
...
```

- Uses `## When to Use` instead of `## Why Do We Need It?`
- Has a `## Template` section (unique to Coding Pattern files)
- Uses `## Time/Space Complexity` instead of `## Performance Considerations`
- Uses `## Interview Problems` with difficulty groups and LeetCode references instead of `## Interview Questions`
- Follows the standard `## Summary` and `## Cheat Sheet` conventions

### SDE Role Guides

These files (in `81-lanes-indian-sde-faang/`, e.g., `81-lanes-indian-sde-faang/81.01-complete-guide.md`) are comprehensive study guides covering multiple topics per file:

- Use repeated sub-heading patterns (e.g., multiple `## Concept`, `## Implementation` sections)
- This is intentional — each topic within a file has its own flow
- Code blocks use `text` tag for conceptual explanations, code patterns, and ASCII diagrams
- Code blocks use `java`, `typescript`, `sql`, etc. for actual code examples
- Has `## See Also` and `## References & Learn More` at the end

---

## Verification Checklist

After making changes, verify the following:

### Required for All New Files

- [ ] Content file opens with the HTML comment `<!-- section: … | category: … | tags: … -->` (no YAML frontmatter)
- [ ] Content file carries 3 badges below the comment: Section (blue), Category (per the Category Values table), Tags (lightgrey)
- [ ] INDEX.md files have 3 badges: Files (blue, links to central repo-root `INDEX.md`), Category, Status
- [ ] All badge URLs follow shields.io conventions
- [ ] Badge values URL-encoded properly (spaces → `%20`)
- [ ] `## Summary` section present (near end of file)
- [ ] `## See Also` section present with correct relative links
- [ ] `## References & Learn More` section present

### File-Type-Specific Structure

**Standard concept files** (most sections):
- [ ] Section order: Definition → Why → How → Code Examples → Real-World → Mistakes → Best Practices → Performance → Summary → Cheat Sheet
- [ ] `## TL;DR` (when present) or `## Definition` is the first content section after metadata/badges
- [ ] `## Code Examples` uses `typescript` language tag
- [ ] If `## Cheat Sheet` is present, the `---` separator goes between it and `## See Also`

**Coding Pattern files** (`70-interview-toolkit/70.2-coding-patterns/`):
- [ ] Uses `## When to Use` instead of `## Why Do We Need It?`
- [ ] Has `## Template` section with code skeleton
- [ ] Section order: Definition → When to Use → Template → How It Works → Code Examples → Common Mistakes → Time/Space Complexity → Interview Problems → Summary → Cheat Sheet
- [ ] Has `## Time/Space Complexity` table instead of `## Performance Considerations`
- [ ] Has `## Interview Problems` grouped by Easy/Medium/Hard with LeetCode references

**Interview Questions files** (last file in each stack/category, `<stack>.<cat>.<seq>-interview-questions.md`):
- [ ] Uses `## Cheat Sheet` as the bottom section (standardized project-wide)
- [ ] Questions grouped by difficulty with H3 headings (Beginner / Intermediate / Senior / FAANG-style)
- [ ] Has `## N Most Asked [Section] Interview Questions` as first section

**System Design case studies** (`30-architecture/30.2-system-design/02-case-studies/`):
- [ ] Starts with `## Requirements` (Functional + Non-Functional) instead of `## Definition`
- [ ] Has `## Capacity Estimation`, `## API Design`, `## Database Design` sections
- [ ] Architecture diagrams in `text` code blocks
- [ ] Has `## Trade-offs` section before `## Summary`

**CheatSheet files** (`70-interview-toolkit/70.3-cheatsheets/`):
- [ ] Starts with `## Quick Reference Table` as first content section
- [ ] No `## Definition` or `## Why Do We Need It?` sections

**Behavioral guides** (`70-interview-toolkit/70.1-behavioral/`):
- [ ] Starts with `## Table of Contents` instead of `## Definition`
- [ ] Uses narrative/storytelling style

**Lane guides** (`81-lanes-indian-sde-faang/` and `80-lanes-abroad-full-stack/` numbered `NN.x` files):
- [ ] Uses `## See Also` and `## References & Learn More` at the end
- [ ] Code blocks use `java`, `text`, `typescript`, `sql` as appropriate

### Why and Common Mistakes Format

- [ ] **Concept files**: Use numbered or bullet lists for these sections
- [ ] **DevOps files** (Docker, K8s, CI/CD): May use `| Problem \| Solution |` table for Why and `| Mistake \| Fix |` table for Common Mistakes
- [ ] Either format is acceptable — but the format should be consistent within each section

### Code Blocks

- [ ] All opening code blocks have a language tag
- [ ] No `ts`, `js`, `shell`, `sh`, `py`, `yml`, `gql` — use full tag names (`typescript`, `javascript`, `bash`, `python`, `yaml`, `graphql`)
- [ ] ASCII diagrams use `text` tag
- [ ] Opening and closing ` ``` ` are balanced (same count)

### See Also

- [ ] `## See Also` uses level-2 heading (`##`), not level-3 (`###`)
- [ ] Links are alphabetized by display text (case-insensitive)
- [ ] `## See Also` comes before `## References` / `## References & Learn More`
- [ ] Cross-section links point at the target section's `INDEX.md` via a repo-relative path (e.g., `../../20-backend/20.6-microservices/INDEX.md`)
- [ ] Intra-section links may use specific file references (e.g., `../03-scaling/40.2.3.01-hpa-scaling.md`)

### File Quality

- [ ] File ends with exactly one trailing newline
- [ ] No trailing whitespace on any line
- [ ] No duplicated sections or headings
- [ ] No broken internal links
- [ ] INDEX.md has `## Navigation` with correct previous/next links
- [ ] INDEX.md has `**Cross-references:**` with related sections
### Running Verification

Run the one-command gate from the repo root before pushing:

```bash
bash scripts/verify.sh
```

It runs, in order, with clear pass/fail output:

| Check | Command | What it verifies |
| --------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Count guard | `python3 scripts/check_counts.py` | Repo-total scale claims ("810 files, 347K lines") match live disk |
| Alignment | `python3 scripts/check_alignment.py` | Markdown table pipes and ASCII box walls align; `--fix` repairs in place |
| Structure | `python3 scripts/check_structure.py` | IDs unique, sequences contiguous, interview files last (known lane-80.x GAPS are intentional and reported as baseline) |
| Link check | `python3 scripts/check_links.py` | Fence-aware broken-link scan — every relative prose link resolves to a real file (external URLs and anchor-only links are skipped) |
| Freshness gate | `python3 scripts/check_freshness.py` | Stale-API signature scan — flags deprecated APIs and dead/dated reference URLs in code fences (fake archive timestamps, retired OWASP cheat-sheet URL forms, `url.parse`, sync Next.js `params`, Pages Router exports outside the Next.js stack, `new Buffer()`, setTimeout chunking) |
| Link baseline | `python3 scripts/link_baseline.py` | External-link audit: `--update` snapshots every cited URL into `scripts/external-links-baseline.json`; bare run diffs the tree against it (exit 1 on unverified ADDED urls); `--probe` GET-probes all baseline URLs. Audit tool, not a per-commit gate |

Each script also runs standalone; all exit non-zero on failure so they can gate CI.

### Quick Troubleshooting

| Issue                                 | Most Likely Cause                                    | Fix                                                               |
| ------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| Badge displays wrong color            | Color value has wrong format or includes extra space | Ensure format: `blueviolet`, `success`, `#800080` (lowercase hex) |
| `%20` not rendering in badge          | URL encoding not applied                             | Replace literal spaces with `%20` in badge URL value portion      |
| Code block not rendering              | Missing closing ` ``` `                              | Check that every opening ` ``` ` has a matching closing ` ``` `   |
| Double newline at end of file         | File has 2+ trailing newlines                        | Use `rstrip(b'\\n') + b'\\n'` to normalize                        |
| Broken `## See Also` link             | Relative path points to wrong directory              | Use `../NN.N-slug/` (target stack folder); verify it exists         |
| Navigation link goes to wrong section | Previous/next links out of sequence                  | Verify section follows the 00→81 numbering order                  |
