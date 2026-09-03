# 合成結果の要約

## 結論

OpenCodeはLinux Agent VM上で実行し、Windows BrowserからSSH port forwarding経由で操作する構成なら実用できた。

OpenCode 1.18.27 + OpenCode Goで、日本語、clipboard、実Repository読解、ファイル編集、.NET build/test、Docker、再接続、Web server再起動後のsession復旧、Security確認、cleanupまでPASSした。

## 問題点

2026-09-03時点では、Agent VM運用にそのまま使うには次の不足がある。

- OpenCode DesktopのNative Remote SSHが未実装
- SSH TUIのclipboard問題が残る
- headless Linuxで `opencode web` のブラウザ自動起動を抑止しにくい
- manual Git worktreeをWeb UIで扱いにくい
- 非対話SSHのPATHが対話shellと異なる
- SSH切断だけではremote OpenCodeが残ることがある

## 対応方法

当面の運用は次で安定した。

1. OpenCode用にはordinary isolated cloneを使う
2. Linux側は `127.0.0.1` だけでOpenCode Webを起動する
3. WindowsからSSH tunnelでlocalhostへ接続する
4. headless差異とPATH差異はLinux helperで吸収する
5. Windows launcherはHTTP 200を待ってBrowserを開く
6. 終了時は別SSH commandでOpenCodeを明示停止する
7. cleanupはdirty / additional commit / unexpected remoteがあれば拒否する

## PoCで確認した結果

- OpenCode Go認証・日本語: PASS
- 約300文字のclipboard貼り付け: PASS
- read-only Repository調査: PASS
- isolated write: PASS
- build: 0 Warning / 0 Error
- test: 347 passed / 1 skipped / 0 failed
- Docker: PASS
- Browser / SSH tunnel再接続: PASS
- Web server再起動後のsession復旧: PASS
- localhost限定listen: PASS
- credential permission 0600: PASS
- cleanup後のport / process / artifact残存なし

## 運用判断

**採用可能。ただしwrapper前提。**

OpenCode自体の開発機能はAgent VM上で十分使えた。一方、Native Remote SSH対応クライアントと比べると接続・起動・終了の運用を自前で補う必要がある。

当面はWeb UI + SSH tunnel方式を使い、Remote SSH、`--no-open`、Git worktree UXなどの上流改善が入れば補助レイヤーを順次削除する。
