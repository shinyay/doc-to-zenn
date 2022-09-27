---
title: "100日後にRustをちょっと知ってる人になる: [Day 34]What’s new in Rust 1.64"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 34 のテーマ

```shell
$ rustc --version
rustc 1.63.0 (4b91a6ea7 2022-08-08)
```

```shell
$ rustup update
```

:::details 実行結果
```shell
info: syncing channel updates for 'stable-x86_64-apple-darwin'
info: latest update on 2022-09-22, rust version 1.64.0 (a55dd71d5 2022-09-19)
info: downloading component 'rust-std' for 'wasm32-unknown-unknown'
info: downloading component 'rust-std' for 'wasm32-wasi'
info: downloading component 'rust-src'
info: downloading component 'cargo'
info: downloading component 'clippy'
info: downloading component 'rust-docs'
info: downloading component 'rust-std'
info: downloading component 'rustc'
info: downloading component 'rustfmt'
info: removing previous version of component 'rust-std' for 'wasm32-unknown-unknown'
info: removing previous version of component 'rust-std' for 'wasm32-wasi'
info: removing previous version of component 'rust-src'
info: removing previous version of component 'cargo'
info: removing previous version of component 'clippy'
info: removing previous version of component 'rust-docs'
info: removing previous version of component 'rust-std'
info: removing previous version of component 'rustc'
info: removing previous version of component 'rustfmt'
info: installing component 'rust-std' for 'wasm32-unknown-unknown'
info: installing component 'rust-std' for 'wasm32-wasi'
info: installing component 'rust-src'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
info: installing component 'rust-std'
info: installing component 'rustc'
info: installing component 'rustfmt'
info: checking for self-updates

  stable-x86_64-apple-darwin updated - rustc 1.64.0 (a55dd71d5 2022-09-19) (from rustc 1.63.0 (4b91a6ea7 2022-08-08))

info: cleaning up downloads & tmp directories
```
:::

```shell
$ rustc --version
rustc 1.64.0 (a55dd71d5 2022-09-19)
```

## Day 34 のまとめ
