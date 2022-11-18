---
title: "100日後にRustをちょっと知ってる人になる: [Day 65]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 65 のテーマ

[Day 64](https://zenn.dev/shinyay/articles/hello-rust-day064) で Rust 1.65.0 のアナウンスノートを眺めてみましたが、そこに `let-else` 文に関する内容がありました。それについては、昨日どのような構文になるかは少し記載したのですが、元々 今までのバージョンにあった `let` 式の使い方との比較などは説明をしていませんでした。

つまり、今回のバージョンアップで、`let-else` 文が追加されることによって、今まで出来ていなかったどのような事が解決できるようになったのか、眺めてみたいかなと思います。

## 既存の if-let

Rust 公式ドキュメント (<https://doc.rust-lang.org/>) の中では `if let` 文について、[列挙型とパターンマッチングのセクション](https://doc.rust-lang.org/book/ch06-03-if-let.html)で紹介されています。

`if let` を使用しないで `match` によるパターンマッチングをしているケースをまず見てみます。

```rust
let optional = Some(5);
match optional {
    Some(i) => {
        println!("Matched {:?}!", i)
    },
    _ => {},        
}
```

## Day 65 のまとめ
