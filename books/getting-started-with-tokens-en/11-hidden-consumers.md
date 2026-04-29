---
title: "Chapter 10 — Hidden token consumers"
---

> **In one line:** Most of the tokens you pay for **never appear in the prompt** — they're loaded silently before your input, auto-attached to every step, and billed without ever being shown.

---

## Why this chapter exists

Chapter 9 covered the **visible budget**. This chapter is about what's underneath — the **submerged part of the iceberg**. The moment you use real tools (an assistant with project rules, an IDE Copilot with a tool catalog, a looping agent, a RAG system that fetches every turn), what's on screen is just the tip. **The bill is dominated by tokens you didn't type, didn't read, and didn't know existed**.

This chapter names the biggest of them, **in order of real damage**. The goal isn't to scare; it's to **make them visible** so the hygiene and measurement chapters that follow have **concrete things to act on**.

---

## The shape of the iceberg

Mental model: every request has **two layers** — the part **you wrote** and the part **the runtime wrote on your behalf**.

```
What you see                 What the model actually receives
------------                 --------------------------------
                             ┌────────────────────────────────┐
                             │  chat template / role markers  │
                             ├────────────────────────────────┤
                             │  system prompt (platform)      │
                             ├────────────────────────────────┤
                             │  always-on instruction files   │
                             ├────────────────────────────────┤
                             │  tool / function catalog       │
                             ├────────────────────────────────┤
                             │  retrieved context             │
                             ├────────────────────────────────┤
                             │  prior turns (history)         │
                             ├────────────────────────────────┤
"refactor this function" ───►│  your message                  │
                             └────────────────────────────────┘
                                         │
                                         ▼
                             ┌────────────────────────────────┐
"done — here you go."   ◄────│  hidden reasoning + reply      │
                             └────────────────────────────────┘
```

You wrote one line. The runtime sent thousands of tokens. The model may have generated **thousands more** before producing its short answer. **Every layer in that diagram is billed**. **Most of them are invisible**.

Let's walk the five biggest consumers.

---

## 1. Always-on instruction files

Modern coding assistants and chat tools support **project-level rules**: a file in the repo (sometimes named after the tool, sometimes a generic agents file) injected into every conversation about that project. **Personal rules** work the same way.

These are excellent for consistency. **And one of the biggest sources of silent waste** — three properties compound badly:

- **Automatic**: written once and forgotten about. Keeps being sent
- **Per-turn**: not just at the start of a conversation; **rides along on every message**
- **Per-step**: in agent loops, every tool call → result → continuation **resends the rule file**. Five tool calls = five copies on the bill

A modest example: project rules are 1,500 tokens (a page or two of guidelines). A long working session: 100 turns. Each turn has multiple tool steps. Conservatively that file got sent **200–300 times**. **Hundreds of thousands of input tokens for a file written once and forgotten**.

The file isn't **getting more useful with each send**. The model already knew the rules from copy 1. It doesn't get smarter by copy 50.

> [!TIP]
> When writing an always-on instruction file, picture: "this is **billed to my account every turn, forever**." Then ask: **would I pay that for this paragraph?** A lot of "important-feeling" sentences don't survive the question.

---

## 2. Tool / function-calling catalog

When you give the model tool-calling capability (function-calling APIs, MCP servers, IDE integrations), **the tool descriptions actually sent to the model are whatever the client/host app decides to include in the prompt.** MCP, for example, only defines that the client can fetch the server's `tools/list`; **how many of those entries the host concatenates into the model prompt on each turn is a host-side implementation decision** (you can include all of them, or pick the relevant ones). So it's not "enabling MCP automatically adds tens of thousands of tokens to every call" — it's **"if your client/IDE forwards the discovered tool set to the model verbatim, you can end up with tens of thousands of tokens of tool definitions"**.

Each tool definition is typically:

- Name
- Natural-language description of what it does and when to use it
- Structured parameter schema (types, defaults, enums, per-field descriptions)
- Sometimes call examples

A single well-documented tool is often a few hundred tokens. Tools with rich nested parameters: more. **The catalog grows linearly with the number of tools**:

```
   1 tool   ≈   small paragraph
  10 tools  ≈   one page
  50 tools  ≈   one chapter
 150 tools  ≈   a small book — sent every turn
```

Easy to hit the upper end without realizing. A dozen MCP servers, each exposing 8–15 tools, **and a client/IDE that simply forwards all of them into the model prompt**, can mean **tens of thousands of tokens of tool definitions before the user message even arrives**. They are present **whether or not the model uses them, and whether or not the current task could possibly relate to them** — but only because the client chose to forward everything; smarter clients can scope what they send. **The cost here is set by the host app's prompt-construction policy, not by the MCP protocol itself.**

And present in **every step of an agent loop** — because the catalog is part of what conditions the model to emit valid tool calls.

