---
title: "100日後にRustをちょっと知ってる人になる: [Day 69]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 69 のテーマ

[Day 68](https://zenn.dev/shinyay/articles/hello-rust-day068) では、**[Blessed.rs](https://blessed.rs/crates)** で紹介されている Lint ツールの **clippy** の使い方を見てみました。今日も引き続き、Blessed.rs で紹介されているクレートを見てみたいかなと思います。

![](https://storage.googleapis.com/zenn-user-upload/cd796ca47507-20221123.png)

というわけで、開発ツールで紹介されている **コードフォーマット**ツールの **rustfmt** について今日は見てみたいかなと思います。

## rustfmt

以下が **rustfmt** のリポジトリです。見てもらえば分かるように、先日の Lint ツールの [clippy](https://github.com/rust-lang/rust-clippy) 同様に、この rustfmt も **[rust-lang](https://github.com/rust-lang)** の配下におかれる Rust の公式なコードフォーマットツールです。

- [rust-lang/rustfmt](https://github.com/rust-lang/rustfmt)

この rustfmt は、コードのスタイルガイドラインに従って、作成するコードを整形するために用いられるものです。
デフォルトでは、次のスタイルガイドに準拠しているようです。

- [Rust Style Guide](https://github.com/rust-lang/fmt-rfcs/blob/master/guide/guide.md)

インデントやライン幅、空白行、またモジュールレベルの項目やステートメント、式、型などの項目でそれぞれフォーマットを定義しています。

## インストール

```shell
rustup component add rustfmt
```

これで、次のコマンドでコードフォーマットを実行できます。

```shell
rustfmt
```

あるいは

```shell
cargo fmt
```

## コードフォーマット実行

次のような、コードスタイルがおかしなサンプルコードを作成してみます。

```rust
fn main(){
for n in 0..10{
println!("{n}: Hello, Rust!");
}
}
```

インデントが崩れていて、ひと目でおかしなコードだとわかりますよね。ただ、コード的には間違いはないので実行はできます。

```shell
$ cargo run

0: Hello, Rust!
1: Hello, Rust!
2: Hello, Rust!
3: Hello, Rust!
4: Hello, Rust!
5: Hello, Rust!
6: Hello, Rust!
7: Hello, Rust!
8: Hello, Rust!
9: Hello, Rust!
```

あと、`clippy` も実施してみましたが特にエラーは発生しませんでした。

ここで、`cargo fmt` を実行してみます。特にメッセージが表示されるわけではないのですが、実行後にソースコードを見てください。

## Day 69 のまとめ