# なぜAgent VMを作ったか

AIコーディングエージェントを使う時間が増えるほど、モデル性能とは別の問題が目立つようになりました。ローカルPCで直接動かすと、ビルド、テスト、Docker、依存関係の導入が普段使うPCの負荷になります。さらに、Windows固有の設定やツール差分が、エージェントへの指示そのものに混ざります。

もう一つの問題は権限です。エージェントに自律的な開発を任せるには、ファイル変更、Git操作、テスト実行、コンテナ操作など、ある程度強い権限が必要です。しかし、その権限を普段使うPCへ直接与えることには抵抗があります。

そこで、実際の開発作業を専用Linux VMへ移しました。

今回の検証では、同じ考え方を **Proxmox VE** と **Microsoft Hyper-V** の両方で構築しました。目的はHypervisorの比較ではありません。Hypervisorが変わっても成立する、AIエージェント向けの実行環境パターンを確認することです。

考え方は単純です。

```text
Windows PC
    │
    │ 指示・監督
    ▼
Linux Agent VM
    │
    ├─ Git
    ├─ Docker
    ├─ Build / Test
    └─ AI coding agents
```

Windows PCは人間のインターフェースとして残し、コード、Toolchain、Runtime、コンテナなど、実際の作業状態をLinux VMへ寄せます。

Windows側では、Claude DesktopのCodeタブで提供される **Claude Code Desktop**、**ChatGPT desktop appのCodex**、**Cursor Agent / Cursor CLI** などを利用・検証しました。Claude Code Desktopは公式にSSH環境をサポートしています。OpenCodeについては、今回欲しかったDesktopからのnative Remote SSHがまだFeature Requestとして残っているため、正式な構成には入れていません。

この記事では、個別のProject名、ホスト名、IPアドレス、ユーザー名、VM固有IDなどは公開しません。公開するのは、別の環境でも再利用できる設計上の知見と運用上の結果です。

## 参照した公開情報

- [Claude Code Desktop — SSH environments](https://code.claude.com/docs/en/desktop)
- [OpenAI — Moving to the new ChatGPT desktop app](https://help.openai.com/en/articles/20001276/)
- [Cursor CLI](https://prod.cursor.com/docs/cli/overview)
- [OpenCode — Remote SSH support feature request](https://github.com/anomalyco/opencode/issues/33273)
