#!/usr/bin/env python3
"""Fetch multiple Zenn articles in one shot for cross-article analysis.

Designed for the `zenn-reader` Agent Skill. The default output is a compact
**triage table** plus short body previews so an agent can quickly decide
which articles deserve a deeper read — without flooding its context.

Stdlib only. Shares URL/HTML/serialization helpers with
``fetch_zenn_article.py`` via ``zenn_lib.py``.

Inputs (any combination — duplicates are de-duplicated by slug):

* Positional ``TARGETS``: ``fetch_zenn_batch.py URL1 URL2 SLUG3``
* ``--from-file PATH``:   read URLs/slugs from a file, one per line.
                          Blank lines and ``#`` comments are ignored.
* ``--stdin``:            read URLs/slugs from standard input.

Output formats (``--format``):

* ``triage`` (default) — Markdown table of metadata + N-char body previews
                         + an error report at the end.
* ``metadata``          — Same table without the previews (lightest).
* ``jsonl``             — One JSON object per article on its own line, plus
                          one error object per failure.
* ``md_full``           — Each article rendered as YAML frontmatter + full
                          body, separated by ``---`` rulers (heavy).

Persistence (``--save`` / ``--out-dir``):

* Each article is written to ``<cache>/<slug>.json`` and ``<cache>/<slug>.md``.
* A combined ``<cache>/index.json`` is generated listing every success and
  every failure for the batch.

Exit codes:
* 0 — all articles fetched successfully
* 1 — at least one fetch failed (other articles may still be in the output)
* 3 — usage error (no inputs, bad flags, etc.)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from typing import Any, Iterable

from zenn_lib import (
    DEFAULT_CACHE_DIR,
    DEFAULT_TIMEOUT,
    EXIT_FETCH,
    EXIT_OK,
    EXIT_USAGE,
    article_summary_fields,
    build_frontmatter,
    extract_slug,
    fetch_article_json,
    html_to_markdown,
    safe_slug_filename,
)

DEFAULT_PREVIEW_CHARS = 200
DEFAULT_DELAY = 1.0


# ---------------------------------------------------------------------------
# Input collection
# ---------------------------------------------------------------------------


def _read_file_targets(path: str) -> list[str]:
    targets: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            targets.append(stripped)
    return targets


def _read_stdin_targets() -> list[str]:
    targets: list[str] = []
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        targets.append(stripped)
    return targets


def collect_targets(args: argparse.Namespace) -> list[str]:
    """Combine positional args, --from-file, and --stdin into one list."""
    combined: list[str] = list(args.targets)
    if args.from_file:
        combined.extend(_read_file_targets(args.from_file))
    if args.stdin:
        combined.extend(_read_stdin_targets())
    return combined


def deduplicate_by_slug(targets: Iterable[str]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Resolve each input to its slug and drop duplicates (preserving order).

    Returns ``(resolved, parse_errors)`` where ``resolved`` is a list of
    ``(original_input, slug)`` for unique slugs and ``parse_errors`` lists
    inputs that couldn't be parsed at all.
    """
    seen: set[str] = set()
    resolved: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []
    for raw in targets:
        try:
            slug = extract_slug(raw)
        except ValueError as e:
            errors.append((raw, str(e)))
            continue
        if slug in seen:
            continue
        seen.add(slug)
        resolved.append((raw, slug))
    return resolved, errors


# ---------------------------------------------------------------------------
# Fetch loop
# ---------------------------------------------------------------------------


