---
title: "100日後にRustをちょっと知ってる人になる: [Day 4]Hello Rust, Hello World"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---

## Day 4 のテーマ

Day 3 な昨日、VS Code と IntelliJ IDEA に Rust プラグインをインストールして、Rust がすぐに開発できるような環境を準備するところまで終わりました。
そしたら、その次に実施するのは全世界の共通手順、**[ハロー・ワールド](https://hello-world-movie.com/)** ですよね。
(リンクは冗談です)
というわけで、今日の Day 4 は ハロー・ワールドを作成するという達成レベル低めに設定した目標をさくっとこなしてみたいと思います。

## プロジェクト作成

IntelliJ IDEA　を使ってプロジェクト作成を行っていきます。

先日 `cargo` を使ってプロジェクトを作成するときには以下のコマンドを実行しました。

```shell
cargo new <PROJECT_NAME>
```

IntelliJ でプロジェクトを新規プロジェクトを作成しようとすると以下の画面が表示されます

![](https://storage.googleapis.com/zenn-user-upload/450b01967ccf-20220826.png)

ここで気になるのは、プロジェクトテンプレートの種類に **バイナリ** と **ライブラリ** があることです。あまり気にしていなかったので、ちょっと調べてみます。

### Cargo による新規プロジェクトの作成

Cargo の公式ドキュメントを参照してみます。

- [Creating a New Package](https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html)

以下のような内容と理解しました。

- **バイナリプロジェクト**
  - 実行可能なプログラムにコンパイルできるバイナリプロジェクトで、直接実行することができるような成果物を開発します。
  - `cargo` 実行時オプション: `--bin`
- **ライブラリプロジェクト**
  - ライブラリプロジェクトは、通常、コアロジックと関数を含んでおり、一緒にある種のライブラリを構成しています。
  - これらは、他の実行可能なプログラムや内部使用のためのライブラリで使用されます。
  - `cargo` 実行時オプション: `--lib`
- デフォルトでは `--bin` バイナリプロジェクトが選択されます。

というわけで、バイナリプロジェクトを選択してすすめるとプロジェクトテンプレートが生成されます。

![](https://storage.googleapis.com/zenn-user-upload/3da9d6f83d39-20220826.png)

## ハロー・ワールド 基本

生成されたプロジェクトテンプレートを見ていきます。

### プロジェクト構造

プロジェクト名のディレクトリ配下に `src` が位置して開発対象コードが生成されていました。
`cargo` コマンドラインから実施した構成と同じですね。

![](https://storage.googleapis.com/zenn-user-upload/0de68971f300-20220826.png)

### 生成コード

生成されたコードを見ていきます。

#### main.rs

エントリーポイントになる `main.rs` が以下のコードを含んで生成されています。

```rust
fn main() {
    println!("Hello, world!");
}
```

### 実行

**Cargo** メニューを選択します。

![](https://storage.googleapis.com/zenn-user-upload/6ace46a6b13b-20220826.png)

そして、`cargo run` をダブルクリックします。

![](https://storage.googleapis.com/zenn-user-upload/b401ce32f59e-20220826.png)

IntelliJ のコンソールに実行結果が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/a5b99ef9b693-20220826.png)

## ハロー・ワールド ほんの少しだけ応用

応用とまでは全く言わないと思いますが、ほんの少しだけ自動生成されたコードを編集しようと思います。明日以降 Rust の言語仕様を学んでいこうと思いますけど、プログラム言語で大事なのは「構文」「関数」「変数」などかなと思っています。どんな言語であったとしても、最低限まずその３点を抑えれば何か書けますよね。

そこで、Rust の学習をすすめていく上でまず参考にするのはここなんでしょうね。

- [Rust Getting started](https://www.rust-lang.org/learn/get-started)

![](https://storage.googleapis.com/zenn-user-upload/3ec016637afa-20220826.png)

ここを見つつ学ぼうと思います。

### 変数と関数

応用といいつつも基本なことを確認していきます、

#### 変数

まず Rust での変数定義についての確認をします。

- [Variables and Mutability](https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html)

Rust では変数が標準で不変なんですね。Kotlin だと `val` と `var` で区別してましたけど、原則 `val` 扱いというのは僕好みな仕様です。
そして、不変な読み取り専用の変数を可変にするには、`mut` キーワードをつければよいということですね。

#### 関数

次に関数について確認をします。

- [Functions](https://doc.rust-lang.org/book/ch03-03-how-functions-work.html)

Rust での関数の宣言方法は、全文字を小文字にし、単語区切りにアンダースコアを使う **スネークケース**なんですね。
そして、定義するキーワードは `fn` ということで覚えました。

#### 実践

以下のようにしてみました。

- **mut** キーワードを使った可変変数の定義
- 可変変数への値の代入
- ユーザー定義関数の呼び出しと引数

```rust
fn main() {
    let mut greeting = "Hello, world!";
    println!("{}", greeting);

    greeting = "Hello, Rust!";

    hello(greeting);
}

fn hello(x: &str) {
    println!("The value of x is: {}", x)
}
```

これを実行すると問題なく動きました。

![](https://storage.googleapis.com/zenn-user-upload/4be61e55fdd8-20220826.png)

## Day 4 のまとめ

今日は、ハロー・ワールドを作成・実施するというものでした。言語仕様などまだろくに知らなくても作成できるような内容ですよね。
明日からは Rust の世界にちょっとずつ Deep Dive していきたいなと思います。
