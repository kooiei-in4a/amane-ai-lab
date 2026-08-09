# FND-03 完全実験アーカイブ

## 対象

Issue #41 `[FND-03] 実PostgreSQL integration test基盤を確立する`。

PostgreSQL 18 / Testcontainersを使い、test isolation、database lifecycle、parallel execution、cleanup、failure reporting、CI実行までを共通integration test foundationとして成立させる課題です。

## 実験の流れ

FND-03は次の順序で実施しました。

1. 14構成による初期実装Benchmark
2. 上位候補の知見を統合したFinal Synthesis
3. Final Synthesisへの17-model independent review
4. Testcontainers 4.13.0一次source突合によるpost-hoc Gold / cleanup Major確定
5. 同一Majorを14構成へ独立修正させるBenchmark
6. 3 JudgeによるFinding adjudication
7. 選択したarchitectureとtest資産を統合したproduction implementation

## Canonicalな最終結果

- Review Benchmarkのblocking Gold root cause検出: 0 / 17
- Major-fix候補のexact Head CI: 14 / 14 SUCCESS
- 3-Judge裁定のmerge-ready: 1 / 14
- Final fix Benchmark 1位: GPT-5.6 Sol / Codex — 94 / 100
- Final production: Agent B APPROVE、Blocker / Major / Minor / Nit = 0 / 0 / 0 / 0
- PR #104 MERGED、Issue #41 CLOSED / COMPLETED

候補別のランキング、全スコア、処理時間、PR、Head SHA、CI、Judge別結果は記事本文へ重複掲載せず、amane AI LabのBenchmarksページに掲載します。

## 技術的な核心

Testcontainers 4.13.0では、Docker resourceの削除完了前にdisposed stateがlatchされるfailure pathがあり、同じfailed instanceへの2回目のDisposeがno-opになり得ます。

さらにMajor修正比較では、Docker create成功後・Testcontainers内部へcontainer IDが保存される前に失敗するpartial-create pathが重要な裁定点になりました。

最終的に選ばれたarchitectureは、create前にunique ownership labelを確立し、Testcontainers instanceやIDだけに依存せず、label query / remove / re-queryでresource absenceを確認します。

## 方法論上の注意

17-model review benchmarkのGoldは完全blindな事前locked Goldではありません。

raw review収集後の追加一次source突合でblocking Majorが明確化されたため、canonical archiveでは `post_hoc_adjudication: true` としています。

そのため「17モデルが事前に固定されたblind Gold testで全滅した」とは表現しません。

## 一次資料

- [Issue #41](https://github.com/kooiei-in4a/minimal-bank-system/issues/41)
- [FND-03 Complete Experiment Archive](https://github.com/kooiei-in4a/minimal-bank-system/tree/main/docs/benchmarks/fnd03-model-comparison)
- [Initial implementation summary](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd03-model-comparison/summary.md)
- [Review Benchmark canonical evaluation](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd03-model-comparison/review-benchmark/full-evaluation.md)
- [Post-hoc Gold](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd03-model-comparison/review-benchmark/gold-review.md)
- [Major-fix adjudicated evaluation](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd03-model-comparison/final-fix/final-evaluation.md)
- [Final production outcome](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd03-model-comparison/final-outcome.md)
