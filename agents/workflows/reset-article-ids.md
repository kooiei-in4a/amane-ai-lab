# workflow: reset-article-ids

記事 ID の初期リセット手順。通常の hard delete 後に retired へ積む運用とは別経路である。
判断基準は `agents/policies/article-lifecycle.md` を参照する。

前提（すべて必須）:

- 人間が「`KB-YYYY-0001` からやり直す」と明示している
- 残す正本記事が 0 件になること
- 立ち上げ直後、または本番記事を捨てて採番をやり直す判断であること

手順:

1. 人間の明示承認を確認する。なければ停止して報告する
2. 残す記事が無いことを確認する。残記事があれば削除対象を確定する
3. 対象の正本ディレクトリをすべて削除する
4. `content/retired-article-ids.json` を空の台帳にする

```json
{
  "schemaVersion": 1,
  "ids": [],
  "notes": {}
}
```

5. `python3 scripts/build_site.py` を実行する
6. `python3 scripts/validate_content.py` を実行する
7. `python3 scripts/check_sensitive_data.py` を実行する
8. 記事一覧が空であること、生成 HTML に旧記事が残っていないことを確認する
9. 必要なら `next_article_id` / `new_article.py` で次 ID が `KB-YYYY-0001` になることを確認する
10. `agents/checklists/delete-article.md` の初期リセット項目を確認する
11. 必要なら Draft PR まで。merge は人間

禁止・注意:

- 正本が 1 件でも残る状態での台帳クリア
- 承認なき ID 再利用
- Git 履歴の書き換え（秘密情報混入時は別承認）
- giscus Discussion の自動削除
