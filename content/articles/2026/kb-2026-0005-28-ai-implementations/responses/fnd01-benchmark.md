# FND-01 実装比較ベンチマーク

## 対象Issue

Issue #39 `[FND-01] Solution・project・build/test CIを確立する` は、.NET 10 modular monolithの土台を作るIssueです。

主な対象は次のとおりです。

- API / Application / Domain / Infrastructure / Testsのproject境界
- project reference
- `net10.0`
- nullable、analyzer、warning policy
- exact NuGet version pinning
- localとCIで同じrestore / build / testを実行できる状態

一方、error envelope、correlation ID、`TimeProvider`、logging、PostgreSQL、Docker、business codeなどは明示的にOut of scopeでした。

この「入れてはいけないもの」が多い点が、FND-01の重要な評価ポイントです。

## 14候補

同一Issueを、次の14構成へ独立実装させました。

| # | Model | Agent / Harness | Effort | 実験時の処理時間記録 | Candidate PR | CI |
|---:|---|---|---|---:|---:|---|
| 1 | DeepSeek V4 Pro | Open Code | Max | 6 | #48 | SUCCESS |
| 2 | Qwen3.7 Plus | Open Code | Max | 12 | #49 | SUCCESS |
| 3 | GPT-5.6 Luna | Open Code | Max | 15 | #50 | SUCCESS |
| 4 | DeepSeek V4 Flash | Open Code | Max | 10 | #51 | SUCCESS |
| 5 | MiMo-V2.5 | Open Code | 未指定 | 12 | #52 | SUCCESS |
| 6 | MiMo-V2.5-Pro | Open Code | 未指定 | 9 | #53 | SUCCESS |
| 7 | MiniMax M3 | Open Code | Thinking | 17 | #54 | SUCCESS |
| 8 | GPT-5.6 Luna | Codex | Xhigh | 14 | #55 | SUCCESS |
| 9 | GPT-5.6 Terra | Codex | Xhigh | 13 | #56 | SUCCESS |
| 10 | GPT-5.6 Sol | Codex | Xhigh | 17 | #57 | SUCCESS |
| 11 | Grok 4.5 | Cursor | high | 8 | #58 | SUCCESS |
| 12 | Composer 2.5 | Cursor | 未指定 | 5 | #59 | SUCCESS |
| 13 | Sonnet 5 | Claude Code | Xhigh | 16 | #60 | SUCCESS |
| 14 | Opus 5 | Claude Code | Xhigh | 19 | #61 | SUCCESS |

処理時間は実験時の記録値です。archiveでは単位を補完していないため、この記事でも勝手に「分」などへ置き換えません。

candidate 14件はすべてCI SUCCESSでした。各candidate PRはmergeせずcloseし、Headはannotated tagで固定されています。

## 比較で見たもの

FND-01の比較では、単にbuildできるかではなく、主に次を確認しました。

- solution / project構成
- project referenceの依存方向
- package version
- compiler / analyzer設定
- test構成
- CI
- secret混入
- placeholder実装
- unrelated change
- 過剰設計
- 後続Issueの先取り

共通のCoding Scoreは100点で、Issue達成度25、正しさ15、Scope遵守15、設計10、テスト10、コード品質10、変更精度10、リスク管理5という枠組みです。

ただし、FND-01のarchiveにはcandidateごとの正式なCoding Scoreが記録されていません。archive作業では再採点もしていません。そのため、この記事ではcandidate順位を復元しません。

## Final integrated implementation

14候補を比較した後、良い設計と検証方法を選んでFinal integrated implementationを作りました。

- Branch: `agent/issue-39-fnd-01-final-code`
- Head: `d8e75bc6eab7fd14b7a58042b24deabe2227e189`
- Coding Score: 99/100
- PR: #62
- Final candidateではなく、curated / synthesized implementation

PR #62では、clean相当の状態からrestore、build、testが成功し、warning 0、Unit 3件、Integration 2件がPASSしています。Agent B独立レビューもBlocker / Major / Minor / Nitすべて0で、merge後のmain CIもPASSしました。

重要なのは、このFinal integrated implementationを「15番目のモデル」として扱っていない点です。14候補の比較後、人間の選択を含めて作った統合成果物です。

## 一次資料

- [Issue #39](https://github.com/kooiei-in4a/minimal-bank-system/issues/39)
- [FND-01 benchmark archive](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd01-model-comparison/analysis.md)
- [共通benchmark方法論](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/model-implementation-benchmark-methodology.md)
- [Final implementation PR #62](https://github.com/kooiei-in4a/minimal-bank-system/pull/62)
