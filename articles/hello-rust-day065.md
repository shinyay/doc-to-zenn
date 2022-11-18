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

上記の例ではまず、`Option` の列挙子でタプル構造体な `Some(T)` に数値を入れています。それを `match` でマッチングさせて取り出しています。
マッチングしている対象の値が１つしかありません。`match` はマッチングする条件を記述するためのものなので、当然ながら複数の条件を定義できます。
今回のように対象の値を１つしか定義しないパターンマッチングならば、`if let` という記法の方がシンプルに記述できます。

ちなみに、この `if let` ですが、`if` `let` ではないことに注意してください。`if` と `let` を組み合わせて利用しているように一見見えてしまいますが、この `if let` は１つのキーワードとして定義されているものです。

![](https://storage.googleapis.com/zenn-user-upload/db371d2c31d7-20221118.png)

そして、以下のように書き直せます。

```rust
if let Some(i) = optional {
    println!("Matched {:?}!", i);
}
```

ここの意味は `let Some(i) = optional` が、真なのか偽なのかを判定しています。
この `let` は代入という意味よりはパターンマッチングとして使われています。

```rust
// EXPRESSION: 何らかの値を返す「式」のこと
// PATTERN: 値がマッチするか否かに用いられる「パターン」のこと
let PATTERN = EXPRESSION;
```

もちろんパターンにマッチしない場合のケースとして、`else` を使用可能です。`else` の後のブロックで束縛を行います。

```rust
if let Some(i) = optional {
    println!("マッチしました {:?}!", i);
} else {
    rintln!{"マッチしません {:?}!", i};
}
```




## Day 65 のまとめ
