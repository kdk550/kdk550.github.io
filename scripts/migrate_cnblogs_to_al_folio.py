#!/usr/bin/env python3
"""Migrate the local CNBlogs archive into al-folio posts.

The script intentionally uses only the Python standard library.  It is safe to
run repeatedly: it removes only known al-folio example posts, posts carrying
the ``cnblogs_post_id`` marker, and the managed CNBlogs image directory.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ARCHIVE = Path(
    "/home/magicat/00文档/blogs/20260711/archive"
)

# Files shipped by the al-folio template at the time this site was created.
# Keeping an explicit allow-list prevents a later rerun from deleting posts the
# site owner created by hand.
AL_FOLIO_EXAMPLE_POSTS = {
    "2015-03-15-formatting-and-links.md",
    "2015-05-15-images.md",
    "2015-07-15-code.md",
    "2015-10-20-disqus-comments.md",
    "2015-10-20-math.md",
    "2018-12-22-distill.md",
    "2020-09-28-twitter.md",
    "2021-07-04-diagrams.md",
    "2022-02-01-redirect.md",
    "2022-12-10-giscus-comments.md",
    "2023-03-20-table-of-contents.md",
    "2023-03-21-tables.md",
    "2023-04-24-videos.md",
    "2023-04-25-audios.md",
    "2023-04-25-sidebar-table-of-contents.md",
    "2023-05-12-custom-blockquotes.md",
    "2023-07-04-jupyter-notebook.md",
    "2023-07-12-post-bibliography.md",
    "2023-12-12-tikzjax.md",
    "2024-01-26-chartjs.md",
    "2024-01-26-echarts.md",
    "2024-01-26-geojson-map.md",
    "2024-01-27-advanced-images.md",
    "2024-01-27-code-diff.md",
    "2024-01-27-vega-lite.md",
    "2024-04-15-pseudocode.md",
    "2024-04-28-post-citation.md",
    "2024-04-29-typograms.md",
    "2024-05-01-tabs.md",
    "2024-12-04-photo-gallery.md",
    "2025-03-26-plotly.md",
}

INTERNAL_POST_LINK_RE = re.compile(
    r"\.\./(?P<post_id>\d+)/index\.md(?P<fragment>#[^)\s\"']*)?"
)
LOCAL_ASSET_RE = re.compile(
    r"(?:\.\./)+assets/(?P<asset>[A-Za-z0-9_./%+-]+)"
)
GENERATED_POST_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-cnblogs-\d+\.md$")
INLINE_TAG_RE = re.compile(
    r"^\s*(?:tags?|标签)\s*[:：]\s*(?P<values>\S.*?)\s*$",
    re.IGNORECASE,
)
TAG_SEPARATOR_RE = re.compile(r"[,，、;；]+")
FENCE_RE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})")

# Normalize the original CNBlogs categories and explicit author-written tag
# lines into one English tag vocabulary for the public site.  Original values
# are retained separately in each post's front matter and in the report.
TAXONOMY_TAG_MAP = {
    "数据结构": "data structures",
    "单调队列": "data structures",
    "堆": "data structures",
    "离散化": "data structures",
    "树状数组": "data structures",
    "线段树": "data structures",
    "栈模拟": "data structures",
    "算法基础": "algorithm basics",
    "排序": "algorithm basics",
    "模拟": "algorithm basics",
    "贪心": "algorithm basics",
    "dp": "dynamic programming",
    "动态规划": "dynamic programming",
    "Codeforces": "contest",
    "Atcoder": "contest",
    "AcWing": "contest",
    "数学": "mathematics",
    "图论": "graph theory",
    "VP": "contest",
    "计算几何": "computational geometry",
    "语法": "reflections",
    "杂但重要": "miscellaneous",
    "构造": "constructive algorithms",
    "字符串": "algorithm basics",
    "博弈": "game theory",
    "AI": "AI",
    "前缀和": "algorithm basics",
}


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Convert the archived CNBlogs Markdown into al-folio posts."
    )
    parser.add_argument(
        "--archive",
        type=Path,
        default=DEFAULT_ARCHIVE,
        help=f"CNBlogs archive root (default: {DEFAULT_ARCHIVE})",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=repo_root,
        help=f"al-folio repository root (default: {repo_root})",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Report path (default: <repo>/migration-report.json)",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def markdown_body(markdown: str, source: Path) -> str:
    """Remove the archive front matter while preserving the body byte-for-byte."""
    lines = markdown.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing YAML front matter: {source}")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :])
    raise ValueError(f"Unterminated YAML front matter: {source}")


def yaml_string(value: Any) -> str:
    """JSON strings and arrays are valid YAML flow scalars."""
    return json.dumps(value, ensure_ascii=False)


def parse_archive_datetime(value: Any, field: str, post_id: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Post {post_id} has no {field} timestamp")
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError as error:
        raise ValueError(
            f"Post {post_id} has an invalid {field} timestamp: {value!r}"
        ) from error


def format_jekyll_datetime(value: datetime) -> str:
    # CNBlogs timestamps in this archive are local China time.
    return value.strftime("%Y-%m-%d %H:%M:%S +0800")


def normalize_taxonomy(values: Any) -> list[str]:
    result: list[str] = []
    if not isinstance(values, list):
        return result
    for value in values:
        if isinstance(value, dict):
            candidate = value.get("name", "")
        else:
            candidate = value
        if isinstance(candidate, str):
            candidate = candidate.strip()
            if candidate and candidate not in result:
                result.append(candidate)
    return result


def inline_tags(markdown: str) -> list[str]:
    """Recover explicit author-written ``tag:`` lines outside code fences."""
    result: list[str] = []
    active_fence: str | None = None
    for line in markdown.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            marker = fence[0]
            if active_fence is None:
                active_fence = marker
            elif active_fence == marker:
                active_fence = None
            continue
        if active_fence is not None:
            continue
        match = INLINE_TAG_RE.match(line)
        if not match:
            continue
        for value in TAG_SEPARATOR_RE.split(match.group("values")):
            value = value.strip().strip("`*_#")
            if value and value not in result:
                result.append(value)
    return result


def normalized_english_tags(*taxonomies: list[str]) -> list[str]:
    """Merge source taxonomy values into the configured English tag set."""
    result: list[str] = []
    for values in taxonomies:
        for value in values:
            mapped = TAXONOMY_TAG_MAP.get(value)
            if mapped is None:
                raise ValueError(f"No English tag mapping configured for {value!r}")
            if mapped not in result:
                result.append(mapped)
    return result


def plain_text_from_markdown(markdown: str) -> str:
    """Extract enough plain text for a short description; never changes a post."""
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^]]*]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#*_>`~|]", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def make_description(metadata: dict[str, Any], body: str, limit: int = 160) -> str:
    body_text = plain_text_from_markdown(body)
    summary = metadata.get("summary", "")
    if isinstance(summary, str):
        # Some archived summaries contain nested entities such as &amp;gt;.
        summary = html.unescape(html.unescape(summary))
        summary = re.sub(r"<[^>]+>", " ", summary)
        summary = re.sub(r"\s+", " ", summary).strip()
    else:
        summary = ""
    # Prefer the full body over the archived summary, which was sometimes cut
    # in the middle of a word by CNBlogs' byte-length limit.
    summary = body_text or summary
    if len(summary) <= limit:
        return summary
    shortened = summary[: limit - 1].rstrip(" ,，。;；:：-")
    return shortened + "…"


def make_front_matter(
    *,
    post_id: str,
    title: str,
    published: datetime,
    updated: datetime,
    description: str,
    tags: list[str],
    source_categories: list[str],
    source_platform_tags: list[str],
    promoted_body_tags: list[str],
    canonical: str,
    source_url: str,
    permalink: str,
) -> str:
    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {yaml_string(title)}",
            f"date: {format_jekyll_datetime(published)}",
            f"updated: {format_jekyll_datetime(updated)}",
            f"description: {yaml_string(description)}",
            f"excerpt: {yaml_string(description)}",
            "categories: []",
            f"tags: {yaml_string(tags)}",
            f"source_categories: {yaml_string(source_categories)}",
            f"source_platform_tags: {yaml_string(source_platform_tags)}",
            f"promoted_body_tags: {yaml_string(promoted_body_tags)}",
            f"canonical: {yaml_string(canonical)}",
            f"source_url: {yaml_string(source_url)}",
            f"permalink: {permalink}",
            f"cnblogs_post_id: {post_id}",
            "comments: false",
            "related_posts: false",
            "---",
            "",
        ]
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def remove_template_examples(posts_dir: Path) -> list[str]:
    removed: list[str] = []
    for name in sorted(AL_FOLIO_EXAMPLE_POSTS):
        path = posts_dir / name
        if path.is_file():
            path.unlink()
            removed.append(name)
    return removed


def remove_previous_migration(posts_dir: Path) -> list[str]:
    removed: list[str] = []
    for path in sorted(posts_dir.glob("*.md")):
        if not GENERATED_POST_RE.fullmatch(path.name):
            continue
        # The marker is a second guard against deleting an unrelated file that
        # merely happens to share the generated naming convention.
        header = path.read_text(encoding="utf-8", errors="replace")[:4096]
        if re.search(r"(?m)^cnblogs_post_id:\s*\d+\s*$", header):
            path.unlink()
            removed.append(path.name)
    return removed


def discover_posts(content_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for post_dir in sorted(content_root.iterdir(), key=lambda path: path.name):
        if not post_dir.is_dir():
            continue
        markdown_path = post_dir / "index.md"
        metadata_path = post_dir / "metadata.json"
        if not markdown_path.is_file() or not metadata_path.is_file():
            continue
        metadata = read_json(metadata_path)
        post_id = str(metadata.get("post_id", post_dir.name))
        if not post_id.isdecimal():
            raise ValueError(f"Invalid post id {post_id!r} in {metadata_path}")
        if post_id != post_dir.name:
            raise ValueError(
                f"Post id mismatch: directory {post_dir.name}, metadata {post_id}"
            )
        published = parse_archive_datetime(metadata.get("published"), "published", post_id)
        records.append(
            {
                "post_id": post_id,
                "post_dir": post_dir,
                "markdown_path": markdown_path,
                "metadata": metadata,
                "published": published,
                "slug": f"cnblogs-{post_id}",
                "permalink": f"/blog/{published.year}/cnblogs-{post_id}/",
                "filename": f"{published:%Y-%m-%d}-cnblogs-{post_id}.md",
            }
        )
    ids = [record["post_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate post ids found in the archive")
    return records


def migrate(args: argparse.Namespace) -> dict[str, Any]:
    archive_root = args.archive.expanduser().resolve()
    repo_root = args.repo.expanduser().resolve()
    content_root = archive_root / "content" / "posts"
    source_assets = archive_root / "assets"
    posts_dir = repo_root / "_posts"
    managed_assets_dir = repo_root / "assets" / "img" / "blog" / "cnblogs"
    report_path = (
        args.report.expanduser().resolve()
        if args.report is not None
        else repo_root / "migration-report.json"
    )

    if not content_root.is_dir():
        raise FileNotFoundError(f"Archive posts directory not found: {content_root}")
    if not source_assets.is_dir():
        raise FileNotFoundError(f"Archive assets directory not found: {source_assets}")
    if not repo_root.is_dir():
        raise FileNotFoundError(f"al-folio repository not found: {repo_root}")

    posts_dir.mkdir(parents=True, exist_ok=True)
    records = discover_posts(content_root)
    routes = {record["post_id"]: record["permalink"] for record in records}

    removed_examples = remove_template_examples(posts_dir)
    removed_previous = remove_previous_migration(posts_dir)
    if managed_assets_dir.exists():
        shutil.rmtree(managed_assets_dir)
    managed_assets_dir.mkdir(parents=True, exist_ok=True)

    totals = {
        "posts": 0,
        "formulas": 0,
        "image_nodes": 0,
        "image_references_rewritten": 0,
        "unique_images_copied": 0,
        "code_blocks": 0,
        "tables": 0,
        "internal_links_rewritten": 0,
        "liquid_raw_wrapped_posts": 0,
        "inline_tags_inferred": 0,
        "normalized_tag_assignments": 0,
    }
    copied_assets: dict[str, dict[str, str]] = {}
    missing_assets: list[dict[str, str]] = []
    unresolved_links: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    post_mappings: list[dict[str, Any]] = []

    for record in records:
        post_id = record["post_id"]
        metadata = record["metadata"]
        try:
            source_text = record["markdown_path"].read_text(encoding="utf-8")
            body = markdown_body(source_text, record["markdown_path"])
            updated = parse_archive_datetime(
                metadata.get("updated") or metadata.get("published"),
                "updated",
                post_id,
            )
            title = str(metadata.get("title", "")).strip()
            if not title:
                raise ValueError(f"Post {post_id} has no title")

            post_link_count = 0

            def replace_post_link(match: re.Match[str]) -> str:
                nonlocal post_link_count
                target_id = match.group("post_id")
                route = routes.get(target_id)
                if route is None:
                    unresolved_links.append(
                        {
                            "source_post_id": post_id,
                            "target": match.group(0),
                            "reason": "target post id is absent from archive",
                        }
                    )
                    return match.group(0)
                post_link_count += 1
                return route + (match.group("fragment") or "")

            body = INTERNAL_POST_LINK_RE.sub(replace_post_link, body)

            asset_reference_count = 0
            post_asset_names: set[str] = set()

            def replace_asset(match: re.Match[str]) -> str:
                nonlocal asset_reference_count
                relative = match.group("asset")
                source = source_assets / relative
                if not source.is_file():
                    missing_assets.append(
                        {
                            "source_post_id": post_id,
                            "asset": relative,
                            "reference": match.group(0),
                        }
                    )
                    return match.group(0)
                destination_name = source.name
                destination = managed_assets_dir / destination_name
                source_digest = sha256(source)
                previous = copied_assets.get(destination_name)
                if previous and previous["sha256"] != source_digest:
                    raise ValueError(
                        f"Asset basename collision for {destination_name}: "
                        f"{previous['source']} and {source}"
                    )
                if not destination.exists():
                    shutil.copy2(source, destination)
                copied_assets[destination_name] = {
                    "source": str(source.relative_to(archive_root)),
                    "destination": str(destination.relative_to(repo_root)),
                    "sha256": source_digest,
                }
                post_asset_names.add(destination_name)
                asset_reference_count += 1
                return f"/assets/img/blog/cnblogs/{destination_name}"

            body = LOCAL_ASSET_RE.sub(replace_asset, body)
            if "{% endraw %}" in body:
                raise ValueError(
                    f"Post {post_id} contains a Liquid endraw tag and cannot be "
                    "safely wrapped"
                )

            canonical = str(
                metadata.get("canonical") or metadata.get("source_url") or ""
            ).strip()
            source_url = str(metadata.get("source_url") or canonical).strip()
            source_categories = normalize_taxonomy(metadata.get("categories"))
            source_platform_tags = normalize_taxonomy(metadata.get("tags"))
            recovered_tags = inline_tags(body)
            tags = normalized_english_tags(
                source_categories, source_platform_tags, recovered_tags
            )
            rich = metadata.get("rich") if isinstance(metadata.get("rich"), dict) else {}
            front_matter = make_front_matter(
                post_id=post_id,
                title=title,
                published=record["published"],
                updated=updated,
                description=make_description(metadata, body),
                tags=tags,
                source_categories=source_categories,
                source_platform_tags=source_platform_tags,
                promoted_body_tags=recovered_tags,
                canonical=canonical,
                source_url=source_url,
                permalink=record["permalink"],
            )
            output_path = posts_dir / record["filename"]
            body_suffix = "" if body.endswith("\n") else "\n"
            output_path.write_text(
                front_matter
                + "{% raw %}\n"
                + body
                + body_suffix
                + "{% endraw %}\n",
                encoding="utf-8",
            )

            remaining_links = INTERNAL_POST_LINK_RE.findall(body)
            for target_id, fragment in remaining_links:
                unresolved_links.append(
                    {
                        "source_post_id": post_id,
                        "target": f"../{target_id}/index.md{fragment or ''}",
                        "reason": "link remained after rewrite",
                    }
                )

            formulas = int(rich.get("formulas", 0) or 0)
            image_nodes = int(rich.get("images", 0) or 0)
            code_blocks = int(rich.get("code_blocks", 0) or 0)
            tables = int(rich.get("tables", 0) or 0)
            totals["posts"] += 1
            totals["formulas"] += formulas
            totals["image_nodes"] += image_nodes
            totals["image_references_rewritten"] += asset_reference_count
            totals["code_blocks"] += code_blocks
            totals["tables"] += tables
            totals["internal_links_rewritten"] += post_link_count
            totals["liquid_raw_wrapped_posts"] += 1
            totals["inline_tags_inferred"] += len(recovered_tags)
            totals["normalized_tag_assignments"] += len(tags)
            post_mappings.append(
                {
                    "post_id": post_id,
                    "title": title,
                    "source": str(record["markdown_path"].relative_to(archive_root)),
                    "destination": str(output_path.relative_to(repo_root)),
                    "permalink": record["permalink"],
                    "published": metadata.get("published"),
                    "updated": metadata.get("updated"),
                    "categories": [],
                    "tags": tags,
                    "source_categories": source_categories,
                    "source_platform_tags": source_platform_tags,
                    "inline_tags_inferred": recovered_tags,
                    "canonical": canonical,
                    "source_url": source_url,
                    "formulas": formulas,
                    "image_nodes": image_nodes,
                    "image_references_rewritten": asset_reference_count,
                    "unique_images": sorted(post_asset_names),
                    "code_blocks": code_blocks,
                    "tables": tables,
                    "internal_links_rewritten": post_link_count,
                }
            )
        except Exception as error:  # Continue so the report identifies every bad post.
            errors.append(
                {
                    "post_id": post_id,
                    "source": str(record["markdown_path"]),
                    "error": f"{type(error).__name__}: {error}",
                }
            )

    totals["unique_images_copied"] = len(copied_assets)
    generated_posts = sorted(path.name for path in posts_dir.glob("*-cnblogs-*.md"))
    remaining_example_posts = sorted(
        name for name in AL_FOLIO_EXAMPLE_POSTS if (posts_dir / name).exists()
    )

    report: dict[str, Any] = {
        "migration_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(archive_root),
        "repository_root": str(repo_root),
        "managed_image_directory": str(managed_assets_dir.relative_to(repo_root)),
        "slug_policy": "cnblogs-<post_id>",
        "permalink_policy": "/blog/<year>/cnblogs-<post_id>/",
        "taxonomy_policy": "merge source categories and explicit body tags into English tags",
        "taxonomy_tag_map": TAXONOMY_TAG_MAP,
        "normalized_tags": sorted(
            {
                tag
                for mapping in post_mappings
                for tag in mapping.get("tags", [])
            }
        ),
        "source_posts_discovered": len(records),
        "totals": totals,
        "generated_post_files": len(generated_posts),
        "official_example_posts_removed": removed_examples,
        "previous_generated_posts_removed": removed_previous,
        "remaining_official_example_posts": remaining_example_posts,
        "copied_assets": [copied_assets[name] for name in sorted(copied_assets)],
        "missing_assets": missing_assets,
        "unresolved_links": unresolved_links,
        "errors": errors,
        "post_mappings": post_mappings,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    args = parse_args()
    try:
        report = migrate(args)
    except Exception as error:
        print(f"migration failed: {type(error).__name__}: {error}", file=sys.stderr)
        return 2

    summary = {
        "source_posts_discovered": report["source_posts_discovered"],
        "totals": report["totals"],
        "generated_post_files": report["generated_post_files"],
        "official_example_posts_removed": len(
            report["official_example_posts_removed"]
        ),
        "remaining_official_example_posts": len(
            report["remaining_official_example_posts"]
        ),
        "missing_assets": len(report["missing_assets"]),
        "unresolved_links": len(report["unresolved_links"]),
        "errors": len(report["errors"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if (
        report["errors"]
        or report["missing_assets"]
        or report["unresolved_links"]
        or report["remaining_official_example_posts"]
        or report["totals"]["posts"] != report["source_posts_discovered"]
        or report["generated_post_files"] != report["source_posts_discovered"]
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
