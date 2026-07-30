# workflow: update-article

1. 対象記事の正本パスを特定する
2. 生成物ではなく正本を編集する
3. `updatedAt` / `lastVerifiedAt` を必要に応じて更新する
4. build / validate / sensitive-data check
5. 差分確認
6. Draft PR（必要な場合）
