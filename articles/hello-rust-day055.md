---
title: "100日後にRustをちょっと知ってる人になる: [Day 55]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 55 のテーマ

[Day 54](https://zenn.dev/shinyay/articles/hello-rust-day054) では Rust でのテストコードの実施の仕方を見てみました。しかし、同一モジュール内に実アプリケーションコードと、テストコードを混在させるという作り方を昨日はしていました。

どこにでも簡単にすぐにテストコードを作るというのは、メリットではあると思います。ただし、テストコードと実コードを分けて管理をしていくということを考えると、体系だてたソースコードの扱い、プロジェクトの扱いが必要になるのは明白かなと思いました。

そこで、今日はもう少しテストの仕方について見てみたいと思います。

## 同一モジュールなテスト

[Day 54](https://zenn.dev/shinyay/articles/hello-rust-day054) 同様に

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn sub(a: i32, b: i32) -> i32 {
    a - b
}

#[test]
fn should_added_number_when_two_numbers() {
    assert_eq!(9, add(3, 6))
}

#[test]
fn should_subtracted_number_when_two_numbers() {
    assert_eq!(3, sub(6, 3))
}
```


## Day 55 のまとめ
