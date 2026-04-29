---
title: "Closing column — Your next step: tokopt"
---

> **In one line:** The **fluency in tokens** you gained from this book **only becomes valuable when used in real work**. **Manual audits matter**, but **sustaining them needs tools**. This closing column is a **preview note** that **those tools will be covered in a separate article**.

---

## Thank you for reading this far

What tokens are, where they're born, where they vanish, and what they cost — across **17 chapters and 2 appendices**, we walked together with the perspective that **"numbers change, structure doesn't"**.

The goal of this book was never to make you an **"optimization expert"**. It was to give you **fluency in the unit**. **That fluency is the prerequisite to read every optimization technique, benchmark, and new model coming next with the right amount of skepticism and the right amount of enthusiasm**.

That fluency is now inside you.

---

## From here on — the "execution" story

This book was **reading**, but **optimization is execution**. At the end of Chapter 16 we proposed three actions:

1. **Run a token audit on one project**
2. **Apply one lowest-effort family (output control), measure next week**
3. **Go back to Chapters 9–14 when you suspect a regression**

You can do these **by hand**. In fact, **the first time we strongly recommend doing it by hand** — to internalize the feel of the metrics.

That said, when you reach the **continuation** stage, different problems show up:

- **No time to run an audit weekly**
- **You need a mechanism to detect "drift before you noticed"**
- **You want the same discipline shared across the whole team**
- **You want it on CI to auto-detect regressions**

This is where **tools** come in.

---

## About tokopt (preview only)

The author is preparing **`tokopt`**, a **toolkit for running the discipline discussed in this book in real work**. It will be covered **in a separate article** as a sister piece to this book.

**Why we did not write tokopt details in this book**:

- This book's **protagonist is "tokens themselves"**, not a specific tool
- Tools evolve. **The structural arguments in this book want to remain robust to changes in numbers and tools**
- We want to avoid the failure mode of **"tool first, discipline later"** — having read this book, **you should now be able to say what a tool needs to solve, in your own words**

We're keeping it as a preview because we want to **prioritize you actually moving your hands first**.

---

## What you can do until then

Without waiting for the `tokopt` article, things you can **start today**:

| Action | Time required | What you need |
|--------|---------------|---------------|
| **Measure your main project's system prompt with `tiktoken`** | 10 min | Python + `tiktoken` |
| **Print Appendix B's cheat sheet and stick it on your desk** | 5 min | Printer |
| **Make a spreadsheet recording Chapter 13's 4 metrics weekly** | 30 min | Spreadsheet |
| **Put a "quarterly audit" on the team calendar** | 5 min | Calendar |
| **Start a reading club going through this book one chapter at a time with colleagues** | 30 min/chapter | Colleagues |

These can all **start without tools**, and **slot in cleanly when a tool arrives**.

---

## Finally — the book's stance, one more time

This book was written from **first principles**. **Memorize the structure that survives price changes, not the price tables. Hold the questions you can ask of any model, not praise for a specific one. Learn to read benchmarks, not chase the latest one.**

Numbers will change. Models will change. **Today's SOTA being obsolete in six months** is the norm in this field.

Even so, **tokens won't disappear**. **Neither will the context window, the asymmetry between prefill and decode, the quadratic cost of attention, the bending relationship between cost and quality, the existence of hidden consumers**. **Nor will the value of disciplined measurement**.

As long as those don't disappear, **the perspective you built in this book will serve you for many years**.

**Spend wisely. And enjoy yourself.**

---

## Appendix: this book's chapter map (reprise)

```
Chapter 1     What is a token ("why this unit")
Chapters 2–5  What:    the substance, generation, language differences, measurement
Chapters 6–9  Where:   context window, cost, performance, places of consumption
Chapters 10–11           hidden consumers
Chapter 12    Quality vs cost
Chapters 13–14           measuring / anti-patterns
Chapter 15    Why optimize
Chapter 16    Roadmap (3 moves + 7 families)
Appendix A    Glossary
Appendix B    Quick reference
This chapter  Next step: tokopt preview
```

---

## A finishing mark

Thank you, truly, for reading this far. **If this book becomes the foundation of your "token sense"**, that will be the highest happiness for the author.

Comments, questions, and corrections are warmly welcome anytime — via Zenn comments or GitHub Issues.

— **End of book** —
