---
title: "100日後にRustをちょっと知ってる人になる: [Day 9]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---

## Day 9 のテーマ

今日は [The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html)の第３章を一通り読んでおこうと思います。

- [Common Programming Concepts](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

この章は、文字通り Rust 固有の言語仕様というよりは、一般的なプログラム開発に最低限求められる以下の概念を Rust を使って説明しています。

- [変数](https://doc.rust-jp.rs/book-ja/ch03-01-variables-and-mutability.html)
- [データ型](https://doc.rust-jp.rs/book-ja/ch03-02-data-types.html)
- [関数](https://doc.rust-jp.rs/book-ja/ch03-03-how-functions-work.html)
- [コメント](https://doc.rust-jp.rs/book-ja/ch03-04-comments.html)
- [制御フロー](https://doc.rust-jp.rs/book-ja/ch03-05-control-flow.html)

それぞれを見ていこうと思います。

## 変数

### 可変性

Rust では変数はデフォルトで**不変** (Immutable) になっています。

同じ名前の変数に２回値を設定すようとする、以下のコードを実行しようとすると、

```rust
fn main() {
    let x = "Hello World";
    println!("xの値は {} です", x);
    x = "Hello Rust";
    println!("xの値は {} です", x);
}
```

次のようなエラーが発生します。

```shell
error[E0384]: cannot assign twice to immutable variable `x`

  |     x = "Hello Rust";
  |     ^^^^^^^^^^^^^^^^ cannot assign twice to immutable variable
```

Rust では、値が変更しないということをコンパイラが担保してくれるため、意図しないところで値が変わってしまい発生するバグを回避することができるのです。

この変数を可変として定義し、値を変更可能にする場合は、`mut` キーワードを使用します。

```rust
let mut x = "Hello World";
```

### 変数と定数

`let` キーワードではなく、`const` キーワード を使って **定数**を定義できます。この定数は不変変数のように値を変更することができません。
Rustの定数の命名規則は、 **全て大文字**で**アンダースコアで単語区切り** です
変数と定数の違いは以下の点です。

- 定数は**型推論**されない
  - 常に型を**注釈**する必要があります
- 定数は `mut` キーワードを使って可変にすることができません
- 定数はグルーバルスコープも含め、**あらゆるスコープ**で定義可能です

### シャドーイング

素手に定義した変数と同じ名前の変数を新しく宣言でき、 新しい変数は、前の変数を覆い隠し(**シャドーイング**)ます。

```rust
fn main() {
    let x = 1;
    let x = x + 2;
    {
        let x = x * 3;
        println!("インナースコープの値: {}", x);  // -> (1+2)*3 = 9
    }
    println!("アウタースコープの値: {}", x);      // -> 1+2 = 3
}
```

変数を `mut` で可変にしているのとは異なり、新しく変数を生成して上書きを行っています。

## データ型

Rust における値は全て何らかの**データ型**になっています。

### スカラー型

スカラー型とは単独の値を表す型のことです。
Rust では以下のスカラー型があります
- 整数型
- 浮動小数点型
- 論理値型
- 文字型

#### 整数型

サイズと符号の有無で以下のような整数型があります。

|サイズ|符号付き|符号なし|
|-----|------|-------|
|8 bit|`i8`|`u8`|
|16 bit|`i16`|`u16`|
|32 bit|`i32`|`u32`|
|64 bit|`i64`|`u64`|
|arch|`isize`|`usize`|

#### 浮動小数点型

以下の2種類の基本型があります。

- `f32`
  - 32 bit
- `f64`
  - 64 bit
  - **デフォルト**

```rust
let x = 1.0; // f64
let y: f32 = 2.0; // f32
```

#### 論理値型

**論理値型**: `bool`

論理値として扱える値は `true` と `false` です。

#### 文字型

**文字型**: `char`

- 文字列: ダブルクォーテーション ("")
- 文字型: シングルクォーテーション ('')

### 複合型

複合型とは複数の値を一つの型にまとめることができる型のことです。
Rust には 2種類の複合型があります。

- タプル型
- 配列

#### タプル型

**タプル**は"複数の型"の"何らか値"を一つの型にまとめる方法です。
丸括弧の中にカンマ区切りで値リストを書いて生成します。

```rust
let tup = (100, 2.3, 4);
```

#### 配列

**配列**はタプルとは異なり全要素が同じ型である必要があります。
Java などの他の言語と異なり、配列のサイズは固定長です。一度宣言すると、サイズの変更はできません。

配列の型は要素の型と要素数で定義します。

- 要素の型: `i32`
- 要素数: `5`

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

## 関数

Rust の関数と変数の命名規則は、**スネークケース**を使うのが慣例です。

Rustにおいて関数定義は、`fn` キーワードで始まり、**関数名**の後に**丸かっこ**の組が続きます。
**波かっこ**が、コンパイラに関数本体の開始と終了の位置を伝えます。

```rust
fn 関数名() {
    do something;
}
```

### 関数の引数

- **引数**: 関数シグニチャの一部になる変数のこと

```rust
fn main() {
    another_function(1);
}

fn another_function(x: i32) {
    println!("x の値は {} です", x);
}
```

Rust の仕様上のポイント: **関数シグニチャにおいて、各仮引数の型を宣言しなければなりません**

### 関数の戻り値

矢印(->)の後に型を書いて戻り値を宣言します。

```rust
fn main() {
    let x = five();
    println!("x の値は {} です", x);
}

fn one() -> i32 {
    1
}
```

## Day 9 のまとめ

プログラムを作るときに必ず必要になる要素、**変数**, **データ型**, **関数**について追いかけてみました。
Rust 固有の仕様というよりは、一般的なプログラム開発の概念ということでした。
Rust を使ってプログラムを書いていく上での最低限必要なところをおさえてみた、というような Day 9 でした。