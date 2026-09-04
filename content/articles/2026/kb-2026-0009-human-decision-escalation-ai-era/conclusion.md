## 31. 今回得たHuman Decision Escalation原則

今回の壁打ちから、Agentic AI設計に再利用できる原則を整理する。

### Principle 1 — Knowledge GapだけでHumanを呼ばない

AIの能力向上で消えるEscalationを中心設計にしない。

### Principle 2 — Humanでなければ意味が変わる時だけ呼ぶ

優先対象：

- First-party Intent
- Real Experience
- Fresh Ground Truth
- Human Authority
- Independent Attestation

### Principle 3 — Internal / Externalを分ける

Internal Human向け：

- 組織固有Context
- 権限
- 機密
- 責任

External Human向け：

- 顧客本人の視点
- 社内にない経験
- 現地確認
- 独立第三者確認

### Principle 4 — Verificationは品質機構であり商品ではない

顧客へ売るのはOutcome。

### Principle 5 — AI Assistanceを許容する

AIを使ったかではなく、Humanが判断へ参加したかを見る。

### Principle 6 — Human Judgmentを正解扱いしない

HumanにもCalibration、Conflict管理、Cohort管理が必要。

### Principle 7 — Text AI DetectionよりInteraction Evidence

操作、音声、具体箇所、条件変化への説明を重視する。

### Principle 8 — MarketplaceよりService First

両面市場の前に、有料需要を手動で確認する。

### Principle 9 — Current WedgeとFuture Platformを別仮説にする

現在の売上を未来API需要の証明にしない。

### Principle 10 — Human Escalationそのものを最小化する

Humanを呼ぶことを価値と考えない。

Agentの価値は、不要なHuman Escalationを減らし、**必要なHuman Decisionだけを高品質に抽出すること**にもある。

この点は、このLabで採用している「人間に確認してもらうのではなく、人間に決めてもらう必要があるときだけ呼ぶ」という原則とも整合する。

今回の検討は、この原則を社内Agent workflowから、外部Humanを含むAI時代の市場設計まで拡張したものと位置付けられる。

---

## 32. 現時点の最終判断

今回生まれたJapan Enterprise Readiness Gateについては、

> 本格開発する価値が確認された

とは判断していない。

現時点の判断は、

> **短期間の販売実験を行う価値がある**

である。

この違いを明確にする。

```yaml
CURRENT_DECISION:
  PRODUCT_BUILD: NO
  MARKETPLACE_BUILD: NO
  HUMAN_API_BUILD: NO
  MARKET_TEST: YES
```

---

## 33. 市場テストの基本設計

最小テストは2週間程度を想定する。

商品は一つ。

```text
Japan Enterprise Readiness Gate

Reviewer:
日本企業の情シス経験者3人

Scope:
Pricing / SSO / Security

SLA:
48時間

Price Hypothesis:
約15万円

Output:
Enterprise Blocker
Evidence
Prioritized Fixes
```

対象企業は、

- 日本語サイトを公開した
- 日本向け価格を出した
- 日本で採用・提携を開始した
- Enterprise planを持つ

など、日本展開の具体的シグナルがある海外B2B SaaSを優先する。

開発は行わない。

---

## 34. Go / No-Go

強いGoシグナル：

```text
初回購入
↓
別ページも確認依頼
↓
修正版の再評価
↓
継続契約
```

弱いシグナル：

```text
面白かった
参考になった
また何かあれば
```

No-Go候補：

- 有料発注が取れない
- 一度買うが再発注しない
- 既存サービスで十分と言われる
- HumanとAI評価に意味のある差がない
- 毎回新規Recruitingが必要で粗利が残らない
- 個別設計が重く標準化できない

---

## 35. R&Dとして残す結論

```yaml
HUMAN_DECISION_ESCALATION:
  USE_HUMAN_FOR_GENERIC_KNOWLEDGE_GAPS: false

  PREFER_HUMAN_WHEN:
    - FIRST_PARTY_INTENT
    - REAL_EXPERIENCE
    - FRESH_GROUND_TRUTH
    - HUMAN_AUTHORITY
    - INDEPENDENT_ATTESTATION

INTERNAL_VS_EXTERNAL:
  INTERNAL:
    - ORGANIZATION_CONTEXT
    - AUTHORITY
    - CONFIDENTIAL_DECISION
    - RESPONSIBILITY

  EXTERNAL:
    - TARGET_CUSTOMER_PERSPECTIVE
    - MISSING_EXTERNAL_EXPERIENCE
    - PHYSICAL_OBSERVATION
    - INDEPENDENT_REVIEW

AI_USE:
  AI_ASSISTANCE: ACCEPTABLE
  AI_SUBSTITUTION: QUALITY_RISK

QUALITY:
  TEXT_ONLY_AI_DETECTION: NOT_PRIMARY
  INTERACTION_EVIDENCE: PREFERRED
  HUMAN_JUDGMENT_IS_GROUND_TRUTH: false

BUSINESS:
  BUILD_MARKETPLACE_FIRST: false
  SELL_SERVICE_FIRST: true
  REQUIRE_REAL_PAYMENT_SIGNAL: true
  REPEAT_PURCHASE_OVER_INITIAL_INTEREST: true

FUTURE_HUMAN_API:
  STATUS: OPTION_ONLY
  TRIGGERS:
    - REPEATED_TASK_SCHEMA
    - HIGH_FREQUENCY_USAGE
    - STRUCTURED_RESULT_DEMAND
    - WEBHOOK_OR_API_DEMAND
    - DOWNSTREAM_AUTOMATION_USE

CURRENT_WEDGE:
  NAME: Japan Enterprise Readiness Gate
  STATUS: MARKET_TEST_CANDIDATE
  BUILD_PRODUCT_NOW: false
```

---

## 36. Final Takeaway

今回の議論で、最初の事業案はほぼ消えた。

しかし、検討自体は無駄ではなかった。

Paid Inboxという具体的なアイデアを壊し続けた結果、より一般的なAgentic AIの設計原則へ到達した。

> **AIに聞けることはAIに聞く。**
>
> **Humanへ聞くのは、Humanでなければその答えの経済的意味が変わる場合だけ。**
>
> **Humanを使う場合も、人間だから正しいとは扱わず、EvidenceとCalibrationを持つ。**
>
> **そして、どれだけ魅力的な未来像を作っても、事業の最後の判断は市場へ返す。**

AI Agentの能力が上がるほど、人間を多く挟むシステムが優れているとは限らない。

むしろ価値が高いのは、

> **Human Decisionを必要最小限まで減らし、本当に人間でなければならない判断だけを正しく抽出し、適切なHumanへ届けること**

かもしれない。

今回の壁打ちは、その仮説を事業案の検討から逆算して再確認したものとして記録する。
