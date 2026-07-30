# Contributing

## 開発の流れ

1. `AGENTS.md` を読む
2. 記事や実装を変更する（正本は `content/articles/`）
3. 生成と検証を実行する

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_site.py
python3 scripts/validate_content.py
python3 scripts/check_sensitive_data.py
python3 -m unittest discover -s tests
```

4. Draft Pull Request を作成する
5. merge はメンテナが行う

## 記事追加

```bash
python3 scripts/new_article.py --title "タイトル" --slug "my-slug"
```

その後、正本ファイルを編集し、build / validate を実行してください。

## 禁止事項

- 生成済みHTML（`articles/`）だけの修正
- 秘密情報の commit
- エージェントによる merge / release / Pages本番設定変更
