---
title: "Chapter 4 — Tokens across languages"
---

> **In one line:** The same meaning costs **2–3× more tokens** in some languages than in others. **Short string ≠ cheap prompt**. CJK, emoji, and code each have their own economics.

---

## Why this chapter exists

Chapter 3 showed that "tokenizers learn vocabulary from training data". The natural next question:

> **If I write the same meaning in a different language, how does the cost change?**

Intuitively, "Chinese has fewer characters, so it should be cheaper". **The reality is the opposite**. This chapter inverts that intuition and gives you a structural explanation for why **multilingual app budgets explode**. You need this when pricing localized products and when designing SLAs for multilingual chatbots.

---

## The moment intuition betrays you

```
English:  "I met a huge dog."          (17 characters)
Japanese: "大きな犬に会った。"         (9 characters)
Chinese:  "我遇到一只大狗。"           (8 characters)
```

**Chinese is shortest on screen** — 8 vs 17, about half. "Chinese version should be half-price" is the natural assumption.

But in practice, **even text that looks shorter on screen often produces more tokens than English**. Under an English-centric vocabulary like `cl100k_base`, Japanese and Chinese frequently land at **roughly 2× the English token count** (the exact ratio depends on the tokenizer generation — always measure on your own text). That's the phenomenon to dissect.

---

## The key is bytes

You only need three facts.

### Fact 1: text is stored as bytes
What you see on screen — `A`, `é`, `あ`, `中`, `🙂` — is, in memory, 1 to several bytes. Almost all modern text uses **UTF-8**.

### Fact 2: UTF-8 byte count varies by character

```
+--------------------------------------+----------------+
| Character class                      | UTF-8 bytes    |
+--------------------------------------+----------------+
| ASCII (A-Z, a-z, 0-9, basic punc)    |       1        |
| Latin extended (é, ñ, ü), Cyrillic, Greek |  2        |
| Arabic, Hebrew                       |       2        |
| CJK ideographs (中, 日)              |       3        |
| Hangul, Hiragana, Katakana           |       3        |
| Many emoji, rare scripts             |       4        |
| Modifier-joined emoji (👨‍👩‍👧‍👦)    |       8–25     |
+--------------------------------------+----------------+
```

**1 ideograph = 3 bytes**. 1 ASCII letter = 1 byte. **There's a 3× difference at the byte level alone**.

### Fact 3: modern byte-level BPE tokenizers see bytes
Recall **byte-level BPE** from Chapter 3. A byte-level BPE tokenizer has no concept of "ideograph" or "emoji" — it only sees **byte-sequence frequencies** (this is the byte-level BPE story; WordPiece and Unigram families may operate at the character level instead).

The training corpus is **mostly English**. So:
- Frequent English byte patterns are densely registered in vocab
- Japanese / Chinese / Arabic byte patterns are sparsely registered
- Result: CJK gets a **double whammy**: 3× bytes + worse vocab efficiency

---

## Why English is "cheap"

The training corpora of major tokenizers are heavily English (Common Crawl, English-leaning web text). So:

- **Frequent English words** (`the`, `and`, `because`, `function`) → single token
- **Frequent English subwords** (`-ing`, `-tion`, `pre-`, `un-`) → single token
- **Frequent English punctuation patterns** (`. `, `, `, `: `) → single token
- **Frequent English code patterns** (`if (`, `def `, `return `) → single token

```
"I met a huge dog."
↓
['I', ' met', ' a', ' huge', ' dog', '.']  ← 6 tokens
```

Roughly one token per word, punctuation independent. **Dense**.

This is the **baseline**. Other languages are described as "how much more than English".

---

## Per-script multipliers (rough shape)

Exact numbers depend on tokenizer; the **shape is stable**.

```
Approx token-count ratio (same meaning, vs English baseline)
(typical modern English-trained BPE)

English        |##########                              1.0×
Spanish        |###########                             1.1×
Italian        |###########                             1.1×
French         |############                            1.2×
Portuguese     |############                            1.2×
German         |#############                           1.3×
Russian        |##############                          1.4×
Greek          |##############                          1.4×
Arabic         |##################                      1.8×
Hebrew         |##################                      1.8×
Hindi          |####################                    2.0×
Bengali        |####################                    2.0×
Korean         |####################                    2.0×
Chinese        |####################                    2.0×
Japanese       |######################                  2.2×
Burmese/Tamil  |##########################              2.6×
Emoji-heavy    |##########################              2.6×
              +----------+----------+----------+----------
              0          1×         2×         3×
```

> [!NOTE]
> These ratios reflect **the bias of the training data**, not properties of the languages themselves. A tokenizer trained on Japanese-heavy data would invert it. But that is **not** the status quo of frontier LLMs.

---

## Same meaning, three scripts

