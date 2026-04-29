---
title: "Chapter 3 — Tokenization algorithms"
---

> **In one line:** A tokenizer = **algorithm + trained vocabulary**. There are really only **3 algorithms** (BPE / WordPiece / Unigram); `SentencePiece` and `tiktoken` are **toolkits / implementations**, not new algorithms. This is why the same text gives different token counts on different models.

---

## Why this chapter exists

Chapter 2 established that tokens are subwords. The next natural question: **who decides those subwords?**

"BPE", "WordPiece", "SentencePiece", "tiktoken" — the term soup is confusing, but **once organized it's surprisingly simple**. This chapter draws the map.

You don't have to implement any of these. Knowing **the shape of the mechanism** makes counting (Ch5), budgeting (Ch6), and optimizing (Ch16+) much clearer.

---

## The four names you'll hear

Almost every modern LLM falls into one of these:

| Name | Kind | One-liner |
|------|------|-----------|
| **BPE** | Algorithm | Start small; iteratively **merge** the most frequent adjacent pair |
| **WordPiece** | Algorithm | BPE-cousin; selects by **likelihood** instead of raw frequency. BERT family |
| **Unigram** | Algorithm | **Reverse direction** — start large, **prune** low-contribution entries |
| **SentencePiece** | Toolkit | Implements both BPE and Unigram; treats whitespace as a normal character (CJK / code friendly) |

You'll also hear `tiktoken` — **not a new algorithm**. It's the GPT-family **byte-level BPE in a fast Rust implementation**.

So the three algorithms to actually remember: **BPE, WordPiece, Unigram**. The rest is implementation detail.

```
                    ┌─── BPE ────────┬─ tiktoken (GPT family)
       Algorithm ───┤                ├─ SentencePiece-BPE
                    │                └─ Hugging Face tokenizers
                    │
                    ├─── WordPiece ──┬─ BERT family
                    │                └─ DistilBERT / ELECTRA
                    │
                    └─── Unigram ────┬─ T5 / mT5
                                     └─ SentencePiece-Unigram
```

---

## 1. BPE (Byte-Pair Encoding)

The simplest and most widely deployed. GPT-family, LLaMA-family, Mistral-family — virtually all frontier LLMs use BPE-family. **Understand BPE and 70% of the tokenizer landscape is done**.

### Training procedure (5 steps)

```
1. Pick target vocabulary size V (e.g., 50,000)
2. Initial vocab = all characters (or bytes 0–255)
3. Pre-split the corpus into words; break each word into character sequence
4. Count occurrences of every adjacent pair in the corpus
5. Merge the most frequent pair → add as new token to vocab → rewrite corpus
   → go to step 4 while |vocab| < V
```

**"Greedy: merge the most frequent pair every round."** That's the entire algorithm.

### Hand walkthrough

Forget about target size; just run it. Corpus:

```
low      ×5
lower    ×2
newest   ×6
widest   ×3
```

Decomposed (`_` = end-of-word marker):
```
l o w _              ×5
l o w e r _          ×2
n e w e s t _        ×6
w i d e s t _        ×3
```

Initial vocab: `{l, o, w, e, r, n, s, t, i, d, _}` (11 entries)

#### Merge 1
Count adjacent pairs:
- `e s`: newest×6 + widest×3 = **9**
- `s t`: newest×6 + widest×3 = **9**
- `l o`: low×5 + lower×2 = **7**

Tiebreak alphabetically → merge `e s`. New token: `es`.

#### Merge 2
Now `es t` count = 9. Merge → `est`.

#### Merge 3
`est _` count = 9 → `est_`.

#### Merge 4
`l o` count = 7 → `lo`.

After enough merges:
```
low_     ×5    ← single token
lower_   ×2
newest_  ×6   ← single token
widest_  ×3
```

In other words, **frequent words in the training corpus become single tokens**. Less frequent stay subword-decomposed.

### Inference (encode) procedure

Training produces an **ordered list of merge rules**. To encode new text:

```
1. Break text into characters
2. Apply merge rules in order (earliest learned first)
3. Done → token sequence
```

Implementations like `tiktoken` do this in close to **O(n)** with tries / FSTs.

### Byte-level BPE

Plain BPE starts from "characters". **Byte-level BPE** starts from "bytes". Differences:

- **Char BPE**: one Unicode character = one unit. Out-of-vocab characters (rare emoji, rare scripts) need `<UNK>` or pre-normalization
- **Byte-level BPE**: 256 byte values. **Any byte sequence** is representable. `<UNK>` does not exist structurally

GPT-family (`tiktoken`) is **byte-level BPE**. That's why "you can paste an emoji and it isn't rejected".

---

## 2. WordPiece

A **cousin** of BPE used in BERT-family.

### Differences from BPE

| Aspect | BPE | WordPiece |
|--------|-----|-----------|
| Merge criterion | Highest frequency | Greatest **likelihood gain** |
| Within-word boundary marker | None (leading-space convention) | **`##` prefix** |
| Math | Counts | Simple probabilistic model |

### `##` prefix

BERT encoding `tokenization`:
```
['token', '##ization']
```

