# ADR-0001: 静的サイトとGitHub Pagesを採用する

- Status: Accepted
- Date: 2026-07-30
- Decision Owners: Koo
- Related Specification: `SPEC-KB-001`

## Context

AIエージェントによる検証結果を公開するナレッジベースが必要である。

記事は主にテキスト、コードブロック、プロンプト、AI回答、考察から構成される。記事公開のために、認証、データベース、サーバーサイドAPIを必要としない。

運用コストを抑え、GitHub上で履歴管理、レビュー、外部コントリビューションを行いたい。

候補として次を検討した。

1. GitHub Pages上の静的HTML
2. Jekyll
3. Astro、Eleventyなどの静的サイトジェネレーター
4. React、Next.jsなどのSPAまたはSSRフレームワーク
5. 外部CMS
6. 独自Webアプリケーション

## Decision

GitHub PublicリポジトリとGitHub Pagesを使用する。

公開成果物はHTML、CSS、Vanilla JavaScriptで構成する。

初期段階ではSPA、SSR、データベース、外部CMSを使用しない。

Pythonスクリプトによるローカル生成は許可するが、公開サイトの実行時にPythonやNode.jsを必要としない。

## Rationale

- GitHub Pagesだけで無料公開できる
- Git履歴とPull Requestを利用できる
- 記事ごとに独立したURLを持てる
- サーバーサイド脆弱性の範囲を抑えられる
- エージェントがファイル単位で変更しやすい
- 別ホスティングへの移行が容易
- 長期的な依存関係保守を抑えられる
- JavaScript無効時も記事を閲覧できる

## Consequences

### Positive

- 運用コストが小さい
- GitHubのレビュー機能と統合できる
- デプロイ構造が単純になる
- 記事の可搬性が高い
- バックエンド運用が不要になる

### Negative

- 管理画面を提供できない
- サーバーサイド検索を利用できない
- 高度な動的機能には向かない
- 記事件数増加時に生成処理が必要になる
- コメント機能は外部サービスへ依存する

## Rejected Alternatives

### Jekyll

GitHub Pagesとの親和性は高いが、Liquid、Front Matter、Jekyll固有挙動への依存が増える。

本プロジェクトではAIエージェント向けの構造化データと独自検証を重視するため、採用しない。

### React / Next.js

現在の要件に対して複雑すぎる。依存関係、ビルド設定、更新対応が増える。

### 外部CMS

認証、権限、外部サービス依存、料金、エクスポートなどの課題が増える。

## Validation

次が成立していることを確認する。

- GitHub Pagesで公開できる
- 記事の主要情報がJavaScriptなしで読める
- サイト生成後に静的ファイルだけで動作する
- ローカルHTTPサーバーでプレビューできる
