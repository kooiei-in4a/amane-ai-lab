# AI Agent Verification Knowledge Base Specification

- Document ID: `SPEC-KB-001`
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-30
- Owner: Koo
- Repository: `https://github.com/kooiei-in4a/amane-ai-lab`

---

## 1. 目的

本プロジェクトは、AIエージェントを利用して実施した調査、設計検討、比較、レビュー、検証結果を、再利用可能な公開ナレッジとして蓄積・共有するための静的Webサイトを構築する。

主な公開内容は次のとおりとする。

1. AIへ入力したプロンプト
2. 複数のAIエージェントから得た回答
3. 回答間の比較
4. 人間による考察・判断
5. 最終的な結論・サマリー
6. 検証時点、モデル、条件、制約
7. 後日判明した訂正や更新履歴

公開経路はGitHub Pagesとし、XなどのSNSから個別記事へ直接誘導できる構成とする。

---

## 2. 設計目標

### 2.1 必須目標

- GitHub PublicリポジトリとGitHub Pagesだけで公開できること
- サーバーサイドアプリケーションやデータベースを必要としないこと
- 記事が100件を超えても管理可能であること
- AIエージェントが記事作成・更新・検査を実行しやすいこと
- 人間がGit差分を確認しやすいこと
- 記事ごとに安定したURLを持つこと
- 入力プロンプトをワンクリックでコピーできること
- 長いAI回答を折りたたんで表示できること
- GitHub上で記事を編集する導線を持つこと
- GitHub Discussionsを利用したコメント欄を持つこと
- 秘密情報、個人情報、顧客情報の公開事故を抑止すること
- AI回答と人間の判断を明確に区別すること

### 2.2 品質目標

- JavaScriptが無効でも記事本文を読めること
- モバイルとデスクトップの両方で閲覧可能であること
- キーボード操作に対応すること
- ページタイトル、description、canonical URL、OGPを設定すること
- 記事生成が再現可能であること
- 同じ入力から同じ公開HTMLを生成できること
- 生成済みHTMLへの手作業変更を原則禁止すること
- 公開前チェックをローカルとCIの両方で実行できること

---

## 3. 非目標

初期リリースでは、次を対象外とする。

- ユーザー登録
- 独自のコメントシステム
- データベース
- 管理画面
- SPAフレームワーク
- React、Vue、Angularなどの導入
- CMSの導入
- サーバーサイド全文検索
- リアルタイム通知
- 独自アクセス解析基盤
- AI APIを利用したサイト上での自動回答
- 公開後の記事をブラウザ上から直接編集する機能
- 多言語対応
- 記事評価、ランキング、いいね機能

---

## 4. 技術構成

### 4.1 基本構成

- Hosting: GitHub Pages
- Repository: GitHub Public repository
- Markup: HTML5
- Styling:
  - 初期段階: Tailwind Play CDNまたは通常のCSS
  - 安定運用: 生成済みCSSまたは通常のCSSをリポジトリへ保存
- Client-side JavaScript: Vanilla JavaScript
- Comments: giscus / GitHub Discussions
- Content generation: Python 3
- CI: GitHub Actions
- Local preview: Python HTTP serverまたはVS Code Live Preview

### 4.2 禁止事項

- 公開サイトに秘密情報を埋め込まない
- ブラウザ側JavaScriptへAPIキーを保存しない
- AI回答を未エスケープの`innerHTML`として描画しない
- 生成済みHTMLだけを変更しない
- 記事IDを再利用しない
- 記事公開後にURLを安易に変更しない
- 外部スクリプトを目的・影響を確認せず追加しない
- 出典を確認せず、AI回答を事実として断定しない

---

## 5. アーキテクチャ

### 5.1 正本と生成物

記事の正本は`content/articles/`配下の構造化データとする。

公開HTMLは正本から生成される成果物とする。

