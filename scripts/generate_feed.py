#!/usr/bin/env python3
"""Generate Atom feed.xml from article index."""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_index import build_index  # noqa: E402
from scripts.kb import ROOT as REPO_ROOT, load_site_config, write_text  # noqa: E402


def atom_date(day: str | None) -> str:
    if not day:
        return "1970-01-01T00:00:00Z"
    return f"{day}T00:00:00Z"


def build_feed(index: dict, config: dict) -> str:
    base = config["baseUrl"].rstrip("/")
    title = escape(config["siteTitle"])
    entries = [
        a
        for a in index["articles"]
        if a["status"] in {"published", "superseded", "archived"}
    ]
    updated = max((a["updatedAt"] for a in entries), default="1970-01-01")
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <title>{title}</title>",
        f'  <link href="{escape(base)}/" rel="alternate"/>',
        f'  <link href="{escape(base)}/feed.xml" rel="self"/>',
        f"  <id>{escape(base)}/</id>",
        f"  <updated>{atom_date(updated)}</updated>",
        f"  <subtitle>{escape(config['description'])}</subtitle>",
    ]
    for article in entries:
        url = base + article["url"]
        lines.extend(
            [
                "  <entry>",
                f"    <title>{escape(article['title'])}</title>",
                f'    <link href="{escape(url)}" rel="alternate"/>',
                f"    <id>{escape(url)}</id>",
                f"    <updated>{atom_date(article['updatedAt'])}</updated>",
                f"    <published>{atom_date(article['publishedAt'] or article['updatedAt'])}</published>",
                f'    <summary type="text">{escape(article["description"])}</summary>',
                "  </entry>",
            ]
        )
    lines.append("</feed>")
    return "\n".join(lines) + "\n"


def main() -> int:
    config = load_site_config()
    index = build_index()
    xml = build_feed(index, config)
    write_text(REPO_ROOT / "feed.xml", xml)
    print(f"wrote {REPO_ROOT / 'feed.xml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
