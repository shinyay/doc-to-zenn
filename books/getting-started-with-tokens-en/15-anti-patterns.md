---
title: "Chapter 14 — Anti-patterns and pitfalls"
---

> **In one line:** Most token waste in real systems isn't exotic — it's **a small set of recurring anti-patterns** that quietly compound, and **a checklist will find them**.

---

## Why this chapter exists

By now you have a model of where tokens come from, what they cost, how they affect quality, and how to measure them. **This chapter is the diagnostic counterpart**. It names **specific failure modes** that show up in real deployments again and again, what they look like from outside, why they're expensive, and **what the healthy version of the same thing looks like**.

It reads end-to-end but is also designed to be **skimmable**. Each anti-pattern follows the same **4-part structure**:

- **Symptom** — what you observe in logs, dashboards, behavior
- **Why it hurts** — the cost, quality, latency mechanism
- **How to find it** — concrete checks you can run
- **What the healthy version looks like** — the version that doesn't waste tokens

If you find more than 2–3 in your own setup, **that's normal**. **The point isn't to shame any specific system**, it's to **give you the vocabulary to name what's happening, and help you prioritize the fix**.

```
        anti-pattern              shape of the cost
        ─────────────────         ──────────────────────
        kitchen-sink prompt   →   flat tax on every turn
        history bloat         →   grows with turn count
        tool overload         →   flat tax + per step
        retrieval over-pull   →   per-query spike
        reasoning leakage     →   per-call multiplier
```

---

## 1. Kitchen-sink system prompt

**Symptom**: a system prompt that has **grown to several thousand tokens** through months of "let's add a rule about this too". It includes a mission statement, a tone guide, an output format, a list of forbidden phrases, **instructions for tools removed last quarter**, and **three contradictory rules** about when to ask clarifying questions.

**Why it hurts**: the system prompt is **billed every turn**. **A bloated system prompt is a fixed tax on every interaction (including the trivial ones)**. Worse, **contradictory rules force the model to spend attention resolving the contradictions instead of answering the question** — cost goes up while **quality goes down**.

**How to find it**: count the tokens in your system prompt. **If it's more than a few hundred, read it end-to-end out loud**. If you find rules you can't justify, rules that contradict each other, or rules for capabilities that no longer exist, you have a kitchen-sink prompt. **Another signal**: nobody on the team can confidently recite what's in it.

**What the healthy version looks like**: **an edited prompt** (not just appended to). Rules are grouped, deduplicated, and pruned regularly. **Capability-specific instructions live with the capability**, not in the global preamble. **Someone owns the prompt and reviews diffs to it like code**.

> [!TIP]
> Useful exercise: **delete the system prompt entirely** and run a small eval. **Add back only the rules whose removal demonstrably hurt quality**. Many won't make the cut.

---

## 2. The auto-generated context-file bloat

**Symptom**: a long machine-generated context file in the repo — exhaustively but unfocusedly documenting the project. An "init" command wrote it. **It's loaded into the agent's context on every session**, and the agent's behavior is somehow **slightly worse than before**.

**Why it hurts**: **long context is not free attention**. Stuff thousands of tokens of low-signal description in and the model **uses some of its capacity processing material that doesn't help with the current task**. The classic "more context, worse answer" effect. **You also pay for the same uninformative tokens every turn**.

**How to find it**: open the file. For each section, ask "**would a new human teammate need to read this?**" If no, **the model doesn't need it either**. **Another check**: on a small fixed test set, **compare quality with and without the file**. If "without" is no worse, the file is pure cost.

**What the healthy version looks like**: **a short, hand-curated context file** containing what a competent newcomer would actually need (project purpose, key conventions, important entry points, known footguns). **Generated content is a starting point but is heavily edited**, not committed verbatim.

---

## 3. MCP / tool overload

**Symptom**: the agent is configured with **a long list of integrations** — every connector, every internal API, every DB. In any given session, **most are not used**, but **their schemas are advertised to the model on every step**.

**Why it hurts**: tool schemas = tokens. Each integration typically contributes the name, description, and parameter schema of every exposed function, and **a single integration can easily be several thousand tokens**. With a dozen integrations enabled, **the per-step overhead can dominate everything else**. Beyond cost, a long tool list also **lowers selection accuracy**: the model is **more likely to pick the wrong tool when choosing from 50 than from 5**.