```text
content/articles/
    ↓ build_site.py
articles/
data/articles.json
sitemap.xml
feed.xml
```

正本と生成物の関係は次のとおりとする。

| 種別 | パス | 位置づけ |
|---|---|---|
| 記事メタデータ | `content/articles/**/article.json` | 正本 |
| 検討背景 | `content/articles/**/background.md` | 正本 |
| 合成結果の要約 | `content/articles/**/conclusion.md` | 正本 |
| 2回答の合成 | `content/articles/**/analysis.md` | 正本 |
| 入力プロンプト | `content/articles/**/prompt.txt` | 正本 |
| AI回答 | `content/articles/**/responses/*.md` | 正本 |
| 公開HTML | `articles/**/index.html` | 生成物 |
| 記事一覧 | `data/articles.json` | 生成物 |
| sitemap | `sitemap.xml` | 生成物 |
| RSS/Atom | `feed.xml` | 生成物 |

### 5.2 記事生成

記事生成処理は次を行う。

1. 記事メタデータを読み込む
2. MarkdownとテキストをHTMLへ変換する
3. HTML特殊文字を安全にエスケープする
4. 共通テンプレートへ値を埋め込む
5. 個別記事HTMLを生成する
6. 記事一覧JSONを再生成する
7. トップページ用データを更新する
8. sitemapを再生成する
9. feedを再生成する
10. 未置換プレースホルダーがないことを検査する

---

## 6. リポジトリ構成

```text
/
├─ AGENTS.md
├─ CLAUDE.md
├─ README.md
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ SECURITY.md
├─ LICENSE
├─ LICENSE-CONTENT
├─ .gitignore
├─ .nojekyll
│
├─ content/
│  └─ articles/
│     └─ YYYY/
│        └─ kb-YYYY-NNNN-slug/
│           ├─ article.json
│           ├─ background.md
│           ├─ prompt.txt
│           ├─ analysis.md
│           ├─ conclusion.md
│           └─ responses/
│              ├─ chatgpt.md
│              ├─ claude.md
│              └─ gemini.md
│
├─ articles/
│  └─ YYYY/
│     └─ kb-YYYY-NNNN-slug/
│        └─ index.html
│
├─ agents/
│  ├─ README.md
│  ├─ policies/
│  ├─ roles/
│  ├─ workflows/
│  ├─ prompts/
│  ├─ schemas/
│  ├─ checklists/
│  └─ examples/
│
├─ docs/
│  ├─ specs/
│  ├─ adr/
│  ├─ operations/
│  └─ agent-prompts/
│
├─ templates/
│  ├─ article.html
│  ├─ index.html
│  └─ partials/
│
├─ assets/
│  ├─ css/
│  ├─ js/
│  └─ images/
│
├─ data/
│  ├─ articles.json
│  └─ tags.json
│
├─ scripts/
│  ├─ new_article.py
│  ├─ build_site.py
│  ├─ validate_content.py
│  ├─ check_sensitive_data.py
│  ├─ generate_index.py
│  ├─ generate_sitemap.py
│  └─ generate_feed.py
│
├─ reports/
│  ├─ reviews/
│  └─ audits/
│
├─ .work/
│
├─ .github/
│  ├─ workflows/
│  ├─ ISSUE_TEMPLATE/
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ copilot-instructions.md
│
├─ .cursor/
│  └─ rules/
│
└─ .vscode/
   ├─ tasks.json
   ├─ settings.json
   ├─ extensions.json
   └─ kb.code-snippets
```

---

## 7. 記事モデル

### 7.1 記事ID

記事IDは次の形式とする。

```text
KB-YYYY-NNNN
```

要件:

- 一度割り当てたIDを変更しない
- 削除済みIDを再利用しない
- giscusのDiscussionマッピングにも同じIDを使用する
- 年が変わった場合は連番を`0001`から開始してよい
- ID採番はスクリプトで行う

