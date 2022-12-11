---
title: "100日後にRustをちょっと知ってる人になる: [Day 83]書籍: Rust プログラミング完全ガイド その7"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 83 のテーマ

![](https://storage.googleapis.com/zenn-user-upload/942b1e806720-20221205.png)

[Day 82](https://zenn.dev/shinyay/articles/hello-rust-day082) までに Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** の 1 章から 14 章までを読み終わりました。

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
- [第12章 データの実装](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC12%E7%AB%A0-%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E5%AE%9F%E8%A3%85)
- [第13章 クロージャを定義する](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC13%E7%AB%A0-%E3%82%AF%E3%83%AD%E3%83%BC%E3%82%B8%E3%83%A3%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第14章 変更可能な文字列を使う](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC14%E7%AB%A0-%E5%A4%89%E6%9B%B4%E5%8F%AF%E8%83%BD%E3%81%AA%E6%96%87%E5%AD%97%E5%88%97%E3%82%92%E4%BD%BF%E3%81%86)
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

残りもう少しなので、この週末中に読み終えようと思っています。

## 第15章 範囲とスライス

この章での内容:

- 終点を含まない範囲も、終点を含む範囲も指定できること
- 範囲を使って、配列やベクターやその他のスライスを定義して使う方法

### 範囲についてメモ

**範囲**とは、`Range<T>` というジェネリック型を具現化したものです。

```rust
let range: std::ops::Range<usize> = 1..10;

println!("
    Range: {:?},
    Start: {},
    End: {},
    Length: {}",
    range, range.start, range.end, range.len());
```

## スライスについてメモ

配列やベクターは、異なる特徴は持っていますが、複数の要素を持つという点で同じようなデータ構造です。これらが持つ要素を参照するために**スライス**という方法があります。

```rust
{
    let arr = [0, 1, 2, 3, 4, 5];
    let vec = vec![0, 1, 2, 3, 4, 5];
    let sarr = &arr[1..3];
    let svec = &vec[3..5];
    println!("{:?}, {:?}", sarr, svec);
}
```

スライスには**ファットポインタ**という構造があり、次の 2 つの値を持っています。

- スライスの最初の要素を指すポインタ
- スライスに含まれる要素数

## 第16章 イテレータを使う

この章での内容:

- Rust でキャラクタ (文字) が文字列に、どう格納されるのか。なぜ直接アクセスできないのか
- イテレータを使って、文字列のキャラクタまたはバイトを読む方法
- イテレータを使って、ベクターや配列から項目を抽出する方法
- 非可変イテレータを使って、ベクターや配列やスライスの項目への参照を取得する方法
- 可変イテレータを使って、ベクターや配列やスライスの項目を変更する方法
- `for` ループでイテレータを使う簡略記法
- イテレータアダプタ (`filter`, `map`, `enumerate`) の使い方
- イテレータコンシューマ (`any`, `all`, `count`, `sum`, `min`, `max`, `collect`) の使い方
- イテレータの連鎖と遅延評価について

**イテレータ**とは、シーケンスの現在位置から項目を抽出した後、それを次の位置まで進めるという動作を実行するオブジェクトのことです。

```rust
fn print_codes(s: &str) {
    for c in s.chars() {
        println!("{}: {}", c, c as u32);
    }
}
print_codes("abcde");
```

`into_iter()` を使用して配列やベクターのイテレータを使用します。

```rust
for item in vec![1, 2, 3, 4, 5].into_iter() {
    println!("{} ", item * 2);
}
```

`into_iter()` を省略して次のように記述できます。

```rust
for item in &vec![1, 2, 3, 4, 5] {
    println!("{} ", *item * 2);
}
```

`iter()` を使用して書くことも可能です。

```rust
for item in vec![1, 2, 3, 4, 5].iter() {
    println!("{} ", *item * 2);
}
```

### イテレータジェネレータ

- 値の取捨選択
  - [filter](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.filter)

- 値の変換
  - [map](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.map)

- カウンタ
  - [enumerate](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.enumerate)

### イテレータコンシューマ

- どれかを判定
  - [any](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.any)

- すべてを判定
  - [all](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.all)

- 個数を数える
  - [count](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.count)

- 値を合計する
  - [sum](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.sum)

- 最小値を求める
  - [min](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.min)

- 最大値を求める
  - [max](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.max)

- コレクションを作る
  - [collect](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.collect)

## 第17章 入出力とエラー処理

この章での内容:

- プログラムを起動したコマンドラインから引数を受け取る方法
- プログラム終了時のステータスコードを OS に返す方法
- プロセスの環境変数を取得/設定する方法
- ランタイムエラーを処理する技法とベストプラクティス
- コンソールのキーボード入力を読み出し、スクリーンに出力する方法
- プリミティブ型を文字列に変換する方法
- バイナリファイルを読み書きする方法
- テキストファイルを行ごとに読む方法

## Day 83 のまとめ

- **第15章 範囲とスライス**
  - 終点を含まない範囲も、終点を含む範囲も指定できること
  - 範囲を使って、配列やベクターやその他のスライスを定義して使う方法
- **第16章 イテレータを使う**
  - Rust でキャラクタ (文字) が文字列に、どう格納されるのか。なぜ直接アクセスできないのか
  - イテレータを使って、文字列のキャラクタまたはバイトを読む方法
  - イテレータを使って、ベクターや配列から項目を抽出する方法
  - 非可変イテレータを使って、ベクターや配列やスライスの項目への参照を取得する方法
  - 可変イテレータを使って、ベクターや配列やスライスの項目を変更する方法
  - `for` ループでイテレータを使う簡略記法
  - イテレータアダプタ (`filter`, `map`, `enumerate`) の使い方
  - イテレータコンシューマ (`any`, `all`, `count`, `sum`, `min`, `max`, `collect`) の使い方
  - イテレータの連鎖と遅延評価について
- **第17章 入出力とエラー処理**
  - プログラムを起動したコマンドラインから引数を受け取る方法
  - プログラム終了時のステータスコードを OS に返す方法
  - プロセスの環境変数を取得/設定する方法
  - ランタイムエラーを処理する技法とベストプラクティス
  - コンソールのキーボード入力を読み出し、スクリーンに出力する方法
  - プリミティブ型を文字列に変換する方法
  - バイナリファイルを読み書きする方法
  - テキストファイルを行ごとに読む方法