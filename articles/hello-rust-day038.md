---
title: "100日後にRustをちょっと知ってる人になる: [Day 38]非同期処理クレートと Web フレームワーク"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 38 のテーマ

[Day36](https://zenn.dev/shinyay/articles/hello-rust-day036)、 [Day 37](https://zenn.dev/shinyay/articles/hello-rust-day037)と Rust 用の Web フレームワークを見てきました。そして、この Web フレームワークを見始めた理由としては、Rust での非同期処理について学ぼうと考えていたのが発端でした。
フレームワークという見方をかえるとすると、**Rocket** も **actix-web** もいずれも非同期処理の機能を提供するモジュール（クレート）を使用しているということになります。

## 非同期処理のクレート

非同期処理という点では、[Day 34](https://zenn.dev/shinyay/articles/hello-rust-day034) の **Rust 1.64** の特徴を紹介した中で `IntoFuture` による非同期処理について見てみました。その文脈で、非同期処理の仕組みとして `await`/`async` キーワードについて簡単に説明しています。
`async` を使って非同期処理を行う関数を定義し、`await` をどこかにつけることによって、その関数の処理待ちをしながら次の処理に進んでいくというものです。

例えば、以下のように非同期処理の関数を定義できます。

```rust
async fn hello_rust() {
    println!("hello, Rust!");
}
```

そしてこの関数を動かすために次のように書くでしょう。

```rust
async fn main() {
    hello_rust().await;
}
```

しかし、これはコンパイルが通りません。`main` 関数はチウ上では非同期化できない (`async` キーワードを `fn` キーワードの前につけることができない) からです。そこで、別途非同期処理ランタイムなクレートを用いて非同期化のサポートをしてもらいます。

この非同期処理ランタイムに期待する機能は、主に次のようなことです。

✅ `async` 定義した関数の実行スケジューリング
✅ スケジューリングした関数の発火 (実際の実行)
✅ 非同期 I/O やネットワークのための API 追加

Web フレームワークのベースとして使われている非同期処理ランタイムには次のようなクレートがあるようです。

- **[tokio](https://tokio.rs/)**
- **[async-std](https://book.async.rs/)**
- **[hyper](https://hyper.rs/)**

## 非同期処理ランタイムと Web フレームワーク

[Day36](https://zenn.dev/shinyay/articles/hello-rust-day036) に代表的な Web フレームワークを調べてみました。ここでは、そのフレームワークが、どの非同期処理ランタイムをベースにしているか、調べて見ました。

### tokio

次のフレームワークが、**tokio** をベースにした Web フレームワークです。

|名称|公式サイト|GitHubリポジトリ|ドキュメント|
|---|--------|---------------|----------|
|actix-web|https://actix.rs/|https://github.com/actix/actix-web|https://docs.rs/actix-web/latest/actix_web/|
|Thruster|-|https://github.com/trezm/Thruster|https://docs.rs/thruster|

### async-std

次のフレームワークが、**async-std** をベースにした Web フレームワークです。

|名称|公式サイト|GitHubリポジトリ|ドキュメント|
|---|--------|---------------|----------|
|Tide|-|https://github.com/rustasync/tide|https://docs.rs/tide|

### hyper

次のフレームワークが、**hyper** をベースにした Web フレームワークです。

|名称|公式サイト|GitHubリポジトリ|ドキュメント|
|---|--------|---------------|----------|
|rocket|https://rocket.rs/|https://github.com/SergioBenitez/rocket|https://rocket.rs/v0.5-rc/guide/introduction/|
|warp|-|https://github.com/seanmonstar/warp|https://docs.rs/warp/|
|gotham|http://gotham.rs/|https://github.com/gotham-rs/gotham/|https://docs.rs/gotham/|
|Thruster|-|https://github.com/trezm/Thruster|https://docs.rs/thruster|
|salvo|-|https://github.com/salvo-rs/salvo|https://docs.rs/salvo/|
|axum|-|https://github.com/tokio-rs/axum|https://docs.rs/axum|
|Poem|-|https://github.com/poem-web/poem|https://github.com/poem-web/poem/blob/master/poem/README.md|
|Viz|https://viz.rs/|https://github.com/viz-rs/viz|https://docs.rs/viz/|

## Day 38 のまとめ

非同期処理が必要となる様々な Web フレームワークにはベースになっている非同期処理ランタイムを提供しているクレートがあることが分かりました。それは主に次の３つでした。

- **[tokio](https://tokio.rs/)**
- **[async-std](https://book.async.rs/)**
- **[hyper](https://hyper.rs/)**

今日はこれらの非同期処理ランタイムでフレームワークを分類してみました。一方で、まだそれぞれの非同期処理ランタイムの特徴をきちんとは調べていないので後日調べてみようと思います。
