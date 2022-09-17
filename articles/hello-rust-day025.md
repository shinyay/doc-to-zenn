---
title: "100日後にRustをちょっと知ってる人になる: [Day 25]cargo-generate"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---

## Day 25 のテーマ

Rust で開発を行うときに、**Cargo** は必須の CLI ですよね。それだけでもとても便利ですけど、`cargo install` で、[crates.io](https://crates.io/) からバイナリクレートをローカルにインストールして、もっと便利にすることもできます。

ちなみに、バイナリクレートとは、`src/main.rs` やバイナリとして指定された他のファイルをもつ場合に生成される **実行可能なプログラム**のことです。

[Day 21](https://zenn.dev/shinyay/articles/hello-rust-day021) でインストールした、WebAssembly 用のサブコマンドな `cargo-wasi` も `cargo install` でインストールしましたね。

```shell
cargo install cargo-wasi
```

## Day 25 のまとめ
