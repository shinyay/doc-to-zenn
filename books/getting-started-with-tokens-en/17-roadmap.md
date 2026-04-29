---
title: "Chapter 16 — A roadmap to optimization"
---

> **In one line:** You can now speak the language of tokens — **this chapter hands you a map of the optimization techniques worth learning next**, and **frames them so you can see the underlying moves behind any "trick" you read about**.

---

## Why this chapter exists

Over the previous 15 chapters you built a working understanding of what tokens really are, how they get produced from text, where they accumulate in real workloads, and what each costs you in money, latency, and answer quality. You saw that the **context window is a budget, not a feature**, that **hidden consumers like system prompts and tool schemas spend that budget before your message even arrives**, and that the relationship between cost and quality **bends, not lines**. In Chapter 15 you saw that **disciplined use isn't about saving pennies — it's about preserving the resources (attention, latency, headroom) that determine whether a system feels good to use at all**.

That's enough background. **You now have everything you need to read optimization advice critically**. When someone proposes a clever prompt trick, a new framework, or a "must-do" pattern, you can ask the **right questions**: **which bucket does it affect, what's its maintenance cost, will it survive contact with my real workload?**

This chapter isn't a tutorial — it's a **preview**. It catalogs the **technique families worth learning in a future optimization-focused guide**, and gives you the **mental model that lets you slot a new technique into the right family the moment you encounter it**.

---

## A mental model: every optimization is one of three moves

Before naming families, **name the moves**. **Almost every token optimization technique that exists (past, present, or yet to be invented) is one of three, dressed up**:

1. **Send fewer tokens**: shrink input. Trim system prompts, scope context, drop unused tool definitions, summarize history
2. **Receive fewer tokens**: shrink output. Ask for terse answers, fixed schemas, bounded length, no preamble
3. **Pay less per token**: change the price you pay for the tokens you do send and receive. Cheaper model on cheaper tasks. **Design prompts so they hit the prefix cache**. Move work to the tier that fits

```
                 ┌─────────────────────────────┐
                 │   THE THREE MOVES           │
                 ├─────────────────────────────┤
   input  ─────► │ 1. Send fewer tokens        │
                 │ 2. Receive fewer tokens     │ ◄───── output
                 │ 3. Pay less per token       │
                 └─────────────────────────────┘
```

When you encounter a new technique, **first name the move**. "**This trick reduces system prompt**" = move 1. "**Force JSON-only**" = move 2. "**Stable content at the top**" = move 3. **Once you've named the move, you can judge whether the technique applies to your situation, or whether it solves a problem you don't have**.

> [!TIP]
> If a proposed optimization doesn't cleanly map to one of the three moves, **be suspicious**. Likely **a quality change wearing a cost-saving costume**, or **a stylistic preference dressed up as engineering**.

---

## The seven families of techniques

The techniques worth learning cluster into **7 families**. **Highest return for least effort first**, in roughly the order to adopt them:

### 1. Output control

**The single highest per-token-ROI lever**. **Tell the model "be terse" once**: skip preamble, answer in N words, return JSON matching this schema, omit explanation unless asked. **That one instruction shifts every future response in the conversation**, and **shifts the more expensive bucket**. Output tokens are pricier than input, **and dominate latency because they're generated one at a time**.

Canonical example: a single system-level rule like "**Reply in one sentence unless asked otherwise**" or "**Respond in JSON matching this schema, no prose**". **A rule that fits on one line cuts output volume in chatty workloads by more than half**, with no loss of useful content.

Output control **compounds with everything else**. **Near-zero added cost, survives nearly every future change**. **One of the easiest wins to measure** — Chapter 13's usage metrics show output tokens cleanly.

---

### 2. Context scoping

**Replace always-on instructions with conditional, scoped, on-demand loading**. Instead of one giant instructions file sent on every request, **split it into many small files loaded only when their relevant workflow is active**. The **minimum sufficient context** principle from Chapter 12.

