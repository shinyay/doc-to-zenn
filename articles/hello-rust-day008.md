---
title: "100日後にRustをちょっと知ってる人になる: [Day 8]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---

## Day 8 のテーマ

Day 6 と Day 7 で [Rust 公式サイトの数当てゲームサンプル](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html)を見ながら Rust の仕様についての学び方について感覚を掴んできました。このサンプルは公式ドキュメントに掲載されているものなので当然いろいろな人達が参考にしていますよね。
そこで、以下の動画で解説されていたものを改めて見てみることにします。

- [Looking at a simple Rust program](https://www.youtube.com/watch?v=84FuMPhoqfo)

## 数字当てゲーム

数字当てゲームは次のような内容でした。

- 1 から 100 までのランダムな整数を生成
- 入力値が小さいか大きいかを表示
- 一致したらメッセージを表示

そのため求められる機能としては以下のようなものが考えられました。

- 乱数生成
- 標準入力
- 数値比較
- パターンマッチング
- 繰り返し

これらの機能を Rust を使って実装することがこの数字当てゲームに求められていました。

### コードの完成形

以下が数字当てゲームの完成形のコードです。

```rust
use std::{io, cmp::Ordering};
use rand::Rng;

fn main() {
    println!("数を予想しましょう。");

    let secret_number = rand::thread_rng().gen_range(1..101);
    println!("生成した値: {}", secret_number);

    loop {
      
        println!("予想した値を入力してください。");
        
        let mut guess = String::new();
    
        io::stdin()
            .read_line(&mut guess)
            .expect("読み込みに失敗しました。");
        
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        
        println!("次のように予測しています: {}", guess);
    
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("小さい"),
            Ordering::Greater => println!("大きい"),
            Ordering::Equal => {
                println!("正解!");
                break;
            }
        }
    }
}
```



## Day 8 のまとめ
