#!/usr/bin/env python3
"""Verify the generated al-folio site against the CNBlogs migration report.

The verifier deliberately uses only the Python standard library.  It prints one
JSON document to stdout and exits with a non-zero status when any required
invariant is not satisfied.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import unquote, urlsplit


EXPECTED_MIGRATED_POSTS = 121
EXPECTED_MIGRATED_IMAGES = 38
EXPECTED_CATEGORY_ARCHIVES = 0
EXPECTED_PROMOTED_BODY_TAGS = 11
EXPECTED_CURATED_TAG_ASSIGNMENTS = 8
EXPECTED_CURATED_POST_TAGS = {
    "17282641": ["data structures"],
    "17394093": ["posts"],
    "17734570": ["posts"],
    "17755661": ["posts"],
    "17786697": ["posts"],
    "18440950": ["posts"],
    "19160805": ["AI"],
    "19161008": ["AI"],
}
CJK_RE = re.compile(r"[\u3400-\u9fff]")
TAG_ANCHOR_RE = re.compile(
    r'<a\b[^>]*href=["\'](?P<href>/blog/tag/[^"\']+)["\'][^>]*>' r"(?P<body>.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
TAG_LIST_RE = re.compile(
    r'<div\b[^>]*class=["\'][^"\']*\btag-category-list\b[^"\']*["\'][^>]*>'
    r"(?P<body>.*?)</div>",
    re.IGNORECASE | re.DOTALL,
)
POST_FILENAME_RE = re.compile(
    r"^(?P<year>\d{4})-\d{2}-\d{2}-(?P<slug>[a-z0-9][a-z0-9-]*)"
    r"\.(?:md|markdown|html)$"
)

DYNAMIC_MARKERS = ("{{", "}}", "{%", "%}", "${", "<%", "%>")
MATH_DELIMITER_RE = re.compile(r"\\\(.+?\\\)|\\\[.+?\\\]", re.DOTALL)
DEMO_TERMS = ("einstein", "al-folio")


class SiteHTMLParser(HTMLParser):
    """Collect local resource references and a few rendered-content signals."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: List[Tuple[str, str, str, int]] = []
        self.visible_text_parts: List[str] = []
        self.identity_text_parts: List[str] = []
        self._hidden_counts: Counter[str] = Counter()
        self._footer_depth = 0
        self.mathjax_loader = False
        self.highlight_nodes = 0
        self.table_nodes = 0
        self.image_nodes = 0
        self.is_article = False

    def handle_starttag(
        self, tag: str, attrs: Sequence[Tuple[str, Optional[str]]]
    ) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value for key, value in attrs if value is not None}
        line = self.getpos()[0]

        if tag in {"head", "script", "style"}:
            self._hidden_counts[tag] += 1
        if tag == "footer":
            self._footer_depth += 1

        classes = set((attr_map.get("class") or "").lower().split())
        if "highlight" in classes or "highlighter-rouge" in classes:
            self.highlight_nodes += 1
        if tag == "table":
            self.table_nodes += 1
        if tag == "img":
            self.image_nodes += 1
        if (
            tag == "meta"
            and (attr_map.get("property") or "").lower() == "og:type"
            and (attr_map.get("content") or "").lower() == "article"
        ):
            self.is_article = True

        if tag == "a" and "href" in attr_map:
            self.references.append(("html", "href", attr_map["href"], line))
        elif tag == "img":
            for attribute in ("src", "srcset"):
                if attribute in attr_map:
                    self.references.append(
                        ("image", attribute, attr_map[attribute], line)
                    )
        elif tag == "source":
            for attribute in ("src", "srcset"):
                if attribute in attr_map:
                    self.references.append(
                        ("image", attribute, attr_map[attribute], line)
                    )
        elif tag == "script" and "src" in attr_map:
            source = attr_map["src"]
            self.references.append(("script", "src", source, line))
            if (
                "mathjax" in source.lower()
                or "mathjax" in (attr_map.get("id") or "").lower()
            ):
                self.mathjax_loader = True
        elif tag == "link" and "href" in attr_map:
            rel = set((attr_map.get("rel") or "").lower().split())
            preload_as = (attr_map.get("as") or "").lower()
            if "stylesheet" in rel or ("preload" in rel and preload_as == "style"):
                self.references.append(("style", "href", attr_map["href"], line))
            elif rel.intersection({"icon", "apple-touch-icon", "mask-icon"}) or (
                "preload" in rel and preload_as == "image"
            ):
                self.references.append(("image", "href", attr_map["href"], line))
            elif "preload" in rel and preload_as == "script":
                self.references.append(("script", "href", attr_map["href"], line))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._hidden_counts and self._hidden_counts[tag] > 0:
            self._hidden_counts[tag] -= 1
        if tag == "footer" and self._footer_depth > 0:
            self._footer_depth -= 1

    def handle_data(self, data: str) -> None:
        if not any(self._hidden_counts.values()):
            self.visible_text_parts.append(data)
            # Theme attribution in the footer is expected and is not demo content.
            if self._footer_depth == 0:
                self.identity_text_parts.append(data)

    @property
    def visible_text(self) -> str:
        return " ".join(self.visible_text_parts)

    @property
    def identity_text(self) -> str:
        return " ".join(self.identity_text_parts)


