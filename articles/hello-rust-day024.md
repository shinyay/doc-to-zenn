---
title: "100日後にRustをちょっと知ってる人になる: [Day 24]rust-webpack"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 24 のテーマ

Rust で生成した **WebAssembly**　を動作させるために Node.js にインポートすることはよくあると思います。
今日は、Rust で生成した **WebAssembly** と **[Webpack](https://webpack.js.org/)** を使って、Web アプリケーションを作成してみようと思います。

次の npm パッケージを使って Node.js と Rust のプロジェクトを用意していきます。

- [create-rust-webpack (rust-webpack-template)](https://www.npmjs.com/package/create-rust-webpack)

### Webpack

Node.js クラスタに住んでいないエンジニアの方だと、あまり聞き覚えがないかもしれないので、まず最初に、**Webpack** とは何かということについて簡単に説明しておきます。

JavaScript モジュールを束ねることができるツール（**モジュールバンドラ**）のことです。

Web アプリケーションを構成するリソースは複数あります。 例えば、Web ページを装飾するために **CSS** を使いますし、**画像**も必要です。
**Webpack** は、これらのリソース (HTML、SVG、JSX、CSS、JavaScript、PNG、JPG) を 1 つに束ねてくれるので、開発する際にリソースを扱いやすくなります。

Webpack を使うことのメリット:
✅ 依存関係のある JavaScript のモジュールを解決
✅ 適切な順序での JavaScript ファイルのコードを結合することが可能
✅ JavaScriptモジュールをブラウザで扱える形に変換可能
✅ 豊富なローダやプラグイン

### create-rust-webpack (rust-webpack-template)

**create-rust-webpack (rust-webpack-template)** を使ってプロジェクトテンプレートを作ってみます。

```shell
$ npm init rust-webpack my-app

 🦀 Rust + 🕸 WebAssembly + Webpack = ❤️
 Installed dependencies ✅
```

以下のような構成でプロジェクトが生成されます。

```shell
my-app/
├── Cargo.toml
├── README.md
├── js/
│   └── index.js
├── node_modules/
├── package-lock.json
├── package.json
├── src/
│   └── lib.rs
├── static/
├── tests/
└── webpack.config.js
```

#### src/lib.js

自動生成されている Rust クレートを見てみます。
`lib.rs` のみが生成されています。

:::details lib.rs
```rust
use wasm_bindgen::prelude::*;
use web_sys::console;


// When the `wee_alloc` feature is enabled, this uses `wee_alloc` as the global
// allocator.
//
// If you don't want to use `wee_alloc`, you can safely delete this.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;


// This is like the `main` function, except for JavaScript.
#[wasm_bindgen(start)]
pub fn main_js() -> Result<(), JsValue> {
    // This provides better error messages in debug mode.
    // It's disabled in release mode so it doesn't bloat up the file size.
    #[cfg(debug_assertions)]
    console_error_panic_hook::set_once();


    // Your code goes here!
    console::log_1(&JsValue::from_str("Hello world!"));

    Ok(())
}
```
:::

## Day 24 のまとめ
