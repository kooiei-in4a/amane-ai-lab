# 背景

`amane-mailer` は現在 Azure Communication Services Email（ACS Email）を送信基盤として利用している。Delivery Report は Event Grid から Storage Queue へ流し、バウンスや配信状態をアプリケーション側で扱える構成にしている。

今後 `amane-mailer` を特定クラウド専用ではなく、複数のメール送信Providerに対応できる形へ育てることを考え、次に実装候補とするサービスを整理した。

今回の問いは次の2点である。

1. 1通0.5 MB程度のトランザクションメールを送る場合、主要サービスの料金はどの程度違うか。
2. 2025年以降の公開情報から見て、どのサービスが実際に広く使われているか。

比較対象は、現行のACS Emailに加えて、Amazon SES、Twilio SendGrid、Mailgun、Zoho ZeptoMailとした。

## 前提と注意

- 料金・料金体系は2026-09-07時点の公式情報を確認する。公式ページで現行の具体額を確定できない場合は推定しない。
- 税、為替、Dedicated IP、Email Validation、Deliverability系アドオン等は基本比較に含めない。
- Azureの表示価格はUSDベースの概算で、契約形態、購入日、通貨等により実請求は変わり得る。
- Azure ACS Emailはメール全体の転送データ量に課金される。
- Amazon SESのアラカルト追加データ料金は送信した添付データが対象であり、0.5 MBのメール全体をそのままAzureと同じ式で課金してはいけない。
- Amazon SESは2026-07-21以降、一部の新規アカウント等でEssentialsから開始する。本文の最安比較は明示的にアラカルトへ切り替えた場合である。
- SendGridやMailgunは月額プランと超過課金があるため、従量課金サービスと単価構造が異なる。
- ZeptoMailはTransactional Email専用で、ニュースレター等のBulk/Promotional用途を対象にしない。現行Pricingページは2026-07-01以降の新規契約向け価格改定を告知し、具体額を表示せずContact salesとしている。一方、別のZohoページには旧来の$2.50/10,000通表示が残っているため、この記事では現行価格として採用しない。
- 市場シェアは6senseが推定するTransactional Email製品の導入企業シェアを参照した。これは送信通数、売上、SMTPトラフィックのシェアではない。

この調査はProvider採用の最終決定ではなく、`amane-mailer` の次の実装順序を考えるための技術選定メモとして位置づける。
