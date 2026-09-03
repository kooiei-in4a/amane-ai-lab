# ChatGPT回答

## 結論

OpenCodeは、2026-09-03時点ではWindows DesktopからLinux Agent VMへNative Remote SSHする用途には向いていない。一方で、**Linux VM上でOpenCode Webをlocalhost限定で起動し、WindowsからSSH port forwarding経由でブラウザ接続する構成なら、実開発に必要な機能は一通り成立した。**

PoCではOpenCode 1.18.27を使用し、OpenCode Go認証、日本語、clipboard、実Repository読解、ファイル編集、.NET build/test、Docker、再接続、セッション復旧、Security確認、cleanupまでPASSした。

ただし、素のOpenCodeをそのまま使うだけでは運用が煩雑だった。headless環境でのブラウザ自動起動、manual Git worktreeの扱い、非対話SSHのPATH差異、SSH切断時のWebプロセス終了などをwrapperで吸収する必要があった。

## 推奨構成

```text
Windows Browser
      ↓
localhost
      ↓
SSH port forwarding
      ↓
Linux Agent VM
      ├─ OpenCode Web
      ├─ OpenCode Go
      ├─ Git
      ├─ build / test
      └─ Docker
```

Linux側は次のようにlocalhostだけでWeb UIを待ち受ける。

```bash
opencode web --hostname 127.0.0.1 --port 4096
```

Windows側はSSH tunnelを作る。

```text
ssh -N -L 127.0.0.1:4096:127.0.0.1:4096 <agent-vm>
```

ブラウザでは `http://127.0.0.1:4096/` を開く。

## 公開情報として確認したOpenCode側の状況

2026-09-03にOpenCodeの公開GitHubを再確認した。

