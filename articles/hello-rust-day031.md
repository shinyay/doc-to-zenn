---
title: "100日後にRustをちょっと知ってる人になる: [Day 31]関連関数とメソッド - Rust By Example"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
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

関数には**特定の型** (構造体など) に紐付いて定義・使用される以下の形式があります。

- **メソッド**
- **関連関数**

`impl` ブロックの内部に、`&self`　つまり、呼び出されている構造体インスタンス自身を引数とする場合が**メソッド**、引数としない（つまりインスタンスが存在しない）場合が**関連関数**になります。

ちなみに、impl ブロックの内部で定義する **関連関数**に対し絵t、 impl ブロックの外部で定義されている関数を**自由関数**と呼びます。

https://github.com/shinyay/doc-to-zenn/blob/main/codes/day_31_functions/src/rectangle.rs

### 関連関数

**関連関数**は、インスタンスに対して関連付けられているのではなく、型自体に関連付けられている関数です。
そのため、新規のインスタンスを生成するコンストラクタに使われたりします。

- 関連関数サンプル

```rust
impl Rectangle {
    fn new(h: u32, w: u32) -> Rectangle {
        Rectangle { hight: h, widthe: w }
    }
}
```

- 関連関数呼び出しサンプル

```rust
let rec = Rectangle::new(3, 5);
```

### メソッド

**メソッド**は、インスタンスに対して関連づいています。つまり関数のように `fn` キーワードで定義します。ですが、関数ではありません。
また、定義するときに最初の引数は必ず `self` (このメソッドが呼び出されれているインスタンスを表す)

- メソッドサンプル

```rust
impl Rectangle {
    fn area(&self) ->u32 {
        self.hight * self.widthe
    }
}
```

- メソッド呼び出しサンプル

```rust
print!("Area={}", rec.area());
```

## Day 31 のまとめ

今日は、**[Rust By Example](https://doc.rust-lang.org/rust-by-example/)** の Functions のセクションを読みながら、関連関数とメソッドについて見てみました。

Java, Kotlin などを使ってきたぼくにとって、**メソッド**と**関数**の言葉の使い方が Rust を始めた当初にしっくりとこない点があったことを思い出しました。

- **メソッド**: メソッドが呼び出される**インスタンスに紐づく**
- **関連関数**: **インスタンスに関連づかない**で、型全体に紐づく