The **discoverability problem** is severe: in most products **the catalog is invisible**. **Integrations enabled months ago** are still loaded.

---

## 3. Retrieved context (RAG bloat)

RAG — fetching relevant snippets from a knowledge source and pasting them into the prompt — is one of the most useful patterns in modern LLM apps. **It's also where tokens leak the easiest**. Cost scales with chunk count and chunk size, and both **drift upward over time**.

```
your question
     │
     ▼
┌─────────────┐    top-K chunks    ┌──────────────────┐
│  retriever  │ ─────────────────► │  prompt builder  │ ──► model
└─────────────┘                    └──────────────────┘
                                        │
                                        │  K chunks × N tokens
                                        ▼
                                    K × N tokens, every turn
```

K = 20, each chunk 500 tokens → retriever adds **10,000 tokens per turn**. Silently builds up over a long conversation. Worse: **retrievers err on the side of recall** — most of the 20 chunks are not actually relevant. **You pay to send them and the model spends attention budget to ignore them** — as we saw in Chapter 8, that's also a **latency and quality** cost.

From the user's perspective the whole thing hides behind "the assistant looked something up". **The actual receipt**: assistant ran 20 searches, pasted results into the prompt, and again on the next turn, and the next.

---

## 4. Hidden reasoning tokens

Many newer models can be configured to produce an **internal chain of reasoning** before the visible answer. The runtime hides that chain from you (only shows the final reply), but **the chain was generated by the model and is typically billed as output tokens**.

Why this hits hard:

- The reasoning chain is **often much longer than the visible reply**. A two-line answer can ride on top of **pages of internal thinking**
- Reasoning effort is often a **dial** (low/medium/high). Cranking it up multiplies hidden output — **an order of magnitude or more** on hard prompts
- Output tokens are the **more expensive kind** (Chapter 7). Hidden reasoning hits the **expensive side of the bill**

