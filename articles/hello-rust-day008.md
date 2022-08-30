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

### Looking at a simple Rust program を見ながら振り返り

一度自分でコードを書いて仕様も見てと学習をしたものなので、[Looking at a simple Rust program](https://www.youtube.com/watch?v=84FuMPhoqfo)の解説を聞くと復習になって理解が深まりました。

ビデオの流れに沿ってコードを振り返ってみます。

#### パッケージリスト

冒頭に `use` キーワードを使用して、このプログラム中で使用するパッケージやクレートのリストを宣言しています。

```rust
use std::{io, cmp::Ordering};
use rand::Rng;
```

これは Java の `import` 文と同じようなものと考えると分かりやすいですね。
上記の定義だと以下のモジュールや Enum を使用していることを表しています。

- [std::io](https://doc.rust-lang.org/std/io/index.html)
- [std::cmp::Ordering](https://doc.rust-lang.org/std/cmp/enum.Ordering.html)
- [rand::Rng](https://docs.rs/rand/0.8.5/rand/trait.Rng.html)

##### パッケージとクレート

**クレート**は Rust コンパイラが一度に考慮する最小量のコードです。
**パッケージ**は一連の機能を提供する 1 つ以上のクレートのバンドルです。

###### 参考リンク

- [Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)

#### アプリケーションのエントリポイント

`main.rs` というコードの中に、以下の関数が定義されています。

```rust
fn main()
```

この関数が、この Rust プログラムのエントリポイントです。
Java の `public static void main (String[] args)` と同じように最初に呼ばれる場所になっています。

#### マクロ

println! は **マクロ**と呼ばれる仕組みです。このマクロとは、Cのプリプロセッサマクロなどとおなじく、ビルド時にソースコードの一部を置き換える仕組みです。

##### 参考リンク

- [macros](https://doc.rust-lang.org/book/ch19-06-macros.html)

#### 不変変数と可変変数

Rust で定義する変数はデフォルトで不変として定義されています。つまり変数に値をバインドすると、その値は変更できなくなります。

##### 参考

- [Variables and Mutability](https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html)

#### 列挙型 Result / Orderring

入力値（文字列）を数値に変換する際に `parse()` 関数を使用しています。

```rust
pub fn parse<F>(&self) -> Result<F, F::Err>
```

この戻り値のタイプである `Rusult` が列挙型になっています。そして含まれている値が `Ok` と `Err` です。

- [Enum std::result::Result](https://doc.rust-lang.org/std/result/enum.Result.html)

```rust
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

また、入力値と生成した値の比較をするときには `cmp()` 関数を使用しています。

```rust
fn cmp(&self, other: &u32) -> Ordering
```

この戻り値のタイプになっている `Ordering` が列挙型になっています。そして含まれる値が、`Less`, `Equal`, `Greater` です。

```rust
pub enum Ordering {
    Less,
    Equal,
    Greater,
}
```

#### match 制御フロー演算子

`Result` や `Ordering` のように列挙型で戻ってくる値を `match` 演算子を使用して判定を行っています。Java の case 文のような使い方です。

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
```

```rust
match guess.cmp(&secret_number) {
    Ordering::Less => println!("小さい"),
    Ordering::Greater => println!("大きい"),
    Ordering::Equal => {
        println!("正解!");
        break;
    }
}
```

## Day 8 のまとめ

今日は Day 7 までにコーディングと言語仕様の確認をしていた数当てゲーム内容を、別の方が説明されているのを見て復習を行いました。
一度自分で確認をした言語仕様について別の方の説明を聞くと理解が深まると感じました。
同じ内容のことも別の説明を聞いたり、情報を読んだりしながら理解を深めたいと思います。