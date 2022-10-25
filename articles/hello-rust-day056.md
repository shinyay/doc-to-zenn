---
title: "100日後にRustをちょっと知ってる人になる: [Day 56]はじめての Fermyon Cloud"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: true
---
## Day 56 のテーマ

今日は2022年10月25日、ということで日本時間の昨夜未明から KubeCon + CloudNativeCon とそれの関連開催の各種カンファレンスがアメリカのデトロイトで始まりました。
昨晩はまだ KubeCon + CloudNativeCon 本体は開催されていなかったのですが、関連開催のいくとかのカンファレンスの中からぼくは **[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** を見ていました。
文字通り、Wasm、WebAssembly 関連の発表があったわけなのですが、その中には先日も少し記事化していた **Wasm Workers Server** を提供している VMware からの発表もありました。
ですが、今回一番ぼくが関心を持ったのは、正確には以前から持っていたのは、**Fermyon** (日本語的にはフェルミオンと発音) の各種発表でした。中でも **Fermyon Cloud** の発表は、ついにやってきましたね、という感じでした。

というわけで、今日は はじめての Fermyon Cloud 、という感じで触ってみたいと思います。

## Fermyon Cloud の前に

WebAssembly アプリケーションの実行環境としての **Fermyon Cloud** の前に、本来だったら Fermyon が提供している次のプロジェクトを説明しておく必要があのです。

- ✅ **Spin**
- ✅ **Fermyon Platform**

今日はそれを一旦スキップして、WebAssembly アプリケーションをビルド＆デプロイして動作する流れを紹介したいと思います。

### Spin

**Spin** は、一言で説明するならば、**WebAssembly** を使用して、アプリケーションを構築、デプロイ、実行するためのフレームワークである、といえます。
また、**Spin** は、アプリケーションの作成、配布、実行を支援する CLI を提供しています。

この **Spin** の導入の仕方や使い方などは、また今度。

### Fermyon Platform

**Fermyon Platform** は、**Spin** によるアプリケーションや、その他の互換性のある **WebAssembly** ワークロードをホストするためのプラットフォームです。

Fermyon は 動作する際につぎのソリューションを使用しています:

- [Nomad](https://www.nomadproject.io/)
- [Consul](https://consul.io/)
- [Bindle](https://github.com/deislabs/bindle)
- [Traefik](https://doc.traefik.io/traefik/)
- [Hippo](https://github.com/deislabs/hippo)

この **Fermyon Platform** についても、また今度。

## Fermyon Cloud

**Spin** をリリースした日に次のような質問があったそうです。

> ホスティングサービスはありますか？Spinはすごいと思うけど、自分でサーバーを管理したくないんです。

開発者が自分のインフラをセットアップする必要がなくなると、もっと楽しい経験をすることができるはずだ、というモチベーションから **Fermyon Cloud** は生まれたそうです。

**Fermyon Cloud** は、**Spin** による Webアプリケーションを実行するためのプラットフォームです。
また、**Fermyon Cloud** のダッシュボードにログインして、アプリケーションの確認、ログファイルの閲覧、デプロイメントの管理を行うことができます。

この **Fermyon Cloud** が **Spin** アプリケーションを動作させるというところから想像できると思いますが、**Fermyon Cloud** は **Fermyon Platform** の上に構築されています。

- リリース管理: **Bindle**
- スケジューリング: **Nomad**
など

## Fermyon Cloud へのアプリケーションデプロイ

繰り返しますが、**Spin** についての詳細な説明は今回はしませんので、そういうものだと思ってください。

### 0. テンプレートの取得

初めて Spin を使う場合、プロジェクトテンプレートが存在しないので、取得を行います。

```shell
spin templates install --git https://github.com/fermyon/spin
```

```shell
Copying remote template source
Installing template redis-rust...
Installing template http-grain...
Installing template http-swift...
Installing template http-c...
Installing template http-rust...
Installing template http-go...
Installing template http-zig...
Installing template redis-go...
Installed 8 template(s)

+-----------------------------------------------------------------+
| Name         Description                                        |
+=================================================================+
| http-c       HTTP request handler using C and the Zig toolchain |
| http-go      HTTP request handler using (Tiny)Go                |
| http-grain   HTTP request handler using Grain                   |
| http-rust    HTTP request handler using Rust                    |
| http-swift   HTTP request handler using SwiftWasm               |
| http-zig     HTTP request handler using Zig                     |
| redis-go     Redis message handler using (Tiny)Go               |
| redis-rust   Redis message handler using Rust                   |
+-----------------------------------------------------------------+
```

### 1. Spin プロジェクトの作成

`spin` CLI を使って次のコマンドで Spin プロジェクトを作成します。

`spin new <テンプレート名> <プロジェクト名>`

ここでは、Rust のプロジェクトを作成します。

```shell
spin new http-rust hello-rust
```

以下、対話式のオプション入力です。

```shell
Project description: Sping Getting Started
HTTP base: /
HTTP path: /...
```

### 2. 生成された Rust コード

以下のコードが自動生成されます:

- **lib.rs**
- **Cargo.toml**
- **spin.toml**


ライブラリクレートのコード(`lib.rs`):

```rust
use anyhow::Result;
use spin_sdk::{
    http::{Request, Response},
    http_component,
};

/// A simple Spin HTTP component.
#[http_component]
fn hello_rust(req: Request) -> Result<Response> {
    println!("{:?}", req.headers());
    Ok(http::Response::builder()
        .status(200)
        .header("foo", "bar")
        .body(Some("Hello, Fermyon".into()))?)
}
```

`Cargo.toml`

```toml
[package]
name = "hello-rust"
authors = ["shinyay <shinya.com@gmail.com>"]
description = "Sping Getting Started"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = [ "cdylib" ]

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

[workspace]
```

`spin.toml`:

```toml
spin_version = "1"
authors = ["shinyay <shinyay@abc.xyz>"]
description = "Sping Getting Started"
name = "hello-rust"
trigger = { type = "http", base = "/" }
version = "0.1.0"

[[component]]
id = "hello-rust"
source = "target/wasm32-wasi/release/hello_rust.wasm"
[component.trigger]
route = "/..."
[component.build]
command = "cargo build --target wasm32-wasi --release"
```

### 3. Spin アプリケーションのビルド

作成したアプリケーションのディレクトリに異動し、`spin` CLI を使って次のコマンドででビルドします:

```shell
spin build
```

```shell
Executing the build command for component hello-rust: cargo build --target wasm32-wasi --release
   Compiling version_check v0.9.4
   Compiling anyhow v1.0.66
   Compiling memchr v2.5.0
   Compiling pulldown-cmark v0.8.0
   Compiling tinyvec_macros v0.1.0
   Compiling proc-macro2 v1.0.47
   Compiling bitflags v1.3.2
   Compiling quote v1.0.21
   Compiling unicode-xid v0.2.4
   Compiling id-arena v2.2.1
   Compiling unicode-ident v1.0.5
   Compiling syn v1.0.103
   Compiling unicode-segmentation v1.10.0
   Compiling wit-bindgen-gen-rust-wasm v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling async-trait v0.1.58
   Compiling bytes v1.2.1
   Compiling fnv v1.0.7
   Compiling itoa v1.0.4
   Compiling percent-encoding v2.2.0
   Compiling tinyvec v1.6.0
   Compiling form_urlencoded v1.1.0
   Compiling heck v0.3.3
   Compiling unicase v2.6.0
   Compiling http v0.2.8
   Compiling unicode-normalization v0.1.22
   Compiling wit-parser v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling wit-bindgen-gen-core v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling wit-bindgen-gen-rust v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling wit-bindgen-rust-impl v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling wit-bindgen-rust v0.2.0 (https://github.com/bytecodealliance/wit-bindgen?rev=cb871cfa1ee460b51eb1d144b175b9aab9c50aba#cb871cfa)
   Compiling spin-macro v0.1.0 (https://github.com/fermyon/spin?tag=v0.6.0#12a50379)
   Compiling spin-sdk v0.6.0 (https://github.com/fermyon/spin?tag=v0.6.0#12a50379)
   Compiling hello-rust v0.1.0 (/Users/yanagiharas/Works/docs/doc-to-zenn/codes/day_56_fermyon-cloud/hello-rust)
    Finished release [optimized] target(s) in 11.43s
Successfully ran the build command for the Spin components.
```

### 4. Fermyon Cloud へのログイン

`spin` CLI を使って次のコマンドで **Fermyon Cloud** にログインします。

```shell
spin login
```

```shell
Copy your one-time code:

ABCDEFGH

...and open the authorization page in your browser:

https://cloud.fermyon.com/device-authorization

Waiting for device authorization...
Waiting for device authorization...
Waiting for device authorization...
Waiting for device authorization...
Waiting for device authorization...
Device authorized!
```

### 4. Fermyon Cloud へのデプロイ

`spin` CLI を使って次のコマンドでビルドしたアプリケーションを **Fermyon Cloud** にデプロイします。

```shell
spin deploy
```

```shell
Uploading hello-rust version 0.1.0+r5cc7a066...
Deploying...
Waiting for application to become ready........ ready
Available Routes:
  hello-rust: https://hello-rust-abcdefgh.fermyon.app (wildcard)
```

### 4. Fermyon Cloud のアプリケーションにアクセス

まず、**Fermyon Cloud** のダッシュボードにアクセスします。

- ダッシュボード
  - <https://cloud.fermyon.com/>

![](https://storage.googleapis.com/zenn-user-upload/a7debc624e8b-20221025.png)

次に、ダッシュボードから表示されているデプロイしたアプリケーション `hello-rust` をクリックするか、または `spin deploy` の実行時に表示されていた **Available Routes** にアクセスします。

**Hello, Fermyon** と表示されているアプリケーションにアクセスが出来ました。

![](https://storage.googleapis.com/zenn-user-upload/9ca2643f5cb8-20221025.png)

## Day 56 のまとめ

今回は、今日開催された **[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** でアナウンスされた **Fermyon Cloud** について紹介しました。
実際の細かなアプリケーションの作成に関わる、**Spin** などは今回の説明からは割愛しましたけれど流れは分かったと思います。

WebAssembly のソースを作った後、ビルドをしてからのデプロイまでの流れの中で、生成された WebAssembly のイメージについて特に意識することもなかったと思います。

このように、**Fermyon Cloud**、そして **Spin** を使うと WebAssembly であることを忘れてしまいそうなくらいのコード作成へのフォーカスができることが分かったと思います。
今後この Fermyon Cloud を使っての Rust アプリケーション開発について詳細にみていきたいと思います。
