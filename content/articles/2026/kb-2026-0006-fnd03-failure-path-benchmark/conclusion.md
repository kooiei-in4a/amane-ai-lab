# まとめ

FND-03では、実PostgreSQL integration test基盤を複数AIへ独立実装させ、統合版へ独立レビューを掛け、そこで残ったMajorをさらに複数AIへ独立修正させました。

最終的に強く残ったのは、モデル順位よりも次の事実です。

- 17件のraw independent reviewは、後からtechnical Goldとして確定したblocking root causeを検出していなかった
- Major修正14候補はすべてexact Head CI SUCCESSだった
- 3-Judge裁定でmerge-readyだったのは1 / 14だった
- 最終productionはBenchmark 1位をそのまま採用せず、複数候補のtest資産と既存regressionを統合して再レビューした

FND-03の問題は、通常の正常系では見えにくいresource cleanupとownershipのfailure pathにありました。

この種のコードでは、「testがある」「CIが緑」「複数ReviewerがApprove」という証拠を積み重ねても、それらが同じ前提に依存していると同じ見逃しを共有します。

特に重要だったのは、壊れ得るTestcontainers instanceそのものをresource ownershipの唯一の根拠にしないことでした。container create前に独立したownership labelを持つことで、ID取得前のfailureでも実resourceを再発見し、cleanupできる設計になりました。

また、17-model review benchmarkのGoldは完全blindな事前locked Goldではなく、raw review収集後の追加一次source調査で明確化したpost-hoc adjudicationです。この制約も結果と一緒に残します。

AIを実務で使うとき、候補やReviewerを増やすこと自体は品質保証になりません。

最終的に必要なのは、**どのtestが何を証明しているか、failure時のownerは誰か、依存libraryのsemanticsは本当に正しいかを一次証拠で確認すること**です。

FND-03は、AIの実装性能だけでなく、レビュー性能、既知問題の修正性能、そして複数AIの結果をどう裁定するかまで含めた実験になりました。

詳細な候補別順位、スコア、処理時間、PR、CI、Judge結果は [Benchmarks](https://kooiei-in4a.github.io/amane-ai-lab/benchmarks/) にまとめています。
