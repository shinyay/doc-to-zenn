---
title: "100日後にRustをちょっと知ってる人になる: [Day 27]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 27 のテーマ

この数日間、Rust を使っての WebAssembly プロジェクトの作成やビルドについて調べてきました。ただ、WebAssembly バイナリを作るだけにしても、いろいろな作り方があることがわかりました。
場当たり的に確認をしていたので、ここで一度整理をしておこうと思います。

## WebAssembly プロジェクトの作成

Rust はコンパイラが標準で WebAssembly に対応しているので、敢えて特別なプロジェクト構成にしなくても WebAssembly バイナリのビルドを行うことは可能です。ですが、Rust のパッケージマネージャの **Cargo** を使うことで便利になったりなど、いろいろなプロジェクト作成の方法がありました。

- プレーンディレクトリ (`mkdir`)
- `cargo new`
- `cargo generate`
- `wasm-pack new`
- `npm init rust-webpack`
- `npm init wasm-app`

### プレーンディレクトリ (`mkdir`)

これは、適当なディレクトリを設けてそこで自由に構成して `rustc` コマンドで直接コンパイルするような場合のみな気がします。

[Day 20](https://zenn.dev/shinyay/articles/hello-rust-day020) で **WASI** のビルドを行ったときにも適当なディレクトリをプロジェクトを開発ディレクトリとして扱いました。

### `cargo new`

これは、**Cargo** によるパッケージ管理とビルドの仕組みを利用するためのプロジェクト構成です。`Cargo.toml` に依存関係などを定義しておくことで自動でライブラリモジュールの取得などを行ってくれます。
`cargo build --target wasm32-wasi` のように、`--target` を指定して WebAssembly バイナリのビルドを行います。

### `cargo generate`

これは、定義済みのプロジェクトテンプレートを用いてプロジェクト構成を作成します。
`cargo generate --git https://github.com/rustwasm/wasm-pack-template` のように GitHub に公開されたプロジェクトテンプレートを直接指定してプロジェクトを作成する事ができます。

- [プロジェクトテンプレート](https://zenn.dev/shinyay/articles/hello-rust-day025#cargo-generate-%E3%81%A7%E6%8C%87%E5%AE%9A%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%83%86%E3%83%B3%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88)

### `wasm-pack new`

これは、Web ブラウザで WebAssembly を動作させることを目的としたプロジェクト構成です。`Cargo.toml` には標準で以下のクレートが登録されています。

- [wasm-bindgen](https://crates.io/crates/wasm-bindgen)
- cdylib
- rlib

また、今までのプロジェクトとは異なり、コンパイルターゲットとして、`wasm32-unknown-unknown` が想定されています。
`wasm-pack build` を行うと暗黙的に `wasm32-unknown-unknown` が指定されてビルドされています。

### `npm init rust-webpack`

これは、Rust, WebAssenbly そして **Webpack** 用の **npm** パッケージである **[create-rust-webpack](https://www.npmjs.com/package/create-rust-webpack)** によりプロジェクトが構成されます。
`npm run build` でビルドすることで、暗黙的に `wasm-pack build` も内部で行われています。

### `npm init wasm-app`

これは、Rust で生成された WebAssembly を含む npm パッケージを使用して、Webpack でバンドルするプロジェクトを作るための **npm** テンプレート [create-wasm-app](https://github.com/rustwasm/create-wasm-app) を使ったプロジェクトです。つまり、このプロジェクト構成のみでは、Rust のコード構成が含まれていません。`wasm-pack-template` と組み合わせて、Rust と JavaScript のプロジェクトの構成にすることができます。

## WebAssembly プロジェクトのビルド

Rust による WebAssembly プロジェクトのビルドも、プロジェクトのタイプにより複数ありました。そこで以下のように整理しておきます。

- `rustc --target wasm32-wasi`
- `rustc --target wasm32-unknown-unknown`
- `cargo build --target wasm32-wasi`
- `cargo build --target wasm32-unknown-unknown`
- `cargo wasi build` // wasm32-wasi 指定
- `wasm-pack build`  // wasm32-unknown-unknown 指定
- `npm run build`

## WebAssembly プロジェクトのテンプレート

`npm init rust-webpack` や `npm init wasm-app` によりプロジェクト構成が自動生成されるように、WebAssemblｙでは予め定義されたプロジェクトテンプレートが以下のように公開されています。

- [wasm-pack-template](https://github.com/rustwasm/wasm-pack-template)
- [create-wasm-app](https://github.com/rustwasm/create-wasm-app)
- [rust-webpack-template](https://github.com/rustwasm/rust-webpack-template)

### wasm-pack-template

`wasm-pack` で使用する Rust および WebAssembly のためのプロジェクトです。

```shell
wasm-pack new
```

```shell
cargo generate --git https://github.com/rustwasm/wasm-pack-template.git

```

### create-wasm-app

`wasm-pack` で Rust から作成された **npm** から使用する JavaScript のプロジェクトです。

```shell
cd <WASM_PROJECT>
npm init wasm-app <PROJECT_NAME>
```

### rust-webpack-template

Rust を WebAssembly にコンパイルし、Webpack の rust-loader で Webpack のビルドパイプラインに直接フックするための定型文が全て予め設定されているプロジェクトです。

```shell
npm init rust-webpack <PROJECT_NAME>
```

## Day 27 のまとめ
