# Zenn JSON API — Field Reference

Notes on the unauthenticated endpoint used by `fetch_zenn_article.py`. This
is intentionally short — read it only when you need to extract a field that
the default summary doesn't expose.

> **Stability warning.** The endpoint is undocumented (Zenn does not publish
> a public API contract). Schema may drift. The script defends against
> missing keys but treat new/renamed fields as expected risk.

## Endpoint

```
GET https://zenn.dev/api/articles/{slug}
```

- `{slug}` is the trailing segment of the article URL, e.g.
  `https://zenn.dev/shinyay/articles/idp-platform-portal` → `idp-platform-portal`.
- Username is **not** part of the API path — slugs are globally unique.
- No auth, no API key. A `User-Agent` header is recommended.
- Common responses: `200` (success), `404` (missing/private/deleted),
  `429` (rate limited).

## Response shape

```json
{
  "article": { ... }
}
```

### Key fields on `article`

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Internal numeric ID |
| `slug` | string | URL slug |
| `title` | string | Article title |
| `emoji` | string | Single emoji shown in the Zenn UI |
| `article_type` | string | `"tech"` or `"idea"` |
| `topics` | list | Each item has `name`, `display_name`, `taggings_count`, `image_url` |
| `path` | string | URL path under `zenn.dev` (e.g. `/shinyay/articles/foo`) |
| `published_at` | string | ISO-8601 publish timestamp |
| `body_updated_at` | string | Last body edit timestamp |
| `body_letters_count` | int | Length in characters (Japanese-aware) |
| `liked_count` | int | "👍" count |
| `bookmarked_count` | int | Bookmark count |
| `comments_count` | int | Top-level comment count |
| `body_html` | string | **Rendered HTML body**. No Markdown source is exposed. |
| `toc` | list | Table-of-contents tree extracted from the headings |
| `og_image_url` | string | Cloudinary-generated OGP image |
| `user` | object | Author info — see below |
| `github_url` | string \| null | Source path on GitHub if the article is synced |
| `github_repository` | object \| null | `{full_name, html_url, branch, ...}` when synced |
| `publication` | object \| null | Set when the article belongs to a Publication |
| `status` | string | Usually `"published"` |
| `is_suspending_private` | bool | True only if temporarily hidden |

### `article.user` (selected)

| Field | Notes |
|-------|-------|
| `username` | Zenn handle (e.g. `shinyay`) |
| `name` | Display name |
| `avatar_url` | Profile image |
| `github_username` | If linked |
| `twitter_username` | If linked |
| `total_liked_count` | Across all of the user's posts |

### `topics[i]` (selected)

| Field | Notes |
|-------|-------|
| `name` | Lowercased canonical name used in `topics:` frontmatter |
| `display_name` | Cased name shown in the UI |
| `taggings_count` | How many articles use this topic |

## What the API does **not** return

- Original Markdown source. If you need the exact source as the author wrote
  it, use the `github_url` field to fetch from GitHub instead.
- View/impression counts.
- Comment bodies (only the count). A separate endpoint exists for comments
  but is out of scope for this skill.
- Books and scraps. Those live at different endpoints
  (`/api/books/{slug}`, `/api/scraps/{slug}`) with **different** schemas.

## Body HTML quirks (relevant when reading the extracted Markdown)

- **Heading anchors.** Each `<h2>`/`<h3>` is wrapped in an anchor `<a>`
  whose visible text is empty. In the extracted Markdown this appears as
  `## \n[](#some-anchor) Heading Text\n` — the heading text is correct
  but appears on the line after the marker.
- **Code blocks.** Language hints come from `class="language-xxx"` on
  either `<pre>` or the inner `<code>`. The script reads both. Articles
  written without a language hint will produce unlabeled fences.
- **Embeds** (Tweets, YouTube, Gists, etc.) collapse to
  `[embed: <iframe-src-or-tag>]` placeholders.
- **Images** become standard `![alt](src)` Markdown.
- **MathJax / mermaid / Zenn-specific message boxes** are best-effort —
  the surrounding text is preserved but custom styling is lost.

## Rate limiting & etiquette

- No documented quota, but observed behavior suggests low double-digit
  requests/minute is safe.
- Add a short delay (1–2 s) between bulk fetches.
- Cache aggressively with `--save` rather than re-fetching the same slug
  multiple times in one session.

## Useful one-liners

Get just the GitHub source URL (for syncing back to a local file):

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --format json \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['article'].get('github_url') or '')"
```

List topics from an article:

```bash
python3 .github/skills/zenn-reader/scripts/fetch_zenn_article.py <URL> --format json \
  | python3 -c "import json,sys; a=json.load(sys.stdin)['article']; print(', '.join(t['name'] for t in a.get('topics',[])))"
```
