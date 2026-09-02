# ChatGPT回答（公開用に編集）

## 結論

今回いちばん効果が大きかったのは、AIエージェントを「ローカルPC上で動く開発ツール」として扱うのではなく、**隔離されたLinux開発環境へ接続するクライアント**として扱うようにしたことです。

Proxmox VEとMicrosoft Hyper-Vの両方で構築した結果、Hypervisor固有の実装差はあっても、次の基本パターンは共通化できました。

```text
Human interface
    │
    ▼
Windows client
    │
    ▼
Linux Agent VM
    ├─ repositories
    ├─ worktrees
    ├─ containers
    ├─ build / test
    └─ agent CLIs
```

特に良かったのは、ローカルPCの負荷低減、開発環境の標準化、操作端末への依存低減、VM境界による安全性、Snapshot / Checkpointによる復旧性、Git worktreeを利用した並行作業です。

## 設計の中心

エージェントの権限を細かく削りすぎると、自律開発のたびに人間の承認が必要になります。そこで、VM内部では開発に必要な能力を持たせつつ、VMの外側への影響をネットワークと仮想化境界で抑える方法を採りました。

つまり、重要なのは「エージェントを弱くする」ことよりも、**強いエージェントを安全に動かせる箱を作ること**です。

## Windows側のクライアント

2026年9月時点では、Claude側はClaude DesktopのCodeタブでClaude Code Desktopを利用でき、SSH環境も公式サポートされています。OpenAI側は新しいChatGPT desktop appにCodexが統合されています。CursorはAgentとCursor CLIを利用できます。

OpenCodeは候補でしたが、Desktopのnative Remote SSH supportがFeature Requestとして残っているため、今回の正式構成には含めませんでした。

## 次に改善するなら

次の重点はVM構築の自動化です。OS、ネットワークポリシー、Toolchain、Agent CLI、Repository配置、Acceptance Testまでをコード化できれば、Agent VMを修理する環境ではなく、必要に応じて再生成できるDisposable Runtimeへ近づけられます。
