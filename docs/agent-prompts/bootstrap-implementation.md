# AI Agent Knowledge Base 初期構築プロンプト

あなたは、静的Webサイト、GitHub Pages、コンテンツ生成基盤、AIエージェント運用設計に精通したシニアソフトウェアエンジニアです。

次のリポジトリに、AIエージェントによる検証結果を公開するナレッジベースの初期基盤を構築してください。

## Repository

```text
https://github.com/kooiei-in4a/amane-ai-lab
```

## 作業ブランチ

現在の既定ブランチから、次の形式で作業ブランチを作成してください。

```text
feature/initial-knowledge-base
```

すでに同等の作業ブランチが存在する場合は、既存ブランチを確認し、重複作成しないでください。

---

## 目的

次の情報を記事として公開・蓄積するGitHub Pagesサイトを構築します。

- 記事タイトル
- 最も目立つ結論サマリー
- 人間による考察・判断プロセス
- 入力したプロンプト全文
- 複数AIエージェントの回答
- モデル、実施日、Web検索有無などの検証条件
- 制約、未確認事項、訂正履歴
- Edit on GitHub
- giscusによるコメント欄

記事作成、更新、生成、検証は、主にAIエージェントが行う前提です。

---

## 設計正本

作業開始前に、次の仕様書とADRを確認してください。

```text
docs/specs/public-knowledge-base-spec.md
docs/adr/0001-static-site-architecture.md
docs/adr/0002-structured-content-source-of-truth.md
docs/adr/0003-ai-agent-governance.md
```

これらがまだ存在しない場合は、このパッケージに含まれる文書をそのまま配置してください。

仕様やADRと矛盾する実装判断が必要になった場合、独断で変更せず停止して報告してください。

---

## 最重要ルール

1. 記事の正本は`content/articles/`とする
2. `articles/`配下のHTMLは生成物とする
3. 生成済みHTMLだけを直接修正しない
4. SPAフレームワークを導入しない
5. サーバーサイド処理を導入しない
6. データベースを導入しない
7. 秘密情報、個人情報、顧客情報を公開しない
8. AI回答を未エスケープHTMLとして描画しない
9. 記事IDは`KB-YYYY-NNNN`形式とする
10. giscusは記事IDによるspecific mappingを前提とする
11. 依頼範囲外の機能を追加しない
12. 不明点を推測で仕様化しない
13. 自動検証失敗時は公開可能と判定しない
14. `main`へのmergeは禁止する
15. Issueの作成、close、編集は禁止する
16. Release、publish、GitHub Pages本番設定変更は禁止する

---

## 許可する操作

次を許可します。

- リポジトリ探索
- 設計確認
- 実装計画作成
- ファイル作成・編集
- ローカルブランチ作成
- Pythonスクリプト実装
- HTML、CSS、JavaScript実装
- GitHub Actions workflow実装
- テストと検証
- commit
- push
- Draft Pull Request作成

次は禁止します。

- merge
- cleanup
- branch削除
- Issue作成
- Issue close
- Issue編集
- release
- package publish
- GitHub Pagesの本番設定変更
- Discussionsカテゴリの実作成
- giscus Appの実インストール
- Git履歴の書き換え

---

## 実行手順

次の順序を厳守してください。

### Phase 1: 探索

リポジトリ全体を確認し、次を報告してください。

- 現在のディレクトリ構成
- 既存のGitHub Pages構成
- 既存のHTML、CSS、JavaScript
- 既存のPythonまたはNode.js環境
- 既存のGitHub Actions
- 既存のライセンス
- 既存のエージェント指示
- 仕様との衝突
- 再利用可能な既存資産

既存資産を確認せず、即座に全面置換しないでください。

### Phase 2: 実装計画

実装前に、次を含む計画を作成してください。

