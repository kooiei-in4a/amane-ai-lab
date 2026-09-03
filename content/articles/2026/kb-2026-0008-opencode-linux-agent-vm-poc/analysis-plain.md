# OpenCodeをLinux VMで使って分かったこと

結論は、**OpenCodeはLinux VM上で動かしてWindowsブラウザから使える。ただし、そのままでは少し面倒なので補助スクリプトが必要だった**、というものだった。

## 何がうまくいったか

WindowsからSSHでLinux VMへ入り、OpenCodeを直接TUIで操作する方法ではなく、Linux側でOpenCode Webを起動し、WindowsブラウザからSSH tunnel経由で使った。

この方法なら、OpenCode Go、日本語入力、コピー&ペースト、コード読解、ファイル編集、build/test、Dockerまで問題なく使えた。ブラウザやSSH tunnelを一度切っても、再接続して同じ作業へ戻れた。

## 何が面倒だったか

OpenCodeにはまだDesktopのNative Remote SSHがない。そのため、他のRemote SSH対応ツールのように「WindowsアプリでSSH先を選ぶだけ」にはならなかった。

さらに実際に試すと、次の差異があった。

- GUIのないLinuxでOpenCode Webがブラウザを開こうとして失敗する
- Git worktreeをWeb UIで期待通りに開けない
- 対話SSHと非対話SSHでPATHが違う
- SSHを切っただけではLinux側のOpenCodeが残ることがある

## どう解決したか

OpenCode専用の小さなhelperを用意した。

- OpenCode用のisolated cloneを作る
- localhost限定でOpenCode Webを起動する
- headless環境の差異を隠す
- Windows launcherからSSH tunnelを張る
- HTTP 200になってからBrowserを開く
- 終了時はOpenCodeを明示的に停止する
- 作業が残っているprojectはcleanupしない

これで普段の操作はかなり単純にできる。

```text
OpenCode用projectを作る
↓
Windows launcherで起動する
↓
Browserで開発する
↓
不要になったらcleanupする
```

## 実用性はどうだったか

PoCではすべての主要項目がPASSした。

- OpenCode Go: PASS
- 日本語: PASS
- 約300文字の貼り付け: PASS
- 実Repositoryの読解: PASS
- ファイル編集: PASS
- build: 0 Warning / 0 Error
- test: 347 passed / 1 skipped / 0 failed
- Docker: PASS
- 再接続: PASS
- Web server再起動後のsession復旧: PASS
- localhost限定公開: PASS
- cleanup: PASS

つまり、**OpenCodeそのものの開発能力に問題があったわけではない。WindowsからLinux Agent VMへつなぐ周辺運用が未成熟だった**。

## 現時点での扱い

OpenCodeはAgent VMへ導入して使える。ただし、Native Remote SSH対応ツールと比べると初期整備は一段多い。

当面はWeb UI + SSH tunnel + wrapperで運用し、OpenCode側にRemote SSHやheadless向けの改善が入ったら回避策を減らしていくのがよい。
