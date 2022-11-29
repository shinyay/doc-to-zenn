---
title: "100日後にRustをちょっと知ってる人になる: [Day 73]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 73 のテーマ

**[Blessed.rs](https://blessed.rs/crates)** で紹介されているクレートについて今日も見てみたいと思います。この 1 週間 **Blessed.rs** 見てきているので、Blessed.rs で紹介されているクレートに関心を持った人もいるのではないでしょうか。

![](https://storage.googleapis.com/zenn-user-upload/76cc64f215c6-20221129.png)

いろいろと見てはきていますが、Day 68 〜 Day 72 ではクレートはクレートでも `cargo` コマンドのサブコマンドとして使用するツールを見てきました。ここで趣向を少し変えて、Rust の標準ライブラリとして提供されていないので提供されるクレートを用いて補完するようなものを見てみたいと思います。

そこで、まず今回は**乱数生成**について見ていこうと思います。

## 乱数生成

Rust 以外の言語、例えば **Java** であれば乱数を生成するときには、標準 API で `java.util.Random` や `Math.random()`、また **Kotlin** であれば `kotlin.random.Random` のようの提供をしています。しかし、Rust では標準ライブラリから乱数を生成する機能を提供していないのです。

そこで、Rust で乱数を生成するときに使用するためには、Rust 開発チームから提供されているクレートの **rand** を使用します。

- [rand](https://docs.rs/rand/latest/rand/)
  - [GitHub リポジトリ](https://docs.rs/rand/latest/rand/)

## Day 73 のまとめ