削除済みIDは`content/retired-article-ids.json`に記録する。
採番スクリプトは live 記事と retired 台帳の両方を参照し、再利用を拒否する。

### 7.2 URL

URL形式:

```text
/articles/YYYY/kb-yyyy-nnnn-slug/
```

URLは公開後に原則変更しない。

### 7.3 記事ステータス

利用可能なステータスは次とする。

```text
draft
review
published
superseded
archived
```

| Status | 意味 |
|---|---|
| `draft` | 執筆中 |
| `review` | 公開前レビュー中 |
| `published` | 公開済み |
| `superseded` | 後継記事あり |
| `archived` | 記録目的で保管 |

### 7.3.1 退役・削除・初期リセット

公開後に記事を下げたい場合の既定は soft 退役とする。

| 経路 | いつ使うか | 正本 | URL | ID |
|---|---|---|---|---|
| `archived` / `superseded` | 記録を残す。URLを維持したい | 残す | 原則維持 | 変更しない |
| hard delete | 誤公開・サンプル廃棄・公開継続不可 | 削除する | 404 | `retired-article-ids.json` に登録し再利用禁止 |
| 記事ID初期リセット | 人間が`KB-YYYY-0001`からやり直すと明示し、残正本が0件 | 全削除 | 旧URLは404 | retired 台帳を空にし、採番を`0001`から再開 |

運用ルールの正本:

- `agents/policies/article-lifecycle.md`
- `agents/workflows/archive-article.md`
- `agents/workflows/delete-article.md`
- `agents/workflows/reset-article-ids.md`

hard delete および初期リセットは人間の明示承認を必要とする。
Git履歴の書き換えは秘密情報混入時のみ別承認とする。
giscus Discussion は自動削除しない。

### 7.4 AI回答の完全性

AI回答には次のいずれかを指定する。

```text
raw
formatted
redacted
excerpted
edited
```

| 値 | 意味 |
|---|---|
| `raw` | 原文 |
| `formatted` | 改行・見出し・コードブロックのみ調整 |
| `redacted` | 非公開情報をマスキング |
| `excerpted` | 一部省略 |
| `edited` | 内容を編集 |

`formatted`以外の変更を行った場合、変更理由を記事内に明示する。

### 7.5 `article.json`

```json
{
  "schemaVersion": 1,
  "id": "KB-2026-0001",
  "slug": "agent-market-share",
  "title": "AIエージェントのシェアを複数ソースで比較する",
  "description": "複数の公開情報を利用してAIエージェント市場を比較した記録。",
  "status": "draft",
  "publishedAt": null,
  "updatedAt": "2026-07-30",
  "lastVerifiedAt": "2026-07-30",
  "tags": [
    "AIエージェント",
    "市場調査"
  ],
  "agents": [
    {
      "name": "ChatGPT",
      "model": "GPT-5.6 Thinking",
      "responseFile": "responses/chatgpt.md",
      "executedAt": "2026-07-30",
      "webSearch": true,
      "attachmentsUsed": false,
      "integrity": "raw",
      "notes": null
    }
  ],
  "giscusTerm": "KB-2026-0001",
  "supersededBy": null
}
```

---

## 8. 記事表示仕様

記事は上から次の順序で表示する。

1. 記事ID、ステータス、公開日、最終確認日
2. 記事タイトル
3. 検討に至った背景
4. 調査プロンプト（既定は折りたたみ）
5. 各AIエージェントの回答
6. 2回答の合成
7. 合成結果の要約（資料版HTMLへのリンクを含む）
8. Edit on GitHub
9. コメント欄
10. ライセンスと免責事項

### 8.1 合成結果の要約

要約は記事内で最も視覚的に目立つ領域とする。

要約だけを読んでも、次を把握できる必要がある。

- 何を調べたか
- 何が分かったか
- 何を採用・推奨するか
- 主要な制約は何か

### 8.2 AI回答

