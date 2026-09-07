# 結論

現時点では、`amane-mailer` のProvider拡張は次の考え方で進めるのが妥当である。

1. **Azure ACS Email**を現行baselineとして維持する。
2. **Amazon SES**を第2Providerの第一候補とする。
3. 第3Providerでは**SendGridまたはMailgun**を入れ、専業ESP型のAPI・Webhook・Suppression運用まで抽象化が耐えられるか確認する。
4. **ZeptoMail**は低コストかつTransactional Email特化の追加候補として扱う。

1通0.5 MB、月100万通の単純な料金規模では、Azure ACS Emailは約$310、SESアラカルトは基本$100で、0.5 MBがすべて添付だった厳しめの仮定でも約$160が目安になる。ZeptoMailはクレジット換算で約$250、SendGrid/Mailgunは月額プラン中心で約$700台の規模になる。

ただし、送信単価だけでProviderを選ばない。実際の設計では、Bounce、Complaint、Suppression、Delivery Event、Retryability、Provider message ID、Sender/Domain verification、Provider固有Capabilityをどこまで共通化するかが重要になる。

2026年の6sense推定ではSendGrid、Amazon SES、MailgunがTransactional Emailカテゴリの主要導入製品として確認できる。一方、ACS EmailとZeptoMailには同じ定義で比較できる有力な公開シェア値を確認できなかった。

このため、次工程では「多数のProviderを一気に追加する」のではなく、**まずSESを2社目として実装し、その差分からProvider abstractionを固める**ことを優先する。
