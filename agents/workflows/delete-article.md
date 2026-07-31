# workflow: delete-article

hard delete（正本削除）の手順。既定は archive であり、本 workflow は例外経路である。
判断基準は `agents/policies/article-lifecycle.md` を参照する。

1. 人間の明示承認を確認する。なければ停止して報告する
2. 対象の記事 ID、正本パス、公開 URL、削除理由を記録する
3. 初期リセットが目的なら `agents/workflows/reset-article-ids.md` へ移る
4. `content/articles/...` の正本ディレクトリを削除する
5. 記事 ID を `content/retired-article-ids.json` の `ids` に追加し、`notes` に理由を書く
6. `python3 scripts/build_site.py` を実行する
7. `python3 scripts/validate_content.py` を実行する
8. `python3 scripts/check_sensitive_data.py` を実行する
9. 差分を確認する（正本削除・retired 更新・生成物更新のみ）
10. `agents/checklists/delete-article.md` を確認する
11. 必要なら Draft PR まで。merge は人間

禁止・注意:

- 削除済み ID の再利用
- 生成 HTML だけの手削除（必ず build で再生成する）
- Git 履歴の書き換え（秘密情報混入時は別承認）
- giscus Discussion の自動削除
