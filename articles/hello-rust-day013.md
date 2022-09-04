---
title: "100日後にRustをちょっと知ってる人になる: [Day 13]FizzBuzz"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 13 のテーマ

今日は **FizzBuzz** を作ってみようと思います。
プログラム言語を学ばれる方って、まず最初に `Hello Wolrd` から入って、少し言語仕様を学んで、そしてお試しに FizzBuzz を作ってみるという方って多いですよね。そんな基本に忠実にぼくも今日は FizzBuzz を少し考えてみようと思います。

### FizzBuzz

まず、**FizzBuzz**についてです。
先にもふれたように、プログラム言語の基礎力確認のための問題です。以下のような内容のものを実装します。

- **1 から 100** までの各数値を新しい行に出力するプログラムを作成します。

- **3 の倍数**ごとに、数字の代わりに `Fizz` と出力します。

- **5 の倍数**ごとに、数字の代わりに `Buzz` と出力します。

- **3 と 5 の両方の倍数**である数値については、数値の代わりに `FizzBu​​zz` を出力します。

### 基本的な FizzBuzz

`for` ループと `if`-`else` ステートメントを使って以下のように記載してみました。

```rust
for x in 1..=100 {
    if x % 3 == 0 && x % 5 == 0 {
        println!("FizzBuzz")
    } else if x % 3 == 0 {
        println!("Fizz")
    } else if x % 5 == 0 {
        println!("Buzz")
    } else {
        println!("{}", x)
    }
}
```

## Day 13 のまとめ
