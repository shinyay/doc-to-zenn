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
    role: String,
}
```

構造体のインスタンスは、構造体の各フィールドを `キー:値` という形式で束縛して生成します。

```rust
let emp = Employee {
    username: String::from("yanashin18618"),
    email: String::from("yanashin@email.com"),
    employee_no = 1,
    role: String::from("Engineer"),
};
```

また、Java のコンストラクタのように構造体を返す関数を定義することも可能です。

```rust
fn create_employee(username: &String, email: &String, employee_no: u32, role: &String) -> Employee {
    Employee {
        username = username.to_string(),
        email = email.to_string(),
        employee_no = employee_no,
        role = role.to_string(),
    }
}
```

関数の仮引数名とフィールド名が同じでも問題はありません。しかし、同じものを 2 回も記述するのは冗長です。Rust では、このような場合は省略ができるようになっています。

```rust
fn create_employee(username: &String, email: &String, employee_no: u32) -> Employee {
    Employee {
        username = username.to_string(),
        email = email.to_string(),
        employee_no, // フィールド名だけでよい
        role = role.to_string(),
    }
}
```

また、フィールドの省略に関しては他のインスタンスを参照するという省略方法もあります。

```rust
let emp1 = Employee {
    username: String::from("yanashin18618"),
    email: String::from("yanashin@email.com"),
    employee_no = 1,
    role: String::from("Engineer"),
};

let emp2 = Employee {
    username: String::from("shinyay"),
    email: String::from("shinyay@email.com"),
    employee_no = 2,
    ..emp1
};
```

`..` に続けてインスタンス名を記述します。emp2 の中で未定義な Employee フィールドを emp1 から参照してとりこむ記述方法です。

## タプル構造体

Java には標準では**タプル**という仕様がないので馴染みのない方もいるかもしれないですね。(Kotlin にはあります)

タプルというのは、順序付けられた複数の要素で構成されるデータの組み合わせのことです。複数の異なる型のデータやオブジェクトなどを格納できて、それぞれの要素には配列のように通し番号が採番されています。これによって要素を識別するようなデータ構造のことを**タプル**と呼びます。

Rust ではタプルは以下のようにデータ型を列挙して定義します。見てもらうとわかるように、フィールド名がありません。
そのため、扱う対象のモデルとしては、フィールド名に意味があまりないもの、またタプル名自体がフィールド名を連想させるものなどがいい気がします。

例えば、RGB カラーとか。以下の例では、IP アドレスを表しています。

```rust
struct Ipv4(u8, u8, u8, u8);
let address = Ipv4(128, 0, 0, 1);
println!("{}.{}.{}.{}", address.0, address.1, address.2, address.3)
```

## ユニット構造体

さて、Rust では `()` のことをユニットと呼んでいました。

- [Primitive Type unit](https://doc.rust-lang.org/std/primitive.unit.html)

このユニット構造体は、フィールドを何も持たない構造体のことです。もはや構造体なのか？という気もしますが、トレイトを実装させるようなときに使いそうです。

## Day 44 のまとめ
