# まとめ

FND-01とFND-02では、14のModel + Agent/Harnessを同じIssueへ独立実装させました。合計28candidateのCIは、archive上すべてSUCCESSでした。

それでも、AI実装の評価をCIだけで終わらせることはできませんでした。

FND-01では、後続Issueを先取りせず、必要な基盤だけを作るScope規律と変更の最小性が重要でした。

FND-02では、テストの有無よりも、production entry point、middleware、serializer、logging providerまで含めて、どの経路を通した証拠なのかが重要になりました。Final synthesisも独立レビューで修正を受け、実Kestrelと実JSON console outputまで確認してからmergeしています。

この結果から、実務での評価単位はモデル名だけでは足りないと考えています。

見るべきなのは `Model + Agent/Harness + Effort + execution attempt` と、その結果として残ったdiff、test、CIです。

また、14候補を毎回作る必要もありません。

通常のIssueなら「1実装 + 別AIの独立レビュー」。基盤、認証、データ整合性など重要なIssueなら「2〜3候補を独立実装 → diff比較 → 必要なら統合 → 別Reviewerで再確認」くらいが現実的です。

今回の実験で残したいのは「どのモデルが1位だったか」より、**AIに複数案を作らせても、最後はIssueと実際の成果物へ戻って判断する**という進め方です。

なお、FND-01 / FND-02のarchiveにはcandidate別Coding Scoreが正式記録されていません。各候補1試行でEffortやHarnessも異なるため、この記事ではモデル一般性能の順位は出していません。
