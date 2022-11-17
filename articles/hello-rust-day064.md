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

さて、そんな離れている間に Rust の **1.65.0** が 11 月 3 日にリリースされていましたね (⑉>ᴗ<ﾉﾉﾞ✩:+✧︎⋆ﾊﾟﾁﾊﾟﾁ

- [Rust 1.65.0 リリースノート](https://github.com/rust-lang/rust/releases/tag/1.65.0)

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

以下のように確認すると、バージョンが上がっていることがわかりました。

```shell
$ rustc -V
rustc 1.65.0 (897e37553 2022-11-02)
```

## Rust 1.65.0 リリースアナウンス

[Day 61](https://zenn.dev/shinyay/articles/hello-rust-day061) でもリリース前に作られていた GitHub 上のリリースノートについて確認をしてみました。ちょっと今日は時間も少し間が空いてしまったので、改めて公式ブログからのアナウンスノートを見てみようと思います。

- [Announcing Rust 1.65.0](https://blog.rust-lang.org/2022/11/03/Rust-1.65.0.html)

### 汎用関連型 "Generic associated types (GATs)"

まず、汎用関連型 "Generic associated types (GATs)" についてです。

- [Generic associated types (GATs)](https://blog.rust-lang.org/2022/11/03/Rust-1.65.0.html#generic-associated-types-gats)

これが、1.65.0 の What's new の最初にきていることからも分かるように、一番期待されていたリリース内容です。また、先日の [Day 62](https://zenn.dev/shinyay/articles/hello-rust-day062) でも見ていましたけれど、正直その時点でよく分からないと言っていたものがこれです。

アナウンスノートにも書かれているように、この **GATs** が実現する内容とは次のことです。
:::message
関連型に対して、ジェネリックデータ型、ライフタイム注釈や定数ジェネリクスを記述することが可能
:::

- [ジェネリックデータ型](https://doc.rust-lang.org/book/ch10-01-syntax.html)
- [ライフタイム注釈](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)

関連型を簡単に振り返ってみると次のような動作をするものでした。

Rust by Example に以下のようなサンプルのトレイトがあります。

```rust
trait Contains {
    type A;
    type B;

    fn contains(&self, &Self::A, &Self::B) -> bool;
}
```

上記のようにトレイトの中に型を定義したものがあります。もしこれをジェネリック型で定義していると次のようになります。

```rust
trait Contains<A, B> {
    fn contains(&self, _: &A, _: &B) -> bool;
}
```

これらのトレイトを実装し、そして使用を考慮したときに関連型か否かの違いが現れます。

```rust
impl Contains<i32, i32> for Container {...}
```

上記のように実装されたているとします。

Contains トレイトを使用する関数を検討する場合、まず関連型を使用しない場合以下のようになります。

```rust
fn difference<A, B, C>(container: &C) -> i32 where
    C: Contains<A, B> { ... }
```

関連型を利用すると、以下のようになります。

```rust
fn difference<C: Contains>(container: &C) -> i32 { ... }
```

つまり、Contains トレイトの中で含まれている A と B については明治をする必要がなくなるというわけです。
このような動作を関連型を使用することで可能になります。

さて、ではこの GATs では何が変更になったのかを考えてみます。

先にもアナウンスノートの話をしたように、関連型でジェネリクスが使えるようになるということ、またライフタイム注釈や定数も使用可能になるということが特徴です。

```rust
trait GATrait {
    // 普通の関連型
    type A;

    // ジェネリクスを用いた関連型
    type B<T>;

    // ライフタイム
    type C<'a>

    // 定数
    type D<const N: usize>
}
```

上記のような表現が、**1.65.0** からできるようになったということです。

### let-else 文

まず最初に、この `let-else` 文は次のような構造になります。

```rust
// let 論駁可能パターン = 値 else { never型を返す処理 };
```

たとえば、HTTP クライアントで reqwest が URL 宛に　GET リクエストを実施し、その結果が Ok を返す場合は、OK(結果) を val に束縛をし、そうではないような場合は関数を抜けます。

```rust
let Ok(val) = reqwest::get(url).await else { return };
```

このように論駁不可能かどうかを識別した上で、その後の機能の使用判断を行うような定義が可能となりました。

## Day 64 のまとめ

11 月 3 日にリリースされた バージョン **1.65.0** について少し振り返ってみました。

- [Generic associated types (GATs)](https://blog.rust-lang.org/2022/11/03/Rust-1.65.0.html#generic-associated-types-gats)
- [`let-else statements`](https://blog.rust-lang.org/2022/11/03/Rust-1.65.0.html#let-else-statements)

まとめではないのですが、本業の都合という言い訳のため２週間ほどブランクが空いてしまっていました。今後はまた気を引き締めて Rust の学習をしていきたいと思います。