---
title: "100日後にRustをちょっと知ってる人になる: [Day 69]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 69 のテーマ

## Day 69 のまとめ

[Day 68](https://zenn.dev/shinyay/articles/hello-rust-day068) では、**[Blessed.rs](https://blessed.rs/crates)** で紹介されている Lint ツールの **clippy** の使い方を見てみました。今日も引き続き、Blessed.rs で紹介されているクレートを見てみたいかなと思います。

![](https://storage.googleapis.com/zenn-user-upload/cd796ca47507-20221123.png)

というわけで、開発ツールで紹介されている **コードフォーマット**ツールの **rustfmt** について今日は見てみたいかなと思います。

## rustfmt

以下が **rustfmt** のリポジトリです。見てもらえば分かるように、先日の Lint ツールの [clippy](https://github.com/rust-lang/rust-clippy) 同様に、この rustfmt も **[rust-lang](https://github.com/rust-lang)** の配下におかれる Rust の公式なコードフォーマットツールです。

- [rust-lang/rustfmt](https://github.com/rust-lang/rustfmt)

この rustfmt は、コードのスタイルガイドラインに従って、作成するコードを整形するために用いられるものです。