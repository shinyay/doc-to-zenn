---
title: "Chapter 6 — The context window"
---

> **In one line:** The context window is the **shared budget** of tokens the model can hold "in mind" during a **single forward pass**. Everything must fit — including the answer it hasn't written yet.

---

## Why this chapter exists

Chapter 5 taught you to count. Now: **what are you counting against?** The container tokens live in.

Window size dictates almost every later design decision:
- How much history to keep
- How many retrieval results to stuff in
- How much "thinking" you let the model do
- What breaks when you forget to leave headroom

Picture **a one-turn notebook**. The page count is **fixed**. The whole conversation, all instructions, retrieved chunks, **and the answer about to be written** must all fit. **There is no extra workspace you control as a user** — the model may keep internal reasoning state, but that too lives inside this window. **If you want it in the model's "thinking", it must be on a visible page**.

---

## What the context window really is

> The maximum number of tokens the model can attend to in a **single forward pass**.

A "forward pass" is the moment the model takes everything visible and produces **the next token**. Every token accessible during that step must fit in the window.

Two consequences — frequent confusion source:

### 1. The window is **shared**

It's not split into "yours" and "the answer's". **One bar, one budget**.

### 2. The window is **per request**, not per conversation

Every model call **rewrites the notebook from scratch**. The model "remembers" nothing — the client (or platform) **resends history every turn**.

This second point is the main source of **bill surprise**. **Long conversations are expensive not because the model remembers, but because you re-send history every turn**.

---

## What shares the window

```
┌────────────────────── Context window ────────────────────────────┐
│ system │ tools │ history │ retrieved │ user │ <-- output budget │
└──────────────────────────────────────────────────────────────────┘
```

In order:

- **System prompt**: always-on instructions. Style, role, guardrails, format. **Resent every call**
- **Tool / function schemas**: each enabled tool's **definition** (name, params, description) takes window tokens. A few rich ones can quietly eat **a lot**
- **Conversation history**: past user / assistant turns. Linear conversation growth
- **Retrieved chunks**: pulled from vector DB, database, files, search APIs and pasted in
- **New user turn**: what the user just typed
- **Output budget**: **reserved space** for the answer the model is about to write

The last is **most forgotten**. The answer isn't generated outside the window — it's **written into the same notebook one token at a time**. Fill the window with input → zero pages left for the answer.

> [!IMPORTANT]
> **Output competes with input for the same budget**. A request that "barely fits" on input **fails the moment the model tries to emit token #1 of the answer**.

---

## Why there's a ceiling

"Memory and storage are cheap — why not just hand over a giant window?"

The answer is **attention**. The mechanism that decides how each token relates to every other. In its standard form it compares **all pairs** — compute and memory cost grow **quadratically** with sequence length. Double the input → cost goes up roughly **4×**, not 2×.

Modern long-context models use many tricks:
- Sparse attention patterns
- Sliding windows
- Hierarchical summarization
- Smart caching
- Hardware-aware kernels

These help a lot, but **three practical ceilings** remain:

1. **Compute**: even with tricks, longer = more per-request work
2. **Memory bandwidth**: model pushes huge intermediate state through limited memory channels. Long context **saturates the pipe**
3. **Quality degradation**: past some length, the model **stops using the window well even though it's there** (see below)

So: huge windows exist, but **"larger" and "used well" are different things**.

---

## Position encoding (briefly)

Tokens alone are an unordered bag. Distinguishing "the cat sat" from "sat the cat" requires **position information**. **Position encoding** supplies it:

- **Absolute**: fixed signal per slot
- **Relative**: encode **distance** between two tokens
- **Rotary (RoPE)**: rotate token representations by a position-dependent angle — has nice mathematical generalization properties

You don't need the math. **The one consequence to remember**: **position encoding was trained for a specific length**. Use the model far beyond its training length and **quality often degrades even though the mechanism still runs**. "Extended context" features help but are **not free upgrades — they're tradeoffs**.

---

## "Lost in the middle"

An empirical finding reproduced across many models — **internalize early**:

> Models attend well to information at the **start** and **end** of long context, but **information buried in the middle** is often missed.

So: **long context ≠ used context**. Pack in 100 retrieval docs with the answer at #50 → the chance the model overlooks it goes up **significantly**.

Practical implications:

