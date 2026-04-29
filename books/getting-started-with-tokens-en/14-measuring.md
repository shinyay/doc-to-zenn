---
title: "Chapter 13 — Measuring tokens"
---

> **In one line:** You can't manage what you can't see, and what you should see is not "tokens used" but **the full cost mix**, **sliced by user and task**, with **honest respect for how heavy-tailed the distribution actually is**.

---

## Why this chapter exists

When a team **first looks at their token telemetry properly**, the reaction is almost always the same: **surprise at where the bill actually goes**. **The expensive workflow is rarely the one they predicted**. The "**small**" feature turns out to dominate. The "**heavy**" feature is cache-friendly and cheap. **A small number of users account for most of the spend**.

The only way to get those insights is to **instrument early, instrument honestly, and resist the temptation to look at averages**.

This chapter is about **the instrumentation layer**. **What to log, how to slice it, which numbers belong on a dashboard, and which to ignore**.

---

## First principles

**You can't manage what you can't see**.

Tokens are different from CPU and memory. **A kernel-level view doesn't come for free**. The only entity that knows exactly how many tokens a request consumed is **the model provider**, and the only moment that information is available is in **the API response**. **If you don't capture it there, it's gone**.

The rule is simple: **every model call must produce a usage record**, and **every usage record must be persisted somewhere queryable**. **Not just logs, not just traces — a structured store you can group, filter, and aggregate**.

**Treat token usage the way the finance team treats invoices**. **You don't sample invoices**.

---

## The four token counts

Modern providers return multiple token counts. **Field names vary, but conceptually it's almost always four**:

```
┌──────────────────────────┬──────────────────────────────────────────────┐
│ field                    │ meaning                                       │
├──────────────────────────┼──────────────────────────────────────────────┤
│ prompt / input tokens    │ Fresh input you sent on this request.         │
│                          │ Billed at the standard input rate.            │
├──────────────────────────┼──────────────────────────────────────────────┤
│ cached tokens            │ Portion of input the provider served from a   │
│                          │ prefix cache. Deeply discounted.              │
├──────────────────────────┼──────────────────────────────────────────────┤
│ completion / output      │ Visible output the model generated.           │
│ tokens                   │ Billed at the output rate.                    │
├──────────────────────────┼──────────────────────────────────────────────┤
│ reasoning tokens         │ Hidden chain-of-thought the model generated   │
│ (when applicable)        │ before the visible answer. Billed as output.  │
└──────────────────────────┴──────────────────────────────────────────────┘
```

**Always log all four. Always.**

Why: **the aggregate "tokens used" count is meaningless for cost**. **Two requests with the same total token count can differ by 5–10× in real cost depending on how much was cached and how much was reasoning**.

If your usage logger only stores **a single integer**, you have **a logger that can't answer the questions that matter**.

---

## The unit you should use internally

Inside your own systems, **don't price in tokens**. **Price in cost**.

**Cost is the single comparable metric across requests, models, and tenants**. **Two requests with very different token shapes can have the same cost**; **two requests with the same total token count can have very different costs**.

The formula is straightforward:

```
cost = input_rate     × input_tokens
     + cached_rate    × cached_tokens
     + output_rate    × output_tokens
     + reasoning_rate × reasoning_tokens
```

**Compute it at log time, store it as a column, and use it as the denominator on every dashboard**. "Cost per request", "cost per user per day", "cost per resolved ticket" — **all answerable**. "Tokens per resolved ticket" is **not answerable**, because **it conflates four different things**.

> [!TIP]
> Store the **rates** that were in effect for the call **alongside the computed cost**, not just the cost. When rates change, you'll want to **re-derive historical numbers without losing the original record**.

---

## The per-X views

**A usage record without dimensions is a number you can't act on**. **Give each record enough metadata that the slices you actually need are possible**:

- **Per call**: a single API request. **The atomic unit**. This is what gets logged
- **Per turn**: one user-facing exchange. May contain multiple internal calls (tool steps, retrieval rounds, retries). In agents, one user message = a dozen calls
- **Per session**: full conversation. Useful for understanding **how cost grows with conversation length** (Chapter 9)
- **Per user**: account or end user
- **Per team / workspace**: the cost center that ultimately sees the invoice
- **Per task type**: codegen vs chat vs RAG vs classification vs background batch

The cheapest way to get all of these: **attach a small set of identifiers to each usage record at capture time** (call id, turn id, session id, user id, tenant id, task tag). **Trying to reconstruct joins from logs after the fact fails in subtle ways**.

---

## Observe the heavy tail

The **single most important fact** about production token usage: **it's not normally distributed**.

