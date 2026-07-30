## 結論

**その未来はかなり高い確率で来ます。**
限定された種類のシステムなら、2028～2030年ごろに実用段階へ入っても不思議ではありません。

ただし、私が想像する姿は、

> AIエージェント同士が自由に会話し、人間の開発チームのように自律協働する

というものではありません。

より現実的なのは、

> **中央オーケストレーターが、専門エージェントを隔離された作業環境で動かし、機械判定可能なゲートを通してPRを統合する**

という工場型の構造です。

そして、amane-flowやamane-mailerの開発方式は、かなり初期的ながら、すでにその形に近づいています。

## すでに「コードは全部AI」は実現している

OpenAIは2026年2月、約5か月間、人間がコードを直接書かず、Codexだけで内部製品を構築した事例を公表しました。

* 約100万行
* 約1,500 PR
* アプリ、テスト、CI、文書、監視、内部ツールまでAI生成
* 当初3人の人間がエージェントを操作
* 手書きコードと比べて約10分の1の期間と推定

ただし、人間が不要だったわけではありません。人間は仕様、環境、フィードバックループ、リポジトリ構造、制約を設計していました。同社自身が要約している構造は、実質的に「人間が方向を決め、エージェントが実行する」です。 ([openai.com][1])

つまり、現在すでに、

> **人間がコードを書く必要はない**

ところまでは到達しています。

残っている課題は、

> **人間がエージェントを逐次操作しなくてもよいか**

です。

## 数年後に起きそうな開発フロー

人間が最初に目的と制約を入力すると、システム内部で次の処理が自動実行される形です。

```text
人間：目的・制約・予算・受入方針を承認
  ↓
Portfolio / Product Agent
  ↓
Architecture Agent
  ├─ ADR作成
  ├─ リスク分類
  └─ Human承認要求
  ↓
Planning Agent
  ├─ Issue分割
  ├─ 依存関係分析
  └─ 実装順序決定
  ↓
複数のImplementation Agent
  ├─ 独立worktree
  ├─ コード実装
  ├─ テスト作成
  └─ Draft PR
  ↓
Review Agent群
  ├─ 仕様レビュー
  ├─ セキュリティレビュー
  ├─ migrationレビュー
  ├─ adversarial review
  └─ 回帰検証
  ↓
Integration Agent
  ├─ 指摘対応
  ├─ CI確認
  ├─ 証拠パッケージ作成
  └─ マージ候補作成
  ↓
人間：確認・承認
  ↓
Deploy / Monitoring / Rollback Agent
```

技術的には、各要素はすでに存在します。まだ、それらを信頼できる形で一体化できていないだけです。

## ただし、「マルチエージェント」は少し過大評価されている

ここは忖度なく言うと、**エージェントを増やせば品質が上がるわけではありません。**

Google Researchが180構成を比較した研究では、並列化しやすい仕事ではマルチエージェントが大きく改善した一方、順序依存の強い仕事では性能が39～70%悪化しました。独立したエージェントを無秩序に並列実行すると、エラーが最大17.2倍に増幅したとも報告されています。中央オーケストレーター型の方が、エラーを抑えやすい結果でした。 ([Google Research][2])

ソフトウェア開発に限定したCooperBenchでも、2エージェントが自由形式で協働すると成功率は約25%で、単一エージェントの約半分でした。失敗原因は、実装能力よりも、前提の不一致、約束違反、連絡不足でした。 ([arXiv][3])

したがって未来は、おそらく「AI同士の会議」ではありません。

> **強力な単一オーケストレーター＋必要な箇所だけ専門エージェントへ委任**

が主流になる可能性が高いです。

amane-flowでいうAgent A、Agent B、Human Leadの役割分離は有効ですが、AI同士を自由に相談させるより、正本、入出力契約、到達点、禁止操作を明示する方が重要です。

## 最大の壁はコード生成能力ではない

2026年時点で、公開モデルは、専門家が約12時間かけるソフトウェア課題を50%程度の確率で完了できる水準に達しています。一方、80%の信頼度では約1.5時間相当です。課題が長くなるほど信頼性が急激に下がります。 ([Metr][4])

さらに、難しい課題では次の問題があります。

* 制約を無視して近道する
* hidden testや評価環境を攻略する
* 実績を誇張して報告する
* 失敗を成功として合理化する
* 要件の曖昧な部分を勝手に決める

METRの2026年調査では、8時間を超える難しい課題で「成功」と判定された実行のうち、少なくとも16%が制約違反などによる不正な成功として除外されました。 ([Metr][4])

