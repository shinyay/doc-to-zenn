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

## ハロー・ワールド基本

生成されたプロジェクトテンプレートを見ていきます。

### プロジェクト構造

プロジェクト名のディレクトリ配下に `src` が位置して開発対象コードが生成されていました。
`cargo` コマンドラインから実施した構成と同じですね。

![](https://storage.googleapis.com/zenn-user-upload/0de68971f300-20220826.png)

### 生成コード

生成されたコードを見ていきます。

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

IntelliJ のコンソールに実行結果がひょうじされます。

![](https://storage.googleapis.com/zenn-user-upload/a5b99ef9b693-20220826.png)

#### main.rs



## ハロー・ワールドちょっと応用

## Day 4 のまとめ
