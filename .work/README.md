# `.work/` — ローカル作業資料（git 管理外）

このディレクトリは記事執筆用の作業置き場である。中身は `.gitignore` により commit されない（この README と `.gitkeep` のみ追跡する）。

## 使い方

1. 記事 ID ごとのサブディレクトリを作る

```text
.work/KB-2026-0001/
  ├─ prompt-draft.txt
  ├─ responses/
  └─ notes.md
```

2. 調査メモ、AI回答の原文、未整形の下書き、参考資料などをここに置く
3. 公開する内容だけを `content/articles/` の正本へ移す
4. `.work/` のファイルを stage / commit しない

## 注意

- 秘密情報・個人情報・顧客情報を置かない（やむを得ず扱う場合も正本へ持ち込まない）
- 正本は常に `content/articles/`
- 生成 HTML（`articles/`）を手で編集しない
