---
title: "100日後にRustをちょっと知ってる人になる: [Day 36]はじめての Web フレームワーク"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 36 のテーマ

[Day 35](https://zenn.dev/shinyay/articles/hello-rust-day035) では、非同期処理の動きをみようと思い Web サーバを作ってみました。昨日の時点ではシングルスレッドの Web サーバでしたが公式ドキュメントの方では、あの実装からスレッドプールを実装しマルチスレッドにしたサーバの説明が行われていました。

- [シングルスレッド・サーバーをマルチスレッド・サーバーにする](https://doc.rust-lang.org/book/ch20-02-multithreaded.html)

このドキュメントに沿えばマルチスレッド化できます。コードの説明は丁寧に行われれているのですが、コンパイルエラーを見ながら、コードを実装していくという流れになっているので少し読みにくいかもしれませんけれど。

さて、Web サーバを作ってみたりしましたが、実際は自分で Web サーバを書き上げることはきっとしないですよね。車輪の再発明のようなことになりますよね。
例えば、Java のアプリケーションを思い浮かべてみると、サーバ用コンポーネントになる [Apache Tomcat](https://tomcat.apache.org/) を自分で実装する人はいないですよね。多くの人は Web フレームワークの [Spring Boot](https://spring.io/projects/spring-boot) を使って**組み込み Tomcat** を使ったりする人が多いのではないでしょうか。

Java と同様に Rust にも Web フレームワークがあります。ただ、Java の **Spring** のようなデファクトと言えるものはまだ確立されていないように見えます。ということで、ぼくの観測範囲で見つけている Rust の Web フレームワークを紹介します。

## Rust Web フレームワーク

アクティブなプロジェクトや、非アクティブなプロジェクトもあると思いますが次のようなフレームワークがあります。
(全量の中からはまだまだ１部分のはず)

|名称|公式サイト|GitHubリポジトリ|ドキュメント|
|---|--------|---------------|----------|
|actix-web|https://actix.rs/|https://github.com/actix/actix-web|https://docs.rs/actix-web/latest/actix_web/|
|rocket|https://rocket.rs/|https://github.com/SergioBenitez/rocket|https://rocket.rs/v0.5-rc/guide/introduction/|
|warp|-|https://github.com/seanmonstar/warp|https://docs.rs/warp/|
|gotham|http://gotham.rs/|https://github.com/gotham-rs/gotham/|https://docs.rs/gotham/|
|Thruster|-|https://github.com/trezm/Thruster|https://docs.rs/thruster|
|Tide|-|https://github.com/rustasync/tide|https://docs.rs/tide|
|salvo|-|https://github.com/salvo-rs/salvo|https://docs.rs/salvo/|
|trillium|https://trillium.rs/|https://github.com/trillium-rs/trillium|https://docs.trillium.rs/|
|axum|-|https://github.com/tokio-rs/axum|https://docs.rs/axum|
|Poem|-|https://github.com/poem-web/poem|https://github.com/poem-web/poem/blob/master/poem/README.md|
|Viz|https://viz.rs/|https://github.com/viz-rs/viz|https://docs.rs/viz/|

この中から１つだけ今日はためしてみます。

## はじめての Rocket

**[Rocket](https://rocket.rs/)** を試してみようと思います。

### Dependency

**rocket** の[最新バージョン](https://crates.io/crates/rocket/versions)は `0.5.0-rc.2` なので、次のように `Cargo.toml` に定義します。

```toml
[dependencies]
rocket = "0.5.0-rc.2"
```

![](https://storage.googleapis.com/zenn-user-upload/a548a1ada73b-20221001.png)

### Crate

`rocket` が使えるように次のクレートを宣言しておきます。

```rust
#[macro_use] extern crate rocket;
```

### Rocket の動作概要

**Rocket** は、暗いアウトからのリクエストを受け付け、処理を実施した後にクライアントにレスポンスを返す Web フレームワークです。以下のステップをライフサイクルとして動作します。

- **ルーティング**
  - クライアントからのリクエストを解析し、宣言された**ルート属性**と照らし合わせて要求ハンドラを決定します。
- **検証**
  - リクエストの検証をおこないます。検証が失敗した場合、リクエストを次のルートに転送するか、エラーハンドラを呼びだします。
- **処理**
  - ルートに関連付けられたリクエストハンドラを呼び出します。
- **応答**
  - 適切な応答を生成してクライアントに送信します。

### ルーティング

**ルート**と**ハンドラ**の定義を行います。

**ルート**は、リクエストと照合するためのパラメータセットです。
**ハンドラ**は、任意の引数を受け取り、任意の型を返す関数です。

照合するパラメータには以下のようなものがあります:

- 静的パス
- 動的パス
- パスセグメント
- フォーム
- クエリー文字列
- リクエストフォーマット指定子
- ボディデータ
など

```rust
#[get("/hello")]　　　　　　　　// <----- ルート
fn index() -> &'static str { //  <----- ハンドラ
    "Hello, Rocket"
}
```

ここでは、`#[get]` を用いて GET リクエストを受け取っています。もちろんそれ以外の HTTP メソッドも対応しているので、`#[post]`, `#[put]` なども使用可能です。

### ルートのマウント

リクエストをディスパッチする前に、ルートのマウントを行います。
`mount` メソッドでは次の処理を行います:

- ベースパスの設定
  - 次の例では `/` と `/test`
- ルートとベースパスの関連付けを `routes!` マクロで実施
  - 次の例では `index` ルートを設定

```rust
#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index])
        .mount("/test", routes![index])
}
```

以上で実装は終了です。雰囲気的には、よくある Web フレームワークの実装に似ていますよね。

### 起動

**Rocket** は起動すると、非同期のマルチスレッドサーバを起動します。そして、リクエストにマッチするルートにディスパッチを行い、リクエスト処理を行います。

起動するには 2 つの方法があります。

- `#[launch]` 属性による起動 (**推奨**)
- `#[rocket::main]` 属性による起動

#### #[launch]

```rust
#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index])
        .mount("/test", routes![index])
}
```

#### #[rocket::main]

```rust
#[rocket::main]
async fn main() -> Result<(), rocket::Error> {
    let _rocket = rocket::build()
        .mount("/", routes![index])
        .mount("/test", routes![index])
        .launch()
        .await?;
    Ok(())
}
```

## Day 36 のまとめ
