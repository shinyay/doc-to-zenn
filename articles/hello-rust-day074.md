---
title: "100日後にRustをちょっと知ってる人になる: [Day 74]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: []
published: false
---
## Day 74 のテーマ

[Day 73](https://zenn.dev/shinyay/articles/hello-rust-day073) では、**乱数**を扱うクレートについて見てみました。そこでも少しふれましたけれど、他のプログラム言語であれば標準ライブラリで提供していそうな乱数の機能が Rust ではないということに驚いていました。また、今回もいかにも標準ライブラリで提供していそうな**日時**を扱う機能について見てみたいとおもっています。

また別の言語のことですが、Java では日時計算を行う時に利用する API として、[Date and Time API](https://docs.oracle.com/javase/8/docs/technotes/guides/datetime/index.html) が標準 API として提供されています。
このように、他のプログラム言語の経験者からすると標準ライブラリで充実した機能が提供されていないことに違和感を持ってしまうかもしれないですよね。

僕自身標準提供されている API を知るということよりも、多くのクレートで何ができるかを知っていくことも大事だと思っているところです。逆に考えれば、それだけ Rust の場合はエコシステムが広がりを見せてきているのかもしれないのかなと感じていたりします。とは
言っても、クレートをいろいろと覚えていかなければならないので学習範囲は広がりそうですけどね。

というわけで、今日は**日時**を扱う **time** というクレートを見ていきたいなと思います。

## time

日時を扱うクレートで代表的なものには、**time** と **chrono** という 2 つがあるようです。今日は **time** について使い方を学びたいなと思います。

以下が、**time** クレートに関するプロジェクトやドキュメントへのリンクです。

- [time (crate.io)](https://crates.io/crates/time)
- [lib.rs](https://lib.rs/crates/time)
- [GitHub](https://github.com/time-rs/time)
- [Book - time](https://time-rs.github.io/book/)
- [docs.rs](https://docs.rs/time/latest/time/#)

**Book** 中心にして **time** について見てみたいと思います。

まず最初に謳い文句として特徴についてです。

- **簡単・安全**
  - わかりやすい API 提供しているそうです。
    - たしかに、[time::OffsetDateTime](https://time-rs.github.io/api/time/struct.OffsetDateTime.html) で提供しているメソッドを見てみると、例えば **UTC時間での取得**や**日曜日から始まる週番号の取得**など直感的にやりたいことを実施できるようなメソッドなどが用意されていそうです。

- **最適化・効率化**
  - `time` は、ナノ秒の精度で **±9999** 年の範囲の日付をサポートしています。
  - さらに大きな範囲で、**±999,999** までの範囲は、`large-dates` 機能でサポートされています。
    - [time - Feature flags](https://docs.rs/time/latest/time/index.html#feature-flags)

- **シリアライズ・デシリアライズ**
  - シリアライゼーションするデファクトなフレームワークの `serde` に対応ということを銘打っています
  - [serde](https://crates.io/crates/serde)
    - (まだ使ったことないです)

- **マクロ**で簡単に日付を作成
  - [time::macros](https://time-rs.github.io/api/time/macros/index.html)

- Windows、Linux、macOS、WebAssemblyターゲットなどをサポート

## Day 74 のまとめ
