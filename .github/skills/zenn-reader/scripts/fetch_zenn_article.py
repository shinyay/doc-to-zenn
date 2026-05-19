#!/usr/bin/env python3
"""Fetch a single Zenn article via the public JSON API and emit a structured summary.

The script is designed for the `zenn-reader` Agent Skill. Default behavior is
read-only and prints to stdout so it never dirties the working tree. Pass
`--save` (or `--out-dir`) to persist the raw JSON and an extracted Markdown
rendering of the body to disk.

Stdlib only — no third-party dependencies. Shared helpers live in
``zenn_lib.py`` next to this file.

Usage:
    python3 fetch_zenn_article.py <url-or-slug> [options]

Examples:
    # Summary + first 4000 chars of body to stdout (default)
    python3 fetch_zenn_article.py https://zenn.dev/shinyay/articles/idp-platform-portal

    # Metadata only, no body — cheap context for triage
    python3 fetch_zenn_article.py idp-platform-portal --no-body

    # Full body + persist raw JSON and Markdown to .zenn-cache/
    python3 fetch_zenn_article.py <url> --full --save

    # Machine-readable JSON for downstream processing
    python3 fetch_zenn_article.py <url> --format json

For multiple URLs, use ``fetch_zenn_batch.py`` instead.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from zenn_lib import (
    DEFAULT_CACHE_DIR,
    DEFAULT_MAX_CHARS,
    DEFAULT_TIMEOUT,
    EXIT_FETCH,
    EXIT_OK,
    EXIT_PARSE,
    EXIT_USAGE,
    build_frontmatter,
    extract_slug,
    fetch_article_json,
    html_to_markdown,
    safe_slug_filename,
)


def render_summary(
    article: dict[str, Any],
    body_md: str,
    *,
    max_chars: int,
    include_body: bool,
    full: bool,
) -> str:
    user = article.get("user") or {}
    topics = ", ".join(
        t.get("display_name") or t.get("name") or ""
        for t in (article.get("topics") or [])
        if isinstance(t, dict)
    )
    path = article.get("path") or ""
    lines = [
        f"# {article.get('emoji', '')} {article.get('title', '(no title)')}",
        "",
        f"- URL          : https://zenn.dev{path}",
        f"- Author       : {user.get('name') or user.get('username') or '?'} (@{user.get('username', '?')})",
        f"- Type         : {article.get('article_type', '?')}",
        f"- Topics       : {topics or '(none)'}",
        f"- Published    : {article.get('published_at', '?')}",
        f"- Updated      : {article.get('body_updated_at', '?')}",
        f"- Likes        : {article.get('liked_count', 0)}  Bookmarks: {article.get('bookmarked_count', 0)}  Comments: {article.get('comments_count', 0)}",
        f"- Body length  : {article.get('body_letters_count', 0)} chars",
    ]
    if article.get("github_url"):
        lines.append(f"- GitHub source: {article['github_url']}")
    lines.append("")

    if include_body:
        body = body_md
        truncated = False
        if not full and max_chars > 0 and len(body) > max_chars:
            body = body[:max_chars]
            truncated = True
        lines.append("## Body")
        lines.append("")
        lines.append(body.rstrip())
        if truncated:
            remaining = article.get("body_letters_count", 0)
            lines.append("")
            lines.append(
                f"... (truncated to {max_chars} chars; full body is ~{remaining} chars — re-run with --full or --save to get the rest)"
            )
    else:
        lines.append("(body omitted — pass --no-body=false or omit the flag to include it)")
    return "\n".join(lines) + "\n"


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fetch_zenn_article.py",
        description="Fetch a Zenn article (JSON + readable Markdown) for in-context analysis.",
    )
    p.add_argument("target", help="Zenn article URL, username/slug, or bare slug")
    p.add_argument("--save", action="store_true", help="Persist raw JSON + extracted Markdown under the cache dir")
    p.add_argument(
        "--out-dir",
        metavar="DIR",
        default=None,
        help=f"Directory for persisted files (implies --save). Default: ./{DEFAULT_CACHE_DIR}",
    )
    p.add_argument(
        "--format",
        choices=("summary", "metadata", "markdown", "json"),
        default="summary",
        help="Stdout format. summary=human-readable, metadata=summary w/o body, "
             "markdown=frontmatter+body only, json=raw API JSON",
    )
    p.add_argument("--no-body", action="store_true", help="Summary mode: omit the body (metadata only)")
    p.add_argument("--full", action="store_true", help="Summary mode: print the entire body (override --max-chars)")
    p.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        metavar="N",
        help=f"Truncate the body preview to N chars in summary mode (default: {DEFAULT_MAX_CHARS})",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        metavar="SEC",
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    try:
        slug = extract_slug(args.target)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT_USAGE

    try:
        article = fetch_article_json(slug, timeout=args.timeout)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT_FETCH

    body_html_raw = article.get("body_html") or ""
    try:
        body_md = html_to_markdown(body_html_raw)
    except Exception as e:  # pragma: no cover
        print(f"error: failed to convert body HTML: {e}", file=sys.stderr)
        return EXIT_PARSE

    save = args.save or args.out_dir is not None
    saved_paths: dict[str, str] = {}
    if save:
        out_dir = args.out_dir or DEFAULT_CACHE_DIR
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as e:
            print(f"error: cannot create --out-dir {out_dir!r}: {e}", file=sys.stderr)
            return EXIT_FETCH
        fname = safe_slug_filename(slug)
        json_path = os.path.join(out_dir, f"{fname}.json")
        md_path = os.path.join(out_dir, f"{fname}.md")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({"article": article}, f, ensure_ascii=False, indent=2)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(build_frontmatter(article))
                f.write("\n")
                f.write(body_md)
        except OSError as e:
            print(f"error: writing cache files: {e}", file=sys.stderr)
            return EXIT_FETCH
        saved_paths = {"json": json_path, "markdown": md_path}

    if args.format == "json":
        print(json.dumps({"article": article, "saved": saved_paths}, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        sys.stdout.write(build_frontmatter(article))
        sys.stdout.write("\n")
        sys.stdout.write(body_md)
    elif args.format == "metadata":
        out = render_summary(article, body_md, max_chars=0, include_body=False, full=False)
        sys.stdout.write(out)
        if saved_paths:
            sys.stdout.write(f"\nSaved:\n  json: {saved_paths['json']}\n  md  : {saved_paths['markdown']}\n")
    else:  # summary
        include_body = not args.no_body
        out = render_summary(
            article,
            body_md,
            max_chars=args.max_chars,
            include_body=include_body,
            full=args.full,
        )
        sys.stdout.write(out)
        if saved_paths:
            sys.stdout.write(f"\nSaved:\n  json: {saved_paths['json']}\n  md  : {saved_paths['markdown']}\n")

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
