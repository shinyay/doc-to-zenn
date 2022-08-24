---
title: "100日後にRustをちょっと知ってる人になる: [Day 2] 開発環境を用意する"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---

## Day 2 のテーマ

Day 1 では、Rust がどのような言語なのかをかなり粗々に概要を調べてみました。
しかし、まだコードは全然記述していません。そもそも開発環境さえ準備をしていません。
そこで Day 2 では、Rust をプログラムできる開発環境を整えようと思います。

次のような点を調べながら開発環境を準備してみます。

- **ランタイム**をどのように導入するのか？
- **ビルド**や**パッケージ管理**の仕組みは一体どのようなものなのか？
- 最適な**コードエディタ**は一体何なのか？

## ランタイムのインストール

どのようなプログラム言語も動かすためには概ね実行形態を生成するための **コンパイラ**や動作させるために必要な標準ライブラリなどを含む**ランタイム**が必要になります。
Java で言うところの、`JDK` や `JRE` のようなもののことです。これをインストールする必要たあります。

### rustup

ここから始める Rust ということで、[Rust の公式ドキュメント](https://www.rust-lang.org/)を見てみます。
**Get Started** から始めようとすると、まず最初に Rust のインストールが求められます。ここで推奨されているインストールツールが、**rustup** です。

- [rustup](https://rustup.rs/)

以下のコマンドを実行し rustup を取得してインストールが実行されます。

```shell
curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh
```

完了すると、次のメッセージが表示されます。

```shell
Rust is installed now. Great!
```

#### rustup サブコマンド

|コマンド|説明|
|-------|---|
|show|Show the active and installed toolchains or profiles|
|update|Update Rust toolchains and rustup|
|check|Check for updates to Rust toolchains and rustup|
|default|Set the default toolchain|
|toolchain|Modify or query the installed toolchains|
|target|Modify a toolchain's supported targets|
|component|Modify a toolchain's installed components|
|override|Modify directory toolchain overrides|
|run|Run a command with an environment configured for a given toolchain|
|which|Display which binary will be run for a given command|
|doc|Open the documentation for the current toolchain|
|man|View the man page for a given command|
|self|Modify the rustup installation|
|set|Alter rustup settings|
|completions|Generate tab-completion scripts for your shell|
|help|Prints this message or the help of the given subcommand(s)|

