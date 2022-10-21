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

今回
```rust
#[handler]
fn reply(req: Request<String>)
```

前回
```rust
#[handler(cache)]
fn reply(req: Request<String>)
```

ハンドラマクロのパラメータに `cache` 属性を付けるかどうかです。

## Day 52 のまとめ
