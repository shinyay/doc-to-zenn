---
title: "100日後にRustをちょっと知ってる人になる: [Day 91]書籍: Webアプリ開発で学ぶRust言語入門 その1"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 91 のテーマ

時が過ぎるのは早いもので、気がつくと Rust の学習を初めて 90 日が経っていました。ちょっと分かってきてるのかどうかはおいておいたとしても、Rust 関連の記事や書籍を読んでもなんとかついていける事が多くなってきているとは思います。
そんな中、また新しく Rust の本を入手したのでさくっと目を通したいと思います。

![](https://storage.googleapis.com/zenn-user-upload/0abe692735b6-20221220.png)

## Webアプリ開発で学ぶ Rust言語入門

今回読もうとしているのは、秀和システムから出版されている、「Webアプリ開発で学ぶ Rust言語入門」です。

- [Webアプリ開発で学ぶ Rust言語入門](shuwasystem.co.jp/book/9784798067315.html)

この本の内容は、Web開発経験がある方を対象に、Rustの基礎文法から、Webアプリケーション開発までチュートリアル形式で体験学習できる入門書となっています。というわけで、この本を読んで Web アプリケーションの開発について学んでみようかなと思います。

### 目次

本の構成は次のようになっています。

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
  - 3.1 axumとは
  - 3.2 環境構築
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

この目次を見る限りだと、1 章 と 2 章 は基本的な文法の解説なので、他の書籍や記事などで既に目を通したことがある内容だと思います。だから、今回は 3 章から読んでいこうと思います。

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.1 axumとは

第 3 章 では、Web アプリケーションフレームワークの **axum** を使って Web アプリケーションを構築していく方法が紹介されています。

Web アプリケーションフレームワークについは、以前 [Day 36](https://zenn.dev/shinyay/articles/hello-rust-day036) や [Day 37](https://zenn.dev/shinyay/articles/hello-rust-day037) で簡単に確認したことがありました。その際に、詳細には見ませんでしたが **axum** についても確認はしていました。

- [GitHub:tokio-rs/axum](https://github.com/tokio-rs/axum)

この axum は 非同期ライブラリで有名な **tokio** の開発チームによるメンテナンスされていあるフレームワークです。人間工学とモジュール性に重点を置いているということが特徴のようです。

- 特徴✨
  - ✅ マクロ不要のAPIでリクエストをハンドラにルーティング
  - ✅ エクストラクタを使った宣言的なリクエストの解析
  - ✅ シンプルで予測可能なエラー処理モデル
  - ✅ 最小限の定型文によるレスポンス生成
  - ✅ ミドルウェア、サービス、ユーティリティの **tower** および **tower-http** エコシステムをフルに活用

### axum のプロジェクト作成

`cargo add` で以下のパッケージを追加します。

- **hyper**
  - HTTP リクエストの処理
- **tower**
  - サーバ構築関連
- **serde, serde_json**
  - JSON パース処理関連
- **mime**
  - HTTP ヘッダの MIME 定義関連
- **tracing, tracing-subscriber**
  - ロギング・デバッグ処理
- **anyhow, thiserror**
  - Result を扱いやすくする ユーティリティ

```shell
cargo add axum
cargo add hyper --features full
cargo add tokio --features full
cargo add tower
cargo add mime
cargo add serde --features derive
cargo add serde_json
cargo add tracing
cargo add tracing-subscriber --features env-filter
cargo add anyhow
cargo add thiserror
```

次のような `Cargo.toml` ができあがりました。

```toml
[dependencies]
anyhow = "1.0.68"
axum = "0.6.1"
hyper = { version = "0.14.23", features = ["full"] }
mime = "0.3.16"
serde = { version = "1.0.151", features = ["derive"] }
serde_json = "1.0.91"
thiserror = "1.0.38"
tokio = { version = "1.23.0", features = ["full"] }
tower = "0.4.13"
tracing = "0.1.37"
tracing-subscriber = { version = "0.3.16", features = ["env-filter"] }
```

### axum Web アプリケーションサンプル

axum を用いたアプリケーションで、最もシンプルなものは次のようなコードになります。起動して、GET アクセスすると、ハードコードしたメッセージを返す、というものです。

```rust
use std::net::SocketAddr;
use axum::Router;
use axum::routing::get;

#[tokio::main]
async fn main() {

    let app = Router::new().route("/", get(root));
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> &'static str {
    "Hello, axum!"
}
```

#### Route

```rust
let app = Router::new().route("/", get(root));
```

`Route` の `route` メソッドを使ってルーティング設定を行います。

- **第一引数**: URL パスのマッチング
- **第二引数**: マッチ時に呼び出す関数

`axum::routing::get` は、GET メソッドによるアクセスを行った場合の呼び出しです。
同様に、`axum::routing::post` ならば、POST メソッドによるアクセスを行った場合となります。
この第二引数は、次のようにメソッドチェーンを用いて、HTTP メソッド各種を定義することが可能です。

```rust
Router::new().route("/",
    get(get_handler)
    .post(post_handler)
    );
```

#### SockerAddr

```rust
let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
```

`from` メソッドにより、`SocketAddr` への変換を行います。

- **第一引数**: IpAddr変換可能な型
- **第二引数**: ポート番号

つまり、この例では IPv4 の `127.0.0.1:3000` を表しています。

#### Server

```rust
axum::Server::bind(&addr)
    .serve(app.into_make_service())
    .await
    .unwrap();
```

- `bind(&addr)`: アドレスをサーバにバインド
- `serve(app.into_make_service())`: サーバの起動処理
- `await`: 非同期に待受け

### axum Web アプリケーションサンプルの実行

`cargo run` コマンドで実行を行います。

起動後に `http://localhost:3000` へのアクセスを行い動作確認を行います。
次のように、`Hello, axum!` が表示されれば正常動作をしています。

```shell
$ curl -X GET localhost:3000

Hello, axum!
```

## Day 91 のまとめ

Rust を用いて作る Web アプリケーションの書籍を読み始めました。以前にも `actix-web` などを使って Web アプリケーションを作ったことがありましたが、今回は `axum` という Web フレームワークの使い方を学んでみます。
今日は、単純なメッセージを返却するのみのアプリケーションを作ってみました。フレームワークの仕様に従ってコードを書くのみでサーバ起動とメッセージ返却の動作を簡単に実装することができました。
次回以降では、ログ出力やデータ入力などの操作をについて見ていきたいと思います。
