# Security Policy

## 報告

秘密情報の混入、脆弱性、公開事故の疑いがある場合は、Issueで詳細な秘密情報を晒さず、リポジトリ管理者へ連絡してください。

## 公開禁止の例

- APIキー、トークン、秘密鍵、接続文字列
- 顧客情報・個人情報
- 社内URL、社内IP、ローカルパス

## エージェント向け

`AGENTS.md` と `agents/policies/publication-safety.md` を確認し、疑いがある場合は commit 前に停止すること。

ローカルでは `python scripts/install_git_hooks.py` により Git pre-commit が有効になる。Cursor でも `git commit` / `git push` 前に同じスキャナが走る。CI のフルスキャンが最後の公開ゲートである。
