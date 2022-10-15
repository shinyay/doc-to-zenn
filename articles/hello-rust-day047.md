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

この中から `From` と `Into` について使い方を確認しておきます。

## From トレイト

`From` トレイトは次の様に定義されています。

```rust
pub trait From<T> {
    fn from(T) -> Self;
}
```

この `From` トレイトは、ある型に対して、別の方からその型を作る方法定義できるようにするものです。

例えば、`str` に対して `String` を作る場合は次のようになります。

```rust
let my_str = "my str";
let my_string = String::from(my_str);
```

また、`i32` から自作の `Number` 型 を作る場合は次のようになります。

```rust
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}
```

```rust
let num = Number::from(30);
```

つまり、このような実装ということになります。

```rust
impl From<変換元> for 変換先 {
    fn from(from: 変換元) -> 変換先 {
    }
}
```

## Into トレイト

`Into` トレイトは次のように定義されています。

```rust
pub trait Into<T> {
    fn into(self) -> T;
}
```

この `Into` は、`From` トレイトの逆の関係のトレイトになっています。
自作の型に `From` トレイトが実装されている場合、`Into` は必要に応じてそれを呼び出します。

```rust
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}
```

ここで `Into` を使用すると以下のように定義が行なえます。

```rust
let num: Number = 30.into();
```

つまり、同じ処理を以下の 2 種類で表わせるということになります。

- **From** トレイト
  - `let num = Number::from(30);`
- **Into** トレイト
  - `let num: Number = 30.into();`

## Day 47 のまとめ

`From` と `Into` が対になっているという説明をよく見かけるのですが、それだけを真に受けると変換の方向を誤解してしまうと思いました。
`From` と `Into` により `T` 型 と `U` 型の間で相互に変換可能になるのではありません。（はじめ僕もそうなのかと思っていました…）
変換の方向は同じで、`T` 型 → `U` 型という変換であることを間違えないように覚えておかないといけないと思います。
どちらも同じひょうげんだとすると、個人的には、`From` を実装していれば事足りるかなと思いました。

（`Into` ならではの使いどころはどこなんでしょう…とちょっと考えたい）

