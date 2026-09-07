# 背景

`amane-mailer` は現在 Azure Communication Services Email（ACS Email）を送信基盤として利用している。Delivery Report は Event Grid から Storage Queue へ流し、バウンスや配信状態をアプリケーション側で扱える構成にしている。

今後 `amane-mailer` を特定クラウド専用ではなく、複数のメール送信Providerに対応できる形へ育てることを考え、次に実装候補とするサービスを整理した。

今回の問いは次の2点である。

1. 1通0.5 MB程度のトランザクションメールを送る場合、主要サービスの料金はどの程度違うか。
2. 2025年以降の公開情報から見て、どのサービスが実際に広く使われているか。

比較対象は、現行のACS Emailに加えて、Amazon SES、Twilio SendGrid、Mailgun、Zoho ZeptoMailとした。

## 前提と注意

- 価格は2026-09-07時点で確認できた公開料金を使用する。
- 税、為替、Dedicated IP、Email Validation、Deliverability系アドオン等は基本比較に含めない。
- Azure ACS Emailはメール全体の転送データ量に課金される。
- Amazon SESのアラカルト追加データ料金は送信した添付データが対象であり、0.5 MBのメール全体をそのままAzureと同じ式で課金してはいけない。
- SendGridやMailgunは月額プランと超過課金があるため、従量課金サービスと単価構造が異なる。
- ZeptoMailはTransactional Email専用で、ニュースレター等のBulk/Promotional用途を対象にしない。
- 市場シェアは6senseが推定するTransactional Email製品の導入企業シェアを参照した。これは送信通数、売上、SMTPトラフィックのシェアではない。

この調査はProvider採用の最終決定ではなく、`amane-mailer` の次の実装順序を考えるための技術選定メモとして位置づける。
