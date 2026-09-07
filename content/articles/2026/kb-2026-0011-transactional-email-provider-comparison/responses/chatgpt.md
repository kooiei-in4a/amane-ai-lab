# 調査結果

## 先に結論

`amane-mailer` の次Providerを考えるなら、現時点では次の順序が扱いやすい。

1. **Amazon SES** — 第2Providerの第一候補
2. **Twilio SendGrid** — 専業ESPの代表として有力
3. **Mailgun** — Webhook、Suppression、Inboundを含む別系統の専業ESP
4. **Zoho ZeptoMail** — Transactional Email特化のクレジット制候補

Azure Communication Services Email（ACS Email）は既存Providerとして継続する。

これは「サービス一般の優劣ランキング」ではない。`amane-mailer` のProvider abstractionを段階的に検証するための実装順序である。

## 料金比較

### Azure Communication Services Email

Microsoft Learnで確認できる料金は次の通り。

- Email Send: **$0.00025 / email**
- Data Transferred: **$0.00012 / MB**

1通0.5 MBなら、

`0.00025 + 0.5 × 0.00012 = $0.00031 / 通`

となる。

| 月間通数 | 概算 |
|---:|---:|
| 1,000 | $0.31 |
| 10,000 | $3.10 |
| 100,000 | $31 |
| 1,000,000 | $310 |

Azureはヘッダー、本文、画像、添付を含む受信者ごとの転送データ量を課金対象としている。Azure Pricingページでは、表示価格はUSDベースの概算であり、契約形態、購入日、通貨等で実請求が変わり得るとも明記されている。

出典:

- [Microsoft Learn - Email pricing in Azure Communication Services](https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing)
- [Azure Communication Services pricing](https://azure.microsoft.com/en-us/pricing/details/communication-services/)

### Amazon SES

Amazon SESは2026年7月にEssentials / Pro / Enterpriseの料金プランを追加した。一方で、**アラカルト料金へ切り替えることも可能**である。

アラカルトのOutbound Emailは、

- **$0.10 / 1,000 emails**
- 添付データ: **$0.12 / GB**

である。

したがって、添付を除く基本送信料金は次の通り。

| 月間通数 | 基本送信料金 |
|---:|---:|
| 1,000 | $0.10 |
| 10,000 | $1.00 |
| 100,000 | $10 |
| 1,000,000 | $100 |

仮に0.5 MBがすべて添付データだった場合は、概算で1,000通あたり約$0.06が追加され、1,000通あたり約$0.16、100万通で約$160になる。実際には0.5 MBのメール全体が添付とは限らないので、Azure ACSと同じ計算式で比較しない。

2026-07-21以降、新しいSESアカウント等はEssentialsから開始する条件があり、0〜1,000万通/月では$0.16/1,000通である。ただし公式にはアラカルトへ切り替え可能とされている。この記事の比較表は**アラカルトへ切り替えた場合**を示す。

出典:

- [Amazon SES pricing](https://aws.amazon.com/ses/pricing/)
- [Amazon SES introduces pricing plans](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-ses-pricing-plans/)

### Twilio SendGrid

SendGrid Email APIは月額プランが中心である。2026年9月時点の公開情報では、代表的なプランは次の通り。

- Free trial: 100 emails/day、60日間
- Essentials 50K: **$19.95 / month**
- Essentials 100K: **$34.95 / month**
- Pro 100K: $89.95 / month
- Pro 300K: $249 / month
- Pro 700K: $499 / month
- Pro 1.5M: $799 / month

100万通では、Pro 700Kに30万通の超過を加える単純計算なら、現行の超過単価$0.0008/emailを使って、

`$499 + 300,000 × $0.0008 = 約$739`

となる。

| 月間通数 | 概算 |
|---:|---:|
| 1,000 | $19.95（継続利用時） |
| 10,000 | $19.95 |
| 100,000 | $34.95 |
| 1,000,000 | 約$739（Pro 700K + 30万通超過） |

実際の請求は契約経路や選択プランで変わり得るため、購入時には最新のPricingページを再確認する。

出典:

- [Twilio SendGrid Email API pricing](https://www.twilio.com/en-us/products/email-api/pricing)
- [AWS Marketplace - Twilio SendGrid Email](https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai)

### Mailgun

Mailgun Sendの公開料金では、

- Free: $0、100 emails/day
- Basic: **$15 / month、10,000 emails**
- Foundation: **$35 / month、50,000 emails**
- Scale: **$90 / month、100,000 emails**

となっている。各プランには超過料金があり、Scaleでは送信量に応じて1,000通あたりの超過単価が$1.10、$0.90、$0.75、$0.60、$0.50…と段階的に示されている。

| 月間通数 | 公開料金から確認できる範囲 |
|---:|---:|
| 1,000 | Freeの日次上限内なら$0、安定運用は有料プラン検討 |
| 10,000 | $15 |
| 100,000 | $90 |
| 1,000,000 | Scale $90 + 超過料金。総額は契約前にControl Panelで確認 |

Mailgun自身が、個別アカウントの最終料金・overageはControl PanelのBilling / Upgradeページを正本として確認するよう案内している。そのため100万通の総額は、この記事では一意の金額に丸めない。

Mailgunは価格だけでなく、REST API、SMTP relay、Tracking、Analytics、Webhook、Suppression、Inbound routingなどを一体で提供する専業ESPである。

出典:

- [Mailgun pricing](https://www.mailgun.com/pricing/)
- [Mailgun Help - overage pricing](https://help.mailgun.com/hc/en-us/articles/6745531451547-What-happens-if-I-send-more-emails-than-my-monthly-plan-provides)

### Zoho ZeptoMail

ZeptoMailは月額サブスクリプションではなくクレジット制で、

- **1 Credit = 10,000 emails**
- 購入クレジットは6か月有効
- 最初の1 Credit（10,000通）は1か月有効の無料枠

という仕組みである。

ただし、現行の公式Pricingページには**「2026-07-01以降の新規契約からPricing Updateを適用」**という告知があり、具体的なper-credit金額は表示せず`Contact sales for pricing`としている。一方、Zohoの別ランディングページには従来の`$2.50 / 10,000 emails`表示が残っている。

同一ベンダーの公開ページ間で価格表示が一致していないため、この記事では$2.50を2026-09-07時点の現行価格として採用しない。

| 月間通数 | 現行公開情報で言えること |
|---:|---|
| 1,000 | 初回無料Creditの範囲内。ただし1日100通上限あり |
| 10,000 | 初回1 Creditは無料・1か月有効 |
| 100,000 | 10 Credits相当。購入単価は要問い合わせ |
| 1,000,000 | 100 Credits相当。購入単価は要問い合わせ |

ZeptoMailはTransactional Email向けであり、Bulk EmailやPromotional Emailを対象にしない。

出典:

- [Zoho ZeptoMail pricing](https://www.zoho.com/zeptomail/pricing.html)
- [Zoho ZeptoMail - Getting started](https://www.zoho.com/zeptomail/help/getting-started.html)
- [Zoho ZeptoMail - product page](https://www.zoho.com/zeptomail/)

## 1通0.5 MB・代表価格の一覧

料金体系が異なるため、単純な安い順ではなく、公式情報から同じ通数で確認できる範囲を並べる。

| Provider | 1,000 | 10,000 | 100,000 | 1,000,000 | 主な料金方式 |
|---|---:|---:|---:|---:|---|
| Azure ACS Email | $0.31 | $3.10 | $31 | $310 | 完全従量＋転送データ |
| Amazon SES（アラカルト） | $0.10〜約$0.16 | $1〜約$1.6 | $10〜約$16 | $100〜約$160 | 完全従量＋添付データ |
| SendGrid | $19.95 | $19.95 | $34.95 | 約$739 | 月額＋超過 |
| Mailgun | $0または$15 | $15 | $90 | Scale $90 + 超過（要確認） | 月額＋超過 |
| ZeptoMail | 初回無料枠内 | 初回1 Credit無料 | 10 Credits相当・価格要問い合わせ | 100 Credits相当・価格要問い合わせ | クレジット制 |

この表は機能やDeliverability支援を同一化したものではない。Dedicated IP、Validation、Deliverability monitoring、サポート等を含めると条件は変わる。

また、SESのレンジ上限は「0.5 MBがすべて添付データ」という比較用の厳しめな仮定であり、通常のメール全体サイズにそのまま適用するものではない。

## 2025年以降の普及度

2026年9月に確認した6senseのTransactional Emailカテゴリでは、ページ上部に274,597 Companies Trackedと表示され、上位は次のように推定されている。

| 順位 | Technology | 推定シェア | Customers |
|---:|---|---:|---:|
| 1 | Constant Contact | 30.44% | 83,581 |
| 2 | **SendGrid** | **14.45%** | **39,676** |
| 3 | **Amazon SES** | **13.97%** | **38,353** |
| 4 | SendinBlue | 9.67% | 26,541 |
| 5 | **Mailgun** | **9.39%** | **25,774** |
| 6 | Mailchimp Transactional Email | 8.66% | 23,768 |
| 7 | Mailjet | 7.32% | 20,098 |

出典: [6sense - Transactional Email market share 2026](https://6sense.com/tech/transactional-email)

ここで重要なのは、この数字が**送信メール通数の市場シェアではなく、6senseが検出・追跡する企業における推定導入シェア**だという点である。

またConstant Contactなどマーケティング寄りの製品も同じカテゴリに含まれるため、`amane-mailer` のProvider候補だけを直接比較するランキングではない。

それでも、SendGrid、Amazon SES、Mailgunが大規模な導入基盤を持つことを確認する補助指標としては使える。

ACS EmailとZeptoMailについては、今回確認できた公開資料では同じ定義で比較できる有力なシェア値を確認できなかった。数字がないことを「利用されていない」と解釈してはいけない。

## amane-mailerから見た意味

### Amazon SESを第2Providerにする理由

SESは価格だけでなく、ACSとは別クラウドの大規模メール基盤である点が重要である。

ACSの次にSESを実装すれば、現在の設計に残っているAzure固有部分を早い段階で発見できる。

例えば次の差が顕在化する。

- Delivery eventの取得方式
- Bounce / Complaintの表現
- Suppressionの扱い
- Provider message ID
- Retryable / permanent errorの分類
- Sender / Domain verification
- Configuration setやタグ等のProvider固有概念

この差を吸収できれば、`amane-mailer` のProvider abstractionが一段現実的になる。

### SendGrid / Mailgunをその次に置く理由

SESとACSはどちらもhyperscaler系のサービスである。

一方、SendGridとMailgunは専業ESPとして、Webhook、Suppression、Analytics、Deliverability運用などをサービスの中心に置いている。

したがって第3・第4Providerとして追加すると、単なるクラウドAPI差分ではなく、**専業ESP型の機能モデルまで共通化すべきか**を検証できる。

### ZeptoMailを後段に置く理由

ZeptoMailはTransactional Emailに特化し、API/SMTP、Webhook、Bounce reports、Suppressionなど、`amane-mailer` と相性のよい機能を持つ。

一方、現行価格は公式ページ間で表示が一致しておらず、正確な購入単価は契約前の確認が必要である。設計検証という意味でも、まずSESと専業ESPを通して共通モデルを固めた後に追加した方が得られる情報が多い。

## 設計上の示唆

Providerを増やすなら、共通化対象を単純な`SendAsync()`だけにしない。

最低限、次の概念をProvider非依存で扱えるか検討する価値がある。

- Send request / result
- Provider message ID
- Delivery status
- Bounce
- Complaint / Spam
- Suppression
- Provider-specific error
- Retryability
- Event/Webhook ingestion
- Attachment / message size limit
- Sender / domain verification state

ただし、全Providerの機能を最小公倍数へ押し込むのも避ける。

**Common core + Provider capabilities** とし、例えばSuppression、Dedicated IP、Tags、Inbound routing等はCapabilityとして表現する方が自然である。

## 調査時点

最終確認: **2026-09-07**

料金とプランは変更されるため、実装または契約時には各Providerの公式料金ページと、必要に応じて管理画面・営業見積を再確認する。
