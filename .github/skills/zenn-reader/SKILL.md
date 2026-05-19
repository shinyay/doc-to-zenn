---
name: zenn-reader
description: >-
  Fetch, read, and analyze one or more published Zenn (zenn.dev) articles from
  URLs inside a Copilot CLI session. Use when given a zenn.dev article URL (or
  a list of URLs), asked to summarize/explain/critique/compare Zenn articles,
  extract their metadata or code blocks, answer questions about their content,
  cluster or contrast multiple articles, or pull a published article back into
  the workspace for review. Calls Zenn's unauthenticated JSON API with
  stdlib-only Python — no API keys required. Supports any author, not only
  the local repo's articles. Two scripts: fetch_zenn_article.py (one URL) and
  fetch_zenn_batch.py (many URLs with a triage table). Trigger phrases:
  zenn.dev, zenn article, read zenn, fetch zenn, summarize zenn, analyze
  zenn article, explain this zenn, compare zenn articles, multiple zenn URLs,
  zenn 記事を読んで, この記事を要約, この zenn 記事を解説, zenn の記事を取得,
  zenn 記事について質問, 複数の zenn 記事を比較, zenn 記事一覧を分析.
license: Complete terms in LICENSE.txt
---

# Zenn Reader

Pulls one or many published Zenn articles into the current Copilot CLI
session as structured text the agent can reason over: metadata (title,
topics, likes, author, dates) plus a readable Markdown rendering of the body
extracted from Zenn's `body_html`. The skill itself only fetches and
normalizes — Q&A, summarization, comparison, and critique are performed by
the agent using that content.

Two scripts are provided:

| Script | Use when |
|--------|----------|
| `scripts/fetch_zenn_article.py` | Working with **one** article in depth |
| `scripts/fetch_zenn_batch.py`   | Working with **multiple** articles (triage, compare, cluster) |

Both share `scripts/zenn_lib.py` (URL parsing, API call, HTML→MD, etc.).

## When to Use This Skill

- The user pastes a `https://zenn.dev/<user>/articles/<slug>` URL and asks
  to read, summarize, explain, critique, or extract anything from it.
- The user shares a **list** of Zenn URLs and asks for comparison,
  clustering, common-theme extraction, or batch metadata.
- The user asks to compare a published Zenn article to a local
  `articles/*.md` file in this repo (e.g. drift detection, fact checking).
- The user wants to pull metadata (topics, like count, publish date,
  GitHub source URL) for a list of articles.
- The user wants to ingest an article's text and then ask follow-up
  questions about it ("この記事の主張をまとめて", "この記事のコードを Rust で書き直して").

Do **not** use this skill for:

- Local files already in `articles/` — read them directly with the `view`
  tool, no network call required.
- Zenn books (`/books/...`) or scraps (`/scraps/...`) — only standalone
  articles (`/articles/<slug>`) are supported in v1.
- Writing or publishing new content — use `zenn-cli` (`npx zenn ...`).

## Prerequisites

- Python 3.8+ available on PATH (`python3 --version`)
- Outbound HTTPS access to `zenn.dev`
- No API key, login, or token required — the Zenn JSON API is public

## Quick Reference — Single Article

```bash
# Default: print summary + first 4000 chars of body to stdout
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL>

# Metadata only (cheapest — use for triage / lists of URLs)
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --no-body

# Full body (use when the article is short or the user explicitly asks)
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --full

# Persist raw JSON + Markdown rendering to ./.zenn-cache/<slug>.{json,md}
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --save

# Machine-readable JSON for downstream tools
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --format json
```

## Quick Reference — Multiple Articles

```bash
# Triage table + 200-char previews for N URLs (default, context-friendly)
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py URL1 URL2 URL3

# Read URLs from a file (one per line, # = comment)
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py --from-file urls.txt

# Pipe URLs in
grep -oE 'https://zenn\.dev/[^ )]+' notes.md | \
  python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py --stdin

# Lightest output (metadata table only, no previews) — for long lists
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py --from-file urls.txt --format metadata

# Save everything + generate index.json for follow-up analysis
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py URL1 URL2 --save

# Idempotent re-run: skip articles already in cache
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py URL1 URL2 --save --skip-cached

# JSON Lines for programmatic chaining
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py URL1 URL2 --format jsonl
```

