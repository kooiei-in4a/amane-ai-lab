# Raw LLM source snapshots

このディレクトリには、今回の統合に入力した2本の他LLM回答を**原文のバイト列へ完全復元できる形**で保存している。

モデル名、Web検索利用有無など、元ファイルから確認できないメタデータは推測していない。

## Source A

元ファイル名:

```text
貼り付けたマークダウン（1）(20260905-120710).md
```

元サイズ: `33102` bytes  
SHA-256:

```text
4d14819524886580e795bebbd221a2eed1459ff0f3ad88cd8ce4dc80470cfc87
```

保存ファイル:

```text
llm-result-a.md.b64.part-01
llm-result-a.md.b64.part-02
llm-result-a.md.b64.part-03
```

復元:

```bash
cat llm-result-a.md.b64.part-* | base64 -d > llm-result-a.md
sha256sum llm-result-a.md
```

## Source B

元ファイル名:

```text
貼り付けたマークダウン（2）(20260905-120720).md
```

元サイズ: `69240` bytes  
SHA-256:

```text
cf0dbf47fda9f1d794548eff0baaf19ecacff3ed65f09444f642b29858612b5b
```

保存ファイル:

```text
llm-result-b.md.gz.b64.part-01
llm-result-b.md.gz.b64.part-02
```

復元:

```bash
cat llm-result-b.md.gz.b64.part-* | base64 -d | gzip -d > llm-result-b.md
sha256sum llm-result-b.md
```

## 利用上の注意

- この2本は市場調査結果や検証済み事実ではなく、仮説空間を広げるための独立ブレスト入力。
- 統合時に採用されなかった少数意見も、後で再探索できるよう原文を保持している。
- 統合版は `../responses/chatgpt.md` を参照する。
