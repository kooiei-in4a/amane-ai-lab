# まず結果

専用Linux VMへAIエージェントの実作業を移した判断は、かなり良かったです。

一番大きかったのは、単にWindows PCの負荷が減ったことではありません。**開発環境そのものを、操作しているPCから切り離せたこと**です。

ビルド、テスト、Docker、Git、言語Runtime、AIエージェント用CLIをVM側へ寄せると、Windows PCは「指示と監督をする端末」に近づきます。別のWindows PCから接続しても、エージェントが見るRepositoryやToolchainは同じです。

さらに、VMを作業単位のセキュリティ境界として使えるようになりました。エージェントには開発に必要な権限を与えながら、Local LANなどVM外へのアクセスは別レイヤーで制限できます。

今回の経験から、マルチエージェントを継続的に使うなら、私は **「作業環境ごとにAgent VMを1つ用意し、複数のエージェントからそのVMを使う」** 方式を有力だと考えています。

# Agent VMで解決したかった4つの問題

## 1. ローカルPCの負荷

AIコーディングエージェントは、回答を生成するだけではありません。Repositoryを探索し、依存関係を導入し、ビルドし、テストし、コンテナを起動します。

これを普段使用するPC上で複数並行すると、CPU、Memory、Disk I/Oの影響を受けます。VMへ処理を移すことで、少なくとも開発負荷と普段のPC利用を分離できます。

## 2. 環境差分

ローカル実行では、利用するPCによってPATH、Git設定、Docker、Runtimeなどが変わります。

Agent VMでは、実際の開発環境を一か所へ固定できます。

```text
Agent VM
├─ repositories
├─ worktrees
├─ runtime
├─ artifacts
└─ scratch
```

実際のディレクトリ名そのものより、**どのProjectでも同じ役割のディレクトリを同じ規則で使う**ことが重要でした。

## 3. 権限と安全性

AIエージェントへ強い権限を与えたい一方で、普段使うPC全体を操作対象にはしたくありません。

ここでは権限を細かく減らすより、境界を変えました。

```text
Local PC
   │
   ▼
┌──────────────────┐
│ Linux Agent VM   │
│                  │
│ Git / Docker     │
│ Build / Test     │
│ Agent CLI        │
└──────────────────┘
   │
   ├─ Internet: 必要な通信
   └─ Local LAN: 原則制限
```

VM内部では開発に必要な能力を持たせ、VM外への到達範囲を制限します。

この構成では「誤操作を絶対に起こさない」ことより、**誤操作が起きたときのBlast Radiusを限定する**ことを重視できます。

## 4. 並行作業

マルチエージェントでは、同じRepositoryに複数のAgentが触ること自体が問題になります。

Git worktreeを使って作業単位を分けると、ImplementationとReviewを別のWorktreeへ分離できます。

```text
Shared Git repository
    ├─ Task A / Implementation
    ├─ Task A / Review
    └─ Task B / Implementation
```

DockerもProject単位のnamespaceを使えば、コンテナ、Network、Volumeの衝突を減らせます。

重要なのは複雑なオーケストレーションではなく、**同時に動いたときに互いを壊さない最低限の規約**でした。

# ProxmoxとHyper-Vの両方で試して分かったこと

今回、同じAgent VMの考え方をProxmox VEとMicrosoft Hyper-Vの両方で実装しました。

Hypervisorごとに具体的な実装方法は違います。ネットワーク分離をHypervisor側で強く掛けやすい環境もあれば、Guest OS側のFirewallを中心にした方が扱いやすい環境もあります。SnapshotやCheckpointの操作方法も異なります。

それでも、上位の設計はほとんど変わりませんでした。

```text
Agent VM common design
    │
    ├─ Linux
    ├─ standardized toolchain
    ├─ Git worktree
    ├─ Docker namespace
    ├─ SSH access
    ├─ network boundary
    └─ recovery point
```

この結果から、Agent VMはProxmox固有、Hyper-V固有のテクニックではなく、Hypervisorの上に置ける共通アーキテクチャとして扱えます。

今後文書化するなら、**Common Specification** と **Hypervisor-specific Implementation** を分けるのがよいと考えています。

# Windows側のAIエージェント

今回の構成では、Windows側は主に人間が作業を開始・監督する場所です。

Claude Code DesktopはClaude DesktopのCodeタブから利用でき、公式ドキュメント上もLocal、Remote、SSHを実行環境として選べます。SSHの場合、実処理は接続先のLinuxマシン側で動きます。

OpenAI側は2026年にCodex appがWindowsへ展開され、その後、新しいChatGPT desktop appへChat、Work、Codexが統合されています。現在の記事では **ChatGPT desktop appのCodex** と表記するのが分かりやすいと判断しました。

