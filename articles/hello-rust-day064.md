---
title: "100日後にRustをちょっと知ってる人になる: [Day 64]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 64 のテーマ

この 2 週間ほど止むに止まれず、Rust ではなく、Java と Kotlin を知っている人になっていました。いわゆる本業に近いところのお仕事をしていたおかげで少し Rust から離れていました。
(Kotlin もなかなか楽しい言語なんですよ、って軽く誘惑しておく😆)

さて、そんな離れている間に Rust の **1.65.0** がリリースされていましたね (⑉>ᴗ<ﾉﾉﾞ✩:+✧︎⋆ﾊﾟﾁﾊﾟﾁ
というわけで、また今日から Rust の勉強を再開していくきっかけとして 1.65.0 から初めていきたいと思います。

## 現状確認

当然ながらバージョンアップをしていないので、`1.64.0` のはずなのですが、現在の Rust のバージョンを確認してみます。

```shell
rustup show
```

```shell
active toolchain
----------------

stable-x86_64-apple-darwin (default)
rustc 1.64.0 (a55dd71d5 2022-09-19)
```

## アップグレード

Rust のバージョンを最新 Stable バージョンにあげていきます。

```shell
rustup update stable
```

:::details 実行結果

```shell
info: syncing channel updates for 'stable-x86_64-apple-darwin'
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

  stable-x86_64-apple-darwin updated - rustc 1.65.0 (897e37553 2022-11-02) (from rustc 1.64.0 (a55dd71d5 2022-09-19))

info: cleaning up downloads & tmp directories
```

:::

```shell
$ rustc -V
rustc 1.65.0 (897e37553 2022-11-02)
```

## Day 64 のまとめ

