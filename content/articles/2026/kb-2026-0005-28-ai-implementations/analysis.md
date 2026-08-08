# 28回AIに実装させ、28回CIが通った。それでも「良い実装」は同じではなかった

## まず結果

今回の実験は2ラウンドです。

- FND-01: 14候補
- FND-02: 14候補
- 合計: 28候補
- archiveに記録されたcandidate CI: 28件すべてSUCCESS

ここだけ見ると、「どのAIでも十分だった」で終わりそうです。

実際には逆でした。

**CIが緑になったところから、比較が始まりました。**

buildとtestが通ることは重要です。ただ、それだけでは「Issueを正しく実装した」「余計なことをしていない」「本番と同じ経路を検証した」とまでは言えません。

## この試行でのランキング

順位は隠さず出します。ただし、これはこのIssue、このHarness、このEffort、この1回の実行結果です。

### FND-02 実装 — Coding Score

| 順位 | Model | Harness | Score |
|---:|---|---|---:|
| 1 | **GPT-5.6 Sol** | **Codex** | **96** |
| 2 | **GPT-5.6 Terra** | **Codex** | **95** |
| 3 | **GPT-5.6 Luna** | **Codex** | **94** |
| 4 | Grok 4.5 | Cursor | 92 |
| 5 | GPT-5.6 Luna | Open Code | 84 |

実務速度を10%加味したPractical Scoreでは、1位 Terra / Codex、2位 Sol / Codex、3位 Grok / Cursorでした。

### FND-02 独立レビュー

同じFinal Synthesisへ17モデルで独立レビューを掛けた結果です。

| 順位 | Model | Harness | Score |
|---:|---|---|---:|
| 1 | **GPT-5.6 Sol xHigh** | **Codex** | **100.0** |
| 2 | **Claude Opus 5 xhigh** | **Claude Code** | **92.5** |
| 3 | **GPT-5.6 Luna** | **Open Code** | **88.0** |
| 4 | ChatGPT Opus 5.6 Sol xhigh | Browser | 87.5 |
| 5 | GPT-5.6 Luna xHigh | Codex | 82.0 |

