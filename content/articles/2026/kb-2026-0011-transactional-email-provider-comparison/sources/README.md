# Sources

最終確認日: 2026-09-07

## Primary pricing / product sources

1. Microsoft Learn — Email pricing in Azure Communication Services
   - https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing
   - 確認事項: $0.00025/email、$0.00012/MB、転送量の対象範囲

2. Microsoft Azure — Azure Communication Services pricing
   - https://azure.microsoft.com/en-us/pricing/details/communication-services/
   - 確認事項: Email pricingの公式Pricingページ、表示価格は概算で契約形態・購入日・通貨等により実請求が変わり得ること

3. Amazon Web Services — Amazon SES pricing
   - https://aws.amazon.com/ses/pricing/
   - 確認事項: アラカルト $0.10/1,000 emails、添付データ $0.12/GB、Essentials $0.16/1,000 emails、新規条件ではEssentials開始・アラカルト切替可能

4. Amazon Web Services — Amazon SES introduces pricing plans
   - https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-ses-pricing-plans/
   - 公開日: 2026-07-21
   - 確認事項: Essentials / Pro / Enterpriseの導入

5. Twilio — SendGrid Email API pricing
   - https://www.twilio.com/en-us/products/email-api/pricing
   - 確認事項: 60日Free trial、Essentials/Pro、各volume tierの超過単価

6. AWS Marketplace — Twilio SendGrid Email
   - https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
   - 確認事項: Essentials 50K $19.95、100K $34.95、Pro 100K $89.95、300K $249、700K $499、1.5M $799等の現行表示

7. Mailgun — Pricing
   - https://www.mailgun.com/pricing/
   - 確認事項: Free、Basic $15/10K、Foundation $35/50K、Scale $90/100Kの公開料金

8. Mailgun Help Center — Overage pricing
   - https://help.mailgun.com/hc/en-us/articles/6745531451547-What-happens-if-I-send-more-emails-than-my-monthly-plan-provides
   - 確認事項: volume別の超過料金、個別アカウントではControl Panelが最終料金の正本であること

9. Zoho ZeptoMail — Pricing
   - https://www.zoho.com/zeptomail/pricing.html
   - 確認事項: Pricing Updateは2026-07-01以降の新規契約から適用、1 credit = 10,000 emails、6か月有効、具体額はContact sales、初回1 creditは無料・1か月有効

10. Zoho ZeptoMail — Getting started
    - https://www.zoho.com/zeptomail/help/getting-started.html
    - 確認事項: Transactional Email専用、1 credit = 10,000 emails、初回無料Credit、購入Creditは6か月有効

11. Zoho ZeptoMail — Product page
    - https://www.zoho.com/zeptomail/
    - 確認事項: 別ページには$2.50/10,000 emails表示が残っている。Pricingページの価格改定告知と表示が一致しないため、本文では$2.50を2026-09-07時点の現行価格として採用しない。

## Market adoption source

12. 6sense — Transactional Email market share 2026
    - https://6sense.com/tech/transactional-email
    - 確認事項: ページ上部274,597 Companies Tracked、SendGrid 14.45%、Amazon SES 13.97%、Mailgun 9.39%
    - 注意: 6senseによる推定導入シェア。送信通数・売上・SMTPトラフィックの市場シェアではない。

## Evidence policy

価格は変更される可能性があるため、契約・実装判断時には上記Primary sourceを再確認する。公式ページ間で価格表示が一致しない場合は、都合のよい数字を採用せず不一致自体を記録する。
市場シェアは測定方法が異なるデータを混ぜず、本文では6senseの同一カテゴリ・同一定義の数値だけを比較に使用した。
