# はじめに

AIコーディングの比較記事は、モデル名と点数だけでも作れます。けれど、実際の開発で知りたいのはもう少し地味なことです。

- 既存の仕様やADRを読めるか
- Issueの範囲だけを直せるか
- buildやtestが本当に通るか
- テストが「実装したつもり」を確認しているだけになっていないか
- 余計な機能を先回りして入れないか
- 最後に人間が安心してmergeできる差分になっているか

そこで `minimal-bank-system` では、同じGitHub Issueを複数のAIコーディング環境へ独立して実装させる実験を2回行いました。

1回目のFND-01は、.NET 10のSolution、project境界、build/test CIを作る基盤整備です。2回目のFND-02は、共通error envelope、correlation ID、`TimeProvider`、JSON technical loggingといったAPI実行契約です。

どちらも14の `Model + Agent/Harness` 構成を使いました。Open Code、Codex、Cursor、Claude Codeが混在し、一部は同じモデルを別のHarnessでも実行しています。

結果だけ先に書くと、archiveに残ったcandidate 28件のCIはすべてSUCCESSでした。

それでも、比較を「全員合格」で終わらせることはできませんでした。

この記事では個別モデルの勝敗より、2回の実装比較から見えてきた**AI実装をどう評価するか**と、**複数のAIをどう開発工程へ組み込むか**をまとめます。