- 変更対象ファイル
- 新規作成ファイル
- 正本と生成物の関係
- 記事生成方式
- Markdown変換方式
- HTMLエスケープ方式
- 検証方式
- GitHub Actions構成
- giscus設定のプレースホルダー方式
- 依存関係
- リスク
- 非対象項目

計画をセルフレビューし、仕様漏れ、過剰実装、セキュリティ上の問題がないか確認してください。

### Phase 3: 基盤実装

少なくとも次を作成してください。

```text
AGENTS.md
CLAUDE.md
README.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
LICENSE
LICENSE-CONTENT
.nojekyll
.gitignore

agents/
docs/
content/articles/
articles/
templates/
assets/css/
assets/js/
assets/images/
data/
scripts/
reports/reviews/
reports/audits/
.work/
.github/workflows/
.github/ISSUE_TEMPLATE/
.cursor/rules/
.vscode/
```

空ディレクトリがGitで保持されない場合は、必要に応じて`.gitkeep`を使用してください。

### Phase 4: エージェント運用ファイル

`AGENTS.md`を共通正本として作成してください。

少なくとも次を明記してください。

- リポジトリの目的
- 正本
- 生成物
- 標準作業手順
- 禁止操作
- 停止条件
- 公開安全性
- 詳細ポリシーへの参照

`agents/`配下へ次を作成してください。

```text
agents/README.md

agents/policies/
  content-authority.md
  publication-safety.md
  redaction-policy.md
  citation-policy.md
  ai-response-integrity.md
  change-scope-policy.md

agents/roles/
  article-author.md
  content-reviewer.md
  privacy-reviewer.md
  fact-checker.md
  site-maintainer.md
  release-reviewer.md

agents/workflows/
  create-article.md
  update-article.md
  review-article.md
  publish-article.md
  correct-published-article.md
  archive-article.md

agents/checklists/
  article-ready.md
  privacy-check.md
  accessibility-check.md
  release-gate.md

agents/schemas/
  article.schema.json
  article-index.schema.json
  review-result.schema.json

agents/examples/
  article.example.json
  review-result.example.json
```

ツール固有ファイルは共通ルールを複製せず、`AGENTS.md`を参照する薄い入口にしてください。

### Phase 5: コンテンツモデル

サンプル記事を1件作成してください。

```text
content/articles/2026/kb-2026-0001-example/
├─ article.json
├─ conclusion.md
├─ analysis.md
├─ prompt.txt
└─ responses/
   ├─ chatgpt.md
   └─ claude.md
```

サンプル内容は架空の安全なデータとしてください。

実在の顧客、個人、非公開情報を使用しないでください。

### Phase 6: 記事テンプレート

`templates/article.html`を実装してください。

必須要件:

- 日本語HTML
- UTF-8
- レスポンシブ表示
- 記事タイトル
- 結論を最も目立たせる
- 人間の考察
- 入力プロンプト全文
- プロンプトコピーボタン
- コピー成功・失敗表示
- AI回答の`details` / `summary`
- すべて開く
- すべて閉じる
- モデル、日付、検索有無、完全性区分
- 制約・未確認事項
- 訂正履歴
- Edit on GitHub
- giscus読み込み領域
- canonical
- description
- OGP
- X card
- アクセシビリティ
- 印刷時の最低限の可読性
- JavaScript無効時も本文を読める

AI回答やプロンプトを`innerHTML`へ直接代入しないでください。

コピー処理は`textContent`を使用してください。

### Phase 7: トップページ

`index.html`または対応するテンプレートを実装してください。

必須要件:

- サイト説明
- 記事件数
- 最新記事一覧
- キーワード検索
- タグ絞り込み
- AIエージェント絞り込み
- 公開日または更新日表示
- 記事ステータス表示
- 個別記事へのリンク
- 検索結果0件表示
- JavaScriptエラー時の最低限の説明

トップページは`data/articles.json`を読み込んで表示してください。

SPAルーターは使用しないでください。

### Phase 8: スクリプト

Python 3で次を実装してください。