def attribute_urls(attribute: str, value: str) -> Iterable[str]:
    """Yield URLs from a normal URL attribute or a responsive srcset."""

    if attribute != "srcset":
        stripped = value.strip()
        if stripped:
            yield stripped
        return

    # Only root-relative URLs are audited.  Looking for entries after either the
    # beginning of srcset or a comma avoids splitting commas inside data: URLs.
    for match in re.finditer(r"(?:^|,)\s*(/[^,\s]+)", value):
        yield match.group(1)


def normalized_local_path(raw_url: str) -> Optional[str]:
    """Return a decoded root-relative path, or None for ignored references."""

    value = html.unescape(raw_url).strip()
    if not value.startswith("/") or value.startswith("//"):
        return None
    if any(marker in value for marker in DYNAMIC_MARKERS):
        return None

    try:
        path = unquote(urlsplit(value).path)
    except ValueError:
        return None
    if not path:
        return None

    normalized = posixpath.normpath(path)
    if path.endswith("/") and normalized != "/":
        normalized += "/"
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    return normalized


def safe_site_candidate(site_root: Path, url_path: str) -> Optional[Path]:
    """Translate a normalized URL path into the site tree without traversal."""

    relative = PurePosixPath(url_path.lstrip("/"))
    if ".." in relative.parts:
        return None
    return site_root.joinpath(*relative.parts)


def resolve_site_target(site_root: Path, url_path: str) -> Optional[Path]:
    """Resolve Jekyll-style pretty URLs as files under _site."""

    candidate = safe_site_candidate(site_root, url_path)
    if candidate is None:
        return None
    if candidate.is_file():
        return candidate
    if (candidate / "index.html").is_file():
        return candidate / "index.html"
    if not PurePosixPath(url_path.rstrip("/")).suffix:
        html_candidate = candidate.with_suffix(".html")
        if html_candidate.is_file():
            return html_candidate
    return None


def relative_string(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def front_matter_text(document: str) -> str:
    """Return the leading YAML front matter without parsing YAML values."""
    lines = document.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:index])
    return ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_html_tree(
    site_root: Path, errors: List[Dict[str, object]]
) -> Dict[Path, SiteHTMLParser]:
    parsed: Dict[Path, SiteHTMLParser] = {}
    for html_file in sorted(site_root.rglob("*.html")):
        parser = SiteHTMLParser()
        try:
            parser.feed(html_file.read_text(encoding="utf-8"))
            parser.close()
        except (OSError, UnicodeError) as exc:
            errors.append(
                {
                    "check": "html_parse",
                    "message": f"Unable to read HTML: {exc}",
                    "path": relative_string(html_file, site_root),
                }
            )
            continue
        parsed[html_file] = parser
    return parsed


def verify_report_counts(
    report: Dict[str, object], errors: List[Dict[str, object]]
) -> Dict[str, object]:
    totals = report.get("totals") if isinstance(report.get("totals"), dict) else {}
    mappings = report.get("post_mappings")
    copied_assets = report.get("copied_assets")
    observed = {
        "source_posts_discovered": report.get("source_posts_discovered"),
        "totals_posts": totals.get("posts"),
        "generated_post_files": report.get("generated_post_files"),
        "post_mappings": len(mappings) if isinstance(mappings, list) else None,
        "totals_unique_images_copied": totals.get("unique_images_copied"),
        "copied_assets": (
            len(copied_assets) if isinstance(copied_assets, list) else None
        ),
    }
    expected = {
        "source_posts_discovered": EXPECTED_MIGRATED_POSTS,
        "totals_posts": EXPECTED_MIGRATED_POSTS,
        "generated_post_files": EXPECTED_MIGRATED_POSTS,
        "post_mappings": EXPECTED_MIGRATED_POSTS,
        "totals_unique_images_copied": EXPECTED_MIGRATED_IMAGES,
        "copied_assets": EXPECTED_MIGRATED_IMAGES,
    }
    for key, expected_value in expected.items():
        if observed[key] != expected_value:
            errors.append(
                {
                    "check": "migration_report",
                    "message": f"{key} is {observed[key]!r}; expected {expected_value}",
                }
            )

    for key in ("missing_assets", "unresolved_links", "errors"):
        value = report.get(key)
        if value not in (None, []):
            errors.append(
                {
                    "check": "migration_report",
                    "message": f"migration report contains non-empty {key}",
                    "count": len(value) if isinstance(value, list) else None,
                }
            )
    return {"expected": expected, "observed": observed}


