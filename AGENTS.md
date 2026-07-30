# AIエージェント向け共通指示

このファイルは、本リポジトリで作業するAIエージェントの共通入口である。
詳細ルールは `agents/` 配下を正本とする。ツール固有ファイルへルールを複製しないこと。

## 目的

AIエージェントによる調査・比較・検証結果を、再利用可能な公開ナレッジとして蓄積する静的サイトを運用する。

設計正本:

- `docs/specs/public-knowledge-base-spec.md`
- `docs/adr/0001-static-site-architecture.md`
- `docs/adr/0002-structured-content-source-of-truth.md`
- `docs/adr/0003-ai-agent-governance.md`

## 正本と生成物

| 種別 | パス | 扱い |
|---|---|---|
| 記事正本 | `content/articles/` | 編集対象 |
| 公開HTML | `articles/` | 生成物。直接編集禁止 |
| 記事一覧 | `data/articles.json` | 生成物 |
| sitemap / feed | `sitemap.xml` / `feed.xml` | 生成物 |

正本を変更したら、必ず生成と検証を実行する。

## 標準作業手順

1. この `AGENTS.md` を読む
2. 対象 workflow を `agents/workflows/` から読む
3. 変更範囲を特定する
4. 正本または許可されたソースを変更する
5. `python3 scripts/build_site.py` を実行する
6. `python3 scripts/validate_content.py` を実行する
7. `python3 scripts/check_sensitive_data.py` を実行する
8. Git差分を確認する
9. セルフレビューする
10. 必要な場合のみ Draft PR を作成する

## 禁止操作

- `articles/` 配下の生成HTMLだけを手で直すこと
- 秘密情報・個人情報・顧客情報の公開
- AI回答を未エスケープの `innerHTML` として描画すること
- 記事IDの再利用・公開後URLの安易な変更
- `main` への merge
- Issue の作成 / close / 編集（依頼されていない場合）
- Release / publish / GitHub Pages 本番設定変更
- Git履歴の書き換え

## 停止条件

次に該当したら commit / push / 公開可能判定をせず停止し、人間へ報告する。

- 秘密情報・個人情報・顧客情報の疑いが解消できない
- 記事ID重複
- 正本と生成物の不一致
- 未解決の Blocker / Major finding
- 出典と結論の明確な矛盾
- AI回答の出所または完全性区分が不明
- 検証コマンド失敗
- 依頼範囲を超える変更が必要
- 削除、URL変更、記事ID変更が必要

## 人間承認が必要な操作

- main への merge
- 公開済み記事の削除
- 記事ID変更 / 公開URL変更
- Git履歴の書き換え・秘密情報混入後の履歴修正
- ライセンス変更
- giscus リポジトリ・カテゴリ変更
- 外部スクリプト追加
- 大規模な全記事再生成
- セキュリティポリシーの緩和

## 公開安全性

公開禁止情報とマスキング方針は `agents/policies/publication-safety.md` と `agents/policies/redaction-policy.md` を参照する。

## 参照

- ポリシー: `agents/policies/`
- 役割: `agents/roles/`
- ワークフロー: `agents/workflows/`
- チェックリスト: `agents/checklists/`
- スキーマ: `agents/schemas/`
- 例: `agents/examples/`
