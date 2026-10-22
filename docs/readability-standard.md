# Readability Rewrite Standard (corpus-wide, 2026-10-16; outline revision 2026-10-21)

Gold reference: `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.02-scope.md`.
Every teaching chapter must read like it: scannable, concrete, senior-deep.

## 0. Why the outline rule changed on 2026-10-21

A generated answer about `let` versus `var` was put beside this corpus's own
chapter on the same topic, and it read better. Measuring the difference rather
than guessing at it:

- **The opening was not the gap.** The generated answer states its claim first
  ("comes down to a mix of historical backward compatibility and modern
  architectural safety"), and this corpus already does the same: 504 of 521
  chapter openings carry a declarative answer sentence behind the reader hook.
- **The headings were the gap.** The generated answer names each step of its
  argument ("The Historical Accident of `var` and `globalThis`"). 500 of 738
  chapter files filed their entire mechanism under one identical pair —
  `## How It Works` plus `### 1. ...`, `### 2. ...`. A chapter's outline is its
  table of contents, its argument summary, and its in-page navigation (the
  reading rail in `assets/reading-ui.js` is built from `h2[id]`), so five
  chapters under one label each announce "How It Works" and nothing else.
  AGENTS.md already forbids the shape ("short, topic-specific headings that
  carry the explanation forward ... do not make every chapter follow the same
  sequence of generic headings"); nothing enforced it.
- **The fix was mechanical, which is why it could be corpus-wide.** The
  specific headings already existed as the umbrella's children. Gate 28
  (`scripts/check_readability.py --write`) removes the label and promotes the
  children to `##`: 488 chapters rewritten, no prose touched, every heading
  text — and therefore every `#anchor` — preserved. 0 incoming `#how-it-works`
  links existed, 0 chapters had `####` grandchildren to re-level.

## 1. The shape (complete file replacement, not patches)

1. **Meta block untouched**: keep the `<!-- section: ... -->` comment and all four
   shield badges (Section, Category, Tags, Read time) byte-identical, in order,
   targets `#`. Do NOT hand-edit the read-time value; it is recomputed globally later.
2. **Hook opening (before first H2)**: 1–3 sentences that state the claim AND
   pose the concrete problem it answers, then a minimal runnable code example
   when the topic allows. No throat-clearing. The claim comes first or arrives
   in the same breath as the question — an opening that only asks, and leaves
   the answer to section 6, reads like a riddle.
3. **## Definition**: one plain-language paragraph (bold the 1–3 load-bearing terms), then a
   `> **Textbook Definition:**` quote for the formal version.
4. **## First Principles**: short — why the mechanism must exist (failure it prevents).
5. **Mechanism sections**: numbered `## N. Title` sections, one per step of the
   argument. Each title names the move ("Lookup Walks Outward, and an Inner
   Name Shadows the Outer One"), never the container ("How It Works",
   "Explanation", "Overview", "Details", "Key Points", "Deep Dive", "In Depth",
   "Mechanism" — retired by gate 28). Each section: one idea, bold lead-ins, a
   tiny code/config snippet proving it, then 1–3 sentences of consequence.
   Tables ONLY for genuine comparisons (2–6 rows); never a table followed by
   paragraphs restating it. Subsections cited by a stable `#anchor` (from
   REVISION companions or interview banks) keep their descriptive titles
   without a number; worked examples may continue in the optional
   `## Code Examples` section; system-design case studies use their own
   requirements→design→trace walkthrough template.
6. **## Summary**: dense 3–6 sentence recap, no new facts.
7. **## See Also / ## References & Learn More / prev-next footer**: preserved
   (see section 2).
8. Optional canon sections (`Why It Matters`, `Code Examples`, `Real-World Use Cases`, `Common Mistakes`, `Best Practices`, `Performance Considerations`) only when they
   add NEW reasoning; never restate the mechanism. No Q&A / revision drills in chapters.

## 2. Preservation contract (hard rules — violations break gates)

- Keep every required section: Definition, First Principles, Summary, See Also,
  `References & Learn More` (exact `##` titles).
- Keep ALL outbound links (See Also, References, inline): same targets. Do not add
  new external URLs. If a reference URL is dead, keep it and report it.
- Heading anchors: before renaming/removing any `##`/`###` heading, grep the repo for
  `](...YourFile.md#...` incoming links. Preserve every referenced slug; if a
  referenced heading must move, keep an equivalent slug. (The 2026-10-21
  promotion preserved slugs because a slug is generated from the heading text,
  not its level — and `grep` found 0 incoming `#how-it-works` anchors.)
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
- `python3 scripts/check_readability.py` — no retired generic heading in your files.
- `python3 scripts/check_links.py` — zero broken links.
- Report: files rewritten, reference URLs kept vs dead-found, incoming anchors preserved.
