---
title: "100日後にRustをちょっと知ってる人になる: [Day 23]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 23 のテーマ

今日は昨日確認していた **wasm-pack** の続きを行おうと思っています。
昨日は `wasm-pack new` コマンドで自動生成されたテンプレートをそのまま使って動作を確認していました。
自動生成されたコードがどのようなものかを見ることもなく動作確認だけを行いました。

と、いうことで、今日は自動生成されたソースコードを読んでいきたいと思います。

## コードリーディング

昨日作成した　`hello-wasm` プロジェクトのソースコードディレクトリ `src` は以下のようになっていました。

```shell
src
├── lib.rs
└── utils.rs
```

以下のようにデフォルトで 2 つのコードが出力されていました。

- lib.rs
- utils.rs

### utils.rs

utils.rs のコードの内容は以下のようになっています:

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

## Day 23 のまとめ
