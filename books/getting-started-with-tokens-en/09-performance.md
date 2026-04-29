---
title: "Chapter 8 — Tokens and performance"
---

> **In one line:** Tokens cost not only money but **time**. Understanding how the model spends each ms is the difference between an app that feels **instant** and one that feels **broken**.

---

## Why this chapter exists

Chapter 7 treated tokens as **bill line items**. Now another side: tokens are also the **unit of work the hardware actually performs**. Every token in / out of your app burns **wall-clock time** on a GPU somewhere. It surfaces as:

- **Latency** to the user
- **Throughput limits** in batch jobs
- **Concurrency ceiling** for your service

**A response that costs almost zero money can still feel slow if you ask wrong**. **A response that costs a lot can feel snappy if you stream it well**. Money and time are correlated, but **not the same currency**.

---

## Two phases, two cost shapes

Inference happens in **two distinct phases**. From the outside they look the same (tokens go in, tokens come out), but **their performance profiles are completely different**. If you remember one thing from this chapter, remember the shape of these two curves.

### Prefill — reading the prompt

When you send a prompt, the model first **reads the entire thing**. This is **prefill**. It pushes each input token through every layer of the network and computes the internal state needed to produce the first output token.

Defining property of prefill: **highly parallel**. The model knows all input tokens before starting, so it processes them in **one big batched pass** using the entire accelerator. GPUs love this. **Doubling input length doesn't double wall-clock time** — the hardware absorbs much of the extra work in parallel.

```
PREFILL
input tokens:  [t1][t2][t3][t4][t5][t6][t7][t8] ... [tN]
                |   |   |   |   |   |   |   |       |
                v   v   v   v   v   v   v   v       v
               +-----------------------------------------+
               |   one big parallel forward pass         |
               +-----------------------------------------+
                                 |
                                 v
                        (ready to emit token 1)
```

### Decode — generating the response

Once prefill finishes, output token generation begins. This is **decode** (or "generation"). Decode is the **opposite** of prefill: fundamentally **sequential**.

To produce output token N, output tokens 1…N-1 must **already exist** (each new token is conditioned on all previous). So **one full forward pass per output token**. The output dimension **cannot be parallelized**. One step at a time.

```
DECODE
              forward pass -> output token 1
              forward pass -> output token 2
              forward pass -> output token 3
              ...
              forward pass -> output token M
```

| Phase | Scales with | Parallel? | Dominant cost |
|-------|-------------|-----------|---------------|
| Prefill | input length | ✅ one batched pass | compute on wide tensors |
| Decode | output length | ❌ one pass per token | memory bandwidth, repetition |

This single distinction explains **almost everything you feel** when using generative AI.

---

## The two latency numbers that matter

Two numbers that capture the felt speed of an LLM call. **Get used to them — you'll see them everywhere**.

### Time-to-first-token (TTFT)

**TTFT** = wait between the user pressing "send" and the first character of the response appearing. Mostly a function of prefill: **longer prompt = longer prefill = longer TTFT**.

Short prompts feel snappy. Very long prompts (bloated system messages, packed conversation history, big document attachments) feel heavy **before any text shows up**.

> **The first second of silence is the most expensive second in the whole interaction** — it's the second the user spends deciding "is this broken?".

> [!TIP]
> If your prefix is stable, the serving stack can reuse work from prior calls (a **KV-cache hit**). On a hit, most of prefill is skipped and **TTFT collapses to near network round-trip time**.

### Inter-token latency and tokens-per-second (TPS)

After the first token appears, the model settles into a **steady drip** of output tokens. **Inter-token latency** = the gap between consecutive tokens; **TPS** = the inverse. This is the model's **typing speed**.

TPS depends mostly on:

- **Model size**: bigger model = more work per token → slower decode
- **Serving stack**: batching, quantization, attention kernels, hardware
- **Concurrency on the server**: your request shares the GPU with others

TPS is **roughly independent of prompt length**. Once decode starts, the model cranks out tokens at its rate regardless of how big the prompt was.

### Putting them together

End-to-end latency for a single request:

```
total_latency  ≈  TTFT  +  (output_tokens / TPS)
                  ^^^^      ^^^^^^^^^^^^^^^^^^^^^
                  prefill   decode
                  (input)   (output)
```

Stare at that for a moment. In many production conversations, the **second term dominates**. A model decoding at modest TPS spends **far longer producing a few hundred output tokens than reading a few thousand input tokens**. That's why "shorter prompt = faster response" is **only half right** — it helps TTFT, but if generation is long, the user still waits out the decode tail.

More bluntly:

> **Input length controls how fast the response starts; output length controls how long it lasts**.

