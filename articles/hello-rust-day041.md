---
title: "100日後にRustをちょっと知ってる人になる: [Day 41]幽霊型 Phantom Type"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 41 のテーマ

[Day 40](https://zenn.dev/shinyay/articles/hello-rust-day040) では、ジェネリクスで書くとやや複雑になりそうな場合に **関連型** という宣言の仕方を使って書き換えることを見てみました。

**型パラメータ**を利用して構造体や関数などの型を汎化させる仕組みのジェネリクスですが、この型パラメータを用いたデザインパターンがあります。
それが、**Phantom Type** といういもので、日本語だと**幽霊型**と呼ぶそうです。
個人的に今まで使ってきた言語では幽霊型と呼ぶようなものがなかった（僕が知らなかっただけ？）なので見ていこうと思います。

## 幽霊型

まず**幽霊型**がどういうものなのか、というのを様々な言語で定義でけられているものを見てみました。
Haskel, Swift, TypeScript, Sacala, Elm など大体次のような内容で説明されていました。

> 型パラメータを使用してコンパイル時には影響を与えるが、実行時の挙動には影響を与えない型を用いたデザインパターンの一種

正直良くわからない表現です。

### Rust 以外の言語での幽霊型

- Haskel のケース

```haskel
data Phantom x a = Phantom
```

- Scala のケース

```scala
case class Phantom[X, A](a: A)
```

いずれのケースも、**型パラメータ** `X` が定義はされているものの使われていないのです。ここで何をしようとしているとかというと、実際の値の型になる `A` は同だっとしても、`X, A` という組み合わせでコンパイルチェックを行い、誤った値を渡した場合にコンパイルエラーにするというもの、らしいです。

まだ正直よく分かりません…

### Rust での幽霊型

Rust で実例を見ながら考えたいと思います。

Rust でも同様に使用しない型パラメータの `X` と使用している型の `A` の組み合わせで構造体を定義します。

```rust
struct PhantomStruct<X, A> {
    value: A
}
```

この場合、次のようなコンパイルエラーが発生します。

>パラメータ `X` は決して使用されません。
>`X` を削除するか、フィールドで参照するか、あるいは `PhantomData` のようなマーカーを使用することを検討してください。
>もし、 `X` を 定数 パラメータにしたい場合は、代わりに `const X: usize` を使用してください。

当然ながら、`X` の削除あるいは利用、または `PhantomData` を使いなさいとエラーメッセージが出力されています。

以下から、`PhantomData` について見てみたいと思います。

- [Struct std::marker::PhantomData](https://doc.rust-lang.org/std/marker/struct.PhantomData.html)

おもしろい表現の説明がありました:

> `T` を所有する **ように振る舞う** ものをマークするために使用されるゼロサイズのタイプ。

実際には `T` 型の値を格納していないのにも関わらず、`T` 型の値を格納しているように動作するようコンパイラに対して支持をするのが、この `std::marker::PhantomData` です。

`PhantomData` を使用して、次のように構造体を修正します。

```rust
use std::marker::PhantomData;

struct PhantomStruct<X, A> {
    value: A,
    phantom: PhantomData<X>
}
```

これを次のようにインスタンスを作ります。

```rust
let _phantom1: PhantomStruct<i32, char> = PhantomStruct {
    value: 'P', 
    phantom: PhantomData
};

let _phantom2: PhantomStruct<i64, char> = PhantomStruct {
    value: 'P', 
    phantom: PhantomData
    };
```

## Day 41 のまとめ
