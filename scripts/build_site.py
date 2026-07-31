#!/usr/bin/env python3
"""Build static site pages from content/articles source of truth."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_feed import build_feed  # noqa: E402
from scripts.generate_index import build_index  # noqa: E402
from scripts.generate_sitemap import build_sitemap  # noqa: E402
from scripts.kb import (  # noqa: E402
    ARTICLES_OUT,
    DATA_DIR,
    ROOT as REPO_ROOT,
    add_heading_ids,
    agent_slug,
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


REQUIRED_FILES = (
    "article.json",
    "background.md",
    "conclusion.md",
    "conclusion-plain.md",
    "analysis.md",
    "analysis-plain.md",
    "prompt.txt",
)
SUMMARY_SOURCE = "conclusion-plain.md"
TLDR_FILENAME = "tldr.json"


def build_summary_parts(conclusion_md: str) -> tuple[str, str]:
    """Build table-of-contents HTML and body HTML with section anchors."""

    headings = re.findall(r"^## (.+)$", conclusion_md, re.MULTILINE)
    toc_html = (
        '<nav class="summary-toc" aria-label="目次">'
        '<h2 class="summary-toc-title">目次</h2><ol>'
    )
    for index, title in enumerate(headings, start=1):
        toc_html += (
            f'<li><a href="#section-{index}">{html_escape(title)}</a></li>'
        )
    toc_html += "</ol></nav>"

    body_html = markdown_to_html(conclusion_md)
    counter = {"value": 0}

    def add_section_id(match: re.Match[str]) -> str:
        counter["value"] += 1
        return f'<h2 id="section-{counter["value"]}">'

    body_html = re.sub(r"<h2>", add_section_id, body_html)
    return toc_html, body_html


def build_summary_document_html(meta: dict, config: dict) -> str:
    article_dir: Path = meta["_dir"]
    conclusion_md = read_text(article_dir / SUMMARY_SOURCE)
    toc_html, body_html = build_summary_parts(conclusion_md)

    base = config["baseUrl"].rstrip("/")
    article_url = base + meta["_url"]
    summary_url = article_url + "summary/"
    first_line = conclusion_md.splitlines()[0].lstrip("# ").strip() if conclusion_md else meta["title"]

    return render_template(
        "summary-document.html",
        {
            "LANG": html_escape(config["language"]),
            "SITE_TITLE": html_escape(config["siteTitle"]),
            "SITE_NAME": html_escape(config["siteName"]),
            "TITLE": html_escape(meta["title"]),
            "DESCRIPTION": html_escape(meta["description"]),
            "CANONICAL_URL": html_escape(summary_url),
            "OG_URL": html_escape(summary_url),
            "ARTICLE_ID": html_escape(meta["id"]),
            "UPDATED_AT": html_escape(meta["updatedAt"]),
            "SUMMARY_TITLE": html_escape(first_line or "3ソース統合サマリー"),
            "SUMMARY_SUBTITLE": html_escape(
                "合成結果を、わかりやすい言葉で短くまとめた資料版。"
            ),
            "TOC_HTML": toc_html,
            "BODY_HTML": body_html,
            "ARTICLE_HREF": html_escape(article_url),
            "HOME_HREF": html_escape(base + "/"),
            "REPO_URL": html_escape(config["repository"]),
            "ASSET_PREFIX": html_escape("../../../.."),
        },
    )


def validate_schema(meta: dict) -> None:
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("jsonschema が必要です: pip install -r requirements.txt") from exc

    schema = json.loads((REPO_ROOT / "agents" / "schemas" / "article.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(meta, schema)


def load_tldr(article_dir: Path) -> list[dict[str, Any]]:
    path = article_dir / TLDR_FILENAME
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        raise ValueError(f"invalid {TLDR_FILENAME}: schemaVersion must be 1")
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError(f"invalid {TLDR_FILENAME}: items must be a list")
    cleaned: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"invalid {TLDR_FILENAME}: item {index} must be an object")
        for key in ("source", "label", "text", "href"):
            if not str(item.get(key) or "").strip():
                raise ValueError(f"invalid {TLDR_FILENAME}: item {index} missing {key}")
        href = str(item["href"]).strip()
        if not href.startswith("#"):
            raise ValueError(f"invalid {TLDR_FILENAME}: item {index} href must start with #")
        cleaned.append(
            {
                "source": str(item["source"]).strip(),
                "label": str(item["label"]).strip(),
                "text": str(item["text"]).strip(),
                "href": href,
            }
        )
    return cleaned


def render_tldr_html(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    rows: list[str] = []
    for item in items:
        source_class = re.sub(r"[^a-z0-9\-]+", "-", item["source"].lower()).strip("-") or "other"
        rows.append(
            "<li>"
            f'<span class="tldr-source tldr-source-{html_escape(source_class)}">'
            f'{html_escape(item["label"])}</span> '
            f'<a class="tldr-link" href="{html_escape(item["href"])}">'
            f'{html_escape(item["text"])}</a>'
            "</li>"
        )
    return (
        '<section class="tldr panel" id="tldr" aria-labelledby="tldr-heading">'
        '<h2 id="tldr-heading">要点（TL;DR）</h2>'
        '<p class="tldr-note">出典ラベル付き。項目をクリックすると該当箇所へ移動します'
        "（折りたたみ内なら自動で開きます）。</p>"
        f'<ol class="tldr-list">{"".join(rows)}</ol>'
        "</section>"
    )


def render_toc_list(entries: list[dict[str, Any]], *, nested: bool = False) -> str:
    if not entries:
        return ""
    tag = "ul" if nested else "ol"
    parts = [f"<{tag}>"]
    for entry in entries:
        indent = " toc-level-2" if entry["level"] >= 2 and nested else ""
        parts.append(
            f'<li class="toc-item{indent}">'
            f'<a href="#{html_escape(entry["id"])}">{html_escape(entry["title"])}</a>'
            "</li>"
        )
    parts.append(f"</{tag}>")
    return "".join(parts)


def render_article_toc_html(
    *,
    has_tldr: bool,
    agent_blocks: list[dict[str, Any]],
) -> str:
    items: list[str] = []
    if has_tldr:
        items.append('<li><a href="#tldr">要点（TL;DR）</a></li>')
    items.append('<li><a href="#article-toc">目次</a></li>')
    items.append('<li><a href="#background-heading">検討に至った背景</a></li>')
    items.append('<li><a href="#prompt-heading">調査プロンプト</a></li>')

    agent_items = ['<li><a href="#agents-heading">AIエージェントの回答</a><ul class="toc-agents">']
    for block in agent_blocks:
        agent_items.append(
            f'<li><a href="#{html_escape(block["panel_id"])}">{html_escape(block["name"])}</a>'
            f'{render_toc_list(block["toc"], nested=True)}</li>'
        )
    agent_items.append("</ul></li>")
    items.extend(agent_items)

    items.append('<li><a href="#analysis-heading">2回答の合成</a></li>')
    items.append('<li><a href="#analysis-plain-heading">2回答の合成（わかりやすい説明）</a></li>')
    items.append('<li><a href="#conclusion-heading">合成結果の要約</a></li>')
    items.append('<li><a href="#conclusion-plain-heading">合成結果の要約（わかりやすい説明）</a></li>')
    items.append('<li><a href="#edit-heading">Edit on GitHub</a></li>')
    items.append('<li><a href="#comments-heading">コメント</a></li>')

    return (
        '<nav class="article-toc panel" id="article-toc" aria-label="目次">'
        '<h2 id="article-toc-heading">目次</h2>'
        f'<ol class="toc-root">{"".join(items)}</ol>'
        "</nav>"
    )


def filter_agent_toc(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep chapter-scale headings only (skip document title)."""

    if entries and entries[0]["level"] == 1:
        entries = entries[1:]
    has_h1 = any(entry["level"] == 1 for entry in entries)
    if has_h1:
        return [entry for entry in entries if entry["level"] == 1]
    return [entry for entry in entries if entry["level"] == 2]


