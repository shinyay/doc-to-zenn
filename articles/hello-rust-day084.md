---
title: "100日後にRustをちょっと知ってる人になる: [Day 84]書籍: Rust プログラミング完全ガイド その8"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 84 のテーマ

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
- [第15章 範囲とスライス](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC15%E7%AB%A0-%E7%AF%84%E5%9B%B2%E3%81%A8%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9)
- [第16章 イテレータを使う](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC16%E7%AB%A0-%E3%82%A4%E3%83%86%E3%83%AC%E3%83%BC%E3%82%BF%E3%82%92%E4%BD%BF%E3%81%86)
- [第17章 入出力とエラー処理](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC17%E7%AB%A0-%E5%85%A5%E5%87%BA%E5%8A%9B%E3%81%A8%E3%82%A8%E3%83%A9%E3%83%BC%E5%87%A6%E7%90%86)
- 第18章 データのカプセル化［メソッドとモジュール］
- 第19章 トレイトを使う
- 第20章 オブジェクト指向プログラミング
- 第21章 標準ライブラリのコレクション
- 第22章 所有権、移動、コピー
- 第23章 借用とライフタイム
- 第24章 さらにライフタイムについて

残り 7 章となりました。今日明日で読み終えようと思ってます。

## 第18章 データのカプセル化［メソッドとモジュール］

この章での内容:

- 関数を呼び出すのに、なぜ関数型記法よりドット記法のほうが便利なのか
- ドット記法を使って呼び出せる関数の宣言で、`impl` と `self` のキーワードを使う方法
- 関数宣言をモジュールに入れてカプセル化し、特定の関数だけを他のモジュールからアクセスできるようにする方法
- モジュールの階層構造を作り、その階層構造に属する任意の関数をアクセスする方法
- 型の別名 (エイリアス) を定義する方法

## 第19章 トレイトを使う
この章での内容:
- トレイトを使えば、ジェネリック関数の呼び出しに関するコンパイラのエラーメッセージが読みやすくなること
- ジェネリックパラメータの制約が 1 つにまとまったり、複数のトレイトに分かれたりする理由
- ジェネリックパラメータに制約がないと、できることがどれほど少ないか
- トレイトに入れた関数のスコープ
- 複数のメソッドを含むトレイトを作る方法
- 複数のトレイトに渡すジェネリックパラメータを制約する方法
- トレイト継承を使う方法
- トレイトを使って外部型にメソッドを追加する方法
- 標準トレイトの `Display` と `Debug` を実装する方法
- 便利なジェネリックトレイトを宣言する方法
- 型指定を持たないトレイトをシンプルに使える関連型
- イテレータの実装
## 第20章 オブジェクト指向プログラミング
## 第21章 標準ライブラリのコレクション
## 第22章 所有権、移動、コピー
## 第23章 借用とライフタイム
## 第24章 さらにライフタイムについて

## Day 84 のまとめ
