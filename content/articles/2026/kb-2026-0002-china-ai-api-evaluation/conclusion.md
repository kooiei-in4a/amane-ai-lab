# 統合結論

## 中心的な問いへの回答

提供された3つのAI調査だけから、単一の「最優秀中国製AIモデル」を確定することはできません。

DeepSeek、Qwen、GLM、Kimiなどの系列は共通して有力候補に挙がりましたが、正確なモデルID、価格、最大出力、日本からの契約条件、データ保持条件に重大な不一致が残っています。そのため、この記事で採用する結論は次の通りです。

> **モデルランキングをそのまま採用せず、役割別の候補群を作り、正確なモデルID・Provider・データ条件を固定した実API試験で採否を決める。**

## 資料の読み分け

この記事には、根拠の異なる結論が3層あります。後ろの追記は前の調査回答を書き換えた正本ではなく、公開後の追加確認です。

| 層 | 根拠 | 範囲 | 確信度の目安 |
| --- | --- | --- | --- |
| 3調査の統合結論 | ChatGPT／Gemini回答の比較 | 中国製候補の評価方法と系列候補 | 方法は高、具体モデルID・料金は低 |
| 個人開発向け追記（2026-08-01） | DeepSeek／GLM／Kimiの一次情報 | 中国製現行モデルの価格・接続・個人開発向け使い分け | 中 |
| コーディング再比較（2026-08-01） | 公表ベンチマークとAPI従量単価 | Coding Agent用途。GPT-5.6／Claude Opus 5も含む | 公表値は中～高、実API成功率は未検証 |

読み方の原則:

1. 法人導入・機密コード・契約可否は、最初の統合結論と検証計画を優先する
2. 中国製APIを個人開発で安く試し始めるなら、個人開発向け追記の価格・接続整理を使う
3. Issue実装や長時間Coding Agentの段階ルーティングは、コーディング再比較を優先する
4. 個人開発向け追記の「難しい実装はV4 Proへ上げる」は、Coding Agent用途では再比較で見直し済みである

## 採用する暫定候補

現時点では、次の役割分担で検証へ進むのが妥当です。

1. **主力・価格性能:** DeepSeekの現行高性能系列
2. **日本語・法人運用:** Qwenの現行国際向け汎用系列
3. **長時間エージェント:** GLMの現行エージェント向け系列
4. **低価格バッチ:** DeepSeekの現行低価格・高速系列
5. **高難度比較:** Kimiの現行フロンティア系列
6. **追加比較:** MiniMaxの現行長文・マルチモーダル系列

資料内の具体的なモデル名は候補探索に使いますが、採用前に公式の現行モデル一覧で再確認します。

### 2026-08-01追記での具体化

| 元の役割 | 追記での具体化 | 残る未確認 |
| --- | --- | --- |
| 主力・価格性能（DeepSeek） | Flash-0731を低価格標準に具体化。Coding Agent標準としてのProは再比較で保留 | 日本カード、実API成功率 |
| 日本語・法人運用（Qwen） | 追記未実施 | 現行国際向けモデルID、リージョン、契約 |
| 長時間エージェント（GLM） | GLM-5.2／Coding Planへ具体化 | Coding Plan新クレジット実効量、529等の運用品質 |
| 低価格バッチ（DeepSeek低価格） | V4 Flash-0731 | ピーク料金適用開始日 |
| 高難度比較（Kimi） | K3はスポット、K2.7 Codeは代替レビュー枠 | 日本カード、ハーネス差を除いた同条件比較 |
| 追加比較（MiniMax） | 追記未実施 | 現行モデルIDと用途適性 |
| （再比較で追加）横断Coding比較 | GPT-5.6 Luna／Terra／Sol、Claude Opus 5 | 月額プラン枠を除いた実運用コスト、実リポジトリ試験 |

## 推奨する導入手順

### 1. 公式情報を固定する

候補ごとに、モデルID、料金、最大出力、リージョン、契約条件、保存・学習・キャッシュ、DPA、ZDR、SLA、廃止予定を確認します。

### 2. 第三者APIで横比較する

PoCでは、同じインターフェースと同じテスト課題で比較します。第三者APIは比較の摩擦を減らしますが、安全性や本番適性を自動的に保証するものではありません。

OpenRouterなどは系列横断の初期比較に便利です。一方、候補が少数に絞れ、公式APIが使える場合は、個人開発向け追記・再比較のように公式経路を優先してよいです。本番は常に採用経路で再試験します。

### 3. 採用経路で再試験する

上位候補は、公式APIまたは本番で固定するProviderを使って再試験します。速度、上限、Tool Calling、障害率、データ経路が変わる可能性があります。

### 4. セキュリティ・法務ゲートを通す

機密コードや顧客情報を扱う場合は、送信禁止情報、マスキング、Provider固定、保存期間、契約文書、越境移転、障害通知を人間が承認します。

### 5. 役割別に採用する

1モデルですべてを処理するのではなく、主力、低価格補助、高難度レビュー、フォールバックに分けます。

## この結論を採用する理由

- 3回答の共通部分を利用できる
- 矛盾を都合よく解消せず、未確認事項として残せる
- モデル名が更新されても評価方法を再利用できる
- 性能だけでなく、契約、運用、セキュリティを判断へ含められる
- 実際のbuild/test、Tool Calling、費用、人間修正量で比較できる

## 採用しなかった考え方

### 1. 総合点1位をそのまま採用する

採点対象のモデル世代やProviderが揃っておらず、点数の前提が異なるため採用しません。

### 2. 3回答の多数決で事実を決める

複数AIが同じ誤情報を参照する可能性があります。一致は調査優先度を上げますが、一次情報の代わりにはなりません。

### 3. 第三者APIを常に最安全とみなす