```python
import tiktoken

texts = {
    "English":  "I love programming and learning new technologies every day.",
    "Japanese": "私は毎日プログラミングと新しい技術を学ぶのが大好きです。",
    "Chinese":  "我喜欢编程和每天学习新技术。",
    "Korean":   "저는 매일 프로그래밍과 새로운 기술을 배우는 것을 좋아합니다。",
    "Arabic":   "أحب البرمجة وتعلم التقنيات الجديدة كل يوم。",
}

enc = tiktoken.get_encoding("cl100k_base")
print(f"{'Lang':10s} | {'chars':>5s} | {'bytes':>5s} | {'tokens':>6s} | {'×Eng':>5s}")
print("-" * 50)

base = len(enc.encode(texts["English"]))
for lang, text in texts.items():
    n_chars  = len(text)
    n_bytes  = len(text.encode("utf-8"))
    n_tokens = len(enc.encode(text))
    ratio    = n_tokens / base
    print(f"{lang:10s} | {n_chars:5d} | {n_bytes:5d} | {n_tokens:6d} | {ratio:4.1f}×")
```

**Exact numbers depend on the tokenizer version and generation**, but the structural pattern you'll typically see looks like this:

```
Lang       | chars | bytes  | tokens trend
--------------------------------------------------
English    | base  | base   | baseline (smallest)
Japanese   | small | ~3×    | ~2× English
Chinese    | small | ~3×    | 1–2× English (closer to English in newer gens)
Korean     | mid   | ~3×    | 2–3× English (root + particle decomposition)
Arabic     | mid   | ~2×    | 1.5–2× English
```

Observations:
- Even when there are fewer characters, **byte count grows** — so token count exceeds English
- Korean tends to land highest because of root + particle decomposition
- Newer `o200k_base` notably improves Chinese and Japanese
- Bytes and tokens **correlate loosely, not perfectly**
- **Always measure on your own text with the tokenizer you actually use**

---

## Code is also a "language"

Source code has its own economics.

### Cheap things
Frequent in training corpora → often single tokens:
- Keywords: `if`, `for`, `return`, `def`, `class`, `function`, `const`
- Idioms: `() {`, `};`, `=>`, `->`, `==`
- Standard indentation: 4 spaces, tabs
- Common identifiers: `self`, `this`, `value`, `result`, `error`, `data`

### Expensive things
- **Long, idiosyncratic identifiers**: `customer_invoice_aggregation_service` won't be one token; it splits into many pieces
- **Mixed casing**: `camelCase` and `snake_case` for the same concept produce different counts
- **Dense punctuation**: `};});` is structural noise that costs multiple tokens
- **Multilingual comments**: English keywords + Japanese comments → CJK multiplier on the comment portion

```
Mental model for code:

  Keywords + simple identifiers     → cheap, near 1:1
  Long descriptive identifiers      → expensive, fragmented
  Indentation, brackets, semicolons → cheap individually, accumulate over long files
  Verbose-key JSON                  → 50%+ can be punctuation
  CJK comments and string literals  → CJK multiplier applies directly
```

---

## Structural noise

Everything in the input is **tokens**. Including things you don't think of as "content":

