---
title: "100日後にRustをちょっと知ってる人になる: [Day 32]クロージャ"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 32 のテーマ

[Day 31](https://zenn.dev/shinyay/articles/hello-rust-day031) では、Rust の関数 (**関連関数**と**メソッド**) について見てみました。
今日はもう 1 つの関数の使い方の**クロージャ**について見てみようと思います。

### クロージャとは

Rust に限らず、いろいろな言語でも クロージャは提供されています。クロージャを使ったコーディングはいろいろなところで活用されてきていると思います。

- [Java](https://openjdk.org/projects/closures/)
- [Kotlin](https://kotlinlang.org/docs/lambdas.html#closures)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)

しかし、一方でクロージャとは何か？のような説明もあちこちで見かけたりしますよね。日本語で **[関数閉包](https://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%83%BC%E3%82%B8%E3%83%A3)** などとされているので分かりにくいのだと思います。簡単に説明すると、変数に束縛できて、関数の引数として渡すことができ名前のない関数 (**無名関数**) のことです。また、関数と異なり、クロージャはその呼び出し元のスコープにある変数をキャプチャすることも出来ます。
つまり、クロージャを使うと以下のような性質で関数が使えることになります。

✅ 生成や代入が可能な関数となる
✅ 引数や戻り値として受け渡しておき、あとから呼び出せる
✅ あとから呼び出した場合、定義した時点で有効な定数や変数にアクセスできる

### Rust でのクロージャ

Rust ではクロージャを `||` で定義します。引数がある場合は、`|param1, param2|` というようにします。`||` のあとに `{}` ブロックで処理の本体を記述します。この処理が式 1 つのみなら `{}` を省略可能です。

- 関数

```rust
fn do_something(param: u32) -> u32 { param + 1 }
```

- クロージャ

```rust
let do_something = |param: u32| -> u32 { param + 1 };
```

- クロージャ (型アノテーションを省略)

```rust
let do_something = |param| { param + 1 };
```

- クロージャ (ブロックを省略)

```rust
let do_something = |param| param + 1 ;
```

クロージャの外部にあるスコープの要素は、以下のような形で取得できます。

- リファレンス: `&T`
- ミュータブルなリファレンス: `&mut T`
- 値そのもの: `T`

```rust
let outer_scope = String::from("スコープ");
let print = ||println!("スコープ: {}", outer_scope);
print();
```

## クロージャとトレイト

**クロージャ**が定義されると，コンパイラは暗黙のうちに新しく**無名の構造体**を作り，その中に取り込んだ変数を格納します。
そして、以下のいずれかの特性によって機能を実装します:

- `Fn`
- `FnMut`
- `FnOnce`

言い換えると、クロージャはいずれかのトレイトのインスタンスになっています。

- **Fn トレイト**
  - `&self` を受け取る
  - `FnMut` を継承する
    - `FnOnce` を継承する

```rust
pub trait Fn<Args>: FnMut<Args> {
    extern "rust-call" fn call(&self, args: Args) -> Self::Output;
}
```

- **FnMutトレイト**
  - `&mut self` を受け取る
  - `FnOnce` を継承する

```rust
pub trait FnMut<Args>: FnOnce<Args> {
    extern "rust-call" fn call_mut(&mut self, args: Args) -> Self::Output;
}
```

- **FnOnce トレイト**
  - `self` を受け取る

```rust
pub trait FnOnce<Args> {
    type Output;
    extern "rust-call" fn call_once(self, args: Args) -> Self::Output;
}
```

### トレイトの選択のされ方

3 種類のトレイトを見れば分かるように、クロージャで定義する処理のされ方によっていずれかのトレイトが実装されます。

- 処理の中で**キャプチャした変数**を**書き換えている場合**、`self` あるいは `&mut self` を受け取る
  - **成立する実装**
    - `FnOnce`
    - `FnMut`
  - **成立しない**
    - `Fn`
- 処理の中で**キャプチャした変数**の**所有権を手放している場合**
  - **成立する**
    - `Fn`

## Day 32 のまとめ

Rust でのクロージャの使い方について簡単に見てみました。関数自体を引数に使ったり、戻り値として扱うようなものと考えれば利用の仕方はいろいろ増えますよね。
スコープの扱いについて考慮だけすれば、まずはクロージャの使いこなしの第一歩なのかなと思います。
