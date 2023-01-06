---
title: "100日後にRustをちょっと知ってる人になる: [Day 97]書籍: Webアプリ開発で学ぶRust言語入門 その7"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 97 のテーマ

[Day 91](https://zenn.dev/shinyay/articles/hello-rust-day091) から読み始めた [Webアプリ開発で学ぶ Rust言語入門](https://www.shuwasystem.co.jp/book/9784798067315.html) ですが、今日でバックエンド部分のデータベースアクセスについては完成させようと思います。

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
  - [4.3 axumとsqlx](https://zenn.dev/shinyay/articles/hello-rust-day096#%E7%AC%AC-4-%E7%AB%A0-sqlx%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6crud%E3%82%92%E5%AE%9F%E8%A3%85%E3%81%99%E3%82%8B---4.3-axum%E3%81%A8sqlx)
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

## 第 4 章 sqlxを使ってCRUDを実装する - 4.4 todoのCRUD

データベースの操作に関する実装は、sqlx を用いて行います。

### sqlx 公式サンプル

書籍の方で参考にしている公式のサンプルを少し眺めてみたいと思います。

- [sqlx - Quickstart](https://github.com/launchbadge/sqlx#quickstart)

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

sqlx のクエリの実行は直感的に分かりやすい構造になっています。

- `query_as`
  - SQL 文字列の初期化
  - [sqlx::query_as](https://docs.rs/sqlx/latest/sqlx/fn.query_as.html)
- `bind`
  - SQL 文字列中に定義しているパラメータに対する値のバインド
  - [pub fn bind<T>](https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html#method.bind)
- `fetch_one`
  - 該当するデータを 1 つのみ取得
  - [pub async fn fetch_one<'e, 'c, E>](https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html#method.fetch_one)
    - 変更をじっこうする場合は `execute`, 該当レコードを `Stream` で取得するばあいは `fetch`

```rust
use futures::TryStreamExt;

let mut rows = sqlx::query("SELECT * FROM users WHERE email = ?")
    .bind(email)
    .fetch(&mut conn);

while let Some(row) = rows.try_next().await? {
    let email: &str = row.try_get("email")?;
}
```

上記のように `fetch` により取得した `Row` を `while` ループにより `row.get()` でレコードを取得します。

### Todo アプリケーションの実装

先日までに作成してきていた Todo アプリケーションのデータベース操作部分の実装を行います。

#### Create - データ挿入

まず、データの挿入操作についての実装を行います。SQL 文は次のようなものになります。戻り値を扱いたいため、`returning *` を設定しています。

```sql
insert into todos (text, completed) values ($1, false) returning *
```

`query_as::<_, Todo>` としているので、`fetch_one` の結果の戻り値を `Todo` にバインドしています。

```rust
async fn create(&self, payload: CreateTodo) -> anyhow::Result<Todo> {
    let todo = sqlx::query_as::<_, Todo>(
        r#"
insert into todos (text, completed)
values ($1, false)
returning *
    "#,
    )
    .bind(payload.text.clone())
    .fetch_one(&self.pool)
    .await?;

    Ok(todo)
}
```

### Find - データ取得

データの取得用のメソッドを実装します。SQL 文は次のようなものになります。

```sql
select * from todos where id=$1
```

ID を指定して特定のレコードの取得を行います。そのため、SQL 文の実行は `fetch_one` を使用します。

```rust
async fn find(&self, id: i32) -> anyhow::Result<Todo> {
    let todo = sqlx::query_as::<_, Todo>(
        r#"
select * from todos where id=$1
    "#,
    )
    .bind(id)
    .fetch_one(&self.pool)
    .await
    .map_err(|e| match e {
        sqlx::Error::RowNotFound => RepositoryError::NotFound(id),
        _ => RepositoryError::Unexpected(e.to_string()),
    })?;

    Ok(todo)
}
```

### Update - データ更新

データ更新には次の SQL 文を使用します。

```sql
update todos set text=$1, completed=$2 where id=$3 returning *
```

更新前の状態を取得してから更新を行っています。

```rust
async fn update(&self, id: i32, payload: UpdateTodo) -> anyhow::Result<Todo> {
    let old_todo = self.find(id).await?;
    let todo = sqlx::query_as::<_, Todo>(
        r#"
update todos set text=$1, completed=$2
where id=$3
returning *
    "#,
    )
    .bind(payload.text.unwrap_or(old_todo.text))
    .bind(payload.completed.unwrap_or(old_todo.completed))
    .bind(id)
    .fetch_one(&self.pool)
    .await?;

    Ok(todo)
}
```

### Delete - データ削除

データの削除を行うには次の SQL 文を使用します。

```sql
delete from todos where id=$1
```

特定の ID を指定してデータを削除します。ここでは特に戻り値を期待しないので、`execute` を使用しています。

```rust
async fn delete(&self, id: i32) -> anyhow::Result<()> {
    sqlx::query(
        r#"
delete from todos where id=$1
    "#,
    )
    .bind(id)
    .execute(&self.pool)
    .await
    .map_err(|e| match e {
        sqlx::Error::RowNotFound => RepositoryError::NotFound(id),
        _ => RepositoryError::Unexpected(e.to_string()),
    })?;

    Ok(())
}
```

## Day 97 のまとめ

今回の実装で sqlx を使ったデータベース操作に関する実装を完成することができました。sqlx を用いると データベースに対する接続や SQL 文の実行など、かなりパターン化された実装をすることができることが分かりました。また、予め非同期対応されている点も Web アプリケーションとして使用するのにとても相性がいいかなと思います。
かなり実装周りはパターン化されてると思いますが、まだ今回のアプリケーションの実装でしか使ったことがないのでもう少し繰り返し使って慣れていきたいなと思いました。
