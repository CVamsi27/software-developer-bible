# Readability Rewrite Standard (corpus-wide, 2026-10-16)

Gold reference: `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.md`.
Every teaching chapter must read like it: scannable, concrete, senior-deep.

## 1. The shape (complete file replacement, not patches)

1. **Meta block untouched**: keep the `<!-- section: ... -->` comment and all four
   shield badges (Section, Category, Tags, Read time) byte-identical, in order,
   targets `#`. Do NOT hand-edit the read-time value; it is recomputed globally later.
2. **Hook opening (before first H2)**: 1–3 sentence concrete problem/question, then a
   minimal runnable code example when the topic allows. No throat-clearing.
3. **## Definition**: one plain-language paragraph (bold the 1–3 load-bearing terms),
   then a `> **Textbook Definition:**` quote for the formal version.
4. **## First Principles**: short — why the mechanism must exist (failure it prevents).
5. **## How It Works**: the mechanism as **numbered `### N. Title` subsections**
   (N = 3–7). Each subsection: one idea, bold lead-ins, a tiny code/config snippet
   proving it, then 1–3 sentences of consequence. Tables ONLY for genuine
   comparisons (2–6 rows); never a table followed by paragraphs restating it.
6. **## Summary**: dense 3–6 sentence recap, no new facts.
7. **## See Also / ## References & Learn More / prev-next footer**: preserved
   (see section 2).
8. Optional canon sections (`Why It Matters`, `Code Examples`, `Real-World Use Cases`,
   `Common Mistakes`, `Best Practices`, `Performance Considerations`) only when they
   add NEW reasoning; never restate the mechanism. No Q&A / revision drills in chapters.

## 2. Preservation contract (hard rules — violations break gates)

- Keep every required section: Definition, First Principles, Summary, See Also,
  `References & Learn More` (exact `##` titles).
- Keep ALL outbound links (See Also, References, inline): same targets. Do not add
  new external URLs. If a reference URL is dead, keep it and report it.
- Heading anchors: before renaming/removing any `##`/`###` heading, grep the repo for
  `](...YourFile.md#...` incoming links. Preserve every referenced slug; if a
  referenced heading must move, keep an equivalent slug.
- Keep all domain terms, API names, and internal mechanisms (V8/JVM/engine specifics,
  failure modes, boundaries). Cut WORDS, never topics. Senior depth is the point.
- Do not touch INDEX.md, REVISION.md, interview-question banks, or any other file.
- Do not commit anything. Leave changes uncommitted in the working tree.

## 3. Readability rules

- Paragraphs: 1–3 sentences. One idea per paragraph.
- Prefer: numbered steps, short bullets with **bold lead-ins**, tiny snippets over prose.
- Every abstract claim gets a concrete instance within 5 lines (code, command, config,
  trace, or number).
- Code fences always carry a language tag; keep examples minimal but runnable in spirit.
- Delete: filler openers ("In today's world"), restated table rows, duplicated
  definitions, hedging chains. If two sentences say one thing, keep the concrete one.
- Verify technical claims against the file's existing References before writing;
  never invent API names, flags, version behavior, or performance numbers.

## 4. Per-batch verification (mandatory before reporting done)

- `python3 scripts/check_template.py` — zero violations in your files.
- `python3 scripts/check_links.py` — zero broken links.
- Report: files rewritten, reference URLs kept vs dead-found, incoming anchors preserved.