Canonical example: a project that started with a single multi-thousand-token instructions doc (covering every workflow the team imagined) and ended with **a small core file plus a dozen small, named, on-demand-loaded files**. **Per-request input dropped substantially, and answer quality usually improved** — because the model wasn't sifting through irrelevant rules.

Scoping is **not a one-time edit, it's a continuing discipline**. Instructions files drift toward bloat as new rules are added "just in case". **Scoping habits** (quarterly review, ruthless pruning) **keep the win**.

---

### 3. Prompt compression and phrasing discipline

**The art of saying the same thing in fewer tokens** — **often more clearly**. **Declarative > imperative** ("**Output: JSON**" beats "Please always make sure to output your responses in JSON format, thanks"). **Strip politeness padding**. **Remove dead rules** (instructions covering scenarios that no longer occur). **Collapse repeated rules into one**.

Canonical example: read a hand-grown instructions file, **read every line out loud, and ask of each**: **is this still true? still needed? could I say it in half the words?** Unglamorous work, per-line savings look small, but **the cumulative effect on a long-lived prompt is substantial**.

Compression has **a quality side effect that's easy to miss**: **terser instructions are followed more reliably**. A model asked five things in a polite English paragraph often does three; **the same five as a numbered list of imperative verbs** = done more often.

---

### 4. Model selection and tiering

**Not every task needs the strongest model**. **Routing easy tasks to a smaller cheap model and reserving the frontier tier for the tasks that genuinely need it** = **one of the largest portfolio-level wins available**, because **the price gap between tiers is large** (often more than an order of magnitude, in either direction).

Canonical pattern: **a router or "auto" mode** — a lightweight first pass classifies the request, dispatches simple ones to a small model, **and only escalates the genuinely hard cases**. **Most workloads have a long tail of trivial requests** — formatting, classification, short rewrites — **that a small model handles indistinguishably from a large one, at a fraction of the cost**.

Tiering also **pays in latency**. **Small models are usually faster**, so easy cases **feel snappier and are cheaper**. The trick is **honest evaluation**: don't assume "**looks good**" — **measure on real traffic before committing**.

---

### 5. Caching discipline

**Design prompts so the stable prefix hits the prefix cache**. When the provider sees the same opening tokens it saw on a previous request, **it bills dramatically less, or skips the work entirely**. **The structural rule is simple**: **stable content at the top, volatile content at the bottom**.

Canonical anti-pattern: **timestamps, request IDs, or per-user variables at the very top of the prompt**. **That single moving token at position 1 invalidates the cache for everything that follows**, **turning a near-free prefix into a full-price one**.

Cache-friendliness can **cut effective input cost by an order of magnitude on workloads that reuse a long, stable system prompt** (most production). **It also reduces latency**, because cached prefix processing is much faster than cold.

---

### 6. Tool / MCP discipline

When you give a model access to tools (function calls, MCP servers, plugins), **every tool's definition, name, description, and parameter schema is sent on every request, whether used or not**. **A bloated catalog quietly inflates input every turn**, and as Chapter 14 noted, **tool selection quality also degrades because the model has to weigh more options**.

Canonical example: a team that connected six tool servers during exploration, never disconnected the four they stopped using, and **watched per-request input climb for unclear reasons**. The fix: **periodic audit, removing the unused, scoping the rest to workflows that need them rather than exposing them everywhere**.

**A small focused tool set is cheaper per step AND yields better tool-selection decisions**. **A rare optimization where cost and quality move together, not against each other**.

---

### 7. Workflow choice

**The most expensive optimization mistake is using the wrong interaction mode for the task**. **A quick ask** (single request, single response) = the cheapest unit of LLM work. **Edit mode** (target a specific change) = moderately expensive. **Full agent loop** (model plans, calls tools, observes results, iterates) = **can cost 5–25× the same outcome**, **because every step re-sends a growing context and produces more output**.