- **Critical instructions where they won't be ignored**: usually start of system prompt, plus a **short restatement near the user's question**
- Rank retrieval chunks by relevance and put **strong ones at both ends**, not the middle
- Don't assume "I gave it the doc, it'll find it". **Giving is necessary, not sufficient**

> [!NOTE]
> Treat **the middle of long prompts as a low-attention zone**. Anything that must go there should be **restated near an edge**.

### Concrete: needle in a haystack

Simple experiment to confirm "lost in the middle" yourself:

```python
# A pile of irrelevant text + a one-line "secret" in the middle
# Note: the `pos` values below are CHARACTER offsets (Python string slicing),
# not token positions. If you want to move the needle by exact token offset,
# tokenize the filler first and choose insertion points in token space.
needle = "The secret password is BANANA42."
filler = "This is filler text. " * 1000  # several thousand tokens
char_positions = [0, 500, 1000, 1500, 2000]  # treated as character offsets

for pos in char_positions:
    haystack = filler[:pos] + needle + filler[pos:]
    prompt = f"{haystack}\n\nQuestion: What is the secret password?"
    # send to model, check answer
    # → accuracy typically dips around the middle
```

Wire this into CI to **quantify whether a new model improves or regresses on "middle use"** when you migrate.

---

## What happens when you exceed the window

**There is no unified answer** — and that's part of the problem. Different platforms (or different parts of the same platform) handle overflow differently:

1. **API hard error**: "prompt too long", immediate reject. **The friendliest failure** — loud, immediate, easy to debug
2. **Silent truncation**: platform drops old messages or trims one end and runs the request anyway. The model reasons over a **shortened version**, and **you may not notice**
3. **Client-side sliding-window summarization**: app code (or framework) replaces old turns with a generated summary to keep total under the cap. Model sees a **compressed history** — compression **you didn't sign off on**

Each hides a **different bug class**:
- Hard error → fails loudly (easy to fix)
- Silent truncation → model contradicts instructions **it never saw**
- Client-side summarization → model drifts from a fact **the user said three turns ago**

We revisit these as **anti-patterns** in Chapter 15.

---

## Output cap is **a ceiling, not a target**

When calling the model you usually specify a max output token count. Tempting to read it as "the model will produce that many" — **it won't**. It's an **upper bound**. Models often stop earlier (sentence done, hit a stop sequence, judged the answer complete).

Two things to remember about the cap:

- **You're billed for what was actually generated**: cap of "a few thousand" doesn't mean billing on a few thousand
- **The cap consumes its full size from your input budget**: even if the model writes 100 tokens, the platform **reserves the space up front**. That reservation comes out of the same window

The second is the **surprise**. Setting a large output cap "just in case" is **not a free safety margin**. It's a **direct deduction from sendable input**. If a "should-fit" prompt fails with a context-length error, **suspect the output cap first**.

---

## Build budget intuition

Specific numbers shift, so memorize the **shape**:

```
Hypothetical model: window = 128K tokens

┌────────────────────────────────────────────────────────────┐
│ system + tools (fixed):       2K   ( 1.5%)                │
│ short history (10 turns):     5K   ( 3.9%)                │
│ long history (50 turns):     25K   (19.5%)                │
│ RAG context (10 docs):       15K   (11.7%)                │
│ user message:                 1K   ( 0.8%)                │
│ output cap reservation:       8K   ( 6.3%)                │
│ safety margin:               13K   (10.2%)                │
│ ─────────────────────────────────                         │
│ free (unused):               59K   (46.1%)                │
└────────────────────────────────────────────────────────────┘
```

Hypothetical, but **"past half = danger zone"** is a useful rule. Not just because of crashes — **attention quality also degrades**. No error doesn't mean "used correctly".

---

## Going deeper

### KV cache, and why long-context **decode** is memory-bound

LLM inference has two phases with very different bottlenecks:

- **Prefill** (process the full prompt at once): big parallel matrix multiplies — typically **compute-bound** (limited by raw GPU FLOPs)
- **Decode** (generate the response one token at a time): each step is dominated by reading the KV cache — **memory-bound** (limited by memory bandwidth)

When the model emits an answer one token at a time, it doesn't redo attention from scratch each step. Instead it stores the **K and V intermediate results for tokens already seen** in a **KV-cache**. Each new token attends to the cache plus itself.

The KV-cache is **fast but big**. Size grows with sequence length × model internal dimension. **In long-context decode**, the dominant cost is **not raw compute but pushing this cache through memory** — that's what "memory-bound" means here, and it's specifically **the decode-side story**.

