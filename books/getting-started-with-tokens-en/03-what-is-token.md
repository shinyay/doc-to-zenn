---
title: "Chapter 2 — What a token really is"
---

> **In one line:** A token is **a chunk of text** the LLM treats as **one indivisible unit** when reading input, generating output, and counting cost — usually a subword (a fragment of a word), sometimes a single character, sometimes a short whole word. **Boundaries are non-intuitive — always measure**.

---

## Why this chapter exists

Chapter 1 gave you the mental model: "tokens are the LLM's reading-and-writing unit". That's enough for everyday talk. But it's not enough to **explain**:

- Why 200 characters of English vs 200 characters of Japanese can differ by 3× in token count
- Why the word `tokenization` is sometimes 1 token, sometimes 2
- Why an emoji `🙂` is "1 character" but eats 4 tokens

This chapter closes that gap. We'll internalize, with code, **why a unit that is neither character nor word was chosen**, and **how actual strings get cut**.

---

## Why does the model need a "unit" at all?

Neural networks **cannot see text directly**. They see **numbers** — concretely, sequences of numeric vectors.

Before `Hello, world!` is processed, it must be turned into **a sequence of integers**. Each integer is a row index into the model's **embedding table** (learned at training time). Each row is a learned vector that provides the token's **initial representation**; the contextual meaning itself is formed by later layers, depending on the surrounding tokens.

```
"Hello, world!" ──[tokenizer]──> [9906, 11, 1917, 0]
                                     ↓ ↓ ↓ ↓
                              [embedding table]
                                     ↓ ↓ ↓ ↓
                          [vec₁, vec₂, vec₃, vec₄]   ← model sees these
```

How you define "the unit" affects **everything else**:

- **Sequence length** — how many units to process the same text
- **Vocabulary size** — how many units the model has to learn (rows in the embedding table)
- **Robustness to unknown input** — typos, neologisms, foreign languages, code, emoji
- **Cost / latency predictability** — both scale linearly with unit count

You'd want to use either "characters" or "words" — natural reaction, **both fail miserably**. Let's see why.

---

## Naive option ①: 1 token = 1 character

Vocabulary fits in **a few thousand entries** (alphabet, digits, common punctuation, basic scripts). No `<UNK>` ever — anything you can type, you can tokenize.

Sounds clean. **Two big problems** kill it.

### Problem 1: sequences explode
A medium English paragraph is **hundreds of characters ≈ tens of words**. Going to character units inflates the model's work **5–10×**. Part of attention scales with the **square** of sequence length, so cost gets worse than linearly. Context windows fill instantly.

| Unit | "Hello, world!" token count |
|------|----------------------------|
| Character | 13 |
| Subword (typical) | 4 |
| Word | 2 |

Character-level pays this **~5× tax** on every text.

### Problem 2: spelling has to be re-learned from scratch
If `cat` is three independent units `c`, `a`, `t`, the model must **learn from co-occurrence statistics from zero** that this 3-character sequence means a small furry animal. From the noise of "this triplet appears near `meow` `purr` `kitten`".

That's wasted **representational capacity** on a problem humans solved in elementary school.

Character-level models exist and serve niche use cases, but they **are not the mainstream of general-purpose LLMs**.

---

## Naive option ②: 1 token = 1 word

The opposite extreme: **a whole word per unit**. `cat` = 1 token. `tokenization` = 1 token. Sequences are short, intuitive.

The problem is **vocabulary**.

### Problem 1: vocab explodes and is never finished
English alone has hundreds of thousands of words, **growing daily**. New product names, new slang, new technical terms, names of yesterday's celebrities. Plus:
- Inflections (run, runs, running, ran)
- Compounds (tokenization, pretokenization, detokenize)
- Typos (teh, recieve)
- Code identifiers (`get_user_by_id`)
- Every other language

Add it all up and you cross **a million units** easily.

### Problem 2: out-of-vocab is faceless
A pure word-level tokenizer replaces every unknown word with the placeholder `<UNK>`. New product names, typos, foreign loanwords — **all collapsed to the same `<UNK>`**. The structure of the original string (root, prefix, suffix) is thrown away.

