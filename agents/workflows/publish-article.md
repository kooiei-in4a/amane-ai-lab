# workflow: publish-article

1. status を `published` にするのは人間承認後とする
2. validate / sensitive-data check が成功していること
3. 生成差分がないこと
4. merge は人間が行う
5. エージェントは merge / Pages本番設定変更を行わない
