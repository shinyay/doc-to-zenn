---
title: "100日後にRustをちょっと知ってる人になる: [Day 35]はじめての Web サーバ"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
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

以下のように、`TcpListener` を用いて、ローカルホスト、8080 ポートにバインドを行います。

```rust
let listner = TcpListener::bind("127.0.0.1:8080").unwrap();
```

ところで、この `bind` メソッドは `Result<T, Error>` を返しています。つまり、エラーが発生することがあることを表しています。ここでのエラーは、ほとんどの場合は OS の仕様や機能に依存するものになります。たとえば、ポート `80` にで接続する場合、管理者権限が必要になるため（管理者以外の場合は、1024 ポート以上しかリッスンできません）接続は通常うまく行きません。

```rust
pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<TcpListener> {
    super::each_addr(addr, net_imp::TcpListener::bind).map(TcpListener)
}
```

一方でここでのエラーを意思する必要はありません。`unwrap` を使うことで、エラーが発生した場合には当該プログラムを停止します。

![](https://storage.googleapis.com/zenn-user-upload/2d3668c34499-20220929.png)

次に、 `for` ブロックでは、`incoming` メソッドにより接続ストリームを与えるイテレータを生成します。

```rust
for stream in listner.incoming() { }
```

この例では、入力ストリームを得た時点で標準出力で `接続確立!` と出力しています。

:::details ここまでのソースコード

```rust
use std::net::TcpListener;

fn main() {
    let listner = TcpListener::bind("127.0.0.1:8080").unwrap();

    for stream in listner.incoming() {
        let stream = stream.unwrap();
        println!("接続確立!");
    }
}
```

:::

ここまでの サーバ処理でリクエストに対するレスポンス処理はやってないのですが、土台になる部分だけだと１分もあれば作れてしまいました。

## Day 35 のまとめ

非同期処理ということでサーバ作成について見てみようとおもったのですが、想像を遥かに上回る簡単さで作れそうだということが分かりました。
一方で非同期に特化しているクレートとして [tokio](https://tokio.rs/) というものもあります。この辺りのクレートなどを活用した場合に Web サーバとしてどんな実装で実現できるかな、という事がきになりました。
非同期処理は最近のアプリケーションプログラミングでは必須といっても過言ではない要素だと思います。このあとしばらくは、Rust での非同期処理について注目したいかな、って思いました。
