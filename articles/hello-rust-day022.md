---
title: "100日後にRustをちょっと知ってる人になる: [Day 22]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 22 のテーマ

この数日間、Rust の観点から **WebAssembly** について見てきています。
この WebAssembly ですが、**WASI** の仕様ではブラウザ以外でも動くことを目的としていますが、もちろん WebAssembly 自体はブラウザ上でポータブルかつ安全に動作することを目的として誕生してきています。ブラウザ上でアプリケーションを動かすというと、**JavaScript** を思い浮かべると思います。では、WebAssembly が目指しているのは JavaScript の置き換えなのでしょうか？

次の記事に興味深い記述がありました。

- [Making WebAssembly better for Rust & for all languages](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/)

> **WebAssembly** は **JavaScript** に取って代わるものではなく、JavaScriptと一緒に使う素晴らしいツールになることを目指しています。

**WebAssembly** を介して、Rust と JavaScript の間で次のようなことが実現できるようになることが望まれているということなのです。

- Rust 開発者は、**Node.js 開発環境を必要とせず**に JavaScript で使用する WebAssembly パッケージを作成できる
- JavaScript 開発者は、**Rust 開発環境を必要とせず**に WebAssembly を使用できる

![](https://storage.googleapis.com/zenn-user-upload/6d2e5411eed5-20220914.png)

## wasm-pack

![](https://storage.googleapis.com/zenn-user-upload/ddd18f0b3f3c-20220914.png)

**wasm-pack** は WebAssembly をターゲットとする Rust クレートを組み立て、パッケージ化するためのツールです。これらのパッケージはnpmレジストリに公開され、他のパッケージと一緒に使用することができます。つまり、JSや他のパッケージと並べて使うことができ、様々な種類のアプリケーションで使うことができます。

- [wasm-pack](https://github.com/rustwasm/wasm-pack)

### wasm-pack インストール

次のシェルでインストールを行います。

```shell
curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
```

:::details wasm-pack -h
```shell
wasm-pack 0.10.3
The various kinds of commands that `wasm-pack` can execute

USAGE:
    wasm-pack [FLAGS] [OPTIONS] <SUBCOMMAND>

FLAGS:
    -h, --help       Prints help information
    -q, --quiet      No output printed to stdout
    -V, --version    Prints version information
    -v, --verbose    Log verbosity is based off the number of v used

OPTIONS:
        --log-level <log-level>    The maximum level of messages that should be logged by wasm-pack. [possible values:
                                   info, warn, error] [default: info]

SUBCOMMANDS:
    build      🏗️  build your npm package!
    help       Prints this message or the help of the given subcommand(s)
    login      👤  Add an npm registry user account! (aliases: adduser, add-user)
    new        🐑 create a new project with a template
    pack       🍱  create a tar of your npm package but don't publish!
    publish    🎆  pack up your npm package and publish!
    test       👩‍🔬  test your wasm!
```
:::

|サブコマンド|説明|
|----------|---|
|build   |NPM パッケージのビルド|
|help    |ヘルプメッセージの表示|
|login   |NPM レジストリにユーザーアカウントを追加|
|new     |プロジェクトテンプレートの新規作成|
|pack    |NPM パッケージの TAR を作成 (公開はしない)|
|publish |NPM パッケージの公開|
|test    |WASM のテスト|

### wasm-pack のクイックスタート

まずは `wasm-pack` の動きを確認してみたいと思います。

#### プロジェクトテンプレートの作成

`hello-wasm` という名前のプロジェクトを作成します。

```shell
wasm-pack new hello-wasm
```

:::details 実行結果
```shell
[INFO]: ⬇️  Installing cargo-generate...
🐑  Generating a new rustwasm project with name 'hello-wasm'...
🔧   Creating project called `hello-wasm`...
✨   Done! New project created /Users/yanagiharas/Works/hello-wasm
[INFO]: 🐑 Generated new project at /hello-wasm
```
:::

以下のような構成でプロジェクトテンプレートが生成されます。

```shell
hello-wasm
├── Cargo.toml
├── LICENSE_APACHE
├── LICENSE_MIT
├── README.md
├── src
│  ├── lib.rs
│  └── utils.rs
└── tests
   └── web.rs
```

自動生成されたソースコードは後ほどみてみることにして、とりあえずビルドしてみます。

### wasm-pack のビルド

プロジェクトテンプレートのルートディレクトリで以下のコマンドを実行します。

```shell
wasm-pack build
```

:::details 実行結果
```shell
[INFO]: 🎯  Checking for the Wasm target...
info: downloading component 'rust-std' for 'wasm32-unknown-unknown'
info: installing component 'rust-std' for 'wasm32-unknown-unknown'
 16.4 MiB /  16.4 MiB (100 %)  15.2 MiB/s in  1s ETA:  0s
[INFO]: 🌀  Compiling to Wasm...
   Compiling proc-macro2 v1.0.43
   Compiling unicode-ident v1.0.4
   Compiling quote v1.0.21
   Compiling wasm-bindgen-shared v0.2.83
   Compiling log v0.4.17
   Compiling syn v1.0.99
   Compiling cfg-if v1.0.0
   Compiling once_cell v1.14.0
   Compiling bumpalo v3.11.0
   Compiling wasm-bindgen v0.2.83
   Compiling wasm-bindgen-backend v0.2.83
   Compiling wasm-bindgen-macro-support v0.2.83
   Compiling wasm-bindgen-macro v0.2.83
   Compiling console_error_panic_hook v0.1.7
   Compiling hello-wasm v0.1.0 (/Users/yanagiharas/Works/hello-wasm)
warning: function `set_panic_hook` is never used
 --> src/utils.rs:1:8
  |
1 | pub fn set_panic_hook() {
  |        ^^^^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: `hello-wasm` (lib) generated 1 warning
    Finished release [optimized] target(s) in 12.02s
[INFO]: ⬇️  Installing wasm-bindgen...
[INFO]: Optimizing wasm binaries with `wasm-opt`...
[INFO]: Optional fields missing from Cargo.toml: 'description', 'repository', and 'license'. These are not necessary, but recommended
[INFO]: ✨   Done in 0.34s
[INFO]: 📦   Your wasm pkg is ready to publish at /Users/yanagiharas/Works/hello-wasm/pkg.
```
:::

実行結果の以下の箇所を見てもらえると分かるように、**wasm32-unknown-unknown** ターゲットを使用してコンパイルを行っていますね。

```shell
info: installing component 'rust-std' for 'wasm32-unknown-unknown'
```

`rustup` コマンドでも確認してみましたが、自動で**wasm32-unknown-unknown**ダウンロードされていますね。

```shell
rustup show

:
installed targets for active toolchain
--------------------------------------

wasm32-unknown-unknown
:
```

以下のような構成に成果物が生成されます。

:::details 成果物構成
```shell
hello-wasm
├── Cargo.lock
├── Cargo.toml
├── LICENSE_APACHE
├── LICENSE_MIT
├── pkg
│  ├── hello_wasm.d.ts
│  ├── hello_wasm.js
│  ├── hello_wasm_bg.js
│  ├── hello_wasm_bg.wasm
│  ├── hello_wasm_bg.wasm.d.ts
│  ├── package.json
│  └── README.md
├── README.md
├── src
│  ├── lib.rs
│  └── utils.rs
├── target
│  ├── CACHEDIR.TAG
│  ├── debug
│  │  ├── build
│  │  │  ├── log-c4086c545319cba9
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-c4086c545319cba9
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.0.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.1.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.2.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.3.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.4.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.5.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.6.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.7.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.8.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.9.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.10.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.11.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.12.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.13.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.14.rcgu.o
│  │  │  │  ├── build_script_build-c4086c545319cba9.build_script_build.ab37a428-cgu.15.rcgu.o
│  │  │  │  └── build_script_build-c4086c545319cba9.d
│  │  │  ├── log-f76e1d0e5fe37622
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── proc-macro2-3cbed03846fcf761
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── proc-macro2-7b299ca0eb78d931
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-7b299ca0eb78d931
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.0.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.1.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.2.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.3.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.4.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.5.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.6.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.7.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.8.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.9.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.10.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.11.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.12.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.13.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.14.rcgu.o
│  │  │  │  ├── build_script_build-7b299ca0eb78d931.build_script_build.c86a9a86-cgu.15.rcgu.o
│  │  │  │  └── build_script_build-7b299ca0eb78d931.d
│  │  │  ├── quote-129c06d561223642
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-129c06d561223642
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.0.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.1.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.2.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.3.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.4.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.5.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.6.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.7.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.8.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.9.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.10.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.11.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.12.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.13.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.14.rcgu.o
│  │  │  │  ├── build_script_build-129c06d561223642.build_script_build.b7840aa5-cgu.15.rcgu.o
│  │  │  │  └── build_script_build-129c06d561223642.d
│  │  │  ├── quote-fea490db2b282146
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── syn-06dea51dce6ae702
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── syn-218b09b4fcb49b40
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-218b09b4fcb49b40
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.0.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.1.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.2.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.3.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.4.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.5.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.6.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.7.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.8.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.9.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.10.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.11.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.12.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.13.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.14.rcgu.o
│  │  │  │  ├── build_script_build-218b09b4fcb49b40.build_script_build.c372d88a-cgu.15.rcgu.o
│  │  │  │  └── build_script_build-218b09b4fcb49b40.d
│  │  │  ├── wasm-bindgen-5b3a79ad4436b3f1
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── wasm-bindgen-33c6ee5785c7cd44
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.0.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.1.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.2.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.3.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.4.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.5.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.6.rcgu.o
│  │  │  │  ├── build_script_build-33c6ee5785c7cd44.build_script_build.b6144499-cgu.7.rcgu.o
│  │  │  │  └── build_script_build-33c6ee5785c7cd44.d
│  │  │  ├── wasm-bindgen-shared-b984bd3bf814ed17
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  └── wasm-bindgen-shared-f6e8d53f593934cc
│  │  │     ├── build-script-build
│  │  │     ├── build_script_build-f6e8d53f593934cc
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.0.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.1.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.2.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.3.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.4.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.5.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.6.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.7.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.8.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.9.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.10.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.11.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.12.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.13.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.14.rcgu.o
│  │  │     ├── build_script_build-f6e8d53f593934cc.build_script_build.01c749de-cgu.15.rcgu.o
│  │  │     └── build_script_build-f6e8d53f593934cc.d
│  │  ├── deps
│  │  │  ├── bumpalo-b655b6eae049e475.d
│  │  │  ├── cfg_if-bc9c12dc3576a706.d
│  │  │  ├── libbumpalo-b655b6eae049e475.rlib
│  │  │  ├── libbumpalo-b655b6eae049e475.rmeta
│  │  │  ├── libcfg_if-bc9c12dc3576a706.rlib
│  │  │  ├── libcfg_if-bc9c12dc3576a706.rmeta
│  │  │  ├── liblog-7e5c333038904839.rlib
│  │  │  ├── liblog-7e5c333038904839.rmeta
│  │  │  ├── libonce_cell-a2b9bd79df042177.rlib
│  │  │  ├── libonce_cell-a2b9bd79df042177.rmeta
│  │  │  ├── libproc_macro2-d53d1e09b7eb3f23.rlib
│  │  │  ├── libproc_macro2-d53d1e09b7eb3f23.rmeta
│  │  │  ├── libquote-d5ab5f6d2ab29cd6.rlib
│  │  │  ├── libquote-d5ab5f6d2ab29cd6.rmeta
│  │  │  ├── libsyn-a0a2cf75bac9b939.rlib
│  │  │  ├── libsyn-a0a2cf75bac9b939.rmeta
│  │  │  ├── libunicode_ident-6cccf60ac10d89b4.rlib
│  │  │  ├── libunicode_ident-6cccf60ac10d89b4.rmeta
│  │  │  ├── libwasm_bindgen_backend-040dfde36dd9b275.rlib
│  │  │  ├── libwasm_bindgen_backend-040dfde36dd9b275.rmeta
│  │  │  ├── libwasm_bindgen_macro-e459735820acadc1.dylib
│  │  │  ├── libwasm_bindgen_macro_support-2ec2193d0f5f8db7.rlib
│  │  │  ├── libwasm_bindgen_macro_support-2ec2193d0f5f8db7.rmeta
│  │  │  ├── libwasm_bindgen_shared-03c3ff7c535952ed.rlib
│  │  │  ├── libwasm_bindgen_shared-03c3ff7c535952ed.rmeta
│  │  │  ├── libwasm_bindgen_test_macro-0fcd318514e57960.dylib
│  │  │  ├── log-7e5c333038904839.d
│  │  │  ├── once_cell-a2b9bd79df042177.d
│  │  │  ├── proc_macro2-d53d1e09b7eb3f23.d
│  │  │  ├── quote-d5ab5f6d2ab29cd6.d
│  │  │  ├── syn-a0a2cf75bac9b939.d
│  │  │  ├── unicode_ident-6cccf60ac10d89b4.d
│  │  │  ├── wasm_bindgen_backend-040dfde36dd9b275.d
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.d
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.0.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.1.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.2.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.3.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.4.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.5.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.6.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.7.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.8.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.9.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.10.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.11.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.12.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.13.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.14.rcgu.o
│  │  │  ├── wasm_bindgen_macro-e459735820acadc1.wasm_bindgen_macro.4afe9ef1-cgu.15.rcgu.o
│  │  │  ├── wasm_bindgen_macro_support-2ec2193d0f5f8db7.d
│  │  │  ├── wasm_bindgen_shared-03c3ff7c535952ed.d
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.d
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.0.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.1.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.2.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.3.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.4.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.5.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.6.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.7.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.8.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.9.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.10.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.11.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.12.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.13.rcgu.o
│  │  │  ├── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.14.rcgu.o
│  │  │  └── wasm_bindgen_test_macro-0fcd318514e57960.wasm_bindgen_test_macro.778e5add-cgu.15.rcgu.o
│  │  ├── examples
│  │  └── incremental
│  ├── release
│  │  ├── build
│  │  │  ├── log-8e17bd435e677e14
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── log-8110063b77aa4aaf
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-8110063b77aa4aaf
│  │  │  │  └── build_script_build-8110063b77aa4aaf.d
│  │  │  ├── proc-macro2-0fe559e1762e1ee2
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── proc-macro2-7f4c886728cc183f
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-7f4c886728cc183f
│  │  │  │  └── build_script_build-7f4c886728cc183f.d
│  │  │  ├── quote-261af119deeae240
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── quote-fcb542550d8e7618
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-fcb542550d8e7618
│  │  │  │  └── build_script_build-fcb542550d8e7618.d
│  │  │  ├── syn-0475f13678b293e4
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  ├── syn-5449a5382e9b53cf
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-5449a5382e9b53cf
│  │  │  │  └── build_script_build-5449a5382e9b53cf.d
│  │  │  ├── wasm-bindgen-13c6dee24a302e99
│  │  │  │  ├── build-script-build
│  │  │  │  ├── build_script_build-13c6dee24a302e99
│  │  │  │  └── build_script_build-13c6dee24a302e99.d
│  │  │  ├── wasm-bindgen-shared-a846eb7adf471474
│  │  │  │  ├── invoked.timestamp
│  │  │  │  ├── out
│  │  │  │  ├── output
│  │  │  │  ├── root-output
│  │  │  │  └── stderr
│  │  │  └── wasm-bindgen-shared-af3ee0b2a0b74a26
│  │  │     ├── build-script-build
│  │  │     ├── build_script_build-af3ee0b2a0b74a26
│  │  │     └── build_script_build-af3ee0b2a0b74a26.d
│  │  ├── deps
│  │  │  ├── bumpalo-b465dce7c673ab11.d
│  │  │  ├── cfg_if-69311013c13c8312.d
│  │  │  ├── libbumpalo-b465dce7c673ab11.rlib
│  │  │  ├── libbumpalo-b465dce7c673ab11.rmeta
│  │  │  ├── libcfg_if-69311013c13c8312.rlib
│  │  │  ├── libcfg_if-69311013c13c8312.rmeta
│  │  │  ├── liblog-72a775263f06ca48.rlib
│  │  │  ├── liblog-72a775263f06ca48.rmeta
│  │  │  ├── libonce_cell-7649f78af27836ca.rlib
│  │  │  ├── libonce_cell-7649f78af27836ca.rmeta
│  │  │  ├── libproc_macro2-7edb806784f0b9d5.rlib
│  │  │  ├── libproc_macro2-7edb806784f0b9d5.rmeta
│  │  │  ├── libquote-75b31fea9a41582c.rlib
│  │  │  ├── libquote-75b31fea9a41582c.rmeta
│  │  │  ├── libsyn-9472bbb8d04120df.rlib
│  │  │  ├── libsyn-9472bbb8d04120df.rmeta
│  │  │  ├── libunicode_ident-2b7c8146a2a6d5dd.rlib
│  │  │  ├── libunicode_ident-2b7c8146a2a6d5dd.rmeta
│  │  │  ├── libwasm_bindgen_backend-72413130f80cca07.rlib
│  │  │  ├── libwasm_bindgen_backend-72413130f80cca07.rmeta
│  │  │  ├── libwasm_bindgen_macro-a662b55e8388c081.dylib
│  │  │  ├── libwasm_bindgen_macro_support-d6cf3c77d8a7cec6.rlib
│  │  │  ├── libwasm_bindgen_macro_support-d6cf3c77d8a7cec6.rmeta
│  │  │  ├── libwasm_bindgen_shared-03ea3bb0d4eb97be.rlib
│  │  │  ├── libwasm_bindgen_shared-03ea3bb0d4eb97be.rmeta
│  │  │  ├── log-72a775263f06ca48.d
│  │  │  ├── once_cell-7649f78af27836ca.d
│  │  │  ├── proc_macro2-7edb806784f0b9d5.d
│  │  │  ├── quote-75b31fea9a41582c.d
│  │  │  ├── syn-9472bbb8d04120df.d
│  │  │  ├── unicode_ident-2b7c8146a2a6d5dd.d
│  │  │  ├── wasm_bindgen_backend-72413130f80cca07.d
│  │  │  ├── wasm_bindgen_macro-a662b55e8388c081.d
│  │  │  ├── wasm_bindgen_macro_support-d6cf3c77d8a7cec6.d
│  │  │  └── wasm_bindgen_shared-03ea3bb0d4eb97be.d
│  │  ├── examples
│  │  └── incremental
│  ├── tmp
│  └── wasm32-unknown-unknown
│     ├── CACHEDIR.TAG
│     └── release
│        ├── build
│        │  └── wasm-bindgen-28655a08673543fc
│        │     ├── invoked.timestamp
│        │     ├── out
│        │     ├── output
│        │     ├── root-output
│        │     └── stderr
│        ├── deps
│        │  ├── cfg_if-cd6edacd88c3b663.d
│        │  ├── console_error_panic_hook-47ace22143464b3a.d
│        │  ├── hello_wasm.d
│        │  ├── hello_wasm.wasm
│        │  ├── libcfg_if-cd6edacd88c3b663.rlib
│        │  ├── libcfg_if-cd6edacd88c3b663.rmeta
│        │  ├── libconsole_error_panic_hook-47ace22143464b3a.rlib
│        │  ├── libconsole_error_panic_hook-47ace22143464b3a.rmeta
│        │  ├── libhello_wasm.rlib
│        │  ├── libwasm_bindgen-09ce07d44fa8d9e4.rlib
│        │  ├── libwasm_bindgen-09ce07d44fa8d9e4.rmeta
│        │  └── wasm_bindgen-09ce07d44fa8d9e4.d
│        ├── examples
│        ├── hello_wasm.d
│        ├── hello_wasm.wasm
│        ├── incremental
│        ├── libhello_wasm.d
│        └── libhello_wasm.rlib
└── tests
   └── web.rs
```
:::

#### package.json

npm パッケージのビルドが正常に行われました。そして、`package.json` が生成されています。
その内容を確認してみます。

```json
{
  "name": "shinyay-hello-wasm",
  "collaborators": [
    "NPM_USER_ID <E_MAIL_ADDRESS>"
  ],
  "version": "0.1.0",
  "files": [
    "hello_wasm_bg.wasm",
    "hello_wasm.js",
    "hello_wasm_bg.js",
    "hello_wasm.d.ts"
  ],
  "module": "hello_wasm.js",
  "types": "hello_wasm.d.ts",
  "sideEffects": false
}
```

### テスト実行

プロジェクトテンプレートを作ったときにテストコードも自動生成されていました。
（内容はまだ見てません…後でみてみます）

というわけで、テストコードを実行してみようと思います。

#### --node オプション

`--node` オプションは、Node.jsでの実行を想定したテストを全て実行するものです

```shell
wasm-pack test --node
```

:::details 実行結果
```shell
[INFO]: 🎯  Checking for the Wasm target...
   Compiling cfg-if v1.0.0
   Compiling scoped-tls v1.0.0
   Compiling wasm-bindgen v0.2.83
   Compiling console_error_panic_hook v0.1.7
   Compiling js-sys v0.3.60
   Compiling hello-wasm v0.1.0 (/Users/yanagiharas/Works/hello-wasm)
warning: function `set_panic_hook` is never used
 --> src/utils.rs:1:8
  |
1 | pub fn set_panic_hook() {
  |        ^^^^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: `hello-wasm` (lib) generated 1 warning
   Compiling wasm-bindgen-futures v0.4.33
   Compiling wasm-bindgen-test v0.3.33
warning: `hello-wasm` (lib test) generated 1 warning (1 duplicate)
    Finished dev [unoptimized + debuginfo] target(s) in 5.62s
[INFO]: ⬇️  Installing wasm-bindgen...
warning: function `set_panic_hook` is never used
 --> src/utils.rs:1:8
  |
1 | pub fn set_panic_hook() {
  |        ^^^^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: `hello-wasm` (lib) generated 1 warning
warning: `hello-wasm` (lib test) generated 1 warning (1 duplicate)
    Finished test [unoptimized + debuginfo] target(s) in 0.12s
     Running unittests src/lib.rs (target/wasm32-unknown-unknown/debug/deps/hello_wasm-4824064db4dae7b5.wasm)
no tests to run!
     Running tests/web.rs (target/wasm32-unknown-unknown/debug/deps/web-726945d3aebc3dc1.wasm)
this test suite is only configured to run in a browser, but we're only testing node.js tests so skipping
```
:::

#### --chrome --headless オプション

`--chrome --headless` オプションは、ブラウザでの実行を想定したすべてのテストの実行するものです

```shell
wasm-pack test --chrome --headless
```

:::details 実行結果
```shell
[INFO]: 🎯  Checking for the Wasm target...
warning: function `set_panic_hook` is never used
 --> src/utils.rs:1:8
  |
1 | pub fn set_panic_hook() {
  |        ^^^^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: `hello-wasm` (lib) generated 1 warning
warning: `hello-wasm` (lib test) generated 1 warning (1 duplicate)
    Finished dev [unoptimized + debuginfo] target(s) in 0.07s
[INFO]: ⬇️  Installing wasm-bindgen...
[INFO]: Getting chromedriver...
warning: function `set_panic_hook` is never used
 --> src/utils.rs:1:8
  |
1 | pub fn set_panic_hook() {
  |        ^^^^^^^^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: `hello-wasm` (lib) generated 1 warning
warning: `hello-wasm` (lib test) generated 1 warning (1 duplicate)
    Finished test [unoptimized + debuginfo] target(s) in 0.10s
     Running unittests src/lib.rs (target/wasm32-unknown-unknown/debug/deps/hello_wasm-4824064db4dae7b5.wasm)
no tests to run!
     Running tests/web.rs (target/wasm32-unknown-unknown/debug/deps/web-726945d3aebc3dc1.wasm)
Set timeout to 20 seconds...
Running headless tests in Chrome on `http://127.0.0.1:59912/`
Try find `webdriver.json` for configure browser's capabilities:
Not found
running 1 test

test web::pass ... ok

test result: ok. 1 passed; 0 failed; 0 ignored
```
:::

### wasm-pack から npm へのログイン

npm パッケージを公開できるように npm レジストリにログインをします。

```shell
wasm-pack login
```

:::details 実行結果
```shell
Username: YOUR_USER_ID
Password: YOUR_PASSWORD
Email: (this IS public) YOUR_EMAIL_ADDRESS
Logged in as <username> on registry.npmjs.org.
```
:::

### wasm-pack から npm へパッケージ公開

`wasm-pack` コマンドから npm レジストリにパッケージを公開します。

```shell
wasm-pack publish
```

:::details 実行結果
```shell
npm notice
npm notice 📦  shinyay-hello-wasm@0.1.0
npm notice === Tarball Contents ===
npm notice 2.8kB README.md
npm notice 784B  hello_wasm_bg.js
npm notice 270B  hello_wasm_bg.wasm
npm notice 80B   hello_wasm.d.ts
npm notice 81B   hello_wasm.js
npm notice 313B  package.json
npm notice === Tarball Details ===
npm notice name:          shinyay-hello-wasm
npm notice version:       0.1.0
npm notice filename:      shinyay-hello-wasm-0.1.0.tgz
npm notice package size:  2.2 kB
npm notice unpacked size: 4.3 kB
npm notice shasum:        f2844678ebe7d3206d[.......]502f28ab708b4
npm notice integrity:     sha512-4VP+MvlF+49[.......]99N8DRoNWnw==
npm notice total files:   6
npm notice
npm notice Publishing to https://registry.npmjs.org/
+ shinyay-hello-wasm@0.1.0
[INFO]: 💥  published your package!
```
:::

 特に問題なく公開することができました。

## Day 22 のまとめ

今日は `wasm-pack` コマンドの導入と、それでできることをいろいろと見てみました。

- wasm-pack インストール
- プロジェクトテンプレートの作成
- プロジェクトビルド
- テスト実行
- npm レジストリへの公開

ただ、自動生成されたコードの内容とか、そもそもテンプレートに手を全く加えていないので、もう少しこのプロジェクトテンプレートについて深堀りしていきたいかなって思いました。
