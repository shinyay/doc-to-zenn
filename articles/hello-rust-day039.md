---
title: "100日後にRustをちょっと知ってる人になる: [Day 39]hyper"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 39 のテーマ

[Day 38](https://zenn.dev/shinyay/articles/hello-rust-day038) では Web フレームワークを構成する非同期処理ランタイムについて調べました。そして次のようなクレートが様々なフレームワークのベースとして使われていました。

- **[tokio](https://tokio.rs/)**
- **[async-std](https://book.async.rs/)**
- **[hyper](https://hyper.rs/)**

今日はこれらの非同期処理クレートについて確認してみようと思います。

## hyper

- **[hyper](https://hyper.rs/)**

まず最初に **hyper** は実際は非同期処理のクレートではありませんでした。非同期処理ランタイムと組み合わせて動作させる 非同期、Multipart 対応の　HTTP/HTTP2 のクライアント/サーバ用の **低レベル**な機能を提供するクレートです。

### 特徴

✅ Web サービスと対話するためのクライアント
✅ Web サービスを構築するためのサーバ
✅ "超"高速
✅ ノンブロッキング・ソケットによる並行性
✅ HTTP/1 および HTTP/2 のサポート

### 使い方

まず **hyper** のクレートのバージョンを確認します。

- [crates.io](https://crates.io/crates/hyper/versions)

![](https://storage.googleapis.com/zenn-user-upload/413ca7a25887-20221005.png)

`Cargo.toml` に依存関係を追加します。

```toml
[dependencies]
hyper = { version = "0.14.20", features = ["full"] }
```

前述したように、**hyper** 自体は非同期処理ランタイムではありません。そのため、ランタイムのクレートの追加が必要になります。以下のように **tokio** を追加します。

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

リクエストの受信とレスポンスの送信のみをする非同期関数 `async` を定義します。

```rust
async fn hello_hyper(req: Request<Body>) -> Result<Response<Body>, Infallible> {
    Ok(Response::new("Hello, hyper".into()))
}
```

`hyper::Response` で返信内容 `hyper::Body` をクライアントに返します。

次にソケットのリッスンを行い、予め定義しておいた非同期関数の `hello_hyper` を呼び出せるようにします。
`make_service_fn` に対して非同期ブロック (`async`) を持つクロージャを渡して、その中で `service_fn` にリクエスト処理を行う `hello_hyper` を渡しています。

```rust
#[tokio::main]
async fn main() {
    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));

    let make_svc = make_service_fn(|_conn| async {
        Ok::<_, Infallible>(service_fn(hello_hyper))
    });

    let server = Server::bind(&addr).serve(make_svc);

    if let Err(e) = server.await {
        eprintln!("server error: {}", e);
    }
}
```

- [hyper::service::make_service_fn](https://docs.rs/hyper/latest/hyper/service/fn.make_service_fn.html)
- [hyper::service::service_fn](https://docs.rs/hyper/latest/hyper/service/fn.service_fn.html)

これで実行できるようになりました。

::: details 実行
```shell
$ cargo run
   Compiling cfg-if v1.0.0
   Compiling pin-project-lite v0.2.9
   Compiling bytes v1.2.1
   Compiling scopeguard v1.1.0
   Compiling smallvec v1.10.0
   Compiling once_cell v1.15.0
   Compiling itoa v1.0.3
   Compiling fnv v1.0.7
   Compiling pin-utils v0.1.0
   Compiling futures-sink v0.3.24
   Compiling hashbrown v0.12.3
   Compiling try-lock v0.2.3
   Compiling httpdate v1.0.2
   Compiling tower-service v0.3.2
   Compiling libc v0.2.134
   Compiling futures-core v0.3.24
   Compiling memchr v2.5.0
   Compiling futures-task v0.3.24
   Compiling httparse v1.8.0
   Compiling slab v0.4.7
   Compiling log v0.4.17
   Compiling lock_api v0.4.9
   Compiling futures-channel v0.3.24
   Compiling tracing-core v0.1.29
   Compiling futures-util v0.3.24
   Compiling want v0.3.0
   Compiling http v0.2.8
   Compiling parking_lot_core v0.9.3
   Compiling signal-hook-registry v1.4.0
   Compiling socket2 v0.4.7
   Compiling num_cpus v1.13.1
   Compiling mio v0.8.4
   Compiling tracing v0.1.36
   Compiling indexmap v1.9.1
   Compiling parking_lot v0.12.1
   Compiling tokio v1.21.2
   Compiling http-body v0.4.5
   Compiling tokio-util v0.7.4
   Compiling h2 v0.3.14
   Compiling hyper v0.14.20
```
```shell
$ curl http://localhost:8080/
Hello, hyper
```
:::

## tokio

- **[tokio](https://tokio.rs/)**

**tokio** は Rust の非同期処理ランタイムです。hyper の利用の際にも組み合わせて使用していました。

### 特徴

- 信頼性
  - メモリやスレッド管理に優れ、未束縛のキュー、バッファオーバーフロー、タスクスターべーションなどの一般的なバグを防ぐことが可能
- 高速
  - マルチスレッドのスケジューラーを提供。アプリケーションは最小限のオーバーヘッドで1秒間に数十万のリクエストを処理することが可能
- 簡単
  - `async/await` は、非同期アプリケーションを書く際の複雑さを軽減。Tokioのユーティリティや活発なエコシステムと組み合わせることによる容易性

![](https://storage.googleapis.com/zenn-user-upload/30c2086ae3b2-20221005.png)

### チュートリアル

公式ドキュメントにチュートリアルが掲載されているので、後日確認してみたいです。

- [チュートリアル](https://tokio.rs/tokio/tutorial)

## async-std

- **[async-std](https://book.async.rs/)**

`async-std` は以下のような重要なインターフェイスを提供しています。

- ファイルシステム操作
- ネットワーク操作
- タイマーなどの並行処理

Rust の標準ライブラリにある `thread` モジュールに似たモデルでタスクを公開します。

### チュートリアル

async-std も公式ドキュメントにチュートリアルが掲載されているので、後日確認してみたいです。

- [チュートリアル](https://book.async.rs/tutorial/index.html#tutorial-writing-a-chat)

## Day 39 のまとめ

非同期処理のランタイムについて調べようと思いましたが、1日で網羅するのは無謀すぎたので分解して見ていきたいと思います。（片手間で勉強をしているので当然ですね笑）
