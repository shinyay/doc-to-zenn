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

## クレートを使用して機能追加

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

## Day 7 のまとめ
