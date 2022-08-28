---
title: "100日後にRustをちょっと知ってる人になる: [Day 6]はじめての Rust プログラミング"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
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

## Day 5 のまとめ
