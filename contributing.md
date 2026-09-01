# Contributing Guide

> **Formatting conventions and best practices** for the Senior Full Stack Interview Bible.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [File Naming](#file-naming)
- [File Metadata](#file-metadata-html-comment--shieldsiobadges)
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

This repository documents senior full-stack engineering interview topics across 33 sections in a 3-lane + 7-stack layout. All content is written in **GitHub Flavored Markdown** (`.md`).

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
├── 10-frontend/ # Frontend (JS → TS → React → Next.js)
│ ├── 10.1-javascript/
│ ├── 10.2-typescript/
│ ├── 10.3-react/
│ ├── 10.4-next.js/
│ ├── 10.5-form-handling/
│ └── 10.6-animation/
│
├── 20-backend/ # Backend (Node → NestJS → REST → DB → Security)
│ ├── 20.1-node.js/
│ ├── 20.2-nestjs/
│ ├── 20.3-rest-apis/
│ ├── 20.4-database/
│ ├── 20.5-security/
│ ├── 20.6-microservices/
│ └── 20.7-graphql/
│
├── 30-architecture/ # Architecture (design patterns + system design)
│ ├── 30.1-design-patterns/
│ └── 30.2-system-design/
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
│ └── 40.9-twelve-factor/
│
├── 50-quality/ # Quality (testing, a11y, performance)
│ ├── 50.1-testing/
│ ├── 50.2-accessibility/
│ └── 50.3-performance-monitoring/
│
├── 60-realtime/ # Real-time (WebSockets)
│ └── 60.1-websockets/
│
├── 70-interview-toolkit/ # Interview toolkit (behavioral, coding patterns, cheatsheets)
│ ├── 70.1-behavioral/
│ ├── 70.2-coding-patterns/
│ └── 70.3-cheatsheets/
│
├── lanes/ # Lane overview (indexes into 80/81)
│ └── INDEX.md
│
├── 80-lanes-abroad-full-stack/ # Abroad Full-Stack lane (EU/remote, 4-week)
│ └── INDEX.md + 18 files
│
└── 81-lanes-indian-sde-faang/ # Indian SDE / FAANG lane (DSA-heavy, 8-week)
    └── INDEX.md + 23 files
```

- **The 7 study stacks** (`10-`, `20-`, `30-`, `40-`, `50-`, `60-`, `70-`) hold the technical material both interview lanes pull from.
- **The 3 lanes** (`00-`, `80-`, `81-`) hold the interview strategy / prep plan. They are **terminal** — they reference into the stacks, never the other way around.
- Stack directories are numbered `00-` through `81-` to make it easy to slot new sections in.
- Each section has an `INDEX.md` file
- Large stacks are grouped into category subfolders (`01-`, `02-`, ... study order) with a per-category `INDEX.md`; small stacks stay flat
- Content files carry hierarchical IDs (`<stack>.<cat>.<seq>-slug.md`) or flat IDs (`<stack>.<seq>-slug.md`), always contiguous

---

## File Naming

| File Type                               | Pattern                                               | Example                                                                      |
| --------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| Stack folder                            | `NN.N-slug/`                                          | `10.1-javascript/`                                                           |
| Category folder (stacks >= ~8 chapters) | `NN-slug/` (2-digit study order)                      | `20.5-security/01-auth/`                                                     |
| Category INDEX                          | `INDEX.md` inside category folder                     | `01-auth/INDEX.md`                                                           |
| Content file in a category              | `<stack>.<cat>.<seq>-slug.md`, seq contiguous from 01 | `20.5.1.04-sessions-cookies.md` (`cat` = folder number without leading zero) |
| Content file in a flat stack            | `<stack>.<seq>-slug.md`, seq contiguous from 01       | `40.1.06-production-patterns.md`                                             |
| Interview questions file                | same rule, always LAST sequence number                | `40.1.10-interview-questions.md`                                             |

- Use **kebab-case** for slugs and directory names
- Numeric IDs are unique repo-wide and sort correctly lexicographically; sequences are contiguous (no gaps)
- Verify with: `python3 scripts/check_structure.py`

---

## File Metadata (HTML comment + shields.io badges)

Every content file **must** begin with metadata in two forms:

1. **HTML comment** (preserved for tooling, hidden in markdown renderers)
2. **shields.io badges** (visual metadata that renders as colored pills)

```markdown
<!-- section: JavaScript | category: Core | tags: concept -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](.)
[![Category](https://img.shields.io/badge/category-Core-blue)](.)
[![Tags](https://img.shields.io/badge/tags-concept-lightgrey)](.)

# File Title
```

### Rules

- **Required fields**: `section`, `category`, `tags`
- `tags` is a comma-separated list: `concept, lld, principles, theory`
- Metadata line goes BEFORE the title (H1)
- INDEX.md and README.md files do **not** have the HTML comment, but they have badges
- Badges are clickable — they link to the section root (`.`)

### Category Values

| Category        | Used For                                                         | Badge color            |
| --------------- | ---------------------------------------------------------------- | ---------------------- |
| `Core`          | JavaScript, TypeScript                                           | blue                   |
| `Frontend`      | React, Next.js, Animation, Form Handling                         | ff6b35 (orange)        |
| `Backend`       | Node.js, NestJS                                                  | success (green)        |
| `API`           | REST APIs, GraphQL                                               | ff6b35 (orange)        |
| `Data`          | Database                                                         | 8b5cf6 (purple)        |
| `Architecture`  | System Design, Microservices, Security, Design Patterns          | 800080 (dark purple)   |
| `DevOps`        | Docker, Kubernetes, CI/CD, Serverless                            | ff7f00 (devops orange) |
| `Observability` | Observability (logging, monitoring, tracing, SLI/SLO, alerting)  | 0ea5e9 (sky)           |
| `Tooling`       | Build Tools, Git Advanced                                        | 64748b (slate)         |
| `Quality`       | Testing, Accessibility, Performance Monitoring                   | 8b5cf6 (purple)        |
| `Real-Time`     | WebSockets                                                       | f59e0b (amber)         |
| `Interview`     | Behavioral, Interview Strategy, Coding Patterns, SDE Role, lanes | red                    |
| `Reference`     | CheatSheets, Monorepo                                            | lightgrey              |
| `Execution`     | Personal execution plans (e.g., Berlin plan)                     | ff6b35 (orange)        |

> **14 categories** total. The `Execution` category is for personalized plans tied to a specific user.

### Category Values

| Category        | Used For                                                        |
| --------------- | --------------------------------------------------------------- |
| `Core`          | JavaScript, TypeScript                                          |
| `Frontend`      | React, Next.js, Animation, Form Handling                        |
| `Backend`       | Node.js, NestJS                                                 |
| `API`           | REST APIs, GraphQL                                              |
| `Data`          | Database                                                        |
| `Architecture`  | System Design, Microservices, Security, Design Patterns         |
| `DevOps`        | Docker, Kubernetes, CI/CD, Serverless                           |
| `Observability` | Observability (logging, monitoring, tracing, SLI/SLO, alerting) |
| `Tooling`       | Build Tools, Git Advanced                                       |
| `Interview`     | Behavioral, Interview Strategy, Coding Patterns, SDE Role       |
| `Reference`     | CheatSheets, Monorepo                                           |
| `Quality`       | Testing, Accessibility, Performance Monitoring                  |
| `Real-Time`     | WebSockets                                                      |

> **13 categories** total. Newer additions (split from overloaded categories): `API` (REST + GraphQL), `Data` (Database), `Observability` (logs/metrics/traces), `Tooling` (build + Git).

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

> **Note:** Badges are only used on INDEX.md files. Content files do not use badges — their metadata (section, type/category, status) is stored in YAML frontmatter instead.

### INDEX.md Badges (3 per file)

```text
[![Files](https://img.shields.io/badge/files-20-blue)](INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)
```

Root-level files (root `INDEX.md`, `README.md`, `CONTRIBUTING.md`) also use badges with the same format.

### Standard Badge Colors

| Color           | Usage                           | Section Examples                                |
| --------------- | ------------------------------- | ----------------------------------------------- |
| `blueviolet`    | Core sections                   | JavaScript, TypeScript                          |
| `success`       | Backend sections                | Node.js, NestJS                                 |
| `#ff6b35`       | API sections                    | REST APIs, GraphQL                              |
| `#8b5cf6`       | Data sections                   | Database                                        |
| `green`         | Quality sections                | Testing, Accessibility, Performance Monitoring  |
| `red`           | Interview sections              | Behavioral, Interview Strategy, Coding Patterns |
| `orange`        | Practice/Questions              | Interview Questions                             |
| `lightgrey`     | Reference sections              | CheatSheets, Monorepo                           |
| `informational` | DevOps type badges, file counts | Docker, Kubernetes, CI/CD, Serverless           |
| `#0ea5e9`       | Observability sections          | Observability                                   |
| `#64748b`       | Tooling sections                | Build Tools, Git Advanced                       |
| `blue`          | Type badges, file counts        | Some sections                                   |
| `brightgreen`   | Status: complete                | All files                                       |
| `#800080`       | System Design                   | 11-System-Design                                |
| `#00b4d8`       | React                           | 03-React                                        |
| `#ff7f00`       | NestJS                          | 06-NestJS                                       |
| `#ffd700`       | Coding Patterns                 | 19-Coding-Patterns                              |
| `yellow`        | Cheat Sheets                    | 20-CheatSheets                                  |

### Status Badge Values

- `complete` → `brightgreen`
- `in-progress` → `yellow` (use when applicable)
- `planned` → `lightgrey` (use when applicable)

### Type Badge Values (URL-encoded)

| Display Value       | Encoding                |
| ------------------- | ----------------------- |
| Concept             | `Concept`               |
| Interview Questions | `Interview%20Questions` |
| Cheat Sheet         | `Cheat%20Sheet`         |
| Overview            | `Overview`              |
| Guide               | `Guide`                 |
| Tool                | `Tool`                  |
| Reference           | `Reference`             |
| Study Plan          | `Study%20Plan`          |
| Practice            | `Practice`              |

---

## Content Structure

### Standard Concept Files

Every concept file follows this exact section order. Sections that are not applicable may be omitted, but the order below is the canonical structure:

```text
# Title

[badges]

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
- [Another Section](../yy-Section/)
- [Related Section](../xx-Section/)

## References & Learn More

- [Resource Title](https://example.com/)
- [Another Resource](https://example.com/)
```

### Section Rules

1. **`## Definition`** — Must be the first content section after badges. Required for all concept files.
2. **`## Summary`** — Required for all content files. Must appear near the end.
3. **`## Cheat Sheet`** — Present in ~58% of files. Either as a **`text` code block** (detailed content) or a **markdown table** (quick reference pairs).
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

**Code-block format** (122 files) — for detailed textual summaries:

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

**Table format** (31 files) — for structured concept/definition pairs:

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
# Section Name — Index

> **N files** — Brief description of the section.

[![Files](https://img.shields.io/badge/files-N-blue)](INDEX.md)
[![Category](https://img.shields.io/badge/category-Name-color)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

| #   | File                         | Topics             |
| --- | ---------------------------- | ------------------ |
| 01  | [File Name](01-File-Name.md) | Topic descriptions |
| 02  | [File Name](02-File-Name.md) | Topic descriptions |

---

**Cross-references:** [Related Section](../xx-Section/) | [Another Section](../yy-Section/)

---

## Navigation

← Previous: `../xx-Section/INDEX.md` · [ Back to Index](INDEX.md) · Next: `../yy-Section/INDEX.md`
```

### INDEX.md Rules

- **Badges**: Always 3 badges: Files (blue), Category (section-specific color), Status (brightgreen)
- **Table**: 3 columns: `#`, `File` (linked), `Topics` (comma-separated keywords)
- **Cross-references**: Bold `**Cross-references:**` with pipe-separated links to related sections
- **Navigation**: Links to previous section INDEX.md, root INDEX.md, and next section INDEX.md. Use `·` as separator.
- The first section (00) shows `(start of series)` for previous; the last section shows `(end of series)` for next.

---

## Code Blocks

### Language Tags

All opening code blocks **must** have a language tag. Use the **full, official** tag name:

| Correct      | Incorrect       |
| ------------ | --------------- |
| `typescript` | `ts`            |
| `javascript` | `js`            |
| `python`     | `py`            |
| `bash`       | `shell` or `sh` |
| `yaml`       | `yml`           |
| `graphql`    | `gql`           |

### Supported Language Tags

| Tag          | Usage                                              |
| ------------ | -------------------------------------------------- |
| `typescript` | TypeScript/JavaScript code examples                |
| `javascript` | Vanilla JS examples                                |
| `python`     | Python/backend examples                            |
| `java`       | Java examples (SDE Role section)                   |
| `sql`        | SQL queries and schema                             |
| `bash`       | Shell commands                                     |
| `yaml`       | YAML config (Docker, K8s, CI/CD)                   |
| `json`       | JSON payloads and responses                        |
| `text`       | ASCII diagrams, plain text output, terminal output |
| `html`       | HTML markup                                        |
| `css`        | CSS styles                                         |
| `graphql`    | GraphQL queries and schemas                        |
| `dockerfile` | Dockerfile syntax                                  |
| `go`         | Go examples                                        |
| `rust`       | Rust examples                                      |
| `ruby`       | Ruby examples                                      |
| `scss`       | SCSS styles                                        |
| `protobuf`   | Protocol Buffer definitions                        |
| `promql`     | Prometheus query language                          |
| `groovy`     | Groovy/Jenkins pipeline scripts                    |
| `ini`        | INI configuration files                            |
| `markdown`   | Markdown formatting examples                       |
| `tsx`        | TypeScript/React JSX (use `typescript` instead)    |
| `jsx`        | JavaScript/React JSX (use `typescript` instead)    |

### ASCII Diagrams

Use `text` code blocks for ASCII art diagrams:

````text
```text
┌─────────────────────────────────────────────────────────────┐
│ COMPONENT NAME │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Sub-component │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────┘
```
````

### State Tracking

When doing batch operations on code blocks (e.g., fixing language tags), always use a **state-machine approach** (tracking `in_code_block` state line-by-line) rather than regex. This prevents corrupting closing ` ``` ` markers.

---

## File Endings & Whitespace

- **All files must end with a single newline** — no more, no less
- **No trailing whitespace** on any line
- Use the project's Python verification script: `python3 -c "
import os, re
issues = []
for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for f in files:
        if not f.endswith('.md'): continue
        fp = os.path.join(root, f)
        with open(fp, 'rb') as fh:
            content = fh.read()
        for i, line in enumerate(content.split(b'\\n'), 1):
            if line != line.rstrip(b' \\t'):
                issues.append(f' {fp}:{i} trailing whitespace')
        if len(content) > 1 and content[-1:] != b'\\n':
            issues.append(f' {fp}: missing final newline')
        elif len(content) > 2 and content[-2:-1] == b'\\n' and content[-3:-2] == b'\\n':
            issues.append(f' {fp}: double trailing newline')
if issues:
    print('Issues found:')
    for i in issues: print(i)
else:
    print(' All 299 files clean')
"
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
- **Path style**: Always use relative paths (e.g., `../xx-Section/`).
- **Cross-section links**: Link to the section directory (e.g., `../01-JavaScript/`), not a specific file.
- **Intra-section links**: When linking to another file within the same section, link to the specific file (e.g., `../05-HPA-Scaling.md`). This is acceptable — ~12% of all See Also links are intra-section file references.

#### Accepted Link Formats

| Variant           | Example                                                             | Usage                              |
| ----------------- | ------------------------------------------------------------------- | ---------------------------------- |
| Section directory | `- [React](10-frontend/10.3-react/)`                                | Cross-section links (88% of links) |
| Specific file     | `- [Jest](50-quality/50.1-testing/02-frameworks/50.1.2.01-jest.md)` | Intra-section links (12% of links) |
| Nested path       | `- [REST APIs](20-backend/20.3-rest-apis/)`                         | Cross-section from subdirectories  |

### In Content Files (`## References & Learn More`)

```text
## References & Learn More

- [Resource Title](https://example.com/)
- [Another Resource](https://example.com/)
```

- **Preferred heading**: `## References & Learn More` (used by ~90% of files)
- **Accepted variant**: `## References` (used by ~10% of files — acceptable when referencing fewer external resources)
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

← Previous: `../xx-Section/INDEX.md` · [ Back to Index](INDEX.md) · Next: `../yy-Section/INDEX.md`
```

- Three links: Previous (left arrow), Home (house icon), Next (right arrow)
- Use `·` as separator
- Section order follows the numbering (00 → 01 → 02 → ... → 31)
- First section: `← Previous: *(start of series)*`
- Last section: `[Next: → *(end of series)*`

---

## Special File Types

### Interview Questions

These files (e.g., `20-Interview-Questions.md`) follow a different structure:

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

These files (e.g., `11-System-Design/01-URL-Shortener.md`) follow a case-study structure:

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

These files (e.g., `20-CheatSheets/System-Design-Cheat-Sheet.md`) start with:

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

These files (in `18-Behavioral/`) start with a `## Table of Contents` rather than `## Definition`:

```text
# Title

[badges]

## Table of Contents

- [Section](#section)
```

- Narrative/storytelling style rather than reference style
- Has `## Summary` and `## References & Learn More` at the end

### Coding Pattern Guides

These files (in `19-Coding-Patterns/`) describe algorithmic patterns for interview preparation. They have a unique structure optimized for problem-solving:

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
| Time       | O(n)      | O(n²)     |
| Space      | O(1)      | O(n)      |

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

These files (in `31-SDE-Role/`) are comprehensive study guides covering multiple topics per file:

- Use repeated sub-heading patterns (e.g., multiple `## Concept`, `## Implementation` sections)
- This is intentional — each topic within a file has its own flow
- Code blocks use `text` tag for conceptual explanations, code patterns, and ASCII diagrams
- Code blocks use `java`, `typescript`, `sql`, etc. for actual code examples
- Has `## See Also` and `## References & Learn More` at the end

---

## Verification Checklist

After making changes, verify the following:

### Required for All New Files

- [ ] File has YAML frontmatter with `section`, `category`, `tags`
- [ ] INDEX.md files have 3 badges: Files, Category, Status
- [ ] Content files do NOT have badges (only frontmatter metadata)
- [ ] All badge URLs follow shields.io conventions
- [ ] Badge values URL-encoded properly (spaces → `%20`)
- [ ] `## Summary` section present (near end of file)
- [ ] `## See Also` section present with correct relative links
- [ ] `## References & Learn More` section present

### File-Type-Specific Structure

**Standard concept files** (most sections):
- [ ] Section order: Definition → Why → How → Code Examples → Real-World → Mistakes → Best Practices → Performance → Summary → Cheat Sheet
- [ ] `## Definition` is the first content section after badges
- [ ] `## Code Examples` uses `typescript` language tag
- [ ] If `## Cheat Sheet` is present, the `---` separator goes between it and `## See Also`

**Coding Pattern files** (`19-Coding-Patterns/`):
- [ ] Uses `## When to Use` instead of `## Why Do We Need It?`
- [ ] Has `## Template` section with code skeleton
- [ ] Section order: Definition → When to Use → Template → How It Works → Code Examples → Common Mistakes → Time/Space Complexity → Interview Problems → Summary → Cheat Sheet
- [ ] Has `## Time/Space Complexity` table instead of `## Performance Considerations`
- [ ] Has `## Interview Problems` grouped by Easy/Medium/Hard with LeetCode references

**Interview Questions files** (`NN-Interview-Questions.md`):
- [ ] Uses `## Cheat Sheet` as the bottom section (standardized project-wide)
- [ ] Questions grouped by difficulty with H3 headings (Beginner / Intermediate / Senior / FAANG-style)
- [ ] Has `## N Most Asked [Section] Interview Questions` as first section

**System Design case studies** (`11-System-Design/`):
- [ ] Starts with `## Requirements` (Functional + Non-Functional) instead of `## Definition`
- [ ] Has `## Capacity Estimation`, `## API Design`, `## Database Design` sections
- [ ] Architecture diagrams in `text` code blocks
- [ ] Has `## Trade-offs` section before `## Summary`

**CheatSheet files** (`20-CheatSheets/`):
- [ ] Starts with `## Quick Reference Table` as first content section
- [ ] No `## Definition` or `## Why Do We Need It?` sections

**Behavioral guides** (`18-Behavioral/`):
- [ ] Starts with `## Table of Contents` instead of `## Definition`
- [ ] Uses narrative/storytelling style

**SDE Role guides** (`31-SDE-Role/`):
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
- [ ] Cross-section links use section directory format: `../XX-Section/`
- [ ] Intra-section links may use specific file references: `../NN-File.md`

### File Quality

- [ ] File ends with exactly one trailing newline
- [ ] No trailing whitespace on any line
- [ ] No duplicated sections or headings
- [ ] No broken internal links
- [ ] INDEX.md has `## Navigation` with correct previous/next links
- [ ] INDEX.md has `**Cross-references:**` with related sections
### Running Verification

Use the project's Python verification scripts:

```bash
# Check file endings and trailing whitespace
python3 -c "
import os
issues = []
for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for f in files:
        if not f.endswith('.md'): continue
        fp = os.path.join(root, f)
        with open(fp, 'rb') as fh:
            content = fh.read()
        for i, line in enumerate(content.split(b'\\n'), 1):
            if line != line.rstrip(b' \\t'):
                issues.append(f' {fp}:{i} trailing whitespace')
        if len(content) > 1 and content[-1:] != b'\\n':
            issues.append(f' {fp}: missing final newline')
        elif len(content) > 2 and content[-2:-1] == b'\\n' and content[-3:-2] == b'\\n':
            issues.append(f' {fp}: double trailing newline')
if issues:
    for i in issues: print(i)
else:
    print(' All files clean')
"

# Regenerate project statistics report
# (requires /tmp/generate_report.py from the session)
python3 /tmp/generate_report.py
```

> **Note:** The report generator script (`/tmp/generate_report.py`) was created during the formatting standardization session. It scans all 333 `.md` files and produces the `PROJECT-STATS.md` report. If the script is unavailable, you can recreate it by reviewing the existing `PROJECT-STATS.md` for the report structure or re-running the formatting audit scripts.

### Quick Troubleshooting

| Issue                                 | Most Likely Cause                                    | Fix                                                               |
| ------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| Badge displays wrong color            | Color value has wrong format or includes extra space | Ensure format: `blueviolet`, `success`, `#800080` (lowercase hex) |
| `%20` not rendering in badge          | URL encoding not applied                             | Replace literal spaces with `%20` in badge URL value portion      |
| Code block not rendering              | Missing closing ` ``` `                              | Check that every opening ` ``` ` has a matching closing ` ``` `   |
| Double newline at end of file         | File has 2+ trailing newlines                        | Use `rstrip(b'\\n') + b'\\n'` to normalize                        |
| Broken `## See Also` link             | Relative path points to wrong directory              | Use `../XX-Section/` format, verify directory exists              |
| Navigation link goes to wrong section | Previous/next links out of sequence                  | Verify section follows the 00→31 numbering order                  |
