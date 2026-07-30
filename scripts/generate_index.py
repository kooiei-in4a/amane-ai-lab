#!/usr/bin/env python3
"""Generate data/articles.json from content/articles."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.kb import DATA_DIR, iter_article_dirs, load_article, write_json  # noqa: E402


def build_index() -> dict:
    articles = []
    for article_dir in iter_article_dirs():
        meta = load_article(article_dir)
        articles.append(
            {
                "id": meta["id"],
                "slug": meta["slug"],
                "title": meta["title"],
                "description": meta["description"],
                "status": meta["status"],
                "publishedAt": meta["publishedAt"],
                "updatedAt": meta["updatedAt"],
                "lastVerifiedAt": meta["lastVerifiedAt"],
                "tags": meta["tags"],
                "agents": [a["name"] for a in meta["agents"]],
                "url": meta["_url"],
                "year": meta["_year"],
            }
        )
    # Stable ordering: updatedAt desc, then id
    articles.sort(key=lambda a: (a["updatedAt"], a["id"]), reverse=True)
    return {
        "schemaVersion": 1,
        "generatedFrom": "content/articles",
        "articles": articles,
    }


def main() -> int:
    index = build_index()
    write_json(DATA_DIR / "articles.json", index)
    # tags aggregate
    tags = sorted({t for a in index["articles"] for t in a["tags"]})
    write_json(DATA_DIR / "tags.json", {"schemaVersion": 1, "tags": tags})
    print(f"wrote {DATA_DIR / 'articles.json'} ({len(index['articles'])} articles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