```text
scripts/new_article.py
scripts/build_site.py
scripts/validate_content.py
scripts/check_sensitive_data.py
scripts/generate_index.py
scripts/generate_sitemap.py
scripts/generate_feed.py
```

#### new_article.py

次を行うこと。

- 次の記事IDを採番
- slugを生成
- 記事ディレクトリを作成
- 必須ファイルを生成
- 重複を拒否
- 作成結果を表示

#### build_site.py

次を行うこと。

- 正本データを読み込む
- JSON Schemaを確認
- MarkdownをHTMLへ変換
- 安全にエスケープ
- 記事HTMLを生成
- 記事一覧JSONを生成
- sitemapを生成
- feedを生成
- 再現可能な出力を行う

現在日時を無条件に埋め込んで、毎回差分が出る実装を避けてください。

#### validate_content.py

少なくとも次を検査すること。

- 記事ID
- ID重複
- slug重複
- 必須ファイル
- 必須フィールド
- 日付形式
- status
- integrity
- giscusTerm
- AI回答ファイル
- 未置換プレースホルダー
- 生成物の存在
- canonical
- Edit on GitHub
- 内部リンク
- 秘密情報候補

検査結果は、成功件数、警告、失敗を区別して表示してください。

終了コードは次としてください。

```text
0: success
1: validation error
2: execution or configuration error
```

#### check_sensitive_data.py

少なくとも次の候補を検出してください。

- 秘密鍵
- APIキーらしい文字列
- bearer token
- connection string
- メールアドレス
- IPv4
- localhost以外の内部IP候補
- Windows絶対パス
- Unix home path
- 社内URL候補
- `[REDACTED_*]`ではない秘密情報候補

誤検知を完全に排除する必要はありません。

検出時に、ファイル名、行番号、検出種別を表示してください。

### Phase 9: giscus

テンプレートにgiscus設定領域を作成してください。

初期値はプレースホルダーまたは設定ファイルとしてください。

必要な値:

```text
repository
repositoryId
category
categoryId
```

マッピング方式:

```text
specific
```

マッピングキー:

```text
記事ID
```

strict mappingを有効としてください。

実際のgiscus AppインストールやGitHub Discussions設定は行わないでください。

READMEに人間が行う設定手順を記載してください。

### Phase 10: GitHub Actions

少なくとも次のworkflowを作成してください。

```text
.github/workflows/validate.yml
.github/workflows/pages.yml
```

#### validate.yml

Pull Requestとmainへのpushで次を実行してください。

- Python準備
- 依存関係インストール
- JSON Schema検証
- サイト生成
- 生成差分確認
- コンテンツ検証
- 秘密情報検査
- 内部リンク検査

生成後に未commit差分が存在する場合は失敗させてください。

#### pages.yml

GitHub Pages向け成果物を生成するworkflowを作成してください。

ただし、実際のPages設定変更や本番公開操作は行わないでください。

既存のPages workflowがある場合は、重複作成せず統合してください。

### Phase 11: ローカル運用

次を作成してください。

```text
.vscode/tasks.json
.vscode/extensions.json
.vscode/settings.json
.vscode/kb.code-snippets
```

最低限のタスク:

- New Article
- Build Site
- Validate
- Sensitive Data Check
- Preview

プレビューは次を基本としてください。

```bash
python -m http.server 8000
```

READMEへ、記事作成からcommitまでの操作例を記載してください。

### Phase 12: 検証

少なくとも次を実行してください。

```bash
python scripts/build_site.py
python scripts/validate_content.py
python scripts/check_sensitive_data.py
python -m unittest discover
git diff --check
```

テスト方式を変更する場合は、実際に実行したコマンドを報告してください。

追加で確認してください。

