---
title: "100日後にRustをちょっと知ってる人になる: [Day 34]What’s new in Rust 1.64"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 34 のテーマ

9 月 22 日に **Rust 1.64.0** が公開されていたのは気づいていたでしょうか？ Rust を本格的に学び始めてから間もない僕にとっては、この早い頻度でアップデートされるのは驚きでした。また、この [#100DaysOfRust](https://twitter.com/search?f=live&q=(%23100DaysOfRust)%20(from%3Ayanashin18618)&src=typed_query) な取り組みを始めてから実は初めての Rust のバージョンアップになるのでした。

- [マイルストン](https://github.com/rust-lang/rust/milestones)

## 1.64.0 へアップデート

アップデートする前にまず現在のバージョンを確認しておきます。

```shell
$ rustc --version
rustc 1.63.0 (4b91a6ea7 2022-08-08)
```

`1.63.0` でした。

それでは、`rustup` CLI を使ってアップデートを行います。

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

## 1.64.0 の特徴

以下の内容が、**1.64.0** での主な特徴です。

- .await 時に IntoFuture
- C 互換の FFI 型 (libstd) の libcore / liballoc への移動
- rustup の コンポーネント として rust-analyzer 利用可能
- Cargo のワークスペース継承
- Cargo のマルチターゲットビルド
- Windows 上でのコンパイル最適化

### .await 時に IntoFuture

Rust 1.64.0 に含まれる改善点の中でも最も注目するべきものは、**IntoFutureトレイト**の安定化です。

この `IntoFuture` は `IntoIterator` に似た特徴です。`for ... in ...` ループをサポートするのではなく、IntoFuture は `.await` の動作方法を変更します。
`IntoFuture` では、`.await` キーワードは `Future` 以外にも待ち受けることが可能です。

#### Future トレイトによる非同期処理

Rust では、非同期な計算は `Future トレイト`として抽象化されています。

関数が非同期であることを明示するために、`async` を利用します。
`async` はコードブロックを `Future トレイト` を実装しているステートマシンに変換するものです。

```rust
async fn hello_world() {
    println!("hello world")
}
```

`await` は非同期処理の結果を待つことを明示するためのキーワードです。
`await` を使うことで `async` で書かれた非同期関数が完了するまで待ち合わせます。
`await` は `async` スコープ内でのみ利用可能です。

`async fn` 内では `.await` を使うことで、ほかの Future トレイト` を実装する別の型の完了を待つことができます。

```rust
async fn hello_world() {
    println!("hello world")
}

async fn hello_world2() {
    println!("hello world2")
}

async fn run() {
    hello_world().await;
    hello_world2().await;
}
```

### C 互換の FFI 型 (libstd) の libcore / liballoc への移動
### rustup の コンポーネント として rust-analyzer 利用可能
### Cargo のワークスペース継承
### Cargo のマルチターゲットビルド
### Windows 上でのコンパイル最適化

## Day 34 のまとめ
