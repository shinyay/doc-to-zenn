---
title: "100日後にRustをちょっと知ってる人になる: [Day 52]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 52 のテーマ

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) そして [Day 51](https://zenn.dev/shinyay/articles/hello-rust-day051) と **Wasm Workers Server** の最もシンプルな基本動作をするアプリケーションについて眺めてみました。

とは言え、基本動作の中でもまだふれていない機能が **Wasm Workers Server** にはあります。標準機能として、**キー/バリューのインメモリストア**を提供しています。

今日は、その キー/バリューストアについて見てみたいと思います。

## キー/バリューストア

キー/バリューストアとは、文字通りキーとそのキーに対する値からなるデータ構造を保管するためのストレージです。ハッシュテーブルとしてよく知られているデータ構造ですよね。**Redis**, **Memcached** や **MongoDB** などが有名ですね。

さて、**Wasm Workers Server**で提供しているキー/バリューストアは、Wasm Wokers Server がまだまだ進化中ということもあり有名な NoSQL のようなリッチな機能は搭載していません。そこは今後に期待ですね。
現在のところは、メモリ上にデータを保管し、再起動するたびにデータ内容はクリーンアップされるようになっています。永続化はまだできません。
制約事項としても予め言われていることがあります:
同時リクエストで同じネームスペースに書き込む場合にデータがオーバーライドされるということです。これは、将来的にはデータ統合の仕組みや別のデータ保存の仕組みによる実装で、大量の書き込みに対しても対応していく予定になっています。

- [Limitations](https://workers.wasmlabs.dev/docs/features/key-value#limitations)

しかし、とは言ってもシンプルながらもこのキー/バリューストアがあることによって、異なるワーカー同士からの読み書きをキー/バリューストア介して行うことができるようになります。

## キー/バリューストアを用いたワーカー

それでは、キー/バリューストアを用いたワーカーを作成してみようと思います。チュートリアルに即して作るだけなのですけれどね…

### Dependencies

先日の超シンプルなレスポンスをかえすだけのアプリケーションの時と同じく以下を Dependency に追加します。

- `anyhow = "1.0.65"`
- `wasm-workers-rs = { git = "https://github.com/vmware-labs/wasm-workers-server/" }`

### Reply 関数

受け取ったリクエストに対してレスポンスを返すだけの `reply` 関数を定義します。

```rust
use anyhow::Result;
use wasm_workers_rs::{handler, http::{self, Request, Response}, cache::Cache};

#[handler(cache)]
fn reply(req: Request<String>, cache: &mut Cache) -> Result<Response<String>> {
    Ok(http::Response::builder()
        .status(200)
        .header("x-generated-by", "wasm-workers-server")
        .body(String::from("Hello Wasm!").into())?)
}
```

Day 50 の時と異なるのは次の 1点です。

今回:

```rust
#[handler]
fn reply(req: Request<String>)
```

前回:

```rust
#[handler(cache)]
fn reply(req: Request<String>)
```

ハンドラマクロのパラメータに `cache` 属性を付けるかどうかです。

#### Cache

Cache を見てみます。

```rust
use std::collections::HashMap;
pub type Cache = HashMap<String, String>;
```

文字通り、`HashMap` データ構造を提供しているものでした。

### キー/バリューストアを用いたレスポンス

キー/バリューストアを用いてカウントアップを行います。
まず、`hashmap` のキーとして、**counter** という文字列を使うことにします。

```rust
let count = cache.get("counter");
```

次に、列挙型な `Option` 型を利用します。`Option` 型は**値が存在しないかもしれない**ときに使用する列挙型です。
定義は次のようになっています。

```rust
enum Option<T> {
    None,
    Some(T),
}
```

`T` 型 (今回の例では `String` 型) が存在するときには、`Some` でラップします。
一方で値が存在しない場合は、`None` になります。

```rust
let count_num = match count {
    Some(count_str) => count_str.parse::<u32>().unwrap_or(0),
    None => 0,
};
```

`Some(count_str) => count_str.parse::<u32>().unwrap_or(0)` では、カウント数の文字列を `u32` な数値にパースし、`unwrap` して値を取り出しています。ここで、デフォルト値としては、`0` を与える `unwrap_or()` メソッドが使用されています。

- [`pub fn unwrap_or(self, default: T) -> T`](https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap_or)

取り出した値は、`reply` 関数が呼ばれるたびにカウントアップしています。

```rust
cache.insert("counter".to_string(), (count_num + 1).to_string());
```

## Day 52 のまとめ
