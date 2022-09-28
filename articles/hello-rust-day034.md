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

この `IntoFuture` は `IntoIterator` に似た特徴です。`for ... in ...` ループをサポートするのではなく、IntoFuture では `.await` の動作方法を変更します。
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

- `[Future](https://doc.rust-lang.org/std/future/trait.Future.html)`

`Future` は `async` を使用して得られる非同期処理を表します。

```rust
pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

- `[async](https://doc.rust-lang.org/std/keyword.async.html)`

現在のスレッドをブロックするのではなく、Futureを返します。
`fn`、`クロージャ`、`ブロック`の前で `async` を使用すると、マークされたコードが `Future` に変わります。そのため、コードはすぐに実行されず、返された `Future` が `.await` されたときにのみ評価されます。

- `[await](https://doc.rust-lang.org/std/keyword.await.html)`

#### (参考)IntoIterator

- [IntoIterator](https://doc.rust-lang.org/std/iter/trait.IntoIterator.html)

`IntoIterator` はイテレータを得るためのトレイトです。

```rust
pub trait IntoIterator {
    type Item;
    type IntoIter: Iterator
    where
        <Self::IntoIter as Iterator>::Item == Self::Item;

    fn into_iter(self) -> Self::IntoIter;
}
```

#### IntoFuture

- [IntoFuture](https://doc.rust-lang.org/stable/core/future/trait.IntoFuture.html)

`IntoFuture` を用いて、任意の型を `Future` に取り込む新しいトレイトです。

```rust
use std::future::IntoFuture;

pub struct Multiply {
    num: u16,
    factor: u16,
}

impl Multiply {
    pub fn new(num: u16, factor: u16) -> Self {
        Self { num, factor }
    }

    pub fn number(mut self, num: u16) -> Self {
        self.num = num;
        self
    }

    pub fn factor(mut self, factor: u16) -> Self {
        self.factor = factor;
        self
    }
}

// IntoFuture の実装
impl IntoFuture for Multiply {
    type Output = u16;
    type IntoFuture = Ready<Self::Output>;

    fn into_future(self) -> Self::IntoFuture {
        ready(self.num * self.factor)
    }
}

async fn run() {
  let num = Multiply::new(0, 0)
      .number(2)
      .factor(2)
      .await;
  assert_eq!(num, 4);
}
```

このように、`IntoFuture` を実装することで任意の型を `Future` にすることができるようになるので使い所は多くあるのではないでしょうか。

### C 互換の FFI 型 (libstd) の libcore / liballoc への移動

C 言語の ABI (Application Binary Interface) を呼び出したり呼び出されたりする際に、Rust のコードは `c_uint` や `c_ulong` といった型別名を使うことで、ターゲット固有のコードや条件文を必要とせず、あらゆるターゲットで C 言語の対応する型にマッチさせることができます。
今までは、これらの型別名は `std` でしか利用できなかったため、組み込みターゲットなど core や alloc しか利用できないコードでは、これらの型を利用することができませんでした。しかし、**1.64.0** から利用できるようになります。

`CStr` および関連する型が `libcore`で、
また `CString` および関連する型が `liballoc`に移動しました。

また、次の型が `std::os::raw` だけでなく `core::ffi` および `std::ffi` で使えるようになりました。

- `c_char`
- `c_double`
- `c_float`
- `c_int`
- `c_long`
- `c_longlong`
- `c_schar`
- `c_short`
- `c_uchar`
- `c_uint`
- `c_ulong`
- `c_ulonglong`
- `c_ushort`

### rustup の コンポーネント として rust-analyzer 利用可能

`rust-analyzer` が、Rust に含まれるツールのコレクションの一部として含まれるようになりました。`rustup` コンポーネントとして利用可能になります。

```shell
rustup component add rust-analyzer
```

### Cargo でのワークスペース共通の設定

Cargo によるワークスペース作成時に、`Cargo.toml` にバージョンや概要などのパッケージ情報、また依存クレートも記述出来るようになりました。

```toml
# Cargo.toml

# ワークスペースの定義
[workspace]
members = ["sub"]

# ワークスペース共通の設定
[workspace.package]
version = "1.2.3"                     # ワークスペース共通のバージョン
edition = "2021"                      # ワークスペース共通のRustエディション
rust-version = "1.64"                 # ワークスペース共通のMSRV
license = "GPL-3.0-or-later"          # ワークスペース共通のライセンス
description = "something"             # ワークスペース共通の概要

# ワークスペース共通の依存クレート
[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
```

```toml
# sub/Cargo.toml
[package]
name = "sub"

version.workspace = true
edition.workspace = true
rust-version.workspace = true
license.workspace = true
description.workspace = true

[dependencies]
tokio.workspace = true
```

以下のフィールドを指定かのうです。

- `authors`
- `categories`
- `description`
- `documentation`
- `edition`
- `exclude`
- `homepage`
- `include`
- `keywords`
- `license`
- `license-file`
- `publish`
- `readme`
- `repository`
- `rust-version`
- `version`

### Cargo のマルチターゲットビルド

複数のターゲットに対してビルドを行う際に、`cargo build` に複数の `--target` オプションを渡して、それらのターゲット全てを一度にビルドすることができるようになりました。
また、`.cargo/config.toml` で `build.target` を複数のターゲットの配列に設定すると、デフォルトで複数のターゲットに対してビルドを行うことができます。

### Windows 上でのコンパイル最適化

Windows 版ビルドでプロファイルに基づく最適化が用いられるようになり、コンパイラのパフォーマンスが **10～20%** 改善

### glibcとkernelの最低要件の変更

Linux 版の最低要件が引き上げらします。

**1.64.0 から:**

- glibc: `2.17`
- kernel: `3.2`

**1.64.0 以前:**

- glibc: `2.11`
- kernel: `2.6.32`

## Day 34 のまとめ

9 月 22 日にリリースされた Rust `1.64.0` について見てみました。

公式のリリースノートはこちらです:

- [リリースノート](https://github.com/rust-lang/rust/blob/master/RELEASES.md#version-1640-2022-09-22)

主要そうなところを一部だけ抜き出してみたので、全量はこちらをみてもらうといいかなと思います。
