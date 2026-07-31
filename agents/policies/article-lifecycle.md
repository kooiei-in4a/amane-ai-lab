# 記事ライフサイクル

## ステータス遷移

```text
draft → review → published → archived | superseded
                              ↓
                         hard delete（例外）
```

| Status | 意味 | 正本 | URL |
|---|---|---|---|
| `draft` | 執筆中 | あり | 生成されるが公開対象外の扱い可 |
| `review` | 公開前レビュー中 | あり | 同上 |
| `published` | 公開済み | あり | 安定維持 |
| `superseded` | 後継記事あり | あり | 原則維持。`supersededBy` を設定 |
| `archived` | 記録目的で保管 | あり | 原則維持 |

## 既定: archive / superseded

公開後に「もう推したくない」「後継がある」場合の既定は soft 退役とする。

- `archived` または `superseded` にする
- 正本と URL は残す
- 手順は `agents/workflows/archive-article.md`

## 例外: hard delete

次のような場合のみ、正本を削除してよい。

- 誤公開・サンプル廃棄
- 公開継続が不適切
- 記事そのものをリポジトリに置きたくない

必須条件:

- 人間の明示承認
- 手順は `agents/workflows/delete-article.md`
- 削除した ID を `content/retired-article-ids.json` に登録する
- 削除済み ID は再利用しない
- 公開 URL は 404 になる（tombstone は作らない）
- Git 履歴の書き換えはしない（秘密情報混入時は別承認）
- giscus Discussion は自動削除しない

## 例外: 記事 ID 初期リセット

通常の「削除済み ID 再利用禁止」と衝突する操作である。次をすべて満たす場合のみ許可する。

- 人間が「`KB-YYYY-0001` からやり直す」と明示した
- 残す正本記事が 0 件である
- サイト立ち上げ直後、または本番記事を捨てて採番をやり直す判断である

手順は `agents/workflows/reset-article-ids.md`。

初期リセットでは `content/retired-article-ids.json` を空の台帳に戻し、次の採番を `KB-YYYY-0001` から開始する。