AI回答は`details`と`summary`を使用して折りたたむ。

各回答には次を表示する。

- エージェント名
- モデル名
- 実行日
- Web検索の有無
- 添付ファイルの有無
- 完全性区分
- 回答本文

### 8.3 コピー機能

コピー対象は表示HTMLではなく、`textContent`として取得したプロンプト本文とする。

要件:

- Clipboard APIを優先する
- Clipboard APIが利用できない場合はフォールバックする
- 成功・失敗を画面上へ通知する
- キーボード操作に対応する
- ボタン連打で表示が破綻しない

### 8.4 コメント

giscusを使用する。

要件:

- GitHub Discussionsを有効化する
- 専用カテゴリを作成する
- 記事IDによるspecific mappingを使用する
- strict mappingを有効にする
- ページ表示直後にはロードせず、ユーザー操作後にロードできることが望ましい
- コメントが第三者投稿であることを明示する
- モデレーション方針へのリンクを表示する

### 8.5 Edit on GitHub

記事ごとに正本ファイルへのリンクを表示する。

リンク先は生成済みHTMLではなく、原則として次のいずれかとする。

```text
content/articles/.../article.json
content/articles/.../
```

---

## 9. トップページ仕様

トップページには次を実装する。

- サイト概要
- 最新記事
- キーワード検索
- タグ絞り込み
- AIエージェント絞り込み
- ステータス表示
- 公開日順
- 更新日順
- 記事件数
- 主要テーマへの導線

記事検索は`data/articles.json`を読み込み、ブラウザ上で絞り込む。

記事本文を検索対象とする全文検索は初期対象外とする。

---

## 10. AIエージェント運用

### 10.1 共通入口

AIエージェントは作業開始時に、ルートの`AGENTS.md`を必ず確認する。

ツール固有ファイルは`AGENTS.md`への入口とし、共通ルールを複製しない。

対象例:

```text
CLAUDE.md
.cursor/rules/knowledge-base.mdc
.github/copilot-instructions.md
```

### 10.2 標準ワークフロー

AIエージェントは次の順序で作業する。

1. 探索
2. 対象範囲の特定
3. 実装計画
4. 計画のセルフレビュー
5. 正本データまたはコードの変更
6. サイト生成
7. 自動検証
8. 差分レビュー
9. セルフレビュー
10. 作業報告
11. 必要な場合のみDraft PR作成

### 10.3 停止条件

次の場合、エージェントは公開・commit・pushを行わず停止する。

- 秘密情報の疑いが解消できない
- 個人情報または顧客情報の疑いがある
- 記事IDが重複している
- 正本と生成物が一致しない
- 未解決のBlockerまたはMajor findingがある
- 出典と結論が明確に矛盾する
- AI回答の出所が不明
- AI回答が原文か編集済みか判断できない
- 検証コマンドが失敗する
- 変更範囲が依頼内容を超える
- 削除、URL変更、記事ID変更が必要になった

---

## 11. 公開安全性

### 11.1 公開禁止情報

次を公開してはならない。

- APIキー
- パスワード
- アクセストークン
- Cookie
- 秘密鍵
- 接続文字列
- 非公開リポジトリの内容
- 顧客名
- 個人のメールアドレス
- 電話番号
- 個人住所
- 社内URL
- 社内IPアドレス
- ローカルファイルパス
- 契約上非公開の金額
- 未公開の障害情報
- 脆弱性の悪用に直結する未修正情報

### 11.2 マスキング

マスキング例:

```text
[REDACTED_API_KEY]
[REDACTED_EMAIL]
[REDACTED_CUSTOMER]
[REDACTED_INTERNAL_URL]
[REDACTED_PATH]
```

マスキングしたAI回答の`integrity`は`redacted`とする。

### 11.3 Git履歴

秘密情報を一度でもGitへ追加した場合、通常の削除だけでは不十分である。

