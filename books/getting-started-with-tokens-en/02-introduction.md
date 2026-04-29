---
title: "Chapter 1 — What is a token? (Introduction)"
---

> **In one line:** A token is the unit a language model **reads, writes, counts, and bills against** — neither a character nor a word, but something **in between**. If you work with LLMs, this is **the one unit** you must internalize first.

---

## Why this chapter exists

In the preface you learned that this book starts by making *the token* feel native to you. This chapter is the **first step** of that internalization. It is intentionally **short and non-technical**. The mechanism (subwords, BPE, UTF-8 byte efficiency, …) is built up from Chapter 2 onward.

What you want here is a **working mental model** that you can carry through every subsequent chapter. Once you have it, the rest of the book becomes **resolution upgrades** to the same picture.

---

## The picture you carry

```
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│  Your prompt       │ ─► │  The model         │ ─► │  Model's reply     │
│  (text in)         │    │  (a fixed-size     │    │  (text out)        │
│                    │    │   "thinking pad")  │    │                    │
└────────────────────┘    └────────────────────┘    └────────────────────┘
         │                          │                          │
         ▼                          ▼                          ▼
   counted and                 max tokens it can           counted and
   billed as tokens            hold at once                billed as tokens
   more = slower               (= context window)          unit price typically
   prefill, more               crossing it = something     3–5× the input price;
   context fits                gets dropped                longer output, linearly
                                                           more latency
```

The picture has **three takeaways** — and only three:

### 1. **Both sides are counted**
Both the prompt you send **and** the reply the model writes are **measured in tokens** and **billed**. Counter-intuitively, **the output unit price is usually higher** (we'll see why in Chapters 7 and 8).

### 2. **The "thinking pad" has a ceiling**
Every model has a **context window** — the maximum number of tokens it can hold at once. If a conversation crosses it, *something* gets dropped. Old messages may be silently truncated, an error returned, or AI-summarized by your framework. Behavior varies by platform, but **"infinite does not fit"** is universal.

### 3. **The model does not see characters**
The model sees a **sequence of integer IDs** (one token = one ID). The string `Hello, world!` becomes something like `[9906, 11, 1917, 0]` *before* the model touches it. This is true at training time and at inference time. **A token is not a billing fiction layered on top — it is the model's native unit of reading and writing**.

That's the whole mental model. The next 15 chapters can each be read as **zooming into one part of this picture**.

---

## Three things "token" does **not** mean

The word "token" gets used in many places in software. In this book, "token" is **none of these**:

### ❌ Security tokens
API keys, OAuth bearer tokens, JWTs, CSRF tokens — secret strings that represent permission. **No relationship** to this book's tokens. Same English word, different domain.

### ❌ Compiler / parser tokens
In language-processing toolchains, "token" means a **syntactic atom** like `if`, `==`, identifiers, literals. LLM tokens borrow the name from this older usage, but **the unit boundaries and meaning are different**.

### ❌ Words, characters, or morphemes themselves
The book's token is its own unit, sitting **between** characters and words. "1 word = 1 token" is wrong. "1 character = 1 token" is also wrong. Both.

> [!NOTE]
> When this book writes **"token" without modifier**, it always means **"the unit a language model reads and writes"**. Other meanings always carry a modifier ("security token", "syntactic token", etc.).

---

## Why subword and not character or word?

The full story is in Chapter 2; the **one-liner** preview:

- **At character granularity**: same text becomes 5–10× longer in unit count → eats the context window and explodes compute
- **At word granularity**: vocabulary balloons into the millions and cannot handle unknown words (typos, neologisms, foreign words)

The **subword** is the unit that absorbs both weaknesses by sitting in the middle. Typically smaller than a word and larger than a character, with one ID per frequently occurring substring. For example, `tokenization` typically splits as `["token", "ization"]` — **two tokens**. Both `token` and `ization` are common enough across English text to deserve their own slot — that is the BPE algorithm's "judgment".

That this is "just right" is empirical, but every modern frontier model has converged on it.

---

## Why everyone cares about tokens — three costs

The reason tokens matter is that **three different costs** are paid in the same unit.

### 💰 Cost 1: Money
Almost every LLM provider bills **per token**. The bill scales **roughly linearly** with token count.

```
cost per call = input tokens     × input rate
              + output tokens    × output rate
              + cached tokens    × cached rate     (when cache hits)
              + reasoning tokens × output rate     (when reasoning is billed)
```

"1M calls per day × 5,000 tokens trimmed each" turns into hundreds of millions of tokens per day saved = **real money**.

### ⏱️ Cost 2: Time
Generating tokens takes **wall-clock time**. A reply twice as long takes about twice as long to generate (Chapter 8 unpacks this).

That's a UX event. "Fast" is perceived as "smart". A 200ms latency improvement changes user behavior.

### 🪣 Cost 3: Capacity
Every model has a **fixed-size context window**. There's an upper bound on what fits, and crossing it drops something.

In other words, **a token is a budget before it is a price**. Even ignore the money, and **the capacity constraint remains unavoidable**.

> [!IMPORTANT]
> Being able to **discuss money, time, and capacity in one unit** is the real return on becoming fluent in tokens. Imagine if CPU usage, memory pressure, and network bandwidth could all be expressed in **one unit** — the LLM world has that. The unit is the token.

---

## Thinking in tokens vs thinking in "prompts" or "requests"

Concretely, **a team that thinks in prompts and a team that thinks in tokens see the same system differently**:

| Question | Prompt-thinker | Token-thinker |
|----------|----------------|---------------|
| "Usage is up" | Look at call count | Look at avg tokens × calls |
| "Cost is high" | Premium model? | Input vs output vs cached vs reasoning? |
| "It's slow" | Server backed up? | Prefill grew? Decode grew? |
| "Quality dropped" | Model regressed? | Context bloated → lost-in-the-middle? |
| "Context-length error" | Just shorten it | Which segment is bloating? |

Thinking in tokens **localizes the problem**. Cloudy "heavy / expensive / slow" complaints become **measurable quantities**. That **upgrades the quality of design decisions** by a level.

---

## A quick word on "tokens will be free anyway"

The full treatment is in Chapter 15; a short preview here.

"Models keep getting cheaper" + "context keeps getting longer" → "the token discussion will be obsolete in a few years" — a **common counter-argument**.

Short rebuttal: **the same thing happened with bandwidth, storage, and telemetry**. All of them got **orders of magnitude cheaper** over 30 years. Nobody says "storage optimization is unnecessary now". Why? **Demand always expands to fill cheaper supply**. As tokens get cheaper, **we use far more of them**. "Unit price down × usage way up" = the bill **does not shrink** (often it grows). That is the historical pattern.

Also, the three non-money costs — **time (latency), capacity (context), quality (lost-in-the-middle)** — are *not* solved by "unit price drops". They are **structural**.

Save the rest for Chapter 15.

---

## What this book covers and doesn't (quick view)

| ✅ Covered | ❌ Not covered |
|------------|----------------|
| What tokens are (Part I) | Specific-model fine-tuning |
| Why they matter (Part II) | RAG pipeline implementation |
| Where they go (Part III) | A "prompt engineering tricks" catalog |
| How to keep healthy (Part IV) | LLM API benchmarks |
| Why optimize (Part V) | Building inference servers |
| Hygiene principles, anti-patterns, measurement | The `tokopt` toolkit (closing column previews only) |

This book's role is to be **the foundation that makes a tricks-catalog readable**, not the catalog itself. After it, you'll be able to read every LLM-optimization article on the internet with **the right amount of skepticism and the right amount of curiosity**.

---

## Recap

- A token is the LLM's unit of **reading, writing, counting, and billing**. Not a character, not a word — its own unit
- **Both sides are counted**: input and output are billed; **output is usually pricier per unit**
- **Context window is fixed**. A token is **a budget before it is a price**
- A token drives **three costs at once**: money, time, capacity
- Thinking in **tokens, not prompt count**, localizes problems and upgrades design judgment
- "Tokens will be free" is **only partially right**: unit price falls, usage explodes, and structural costs (capacity, quality) don't yield to price drops anyway

---

## Exercises

**Exercise 1.1** (5 min)  
For an LLM service you used recently (ChatGPT, Copilot, Claude, …), answer:
- What's the billing unit? (Calls? Tokens? Monthly?)
- Can you state the context window size?
- **What's the source** of that number? (Docs? Hearsay? Hazy memory?)

**Exercise 1.2** (10 min)  
Install `tiktoken` and run:
```bash
pip install tiktoken
```
```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
samples = [
    "Hello, world!",
    "こんにちは、世界！",
    "def hello_world(): pass",
    "🚀🚀🚀",
]
for s in samples:
    tokens = enc.encode(s)
    print(f"{len(tokens):3d} tokens | {len(s):3d} chars | {repr(s)}")
```
Note how far your prediction was from reality. The gap closes through Chapter 4.

---

## On to the next chapter

You have the mental model. Next, we open the box: **what kind of unit, exactly, is a token, and why did the field settle on subwords?**

→ [Chapter 2 — What a token really is](03-what-is-token)
