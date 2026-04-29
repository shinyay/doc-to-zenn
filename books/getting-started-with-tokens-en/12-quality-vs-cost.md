---
title: "Chapter 11 — The quality vs cost curve"
---

> **In one line:** **More context ≠ better answer**. Quality rises with prompt size, plateaus, and **eventually drops**. Aim for **minimum sufficient** context, not **maximum possible**.

---

## Why this chapter exists

By now you have strong intuition that tokens cost money, context-window space, and latency. A reasonable next thought: *"Sure, but if I can afford it, more context = better, right? Bigger prompt = smarter answer?"*

**That assumption is the most expensive mistake in this entire guide.**

The relationship between context size and answer quality is **not monotonic**. Not even close. **Quality rises with context size, plateaus over a comfortable middle, then degrades** as the prompt grows further — sometimes sharply. You end up paying **more tokens for a worse answer**.

This chapter explains the **shape of the curve, why it bends down, and how to think about "the right amount" as an engineering decision (not a vibes call)**.

---

## The tempting (wrong) mental model

The naive model many people carry:

```
quality
 ^
 |                                    ___________
 |                              _____/
 |                        _____/
 |                  _____/
 |            _____/
 |      _____/
 |_____/______________________________________________> context size
```

"**More relevant material in the prompt = better-grounded answer = better outcome. Just keep adding stuff.**"

This model is correct for the **first part** of the curve. If you're missing the one file the answer needs, adding it helps a lot. If you have zero examples of the desired output style, adding two examples helps a lot.

**But the curve doesn't stay flat at the top. It bends.**

---

## The actual shape

A more honest sketch:

```
quality
 ^
 |              ___________
 |           __/           \___
 |         _/                  \__
 |       _/                       \__
 |     _/                            \___
 |   _/                                  \____
 |  /                                         \___
 | /                                              \__
 |/_____________________________________________________> context size
   ^         ^                ^                 ^
   too       sweet            plateau           degradation
   little    spot                               zone
```

**Four regions** worth naming:

1. **Too little context**: model is guessing. Doesn't know your codebase, conventions, the facts the answer depends on. **Low quality from missing information**
2. **Sweet spot**: relevant files, relevant rules, clear task. **Quality climbs steeply**
3. **Plateau**: adding "maybe relevant" material doesn't help much. **You're paying for tokens that produce no measurable lift**
4. **Degradation zone**: **actively making the answer worse**. The signal is drowning in noise you added

Most teams **accidentally live in the plateau or degradation zone** — adding context **feels like "showing your work"** and feels like the responsible move, even when it isn't helping the model.

---

## Why quality drops with too much context

Degradation is no mystery. **Five concrete mechanisms**:

### 1. Lost in the middle
The model doesn't weight all tokens equally. Empirical studies consistently show a **position-dependent recall pattern** (often called "lost in the middle"): information at the **start** and **end** of the context tends to be reliably recalled and used, while **information buried in a long middle is systematically de-prioritized**. It's better understood as a recall-vs-position effect than as one specific "U-shaped attention" mechanism — strength and shape vary by model and task, and newer generations mitigate it to varying degrees.

```
attention to a fact, by position in prompt:

high |█                                                 █
     |█                                                 █
     |█                                              ███
     |██                                            ████
     |██                                          ██████
     |███                                        ███████
     |████                                      ████████
     |█████  ___________________________________█████████
 low |__________________________________________________
       start            middle                      end
```

If the critical sentence the answer needs is at line 420 of a 900-line dump, the model may not "see" it strongly enough to reason from it — even though it's strictly inside the context.

### 2. Distraction and dilution
The model distributes attention across the whole prompt. **Every irrelevant token competes with relevant tokens for attention budget**.

Adding 5,000 tokens of "this might help" **lowers the relative weight of the 200 tokens that actually mattered**. Because attention is softmax-normalized, irrelevant "distractor" tokens **steal attention mass** from the relevant ones — the model isn't literally averaging over the padding; it just becomes **harder for it to sharply select the few tokens that matter**. The S/N ratio of your prompt **directly affects the S/N ratio of the answer**.

A useful mental image: **shouting in a quiet room vs shouting in a stadium**. Same volume, very different effect.

### 3. Conflicting signals
A big always-on instruction file — thousands of tokens of "agent rules" or repo-wide guidelines — tends to **accumulate contradictions** over time. One section says "prefer brevity"; another says "always include detailed explanations". One says "never modify file X"; another says "keep all related files in sync".

When a user request lands on top of a stack of partially-conflicting rules, the model **has to pick which rule to follow**. Sometimes well. **Often unpredictably**. The longer the instruction stack, the more likely you're sitting on **contradictions you've forgotten you wrote**.

### 4. Anchoring on examples
Few-shot examples are powerful. **Too-long few-shot is powerful in the wrong direction**. If 10 worked examples all share a structural quirk (e.g. all return JSON in a particular wrapper field), the model may **faithfully copy that quirk** even when the current task doesn't need it.

**Examples are cages**. The model **mimics the shape of the examples instead of solving the underlying task**. **Two crisp, well-chosen examples often beat ten sloppy ones**.

