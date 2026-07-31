"""Shared helpers for knowledge-base scripts."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

import bleach
import markdown as md

ROOT = Path(__file__).resolve().parents[2]
CONTENT_ARTICLES = ROOT / "content" / "articles"
ARTICLES_OUT = ROOT / "articles"
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
CONFIG_PATH = ROOT / "config" / "site.json"
ARTICLE_SCHEMA = ROOT / "agents" / "schemas" / "article.schema.json"
INDEX_SCHEMA = ROOT / "agents" / "schemas" / "article-index.schema.json"

ARTICLE_ID_RE = re.compile(r"^KB-(\d{4})-(\d{4})$")
DIR_NAME_RE = re.compile(r"^kb-(\d{4})-(\d{4})-(.+)$")

MD = md.Markdown(
    extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    output_format="html5",
)

ALLOWED_TAGS = [
    "p",
    "br",
    "hr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "b",
    "i",
    "code",
    "pre",
    "blockquote",
    "a",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "span",
    "div",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "class", "aria-label"],
    "code": ["class"],
    "pre": ["class"],
    "span": ["class"],
    "div": ["class"],
    "h1": ["id"],
    "h2": ["id"],
    "h3": ["id"],
    "h4": ["id"],
    "h5": ["id"],
    "h6": ["id"],
}

HEADING_HTML_RE = re.compile(r"<h([1-6])>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def slugify_heading(text: str) -> str:
    """Build a stable, URL-safe fragment id from heading text."""

    cleaned = TAG_RE.sub("", text)
    cleaned = cleaned.strip().lower()
    cleaned = cleaned.replace("\u3000", " ")
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"[^\w\-一-龥ぁ-んァ-ヴー]", "", cleaned, flags=re.UNICODE)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return (cleaned or "section")[:96]


def agent_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "agent"


def add_heading_ids(
    html: str,
    *,
    prefix: str = "",
    toc_max_level: int = 2,
) -> tuple[str, list[dict[str, Any]]]:
    """Insert unique heading ids and collect TOC entries up to toc_max_level."""

    used: dict[str, int] = {}
    entries: list[dict[str, Any]] = []

    def replacer(match: re.Match[str]) -> str:
        level = int(match.group(1))
        inner = match.group(2)
        plain = TAG_RE.sub("", inner).strip()
        base = slugify_heading(plain)
        candidate = f"{prefix}{base}" if prefix else base
        count = used.get(candidate, 0) + 1
        used[candidate] = count
        heading_id = candidate if count == 1 else f"{candidate}-{count}"
        if level <= toc_max_level and plain:
            entries.append({"id": heading_id, "level": level, "title": plain})
        permalink = (
            f'<a class="heading-permalink" href="#{html_escape(heading_id)}" '
            f'aria-label="この見出しへのリンク">#</a>'
        )
        return f'<h{level} id="{html_escape(heading_id)}">{permalink}{inner}</h{level}>'

    return HEADING_HTML_RE.sub(replacer, html), entries


def markdown_to_html(text: str) -> str:
    MD.reset()
    rendered = MD.convert(text)
    return bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=["http", "https", "mailto"],
        strip=True,
    )


def load_site_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def html_escape(text: str) -> str:
    return escape(text, quote=True)


def article_url_path(meta: dict[str, Any]) -> str:
    year = meta["id"].split("-")[1]
    slug = meta["slug"]
    seq = meta["id"].split("-")[2]
    return f"/articles/{year}/kb-{year}-{seq}-{slug}/"


def article_dir_name(meta: dict[str, Any]) -> str:
    year = meta["id"].split("-")[1]
    seq = meta["id"].split("-")[2]
    return f"kb-{year}-{seq}-{meta['slug']}"


def iter_article_dirs() -> list[Path]:
    if not CONTENT_ARTICLES.exists():
        return []
    dirs: list[Path] = []
    for year_dir in sorted(CONTENT_ARTICLES.iterdir()):
        if not year_dir.is_dir():
            continue
        for article_dir in sorted(year_dir.iterdir()):
            if article_dir.is_dir() and (article_dir / "article.json").exists():
                dirs.append(article_dir)
    return dirs


def load_article(article_dir: Path) -> dict[str, Any]:
    meta = json.loads((article_dir / "article.json").read_text(encoding="utf-8"))
    meta["_dir"] = article_dir
    meta["_year"] = meta["id"].split("-")[1]
    meta["_url"] = article_url_path(meta)
    meta["_dirname"] = article_dir_name(meta)
    return meta


def render_template(template_name: str, mapping: dict[str, str]) -> str:
    raw = read_text(TEMPLATES_DIR / template_name)
    out = raw
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", out)))
    if unresolved:
        raise ValueError(f"Unresolved placeholders in {template_name}: {unresolved}")
    return out
