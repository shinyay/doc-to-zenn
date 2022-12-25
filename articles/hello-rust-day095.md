---
title: "100日後にRustをちょっと知ってる人になる: [Day 95]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
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

## Day 95 のまとめ