`##ization` means "this is mid-word". In BERT's vocab, `ization` and `##ization` are **different entries** (one is standalone, the other is mid-word continuation).

Same information as BPE's "leading space ` world` vs `world`" — **just a different way to encode word boundaries**.

### Likelihood-based merging

For each candidate pair, compute "how much does merging increase the corpus probability". Pick the highest-gain pair. Roughly:

```
score(x, y) = freq(xy) / (freq(x) × freq(y))
```

If `x` and `y` each appear often standalone, the score drops even if `xy` is also frequent. The intuition: **only merge when the pair is genuinely informative**.

In practice, BPE and WordPiece outputs aren't dramatically different. Recent frontier LLMs have converged on BPE.

---

## 3. Unigram

**Reverse-direction approach**.

```
1. Start with a large candidate vocab (hundreds of thousands)
2. Assign each entry a probability
3. Use EM to find the segmentation that maximizes corpus probability
4. Score each entry by "if removed, how much does total probability drop?"
5. Drop low-contribution entries
6. Stop when target size reached
```

Distinguishing features:

- **Multiple valid splits for the same string** (BPE is deterministic; Unigram is **probabilistic**)
- **Subword regularization** during training improves robustness (sample different segmentations)
- Used in T5, ALBERT, XLNet

User-facing it's hard to distinguish from BPE, but the property "the same string can have multiple tokenizations" is worth knowing so you don't get surprised.

---

## 4. SentencePiece

**A toolkit, not an algorithm**. Google's library (C++ + Python bindings) with two relevant features:

### 1. Treats whitespace as just-a-character

Standard BPE/WordPiece **pre-splits** text into words first — assumes a space-separated language. SentencePiece **replaces space with `▁`** (U+2581 LOWER ONE EIGHTH BLOCK) and treats it as a normal character. Result:

- Works **uniformly across CJK, Thai, and other unspaced languages**
- Handles **source code** (indentation, pretty-printed JSON) cleanly
- Doesn't break if your input's whitespace style differs from the training corpus

### 2. Implements both BPE and Unigram

`--model_type=bpe` or `--model_type=unigram`. LLaMA-family uses SentencePiece-BPE; T5-family uses SentencePiece-Unigram.

### 3. Language-agnostic

Doesn't depend on English-style word boundaries. Widely used for **multilingual** models.

---

## 5. tiktoken (GPT-family)

OpenAI's **fast byte-level BPE implementation**:

- Rust core, Python bindings
- Bundled vocabulary files for GPT-2, GPT-3, GPT-3.5, GPT-4, GPT-4o, …
- **Even within a family, model versions can use different vocabs** — be careful

```python
import tiktoken

# By model name
enc = tiktoken.encoding_for_model("gpt-4")          # cl100k_base
enc = tiktoken.encoding_for_model("gpt-4o")         # o200k_base

# By encoding name directly
enc_gpt2     = tiktoken.get_encoding("gpt2")        # GPT-2
enc_p50k     = tiktoken.get_encoding("p50k_base")   # GPT-3 (Codex)
enc_cl100k   = tiktoken.get_encoding("cl100k_base") # GPT-3.5 / GPT-4
enc_o200k    = tiktoken.get_encoding("o200k_base")  # GPT-4o
```

**Newer generations have larger vocabs** (cl100k = 100K → o200k = 200K), driven by improved multilingual / code coverage.

---

## Cross-tokenizer cheat sheet

```
┌──────────────────┬──────┬───────────┬──────────┬────────────────┐
│ Model lineage    │ Algo │ Toolkit   │ Vocab    │ Notes          │
├──────────────────┼──────┼───────────┼──────────┼────────────────┤
│ GPT-2/3          │ BPE  │ tiktoken  │ ~50K     │ byte-level     │
│ GPT-3.5/4        │ BPE  │ tiktoken  │ 100K     │ cl100k_base    │
│ GPT-4o           │ BPE  │ tiktoken  │ 200K     │ multilingual ↑ │
│ LLaMA 1/2/3      │ BPE  │ SentP     │ 32K-128K │ byte-level     │
│ Mistral / Mixtral│ BPE  │ SentP     │ 32K      │ LLaMA-aligned  │
│ Claude (assumed) │ BPE  │ private   │ ~100K    │ undisclosed    │
│ Gemini (assumed) │ BPE  │ SentP-ish │ ~256K    │ multilingual   │
│ BERT             │ WP   │ HF        │ 30K      │ ## prefix      │
│ T5 / mT5         │ Uni  │ SentP     │ 32K-250K │ stochastic     │
└──────────────────┴──────┴───────────┴──────────┴────────────────┘
```

> [!NOTE]
> Vendors like **Anthropic and Google do not publish their tokenizers**. For those you have to use the **provider's `count_tokens` endpoint** to measure exactly.

---

## Why this directly hits the bill

**The same string has different token counts under different tokenizers** — one of the most important facts in this book.

```python
import tiktoken

text = """The quick brown fox jumps over the lazy dog.
これは日本語のテキストです。Tokenization は奥が深い。"""

for enc_name in ["gpt2", "p50k_base", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    n = len(enc.encode(text))
    print(f"{enc_name:15s}: {n:4d} tokens")

# Example output:
# gpt2           :   89 tokens
# p50k_base      :   89 tokens
# cl100k_base    :   59 tokens
# o200k_base     :   42 tokens
```