This is also why providers can offer discounts on **cached input tokens**: when the prefill result (the K/V) for a shared prefix is already in memory, reuse is **genuinely cheaper** than reconstruction.

### Sliding window vs full attention

Standard attention: every token sees every token. **Sliding-window attention**: each token only sees a fixed number of recent neighbors. Breaks the quadratic — at the cost of giving up global awareness for **scalability**.

Many long-context models combine: full in some layers, windowed in others — so global information **propagates without paying the full price everywhere**.

The tradeoff is real: a pure-window model can mechanically handle ultra-long sequences, but information from the far end **has to bounce through intermediate tokens** to reach the present, with signal degrading along the way. One root of "lost in the middle".

### Long-context model variants have tradeoffs

A "long-context release" usually isn't just **the same model with a bigger number**. Often it's been **retrained / fine-tuned with different position encoding, different attention patterns, or both** to behave well at length.

Compared to its short sibling:
- Slower per token
- Sometimes weaker on short-context benchmarks
- More expensive to serve

The right choice is **workload-dependent**, not "bigger number wins".

### Doubling the window doesn't double the price

Pricing is per-token, **you pay for what you actually send and receive**. A 2× window doesn't auto-double per-call cost — only for the **extra space you actually use**. Window size = capacity; price tracks **consumption**.

That said, very long requests aren't "more of the same". They use **more memory-bound hardware**, so some providers **vary input rates by length** or charge differently for **cached vs uncached**. Chapter 7 dives into the economics.

---

## FAQ

**Q1.** "With a 128K model, can I dump a 100K document and ask for a summary?"  
A. **You can put it in as input**, but **output budget plus 'lost in the middle'** make it inadvisable. Chunk → summarize → hierarchically resummarize is more predictable and higher quality.

**Q2.** "If I don't send the full history, won't the model lose context?"  
A. Yes — that's exactly the design tradeoff: full history (expensive) vs summarized history (degradation risk) vs targeted excerpts (middle ground). A common strategy is **switching by conversation length**.

**Q3.** "Is a model with a '1M context window' invincible?"  
A. **Window size and effective use are different things**. As length grows, "lost in the middle", degradation, latency, and cost all bite. Run "needle in haystack" on **your** use case to **measure** effective length.

**Q4.** "I set `max_tokens=4096` and it cut off at 3000."  
A. The cap is an **upper bound**. Models stop on EOS, stop sequences, or "answer complete". Truncation = suspect **prompt-side instructions** (any "200 chars max"? short few-shot examples?).

**Q5.** "I heard bigger windows hurt quality — true?"  
A. **Task-dependent**. Short questions: window doesn't matter. Long-context reasoning (multi-doc, long history): can degrade due to training-length mismatch and "lost in the middle". When switching models, **A/B on your representative tasks**.

---

## Recap

- The context window is a **shared budget** for system + tools + history + retrieved + user + **output**
- **Output competes with input**. Whatever `max_tokens` reserves is unavailable to input
- The ceiling comes from attention's **quadratic cost** plus **degradation past training length**
- **"Lost in the middle"** is real — put important things at the **edges**, not buried
- Overflow behavior is **platform-dependent**: hard error / silent truncation / client-side summarization — each hides different bugs
- Window = capacity; price = consumption

---

## Exercises

**Exercise 6.1** (5 min)  
For a typical recent LLM call, compute **what % of the window** is consumed by system + tools + history + user + max_tokens.

**Exercise 6.2** (10 min)  
Implement a "needle in a haystack" test:
1. One sentence: "The secret keyword is XXXX"
2. Insert at 5 different positions in a few-thousand-token filler
3. Ask "what is the secret keyword?" each time
4. Plot accuracy vs position

Does accuracy dip in the middle? You now have a model-comparison template.

**Exercise 6.3** (challenge)  
Pick a scenario in your app where **a long conversation might exceed the window**. Determine **which of the three overflow behaviors** (hard error / drop old / replace with summary) actually triggers. **If reading the code doesn't tell you, write a test that intentionally exceeds the window and run it**. Reliable way to surface hidden behavior.

---

## On to the next chapter

Container understood. Next: **the price of what's inside** — why "input", "output", "cached", and "reasoning" tokens don't share a single rate.

→ [Chapter 7 — Token economics](08-economics)
