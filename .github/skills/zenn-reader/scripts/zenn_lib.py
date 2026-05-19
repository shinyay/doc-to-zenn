"""Shared helpers for the zenn-reader skill.

Used by both ``fetch_zenn_article.py`` (single article) and
``fetch_zenn_batch.py`` (many articles). Standard library only.
"""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any

API_BASE = "https://zenn.dev/api/articles"
USER_AGENT = "zenn-reader-skill/1.0 (+https://github.com/shinyay/doc-to-zenn)"
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_CHARS = 4000
DEFAULT_CACHE_DIR = ".zenn-cache"

# Exit codes shared by both CLIs.
EXIT_OK = 0
EXIT_FETCH = 1
EXIT_PARSE = 2
EXIT_USAGE = 3

_SLUG_RE = re.compile(r"^[A-Za-z0-9_\-]{1,128}$")
_URL_PATH_RE = re.compile(r"^/(?:[^/]+/)?articles/([^/?#]+)/?$")


# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------


def extract_slug(raw: str) -> str:
    """Accept a Zenn article URL, ``username/slug`` shorthand, or a bare slug.

    Raises ``ValueError`` if no usable slug can be derived.
    """
    if not raw or not raw.strip():
        raise ValueError("empty input")

    candidate = raw.strip()

    if candidate.startswith(("http://", "https://")):
        parsed = urllib.parse.urlparse(candidate)
        if parsed.netloc and "zenn.dev" not in parsed.netloc:
            raise ValueError(f"not a zenn.dev URL: {parsed.netloc}")
        m = _URL_PATH_RE.match(parsed.path)
        if not m:
            raise ValueError(
                f"URL does not look like a Zenn article path: {parsed.path!r}"
            )
        candidate = m.group(1)
    elif "/" in candidate:
        parts = [p for p in candidate.split("/") if p]
        if "articles" in parts:
            idx = parts.index("articles")
            if idx + 1 >= len(parts):
                raise ValueError(f"no slug after 'articles' in {raw!r}")
            candidate = parts[idx + 1]
        elif len(parts) == 2:
            candidate = parts[1]
        else:
            raise ValueError(f"cannot extract slug from {raw!r}")

    if not _SLUG_RE.match(candidate):
        raise ValueError(f"slug contains unexpected characters: {candidate!r}")
    return candidate


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def fetch_article_json(slug: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Call the Zenn JSON API and return the ``article`` dict.

    Raises ``RuntimeError`` (with a clear message) on HTTP, decoding, or
    schema problems so callers can map them to exit codes.
    """
    url = f"{API_BASE}/{urllib.parse.quote(slug, safe='')}"
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise RuntimeError(
                f"article not found (404): slug={slug!r}. "
                "It may be private, deleted, or the slug is wrong."
            ) from e
        if e.code == 403:
            raise RuntimeError(f"access forbidden (403) for slug={slug!r}") from e
        if e.code == 429:
            raise RuntimeError("rate limited by Zenn (429). Retry after a delay.") from e
        raise RuntimeError(f"HTTP {e.code} fetching {url}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error fetching {url}: {e.reason}") from e
    except TimeoutError as e:
        raise RuntimeError(f"timeout after {timeout}s fetching {url}") from e

    try:
        payload = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise RuntimeError(f"invalid JSON from {url}: {e}") from e

    article = payload.get("article")
    if not isinstance(article, dict):
        raise RuntimeError(f"unexpected response schema from {url}: no 'article' key")
    return article


# ---------------------------------------------------------------------------
# HTML -> Markdown-ish text
# ---------------------------------------------------------------------------


class _HtmlToMd(HTMLParser):
    """Best-effort, stdlib-only HTML -> Markdown converter.

    Faithfulness is not guaranteed — it favors readability for downstream
    LLM consumption. Unknown or rich embeds collapse to ``[embed: ...]``
    markers and code blocks are preserved with language hints when present.
    """

    _BLOCK_TAGS = {
        "p", "div", "section", "article", "header", "footer", "main",
        "ul", "ol", "li", "blockquote", "pre", "table", "tr", "hr",
        "h1", "h2", "h3", "h4", "h5", "h6",
    }
    _SKIP_TAGS = {"script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._out: list[str] = []
        self._skip_depth = 0
        self._in_pre = 0
        self._code_lang_stack: list[str] = []
        self._list_stack: list[tuple[str, int]] = []
        self._link_href: list[str] = []

    def _emit(self, text: str) -> None:
        if self._skip_depth:
            return
        self._out.append(text)

    def _emit_block_break(self) -> None:
        if not self._out:
            return
        tail = "".join(self._out[-2:])
        if tail.endswith("\n\n"):
            return
        if tail.endswith("\n"):
            self._out.append("\n")
        else:
            self._out.append("\n\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrd = {k: (v or "") for k, v in attrs}
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1
            return
        if tag in self._BLOCK_TAGS:
            self._emit_block_break()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._emit("#" * int(tag[1]) + " ")
        elif tag == "li":
            if self._list_stack:
                kind, counter = self._list_stack[-1]
                if kind == "ol":
                    self._list_stack[-1] = (kind, counter + 1)
                    self._emit(f"{counter}. ")
                else:
                    self._emit("- ")
        elif tag == "ul":
            self._list_stack.append(("ul", 1))
        elif tag == "ol":
            self._list_stack.append(("ol", 1))
        elif tag == "blockquote":
            self._emit("> ")
        elif tag == "hr":
            self._emit("---\n\n")
        elif tag == "pre":
            self._in_pre += 1
            lang = ""
            cls = attrd.get("class", "")
            m = re.search(r"language-([\w+\-.]+)", cls)
            if m:
                lang = m.group(1)
            self._code_lang_stack.append(lang)
            self._emit(f"```{lang}\n")
        elif tag == "code" and self._in_pre == 0:
            self._emit("`")
        elif tag == "code" and self._in_pre > 0:
            lang_attr = attrd.get("class", "")
            m = re.search(r"language-([\w+\-.]+)", lang_attr)
            if m and self._code_lang_stack and not self._code_lang_stack[-1]:
                self._code_lang_stack[-1] = m.group(1)
                for i in range(len(self._out) - 1, -1, -1):
                    if self._out[i].startswith("```"):
                        self._out[i] = f"```{m.group(1)}\n"
                        break
        elif tag in {"strong", "b"}:
            self._emit("**")
        elif tag in {"em", "i"}:
            self._emit("*")
        elif tag == "a":
            self._link_href.append(attrd.get("href", ""))
            self._emit("[")
        elif tag == "img":
            alt = attrd.get("alt", "").strip()
            src = attrd.get("src", "").strip()
            self._emit(f"![{alt}]({src})")
        elif tag == "br":
            self._emit("\n")
        elif tag == "iframe":
            src = attrd.get("src", "")
            self._emit(f"\n[embed: {src}]\n")
        elif tag == "embed-zenn-tweet" or "embed" in tag:
            self._emit(f"\n[embed: {tag}]\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._emit("\n\n")
        elif tag == "li":
            self._emit("\n")
        elif tag in {"ul", "ol"}:
            if self._list_stack:
                self._list_stack.pop()
            self._emit("\n")
        elif tag == "blockquote":
            self._emit("\n")
        elif tag == "pre":
            self._in_pre = max(0, self._in_pre - 1)
            if self._code_lang_stack:
                self._code_lang_stack.pop()
            self._emit("\n```\n\n")
        elif tag == "code" and self._in_pre == 0:
            self._emit("`")
        elif tag in {"strong", "b"}:
            self._emit("**")
        elif tag in {"em", "i"}:
            self._emit("*")
        elif tag == "a":
            href = self._link_href.pop() if self._link_href else ""
            self._emit(f"]({href})")
        elif tag in self._BLOCK_TAGS:
            self._emit_block_break()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        self._emit(data)

    def get_text(self) -> str:
        text = "".join(self._out)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = "\n".join(line.rstrip() for line in text.splitlines())
        return text.strip() + "\n"


def html_to_markdown(body_html: str) -> str:
    """Convert Zenn ``body_html`` to readable Markdown-ish text."""
    if not body_html:
        return ""
    parser = _HtmlToMd()
    try:
        parser.feed(body_html)
        parser.close()
    except Exception as e:  # pragma: no cover - defensive
        return f"[html parse error: {e}]\n\n{html.unescape(body_html)}"
    return parser.get_text()


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def yaml_escape(value: Any) -> str:
    """Conservative YAML scalar emitter — quotes if needed, escapes safely."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if not s:
        return '""'
    needs_quoting = (
        any(ch in s for ch in ':#&*!|>%@`\n"\'')
        or s[0] in "-?[{"
        or s.strip() != s
    )
    if not needs_quoting:
        return s
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def build_frontmatter(article: dict[str, Any]) -> str:
    """Build a YAML frontmatter block for an article dict."""
    user = article.get("user") or {}
    topics = [t.get("name") for t in (article.get("topics") or []) if isinstance(t, dict)]
    topics_yaml = "[" + ", ".join(yaml_escape(t) for t in topics if t) + "]"
    lines = [
        "---",
        f"source_url: {yaml_escape('https://zenn.dev' + (article.get('path') or ''))}",
        f"title: {yaml_escape(article.get('title'))}",
        f"emoji: {yaml_escape(article.get('emoji'))}",
        f"article_type: {yaml_escape(article.get('article_type'))}",
        f"topics: {topics_yaml}",
        f"author: {yaml_escape(user.get('username'))}",
        f"author_name: {yaml_escape(user.get('name'))}",
        f"published_at: {yaml_escape(article.get('published_at'))}",
        f"body_updated_at: {yaml_escape(article.get('body_updated_at'))}",
        f"liked_count: {yaml_escape(article.get('liked_count'))}",
        f"bookmarked_count: {yaml_escape(article.get('bookmarked_count'))}",
        f"body_letters_count: {yaml_escape(article.get('body_letters_count'))}",
        f"github_url: {yaml_escape(article.get('github_url'))}",
        "---",
    ]
    return "\n".join(lines) + "\n"


def safe_slug_filename(slug: str) -> str:
    """Sanitize a slug into something safe to use as a filename."""
    sanitized = re.sub(r"[^A-Za-z0-9_\-]", "_", slug)
    return sanitized[:120] or "article"


def article_summary_fields(article: dict[str, Any]) -> dict[str, Any]:
    """Return a compact dict of the most useful display fields for an article."""
    user = article.get("user") or {}
    topics = [
        t.get("display_name") or t.get("name") or ""
        for t in (article.get("topics") or [])
        if isinstance(t, dict)
    ]
    return {
        "slug": article.get("slug"),
        "title": article.get("title") or "(no title)",
        "emoji": article.get("emoji") or "",
        "article_type": article.get("article_type") or "?",
        "topics": [t for t in topics if t],
        "topics_names": [
            t.get("name") for t in (article.get("topics") or []) if isinstance(t, dict)
        ],
        "author_username": user.get("username") or "?",
        "author_name": user.get("name") or user.get("username") or "?",
        "url": "https://zenn.dev" + (article.get("path") or ""),
        "published_at": article.get("published_at") or "",
        "body_updated_at": article.get("body_updated_at") or "",
        "liked_count": article.get("liked_count") or 0,
        "bookmarked_count": article.get("bookmarked_count") or 0,
        "comments_count": article.get("comments_count") or 0,
        "body_letters_count": article.get("body_letters_count") or 0,
        "github_url": article.get("github_url") or "",
    }


__all__ = [
    "API_BASE",
    "USER_AGENT",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_CHARS",
    "DEFAULT_CACHE_DIR",
    "EXIT_OK",
    "EXIT_FETCH",
    "EXIT_PARSE",
    "EXIT_USAGE",
    "extract_slug",
    "fetch_article_json",
    "html_to_markdown",
    "yaml_escape",
    "build_frontmatter",
    "safe_slug_filename",
    "article_summary_fields",
]