Across users, across sessions, across tasks — **the distribution is heavy-tailed**. **A small number of users (or sessions, or task types) consume most of the total cost**. **The mean is pulled up by the tail and is not representative of real users**.

**If you only look at average cost per user**, you'll **be confidently wrong** about almost everything: pricing, capacity planning, where to optimize, who to talk to.

Typical user-cost histogram:

```
users
  │
  │ █
  │ █
  │ █ █
  │ █ █ █
  │ █ █ █ █
  │ █ █ █ █ █
  │ █ █ █ █ █ █ █ █
  │ █ █ █ █ █ █ █ █ █ █  █  █     █                       █
  └──────────────────────────────────────────────────────────────►
    low                                                       high
                          cost per user per day

      ↑ most users live here       ↑ a thin tail lives here
        (the median)                 (and pays most of the bill)
```

**The mean of this distribution sits to the right of the bulk, in a region almost no real user occupies**. **If you quote the mean, you're describing a fictional user**.

What to quote instead:

- **Median**: the typical user. Honest about the bulk
- **p90**: heavier than 90% of users. Where "power users" begin
- **p95, p99**: where the tail lives. **Where the bill comes from**
- **Max**: the single highest user that day. Often surprising. **Sometimes a bug**

**A good dashboard shows median, p90, p99, and max side by side**. **The shape between them tells you more than any single number**.

---

## Metrics worth tracking in practice

A **small disciplined set of metrics** will get you far. **Resist the urge to track everything**.

### Cost per user per day
Track median, p90, p99. **Median = is the typical user getting more expensive over time?** **p99 = is the tail fattening?** — usually **the more urgent signal**.

### Cost per task / cost per correct answer
The **real productivity metric** discussed in Chapter 11. **Cost per task without quality is half the picture**; **cost per correct task is the whole picture**.

### Cache hit ratio
`cached_tokens / prompt_tokens`. **Direct measurement of whether prefix discipline (Chapter 12) is working**. A drop in the ratio = **something started invalidating the prefix** — usually a recent change to the system prompt or context-assembly path.

### Output / input ratio
A sudden increase here = often **a prompt regression toward verbosity** — someone added "explain your reasoning" or "be thorough" without considering cost.

### Reasoning ratio
`reasoning_tokens / output_tokens`. A sudden increase = often **a difficulty spike** (the workload got harder) or **a misconfigured reasoning-effort setting**. **Either is worth investigating**.

### Tool-call count per turn
**The cheapest early-warning signal in agent workflows**. **A high value almost always means the agent is looping** — same-tool retries, tool-to-tool oscillation, failure to converge.

**Six metrics**. **You don't need more on the front page**.

---

## Budgets, caps, and alerts

**Metrics tell you what happened**. **Budgets and alerts tell you when to act**.

A reasonable starting set:

- **Per-user soft cap**: a warning threshold that fires a notification (to the user, to you, or both) but **doesn't block**. Set at **roughly the p95 of healthy usage**. **Many will be false alarms**; **the true positives are what you want to see**
- **Per-user hard cap**: a blocking threshold, or a downgrade to a cheaper model / rate-limited tier. Set well above soft cap, **at a level where a single user could materially damage unit economics**
- **Per-team monthly budget with daily burn-rate alert**: if a team is on track to exceed its monthly budget by day 18, **you want to know on day 12, not day 30**. **Burn-rate alerts beat threshold alerts**
- **Anomaly alerts on percentile shifts**: p99 doubling overnight = **something changed** — a deploy, a new feature, a new use case. **The alert should tell you which dimension shifted**, not just "cost went up"

> [!IMPORTANT]
> **A hard cap that surprises a paying user is worse than the cost it saves**. **Always pair caps with clear messaging and an upgrade path**. **Cost control that erodes trust isn't cost control**.

---

## Sampling and PII

**Two streams, two policies**.

### Usage metadata
Token counts, cost, identifiers, latency, model id, cache hit ratio. **Log everything on every call. No sampling**. **This stream is small** (hundreds of bytes per call), **cheap to store, and indispensable**.

### Full prompt and response bodies
The actual text. **Log only when you have a clear and safe need**: debugging failed prompts, building eval sets, investigating quality regressions. **Keep retention short**. **Strip / redact sensitive fields**. **Respect the regulatory constraints that apply to your data** — many domains forbid storing user content beyond a narrow purpose, and **some forbid sending it to third parties at all**.

A mistake to avoid: **conflating the two streams**. Sampling the usage log because "**the body log is too big**" = **you've lost cost visibility to save on something that could have been stored separately and cheaply**.

---

## Telemetry hygiene

**Keep the cost & usage stream separate from your application trace stream**.

