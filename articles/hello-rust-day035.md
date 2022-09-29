---
title: "100日後にRustをちょっと知ってる人になる: [Day 35]はじめての Web サーバ"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 35 のテーマ

[Day 34](https://zenn.dev/shinyay/articles/hello-rust-day034) では、リリースされたばかりの Rust 1.64.0 の特徴についてみてみました。その特徴の中でも、新しく安定化された **IntoFuture** による非同期処理が一番注目する内容だったかなと思います。
今まで Rust での非同期処理をあまり見てきてはいないので、改めて Rust による非同期処理について学んでいきたいと思います。言語仕様自体ももちろん見ていきたいと思っていますが、まずは動くものから見たいかなと思います。そこで、非同期処理といえば大体な人がイメージするのは Web サーバだと思います。（偏見ならすみません）

今日は、Rust で簡単な Web サーバを作っていこうと思います。

## はじめての Web サーバ

そもそもですが、Web サーバがまず最初に行わなければならないことは何でしょう。言うまでもないですよね、**TCP** 接続のリッスンです。Web サーバはクライアントからのリクエストを受け付け、サーバ上で処理をし、そしてクライアントにレスポンスを返します。この接続をやり取りするために TCP プロトコルと HTTP プロトコルが使われています。

Rust では、ネットワーク接続するための機能が、標準ライブラリとして `std::net` というモジュールで提供されています。

- [std::net](https://doc.rust-lang.org/std/net/)

この `std::net` が提供するものの中に、文字通り TCP をリッスンするための機能を実装した Struct `TcpListner` があります。

- [TcpListner](https://doc.rust-lang.org/std/net/struct.TcpListener.html)

この TcpListner により、TCP ソケットサーバとして接続を待機します。
まず、TcpListener をソケットアドレスにバインドして作成した後に、TCP 接続の着信を待ち受けます。この接続は、`accept` を呼び出すか、`incoming` が返すイテレータを反復することで受け入れることができます。そして、この作成した TCP ソケットは、値が削除されるとクローズされます。

```rust
let listner = TcpListener::bind("127.0.0.1:8080").unwrap();
```

## Day 35 のまとめ