def verify_posts(
    report: Dict[str, object],
    repository_root: Path,
    site_root: Path,
    parsed: Dict[Path, SiteHTMLParser],
    errors: List[Dict[str, object]],
) -> Tuple[Dict[str, object], List[Path]]:
    mappings = report.get("post_mappings")
    if not isinstance(mappings, list):
        errors.append({"check": "post_html", "message": "post_mappings is not a list"})
        mappings = []

    expected_paths: List[Path] = []
    migrated_source_names: set[str] = set()
    invalid_mappings: List[object] = []
    for mapping in mappings:
        if not isinstance(mapping, dict) or not isinstance(
            mapping.get("permalink"), str
        ):
            invalid_mappings.append(mapping)
            continue
        permalink = normalized_local_path(mapping["permalink"])
        if permalink is None:
            invalid_mappings.append(mapping.get("post_id"))
            continue
        candidate = safe_site_candidate(site_root, permalink)
        if candidate is None:
            invalid_mappings.append(mapping.get("post_id"))
            continue
        expected_paths.append(candidate / "index.html")
        destination = mapping.get("destination")
        if not isinstance(destination, str):
            invalid_mappings.append(mapping.get("post_id"))
            continue
        migrated_source_names.add(destination)

    source_post_names = {
        relative_string(path, repository_root)
        for pattern in ("*.md", "*.markdown", "*.html")
        for path in (repository_root / "_posts").glob(pattern)
        if path.is_file()
    }
    missing_migrated_sources = sorted(migrated_source_names - source_post_names)
    manual_source_names = sorted(source_post_names - migrated_source_names)
    manual_expected_paths: List[Path] = []
    invalid_manual_sources: List[str] = []
    for source_name in manual_source_names:
        source_path = repository_root / source_name
        try:
            source_text = source_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            invalid_manual_sources.append(source_name)
            continue
        source_front_matter = front_matter_text(source_text)
        if not source_front_matter:
            invalid_manual_sources.append(source_name)
            continue
        permalink_match = re.search(
            r"(?m)^permalink:\s*(?P<value>[^#\r\n]+?)\s*(?:#.*)?$",
            source_front_matter,
        )
        if permalink_match:
            permalink = permalink_match.group("value").strip().strip("\"'")
        else:
            filename_match = POST_FILENAME_RE.fullmatch(source_path.name)
            if not filename_match:
                invalid_manual_sources.append(source_name)
                continue
            date_match = re.search(
                r"(?m)^date:\s*[\"']?(?P<year>\d{4})-\d{2}-\d{2}",
                source_front_matter,
            )
            year = (
                date_match.group("year") if date_match else filename_match.group("year")
            )
            permalink = f"/blog/{year}/{filename_match.group('slug')}/"
        normalized_permalink = normalized_local_path(permalink)
        if normalized_permalink is None:
            invalid_manual_sources.append(source_name)
            continue
        candidate = safe_site_candidate(site_root, normalized_permalink)
        if candidate is None:
            invalid_manual_sources.append(source_name)
            continue
        output_path = (
            candidate
            if PurePosixPath(normalized_permalink).suffix
            else candidate / "index.html"
        )
        manual_expected_paths.append(output_path)

    duplicates = sorted(
        relative_string(path, site_root)
        for path, count in Counter(expected_paths).items()
        if count > 1
    )
    missing = sorted(
        relative_string(path, site_root)
        for path in set(expected_paths)
        if not path.is_file()
    )
    actual_migrated = set(site_root.glob("blog/*/cnblogs-*/index.html"))
    expected_set = set(expected_paths)
    unexpected = sorted(
        relative_string(path, site_root) for path in actual_migrated - expected_set
    )
    manual_expected_set = set(manual_expected_paths)
    manual_migrated_collisions = sorted(
        relative_string(path, site_root) for path in manual_expected_set & expected_set
    )
    all_expected_posts = expected_set | manual_expected_set
    missing_article_metadata = sorted(
        relative_string(path, site_root)
        for path in all_expected_posts
        if path.is_file() and not (parsed.get(path) and parsed[path].is_article)
    )
    missing_manual = sorted(
        relative_string(path, site_root)
        for path in manual_expected_set
        if not path.is_file()
    )
    duplicate_manual_permalinks = sorted(
        relative_string(path, site_root)
        for path, count in Counter(manual_expected_paths).items()
        if count > 1
    )
    manual_found = sum(path.is_file() for path in manual_expected_set)
    total_expected = EXPECTED_MIGRATED_POSTS + len(manual_source_names)
    total_found = len(
        actual_migrated | {path for path in manual_expected_set if path.is_file()}
    )

    if invalid_mappings:
        errors.append(
            {
                "check": "post_html",
                "message": "one or more post mappings have invalid permalinks",
                "values": invalid_mappings,
            }
        )
    if duplicates:
        errors.append(
            {
                "check": "post_html",
                "message": "duplicate post permalinks",
                "paths": duplicates,
            }
        )
    if missing:
        errors.append(
            {
                "check": "post_html",
                "message": "mapped post HTML files are missing",
                "paths": missing,
            }
        )
    if unexpected:
        errors.append(
            {
                "check": "post_html",
                "message": "unexpected generated CNBlogs post HTML files",
                "paths": unexpected,
            }
        )
    if missing_article_metadata:
        errors.append(
            {
                "check": "post_html",
                "message": "mapped posts are missing article metadata",
                "paths": missing_article_metadata,
            }
        )
    if missing_migrated_sources:
        errors.append(
            {
                "check": "post_html",
                "message": "migration report destinations are missing from _posts",
                "paths": missing_migrated_sources,
            }
        )
    if invalid_manual_sources:
        errors.append(
            {
                "check": "post_html",
                "message": "manual post filenames or permalinks are invalid",
                "paths": invalid_manual_sources,
            }
        )
    if duplicate_manual_permalinks:
        errors.append(
            {
                "check": "post_html",
                "message": "manual posts have duplicate permalinks",
                "paths": duplicate_manual_permalinks,
            }
        )
    if manual_migrated_collisions:
        errors.append(
            {
                "check": "post_html",
                "message": "manual posts collide with migrated permalinks",
                "paths": manual_migrated_collisions,
            }
        )
    if missing_manual:
        errors.append(
            {
                "check": "post_html",
                "message": "manual post HTML files are missing",
                "paths": missing_manual,
            }
        )
    if len(actual_migrated) != EXPECTED_MIGRATED_POSTS:
        errors.append(
            {
                "check": "post_html",
                "message": f"found {len(actual_migrated)} migrated post HTML files; expected {EXPECTED_MIGRATED_POSTS}",
            }
        )
    if total_found != total_expected:
        errors.append(
            {
                "check": "post_html",
                "message": f"found {total_found} total rendered posts; expected {total_expected}",
            }
        )

    summary = {
        "migrated_expected": EXPECTED_MIGRATED_POSTS,
        "migrated_mapped": len(expected_paths),
        "migrated_found": len(actual_migrated),
        "manual_expected": len(manual_source_names),
        "manual_found": manual_found,
        "manual_sources": manual_source_names,
        "manual_paths": sorted(
            relative_string(path, site_root) for path in manual_expected_set
        ),
        "total_expected": total_expected,
        "total_found": total_found,
        "missing": missing,
        "missing_manual": missing_manual,
        "unexpected": unexpected,
        "missing_article_metadata": missing_article_metadata,
        "missing_migrated_sources": missing_migrated_sources,
        "invalid_manual_sources": invalid_manual_sources,
        "duplicate_manual_permalinks": duplicate_manual_permalinks,
        "manual_migrated_collisions": manual_migrated_collisions,
        "duplicate_permalinks": duplicates,
        "invalid_mappings": len(invalid_mappings),
    }
    return summary, sorted(path for path in all_expected_posts if path.is_file())


