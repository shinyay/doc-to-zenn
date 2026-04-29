---
title: "Chapter 7 — Token economics"
---

> **In one line:** Tokens are the **unit of compute** and the **unit of price**. Three things explain almost every billing surprise: input/output asymmetry, prefix caching discounts, and the hidden cost of reasoning tokens.

---

## Why this chapter exists

So far we've treated tokens as a **technical quantity**. Now we switch lens. Tokens are also the **unit of the bill**, the **unit of budget**, the **unit of capacity planning**. Specific rates change every few months but **the shape of pricing** is stable, so we internalize the shape.

If you remember one thing:

> **The model bill is determined not by request count but by**tokens flowing through the request. **And not all tokens are priced equally**.

---

## The unit of price: per million tokens

Almost every hosted-model provider publishes prices the same way: **per million tokens (per MTok)**. Each model lists **two rates**:

- **Input rate**: per token sent to the model (system + history + retrieved + user + tools + attachments)
- **Output rate**: per token the model generates

"Per million" rather than "per token" is **for readability** (per-token would be too many leading zeros). Base formula:

```
cost_for_a_call = (input_tokens  / 1_000_000) × input_rate
                + (output_tokens / 1_000_000) × output_rate
```

That's the **whole formula** for a single call without caching or reasoning. The rest of the chapter is modifiers: discounts on some input, hidden surcharges on output, aggregation across many calls.

> [!NOTE]
> When comparing models, always compare **the pair**. A model cheap on input but expensive on output may be attractive or punishing depending on the workload's shape.

---

## The input/output asymmetry

The single **most important pricing fact**, and the one that surprises beginners most:

> **Output tokens cost several times more than input tokens**. The multiplier is provider/tier-dependent — across the industry typically **3–5×**, sometimes more for frontier models.

Why? Not arbitrary pricing — it **reflects underlying compute**.

- **Input is parallel**: a 10,000-token prompt is consumed by the model in **a single forward pass** (the prefill) — efficiently batched matrix operations. The GPU is densely used → **cheap per token**
- **Output is autoregressive (sequential)**: each output token requires **its own forward pass through the entire model**, conditioned on tokens generated so far. No parallelizing the future — generate token 1, then token 2 conditioned on token 1, then token 3 conditioned on tokens 1 and 2…

```
INPUT (parallel, cheap per token)        OUTPUT (sequential, expensive per token)

  [t1 t2 t3 t4 t5 ... tN]                 [o1] -> [o1 o2] -> [o1 o2 o3] -> ...
   \  \  \  \  \      /                    ^         ^            ^
    \  \  \  \  \    /                     |         |            |
     >>> 1 forward pass <<<            1 fwd     1 fwd        1 fwd
                                        pass      pass         pass
```

Reading 1M tokens = one big **parallelizable** prefill — cheap **per token**. **Writing** 1M tokens = a million sequential forward passes, expensive **per token**. The point isn't that reading is absolutely cheap, but that the **per-token cost** is very different.

### Practical implication

The asymmetry changes prompt-editing decisions:

- Adding **100 input tokens** to the system prompt (a small instruction, a clarifying example) is **almost free**. Even called every turn, it's a tiny increment relative to the output produced
- Adding **500 output tokens** to every response ("explain reasoning step by step", "always include a summary") is **really expensive**. Output is on the high side of the asymmetry, and every added sentence keeps paying at the high rate forever

Lesson: **Be generous with what you ask the model to read; be frugal with what you ask it to write**.

---

## Cached tokens: the stable-prefix discount

Most modern hosted APIs support **prompt caching / prefix caching**.

How it works: as the model processes input, it builds **per-layer K/V cache** (internal Transformer state). When a **subsequent request begins with the exact same prefix**, the provider can **reuse that internal state** instead of recomputing from scratch.

The savings are passed back: **cached input tokens are heavily discounted** — often **~10% of full rate** (varies by provider). **Right order of magnitude as a mental model**.

