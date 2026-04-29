---
title: "Chapter 12 — Token-hygiene principles"
---

> **In one line:** Token hygiene is **a small set of habits that quietly keep the bill healthy** — about layout, scope, phrasing, output, context, model selection, sessions, tools, and measurement — applied **before reaching for any specific optimization technique**.

---

## Why this chapter exists

The previous chapters mapped the territory: what tokens are, how to count them, what gets expensive, where they're spent, what happens when there are too many, the quality-vs-cost tradeoff. **Before starting serious optimization, there's a layer beneath optimization that matters more than any single trick** — that's **hygiene**.

Hygiene is **a small, almost-boring set of habits** that, applied consistently, prevent token use from drifting into a problem. **Nothing clever**. **No new tools or frameworks required**. Most are **decisions you make once and stop thinking about**. But they **compound** — projects that respect them tend not to need heroic optimization later, because **they never wasted in the first place**.

This chapter walks through **10 principles**. Each is **a principle, not a recipe**. The recipe families — caching, retrieval, summarization, batching, distillation — are previewed in Chapter 16. Here we give you **the foundation habits the recipes sit on**.

**Adopting even 2–3 of them produces a noticeable difference**. **Adopting all 10 crosses the line** from "hobby project" to "system that scales without surprise".

---

## 1. Stable prefix, volatile suffix

Modern inference stacks **reuse computation when the prefix of two requests is identical**. The internal representation of the shared prefix is cached, and the next request that starts with the same bytes doesn't have to recompute it. **The cached portion is usually billed at a fraction of normal input price**.

This caching is **positional and strict**. It works **forward from the start of the prompt** and **stops at the first byte that differs**. **A single character change at the top of the prompt invalidates everything after it**.

The hygiene rule that falls out is simple: **what doesn't change goes at the top; what does change goes at the bottom**.

```
[ system prompt        ]   ← stable, set once per project
[ project rules        ]   ← stable, edited rarely
[ tool definitions     ]   ← stable, change with releases
[ retrieved context    ]   ← varies per query
[ conversation history ]   ← grows over time
[ current user message ]   ← always different
```

**The wrong layout** — putting timestamps, session IDs, "today's date is…" **at the top** — **invalidates the cache on every request**. **The right layout** treats the prompt as a **layered cake**: the bottom layers are baked once and reused; the top is fresh.

You don't need to think about the caching mechanism in detail. **Just keep the volatile parts at the bottom**.

---

## 2. Scope load on demand, not always-on

**Anything loaded automatically is billed every turn, forever**. **The single most common source of unnoticed token spend**.

The pattern shows up everywhere: a global instructions file appended to every prompt, a preamble describing the project on every request, a tool catalog including every tool the assistant **might** need, a memory store injecting user preferences regardless of relevance. **Each of these is billed every turn — not just on the specific turns where it matters**.

Hygiene rule: **default to load when relevant, not load always**. For each text block attached to a prompt, **one question**:

> **Does the model need this every turn, or only when working on a specific file / task / topic?**

If the answer is "only when working on X", **it does not belong on the global path**. **Conditionally load it** — when the file is touched, when the topic comes up, when a tool is actually likely to fire. Most platforms support **scoped or conditional instruction loading**; **use it**.

The arithmetic is unforgiving. **A 1,000-token always-on instruction file** = 1,000 × every turn × every session × every user. **The same 1,000-token file scoped to one filepath** = 1,000 once or twice a week. **Same content. Different bill**.

---

## 3. Declarative over imperative phrasing

**Two prompts can express the same intent in wildly different token counts**.

```
Imperative (verbose):
"If you have an opportunity to return data, please format it
as JSON, and don't forget to use proper JSON syntax, and
make sure not to include comments in JSON, and ensure all
strings are properly quoted, and..."

Declarative (concise):
"Always respond with valid JSON. No comments."
```

The declarative version is **shorter, clearer, and in practice more reliable**. **Long, hedged, qualified instructions are not just more expensive — they're harder for the model to follow**. Every "please", "remember to", and "make sure that" **costs both tokens and instruction-following clarity**.

Hygiene rule: **write the way a style guide is written, not the way a nervous email is written**. State the constraint **once, in the imperative present tense**, and trust the model to follow. If it doesn't, the fix is rarely "more words". **It's usually a sharper, shorter rule, or moving the rule closer to the part that matters**.

