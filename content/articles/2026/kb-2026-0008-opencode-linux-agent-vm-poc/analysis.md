# OpenCodeをAgent VMで使うPoCの結果

## 結論

OpenCodeは、Linux Agent VM上で実行し、WindowsからSSH経由で操作する構成に**採用可能**だった。

ただし、2026-09-03時点ではNative Remote SSHがないため、Windows側のOpenCode DesktopからLinux VMを直接開く構成ではない。実用になったのは、Linux VM上のOpenCode Webを `127.0.0.1` だけで待ち受け、WindowsからSSH port forwardingで接続する方式だった。

この構成で、OpenCode Go、日本語、clipboard、実Repository読解、ファイル編集、build/test、Docker、Browser/tunnel再接続、Web server再起動後のsession復旧、Security確認まで通った。

一方、素のOpenCodeをそのままAgent VMへ載せるだけでは運用上の穴が残った。正式運用にはhelper / launcherで差異を吸収する必要がある。

## 検証した構成

```text
Windows Browser
      ↓
127.0.0.1:4096
      ↓
SSH port forwarding
      ↓
Linux Agent VM
      ├─ OpenCode 1.18.27
      ├─ OpenCode Go
      ├─ Git
      ├─ .NET build / test
      └─ Docker
```

Windows PCはUIと指示・監督に寄せ、Repository、shell、Docker、認証、AIエージェントの実行状態はLinux VM側に置いた。

## 問題点

### Native Remote SSHはまだ使えない