```
fresh input  :  ████████████████████  (full)
cached input :  ██                    (~10%)
output       :  ████████████████████████████████████████████████████████████  (3–5×)
```

### What "the same prefix" means

The cache is typically **prefix-keyed**: as long as the new request's start matches a prior request's start **byte-for-byte (or token-for-token)**, you hit. **The instant they diverge**, everything after is treated as fresh.

Huge implications for prompt structure:

- **Stable content first**: system prompt, tool definitions, persistent role, large reference docs unchanged across turns — all at the **start**
- **Volatile content last**: user's latest message, latest tool result, anything per-turn — at the end, keeping the long expensive prefix above **cacheable**

A 50,000-token system prompt that's identical every call is, at steady state, **roughly an order of magnitude cheaper** than a 50,000-token system prompt regenerated every call. Same token count, ~10× billing difference (the exact ratio depends on provider).

> [!TIP]
> When redesigning a prompt, ask: "Did I just **break the cacheable prefix by moving one line**?" Reordering one sentence at the top can invalidate every cache below it.

### Cacheable-prefix pattern

```python
# Good: stable → volatile
messages = [
    {"role": "system", "content": LARGE_STABLE_SYSTEM_PROMPT},  # cached
    {"role": "system", "content": REFERENCE_DOCS},              # cached
    *conversation_history,                                      # partially cached
    {"role": "user", "content": new_user_message},              # volatile
]

# Bad: timestamp at top destroys the cache every call
messages = [
    {"role": "system", "content": f"Current time: {now()}\n{LARGE_SYSTEM_PROMPT}"},  # different every call!
    ...
]
```

Putting **volatile data like a timestamp at the top** invalidates **everything below it**. If you need a timestamp, put it at the **end** or **fetch it via a tool**.

---

## Reasoning tokens: invisible output

Newer wrinkle: many newer models are designed to **"think" before answering**. Internally they generate a reasoning token stream (a **private scratch pad**) and only after that emit the visible answer.

The user sees only the **final answer** — but for billing, the **hidden reasoning tokens are real tokens**, generated autoregressively at full output cost. **Most providers bill them as output tokens**, but **the exact accounting (folded into output, reported on a separate line, or even free vs paid) varies by provider** — always check the billing docs of the model you use.

```
visible to user:    [final answer tokens]
billed as output:   [reasoning tokens] + [final answer tokens]
                    \________________/
                     unseen but paid for
```

For models that expose a "reasoning effort" / "thinking budget" knob:

- **Low effort**: a few hundred reasoning tokens — small surcharge over the visible answer
- **High effort**: **thousands or tens of thousands** of reasoning tokens — sometimes far more than the visible answer itself. On hard problems, reasoning **dominates output cost**

Practical consequences:

1. When measuring "reasoning model" cost, **always include reasoning tokens**. Counting only the visible answer **massively understates the bill**
2. Cranking reasoning effort up "just in case" is **the easiest way to silently double output cost**. Reasoning effort is **a knob to tune per task**, not a default to raise

---

## Tiers within a model family

Most providers ship a model family in **performance/price tiers**:

| Tier | Typical use | Relative price per token |
|------|-------------|--------------------------|
| 🟢 Small / cheap | Classification, extraction, routing, simple drafts | Lowest |
| 🟡 Mid-tier | General chat, summarization, most apps | Mid |
| 🔴 Frontier | Hard reasoning, complex code, high-stakes decisions | Highest |

The gap between cheapest and frontier is **often an order of magnitude, sometimes more**. Frontier reasoning models are even more, factoring in their tendency to think more.

This is why "**always use the best model**" is rarely correct. Workloads dominated by simple, repetitive calls can usually run on the cheap model at **1/10 the cost** with no measurable quality loss. Workloads where a few hard decisions matter most: **frontier only for those**, cheap tier for the rest. The pattern (**route by request type**) recurs throughout this book.