def render_agent_sections(meta: dict) -> tuple[str, list[dict[str, Any]]]:
    parts: list[str] = []
    agent_blocks: list[dict[str, Any]] = []
    article_dir: Path = meta["_dir"]
    for agent in meta["agents"]:
        response_path = article_dir / agent["responseFile"]
        if not response_path.exists():
            raise FileNotFoundError(f"missing response: {response_path}")
        body_md = read_text(response_path)
        body_html = markdown_to_html(body_md)
        slug = agent_slug(agent["name"])
        prefix = f"agent-{slug}-"
        body_html, toc_entries = add_heading_ids(body_html, prefix=prefix, toc_max_level=3)
        panel_id = f"agent-{slug}"
        notes = agent.get("notes") or ""
        notes_html = (
            f'    <p class="agent-notes">{html_escape(notes)}</p>\n' if notes else ""
        )
        agent_blocks.append(
            {
                "name": agent["name"],
                "panel_id": panel_id,
                "toc": filter_agent_toc(toc_entries),
            }
        )
        parts.append(
            f"""
<section class="agent-response" data-agent="{html_escape(agent['name'])}">
  <details id="{html_escape(panel_id)}">
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
    return "\n".join(parts), agent_blocks


def prepare_section_html(md_text: str, *, prefix: str) -> str:
    html = markdown_to_html(md_text)
    html, _ = add_heading_ids(html, prefix=prefix, toc_max_level=2)
    return html


def build_article_html(meta: dict, config: dict) -> str:
    article_dir: Path = meta["_dir"]
    for name in REQUIRED_FILES:
        if not (article_dir / name).exists():
            raise FileNotFoundError(f"missing {name} in {article_dir}")

    tldr_items = load_tldr(article_dir)
    conclusion_html = prepare_section_html(
        read_text(article_dir / "conclusion.md"), prefix="conclusion-"
    )
    conclusion_plain_html = prepare_section_html(
        read_text(article_dir / "conclusion-plain.md"), prefix="conclusion-plain-"
    )
    analysis_html = prepare_section_html(
        read_text(article_dir / "analysis.md"), prefix="analysis-"
    )
    analysis_plain_html = prepare_section_html(
        read_text(article_dir / "analysis-plain.md"), prefix="analysis-plain-"
    )
    background_html = prepare_section_html(
        read_text(article_dir / "background.md"), prefix="background-"
    )
    prompt_text = read_text(article_dir / "prompt.txt")
    agents_html, agent_blocks = render_agent_sections(meta)

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
    tldr_html = render_tldr_html(tldr_items)
    toc_html = render_article_toc_html(has_tldr=bool(tldr_items), agent_blocks=agent_blocks)

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
            "TLDR_HTML": tldr_html,
            "TOC_HTML": toc_html,
            "BACKGROUND_HTML": background_html,
            "CONCLUSION_HTML": conclusion_html,
            "CONCLUSION_PLAIN_HTML": conclusion_plain_html,
            "ANALYSIS_HTML": analysis_html,
            "ANALYSIS_PLAIN_HTML": analysis_plain_html,
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
    rendered_articles: list[tuple[dict, str, str]] = []

    # Render every source successfully before replacing committed generated pages.
    # This prevents an invalid later article from leaving a partially refreshed tree.
    for article_dir in iter_article_dirs():
        meta = load_article(article_dir)
        public_meta = {k: v for k, v in meta.items() if not k.startswith("_")}
        validate_schema(public_meta)
        rendered_articles.append(
            (
                meta,
                build_article_html(meta, config),
                build_summary_document_html(meta, config),
            )
        )

    reset_articles_output()
    for meta, html, summary_html in rendered_articles:
        out_dir = ARTICLES_OUT / meta["_year"] / meta["_dirname"]
        write_text(out_dir / "index.html", html)
        write_text(out_dir / "summary" / "index.html", summary_html)

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