- **Repeated indentation**: deeply nested YAML or Python class structures pay for leading whitespace
- **Trailing whitespace**: invisible, not free
- **Markdown tables**: pipes, hyphens, alignment markers, repeated headers — **scaffolding billed per row**
- **Code fences**: ``` ```python ``` openings/closings, blank lines
- **Boilerplate header/footer**: a "system context" pasted on every request pays **every time** (without caching)

Strip a long Markdown doc to "just the prose" and re-measure: the structural overhead is often **shockingly large**.

---

## Numbers and arithmetic

Numbers have their own pitfalls. Tokenizers vary:

- Some: short integers as one token (`12345` → 1)
- Some: 2–3 digit groups (`12345` → `123` + `45`)
- Some: per-digit (`12345` → `1`+`2`+`3`+`4`+`5`)

This affects **quality, not just cost**. Per-digit tokenizers tend to be **better at arithmetic** because they see digits uniformly. Bundled tokenizers are cheap but represent similar numbers differently. **Worth checking explicitly if numbers matter to your app**.

---

## Four intuitions to retire

1. **"Translating to a shorter script makes it cheaper"** ❌  
   Reverse: translating English to Japanese / Chinese almost always **adds tokens**.

2. **"Code is just text, similar cost"** ❌  
   Short idiomatic code can be denser than English; long identifiers and verbose JSON can be far heavier.

3. **"Localized version costs the same as English"** ❌  
   A Japanese support chatbot consumes about **2× the tokens** of the English version doing the same work.

4. **"Adding a language is just a feature"** ❌  
   It's a **persistent cost multiplier on every request**. Not a reason to avoid it, but a reason to **budget honestly**.

> [!WARNING]
> When designing per-user / per-conversation token budgets, **don't size based on English-only tests**. Simulate the same conversations in your worst-multiplier language and budget for that. Otherwise non-English users silently get **truncated answers** and **early limits**, invisible from English-only dashboards.

---

## Going deeper

### Newer tokenizers narrow the gap (slowly)

Tokenizer designers are aware. Recent vocabularies **deliberately allocate slots** for frequent CJK characters, frequent CJK bigrams, and code patterns.

Compare `cl100k_base` (GPT-4) vs `o200k_base` (GPT-4o): CJK and emoji efficiency improve substantially. Multipliers compress generation by generation, but they **never go to zero** — vocab slots are finite, and English data still dominates training.

**For multilingual-cost-sensitive apps, re-measure on every model update**. New models can quietly raise (or lower) your budget.

### Equity dimension

Frankly: **under per-token billing, people writing non-Latin scripts pay more for the same idea**.

- A Japanese student using a paid LLM for homework help pays **about 2× more** than their English-speaking peer
- A small business in Korea pays a **structural premium** unrelated to value received

This is not a curiosity — it's a real **product / pricing problem**. Some companies absorb the difference; some pass it through; some train language-specific tokenizers. **None is intrinsically wrong, but ignoring the difference quietly disadvantages certain users**.

### Levers to soften the multilingual penalty

In order of effort:

1. **Keep structure in English**: field names, JSON keys, schema headers, system prompts, instructions in English; only user-facing content in target language — concentrate the multiplier on the unavoidable part
2. **Cache heavy stable parts**: long system prompts, style guides, personas, retrieval contexts — pay full price **once** via provider caching (Chapter 10)
3. **Don't round-trip translate unnecessarily**: if a user wrote Japanese, don't silently translate → process → translate back unless quality demands it. Each round-trip = tokens
4. **Pick locale-aware tokenizers**: when comparable models exist and your app is non-English-centric, **target-script vocab coverage** is a legitimate selection criterion
5. **Concise identifiers in shared prompts**: descriptive names are good for humans, costly in tokens. Balance per project

### Emoji and modern text

Modern UGC — chat, social, reviews — is full of emoji, combining characters, ZWJ joiners. A "single" family emoji `👨‍👩‍👧‍👦` is around **25 bytes** of UTF-8 and can cost **double-digit tokens** depending on the tokenizer. For apps processing casual text at scale, **emoji is real recurring cost, not rounding error** — measure on the tokenizer you actually use.

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
for e in ["🙂", "👨‍👩‍👧‍👦", "🏳️‍🌈", "👨🏻‍💻"]:
    print(f"{e} : {len(e.encode('utf-8'))} bytes, {len(enc.encode(e))} tokens")
```

---

## FAQ

**Q1.** "Chinese packs meaning into one character — shouldn't tokens reflect that?"  
A. **No, opposite**. Each Chinese character = 3 bytes, and is sparsely registered in English-trained vocabularies. **The on-screen brevity is misleading**.

**Q2.** "Adding Unicode support helps multilingual?"  
A. Unicode defines character **encoding**, not vocabulary **content**. Unicode-supporting tokenizers can still be expensive on languages absent from training data.

**Q3.** "Removing emoji cuts cost?"  
A. For emoji-heavy apps (customer chat) yes; for normal business documents, noise.

**Q4.** "Just standardize on English ASCII code — optimal?"  
A. Cost-only, mostly yes. But sacrificing **localization value** for "all English" is a product decision, not a technical one. Token optimization is means, not end.

**Q5.** "Will a Japanese LLM (rinna etc.) make Japanese cheap?"  
A. **Yes** — Japanese-trained tokenizers compress Japanese efficiently. Trade-off: check English-benchmark performance.

---

## Recap

- **Characters ≠ bytes ≠ tokens**. Each mapping has its own bias
- English = cheap baseline. Latin-extended 1.1–1.4×, CJK / Arabic / many Indic scripts 1.8–2.5×
- **Short on screen ≠ cheap in tokens** — often the reverse
- Code, JSON, Markdown, deep indentation, long identifiers, emoji each have **counter-intuitive cost shapes**
- Localized products have **structurally different unit economics** from the English version — budget, price, and measure per-language
- Newer tokenizers compress the gap. **Re-measure on every model update**

---

## Exercises

**Exercise 4.1** (5 min)  
Take a recent text you wrote in your native non-English language (Slack message, email, blog) and measure with `cl100k_base`. Compare to its English translation. Ratio?

**Exercise 4.2** (10 min)  
Pick a file with long identifiers from your codebase.
1. Measure with `tiktoken`
2. Make a "shortened" version (e.g., `customerInvoiceService` → `cis`)
3. Re-measure
4. % reduction?

Not advocating shortening — this is a cost-shape exercise.

**Exercise 4.3** (challenge)  
For your top 3 user locales, measure typical conversation samples. Compute multipliers vs English and use them to redesign per-locale `max_tokens` budgets.

---

## On to the next chapter

Knowing that languages cost differently, you next need **how to actually count your text**. Chapter 5 covers `tiktoken`, `transformers`, `@dqbd/tiktoken`, and small CI-friendly tools.

→ [Chapter 5 — Counting tokens](06-counting-tokens)
