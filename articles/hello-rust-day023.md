---
title: "100日後にRustをちょっと知ってる人になる: [Day 23]wasm-pack テンプレート Deep Dive"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: true
---
## Day 23 のテーマ

今日は昨日確認していた **wasm-pack** の続きを行おうと思っています。
昨日は `wasm-pack new` コマンドで自動生成されたテンプレートをそのまま使って動作を確認していました。
自動生成されたコードがどのようなものかを見ることもなく動作確認だけを行いました。

と、いうことで、今日は自動生成されたソースコードを読んでいきたいと思います。

## コードリーディング

昨日作成した　`hello-wasm` プロジェクトを一部抜粋してました。

大事になってくるのは次のコードです:

- `Cargo.toml` - Cargo のマニフェスト
- `src/lib.rs` - ライブラリモジュール
- `src/utils.rs` - ユーティリティモジュール

```shell
hello-wasm
├── Cargo.toml
└── src
   ├── lib.rs
   └── utils.rs
```

### Caego.toml

まず最初にこのプロジェクトのマニフェストとなる `Cargo.toml` について見てみます。

:::details Cargo.toml
```toml
[package]
name = "hello-wasm"
version = "0.1.0"
authors = ["shinyay <mail@address>"]
edition = "2018"

[lib]
crate-type = ["cdylib", "rlib"]

[features]
default = ["console_error_panic_hook"]

[dependencies]
wasm-bindgen = "0.2.63"

# The `console_error_panic_hook` crate provides better debugging of panics by
# logging them with `console.error`. This is great for development, but requires
# all the `std::fmt` and `std::panicking` infrastructure, so isn't great for
# code size when deploying.
console_error_panic_hook = { version = "0.1.6", optional = true }

# `wee_alloc` is a tiny allocator for wasm that is only ~1K in code size
# compared to the default allocator's ~10K. It is slower than the default
# allocator, however.
wee_alloc = { version = "0.4.5", optional = true }

[dev-dependencies]
wasm-bindgen-test = "0.3.13"

[profile.release]
# Tell `rustc` to optimize for small code size.
opt-level = "s"
```
:::

まず `ceate-type` について見てみます。

```toml
[lib]
crate-type = ["cdylib", "rlib"]
```

`crate-type=cdylib`:
これは動的なシステムライブラリの生成を表します。他言語からロードするために使用されます。ただし WebAssembly ターゲットとしては、単に開始関数がないということを表します。

`crate-type=rlib`:
「Rustライブラリ」ファイルが生成されます。これは、中間成果物として使用され、「静的なRustライブラリ」と考えることができます。また、`wasm-pack test` でライブラリのユニットテストができるようにしています。

次に、`features` について見てます。

```toml
[features]
default = ["console_error_panic_hook"]
```

ここででデフォルトフィーチャーとして `console_error_panic_hook` が追加されています。これは、パニックメッセージを開発者コンソールにログ出力する機能です。

- [Crate console_error_panic_hook](https://docs.rs/console_error_panic_hook/latest/console_error_panic_hook/)

最後に `[dependencies]` アノテーションで追加されている依存関係を見ておきます。

- [wasm-bindgen](https://crates.io/crates/wasm-bindgen)
- [console_error_panic_hook](https://crates.io/crates/console_error_panic_hook)
- [wee_alloc](https://crates.io/crates/wee_alloc)

`wasm-bindgen` は、`#[wasm-bindgen]` 属性により、JavaScript と Rust で生成された wasm の間のインタフェースを表すコードをタグ付けすることができます。この属性を使って、JSをインポートし、Rustをエクスポートすることができます。
`wee_alloc` は、小さなコードサイズのために最適化されたアロケータです。

### utils.rs

utils.rs のコードの内容は以下のようになっています:

:::details utils.rs
```rust
pub fn set_panic_hook() {
    // When the `console_error_panic_hook` feature is enabled, we can call the
    // `set_panic_hook` function at least once during initialization, and then
    // we will get better error messages if our code ever panics.
    //
    // For more details see
    // https://github.com/rustwasm/console_error_panic_hook#readme
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}
```
:::

次の箇所では、`cfg` 属性を使って条件付きコンパイルを行います。
以下の場合は、`console_error_panic_hook` フィーチャーが設定されているかどうかをチェックするよう Rust に指示します。
もし設定されていれば、後続の関数(`console_error_panic_hook::set_once()`)を呼び出します。もし設定されていなければ呼び出されません。

```rust
#[cfg(feature = "console_error_panic_hook")]
```

`console_error_panic_hook` の有無で出力結果が変わり、デバッグを容易にします。

設定なし:
`"RuntimeError: Unreachable executed"`


設定あり:
`"panicked at 'index out of bounds: the len is 3 but the index is 4', libcore/slice/mod.rs:2046:10"`

### lib.rs

:::details lib.rs
```rust
mod utils;

use wasm_bindgen::prelude::*;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet() {
    alert("Hello, hello-wasm!");
}
```
:::

まず最初に `utils.rs` をモジュールとして取り込む宣言を最初にしています。これにより、先のユーティリティ用の `utils.rs` が、この呼出元の `lib.js` から使用できるようになります。

```rust
mod utils;
```

次に `wasm_bindgen` クレートを使用するために、 `use` キーワードをつかっています。こうすることで、クレートの内容を簡単に参照することができるようになります。以下の記述の場合は、`prelude` のスコープの機能を接頭辞なしで使用できるようになります。

```rust
use wasm_bindgen::prelude::*;
```

次の属性 `#[wasm_bindgen]` は、後続の関数が **Rust** と **JavaScript** の両方でアクセス可能であることを示すものです。

```rust
#[wasm_bindgen]
extern {
    fn alert(s: &str);
}
```

`extern` キーワードは外部関数インターフェースをあらわしています。
`alert` 関数は、文字列である&str型のパラメータsを1つだけ必要とすることがわかります。
Rustでは、"Hello, Wasm!"のような文字列リテラルはすべて `&str` 型になります。つまり、`alert` は `alert("Hello, Wasm!");` と書くことで呼び出すことができます。

- [Keyword extern](https://doc.rust-lang.org/std/keyword.extern.html)

## Day 23 のまとめ

`wasm-pack` で作ったプロジェクトテンプレートを今日は見直してみました。
Rust <-> JavaScript な相互でのやりとりに関する基本的なところの気づきをいろいろと得ることができました。
相互でのやり取りの仕組みは分かってきたので、このテンプレートをベースに少しアレンジしたものを作ってみたいかなと思います。