**How to find it**: on a typical agent step, measure **how many input tokens are consumed before any user content**. If the tool definitions are more than a small fraction of total input, you're **over-provisioned**. **Track tool-use frequency** and consider any tool that fires in less than a few percent of sessions a candidate for removal or lazy loading.

**What the healthy version looks like**: tools are **scoped to the task at hand**. The agent has a small default set, and additional tools are loaded only when the conversation indicates they're needed. **Schemas are written terse** — short descriptions, minimal parameter docs — because the model reads them every step.

```
    bad:                          good:
    ┌──────────────────┐          ┌──────────────────┐
    │ 30 tools always  │          │ 5 default        │
    │ loaded           │          │ + lazy loaded    │
    │ ~6000 tokens     │          │ ~800 tokens      │
    │ per step         │          │ per step         │
    └──────────────────┘          └──────────────────┘
```

---

## 4. Reasoning leakage

**Symptom**: every response (including "what's 2 + 2?") is preceded by **several paragraphs of "let's think step by step"** before the actual answer. Or, **the reasoning-effort dial is permanently at the highest setting** because someone read it "increases quality".

**Why it hurts**: reasoning tokens are billed. On models that emit internal reasoning traces, **even when the user doesn't see them, they count against the output budget**. On trivial questions, **reasoning can be 10–20× the size of the actual answer**. **Across millions of calls, a large bill for zero benefit**.

**How to find it**: sample a few hundred recent responses and look at **the ratio of reasoning tokens (or visible thinking preambles) to final answer tokens**. On easy questions, this ratio should be small. **If easy and hard look the same, reasoning is leaking**.

**What the healthy version looks like**: **reasoning effort is matched to task difficulty**. Easy questions get short answers without preambles; hard questions get full reasoning. **If the system supports it, route by predicted difficulty**; if not, instruct the model to "**skip preamble unless the problem requires it**".

---

## 5. Pathological history growth

**Symptom**: a long session that started fast and **gets slower every turn**. By turn 50, new messages are noticeably longer and more expensive even though the user's question is the same size. Eventually **quality collapses** — the model forgets the start of the conversation, contradicts itself, or refuses to engage with the latest message.

**Why it hurts**: **conversation history is replayed every turn**. The assistant emits a verbose reply → it joins the next turn's input. 50 verbose replies in a row → all of them are input on turn 51. **Tokens per turn grow monotonically until you hit the context window** — and then it silently truncates or breaks.

**How to find it**: **plot input tokens per turn for long sessions**. Healthy session = a roughly stable line that occasionally bumps when new material is introduced. **Pathological session = a steadily rising line**. The slope tells you "**how much history debt each turn adds**".

**What the healthy version looks like**: **older turns are summarized / dropped / compressed past a threshold**. The assistant's own outputs are kept terse so they don't bloat the history.

---

## 6. Polite filler in outputs

**Symptom**: every response opens with "**Of course, I'd be happy to help! Here's what you asked for:**" and closes with "**Let me know if you have any other questions!**" **The actual answer is sandwiched in the middle**.

**Why it hurts**: output tokens are usually **the most expensive thing** in the system, and **these phrases serve no informational purpose**. On a single response, trivial. **At millions of calls per day**, a meaningful line item. **They also add latency** — every word the model emits = time the user waits.

**How to find it**: sample some responses and measure **how many tokens precede the first sentence that actually answers the user's question**. Consistently more than a handful = filler problem.

**What the healthy version looks like**: **the system prompt explicitly forbids opening pleasantries and closing offers of further help**. The model goes straight to substantive content. In isolation any single example sounds curt, but **as a consistent style it reads as professional and respectful of the reader's time**.

---

## 7. Pasting huge logs and stack traces

**Symptom**: a user pastes **a 10,000-token stack trace** to ask about one specific error. The agent answers. Fifty turns later, **that stack trace is still in the history, replayed on every call**.

**Why it hurts**: **a one-time spike in input becomes a recurring tax**. The user paid for it once when it was relevant, and **continues paying for it every turn afterward, even though the current discussion is unrelated**. **One of the most common causes of unexpectedly expensive sessions**.

**How to find it**: look for sessions where one early turn is dramatically larger than the rest, and input-per-turn stays high afterward. **Signature = a step function in per-turn token count that doesn't come back down**.

**What the healthy version looks like**: **large pasted artifacts are summarized after the turn that used them**. The summary keeps the relevant insight ("the error is a null reference at foo.py:42") and discards the raw text. **Agent runtimes can automate this on size thresholds**; users can do it manually by editing/pruning history.

