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

```shell
   Compiling day_54_unit-test v0.1.0
    Finished test [unoptimized + debuginfo] target(s) in 0.43s
     Running unittests src/main.rs

running 1 test
test ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

特に問題が発生せず正常終了する場合は、上記のように `test ... ok` と表示されます。
テストが失敗する場合は、以下のように表示されます。

```shell
running 1 test
test test_message ... FAILED

failures:

---- test_message stdout ----
Hello
thread 'test_message' panicked at 'assertion failed: `(left == right)`
  left: `"Hello!"`,
 right: `"Hello"`', src/main.rs:12:5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    test_message

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

どこで失敗したか、なぜ失敗したかを表示してくれます。

また、特定のテストコードだけを実施したい場合は、テスト関数名を指定して実行できます。

```shell
cargo test test_message
```

## Day 54 のまとめ