---

## Streaming: the UX trick that buys nothing yet buys everything

Decode is sequential, so the model knows each output token the moment it's generated. **No reason to wait for the whole response**. Modern APIs **stream** tokens back as they're produced.

Streaming **saves zero tokens**. Total compute is identical. But the user-side experience flips:

```
NON-STREAMING                    STREAMING
                                  
[send] ............ [whole]      [send] [t1][t2][t3][t4][t5]...
       <-- silence -->                  <-- words appearing -->
       perceived latency                perceived latency
       = total_latency                  ≈ TTFT
```

The user starts reading the moment the first token arrives. By the time they finish the first sentence, the model has produced the next several. **A 10-second response can feel almost instant if streaming hides the decode tail behind the user's reading speed**.

Practical consequences:

1. **Always stream in interactive UIs**: chat, autocomplete, code suggestions — anything a human watches. Same bill, dramatically different experience
2. **Streaming makes TTFT the felt-latency number**: prompt length and prefix-caching optimizations now **directly affect product responsiveness**

```python
# OpenAI streaming example
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

---

## Throughput vs latency: the batching tradeoff

Behind an API endpoint, providers don't run your request alone on a dedicated GPU. They **batch** many concurrent requests. Hardware can run a wide matmul almost as fast as a narrow one, so **packing many requests increases total throughput (sum of TPS across users)** at the cost of per-request latency.

```
LOW BATCH (few users)              HIGH BATCH (many users)
+---------+                        +---------+---------+---------+
| req A   |                        | req A | req B | req C | ... |
+---------+                        +---------+---------+---------+
A is fast,                         A is slower,
GPU underused                      GPU saturated, cheaper per token
```

You don't see batches as a user — you see consequences:

- **Latency varies with load**: same request feels different at 3am vs peak
- **Cheap tier models often run hotter batches**: that's part of why they're cheaper per token, traded against latency consistency
- **Throughput-oriented workloads (overnight batch, doc pipelines) want batch-friendly designs**: many concurrent requests on a small fast model often produce **more done-work-per-minute** than one request on a big slow model

The right question isn't "what's the fastest single-call model?" but **"what configuration finishes all my work in the available time and budget?"**.

---

## KV-cache, in plain English

"KV-cache" has come up twice already. Worth understanding — it's the structural reason prefix caching is so powerful, and it returns in Chapter 10.

Each Transformer layer stores **two tensors per sequence position**: **K** (keys) and **V** (values). Attention uses them to decide what each token should attend to. To produce token N, the model needs K and V for tokens 1…N-1.

Without a cache, every new token would force **recomputing K, V for all prior tokens** — quadratic, unaffordable. Serving systems store K and V as they go — that's the **KV-cache**. Each decode step **only computes K, V for the one new token** and reuses everything else.

```
KV-CACHE DURING DECODE

  past:  [K1,V1][K2,V2][K3,V3] ... [K_{n-1},V_{n-1}]   <-- already cached
  new:   [Kn,Vn]                                        <-- only this is computed
         -----------------------------------------------
         attention runs over the whole thing
