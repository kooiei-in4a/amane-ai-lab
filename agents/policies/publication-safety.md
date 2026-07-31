# 公開安全性

## 公開禁止

- APIキー、パスワード、アクセストークン、Cookie、秘密鍵、接続文字列
- 非公開リポジトリの内容
- 顧客名、個人メール、電話番号、個人住所
- 社内URL、社内IP、ローカルファイルパス
- 契約上非公開の金額
- 未公開障害情報、悪用に直結する未修正脆弱性情報

## 検査

公開前に `python scripts/check_sensitive_data.py` を実行する。

疑いが解消できない場合は停止し、人間へ報告する。

### 自動ゲート（多層）

| 層 | 仕組み | タイミング |
|---|---|---|
| ローカル | Git `pre-commit`（`.githooks/`） | commit 直前（staged のみ） |
| エージェント | Cursor `beforeShellExecution` | `git commit` / `git push` 直前 |
| 共有 | CI（`validate.yml` / `pages.yml`） | PR・Pages デプロイ前（フルスキャン） |

初回セットアップ:

```bash
python scripts/install_git_hooks.py
```

- Git hook は `core.hooksPath=.githooks` をローカル設定する（リポジトリには `.githooks/` をコミットする）
- Cursor hook は `.cursor/hooks.json` を参照する（`--no-verify` でも Cursor 側はブロックしうる）
- 最終的な公開阻止は CI のフルスキャンに依存する

## Git履歴

秘密情報を一度でもGitへ追加した場合、通常の削除だけでは不十分である。

- commit前に検出したら停止する
- commit後に検出したら通常修正を続行せず、人間へ報告する