- 生成処理を2回実行して差分が出ない
- サンプル記事が生成される
- 記事一覧にサンプル記事が表示される
- プロンプトコピーが動作する
- アコーディオンが動作する
- 不正な記事IDを検出できる
- 重複記事IDを検出できる
- 未置換プレースホルダーを検出できる
- 危険文字列のサンプルを検出できる
- AI回答内のHTMLが実行されず文字列として表示される

ブラウザ自動テストを導入する場合、初期要件に対して過剰な依存関係を追加しないでください。

---

## 実装上の優先順位

優先順位は次のとおりです。

1. 公開安全性
2. 正本と生成物の分離
3. 再現可能な生成
4. AIエージェントが迷わない運用構造
5. 検証の自動化
6. 読みやすさ
7. デザイン
8. 将来拡張

見栄えのために、安全性、単純性、再現性を損なわないでください。

---

## スコープ外

今回、次を実装しないでください。

- 独自CMS
- 認証
- データベース
- React
- Vue
- Angular
- Next.js
- Nuxt
- Astro
- Eleventy
- Node.jsベースの大規模ビルド基盤
- 検索サーバー
- アクセス解析
- 多言語
- OGP画像自動生成
- 自動X投稿
- AI API呼び出し
- 自動merge
- 自動公開承認
- 記事ランキング
- 全文検索ライブラリ

必要性を発見した場合は、実装せず、将来候補として報告してください。

---

## セルフレビュー

実装後、次の観点で独立したセルフレビューを行ってください。

### Architecture

- 仕様とADRに従っているか
- 不要な依存関係がないか
- 正本と生成物が混在していないか
- 再現可能な生成になっているか

### Security and Privacy

- AI回答がHTMLとして実行されないか
- 秘密情報検査が機能するか
- 外部スクリプトの利用が限定されているか
- giscusの読み込みと説明が適切か
- 公開禁止情報が文書化されているか

### Agent Operability

- AIエージェントが入口を判断できるか
- workflowが具体的か
- 停止条件が明確か
- ツール固有ファイルにルールが重複していないか
- 生成物直接編集禁止が明確か

### Maintainability

- 100記事以上でも管理可能か
- 記事追加時に既存ファイルを手作業変更しなくてよいか
- テンプレート変更が再生成で反映されるか
- エラーメッセージが理解可能か

### Accessibility

- キーボード操作が可能か
- `details` / `summary`が適切か
- ボタンにラベルがあるか
- 状態通知があるか
- コントラストやフォーカス表示に問題がないか

findingは次の重大度で分類してください。

```text
Blocker
Major
Minor
Suggestion
```

BlockerまたはMajorが残っている場合、完了判定しないでください。

---

## GitとPull Request

検証が成功した場合のみcommitしてください。

推奨commit例:

```text
feat: bootstrap AI knowledge base
```

push後、Draft Pull Requestを作成してください。

Pull Request本文には次を記載してください。

- 目的
- 実装概要
- 正本と生成物
- 追加したスクリプト
- 追加したエージェント運用文書
- 実行した検証
- 検証結果
- 未設定項目
- 残存リスク
- 人間による作業が必要な項目
- スコープ外として見送った項目

Draft PR作成後、Ready for reviewへ変更しないでください。

---

## 最終報告形式

最終報告は日本語で、次の形式にしてください。

```markdown
# 実装結果

## 判定

PASS / PASS WITH MINOR FINDINGS / STOPPED

## 変更概要

## 作成・変更ファイル

## アーキテクチャ上の判断

## 実行したコマンド

## 検証結果

## セルフレビュー結果

### Blocker

### Major

### Minor

### Suggestion

## 未設定項目

## 人間による作業が必要な項目

## 残存リスク

## Git情報

- Branch:
- Commit:
- Draft PR:

## Agent B向け独立レビュー依頼プロンプト
```

最後に、今回の実装を別のAIエージェントが独立レビューするためのプロンプトを出力してください。

独立レビューでは、実装者の説明を追認せず、コード、生成物、仕様、ADR、テスト、CIを直接確認するよう指示してください。