> [!NOTE]
> **The single pattern most worth fixing first in interactive coding tools**. The combination of "users paste large outputs" and "sessions run long" makes cost grow especially quickly.

---

## 8. Tool-call ping-pong loops

**Symptom**: the agent calls tool A → looks at the result → calls B → looks at the result → **calls A again with the same parameters** → same result → calls B again... The user sees a spinner; the dashboard sees a stream of API calls; **nothing is making progress**.

**Why it hurts**: each loop step pays **the full input cost including the growing history of previous tool calls and results**. A 10-step loop before someone notices ends up costing **far more than a normal direct-answer turn** — because each later step replays a longer history than the step before. **And when the loop finally terminates (usually a step limit), the user often doesn't get a useful answer for that money**, which is what makes it especially painful.

**How to find it**: track tool-call count per user message. Alert on sessions exceeding a sane ceiling. **Repeated identical tool calls with identical parameters in a single session = the smoking gun for a loop**.

**What the healthy version looks like**: **the runtime detects repeat calls with identical parameters** and either short-circuits with the cached result or breaks the loop. **The agent is encouraged to recognize when it's not progressing and ask the user for help instead of grinding**. **A hard cap on tool calls per turn** protects the worst case.

---

## 9. Over-pulling RAG

**Symptom**: a RAG system that pulls 30 chunks per query "**to be safe**". The chunks are stuffed into the prompt. **The model has to find the needle in a haystack of its own making, and often misses** — producing worse answers than it would have with 5 well-chosen chunks.

**Why it hurts**: cost is direct — you pay for every chunk you include on every query. **The quality cost is subtler**: the model's attention is finite, and **making it range over 30 mostly-irrelevant chunks dilutes its focus on the actually-important few**. **More expensive AND less accurate**.

**How to find it**: run **an evaluation with varying retrieval chunk counts**. If accuracy plateaus / degrades past a small number, you're **over-retrieving**. Also look at **the rank distribution of "the chunk that actually answered the question"** — if it's almost always in the top few, **you're paying for the rest for nothing**.

**What the healthy version looks like**: retrieval returns **a small number of high-quality chunks** with **re-ranking that promotes the most relevant**. **Recall is tuned against a labelled eval set**, not maximized blindly. The long tail of "just in case" chunks lives in **a second tier that's only consulted when the primary tier is insufficient**.

---

## 10. Wrong-tier model defaults

**Symptom (over-sized)**: every interaction goes to **the most capable, most expensive model** — including "what's today's date?" and "summarize this paragraph in one line". **The dashboard shows flat high cost-per-call regardless of difficulty**.

**Symptom (under-sized)**: every interaction goes to a small cheap model, but **retry rates are high, users are frustrated and re-ask, and there's a frequent escalation path to a larger model** — the small model **isn't actually saving money**.

**Why it hurts**: **both extremes lose**. Over-sized = paying a large multiplier for capability the task doesn't need. Under-sized = small per-call multiplier, but **retries and escalations multiply call count**, often making it **more expensive overall**, **slower, and more annoying**.

**How to find it**: plot cost-per-successful-task (not cost-per-call). **If your big-model setup isn't meaningfully better in success rate than a smaller alternative, you're overpaying**. **If your small-model setup has a high retry/escalation rate, you're underpaying**.

**What the healthy version looks like**: **a routing layer that sends easy tasks to small models and hard ones to larger models**, with an **explicit policy for what counts as "hard"**. **The policy is reviewed against measured outcomes, not assumptions**.

---

## 11. Markdown-table abuse

**Symptom**: responses contain **wide markdown tables with dozens of columns and many rows**. Downstream systems parse them via pipe splits. **Sometimes a value contains a pipe character and parsing breaks**.

**Why it hurts**: markdown tables are **dense in punctuation tokens** (pipes, dashes, alignment markers, escapes) — none of which contribute to the data. **A table that would be a few hundred tokens in JSON or CSV easily doubles in markdown**. **You also pay extra to form and maintain alignment, and inherit the brittle parsing problem**.

**How to find it**: if structured output is being received as a markdown table that's then parsed, this anti-pattern. **Render the same data as a table, JSON, and CSV side by side** — the table is almost always the largest.

**What the healthy version looks like**: structured outputs are requested in **structured formats**. JSON for nested or typed data, CSV for tabular, **markdown tables only for human consumption in chat clients**.

---

## 12. Forgotten debug output

**Symptom**: the system prompt says "**always print all intermediate variables**" or "**include full reasoning at the end of every response**". **Added during development for debugging, never removed**. In production, **the model dutifully complies on every call**.