Canonical mistake: **reflexively reaching for an agent loop even when the task is a one-shot question**. Canonical fix: **match the mode to the task**. "What does this function do?" = ask mode, "Rename this variable across this file" = edit mode, "Investigate why the test suite started failing on Tuesday and propose a fix" = agent mode.

Workflow choice last in adoption order = **not because it's least important** (it may be the single most impactful per-request decision) — **but because it requires the other 6 families in place first**. **Once your prompts, contexts, tools, and model selection are disciplined, picking the right workflow is the move that compounds all the others**.

---

## Where to start

If you adopt these families in the order they appear, you'll see **meaningful savings from the first two, substantial savings from the first four**.

| Order | Family | Effort | Typical impact |
|-------|--------|--------|----------------|
| 1 | Output control | very low | high — immediate impact on every response |
| 2 | Context scoping | low–medium | high — reduces input on every request |
| 3 | Prompt compression | medium | medium — compounds with scoping |
| 4 | Model tiering | medium | high — large gap between tiers |
| 5 | Caching discipline | low (if structural) | high on stable workloads |
| 6 | Tool discipline | low | medium — also a quality win |
| 7 | Workflow choice | continuous | high per decision |

**The first two families are nearly free to adopt and pay back immediately**. **The next two require measurement work but unlock the largest portfolio savings**. **The last three are polish** — important, **but they only matter once the foundation is in place**. Past the seven families, **you hit diminishing returns quickly**.

---

## What not to start with

**A surprising amount of online advice** says to **start by fiddling with the reasoning-effort dial, sampling parameters like temperature or top-p, or token-level decoding tricks**. **Resist**. Compared to the 7 families above, **those levers have small effect, and are easy to over-tune in ways that hurt quality more than they save cost**.

**A useful heuristic**: **if a proposed optimization requires you to learn a new dial before you've audited your system prompt, your tool catalog, and your model choice, it's the wrong starting point**. **The big wins live in structure, not parameters**. **Reach for dials only after the structural work is done and measurement shows you where the remaining cost actually lives**.

> [!WARNING]
> **Premature parameter tuning is one of the most common ways teams convince themselves they "optimized" while leaving the real savings on the table**. **Audit structure first**.

---

## A short closing reflection

The point of this guide was never to make you a token-optimization expert. **It was to make you fluent in the unit**. **That fluency is the prerequisite for every technique above and every technique not yet invented**. Without it, optimization advice is **folklore** — a list of tricks someone heard worked once. With it, **every piece of advice you read lands with the right amount of skepticism and the right amount of enthusiasm**. You can ask: **which move is this, what's its maintenance cost, what does it assume about my workload, do my own measurements confirm it?**

**Optimization, like accounting, is mostly about being able to read the books**. **The arithmetic isn't hard**. **The discipline is keeping the books, reading them honestly, and acting on what they say**. **You can now do that**.

---

## Going deeper: the quarterly token audit

**Optimization is not a one-time project**. **Treat it like security review or dependency upgrades — an organizational practice on a recurring cadence**.

**Several forces conspire to undo early wins**. **Model prices shift**, sometimes downward in ways that **change which tier is right for which task**. **New caching mechanisms appear**, rewarding (or punishing) prompt structures that were neutral last year. **Instructions files drift toward bloat as well-meaning contributors add "one more rule"**. **Tool catalogs grow as people connect a server and forget to disconnect**. **Workflows quietly shift from ask-mode to agent-mode**, one team at a time, until the bill notices.

**The practical countermeasure = a quarterly token audit**:

```
   ┌──────────────────────────────────────────────────┐
   │   QUARTERLY TOKEN AUDIT                          │
   ├──────────────────────────────────────────────────┤
   │ 1. Pull last quarter's usage metrics              │
   │ 2. Identify top 3 cost drivers                    │
   │ 3. Re-read the system prompt out loud             │
   │ 4. Tool list — remove anything unused for 90 days │
   │ 5. Re-check model tier vs task difficulty         │
   │ 6. Verify cache-friendly prefix structure         │
   │ 7. Note one experiment to run next quarter        │
   └──────────────────────────────────────────────────┘
```

