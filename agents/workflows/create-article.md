# workflow: create-article

1. `AGENTS.md` を読む
2. `python3 scripts/new_article.py --title "..." --slug "..."` でひな型作成
3. 正本ファイルを編集する
4. `python3 scripts/build_site.py`
5. `python3 scripts/validate_content.py`
6. `python3 scripts/check_sensitive_data.py`
7. 差分確認とセルフレビュー
8. 必要なら Draft PR

停止条件に該当したら即停止する。
