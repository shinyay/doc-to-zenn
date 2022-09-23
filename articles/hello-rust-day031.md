---
title: "100日後にRustをちょっと知ってる人になる: [Day 31]関数 - Rust By Example"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 31 のテーマ

[Day 30](https://zenn.dev/shinyay/articles/hello-rust-day030) でいろいろと Rust の学習用リソースをリスト化しました。
今日はその中のものを見ていこうと思い、**[Rust By Example](https://doc.rust-lang.org/rust-by-example/)** の内容を見たいと思います。

セクションとしては、以下の 24 種類用意されていました。

1. [Hello World](https://doc.rust-lang.org/rust-by-example/hello.html)
2. [Primitives](https://doc.rust-lang.org/rust-by-example/primitives.html)
3. [Custom Types](https://doc.rust-lang.org/rust-by-example/custom_types.html)
4. [Variable Bindings](https://doc.rust-lang.org/rust-by-example/variable_bindings.html)
5. [Types](https://doc.rust-lang.org/rust-by-example/types.html)
6. [Conversion](https://doc.rust-lang.org/rust-by-example/conversion.html)
7. [Expressions](https://doc.rust-lang.org/rust-by-example/expression.html)
8. [Flow of Control](https://doc.rust-lang.org/rust-by-example/flow_control.html)
9. [Functions](https://doc.rust-lang.org/rust-by-example/fn.html)
10. [Modules](https://doc.rust-lang.org/rust-by-example/mod.html)
11. [Crates](https://doc.rust-lang.org/rust-by-example/crates.html)
12. [Cargo](https://doc.rust-lang.org/rust-by-example/cargo.html)
13. [Attributes](https://doc.rust-lang.org/rust-by-example/attribute.html)
14. [Generics](https://doc.rust-lang.org/rust-by-example/generics.html)
15. [Scoping rules](https://doc.rust-lang.org/rust-by-example/scope.html)
16. [Traits](https://doc.rust-lang.org/rust-by-example/trait.html)
17. [macro_rules!](https://doc.rust-lang.org/rust-by-example/macros.html)
18. [Error handling](https://doc.rust-lang.org/rust-by-example/error.html)
19. [Std library types](https://doc.rust-lang.org/rust-by-example/std.html)
20. [Std misc](https://doc.rust-lang.org/rust-by-example/std_misc.html)
21. [Testing](https://doc.rust-lang.org/rust-by-example/testing.html)
22. [Unsafe Operations](https://doc.rust-lang.org/rust-by-example/unsafe.html)
23. [Compatibility](https://doc.rust-lang.org/rust-by-example/compatibility.html)
24. [Meta](https://doc.rust-lang.org/rust-by-example/meta.html)

この中から、[Functions](https://doc.rust-lang.org/rust-by-example/fn.html) (関数) を見てみたと思います。

## 関数

- 関数の定義方法: `fn` キーワード
  - 型定義:
    - 引数は、型を指定する必要あり (例: fn foobar(`n: u32`) -> u32 )
    - 戻り値は、->の後に型を指定する必要あり (例: fn foobar(n: u32) `-> u32` )

https://github.com/shinyay/doc-to-zenn/blob/main/codes/day_31_functions/src/main.rs

### Associated functions (関連関数) とメソッド

関数には**特定の型**に紐付いて定義・使用される以下の形式があります。

- **メソッド**
- **関連関数**

## Day 31 のまとめ