**Why it hurts**: output tokens scale linearly with how much you make the model produce. **Asking for full intermediate state on every call multiplies typical output size by a large factor with zero value to end users**. The debug output is usually discarded, parsed away, or hidden in the UI — **you're paying for content nobody reads**.

**How to find it**: read the production system prompt for words like "explain", "show your work", "include all", "print every". Look at **the actually-displayed portion** of the output payload.

**What the healthy version looks like**: debug instructions are **scoped to the debug environment or feature flag**. The production prompt asks for **only what users need to see**.

---

## 13. Cache-busting prefixes

**Symptom**: the system prompt starts with a line like "**Session ID: 7f3c-...**" or "**Request timestamp: ...**". **The cache hit rate on the prefix is near zero** even though **the rest of the prompt is identical across millions of calls**.

**Why it hurts**: prefix caching gives **substantial cost and latency reductions** on cached input tokens, and is **keyed on strict prefix**. **A unique value at the very top of the prompt makes every call look different to the cache, even if the next 4000 tokens are identical**. **The savings are forfeited completely**.

**How to find it**: check the cache hit rate of your system prompt. If it's far below what prompt stability would suggest, **look at the first few tokens of every call**. If they vary, you have a cache-busting prefix.

**What the healthy version looks like**: volatile metadata (IDs, timestamps, per-request flags) lives **at the bottom of the prompt, after the stable content**. **The cache absorbs the long stable prefix**, and **only the short volatile suffix pays full price**. **One of the highest-leverage fixes in this whole chapter**: the change is mechanical, **the savings are immediate**.

```
    cache-busting:                            cache-friendly:
    ┌──────────────────────────────┐          ┌──────────────────────────────┐
    │ [unique session id]          │          │ [stable system prompt]       │
    │ [stable system prompt]       │   →      │ [stable tool definitions]    │
    │ [stable tool definitions]    │          │ [unique session id]          │
    │ [user message]               │          │ [user message]               │
    └──────────────────────────────┘          └──────────────────────────────┘
        cache hit rate: ~0%                       cache hit rate: high
```

---

## 14. Re-summarizing every turn

**Symptom**: the agent framework runs **a "summarize the conversation so far" step before every user turn**. The summaries are reasonable. **The cost is not** — you're paying to **re-do the same summarization work over and over on largely the same content**.

**Why it hurts**: the summary is itself a model call, and **the input is proportional to history length**. Doing it every turn = **roughly quadratic work in turn count**. **Most of what gets summarized on turn N+1 was already summarized on turn N**. **You're paying to make the model re-read the same material indefinitely**.

**How to find it**: look at **non-user model calls per user turn**. **A steady "summarize" call every turn regardless of how much new material was added** = **over-summarization**.

**What the healthy version looks like**: summarization runs **on a threshold** — when history exceeds a token count, or when crossing a logical boundary (new task, new file, new sub-conversation). **Between thresholds, the existing summary is reused**. A small loss in summary freshness in exchange for a large reduction in repeated work.

---

## Diagnostic checklist

Scan your own setup:

