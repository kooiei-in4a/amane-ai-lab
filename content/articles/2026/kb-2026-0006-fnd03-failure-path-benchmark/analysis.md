# 17のAIレビューが見逃した。14の修正は全部CI成功、それでもmergeできたのは1つだった

## まず結果

FND-03で最終的に残った数字は、かなり極端でした。

- 初期実装: 14構成、13件を採点
- Final Synthesis: 当時98/100相当と評価
- 独立レビュー: 17構成
- blocking Majorを実質検出したReviewer: **0 / 17**
- Major修正: 14構成
- exact Head CI: **14 / 14 SUCCESS**
- 3-Judge最終裁定でmerge-ready: **1 / 14**
- 最終production: Agent B APPROVE、Blocker / Major / Minor / Nit = 0 / 0 / 0 / 0

最終修正Benchmarkの1位は **GPT-5.6 Sol / Codex — 94/100** でした。2位はClaude Opus 5 / Claude Code 80、3位はGPT-5.6 Luna / Codex 77です。

これは、このIssue、このHarness、このEffort、この1回の実行結果です。モデル一般の性能順位ではありません。

全14候補の順位、中間Stageのランキング、PR、Head SHA、CI、Judge内訳は [Benchmarks](https://kooiei-in4a.github.io/amane-ai-lab/benchmarks/) に分けています。

## FND-03で作ったもの

FND-03の目的は、実PostgreSQL 18を使うintegration test基盤です。

単にcontainerを起動してqueryが通れば完了、というIssueではありません。

後続Issueではrow lock、advisory lock、constraint、trigger、migrationなどPostgreSQL固有の挙動を検証します。その土台になるため、test基盤側で次を保証する必要があります。

- test同士が状態を共有しない
- database lifecycleを自動管理する
- 並列実行しても壊れない
- cleanup失敗を握り潰さない
- startup / connection failureを明確なtest failureにする
- CIでも同じ実PostgreSQL testを動かす
- InMemory / SQLiteへfallbackしない

初期実装比較では、database isolation、parallel safety、cleanup failure handlingで差が付きました。

## 14候補を比較し、Final Synthesisを作った

初期BenchmarkではGPT-5.6 Sol / Codexが96/100で1位でした。

ただし、最終成果物は1位候補をそのまま採用していません。複数候補の良い設計とfailure testを選んでFinal Synthesisを作りました。

当時の評価は98/100。CIもSUCCESS。cleanup retry、startup failure、connection failure、parallel executionまでかなり厚く検証していました。

ここだけを見ると、十分にmergeできそうです。

実際、この評価は後から **SUPERSEDED** になりました。

## 17の独立レビューは、blocking Majorを見つけられなかった

Final Synthesisへ、同じ条件で17のModel + Harnessを独立レビューとして投入しました。

completedしたReviewerはすべてAPPROVE。レビュー品質には差がありましたが、後からtechnical Goldになったblocking root causeを実質検出したReviewerは0件でした。

問題はTestcontainers .NET 4.13.0のdispose semanticsにありました。

概略すると、cleanup時にDocker resourceの削除が失敗しても、Testcontainers内部では先にdisposed stateが固定される経路があります。そのfailed instanceへもう一度 `DisposeAsync()` しても、2回目はno-op成功になり得ます。

Final Synthesisは「同じinstanceでcleanupをretryできる」ことを自分のtestで確認していました。しかし、そのtestが再現していたfailureと、Testcontainers内部の本当のfailure pathは同じではありませんでした。

つまり、**テストはあった。failure injectionもあった。それでも、依存libraryのstate machineを誤解していた。**

## Green CIは、この問題を反証できない

このMajorが厄介なのは、通常のCIではほぼ見えない点です。

正常系ではcontainerは消えます。databaseも消えます。testも全部通ります。

必要なのは、Docker resource削除の途中だけが失敗し、その後同じTestcontainers instanceをretryするような狭いfailure pathです。

そのためFND-03では、次の区別がはっきりしました。

**CI SUCCESSは「実行したtestが通った」証拠です。実行していないfailure pathまで正しい証拠ではありません。**

これは当たり前に見えますが、14候補すべてCI SUCCESSだった最終修正ラウンドでも、同じことがもう一度起きました。

## Majorを教えてから14構成に直させた

次の実験では、見つかったcleanup Majorを明示し、14のModel + Harnessへ同一Baseから独立修正させました。

今度は問題を知っています。

しかも14件すべてexact Head CI SUCCESSでした。

それでも3 Judgeで実コードとTestcontainers 4.13.0の一次sourceを突き合わせると、merge-readyは1件だけでした。

理由は、元のMajorを直そうとしたことで、さらに深いownership問題が見えたためです。

## IDを取得する前に失敗したら、誰がcontainerを回収するのか

最終裁定で特に効いたのがpartial-create pathです。

Docker側ではcontainer creationに成功した。しかしTestcontainersがそのIDを自分の内部stateへ保存する前に失敗した。

この瞬間には、

- Docker上にはcontainerが存在する
- application側からcandidate IDを取得できない
- Testcontainersのnative Disposeを信用できない

という状態が起こり得ます。

多くの修正案は、container IDやTestcontainers instanceをcleanup ownershipの根拠にしていました。そのためIDを失うと、実resourceが残っていてもauthoritativeなownerを失います。

1位のGPT-5.6 Sol / Codex案は、containerをcreateする前にunique ownership labelを決めました。

そしてnative Disposeの成否だけに依存せず、labelでDocker resourceを検索し、removeし、もう一度検索して消えたことを確認します。

重要なのは「retryを増やした」ことではありません。

**壊れ得るlibrary objectとは別に、resource ownershipを識別できる手段を持ったこと**です。

## 多数決ではなく、一次証拠でJudgeを裁定した

Major修正Benchmarkでは3つのJudgeを使いました。

Judge同士の評価も一致していません。

あるJudgeが高く評価した候補を、別Judgeはmerge不可としました。そこでraw scoreの平均を最終結果にはしていません。

Testcontainers 4.13.0のsource、candidate exact Head、failure test、CIを戻って確認し、Findingごとに成立するかを裁定してから最終順位を決めました。

これはAIを増やすときに重要だと思っています。

AI Reviewerを3つ使うことと、3票で多数決することは同じではありません。

**異なるReviewerから異なる仮説を集め、最後は一次証拠へ戻る。**

FND-03ではこの方法が必要でした。

## Review Benchmarkには方法論上の注意がある

17-model review benchmarkについては、結果の扱いに注意が必要です。

最終的なGold Majorは、全Reviewerの回答を集める前に完全固定されていたものではありません。

最初のReferenceを固定した後、追加でTestcontainers 4.13.0の一次sourceを調べてMajorを明確化しました。そのためarchiveでは `post_hoc_adjudication: true` としています。

つまり、「17モデルにblind testをして全員不合格だった」という表現はしません。

正確には、**17件のraw reviewを保存した後、追加一次調査で確定したblocking Goldに照らすと、17件ともそのroot causeを検出していなかった**、です。

失敗結果を強く見せるために実験条件を単純化しないことも、このLabでは重要だと考えています。

## 実装能力、レビュー能力、修正能力は分けて見た方がいい

FND-03全体を見ると、少なくとも3つの能力を分けた方がよさそうです。

1. 未知のIssueを実装する能力
2. 一見完成した実装から未知の欠陥を見つける能力
3. root causeを提示された後にfailure spaceを閉じる能力

同じモデルが全部で同じ順位になるとは限りません。

初期実装で高得点でもReviewerとしてMajorを見つけられるとは限らず、Majorを理解しても完全なfixを作れるとは限りません。

「コーディング性能」という1つの数字へまとめると、この差は見えなくなります。

## 実務なら14候補も17Reviewerも使わない

この規模はBenchmarkだから行っています。

普段の開発なら、ここまで増やす必要はありません。

私なら重要な基盤Issueでは、

- 1〜3の独立実装
- 別Model / Harnessによる独立レビュー
- failure pathを意識したtest
- 依存libraryの挙動が重要なら一次source確認
- 最後はIssueと実コードへ戻ってmerge判断

くらいに縮めます。

特に、cleanup、transaction、lock、retry、cancellationのような**失敗時のstate transitionが品質を決めるコード**では、正常系CIの緑だけで判断しない方がいいです。

## 今回の最終production

最終production implementationでは、1位PR #108のownership architectureを軸に、別候補のactual Testcontainers latch / second-no-op testと、元Baseにあったunreachable-Docker regressionを統合しました。

Final Headに対するAgent B独立レビューはAPPROVE、Blocker / Major / Minor / Nitはすべて0。pre-merge、post-merge CIもSUCCESSし、Issue #41をcloseしています。

ここでも「Benchmark 1位をそのままproductionへ入れた」わけではありません。

候補比較は意思決定材料であって、production outcomeは別の成果物として残しています。

## 最後に残った教訓

FND-03で一番印象に残ったのは、AIが間違えたことではありません。

**かなり強い実装、かなり厚いtest、複数のAI Reviewer、green CIが揃っていても、全員が同じ前提を見誤ることがある**という点です。

AIを増やすほど安全になるとは限りません。同じ証拠、同じ抽象化、同じlibrary理解に依存していれば、見逃しも共有します。

だから最後に必要なのは、多数決よりも、

- 何を証明したtestなのか
- failure時に誰がresourceを所有するのか
- 依存libraryは本当にそのsemanticsなのか
- CI greenが何を証明していないのか

を一次証拠へ戻って確認する工程でした。

FND-03は、モデル比較というより、**AIエージェントを使った開発で「何を信用するか」を試した実験**になりました。
