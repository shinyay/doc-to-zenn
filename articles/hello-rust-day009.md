---
title: "100日後にRustをちょっと知ってる人になる: [Day 9]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
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

## データ型

## 関数

## コメント

## 制御フロー

## Day 9 のまとめ
