# 結論

Proxmox VEとMicrosoft Hyper-Vの両方で専用Linux Agent VMを構築した結果、AIコーディングエージェントの実行環境をローカルPCから分離する方式は、実運用上かなり有効でした。

得られた効果は4つです。

1. Build、Test、Dockerなどの負荷を普段使うPCから分離できる
2. Repository、Toolchain、Runtimeを一か所へ固定でき、操作端末への依存を減らせる
3. AI Agentへ十分な権限を与えつつ、影響範囲をVM境界へ限定できる
4. Git worktreeやDocker namespaceを使い、複数Agentの並行作業を整理しやすい

特に重要だったのは、**「AI Agentをどこまで制限するか」ではなく「AI Agentが自由に動いてよい範囲をどこに置くか」**という視点です。

VM内部には開発能力を与え、VM外への到達範囲を制御する。この設計なら、自律性を失わずにBlast Radiusを抑えられます。

また、ProxmoxとHyper-Vで同じ設計が成立したため、これは特定Hypervisorのテクニックというより、Agent execution environmentのアーキテクチャパターンとして扱えます。

マルチエージェントを前提にする場合は、Agentごとに別環境を作るより、**Projectや作業環境ごとにAgent VMを1つ作り、複数Agentで共有する**構成が有効なケースがあります。

次の課題は、Agent VMを手作業で維持する環境から、構成定義から再生成できるDisposable Agent Runtimeへ進化させることです。
