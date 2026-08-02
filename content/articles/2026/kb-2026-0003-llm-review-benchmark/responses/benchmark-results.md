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

## Round 2の実行環境

Round 2は、同じポータブルプロンプトとEvidence bundleを各実行環境へ投入しました。環境ごとのUI、ファイル読込み、推論モード、ツール実装は同一ではありません。

| 実行環境 | モデル・設定 |
| --- | --- |
| Browser | ChatGPT 5.6 Sol High、Sol XHigh、Sol Middle、Sol Fast、Luna XHigh、Gemini 3.6 Flash、Gemini 3.6 Pro、Gemini 3.6 Thinking、Claude Sonnet 5 High（browser実行） |
| Cursor | Gork 4.5 High Fast、Composer 2.5 Fast |
| OpenCode | Kimi K3、GLM 5.2 High、DeepSeek V4 Pro、DeepSeek V4 Flash |
| Claude Desktop app | Claude Sonnet 5 High（通常実行） |

Claude Sonnet 5 Highは、Browser実行とDesktop app実行を別レビューとして評価しました。したがって、レビュー成果物は16件、モデル・構成ラベルは15種類です。

## モデル別総合順位・実行時間

| 順位 | モデル | 実行環境 | 点数 | Verdict評価 | 概算時間 |
| ---: | --- | --- | ---: | --- | ---: |
| 1 | ChatGPT 5.6 Sol High | Browser | 95 | 正しい | 約7分 |
| 2 | ChatGPT 5.6 Sol XHigh | Browser | 92 | 正しい | 約10分 |
| 3 | ChatGPT 5.6 Sol Middle | Browser | 91 | 正しい | 約4分 |
| 4 | ChatGPT 5.6 Sol Fast | Browser | 90 | 正しい | 約2分 |
| 5 | Gork 4.5 High Fast | Cursor | 88 | 正しい | 約4分 |
| 6 | ChatGPT 5.6 Luna XHigh | Browser | 86 | 正しい | 約7分 |
| 7 | Claude Sonnet 5 High（browser実行） | Browser | 77 | 正しい | 約12分 |
| 8 | Kimi K3 | OpenCode | 76 | 正しい | 約18分 |
| 9 | Composer 2.5 Fast | Cursor | 73 | 不正確 | 約2分 |
| 10 | GLM 5.2 High | OpenCode | 62 | 不正確 | 約5分 |
| 11 | Claude Sonnet 5 High（通常実行） | Claude Desktop app | 58 | 不正確 | 約12分 |
| 12 | DeepSeek V4 Pro | OpenCode | 56 | 不正確 | 約5分 |
| 13 | DeepSeek V4 Flash | OpenCode | 55 | 不正確 | 約7分 |
| 14 | Gemini 3.6 Flash | Browser | 54 | 結論のみ正しい | 約1分 |
| 15 | Gemini 3.6 Pro | Browser | 52 | 不正確 | 約4分 |
| 16 | Gemini 3.6 Thinking | Browser | 51 | 不正確 | 約2分 |

点数は、この固定課題に対する手動審理結果です。モデルの一般性能ランキングではありません。

時間は手元で計測した概算の参考値です。API単体の推論時間ではなく、画面操作、Evidence読込み、ツール処理、回答表示までを含む場合があります。実行環境、混雑、キャッシュ、出力量が統制されていないため、厳密な速度ベンチマークとして扱えません。

## 精度と速度を合わせて読む

今回の課題では、Sol Fastは約2分で90点、Sol Middleは約4分で91点でした。高いPrecisionを保ちながら短時間で一次判定する用途では有力です。

Sol HighとSol XHighは時間を多く使いますが、正本横断のMajor Findingまで検出しました。最終ゲートや高リスク仕様では、追加時間に意味があります。

一方、短時間で終わること自体は品質を保証しません。Gemini 3.6 Flashは約1分でしたが、主要根拠の多くを外しました。Kimi K3は約18分を要しましたが、点数は76でした。時間と精度は単純比例しません。

## Verdictの内訳

- 根拠と重大度を含めて正しい`FAIL / NOT READY`: 8件
- 結論だけ`FAIL`で、主要根拠または重大度が不正確: 1件
- 誤って`READY FOR KOO APPROVAL`: 7件

半数近くのレビューは、Majorが残る仕様を承認可能と判断しました。

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

| 実行 | 環境 | 点数 | Verdict | 概算時間 |
| --- | --- | ---: | --- | ---: |
| 通常実行 | Claude Desktop app | 58 | READY | 約12分 |
| browser実行 | Browser | 77 | NOT READY | 約12分 |

同じモデルラベル、ほぼ同じ所要時間でも19点差があり、Verdictが反転しました。実行環境、サンプリング、読み取り順、ツール利用などの影響をモデル能力と分離できないため、単発結果を確定判定に使うべきではありません。
