---
title: "100日後にRustをちょっと知ってる人になる: [Day 55]体系化したテスト"
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

## 異なるモジュールとしてのテスト

さて、テストの実施に関してモジュールとして分離して管理する方法はわかりました。一方でソースファイル単位でテストコードを分離してしまいたいケースもあると思います。

例えば、先程までの同一モジュール内のテストが、同一モジュール向けのみのライブラリ内テスト（単体テスト）だとすると、ライブラリを跨っての結合テストのような場合です。
この場合は、一度に複数のライブラリの公開インターフェースに対するテストを目的とするため特定のモジュール内に含んで管理して、責任範囲がどこにあるかが不明瞭になるよりも独立させてしまった方が分かりやすいです。

そのような場合は、テストディレクイトリを作成し、そこにテストコードをいれることでテスト用のコードだと認識されます。

```shell
project
 ├─ .git
 ├─ src
 │   └─ main.rs
 ├─ target
 └─ tests <----------------ここがテストディレクトリ
      └─ test.rs
```

使用対象のクレートを指定してテストコードを実装していきます。

```rust
use day_55_test;
#[test]
fn integration_test() {
    assert_eq!(3,day_55_test::sub(day_55_test::add(3, 6), day_55_test::add(2, 4)));
}
```

## テスト用のマクロ

テストに実施するマクロは以下のようなものが提供されています。

|マクロ|説明|
|-----|----|
|assert!(x);      |x が ture ならば正常、異なればパニック|
|assert_eq!(x, y);|x == y ならば正常、異なればパニック|
|assert_ne!(x, y);|x != y ならば正常、異なればパニック|

### マクロ実装例

テスト対象の関数

```rust
fn add(x: u32, y: u32) -> u32 {
    x + y
}
```

テストコード例

```rust
#[test]
fn test_add() {
    assert!(add(1, 2) ==  3);       // 正常（ 1 + 2 == 3 -> true ）
    assert_eq!(add(1, 2), 3);       // 正常（ 1 + 2 == 3 ）
    assert_ne!(add(1, 2), 4);       // 正常（ 1 + 2 != 4 ）
    assert_eq!(add(1, 2), 1);       // エラー（ 1 + 2 == 1 ）
}
```

## Day 55 のまとめ

テストコードの置き場所や実装方法について、[Day 54](https://zenn.dev/shinyay/articles/hello-rust-day054) に引き続いて見てみました。

- テスト用モジュール `#[cfg(test)]`
- 結合テスト用ディレクトリ `tests`

このようなテストの体系化は個人開発からチーム開発に広がるときにはより重要になってくるコンセントだと思います。テストのすすめ方については、さらに慣れていく必要があるなと思います。