### 5. Latency and timeouts
Long context takes longer to process. **TTFT roughly grows with prompt size** (Chapter 8). That delay interacts badly with **retry logic, user patience, and agent tool-call timeouts**.

A prompt that **would have produced a great answer in 40 seconds** is worthless if the client gives up at 30. **Not a bad answer — no answer**.

---

## Needle-in-a-haystack vs real reasoning

Vendors love to publish "needle in a haystack" benchmarks: hide one sentence somewhere in a million tokens of filler, ask the model to retrieve it, report near-perfect accuracy. **The result is real**. **But reading it as "the model can usefully reason over a million tokens" is misleading**.

**Two different abilities are at play**:

| Ability | What it measures | How it scales with context |
|---------|------------------|----------------------------|
| Retrieval | Can the model locate one specific fact? | **Decays slowly**. Often near-perfect even at very long context |
| Reasoning | Can the model integrate many facts and reach a correct conclusion? | **Decays much faster**. Performance drops **well before** the window is full |

> [!IMPORTANT]
> "**The model accepts N tokens**" and "**the model reasons well over N tokens**" are different claims. The former is hardware/architecture; the latter is empirical, and **the honest answer is almost always "less than the maximum"**.

Practical implication: **don't let the advertised context window set your expectations for answer quality on complex multi-step tasks**. The **effective context** (the region where the model still reasons sharply) is **meaningfully smaller** than the **maximum context**.

---

## The reasoning-effort dial

Some models expose a reasoning-effort setting (low/medium/high). **Higher settings let the model spend more hidden reasoning tokens before producing the visible answer**. As we saw in Chapter 10, **those hidden tokens are real cost**.

The tradeoff is real but **not "higher is always better"**:

```
            low effort        medium effort       high effort
 quality:   ok                better              best (on hard tasks)
 cost:      cheap             mid                 expensive
 latency:   fast              mid                 slow
 best for:  trivial / lookup  typical work        truly hard reasoning
```

For trivial tasks — "rename a variable", "summarize this paragraph" — high reasoning is **pure waste**. **The model burns hidden tokens deliberating on questions that don't need deliberation**. You pay more, wait longer, and get an answer indistinguishable from the cheap setting.

For hard tasks — multi-step debugging, architecture decisions, subtle math — high reasoning **earns its cost**. **The hidden tokens buy correctness that low-effort runs can't reach at any prompt length**.

**The right dial is task-dependent**. Default-high is as wrong as default-low.

---

## The minimum-sufficient-context principle

Tying the threads together gives **one principle**:

> **Aim for minimum sufficient context**. Just what the model needs to answer well — no less, no more.

- *Less* wastes **quality**: the model guesses what it could have known
- *More* wastes **cost** (you pay for unused tokens), **quality** (the curve bends down), **and latency** (TTFT grows)

**Reframe prompt design**. Not "**what could be relevant?**" but "**what's the smallest input set that lets a competent model answer this correctly?**". **That question has a different, usually much smaller answer**.

Chapter 12 turns this principle into concrete habits. The takeaway here is the mindset shift: **adding context is a cost, not a free hedge**.

---

## The right metric: cost per correct answer

Token cost alone is an **incomplete metric**, and it can mislead badly. **The metric that actually matters is cost per correct answer**.

Consider two configs for the same task:

```
Setup A: small cheap model
  - cost per attempt:                    low
  - first-attempt accuracy:              50%
  - average attempts to get a correct:   ~2
  - total cost per correct:    low × 2  =  mid
  - total latency per correct: fast × 2 =  mid
  - human-time reviewing wrong outputs:  nonzero

Setup B: stronger model, one-shot
  - cost per attempt:                    high
  - first-attempt accuracy:              90%
  - average attempts to get a correct:   ~1.1
  - total cost per correct:    high × 1.1
  - total latency per correct: slow × 1.1
  - human-time reviewing wrong outputs:  near zero
```

Depending on the numbers, Setup B can be **cheaper per correct answer than Setup A** — even with a higher per-call cost. **And this calculation doesn't even price the human time spent reading, rejecting, and re-prompting Setup A's wrong outputs**.

**Token cost alone flatters cheap-but-wrong setups**. **Cost per correct answer punishes them honestly**. Chapter 13 dives into measuring this for real.

---

## The curve in practice

Three concrete patterns where the curve shows its teeth:

### Refactoring: whole codebase vs relevant files
Dumping the whole repo into a refactoring prompt **feels thorough**. **In practice the model's edits are less surgical, drift to unrelated files, and "fix" things that didn't need fixing**. **Three or four well-chosen files almost always produce cleaner diffs than the full tree**.

### RAG: 10 strong hits vs 50 mediocre hits
A retrieval pipeline that returns 50 chunks "to be safe" **usually performs worse** than the same pipeline tuned to return 10 high-precision chunks. The extra 40 dilute relevance, **the prompt grows longer and slower, and answer quality drops**.

