# コンテンツ権限

## 正本

- 記事の正本は `content/articles/` 配下の構造化ファイルとする。
- `articles/` 配下のHTML、`data/articles.json`、`sitemap.xml`、`feed.xml` は生成物とする。

## 編集ルール

1. 表示や文言の修正は正本を変更する。
2. 生成物だけを直接変更してはならない。
3. 正本変更後は `python scripts/build_site.py` を実行する。
4. CIは再生成差分が残る場合に失敗させる。

## 禁止

- 生成済みHTMLへの手作業パッチ
- 記事IDの再利用
- 公開後URLの独断変更
- AI回答の完全性区分を偽ること
