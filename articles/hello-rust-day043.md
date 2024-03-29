---
title: "100日後にRustをちょっと知ってる人になる: [Day 43]モジュールシステム"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 43 のテーマ

[Day 42](https://zenn.dev/shinyay/articles/hello-rust-day042) で Rust プログラムにメタデータを追加して性質や機能を追加する仕組みの**属性 (アトリビュート)** について見てみました。

この属性は Rust のモジュールシステムを通して様々な対象に付与することができました。
この Rust のモジュールシステムは、他の言語と比べても強力なものだと言われています。
というわけで、改めて Rust のモジュールシステムについて考えてみたいと思います。

## モジュールシステム

以前にも Rust のモジュールの仕組みについてまとめたことがありましたが、あらためて表でまとめます。

|モジュールシステムの要素|説明|
|--------------------|---|
|パッケージ|Cargo で管理する Rust プロジェクト|
|クレート|パッケージに含まれれる**実行バイナリ**および**ライブラリ**|
|モジュール|関数などの要素を含む論理的な階層|

### クレート

クレートは多分 Rust 特有の言葉なのかなと思います。僕の知っている限りでは他の言語で聞いた事がないので。
Crate という単語は木枠という意味の単語で、Rust では**ソースコードを格納するところ**のことをクレートと呼んでいます。
`cargo new` コマンドでパッケージを作成すると、デフォルトでクレートが 1 つ作成されています。

クレートには次の 2 種類があります。

- 実行バイナリクレート (`cargo new --bin (bin は省略可)`)
- ライブラリクレート (`cargo new --lib`)

#### 実行バイナリクレート

実行バイナリクレートは、**エントリポイント (main 関数)** を持つクレートです。
`cargo` コマンドで作成したパッケージ内につくられる `main.rs` が**クレート**になり、**モジュールの起点** になるので**クレートルート**とも呼びます。

```shell
modules/
├── Cargo.toml
└── src
    └── main.rs <--- クレートルート
```

#### ライブラリクレート

ライブラリクレートは、**エントリポイントを持たない**クレートです。

```shell
libraries/
├── Cargo.toml
└── src
    └── lib.rs <--- クレートルート
```

実行バイナリが存在しているところで、ライブラリクレートを作成し 2 つのクレートルートを持つパッケージを作成することも可能です。

### モジュール

モジュールとは、クレートの中の構成要素に対して名前空間を付与して論理的な階層構造をもたせることができるような仕組みです。

`mod` キーワードによってモジュールを定義します。また、モジュール本体は、`{}` (波括弧) で囲んだ部分になります。また、モジュール内部にモジュールを定義することも可能です。

```rust
mod Module1 {
    mod Module2 {
        fn doSomething()
    }

    mod Module3 {
        fn doSomethingElse()
        fn doNothing()
    }
}
```

また、この上記の定義だと同じモジュール内に対してのみ後悔されている状態になっています。
そのため、外部にもモジュールを公開するためには、`pub` キーワードを使用します。

```rust
pub mod Module1 {
    pub mod Module2 {
        pub fn doSomething()
    }

    pub mod Module3 {
        pub fn doSomethingElse()
        pub fn doNothing()
    }
}
```

### パス

この公開しているモジュールを使用するために、**パス** を考慮する必要があります。パスは、Java でいうところのパッケージに似ているようなものだと思えばいいと思います。

Rust のモジュールの場合、パスの起点となっているのがクレートルートになります。クレートルート名は `cargo new` で作成したパッケージ名か、あるいは `crate` とすることでルートを表しています。

先程のモジュールの例だと次のような階層になります。

```shell
crare
└── Module1
    ├── Module2
    │   └── doSomething
    └── Module3
        ├── doSomethingElse
        └── doNothing
```

Java のパッケージと異なるのは、パスの指定方法に次の 2 種類あるところです。

- 絶対パス
  - クレートルートから指定
- 相対パス
  - `self` (現在のモジュール) あるいは `super` (親のモジュール) を使い相対的に指定

パスの区切り文字には、`::` を使用します。

`doSomething` を指定する場合は次のようになります。

```rust
// 絶対パス指定
crate::Module1::Module2::doSomething
```

### モジュールの使い方

`use` キーワードを使用して、パスを指定することでモジュールを使うことができます。

```rust
use crate::Module1::Module2::doSomething;
```

また、`as` キーワードをつけることで別名を指定することが可能です。

```rust
use crate::Module1::Module2::doSomething as Something;
```

あるモジュール配下のモジュールを全て `use` キーワードで列挙するのは冗長になります。

```rust
// 冗長な書き方
use crate::Module1::Module2::doSomething
use crate::Module1::Module3::doSomethingElse
```

そこで、`{}` でまとめて記述することが可能です。

```rust
use crate::Module1::{Module2::doSomething, Module3::doSomethingElse}
```

## Day 43 のまとめ

モジュールシステムは Rust でプログラムを書いていく上での構造上の基本になるものです。
今更感がありますが、簡単に振り返ってみました。
