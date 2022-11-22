---
title: "100日後にRustをちょっと知ってる人になる: [Day 68]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 68 のテーマ
[Day 66](https://zenn.dev/shinyay/articles/hello-rust-day066) で **[Blessed.rs](https://blessed.rs/crates)** の紹介をしました。おすすめのクレートを紹介してくれているサイトでした。とはいえ、そこで紹介しているクレートは全く見ていなかったので、今後見ながら使い方を学んでいこうと思います。

![](https://storage.googleapis.com/zenn-user-upload/56c77826cbc7-20221122.png)

というわけで、Blessed.rs を開いて上から見ていこうとおもったのですけど、一番上は `rustup` で普通に使っている CLI だったのでその次の **clippy** について見ていきたいと思います。Lint ツールなので、Rust 初学者でない人達にとっては普通に使っているツールなのだろうと思いつつも、ぼくはまだ使ったことがないので改めて今回見てみたいなと思います。

## clippy

- [clippy](https://github.com/rust-lang/rust-clippy)

**clippy** は Blessed.rs ユースケースとしても説明されているように、**Linting** つまり Lint ツールや、Linter と呼ばれているプログラムコードの静的チェックツールです。Lint ツールに馴染みのない人向けに簡単に説明をすると、予め特定の言語の書き方に対するルールを定めておき、そのルールに対して記述しているコードを照らし合わせて適切なのかどうかをチェックしてくれるツールです。
例えば、次のような内容をチェックします。


## Day 68 のまとめ