---

## Two billing styles

Tokens are the underlying reality, but users see them in **two different shapes**.

### 1. Pay-per-token (direct API, usage-based)

End of period: bill is **exact tokens consumed × respective rates**. No flat fee, no quota, no cap unless you set one.

- **Pros**: linear, transparent, easy to model. Traffic 2× → bill 2×
- **Cons**: no natural ceiling. **Runaway loops**, **misconfigured agents**, **viral product**: yesterday's order-of-magnitude bill spike is invisible until you look

Almost every direct API offering. Living on it requires **your own observability and budget guards** (Chapter 14).

### 2. Request-based / quota-based (subscription, per-request)

What end users mostly see. Pay flat per period (monthly sub, seat license, included quota), get "requests" / "messages" / "premium requests" / "credits" in return.

- **Pros**: predictable for the buyer, capped, easy to budget
- **Cons**: **billing unit (request) and consumption unit (token) have no fixed relationship**. One request might be a single-line question or a 50-turn agent session burning millions of tokens internally. **Indistinguishable from inside the quota**

```
pay-per-token:                   quota:

bill = Σ tokens × rate           bill = flat_monthly_fee
                                 allowance: N "requests" / month
predictable per call,            predictable per month,
unbounded per month              opaque per call
```

Real products often **mix both**: free/included request quota → overage at token rates. **Builders need to understand both sides** — what users see (quotas / requests) and what providers bill (tokens).

### Free-tier and fallback UX

Because per-tier costs differ massively, products often:

- **"Auto" model selection**: system silently routes each request to "cheapest model that will succeed"
- **Fallback chain**: failed cheap-model request retried on stronger model
- **Budget-exhaustion graceful degradation**: switch from frontier to mid-tier rather than rejecting the request

These are **UX choices**, but they're entirely driven by this chapter's economics. Products that don't think hard about **which tier handles which request** either overspend or underdeliver.

---

## Worked example

Scenario:
- system + tools = **5,000 tokens**
- reference doc attached on every call = **45,000 tokens**
- conversation has **100 turns**
- average user message **200 tokens**, average answer **300 tokens**

Track input cost only, **without caching** first:

Each turn sends: 5,000 (system) + 45,000 (doc) + history so far + new message. Ignoring history growth, you send a **50,000-token always-on context for 100 turns**:

```
50,000 tokens × 100 turns = 5,000,000 input tokens
```

That's **the same input bill as one 5M-token request**. **Repetition is the cost**. You didn't write 5M tokens — you wrote 50K once and resent it 99 times.

Now with caching on. The 50,000-token prefix is identical from turn 2 onward:

- Turn 1: 50,000 fresh input
- Turns 2–100: 50,000 **cached** input + the few fresh tokens of the new message

If cached costs ~1/10 of full rate, the input bill across 99 turns drops by **about 90%**. Output bill is unchanged (cache is input-only). **The dominant cost shrinks dramatically**.

The central economic insight for long sessions:

> Without caching, what you're really paying for is **re-reading the same context over and over**. Caching is precisely the mechanism that destroys this cost.

---

## Going deeper

### Volume discounts and committed spend

At meaningful scale, **list price isn't the price you pay**. Providers commonly offer:

- **Volume discounts**: per-MTok rate drops past monthly thresholds
- **Committed-spend agreements**: discount in exchange for guaranteed minimum monthly spend over a term

List price is a **ceiling, not a floor**. If you're forecasting a large workload, plan with **rates assumed-negotiable**.

Hidden cost of multi-vendor strategy: spreading traffic can leave you **below the volume tier on every vendor**.

### Region-based price differences

Some providers vary per-MTok rate by **calling region**. Differences are usually modest but nonzero. Interacts with **data-residency requirements**: the cheapest region may not be one you're **allowed to use**. Treat region as a **joint cost+compliance decision**.

