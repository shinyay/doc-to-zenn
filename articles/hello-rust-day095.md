---
title: "100日後にRustをちょっと知ってる人になる: [Day 95]書籍: Webアプリ開発で学ぶRust言語入門 その5"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 95 のテーマ

[Day 91](https://zenn.dev/shinyay/articles/hello-rust-day091) から読み始めた [Webアプリ開発で学ぶ Rust言語入門](https://www.shuwasystem.co.jp/book/9784798067315.html) のですが、[Day 94](https://zenn.dev/shinyay/articles/hello-rust-day094) でデータベースの代わりにメモリ上で HashMap を使ってのデータ保管が行える Web アプリケーションを作るところまでは見てみました。今日からは、実際のデータベースを使ってアプリケーションをどうやって作るかを見ていきたいと思います。

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
  - [3.3 テスト](https://zenn.dev/shinyay/articles/hello-rust-day092#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.3-%E3%83%86%E3%82%B9%E3%83%88)
  - [3.4 Todo情報を保存する](https://zenn.dev/shinyay/articles/hello-rust-day094#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.4-todo%E6%83%85%E5%A0%B1%E3%82%92%E4%BF%9D%E5%AD%98%E3%81%99%E3%82%8B)
  - [3.5 httpリクエスト](https://zenn.dev/shinyay/articles/hello-rust-day094#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.5-http-%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88)
  - [3.6 バリデーションの追加](https://zenn.dev/shinyay/articles/hello-rust-day094#%E7%AC%AC-3-%E7%AB%A0-axum%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6http%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B---3.6-%E3%83%90%E3%83%AA%E3%83%87%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E8%BF%BD%E5%8A%A0)
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

## 第 4 章 sqlxを使ってCRUDを実装する - 4.1 データベース基礎

この書籍で扱うデータベースは、PostgreSQL が採用されています。また、ネイティブにインストールするのではなく Docker による利用が説明されていました。細かな説明は書籍を参照してもらうといいと思いますが Dcoker Compose を使用して Volume のマウントなどを併せて環境設定が行われています。

Dokerfile

```dockerfile
FROM postgres:13-alpine AS database
ENV LANG ja_JP.utf8
```

docker-compose.yml

```yaml
version: "3.8"
services:
  database:
    build:
      context: .
      dockerfile: Dockerfile
      target: 'database'
    ports:
      - "5432:5432"
    volumes:
      - pgdate:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: admin
      POSTGRES_USER: admin
      POSTGRES_DB: todos
      TZ: Asia/Tokyo
    restart: always
volumes:
  pgdate:
```

## 第 4 章 sqlxを使ってCRUDを実装する - 4.2 sqlxとは

Rust の データベース用のクレートとしてどのようなものがあるかは、[crates.io](https://crates.io/categories/database) を見るとリストが出てきます。

![](https://storage.googleapis.com/zenn-user-upload/2fdf2d7fe7c1-20221225.png)

僕個人的には、どのクレートが人気なのか優れているのか勘所がまだまだないので分からないのですけれど、この本に書かれているものとしては次の 2 つが有力な選択肢らしいです。

- [diesel](https://crates.io/crates/diesel)
- [sqlx](https://crates.io/crates/sqlx)

### diesel

![](https://storage.googleapis.com/zenn-user-upload/b3778cdf17b1-20221225.png)

**diesel** は、Rust の **OR マッパー**かつ**クエリービルダー**です。

- [diesel](https://diesel.rs/)
  - [GitHub](https://github.com/diesel-rs/diesel)

#### 使い方

公式ドキュメントで使い方を見てみます。次のコードが公式でサンプルとして紹介されていたものです。

```rust
use self::models::*;
use diesel::prelude::*;
use diesel_demo::*;

fn main() {
    use self::schema::posts::dsl::*;

    let connection = &mut establish_connection();
    let results = posts
        .filter(published.eq(true))
        .limit(5)
        .load::<Post>(connection)
        .expect("Error loading posts");

    println!("Displaying {} posts", results.len());
    for post in results {
        println!("{}", post.title);
        println!("-----------\n");
        println!("{}", post.body);
    }
}
```

ポイントになるのは、次の箇所です。

```rust
let results = posts
    .filter(published.eq(true))
    .limit(5)
    .load::<Post>(connection)
    .expect("Error loading posts");
```

`filter` や `limit` などを使って SQL を組み立てる SQL ビルダーとして機能しています。

### sqlx

🧰 The Rust SQL Toolkit

- [GitHub](https://github.com/launchbadge/sqlx)

**sqlx** は diesel とは異なり、シンプルな SQL ライブラリです。sqlx は OR マッパーの機能も SQL クエリービルダーの機能も持ってはいません。SQL のコンパイル時チェックとマイグレーションを行う非常にシンプルなライブラリです。

#### sqlx のインストール

`cargo` コマンドを使って **sqlx** の CLI をインストールします。

```shell
cargo install sqlx-cli
```

```shell
$ cargo --list

Installed Commands:
  :
    sqlx
  :
```

sqlx CLI のヘルプを見てみます。

```shell
$ sqlx -h

sqlx-cli 0.6.2
Jesper Axelsson <jesperaxe@gmail.com>, Austin Bonander <austin.bonander@gmail.com>
Command-line utility for SQLx, the Rust SQL toolkit.

USAGE:
    sqlx <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    database    Group of commands for creating and dropping your database
    help        Print this message or the help of the given subcommand(s)
    migrate     Group of commands for creating and running migrations
    prepare     Generate query metadata to support offline compile-time verification
```

SQL のマイグレーションファイルをこの CLI で作成することができます。

`sqlx migrate add <ファイル名>` でマイグレーションファイルを `migrations` ディレクトリの下に作成されます。

```shell
$ sqlx migrate add init

Creating migrations/20221225125911_init.sql

Congratulations on creating your first migration!

Did you know you can embed your migrations in your application binary?
On startup, after creating your database connection or pool, add:

sqlx::migrate!().run(<&your_pool OR &mut your_connection>).await?;

Note that the compiler won't pick up new migrations if no Rust source files have changed.
You can create a Cargo build script to work around this with `sqlx migrate build-script`.

See: https://docs.rs/sqlx/0.5/sqlx/macro.migrate.html
```

#### 使い方

公式のサンプルを見てみると、以下のようなコードが紹介されていました。これを見ると非同期処理にも対応しているようですね。
実際の使い方については、次の章で紹介されているので次回じっくり見ていきたいと思います。

```rust
use sqlx::postgres::PgPoolOptions;

#[async_std::main]
async fn main() -> Result<(), sqlx::Error> {
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect("postgres://postgres:password@localhost/test").await?;

    let row: (i64,) = sqlx::query_as("SELECT $1")
        .bind(150_i64)
        .fetch_one(&pool).await?;

    assert_eq!(row.0, 150);

    Ok(())
}
```

## Day 95 のまとめ

Rust で扱うデータベース操作を学びはじめました。
特に Web アプリケーションを考える上ではデータベース構成は必須になってくるので、ここで基本的にな使い方を学びたいと思います。
次回は、先日まで作っていた Todo アプリケーションの HashMap の部分をデータベースに置き換えていくことになります。
