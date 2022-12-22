---
title: "100日後にRustをちょっと知ってる人になる: [Day 93]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 93 のテーマ

[Day 91](https://zenn.dev/shinyay/articles/hello-rust-day091) から読み始めた [Webアプリ開発で学ぶ Rust言語入門](shuwasystem.co.jp/book/9784798067315.html) のですが、今日も少しずつ読み進めようと思います。

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

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.4 Todo情報を保存する

3.4 章 からは、サンプルアプリケーションとして **Todo アプリ**の開発をしながら Rust の学習を進めていく流れになっています。Todo アプリケーションは、その他の言語でも Web アプリケーションの題材としてよく扱われる内容なので、デザインについては想像できる人が多いのではないかなって思います。HTTP メソッドに対応した、CRUD 操作を紐付けていくという流れになりますよね。それを、Rust で実装する場合はどのようにしていくのかを、ぼくも学びたいと思います。

|HTTP メソッド|CRUD 操作|
|-----------|---------|
|GET|Create (作成)|
|POST|Read (参照)|
|PUT|Update (更新)|
|DELETE|Delete (削除)|

## TodoRepository の作成

### エラー用の enum

Debug と Error マクロを持つ Error 用の enum を作ります。ここでは、まずは `NotFound` のみを定義しています。

```rust
#[derive(Debug, Error)]
enum RepositoryError {
    #[error("NotFound, id is {0}")]
    NotFound(i32),
}
```

### TodoRepository の振る舞いのためのトレイト

ここで、`TodoRepository: Clone + std::marker::Send + std::marker::Sync + 'static` として `A + B` のように記述しているのは、複数のトレイトを継承しているということです。

```rust
pub trait TodoRepository: Clone + std::marker::Send + std::marker::Sync + 'static {
    :
}
```

ここで継承したのは、次のトレイトです。この時点では、なぜこのトレイトを継承しているか分かりにくいですが、axum のお作法として `Clone + Send + Sync + 'static` を継承するようです。

- [std::clone::Clone](https://doc.rust-lang.org/std/clone/trait.Clone.html)
- [std::marker::Send](https://doc.rust-lang.org/std/marker/trait.Send.html)
- [std::marker::Sync](https://doc.rust-lang.org/std/marker/trait.Sync.html)

そして、実際の振る舞いとしては次のように CRUD 操作を作っています。

```rust
pub trait TodoRepository: Clone + std::marker::Send + std::marker::Sync + 'static {
    fn create(&self, payload: CreateTodo) -> Todo;
    fn find(&self, id: i32) -> Option<Todo>;
    fn all(&self,) -> Vec<Todo>;
    fn update(&self, id: i32, payload: UpdateTodo) -> anyhow::Result<Todo>;
    fn delete(&self, id: i32) -> anyhow::Result<()>;
}
```

## Day 93 のまとめ