Accepted `<URL>` forms (both scripts):

| Form | Example |
|------|---------|
| Full URL | `https://zenn.dev/shinyay/articles/idp-platform-portal` |
| Publication URL | `https://zenn.dev/link/articles/8a010aff542625` |
| `user/slug` shorthand | `shinyay/idp-platform-portal` |
| Bare slug | `idp-platform-portal` |

Batch script behavior:

| Aspect | Detail |
|--------|--------|
| Duplicates | De-duped by slug, preserving first-seen order |
| Rate limit | Sleeps `--delay` seconds between requests (default 1s) |
| Errors | Continue on failure; full error list appended to output |
| Exit code | `0` if all succeeded, `1` if any failed, `3` for usage errors |
| Progress | Per-article status on stderr (suppress with `--quiet`) |

## Step-by-Step Workflow — Single Article

### Step 1 — Identify the article

Extract the URL (or slug) from the user's prompt.

### Step 2 — Choose the right verbosity

Pick the lightest mode that satisfies the user's request to avoid burning
context on irrelevant body text:

| User intent | Recommended flags |
|-------------|-------------------|
| "What is this article about?" / quick summary | (default — summary + 4000 char preview) |
| "List the topics / likes / author" | `--no-body` |
| "Quote the conclusion" / "Translate the whole thing" | `--full` |
| "Compare it to our local copy" | `--save` (then `diff` with `articles/<slug>.md`) |
| Programmatic chaining | `--format json` |

### Step 3 — Run the script

Always invoke via `python3` and pass the URL verbatim. The script writes
nothing to disk unless `--save` or `--out-dir` is set.

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py "<URL>" [flags]
```

### Step 4 — Reason over the result

The stdout output starts with a metadata block followed by the body.
Use that content directly to answer the user's question, summarize, or
critique. **Do not re-fetch the same URL within the same task** — the
output is already in context.

### Step 5 — (Optional) Persist for follow-up work

If the user expects iterative work on the same article (multi-turn Q&A,
local edits, comparison with `articles/<slug>.md`), re-run once with
`--save`. The cache directory `./.zenn-cache/` is gitignored.

## Step-by-Step Workflow — Multiple Articles

Use the **two-stage triage→deep-dive** pattern. It keeps the agent's
context bounded even when the user shares 10+ URLs.

### Stage A — Triage (one batch call)

Run `fetch_zenn_batch.py` on all URLs at once. The default `triage`
format returns a comparison table plus a 200-char preview per article —
enough to cluster, dedupe, or rank without flooding context.

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py \
  URL1 URL2 URL3 URL4 URL5 \
  --save                # persist raw JSON + index.json for stage B
```

For very long lists (20+), use `--format metadata` to skip the previews
entirely and just get the table.

### Stage B — Deep-dive on the relevant subset

Decide which articles deserve full reading from the triage output, then
either:

* Run `fetch_zenn_article.py … --full` for each chosen URL, **or**
* Read the cached `.zenn-cache/<slug>.md` files directly with the `view`
  tool (no extra HTTP calls).

### Stage C — Cross-article analysis

With both raw JSON (`.zenn-cache/<slug>.json`) and rendered Markdown
(`.zenn-cache/<slug>.md`) on disk, you can:

* Compute aggregate stats from `.zenn-cache/index.json` (likes by topic,
  publish-date distribution, author overlap…).
* `diff` published vs. local copies (`diff articles/X.md .zenn-cache/X.md`).
* Extract code blocks across articles for cross-reference.
* Identify cross-references between the articles.

## Examples

### Summarize a single Zenn article

User: 「この記事を要約して https://zenn.dev/zenn/articles/zenn-cli-guide」

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py \
  https://zenn.dev/zenn/articles/zenn-cli-guide --max-chars 8000
```

Then write the summary in the user's language based on the printed body.

### Compare multiple Zenn articles

User: 「これらの記事の共通テーマと違いを教えて URL1 URL2 URL3」

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py \
  URL1 URL2 URL3 --save --preview-chars 400
```

The triage table reveals the metadata; previews + the optional cached
`.md` files in `.zenn-cache/` give the agent enough to identify common
themes and contrast positions.

### Triage a long URL list before deep-diving

User shares 15 URLs and asks "どれが Platform Engineering 関連？":

