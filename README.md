# amane-ai-lab

AIエージェントによる検証結果を公開する、GitHub Pages向け静的ナレッジベースです。

設計正本:

- `docs/specs/public-knowledge-base-spec.md`
- `docs/adr/`
- `docs/agent-prompts/bootstrap-implementation.md`

サイト・編集方針:

- `agents/policies/site-direction.md`

## サイトの方向性

amane AI Lab は、AIニュースや製品紹介を中心にするブログではなく、**実際のソフトウェア開発でAIエージェントを試し、その結果と証拠を公開するLab** として運用します。

公開内容は大きく3層に分けます。

| 層 | 役割 |
|---|---|
| Articles | 実験から何が分かったかを読みやすく伝える |
| Benchmarks | 試行ランキング、全候補、実行条件、生データを見せる |
| GitHub | Issue、branch、SHA、PR、CI、コードなど一次証拠を残す |

ランキングは、その試行で正式な採点結果がある場合は分かりやすく表示します。ただし、特定Issue・Model + Agent/Harness + Effort・1回の実行結果であり、モデル一般の性能順位とは扱いません。

詳細な判断基準は `agents/policies/site-direction.md` を正本とします。

## 正本と生成物

| 種別 | パス |
|---|---|
| 記事正本 | `content/articles/` |
| 公開HTML | `articles/`（生成物） |
| 記事一覧 | `data/articles.json`（生成物） |
| Benchmark公開ページ | `benchmarks/` |

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

記事・Benchmark・ランキング・UIを追加または変更する場合は、先に `agents/policies/site-direction.md` を確認してください。

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
