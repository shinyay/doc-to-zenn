---
title: "100日後にRustをちょっと知ってる人になる: [Day 26]3分で Wasm をブラウザで動かす"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 26 のテーマ

[Day 25](https://zenn.dev/shinyay/articles/hello-rust-day025) で、`cargo generate` コマンドを使って Rust のプロジェクトテンプレートを作る事がえきるようになりした。
ということで、今日は 3分以内で WebAssembly をブラウザで動かすことができるくらいの内容を、`cargo generate` でプロジェクトを作るところからやってみようと思います。

## Rust プロジェクト作成

まずは、`cargo generate` コマンドでプロジェクトを作ります。

- `--name` オプションは、予めプロジェクト名を指定するオプションです。

```shell
cargo generate --git https://github.com/rustwasm/wasm-pack-template --name day_26_rust_wasm_tutorial
```

:::details プロジェクト構成
```shell
day-26-rust-wasm-tutorial
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
:::

`src/lib.rs` は、WebAssembly にコンパイルする Rust クレートのルートです。JavaScript とのインターフェースに**wasm-bindgen**を使用しているのが分かります。

JavaScript の `window.alert` 関数をインポート

```rust
#[wasm_bindgen]
extern {
    fn alert(s: &str);
}
```

メッセージを出力する `greet` 関数をエクスポート

```rust
#[wasm_bindgen]
pub fn greet() {
    alert("Hello, day-26-rust-wasm-tutorial!");
}
```

## Rust プロジェクトビルド

```shell
wasm-pack build
```

以下のように `pkg` ディレクトリ配下にビルド成果物が出力されました。

:::details pkg
```shell
pkg
├── day_26_rust_wasm_tutorial.d.ts
├── day_26_rust_wasm_tutorial.js
├── day_26_rust_wasm_tutorial_bg.js
├── day_26_rust_wasm_tutorial_bg.wasm
├── day_26_rust_wasm_tutorial_bg.wasm.d.ts
├── package.json
└── README.md
```
:::

- `xxx.wasm`
  - Rust コンパイラが生成した WebAssembly バイナリ
- `xxx.js`
  - **wasm-bindgen** により生成された Rust と JavaScript を仲介するインターフェースを公開する JavaScript コード

## JavaScript プロジェクト作成

WebAssebmly を Web ページ上で公開するために、次の JavaScprit テンプレートを使用します。

- [create-wasm-app](https://github.com/rustwasm/create-wasm-app)

`www` という名前でプロジェクトを作成します。

```shell
npm init wasm-app www
```

次のような構成でプロジェクトが作成されます。

:::details www
```shell
www
├── bootstrap.js
├── index.html
├── index.js
├── LICENSE-APACHE
├── LICENSE-MIT
├── package-lock.json
├── package.json
├── README.md
└── webpack.config.js
```
:::

## JavaScript プロジェクトカスタマイズ

生成された `package.json` には、先にビルドした　WebAssebmly に対する依存関係が定義されていません。
そこで、`dependencies` フィールドを追加してます。

```json
{
//...
//...

  "dependencies": {
    "day-26-rust-wasm-tutorial": "file:../pkg"
  }

//...
//...
}
```



```shell
cd www
npm install
```

## Day 26 のまとめ