This habit alone tends to **halve system prompts on a first pass**.

---

## 4. Output discipline

**The output side of the bill is usually the more expensive side per token**. Generated tokens cost a multiple of input tokens, and unlike input — which is capped by the context window — **output is bounded only by what the model decides to generate**.

That makes one-line instructions like "**Code only, no explanation**" or "**Reply in three sentences or fewer**" **one of the highest-ROI additions you can make to a prompt**. **Pay a few tokens once, save hundreds per response**.

```
Without output discipline:
  request:  ~500 tokens
  response: ~1,800 tokens   ← model explains, summarizes, hedges, recaps

With output discipline:
  request:  ~510 tokens     ← +10 for the constraint
  response: ~250 tokens     ← model answers and stops
```

**The reverse is also true**: **don't ask for "thorough, complete, exhaustive" answers unless you actually want them**. Words like "complete", "comprehensive", "detailed" are **output amplifiers**. Appropriate when you genuinely need a long-form deliverable. **Wasteful when you just wanted the answer**.

> [!TIP]
> Useful default for chat-style assistants: "**Be concise. Use short paragraphs. Skip recaps.**" Three short clauses, big effect on average response length.

Output discipline also **improves UX**. **Fast, tight responses are almost always preferred over long ones** — and they **ship faster because there's less to generate**.

---

## 5. Minimum sufficient context

Chapter 11 made the case from a quality angle: **more context is not always better, and past a point actively harms**. The hygiene angle is the same point seen from cost. **Every turn, you're paying for whatever you put in front of the model**.

Hygiene rule: **give the model what it needs to answer well**. **Not what's available**. Not what's "**potentially useful**". Not "**interesting background**". **Minimum sufficient context**.

In practice, before each retrieval/include, ask:

- Is this relevant to *this query*, or just to the topic?
- Do I need this **whole document**, or just **one section**?
- Is this conversation history still load-bearing, or has the content been superseded?
- Does **a one-line summary do the same job as the full text**?

**The answer is often "less worked"**. The "throw everything in just in case" pattern is **comfortable but expensive** — and as Chapter 11 showed, **the quality curve peaks earlier than intuition suggests**.

This principle **composes with principle 1 (stable prefix)**. **Minimum sufficient context tends to mean volatile context** (per-query retrieved chunks) — pruning it is **doubly good**: smaller bill, and the cached prefix carries more of the load.

---

## 6. Right-size the model

Models come in **tiers**. The **cost difference between cheapest and strongest tiers is usually about an order of magnitude per token** — sometimes more. Capability differences are real but **don't apply uniformly to every task**.

**A small model is usually fine for**:

- Classification / labeling
- Reformatting structured data
- Summarizing well-formed text
- Routing requests to the appropriate downstream handler
- Drafting before a more capable model edits

**A frontier model earns its cost when**:

- Multi-step reasoning across lots of context
- The output is high-stakes (security, accuracy, user-facing voice)
- The task has been observed to fail at smaller tiers

Hygiene rule: **pick the smallest model that produces acceptable quality for the task, and re-evaluate when the lineup changes**. **Defaulting every call to the strongest model is the single most expensive habit in production systems** — and **it's almost always unnecessary for the majority of traffic**.

A common, healthy pattern: **two-tier setup**. A cheap default handles the bulk, the strong model is invoked only when the task is flagged "hard" or when the cheap model's output fails a check.

---

## 7. Right-size the reasoning effort

Many current models expose a reasoning-effort knob — sometimes explicit (a parameter), sometimes implicit (a "thinking" mode). **Turning the knob up means the model generates hidden reasoning tokens before answering. Those hidden tokens are billed**.

When the knob is at max, **reasoning tokens often dominate the output bill** — sometimes by an order of magnitude over the visible response. The cost pattern was described in Chapter 10.

Hygiene rule: **default to medium (or its equivalent)**. **Turn it up only on tasks that genuinely need it** — proofs, multi-file debugging, multi-step change planning. **Turn it down for routine work** — format conversions, single-file edits, short answers, classification.

