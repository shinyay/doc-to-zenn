---
title: "Chapter 9 — Where tokens are spent"
---

> **In one line:** Your user message is **almost never the bulk of the bill**. The bill is dominated by **the instructions, tools, history, and retrieved context that ride along on every call**.

---

## Why this chapter exists

By now you understand tokens as a **unit of work, money, and latency**. Natural next question: **where do they go?**

When you ask a coding assistant a one-line question and get back a one-paragraph answer, why does the meter spin so fast?

Answer: a "single LLM call" is **almost never just your question**. It's a package assembled from **seven different segments**, all of which the model must consume every time. In agentic settings (model calls tools and loops), **that whole package is resent every step**.

This chapter opens the package. After you see what's inside, how big each part is, and why it's there, it becomes obvious why a 50-token question can quietly eat **tens of thousands of tokens**.

---

## Anatomy of a single call

A modern LLM call — chat message, agent step, or tool-use turn — is built from **the same building blocks**. Names vary across providers and frameworks, but the structure is remarkably consistent.

Seven canonical input segments + the output, in roughly the order they appear in the request:

### 1. System prompt

The instructions block telling the model "who you are and how to behave": "You are a helpful assistant…" + tone rules, format rules, refusal policy.

- **Sent every turn**
- Usually written once by the app developer
- Hundreds of tokens for a simple assistant; can balloon to **thousands** for production with many rules

It doesn't appear in the chat UI but is **the first thing the model reads**.

### 2. Always-on instruction files

A segment users **often don't even know exists**. Many agentic tools auto-inject a **project-level instruction file** on every call: repo-level guidelines, contributor instructions, project rule files the tooling auto-discovers.

- Sent **every turn, every step** of the session
- Written by you or your team — **often without thinking about token cost**
- Easily **1,000–5,000 tokens** in a serious project

The danger: these **feel like documentation, not context**. Written once and forgotten. The model **re-reads them on every call, forever**.

### 3. Tool / function schemas

If the assistant can use tools (read/write files, shell, web search, DB queries), each tool comes with a JSON-Schema-like description: name, docstring, typed parameter list. The model has to know **all of it**.

- **Sent every step** — even when no tool is used
- Each tool is typically **100–500 tokens** (depending on parameter count and description verbosity)
- A medium agent with 10–15 tools: **2,000–5,000 tokens of just schemas before any work happens**

**Removing one rarely-used tool** is one of the highest-leverage token optimizations there is. Detailed in Chapter 13.

### 4. Conversation history

**Every prior user message and every prior assistant reply** in the current session is replayed to the model on each new call. **The model has no cross-call memory** — the transcript is the memory.

- Grows **monotonically** during a session
- Includes both your messages and the assistant's **full replies** — including verbose tool-call traces
- Can **dominate everything else** after a few dozen turns

That's why long conversations get slow and expensive even when individual messages are short. Measured in Chapter 14.

### 5. Retrieved context

Specific to this turn, the app pulls in **extra material**: file contents being referenced, search results, RAG hits from a vector DB, recent error logs, open editor tabs. All of it gets prepended **before the user message**.

- In principle **only this turn** — but in practice, retrieval chunks often **leak into the conversation history and replay forever**
- Size varies wildly: hundreds of tokens (tight retrieval) to tens of thousands ("dump the whole file")

The segment **most rewarded by careful design** — because it's **most under your control**.

### 6. Current user message

What you actually typed.

- Usually **the smallest segment** of the whole request
- A few to a few hundred tokens for a typical question

The fact that **the part expressing your intent is often <1% of what gets sent** is worth letting sink in.

### 7. Reasoning hint / scratchpad / chain-of-thought

When applicable, the request includes reasoning scaffolding: hidden scratch space for the model to "think", continuing prior reasoning, structured instructions for internal reasoning. **Not all models support it, not all apps use it**.

- Sent when the app opts in
- Size depends on technique — negligible to substantial

### And: the output

The model's reply. On some models, this includes **hidden reasoning tokens that are billed but not displayed**.

- Generated **token by token** — the reason output is the slow part
- Per token, output is **often the most expensive piece** of the entire interaction

---

## Stack and visualize

The package for a mid-conversation agent turn at realistic relative sizes:

```
┌─────────────────────────────────────────────────────────────┐
│  1. System prompt                                           │ small
├─────────────────────────────────────────────────────────────┤
│  2. Always-on instruction files (AGENTS.md, project rules)  │ med-large
├─────────────────────────────────────────────────────────────┤
│  3. Tool / function schemas (one block per tool)            │ med-large
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  4. Conversation history (grows every turn)                 │ large
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  5. Retrieved context (file contents, RAG hits)             │ large
├─────────────────────────────────────────────────────────────┤
│  6. Current user message                                    │ tiny ← you
├─────────────────────────────────────────────────────────────┤
│  7. Reasoning scaffold (when applicable)                    │ varies
├─────────────────────────────────────────────────────────────┤
│  ──── model is about to generate ────                      │
├─────────────────────────────────────────────────────────────┤
│  8. Output (assistant reply, possibly + hidden reasoning)   │ small-med
└─────────────────────────────────────────────────────────────┘
```

Two things stand out: first, **the user message is a thin slice**. Second, the segments above it (which you didn't type and probably didn't see) are doing **almost all the work**.

---

## Walk through a real example

Let's put numbers on it. Suppose a coding assistant is asked to refactor a single function in a medium repository. User input:

> "Refactor `parsePayload` in `lib/parser.js` to handle empty-string cases."

The visible question. What actually gets sent on this turn:

| # | Segment | Approx tokens | Notes |
|---|---------|---------------|-------|
| 1 | System prompt | ~300 | Standard "you are a coding assistant" rules |
| 2 | Always-on instruction files | ~2,000 | Project contributor + coding style rules |
| 3 | Tool schemas (12 tools) | ~3,000 | read/write/shell/search/edit/diff/test runner… avg ~250 each |
| 4 | Conversation history (last 6 turns) | ~5,000 | Discussion leading to this refactor |
| 5 | Retrieved file context | ~4,000 | `lib/parser.js` + 2 related files |
| 6 | Current user message | ~50 | The actual question |
| 7 | Reasoning scaffold | ~0 | Not used |
|   | **Input subtotal** | **~14,350** | |
| 8 | Output | ~800 | Brief explanation + code edit |
|   | **Total** | **~15,150** | |

A 50-token question arrived on a **wave of ~14,350 tokens of context**. The actual words of intent are **~0.3% of the input bill**.

This **isn't a pathological case**. It's a carefully-set-up agent's normal operation. A casually-set-up one (5,000-token instruction file, 25 tools, dump-the-whole-repo retrieval) easily hits **5× this** for the same question.

> [!NOTE]
> The exact ratio depends on your setup, but the **shape of the breakdown is universal**: small message, small output, much larger envelope of supporting context. **Optimizing only the user message is optimizing the wrong thing**.

---

## Multi-step agent loops: the bill, re-billed

We've looked at one turn. Agentic assistants rarely **finish a task in one turn**. They iterate.

```
┌──────────────────────────────────────────────────────────┐
│  Step 1: model reads full context, writes a tool call    │
│          → tool runs, returns output                     │
├──────────────────────────────────────────────────────────┤
│  Step 2: model reads full context + tool output, writes  │
│          another tool call                               │
├──────────────────────────────────────────────────────────┤
│  Step 3: model reads all prior tool outputs + full ctx... │
├──────────────────────────────────────────────────────────┤
│  ...                                                      │
├──────────────────────────────────────────────────────────┤
│  Step N: model produces the final answer                 │
└──────────────────────────────────────────────────────────┘
```

**Crucial detail**: each step is **a complete LLM call**. The model has no inter-step memory. Step 2 sends all of step 1 + the tool output. Step 3 sends all of steps 1 and 2. And so on.

So **each round re-pays the full context bill**, plus only the new tool output is added on top.

In our example: one turn = ~14,350 input. To actually solve the refactor the model might:

1. Read the file
2. Read related files
3. Run tests
4. Inspect a test failure
5. Propose an edit
6. Apply the edit
7. Re-run tests
8. Confirm and answer

…roughly 8 steps. Each step resends the system prompt, always-on files, tool schemas, growing history, and accumulated tool outputs **in full**. A 10-step agent loop can multiply **per-turn input cost by ~10×** (or more, since history grows during the loop).

A 50-token question drove **over 100K input tokens of work**.

---

## Compounding across a session

Zoom out further. Real sessions are multi-turn:

```
total_input_tokens  ≈  Σ_t (system + always_on + tools + history_t + retrieved_t + msg_t) × steps_t

total_output_tokens ≈  Σ_t output_t × steps_t
```

Things falling out of this formula:

- **History grows**: `history_t` increases every turn → **later turns are systematically more expensive than earlier ones**
- **Tool-heavy turns are multiplicative, not additive**: adding one agent step ≠ adding a fixed cost — it's adding **another full context envelope**
- **Fixed parts compound**: the per-step "tax" of system + always-on + tools is paid `N × M` times over N turns × M average steps. **Cutting 1,000 tokens from this fixed tax often beats cutting 10,000 tokens from a single retrieval**

