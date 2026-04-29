---
title: "Chapter 5 — Counting tokens"
---

> **In one line:** Every cost you care about (money, latency, context budget) starts with a **token count**. So you need three tools — **exact** (in code), **approximate** (in browser), and **mental** (rule of thumb).

---

## Why this chapter exists

After four chapters of "what tokens are" and "how they vary by language", we shift to **practice**. The first practical question:

> Can you immediately answer **"how many tokens is this text?"**

If not, you can only **guess** at bills, latency, and the context window. This chapter equips you with three measurement modes (exact / approximate / mental) plus a **budgeting workflow** usable for any prompt.

---

## Why count

Every meaningful LLM constraint is **denominated in tokens**:

- **Money**: input × rate + output × rate
- **Latency**: roughly proportional to (input tokens + output tokens)
- **Context window**: hard ceiling. Crossing it = request fails or older content silently dropped

Without counting, all of these are **vibes**. Vibes calibrated on English prose are **orders of magnitude off** for code, JSON, and non-Latin text (Chapter 4).

The question is not *whether* to count, but **at what fidelity**.

---

## Three measurement modes

```
   Exact            Approximate         Rule-of-thumb
 ┌────────┐       ┌──────────┐         ┌────────────┐
 │  code  │ ───▶ │  web tool │  ────▶ │  mental    │
 │tokenizer│      │  browser  │        │  napkin    │
 └────────┘      └──────────┘         └────────────┘
   slow,            fast,                instant,
   precise          mostly right         rough
```

Match decision weight to mode:

- **Production cost estimate** → **Exact**
- **Sanity-check a draft prompt** → **Approximate**
- **Whiteboard architecture sketch** → **Rule of thumb**

---

## Mode 1: Exact (in code)

Encode with the model's **actual tokenizer** and take the length. **Trust nothing else for money / latency / context-limit decisions**.

Recap from Chapter 3: each model family has its own vocab. **Wrong tokenizer = 10–30% error**. First question is always: **"Which tokenizer matches the model I'm actually calling?"**.

### Python — `tiktoken` (OpenAI family)

```python
import tiktoken

text = "How many tokens is this sentence?"

# Resolve from the model name (library maps to correct vocab)
enc = tiktoken.encoding_for_model("gpt-4o")

token_ids = enc.encode(text)
print(len(token_ids))    # the count you want
print(token_ids[:10])    # integer IDs (handy for debugging)

# Visualize how it split
for tid in token_ids:
    print(f"{tid:6d} -> {repr(enc.decode([tid]))}")
```

Notes:
1. Pass the **model name**, not the tokenizer — re-resolve when you switch models
2. `encode` returns a list of integer IDs; count is `len(...)`. Decoding individual IDs trains intuition for **where it split**

### Python — Hugging Face `transformers` (open-weight family)

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")
# Authenticated repos: set HF_TOKEN env var

token_ids = tokenizer.encode("How many tokens is this sentence?")
print(len(token_ids))
```

`AutoTokenizer` figures out BPE / WordPiece / SentencePiece and returns a uniform interface. Important flags:

- `add_special_tokens=False` — don't include `<bos>`, `<eos>`; **count just the body**
- `return_tensors=None` (default) — Python list (what you want for counting)

### JavaScript / TypeScript

Browser or Node:

```ts
// 1. js-tiktoken (GPT family JS port)
import { encodingForModel } from "js-tiktoken";
const enc = encodingForModel("gpt-4o");
console.log(enc.encode("How many tokens is this sentence?").length);
```

```ts
// 2. gpt-tokenizer (zero deps, vocab bundled)
import { encode } from "gpt-tokenizer";
console.log(encode("How many tokens is this sentence?").length);
```

```ts
// 3. @anthropic-ai/tokenizer (Claude approximation — note: not official)
import { countTokens } from "@anthropic-ai/tokenizer";
console.log(countTokens("How many tokens is this sentence?"));
```

Same pattern as Python: load tokenizer matching model → encode → length.

### When the provider doesn't publish a local tokenizer

Anthropic Claude and Google Gemini, for example, **don't publish their tokenizer**. Official routes:

- Call the API's **`count_tokens` endpoint** if available
- Otherwise call with a minimal prompt and read `usage.input_tokens`

```python
# Anthropic example
import anthropic
client = anthropic.Anthropic()