**The audit doesn't have to be heavy**. **An hour per project per quarter is enough to catch regressions before they become budget items**. **The goal isn't to reach a perfect state** (there isn't one) — **the goal is to keep the system from drifting too far from the discipline you established**.

**Build this habit and the 7 families stop being a checklist and become how you work**.

---

## FAQ

**Q1.** "Should I do all 7 families at once?"  
A. **No**. Adopt in order, **measure** the effect of each before moving to the next. All at once = you can't tell which worked.

**Q2.** "Is optimization a publication-time thing, irrelevant to future models?"  
A. **The 3 moves are invariant**. New models, prices, mechanisms come and go, but **the framework survives**. Only surface tricks change.

**Q3.** "Reasoning effort and temperature aren't worth touching at all?"  
A. **Fine after the structural work is done**. **Order matters**. Dials first is the typical mistake.

**Q4.** "Isn't a quarterly audit overkill for a small team?"  
A. **Even 30 minutes is valuable**. Cadence > rigor. The point is "don't ever forget".

**Q5.** "What concrete technique should I learn next?"  
A. **Start with output control** — least effort, highest immediate impact. Add one rule and measure for a week.

---

## Recap

- **Every optimization is one of three moves**: send fewer, receive fewer, pay less per token. **Name the move before evaluating the technique**
- **7 families of techniques** cover nearly everything worth learning: output control, context scoping, prompt compression, model tiering, caching discipline, tool discipline, workflow choice
- **Adopt in roughly that order**. The first two are nearly free. The next two unlock the largest savings. The last three are polish and compounding
- **Don't start with reasoning-effort dials or sampling parameters**. Structural fixes dwarf parameter fixes
- **Optimization is a recurring practice, not a one-time project**. Without an audit cadence, costs drift back
- **Fluency in the unit (tokens)** is what makes every future optimization technique legible to you. **That fluency was the goal of the guide**

---

## Exercises

**Exercise 16.1** (5 min)  
Recall one piece of optimization advice you read recently and identify **which of the 3 moves** it is. Write down its **maintenance cost and workload assumptions**.

**Exercise 16.2** (30 min)  
Run **a token audit using Chapter 13's metrics** on one project. Identify the **top 3 cost drivers** and **pick the lowest-effort family to apply**.

**Exercise 16.3** (challenge)  
Propose a **quarterly token audit process** for your team: who runs it, what checklist, where reported, what success metrics.

---

## On to the next chapter

Here, "next" is not reading but **execution**: **three concrete actions**:

1. **Run a token audit on one project this week**. Use the metrics and methods from Chapter 13. **Pick a single project, not the whole portfolio**, and figure out where its tokens actually go. **The result will probably surprise you, and the surprise is the point**: it tells you which family to start with

2. **Pick the lowest-effort family from this chapter and apply it**. For most readers, that = **output control**: add one rule to your system prompt, deploy today, measure next week. **Resist the urge to do all 7 at once**. **One change measured beats seven changes unmeasured**

3. **Return to Chapters 9–14 when you suspect a regression**. Those chapters — where tokens are spent, hidden consumers, the quality-cost curve, hygiene principles, measurement, anti-patterns — are **the working chapters of this guide**. **Re-read them when something feels off**. **Bookmark them**

You started this guide knowing tokens as "**the unit LLMs bill in**". You finish knowing tokens as **the unit LLMs think in, spend time in, forget in, and succeed or fail in**. **That shift in perspective is the whole point**. **Everything else** — the 7 families, the 3 moves, the quarterly audit — **is how you use it**.

**Good luck. Spend wisely.**

→ [Appendix A — Glossary](18-glossary)