```bash
# Stage A: ultra-light triage
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py \
  --from-file user_urls.txt --format metadata --save

# Stage B: only fetch full bodies for the relevant subset
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py \
  <chosen-url> --full
```

### Aggregate stats from a batch

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_batch.py \
  --from-file urls.txt --save --quiet --format metadata > /dev/null

python3 -c "
import json
data = json.load(open('.zenn-cache/index.json'))
total_likes = sum(a['liked_count'] for a in data['successes'])
topics = [t for a in data['successes'] for t in a['topics_names']]
from collections import Counter
print('total likes:', total_likes)
print('top topics:', Counter(topics).most_common(5))
"
```

### Compare a published article to its local source

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py \
  https://zenn.dev/shinyay/articles/idp-platform-portal --save --full
diff -u articles/idp-platform-portal.md .zenn-cache/idp-platform-portal.md | head -200
```

### Answer follow-up questions

After the initial fetch, the article body is in context. Answer further
questions directly without re-fetching unless the user explicitly asks
for fresh data.

## Output Schema

Summary mode prints:

```
# <emoji> <title>

- URL          : https://zenn.dev/<path>
- Author       : <name> (@<username>)
- Type         : tech | idea
- Topics       : <comma list>
- Published    : <ISO-8601>
- Updated      : <ISO-8601>
- Likes        : N  Bookmarks: N  Comments: N
- Body length  : N chars
- GitHub source: <URL if synced from GitHub>

## Body

<markdown body, truncated unless --full>
```

Saved files (`--save`):

| File | Contents |
|------|----------|
| `.zenn-cache/<slug>.json` | Raw Zenn API response (full schema) |
| `.zenn-cache/<slug>.md` | YAML frontmatter + extracted Markdown body |
| `.zenn-cache/index.json` | (batch only) summary of every success + failure in the batch |

`index.json` schema (batch):

```json
{
  "generated_at": "<ISO-8601 UTC>",
  "batch_size": 5,
  "success_count": 4,
  "error_count": 1,
  "successes": [
    {
      "slug": "...", "title": "...", "emoji": "...", "article_type": "tech",
      "topics": ["..."], "topics_names": ["..."],
      "author_username": "...", "author_name": "...",
      "url": "https://zenn.dev/...",
      "published_at": "...", "body_updated_at": "...",
      "liked_count": 0, "bookmarked_count": 0, "comments_count": 0,
      "body_letters_count": 0, "github_url": "...",
      "input": "<original input>",
      "json_path": ".zenn-cache/<slug>.json",
      "md_path": ".zenn-cache/<slug>.md",
      "cached": false
    }
  ],
  "errors": [
    { "input": "<original input>", "slug": "<or empty>", "error": "..." }
  ]
}
```

## Troubleshooting

| Symptom | Cause / Fix |
|---------|-------------|
| `error: article not found (404)` | Slug is wrong, article is private, or it was deleted. Verify the URL in a browser. |
| `error: rate limited by Zenn (429)` | Wait a few seconds, then retry. Do not loop. |
| `error: timeout after Ns` | Network slow — retry with `--timeout 30`. |
| `error: not a zenn.dev URL` | Input is from a different domain. Confirm the URL. |
| Body looks garbled or code is unlabeled | Zenn serves only `body_html` (no source Markdown). The stdlib HTML→MD conversion is best-effort. For exact code blocks, fetch the GitHub source via the `github_url` field in the metadata. |
| Heading shows `[](#anchor) TL;DR` first | Cosmetic only — Zenn wraps each heading in a permalink anchor. The heading text follows it. |

## Design Notes

- **Read-only by default.** No file writes unless `--save` / `--out-dir`.
- **Stdlib only.** No `pip install` required — runs anywhere Python 3.8+ runs.
- **Bounded context.** Default `--max-chars 4000` keeps long articles from
  flooding the agent's context window.
- **Agent-owned analysis.** The script never calls an LLM — Q&A is performed
  by Copilot using the fetched content.

## References

- [Zenn API quirks & JSON schema notes](./references/zenn-api.md)
- [fetch_zenn_article.py](./scripts/fetch_zenn_article.py) — single article
- [fetch_zenn_batch.py](./scripts/fetch_zenn_batch.py) — multiple articles
- [zenn_lib.py](./scripts/zenn_lib.py) — shared helpers (no CLI)