**2× spread on the same text**. Newer-generation tokenizers improve multilingual efficiency dramatically.

Implications:
- "How many tokens is this text?" is **unanswerable without specifying a model**
- Comparing the same prompt across providers requires **measuring per-provider**
- **Migrating between models** can reshape budgets (a prompt that fit may now overflow, or vice versa)

---

## Going deeper

### BPE's "whitespace anchor" issue and byte-level rescue

Char BPE typically trains under the assumption that **merges don't cross word (space) boundaries**. Reasonable for English; broken for:
- Unspaced languages (Chinese)
- Source code
- Production text whose whitespace conventions differ from the training corpus

**Byte-level BPE** drops the assumption — looks at **byte sequences only**. Whitespace, newlines, indentation merge naturally per their frequency. This is the **essence of generalization**.

### Unigram and subword regularization

Unigram's stochastic segmentation lets training **randomly pick different tokenizations of the same input**. Result:
- Model becomes robust to "the same thing said differently"
- Inference uses best-decoding to pick one

Benchmarks differences are small overall, but **multilingual robustness gains are reported**.

### Inspecting a vocab

The `cl100k_base` vocab is published — you can poke at entries directly:

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
print(enc.n_vocab)  # 100277

for i in [0, 100, 1000, 10000, 100000]:
    print(f"{i:6d}: {repr(enc.decode([i]))}")
```

**Early IDs are punctuation; later IDs are long English phrases or multilingual fragments**. Just browsing builds intuition for **what is "cheap"**.

### Special tokens

In addition to text tokens, tokenizers carry **special tokens**:
- `<|endoftext|>` — end of sequence
- `<|im_start|>`, `<|im_end|>` — chat-template role boundaries
- `<|fim_prefix|>`, `<|fim_middle|>`, `<|fim_suffix|>` — code completion
- `<|tool_call|>` — function calling (varies by family)

These **don't appear in normal encoding** (need special preprocessing). Chat APIs **insert them automatically**. That's why "my message is 100 tokens but the API charged 125" — the difference comes from these.

---

## Common misconceptions

### ❌ "The tokenizer isn't part of the model"
**Wrong**. The tokenizer is **trained alongside the model**. Vocab size, distribution, special-token placement are tightly coupled with model design. **Swapping tokenizers breaks performance**.

### ❌ "BPE and WordPiece are obviously different algorithms"
**Mostly the same**. Differences are merge criterion (frequency vs likelihood) and boundary marker (leading-space vs `##`); outputs are similar. Real choice = **whatever the model uses**.

### ❌ "SentencePiece is fast/slow"
**Toolkit, not algorithm** — speed depends on options. `tiktoken` is highly optimized for GPT-family BPE, fast — but that's a toolkit comparison, not an algorithm comparison.

### ❌ "`tiktoken` works for any model"
Roughly: only OpenAI families. **Won't give accurate counts for others**. Anthropic, Google, Mistral all need their own tokenizer or a `count_tokens` API.

---

## Recap

- Modern LLM tokenizers boil down to **BPE / WordPiece / Unigram**
- `SentencePiece` is a **toolkit**; `tiktoken` is a **fast byte-level BPE implementation**
- BPE = "greedy merge most frequent pair" — simple, practical, dominant in frontier LLMs
- WordPiece = BERT-family cousin; uses `##` for mid-word boundary
- Unigram = top-down (prune); supports stochastic split, **strong multilingual**
- **Same string + different tokenizer = different token count** — always re-measure when comparing or porting
- Newer tokenizers tend to have larger vocab and better multilingual efficiency

---

## Exercises

**Exercise 3.1** (5 min)
```python
import tiktoken
texts = [
    "The quick brown fox jumps over the lazy dog",
    "素早い茶色の狐は怠け者の犬を飛び越えた",
    "敏捷的棕色狐狸跳过懒狗",
    "def hello(): return 'world'",
]
for enc_name in ["gpt2", "p50k_base", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    print(f"\n{enc_name}:")
    for text in texts:
        print(f"  {len(enc.encode(text)):4d} | {text}")
```
Why does CJK get cheaper in newer tokenizers? (Answer in Chapter 4.)

**Exercise 3.2** (10 min) — Hand-run BPE for 5 merges
```
corpus: "the cat sat on the mat the dog sat on the log"
```
1. Word-split (11 words)
2. Char + end-of-word marker
3. Count adjacent pairs
4. Merge most frequent
5. Repeat 5 times

Paper: 10 min. Python: ~30 lines.

**Exercise 3.3** (challenge)  
Find the tokenizer documentation for an LLM provider you use (Anthropic, Google, Mistral, …). What's published vs not? Disclosure level affects vendor lock-in.

---

## On to the next chapter

You've seen **how** tokenization works. Next: **why the same mechanism imposes wildly different costs across languages**, derived from UTF-8 byte efficiency.

→ [Chapter 4 — Tokens across languages](05-tokens-across-languages)
