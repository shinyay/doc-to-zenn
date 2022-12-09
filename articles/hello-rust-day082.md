---
title: "100日後にRustをちょっと知ってる人になる: [Day 82]書籍: Rust プログラミング完全ガイド その6"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 82 のテーマ

![](https://storage.googleapis.com/zenn-user-upload/942b1e806720-20221205.png)

[Day 81](https://zenn.dev/shinyay/articles/hello-rust-day081) までに Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** の 1 章から 11 章までを読み終わりました。

- [第1章 Rustを始めよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC1%E7%AB%A0-rust%E3%82%92%E5%A7%8B%E3%82%81%E3%82%88%E3%81%86)
- [第2章 数値演算などの基本を把握しよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC2%E7%AB%A0-%E6%95%B0%E5%80%A4%E6%BC%94%E7%AE%97%E3%81%AA%E3%81%A9%E3%81%AE%E5%9F%BA%E6%9C%AC%E3%82%92%E6%8A%8A%E6%8F%A1%E3%81%97%E3%82%88%E3%81%86)
- [第3章 オブジェクトに名前を付ける](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC3%E7%AB%A0-%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E5%90%8D%E5%89%8D%E3%82%92%E4%BB%98%E3%81%91%E3%82%8B)
- [第4章 実行の流れを制御する](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC4%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第5章 データシーケンスを使う](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC5%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第6章 基本のデータ型を使う](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC6%E7%AB%A0-%E5%9F%BA%E6%9C%AC%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B%E3%82%92%E4%BD%BF%E3%81%86)
- [第7章 列挙と照合](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC7%E7%AB%A0-%E5%88%97%E6%8C%99%E3%81%A8%E7%85%A7%E5%90%88)
- [第8章 混成的なデータ構造を使う](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC8%E7%AB%A0-%E6%B7%B7%E6%88%90%E7%9A%84%E3%81%AA%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0%E3%82%92%E4%BD%BF%E3%81%86)
- [第9章 関数を定義する](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC9%E7%AB%A0-%E9%96%A2%E6%95%B0%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第10章 ジェネリックな関数や型を定義する](https://zenn.dev/shinyay/articles/hello-rust-day081#%E7%AC%AC10%E7%AB%A0-%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AA%E3%83%83%E3%82%AF%E3%81%AA%E9%96%A2%E6%95%B0%E3%82%84%E5%9E%8B%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第11章 メモリを割り当てる](https://zenn.dev/shinyay/articles/hello-rust-day081#%E7%AC%AC11%E7%AB%A0-%E3%83%A1%E3%83%A2%E3%83%AA%E3%82%92%E5%89%B2%E3%82%8A%E5%BD%93%E3%81%A6%E3%82%8B)
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

今週中にこの書籍を読み終えるためには少しペースを上げねばと思う今日この頃。さて、今日はどこまで読み進められるでしょうか。というわけで、読んでいきたいと思います。

## 第12章 データの実装

この章での内容:

- さまざまな方のオブジェクトがスタックに占めるバイト数を調べる方法
- 外部モジュールで宣言された関数をアクセスするパスを短縮する方法
- プリミティブ型のオブジェクトにビットがどう保存されるのか
- オブジェクトがメモリのどこに保存されのかを調べる方法
- パディングによって、ある種のオブジェクトが占めるサイズが増える理由
- ベクターはどの様に実装されるのか

### オブジェクトサイズ確認についてメモ

`size_of` 関数でオブジェクトサイズを確認します。`&i8` や `&i128` のようなリファレンスのサイズは、メモリアドレスのサイズです。

```rust
use std::mem::size_of;
println!("i8:{} i16:{} i32:{} i64:{} i128:{} bool:{} char:{} isize:{} usize:{} &i8:{} &i128:{}",
    size_of::<i8>(),
    size_of::<i16>(),
    size_of::<i32>(),
    size_of::<i64>(),
    size_of::<i128>(),
    size_of::<bool>(),
    size_of::<char>(),
    size_of::<isize>(),
    size_of::<usize>(),
    size_of::<&i8>(),
    size_of::<&i128>(),
);
```

```test
i8:1 i16:2 i32:4 i64:8 i128:16 bool:1 char:4 isize:8 usize:8 &i8:8 &i128:8
```

### メモリ上のバイト位置についてメモ

通常コードを書いている上でもは特にアドレスを意識することはないのかもしれません。ですが、厳密なルールも存在するので Rust 
におけるメモリへの配置位置のルールについてです。

- **プリミティブ型のオブジェクトは、どれもそのサイズの整数倍となるアドレスに置かなければならない。**

## 第13章 クロージャを定義する

この章での内容:

- 引数と戻り値が型推論され、波括弧を書く必要がなく、関数定義の時点で生きていた変数をアクセスできる、という無名のインライン関数がなぜ必要なのか
- そのような軽量関数 (**クロージャ**) を、どのようにすれば宣言して呼び出せるのか

### クロージャについてメモ

クロージャの基本的な書き方は次のようになります。

```rust
|arg: T| -> T {
    expr_1;
    ...
    expr_n
};
```

クロージャは引数や戻り値の型が自明であれば省略できます。つまり、次のようなクロージャはすべて同じ意味になります。

- 引数と戻り値の型を指定

```rust
let case1 = |x: u32| -> u32 { x + 1 };
```

- 型を省略

```rust
let case2 = |x| { x + 1 };
```

- 波括弧を省略

```rust
let case2 = |x| x + 1 ;
```

## 第14章 変更可能な文字列を使う

この章での内容:

- 静的な文字列がどのように実装されるのか
- 動的な文字列がどのように実装されるのか
- 動的文字列で、どうすれば文字の追加や削除ができるのか
- 静的文字列を動的文字列に、あるいはその逆に変換する方法
- 複数の文字列を連結する方法

### 静的文字列についてメモ

次のように `&str` 型で定義している文字列は変更できない文字列で、**静的文字列**と呼ばれます。

```rust
let a: &str = "This is String.";
```

ちなみに、次のように書くとエラーが発生します。

```rust
let a: str = "This is String.";
```

**[E0277] Error: the size for values of type `str` cannot be known at compilation time**

コンパイル時には文字列のサイズを知ることが出来ないというエラーが発生します。

`&str` 型は `str` への参照なのですが、**参照だけでなく**、**ポインタと長さのペア**になっています。

### 動的文字列についてメモ

文字列を実行時に作成したり変更したりする場合には、静的文字列の `&str` を使用することができません。
そこで、動的文字列の `String` 型を使用します。

以下のような `String` 型の定義方法があります。

```rust
let a = String::from("Hello String");
let b = "Hello String".to_string();
let c = "Hello String".to_owned();
let d = format!("Hello String");
```
## Day 82 のまとめ
