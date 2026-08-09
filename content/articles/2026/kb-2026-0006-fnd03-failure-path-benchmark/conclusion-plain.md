# まとめ

今回の実験では、AIにコードを書かせるだけでなく、別のAIにレビューさせ、見つかった問題をさらに複数のAIに直させました。

それでも、AIを増やせば自動的に安全になるわけではありませんでした。

17のレビュー結果は、後から分かった重大なcleanup問題を見つけられていませんでした。問題を教えた後の14修正案は全部CIが成功しましたが、そのままmergeできると判断できたのは1件だけです。

理由は、通常のテストでは起きにくい失敗経路にありました。

containerを作った直後や削除の途中で失敗すると、管理objectが壊れたりIDを失ったりして、実際のcontainerだけが残る可能性があります。

最も強かった修正は、管理objectやcontainer IDだけに頼らず、作成前から専用labelでownershipを持つ方法でした。

この結果から、重要なコードでは次を確認した方がよいと考えています。

- CIが何を確認していて、何を確認していないか
- 失敗したときresourceを誰が回収するか
- 依存libraryの実際の挙動を確認したか
- 複数AIの意見が同じ前提に依存していないか

AIの多数決より、最後に一次証拠へ戻ることが重要でした。

## FND-04で変えること

次のFND-04では、FND-03と同じやり方をそのまま繰り返しません。

- 実装候補は14から8程度へ減らす
- EF Core / Npgsqlの前提やfailure pathをcandidate実行前に確認する
- evaluator専用のadversarial probeを事前に用意する
- セルフレビューをH0実装、Formal Self-Review、H1修正に分けて効果を測る
- Reviewer数を減らし、仕様、framework、failure path、test assuranceなど役割を分ける
- Real Final Synthesisとは別に、意図的な欠陥を入れたControlled Mutantでreview能力を測る
- Judgeはまず2件とし、重大な不一致がある場合だけ3件目を使う
- Major修正は原則として上位候補だけに絞る
- production mergeとbenchmark archiveを別工程として扱う

また、実装点数だけでなく、Self-Review Gain、External Review Quality、Gold Alignment、Execution Reliability、Time / Costを分けて記録する予定です。

全候補の詳しい順位やスコアはBenchmarksページで公開します。