OpenCode DesktopのRemote SSH要望 [#33273](https://github.com/anomalyco/opencode/issues/33273) は2026-09-03時点でOpenだった。

そのため、Claude Code Desktop等で期待する「WindowsアプリからSSH先を開く」体験はまだ前提にできない。

### SSH上のTUIを直接操作する方式には既知問題がある

SSH上でOpenCodeを直接起動する方式は可能だが、clipboardが機能しない報告 [#46377](https://github.com/anomalyco/opencode/issues/46377) がOpenだった。

今回の目的は日本語や長文を含む日常開発なので、TUI over SSHを主経路にせずBrowserへ逃がした。

### headless Linuxと `opencode web` の相性

GUIのないVMで `opencode web` を起動すると、環境によってはブラウザを開くための `xdg-open` がなく起動できなかった。ブラウザ自動起動を止める `--no-open` 相当の要望 [#43636](https://github.com/anomalyco/opencode/issues/43636) はOpenである。

### Git worktreeは今回のWeb UIで扱いにくかった

Agent VMの既存運用ではGit worktreeを使って並列作業を分離している。しかし今回のPoCではmanual worktreeをOpenCode Webのprojectとして期待通りに開けなかった。

Web UIのproject navigation / Git worktree UX改善要望 [#24002](https://github.com/anomalyco/opencode/issues/24002) はClosed / not plannedであり、当面これを前提にした方がよい。

### 非対話SSHのPATHは対話SSHと違う

Windows launcherからSSH remote commandを起動したところ、対話SSHでは見えていたOpenCode実体を見つけられなかった。原因は非対話SSHのPATHにユーザーlocal binが含まれないことだった。

### SSH切断だけではremote process cleanupにならない

Windows側でSSHを終了してもOpenCode WebがLinux側に残るケースを確認した。signal trapやSSH session監視だけでは安定しなかった。

## 対応方法

### Web UI + SSH tunnelを正式経路にする

Linux側ではlocalhostだけでOpenCode Webを起動する。

```bash
opencode web --hostname 127.0.0.1 --port 4096
```

Windows側ではloopback同士をSSH port forwardingする。

```text
ssh -N -L 127.0.0.1:4096:127.0.0.1:4096 <agent-vm>
```

これでLANへOpenCode Webを直接公開せず、Windows Browserから利用できる。

### headless差異はprocess-local shimで吸収する

`xdg-open` のためだけにGUI関連packageをVMへ追加するのではなく、OpenCode起動時のPATHにだけno-op shimを差し込む。

これはOpenCode側に `--no-open` が入れば削除できる暫定策である。

### OpenCode用projectはordinary cloneにする

manual worktreeに固執せず、OpenCode用のisolated cloneを別に作る。PoCでは通常cloneへ切り替えるとproject選択、read/write、build/testがすべて通った。

安全側に倒すため、PoC後の運用helperでは初期状態でGit remoteを外し、AIが誤ってpushできる経路を持たせない構成にした。

### 非対話SSHでは実体を明示解決する

helper内部でinteractive shellのPATHを期待しない。OpenCode実体を明示的に解決し、起動時PATHも必要最小限に固定する。

### lifecycleを明示管理する

Windows launcherは次の順で処理する。

```text
preflight stale cleanup
↓
SSH tunnel + remote OpenCode Web起動
↓
HTTP 200まで待機
↓
Windows Browser起動
↓
作業
↓
remote stop helperで明示停止
↓
SSH終了
```

Windows側が異常終了した場合も、次回起動時のpreflight cleanupで前回のstale processを回収できる。

### cleanupはfail-closedにする

OpenCode用projectを消すhelperは、次の場合に削除を拒否する。

- uncommitted changeがある
- base以降のcommitがある
- 想定外のGit remoteがある
- OpenCode processがまだprojectを利用している

「AI用の一時cloneだから消してよい」と推測せず、作業消失を防ぐ。

## 実機PoCのAcceptance結果

| Phase | 内容 | 結果 |
|---|---|---|
| 1 | OpenCode CLI導入 | PASS |
| 2 | OpenCode Go認証、日本語応答 | PASS |
| 3 | localhost限定Web起動 | PASS |
| 4 | Windows Browser + SSH tunnel | PASS |
| 5 | 実Repository read-only調査 | PASS |
| 6 | ファイル編集、build、test | PASS |
| 7 | Docker / Toolchain | PASS |
| 8 | Session / Recovery | PASS |
| 9 | Security | PASS |
| 10 | Cleanup | PASS |

### build / test

公開Repositoryを使ったisolated write testでは、PoC専用ファイル1件だけを追加した状態でbuild/testを実施した。

- build: 0 Warning / 0 Error
- test: 347 passed / 1 skipped / 0 failed
- HEAD / branchは変更なし
- commit / pushなし

新規cloneではrestore済みassetsがなかったため、最初の `--no-restore` は失敗した。既存projectで宣言済みの依存をrestoreした後は正常に通った。

### Docker

Docker Engine 29.7.2 / Docker Compose v5.5.0で、一時コンテナを `--rm` 付きで実行した。

- exit code 0
- 想定文字列を出力
- privilegedなし
- host networkなし
- host mountなし
- volume / networkの明示作成なし
- 終了後のcontainer残存なし

### Session / Recovery

次を実際に切断・再起動した。

- Browser tab
- SSH tunnel
- OpenCode Web server

再接続後に同じprojectへ戻れ、会話sessionも復旧した。Windows側が一時的に消えても、Linux VM側のRepository状態は維持された。

### Security

- OpenCode Webは `127.0.0.1` のみにlisten
- LAN直接公開なし
- OpenCode Go credentialはowner-only permission（0600）
- Repository内のcredential様文字列scanはPASS
- PoC isolated cloneはGit remoteなし
- cleanup後にport / process / PoC artifact残存なし

## 試して分かった細かいこと

### `Connection refused` が数回出ても、必ずしも失敗ではない

SSH tunnelはOpenCode Webより先にlistenする。このためlauncherがHTTP確認を始めた瞬間は、remote側4096がまだ起動しておらずSSHの `connect failed: Connection refused` が出ることがある。

最終的にHTTP 200を確認してからBrowserを開けば問題ない。launcher側は「TCP portが開いたか」ではなく「HTTP 200が返ったか」をready条件にした方がよい。

### `OPENCODE_SERVER_PASSWORD is not set` 警告の扱い

localhost-onlyでも警告は表示された。今回の構成ではOpenCodeを `0.0.0.0` へbindせず、SSH tunnelからしか到達させないことで外部公開を避けた。

今後LANや別hostへ直接公開する設計に変えるなら、このPoCのSecurity前提は成立しないため、認証を含めて再設計が必要になる。

### API keyのTUI貼り付けで詰まった

SSH TUIへAPI keyを貼れなかったため、先にWeb UIを成立させ、Windows BrowserからOpenCode Goを接続した。この経路ならWindows clipboardをそのまま使えた。

### 約300文字の日本語clipboardは問題なかった

Web UI経由では長めの日本語貼り付けが成功した。TUIのSSH clipboard問題を避けるという狙いは達成できた。

### direct SSHの `Ctrl+C` をremote cleanupと考えない

remote OpenCodeが残ることがあったため、SSH transportの終了とAgent process lifecycleを分けて考える必要がある。正式運用では明示stopを採用した。

## 運用判断

今回の結論は「OpenCodeはAgent VMで使えない」ではない。

**機能的には十分使える。ただしNative Remote SSHがない現状では、Agent VM運用を成立させるための薄い運用レイヤーが必要である。**

wrapper完成後の日常操作は、次の3つ程度まで落とせる。

```text
project作成
↓
Windows launcherで起動
↓
不要になったらcleanup
```

一方、初期構築だけを見るとNative Remote SSH対応のクライアントより明らかに煩雑だった。OpenCode側でRemote SSH、`--no-open`、worktree UXが改善されれば、この補助レイヤーは順次削除したい。

## 関連情報

- [KB-2026-0007: AIコーディングエージェントをLinux VMへ分離して分かったこと](https://kooiei-in4a.github.io/amane-ai-lab/articles/2026/kb-2026-0007-ai-agent-linux-vm-environment/)
- [OpenCode Web documentation](https://opencode.ai/docs/web/)
- [OpenCode Go documentation](https://opencode.ai/docs/go/)
- [Remote SSH support for OpenCode desktop #33273](https://github.com/anomalyco/opencode/issues/33273)
- [Flag to start web server without launching browser #43636](https://github.com/anomalyco/opencode/issues/43636)
- [Clipboard copying does not work when OpenCode is running over SSH #46377](https://github.com/anomalyco/opencode/issues/46377)
- [Web UI project navigation / Git worktree support #24002](https://github.com/anomalyco/opencode/issues/24002)