比較には便利ですが、Routerと実推論ホストの両方を評価する必要があります。自動ルーティングで送信先が変わることもあります。

### 4. オープンウェイトなら安全とみなす

自社管理環境で運用すればデータ境界を管理しやすくなりますが、GPU、運用、脆弱性対応、モデル更新、ライセンス確認の負担があります。

## 確信度

- **評価方法と導入手順:** 高
- **候補系列の選定:** 中
- **追記で触れた中国製現行モデルの公開価格・モデルID:** 中～高（時点依存）
- **Coding Agentの最終順位:** 低～中（公表ベンチ依存、実API未検証）
- **資料内の具体的な価格・上限・契約条件（調査時点の主張含む）:** 低から中
- **単一モデルの最終順位（法人・機密含む）:** 低

## 適用条件

この結論は、日本からAPIを契約し、コーディング支援、AIエージェント、業務システムへ組み込む用途を想定しています。中国国内だけで完結するサービス、画像・動画専用モデル、特定産業の専用契約は別評価が必要です。

## 残余リスク

- 調査直後にモデルや価格が更新される
- 公開仕様と実APIの挙動が異なる
- カード承認やKYCが利用者ごとに異なる
- Providerの自動切替でデータ送信先が変わる
- 長いコンテキストが実際の理解精度へ結びつかない
- 生成コードに不具合やライセンス問題が残る
- 契約文書が機密コードの送信を許可しない
- モデル廃止で再現性が失われる

## 次に取るべき行動

一部は2026-08-01追記で進みましたが、採用確定に必要な検証は残っています。

追記で一部進んだこと:

- 名前を挙げた中国製モデルの公開価格・モデルIDの一次確認
- Coding Agent向けの暫定ルーティング案（公表ベンチとAPI単価ベース）

いまも必要なこと:

1. 同一の10課題を実APIで最低3回ずつ実行する
2. 日本カード／KYCを実際の契約画面で確認する
3. Qwen／MiniMaxの現行モデルIDを一次情報で固定する
4. 機密区分とセキュリティ・法務ゲートを決める
5. 上位候補を採用予定Providerで再試験する
6. build/test、成功率、費用、APIエラー、人間修正量を記録する
7. 主力、補助、レビュー、フォールバックの役割を決定する

## 個人開発者向け追記（2026-08-01）

この追記は、公開後に個人開発用途へ絞って現行モデルの一次情報を再確認した派生結論です。元の3調査だけで正式モデルIDや料金を確定したものではありません。価格・上限・契約条件は時点依存のため、採用前に公式ページで再確認してください。

この節の「難しい実装はDeepSeek V4 Proへ上げる」構成は、直後の「コーディング性能・API費用の再比較」で **Coding Agent用途に限り見直し** されています。価格・接続の一次情報としては有効ですが、Issue実装や長時間Agentの標準昇格先は再比較節を優先してください。

調査基準日：2026年8月1日

対象：

- DeepSeek V4 Flash
- DeepSeek V4 Pro
- GLM-5.2
- Kimi K2.7 Code
- Kimi K3

### 使い分けの結論

個人開発では、次の使い分けが最も合理的です。

1. **日常開発の標準：DeepSeek V4 Flash**
2. **難しい実装・設計判断：DeepSeek V4 Pro**
3. **毎日エージェントを大量に使う場合：GLM-5.2 Coding Plan**
4. **コード特化モデルの比較・代替：Kimi K2.7 Code**
5. **非常に難しい課題だけ：Kimi K3**

