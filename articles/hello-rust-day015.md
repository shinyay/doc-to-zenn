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

VS Code にインストールした Codespaces の拡張機能では、**dev container** を作成する機能が提供されています。それを使用して `.devcontainer` を作成していきます。


#### 1. コマンドパレットから dev container 作成メニューの選択

**⌘ + ⇧ + P** で VS Code のコマンドパレットを開きます。
メニューに `Codespaces` と入力し、`Codespaces: Add Development Container Config...` を選択します。

![](https://storage.googleapis.com/zenn-user-upload/1380768154dc-20220906.png)

#### 2. Rust 用の dev container 定義の選択

なんと今まで知らなかったのですけれど、**Rust 用の dev container** 定義が提供されていました！
ゼロベースで作る必要があると思っていたのですけど、これはうれしい。
ありがとう、VS Code 🙏
これを選んでみます。

![](https://storage.googleapis.com/zenn-user-upload/58bb19cdabba-20220906.png)

#### 3. Ubuntu(Debian) ベースイメージのバージョン選択

**buster** がデフォルトと表示されているので、これを選択します。

|Ubutu|Debian|略称|
|-----|------|---|
|18.04 - 19.10|10|buster|
|20.04 - 21.10|11|bullsye|

![](https://storage.googleapis.com/zenn-user-upload/b4e6fd4d3034-20220906.png)

#### 4.dev container 設定

**devcontainer.json** に定義されると思われる、dev container に含める CLI やツールをここで選択できるようです。

![](https://storage.googleapis.com/zenn-user-upload/4b5a41763c2e-20220906.png)

試しに dev container 内でコンテナを使用できるように **Docker in Docker** を選択してみます。

![](https://storage.googleapis.com/zenn-user-upload/ac2adb57cf1e-20220906.png)

dev container に含める **Docker Engine** のバージョンを選択します。

![](https://storage.googleapis.com/zenn-user-upload/da5209acd16e-20220906.png)

![](https://storage.googleapis.com/zenn-user-upload/de12d42af444-20220906.png)

![](https://storage.googleapis.com/zenn-user-upload/7899d5de9cc5-20220906.png)

![](https://storage.googleapis.com/zenn-user-upload/69d2ad717164-20220906.png)

## Day 15 のまとめ
