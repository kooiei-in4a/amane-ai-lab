# 合成結果の要約（わかりやすい説明）

OpenCodeはLinux VM上で動かし、WindowsのブラウザからSSH経由で使えることを確認できた。

日本語、コピー&ペースト、コードの読取り、ファイル編集、build/test、Docker、再接続まで問題なく動いたので、開発機能としては実用できる。

ただし、OpenCodeにはまだWindows DesktopからLinuxへ直接Remote SSHする機能がなく、headless LinuxやGit worktree、SSH切断時の終了処理にも細かい問題があった。

そのため当面は、OpenCode専用のcloneを作り、Linux側でWeb UIをlocalhostだけに起動し、WindowsからSSH tunnelで接続する。起動・停止・cleanupは補助スクリプトでまとめる。

結論は、**OpenCodeはAgent VMで使えるが、現時点ではwrapperを用意して使うのが現実的**というものになった。
