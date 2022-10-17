---
title: "100日後にRustをちょっと知ってる人になる: [Day 48]文字列の型: str型とString型"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 48 のテーマ

[Day 46](https://zenn.dev/shinyay/articles/hello-rust-day046) では、型を変換するためのトレイトな `From` と `Into` の使い方について見てみました。

`From` トレイトは、**ある型に対して、別の型からその型を作る方法を定義できるようにするもの**でした。
使い方の例として、`str` に対して `String` を作る場合の(サンプル](https://zenn.dev/shinyay/articles/hello-rust-day047#from-%E3%83%88%E3%83%AC%E3%82%A4%E3%83%88)を見てみました。

ところで、この文字列に関する 2 つの型があります。

- `str` 型
- `String` 型

これらをそれぞれどのようなもので、どんな時に使うべきなのかきちんと理解しているかどうか、ということを自分に確認する意味も込めて 2 つの型についてまとめようと思います。

## str 型と String 型

まず、それぞれの型で文字列を出力させてみます。

```rust
let s_str: &str = "This is str";
let s_string: String = String::from("This is String");

println!("str: {}", s_str);
println!("String: {}", s_string);
```

```shell
str: This is str
Strint: This is String
```

出力させる文字列の初期化の方法がことなりますが、いずれの型の場合も同じ様に出力することができています。

というわけで、性質の違いを見ていきたいと思います。

## str 型

まず `str` のリファレンスを見てみようと思います。

- [Primitive Type str](https://doc.rust-lang.org/std/primitive.str.html)

リファレンスにもかかれているように、`str` 型は Rust の**プリミティブデータ型**です。

このリファレンスに 2 つポイントになることが書かれています。

- 通常は**借用**した形で `&str` が使われる
- **文字列スライス**と呼ぶ

### なぜ借用

**借用**とは Rust の中で重要なコンセプトの 1 つで**所有権**を得ることなく値を参照する仕組みのことでした。
プリミティブ型の `str` では `This is str` と定義するとメモリ上に配置先が確保されて割り当てられる文字列のリテラルになります。
`&str` はその**メモリ上の位置を参照**するという呼び出し型なのです。

ここで気をつける必要があるのは、`This is str` を格納するために確保されたメモリ上の場所のため、`This is str` を入れるための大きさしか割り当てられていません。しらがって、この `&str` で定義した文字列に対して Concat など変更ができないのです。




## Day 48 のまとめ