def verify_pagination(
    repository_root: Path,
    site_root: Path,
    total_posts: int,
    errors: List[Dict[str, object]],
) -> Dict[str, object]:
    blog_source = repository_root / "_pages" / "blog.md"
    try:
        blog_source_text = blog_source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(
            {
                "check": "pagination",
                "message": f"cannot read blog pagination configuration: {exc}",
            }
        )
        blog_source_text = ""
    page_size_match = re.search(
        r"(?m)^\s*per_page:\s*(?P<value>\d+)\s*(?:#.*)?$", blog_source_text
    )
    per_page = int(page_size_match.group("value")) if page_size_match else 0
    if per_page <= 0:
        errors.append(
            {
                "check": "pagination",
                "message": "blog pagination per_page must be a positive integer",
            }
        )
        per_page = 1

    total_pages = max(1, (total_posts + per_page - 1) // per_page)
    expected = {
        site_root / "blog" / "page" / str(page) / "index.html"
        for page in range(2, total_pages + 1)
    }
    discovered = {
        path
        for path in site_root.glob("blog/page/*/index.html")
        if path.parent.name.isdigit()
    }
    missing = sorted(relative_string(path, site_root) for path in expected - discovered)
    unexpected = sorted(
        relative_string(path, site_root) for path in discovered - expected
    )
    blog_index = site_root / "blog" / "index.html"

    if not blog_index.is_file():
        errors.append({"check": "pagination", "message": "blog/index.html is missing"})
    if missing:
        errors.append(
            {
                "check": "pagination",
                "message": "pagination pages are missing",
                "paths": missing,
            }
        )
    if unexpected:
        errors.append(
            {
                "check": "pagination",
                "message": "unexpected pagination pages were generated",
                "paths": unexpected,
            }
        )
    if len(discovered) != len(expected):
        errors.append(
            {
                "check": "pagination",
                "message": f"found {len(discovered)} pagination pages; expected {len(expected)} for {total_posts} posts",
            }
        )

    return {
        "blog_index_exists": blog_index.is_file(),
        "post_count": total_posts,
        "per_page": per_page,
        "total_pages": total_pages,
        "expected": len(expected),
        "expected_range": f"2-{total_pages}" if total_pages > 1 else None,
        "found": len(discovered),
        "missing": missing,
        "unexpected": unexpected,
    }


def rendered_tag_links(document: str) -> Dict[str, List[str]]:
    """Return rendered tag archive routes and labels from the blog index."""
    found: Dict[str, set[str]] = defaultdict(set)
    for section in TAG_LIST_RE.finditer(document):
        for match in TAG_ANCHOR_RE.finditer(section.group("body")):
            route = normalized_local_path(match.group("href"))
            if route is None:
                continue
            route = route.rstrip("/") + "/"
            label = re.sub(r"<[^>]+>", " ", match.group("body"))
            label = " ".join(html.unescape(label).split())
            if label:
                found[route].add(label)
    return {route: sorted(labels) for route, labels in sorted(found.items())}


def verify_internal_links(
    site_root: Path,
    parsed: Dict[Path, SiteHTMLParser],
    errors: List[Dict[str, object]],
) -> Tuple[Dict[str, object], set[str]]:
    checked_by_kind: Counter[str] = Counter()
    unique_targets: set[str] = set()
    image_targets: set[str] = set()
    broken: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)

    for source, parser in parsed.items():
        source_name = relative_string(source, site_root)
        for kind, attribute, value, line in parser.references:
            for raw_url in attribute_urls(attribute, value):
                target = normalized_local_path(raw_url)
                if target is None:
                    continue
                checked_by_kind[kind] += 1
                unique_targets.add(target)
                if kind == "image":
                    image_targets.add(target)
                if resolve_site_target(site_root, target) is None:
                    broken[(kind, target)].append(
                        {
                            "source": source_name,
                            "line": line,
                            "attribute": attribute,
                            "value": raw_url,
                        }
                    )

    broken_summary: List[Dict[str, object]] = []
    for (kind, target), occurrences in sorted(broken.items()):
        broken_summary.append(
            {
                "kind": kind,
                "target": target,
                "occurrences": len(occurrences),
                "source_examples": occurrences[:5],
            }
        )
    if broken_summary:
        errors.append(
            {
                "check": "internal_links",
                "message": f"{len(broken_summary)} unique root-relative targets do not exist",
                "targets": [item["target"] for item in broken_summary],
            }
        )

    summary = {
        "html_files_scanned": len(parsed),
        "references_checked": sum(checked_by_kind.values()),
        "references_by_kind": dict(sorted(checked_by_kind.items())),
        "unique_targets": len(unique_targets),
        "broken_unique_targets": len(broken_summary),
        "broken": broken_summary,
    }
    return summary, image_targets


