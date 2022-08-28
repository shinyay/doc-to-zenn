---
title: "100日後にRustをちょっと知ってる人になる: [Day 6]はじめての Rust プログラミング"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---

## Day 5 のテーマ

[The Rust Programming Language](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html) の第2章で数当てゲームの実装をしながら、Rust プログラミングの基本を学ぶということが行われています。

- [Programming a Guessing Game](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html)

この第2章の内容を追いかけてみたいと思います。

## 数当てゲームの実装

次のような内容のプログラムを実装します:

- 1 から 100 までのランダムな整数を生成
- プレイヤーに予想した数字の入力を要求
- 入力値が小さいか大きいかを表示
- 一致したらメッセージを表示

### プレイヤーからの入力

プレイヤーに標準入力で予測値の入力を要求します。

```rust
fn main() {
    println!("数を予想しましょう。");
    println!("予想した値を入力してください。");
    
    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("読み込みに失敗しました。");
        
    println!("次のように予測しています: {}", guess);
}
```

#### 標準入出力ライブラリ (`io`)

`std` という標準ライブラリに含まれている `io` (入出力ライブラリ) を使用します。

```rust
use std::io;
```

入力を受け取るときには、`read_line` メソッドを呼び出しています。

- [read_line](https://doc.rust-lang.org/std/io/struct.Stdin.html#method.read_line)

```rust
pub fn read_line(&self, buf: &mut String) -> Result<usize>
```

引数に**可変変数**の文字列を**参照**で渡されていることが分かります。参照渡ししたデータは何度もメモリにコピーしなくても済むため経済的です。

`&` キーワードにより、それがついている引数は**参照**であることを表します。

#### 不変変数(immutable) と 可変変数(mutable)

Rust では変数はデフォルトでは、**不変変数(immutable)**です。
その変数を **可変変数(mutable)** にする場合は、変数名の前に `mut` をつけて定義します。

```rust
let mut guess = String::new();
```

#### println のプレースホルダー

`println!` を使って文字列を表示しますが、プレースホルダーを使用してフォーマット文字列を表示することができます。プレースホルダーの表現には波括弧 `{}` を使用します。
この波括弧を複数使えば、複数の値を表示することができます。

```rust
println!("次のように予測しています: {}", guess);
```

## Day 5 のまとめ

数当てゲーム見ながら、Rust の言語仕様を見ながら勉強をすすめました。コードを書きながら言語仕様を見るのはたのしいですね。
今日参考にしていた数当てゲームは全部終わったのですけど、まだ知らない仕様のところを見切れてないので続きは明日にしようと思います。
