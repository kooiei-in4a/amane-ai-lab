# workflow: archive-article

公開後に記録を残したまま退役させる手順。既定経路である。
hard delete や ID 初期リセットが必要なら本 workflow ではなく、それぞれ
`agents/workflows/delete-article.md` / `agents/workflows/reset-article-ids.md` を使う。

1. status を `archived` または `superseded` にする
2. `supersededBy` がある場合は設定する
3. URL は原則維持する
4. build / validate / sensitive-data check を実行する
5. 必要なら Draft PR まで。merge は人間

削除（正本除去）が必要なら停止し、人間承認のうえで `delete-article` へ移る。
