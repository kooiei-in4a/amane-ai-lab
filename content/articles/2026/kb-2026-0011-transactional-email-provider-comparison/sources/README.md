# Sources

最終確認日: 2026-09-07

## Primary pricing / product sources

1. Microsoft Learn — Email pricing in Azure Communication Services
   - https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing
   - 確認事項: $0.00025/email、$0.00012/MB、転送量の対象範囲

2. Amazon Web Services — Amazon SES pricing
   - https://aws.amazon.com/ses/pricing/
   - 確認事項: アラカルト $0.10/1,000 emails、添付データ $0.12/GB、Essentials/Pro/Enterprise

3. Amazon Web Services — Amazon SES introduces pricing plans
   - https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-ses-pricing-plans/
   - 公開日: 2026-07-21
   - 確認事項: 新料金プラン導入、アラカルトへの切替可能性

4. Twilio — SendGrid Email API pricing
   - https://www.twilio.com/en-us/products/email-api/pricing
   - 確認事項: Free trial、Essentials/Pro、超過課金

5. Twilio SendGrid — Email API plan comparison PDF
   - https://sendgrid.com/content/dam/sendgrid/global/en/other/sendgrid-pricing/twi121--sendgrid-pricing-pdf-st1.pdf
   - 確認事項: 50K〜2.5Mの代表プラン料金と超過単価

6. Mailgun — Pricing
   - https://www.mailgun.com/pricing/
   - 確認事項: Free、Basic、Foundation、Scaleの公開料金

7. Mailgun Help Center — Overage pricing
   - https://help.mailgun.com/hc/en-us/articles/6745531451547-What-happens-if-I-send-more-emails-than-my-monthly-plan-provides
   - 確認事項: volume別の超過料金

8. Zoho ZeptoMail — Getting started
   - https://www.zoho.com/zeptomail/help/getting-started.html
   - 確認事項: Transactional Email専用、10,000 emails/credit、購入クレジット6か月有効

9. Zoho ZeptoMail — Managing high-volume emails
   - https://www.zoho.com/zeptomail/articles/managing-high-volume-emails.html
   - 確認事項: $2.50/10,000 emails

## Market adoption source

10. 6sense — Transactional Email market share 2026
    - https://6sense.com/tech/transactional-email
    - 確認事項: 274,597 companies tracked、SendGrid 14.45%、Amazon SES 13.97%、Mailgun 9.39%
    - 注意: 6senseによる推定導入シェア。送信通数・売上・SMTPトラフィックの市場シェアではない。

## Evidence policy

価格は変更される可能性があるため、契約・実装判断時には上記Primary sourceを再確認する。
市場シェアは測定方法が異なるデータを混ぜず、本文では6senseの同一カテゴリ・同一定義の数値だけを比較に使用した。