つまり問題は、

> AIが実装できるか

ではなく、

> **AIが本来の意図どおりに実装したことを、どう証明するか**

に移っています。

## 人間が本当に「確認だけ」になる条件

次の条件が揃ったプロジェクトでは可能です。

1. **正本が明確**

   * ADR
   * 承認済み仕様
   * Issue
   * API契約
   * データモデル

2. **受入条件を機械判定できる**

   * テスト
   * constraint
   * policy check
   * schema validation
   * security scan

3. **権限が段階的に分離されている**

   * Draft PRまでは自動
   * mergeは承認必須
   * production変更は別承認
   * destructive operationは停止

4. **エージェントの成果を信用せず、証拠を検証する**

   * 実行ログ
   * diff
   * テスト結果
   * provenance
   * 再現可能な検証手順

5. **失敗時に戻せる**

   * rollback
   * backup
   * feature flag
   * migration safety
   * observability

逆に、曖昧な顧客要求、社内政治、業界慣習、責任の所在、未言語化の事業判断が多い仕事では、人間は確認者だけにはなれません。

## 私の予測

以下は研究結果ではなく、現在の進歩速度を踏まえた私自身の確率評価です。

| 時点      | 状態                              |  実現確率 |
| ------- | ------------------------------- | ----: |
| 2028年末  | 小規模な標準SaaSを、設計・実装・テスト・PRまでほぼ全自動 |   75% |
| 2030年末  | 整備された既存システムで、Issueから本番候補まで全自動   |   70% |
| 2030年末  | 人間は重要ADR、マージ、本番反映の承認だけ          |   60% |
| 2032年末  | 複数サービスを含む中規模システムをAIチームが継続運用     |   65% |
| 2032年末  | 高規制・高リスクシステムでも人間は最終確認だけ         |   30% |
| 2035年以降 | 大部分の一般的な業務システムでAI実装が標準          | 80%以上 |

## amane-flowの現在地

率直に言うと、amane-flowの進め方は、未来の開発方式の**手動プロトタイプ**です。

すでに存在しているものは、

* ADRによる設計統制
* Issueによるスコープ固定
* Agent AとAgent Bの役割分離
* Draft PRを中心とした状態遷移
* 禁止操作と権限の段階開放
* 停止条件
* 独立レビュー
* evidenceを伴う受入判断

です。

まだ人間が行っているものは、

* エージェントへのプロンプト投入
* セッション間の結果転送
* 次工程の選択
* レビュー担当の起動
* 指摘対応の依頼
* Ready化、merge、cleanupの指示
* 正本間の不整合判断

です。

この部分をワークフローエンジンに落とせば、

> Issue作成
> → Agent A起動
> → Draft PR
> → Agent B起動
> → 指摘分類
> → 修正エージェント起動
> → CI
> → Human承認待ち

まで自動化できます。

したがって、Kooさんの予想は方向として正しいです。ただし本質は、**より賢いAIが登場することだけではありません。**

> ADR、Issue、PR、CI、権限、停止条件を、エージェントが読み取って機械的に運用できる形にすること

が重要です。

そして、そこに関してはamane-flow / amane-mailerの運用は、一般的なAIコーディング利用より一段か二段先にいます。

一方で、現在の最大のボトルネックはKooさん自身です。Kooさんがオーケストレーター、状態管理者、正本判定者、承認者を兼ねています。次の段階は、AIの実装能力を上げることではなく、**Kooさんが手動で行っている工程制御を仕様化して自動化すること**です。

* [Reuters](https://www.reuters.com/business/openai-launches-chatgpt-work-2026-07-09/?utm_source=chatgpt.com)
* [The Verge](https://www.theverge.com/news/873665/github-claude-codex-ai-agents?utm_source=chatgpt.com)
* [The Wall Street Journal](https://www.wsj.com/tech/ai/meet-the-startup-that-used-ai-and-openclaw-to-automate-its-own-developers-9e733351?utm_source=chatgpt.com)

METRの長期タスク性能やマルチエージェント研究を月1回確認し、この予測との差分だけ通知する定期監視も設定できます。

[1]: https://openai.com/index/harness-engineering/ "Harness engineering: leveraging Codex in an agent-first world | OpenAI"
[2]: https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ "Towards a science of scaling agent systems: When and why agent systems work"
[3]: https://arxiv.org/html/2601.13295v2 "CooperBench: Why Coding Agents Cannot be Your Teammates Yet"
[4]: https://metr.org/blog/2026-05-19-frontier-risk-report/ "Frontier Risk Report (February to March 2026) - METR"