count = client.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello, world."}],
)
print(count.input_tokens)
```

```python
# OpenAI — read usage
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=1,
)
print(resp.usage.prompt_tokens, resp.usage.completion_tokens)
```

> [!NOTE]
> API-based counting **consumes real tokens**. For repeated CI checks of prompt size, **prefer a local tokenizer** when one exists. API is the last resort.

---

## Mode 2: Approximate (web tools)

Major providers and tokenizer projects publish web pages where you paste text and see colored splits + counts:

- OpenAI: `https://platform.openai.com/tokenizer`
- HuggingFace: `https://huggingface.co/spaces/Xenova/the-tokenizer-playground`
- Tiktokenizer: `https://tiktokenizer.vercel.app/`

**Use when**:
- Sanity-checking a hand-written prompt
- Exploring emoji / code / mixed-script behavior
- No local dev environment

**Don't use when**:
- At scale (you can't paste 1000 prompts in sequence)
- **Input contains confidential data** (text leaves your machine)
- Model is closed and not hosted there

**A microscope, not a measuring tape**.

---

## Mode 3: Mental (rule-of-thumb)

For napkin math — sizing a feature, judging "this context blob feels too big", comparing design options — exact numbers aren't needed. **±30% is fine**.

| Content type | Rough density | Equivalent |
|--------------|---------------|------------|
| English prose | ~4 chars/token | ~0.75 tokens/word |
| Source code | ~3 chars/token | denser than prose |
| JSON, XML, quote-heavy | ~2–3 chars/token | even denser |
| CJK | 1–3 tokens per char | many tokens per char |
| Other complex scripts | wildly varies | **always measure** |

Concrete feel:
- 200-word English email → ~150 tokens
- 1,000-char JS function → 300–350 tokens
- 1,000-char nested JSON → 400–500 tokens
- 200-char Japanese paragraph → 200–600 tokens (tokenizer-dependent)

> [!WARNING]
> **"1 token ≈ 4 chars"** is the most-cited and **most-misused** number in the LLM world. It's for **English prose under a specific tokenizer family**. Apply it to code / JSON / non-Latin text and you'll be **massively under-budgeted**. Calibrate any new input type with one real measurement.

---

## Counting **conversations**, not just strings

So far we counted **plain text**. Real prompts are **templated**.

In chat APIs, each message is wrapped in role markers and delimiters:

```
<start>system
You are a helpful assistant.
<end>
<start>user
What's the capital of France?
<end>
<start>assistant
```

**The wrapping is invisible but real and counted**. Even a short 2-turn conversation pays **dozens of scaffolding tokens** with "no content".

Rule: **tokenize the templated prompt, not raw messages**.

```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B-Instruct")
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "What's the capital of France?"},
]
templated = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
ids = tok.encode(templated, add_special_tokens=False)
print(f"Templated tokens: {len(ids)}")
```

OpenAI's docs include `num_tokens_from_messages()` (overhead coefficient varies by model version).

### Tool / function definitions are also counted

When you give the model an available-tools list, **each tool definition (name, description, parameter schema, all nesting) gets serialized into the prompt and tokenized**.

The user doesn't see it. Chat UI doesn't show it. **But every turn pays for it**.

A handful of richly-described tools can consume **more tokens than the user's actual question**. Chapter 10 details.

---

## Budgeting the output

Input is measurable up front. **Output is not** — by definition, it hasn't been generated yet.

Instead, set an **upper bound** with `max_tokens` (or `max_output_tokens`):

```python
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    max_tokens=500,   # cut at 500 tokens
)
```

Important properties:
- **Most providers bill on actual generated count**, not the cap
- The cap is a **safety net, not a target**. Models usually stop earlier
- Too-low cap = **truncated answers**. Size for the **longest reasonable response**, not the average

For estimation, assume "uses half to all of the cap" for safety.

---

## Budgeting workflow

A flow usable for nearly any prompt — one-shot script through long-running agent:

```
┌─────────────────────────────────────────────────┐
│ 1. Context window ceiling                       │  (model property)
│        −                                        │
│ 2. Safety margin (~10–20%)                      │  (your choice)
│        −                                        │
│ 3. Expected output cap                          │  (max_tokens)
│        =                                        │
│ 4. Input budget                                 │
│                                                 │
│ 5. Measure / estimate input tokens              │
│        Over budget → trim, summarize, paginate  │
└─────────────────────────────────────────────────┘
```

Step by step:

1. **Ceiling**: look up the actual model's context window. Treat as a **hard wall**
2. **Safety margin**: take 10–20% off the top — covers chat-template overhead, tool definitions, measurement error. **Headroom is cheaper than crashing into the wall**
3. **Output cap**: pick the max acceptable response length and reserve it; otherwise long answers **eat the input space mid-conversation**
4. **Input budget**: what's left for system prompt + history + retrieval context + user message **combined**
5. **Measure**: tokenize the templated prompt (Mode 1) or estimate (Mode 3). If over, cut something — Chapter 13 covers what

Looks obvious on paper, but most production prompts skip step 2 and **discover the margin's existence by failing**.

### Budget check in CI

A "does this prompt template fit the input budget" CI check is one of the **highest-ROI guardrails**:

```python
# tests/test_prompt_budget.py
import tiktoken
from myapp.prompts import build_system_prompt, build_tools_schema

MAX_INPUT_BUDGET = 6000  # context window − safety − output reservation

def test_system_prompt_within_budget():
    enc = tiktoken.encoding_for_model("gpt-4o")
    sys_tokens   = len(enc.encode(build_system_prompt()))
    tools_tokens = len(enc.encode(build_tools_schema()))
    static_total = sys_tokens + tools_tokens

    assert static_total < MAX_INPUT_BUDGET * 0.5, \
        f"Static prompt overhead too large: {static_total} tokens (>50% of budget)"
```

A threshold like "static system + tool definitions must not exceed half the budget" catches quality regressions before deploy.

---

## Going deeper

### Tokens are not network bytes
The JSON wrapping of an API request (`"role"`, `"content"` keys, braces, indentation) is **not tokenized, not billed**. Only the **values** that reach the prompt are counted.

Network-bandwidth measurements show numbers far larger than the billed token count. **That gap is normal** and not worth chasing.

### Whitespace and normalization differ across implementations
Different tokenizers handle leading whitespace, runs of whitespace, and newlines differently. Some absorb leading space into the next token; some make it its own token; some strip.

Implication: **don't compare token counts across tokenizers**. "1,000 tokens" only has meaning **for a specific model**.

### Chat templates differ by model family
Two models on the same tokenizer can use **different role markers and delimiters**. Same message list = different templated counts.

Switch model family → **re-measure templated prompts**. Counts are not portable.

### Cache the count
The **static parts** of a prompt (system instructions, tool definitions, few-shot examples) don't need re-tokenization on every request:

```python
class PromptCounter:
    def __init__(self):
        self.enc = tiktoken.encoding_for_model("gpt-4o")
        self._static = len(self.enc.encode(build_system_prompt()))
        self._tools  = len(self.enc.encode(build_tools_schema()))

    def total(self, dynamic_text: str) -> int:
        return self._static + self._tools + len(self.enc.encode(dynamic_text))
```

At millions of calls, **repeated tokenization of static parts is real cost**. Count once at startup.

### Special-token on/off
`tiktoken.encode` has `disallowed_special`. Default rejects user input that contains `<|endoftext|>`-class tokens (prompt-injection defense):

```python
enc.encode(text, disallowed_special=())  # allow all (only for trusted input)
```

For user-supplied input, **keep the default** to block special-token injection.

---

## FAQ

**Q1.** "Isn't `chars / 4` enough?"  
A. Only for English prose. Japanese, code, JSON are **off by an order of magnitude**. Always calibrate the first time on a new input type.

**Q2.** "Reuse a tokenizer across models?"  
A. **No**. Family-specific vocab. Measuring Claude with GPT-4's `tiktoken` can be off by 20%+.

**Q3.** "Is `tiktoken` a production latency bottleneck?"  
A. Negligible. μs-order Rust. Dust compared to the LLM call itself (hundreds of ms to seconds).

**Q4.** "Re-count the entire history every turn?"  
A. **Incremental counting** suffices — tokenize only the new message and add to the running total.

**Q5.** "How do I predict output token count?"  
A. **You can't** (have to generate). But you can statistically learn output-length distributions for similar past tasks and produce **interval estimates**. Log `usage.completion_tokens` in production and model later.

---

## Recap

- Measurement is the foundation. **An unmeasured budget cannot be managed**
- Match mode to decision weight: production = code, sanity = web, design = mental
- Rules of thumb are tokenizer-dependent. **"1 token = 4 chars"** is English-prose only
- Measure the **templated prompt** — including chat role markers and tool definitions
- **Output is not measurable up front**. Cap with `max_tokens`; budget = window − safety − output reservation
- **Cache** static-part counts; only add dynamic part each call

---

## Exercises

**Exercise 5.1** (5 min)  
Copy a recent Slack DM and count it with both `cl100k_base` and `o200k_base`. Difference?

**Exercise 5.2** (10 min)  
Build the **templated prompt** of system + tools + a typical user message and count it. **What % is the tools schema**?

**Exercise 5.3** (CI challenge)  
Wrap the above in a pytest test with a threshold (e.g. static fixed cost < 2000 tokens). Fails the build on unintended bloat.

---

## On to the next chapter

You can count. The next question: **what are you counting against?** The hard ceiling that all your prompts, history turns, and retrieval docs must fit under. That's **the context window**.

→ [Chapter 6 — The context window](07-context-window)