1. **Per-call cost is high regardless of difficulty** → kitchen-sink prompt (#1), reasoning leakage (#4)
2. **Per-step input tokens climb over time within a session** → pathological history growth (#5), pasted artifacts (#7)
3. **New sessions get noticeably more expensive after adding new integrations** → tool overload (#3)
4. **Most output volume is preamble / boilerplate, not the answer** → polite filler (#6), forgotten debug output (#12)
5. **RAG pulls many chunks but accuracy is no different than from a few** → over-RAG (#9)
6. **Model spend grows much faster than user count** → ping-pong loops (#8), re-summarization (#14)
7. **Cache hit rate on the system prompt is near zero despite a stable prompt** → cache-busting prefix (#13)
8. **Users complain "smart but slow and expensive"** → over-sized model defaults (#10)
9. **Users complain "fast but wrong"** → under-sized defaults (#10), bloated context drowning the signal (#1, #2)
10. **Walls of text nobody reads** → table abuse (#11), debug output (#12)
11. **Project's auto-generated context file is large** → audit it section by section (#2)
12. **Multiple identical tool calls with identical parameters in one session** → in a loop (#8)

---

## Going deeper

### Anti-patterns amplify each other

These don't show up in isolation, and the interactions are typically **larger than a simple sum** — and through specific mechanisms they can stack **multiplicatively**. Consider a system that has **all** of: a 5,000-token kitchen-sink prompt, schemas advertised for 20 integrations, and reasoning effort at maximum. Reasoning runs over a context already swollen by the prompt and tool schemas, so each reasoning step is more expensive. The prompt is in front of every reasoning step, so its bloat **gets paid for repeatedly**. **By the time the call finishes, the same overheads have been paid for through three different paths**.

**Good news: when you fix things, the same amplification runs in your favor**. Halve the prompt and reasoning gets cheaper too, because reasoning input shrinks. Lazy-load tools and both prompt and reasoning overheads drop. Lower reasoning on easy tasks and **its contribution falls out of bulk traffic almost entirely**. **Every fix raises the value of every other fix**.

```
    naïvely additive view:           often "more than the sum":

    cost ≈ base + a + b + c          cost ≈ base × (1+a) × (1+b) × (1+c)
                                         on the paths where the effects
                                         genuinely compound

    1 fix → save a                   1 fix → proportional savings
    all 3 fixes → save a+b+c         all 3 fixes → can save more than the sum
```

That's why **an audit pays better than any single optimization**. If you only have time for one pass, **don't deep-dive a single anti-pattern; sweep across the top 3–4**.

### Most are organizational, not technical

Most of these anti-patterns **are not bugs in the model**. They're **organizational**. The kitchen-sink prompt grew because **nobody owned it**. Tool overload happened because **every team wanted their integration enabled**. Debug output stayed because **nobody removed it**. **The technical fix is usually obvious; the hard problem is putting an owner on the prompt, the tool list, the production prompt — someone responsible for keeping it lean**. Without ownership, **the same anti-pattern grows back within a quarter**.

> [!IMPORTANT]
> **Anti-patterns are easier to prevent than to remove**. Once a system prompt has accumulated 1,000 contradictory rules, **nobody wants to touch it for fear of breaking something**. **Build review habits** and **the measurement infrastructure from Chapter 13** so that prompts and tool lists **never get to that state**.

---

## FAQ

**Q1.** "If it's working, shouldn't I leave it alone?"  
A. Anti-patterns produce **silent costs**. Even when working, **you're losing on the bill and on latency**.

**Q2.** "We don't have resources to fix everything."  
A. **Identify the top 3–4 with the checklist** and **audit them all at once**. The multiplicative effect beats single deep dives.

**Q3.** "The org won't assign a prompt owner."  
A. **Make the cost dashboard public** and **make the cost owner visible**. The data calls the owner out naturally.

**Q4.** "Removing the auto-generated file feels risky."  
A. **A/B test against a small eval set**. Often performance is unchanged. **Conviction is replaced by evidence**.

**Q5.** "Aren't ping-pong loops a function of agent intelligence?"  
A. **Defend against them at the runtime level with hard caps and duplicate detection**. Don't rely on intelligence.

---

## Recap

- **The same small set of anti-patterns** shows up in nearly every real deployment. Once named, they're fixable
- Each anti-pattern has **a recognizable symptom, a concrete check, and a healthy alternative**. You don't have to invent the diagnosis from scratch
- The biggest single wins are **mechanical**: trim the system prompt, lazy-load tools, push volatile content to the bottom, stop repeating expensive work like full re-summarization
- Anti-patterns **compound multiplicatively**. A 3–4-item audit beats a single deep dive
- Most are **organizational problems in technical disguise**. Without owners on prompts, tool lists, and context files, they grow back
- Use the **diagnostic checklist as a periodic review** — one pass per quarter keeps most systems healthy

---

## Exercises

**Exercise 14.1** (15 min)  
**Kitchen-sink check** your system prompt: measure tokens, read it out loud, and identify three contradictory or unnecessary rules.

**Exercise 14.2** (10 min)  
Scan your project against the diagnostic checklist. **List every applicable anti-pattern**, then prioritize fixes by considering **the multiplicative effect**.

**Exercise 14.3** (challenge)  
Check whether you have a **cache-busting prefix**. If yes, **move the volatile element to the bottom** and measure how the cache hit ratio changes.

---

## On to the next chapter

You now have the vocabulary for the most common ways token budget is wasted, and a checklist for scanning your own setup. **The next chapter steps back from tactics and asks the strategic question**: why does this matter at the product, team, and business level? **Token optimization is sometimes treated as a bookkeeping concern — but at scale it becomes strategic and shapes what you can ship**.

→ [Chapter 15 — Why optimization matters](16-why-optimize)
