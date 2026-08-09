# はじめに

AIが書いたコードを、別のAIにレビューさせれば安全になるのか。

FND-03では、この問いをかなり厳しい形で試すことになりました。

対象は `minimal-bank-system` のIssue #41、実PostgreSQL 18を使うintegration test基盤です。TestcontainersでPostgreSQLを起動し、test isolation、parallel execution、cleanup、startup failure、CIまで含めて、後続Issueが安全に使える共通fixtureを作ります。

最初に14の `Model + Agent/Harness` へ同じIssueを独立実装させました。比較後、良い設計を統合したFinal Synthesisを作り、当時は98/100相当まで仕上がったと評価していました。

そのFinal Synthesisを17のAI構成へ独立レビューさせます。

結果は、completedしたReviewerがすべてAPPROVEでした。

ところが、その後Testcontainers 4.13.0の一次sourceまで追うと、container cleanupのfailure pathにmerge-blocking Majorが残っていました。

そこで今度は、そのMajorを14構成へ同一条件で修正させました。14件すべてexact Head CIはSUCCESSです。

それでも3つのJudgeで一次証拠を突き合わせると、merge-readyと判定できたのは1件だけでした。

この記事では、細かな候補別採点表を並べるのではなく、**なぜCI greenとAIレビューを重ねても不足したのか**、そして**複数AIを使うとき最後に何を信用すべきか**を整理します。

全候補、全順位、PR、Head SHA、CI、Judge内訳は [Benchmarks](https://kooiei-in4a.github.io/amane-ai-lab/benchmarks/) に分けて掲載します。
