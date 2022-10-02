---
title: "100日後にRustをちょっと知ってる人になる: [Day 37]はじめての Web フレームワーク その2"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 37 のテーマ

[Day 36](https://zenn.dev/shinyay/articles/hello-rust-day036) で Rust で作る　Web フレームワークを見てみました。いろいろなフレームワークがあるのですが、その中から **Rocket** を少し触って簡単なアプリケーションの作り方を見てみました。

今日も別のフレームワークを使ってみようと思います。

## actix-web

今日使ってみようと思うフレームワークは **actix-web** です。

- [actix-web](https://actix.rs/)
  - [crates.io](https://crates.io/crates/actix-web)

### actix-web の特徴

actix-web は非同期処理をする　Web サーバの機能をもっているのですが、一番の特徴はアクターモデルを使用していることのようです。非同期処理のランタイムの上に、アクターモデルのレイヤーを持っていることです。

アクターモデルという概念は **Akka** でよく耳にする言葉だと思います。並列処理を効率的に処理するために誕生した実装モデルです。
アプリケーションの処理を細切れとされた複数の処理の集合とみなし、それぞれの処理をアクターという実体で実行するものです。アプリケーション全体の処理としては、アクター間の連携によって実現します。この連携は、あるアクターが別のアクターに対してメッセージを送信し、受信側はメッセージに応じた処理を非同期に行うことができます。

✅ HTTP/1.x および HTTP/2 をサポート
✅ ストリーミングとパイプライン
✅ マクロによるリクエストルーティング
✅ Tokioとの完全な互換性
✅ キープアライブおよびスローリクエストの処理
✅ クライアント/サーバー WebSocketの サポート
✅ 透過的なコンテンツ圧縮/解凍 (br、gzip、deflate、zstd)
✅ マルチパートストリーム
✅ 静的アセット
✅ OpenSSL を使用した SSL サポート
✅ ミドルウェア機能 (ロガー、セッション、CORS など)
✅ `awc` クレート HTTP クライアントとの統合
✅ Rust `1.59+` で実行可能

### Hello, World!

何はともあれ、動くアプリケーションを作ってみようと思います。

まずは `Cargo.toml` に `actix-web` への依存関係を追加しておきます。
現在の最新バージョンを確認し追加します。

![](https://storage.googleapis.com/zenn-user-upload/c3eadcb6955f-20221002.png)

```toml
[dependencies]
actix-web = "4.2.1"
```

まず、クライアントからのリクエストを受け付けるリクエストハンドラを作ります。

**Rocket** と同じ様にリクエストハンドラの関数に対して、組み込みマクロの `#[get("/")]` を使用してルーティングを関連付けます。またこの関数は非同期 (`async`) で定義をします。このルーティングマクロでは、応答するHTTP メソッドと、パスの指定を行います。

```rust
#[get("/")]
async fn hello() -> impl Responder {}
```

次に、`App` インスタンスを作成し、`App::service` を使用してリクエストハンドラを登録します。
そして、アドレスをバインドして HttpServer の起動を行います。

```rust
#[actix_web::main]
async fn main() -> Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(hello)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
```

`#[actix_web::main]` を使用して、`main` 関数を非同期で実行します。

## Day 37 のまとめ

actix-web でシンプルな Hello world なアプリケーションを作ってみました。実質、十数行ほどを書くだけで作れました。この actix-web は HTTP/2 対応や、WebSocket 対応などがあるので、もっと使いこなしな実装を調べてみたいと思います。

ですが、昨日少し触った Rocket 同様に Web フレームワークを使うと、Rust でも簡単に Web アプリケーションが作れるということが分かりました。
