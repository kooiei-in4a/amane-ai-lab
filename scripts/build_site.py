#!/usr/bin/env python3
"""Build static site pages from content/articles source of truth."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_feed import build_feed  # noqa: E402
from scripts.generate_index import build_index  # noqa: E402
from scripts.generate_sitemap import build_sitemap  # noqa: E402
from scripts.kb import (  # noqa: E402
    ARTICLES_OUT,
    DATA_DIR,
    ROOT as REPO_ROOT,
    html_escape,
    iter_article_dirs,
    load_article,
    load_site_config,
    markdown_to_html,
    read_text,
    render_template,
    write_json,
    write_text,
)


REQUIRED_FILES = ("article.json", "conclusion.md", "analysis.md", "prompt.txt")


def validate_schema(meta: dict) -> None:
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("jsonschema が必要です: pip install -r requirements.txt") from exc

    schema = json.loads((REPO_ROOT / "agents" / "schemas" / "article.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(meta, schema)


def render_agent_sections(meta: dict) -> str:
    parts: list[str] = []
    article_dir: Path = meta["_dir"]
    for agent in meta["agents"]:
        response_path = article_dir / agent["responseFile"]
        if not response_path.exists():
            raise FileNotFoundError(f"missing response: {response_path}")
        body_md = read_text(response_path)
        body_html = markdown_to_html(body_md)
        notes = agent.get("notes") or ""
        notes_html = (
            f'    <p class="agent-notes">{html_escape(notes)}</p>\n' if notes else ""
        )
        parts.append(
            f"""
<section class="agent-response" data-agent="{html_escape(agent['name'])}">
  <details>
    <summary>
      <span class="agent-name">{html_escape(agent['name'])}</span>
      <span class="agent-meta">{html_escape(agent['model'])} / {html_escape(agent['executedAt'])} / integrity={html_escape(agent['integrity'])}</span>
    </summary>
    <dl class="agent-facts">
      <div><dt>Web検索</dt><dd>{"あり" if agent["webSearch"] else "なし"}</dd></div>
      <div><dt>添付</dt><dd>{"あり" if agent["attachmentsUsed"] else "なし"}</dd></div>
      <div><dt>完全性</dt><dd>{html_escape(agent["integrity"])}</dd></div>
    </dl>
{notes_html}    <div class="agent-body prose">{body_html}</div>
  </details>