def verify_migrated_images(
    repository_root: Path,
    site_root: Path,
    report: Dict[str, object],
    referenced_images: set[str],
    errors: List[Dict[str, object]],
) -> Dict[str, object]:
    copied_assets = report.get("copied_assets")
    if not isinstance(copied_assets, list):
        copied_assets = []

    missing_source: List[str] = []
    missing_built: List[str] = []
    source_hash_mismatch: List[str] = []
    built_hash_mismatch: List[str] = []
    unreferenced: List[str] = []
    invalid_entries: List[object] = []
    destinations: List[str] = []

    for asset in copied_assets:
        if not isinstance(asset, dict):
            invalid_entries.append(asset)
            continue
        destination = asset.get("destination")
        expected_hash = asset.get("sha256")
        if not isinstance(destination, str) or not isinstance(expected_hash, str):
            invalid_entries.append(asset)
            continue
        relative = PurePosixPath(destination)
        if relative.is_absolute() or ".." in relative.parts:
            invalid_entries.append(destination)
            continue

        destinations.append(destination)
        source_file = repository_root.joinpath(*relative.parts)
        built_file = site_root.joinpath(*relative.parts)
        url = "/" + relative.as_posix()

        if not source_file.is_file():
            missing_source.append(destination)
        elif sha256_file(source_file) != expected_hash:
            source_hash_mismatch.append(destination)
        if not built_file.is_file():
            missing_built.append(destination)
        elif sha256_file(built_file) != expected_hash:
            built_hash_mismatch.append(destination)
        if url not in referenced_images:
            unreferenced.append(destination)

    duplicate_destinations = sorted(
        destination for destination, count in Counter(destinations).items() if count > 1
    )
    problems = {
        "missing_source": sorted(missing_source),
        "missing_built": sorted(missing_built),
        "source_hash_mismatch": sorted(source_hash_mismatch),
        "built_hash_mismatch": sorted(built_hash_mismatch),
        "unreferenced": sorted(unreferenced),
        "duplicate_destinations": duplicate_destinations,
        "invalid_entries": invalid_entries,
    }
    for name, values in problems.items():
        if values:
            errors.append(
                {
                    "check": "migrated_images",
                    "message": f"migrated image check has non-empty {name}",
                    "values": values,
                }
            )

    return {
        "expected": EXPECTED_MIGRATED_IMAGES,
        "reported": len(copied_assets),
        "source_files_verified": len(copied_assets) - len(missing_source),
        "built_files_verified": len(copied_assets) - len(missing_built),
        "references_verified": len(copied_assets) - len(unreferenced),
        **problems,
    }


