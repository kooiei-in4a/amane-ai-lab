#!/usr/bin/env python3
"""Create a new article scaffold under content/articles/."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.kb import (  # noqa: E402
    ARTICLE_ID_RE,
    CONTENT_ARTICLES,
    DIR_NAME_RE,
    ROOT,
    iter_article_dirs,
    load_article,
    write_json,
    write_text,
)

RETIRED_IDS_PATH = ROOT / "content" / "retired-article-ids.json"


def load_retired_ids() -> set[str]:
    if not RETIRED_IDS_PATH.exists():
        return set()
    data = json.loads(RETIRED_IDS_PATH.read_text(encoding="utf-8"))
    ids = data.get("ids", [])
    if not isinstance(ids, list):
        raise SystemExit(f"invalid retired ids file: {RETIRED_IDS_PATH}")
    return {str(item) for item in ids}


def next_article_id(year: str) -> str:
    """Allocate the next ID for a year without reusing live or retired IDs."""

    max_seq = 0
    for article_dir in iter_article_dirs():
        meta = json.loads((article_dir / "article.json").read_text(encoding="utf-8"))
        m = ARTICLE_ID_RE.match(meta["id"])
        if not m:
            continue
        if m.group(1) == year:
            max_seq = max(max_seq, int(m.group(2)))
    for retired_id in load_retired_ids():
        m = ARTICLE_ID_RE.match(retired_id)
        if m and m.group(1) == year:
            max_seq = max(max_seq, int(m.group(2)))
    return f"KB-{year}-{max_seq + 1:04d}"


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        raise SystemExit("slug を生成できませんでした。--slug を指定してください。")
    return s[:80]


def reject_duplicates(article_id: str, slug: str, year: str) -> None:
    if article_id in load_retired_ids():
        raise SystemExit(f"削除済み記事IDは再利用できません: {article_id}")
    for article_dir in iter_article_dirs():
        meta = load_article(article_dir)
        if meta["id"] == article_id:
            raise SystemExit(f"記事IDが重複しています: {article_id}")
        if meta["slug"] == slug and meta["_year"] == year:
            raise SystemExit(f"slugが同年で重複しています: {slug}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new knowledge-base article scaffold")
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", default="")
    parser.add_argument("--year", default=str(date.today().year))
    parser.add_argument("--description", default="")
    args = parser.parse_args()

    year = args.year
    if not re.fullmatch(r"\d{4}", year):
        raise SystemExit("--year は YYYY 形式で指定してください")

    slug = args.slug or slugify(args.title)
    article_id = next_article_id(year)
    seq = article_id.split("-")[2]
    dirname = f"kb-{year}-{seq}-{slug}"
    if not DIR_NAME_RE.match(dirname):
        raise SystemExit(f"不正なディレクトリ名: {dirname}")

    reject_duplicates(article_id, slug, year)

    today = date.today().isoformat()
    article_dir = CONTENT_ARTICLES / year / dirname
    if article_dir.exists():
        raise SystemExit(f"既に存在します: {article_dir}")

    responses = article_dir / "responses"
    responses.mkdir(parents=True, exist_ok=False)

    meta = {
        "schemaVersion": 1,
        "id": article_id,
        "slug": slug,
        "title": args.title,
        "description": args.description or f"{args.title} の検証記録。",
        "status": "draft",
        "publishedAt": None,
        "updatedAt": today,
        "lastVerifiedAt": today,
        "tags": [],
        "agents": [
            {
                "name": "ChatGPT",
                "model": "REPLACE_ME",
                "responseFile": "responses/chatgpt.md",
                "executedAt": today,
                "webSearch": False,
                "attachmentsUsed": False,
                "integrity": "raw",
                "notes": None,
            }
        ],
        "giscusTerm": article_id,
        "supersededBy": None,
    }
    write_json(article_dir / "article.json", meta)
    write_text(
        article_dir / "background.md",
        "# 検討に至った背景\n\n（調査に至った経緯を書く）\n",
    )
    write_text(article_dir / "prompt.txt", "（入力プロンプトを書く）\n")
    write_text(responses / "chatgpt.md", "# ChatGPT回答\n\n（回答を貼る）\n")
    write_text(article_dir / "analysis.md", "# 2回答の合成\n\n（合成結果を書く）\n")
    write_text(
        article_dir / "analysis-plain.md",
        "# 2回答の合成（わかりやすい説明）\n\n（平易な合成を書く）\n",
    )
    write_text(article_dir / "conclusion.md", "# 合成結果の要約\n\n（要約を書く）\n")
    write_text(
        article_dir / "conclusion-plain.md",
        "# 合成結果の要約（わかりやすい説明）\n\n（平易な要約を書く）\n",
    )

    print(f"created: {article_dir}")
    print(f"id: {article_id}")
    print(f"slug: {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
