---
title: "100日後にRustをちょっと知ってる人になる: [Day 44]構造体"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 44 のテーマ

[Day 43](https://zenn.dev/shinyay/articles/hello-rust-day043) では、Rust のモジュールシステムについて振り返ってみました。
モジュールの中でも**トレイト**と**構造体**は頻繁に使用するものになってくるのではないでしょうか。
ご存知の様に、Rust はオブジェクト指向の言語ではありません。しかし、このトレイトや構造体をうまく利用することでオブジェクト指向のような設計を行うことが可能になります。
厳密には異なりますが、トレイトと構造体は Java における インターフェースとクラスの関係のようなものと考えると分かりやすいかもしれません。

- **構造体** --> クラス
- **トレイト** --> インターフェース

このクラスのように扱うことも可能な Rust の構造体について見ていきたいと思います。

## 構造体

**構造体** そのものは、C/C++ 言語にもあるようにデータ型の要素を集めたものです。
個々の要素を **フィールド**と呼びます。

```rust
struct Employee {
    username: String,
    email: String,
    employee_no: u32,
}
```

構造体のインスタンスは、構造体の各フィールドを `キー:値` という形式で束縛して生成します。

```rust
let emp = Employee {
    username: String::from("yanashin18618"),
    email: String::from("yanashin@email.com"),
    employee_no = 1,
};
```

## Day 44 のまとめ
