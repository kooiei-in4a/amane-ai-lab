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

## FND-04ではどう変えるか

次のFND-04では、この反省を実験設計へ反映します。

まず、candidateやReviewerを見る前にReferenceを強くします。FND-04はEF Core / Npgsql migrationの挙動に依存するため、外部libraryの前提、failure path、testが証明する範囲、evaluator専用runtime probeを事前に固定します。特にmodel drift、explicit migrator failure、API startupでschemaが変化しないことは、visible testが存在するだけでなく、意図的に壊したとき本当にFAILすることまで確認します。

candidate数も減らします。FND-03のように14構成を毎回投入するのではなく、実績の安定したCore候補と少数のChallengerへ絞り、8構成程度を基本とします。一方で、同じモデルを異なるHarnessで継続観測する枠は残します。評価単位は引き続き `Model + Agent/Harness + Effort + execution attempt` です。

セルフレビューは、実装execution内の曖昧な確認ではなく、**H0実装 → fresh contextでFormal Self-Review → H1修正**として分離します。これにより、H0 Score、H1 Score、Self-Review Gain、valid finding、false positive、追加時間、追加差分を測定できるようにします。セルフレビューはAgent Bの代替にはしません。

外部レビューも人数より役割の異質性を優先します。同一プロンプトを多数へ投げる方式から、Specification / Scope、Framework semantics、Runtime / Failure injection、Test assurance、Deep technical、Fast independent reviewのように責務を分けた少数Reviewerへ寄せます。

さらに、review性能の測定にはReal Final Synthesisだけでなく、事前に欠陥を埋め込んだ**Controlled Mutant**を併用する予定です。Real targetは実際のmerge gate、Mutant targetはpre-locked Goldによるreview能力測定と役割を分けます。これにより、FND-03で発生したpost-hoc Goldの弱点を減らします。

Judgeも常時3件ではなく、まず2 Judgeで比較し、VerdictやMajor root causeが割れた場合だけ3件目を追加する方式を基本にします。Major修正が必要になった場合も、全モデル一斉修正ではなく上位候補を中心に絞ります。

最後に、production mergeとbenchmark archiveを分離します。candidate registry、Head、CI、raw artifact、tag、PR close、branch cleanupは継続して残しますが、archive整理そのものを次Issue開始のcritical pathにはしません。

FND-04では、単一の総合順位だけでなく、**Implementation Score / Self-Review Gain / External Review Quality / Gold Alignment / Execution Reliability / Time・Cost**を別々に蓄積する方向へ進めます。

詳細な候補別順位、スコア、処理時間、PR、CI、Judge結果は [Benchmarks](https://kooiei-in4a.github.io/amane-ai-lab/benchmarks/) にまとめています。
