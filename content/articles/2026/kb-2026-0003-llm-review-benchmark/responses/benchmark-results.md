# 16件のLLMレビュー結果

## 最終仕様判定

16件のレビューを統合しても、仕様そのものの最終結論はRound 1から変わりませんでした。

- Verdict: `FAIL`
- Ready recommendation: `NOT READY`
- Blocker: 0
- Major: 4
- Minor: 5
- Nit: 2

Majorは次の4件です。

1. 解約後の口座基本情報参照・現在残高直接参照が未定義
2. 必須Acceptance CriteriaとREQ追跡が実質的に不足
3. 冪等性の結果固定と競合後再試行の外部契約が未確定
4. 利用者管理・役割権限管理のv0.1.0製品範囲が未定義

## モデル別総合順位

| 順位 | モデル | 点数 | Verdict評価 |
| ---: | --- | ---: | --- |
| 1 | ChatGPT 5.6 Sol High | 95 | 正しい |
| 2 | ChatGPT 5.6 Sol XHigh | 92 | 正しい |
| 3 | ChatGPT 5.6 Sol Middle | 91 | 正しい |
| 4 | ChatGPT 5.6 Sol Fast | 90 | 正しい |
| 5 | Gork 4.5 High Fast | 88 | 正しい |
| 6 | ChatGPT 5.6 Luna XHigh | 86 | 正しい |
| 7 | Claude Sonnet 5 High（browser実行） | 77 | 正しい |
| 8 | Kimi K3 | 76 | 正しい |
| 9 | Composer 2.5 Fast | 73 | 不正確 |
| 10 | GLM 5.2 High | 62 | 不正確 |
| 11 | Claude Sonnet 5 High（通常実行） | 58 | 不正確 |
| 12 | DeepSeek V4 Pro | 56 | 不正確 |
| 13 | DeepSeek V4 Flash | 55 | 不正確 |
| 14 | Gemini 3.6 Flash | 54 | 結論のみ正しい |
| 15 | Gemini 3.6 Pro | 52 | 不正確 |
| 16 | Gemini 3.6 Thinking | 51 | 不正確 |

点数は、この固定課題に対する手動審理結果です。モデルの一般性能ランキングではありません。

## Verdictの内訳

- 根拠と重大度を含めて正しい`FAIL / NOT READY`: 8件
- 結論だけ`FAIL`で、主要根拠または重大度が不正確: 1件
- 誤って`READY FOR KOO APPROVAL`: 7件

半数のレビューは、Majorが残る仕様を承認可能と判断しました。

## Gold Findingの検出状況

| Finding | Full | Partial | Miss |
| --- | ---: | ---: | ---: |
| 解約後参照 | 2 | 0 | 14 |
| AC・実質トレーサビリティ | 6 | 8 | 2 |
| 冪等性・競合後再試行 | 6 | 4 | 6 |
| 利用者・役割管理範囲 | 6 | 1 | 9 |
| error code原因対応 | 4 | 4 | 8 |
| Audit Log／障害ログ | 4 | 1 | 11 |
| ADR文言の方式先取り | 1 | 0 | 15 |
| 取引履歴0件 | 1 | 0 | 15 |
| §7.3と未決事項の矛盾 | 3 | 3 | 10 |

もっとも見つかりにくかったMajorは、正本中の「解約後に許可する操作は、顧客情報参照と取引履歴閲覧のみ」という限定でした。明確に検出したのはSol HighとSol XHighだけです。

## Round 1とRound 2の比較

同一モデル・同一モードで比較できた5組は次のとおりです。

| モデル | Round 1 | Round 2 | 差分 |
| --- | ---: | ---: | ---: |
| Kimi K3 | 80 | 76 | -4 |
| Composer 2.5 Fast | 78 | 73 | -5 |
| Gork 4.5 High Fast | 76 | 88 | +12 |
| GLM 5.2 High | 66 | 62 | -4 |
| DeepSeek V4 Pro | 46 | 56 | +10 |

平均は69.2から71.0へ上昇しましたが、正しいVerdict数は2件から2件のままでした。プロンプト改善だけでは、主要な見逃しを安定して解消できませんでした。

## 同一モデルの再現性

Claude Sonnet 5 Highは同じRound 2で2回実行しました。

| 実行 | 点数 | Verdict |
| --- | ---: | --- |
| 通常実行 | 58 | READY |
| browser実行 | 77 | NOT READY |

同じモデルラベルでも19点差があり、Verdictが反転しました。実行環境、サンプリング、読み取り順、ツール利用などの影響をモデル能力と分離できないため、単発結果を確定判定に使うべきではありません。