def fetch_many(
    resolved: list[tuple[str, str]],
    *,
    timeout: float,
    delay: float,
    cache_dir: str | None,
    skip_cached: bool,
    progress: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Fetch articles sequentially.

    Returns ``(successes, errors)``. ``successes`` items are dicts of
    ``{input, slug, article, body_md, cached}``. ``errors`` items are dicts
    of ``{input, slug, error}``.
    """
    successes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    total = len(resolved)
    for idx, (raw, slug) in enumerate(resolved, start=1):
        if progress:
            print(f"[{idx}/{total}] fetching {slug} ...", file=sys.stderr, flush=True)

        # Skip if cached and requested
        if skip_cached and cache_dir:
            fname = safe_slug_filename(slug)
            cached_json = os.path.join(cache_dir, f"{fname}.json")
            if os.path.exists(cached_json):
                try:
                    with open(cached_json, "r", encoding="utf-8") as f:
                        cached_payload = json.load(f)
                    cached_article = cached_payload.get("article")
                    if isinstance(cached_article, dict):
                        body_md = html_to_markdown(cached_article.get("body_html") or "")
                        successes.append({
                            "input": raw,
                            "slug": slug,
                            "article": cached_article,
                            "body_md": body_md,
                            "cached": True,
                        })
                        if progress:
                            print(f"    -> cached, skipped", file=sys.stderr, flush=True)
                        continue
                except (OSError, json.JSONDecodeError):
                    pass  # fall through to refetch

        try:
            article = fetch_article_json(slug, timeout=timeout)
        except RuntimeError as e:
            errors.append({"input": raw, "slug": slug, "error": str(e)})
            if progress:
                print(f"    -> ERROR: {e}", file=sys.stderr, flush=True)
            if idx < total and delay > 0:
                time.sleep(delay)
            continue

        body_md = html_to_markdown(article.get("body_html") or "")
        successes.append({
            "input": raw,
            "slug": slug,
            "article": article,
            "body_md": body_md,
            "cached": False,
        })

        if idx < total and delay > 0:
            time.sleep(delay)

    return successes, errors


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def save_to_disk(
    out_dir: str,
    successes: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    parse_errors: list[tuple[str, str]],
) -> str:
    """Write JSON+MD per success and an index.json. Returns path to index."""
    os.makedirs(out_dir, exist_ok=True)
    index_successes: list[dict[str, Any]] = []
    for item in successes:
        article = item["article"]
        slug = item["slug"]
        fname = safe_slug_filename(slug)
        json_path = os.path.join(out_dir, f"{fname}.json")
        md_path = os.path.join(out_dir, f"{fname}.md")
        if not item.get("cached"):
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({"article": article}, f, ensure_ascii=False, indent=2)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(build_frontmatter(article))
                f.write("\n")
                f.write(item["body_md"])
        summary = article_summary_fields(article)
        summary["input"] = item["input"]
        summary["json_path"] = json_path
        summary["md_path"] = md_path
        summary["cached"] = item.get("cached", False)
        index_successes.append(summary)

    index_errors = [
        {"input": e["input"], "slug": e.get("slug", ""), "error": e["error"]}
        for e in errors
    ] + [
        {"input": raw, "slug": "", "error": err}
        for raw, err in parse_errors
    ]

    index_path = os.path.join(out_dir, "index.json")
    payload = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "batch_size": len(successes) + len(errors) + len(parse_errors),
        "success_count": len(successes),
        "error_count": len(errors) + len(parse_errors),
        "successes": index_successes,
        "errors": index_errors,
    }
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return index_path


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------


def _md_escape_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: max(0, n - 1)].rstrip() + "…"


def render_triage(
    successes: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    parse_errors: list[tuple[str, str]],
    *,
    preview_chars: int,
    include_previews: bool,
) -> str:
    total = len(successes) + len(errors) + len(parse_errors)
    err_count = len(errors) + len(parse_errors)
    lines: list[str] = []
    lines.append(f"# Zenn batch summary ({len(successes)}/{total} articles fetched, {err_count} errors)")
    lines.append("")

    if successes:
        lines.append("| # | Title | Author | Type | Topics | 👍 | 🔖 | Published |")
        lines.append("|---|-------|--------|------|--------|----|----|-----------|")
        for i, item in enumerate(successes, start=1):
            f = article_summary_fields(item["article"])
            topics_str = ", ".join(f["topics"]) if f["topics"] else "-"
            published_short = f["published_at"][:10] if f["published_at"] else "-"
            cached_marker = " *(cached)*" if item.get("cached") else ""
            lines.append(
                "| {i} | {emoji} {title}{cached} | @{author} | {atype} | {topics} | {likes} | {bm} | {pub} |".format(
                    i=i,
                    emoji=f["emoji"],
                    title=_md_escape_cell(_truncate(f["title"], 60)),
                    cached=cached_marker,
                    author=_md_escape_cell(f["author_username"]),
                    atype=f["article_type"],
                    topics=_md_escape_cell(_truncate(topics_str, 40)),
                    likes=f["liked_count"],
                    bm=f["bookmarked_count"],
                    pub=published_short,
                )
            )
        lines.append("")
        lines.append("### URLs")
        for i, item in enumerate(successes, start=1):
            f = article_summary_fields(item["article"])
            lines.append(f"- [{i}] {f['url']}")
        lines.append("")
    else:
        lines.append("_No articles successfully fetched._")
        lines.append("")

    if include_previews and successes:
        lines.append("## Previews")
        lines.append("")
        for i, item in enumerate(successes, start=1):
            f = article_summary_fields(item["article"])
            body = item["body_md"]
            preview = _truncate(body.strip().replace("\n\n", " ").replace("\n", " "), preview_chars)
            lines.append(f"### [{i}] {f['emoji']} {f['title']}")
            lines.append(f"_{f['url']}_  ·  {f['body_letters_count']} chars total")
            lines.append("")
            lines.append(preview)
            lines.append("")

    if err_count:
        lines.append("## Errors")
        lines.append("")
        for e in errors:
            lines.append(f"- `{e['input']}` (slug=`{e.get('slug', '')}`): {e['error']}")
        for raw, err in parse_errors:
            lines.append(f"- `{raw}`: {err}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_jsonl(
    successes: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    parse_errors: list[tuple[str, str]],
) -> str:
    out: list[str] = []
    for item in successes:
        payload = {
            "ok": True,
            "input": item["input"],
            "slug": item["slug"],
            "cached": item.get("cached", False),
            "article": item["article"],
        }
        out.append(json.dumps(payload, ensure_ascii=False))
    for e in errors:
        out.append(json.dumps({"ok": False, "input": e["input"], "slug": e.get("slug", ""), "error": e["error"]}, ensure_ascii=False))
    for raw, err in parse_errors:
        out.append(json.dumps({"ok": False, "input": raw, "slug": "", "error": err}, ensure_ascii=False))
    return "\n".join(out) + ("\n" if out else "")


def render_md_full(
    successes: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    parse_errors: list[tuple[str, str]],
) -> str:
    parts: list[str] = []
    for i, item in enumerate(successes, start=1):
        article = item["article"]
        parts.append(f"<!-- Article {i} of {len(successes)} -->")
        parts.append(build_frontmatter(article))
        parts.append("")
        parts.append(item["body_md"].rstrip())
        parts.append("")
        parts.append("---")
        parts.append("")
    if errors or parse_errors:
        parts.append("<!-- Errors -->")
        for e in errors:
            parts.append(f"- `{e['input']}`: {e['error']}")
        for raw, err in parse_errors:
            parts.append(f"- `{raw}`: {err}")
        parts.append("")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fetch_zenn_batch.py",
        description="Fetch multiple Zenn articles in one shot for cross-article analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
    # Triage 3 URLs to stdout
    fetch_zenn_batch.py URL1 URL2 URL3

    # Read URLs from a file
    fetch_zenn_batch.py --from-file urls.txt

    # Combine sources, save everything, generate index.json
    fetch_zenn_batch.py URL1 --from-file extras.txt --save

    # Lightest output for triage of a long list
    fetch_zenn_batch.py --from-file urls.txt --format metadata

    # Pipe URLs in
    grep zenn.dev notes.md | fetch_zenn_batch.py --stdin
""",
    )
    p.add_argument(
        "targets",
        nargs="*",
        help="Zenn URLs or slugs (any combination of full URLs, user/slug shorthand, or bare slugs)",
    )
    p.add_argument("--from-file", metavar="PATH", help="Read URLs/slugs from a file (one per line; # = comment)")
    p.add_argument("--stdin", action="store_true", help="Read URLs/slugs from stdin (one per line)")
    p.add_argument(
        "--format",
        choices=("triage", "metadata", "jsonl", "md_full"),
        default="triage",
        help="Output format (default: triage)",
    )
    p.add_argument(
        "--preview-chars",
        type=int,
        default=DEFAULT_PREVIEW_CHARS,
        metavar="N",
        help=f"Body preview length in triage mode (default: {DEFAULT_PREVIEW_CHARS})",
    )
    p.add_argument("--save", action="store_true", help="Persist raw JSON + MD per article + index.json under the cache dir")
    p.add_argument(
        "--out-dir",
        metavar="DIR",
        default=None,
        help=f"Directory for persisted files (implies --save). Default: ./{DEFAULT_CACHE_DIR}",
    )
    p.add_argument(
        "--skip-cached",
        action="store_true",
        help="If --save and a <slug>.json already exists in the cache, reuse it instead of refetching",
    )
    p.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        metavar="SEC",
        help=f"Sleep between successive HTTP requests (default: {DEFAULT_DELAY}s)",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        metavar="SEC",
        help=f"HTTP timeout per request (default: {DEFAULT_TIMEOUT}s)",
    )
    p.add_argument("--quiet", action="store_true", help="Suppress per-article progress on stderr")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    raw_targets = collect_targets(args)
    if not raw_targets:
        print(
            "error: no inputs. Pass URLs as positional arguments, --from-file PATH, or --stdin.",
            file=sys.stderr,
        )
        return EXIT_USAGE

    resolved, parse_errors = deduplicate_by_slug(raw_targets)
    if not resolved and parse_errors:
        for raw, err in parse_errors:
            print(f"error: {raw!r}: {err}", file=sys.stderr)
        return EXIT_USAGE

    save = args.save or args.out_dir is not None
    out_dir = args.out_dir or DEFAULT_CACHE_DIR if save else None

    successes, fetch_errors = fetch_many(
        resolved,
        timeout=args.timeout,
        delay=args.delay,
        cache_dir=out_dir if (save and args.skip_cached) else None,
        skip_cached=args.skip_cached and save,
        progress=not args.quiet,
    )

    index_path: str | None = None
    if save and out_dir is not None:
        try:
            index_path = save_to_disk(out_dir, successes, fetch_errors, parse_errors)
        except OSError as e:
            print(f"error: writing cache files: {e}", file=sys.stderr)
            return EXIT_FETCH

    if args.format == "triage":
        sys.stdout.write(render_triage(
            successes,
            fetch_errors,
            parse_errors,
            preview_chars=args.preview_chars,
            include_previews=True,
        ))
    elif args.format == "metadata":
        sys.stdout.write(render_triage(
            successes,
            fetch_errors,
            parse_errors,
            preview_chars=0,
            include_previews=False,
        ))
    elif args.format == "jsonl":
        sys.stdout.write(render_jsonl(successes, fetch_errors, parse_errors))
    elif args.format == "md_full":
        sys.stdout.write(render_md_full(successes, fetch_errors, parse_errors))

    if index_path:
        sys.stdout.write(f"\nSaved {len(successes)} article(s) to {out_dir}/\nIndex: {index_path}\n")

    if fetch_errors or parse_errors:
        return EXIT_FETCH
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
