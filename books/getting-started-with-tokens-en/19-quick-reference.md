---
title: "Appendix B — Quick reference"
---

> **In one line:** This book's 17 chapters + Appendix A **compressed onto a single page**. **A cheat sheet to come back to during real work and use as a decision filter**.

---

## 1. The 3 moves

> **Every optimization is a disguise of one of three**

| # | Move | Typical examples |
|---|------|------------------|
| 1 | **Send less** | Trim system prompt, context scoping, summarize history, drop unused tools |
| 2 | **Receive less** | Terse instructions, fixed JSON schema, no preamble, length cap |
| 3 | **Pay less per token** | Cheaper model tier, prefix-cache design, matching workflow mode |

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

## 3. The 10 hygiene principles (Chapter 12)

```
1.  Justify every token              if you can't ask "why is this here?", it's a deletion candidate
2.  Most stable thing first          maximize cache hit
3.  Volatile content last            don't break the stable prefix
4.  Declarative > Imperative         "Output: JSON" beats "Always make sure to use JSON..."
5.  Aggregate repetitions            don't write the same intent in 3 places
6.  Periodically delete dead rules   instructions for scenarios that don't happen are dead weight
7.  Scope and load tools             don't expose all tools to all workflows
8.  Summarize history → cut it       old turns are worth cutting even when irrecoverable
9.  Measure before you touch         decide on metrics, not guesses
10. Sustain the discipline           a one-off cleanup drifts in 3 months
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
