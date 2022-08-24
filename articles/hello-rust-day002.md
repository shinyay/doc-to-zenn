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

以下のコマンドを実行して rustup を取得してインストールが実行されます。

```shell
curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh
```

完了すると、次のメッセージが表示されます。

```shell
Rust is installed now. Great!
```

インストールが完了したら、以下のコマンドを実行してバージョンを確認してみましょう。

```shell
rustc --version
rustc 1.63.0 (4b91a6ea7 2022-08-08)
```

#### rustup サブコマンド

|コマンド|説明|
|-------|---|
|show|インストールされているツールチェインやプロファイルを表示|
|update|Rustツールチェーンとrustupを更新|
|check|Rustツールチェーンとrustupの更新を確認|
|default|デフォルトのツールチェーンを設定|
|toolchain|インストールされたツールチェーンを変更または問い合わせ|
|target|ツールチェインのサポートされるターゲットを変更|
|component|ツールチェインのインストールされたコンポーネントを変更|
|override|ディレクトリツールチェーンオーバーライドを変更|
|run|えられたツールチェイン用に設定された環境でコマンドを実行|
|which|与えられたコマンドに対してどのバイナリが実行されるかを表示|
|doc|現在のツールチェインのドキュメントを表示|
|man|与えられたコマンドのマニュアルページを表示|
|self|rustupのインストールを修正|
|set|rustupの設定を変更|
|completions|シェル用のタブ補完スクリプトを生成|
|help|ヘルプを表示|

#### Rust のアップデート

`rustup` の以下のサブコマンドを実行することでアップデートが可能です。

```shell
rustup update
```

#### Rust のアンインストール

`rustup` の以下のサブコマンドを実行することでアンインストールが可能です。

```shell
rustup self uninstall
```

### 参考

- [The rustup book](https://rust-lang.github.io/rustup/index.html)

## Rust のビルドやパッケージ管理の仕組み

Java であれば **Maven** や **Gradle**, Python であれば **pip**, また Node であれば **npm** のように各プログラム言語にはその言語で使用するパッケージを管理するためのツールが提供されています。Rust では、**Cargo** というパッケージ管理ツールを使用します。

### Cargo

この **Cargo** は `rustup` で Rust をインストールした際に同時に導入されています。

以下のコマンドで確認してみてください。

```shell
cargo --version
cargo 1.63.0 (fd9c4297c 2022-07-01)
```

この `cargo` を使って Rust プログラムのビルドやコードが依存しているライブラリにダウンロードなどを実施することが可能です。

#### cargo サブコマンド

|コマンド|説明|
|-------|---|
|build|Compile the current package|
|check|Analyze the current package and report errors, but don't build object files|
|clean|Remove the target directory|
|doc|Build this package's and its dependencies' documentation|
|new|Create a new cargo package|
|init|Create a new cargo package in an existing directory|
|add|Add dependencies to a manifest file|
|run| Run a binary or example of the local package|
|test|Run the tests|
|bench|Run the benchmarks|
|update|Update dependencies listed in Cargo.lock|
|search|Search registry for crates|
|publish|Package and upload this package to the registry|
|install|Install a Rust binary. Default location is $HOME/.cargo/bin|
|uninstall|Uninstall a Rust binary|