**Caching helps**. Many providers cache the prefix of your request (the part that doesn't change between calls), so the system prompt isn't re-billed at full price every step. **But caching is a discount, not amnesty** — token counts themselves don't change, just become cheaper. The shape of the problem is unchanged.

---

## Input/output ratio in practice

Two facts that pull in opposite directions, hold both in your head:

- **By volume**: input dominates. In agentic workloads, input is commonly **10–100× output or more**
- **By money**: **output often dominates**. Output's much higher per-token rate means a smaller number of output tokens can outweigh a much larger input on the bill

Practical implication: **you can't just optimize one side**.

- Look only at input → **surprised by the bill**
- Look only at output → **surprised by latency and context-window pressure**

Good measurement (Chapter 14) **tracks both**.

---

## Going deeper

### Chat templates use "invisible" tokens
The model doesn't actually see a clean list of `{role: "user", content: "…"}`. Behind the scenes the chat is **rendered through a template into a single token stream**, with role markers, turn delimiters, and special control tokens between every message. These are **real tokens** — they consume context-window space and are billed, but never appear in any message text.

In long conversations of many short turns, **template overhead can compound to several percent of total input**. Not the biggest item, but **real**. It's also why your token count never **exactly matches** a naive sum of message lengths.

### Tool results count as next-turn input
When a tool returns output, that output has to get back to the model somehow. Most providers **append the tool result as a special message in the conversation** → it becomes **part of input on the next step**. **A tool that returns a 5,000-token file content keeps buying 5,000 input tokens on every subsequent step until that piece of history is dropped or summarized**.

Most common surprise in agent cost analysis: a single early-session "read this big file" tool call **continues being billed in full for the rest of the session**.

### Reasoning tokens are real even when hidden
Some models do an internal reasoning pass before producing the visible answer. These reasoning tokens are **generated, billed, and counted against the context window** — even though they may not appear in the response.

Cost-wise, treat reasoning tokens as **output**; capacity-wise, as **context-window consumption**. A "short reply" from a reasoning model is deceptive: the visible part can be small while a **lot of token generation** happened underneath.

> [!TIP]
> When investigating a surprise bill or slow response, **walk the seven segments and ask "which one grew?"**. The answer is almost always **a specific one**, and it's almost never the user message.

---

## FAQ

**Q1.** "If I shorten my user message, does my bill drop?"  
A. Marginally. Improves only **about 1% of the total**. Looking at **system + tools + history** is **orders of magnitude more effective**.

**Q2.** "If I don't send the full history, will the model lose context?"  
A. Largely yes. So it's a design tradeoff: full (expensive) vs summarized (degradation risk) vs targeted excerpts (middle ground). **Switch by conversation length** is a common strategy.

**Q3.** "Are tool definitions cheaper as Markdown vs JSON Schema?"  
A. **Depends on how you write them**. Verbose descriptions, long enums, deep nesting are heavy in either. **Minimum required information** is the biggest lever.

**Q4.** "If caching is on, do I have nothing to worry about?"  
A. **No**. Caches invalidate (prefix changes, TTL, evict). You always need to **design to preserve cacheability**.

**Q5.** "I want a different dynamic system prompt every call — compromise?"  
A. **Put the dynamic part at the end**. e.g., `[stable system] + [stable tool defs] + [dynamic user-specific config]`. Keep the stable prefix cacheable.

---

## Recap

- Each LLM call is a package of **7 input segments + the output**
- The user message is **the smallest part**; supporting context dominates
- Each tool definition ~100–500 tokens; conversation history grows per turn; always-on files are paid every step
- **Agent loops re-pay the full context bill every step**: 10 steps → ~10× per-turn cost
- Across a session, **fixed segments (system + always-on + tools) are paid `N × M` times — a tax**. Cutting it has outsized impact
- By volume input dominates; by money output often dominates. **Measure both**
- Chat templates, replayed tool outputs, hidden reasoning tokens — **real consumption** that doesn't appear in any message text

---

## Exercises

**Exercise 9.1** (5 min)  
Take a representative request and decompose it via `logprobs` or your provider's usage breakdown. Get **actual token counts for each of the 7 segments**.

**Exercise 9.2** (10 min)  
Measure the token count of just your app's **always-on instruction files + tool schemas**. What % of the context window is this **per-step tax** you're paying?

**Exercise 9.3** (challenge)  
For one **typical multi-step task** in your agent, log the input token count at every step. Plot the **cumulative cost** and observe **how it grows**. You should see ~10× per-turn growth around 10 steps.

---

## On to the next chapter

You've seen the visible segments. Next we expose what's easy to miss — **hidden token consumers that drain budget without showing up in any chat transcript**.

→ [Chapter 10 — Hidden token consumers](11-hidden-consumers)
