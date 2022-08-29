---
title: "100日後にRustをちょっと知ってる人になる: [Day 7]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---

## Day 7 のテーマ

昨日の続きで、「数当てゲーム」を作りながら、Rust の言語仕様を見ていきます。

## 数当てゲームの実装

以下の内容を追加で実装していきます。

- 1 から 100 までのランダムな整数を生成
- 入力値が小さいか大きいかを表示
- 一致したらメッセージを表示

### クレートを使用して機能追加

Rust の**クレート**とはコンパイルの単位でコードの集まりです。`cargo new` を実行してパッケージを作成すると実行バイナリのクレートが１つ作成されることになります。
ライブラリ用のプロジェクトで生成したライブラリクレートには、別のプログラムで使用するコードが含まれており連携して使用します。単独では実行できません。
乱数を発生させるために、`Cargo.toml` に `rand` クレートを追加します。

```toml
[dependencies]
rand = "0.8.5"
```

このプロジェクトを `cargo build` します。すると、必要な依存関係を **https://crates.io/**から取得しコンパイルが行われます。

```shell
$ cargo build
    Blocking waiting for file lock on package cache
    Updating crates.io index
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
   Compiling libc v0.2.132
   Compiling cfg-if v1.0.0
   Compiling ppv-lite86 v0.2.16
   Compiling getrandom v0.2.7
   Compiling rand_core v0.6.3
   Compiling rand_chacha v0.3.1
   Compiling rand v0.8.5
   Compiling day_6_guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 2m 59s
```

`rand` クレートの提供する `thread_rng` 関数を使用して乱数を生成します。

- [thread_rng](https://rust-random.github.io/rand/rand/fn.thread_rng.html)
- [gen_range](https://rust-random.github.io/rand/rand/trait.Rng.html#method.gen_range)

```rust
let secret_number = rand::thread_rng().gen_range(1..101);
```

この `gen_range` メソッドが使用している範囲表現は、`開始..終了` という形式です。この表現での値は、下限値は含みますが上限値は含みません。そのため、上限を100とするために `101` と指定しています。

#### クレートとパッケージ

Rust のモジュールシステムをここで調べてみました。

|要素|概要|
|---|---|
|パッケージ|Cargoパッケージマネージャで管理されるクレートの集合|
|クレート|パッケージ内の個々の実行バイナリとライブラリ|
|モジュール|関数などの要素の論理的な階層|
|パス|関数などの要素やモジュールの論理的な場所を示す名前|

![](https://storage.googleapis.com/zenn-user-upload/02e25cdb49d1-20220829.png)

### 数値の比較

`match` 式と `Ordering` 列挙子を使って比較を行います。

- [match制御フロー](https://doc.rust-lang.org/book/ch06-02-match.html)
- [Ordering列挙子](https://doc.rust-lang.org/std/cmp/enum.Ordering.html)

`Ordering` も `enum` の1つで `Less`, `Greater`, `Equal` の3つの列挙子を持っています。
そして、`cmp` メソッドが比較した2つの値から `Ordering` 列挙型の列挙子を返します。
`match式`は、Java で言うところの Case分のようなものですね。パターンを照合して合致したら、そのときの結果を返すというものです。

### 型の変換

Rust は強い静的型システムを持ち、型推論も行う言語です。
そのため、比較しようとしている以下の部分で文字列と数値の比較ができずエラーにこのままだとなってしまいます。

```rust
match guess.cmp(&secret_number)
```

`guess` が文字列、`secret_number` が数値型です。
そこで、`guess` を数値型に変換を行う処理を追加します。

```rust
let guess: u32 = guess.trim().parse().expect("数値を入力してください");
```

ここでは、`String` が持つ `parse` メソッドを使用して数値変換を行っています。

- [parse](https://doc.rust-lang.org/std/primitive.str.html#method.parse)

#### 変数のシャドーイング

Rust では既に宣言済みの変数と同じ名前の変数を新しく宣言することができます。
ここでは、`guess` が繰り返し宣言されました。これを **シャドーイング** と呼びます。
このとき、新しく宣言された同一名の変数は、前の変数を覆い隠すような動作になります。

例：
```rust
fn main() {
    let x = 1;
    let x = x + 2;
    let x = x * 3;
    println!("The value of x is: {}", x);
}
```

このようなケースの場合、答えは `9` が表示されます。
覆い隠すということが分かれば、どのように `x`  に値が格納されていったか想像できますよね。

## Day 7 のまとめ

