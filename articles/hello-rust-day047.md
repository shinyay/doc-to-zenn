---
title: "100日後にRustをちょっと知ってる人になる: [Day 47]型変換ためのトレイト: From / Into"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 47 のテーマ

[Day 46](https://zenn.dev/shinyay/articles/hello-rust-day046) では、Rust の**型**に関して見てみました。どのような型システムをとっているのか、また型を明示的に変換するキャストの仕組みなどについて確認を行いました。

ところでこの型の変換に関してですが、`std::convert` という型を変換するトレイトを提供しているモジュールがあります。

- [`std::convert`](https://doc.rust-lang.org/std/convert/index.html)

提供しているトレイト毎に目的が異なった変換を実施します:

- [AsRef](https://doc.rust-lang.org/std/convert/trait.AsRef.html): 参照から参照への変換
- [AsMut](https://doc.rust-lang.org/std/convert/trait.AsMut.html): MutableからMutableへの変換
- [From](https://doc.rust-lang.org/std/convert/trait.From.html): 値から値への変換
- [Into](https://doc.rust-lang.org/std/convert/trait.Into.html): 現在のクレートの外側の型への値から値への変換


## Day 47 のまとめ