```
high reasoning, simple task
  ┌────────────┬──────────────────────────────┬─────┐
  │  prompt    │  hidden reasoning tokens     │ ans │
  └────────────┴──────────────────────────────┴─────┘

medium reasoning, simple task
  ┌────────────┬──────────┬─────┐
  │  prompt    │ thinking │ ans │
  └────────────┴──────────┴─────┘
```

**Both produced the same answer. Only one of them paid for it.**

---

## 8. End sessions on topic change

Long conversations accumulate history. **Every turn, the previous turns' messages are added to the prefix sent on the next request**. Caching makes that cheaper, but not free, and **even with billing suppressed, the conversation keeps growing in a window-term sense**.

Hygiene rule: **start a new session when the topic changes**. The cost of "**a fresh start**" (re-establishing system prompt, project rules, current focus) is **almost always less than dragging the irrelevant prior topic along for the rest of the day**.

Especially true in assistant-style use. A conversation that started "help me name this feature" and is now "debug this stack trace" is **paying for the long, irrelevant prefix on every debug turn**. The stack trace doesn't benefit from the naming discussion. **Starting a new session drops that ballast**.

**Sessions are cheap. Topics aren't.**

> [!NOTE]
> "**End on topic change**" is **not** "**end after every message**". When the model is genuinely building useful state across turns — a debugging trail, an evolving design, a long edit — sessions are valuable. **End them when that state stops being load-bearing**.

---

## 9. Treat tools as inventory

**Each tool you expose to the model** (name, description, parameter schema, usage notes) **is included in the prompt every turn the tool is available**. A 50-tool catalog makes you **pay 50 tools' worth of tokens, regardless of whether the model uses any of them**.

Chapter 10 covered the mechanism. Hygiene rule: **treat the tool catalog as inventory**. Audit it periodically. For each tool, ask:

- Is this tool **actually being called**? (logs will tell you)
- Could two similar tools be **merged into one with richer parameters**?
- Could **rarely-used tools** move to **a separate scoped catalog** loaded only when relevant?
- Is the description **doing real work**, or is it **boilerplate that could be cut in half**?

A tool in the catalog that **isn't called pays rent for zero value**. **A 200-token description that does the same job as a 60-token one is overpaying**. **Catalogs that accumulate tools over time without pruning are almost always larger than they need to be**.

**Because the savings apply to every turn, this is one of the highest-leverage audits available**.

---

## 10. Measure before optimizing

**You can't improve what you can't see**. Every other principle in this chapter is easier to apply and verify when you have **basic visibility into where tokens actually go**.

Hygiene rule: **log per-call usage and break it down**. At minimum:

- input tokens (uncached)
- input tokens (cached, if the provider exposes it)
- output tokens
- reasoning tokens (if the model exposes them separately)
- model used
- session/request identifier

**A small amount of plumbing**. **The payoff is large**. **Often within the first week**, you discover that the bill is concentrated in **a handful of patterns**: a chatty system prompt, an always-on tool catalog, a runaway conversation, a single endpoint defaulting to the strongest model. **Invisible without measurement, all quick fixes once visible**.

Chapter 13 dives into this. For hygiene purposes, the principle is: **instrument first, optimize second**. **Optimization without measurement is guessing** — and **what you guess about is rarely what's actually costing you**.

---

## These principles compound

Each principle, read alone, is **modest**. A shorter system prompt. A scoped instructions file. A "no preamble" rule. A small model on the easy path. A new session when the topic changes.

**Applied together, they multiply**. A prompt that is **half as long, prefix-cached, on a smaller model, output-bounded, and in a fresh session** isn't 5× cheaper than the alternative — **it's often 20× to 50× cheaper for the same task**. **And quality is usually higher**, because each move also reduces noise the model has to sort through.

You don't need to adopt all 10 at once. **Two or three materially shift the economics**. **Adopting all 10 is the difference between a project that works at small scale and one that scales sustainably without operational surprise**.

```
        cost per task
          ▲
          │   ●  no hygiene
          │
          │      ●  + output discipline
          │
          │         ●  + scoped loading
          │
          │            ●  + right-sized model
          │
          │               ●  + cache-friendly layout
          │                  ●  + tool audit
          │                     ●  ...
          └──────────────────────────────────► principles applied
```