def verify_identity(
    site_root: Path,
    parsed: Dict[Path, SiteHTMLParser],
    errors: List[Dict[str, object]],
) -> Dict[str, object]:
    pages = (site_root / "index.html", site_root / "blog" / "index.html")
    result: Dict[str, object] = {}
    for page in pages:
        name = relative_string(page, site_root)
        parser = parsed.get(page)
        if parser is None:
            result[name] = {
                "exists": False,
                "contains_magicat": False,
                "demo_terms": [],
            }
            errors.append(
                {"check": "identity", "message": f"identity page is missing: {name}"}
            )
            continue

        text = " ".join(parser.identity_text.lower().split())
        contains_magicat = "magicat" in text
        demo_terms = [term for term in DEMO_TERMS if term in text]
        result[name] = {
            "exists": True,
            "contains_magicat": contains_magicat,
            "demo_terms": demo_terms,
        }
        if not contains_magicat:
            errors.append(
                {"check": "identity", "message": f"{name} does not contain magicat"}
            )
        if demo_terms:
            errors.append(
                {
                    "check": "identity",
                    "message": f"{name} contains al-folio demo identity text",
                    "terms": demo_terms,
                }
            )
    return result


def verify_content_features(
    site_root: Path,
    post_paths: Sequence[Path],
    parsed: Dict[Path, SiteHTMLParser],
    errors: List[Dict[str, object]],
) -> Dict[str, object]:
    mathjax_loader_pages: List[str] = []
    formula_pages: List[str] = []
    highlight_pages: List[str] = []
    table_pages: List[str] = []
    image_pages: List[str] = []

    for post_path in post_paths:
        parser = parsed.get(post_path)
        if parser is None:
            continue
        name = relative_string(post_path, site_root)
        if parser.mathjax_loader:
            mathjax_loader_pages.append(name)
        if MATH_DELIMITER_RE.search(parser.visible_text):
            formula_pages.append(name)
        if parser.highlight_nodes:
            highlight_pages.append(name)
        if parser.table_nodes:
            table_pages.append(name)
        if parser.image_nodes:
            image_pages.append(name)

    required = {
        "mathjax_loader_pages": mathjax_loader_pages,
        "formula_markup_pages": formula_pages,
        "highlight_pages": highlight_pages,
        "table_pages": table_pages,
        "image_pages": image_pages,
    }
    for feature, pages in required.items():
        if not pages:
            errors.append(
                {
                    "check": "content_features",
                    "message": f"no migrated post demonstrates {feature}",
                }
            )

    return {
        "mathjax": {
            "loader_pages": len(mathjax_loader_pages),
            "formula_markup_pages": len(formula_pages),
        },
        "code_highlight_pages": len(highlight_pages),
        "html_table_pages": len(table_pages),
        "image_pages": len(image_pages),
    }