### System prompts: 200 tokens vs 5,000 tokens
A focused 200-token prompt that names **role, format, and one or two non-negotiables** **often beats** a sprawling 5,000-token guidelines doc. The long version contains more "wisdom" and **produces less in answers** — partly because the model has to weigh dozens of rules of varying relevance against a real request.

**In each case, the team that shrunk the context didn't just save money. They got better answers.**

---

## Going deeper

### Effective context vs maximum context
The advertised window is the upper bound on what the model **accepts**, not what it **uses well**. Empirical studies of long-context utilization **repeatedly** find reasoning quality starts to degrade well before the window is full, and that degradation is **task-dependent**: **extraction tasks hold up longer than multi-hop reasoning tasks**. **When planning a system, treat effective context as the real budget**.

### Position-dependent recall
The position-dependent recall pattern (often called "lost in the middle") means **where you place a fact** matters as much as **whether you include it**. The same critical instruction can produce **visibly different answers** depending on whether it's near the start, in the middle, or right before the user message. **Important rules belong near the top or near the bottom — don't bury them in the middle**.

### Why fine-tuning or RAG can beat brute-force long context
Three broad options for handling domain knowledge: cram everything into the prompt, retrieve relevant slices when needed (RAG), or bake into the weights (fine-tuning). **Cramming is the most expensive per call, scales worst, and pushes you into the degradation zone fastest**.

Each option has its sweet spot:

- **RAG** shines for **large, frequently-updated, or citation-sensitive knowledge**: keeps the prompt small and surgical while letting you pull in fresh content and sources on demand
- **Fine-tuning** mainly bakes in **behaviors, style, and small recurring knowledge**: things like "always use this output format", "match this tone", or "domain-specific phrasing" move out of the prompt cleanly. It's **not a drop-in replacement for retrieval when the underlying facts are large, changing, or need to be cited** — old or wrong knowledge baked into weights is hard to detect later
- **Stuffing everything into long context** is **rarely the best of the three**; **it's just the easiest to reach for**

In practice, a strong combination is: **fine-tune for behavior and style, RAG for changing knowledge, and only put what is genuinely needed for this turn into the prompt**.

### Quality is a distribution, not a number
There isn't "**a** quality" for a prompt. There's a **distribution of qualities across runs**, and longer/noisier prompts tend to **lower the mean and widen the distribution**. **More variance** = harder to evaluate, easier to miss regressions. **Short focused prompts aren't only better on average — they're more predictable**.

> [!NOTE]
> If you take one thing from this chapter into Chapter 12: **stop optimizing prompts for completeness, start optimizing for sufficiency**. Completeness is for documents. **Sufficiency is for inference**.

---

## FAQ

**Q1.** "Big-window model means I can dump anything in safely?"  
A. **No**. **Effective < maximum**. Advertised size is "what it accepts"; reasoning quality drops well before that.

**Q2.** "Including review time, which is actually cheaper?"  
A. **Compute cost per correct answer**. A cheap-but-wrong model is **often more expensive in reality** once human review and re-prompting are added.

**Q3.** "How many few-shot examples is right?"  
A. Task-dependent, but start with **2–3 well-chosen examples**. If 10 don't help (or hurt), **experiment with fewer**.

**Q4.** "Can the U-shape be avoided?"  
A. **Mitigated by structure**: critical info at start/end, label/index files, summarize first. Not fully eliminated.

**Q5.** "I want to fix reasoning effort to low to save money."  
A. Fine for easy tasks. **On hard tasks, increased wrong answers make the 'savings' more expensive**. Route by task type.

---

## Recap

- Quality vs context size is **not monotonic**. It rises, plateaus, and **degrades**
- Drivers of degradation: **lost-in-the-middle attention**, **dilution by irrelevant tokens**, **conflicting always-on instructions**, **over-anchoring on examples**, **latency / timeout effects**
- Accepting N tokens and reasoning well over N tokens are different. **Effective < maximum**, and the gap is biggest on hard reasoning tasks
- The reasoning-effort dial is a real lever, but **higher isn't always better**. Match it to the task
- Right design goal: **minimum sufficient context** — exactly what the model needs, nothing more
- Right metric: **cost per correct answer**. Cheap-and-wrong is often expensive once retries and review are counted
- Real-world wins often come from **removing tokens, not adding them**: fewer RAG hits, smaller system prompt, narrower file selection

---

## Exercises

**Exercise 11.1** (10 min)  
Take one of your prompts and **remove paragraphs one at a time**, watching for the point where quality drops. Where is **minimum sufficient**?

**Exercise 11.2** (10 min)  
For one hard task, run **3 trials at low/medium/high reasoning effort**. Record **accuracy, latency, estimated cost**. Pick the winner by **cost per correct answer**.

**Exercise 11.3** (challenge)  
In your RAG pipeline, reduce **top-K from 20 → 10 → 5** and measure eval-set accuracy at each setting. **Plot the curve and find the sweet spot**.

---

## On to the next chapter

You see *why* less is often more. Next we turn this into **a working set of habits** — practical token hygiene applicable across every prompt, every agent, every pipeline.

→ [Chapter 12 — Token-hygiene principles](13-hygiene)
