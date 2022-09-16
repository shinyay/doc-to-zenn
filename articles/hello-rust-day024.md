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

### Node プロジェクト ビルド

Node プロジェクト のビルドを行ってみます。

```shell
npm run build
```

```shell
> rust-webpack-template@0.1.0 build
> rimraf dist pkg && webpack

🧐  Checking for wasm-pack...

✅  wasm-pack is installed at /Users/yanagiharas/.cargo/bin/wasm-pack.

ℹ️  Compiling your crate in release mode...

[INFO]: 🎯  Checking for the Wasm target...
[INFO]: 🌀  Compiling to Wasm...
warning: Found `debug_assertions` in `target.'cfg(...)'.dependencies`. This value is not supported for selecting dependencies and will not work as expected. To learn more visit https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#platform-specific-dependencies
    Finished release [optimized] target(s) in 0.11s
[INFO]: ⬇️  Installing wasm-bindgen...
[INFO]: Optimizing wasm binaries with `wasm-opt`...
[INFO]: Optional fields missing from Cargo.toml: 'repository', 'license'. These are not necessary, but recommended
[INFO]: ✨   Done in 0.42s
[INFO]: 📦   Your wasm pkg is ready to publish at /Users/yanagiharas/Works/webpack/my-app/pkg.
✅  Your crate has been correctly compiled

Hash: e2d0748e414083bccec3
Version: webpack 4.46.0
Time: 963ms
Built at: 09/16/2022 9:15:02 PM
                           Asset       Size  Chunks                         Chunk Names
                            1.js   1.66 KiB       1  [emitted]
13da791a2d775754b78b.module.wasm   10.1 KiB       1  [emitted] [immutable]
                      index.html  179 bytes          [emitted]
                        index.js   2.99 KiB       0  [emitted]              index
Entrypoint index = index.js
[0] ./js/index.js 48 bytes {0} [built]
[1] ./pkg/index.js 97 bytes {1} [built]
[2] ./pkg/index_bg.js 1.6 KiB {1} [built]
[3] ./pkg/index_bg.wasm 10.1 KiB {1} [built]
[4] (webpack)/buildin/harmony-module.js 573 bytes {1} [built]
```

```
```

## Day 24 のまとめ