### Hosted vs self-hosted economics

- **Hosted**: $/token (pay only for what you consume)
- **Self-hosted**: fundamentally **$/GPU-hour** (pay for time the hardware exists)

Not the same currency. Conversion is harder than it looks:

```
effective_$_per_token = (gpu_hours_consumed × $_per_gpu_hour) / tokens_processed
```

Self-hosted is cheaper per token **only when well-utilized**. At 10% utilization, the effective per-token rate **exceeds hosted by a lot**. Why self-hosting only economically wins on **sustained high volume**.

### Effective rate, with caching

When caching is in play, **list input rate is no longer the input rate**. The number to track is **effective input rate**:

```
effective_input_rate = (fresh_input × fresh_rate + cached_input × cached_rate) / total_input
```

Workloads with a big stable prefix + small volatile tail can drop their steady-state effective rate to **15–25% of full rate** — **structural savings invisible from the price table alone**. Conversely, workloads that change the prefix every turn pay full rate regardless.

When comparing providers/models for a real workload, compute the **effective rate for your access pattern** — not list.

---

## FAQ

**Q1.** "Input is cheap, so optimal = always send a huge context and keep output short?"  
A. Roughly right *if caching is in play*. But assumes you don't break **cacheability**. Stable prefix on top, volatile at bottom — protect that rule.

**Q2.** "Can I just set `reasoning_effort=low` on a reasoning model to lower cost?"  
A. **Yes, but accuracy usually drops too**. Find the **minimum required effort per task type** experimentally.

**Q3.** "How long does the cache live?"  
A. Provider-dependent: 5 minutes to 24 hours. **Frequently-accessed** prefixes often get extended. Long-idle prefixes are evicted.

**Q4.** "Output rate is high, so getting JSON back saves money?"  
A. **Mostly yes**. You pay for the structural symbols (`{`, `}`, `"key":`), but save on **verbose prose**. Long key names erode the savings (`"customer_invoice_id"` vs `"id"`).

**Q5.** "Can I see reasoning tokens in `usage`?"  
A. Provider-dependent. OpenAI o-series exposes `usage.completion_tokens_details.reasoning_tokens`. Anthropic extended thinking gives a similar breakdown. **Wire this into your monitoring**.

---

## Recap

- Prices are **per million tokens**, separate rates for input and output
- **Output is 3–5× input** — reflects parallel vs sequential compute
- **Cached input is heavily discounted** (~10%). Stable prefixes are an order of magnitude cheaper than volatile ones
- **Reasoning tokens are billed as output** (even though invisible). Can dominate on hard tasks
- Cross-tier price gaps are **often an order of magnitude**. Routing simple work to cheap models is **the highest-leverage optimization**
- Two billing styles: pay-per-token (linear, unbounded, transparent) and quota (flat, capped, opaque)
- Long-session cost is governed less by **what you said** than by **how many times you re-sent the same context**. Caching is the mechanism that breaks that
- At scale, confront **volume discounts, region, hosted vs self-hosted, and effective rate**

---

## Exercises

**Exercise 7.1** (5 min)  
Look up your usual model's input/output rates. Compute the **output / input ratio**. In the 3–5× range?

**Exercise 7.2** (10 min)  
For one of today's requests, compute:
1. fresh input × fresh_rate
2. cached input × cached_rate (if you use caching)
3. output × output_rate
4. sum = cost per call

Multiply by monthly traffic to get a **monthly forecast**.

**Exercise 7.3** (challenge)  
Re-read your app's prompts and **draw the line between "cacheable prefix" and "volatile tail"**. Is there a rewrite that **pushes more of the prompt into the prefix half**? Propose one concrete improvement.

---

## On to the next chapter

We saw how tokens become **money**. Next: **time** — latency, throughput, what users feel as "fast". Same per-token mechanics, but with a **different denominator**.

→ [Chapter 8 — Tokens and performance](09-performance)
