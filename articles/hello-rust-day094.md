---
title: "100日後にRustをちょっと知ってる人になる: [Day 94]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 94 のテーマ

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

先日に引き続き、Todo アプリケーションの実装について見ていきます。

### リポジトリの共有

引数に `TodoRepository` トレイトを追加しています。これを `axum::routing::Router#layer` によりアプリケーション内で共有するようにします。状態を保持するために使用できるExtension機能を使って再利用しています。

```rust
fn create_app<T: TodoRepository>(repository: T) -> Router {
    Router::new()
        :
        .route("/", get(root))
        :
        .layer(Extension(Arc::new(repository)))
}
```

- [axum::routing::Router#layer](https://docs.rs/axum/latest/axum/routing/struct.Router.html#method.layer)
- [axum::Extension](https://docs.rs/axum/latest/axum/struct.Extension.html)

同様に、GET や POST を行うハンドラ側でも `Extension` を受け取るようにします。

```rust
pub async fn create_todo<T: TodoRepository>(
    Json(payload): Json<CreateTodo>,
    Extension(repository): Extension<Arc<T>>,
) -> impl IntoResponse {
    let todo = repository.create(payload);

    (StatusCode::CREATED, Json(todo))
}
```

### スレッドセーフに HashMap からの取得

ロックの排他的書き込みアクセスを解放するために使用する構造体の `std::sync::RwLockWriteGuard` を使用して Read / Write 権限のある `HashMap` をスレッドセーフに取得します。

```rust
impl TodoRepositoryForMemory {
    pub fn new() -> Self {
        TodoRepositoryForMemory {
            store: Arc::default(),
        }
    }

    fn write_store_ref(&self) -> RwLockWriteGuard<TodoDatas> {
        self.store.write().unwrap()
    }

    fn read_store_ref(&self) -> RwLockReadGuard<TodoDatas> {
        self.store.read().unwrap()
    }
}
```

- [std::sync::RwLockWriteGuard](https://doc.rust-lang.org/std/sync/struct.RwLockWriteGuard.html)

## Day 94 のまとめ
