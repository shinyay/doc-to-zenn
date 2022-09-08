---
title: "100日後にRustをちょっと知ってる人になる: [Day 17]トレイト"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 17 のテーマ

Day 16 でクロージャの扱いについて考えている中で、きちんと Rust の**トレイト**という仕組みのことを理解した上でないと説明しきれないところがあると思いました。
ということで、今日は**トレイト**についてまとます。

## トレイト

基本に立ち戻り、[The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html) でのトレイトの定義を見てみようと思います。

- [Traits: Defining Shared Behavior](https://doc.rust-lang.org/book/ch10-02-traits.html)

> A trait defines functionality a particular type has and can share with other types.

つまり、**特定の型に対して任意の振る舞いを設定するための機能** です。言い換えると、**複数の型で利用目的や呼び出し方法が共通である関数があるとき**、それらをトレイトとしてまとめて使用します。

### トレイトの定義

`trait` キーワードを使用してトレイトの定義を行います。

- [Keyword trait](https://doc.rust-lang.org/std/keyword.trait.html)

トレイトは次の3つの項目から構成することができます:

- 関数とメソッド
- 型
- 定数

```rust
trait TraitName {
    fn method_name()
}
```

たとえば、`FooBar` というトレイトを定義しまう。ここでは、とりあえず何処理を行うのみのメソッドを定義しています。

```rust
trait FooBar {
    fn do_something(&self);
}
```

### トレイトの実装

`impl` キーワードを使用してトレイトの実装を行います。
`impl` キーワードの後に実装するトレイト名を宣言し、`for` キーワードを置いて実装対象の型名を指定します。型名は構造体定義を使うことが多いかなと思いました。

たとえば、`Foo`と`Bar`という構造体があったとします。その構造体に対してトレイトを使用して処理を追加することができます。それぞれの構造体に対して `println!`マクロで標準出力をする処理を追加しました。

```rust
struct Foo;
impl FooBar for Foo {
    fn do_something(&self) {
        println!("Foo");
    }
}

struct Bar;
impl FooBar for Bar {
    fn do_something(&self) {
        println!("Bar");
    }
}
```

### 呼び出し

以下のようにして呼び出すことが可能です。
トレイトを実装した構造体 `Foo`と`Bar`のインスタンスを生成し、実装したメソッドを呼び出しています。

```rust
    let foo = Foo;
    let bar = Bar;

    foo.do_something();
    Bar::do_something(&bar);

    FooBar::do_something(&foo);
    FooBar::do_something(&bar);
```

## Day 17 のまとめ

今日は**トレイト**についていろいろと見てみました。Rustは厳密なオブジェクト指向ではないですよね。継承がRustにはないですが、トレイトを使って**ポリモフィズム**ができるので、オブジェクト指向風にはプログラムを書くことができそうですよね。
このトレイトを上手に使うことが Rust のプログラムを作っていく肝にもなりそうな気がしました。
