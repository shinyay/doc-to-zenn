---
title: "100日後にRustをちょっと知ってる人になる: [Day 77]REPL ツール: Evcxr"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
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

## Day 77 のまとめ
