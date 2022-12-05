---
title: "100日後にRustをちょっと知ってる人になる: [Day 77]REPL ツール: Evcxr"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 77 のテーマ

[Day 76](https://zenn.dev/shinyay/articles/hello-rust-day076) から Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** を読み始めました。書籍の中でサンプルコードがたくさん出てくるのでとても便利なのですが、１つ１つソースコードを起こしてコンパイルして実行するのは面倒ですよね。
こんな時に、Java あれば **JShell**、Kotlin であれば **ki shell** のように **REPL** ツールがあると便利ですよね。というわけで、Rust にも REPL ツールがないものかと探してみたのでした。

## Evcxr

何か欲しい物があるときは、とりあえず [crate.io](https://crates.io/) で検索してみることにしています。というわけで、REPL を検索してみました。

- [](https://crates.io/search?q=repl)

![](https://storage.googleapis.com/zenn-user-upload/ddd371ce94f3-20221205.png)

いろいろとREPL なものが見つかったことに驚いたのですが、その中で最もダウンロード数の多かった **evcxr_repl** を使ってみることにします。

![](https://storage.googleapis.com/zenn-user-upload/745412eda96a-20221205.png)

- [Evcxr Rust REPL](https://crates.io/crates/evcxr_repl)

この **evcxr** は最近 Rust のフォーカスし始めている Google が作成している REPL ツールでした。

- [google/evcxr](https://github.com/google/evcxr)

それでは、この REPL ツール **evcxr** をインストールして使ってみたいと思います。

## インストール

**evcxr** のインストール方法は 2 種類あります。

- ✅ ビルド済みバイナリの取得
  - [ここ](https://github.com/google/evcxr/releases)からビルド済みイメージをダウンロードできます
- ✅ 自分でビルド
  - 自分でビルドと言っても難しいわけではなく、`cargo` コマンドを使ってビルドを行いバイナリをインストールします

ここでは、`cargo` によるインストールをしてみたいと思います。

次のコマンドを実行します:

```shell
cargo install evcxr_repl
```

終了すると、`$HOME/.cargo/bin/` にインストール出来ていることが確認できます。

## evcxr の使用

```shell
evcxr -h
```

現時点で最新版の `0.14.1` の `evcxr` がインストールできています。

```shell
evcxr 0.14.1

USAGE:
    evcxr [FLAGS] [OPTIONS]

FLAGS:
        --disable-readline
    -h, --help                Prints help information
        --ide-mode
    -V, --version             Prints version information

OPTIONS:
        --edit-mode <edit-mode>     [default: emacs]  [possible values: vi, emacs]
        --opt <opt>                Optimization level (0, 1 or 2) [default: ]
```

では、動かしてみます。

```shell
$ evcxr
Welcome to evcxr. For help, type :help
>>
```

プロンプトが出てくるので、ここに Rust のコードを打ち込んでいきます。

```rust
>> let message = "Hello EVCXR".to_string();
>> message
"Hello EVCXR"
>> println!("Message:{}", message);
Message:Hello EVCXR
>>
```

実行できていますね、インタラクティブに Rust のコードの動作確認ができます。

終了する時は、`:quit` です。

```shell
>> :quit
```

## Day 77 のまとめ

今日は REPL ツールの **evcxr** について見てきました。しかし、使っている間ずっと思っていたのが、この **evcxr** というコマンドが何を表しているか分からないので覚えられないなと思っていたのです。しかし、ようやく気づきました。

この **evcxr** が Rust の評価コンテキストを使用して作られているということだったので、**ev**aluation **c**onte**x**t for **r**ust ということなんだろうな、と分かりました。

これでコマンド名を覚えられるはず！と思っています。

いずれにしても、コマンド名が覚えられるかおいておいて Rust で REPL が使えるのはちょっとしたコードを試す時にとても便利なので、ぜひ使ってみてはいかがでしょうか。