</section>
""".strip()
        )
    return "\n".join(parts)


def build_article_html(meta: dict, config: dict) -> str:
    article_dir: Path = meta["_dir"]
    for name in REQUIRED_FILES:
        if not (article_dir / name).exists():
            raise FileNotFoundError(f"missing {name} in {article_dir}")

    conclusion_html = markdown_to_html(read_text(article_dir / "conclusion.md"))
    analysis_html = markdown_to_html(read_text(article_dir / "analysis.md"))
    prompt_text = read_text(article_dir / "prompt.txt")
    agents_html = render_agent_sections(meta)

    base = config["baseUrl"].rstrip("/")
    page_url = base + meta["_url"]
    edit_url = (
        f"{config['repository']}/tree/main/content/articles/"
        f"{meta['_year']}/{meta['_dirname']}/"
    )
    giscus = config["giscus"]
    giscus_attrs = "\n".join(
        [
            f'  data-repo="{html_escape(giscus["repo"])}"',
            f'  data-repo-id="{html_escape(giscus["repoId"])}"',
            f'  data-category="{html_escape(giscus["category"])}"',
            f'  data-category-id="{html_escape(giscus["categoryId"])}"',
            f'  data-mapping="{html_escape(giscus["mapping"])}"',
            f'  data-term="{html_escape(meta["giscusTerm"])}"',
            f'  data-strict="{html_escape(giscus["strict"])}"',
            f'  data-reactions-enabled="{html_escape(giscus["reactionsEnabled"])}"',
            f'  data-emit-metadata="{html_escape(giscus["emitMetadata"])}"',
            f'  data-input-position="{html_escape(giscus["inputPosition"])}"',
            f'  data-theme="{html_escape(giscus["theme"])}"',
            f'  data-lang="{html_escape(giscus["lang"])}"',
            f'  data-loading="{html_escape(giscus["loading"])}"',
        ]
    )

    tags_html = "".join(f'<li>{html_escape(t)}</li>' for t in meta["tags"])
    published = meta["publishedAt"] or "未公開"

    return render_template(
        "article.html",
        {
            "LANG": html_escape(config["language"]),
            "SITE_TITLE": html_escape(config["siteTitle"]),
            "SITE_NAME": html_escape(config["siteName"]),
            "TITLE": html_escape(meta["title"]),
            "DESCRIPTION": html_escape(meta["description"]),
            "CANONICAL_URL": html_escape(page_url),
            "OG_URL": html_escape(page_url),
            "ARTICLE_ID": html_escape(meta["id"]),
            "STATUS": html_escape(meta["status"]),
            "PUBLISHED_AT": html_escape(published),
            "UPDATED_AT": html_escape(meta["updatedAt"]),
            "LAST_VERIFIED_AT": html_escape(meta["lastVerifiedAt"]),
            "TAGS_HTML": tags_html,
            "CONCLUSION_HTML": conclusion_html,
            "ANALYSIS_HTML": analysis_html,
            "PROMPT_TEXT": html_escape(prompt_text),
            "AGENTS_HTML": agents_html,
            "EDIT_URL": html_escape(edit_url),
            "REPO_URL": html_escape(config["repository"]),
            "GISCUS_ATTRS": giscus_attrs,
            "HOME_HREF": html_escape(base + "/"),
            "ASSET_PREFIX": html_escape("../../.."),
        },
    )


def build_home_html(index: dict, config: dict) -> str:
    base = config["baseUrl"].rstrip("/")
    return render_template(
        "index.html",
        {
            "LANG": html_escape(config["language"]),
            "SITE_TITLE": html_escape(config["siteTitle"]),
            "SITE_NAME": html_escape(config["siteName"]),
            "DESCRIPTION": html_escape(config["description"]),
            "CANONICAL_URL": html_escape(base + "/"),
            "OG_URL": html_escape(base + "/"),
            "REPO_URL": html_escape(config["repository"]),
            "ARTICLE_COUNT": str(len(index["articles"])),
            "ASSET_PREFIX": ".",
        },
    )


def reset_articles_output(output_dir: Path = ARTICLES_OUT) -> None:
    """Recreate the generated article tree so removed sources cannot stay public."""

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Keep the directory in Git even when no articles are published.
    (output_dir / ".gitkeep").write_text("", encoding="utf-8")


def main() -> int:
    config = load_site_config()
    rendered_articles: list[tuple[dict, str]] = []

    # Render every source successfully before replacing committed generated pages.
    # This prevents an invalid later article from leaving a partially refreshed tree.
    for article_dir in iter_article_dirs():
        meta = load_article(article_dir)
        public_meta = {k: v for k, v in meta.items() if not k.startswith("_")}
        validate_schema(public_meta)
        rendered_articles.append((meta, build_article_html(meta, config)))

    reset_articles_output()
    for meta, html in rendered_articles:
        out_dir = ARTICLES_OUT / meta["_year"] / meta["_dirname"]
        write_text(out_dir / "index.html", html)

    index = build_index()
    write_json(DATA_DIR / "articles.json", index)
    tags = sorted({t for a in index["articles"] for t in a["tags"]})
    write_json(DATA_DIR / "tags.json", {"schemaVersion": 1, "tags": tags})
    write_text(REPO_ROOT / "sitemap.xml", build_sitemap(index, config["baseUrl"]))
    write_text(REPO_ROOT / "feed.xml", build_feed(index, config))
    write_text(REPO_ROOT / "index.html", build_home_html(index, config))

    print(f"built {len(rendered_articles)} article(s)")
    print("wrote data/articles.json, sitemap.xml, feed.xml, index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
