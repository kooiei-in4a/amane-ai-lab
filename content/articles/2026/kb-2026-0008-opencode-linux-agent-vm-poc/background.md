# 検討に至った背景

2026年9月、AIコーディングエージェントの実行場所をWindows PCからLinux VMへ分離する構成を、OpenCodeでも実現できるかを検証した。

前提となるAgent VMの考え方は、先に公開した [KB-2026-0007: AIコーディングエージェントをLinux VMへ分離して分かったこと](https://kooiei-in4a.github.io/amane-ai-lab/articles/2026/kb-2026-0007-ai-agent-linux-vm-environment/) で整理している。Windowsは指示・監督のUIに寄せ、Git、Docker、build/test、AIエージェント本体はLinux VM側に置く構成である。

OpenCodeでも理想はWindows側のDesktopからRemote SSHでLinux VMを直接開くことだった。しかし、2026-09-03時点でOpenCode DesktopのRemote SSH要望 [#33273](https://github.com/anomalyco/opencode/issues/33273) はOpenのままだった。また、SSH上でTUIを直接操作する方式にはclipboard問題 [#46377](https://github.com/anomalyco/opencode/issues/46377) が残っている。

そこで、OpenCode自体はLinux VM上で動かし、Web UIだけをWindowsブラウザへ出す構成を試した。

```text
Windows Browser
    ↓
127.0.0.1:4096
    ↓ SSH port forwarding
Linux Agent VM
    ↓
OpenCode Web / OpenCode Go
    ↓
Git / build / test / Docker
```

PoCの判定対象は「インストールできるか」ではなく、実際の開発作業に必要な一連の操作が成立するかとした。OpenCode Go認証、日本語入力、clipboard、実Repository読解、ファイル編集、.NET build/test、Docker、再接続、セッション復旧、localhost限定公開、cleanupまで段階的に確認した。

この記事では実機環境のホスト名、IPアドレス、ユーザー名、ローカルパスは公開しない。コマンド例も公開可能な一般形へ置き換えている。
