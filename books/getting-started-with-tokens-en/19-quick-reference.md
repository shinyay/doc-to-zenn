---
title: "Appendix B — Quick reference"
---

> **In one line:** This book's 16 main chapters + Appendix A **compressed onto a single page**. **A cheat sheet to come back to during real work and use as a decision filter**.

---

## 1. The 3 moves

> **Every optimization is a disguise of one of three**

| # | Move | Typical examples |
|---|------|------------------|
| 1 | **Send less** | Trim system prompt, context scoping, summarize history, drop unused tools |
| 2 | **Receive less** | Terse instructions, fixed JSON schema, no preamble, length cap |
| 3 | **Pay less per token** | Cheaper model tier, prefix-cache design, task-appropriate model routing |

---

## 2. The 7 technique families — adoption order

| Order | Family | Effort | Impact |
|-------|--------|--------|--------|
| 1 | **Output control** | Very low | High |
| 2 | **Context scoping** | Low–medium | High |
| 3 | **Prompt compression** | Medium | Medium |
| 4 | **Model tiering** | Medium | High |
| 5 | **Caching discipline** | Low | High (with stable prefix) |
| 6 | **Tool / MCP discipline** | Low | Medium |
| 7 | **Workflow choice** | Continuous | High per decision |

**Rule**: Don't start from parameter dials (temperature etc.). **Structural work first**.

---

## 3. Hygiene checklist (the 10 principles from Chapter 12)

```
1.  Stable prefix, volatile suffix        stable up front, volatile at the end
2.  Load on demand, not always-on          send things only when they're relevant
3.  Declarative > Imperative               "Output: JSON" beats "Always make sure to use JSON..."
4.  Output discipline                      explicitly constrain output length
5.  Minimum sufficient context             just enough context, not more
6.  Right-size the model                   pick the model tier that matches the task
7.  Right-size the reasoning effort        match reasoning effort to task difficulty
8.  End sessions on topic change           cut the session when the topic shifts
9.  Treat tools as inventory               manage the tool surface like inventory
10. Measure before optimizing              decide on metrics, not on guesses
```

---

## 4. 14 anti-patterns at a glance (Chapter 14)

| Category | Anti-pattern |
|----------|-------------|
| Prompt | Politeness padding / same instruction 3× / leftover dead rules |
| Context | All-workflow instructions in one file / RAG over-pulling |
| Tools | Unused MCP connections left attached / duplicate tool definitions |
| Model | Everything on the top tier / no router |
| Workflow | Agent loop on a one-shot question / agent task done as ask |
| Metrics | Looking only at the mean / not bucketing |
| Cache | Volatile tokens at position 1 / per-user variables at the head |

---

## 5. The 4 token counts to measure (Chapter 13)

```
┌──────────────┬─────────────────────────────────────────┐
│ Input        │ The whole prompt (incl. hidden consumers)│
│ Output       │ What the model generated                 │
│ Reasoning    │ Internal thought (billed by some vendors)│
│ Cached       │ Prefix-cache hit portion (discounted)    │
└──────────────┴─────────────────────────────────────────┘
```

**Stats to look at**: mean ❌ → **p50 / p95 / p99** ⭕

---

## 6. Quarterly token-audit checklist (Chapter 16)

```
□ 1. Pull last quarter's metrics
□ 2. Identify the top 3 cost drivers
□ 3. Re-read the system prompt aloud
□ 4. Tool list — delete anything unused for 90 days
□ 5. Re-check model tier vs task difficulty
□ 6. Verify cache-friendly prefix structure
□ 7. Record one experiment for next quarter
```

---

## 7. "Which chapter to come back to when stuck" map

| Symptom | Go back to |
|---------|-----------|
| I don't understand why my input keeps growing | **Chapter 10 / Chapter 11** (hidden consumers) |
| I lowered cost and quality dropped | **Chapter 12** (quality vs cost) |
| I don't understand what my metrics are saying | **Chapter 13** (measuring) |
| Something feels like "an optimization that lost me money" | **Chapter 14** (anti-patterns) |
| Is optimizing even worth it? | **Chapter 15** (why optimize) |
| Where do I even start? | **Chapter 16** (roadmap) |

---

## 8. Editorial discipline (this book's stance)

- ❌ Don't write specific vendor prices
- ❌ Don't write specific model spec
- ⭕ Write in "3–5×", "~1/10", "in orders of magnitude"
- ⭕ **Numbers change. The structure doesn't.**

---

## On to the next chapter

→ [Closing column — Your next step: tokopt](20-next-step-tokopt)