```
input: "I love using Anthropic's Claude!"
out-of-vocab: "Anthropic's", "Claude"
model sees: [I, love, using, <UNK>, <UNK>, !]
```

### Problem 3: doesn't generalize
A model that has seen `tokenize` thousands of times treats `tokenization` as **a totally different thing**. The obvious relationship is **wasted**.

---

## The compromise: subword tokens

Characters are too small. Words are too big. **The middle ground that absorbs both weaknesses** is the subword.

A subword tokenizer **observes large amounts of text** and learns "which byte/character sequences appear often enough to deserve their own slot?".

The result is a kind of stratification:

- **Frequent short words** become 1 token: `the`, `and`, `is`, `to`
- **Frequent long words** also become 1 token: `because`, `function`, `important`
- **Mid-frequency words** split into 2–3 pieces: `tokenization → ["token", "ization"]`
- **Rare words** split into many: `antidisestablishmentarianism → ["anti", "dis", "establish", "ment", "arian", "ism"]`
- **In byte-level BPE families**, truly unseen input can fall back to **byte-level** (more later)

```
character-level                 subword                    word-level
   ┌────────────┐         ┌────────────────┐         ┌────────────┐
   │ small vocab│         │ medium vocab   │         │ huge vocab │
   │ huge       │  ◄────► │ medium         │  ◄────► │ short      │
   │ sequence   │         │ sequence       │         │ sequence   │
   │ no UNK     │         │ no UNK (byte)  │         │ many UNKs  │
   └────────────┘         └────────────────┘         └────────────┘
                                  ▲
                                  │
                          modern LLMs live here
```

Vocab size varies by model but is typically **tens of thousands to ~200,000**. BPE-family tokenizers usually land in the 50,000–100,000 range.

Specific algorithms (BPE, WordPiece, Unigram, SentencePiece) are Chapter 3. For now: just internalize the **shape** of "the middle ground".

---

## Tokenization in concrete examples

> [!NOTE]
> All examples below were measured with the GPT-4-family `cl100k_base` tokenizer. Different tokenizers will produce different splits. **The pattern matters more than the exact numbers**.

