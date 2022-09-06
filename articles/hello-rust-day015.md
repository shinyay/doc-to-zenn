---
title: "100日後にRustをちょっと知ってる人になる: [Day 15]dev container"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 15 のテーマ

Day 14 では **GitHub Codespaces** で Rust 環境を作ることにチャレンジしてみました。
昨日の結果として分かったことは次のことでした。

- 「GitHub」+「Visual Studio Code」+「Ubuntu」が動作するクラウド環境ということ
- Codespaces で提供されるデフォルトのコンテナ環境には Rust のランタイム環境が入っていないということ
- **[dev container](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/introduction-to-dev-containers)** という仕組みを使ってランタイム環境をカスタマイズできるということ

というわけで、今日は **dev container** を使って Rust 環境を作ろうと思います。

## dev container

**dev container** はプロジェクトルートに以下のような構成でファイルを配置して設定を行います。

```shell
.devcontainer/
├── Dockerfile
└── devcontainer.json
```

- **devcontainer.json**: Codespaces の設定ファイル
- **Dockerfile**: dev container の実態

これらの設定ファイルを用意していきます。

### VS Code からの作成

**⌘ + ⇧ + P** で VS Code のコマンドパレットを開きます。
メニューに `Codespaces` と入力し、`Codespaces: Add Development Container Config...` を選択します。

![](https://storage.googleapis.com/zenn-user-upload/1380768154dc-20220906.png)

## Day 15 のまとめ
