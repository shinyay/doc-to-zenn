---
title: "100日後にRustをちょっと知ってる人になる: [Day 75]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 75 のテーマ

[Day 74](https://zenn.dev/shinyay/articles/hello-rust-day074) で紹介をした日時を扱うクレート `time` の特徴の中で、シリアライゼーションやデシリアライゼーションを行うフレームワークでデファクトスタンダードになっているという `serde` というクレートについて、名前だけ引用しました。その際にも言っていましたが使ったことがまだないので、今回は `serde` について学ぼうと思います。

## serde

まず最初に以下が **serde** に関する文書やリポジトリのリンクです。

- **[crate.io](https://crates.io/crates/serde)**
- **[lib.rs](https://lib.rs/crates/serde)**
- **[docs.rs](https://docs.rs/serde/latest/serde/)**
- **[GitHub](https://github.com/serde-rs/serde/tree/master)**
- **[book - serde](https://serde.rs/)**

それでは、serde について book の内容を中心にして見ていきたいと思います。

### 概要

あらためて、**serde** が何か？ということから説明します。**serde** とは、**ser**ialization と **de**serialization を行うたいめのフレームワークです。

serde は、サポートされるデータ構造を、サポートされるデータ形式を使ってシリアライズおよびデシリアライズすることを可能にします。データ構造とデータ形式の間の相互作用は Rust コンパイラによって完全に最適化され、serde によるシリアライズはデータ構造とデータ形式の特定の選択に対して手書きのシリアライザと同じ速度で実行されるようにすることができます。

### データ形式

**serde** は数多くのデータ形式に対応しています。以下のリストは serde に実装されているデータ形式の一部です。

- [JSON](https://github.com/serde-rs/json)
- [Postcard](https://github.com/jamesmunns/postcard)
- [CBOR](https://github.com/enarx/ciborium)
- [YAML](https://github.com/dtolnay/serde-yaml)
- [MessagePack](https://github.com/3Hren/msgpack-rust)
- [TOML](https://docs.rs/toml)
- [Pickle](https://github.com/birkenfeld/serde-pickle)
- [RON](https://github.com/ron-rs/ron)
- [BSON](https://github.com/mongodb/bson-rust)
- [Avro](https://docs.rs/apache-avro)
- [JSON5](https://github.com/callum-oakley/json5-rs)
- [URL](https://docs.rs/serde_qs)
- [Envy](https://github.com/softprops/envy)
- [Envy Store](https://github.com/softprops/envy-store)
- [S-expressions](https://github.com/rotty/lexpr-rs)
- [D-Bus](https://docs.rs/zvariant)
- [FlexBuffers](https://github.com/google/flatbuffers/tree/master/rust/flexbuffers)
- [Bencode](https://github.com/P3KI/bendy)
- [DynamoDB Items](https://docs.rs/serde_dynamo)
- [Hjson](https://github.com/Canop/deser-hjson)

### データ構造

**serde** は Rust 一般的なデータ型に対応していて、上記のデータ形式でシリアライズ・デシリアライズをすることが可能です。例えば、次のような型は全てサポートされています。

- `String`
- `&str`
- `usize`
- `Vec<T>`
- `HashMap<K,V>`

### derive マクロ

**serde** では、データ構造に対して `Serialize` および `Deserilialze` のトレイト実装を生成してくれる `derive` マクロが提供されています。これによって、serde がサポートしているデータ形式の全てで便利に表現をすることが可能になります。

この `derive` マクロを使用するためには、`Cargo.toml` のserde の依存関係でフィーチャーとして `derive` を追加する必要があります。

```shell
cargo add serde --features derive
```

```toml
[dependencies]
serde = { version = "1.0.148", features = ["derive"] }
```

## JSON 形式のシリアライズ / デシリアライズを試してみる

先にも書いていたように **serde** は様々なデータ形式をサポートしています。しかし、最初に試すのであれば一番馴染みのある **JSON** 形式を試してみようと思います。

JSON に対応したクレートとして、`serde_json` があります。

- [serde_json (crate.io)](https://crates.io/crates/serde_json)
  - [API](https://docs.rs/serde_json/latest/serde_json/)

以下のように `Cargo.toml` に `serde_json` を追加します。

```toml
[dependencies]
serde = { version = "1.0.148", features = ["derive"] }
serde_json = "1.0.89"
```

シリアライズ / デシリアライズの対象とする構造体に `#[derive(Serialize, Deserialize)]` を記述しておきます。

```rust
#[derive(Serialize, Deserialize, Debug)]
struct Point {
    x: i32,
    y: i32
}
```

### シリアライズ

`serde_json::to_string` 関数によって、与えられたデータ構造を JSON の String としてシリアライズします。

- [serde_json::to_string](https://docs.rs/serde_json/latest/serde_json/fn.to_string.html)

```rust
let point = Point { x: 1, y: 2};

let serialized = serde_json::to_string(&point).unwrap();
println!("シリアライズ: {serialized}");
```

:::details 実行結果
```
シリアライズ: {"x":1,"y":2}
```
:::

### デシリアライズ

`serde_json::from_str` 関数によって、JSON 文字列から T 型のインスタンスでデシリアライズします。

- [serde_json::from_str](https://docs.rs/serde_json/latest/serde_json/fn.from_str.html)

```rust
let deserialized: Point = serde_json::from_str(&serialized).unwrap();
println!("デシリアライズ = {:?}", deserialized);
```

## Day 75 のまとめ

**serde** を使っていて感じたのが、derive マクロがとても便利でシリアライズ・デシリアライズのトレイトをコンパイル時に自動生成してくれているので簡単のものの場合は特にマクロにまかせてしまえます。コードをシンプルに書けるのは serde の強みかなと思いました。
また、このコンパイル時に自動生成と行っても特に動的リフレクションのようなオーバーヘッドは発生しないようでした。

JSON 形式以外のデータ形式のシリアライズ・デシリアライズも試してみたいなと思いました。