Application traces (spans, logs, performance metrics) are usually **aggressively sampled** in production. **That's fine for traces**; you don't need every span to understand latency. **But sampling cost data = irrecoverably losing money**. **A sampled invoice is a wrong invoice**.

Architecturally:

```
   ┌──────────────────┐         ┌────────────────────────┐
   │   model call     │────┬───►│  usage stream          │
   │                  │    │    │  (never sampled)       │
   │                  │    │    │  → cost warehouse      │
   │                  │    │    └────────────────────────┘
   │                  │    │
   │                  │    │    ┌────────────────────────┐
   │                  │    └───►│  trace stream          │
   │                  │         │  (sampled, short TTL)  │
   │                  │         │  → tracing backend     │
   └──────────────────┘         └────────────────────────┘
```

**The two streams can share infrastructure, but the policies should differ**. **The cost stream is a financial record**. **Treat it that way**.

---

## Going deeper

### Cost attribution in multi-tenant systems
If one app serves multiple customers, **every call needs to carry a tenant ID from the moment it leaves the client**. **Reconstructing tenant attribution from server logs after the fact is painful and often impossible**. **The right place is the request boundary**, and it should **propagate through all internal hops**.

### Detecting prompt regressions in CI
If you have a representative task suite, **run it on every change that touches a prompt or a context-assembly path**, and **record average tokens per task**. **Non-trivial changes in that number** (in either direction) **are signals worth reviewing**. Someone added a paragraph to the system prompt and input tokens per task jumped 30%? — **you want to catch that before it ships**. **The cheapest token-saving control you can install**.

### Effective rate per million tokens
A useful proxy metric for cache health: **total cost ÷ total input tokens**, expressed per million. **As cache hit ratio improves, this number drops**, even if input volume grows. **As it degrades** (e.g. after a prompt change that invalidates the prefix), **the number jumps**. **A single, blunt view, tracked over time, of whether you're getting more or less efficient on the same workload**.

### Rate-limit telemetry
Not strictly cost, but adjacent. **If you log which calls were throttled, retried, or rejected, you can correlate cost spikes with provider-side pressure**, and **distinguish "spending more because doing more" from "spending more because retrying"**.

---

## FAQ

**Q1.** "Isn't the provider's dashboard enough?"  
A. Aggregated, delayed, and not granular. **Can't slice by your dimensions (tenant, feature, user)**. **Your own store is mandatory**.

**Q2.** "Isn't logging every call heavy?"  
A. A usage record is hundreds of bytes. Even at millions of calls per month, that's GB-scale. **Storage is cheap; lost visibility is expensive**.

**Q3.** "How do I resist the urge to look at averages?"  
A. **Don't put averages on the dashboard**. Show only median, p90, p99, max. **What's not visible doesn't get cited**.

**Q4.** "Cost calculation is complicated when models change."  
A. **Codify the rate table** and snapshot it at log time. When you swap models, just update the table.

**Q5.** "Should I log prompt bodies too?"  
A. Useful for debugging and eval-building. **Short retention, redacted, sampling OK** in a separate stream.

---

## Recap

- You can't manage what you can't see. Capture **a usage record on every call, in a structured store, with no sampling**
- **Always log four token counts** — fresh input, cached input, visible output, hidden reasoning. **A single "tokens used" number hides the cost mix**
- **Internally price in cost, not tokens**. Compute and store cost at log time
- **Make every record sliceable per call / turn / session / user / team / task type**
- **Token usage is heavy-tailed**. **Averages mislead**. **Lead with median, p90, p99, max**
- Track a **small disciplined set**: cost per user, cost per correct task, cache hit ratio, output/input ratio, reasoning ratio, tool-calls per turn
- Pair with **soft caps, hard caps, monthly budgets with burn-rate alerts, percentile-shift anomaly alerts**
- **Separate the cost stream from the trace stream**. Sample the latter freely; **never sample the former**
- **Watch tokens-per-task averages in CI** as a regression signal for prompt changes

---

## Exercises

**Exercise 13.1** (15 min)  
Add code to one endpoint of your app that logs **the four token counts + cost + identifiers**.

**Exercise 13.2** (10 min)  
From the past week's usage logs, compute **median, p90, p99, max cost per user**. **What's the mean-to-median ratio**? How heavy is your tail?

**Exercise 13.3** (challenge)  
Build **a CI job that includes prompt changes** and measures **average tokens per task** on a representative suite. **Alert on a ±20% change**.

---

## On to the next chapter

When spend is **clearly visible**, the **patterns that waste it become obvious**. The next chapter catalogs the most common ones — **the anti-patterns and pitfalls that a healthy monitoring setup will surface**, and **how to recognize them before the bill tells you**.

→ [Chapter 14 — Anti-patterns and pitfalls](15-anti-patterns)
