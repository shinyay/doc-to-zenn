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

## Rust プロジェクト作成



```shell
npm init wasm-app www
```

```shell
cd www
npm install
```

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
## Day 26 のまとめ