特に有力なのは、**Flashを通常モデル、Proを上位モデルとして切り替える構成**です。両方とも同じDeepSeek APIキーとエンドポイントで利用でき、Claude Codeなどではモデル役割に応じた振り分けもできます。価格差も小さく、個人開発では最も費用を抑えやすい構成です。出典: [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

### 実用比較

| モデル | 個人開発での役割 | 入力／出力価格 | Context | 開発ツール接続 | 個人開発評価 |
| --- | --- | ---: | ---: | --- | --- |
| **DeepSeek V4 Flash** | 日常実装、テスト、レビュー、補助Agent | $0.14／$0.28 | 1M | OpenAI・Anthropic互換 | **A+** |
| **DeepSeek V4 Pro** | 難しいIssue、設計、複数ファイル変更 | $0.435／$0.87 | 1M | OpenAI・Anthropic互換 | **A+** |
| **GLM-5.2** | 長時間Agent、定額で大量利用 | $1.40／$4.40 | 1M | Claude Code、Cline、OpenCode | **A～B** |
| **Kimi K2.7 Code** | コード修正、長時間Coding Agent | $0.95／$4.00 | 256K | OpenAI互換、Claude Code等 | **A-** |
| **Kimi K3** | 大規模リポジトリ、高難度タスク | $3.00／$15.00 | 1M | OpenAI互換、Codex等 | **B** |

価格はキャッシュミス入力と通常出力の100万トークン単価です。DeepSeekはキャッシュ入力が極端に安く、Flashは$0.0028、Proは$0.003625です。Kimi K3はキャッシュ入力$0.30、K2.7 Codeは$0.19です。出典: [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

### 実際の費用感

次の仮定で1タスク当たりの費用を計算します。

- 小規模：入力10万、出力1万トークン
- 中規模：入力100万、出力10万トークン
- 大規模：入力500万、出力50万トークン
- キャッシュなし
- Tool Callingや検索の追加料金を除外

| モデル | 小規模 | 中規模 | 大規模 |
| --- | ---: | ---: | ---: |
| DeepSeek V4 Flash | **$0.017** | **$0.17** | **$0.84** |
| DeepSeek V4 Pro | **$0.052** | **$0.52** | **$2.61** |
| GLM-5.2 | $0.18 | $1.84 | $9.20 |
| Kimi K2.7 Code | $0.14 | $1.35 | $6.75 |
| Kimi K3 | $0.45 | $4.50 | $22.50 |

エージェントが同じリポジトリ情報を繰り返し送信し、キャッシュが効けば実費は下がります。一方、Thinkingモデルが長い推論や大量の出力を生成すると、表より高くなる可能性があります。

この差を見る限り、個人開発でKimi K3を常用する理由は限定的です。大規模タスク1件で、DeepSeek V4 Proの約8.6倍になります。

### DeepSeek V4 Flash

**最初に試すべきモデルです。**

公式にはV4 Proに近い推論性能を持ち、単純なAgentタスクではProと同等、Proより高速・低価格とされています。2026年7月31日版のモデルバージョンは`DeepSeek-V4-Flash-0731`です。出典: [DeepSeek V4 Preview Release](https://api-docs.deepseek.com/news/news260424/)

向いている用途:

- 小規模～中規模の機能実装
- テスト生成
- コードレビュー
- ビルド・テスト失敗の調査
- ドキュメント更新
- サブエージェント
- リポジトリ探索
- 大量のIssue整理
- 低価格なセカンドレビュー

長所:

- 入力$0.14、出力$0.28という非常に低い価格
- 100万トークン
- 最大38.4万トークン出力
- Tool Calling対応
- JSON Output対応
- OpenAI API互換
- Anthropic API互換
- Responses API対応
- 同時実行上限2,500
- Thinking／Non-Thinkingを切替可能

出典: [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

弱点:

- 難しい設計判断ではProより精度が落ちる可能性がある
- 大規模変更で局所的に正しいが、全体方針を外す可能性がある
- 公式APIは今後、ピーク時間帯を通常価格の2倍にする予定
- 画像入力には対応していない

予定されているピーク時間は北京時間9～12時、14～18時です。日本時間では10～13時、15～19時になります。ただし2026年8月1日時点では、適用開始日は正式発表されていません。出典: [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

判定: **通常タスクの80%程度をFlashへ任せ、失敗したものだけProへ上げる運用が適切です。**

### DeepSeek V4 Pro

**価格性能比では最も有力な主力モデルです。**

公式にはAgentic Coding、数学、STEM、コード推論を中心とした上位モデルとして位置付けられています。1.6兆パラメータのMoEで、1トークン当たり490億パラメータを使用します。出典: [DeepSeek V4 Preview Release](https://api-docs.deepseek.com/news/news260424/)

向いている用途:

- GitHub Issueからの自動実装
- 複数ファイルにまたがる変更
- ADRや仕様に基づく実装
- 難しいバグ調査
- データベースMigration
- セキュリティレビュー
- 独立レビュー
- Flashが失敗したタスク
- 実装計画と影響分析

長所:

- 入力$0.435、出力$0.87
- 100万トークン
- 最大38.4万トークン出力
- Tool Calling、JSON Output対応
- OpenAI・Anthropic互換
- Claude Codeへ直接接続可能
- Flashと同じAPIキー、同じBase URL

Claude Codeでは、Opus系のモデル指定をV4 Pro、Sonnet／Haiku系をV4 Flashへ割り当てる公式設定例があります。サブエージェントだけFlashへ回す構成も可能です。出典: [Integrate with Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/)

弱点:

- Flashより遅い
- 2026年8月1日時点ではResponses API未対応
- Responses API対応は2026年8月上旬予定
- 公式APIの日本カード対応は公開情報だけでは断定できない
- 法人向けDPA、ZDR、SLAの情報が少ない

出典: [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

判定: **個人開発の主力モデルとして有力です。** ただし、最初から全タスクでProを使う必要はありません。

```text
探索・単純修正・テスト生成
        ↓
V4 Flash
        ↓ 失敗・不十分
V4 Pro
        ↓ それでも不十分
GLM-5.2 または Kimi K3
```

この段階昇格方式が、費用と品質のバランスに優れます。

### GLM-5.2

**API従量課金より、Coding Planを使う場合に価値があります。**

従量課金は入力$1.40、出力$4.40で、DeepSeek V4 Proよりかなり高額です。一方、GLM Coding Planは月額$18からで、GLM-5.2をClaude Code、Cline、OpenCodeなどから利用できます。出典: [Z.AI Pricing](https://docs.z.ai/guides/overview/pricing)

Coding Planの価格（2026年4月時点の公式標準価格）:

| Plan | 月額 | 公式が想定する利用 |
| --- | ---: | --- |
| Lite | $18 | 1プロジェクト |
| Pro | $72 | 1～2プロジェクト |
| Max | $160 | 2プロジェクト以上 |

出典: [Legacy Plan Migration Notice](https://docs.z.ai/devpack/transition)

ただし、2026年7月30日に新しいクレジット方式へ移行しています。新規契約者には新方式が適用されるため、購入画面の最終価格とクレジット量を確認する必要があります。出典: [Plan Update Announcement](https://docs.z.ai/devpack/notice/usage-revision)

向いている用途:

- Claude CodeやClineを毎日長時間使う
- 複数回のTool Calling
- 長時間の自律実装
- 大規模なリポジトリ解析
- 月額費用を固定したい
- Web検索、Web Reader、Vision MCPも使いたい

長所:

- 100万トークン
- 長時間Coding Agent向けに訓練
- コーディング規約、変更禁止事項、テスト要求への追従を重視
- Claude Code、Cline、OpenCodeを公式サポート
- Web Search、Web Reader、Vision MCPを定額枠内で利用可能
- PayPalまたはカードによる支払い経路がある

出典: [GLM-5.2](https://docs.z.ai/guides/llm/glm-5.2)

重要な制約（Coding Planは通常の汎用API定額枠ではない）:

- 公式サポート対象のCodingツールに限定
- 専用エンドポイントが必要
- 独自業務システムから自由に呼び出す用途には使用できない
- 枠を使い切っても従量課金残高へ自動移行しない
- 5時間枠と週間枠の両方がある
- 同時実行数はプランと混雑状況で動的に変わる

出典: [Z.AI FAQ](https://docs.z.ai/devpack/faq)

複数プロジェクトを並行してAI開発している個人開発者は、公式分類上はPro相当になりやすいです。しかし月額$72になると、DeepSeek V4 Proを相当量使っても到達しにくい金額です。

したがって、次の順で判断するのが適切です。

1. まずGLM-5.2を従量課金で数ドル試す
2. Claude CodeまたはClineで実案件を3～5件実施
3. 品質が明確に良ければLiteを1か月契約
4. Liteの同時実行や週間枠が不足した場合だけProを検討
5. 年払いは運用安定性を確認するまで避ける

最近の利用者投稿には、529エラー、レート制限、予想より速いクレジット消費を訴えるものがあります。あくまで個別事例ですが、最初から長期契約せず月払いで確認すべき理由になります。参考: [Reddit: GLM Coding plan dilemma](https://www.reddit.com/r/ZaiGLM/comments/1u6dmy4/glm_coding_plan_dilemma/)

判定:

- **毎日長時間使う：A**
- **月数回だけ使う：B**
- **独自APIプログラムへの組み込み：Coding Planでは不適**

### Kimi K2.7 Code

**コード専用モデルとしては有力ですが、DeepSeekより割高です。**

K2.7 Codeはコード生成、コード編集、長時間Agentに特化しています。256Kコンテキストで、Thinkingは常時有効です。出典: [Kimi K2.7 Code Quickstart](https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart)

向いている用途:

- 複数ファイル変更
- 既存コードの修正
- 長い仕様への追従
- リファクタリング
- バグ修正
- コーディングAgent
- 画像や動画を含むUI調査
- DeepSeekとは異なるモデルによる独立レビュー

長所:

- コード用途専用
- 長いコンテキストでの指示追従を強化
- 複数段階Tool Calling対応
- テキスト、画像、動画入力
- OpenAI API互換
- Claude Code、Cline等へ接続可能
- HighSpeed版は約180 tokens/s、短いコンテキストでは最大260 tokens/s

出典: [Kimi K2.7 Code Quickstart](https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart)

弱点:

- 入力$0.95、出力$4.00
- DeepSeek Proより入力約2.2倍、出力約4.6倍
- コンテキストは256Kで、DeepSeek／GLM／K3の4分の1
- Thinkingを無効化できない
- 単純な変更でも推論トークンを消費しやすい
- HighSpeed版はリソース不足による速度変動があると公式が明記

出典: [Kimi / Moonshot platform](https://platform.moonshot.ai/)

判定: **主力にするより、DeepSeekが苦手な課題を別のモデルで再検討する用途に向きます。** 特に独立レビューでは、DeepSeekで実装し、Kimi K2.7 Codeでレビューするなど、開発元の異なるモデルを組み合わせる価値があります。

### Kimi K3

**能力検証の価値は高いものの、日常利用には高価です。**

2.8兆パラメータ、1,040億アクティブパラメータ、100万トークン、画像入力に対応したフラッグシップモデルです。長時間Coding、大規模リポジトリ、ターミナル操作、視覚情報を伴う開発を主対象としています。出典: [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)

向いている用途:

- 非常に大きなコードベース
- 複数時間にわたるAgentタスク
- フロントエンドのスクリーンショット検証
- 高度な設計と実装を一括処理
- 他モデルが解決できなかった問題
- 最終レビュー
- 大規模な知識整理と実装の統合

長所:

- 100万トークン
- ネイティブ画像入力
- Tool Calling
- `tool_choice`
- 動的Tool Loading
- JSON Mode
- JSON Schema
- reasoning effortをlow／high／maxから選択可能
- OpenAI互換
- Claude Code、OpenCode、Codex等との統合情報あり

出典: [Kimi K3 Pricing](https://platform.moonshot.ai/docs/pricing/chat-k3)

弱点:

- 入力$3、出力$15
- 常に推論する
- デフォルトのreasoning effortが`max`
- 何も設定せず使うと費用が膨らみやすい
- 公開直後で、長期間の運用実績がない
- Web検索機能は更新中で、公式も当面の利用を推奨していない
- 個人環境でのセルフホストは現実的ではない

出典: [Kimi K3 Pricing](https://platform.moonshot.ai/docs/pricing/chat-k3)

契約・支払い: K3は最低$1をチャージすれば利用可能になります。Kimiの利用規約では、クレジットカードまたはデビットカードによる課金が想定されています。ただし、日本発行カードが必ず承認されるとは公式には明記されていません。出典: [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)

判定: **常用モデルではなく、スポット利用モデルです。**

利用時は原則として次の設定が適切です。

```text
通常の難しい課題：reasoning_effort = low
かなり難しい課題：reasoning_effort = high
失敗した最重要課題：reasoning_effort = max
```

最初から`max`を常用するのは費用面で推奨しません。

### 開発ツール別の適性

| ツール | DeepSeek V4 | GLM-5.2 | Kimi K2.7 | Kimi K3 |
| --- | --- | --- | --- | --- |
| Claude Code | **公式手順あり** | **公式対応** | 公式手順あり | 公式手順あり |
| Cline | 利用可能 | **公式対応** | **公式手順あり** | 公式手順あり |
| OpenCode | 公式統合あり | **公式対応** | 利用可能 | 公式統合あり |
| Codex CLI | 公式資料あり | 条件付き | 公式統合あり | 公式統合あり |
| Continue | OpenAI互換で利用可能 | OpenAI互換で利用可能 | OpenAI互換で利用可能 | OpenAI互換で利用可能 |
| Cursor内蔵Agent | 直接利用は不確実 | 直接利用は不確実 | 直接利用は不確実 | 直接利用は不確実 |
| 独自プログラム | **適する** | 従量APIなら適する | **適する** | 適するが高価 |

Cursorに無理に接続するより、これらのモデルについては**Claude Code、Cline、OpenCodeまたは独自のOpenAI互換クライアント**を使う方が確実です。

### OpenRouterを使うべきか

今回の4系列だけを試すなら、個人開発でも**最初は公式APIを推奨**します。

公式APIがよい理由:

- 最新モデルが最初に利用可能になる
- Prompt Cacheなどのモデル固有機能を使える
- Tool Callingの互換性が高い
- 推論Providerを意識しなくてよい
- 障害原因を切り分けやすい
- OpenRouterを経由する追加のデータ経路がない

OpenRouterがよい場合:

- DeepSeek公式で日本カードが通らない
- APIキーを1つにまとめたい
- 同じタスクを複数モデルで比較したい
- 利用上限を一括管理したい
- Provider障害時に自動切替したい

個人開発での推奨順:

```text
DeepSeek公式API
Kimi公式API
GLM Coding PlanまたはZ.ai従量API
        ↓
決済・接続に問題があるモデルだけOpenRouter
```

### 個人開発向け推奨構成

#### 構成A：最も推奨

```text
通常の探索・実装・テスト
    DeepSeek V4 Flash

難しい実装・設計・最終修正
    DeepSeek V4 Pro

別モデルによる独立レビュー
    Kimi K2.7 Code
```

かなり積極的に使っても、DeepSeek部分は数ドル～数十ドル程度に収まりやすい構成です。Kimiは必要な課題だけに限定します。

#### 構成B：定額で大量利用

```text
日常のCoding Agent
    GLM-5.2 Coding Plan

重要な最終レビュー
    DeepSeek V4 Pro
```

GLM Liteを1か月試し、同時実行や週間枠が不足した場合のみProを検討します。2プロジェクト並行だからといって、最初から月額$72を契約する必要はありません。

#### 構成C：高難度タスク対応

```text
通常
    DeepSeek V4 Flash

難しい
    DeepSeek V4 Pro

解決できない
    GLM-5.2

最終手段
    Kimi K3
```

### 最終順位

個人開発の総合順位（中国製モデルの価格・接続を中心にした整理）:

1. **DeepSeek V4 Pro／Flash**
2. **GLM-5.2**
3. **Kimi K2.7 Code**
4. **Kimi K3**

この順位は、中国製APIに絞った個人開発でのコスト・接続容易性の整理です。ベンダー横断のCoding Agentルーティングは、次節「コーディング性能・API費用の再比較」を優先します。

最初に試す順番:

1. DeepSeekへ少額チャージ
2. Flashで日常タスクを5件実施
3. 同じ難しいタスクをProで実施
4. Kimiへ$1チャージし、K2.7 CodeとK3を比較
5. GLM-5.2を従量課金で試す
6. GLMが継続的に有効ならCoding Plan Liteを1か月契約

最終判断: **中国製APIに限った個人開発のコスト、実装品質、接続容易性では、DeepSeek V4 Flash／Proの組み合わせが第一候補です。** Coding Agent用途での標準昇格先や横断比較は、次節の再比較を優先してください。

GLM-5.2は大量利用時の定額候補、Kimi K2.7 Codeはコード特化の代替モデル、Kimi K3は高難度課題のスポット利用と位置付けるのが適切です。

この4系列は更新が速いため、価格、モデルID、廃止予定を月1回確認する監視設定も有効です。

> 注意: この追記は個人開発向けの実務仮説です。法人導入、機密コード送信、日本カード承認、実API性能は、元記事の検証計画とセキュリティ・法務ゲートを通して確定してください。

## コーディング性能・API費用の再比較（2026-08-01）

調査・価格確認日：2026年8月1日

ここでは「Opus 5」を**Claude Opus 5**として扱います。費用はすべてAPIの従量課金で統一し、Cursor、Claude Code、Codex、ChatGPTなどの月額プランに含まれる利用枠は除外します。

この節は、直前の個人開発向け追記のうち、**Coding Agentとしての主力候補**をベンチマークとAPI単価で再評価したものです。直前追記ではDeepSeek V4 Proを難しい実装の主力候補としましたが、コーディングベンチマークまで確認すると、**現時点ではV4 Proより最新のV4 Flash-0731を優先して試すべき**です。DeepSeek自身が、7月31日版FlashのAgent性能はV4 Pro Previewを大幅に上回ると説明しています。現行Proはまだ更新されていません。出典: [DeepSeek API Updates](https://api-docs.deepseek.com/updates/)

### 再比較の結論

個人開発での現実的な選択は、次のようになります。

1. **低価格な日常開発：GPT-5.6 LunaまたはDeepSeek V4 Flash**
2. **性能と価格の総合バランス：GPT-5.6 Terra**
3. **中国製モデルの主力候補：GLM-5.2**
4. **難しいターミナル・長時間Agent：GPT-5.6 SolまたはKimi K3**
5. **実リポジトリの難しいバグ修正：Claude Opus 5**

### ベンチマークの見方

今回重視したのは次の指標です。

| ベンチマーク | 主に評価するもの | 個人開発での意味 |
| --- | --- | --- |
| SWE-bench Pro | 実在GitHub Issueの修正 | 既存プロジェクトのバグ修正能力 |
| DeepSWE v1.1 | 長時間・リポジトリ横断の修正 | 複数ファイル変更やIssue実装 |
| Terminal-Bench 2.1 | ターミナル、Git、ビルド、ツール操作 | Cline、Codex、Claude Code型Agent |
| FrontierSWE | 長時間のオープンな開発課題 | 高自律Agentとしての持続力 |
| ProgramBench | 仕様からプログラムを新規構築 | 新機能・小規模アプリの実装 |

HumanEvalやLiveCodeBenchは単体コード生成を見るには有効ですが、**Issueからの実装、複数ファイル変更、ビルド・テスト・修正**には、上記のAgent型ベンチマークの方が参考になります。

ただしスコアはモデルだけでなく、Codex、Claude Code、Kimi Code、DeepSeek Harnessなどの**実行ハーネス、推論強度、最大実行時間、再試行回数**にも左右されます。特にKimi K3とDeepSeek V4 Flashは自社ハーネス・最大推論設定での公表値なので、同じ数字でも完全な横比較ではありません。出典: [DeepSeek API Updates](https://api-docs.deepseek.com/updates/)

### 主要コーディングベンチマーク

| モデル | SWE-bench Pro | DeepSWE v1.1 | Terminal-Bench 2.1 | その他 | 証拠の確度 |
| --- | ---: | ---: | ---: | ---: | --- |
| **Claude Opus 5** | **79.2%** | 68.8% | 未確認 | Frontier-Bench 43.3% | 高 |
| **GPT-5.6 Sol** | 64.6% | **72.7%** | **88.8%** | Coding Agent Index 80.0 | 高 |
| **GPT-5.6 Terra** | 63.4% | 69.6% | 87.4% | Coding Agent Index 77.4 | 高 |
| **GPT-5.6 Luna** | 62.7% | 67.2% | 84.7% | Coding Agent Index 74.6 | 高 |
| **Kimi K3** | 未公表 | 67.5%※ | 88.3%※ | FrontierSWE 81.2、ProgramBench 77.8 | 中 |
| **GLM-5.2** | 62.1% | 条件差が大きい | 81.0～82.7% | FrontierSWE 74.4 | 中～高 |
| **DeepSeek V4 Flash-0731** | 未公表 | 54.4% | 82.7% | NL2Repo 54.2、Toolathlon 70.3 | 中～高 |
| **DeepSeek V4 Pro** | 現行同条件値なし | 現行同条件値なし | 現行同条件値なし | 旧Preview評価のみ | 低～中 |
| **Kimi K2.7 Code** | 未公表 | 未公表 | 未公表 | 正確な主要指標が不足 | 低～中 |

※Kimi K3はKimi Codeハーネス、最大推論設定によるMoonshot公表値です。公式DeepSWEリーダーボードのmini-SWE-agent構成では67.3です。

GPT-5.6系列は同じOpenAI公開表内で評価されているため、Sol、Terra、Lunaの比較は比較的信頼できます。TerraはSolより大幅に安い一方、主要コーディング指標の差は小さく、Lunaも低価格モデルとしては非常に高い水準です。出典: [OpenAI GPT-5.6](https://openai.com/index/gpt-5-6/)

Opus 5はSWE-bench Pro 79.2%で突出しています。一方、DeepSWEではSolの72.7%に対して68.8%です。これは、**明確な実リポジトリIssueの修正ではOpus、長時間のAgent作業やターミナル操作ではSol**という傾向を示します。出典: [Claude Opus 5 System Card](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/Claude%20Opus%205%20System%20Card.pdf)

Kimi K3はTerminal-Bench 2.1で88.3%とSolにかなり近く、FrontierSWEも81.2と強力です。ただしMoonshot自身も総合性能では最上位のクローズドモデルにまだ届かないと説明しており、現状は「中国製モデルの高性能候補」と評価するのが適切です。出典: [Kimi K3](https://www.kimi.com/blog/kimi-k3)

GLM-5.2はFrontierSWE 74.4で、長時間Agentとして有力です。Terminal-Benchの公表値にはハーネス差があり、81.0～82.7程度ですが、従量価格を考えると高い価格性能比です。出典: [GLM-5.2](https://z.ai/blog/glm-5.2)

### API単価比較

100万トークン当たり、通常速度・短文コンテキスト帯の価格です。

| モデル | 入力 | キャッシュ入力 | 出力 | Context |
| --- | ---: | ---: | ---: | ---: |
| **DeepSeek V4 Flash** | **$0.14** | **$0.0028** | **$0.28** | 1M |
| **GPT-5.6 Luna** | $0.20 | $0.02 | $1.20 | 約1.05M |
| **DeepSeek V4 Pro** | $0.435 | $0.003625 | $0.87 | 1M |
| **Kimi K2.7 Code** | $0.95 | $0.19 | $4.00 | 256K |
| **GLM-5.2** | $1.40 | $0.26 | $4.40 | 1M |
| **GPT-5.6 Terra** | $2.00 | $0.20 | $12.00 | 約1.05M |
| **Kimi K3** | $3.00 | $0.30 | $15.00 | 1M |
| **Claude Opus 5** | $5.00 | $0.50 | $25.00 | 1M |
| **GPT-5.6 Sol** | $5.00 | $0.50 | $30.00 | 約1.05M |

DeepSeekのキャッシュ入力は極端に安く、同一リポジトリや同一仕様を繰り返し送るCoding Agentと相性がよい価格設定です。出典: [DeepSeek Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

GPT-5.6 TerraとLunaは2026年7月30日に値下げされました。現在の標準価格はTerraが$2／$12、Lunaが$0.20／$1.20です。長大な単一リクエストでは別の長文価格帯が適用されるため、後述の費用は複数リクエストの合計として計算しています。出典: [OpenAI Pricing](https://developers.openai.com/api/docs/pricing)

KimiとGLMの料金は公式APIの従量課金です。GLM Coding Planなどの定額枠はこの表に含めていません。出典: [Z.AI Pricing](https://docs.z.ai/guides/overview/pricing)

Claude Opus 5は入力$5、出力$25で、キャッシュ読取は$0.50です。初回キャッシュ書込みは5分保持で$6.25、1時間保持で$10になります。出典: [Claude Pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)

### 個人開発に近い費用感

次のトークン量を、複数回のAPI呼び出しの合計として想定します。

```text
入力合計：100万トークン
出力合計：10万トークン
```

これは、リポジトリ探索、複数回の修正、テスト結果の再入力、セルフレビューまで行う**中～大規模のIssue対応1件**を想定した値です。

#### キャッシュなし

| 費用順 | モデル | 1セッション | 月20回 | DeepSeek Flash比 |
| --: | --- | ---: | ---: | ---: |
| 1 | **DeepSeek V4 Flash** | **$0.168** | **$3.36** | 1.0倍 |
| 2 | **GPT-5.6 Luna** | **$0.32** | **$6.40** | 1.9倍 |
| 3 | DeepSeek V4 Pro | $0.522 | $10.44 | 3.1倍 |
| 4 | Kimi K2.7 Code | $1.35 | $27.00 | 8.0倍 |
| 5 | GLM-5.2 | $1.84 | $36.80 | 11.0倍 |
| 6 | GPT-5.6 Terra | $3.20 | $64.00 | 19.0倍 |
| 7 | Kimi K3 | $4.50 | $90.00 | 26.8倍 |
| 8 | Claude Opus 5 | $7.50 | $150.00 | 44.6倍 |
| 9 | GPT-5.6 Sol | $8.00 | $160.00 | 47.6倍 |

5倍規模の重いセッション（入力500万・出力50万）では、この表の1セッション費用をそのまま5倍にします。

例：

- DeepSeek Flash：$0.84
- Luna：$1.60
- GLM-5.2：$9.20
- Terra：$16.00
- Kimi K3：$22.50
- Opus 5：$37.50
- Sol：$40.00

外部検索、コンテナ、コード実行、OpenRouter手数料、税金は含めていません。出典: [DeepSeek Pricing](https://api-docs.deepseek.com/quick_start/pricing/)

#### 80%の入力でキャッシュが効く場合

入力100万のうち80万トークンがキャッシュヒットし、出力10万トークンと仮定します。

| 費用順 | モデル | キャッシュなし | 80%キャッシュ | 削減率 |
| --: | --- | ---: | ---: | ---: |
| 1 | **DeepSeek V4 Flash** | $0.168 | **$0.058** | 65% |
| 2 | **GPT-5.6 Luna** | $0.320 | **$0.176** | 45% |
| 3 | **DeepSeek V4 Pro** | $0.522 | **$0.177** | 66% |
| 4 | Kimi K2.7 Code | $1.350 | $0.742 | 45% |
| 5 | GLM-5.2 | $1.840 | $0.928 | 50% |
| 6 | GPT-5.6 Terra | $3.200 | $1.760 | 45% |
| 7 | Kimi K3 | $4.500 | $2.340 | 48% |
| 8 | Claude Opus 5 | $7.500 | $3.900 | 48% |
| 9 | GPT-5.6 Sol | $8.000 | $4.400 | 45% |

これはキャッシュが既に作成された後の再利用費用です。OpenAIとAnthropicは初回キャッシュ書込みに追加料金がかかるため、最初の呼び出しは表より高くなります。

注目点は、**キャッシュが効くとDeepSeek V4 ProとGPT-5.6 Lunaがほぼ同額**になることです。ただしLunaの方が主要コーディングベンチマークの公開根拠は強く、DeepSeek Proは現行Agent評価が不足しています。

### 性能と費用を統合した評価

#### Claude Opus 5

**評価：最高精度のスポット利用**

SWE-bench Pro 79.2%は今回の比較対象で最高です。明確なIssue、既存テスト、受入条件があるリポジトリ修正では最も有力です。ただし、1セッション$7.50なので日常的な探索や単純修正には過剰です。

適した使い方：

- 難しいバグ修正
- 実装者とは別モデルによる最終レビュー
- Migrationや並行処理など失敗コストの高い変更
- 他モデルが2回以上失敗した課題

#### GPT-5.6 Sol

**評価：最高クラスの総合Coding Agent**

DeepSWE 72.7、Terminal-Bench 88.8、Coding Agent Index 80で、ターミナル、ツール利用、長時間Agentの総合力が高いモデルです。ただし費用はOpus 5よりわずかに高いため、個人開発での常用には向きません。

適した使い方：

- 長時間の自律実装
- ビルド、テスト、修正を繰り返すAgent
- フロントエンドの視覚確認
- 複雑なTool Calling
- 最重要タスク

#### GPT-5.6 Terra

**評価：個人開発の総合バランス1位**

Solとの差は次の程度です。

| 指標 | Sol | Terra | 差 |
| --- | ---: | ---: | ---: |
| SWE-bench Pro | 64.6 | 63.4 | -1.2 |
| DeepSWE | 72.7 | 69.6 | -3.1 |
| Terminal-Bench | 88.8 | 87.4 | -1.4 |
| 1セッション費用 | $8.00 | $3.20 | **60%安い** |

Solの40%の費用で、主要Coding指標の差は小さく収まっています。OpenAI／Codex系のTool CallingやResponses APIまで含めると、個人開発の主力として有力です。出典: [OpenAI GPT-5.6](https://openai.com/index/gpt-5-6/)

#### GPT-5.6 Luna

**評価：低価格モデルの最有力**

LunaはDeepSeek Flashの約1.9倍ですが、主要評価では次の水準です。

- SWE-bench Pro：62.7
- DeepSWE：67.2
- Terminal-Bench：84.7
- Coding Agent Index：74.6

DeepSeek FlashのDeepSWE 54.4に対して67.2なので、**1回の成功率や人間の修正時間まで含めれば、Lunaの方が安くなる可能性があります**。

単純なトークン単価ではFlash、タスク完遂率を含む実費ではLunaが有力です。

#### Kimi K3

**評価：中国製モデルの性能最上位候補**

Terminal-Bench 88.3はSolの88.8にかなり近く、FrontierSWE 81.2も強力です。1セッション$4.50なので、Solより44%安く、Opus 5より40%安くなります。

ただし以下を考慮する必要があります。

- ベンチマークの多くがKimi Codeハーネス
- 最大推論設定
- 公開直後
- 出力$15と高い
- 常時Thinking
- デフォルト推論強度が高い

日常利用ではなく、GLM、Terra、DeepSeekが失敗した課題で使う位置付けが適切です。

#### GLM-5.2

**評価：中国製モデルの価格性能バランス1位**

1セッション$1.84で、FrontierSWE 74.4、Terminal-Bench 81～82.7程度です。

Terraより安く、DeepSeekより長時間Agentの公開評価が強いため、次の用途に向きます。

- GitHub Issueからの実装
- 長い仕様への追従
- 複数ファイル変更
- Cline、Claude Code、OpenCode
- 定額Coding Planによる大量利用

中国製モデルだけで選ぶなら、**主力はGLM-5.2、低価格処理はDeepSeek Flash、高難度はKimi K3**という構成が合理的です。

#### DeepSeek V4 Flash

**評価：最安の実用Coding Agent**

1セッション$0.168は圧倒的です。Terminal-Bench 82.7も低価格モデルとして高く、2026年7月31日の再学習でAgent性能が大きく改善しました。

向いている処理：

- リポジトリ探索
- テスト生成
- コードレビューの一次分析
- 小規模Issue
- ドキュメント更新
- CIログ分析
- サブエージェント
- 大量の並列処理

難しい複数ファイル変更で失敗したら、GLMまたはTerraへ昇格させる使い方が適切です。

#### DeepSeek V4 Pro

**評価：コーディング主力としては現在評価保留**

名称からFlashより上位に見えますが、7月31日に更新されたのはFlashだけで、Proは未更新です。DeepSeekは最新FlashのAgent評価がV4 Pro Previewを大きく上回ると説明しています。出典: [DeepSeek API Updates](https://api-docs.deepseek.com/updates/)

現時点では次の用途に限定するのが妥当です。

- 数学的・アルゴリズム的な推論
- Flashとは別の回答を得る
- 設計案の比較
- Flashが推論面で失敗したケース

Coding Agentの標準モデルとして、Flashより先に選ぶ根拠は弱くなっています。

#### Kimi K2.7 Code

**評価：性能より、公開評価不足が問題**

コード特化、256K、画像・動画、Thinking、Tool Callingという仕様は魅力的ですが、SWE-bench Pro、DeepSWE、Terminal-Benchなどの同条件スコアが十分公開されていません。

1セッション$1.35とGLMより安いものの、現時点では次の位置付けです。

- Kimi K3より安いKimi系モデル
- 画像・動画を含むコード修正
- Kimi Code CLIの標準モデル
- 独立レビュー用の別系列モデル

ベンチマーク透明性を重視するなら、GLM-5.2またはGPT-5.6 Luna／Terraを先に評価すべきです。

### 個人開発向け最終順位

#### 性能だけを重視

1. **Claude Opus 5**：実リポジトリIssue修正
2. **GPT-5.6 Sol**：総合Coding Agent
3. **Kimi K3**：長時間・ターミナルAgent
4. **GPT-5.6 Terra**
5. **GLM-5.2**
6. **GPT-5.6 Luna**
7. **DeepSeek V4 Flash**
8. DeepSeek V4 Pro：現行評価不足
9. Kimi K2.7 Code：公開評価不足

#### 価格性能比を重視

1. **GPT-5.6 Luna**
2. **DeepSeek V4 Flash**
3. **GLM-5.2**
4. **GPT-5.6 Terra**
5. DeepSeek V4 Pro
6. Kimi K3
7. Kimi K2.7 Code
8. Claude Opus 5
9. GPT-5.6 Sol

Lunaを1位としたのは、Flashより少し高いだけで、公開されている主要Coding Agentベンチマークがかなり高いためです。純粋なトークン単価だけならFlashが1位です。

### 推奨する段階的ルーティング

Issue単位でAI実装、独立レビュー、CI確認を行う場合は、次の4段階が適します。

```text
第1段階：探索・小規模修正・一次レビュー
  DeepSeek V4 Flash
  または GPT-5.6 Luna

第2段階：通常のIssue実装
  GLM-5.2
  または GPT-5.6 Terra

第3段階：難しい長時間Agent
  Kimi K3
  または GPT-5.6 Sol

第4段階：失敗コストの高い最終レビュー
  Claude Opus 5
```

#### 最も推奨する構成

| 役割 | 推奨モデル |
| --- | --- |
| リポジトリ探索 | DeepSeek V4 Flash |
| 日常的な実装 | GPT-5.6 Luna |
| 本格的なIssue実装 | GLM-5.2またはGPT-5.6 Terra |
| 独立レビュー | Claude Opus 5 |
| 最難関タスク | GPT-5.6 SolまたはKimi K3 |

**単一モデルに統一するならGPT-5.6 Terra。**

**中国製モデルに限定するならGLM-5.2。**

**費用最優先ならDeepSeek V4 Flash。**

**実装成功率と費用の両方を見るならGPT-5.6 Luna。**

価格・ベンチマーク・モデル更新を月1回確認する監視設定も有効です。

> 注意: API従量課金のみの比較です。月額プラン枠、OpenRouter手数料、実APIでの成功率・人間修正時間は含まれません。法人導入や機密コード送信は、元記事の検証計画とセキュリティ・法務ゲートを通してください。