def verify_navigation_news_taxonomy(
    site_root: Path,
    report: Dict[str, object],
    errors: List[Dict[str, object]],
) -> Dict[str, object]:
    """Verify the English navigation, news page, and full taxonomy archives."""
    home_path = site_root / "index.html"
    news_path = site_root / "news" / "index.html"
    home = home_path.read_text(encoding="utf-8") if home_path.is_file() else ""
    news = news_path.read_text(encoding="utf-8") if news_path.is_file() else ""
    nav_targets = {"about": "/", "blog": "/blog/", "news": "/news/"}
    missing_nav = [
        label
        for label, target in nav_targets.items()
        if not re.search(
            rf'<a class="nav-link" href="{re.escape(target)}">\s*{label}\b',
            home,
            re.IGNORECASE,
        )
    ]
    if missing_nav:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "English navigation labels are missing",
                "values": missing_nav,
            }
        )

    announcement = "Launched the new website"
    if not news_path.is_file() or announcement not in news:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "news page or launch announcement is missing",
            }
        )

    tag_archives = list((site_root / "blog" / "tag").glob("*/index.html"))
    category_archives = list((site_root / "blog" / "category").glob("*/index.html"))
    tag_archive_routes = {
        f"/blog/tag/{archive.parent.name}/" for archive in tag_archives
    }
    blog_path = site_root / "blog" / "index.html"
    blog = blog_path.read_text(encoding="utf-8") if blog_path.is_file() else ""
    automatic_tag_links = rendered_tag_links(blog)
    automatic_tag_routes = set(automatic_tag_links)
    ambiguous_tag_routes = {
        route: labels
        for route, labels in automatic_tag_links.items()
        if len(labels) > 1
    }
    missing_tag_links = sorted(tag_archive_routes - automatic_tag_routes)
    missing_tag_archives = sorted(automatic_tag_routes - tag_archive_routes)
    if missing_tag_links or missing_tag_archives or ambiguous_tag_routes:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "automatic blog tag links and generated tag archives differ",
                "archives_without_links": missing_tag_links,
                "links_without_archives": missing_tag_archives,
                "ambiguous_routes": ambiguous_tag_routes,
            }
        )
    if len(category_archives) != EXPECTED_CATEGORY_ARCHIVES:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": f"found {len(category_archives)} category archives; expected {EXPECTED_CATEGORY_ARCHIVES}",
            }
        )

    totals = report.get("totals") if isinstance(report.get("totals"), dict) else {}
    inferred_tags = totals.get("inline_tags_inferred")
    if inferred_tags != EXPECTED_PROMOTED_BODY_TAGS:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": f"migration report has {inferred_tags!r} promoted body tags; expected {EXPECTED_PROMOTED_BODY_TAGS}",
            }
        )

    curated_assignments = totals.get("curated_tag_assignments")
    if curated_assignments != EXPECTED_CURATED_TAG_ASSIGNMENTS:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": f"migration report has {curated_assignments!r} curated tag assignments; expected {EXPECTED_CURATED_TAG_ASSIGNMENTS}",
            }
        )

    reported_curated_tags = report.get("curated_post_tags")
    if reported_curated_tags != EXPECTED_CURATED_POST_TAGS:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "curated post tag assignments do not match policy",
                "expected": EXPECTED_CURATED_POST_TAGS,
                "observed": reported_curated_tags,
            }
        )

    reported_tags = report.get("normalized_tags")
    normalized_tags = set(reported_tags) if isinstance(reported_tags, list) else set()
    taxonomy_tag_map = report.get("taxonomy_tag_map")
    derived_migrated_tags = {
        tag
        for tag in (
            taxonomy_tag_map.values() if isinstance(taxonomy_tag_map, dict) else []
        )
        if isinstance(tag, str)
    }
    if isinstance(reported_curated_tags, dict):
        derived_migrated_tags.update(
            tag
            for tags in reported_curated_tags.values()
            if isinstance(tags, list)
            for tag in tags
            if isinstance(tag, str)
        )
    if normalized_tags != derived_migrated_tags:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "reported migrated tags do not match the migration policy",
                "missing": sorted(derived_migrated_tags - normalized_tags),
                "unexpected": sorted(normalized_tags - derived_migrated_tags),
            }
        )
    automatic_tag_names = {
        label for labels in automatic_tag_links.values() for label in labels
    }
    missing_migrated_tags = sorted(normalized_tags - automatic_tag_names)
    if missing_migrated_tags:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "migrated tags are missing from automatic tag navigation",
                "values": missing_migrated_tags,
            }
        )

    mappings = report.get("post_mappings")
    mappings = mappings if isinstance(mappings, list) else []
    nonempty_public_categories: List[str] = []
    non_english_public_tags: List[Dict[str, object]] = []
    invalid_curated_posts: List[Dict[str, object]] = []
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        post_id = str(mapping.get("post_id", "unknown"))
        categories = mapping.get("categories")
        if isinstance(categories, list) and categories:
            nonempty_public_categories.append(post_id)
        tags = mapping.get("tags")
        expected_curated_tags = EXPECTED_CURATED_POST_TAGS.get(post_id)
        if expected_curated_tags is not None:
            if (
                mapping.get("curated_tags") != expected_curated_tags
                or tags != expected_curated_tags
            ):
                invalid_curated_posts.append(
                    {
                        "post_id": post_id,
                        "expected": expected_curated_tags,
                        "curated_tags": mapping.get("curated_tags"),
                        "tags": tags,
                    }
                )
        if isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str) and CJK_RE.search(tag):
                    non_english_public_tags.append({"post_id": post_id, "tag": tag})
    for tag in sorted(automatic_tag_names):
        if CJK_RE.search(tag):
            non_english_public_tags.append({"source": "blog navigation", "tag": tag})
    if nonempty_public_categories:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "public post categories should be empty after tag unification",
                "post_ids": nonempty_public_categories,
            }
        )
    if non_english_public_tags:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "public tags contain Chinese text",
                "values": non_english_public_tags,
            }
        )
    if invalid_curated_posts:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": "curated posts do not have their expected public tags",
                "values": invalid_curated_posts,
            }
        )

    return {
        "english_navigation": {
            "expected": sorted(nav_targets),
            "missing": missing_nav,
        },
        "news_page": news_path.is_file(),
        "launch_announcement": announcement in news,
        "tag_archives": len(tag_archives),
        "automatic_tag_links": automatic_tag_links,
        "automatic_tag_count": len(automatic_tag_names),
        "ambiguous_tag_routes": ambiguous_tag_routes,
        "archives_without_links": missing_tag_links,
        "links_without_archives": missing_tag_archives,
        "category_archives": len(category_archives),
        "promoted_body_tags": inferred_tags,
        "curated_tag_assignments": curated_assignments,
        "curated_post_tags": reported_curated_tags,
        "normalized_tags": sorted(normalized_tags),
        "nonempty_public_categories": nonempty_public_categories,
        "non_english_public_tags": non_english_public_tags,
        "invalid_curated_posts": invalid_curated_posts,
    }


