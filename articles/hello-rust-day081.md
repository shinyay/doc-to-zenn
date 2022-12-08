---
title: "100日後にRustをちょっと知ってる人になる: [Day 81]書籍: Rust プログラミング完全ガイド その5"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 81 のテーマ

![](https://storage.googleapis.com/zenn-user-upload/942b1e806720-20221205.png)

[Day 79](https://zenn.dev/shinyay/articles/hello-rust-day079) までに Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** の 1 章から 7 章までを読み終わりました。

- [第1章 Rustを始めよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC1%E7%AB%A0-rust%E3%82%92%E5%A7%8B%E3%82%81%E3%82%88%E3%81%86)
- [第2章 数値演算などの基本を把握しよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC2%E7%AB%A0-%E6%95%B0%E5%80%A4%E6%BC%94%E7%AE%97%E3%81%AA%E3%81%A9%E3%81%AE%E5%9F%BA%E6%9C%AC%E3%82%92%E6%8A%8A%E6%8F%A1%E3%81%97%E3%82%88%E3%81%86)
- [第3章 オブジェクトに名前を付ける](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC3%E7%AB%A0-%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E5%90%8D%E5%89%8D%E3%82%92%E4%BB%98%E3%81%91%E3%82%8B)
- [第4章 実行の流れを制御する](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC4%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第5章 データシーケンスを使う](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC5%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第6章 基本のデータ型を使う](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC6%E7%AB%A0-%E5%9F%BA%E6%9C%AC%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B%E3%82%92%E4%BD%BF%E3%81%86)
- [第7章 列挙と照合](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC7%E7%AB%A0-%E5%88%97%E6%8C%99%E3%81%A8%E7%85%A7%E5%90%88)
- [第8章 混成的なデータ構造を使う](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC8%E7%AB%A0-%E6%B7%B7%E6%88%90%E7%9A%84%E3%81%AA%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0%E3%82%92%E4%BD%BF%E3%81%86)
- [第9章 関数を定義する](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC9%E7%AB%A0-%E9%96%A2%E6%95%B0%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- 第10章 ジェネリックな関数や型を定義する
- 第11章 メモリを割り当てる
- 第12章 データの実装
- 第13章 クロージャを定義する
- 第14章 変更可能な文字列を使う
- 第15章 範囲とスライス
- 第16章 イテレータを使う
- 第17章 入出力とエラー処理
- 第18章 データのカプセル化［メソッドとモジュール］
- 第19章 トレイトを使う
- 第20章 オブジェクト指向プログラミング
- 第21章 標準ライブラリのコレクション
- 第22章 所有権、移動、コピー
- 第23章 借用とライフタイム
- 第24章 さらにライフタイムについて

今週中にこの書籍を読み終えようとおもっているのですが、今日はどこまで読み進められるでしょうか。というわけで、読んでいきたいと思います。

## 第10章 ジェネリックな関数や型を定義する

この章での内容:

- ただ 1 つの関数定義で呼び出しによって各種のデータ型を処理できるようにする豊富お
- ジェネリック関数が使う方の指定を型推論によって省略する方法
- 構造体やタプル構造体や列挙の型を、ただ 1 回書くだけで個々のインスタンスが別々のデータ型を格納できるようにする方法
- Option と Result という 2 種類の重要な標準ジェネリック列挙体の使い方。`Option` は選択可能なオプションを表現する。`Result` は失敗の有無と関数の実行結果を表す
- 標準関数を使って `Option` と `Result` の処理を容易にする方法

### ジェネリック関数についてメモ

**型パラメータ**の `T` 使っての関数の定義がジェネリック関数です。使用する時に具体的な型を指定、または型推論により型を指定します。

```rust
fn f<T>(param: T) ->T {
    param
}

let a = f(1);
let b = f(1.2);
let c = f("string");

println!("{:?}", a);
println!("{:?}", b);
println!("{:?}", c);
```

### ジェネリック構造体についてメモ

**型パラメータ**をジェネリックな構造体として使用する事もできます。

```rust
struct S<T1, T2> {
    n1: T1,
    n2: T2,
}

let a = S {
    n1: 1,
    n2: 'a',
};
```

### Option<T> 列挙体についてメモ

Option<T> は以下のように定義されています。

```rust
enum Option<T> {
    Some(T),
    None,
}
```

これは、**何か T 型であるものを返すか、あるいは返すものがない**という意味になります。

### Result<T> 列挙体についてメモ

Result<T> は次のように定義されています。

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Option や Result の値に関する処理を簡単にしてくれるユーティリティがあります。例えば以下のようなものです:

- [is_ok メソッド](https://doc.rust-lang.org/std/result/enum.Result.html#method.is_ok)
- [is_err メソッド](https://doc.rust-lang.org/std/result/enum.Result.html#method.is_err)
- [unwrap メソッド](https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap)

## 第11章 メモリを割り当てる

この章での内容:

- メモリ割り当ての種類。それぞれの性能と性質と制限事項
- あるオブジェクトに、どのアロケーションを使うかを Rust で指定する方法
- リファレンスと Box はどこが違うのか

### ヒープ領域 - BOX の使い方についてメモ

例えば次のような構造体があります。

```rust
struct Point {
    x: i32,
    y: i32,
}
```

これをヒープ領域に確保したい場合は、`Box` を使って次のようにします。

```rust
let p: Box<Point> = Box::new(Point {
    x: 1,
    y: 2,
});
```

```rust
println!("{} {}", p.x, p.y);
```

C 言語で `malloc()` を使用してヒープ領域を確保するような操作を、Rust では `Box` を使っていると思えばよいかもしれません。

## Day 81 のまとめ

今日は 10 章の**ジェネリック関数**をはじめとするジェネリックな構造についてと、 11 章の　ヒープ領域の使い方などに関するメモリの割当てについて読み進めてみました。

- **第10章 ジェネリックな関数や型を定義する**
  - ただ 1 つの関数定義で呼び出しによって各種のデータ型を処理できるようにする豊富お
  - ジェネリック関数が使う方の指定を型推論によって省略する方法
  - 構造体やタプル構造体や列挙の型を、ただ 1 回書くだけで個々のインスタンスが別々のデータ型を格納できるようにする方法
  - Option と Result という 2 種類の重要な標準ジェネリック列挙体の使い方。`Option` は選択可能なオプションを表現する。`Result` は失敗の有無と関数の実行結果を表す
  - 標準関数を使って `Option` と `Result` の処理を容易にする方法
- 第11章 メモリを割り当てる
  - メモリ割り当ての種類。それぞれの性能と性質と制限事項
  - あるオブジェクトに、どのアロケーションを使うかを Rust で指定する方法
  - リファレンスと Box はどこが違うのか
