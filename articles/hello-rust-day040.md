---
title: "100日後にRustをちょっと知ってる人になる: [Day 40]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 40 のテーマ

[Day 33](https://zenn.dev/shinyay/articles/hello-rust-day033) でジェネリクスに関する基本内容を確認しました。

以下のように、ダイヤモンド演算子 `<>` を使い、ジェネリック型の名前を指定することで定義する事ができることを確認していました。

```rust
struct Point<T> { x: T, y: T }

impl<T> Point<T> {
    fn do_something(self) -> (T, T) {
        (self.x, self.y)
    }
}
```

また、ジェネリック型の対して特定の処理 (**トレイト**) を実装しなければならないという事ができることを確認していました。その方式を **トレイト境界**と呼び、以下のように定義することを確認していました。

```rust
fn printer<T: Display>(t: T) {
    println!("{}", t);
}
```

上記の例では、`Displya` トレイトを実装している `T` 型をパラメータとして受け取る `printer` 関数が定義されています。つまり、`println!` マクロでパラメータを表示させようとしていますが、`T` が指定されたトレイトを実装していない場合はコンパイルエラーになってしまいます。

このように、ジェネリクスをつかってプログラムをコンパクトに書きつつも規定をかけていくことができることを確認できていました。

今回はジェネリクスを使って便利にすることができる、**Associated Type (関連型)**と**Phantom Type (幽霊型)** についてまとめたいと思います。
（しかし、ほんとに日本語訳として幽霊型でまかり通っているのかな？？？🤔）

## 関連型

### 関連型を使っていない場合

まず最初に次のケースでのジェネリクスの利用について考えてみてください。

- あるトレイトがジェネリック型を用いて定義されている場合

この場合、このトレイトが実装されたものを使用する場合どうなるでしょうか？

実装例を見ながら考えてみましょう。

- 構造体

```rust
// 32 bit の整数型の要素を２つもつ構造体
struct Point(i32, i32);
```

- トレイト

```rust
// Point の座標があっているかどうかを確認するトレイト
trait Position<X, Y> {
    fn exist(&self, _: &X, _: &Y) -> bool;
    fn h_axis(&self) -> i32;
    fn v_axis(&self) -> i32;
}
```

- 実装

```rust
impl Position<i32, i32> for Point {
    // ２つの要素が正しいことを確認
    fn exist(&self, x: &i32, y: &i32) -> bool {
        (&self.0 == x) && (&self.1 == y)
    }

    // x座標を取得
    fn h_axis(&self) -> i32 {
        self.0
    }

    // y座標を取得
    fn v_axis(&self) -> i32 {
        self.1
    }
}
```

- main 関数

```rust
fn main() {
    let x = 5;
    let y = 10;

    let point = Point(x, y);

    println!("Point X:{}, Y:{}", &x, &y);
    println!("Exist?:{}", point.exist(&x, &y));

    println!("Point-X:{}", point.v_axis());
    println!("Point-X:{}", point.h_axis());
}
```

ここまでで、一旦動くようになります。
ですが、次のことを考えてみてください。

トレイト境界として `Position` を制約された引数をもつ関数がある場合はどうなるでしょうか？
次のように、`X` と `Y` は `Z` に含まれているにも関わらず、`X` と `Y` を 2 回書いています。

```rust
fn new_point<X, Y, Z>(point: &Z) where Z: Position<X, Y> {...}
```

冗長なので、できれば 2 回は書きたくないですよね。

こういう場合に関連型を使うと便利になります。

### 関連型を使う場合

関連型を使うと、トレイトの中に **アウトプット型** として書くことにより可読性を向上させることができます。

次のようにトレイトを定義します。
ポイントとしては、`X` と `Y` を `type` キーワードを使って**トレイト内部で定義**するようにしています

```rust
trait Position {
    type X;
    type Y;

    fn exist(&self, _: &Self::X, _: &Self::Y) -> bool;
    fn h_axis(&self) -> i32;
    fn v_axis(&self) -> i32;
}
```

## Day 40 のまとめ

