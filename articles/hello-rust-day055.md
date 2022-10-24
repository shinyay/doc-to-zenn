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

[Day 54](https://zenn.dev/shinyay/articles/hello-rust-day054) 同様に同一のモジュール内に実際のアプリケーションコードとテストコードを記載すると次のようになります。

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

テストコードと実アプリケーションのコードを同一のモジュールに書く場合、`#[test]` 属性がついている関数がテストコード対象の関数であるということは分かるものの、順序や場所に規制なくテストコードを配置できてしまうことは可読性を落としてしまうことがあります。

そこで、Rust では、テストコードをひとまとめにしたテストモジュールを定義することが可能です。

### テストモジュール #[cfg(test)]

次の注釈が入っているモジュールがテスト専用モジュールになります。

- **#[cfg(test)]**

この `cfg` は[条件付きコンパイル](https://doc.rust-lang.org/reference/conditional-compilation.html#conditional-compilation) で使用する属性です。

- [The cfg attribute](https://doc.rust-lang.org/reference/conditional-compilation.html#the-cfg-attribute)
- [cfg](https://doc.rust-lang.org/rust-by-example/attribute/cfg.html)

ここでの条件付きコンパイルは、`cargo build` を実行したときではなく、`cargo test` を実行した時だけにテストコードをコンパイルして実行するようにするものです。
このように、モジュールを分離しておくことにより通常のビルド時はテストコードが含まれないのでコンパイルに要する時間や、コンパイル後の成果物のサイズも節約する事が可能です。

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn sub(a: i32, b: i32) -> i32 {
    a - b
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn should_added_number_when_two_numbers() {
        assert_eq!(9, add(3, 6))
    }

    #[test]
    fn should_subtracted_number_when_two_numbers() {
        assert_eq!(3, sub(6, 3))
    }
}
```


<!-- テストファーストような考え方でコーディングを行う場合、テストコードと実アプリケーションコードは別のソースファイルとして分けられている方が効率的です。つまりテスト用のモジュールを作ることができればよいということになります。 -->

## Day 55 のまとめ
