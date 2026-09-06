#!/usr/bin/env python3
"""One-time normalization of the imported blog posts.

This utility is intentionally kept separate from the historical CNBlogs
migration script.  It gives the repository a reproducible, reviewable mapping
from the old imported filenames to the unified English slugs used by the site.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


SLUGS = {
    "15022440": "cin-number-input-and-character-encounter",
    "15047098": "noip-2015-junior-mine-sweeper-game",
    "15050262": "counting-sort-luogu-p1271-student-council-election",
    "15050384": "selection-sort",
    "15057867": "quick-sort-template-luogu-p1177",
    "15059076": "luogu-p2089-roast-chicken",
    "15061019": "memset-scope-and-initialization-errors-luogu-p1618",
    "15068443": "binary-search-and-binary-answer",
    "15070230": "cpp-syntax-notes-ternary-binary-typedef-define-vector-union",
    "15074331": "vector-and-shift-operator-parse-error",
    "15077000": "queue",
    "15077139": "self-reflection-no-1",
    "15080790": "luogu-p2615-magic-square",
    "15089329": "luogu-p1009-sum-of-factorials",
    "15089397": "swap-two-variables",
    "15145188": "a-to-the-b-fast-power",
    "15526764": "computational-geometry-uva-11178-morleys-theorem",
    "15526781": "current-learning-state",
    "15558982": "uva-11437-triangle-fun",
    "15559001": "poj-2318-acwing-2983-toy",
    "15559024": "poj-3304",
    "15559029": "usaco-5-1-fencing-the-cows-convex-hull",
    "15559062": "shoi-2012-credit-card-convex-hull",
    "15559073": "cqoi-2006-convex-polygon-half-plane-intersection",
    "15559110": "that-nice-euler-circuit-uvalive-3263",
    "15570283": "uva-11800-determine-the-shape",
    "15605008": "educational-codeforces-round-117-ab",
    "15612896": "icpc-2021-shanghai-warmup-two-point-removal",
    "16084546": "march-notes",
    "16102198": "april-notes",
    "16111971": "cpp-complex-number-class",
    "16175918": "date-class-tomorrows-date",
    "16176722": "uva-10104",
    "16205079": "uva-10815-andys-first-dictionary",
    "16206292": "uva-156-ananagrams",
    "16209267": "stl-algorithm-summary",
    "16246867": "uva-227-puzzle",
    "16248802": "tokitsukaze-strange-inequality-codeforces-round-789",
    "16262095": "friend-function-distance-between-two-points",
    "16276160": "pythagorean-triples-and-number-theory-exercises",
    "16289041": "teacher-cadre-inheritance-homework",
    "16301119": "uva-1589-xiangqi",
    "16358925": "date-operator-overload-homework",
    "16535093": "dag-topological-sort-template",
    "16535143": "luogu-p5318-document-search",
    "16535165": "luogu-p3916-graph-traversal",
    "16535187": "luogu-p1113-jobs",
    "16535206": "luogu-p4017-maximum-food-chain-count",
    "16535223": "luogu-p1807-longest-path",
    "16535303": "luogu-p1127-word-chain-euler-path",
    "16535330": "luogu-p2853-cow-picnic",
    "16535413": "luogu-p1347-ranking",
    "16535716": "gardener-and-tree-topological-sort",
    "16535726": "codeforces-round-744-vp-abde",
    "16536494": "codeforces-round-762-vp-abce",
    "16566709": "luogu-p4053-building-repair",
    "16916516": "2022-icpc-shenyang-hefei-trip",
    "16945914": "problem-solving-backlog",
    "17057781": "uva-10404",
    "17059064": "codeforces-educational-rounds-link",
    "17063289": "educational-codeforces-round-1-summary",
    "17069418": "educational-codeforces-round-2-summary",
    "17070875": "educational-codeforces-round-3-summary",
    "17282382": "scoi-2010-sequence-operations",
    "17282481": "usaco-2008-hotel-g",
    "17282538": "noi-online-1-bubble-sort",
    "17282595": "torcoder",
    "17282641": "new-year-tree",
    "17301214": "phoenix-and-beauty",
    "17301315": "plus-and-multiply",
    "17316484": "usaco-2012-flowerpot-monotonic-queue",
    "17325343": "hncpc-2022-vp-record",
    "17340896": "non-zero-segments",
    "17341063": "solve-the-maze",
    "17359861": "dynamic-segment-tree-template",
    "17360427": "segment-tree-over-values-template",
    "17364818": "persistent-segment-tree-kth-and-top-k-sum",
    "17365044": "offline-distinct-count-and-persistent-segment-tree",
    "17368435": "chemistry-experiment-segment-tree-binary-search",
    "17378153": "ehab-and-pathetic-mexs",
    "17380089": "hubei-contest-vp-mchjf-k",
    "17380982": "number-theory-block-decomposition",
    "17385691": "personal-templates",
    "17394093": "junior-students-notes",
    "17429104": "2021-sichuan-contest",
    "17455486": "atcoder-beginner-contest-304-abcdef",
    "17455881": "luogu-p4942-xiaokais-number",
    "17467464": "atcoder-beginner-contest-240-d",
    "17496565": "atcoder-beginner-contest-302-abcdef",
    "17521051": "acwing-weekly-contest-108-array-concatenation",
    "17521094": "acwing-weekly-contest-110-intelligence-pill",
    "17521119": "atcoder-beginner-contest-308-af",
    "17593730": "luogu-p1273-cable-television-network",
    "17611545": "dynamic-programming-problem-notes",
    "17616549": "problem-solving-notes-2023-08",
    "17623748": "baidu-star-preliminary-contest-1-trip",
    "17636155": "2022-icpc-asia-regionals-online-contest-1",
    "17641079": "2022-icpc-asia-regionals-online-contest-2",
    "17652057": "german-collegiate-programming-contest-2021",
    "17655905": "2020-2021-acm-icpc-asia-nanjing-regional-contest",
    "17659255": "codeforces-round-894",
    "17660205": "multiset-solvable-problem-notes",
    "17670762": "2022-icpc-asia-nanjing-regional-contest",
    "17672708": "educational-codeforces-round-5",
    "17672888": "educational-codeforces-round-15",
    "17674011": "educational-codeforces-round-23",
    "17674500": "educational-codeforces-round-6",
    "17675933": "educational-codeforces-round-7",
    "17706686": "2022-icpc-jinan-site",
    "17706702": "2021-china-collegiate-programming-contest-womens-special",
    "17713269": "2022-china-collegiate-programming-contest-womens-special",
    "17734570": "aurora-studio",
    "17734624": "2021-china-collegiate-programming-contest-harbin",
    "17735234": "2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad",
    "17745941": "2022-china-collegiate-programming-contest-ccpc-weihai-site-eajgci",
    "17755661": "algorithm-notes",
    "17786697": "three-round-assessment",
    "18440950": "final-xcpc-story",
    "19160805": "rtx-5060ti-llama-factory-deployment",
    "19161008": "npu-xinference-embedding-reranker-deployment",
    "19161022": "rtx-5060ti-xinference-setup",
}

REMOVED_FIELDS = {
    "canonical",
    "source_url",
    "source_categories",
    "source_platform_tags",
    "promoted_body_tags",
    "permalink",
    "cnblogs_post_id",
}


def clean_front_matter(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("post has no YAML front matter")
    end = next(
        (i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None
    )
    if end is None:
        raise ValueError("post has unterminated YAML front matter")
    header = [
        line for line in lines[1:end]
        if line.split(":", 1)[0].strip() not in REMOVED_FIELDS
    ]
    return "".join([lines[0], *header, lines[end:][0], *lines[end + 1 :]])


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    posts = sorted(root.joinpath("_posts").glob("*-cnblogs-*.md"))
    if len(posts) != len(SLUGS):
        raise SystemExit(f"expected {len(SLUGS)} imported posts, found {len(posts)}")

    routes: dict[str, str] = {}
    rename_plan: list[tuple[Path, Path]] = []
    for source in posts:
        match = re.fullmatch(r"(?P<date>\d{4}-\d{2}-\d{2})-cnblogs-(?P<id>\d+)\.md", source.name)
        if not match or match.group("id") not in SLUGS:
            raise SystemExit(f"unmapped post filename: {source.name}")
        date = match.group("date")
        post_id = match.group("id")
        slug = SLUGS[post_id]
        destination = root / "_posts" / f"{date}-{slug}.md"
        rename_plan.append((source, destination))
        year = date[:4]
        routes[f"/blog/{year}/cnblogs-{post_id}/"] = f"/blog/{year}/{slug}/"

    destinations = [destination for _, destination in rename_plan]
    if len(destinations) != len(set(destinations)):
        raise SystemExit("slug collision in normalization map")

    for source, _ in rename_plan:
        text = clean_front_matter(source.read_text(encoding="utf-8"))
        text = text.replace("/assets/img/blog/cnblogs/", "/assets/img/blog/posts/")
        for old_route, new_route in routes.items():
            text = text.replace(old_route, new_route)
        source.write_text(text, encoding="utf-8")

    temporary: list[tuple[Path, Path]] = []
    for index, (source, destination) in enumerate(rename_plan):
        temporary_path = root / "_posts" / f".normalize-{index:03d}.md"
        source.rename(temporary_path)
        temporary.append((temporary_path, destination))
    for temporary_path, destination in temporary:
        temporary_path.rename(destination)

    old_assets = root / "assets" / "img" / "blog" / "cnblogs"
    new_assets = root / "assets" / "img" / "blog" / "posts"
    if old_assets.exists():
        if new_assets.exists():
            raise SystemExit(f"destination already exists: {new_assets}")
        old_assets.rename(new_assets)
    print(f"normalized {len(rename_plan)} posts and moved assets to {new_assets}")


if __name__ == "__main__":
    main()
