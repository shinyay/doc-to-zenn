---
title: "100日後にRustをちょっと知ってる人になる: [Day 53]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 53 のテーマ

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) 〜 [Day 52](https://zenn.dev/shinyay/articles/hello-rust-day052) と **[Wasm Workers Server](https://github.com/vmware-labs/wasm-workers-server)** について見てみました。

WebAssembly を用いたサーバーレスなアプリケーションを動作させる HTTP サーバーの導入、そしてサーバーレスなアプリケーションな **ハンドラ** の作成を行い、実際に動かしてみました。

さて、この **Wasm Workers Server** の目指しているコンセプトは、**互換性**と**シンプルさ**でした。そのため、作成するワーカーは互換性ある標準準拠したものになります。

Rust によるハンドラを作成する場合、**[wasm-workers-server-kit](https://github.com/vmware-labs/wasm-workers-server/tree/main/examples#rust-handlers)** クレートを使用する必要があります。今回は、この**wasm-workers-server-kit** について見てみようと思います。

## wasm-workers-server-kit クレート

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) と [Day 52](https://zenn.dev/shinyay/articles/hello-rust-day052) で作成したワーカーの中で、次のクレートを依存関係に追加しました。

- `wasm-workers-rs = { git = "https://github.com/vmware-labs/wasm-workers-server/" }`

そのリポジトリに配置され参照している `Cargo.toml` を確認してみます。

```toml
[package]
name = "wasm-workers-server"
version = "0.5.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[[bin]]
name = "wws"
path = "src/main.rs"

[dependencies]
wasmtime = "1.0.1"
wasmtime-wasi = "1.0.1"
anyhow = "1.0.63"
wasi-common = "1.0.1"
actix-web = "4"
env_logger = "0.9.0"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0.85"
glob = "0.3.0"
toml = "0.5.9"
clap = { version = "4.0.10", features = ["derive"] }

[workspace]
members = [
  "kits/rust",
  "kits/rust/handler",
  "kits/javascript"
]
# Exclude examples
exclude = [
  "examples/rust-basic",
  "examples/rust-kv"
]
```

## Day 53 のまとめ
