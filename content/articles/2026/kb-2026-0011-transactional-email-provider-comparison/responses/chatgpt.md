# 調査結果

## 先に結論

`amane-mailer` の次Providerを考えるなら、現時点では次の順序が扱いやすい。

1. **Amazon SES** — 第2Providerの第一候補
2. **Twilio SendGrid** — 専業ESPの代表として有力
3. **Mailgun** — Webhook、Suppression、Inboundを含む別系統の専業ESP
4. **Zoho ZeptoMail** — 低コストのTransactional Email特化候補

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

Azureはヘッダー、本文、画像、添付を含む受信者ごとの転送データ量を課金対象としている。

出典: [Microsoft Learn - Email pricing in Azure Communication Services](https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing)

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

2026-07-21以降、新規SESアカウント等はEssentialsから開始する条件があるが、公式にはアラカルトへ切り替え可能とされている。

出典:

- [Amazon SES pricing](https://aws.amazon.com/ses/pricing/)
- [Amazon SES introduces pricing plans](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-ses-pricing-plans/)

### Zoho ZeptoMail

ZeptoMailは月額サブスクリプションではなくクレジット制で、

- **1 Credit = 10,000 emails**
- **1 Credit = $2.50**
- 購入クレジットは6か月有効

となっている。

単純換算では、

| 月間通数 | 必要クレジット相当 |
|---:|---:|
| 1,000 | $2.50を購入し残りを後日利用 |
| 10,000 | $2.50 |
| 100,000 | $25 |
| 1,000,000 | $250 |

小量時には最低購入単位が効くが、継続利用時の単価は1,000通あたり$0.25相当である。

ZeptoMailはTransactional Email向けであり、Bulk EmailやPromotional Emailを対象にしない。

出典:

- [Zoho ZeptoMail - Getting started](https://www.zoho.com/zeptomail/help/getting-started.html)
- [Zoho ZeptoMail - high volume email](https://www.zoho.com/zeptomail/articles/managing-high-volume-emails.html)

### Twilio SendGrid

SendGrid Email APIは従量制ではなく月額プランが中心である。2026年9月時点の公開情報では、代表的なプランは次の通り。

- Free trial: 100 emails/day、60日間
- Essentials 50K: **$19.95 / month**
- Essentials 100K: **$34.95 / month**
- Pro 100K: $89.95 / month
- Pro 300K: $249 / month
- Pro 700K: $499 / month
- Pro 1.5M: $799 / month

最小コスト側で見ると概ね次の規模感になる。

| 月間通数 | 概算 |
|---:|---:|
| 1,000 | $19.95（継続利用時） |
| 10,000 | $19.95 |
| 100,000 | $34.95 |
| 1,000,000 | 約$730台（700Kプラン＋超過を使う場合の目安） |

実際の請求は選択プランと超過単価で決まるため、100万通付近では購入時に最新のvolume selectorを再確認する必要がある。

出典:

- [Twilio SendGrid Email API pricing](https://www.twilio.com/en-us/products/email-api/pricing)
- [SendGrid Email API plan comparison](https://sendgrid.com/content/dam/sendgrid/global/en/other/sendgrid-pricing/twi121--sendgrid-pricing-pdf-st1.pdf)

### Mailgun

Mailgun Sendの公開料金では、

- Free: $0、100 emails/day
- Basic: **$15 / month、10,000 emails**
- Foundation: **$35 / month、50,000 emails**
- Scale: **$90 / month、100,000 emails** から

となっている。各プランには超過料金があり、volumeによって段階的に変わる。

| 月間通数 | 公開料金から見た目安 |
|---:|---:|
| 1,000 | Freeの日次上限内なら$0、安定運用は有料プラン検討 |
| 10,000 | $15 |
| 100,000 | 約$75〜90程度のvolume tierを要確認 |
| 1,000,000 | 約$700前後のScale volume tierが目安。購入時再確認 |

Mailgunは価格だけでなく、REST API、SMTP relay、Tracking、Analytics、Webhook、Suppression、Inbound routingなどを一体で提供する専業ESPである。

出典:

- [Mailgun pricing](https://www.mailgun.com/pricing/)
- [Mailgun Help - overage pricing](https://help.mailgun.com/hc/en-us/articles/6745531451547-What-happens-if-I-send-more-emails-than-my-monthly-plan-provides)

## 1通0.5 MB・代表価格の一覧

条件差を含めて見ると、概ね次の順になる。

| Provider | 1,000 | 10,000 | 100,000 | 1,000,000 | 主な料金方式 |
|---|---:|---:|---:|---:|---|
| Amazon SES（アラカルト） | $0.10〜約$0.16 | $1〜約$1.6 | $10〜約$16 | $100〜約$160 | 完全従量＋添付データ |
| ZeptoMail | $2.50最低購入 | $2.50 | $25 | $250 | 1万通単位クレジット |
| Azure ACS Email | $0.31 | $3.10 | $31 | $310 | 完全従量＋転送データ |
| SendGrid | $19.95 | $19.95 | $34.95 | 約$730台 | 月額＋超過 |
| Mailgun | $0または$15 | $15 | 約$75〜90 | 約$700前後 | 月額＋超過 |

この表は機能やDeliverability支援を同一化したものではない。Dedicated IP、Validation、Deliverability monitoring、サポート等を含めると条件は変わる。

## 2025年以降の普及度

2026年9月に確認した6senseのTransactional Emailカテゴリでは、274,597社を追跡し、上位は次のように推定されている。

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

ZeptoMailは価格が安くTransactional Emailに特化しているため、`amane-mailer` の用途との相性はよい。

ただし、まずSESと専業ESPを通して共通モデルを固めた後に追加した方が、Provider abstractionの検証順序として得られる情報が多い。

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

料金とプランは変更されるため、実装または契約時には各Providerの公式料金ページを再確認する。
