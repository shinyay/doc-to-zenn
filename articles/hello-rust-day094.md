---
title: "100日後にRustをちょっと知ってる人になる: [Day 94]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
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

取得した HashMap を利用して、CRUD の実装を行います。

例えば全件取得の `all` メソッドの場合は `values()` でイテレータを取得した後に借用した値をクローンして、ベクターにします。借用値が含まれるため、値のコピーを行うクローンをする必要があります。

```rust
fn all(&self) -> Vec<Todo> {
    let store = self.read_store_ref();
    Vec::from_iter(store.values().map(|todo| todo.clone()))
}
```

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.5 http リクエスト

CRUD 操作に対するハンドラの定義を行います。

- Create: 作成

```rust
pub async fn create_todo<T: TodoRepository>(
    Json(payload): Json<CreateTodo>,
    Extension(repository): Extension<Arc<T>>,
) -> impl IntoResponse {
    let todo = repository.create(payload);

    (StatusCode::CREATED, Json(todo))

}
```

- Find: 参照

```rust
pub async fn find_todo<T: TodoRepository>(
    Path(id): Path<i32>,
    Extension(repository): Extension<Arc<T>>,
) -> Result<impl IntoResponse, StatusCode> {
    let todo = repository.find(id).ok_or(StatusCode::NOT_FOUND)?;
    Ok((StatusCode::OK, Json(todo)))
}
```

- All: 全件参照

```rust
pub async fn all_todo<T: TodoRepository>(
    Extension(repository): Extension<Arc<T>>,
) -> impl IntoResponse {
    let todo = repository.all();
    (StatusCode::OK, Json(todo))
}
```

- Update: 更新

```rust
pub async fn update_todo<T: TodoRepository>(
    Path(id): Path<i32>,
    Json(payload): Json<UpdateTodo>,
    Extension(repository): Extension<Arc<T>>,
) -> Result<impl IntoResponse, StatusCode> {
    let todo = repository
        .update(id, payload)
        .or(Err(StatusCode::NOT_FOUND))?;
    Ok((StatusCode::CREATED, Json(todo)))
}
```

- Delete: 削除

```rust
pub async fn delete_todo<T: TodoRepository>(
    Path(id): Path<i32>,
    Extension(repository): Extension<Arc<T>>,
) -> StatusCode {
    repository
        .delete(id)
        .map(|_| StatusCode::NO_CONTENT)
        .unwrap_or(StatusCode::NOT_FOUND)
}
```

## 第 3 章 axumを使ってhttpリクエストを処理する - 3.6 バリデーションの追加

`validator` を追加することで、バリデーション機能を追加することが可能です。

- [validator](https://crates.io/crates/validator)

`cargo add` コマンドで依存関係を追加します。

```shell
cargo add validator --features derive
```

`validate` を追加したら、以下のようにバリデーション条件を設定します。

```rust
#[derive(Debug, Serialize, Deserialize, Clone, PartialEq, Eq, Validate)]
pub struct CreateTodo {
    #[validate(length(min = 1, message = "Can not be empty"))]
    #[validate(length(max = 100, message = "Over text length"))]
    text: String,
}
```

`CreateTodo` 構造体の要素の `text` に対して、最小文字数の設定 (空文字の禁止) と文字数上限設定を設けています。

これを、axum のリクエスト処理の中で対応させるようにトレイトを実装する必要があります。

```rust
#[async_trait]
impl<T, B> FromRequest<B> for ValidatedJson<T>
where
    T: DeserializeOwned + Validate,
    B: http_body::Body + Send,
    B::Data: Send,
    B::Error: Into<BoxError>,
{
    type Rejection = (StatusCode, String);

    async fn from_request(req: &mut RequestParts<B>) -> Result<Self, Self::Rejection> {
        let Json(value) = Json::<T>::from_request(req).await.map_err(|rejection| {
            let message = format!("Json parse error: [{}]", rejection);
            (StatusCode::BAD_REQUEST, message)
        })?;
        value.validate().map_err(|rejection| {
            let message = format!("Validation error: [{}]", rejection).replace('\n', ", ");
            (StatusCode::BAD_REQUEST, message)
        })?;
        Ok(ValidatedJson(value))
    }
}
```

以下でバリデートを行い、失敗したらエラーを返しています。

```rust
value.validate().map_err(|rejection| {
    let message = format!("Validation error: [{}]", rejection).replace('\n', ", ");
    (StatusCode::BAD_REQUEST, message)
})?;
```

## Day 94 のまとめ

一旦今日の時点で、DB の代わりに HashMap を使ってのデータ送受信ができる状態にはなりました。感覚的には、昨日も感想で書いたように axum 独特の実装の癖みたいなところが乗り越えられたらテンプレート通りに実装ができそうな気がします。
今はまだその癖に慣れきってないので、もう少し練習して作法が頭に入るようにしたいかなと思います。

ちなみに、axum のバージョン v0.6.0 以降だと、**Webアプリ開発で学ぶ Rust言語入門** のサンプルコードは動かないですね。`FromRequest` 周りの仕様が少し変わっていますね。

- [Announcing axum 0.6.0](https://tokio.rs/blog/2022-11-25-announcing-axum-0-6-0)