```

Extend the same idea across requests: **two requests sharing a prefix** (e.g. the same long system message) have identical KV tensors for that prefix. **Serving stacks with prefix caching** recognize this and **reuse the cached K, V** instead of recomputing.

That's why a cached prefix is both **fast** (no prefill compute on the cached portion) and **cheap** (providers offer big discounts on cache-hit input). **Same mechanism, two payoffs**.

Flip side: **caches are finite** and can be evicted under load. Cache keys are sensitive to **exact prefix bytes** — change one character at the start of your prompt and **everything below is invalidated**. Designing for cacheability means **stable front, variable tail**.

---

## Practical patterns

### For interactive chat UX
- **Stabilize the prefix**: system prompt, instructions, persona, reused context up front. Identical across turns. User's new input at **the very end**
- **Stream the output**: always. No reason not to
- **Cap max output length to a sensible budget**: runaway long generation hurts wall clock more than long prompts do
- **Monitor TTFT as a product metric**: that's the number users actually feel

### For batch jobs
- **Optimize total throughput, not per-request latency**: summarize 10K docs overnight → question is "total wall clock and total cost", not "speed of one summary"
- Where quality allows, prefer **many concurrent requests on a small fast model over one on a big slow one**
- **Reuse a stable prompt template across all items**: same prefix, only the tail changes. Prefix caching pays **huge dividends here**

### For looping agents
Agentic systems (plan, call tool, repeat) is where intuitions about cost and performance break **fastest**. Cost is Chapter 11; the performance side is just as severe:

- **Each loop iteration pays its own prefill bill**: rebuilding the prompt from scratch each step makes the model **re-read everything every time**. 10 steps × fat context = 10 prefills on a growing prompt
- **Design loops to run on the same prefix**: append new observations to the tail. Don't reorder history at the front
- **Cache hits make agents viable**: long agent loops without prefix caching are slow and expensive. With caching, the marginal cost of an extra step stays sane

> [!IMPORTANT]
> If your agent's wall-clock time scales **worse than the number of steps**, suspect **a prefix that mutates between iterations**. A small change at the prompt's front invalidates every cache below it.

---

## Going deeper

### Speculative decoding
Decode is slow because it's sequential (one pass per token). **Speculative decoding** is a clever trick that breaks the sequence. A **small fast "draft" model** proposes several tokens at once. The **large "target" model** then **verifies them in one parallel pass**. If the draft matches what target would emit, accept all → **multiple decoded tokens for the price of one big-model pass**. If the draft was wrong, fall back at that point.

Output is **mathematically identical to the big model alone** — **no quality loss**. Just less wall-clock time. Many production serving stacks use this. Users don't see the mechanism, just notice TPS higher than the raw decode rate suggests.

### Mixture-of-experts (MoE) models
Traditional dense models use **all parameters on every token**. **MoE** activates **only some — a few experts out of many** per token. **Total parameter count is huge, per-token compute is small**.

Performance implications:
- MoE can be **collectively huge yet per-token cheap and fast**
- Performance under load can be **lumpy** (routing affects which experts get hit, batching is trickier)
- Per-token price reflects **active**, not **total** parameters → "huge" models can be **surprisingly cheap**

### Public benchmarks vs production reality
Benchmark TPS uses near-ideal conditions: warm caches, short batch queues, well-tuned hardware. **Production latency is messy**: concurrency varies, caches evict, networks are flaky, long-tail requests stretch the queue, cold starts and retries add overhead.

Lesson: **measure your latency on your traffic**. Headline numbers are useful for ballpark comparison, not capacity planning. Chapter 14 covers measurement.

---

## FAQ

**Q1.** "Will shorter prompts make responses faster?"  
A. **Helps TTFT**. Total latency depends on output length too. If you expect a long answer, controlling output length matters more.

**Q2.** "Does streaming save tokens?"  
A. **Zero**. Only changes the felt experience. Bill is identical.

**Q3.** "High-TPS model = good model?"  
A. Speed is one dimension. Look at **quality, context, cost, cache support** too. "Benchmark TPS" doesn't guarantee production reproducibility.

**Q4.** "Can I control the KV-cache?"  
A. Provider-dependent. Some let you mark messages with `cache_control: {"type": "ephemeral"}` for explicit control. Many do **automatic** prefix detection. **Read your provider's caching docs**.

**Q5.** "Will more concurrent requests scale throughput linearly?"  
A. **Up to a point**. Server-side batch depth limits, rate limits, and queue waits cap it. **Find the sweet spot empirically**.

---

## Recap

- Inference has two phases: **prefill** (parallel, scales with input length) and **decode** (sequential, scales with output length)
- **TTFT** is dominated by prefill; **TPS** by model size + serving stack
- total latency ≈ TTFT + output_tokens / TPS. **For long generations, output length dominates wall-clock time**
- **Streaming** saves no tokens but transforms felt experience. **Always in interactive UIs**
- Providers **batch** — surfaces as variable speed
- **KV-caching** is the structural reason cached prefixes are fast and cheap
- **Chat**: stabilize prefix, stream, cap output. **Batch**: maximize total throughput. **Agents**: protect the cache across iterations
- **Speculative decoding** raises TPS; **MoE** breaks "bigger = slower"
- **Production latency ≠ benchmark latency**. Measure your own

---

## Exercises

**Exercise 8.1** (5 min)  
Run a representative request with streaming enabled. Record **time of first chunk** and **time of completion**. Ratio of **TTFT** to **total**?

**Exercise 8.2** (10 min)  
Run the same prompt with `max_tokens=100` and `max_tokens=1000`. Compare actual latency. Observe the scaling of output length vs wall-clock time.

**Exercise 8.3** (challenge)  
For your app's prompts, check:
1. Is the first 1KB of prefix really **stable**? (any timestamps, random IDs, usernames sneaking in?)
2. If not, can you move them to the tail?
3. After moving, measure TTFT change

---

## On to the next chapter

You now know the **two currencies** tokens are paid in (money and ms). Next we **dissect a single API call** and trace **where each token went** — system message, tools, format overhead, all the parts you didn't realize you were billed for.

→ [Chapter 9 — Where tokens are spent](10-where-spent)
