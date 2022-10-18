---
title: "100日後にRustをちょっと知ってる人になる: [Day 50]Wasm Workers Server"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 50 のテーマ

折返し地点の Day 50 になりました。思い返せば、Rust を勉強し始めた理由は **WebAssembly** を知ってる人になろうと思いはじめ、だったら Rust を知っておいた方が良さそうだ、という軽い気持ちでした。

今日はその動機のきっかけになった WebAssembly についてあらためて見てみようと思います。
というのも、ちょうど VMware がオープンソースのプロジェクトで **Wasm Worker Server** というものを今日発表したのです。その触ってみた内容をすこしまとめようと思います。

## Wasm Worker Server

まず最初に、この **Wasm Worker Server** が何かを説明します。
一言で言い表すならば、サーバーレスの仕組みを提供するプロジェクトです。ただし、サーバーレスとして動作させる対象のワークロードは、**ワーカー (Worker)** と呼ばれる軽量な構成で組み上げられたものになります。

そして、この**Wasm Worker Server**自体は自己完結型のバイナリとして実装されています。
これが単独で、ワーカーをホストしている WebAssembly ランタイムに対して HTTP リクエストをルーティングをします。

- [GitHub Repository](https://github.com/vmware-labs/wasm-workers-server)

### ワーカー (Worker)

継承な構成と紹介した**ワーカー (Worker)** ですが、これは**HTTP リクエストを受信して HTTP レスポンスを返すスクリプトまたは関数のこと**を指しています。
アプリケーション全体としては、このワーカーを複数組み合わせて開発することが可能です。それぞれのワーカーが特定のイベントをリッスンし、それに対する応答を提供します。アプリケーションを小さく分割した Microservices ならぬ **Nanoservices** と言えるようなもとも考えてもいいかもしれません。

このワーカーによる開発モデルはいくつかメリットが考えられます。

- 🧑‍💻 容易な開発: より小さくより集中できるように設計可能
- 🛠 容易なテスト: ワーカー毎に個別にテスト可能
- 🚀 容易なデプロイ: シンプルなコマンド 1 つでデプロイ可能

## Wasm Workers Server の始め方

以下ののようにシェルを実行し、**Wasm Workers Server** (`wws`) をインストールします。

```shell
curl https://raw.githubusercontent.com/vmware-labs/wasm-workers-server/main/install.sh | bash
```

正常にインストールできると、以下のようにヘルプを実行して使い方を確認してみましょう。

```shell
wws --help
```

```shell
Usage: wws [OPTIONS] [PATH]

Arguments:
  [PATH]  Folder to read WebAssembly modules from [default: .]

Options:
      --host <HOSTNAME>  Hostname to initiate the server [default: 127.0.0.1]
  -p, --port <PORT>      Port to initiate the server [default: 8080]
  -h, --help             Print help information
  -V, --version          Print version information
```

ヘルプを見ると非常に簡単なことが分かると思います。`wws <対象のワーカー>` これだけで起動します。

## はじめての Rust ワーカー

**Wasm Worker Server** だけがあっても仕方がないので、ワーカーを作ってみたいと思います。
ただ、今日はチュートリアルに従って作り方を見ていこうと思います。

### Dependencies

以下の 2 つを追加しています。

- [anyhow](https://docs.rs/anyhow/latest/anyhow/)
- [wasm-workers-rs](https://github.com/vmware-labs/wasm-workers-server)

```toml
[dependencies]
anyhow = "1.0.65"
wasm-workers-rs = { git = "https://github.com/vmware-labs/wasm-workers-server/" }
```

#### anyhow

`anyhow` は [Day 49](https://zenn.dev/shinyay/articles/hello-rust-day049) で扱った**エラー処理**を使いやすくするためのクレートです。`anyhow::Error` を使うことでエラー処理を簡単に扱えるようになります。

- [anyhow(https://crates.io/crates/anyhow)

今日は、`anyhow` の使い方ではなく、ワーカーを作ることをまず第一にしたいので内容はスキップします。
ただ、この `anyhow` はエラー処理を行う際のデファクトなクレートとも言われているので、改めて使い方は確認しておきたいと思います。

#### wasm-workers-rs

`wasm-workers-rs` は GitHub リポジトリを参照しています。参照先の `https://github.com/vmware-labs/wasm-workers-server/` の直下に配備されている `Cargo.toml` を取得しています。

`wasm-workers-server` のバージョン `0.5.0` では、以下のような依存関係が定義されています。

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

`wasmtime` や `wasi-common` などの WebAssembly ランタイムが含まれていることが確認できます。また、Web フレームワークの `actix-web` も含まれています。

なお、`Cargo.toml` では、以下のような書式により依存関係で **GitHub リポジトリ**を指定する事が可能になっています。
wasm-workers-rs = { git = "https://github.com/vmware-labs/wasm-workers-server/" }

## Day 50 のまとめ
