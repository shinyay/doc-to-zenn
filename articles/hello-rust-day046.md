---
title: "100日後にRustをちょっと知ってる人になる: [Day 46]型"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 46 のテーマ

[Day 44](https://zenn.dev/shinyay/articles/hello-rust-day044)、[Day 45](https://zenn.dev/shinyay/articles/hello-rust-day045)と様々な型のデータをまとめて管理するデータの取り扱いの仕組みである **構造体**と**列挙型**について見てみました。

ここで、基本に返って取り扱っているデータの **"型"** そのものについて見てみたいと思います。

## Rust の型

まず、Rust という言語そのものついてです。
プログラム言語には**型システム**という考え方があります。プログラムの構成要素や値に対して **型** という特性を割り付けるための体系です。
そして、その分類には次のようなものがあります。

- 型検査の性質
  - 動的型付け
  - 静的型付け
- 型解釈の性質
  - 強い型付け
  - 弱い型付け

**動的型付け**と**静的型付け**の違いとは、型を検査する**タイミング**の違いを表しています。

- **静的型付け**: プログラムの実行前 (**コンパイル時**または**インタプリタ開始時**)に型検査を行う
- **動的型付け**: プログラムを実行しながら型検査を行う

**強い型付け**と**弱い型付け**の違いとは、ある値がとる型に対して厳密化どうかという違いになります。

- **強い型付け**: ある処理や演算が間違っている型の引数を近視するため、検査をパスすると安全が保証されるという型付け
- **弱い型付け**: 案文句的に値の型を変換あるいはキャストするため、検査をパスしても安全さは必ずしも保証されない型付け

このような型システムの分類の中で、Rust は次のような型システムに分類されます:

- **静的型付け**
- **強い型付け**

## Rust の型変換

型分類で**強い型付け**に分類される Rust は暗黙的に型変換が行われることはありません。しかし、Rust は明示的には型変換を行うことが可能です。

`as` キーワードを使用して型を変換することが可能です。

```rust
let float = 3.1415_f32;
let integer = float as u8;

println!("型変換: {} -> {}", float, integer);
// 型変換: 3.1415 -> 3
```

**浮動小数点型** を **整数型** に明示的に切り上げました。

## Rust のリテラル

型変換の例で浮動小数点型を表すときにサフィックスに**f32**とつけていました。'3.1415**_f32**'
このように、サフィックスに型を指定することで Rust は型を指定する事が可能です。

サフィックスを付けずに型を表現する場合は、デフォルトの型が決まっています。

- **整数型の場合**: `i32`
- **浮動小数点型の場合**: `f64`

## 型のエイリアス

Rust では型名にエイリアス（別名）を設定することが可能です。

`type` キーワードを使って、既存の型に新しく別名をつけることができます。

名前の付け方にはルールがあり、**UpperCamelCase** にする必要があります。
ただし、プリミティブ型 (`f32` など)はその限りではないです。

```rust
type let nanoseconds: NanoSecond = 5; = u64;
let nanoseconds: NanoSecond = 5;
```

整数型の `u64` に対して、ナノ秒を表す型として `NanoSecond` という型を定義しました。

## Day 46 のまとめ

Rust が扱う型の性質について見てきました。

- 型システム
- 型変換
- リテラル
- 型エイリアス

Rust が言語の性質として、**静的型付け**かつ**強い型付け**と厳密な型システムな言語に分類されます。これによって安全がコードがかけると言えると思います。
しかし、**型変換**の仕組みや、**エイリアス**をつけることによって自由な型の操作ができそうだとも思いました。
