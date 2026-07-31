# workflow: create-article

1. `AGENTS.md` を読む
2. `python3 scripts/new_article.py --title "..." --slug "..."` でひな型作成
3. 調査メモ・AI回答原文・下書きなど、公開しない作業資料は `.work/<article-id>/` に置く（git 管理外。詳細は `.work/README.md`）
4. 公開する内容だけを `content/articles/` の正本へ反映する（`background.md` → `prompt.txt` → `responses/` → `analysis.md` / `analysis-plain.md` → `conclusion.md` / `conclusion-plain.md`）。`article.json` の `description` はタイトル直下の短い中心結論（2〜4行程度）としても表示されるので、meta用の一文で終わらせず中心結論を書く
5. `python3 scripts/build_site.py`
6. `python3 scripts/validate_content.py`
7. `python3 scripts/check_sensitive_data.py`
8. 差分確認とセルフレビュー
9. 必要なら Draft PR

停止条件に該当したら即停止する。

`.work/` の中身を commit してはならない。秘密情報・個人情報・顧客情報も置かない（置く場合は公開前に必ず除去し、正本へは持ち込まない）。
