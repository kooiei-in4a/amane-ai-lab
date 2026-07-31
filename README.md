# amane-ai-lab

AIエージェントによる検証結果を公開する、GitHub Pages向け静的ナレッジベースです。

設計正本:

- `docs/specs/public-knowledge-base-spec.md`
- `docs/adr/`
- `docs/agent-prompts/bootstrap-implementation.md`

## 正本と生成物

| 種別 | パス |
|---|---|
| 記事正本 | `content/articles/` |
| 公開HTML | `articles/`（生成物） |
| 記事一覧 | `data/articles.json`（生成物） |

生成物を直接編集しないでください。

## セットアップ

```bash
python3 -m pip install -r requirements.txt
python3 scripts/install_git_hooks.py
python3 scripts/build_site.py
python3 scripts/validate_content.py
python3 scripts/check_sensitive_data.py
python3 -m http.server 8000
```

`install_git_hooks.py` で commit 前の機密情報スキャン（`.githooks/pre-commit`）を有効化する。

ブラウザで `http://localhost:8000/` を開きます。

## 記事作成

```bash
python3 scripts/new_article.py --title "タイトル" --slug "my-slug"
# 正本を編集
python3 scripts/build_site.py
python3 scripts/validate_content.py
python3 scripts/check_sensitive_data.py
git add content articles data index.html sitemap.xml feed.xml
git commit -m "content: add article"
```

## AIエージェント

作業前に `AGENTS.md` を読んでください。詳細は `agents/` 配下です。

## giscus（人間設定）

コメント欄は giscus を使います。初期値はプレースホルダーです。

1. GitHub Discussions を有効化
2. giscus App をインストール
3. `config/site.json` の `giscus.repo` / `repoId` / `category` / `categoryId` を設定
4. mapping は `specific`、term は記事ID、strict を有効

## ライセンス

- コード: MIT（`LICENSE`）
- コンテンツ: CC BY 4.0（`LICENSE-CONTENT`）