CursorはIDE内のAgentだけでなくCursor CLIも提供しています。VM側にCLIを置くと、Windows側のUIとLinux側の作業環境を分離する構成にも組み込みやすくなります。

OpenCodeも候補にしましたが、今回欲しかったDesktopからのnative Remote SSHは、公開IssueではFeature Requestの状態です。そのため、無理に回避策を標準構成へ入れず、Remote SSH周辺が成熟してから再評価することにしました。

# 良かった点

## ローカルPCの負荷が減った

Build、Test、DockerなどをVM側へ移せます。特に複数エージェントを同時に動かす場合、普段使うPCと実行負荷を分離できる効果は大きくなります。

## 操作端末に依存しにくい

Repository、Runtime、Docker、Git設定などの実体はVM側にあります。

そのため、「どのWindows PCから操作しているか」は開発環境の主要な差分ではなくなります。

## エージェントへの指示を標準化できる

同じディレクトリ規約、同じGitモデル、同じDockerルールを前提にできます。

Agentごと、PCごとに「Repositoryはどこか」「Dockerは使えるか」といった前置きを繰り返す必要が減りました。

## 強い権限を与えやすい

Local PCへ強い自律操作権限を直接与えるより、専用VMの内部へ閉じ込めた方が判断しやすくなります。

ここで効いたのはLinuxそのものより、**VMが明確な所有境界になっていること**です。

## 戻せる

SnapshotやCheckpointがあると、「壊さないこと」だけに設計を寄せなくて済みます。

エージェントが環境を壊したとき、原因を調査して直すだけでなく、正常なRecovery Pointへ戻す選択肢を持てます。

# クラウドエージェントとの関係

クラウド上で動くAIエージェントには、インフラを用意せずすぐ使える大きな利点があります。

一方で、複数ベンダーのAgentを同じ開発プロセスで組み合わせる場合、自分で管理するAgent VMにも利点があります。

```text
Claude
Codex
Cursor
Other agents
    │
    ▼
Shared Agent VM
    ├─ Git
    ├─ Toolchain
    ├─ Docker
    └─ Runtime
```

エージェントごとに別々の実行環境を持つのではなく、同じRepository、同じテスト環境、同じNetwork Policyを共有できます。

そのため、すべてをVMへ寄せるか、すべてをクラウドへ寄せるかの二択ではありません。短い単発作業はクラウド、複数Agentが継続して触るProjectはAgent VM、といった使い分けも考えられます。

# 積み残し

## VM構築の自動化

現状で最も価値がある改善は、Agent VMを再現可能にすることです。

OS初期設定、Network Policy、Toolchain、AI Agent CLI、Repositoryの初期配置、Acceptance Testまでを自動化できれば、VMを長期間手でメンテナンスする必要が減ります。

## Common Specificationの分離

ProxmoxとHyper-Vでは実装方法が違うため、「Agent VMとして必ず満たす条件」と「Hypervisor別設定」を分離したいと考えています。

## Agent Toolの更新管理

AI Agent関連ツールは更新が速いため、Version確認、Upgrade、Compatibility Test、Rollbackを簡単に回せる仕組みが必要です。

## OpenCodeの再評価

OpenCodeは正式構成へ入れていません。Remote SSH周辺の機能が今回の運用モデルに適合する状態になった時点で再評価します。

# 構築するときの順序

次に同じ環境を作るなら、手順は次の順序にします。

1. Agent VMの責務とSecurity Boundaryを決める
2. Hypervisor上にLinux VMを作る
3. StorageとNetwork Policyを設定する
4. SSHとユーザー権限を設定する
5. Git、Docker、言語Runtimeなど共通Toolchainを入れる
6. AI Agent CLIを導入する
7. Repository / Worktree / Runtime / Artifactの規約を作る
8. Docker resourceのnamespaceルールを決める
9. Windows側のAI Agentから接続してE2E確認する
10. 正常状態のRecovery Pointを作る
11. 構築手順を自動化する

最初から個々のAgent設定に入るより、**VM境界、Network境界、Filesystem、Gitモデル、Dockerモデル、Recoveryモデルを先に決める**方がやり直しが減ります。

# 今回得られた知見

今回の経験を一文にすると、次のようになります。

> AIエージェントを細かく縛るより、十分な権限で自由に動いてよい隔離環境を作り、その環境の外へ出られる範囲を制御する方が、実用的な自律開発と安全性を両立しやすい。

そして、マルチエージェントではその「隔離環境」をAgentごとに作るのではなく、**作業環境ごとにAgent VMを用意し、複数Agentが同じ環境を共有する**方が扱いやすい場面があります。

最終的には、Agent VMを大事に手修復し続けるのではなく、構成から再生成できる **Disposable Agent Runtime** にしていくのが次の目標です。
