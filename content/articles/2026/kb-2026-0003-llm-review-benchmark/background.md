# 検討に至った背景

AIエージェントへ仕様書やPull Requestのレビューを依頼すると、もっともらしい指摘は多数得られます。しかし、実務で重要なのは指摘数ではありません。

- 本当に重要な欠陥を見つけられたか
- 正本にない改善案を欠陥として扱っていないか
- MajorをMinorへ過小評価していないか
- `READY`や`FAIL`の結論が指摘内容と整合しているか
- 同じモデルを再実行したとき、同じ結論になるか

これらを確認するため、最小銀行システムの製品仕様書を固定対象とし、複数のLLMへ独立レビューを依頼しました。

## 実験の特徴

対象は1つの仕様書、1つの固定Base SHA、1つの固定Head SHAです。レビュー対象や正本を途中で変更せず、各モデルへ同じEvidence bundleを渡しました。

Round 1では複数モデルの指摘を人間が審理し、根本原因単位のGold Findingを確定しました。Round 2ではプロンプトを改善し、外部検索、他モデル結果、Gold Finding、過去の評価結果をモデルへ渡さず、16件の独立レビューを再実行しました。

この構成により、単なるモデル人気や自己申告ではなく、同一課題に対するFinding Precision、Gold Finding Recall、重大度判断、根拠、修正案、Scope disciplineを比較できます。

## 公開データ

実験データは次のリポジトリに保存しています。

- Round 1: `kooiei-in4a/minimal-bank-system/docs/reviews/spec-review-001/`
- Round 2: `kooiei-in4a/minimal-bank-system/docs/reviews/spec-review-002/`
- 対象仕様: `docs/specs/bank-system-specification.md`

Round 2には16件の生レビュー、Finding審理、モデル評価、Round 1との比較、最終統合分析が含まれます。
