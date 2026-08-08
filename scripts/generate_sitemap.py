#!/usr/bin/env python3
"""Generate sitemap.xml from article index."""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_index import build_index  # noqa: E402
from scripts.kb import ROOT as REPO_ROOT, load_site_config, write_text  # noqa: E402


def build_sitemap(index: dict, base_url: str) -> str:
    base = base_url.rstrip("/")
    urls = [
        ("/", None),
        ("/benchmarks/", None),
    ]
    for article in index["articles"]:
        if article["status"] not in {"published", "superseded", "archived"}:
            continue
        lastmod = article["updatedAt"]
        urls.append((article["url"], lastmod))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, lastmod in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(base + path)}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{escape(lastmod)}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    config = load_site_config()
    index = build_index()
    xml = build_sitemap(index, config["baseUrl"])
    write_text(REPO_ROOT / "sitemap.xml", xml)
    print(f"wrote {REPO_ROOT / 'sitemap.xml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
