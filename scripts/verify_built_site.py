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


EXPECTED_POSTS = 121
EXPECTED_PAGINATION_PAGES = 24
EXPECTED_MIGRATED_IMAGES = 38
EXPECTED_TAG_ARCHIVES = 11
EXPECTED_CATEGORY_ARCHIVES = 16
PAGINATION_FIRST = 2
PAGINATION_LAST = PAGINATION_FIRST + EXPECTED_PAGINATION_PAGES - 1

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
            if "mathjax" in source.lower() or "mathjax" in (
                attr_map.get("id") or ""
            ).lower():
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
        "copied_assets": len(copied_assets) if isinstance(copied_assets, list) else None,
    }
    expected = {
        "source_posts_discovered": EXPECTED_POSTS,
        "totals_posts": EXPECTED_POSTS,
        "generated_post_files": EXPECTED_POSTS,
        "post_mappings": EXPECTED_POSTS,
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
    site_root: Path,
    errors: List[Dict[str, object]],
) -> Tuple[Dict[str, object], List[Path]]:
    mappings = report.get("post_mappings")
    if not isinstance(mappings, list):
        errors.append(
            {"check": "post_html", "message": "post_mappings is not a list"}
        )
        mappings = []

    expected_paths: List[Path] = []
    invalid_mappings: List[object] = []
    for mapping in mappings:
        if not isinstance(mapping, dict) or not isinstance(mapping.get("permalink"), str):
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

    duplicates = sorted(
        relative_string(path, site_root)
        for path, count in Counter(expected_paths).items()
        if count > 1
    )
    missing = sorted(
        relative_string(path, site_root) for path in set(expected_paths) if not path.is_file()
    )
    actual = set(site_root.glob("blog/*/cnblogs-*/index.html"))
    expected_set = set(expected_paths)
    unexpected = sorted(relative_string(path, site_root) for path in actual - expected_set)

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
    if len(actual) != EXPECTED_POSTS:
        errors.append(
            {
                "check": "post_html",
                "message": f"found {len(actual)} generated post HTML files; expected {EXPECTED_POSTS}",
            }
        )

    summary = {
        "expected": EXPECTED_POSTS,
        "mapped": len(expected_paths),
        "found": len(actual),
        "missing": missing,
        "unexpected": unexpected,
        "duplicate_permalinks": duplicates,
        "invalid_mappings": len(invalid_mappings),
    }
    return summary, sorted(expected_set)


def verify_pagination(
    site_root: Path, errors: List[Dict[str, object]]
) -> Dict[str, object]:
    expected = {
        site_root / "blog" / "page" / str(page) / "index.html"
        for page in range(PAGINATION_FIRST, PAGINATION_LAST + 1)
    }
    discovered = {
        path
        for path in site_root.glob("blog/page/*/index.html")
        if path.parent.name.isdigit()
    }
    missing = sorted(relative_string(path, site_root) for path in expected - discovered)
    unexpected = sorted(relative_string(path, site_root) for path in discovered - expected)
    blog_index = site_root / "blog" / "index.html"

    if not blog_index.is_file():
        errors.append(
            {"check": "pagination", "message": "blog/index.html is missing"}
        )
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
    if len(discovered) != EXPECTED_PAGINATION_PAGES:
        errors.append(
            {
                "check": "pagination",
                "message": f"found {len(discovered)} pagination pages; expected {EXPECTED_PAGINATION_PAGES}",
            }
        )

    return {
        "blog_index_exists": blog_index.is_file(),
        "expected": EXPECTED_PAGINATION_PAGES,
        "expected_range": f"{PAGINATION_FIRST}-{PAGINATION_LAST}",
        "found": len(discovered),
        "missing": missing,
        "unexpected": unexpected,
    }


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
        destination
        for destination, count in Counter(destinations).items()
        if count > 1
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
            result[name] = {"exists": False, "contains_magicat": False, "demo_terms": []}
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
    category_archives = list(
        (site_root / "blog" / "category").glob("*/index.html")
    )
    if len(tag_archives) != EXPECTED_TAG_ARCHIVES:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": f"found {len(tag_archives)} tag archives; expected {EXPECTED_TAG_ARCHIVES}",
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
    if inferred_tags != EXPECTED_TAG_ARCHIVES:
        errors.append(
            {
                "check": "navigation_news_taxonomy",
                "message": f"migration report has {inferred_tags!r} promoted body tags; expected {EXPECTED_TAG_ARCHIVES}",
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
        "category_archives": len(category_archives),
        "promoted_body_tags": inferred_tags,
    }


def audit(repository_root: Path, report_path: Path, site_root: Path) -> Dict[str, object]:
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
    posts, post_paths = verify_posts(report, site_root, errors)
    pagination = verify_pagination(site_root, errors)
    internal_links, image_targets = verify_internal_links(site_root, parsed, errors)
    migrated_images = verify_migrated_images(
        repository_root, site_root, report, image_targets, errors
    )
    identity = verify_identity(site_root, parsed, errors)
    content_features = verify_content_features(
        site_root, post_paths, parsed, errors
    )
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
