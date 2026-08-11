<!-- section: Abroad Full-Stack Lane | category: Interview | tags: behavioral, eu, culture, reference -->
[![Section](https://img.shields.io/badge/section-Abroad%20Full-Stack%20Lane-blue)](#)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Tags](https://img.shields.io/badge/tags-behavioral%20%C2%B7%20eu%20%C2%B7%20culture%20%C2%B7%20reference-lightgrey)](#)

# Behavioral — EU Mid-Stage Style

> **EU behavioral interviews are different from FAANG.** Less "leadership principles", more "show me you can ship in a small, async, English-fluent team." This file is the framework + 15 common questions with answer skeletons.

## TL;DR

- **EU mid-stage behavioral = STAR + Reflection, 5-8 stories practiced out loud.** Same as FAANG, different emphasis.
- **Senior signal = "what would you do differently"** — show self-awareness, not just wins.
- **Async + English fluency is tested.** Written questions are common. Write clearly, don't use AI to generate.
- **Cultural fit is real but not "fit in" pressure** — they're checking you can work in a multicultural, distributed team.

See [story-bank.md](story-bank.md) for the 8 STAR+R stories you should have ready. This file is the **what they ask + how to answer** layer.

---

## The STAR+R Framework

- **Situation** (10%): 1-2 sentences, set the scene
- **Task** (10%): 1 sentence, your specific responsibility
- **Action** (40%): 2-3 sentences, what YOU did (not the team). Use "I", not "we".
- **Result** (30%): 1-2 sentences, the outcome with a metric
- **Reflection** (10%): 1 sentence, what you'd do differently or what you learned

**The Reflection is the senior signal.** It's the difference between "I shipped X" and "I'm still learning X."

---

## The 15 Most Common EU Mid-Stage Behavioral Questions

### 1. "Tell me about yourself" (60-90 sec)

**Structure:**
- Who you are (1 sentence)
- What you do now (1 sentence)
- 2-3 key achievements (30 sec)
- Why you're here (1 sentence)

**Template:**
"I'm a [role] with [X] years of experience building [domain]. Most recently at [company], I [achievement 1 with metric] and [achievement 2 with metric]. Before that, [brief context]. I'm looking for [what you want] because [reason]."

**Example:**
> "I'm a senior full-stack engineer with 5 years of experience building multi-tenant healthcare SaaS. Most recently at Docita, I shipped a production multi-tenant system from scratch as the sole engineer, supporting 50+ clinics. Before that at MAQ Software, I reduced API latency by 30% and mentored 4 engineers. I'm looking for an EU mid-stage role with a take-home + system design loop because I want to ship production code in a smaller team and build toward staff."

### 2. "Why are you leaving your current role?" (60 sec)

**The honest answer:**
- "I founded Docita 18 months ago. We hit product-market fit on the clinical SaaS, and now I'm ready to join a larger engineering team to scale my impact."
- "My current company is [pre-PMF, no Series A, etc.]. I want to join a more established team where I can focus on engineering, not fundraising."

**The red-flag answer to avoid:** "My manager is bad" / "Politics" / "I was laid off" (this one is OK to say, but say it with what you learned).

### 3. "Why this company?" (60 sec, specific, not generic)

**The structure:**
- 1 product feature or engineering blog post that excited you
- 1 specific person/team you'd learn from
- 1 thing about the company culture that aligns with how you work
- Close with "and I'm particularly excited about [specific recent product/launch]"

**Example for n8n:**
> "I read your engineering blog post on the new execution engine — the way you handled state recovery on partial failure is exactly the kind of distributed systems work I want to do. I'm also excited about [specific person, e.g., your CTO X] based on [their talk / their GitHub]. Your culture of async-first communication + the 4-day workweek policy aligns with how I work best. And I'm particularly excited about the recent [Workflow Code] launch — that's the kind of feature that opens a new category."

### 4. "Tell me about a time you had a technical disagreement"

**What they test:** Can you disagree without being disagreeable?

**Structure:**
- Situation: 1 sentence, the disagreement
- Your view: 1 sentence
- Their view: 1 sentence
- What you did: 1-2 sentences (how you resolved)
- Result: 1 sentence
- Reflection: 1 sentence

**Example skeleton:**
> "At Docita, my co-founder wanted to use MongoDB for everything because it was familiar. I thought Postgres was better for the relational data we had. We agreed to spend 2 days prototyping each, then compare. Postgres was 3x faster on our main query, and we kept it for the relational data while using Mongo for the document store. Looking back, I should have started with the prototype approach instead of arguing for 3 days first."

### 5. "Tell me about a time you had to ship under pressure"

**What they test:** Can you prioritize, communicate, and deliver?

### 6. "Tell me about a time you failed"

**What they test:** Self-awareness, learning, resilience.

### 7. "Tell me about your most impactful project"

**What they test:** Can you articulate business value, not just technical details?

### 8. "Walk me through a system you designed from scratch"

**What they test:** Can you talk architecture at the right level of detail?

### 9. "How do you handle disagreements about technical approach?"

**What they test:** Same as #4. Often asked twice in different forms.

### 10. "How do you stay current with technology?"

**What they test:** Genuine curiosity vs buzzword-chasing.

**Good answer:** "I read [specific sources: Hacker News, specific newsletters, specific blogs]. I build side projects in [technologies I want to learn]. I went deep on [X] last quarter because [Y]."

**Red-flag answer:** "I follow thought leaders on Twitter" (too passive).

### 11. "Why this location / remote / hybrid?"

**What they test:** Genuine commitment, not "I'll move back in 6 months."

**Structure:**
- Family context (if relevant): "My wife is a Pega consultant and Berlin is a Pega hub"
- Long-term commitment: "We're planning to put our kid in international school here, we're staying"
- Why this city: 1-2 specific things (Pega market, international schools, lifestyle)

### 12. "What are your salary expectations?" (often written + verbal)

**See:** [Comp Eu Benchmarking](comp-eu-benchmarking.md) for full comp strategy.

**TL;DR:** Give a range in EUR, based on the city's tier. Don't go first if you can avoid it. "Based on my research, senior full-stack roles in Berlin are EUR 75-100K base + 0.05-0.3% equity. I'm flexible based on the full package."

### 13. "What would you do in your first 90 days?"

**What they test:** Do you have a plan? Are you realistic?

**Structure:**
- Days 1-30: Learn. Read the codebase, ship a tiny PR, meet everyone.
- Days 30-60: Take ownership of one small project. Build trust.
- Days 60-90: Lead a feature or initiative. Have an opinion.

**Example:**
> "First 30 days: read the codebase, meet the team, ship a small bug fix or refactor PR. Days 30-60: take ownership of one feature or service, start pairing with team members. Days 60-90: lead a small project from design to ship, propose improvements to the dev workflow."

### 14. "Do you have any questions for us?"

**Always have 3-5 questions. They should be specific, not generic.**

**Good questions:**
- "What does the team structure look like for the role I'd be joining?"
- "What's the biggest challenge the team is facing right now?"
- "How does the team handle on-call / incident response?"
- "What's the engineering culture like — async-first, sync standups, how do you make decisions?"
- "What's the promotion path from senior to staff?"
- "What's the tech debt situation look like, and is there time allocated to pay it down?"

**Bad questions:**
- "What's the salary?" (wait for them to bring it up)
- "How many vacation days?" (ask later, after the offer)
- "What's the company culture like?" (too generic, ask something specific)

### 15. "Is there anything else we should know about you?"

**The closing question. Use it.**

**Template:** "Two things. First, [X strength]. Second, [Y motivation or context]."

**Example:** "Two things. First, I've been the sole engineer at Docita for 18 months — I can wear every hat from product to DevOps. Second, my wife is a Pega consultant, and the Netherlands is a Pega hub, so we're committed to relocating to Amsterdam long-term."

---

## Async Written Questions (very common at EU mid-stage)

SumUp, Scalable, sennder, and many others send **written questions before the live loop**. You write 1-2 page answers, asynchronously, in English.

**Tips:**
- Don't use ChatGPT to write the answer. They can tell. Use it to brainstorm, then write it yourself.
- Be specific. Use your actual numbers, actual projects, actual lessons.
- Keep it under 1 page per question. They don't want essays.
- Use the STAR+R framework even in writing.
- Edit for clarity, not for length.

**Common async questions:**
- "Tell me about a time you had a hard technical disagreement"
- "Why [company]?"
- "What would you do in your first 90 days?"
- "Describe a system you designed from scratch"
- "How do you handle disagreements on technical approach?"

---

## The 8 STAR+R Stories You Should Have Ready

See [story-bank.md](story-bank.md) for the 8 ready-to-deliver stories mapped to these 15 questions. The pattern:

1. **0→1 founding at Docita** — sole engineer shipped production multi-tenant SaaS
2. **30% API latency reduction at MAQ** — query tuning + indexing + caching
3. **25% faster delivery at MAQ** — refactoring around reusable TS patterns
4. **4 engineers mentored, 20% better sprint predictability**
5. **Microservices platform at Cognizant** — Spring Boot + Eureka + Zuul
6. **RBAC + audit logging for healthcare compliance**
7. **85% test coverage, 15% fewer production incidents**
8. **Production observability + incident response**

Each story is structured: punchline-first → 60 sec delivery → reflection. Adapt to each question, don't recite.

---

## What gets you REJECTED on behavioral

- **STAR answer is just S and T, no A or R.** They want to hear what YOU did.
- **No metric in the result.** "I improved performance" is not a result. "I improved performance by 30%" is.
- **No reflection.** Senior signal is self-awareness, not just wins.
- **"Why this company?" is generic.** "Great products, smart people" = junior answer.
- **"Tell me about a conflict" → "I don't really have conflicts"** = red flag. You do, you just haven't articulated them.
- **Generic questions at the end.** "How many vacation days?" = you're not interested in the work.
- **AI-generated written answers.** They're checking your English fluency. If your writing is suspiciously perfect, you failed.

---

## TL;DR

- **STAR+R framework:** Situation, Task, Action, Result, Reflection.
- **15 common questions** with answer skeletons above. Practice the 8 stories in [story-bank.md](story-bank.md).
- **EU-specific:** async + written questions, English fluency, family/relocation, why-this-city, salary in EUR.
- **Senior signal = Reflection.** Show what you learned, not just what you shipped.
