---
title: "100日後にRustをちょっと知ってる人になる: [Day 57]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 57 のテーマ

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056) では、**[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** で発表のあった **Fermyon Cloud** について使い方とシンプルなアプリケーションの作成＆デプロイの流れを見てみました。
しかし、流れを見ただけであって、実際には "何"をしているのかまでは説明を割愛していたところがあります。そこで、今日以降の中で **Fermyyon** のソリューションについて少し眺めつつ、それが Rust によるアプリケーションと組み合わせの効果がどのようにあるのか、そんなところを考えていきたいと思います。


さて、Day 56 で次のように伝えて居たと思います:

>WebAssembly アプリケーションの実行環境としての **Fermyon Cloud** の前に、本来だったら Fermyon が提供している次のプロジェクトを説明しておく必要があるのです。
>
>- ✅ **Spin**
>- ✅ **Fermyon Platform**

ということで、今日は **Spin** について少し見ていきたいと思います。

## Spin

**[Spin](https://github.com/fermyon/spin)** は WebAssembly コンポーネントを用いてイベント・ドリブンなサーバーサイド アプリケーションを作り、そして動かすためのフレームワークです。つまり、HTTP リクエストに対してレスポンスを返すような機能を持つ WebAssembly モジュールを書くためのインターフェースを提供するが、**Spin** なのです。

また、この **Spin** の注目すべき点は、多言語フレームワークであることです。**WebAssembly** と耳にすると、**Rust** や **Go** を思い浮かべるかもしれません。Spin ではもちろん Rust と Go をサポートしていますが、それ以外の言語もサポートをしています。

- サポート言語
  - Rust
  - Go
  - C/C++
  - Python
  - Ruby
  - AssemblyScript
    - <https://www.assemblyscript.org/>
  - Grain
    - <https://grain-lang.org/>
  - Zig
    - <https://ziglang.org/>
  - C#
  - その他 .NET 言語 (F# など)

## Spin のインストール

**Spin** をインストールしてみます。

現在 Spin は、以下の環境で動作をします。

- Linux (amd64)
- macOS (Intel)
- macOS (Apple Silicon)
- Windows with WSL2 (amd64)

それらの環境で以下を実行して Spin をカレントディレクトリに取得します。

```shell
curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash
```

そして、必要に応じてパスの通っている `/usr/local/bin/` ディレクトリに移動させます。

```shell
sudo mv spin /usr/local/bin/
```

インストール作業は以上です。

```shell
spin --help
```

```shell
spin 0.6.0 (12a5037 2022-10-21)
The Spin CLI

USAGE:
    spin <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    bindle       Commands for publishing applications as bindles
    build        Build the Spin application
    deploy       Deploy a Spin application
    help         Print this message or the help of the given subcommand(s)
    login        Log into the server
    new          Scaffold a new application or component based on a template
    plugin       Install/uninstall Spin plugins
    templates    Commands for working with WebAssembly component templates
    up           Start the Spin application
```

### Cargo による Spin のインストール

Rust のパッケージマネージャーとして使われるツールの、`cargo` を使用してインストールすることも可能です。
以下のコマンドを実行することでインストールが行われます。

```shell
git clone https://github.com/fermyon/spin -b v0.6.0
cd spin
rustup target add wasm32-wasi
cargo install --locked --path .
```

## Spin によるアプリケーション開発

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056#1.-spin-%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE%E4%BD%9C%E6%88%90) でもサンプルアプリケーションを作ってみましたが、あらためて作り方をおさらいします。

以下のコマンドでプロジェクトテンプレートを作成します。

`spin new <テンプレート名> <プロジェクト名>`

現在テンプレートとしては以下のものがあります。

| 名前         |説明                                               |
|-------------|---------------------------------------------------|
| http-c       |HTTP request handler using C and the Zig toolchain |
| http-go      |HTTP request handler using (Tiny)Go                |
| http-grain   |HTTP request handler using Grain                   |
| http-rust    |HTTP request handler using Rust                    |
| http-swift   |HTTP request handler using SwiftWasm               |
| http-zig     |HTTP request handler using Zig                     |
| redis-go     |Redis message handler using (Tiny)Go               |
| redis-rust   |Redis message handler using Rust                   |

### http-rust テンプレートによるアプリケーション作成

`spin new` コマンドによりプロジェクトを作成します。

```shell
spin new

Pick a template to start your project with:
  http-c (HTTP request handler using C and the Zig toolchain)
  http-go (HTTP request handler using (Tiny)Go)
  http-grain (HTTP request handler using Grain)
> http-rust (HTTP request handler using Rust)
  http-swift (HTTP request handler using SwiftWasm)
  http-zig (HTTP request handler using Zig)
  redis-go (Redis message handler using (Tiny)Go)
  redis-rust (Redis message handler using Rust)
```

```shell
Pick a template to start your project with: http-rust (HTTP request handler using Rust)
Enter a name for your new project: hello-spin-rust
Project description: はじめてのSpin
HTTP base: /
HTTP path: /...
```

次のような階層でファイルが生成されます。

```shell
hello-spin-rust
├── Cargo.toml
├── spin.toml
└── src
   └── lib.rs
```

#### spin.toml

**Spin** アプリケーションのマニフェストになる、`spin.toml` が以下のような内容で生成されています。

```toml
spin_version = "1"
authors = ["shinyay <shinya.com@gmail.com>"]
description = "はじめてのSpin"
name = "hello-spin-rust"
trigger = { type = "http", base = "/" }
version = "0.1.0"

[[component]]
id = "hello-spin-rust"
source = "target/wasm32-wasi/release/hello_spin_rust.wasm"
[component.trigger]
route = "/hello"
[component.build]
command = "cargo build --target wasm32-wasi --release"
```

このマニフェストに記載されている内容でポイントになるのは次の 2 点です：

- `source = "target/wasm32-wasi/release/hello_spin_rust.wasm"`
- `route = "/hello"`

まず `source` では、Spin が実行対象とする **WebAssembly** モジュールが指定されています。
次に `route` が WebAssembly モジュールが HTTP リクエストを受け付けるエンドポイントのアクセスルートです。

#### Cargo.toml

この Spin アプリケーションプロジェクトのデフォルトで定義されている Dependencies をみてみます。

```toml
[dependencies]
# Useful crate to handle errors.
anyhow = "1"
# Crate to simplify working with bytes.
bytes = "1"
# General-purpose crate with common HTTP types.
http = "0.2"
# The Spin SDK.
spin-sdk = { git = "https://github.com/fermyon/spin", tag = "v0.6.0" }
# Crate that generates Rust Wasm bindings from a WebAssembly interface.
wit-bindgen-rust = { git = "https://github.com/bytecodealliance/wit-bindgen", rev = "cb871cfa1ee460b51eb1d144b175b9aab9c50aba" }
```

以下の 5 つの Dependency が設定されていました。

- `anyhow`
- `bytes`
- `http`
- `spin-sdk`
- `wit-bindgen-rust`

#### lib.rs

モジュールのコードを見てみます。

```rust
use anyhow::Result;
use spin_sdk::{
    http::{Request, Response},
    http_component,
};

/// A simple Spin HTTP component.
#[http_component]
fn hello_spin_rust(req: Request) -> Result<Response> {
    println!("{:?}", req.headers());
    Ok(http::Response::builder()
        .status(200)
        .header("foo", "bar")
        .body(Some("Hello, Fermyon".into()))?)
}
```

一件したところ、そこまで珍しいコード構成にはなっていないことが分かると思います。一般的な `http` クレートを使用したアプリケーションコードとほぼ変わらないと感じると思います。

- [Crate http](https://docs.rs/http/latest/http/)

ポイントになるのは、`http_component` マクロが付いている、というところです。
これが、Spin アプリケーションを作っていく上での大事なマクロだということを覚えておいてください。

## Spin によるアプリケーションビルド

`spin build` コマンドにより、`spin.toml` に定義したコマンドを実行してビルドを実施します。
このケースでは実行されるコマンド内容は次のものになります。

```shell
cargo build --target wasm32-wasi --release
```

つまり、環境には予め `wasm32-wasi` ターゲットが必要だということが分かります。
インストールについては、以下の記事にて紹介をしています、

- [Day 20: wasm32-wasi ターゲットのインストール](https://zenn.dev/shinyay/articles/hello-rust-day020#wasm32-wasi-%E3%82%BF%E3%83%BC%E3%82%B2%E3%83%83%E3%83%88%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)

## Day 57 のまとめ