def audit(
    repository_root: Path, report_path: Path, site_root: Path
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    if not report_path.is_file():
        return {
            "status": "FAIL",
            "repository_root": str(repository_root),
            "report": str(report_path),
            "site": str(site_root),
            "checks": {},
            "errors": [
                {"check": "inputs", "message": "migration report does not exist"}
            ],
        }
    if not site_root.is_dir():
        return {
            "status": "FAIL",
            "repository_root": str(repository_root),
            "report": str(report_path),
            "site": str(site_root),
            "checks": {},
            "errors": [{"check": "inputs", "message": "site directory does not exist"}],
        }

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {
            "status": "FAIL",
            "repository_root": str(repository_root),
            "report": str(report_path),
            "site": str(site_root),
            "checks": {},
            "errors": [
                {"check": "inputs", "message": f"cannot read migration report: {exc}"}
            ],
        }
    if not isinstance(report, dict):
        return {
            "status": "FAIL",
            "repository_root": str(repository_root),
            "report": str(report_path),
            "site": str(site_root),
            "checks": {},
            "errors": [
                {"check": "inputs", "message": "migration report root is not an object"}
            ],
        }

    parsed = parse_html_tree(site_root, errors)
    report_counts = verify_report_counts(report, errors)
    posts, post_paths = verify_posts(report, repository_root, site_root, parsed, errors)
    pagination = verify_pagination(
        repository_root, site_root, int(posts["total_expected"]), errors
    )
    internal_links, image_targets = verify_internal_links(site_root, parsed, errors)
    migrated_images = verify_migrated_images(
        repository_root, site_root, report, image_targets, errors
    )
    identity = verify_identity(site_root, parsed, errors)
    content_features = verify_content_features(site_root, post_paths, parsed, errors)
    navigation_news_taxonomy = verify_navigation_news_taxonomy(
        site_root, report, errors
    )

    return {
        "status": "PASS" if not errors else "FAIL",
        "repository_root": str(repository_root),
        "report": str(report_path),
        "site": str(site_root),
        "checks": {
            "migration_report": report_counts,
            "post_html": posts,
            "pagination": pagination,
            "internal_links": internal_links,
            "migrated_images": migrated_images,
            "identity": identity,
            "content_features": content_features,
            "navigation_news_taxonomy": navigation_news_taxonomy,
        },
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root,
        help="repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="migration report path (default: ROOT/migration-report.json)",
    )
    parser.add_argument(
        "--site",
        type=Path,
        help="built site path (default: ROOT/_site)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    report = (args.report or root / "migration-report.json").resolve()
    site = (args.site or root / "_site").resolve()
    result = audit(root, report, site)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
