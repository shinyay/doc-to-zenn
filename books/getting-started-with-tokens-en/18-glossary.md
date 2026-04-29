---
title: "Appendix A — Glossary"
---

> **In one line:** All the terms used throughout this book, **alphabetically**, with **a short definition + which chapter covers it in depth**. **Use this as a reference to come back to as you read**.

---

## A

**Agent** — A loop-style workflow where the model plans → calls tools → observes → iterates. **The most expensive mode**. Use only when the task warrants it. → Chapter 16

**Anti-pattern** — A structural failure that, despite being framed as "cost optimization", produces a worse outcome. → Chapter 14

**Attention** — The core mechanism in Transformers. Each token "talks to" every other token. **Cost ∝ length²**. → Chapter 8

---

## B

**BPE (Byte Pair Encoding)** — The most common subword tokenization algorithm. **Iteratively merges the most frequent pairs**. Widely used in GPT and Llama families. → Chapter 3

**Bytes per token** — Bytes per token of text. **A metric that varies hugely by language and script**. → Chapter 4

---

## C

**Cache (prompt cache / prefix cache)** — A mechanism that reuses the processing of common leading token sequences. **Stable-prefix design enables dramatic savings**. → Chapter 12 / Chapter 13

**Compaction** — Summarizing/compressing past history in long conversations. **Comes with irrecoverable information loss**. → Chapter 10

**Context window** — The maximum number of tokens the model can "see" in one request. **A budget, not a feature**. → Chapter 6

**Context scoping** — The discipline of replacing always-on instructions sent on every request with workflow-conditional, on-demand loading. → Chapter 16

---

## D

**Decode** — The phase that **generates tokens one at a time, sequentially**. **Latency depends on both input and output length**. → Chapter 8

**Distillation** — Training a small model on a large model's outputs. **Quality reinforcement when moving across tiers**. This book mentions the concept in passing; there is no dedicated chapter.

---

## E

**Embedding** — A **learned vector representation** of a token ID. It's the **initial representation that later transformer layers operate on**, not "the meaning of a word" in any literal sense — better thought of as "a geometric position assigned to each token through training". Note that it lives at the **subword / token level**, not at the word level. → Chapter 3

---

## F

**Few-shot prompting** — Including a small number of input/output examples in the prompt to show the model a pattern. **Each example consumes hundreds of tokens**. → Chapter 10

**Function calling** — A mechanism where the model returns structured JSON to invoke a tool. **The schema is sent on every request**. → Chapter 10 / Chapter 14

---

## G

**Greedy decoding** — A simple decode strategy that picks the highest-probability token at each step. Deterministic but no diversity.

---

## H

**Hidden consumer** — Elements (system prompt, tool schemas, history, RAG context, etc.) that consume the context window before the user message even arrives. → Chapter 10 / Chapter 11

**Hygiene** — Not individual tricks, but **a set of principles that, observed continuously, stabilize cost and quality**. → Chapter 12

---

## I

**Input tokens** — Tokens sent to the model. **Usually cheaper than output tokens**. → Chapter 7 / Chapter 9

---

## J

**JSON mode** — A model/provider feature that **constrains output to be valid JSON**. It guarantees "the output will parse as JSON"; **strict conformance to a specific schema is a separate mechanism** (structured outputs / JSON schema enforcement / function calling, etc.). Helps with **reduced output volume and reliable downstream parsing**. → Chapter 16

---

## K

**KV cache (Key-Value cache)** — An internal cache that holds attention's intermediate values per token. **Size is proportional to context length**, and pressures GPU memory in long conversations. → Chapter 8

---

## L

**Latency** — Time from request send to response complete. Composed of **TTFT + output length × per-token time**. → Chapter 8

**LLM (Large Language Model)** — Large language model. The subject of this entire book.

---

## M

**MCP (Model Context Protocol)** — A standard protocol for exposing external tools and data sources to the model. **Dead weight on every request if the catalog is unused**. → Chapter 14

**Mental model** — The view that internalizes tokens as "the unit of billing", "the unit of thought", and "the unit of budget". The goal of this entire book.

**Model tiering** — A strategy of routing easy tasks to cheap models and hard tasks to high-capability models. **The price gap between tiers is usually an order of magnitude or more**. → Chapter 16

**MTok** — Million Tokens (1,000,000 tokens). The standard unit on provider price tables.

---

## N

**Normalization** — Pre-tokenization text preprocessing (lowercasing, Unicode NFC, etc). **Differs subtly per vendor and affects reproducibility**. → Chapter 3

---

## O

**Output tokens** — Tokens the model generates. **Usually more expensive than input, and dominate latency**. → Chapter 7 / Chapter 9

---

## P

**Prefill** — The phase that **processes the entire input in parallel at once**. **Cost is proportional to input length**, and latency manifests as TTFT. → Chapter 8

**Prompt compression** — The art of saying the same intent in fewer tokens. **Declarative > imperative**, removing politeness padding, etc. → Chapter 16

---

## Q

**Quantile** — A metric viewed via **p50/p95/p99**, not means. **Essential for capturing heavy tails**. → Chapter 13

---

## R

**RAG (Retrieval-Augmented Generation)** — A technique that injects external search results into the prompt to improve answer accuracy. **Over-pulling is the canonical cost driver from Chapter 10**.

**Reasoning tokens** — Tokens the model generates internally during its "thinking" process. **Invisible to the user but may still be billed**. → Chapter 7

---

## S

**Sampling parameters** — Dials that control decode strategy: temperature, top-p, top-k, etc. **Touch only after the structural work**. → Chapter 16

**Subword** — A tokenization unit smaller than a word and larger than a character. BPE, WordPiece, SentencePiece are representatives. → Chapter 3

**System prompt** — Instructions injected at the head of every request, persistently. **The biggest "hidden consumer" candidate**. → Chapter 10 / Chapter 11

---

## T

**Throughput** — The volume of tokens processed per unit time. **Depends on batch size and KV cache**. → Chapter 8

**Tokenizer** — A converter between text and token IDs. **Differs per vendor, not interchangeable**. → Chapter 3

**TTFT (Time To First Token)** — Time from request send to the arrival of the first output token. **Dominated by prefill time**. → Chapter 8

---

## U

**Unicode** — A character encoding standard. **One character can be 1–4 bytes and 1 to several tokens**. → Chapter 4

---

## V

**Vocabulary** — The full set of tokens the tokenizer recognizes. Usually tens of thousands to over a hundred thousand. **Out-of-vocab** is decomposed into subwords. → Chapter 3

---

## W

**Workflow mode** — The 3 modes ask / edit / agent. **The same outcome can cost 5–25× more depending on the mode**. → Chapter 16

---

## Note: terms **deliberately avoided** in this book

- **Specific vendor prices** ("$/MTok") — the book's stance: numbers change, structures don't
- **Specific model spec** ("model X has a window of N tokens") — same
- **Recommended values for specific parameters** ("temperature=0.7 is best") — structural work first

---

## On to the next chapter

→ [Appendix B — Quick reference](19-quick-reference)
