# 記事削除・ID 初期リセットチェック

## 共通

- [ ] 人間の明示承認がある
- [ ] archive では不十分である理由が明確
- [ ] 対象の記事 ID / 正本パス / 公開 URL を確認した
- [ ] 正本を変更し、生成物だけを手で消していない
- [ ] `python3 scripts/build_site.py` 成功
- [ ] `python3 scripts/validate_content.py` 成功
- [ ] `python3 scripts/check_sensitive_data.py` 成功
- [ ] Git 履歴の書き換えをしていない（秘密情報時は別承認）
- [ ] giscus を自動削除していない
- [ ] Draft PR までとし、merge は人間

## hard delete（通常）

- [ ] `content/retired-article-ids.json` に ID を追加した
- [ ] `notes` に削除理由がある
- [ ] 当該 ID が再利用されないこと

## 記事 ID 初期リセット

- [ ] 人間が `KB-YYYY-0001` からのやり直しを明示した
- [ ] 残す正本記事が 0 件
- [ ] `retired-article-ids.json` が空の台帳（`ids: []`, `notes: {}`）
- [ ] 次の採番が `KB-YYYY-0001` になることを確認した（または確認可能）
