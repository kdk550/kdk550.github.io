#!/usr/bin/env python3
"""Verify the generated al-folio site against the current repository content.

The verifier deliberately uses only the Python standard library.  It prints one
JSON document to stdout and exits with a non-zero status when any required
invariant is not satisfied.
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import unquote, urlsplit


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
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-"
    r"(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.(?:md|markdown|html)$"
)
REMOVED_FRONT_MATTER_FIELDS = {
    "canonical",
    "source_url",
    "source_categories",
    "source_platform_tags",
    "promoted_body_tags",
    "permalink",
    "cnblogs_post_id",
}
LEGACY_POST_REFERENCE_RE = re.compile(
    r"(?:cnblogs-\d+|https?://(?:www\.)?cnblogs\.com/magicat(?:/|$))",
    re.IGNORECASE,
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


def verify_current_posts(
    repository_root: Path,
    site_root: Path,
    parsed: Dict[Path, SiteHTMLParser],
    errors: List[Dict[str, object]],
) -> Tuple[Dict[str, object], List[Path]]:
    """Verify the current unified post collection without migration metadata."""
    source_paths = sorted(
        path
        for pattern in ("*.md", "*.markdown", "*.html")
        for path in (repository_root / "_posts").glob(pattern)
        if path.is_file()
    )
    expected_paths: List[Path] = []
    invalid_sources: List[str] = []
    duplicate_paths: List[str] = []
    removed_fields: List[Dict[str, object]] = []
    legacy_references: List[str] = []

    for source in source_paths:
        name = relative_string(source, repository_root)
        match = POST_FILENAME_RE.fullmatch(source.name)
        if not match:
            invalid_sources.append(name)
            continue
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            invalid_sources.append(name)
            continue
        front_matter = front_matter_text(text)
        if not front_matter:
            invalid_sources.append(name)
            continue
        found_fields = [
            line.split(":", 1)[0].strip()
            for line in front_matter.splitlines()
            if ":" in line and line.split(":", 1)[0].strip() in REMOVED_FRONT_MATTER_FIELDS
        ]
        if found_fields:
            removed_fields.append({"path": name, "fields": sorted(set(found_fields))})
        if LEGACY_POST_REFERENCE_RE.search(text):
            legacy_references.append(name)
        date_match = re.search(
            r"(?m)^date:\s*[\"']?(?P<date>\d{4}-\d{2}-\d{2})",
            front_matter,
        )
        date_value = date_match.group("date") if date_match else None
        filename_date = source.name[:10]
        try:
            date.fromisoformat(filename_date)
        except ValueError:
            invalid_sources.append(name)
            continue
        if date_value is None or date_value != filename_date:
            invalid_sources.append(name)
            continue
        year = match.group("year")
        expected = site_root / "blog" / year / match.group("slug") / "index.html"
        expected_paths.append(expected)

    for path, count in Counter(expected_paths).items():
        if count > 1:
            duplicate_paths.append(relative_string(path, site_root))

    missing = sorted(
        relative_string(path, site_root)
        for path in set(expected_paths)
        if not path.is_file()
    )
    actual_article_paths = {
        path
        for path in site_root.glob("blog/[0-9][0-9][0-9][0-9]/*/index.html")
        if path.is_file()
    }
    expected_set = set(expected_paths)
    unexpected = sorted(
        relative_string(path, site_root) for path in actual_article_paths - expected_set
    )
    missing_article_metadata = sorted(
        relative_string(path, site_root)
        for path in expected_set
        if path.is_file() and not (parsed.get(path) and parsed[path].is_article)
    )

    if invalid_sources:
        errors.append(
            {
                "check": "post_html",
                "message": "posts must use YYYY-MM-DD-lowercase-slug filenames, matching date front matter",
                "paths": invalid_sources,
            }
        )
    if removed_fields:
        errors.append(
            {
                "check": "post_front_matter",
                "message": "posts contain fields removed from the unified format",
                "posts": removed_fields,
            }
        )
    if legacy_references:
        errors.append(
            {
                "check": "post_content",
                "message": "posts contain legacy CNBlogs routes or the author's old CNBlogs URL",
                "paths": legacy_references,
            }
        )
    if duplicate_paths:
        errors.append(
            {"check": "post_html", "message": "duplicate post URLs", "paths": duplicate_paths}
        )
    if missing:
        errors.append(
            {"check": "post_html", "message": "rendered post HTML files are missing", "paths": missing}
        )
    if unexpected:
        errors.append(
            {"check": "post_html", "message": "unexpected rendered article HTML files", "paths": unexpected}
        )
    if missing_article_metadata:
        errors.append(
            {
                "check": "post_html",
                "message": "rendered posts are missing article metadata",
                "paths": missing_article_metadata,
            }
        )

    summary = {
        "source_posts": len(source_paths),
        "valid_posts": len(expected_paths),
        "rendered_posts": len(actual_article_paths),
        "expected": len(expected_set),
        "found": len(actual_article_paths & expected_set),
        "missing": missing,
        "unexpected": unexpected,
        "invalid_sources": invalid_sources,
        "removed_front_matter_fields": removed_fields,
        "legacy_references": legacy_references,
        "duplicate_urls": duplicate_paths,
        "missing_article_metadata": missing_article_metadata,
    }
    return summary, sorted(path for path in expected_set if path.is_file())


def verify_current_navigation_taxonomy(
    site_root: Path, errors: List[Dict[str, object]]
) -> Dict[str, object]:
    """Check navigation and generated tag archives for the current site."""
    home_path = site_root / "index.html"
    news_path = site_root / "news" / "index.html"
    blog_path = site_root / "blog" / "index.html"
    home = home_path.read_text(encoding="utf-8") if home_path.is_file() else ""
    news = news_path.read_text(encoding="utf-8") if news_path.is_file() else ""
    blog = blog_path.read_text(encoding="utf-8") if blog_path.is_file() else ""
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
            {"check": "navigation", "message": "navigation labels are missing", "values": missing_nav}
        )
    if not news_path.is_file():
        errors.append({"check": "navigation", "message": "news page is missing"})
    tag_archives = list((site_root / "blog" / "tag").glob("*/index.html"))
    category_archives = list((site_root / "blog" / "category").glob("*/index.html"))
    automatic_tag_links = rendered_tag_links(blog)
    archive_routes = {f"/blog/tag/{p.parent.name}/" for p in tag_archives}
    missing_links = sorted(archive_routes - set(automatic_tag_links))
    missing_archives = sorted(set(automatic_tag_links) - archive_routes)
    if missing_links or missing_archives:
        errors.append(
            {
                "check": "taxonomy",
                "message": "tag navigation and archives differ",
                "archives_without_links": missing_links,
                "links_without_archives": missing_archives,
            }
        )
    if category_archives:
        errors.append(
            {"check": "taxonomy", "message": "category archives should be empty", "paths": [str(p) for p in category_archives]}
        )
    return {
        "english_navigation": {"expected": sorted(nav_targets), "missing": missing_nav},
        "news_page": news_path.is_file(),
        "tag_archives": len(tag_archives),
        "automatic_tag_links": automatic_tag_links,
        "archives_without_links": missing_links,
        "links_without_archives": missing_archives,
        "category_archives": len(category_archives),
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
                    "message": f"no post demonstrates {feature}",
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


def audit(repository_root: Path, site_root: Path) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    if not site_root.is_dir():
        return {
            "status": "FAIL",
            "repository_root": str(repository_root),
            "site": str(site_root),
            "checks": {},
            "errors": [{"check": "inputs", "message": "site directory does not exist"}],
        }

    parsed = parse_html_tree(site_root, errors)
    posts, post_paths = verify_current_posts(repository_root, site_root, parsed, errors)
    pagination = verify_pagination(
        repository_root, site_root, int(posts["expected"]), errors
    )
    internal_links, image_targets = verify_internal_links(site_root, parsed, errors)
    image_root = repository_root / "assets" / "img" / "blog" / "posts"
    source_images = (
        {
            "/" + path.relative_to(repository_root).as_posix()
            for path in image_root.rglob("*")
            if path.is_file()
        }
        if image_root.is_dir()
        else set()
    )
    referenced_post_images = {
        target
        for target in image_targets
        if target.startswith("/assets/img/blog/posts/")
    }
    missing_source_images = sorted(referenced_post_images - source_images)
    if missing_source_images:
        errors.append(
            {
                "check": "images",
                "message": "rendered posts reference images absent from the repository",
                "paths": missing_source_images,
            }
        )
    images = {
        "source_files": len(source_images),
        "referenced_post_files": len(referenced_post_images),
        "missing_source_files": missing_source_images,
        "unreferenced_source_files": sorted(source_images - referenced_post_images),
    }
    identity = verify_identity(site_root, parsed, errors)
    content_features = verify_content_features(site_root, post_paths, parsed, errors)
    navigation_news_taxonomy = verify_current_navigation_taxonomy(site_root, errors)

    return {
        "status": "PASS" if not errors else "FAIL",
        "repository_root": str(repository_root),
        "site": str(site_root),
        "checks": {
            "post_html": posts,
            "pagination": pagination,
            "internal_links": internal_links,
            "images": images,
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
        "--site",
        type=Path,
        help="built site path (default: ROOT/_site)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    site = (args.site or root / "_site").resolve()
    result = audit(root, site)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
