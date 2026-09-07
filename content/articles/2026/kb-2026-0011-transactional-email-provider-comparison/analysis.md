# 分析

今回の比較では、単純な料金順位と `amane-mailer` の実装優先順位を分けて考える必要がある。

価格だけならAmazon SESのアラカルトが最も強く、ZeptoMailとAzure ACS Emailがその次に来る。一方、SendGridやMailgunは月額プランが中心で、送信単価だけを見ると高い。しかし専業ESPとしてWebhook、Suppression、Analytics、Deliverability運用まで含むため、比較対象としての価値は別にある。

## 市場シェアの読み方

6senseの2026年推定では、SendGrid 14.45%、Amazon SES 13.97%、Mailgun 9.39%で、この3製品はTransactional Emailカテゴリの主要サービスとして広く検出されている。

ただし、この数字は「全世界の送信メールの何%を処理したか」ではない。6senseが追跡する企業における推定導入シェアである。ACS EmailとZeptoMailに同じ定義の比較可能な値がないため、シェア不明を低品質や低利用と結び付けない。

## amane-mailerで得たいもの

第2ProviderとしてSESを追加する価値は、コスト削減よりも**抽象化境界の検証**にある。

ACSだけで設計している間は、Delivery Report、Event Grid、Azure固有IDやエラー分類が共通概念に見えやすい。SESを追加すると、Bounce/Complaint、SNS/EventBridge等のイベント経路、Suppression、Configuration Setなど別の概念体系と向き合うことになる。

この段階でCommon coreを固め、その後SendGridまたはMailgunを追加すれば、hyperscaler型だけでなく専業ESP型にも抽象化が耐えられるか確認できる。

ZeptoMailはTransactional Email特化で価格も低いため有力だが、設計検証という意味ではSESと専業ESPを先に実装した方が、先に異質な差分を発見しやすい。

## 暫定的な実装順

```text
Application
    ↓
amane-mailer
    ↓
Provider abstraction
    ├─ Azure ACS       ← current baseline
    ├─ Amazon SES      ← next
    ├─ SendGrid        ← specialist ESP
    ├─ Mailgun         ← specialist ESP / inbound-capable
    └─ ZeptoMail       ← low-cost transactional specialist
```

順番は固定ではない。第3ProviderはSendGridかMailgunのどちらか一方を先に実装すれば、Provider abstractionの検証としては十分な可能性が高い。

重要なのは、Provider数を増やすこと自体ではなく、2社目・3社目で見つかった差分を共通モデルとProvider固有Capabilityへ正しく分離することである。