Each habit lowers the floor a bit. **The compound effect lowers it a lot**.

---

## Going deeper

Think of these principles as **design constraints, not last-mile fixes**.

**The biggest savings in token economics come from system-level decisions made early and revisited rarely**:

- Which tools are exposed by default
- Which instructions are global vs scoped
- Which model is the default per request type
- How sessions are bounded
- Where volatile content lives in the prompt
- What the default reasoning effort is
- What the default output cap is

**These are architectural choices**. Cheap to make at project start, **expensive to undo after the system is in production with thousands of users hitting it daily**.

In contrast, **late-stage prompt micro-tuning** — trimming a sentence here, tightening a tool description there — has **diminishing returns**. Real work, but **ceiling work, not floor work**. **A project that did the architectural work has very little prompt micro-tuning left**; **a project that skipped it can't get back via micro-tuning**.

The recipe families in Chapter 16 — caching, retrieval, summarization, batching, distillation — **all sit on top of these principles**. **Applying a clever caching strategy to a prompt with a volatile timestamp at the top doesn't help**. **Applying retrieval to a prompt that already global-loads everything doesn't help**. **Principles first, recipes amplify**.

> [!IMPORTANT]
> If you remember one thing from this chapter: **most token waste is decided before any optimization is attempted**. Default loads, default model, default tool catalog, default output length — **those defaults set the floor**. **Optimization works against the floor, not below it**.

---

## FAQ

**Q1.** "If my model doesn't have effective caching, is principle 1 irrelevant?"  
A. Caching is the largest effect, but layered prompts are also good design for **lost-in-the-middle mitigation** (important info at start/end) and **maintainability**.

**Q2.** "Doesn't going declarative sometimes hurt instruction-following accuracy?"  
A. Rarely. When it does, that's a sign **the rule is ambiguous or contradictory**. Fix it with **a sharper formulation, not more words**.

**Q3.** "What if my output cap cuts off the answer?"  
A. **Cap at task length + α**. Post-process (continuation request) only when truncation occurs. Defaulting to unlimited is the opposite-direction sin.

**Q4.** "I can't predict where small models will fail."  
A. **Build an eval set and measure**. Once you see failure patterns, you can build **routing rules** (hard flag, confidence threshold).

**Q5.** "Splitting sessions loses past context."  
A. If that context is **load-bearing for the new topic, pass a short summary**. You'll often find **the context wasn't actually needed**.

---

## Recap

- **Stable prefix, volatile suffix**: invariant content at the top, per-request content at the bottom
- **Scope load on demand**: always-on content is billed every turn forever; default to conditional loading
- **Declarative over imperative**: short direct rules are cheaper, clearer, and better followed
- **Output discipline**: output is the expensive side; one-line constraints on length/format have large ROI
- **Minimum sufficient context**: what's needed to answer well, not what's available
- **Right-size the model**: default to small; reserve the strongest tier for tasks that genuinely benefit
- **Right-size the reasoning effort**: default medium; turn up only on hard problems
- **End sessions on topic change**: long sessions accumulate ballast; new sessions drop it
- **Treat tools as inventory**: every tool in the catalog is billed every turn; audit and prune
- **Measure before optimizing**: per-call usage logs reveal where the bill actually lives — usually not where you'd guess
- These habits **compound**: 2–3 noticeably shift the bill, all 10 shift project viability
- Treat them as **design constraints, not last-mile fixes**. The biggest savings come from early system-level decisions

---

## Exercises

**Exercise 12.1** (10 min)  
Sketch your app's prompt layout and **identify where volatile elements have crept in**. Estimate **how the cache hit rate would change** if you reordered.

**Exercise 12.2** (15 min)  
Rewrite your system prompt as **a declarative ruleset** and measure the token count delta. Does output quality on the same tasks hold?

**Exercise 12.3** (challenge)  
Audit your tool catalog. Identify **tools not called in the last 30 days**, **tools with boilerplate descriptions**, and **merge candidate pairs**.

---

## On to the next chapter

Hygiene only becomes a **habit** when you can **see** it working. The next chapter turns these principles **from advice into something verifiable in numbers** — instrumenting per-call usage, building a basic dashboard, and how to read it.

→ [Chapter 13 — Measuring tokens](14-measuring)