全候補、処理時間、PR、CI、評価全文は [Benchmarks](https://kooiei-in4a.github.io/amane-ai-lab/benchmarks/) に分けて載せています。

FND-01は候補別の正式Coding Score表がarchiveに残っていません。PR、CI、処理時間は残っているので生データは公開しますが、後から都合よく順位は作っていません。

## 2つの課題は意図的に性質が違う

FND-01とFND-02は、同じFoundationの連続Issueですが、評価の難しさが違います。

| | FND-01 | FND-02 |
|---|---|---|
| 主題 | Solution / project / build-test CI | API request共通のruntime contract |
| 主な成果物 | project境界、reference、compiler設定、CI | error、correlation、time、technical log |
| 重要な確認 | 必要な基盤だけを作ったか | 実際のHTTP / logging出力まで成立するか |
| 典型的な危険 | 後続Issueの先取り、過剰scaffold | testだけ成立しproduction wiringが未証明 |

FND-01では、**作りすぎないこと**が品質です。

FND-02では、**どこを通して確認したか**が品質になります。

同じ「CI SUCCESS」でも、見なければならない中身が違います。

## 14のModel + Agent/Harnessを同じIssueへ投入した

2ラウンドとも、Open Code、Codex、Cursor、Claude Codeを含む14構成を使いました。

モデルにはDeepSeek、Qwen、GPT-5.6 Luna / Terra / Sol、Grok、Composer、Claude Sonnet / Opus、MiMo、MiniMaxが含まれます。

ここで `Model + Agent/Harness` と書いているのは、モデルだけで結果が決まらないからです。

- repositoryをどう探索するか
- どのファイルを読むか
- shellやGitをどう使うか
- build/testをどこまで回すか
- failure時にretryするか
- diffを最後に見直すか
- contextをどこまで保持できるか

こうした部分はAgent/Harness側の影響を受けます。

実験にはGPT-5.6 LunaをOpen CodeとCodexの両方で実行した候補もあります。同じモデル名でも実行環境が違うため、結果をそのまま「Lunaの能力」とは呼べません。

Effort設定もMax、Xhigh、high、Thinking、未指定が混在しています。各候補1試行です。完全統制されたモデル性能試験ではありません。

その代わり、**実際の開発環境で何が出てくるかを見る実験**として扱っています。

## FND-01で見たのは「必要な分だけ作れるか」

FND-01のClose conditionは、.NET 10 modular monolithのproject境界を作り、localとCIでrestore / build / testが成功することでした。

Out of scopeもかなり明確でした。

- HTTP error contract
- correlation ID
- `TimeProvider`
- logging
- PostgreSQL
- Testcontainers
- EF Core
- Docker Compose
- health endpoint
- Identity
- business code

AIに基盤を作らせると、「将来必要そうだから」という理由で先回りしたくなる余地があります。

しかし、このIssueでは先回りは加点ではありません。

後続Issueが所有する責任を勝手に持ち込めば、いまは動いても、次のIssueで責任境界が崩れます。

そのため共通Coding Scoreでは、Issue達成度だけでなくScope遵守15点、変更精度・最小性10点を独立して持たせました。

**コード量が多いほど高性能、という評価をしないためです。**

FND-01の14候補はすべてCI SUCCESSでした。その後、候補を比較してFinal integrated implementationを作り、99/100で独立レビューを通し、PR #62としてmergeしました。

候補別の正式Coding Score表はarchiveされていません。これは記録上の欠落なので、今後同じ実験をするときはランキング表そのものも正本として残すようにします。

## FND-02では「テストがある」だけでは足りなくなった

FND-02は一段難しくなります。

対象はerror envelope、correlation ID、`TimeProvider`、JSON console technical logging、secret非露出です。

例えばmiddlewareを直接呼び出すunit testを書けば、そのmiddleware単体の挙動は確認できます。

でも、それで次まで証明できるでしょうか。

- productionのDIへ本当に登録されているか
- middleware順序が正しいか
- ASP.NET Coreのserializerを通した最終JSONが正しいか
- 実際のlogging providerが期待したJSONを出すか
- request / response / logで同じcorrelation IDを追えるか

ここは別問題です。

FND-02の比較から、共通benchmark方法論には「検証証拠の忠実度」という考え方を追加しました。

ざっくり言えば、証拠の強さは次のように違います。

1. production entry point / production pipelineを通したrequest-level test
2. test側でproduction componentを組み直したhost
3. middlewareやserviceを直接呼ぶtest

下のtestが悪いわけではありません。確認できる範囲が違います。

特にsecurity、logging、serializationのように**最終的に外へ出るもの**を確認するときは、本番に近い経路を通さないと証拠が弱くなります。

## Final synthesisも、そのままではmergeしなかった

FND-02でも14候補のCIはすべてSUCCESSでした。

比較後、良い部分を選んでFinal synthesisを作りました。ただし、それをそのままmergeはしていません。

独立レビューで残ったMajor 1件とMinor 1件に対応し、最終PR #83では次まで詰めました。

- generic 500を `internal_error` に固定
- application pipeline内の404 / 405 / 415を共通error envelopeへ統一
- request abortと内部cancellationを区別
- response開始後に例外が起きた場合、正常な200として終わらせずabort
- 実Kestrelでrequestを通す
- 実JSON console outputでpositive controlとsecret非露出を確認

最終的にUnitTests 3件、IntegrationTests 27件がPASSし、warning 0、CI PASS。Agent B再レビューではBlocker / Major / Minor / Nitがすべて0になりました。

この流れは、今回の実験でかなり大事な部分です。

**14候補を比較したから正しいのではなく、統合版ももう一度疑う。**

多数決でもありません。

「多くのAIが同じ実装をしたから採用する」ではなく、Issueと仕様に戻って、最終成果物を独立して確認します。

## 順位は出す。ただし、そのまま一般化しない

ランキングは分かりやすいし、実際に役に立ちます。

今回なら、FND-02実装ではCodex上のGPT-5.6 Sol / Terra / Lunaが上位3つでした。独立レビューではGPT-5.6 Sol / Codexが1位、Claude Opus 5 / Claude Codeが2位でした。

ここから「GPTは常にClaudeより強い」とは言いません。

この実験で言えるのは、**この課題、この設定、この実行環境ではこの順位になった**というところまでです。

順位を入口にしつつ、実務では次も見ます。

- Scopeを守ったか
- テストの証拠はどこまで強いか
- 不要な変更が多くないか
- 速度を含めると順位がどう変わるか
- 同じモデルでもHarnessを変えるとどうなるか

モデルは更新されます。価格も変わります。Harnessも変わります。

一方、**Issue、diff、test、CIを証拠にして評価する方法**は比較的長く使えます。

## 14候補を毎回作る必要はない

14候補×2ラウンドは、普段の開発方法としては多すぎます。

今回は比較実験なのでここまでやりました。

実務へ持ち込むなら、私は次のくらいに縮めます。

### 通常のIssue

1つの実装Agentで作る。

その後、別のModelまたは別Harnessで独立レビューする。

### 基盤・認証・データ整合性など重要なIssue

2〜3の異なるModel + Harnessへ独立実装させる。

差分を比較し、良い設計を選んで統合する。

最後は候補を作ったAgentとは別のReviewerで確認する。

### 評価したい新モデルが出たとき

既存の実Issueを使い、common baseと採点基準を固定して比較する。

公開ベンチマークの数字だけではなく、自分のrepositoryで何が起きるかを見る。

この程度なら、実験で得たやり方を日常の開発へ持ち込みやすいと思います。

## 今回の実験で残したいもの

モデル名だけでなく、次の流れも残したいと思っています。

```text
IssueとScopeを先に固定
        ↓
複数候補を独立実装
        ↓
Head / PR / CIをsnapshot
        ↓
実diffを同じ基準で比較
        ↓
必要ならFinal synthesis
        ↓
別Agentで独立レビュー
        ↓
merge
```

AIがコードを書く速度は上がっています。

その分、人間側では「何を作らせるか」「どの証拠なら信用するか」「どこで別の目を入れるか」の設計が重要になります。

今回の28実装は、その確認のための実験でした。

## この結果の限界

この結果を読むときには、少なくとも次を差し引く必要があります。

- 各候補1試行
- Effort設定が統一されていない
- Agent/Harnessが異なる
- 実行時間の条件も完全統制ではない
- FND-01の候補別Coding Score表は保存されていない
- 2つのIssueだけでモデル一般性能は決められない

したがって、「モデルAはモデルBより常に強い」という結論には使いません。

今回確認できたのは、**同じrepository、同じIssueでも、AI実装を評価するにはCI以外の証拠が必要になる**ということです。