Trap: the visible reply **looks short and cheap**. Question → paragraph. **Feels small**. Real generation (what you're paying for) may be **dozens of times larger**.

> [!NOTE]
> Hidden reasoning **is often genuinely worth the cost** on hard problems. We're not saying it's bad. We're saying **its cost is invisible by design** — so **you have to actively decide when it's appropriate**. Defaulting to "high" is the **money version of leaving the lights on**.

---

## 5. Multi-step agent loops

**The largest hidden multiplier is the agent loop itself**.

A request that **feels like one question** ("fix the failing test") expands behind the scenes into many steps: read the test file → read the implementation → search related code → run tests → read failure → edit a file → re-run tests → read new failure → re-edit… **Each step is a full forward pass through the model**. Each pass receives the full context up to that point: system prompt, instruction files, tool catalog, prior tool calls, prior tool results, the original question.

```
turn 1: user asks
        ├── pass 1: context + question                    → tool call A
        ├── pass 2: context + tool result A               → tool call B
        ├── pass 3: context + results A, B                → tool call C
        ├── pass 4: context + results A, B, C             → tool call D
        └── pass 5: context + results A, B, C, D          → final answer
```

**Five passes for "one question"**. **Context gets bigger every pass** — each pass appends the previous tool result. **The fifth pass is the most expensive**. At 15 steps the last few are **very** expensive.

This is the **mechanism behind agent-framework bill surprises**. The UX doesn't say "I'm about to pay for 30 cumulative context round-trips". The product just shows a spinner and a result.

---

## Smaller hidden consumers worth naming

The big five do most of the damage, but at high-volume usage the **small leaks** add up too:

**Chat template tokens**: every chat-style API wraps messages in role markers, delimiters, special tokens. A few tokens per message — but **multiplied across every message of every turn of every conversation**, non-trivial.

**Tool result echo**: when a tool returns, its output is appended to the conversation and **stays in history for the rest of the session**. A tool that returns long JSON, called early in a session, **gets re-billed every subsequent turn until that piece of history is dropped or the conversation ends**.

**Pasted error blobs and stack traces**: a user dumps a 1000-line stack trace to debug. Issue solved 3 turns later. **The stack trace stays in the conversation history for the next 40 turns and rides on every request**.

**Polite filler**: "Of course, I'd be happy to help. Let me take a look at what you've shared…". Trivial in a single call. **Real money across millions of calls in a deployed product**, and on **output tokens (the expensive side)** at that.

---

## The discoverability problem

What makes these consumers dangerous isn't **their size on a single call**. It's that they're **invisible on the bill**.

Most platforms **aggregate**. Monthly totals, maybe a daily/per-API-key breakdown. Nothing tells you "**of the 50K input you sent this turn, 47K was system + project rules + a tool catalog you enabled six months ago, and 3K was the actual question**". **Without the breakdown there's no signal to act on**. The bill goes up; you can't see which knob moved.

Which is exactly why **Chapter 14 (measurement)** exists. **Hygiene without measurement is guessing**. The first job of measurement is to **decompose the iceberg and label its layers**.

A useful exercise meanwhile: for any LLM tool you use today, **stop and ask yourself what gets loaded before your prompt reaches the model**. An invisible platform system prompt? A rule file you wrote months ago? A tool catalog from an integration you forgot you enabled? A vector DB that fetches 20 hits when 5 would do? If you can't answer for tools you use daily, **you don't have control over their cost**.

---

## Going deeper

### Prompt caching as a **partial mitigation**
Many providers offer some form of prompt prefix caching. **A cache hit is not automatic, though — every provider has its own rules** (minimum length to cache, where breakpoints can be placed, cache TTL, billing details). When the start of your prompt (system prompt, instructions, tool catalog) is identical to your next call **byte-for-byte (or token-for-token)** and you satisfy the provider's rules, the runtime can charge those repeat tokens at a **substantially lower rate** — they're already processed. When the conditions line up, this is **genuinely useful**.

**But the iceberg doesn't shrink**. The bill still scales with tokens sent; **only the cached part's unit price drops**. Caching rewards **having a stable, deduplicated prefix**; it doesn't reward **having a small one**. **And cached tokens still count against the context window** — the $ cost drops, but you still pay the **attention and latency cost**.

This creates a key distinction:

- **Context size**: what fits — tokens the model can attend to in one call
- **Billed tokens**: what you pay for — **lower** than context size when caching applies, and **higher** when hidden reasoning output is counted

The two diverge under caching, and **mislead anyone reasoning naively about "tokens in, tokens out"**. A cached 50K-token prefix is cheaper than uncached, but **the model still has to think over all 50K**.

### Aggressive history pruning
Some agent runtimes deliberately **drop or summarize old turns and old tool results** as the loop progresses, to keep context lean. Trades a little recall for a lot of cost and latency. **One of the most effective hidden-consumer mitigations** — but **needs care**: prune the wrong thing and the agent loses the thread. Chapter 13 returns to this.

The combination — **cache what's stable, prune what's old** — is the state of the art for keeping long agent sessions affordable. **Neither replaces "don't load the unnecessary tokens in the first place"**.

---

## FAQ

**Q1.** "If caching is on, is it safe to grow the instruction file?"  
A. **No**. Context-window space, attention, and latency are still costs. Caching only reduces $. **"Lost in the middle" gets worse too**.

**Q2.** "Can I dynamically narrow the tool catalog?"  
A. Platform-dependent. Some support "load only tools that this turn might need" mechanisms ("tool selection"). Even **manually disabling unused integrations** has big effect.

**Q3.** "How do I tune reasoning effort?"  
A. Find **minimum required effort** experimentally per task. Don't default to "high"; design to **escalate only on hard tasks**.

**Q4.** "Does replacing all history with a summary make it cheap?"  
A. **Cheaper, but quality regression risk**. **Keep recent N turns raw, summarize older** is a common hybrid.

**Q5.** "Should polite filler be removed?"  
A. User-facing: tradeoff with UX. **Internal output of batch jobs / agents**: yes — instruct "no preamble" explicitly in the prompt.

---

## Recap

- The visible prompt is the **tip of the iceberg**. The bill is dominated by tokens the runtime added on your behalf
- **Five biggest hidden consumers**: always-on instruction files, tool / function catalog, retrieved context, hidden reasoning output, the multi-step agent loop itself
- Each multiplies per turn, per step, or both. **Small per-call costs become large per-session costs**
- Small leaks — chat templates, tool-result echo, pasted errors, polite filler — also **compound at scale**
- Most platforms **don't provide source-level breakdown**. Without telemetry you **can't see where it went, can't act**
- **Prompt caching** lowers the unit price of stable prefixes but **doesn't shrink the iceberg**. **History pruning** does, but needs care
- First question for every LLM tool you use: **"what gets loaded before my prompt arrives, every time?"**

---

## Exercises

**Exercise 10.1** (5 min)  
For an agentic tool you used today, list every **enabled integration / MCP server / rules file**. Estimate **approximate token sizes** for each.

**Exercise 10.2** (10 min)  
Re-read your app's **always-on instruction file** and identify 3 paragraphs that **don't reproduce their value each time they're sent**. How much does removing them save?

**Exercise 10.3** (challenge)  
For a typical task in your agent, log the **cumulative input tokens at each step**. Plot them and observe **how much more expensive the Nth step is than the 1st**.

---

## On to the next chapter

You know where tokens go and where they hide. Natural next question: **if I cut all of these, do I cut quality too?** The answer is more interesting than yes/no. **Past a certain point, paying more doesn't buy quality** — and **below that, careful spending often beats lavish spending**.

→ [Chapter 11 — The quality vs cost curve](12-quality-vs-cost)