### Example 1: a short greeting

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
print(enc.encode("Hello, world!"))
# [9906, 11, 1917, 0]
print([enc.decode([t]) for t in enc.encode("Hello, world!")])
# ['Hello', ',', ' world', '!']
```

**4 tokens**. Notice:

1. **Punctuation (`,`, `!`) is its own token** — short, frequent.
2. **The space before `world` is absorbed into the next token, becoming ` world`**. This is an important convention: `" world"` (with leading space) and `"world"` (without) have **different token IDs**. The same word at the start vs middle of a sentence is split differently for this reason.

### Example 2: medium-length word

```python
print([enc.decode([t]) for t in enc.encode("tokenization")])
# ['token', 'ization']
```

**2 tokens**. `token` is frequent. `ization` is a frequent suffix (organization, civilization, modernization). **Both deserve a slot**, and the model retains the generalization that word-level would have thrown away.

### Example 3: long, rare word

```python
print([enc.decode([t]) for t in enc.encode("antidisestablishmentarianism")])
# Example: ['ant', 'idis', 'establish', 'ment', 'arian', 'ism']
# Exact split varies by tokenizer release; the structural point is that it shatters into multiple subword pieces.
```

**Several tokens** (the exact split varies by tokenizer). This is where subword **taxes** rare long words. The vocab doesn't have the whole word; instead, it assembles it from frequent **subword pieces**. These are not strict linguistic morphemes — they are **fragments learned from frequency**.

### Example 4: a code snippet

```
def hello_world():
```

An example split:
```
['def', ' hello', '_world', '():']
```

A handful of tokens. **The exact split varies a lot by tokenizer** — some absorb `_` into the surrounding identifier, others break it out as its own token. Code observations:

- **How `_` in `snake_case` is bundled depends on the tokenizer** — it may be absorbed into the identifier, or split out as its own token
- **`()` is often one token** (empty parens are common in code)
- **`:` is often its own token**
- **Indentation** (leading whitespace/tabs) is its **own token category**, sometimes 4 spaces collapse to 1 token

This is why "code is less token-efficient than prose" — symbols and identifiers everywhere.

### Example 5: numbers

```
12345
```

Possible splits:
```
["12345"]                — tokenizer that has 5-digit number as one token
["123", "45"]            — splits in groups of 3
["1", "2", "3", "4", "5"] — single digits
```

Numbers are the **most variable** category. Some tokenizers have dedicated slots for 0–999 or for years (1990, 2024). **Affects arithmetic accuracy** — a model that holds `123` as one token represents the number differently than one holding it as `1, 2, 3`.

### Example 6: whitespace, newlines, emoji

```python
print(len(enc.encode("    "))) # 4 spaces → 1 token
print(len(enc.encode("\n")))   # newline → 1 token
print(len(enc.encode("\n\n"))) # double newline → 1 token (frequent)
print(len(enc.encode("🙂")))   # simple emoji → a small handful of tokens (≈2 in cl100k_base)
print(len(enc.encode("👨‍👩‍👧‍👦"))) # family emoji (ZWJ composite) → can hit double-digit tokens
```

Emojis are surprisingly **heavy**. A single emoji is multiple Unicode bytes; if not in the learned vocab, the tokenizer **falls back to byte-level**.

---

## Five common misconceptions

You should now be able to explain why each of these is wrong.

### ❌ Misconception 1: "1 token = 1 word"
**Wrong**. Short frequent words are 1 token; long or rare words split into 2–6. Rule of thumb for English prose: "1 token ≈ 0.75 words" — but variance is large, and **the rule breaks down for code, non-English, and symbol-heavy text**.

### ❌ Misconception 2: "1 token = 1 character"
**Wrong, in the other direction**. `because` (7 chars) is 1 token. Emoji `🙂` (1 char) is 3–4 tokens. **Character count is an even worse predictor of token count**.

### ❌ Misconception 3: "Tokens are the same across models"
**Wrong**. Each model family ships its own tokenizer. **Same string → very different counts depending on tokenizer**. A prompt that fits comfortably in one model can overflow in another. Chapter 3 details.

### ❌ Misconception 4: "Shorter strings = fewer tokens"
**Wrong**, especially in multilingual contexts. Japanese, Chinese, or Arabic text may express the same meaning in **fewer characters** than English, but with **2–3× more tokens**. Chapter 4 details.

### ❌ Misconception 5: "Extra whitespace is free"
**Wrong**. Spaces, tabs, and newlines are **part of tokens**. Indentation, blank lines between paragraphs, and pretty-printed JSON **do consume tokens**. Small per call, but adds up at scale.

### ❌ Bonus 6: "The model sees the characters I typed"
**Half wrong**. The model sees a **sequence of integer IDs**. `Hello` and ` Hello` (leading space) become **different IDs** and look like **different things** to the model. When you debug prompt behavior seriously, you query the tokenizer for "what did the model see?".

---

## Going deeper

Practically, you have what you need. The rest is for "*why* this is the way it is" curiosity.

### Why vocab size lands at "tens of thousands to ~200K"

Modern tokenizer vocab typically lives in the **30,000–200,000** range. Why?

- **Larger vocab**: more coverage per token → shorter sequences → faster inference, better context-window utilization. **But** the input embedding table and output projection blow up (more parameters, more memory). Rare entries are seen too little during training and **fail to learn**.
- **Smaller vocab**: more pieces per word → longer sequences → slower inference, tighter window. **But** lighter table, higher per-token reuse, **easier learning**.

"Tens of thousands to ~200K" is the empirical sweet spot — **not a single right answer**. Designers may pick differently.

### Byte-level fallback and the death of `<UNK>`

Old tokenizers replaced out-of-vocab with `<UNK>`. That is **information loss** — the original spelling is unrecoverable.

**Byte-level BPE tokenizers** largely solve this problem. By taking the smallest unit to be **the 256 byte values**, *any* Unicode character, emoji, or accidentally-pasted binary fragment is **representable**. Frequent byte sequences merge into larger tokens; rare ones decompose to bytes. Other tokenizer families like WordPiece or Unigram may still retain `<UNK>` depending on their design.

```
"normal text" → a few tokens
"¡Hola!"      → a few tokens (frequent multilingual is merged)
"中文"        → a few tokens
"🦄"          → 4 tokens (byte decomposition)
"\xfe\xff"    → 2 tokens (raw bytes)
```

This is why modern models handle **any** input gracefully. There is no "rejected input" — only "**input that uses many tokens**".

### Token IDs vs token strings

When `tiktoken` shows `["Hello", ",", " world", "!"]`, that's a **human-friendly display**. Internally each is an integer ID (a row index). **The model sees only the IDs**.

Two practical implications:

1. **The display hides hidden surprises**: leading spaces, invisible joiners, no-break spaces — visually identical, different IDs.
2. **IDs are not portable across models**: ID 1432 in model A and ID 1432 in model B are **utterly unrelated**. "Sharing a token count" is a quantity, not an identifier statement.

### Why the leading-space convention

Why does ` world` (with leading space) get its own slot?

In English, virtually every word appears **preceded by a space** (except sentence/paragraph initial). If the space were its own token, every document would pay **one token per space** — a large fixed tax.

Folding the leading space **into the next token** allows "mid-sentence `the`" (` the`) and "sentence-initial `the`" to be **separate slots** — both frequent enough to be valuable. Net effect: meaningful token reduction on normal English.

Once you know the convention, no surprise.

### Tokenization is deterministic but not lossy

The same input under the same tokenizer always produces **the same output** (deterministic, not stochastic).

`decode` recovers the **exact original string** (byte-fallback included). **No information loss**. This is the key improvement over the `<UNK>` era.

```python
text = "🦄 こんにちは, world! 中文"
tokens = enc.encode(text)
restored = enc.decode(tokens)
assert text == restored  # True
```

---

## Recap

- **Tokens are subword units** — neither characters nor words; mid-pieces learned from frequency
- Character-level explodes the sequence; word-level explodes vocab and stumbles on unknowns — subword is the **practical solution**
- Modern **byte-level BPE** tokenizers use byte fallback to largely eliminate `<UNK>` (some WordPiece/Unigram setups can still retain it depending on design)
- "Character count → token count" and "word count → token count" predictions are **unreliable**. **Measure**.
- **Leading space** is folded into the next token — know this or be confused
- **Token IDs are not portable across models**. When comparing "token count", verify the **same tokenizer was used**
- All five common misconceptions are wrong; by the end of the book you will reflexively reject them

---

## Exercises

**Exercise 2.1** (5 min)  
For each string below, **predict the token count first**, then measure:
```python
samples = [
    "AI", "AGI", "Anthropic", "OpenAI",
    "GitHub Copilot",
    "tokenization", "pretokenization", "untokenizable",
    "    indented_code = True",
    '{"name": "Alice", "age": 30}',
]
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
for s in samples:
    print(f"{len(enc.encode(s)):3d} | {s!r}")
```
Explain each surprise.

**Exercise 2.2** (10 min)  
Take a system prompt you actually use (e.g. a `.github/copilot-instructions.md`) and run it through a tokenizer. Note:
- Total tokens
- Longest word in tokens
- How many tokens go to whitespace/newlines/symbols

If anything feels "heavier than expected", trust that intuition — Chapter 13 turns it into measurement.

**Exercise 2.3** (optional)  
Compare encodings:
```python
for enc_name in ["gpt2", "p50k_base", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    print(f"{enc_name:15s}: {len(enc.encode('tokenization is fun'))} tokens")
```

---

## On to the next chapter

You've seen the unit. Next: **who decides those tokens, and how**. BPE, WordPiece, Unigram, SentencePiece — names you have heard but maybe never sorted out. Chapter 3 draws the map.

→ [Chapter 3 — Tokenization algorithms](04-tokenization-algorithms)
