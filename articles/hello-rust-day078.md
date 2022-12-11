---
title: "100日後にRustをちょっと知ってる人になる: [Day 78]書籍: Rust プログラミング完全ガイド その2"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 78 のテーマ

![](https://storage.googleapis.com/zenn-user-upload/942b1e806720-20221205.png)

[Day 76](https://zenn.dev/shinyay/articles/hello-rust-day076) から Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** を読み始めています。初回は 1 章から 3 章までを読みました。

- [第1章 Rustを始めよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC1%E7%AB%A0-rust%E3%82%92%E5%A7%8B%E3%82%81%E3%82%88%E3%81%86)
- [第2章 数値演算などの基本を把握しよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC2%E7%AB%A0-%E6%95%B0%E5%80%A4%E6%BC%94%E7%AE%97%E3%81%AA%E3%81%A9%E3%81%AE%E5%9F%BA%E6%9C%AC%E3%82%92%E6%8A%8A%E6%8F%A1%E3%81%97%E3%82%88%E3%81%86)
- [第3章 オブジェクトに名前を付ける](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC3%E7%AB%A0-%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E5%90%8D%E5%89%8D%E3%82%92%E4%BB%98%E3%81%91%E3%82%8B)
- 第4章 実行の流れを制御する
- 第5章 データシーケンスを使う
- 第6章 基本のデータ型を使う
- 第7章 列挙と照合
- 第8章 混成的なデータ構造を使う
- 第9章 関数を定義する
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

今日もその続きを読みながら、また感想をまとめたいと思います。なお、書籍のサマリーを書いてしまうと出版社に申し訳ないと思うので、あくまで感想と気に入った箇所を転記ではなく自分の言葉で書いてみる、というようなことができればいいかなと思っています。

### 第4章 実行の流れを制御する

この章での内容:

- 真偽の条件で選んだ一群の文を実行する `if` 文
- 真偽の条件で選んだ値を生成する `if` 式
- 真偽の条件が成立する間、一群の文を繰り返し実行する `while` 文
- 決まった回数だけ、一群の文を繰り返し実行する `for` 文
- 変数の有効性を決めるスコープ

`if` 文の書式について、`if` キーワードのあとに **丸括弧 ()** で囲む必要がない、囲まないのが普通、という説明がありました。Rust を書き始めてからは特に何も考えずに丸括弧をつけていませんでしたが、たしかに Java や Kotlin だと 丸括弧で囲んでいました。改めて納得をしてしまった説明でした。

```kotlin
var num = 1
if (num == 1) {
    println("Number: $num")
}
```

```rust
let num = 1;
if num == 1 {
    println!("Number: {}", num)
}
```

`if` **文** の次に `if` **式**が紹介されています。Kotlin では普通に `if` 式を使っていたのですが、よくよく思い返してみると Java にはいまだに `if` 式が実装されてはいないですよね。

```rust
let num = 0;
println!("{}", if num == 1 {
        "One"
    } else {
        "Etc"
    }
);
```

### 第5章 実行の流れを制御する

この章での内容:

- 同じ型を持つオブジェクト (配列やベクター) の並びを定義する方法
- 配列やベクターの初期内容を項目リストまたは項目と繰り返し回数の指定で設定する方法
- 配列やベクターの項目の値を読み書きする方法
- ベクター濃い木の追加と削除を行う豊富お
- 多次元配列の作り方
- 空の配列やベクターの作り方
- 配列やベクターの全体をコピーあるいはプリントする方法
- コンパイラがプログラミングエラーの疑いがあるコードを拒否するか黙ってゆるかを指定する方法
- パニックとは何か

### 属性についてのメモ

Rust のコンパイラはとても優秀で様々なエラーになりうるコードを分析してくれます。エラーになりうるけれど、実はエラーではないようなコード（最後に代入してから一度も使用していないコードなど）にどのように振る舞って欲しいかを設定することができます。

- **deny**: エラーメッセージを出し実行可能な**コードを生成しない**
- **warn**: 警告メッセージを出すが、実行可能な**コードを生成する**
- **allow**: メッセージを出さず、実行可能な**コードを生成する**

他の言語では実行時エラー発生時にスレッドの実行を中止することを**アボート**などと呼んでいそうな気がしますが、Rust では **パニック**と呼びます。パニック= `RuntimeException` の発生ととらえればいいと思います。

### 多次元配列についてのメモ

```rust
let mut x = [[[1; 2]; 4]; 8];
```

これが意味するのは、8 個の要素を持つ配列で、その各要素が 7 個の要素を持ち、そしてその要素のそれぞれが 2 個の要素を持つ、そんな多次元配列になっています。
プリントするときには、一番外側の配列から指定するので、次のようになります。

```rust
println!("{}", x[7][3][1]);
```

### ベクターについてのメモ

ベクターの定義には、`vec` マクロを使って作成します。

```rust
let mut x = vec!["Hello", "World", "in", "Rust"];
println!("{}", x.len());
```

ベクターの操作:

```rust
x.push("!");
x.remove(2);
x.insert(2, "for");
for i in 0..x.len() { print!("{} ", x[i]); } println!();
```

- `vector.push(item)` = `vector.insert(vector.len(), item)`
- `vector.pop()` = `vector.remove(vector.len() - 1)`

## Day 78 のまとめ

今日は、4 章の `if` に関して、5 章の配列・ベクターについて読みました。自分の理解とは別の説明内容での文章を読むと新しい気付きがあって学びが進みますね。この調子で読み進めようと思います。

- **第4章 実行の流れを制御する**
  - 真偽の条件で選んだ一群の文を実行する `if` 文
  - 真偽の条件で選んだ値を生成する `if` 式
  - 真偽の条件が成立する間、一群の文を繰り返し実行する `while` 文
  - 決まった回数だけ、一群の文を繰り返し実行する `for` 文
  - 変数の有効性を決めるスコープ
- **第5章 実行の流れを制御する**
  - 同じ型を持つオブジェクト (配列やベクター) の並びを定義する方法
  - 配列やベクターの初期内容を項目リストまたは項目と繰り返し回数の指定で設定する方法
  - 配列やベクターの項目の値を読み書きする方法
  - ベクター濃い木の追加と削除を行う豊富お
  - 多次元配列の作り方
  - 空の配列やベクターの作り方
  - 配列やベクターの全体をコピーあるいはプリントする方法
  - コンパイラがプログラミングエラーの疑いがあるコードを拒否するか黙ってゆるかを指定する方法
  - パニックとは何か