エージェントは秘密情報を検出した場合、commit前に停止する。

commit後に検出された場合、通常の修正を続行せず、人間へ報告する。

---

## 12. 自動検証

`validate_content.py`は少なくとも次を検査する。

- JSON Schema適合
- 記事ID形式
- 記事ID重複
- slug重複
- URL重複
- 必須ファイルの存在
- AI回答ファイルの存在
- 日付形式
- 記事ステータス
- 完全性区分
- giscusTermと記事IDの一致
- 未置換テンプレート変数
- HTML内の重複ID
- 必須meta要素
- canonical URL
- Edit on GitHub URL
- 内部リンク切れ
- 秘密情報候補
- メールアドレス候補
- IPアドレス候補
- 内部URL候補
- 極端に大きなファイル

---

## 13. CI要件

Pull Requestおよびmainへのpush時に次を実行する。

1. Python依存関係の準備
2. JSON Schema検証
3. サイト再生成
4. Git差分確認
5. コンテンツ検証
6. HTML検証
7. 内部リンク検査
8. 秘密情報検査
9. 公開成果物生成
10. GitHub Pagesへのデプロイ

再生成後に未commit差分が存在する場合、CIを失敗させる。

---

## 14. 受入条件

### AC-01 リポジトリ

- 指定のディレクトリ構成が存在する
- `AGENTS.md`が存在する
- 正本と生成物の関係が明記されている

### AC-02 記事生成

- コマンド一つで記事ひな型を作成できる
- コマンド一つでサイト全体を生成できる
- 同じ正本から同じHTMLを生成できる

### AC-03 記事表示

- タイトルが表示される
- 結論が最も目立つ
- 考察が表示される
- プロンプト全文が表示される
- プロンプトをコピーできる
- 複数AI回答を折りたためる
- Edit on GitHubが表示される
- giscusを読み込める

### AC-04 トップページ

- すべての公開記事が一覧に表示される
- キーワードで絞り込める
- タグで絞り込める
- AIエージェントで絞り込める
- 記事リンクが正しい

### AC-05 安全性

- 未エスケープのAI回答がHTMLとして実行されない
- 秘密情報検査が存在する
- マスキングポリシーが存在する
- 公開前チェックリストが存在する

### AC-06 AIエージェント運用

- 記事作成ワークフローが存在する
- 更新ワークフローが存在する
- 独立レビューワークフローが存在する
- 公開停止条件が定義されている
- 生成済みHTMLの直接編集禁止が明記されている

### AC-07 CI

- Pull Requestで検証が実行される
- 生成差分が残っている場合に失敗する
- 検証失敗時にGitHub Pagesへ公開されない

---

## 15. 初期リリース範囲

初期リリースでは次を実装する。

- リポジトリ基本構成
- `AGENTS.md`
- エージェントポリシー
- 記事テンプレート
- 記事作成スクリプト
- サイト生成スクリプト
- コンテンツ検証スクリプト
- 記事一覧
- タグ・キーワード絞り込み
- プロンプトコピー
- AI回答アコーディオン
- Edit on GitHub
- giscus埋め込み領域
- sitemap
- feed
- GitHub Actions
- サンプル記事1件

初期リリースでは、giscusの実リポジトリIDとカテゴリIDは設定値またはプレースホルダーとしてもよい。

---

## 16. 将来拡張

将来的に検討可能な項目:

- Markdown主体の記事記述
- OGP画像の自動生成
- 記事間リンク
- シリーズ機能
- 関連記事
- 記事の鮮度検査
- リンク切れ定期検査
- 複数言語
- Pagefindなどによる静的全文検索
- 記事統計
- Schema.org構造化データ
- GitHub Issueからの記事作成
- AI回答比較表の自動生成
- 訂正履歴の自動表示
- 記事作成からX投稿文生成までの一括処理

これらは初期実装へ含めず、必要性を確認してからADRまたはIssueで決定する。