- OpenCode DesktopのRemote SSH要望 [#33273](https://github.com/anomalyco/opencode/issues/33273) はOpen。
- `opencode web` でブラウザ自動起動を抑止する `--no-open` 相当の要望 [#43636](https://github.com/anomalyco/opencode/issues/43636) はOpen。
- SSH上のOpenCode TUIでclipboardが機能しない報告 [#46377](https://github.com/anomalyco/opencode/issues/46377) はOpen。
- Web UIのproject navigation / Git worktree UX改善要望 [#24002](https://github.com/anomalyco/opencode/issues/24002) はClosed / not planned。今回の実機PoCでもmanual Git worktreeをWeb UIから期待通りに開けず、通常cloneへ切り替えると成功した。

## PoC結果

| 項目 | 結果 |
|---|---|
| Linux CLI導入 | PASS |
| OpenCode Go認証 | PASS |
| 日本語応答 | PASS |
| Windows Browser + SSH tunnel | PASS |
| 約300文字のclipboard貼り付け | PASS |
| 実Repository read-only調査 | PASS |
| isolated環境でのファイル編集 | PASS |
| .NET build | PASS、0 Warning / 0 Error |
| .NET test | PASS、347 passed / 1 skipped / 0 failed |
| Docker | PASS |
| Browser / tunnel再接続 | PASS |
| Web server再起動後のsession復旧 | PASS |
| localhost限定listen | PASS |
| credential permission | PASS、0600 |
| push経路なしの隔離 | PASS |
| cleanup | PASS |

Docker検証ではDocker Engine 29.7.2、Docker Compose v5.5.0で一時コンテナを `--rm` 実行し、終了後の残存がないことを確認した。

## 問題点と対応

### 1. Native Remote SSHがない

Windows版OpenCode DesktopをRemote SSHクライアントとして使う構成は採れなかった。

**対応:** SSHを画面転送ではなく安全なtransportとして使い、Windows BrowserからOpenCode Webを操作する。

### 2. SSH TUIのclipboard問題を避けたい

SSH上でOpenCode TUIを直接操作する方式には公開Issueがある。

**対応:** Browser UIを使う。今回のPoCでは日本語入力と約300文字の貼り付けが正常に動いた。

### 3. headless Linuxで `opencode web` がブラウザを開こうとする

GUIのないLinux VMではブラウザ起動処理が不要で、環境によっては `xdg-open` 不在で起動に失敗した。ブラウザ自動起動を止める公式flagはまだ要望段階だった。

**対応:** OpenCodeプロセスにだけ見える軽量な `xdg-open` shimを用意し、OS全体へGUI関連packageを追加しない。

### 4. manual Git worktreeをWeb UIで開けなかった

Agent VMの通常運用ではGit worktreeが便利だが、今回のOpenCode Webでは手動作成したworktreeを期待通りに開けなかった。

**対応:** OpenCode用には普通のisolated cloneを作る。PoCではcloneへ切り替えた後、read/write/build/testが正常に動いた。

### 5. 非対話SSHではPATHが違う

対話SSHでは見えていたOpenCodeが、Windows launcherからのremote commandでは見つからなかった。非対話SSHのPATHにユーザーlocal binが含まれていなかったためだった。

**対応:** launcher/helper内部ではOpenCode実体を絶対位置で解決し、interactive shellのPATHへ依存しない。

### 6. SSH切断だけではOpenCode Webが終了しない

Windows側でSSHを切った後もLinux側にOpenCode Webが残るケースを確認した。HUP/TERM trapやSSH session監視だけでは安定しなかった。

**対応:** lifecycleを明示管理する。Windows launcherは起動前にstale processをcleanupし、通常終了時には別SSH commandで対象project/portのOpenCodeを明示停止する。次回起動時にもpreflight cleanupを行う。

## 実運用用に作った役割

最終的には次の役割をhelperへ分離した。

- `opencode-agent-project`: 最新baseからOpenCode専用isolated cloneを作る。初期状態ではremoteを外し、誤push経路を持たせない。
- `opencode-agent-web`: 対象projectでlocalhost限定のOpenCode Webを起動する。headless差異と非対話SSH PATHを吸収する。
- `opencode-agent-stop`: 対象projectとportに一致するOpenCodeだけを明示停止する。
- `opencode-agent-cleanup`: dirty、追加commit、想定外remoteがあるprojectは削除を拒否する。
- Windows launcher: preflight cleanup → SSH tunnel → OpenCode起動 → HTTP 200待機 → Browser起動 → 明示停止、をまとめる。

## 実際に試して分かった細かいこと

- 新規cloneで `dotnet build --no-restore` を先に実行するとassets不足で失敗した。既存projectで宣言済みのNuGet依存をrestoreした後はbuild/testとも成功した。
- OpenCodeは依存取得が必要な場面で人間へ許可を求めて停止できた。PoCとしては望ましい挙動だった。
- SSH tunnelはOpenCode Webより先にlistenするため、起動直後に `connect failed: Connection refused` が数回見えることがある。HTTP 200を待ってからBrowserを開けば問題なかった。
- `OPENCODE_SERVER_PASSWORD is not set` という警告は出るが、PoCでは `127.0.0.1` のみにbindしSSH tunnelからだけ接続したため、LANへ直接公開しなかった。
- Browserを閉じてもLinux側のRepository状態は保持される。SSH tunnel再接続とWeb server再起動の両方で同じproject/sessionへ戻れた。
- 認証情報はowner-only permissionで保持し、Repository内にcredential様文字列がないことを確認した。

## 判断

**技術的には採用可能。運用面ではwrapper前提。**

Native Remote SSHを持つAI開発クライアントと比べると、OpenCodeはAgent VMで使うための初期整備が一段多い。ただしwrapperで差異を隠せば、日常操作は「project作成」「Windows launcher起動」「不要時cleanup」程度まで単純化できる。

OpenCode側でRemote SSH、`--no-open`、worktree UXが改善されたら、現在のwrapperを順に削っていくのがよい。

## 参照

- [OpenCode Web documentation](https://opencode.ai/docs/web/)
- [OpenCode Go documentation](https://opencode.ai/docs/go/)
- [Remote SSH support for OpenCode desktop #33273](https://github.com/anomalyco/opencode/issues/33273)
- [Flag to start web server without launching browser #43636](https://github.com/anomalyco/opencode/issues/43636)
- [Clipboard copying does not work when OpenCode is running over SSH #46377](https://github.com/anomalyco/opencode/issues/46377)
- [Web UI project navigation / Git worktree support #24002](https://github.com/anomalyco/opencode/issues/24002)
