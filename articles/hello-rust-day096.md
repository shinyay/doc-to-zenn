---
title: "100日後にRustをちょっと知ってる人になる: [Day 96]書籍: Webアプリ開発で学ぶRust言語入門 その6"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 96 のテーマ

[Day 91](https://zenn.dev/shinyay/articles/hello-rust-day091) から読み始めた [Webアプリ開発で学ぶ Rust言語入門](https://www.shuwasystem.co.jp/book/9784798067315.html) ですが、年末年始休暇に入ってから少し滞っていました。本自体は読み終えたので、実際にコードも書きつつ復習してみたいと思います。

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
  - [4.1 データベース基礎](https://zenn.dev/shinyay/articles/hello-rust-day095#%E7%AC%AC-4-%E7%AB%A0-sqlx%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6crud%E3%82%92%E5%AE%9F%E8%A3%85%E3%81%99%E3%82%8B---4.1-%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E5%9F%BA%E7%A4%8E)
  - [4.2 sqlxとは](https://zenn.dev/shinyay/articles/hello-rust-day095#%E7%AC%AC-4-%E7%AB%A0-sqlx%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6crud%E3%82%92%E5%AE%9F%E8%A3%85%E3%81%99%E3%82%8B---4.2-sqlx%E3%81%A8%E3%81%AF)
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

## 第 4 章 sqlxを使ってCRUDを実装する - 4.3 axumとsqlx

[Day 95](https://zenn.dev/shinyay/articles/hello-rust-day095) で確認をしてみた sqlx を使用してデータベースに情報を永続化できるようにアプリケーションを修正していきます。

### sqlx の準備

`Cargo.toml` に依存関係を追加していきます。

- sqlx ("runtime-tokio-rustls" フィーチャー)
- dotenv

```shell
cargo add sqlx --features "runtime-tokio-rustls"
cargo add dotenv
```

### リポジトリの非同期対応

**sqlx** は非同期処理に対応をしています。

- [SQLx](https://github.com/launchbadge/sqlx)

> SQLx は非同期な SQL クレートで、DSL を使わずにコンパイル時にクエリをチェックするのが特徴です。
>
> - 最大の同時実行性を実現するために、async/await を使って構築されています。

作成していた以下のコードは非同期には非同期になっていません。これらのメソッドを非同期として定義したいため、`#[async_trait]` マクロを付け足します。

- [async_trait](https://docs.rs/async-trait/latest/async_trait/)

このマクロにより、`async fn ...` という記法ができるようになるので、以下のコードを修正します。

- 修正前

```rust
pub trait TodoRepository: Clone + std::marker::Send + std::marker::Sync + 'static {
    fn create(&self, payload: CreateTodo) -> Todo;
    fn find(&self, id: i32) -> Option<Todo>;
    fn all(&self) -> Vec<Todo>;
    fn update(&self, id: i32, payload: UpdateTodo) -> anyhow::Result<Todo>;
    fn delete(&self, id: i32) -> anyhow::Result<()>;
}
```

- 修正後

```rust
#[async_trait]
pub trait TodoRepository: Clone + std::marker::Send + std::marker::Sync + 'static {
    async fn create(&self, payload: CreateTodo) -> anyhow::Result<Todo>;
    async fn find(&self, id: i32) -> anyhow::Result<Todo>;
    async fn all(&self) -> anyhow::Result<Vec<Todo>>;
    async fn update(&self, id: i32, payload: UpdateTodo) -> anyhow::Result<Todo>;
    async fn delete(&self, id: i32) -> anyhow::Result<()>;
}
```

## Day 96 のまとめ
