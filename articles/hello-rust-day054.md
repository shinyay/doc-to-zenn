---
title: "100日後にRustをちょっと知ってる人になる: [Day 54]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 54 のテーマ

今までいろいろなサンプルを作って動かしてみたりしてきました。ただ、その動作確認は実際に動かしてみたり、動作を目で確認してみたりというものでした。通常、コードを書いて動作確認をする場合はテストコードを書いて単体テストなどを行ったりしますよね。Rust も単体テストを実行する仕組みがああります。

今日はすこしその単体テストの仕方を見てみたいと思います。

## テストの書き方

テストの書き方はとてもシンプルです。
関数の `fn` キーワードの前に `#[test]` を付けるだけです。

テスト対象の関数:

```rust
fn print_message(msg: String) -> String {
    println!("{}", msg);
    msg
}
```

テスト関数:

```rust
#[test]
fn test_message() {
    assert_eq!("Hello", print_message("Hello".to_string()));
}
```

## テストの実行

`cargo test` コマンドでテストを実行します。

```shell
cargo test
```

## Day 54 のまとめ
