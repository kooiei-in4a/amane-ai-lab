# FND-02 実装比較ベンチマーク

## 対象Issue

Issue #40 `[FND-02] 共通API実行契約を確立する` は、FND-01で作った基盤の上に、API request共通の実行契約を置くIssueです。

主な対象は次のとおりです。

- 共通REST error envelope
- exception-to-HTTP mappingの拡張点
- correlation IDの生成・伝播
- caller supplied correlation IDの扱い
- injected `TimeProvider`
- JSON console technical logging
- sensitive dataをtechnical logへ出さない方針
- request-level API integration test

business error code全件、Audit Log persistence、認証認可、PostgreSQL、Docker、health contractなどはOut of scopeでした。

FND-01より難しいのは、コードが存在するだけでは足りず、HTTP request、middleware、DI、serializer、logging providerを通った**最終的な外部出力**まで確認する必要がある点です。

## 14候補

FND-01と同じ14のModel + Agent/Harness構成を使いました。

| # | Model | Agent / Harness | Candidate PR | CI |
|---:|---|---|---:|---|
| 1 | DeepSeek V4 Pro | Open Code | #67 | SUCCESS |
| 2 | Qwen3.7 Plus | Open Code | #70 | SUCCESS |
| 3 | GPT-5.6 Luna | Open Code | #72 | SUCCESS |
| 4 | DeepSeek V4 Flash | Open Code | #81 | SUCCESS |
| 5 | MiMo-V2.5 | Open Code | #74 | SUCCESS |
| 6 | MiMo-V2.5-Pro | Open Code | #78 | SUCCESS |
| 7 | MiniMax M3 | Open Code | #76 | SUCCESS |
| 8 | GPT-5.6 Luna | Codex | #66 | SUCCESS |
| 9 | GPT-5.6 Terra | Codex | #68 | SUCCESS |
| 10 | GPT-5.6 Sol | Codex | #71 | SUCCESS |
| 11 | Grok 4.5 | Cursor | #65 | SUCCESS |
| 12 | Composer 2.5 | Cursor | #69 | SUCCESS |
| 13 | Claude Sonnet 5 | Claude Code | #80 | SUCCESS |
| 14 | Claude Opus 5 | Claude Code | #79 | SUCCESS |

FND-02もcandidate 14件すべてCI SUCCESSでした。candidate HeadとPR Headを確認したうえでannotated tagへ固定し、candidate PRは比較実験としてcloseされています。

FND-02のarchiveにもcandidate別の正式Coding Scoreは記録されていません。ここでも点数や順位は補完しません。

## FND-02で増えた「証拠の質」という観点

FND-02の比較を通して、共通benchmark方法論には検証証拠の扱いが追加されました。

runtime wiringや外部から見えるcontractを評価するとき、次の3つは同じ証拠ではありません。

1. production entry point / production pipelineを通すrequest-level test
2. test側でproduction componentを組み直したhost
3. middleware / handler / serviceの直接呼出し

3でも局所的なロジックは確認できます。しかし、実際のDI設定、middleware順序、serializer、logging設定が本番と同じかまでは証明できません。

loggingやsecret non-disclosureも同じです。test loggerが作った文字列だけを確認しても、実際のJSON console providerが何を出すかの証拠にはなりません。

この知見はFND-02の比較後、共通benchmark方法論へ反映されました。

## Final synthesisも一度では終わらなかった

14候補を比較した後、`agent/issue-40-fnd-02-final-code` でFinal synthesisを作成しました。

その後の独立レビューでは、残ったMajor 1件とMinor 1件への対応が必要になりました。最終PR #83では、承認済み判断D-01 / D-02に沿って次を修正しています。

- generic 500を `internal_error` として固定
- application pipeline内の404 / 405 / 415を共通error envelopeへ統一
- request abortとapplication内部cancellationを区別
- response開始後のexceptionを正常な200完了として扱わずabort
- 実Kestrelと実JSON console出力を使ってsecret非露出を確認

最終Head `d987733d1a606b21c971860565c687e4ba47ff8a` では、UnitTests 3/3、IntegrationTests 27/27、warning 0、CI PASS。Agent B再レビューはBlocker / Major / Minor / Nitすべて0、Claude Opus 5による最終レビューもAPPROVE / Merge Ready YESとなり、PR #83はmergeされています。

ここで重要なのは、14候補を比較して統合版を作っても、それだけでmerge可能とはしなかったことです。Final synthesisにも通常の実装と同じ独立レビューを掛けました。

## 一次資料

- [Issue #40](https://github.com/kooiei-in4a/minimal-bank-system/issues/40)
- [FND-02 benchmark archive](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/fnd02-model-comparison/analysis.md)
- [共通benchmark方法論](https://github.com/kooiei-in4a/minimal-bank-system/blob/main/docs/benchmarks/model-implementation-benchmark-methodology.md)
- [Final synthesis PR #83](https://github.com/kooiei-in4a/minimal-bank-system/pull/83)
