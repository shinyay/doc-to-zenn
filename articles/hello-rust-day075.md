---
title: "100日後にRustをちょっと知ってる人になる: [Day 75]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 75 のテーマ

[Day 74](https://zenn.dev/shinyay/articles/hello-rust-day074) で紹介をした日時を扱うクレート `time` の特徴の中で、シリアライゼーションやデシリアライゼーションを行うフレームワークでデファクトスタンダードになっているという `serde` というクレートについて、名前だけ引用しました。その際にも言っていましたが使ったことがまだないので、今回は `serde` について学ぼうと思います。

## serde

まず最初に以下が **serde** に関する文書やリポジトリのリンクです。

- **[crate.io](https://crates.io/crates/serde)**
- **[lib.rs](https://lib.rs/crates/serde)**
- **[docs.rs](https://docs.rs/serde/latest/serde/)**
- **[GitHub](https://github.com/serde-rs/serde/tree/master)**
- **[book - serde](https://serde.rs/)**

それでは、serde について book の内容を中心にして見ていきたいと思います。

### 概要

あらためて、**serde** が何か？ということから説明します。**serde** とは、**ser**ialization と **de**serialization を行うたいめのフレームワークです。

serde は、サポートされるデータ構造を、サポートされるデータ形式を使ってシリアライズおよびデシリアライズすることを可能にします。データ構造とデータ形式の間の相互作用は Rust コンパイラによって完全に最適化され、serde によるシリアライズはデータ構造とデータ形式の特定の選択に対して手書きのシリアライザと同じ速度で実行されるようにすることができます。

## Day 75 のまとめ
