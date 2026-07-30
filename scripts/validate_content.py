#!/usr/bin/env python3
"""Validate article source content and generated artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.kb import (  # noqa: E402
    ARTICLE_ID_RE,
    ARTICLES_OUT,
    ARTICLE_SCHEMA,
    CONTENT_ARTICLES,
    DATA_DIR,
    INDEX_SCHEMA,
    ROOT as REPO_ROOT,
    iter_article_dirs,
    load_article,
    load_site_config,
)

try:
    import jsonschema
except ImportError:  # pragma: no cover
    print("ERROR: jsonschema is required. pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


class Reporter:
    def __init__(self) -> None:
        self.ok = 0
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def success(self, msg: str) -> None:
        self.ok += 1
        print(f"OK  {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)
        print(f"WARN {msg}")

    def error(self, msg: str) -> None:
        self.errors.append(msg)
        print(f"ERR {msg}", file=sys.stderr)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    reporter = Reporter()
    try:
        article_schema = load_json(ARTICLE_SCHEMA)
        index_schema = load_json(INDEX_SCHEMA)
        config = load_site_config()
    except Exception as exc:  # noqa: BLE001
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2

    articles = []
    ids: set[str] = set()
    slugs: set[tuple[str, str]] = set()
    urls: set[str] = set()

    dirs = iter_article_dirs()
    if not dirs:
        reporter.warn("content/articles に記事がありません")

    for article_dir in dirs:
        try:
            meta = load_article(article_dir)
            public = {k: v for k, v in meta.items() if not k.startswith("_")}
            jsonschema.validate(public, article_schema)
            reporter.success(f"schema {meta['id']}")
        except Exception as exc:  # noqa: BLE001
            reporter.error(f"{article_dir}: schema/load failed: {exc}")
            continue

        if not ARTICLE_ID_RE.match(meta["id"]):
            reporter.error(f"{meta['id']}: invalid id format")
        if meta["id"] in ids:
            reporter.error(f"duplicate id: {meta['id']}")
        ids.add(meta["id"])

        slug_key = (meta["_year"], meta["slug"])
        if slug_key in slugs:
            reporter.error(f"duplicate slug in year {meta['_year']}: {meta['slug']}")
        slugs.add(slug_key)

        if meta["_url"] in urls:
            reporter.error(f"duplicate url: {meta['_url']}")
        urls.add(meta["_url"])

        for required in ("conclusion.md", "analysis.md", "prompt.txt"):
            if not (article_dir / required).exists():
                reporter.error(f"{meta['id']}: missing {required}")
            else:
                reporter.success(f"{meta['id']}: {required}")

        for agent in meta["agents"]:
            response = article_dir / agent["responseFile"]
            if not response.exists():
                reporter.error(f"{meta['id']}: missing {agent['responseFile']}")
            else:
                reporter.success(f"{meta['id']}: {agent['responseFile']}")

        for field in ("updatedAt", "lastVerifiedAt"):
            if not DATE_RE.match(str(meta.get(field, ""))):
                reporter.error(f"{meta['id']}: invalid {field}")
        if meta["publishedAt"] is not None and not DATE_RE.match(meta["publishedAt"]):
            reporter.error(f"{meta['id']}: invalid publishedAt")

        if meta["giscusTerm"] != meta["id"]:
            reporter.error(f"{meta['id']}: giscusTerm mismatch")
        else:
            reporter.success(f"{meta['id']}: giscusTerm")

        expected_dirname = f"kb-{meta['_year']}-{meta['id'].split('-')[2]}-{meta['slug']}"
        if article_dir.name != expected_dirname:
            reporter.error(
                f"{meta['id']}: directory name {article_dir.name} != {expected_dirname}"
            )

        out_html = ARTICLES_OUT / meta["_year"] / expected_dirname / "index.html"
        if not out_html.exists():
            reporter.error(f"{meta['id']}: generated HTML missing: {out_html}")
        else:
            html = out_html.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(html):
                reporter.error(f"{meta['id']}: unresolved placeholders in HTML")
            if f'rel="canonical" href="{config["baseUrl"].rstrip("/")}{meta["_url"]}"' not in html:
                # soft check: canonical contains article url path
                if meta["_url"] not in html:
                    reporter.error(f"{meta['id']}: canonical/url missing in HTML")
                else:
                    reporter.success(f"{meta['id']}: url present in HTML")
            else:
                reporter.success(f"{meta['id']}: canonical")
            if "Edit on GitHub" not in html:
                reporter.error(f"{meta['id']}: Edit on GitHub section missing")
            else:
                reporter.success(f"{meta['id']}: Edit on GitHub")
            # duplicate id attributes (naive)
            ids_in_html = re.findall(r'\bid="([^"]+)"', html)
            dup = {i for i in ids_in_html if ids_in_html.count(i) > 1}
            if dup:
                reporter.error(f"{meta['id']}: duplicate HTML ids: {sorted(dup)}")
            if "<script>alert" in html and "&lt;script&gt;alert" not in html and "alert(&quot;xss&quot;)" not in html:
                # XSS sample should be escaped in body text
                if "&lt;script&gt;" not in html and "alert(\"xss\")" in html:
                    reporter.error(f"{meta['id']}: possible unescaped script content")

        articles.append(meta)

    index_path = DATA_DIR / "articles.json"
    if index_path.exists():
        try:
            index = load_json(index_path)
            jsonschema.validate(index, index_schema)
            reporter.success("articles.json schema")
            index_ids = {a["id"] for a in index["articles"]}
            source_ids = {a["id"] for a in articles}
            if index_ids != source_ids:
                reporter.error(f"articles.json ids mismatch source={sorted(source_ids)} index={sorted(index_ids)}")
            else:
                reporter.success("articles.json ids match source")
        except Exception as exc:  # noqa: BLE001
            reporter.error(f"articles.json invalid: {exc}")
    else:
        reporter.error("data/articles.json missing")

    for path in (REPO_ROOT / "index.html", REPO_ROOT / "sitemap.xml", REPO_ROOT / "feed.xml"):
        if path.exists():
            reporter.success(f"exists {path.name}")
            if path.suffix == ".html" and PLACEHOLDER_RE.search(path.read_text(encoding="utf-8")):
                reporter.error(f"unresolved placeholders in {path.name}")
        else:
            reporter.error(f"missing {path}")

    # Internal link check: article URLs referenced from index data
    if index_path.exists():
        index = load_json(index_path)
        for item in index["articles"]:
            rel = item["url"].lstrip("/")
            target = REPO_ROOT / rel / "index.html"
            if not target.exists():
                reporter.error(f"broken internal link: {item['url']}")
            else:
                reporter.success(f"link ok {item['url']}")

    print()
    print(f"success={reporter.ok} warnings={len(reporter.warnings)} errors={len(reporter.errors)}")
    if reporter.errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
