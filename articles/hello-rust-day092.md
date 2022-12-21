---
title: "100日後にRustをちょっと知ってる人になる: [Day 92]書籍: Webアプリ開発で学ぶRust言語入門 その2"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 92 のテーマ

[Day 91](https://zenn.dev/shinyay/articles/hello-rust-day091) から読み始めた [Webアプリ開発で学ぶ Rust言語入門](shuwasystem.co.jp/book/9784798067315.html) のですが、今日も読み進めようと思います。

![](https://storage.googleapis.com/zenn-user-upload/0abe692735b6-20221220.png)

- **第 1 章 RustとWeb開発**
  - 1.1 Rustでの開発の準備
- **第 2 章 Rust基礎**
  - 2.1 変数とデータ型
  - 2.2 関数の実装
  - 2.3 制御構造
  - 2.4 所有権による安全性
  - 2.5 データ構造
  - 2.6 async/await
  - 2.7 クレートとモジュール
  - 2.8 テスト
  - 2.9 よく使うライブラリ
- **第 3 章 axumを使ってhttpリクエストを処理する**
  - [3.1 axumとは](https://zenn.dev/shinyay/articles/hello-rust-day091#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.1-axum%E3%81%A8%E3%81%AF)
  - [3.2 環境構築](https://zenn.dev/shinyay/articles/hello-rust-day091#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.2-%E7%92%B0%E5%A2%83%E6%A7%8B%E7%AF%89)
  - 3.3 テスト
  - 3.4 Todo情報を保存する
  - 3.5 httpリクエスト
  - 3.6 バリデーションの追加
- **第 4 章 sqlxを使ってCRUDを実装する**
  - 4.1 データベース基礎
  - 4.2 sqlxとは
  - 4.3 axumとsqlx
  - 4.4 todoのCRUD
  - 4.5 sqlxのテスト
- **第 5 章 Todoアプリの体裁を整える**
  - 5.1 フロントエンド開発
  - 5.2 React環境構築
  - 5.3 TodoアプリのUI実装
  - 5.4 外部APIとの通信（1）
  - 5.5 外部APIとの通信（2）
- **第 6 章 Todoにラベルをつける**
  - 6.1 ラベルのCRUD
  - 6.2 TodoRepositoryのラベル対応
  - 6.3 ラベル機能を画面に追加する
  - 6.4 さらなる機能拡張

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.2 環境構築

### ロギング

前回作成したコードにはまだログ出力に関する実装はしていませんでした。そこで、ログ出力を追加したいと思います。ログ出力には次のクレートをを使用します。

- [tracing](https://crates.io/crates/tracing)

`tracing_subscriber::fmt::init();` によって `tracing` の初期化を行います。

そして `debug` レベルの場合に出力するログは次の様に `debug` メソッドを使って出力を行います。

```rust
let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
tracing::debug!("listening on {}", addr);
```

```shell
$ RUST_LOG=debug cargo run

2022-12-21T03:46:00.781809Z DEBUG day_91_hello_axum: listening on 127.0.0.1:3000
2022-12-21T03:46:07.831426Z DEBUG hyper::proto::h1::io: parsed 3 headers
2022-12-21T03:46:07.831466Z DEBUG hyper::proto::h1::conn: incoming body is empty
2022-12-21T03:46:07.831704Z DEBUG hyper::proto::h1::io: flushed 129 bytes
2022-12-21T03:46:07.831932Z DEBUG hyper::proto::h1::conn: read eof
```

### 入出力用 JSON データ

次に GET メソッドだけでなく、POST メソッドを扱うインターフェースにします。
まず、インプットとアウトプットに期待するデータの型として、構造体を用意します。

入力用

```rust
#[derive(Deserialize)]
struct CreateUser {
    username: String,
}
```

出力用

```rust
#[derive(Serialize)]
struct User {
    id: u64,
    username: String,
}
```

それぞれ、入力時には `Deserialize`, 出力時には `Serialize` を行って JSON を扱っています。

```rust
async fn create_user (Json(payload): Json<CreateUser>) -> impl IntoResponse {
    :
    :
    (StatusCode::CREATED, Json(user))
}
```

axum::Json によりリクエストボディを serde::Serialize を実装した何らかの型にデシリアライズすることができます。

- [axum::Json](https://docs.rs/axum/0.2.3/axum/struct.Json.html)

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.3 テスト

axum で作られた Web アプリケーションのテスト方法についてみていきます。ここでは、End to End テストではなく、単体テストという観点にフォーカスします。

### tower::ServiceExt

Web アプリケーションは実行する場合はサーバ起動が伴いますが、このテスト実行の中では実際にはサーバを起動しません。`tomwe::ServerExt` トレイトにある、`oneshot` メソッドを利用します。

- [tower::ServiceExt](https://docs.rs/tower/latest/tower/trait.ServiceExt.html)

`oneshot` メソッドは、リクエストを渡すと `Router` インスタンスから１度だけハンドリングを実施して、レスポンスを生成してくれるユーティリティメソッドです。

### テスト用条件付きコンパイルとテスト用モジュール

テスト用のコードは、プロダクションモジュールには混ぜたくないと思います。そこで、テスト用注釈を使っての条件付きコンパイル、それとテスト用のモジュールを作成していきます。

次のように注釈することで、この配下のブロックはテスト時にコンパイルされる条件付けが行われます。また、注釈をつける対象としてモジュール `mod` を作成することで、以降のコードが実際のプロダクションロジックとは区別することが可能です。

```rust
#[cfg(test)]
mod test {
  :
}
```

### 最初のテストコード: Hello World テスト

#### リクエストの作成

`Request::builder` を利用してリクエストを作成します。

- [(axum::http::)Request::builder](https://docs.rs/http/latest/http/request/struct.Request.html#method.builder)

```rust
let req = Request::builder().uri("/").body(Body::empty()).unwrap();
```

URI は、`Hello world` の出力を想定しているエンドポイントの `/` ルートを設定しています。GET アクセスのため、特に Body には何も設定する必要がないため `Body::empty()` メソッドで空にしています。この戻り値は、`Result` になるため (設定次第では失敗する可能性の呼び出しのため) `unwrap` して内容を取り出しています。

このリクエスト内容を、`tower::ServiceExt` の `oneshot` 関数によって実行します。これは、非同期の関数のため `await` し、`unwrap` して結果を取り出します。

```rust
let res = create_app().oneshot(req).await.unwrap();
```

## Day 92 のまとめ

ログ出力に関してと、GETに加えてPOSTメソッドの扱いについて確認をしてみました。
