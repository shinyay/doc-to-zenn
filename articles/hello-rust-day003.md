---
title: "100日後にRustをちょっと知ってる人になる: [Day 3]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---

## Day 3 のテーマ

コード開発といえば、統合開発環境 (IDE) やコードエディタを使わない人はほとんどいないと思います。ぼく自身、Java や Kotlin を書くときには **IntelliJ IDEA** を長らく愛用し続けています。編集対象の言語に対応したエディタを使うメリットは、その言語の補完をしてくれたり、テスト支援をしてくれたりなど、便利な機能を使うことができるので捗ります。
使わない手はないので、Day 3 では、Rust を開発できる編集環境を準備したいと思っています。

### Day 2 の振り返り: コードエディタ

Day 2 では、Rust 公式ドキュメントが紹介しているエディタ一覧を見てみました。

- [Tools](https://www.rust-lang.org/tools)

以下のエディタが掲載されていました。
|エディタ名|リンク|
|--------|-----|
|VS Code|<https://marketplace.visualstudio.com/items?itemName=matklad.rust-analyzer>|
|Sublime Text|<https://github.com/rust-lang/rust-enhanced>|
|Atom|<https://github.com/rust-lang/atom-ide-rust>|
|IntelliJ IDEA|<https://plugins.jetbrains.com/plugin/8182-rust>|
|Eclipse|<https://www.eclipse.org/downloads/packages/release/2019-09/r/eclipse-ide-rust-developers-includes-incubating-components>|
|Vim|<https://github.com/rust-lang/rust.vim>|
|Emacs|<https://github.com/rust-lang/rust-mode>|
|geany|<https://geany.org/about/filetypes/>|

全部試してみたいところですけど、手元の Mac にインストールしているエディタが２つ含まれていたので、それを使ってみたいと思います。

インストール済だったのはこちら:

- **Visual Studio Code**

- **IntelliJ IDEA**

## Visual Studio Code

Visual Studio Code の公式ドキュメントに Rust についての説明がありました。それを見ながら Visual Studio Code を設定してみようと思います。

### インストール

- [Rust in Visual Studio Code](https://code.visualstudio.com/docs/languages/rust)

拡張機能ビュー (⇧⌘X) を開いて、`Rust` で検索をして拡張機能を探します。
すると、Rust の公式から提供されている **Rust** という拡張機能が見つかると思います。

![](https://storage.googleapis.com/zenn-user-upload/943a574d2794-20220825.png)

説明を見てもらうと分かるようにこの拡張機能は廃止されていました。

> This extension is deprecated. Use the rust-analyzer extension instead.

代わりに **rust-analyzer** を使うようにガイドされていました。今日参照している VS Code の公式ドキュメントでは rust-analyzer のみの導入手順になっています。しかし、個人で紹介されている手順などを見てみると、 Rust 拡張機能の導入が紹介されているものも目にしました。rust-analyzer だけでよい、ということで先に進めようと思います。

![](https://storage.googleapis.com/zenn-user-upload/5173ed466165-20220825.png)

### 特長

拡張機能の紹介には以下のような機能が紹介されていました。

- コード補完
- 定義、実装、型定義への移動
- 全参照の検索、ワークスペースのシンボル検索、シンボルのリネーム
- 型とドキュメントがホバー表示
- 型とパラメータ名のヒント
- セマンティックシンタックスハイライト
- 豊富なアシスト機能（コードアクション）
- エラーからの提案の適用

### VS Code で Rust プロジェクトの表示

Day 2 で作成した `hello-rust` プロジェクトを VS Code で開いてみます。

拡張機能 適用後
![](https://storage.googleapis.com/zenn-user-upload/2909d489777a-20220825.png)

拡張機能 適用前
![](https://storage.googleapis.com/zenn-user-upload/b10ce609d440-20220825.png)

コードのカラーリングは微妙に変化してますね。

### VS Code で Rust の操作

拡張機能が提供している機能を少し試してみようと思います。

#### ビルドと実行

VS Code にターミナル(⌃⇧\`) を開きます。そのターミナル上で `cargo` を使用してビルドと実行を行います。

ビルド:

```shell
cargo build
```

実行:

```shell
cargo run
```

![](https://storage.googleapis.com/zenn-user-upload/3c50a78c3037-20220825.png)

#### ヒント表示

文字を入力するタイミングで予測してキーワードを表示してくれます。

![](https://storage.googleapis.com/zenn-user-upload/472b7cb84359-20220825.png)

#### ドキュメントのホバー表示

キーワードにマウスカーソルを合わせると説明が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/b290918fb75f-20220825.png)

#### コード補完

途中まで入力すると予測して補完をしてくれます。

![](https://storage.googleapis.com/zenn-user-upload/9679442d7c97-20220825.png)

#### セマンティクス シンタックス ハイライト

画像の例では、セマンティクスを判断して、**不変**と**可変**の変数の表示方法が変更されています。
可変変数に下線がひかれて表示されています。

![](https://storage.googleapis.com/zenn-user-upload/aa5a803afe82-20220825.png)

## IntelliJ IDEA

**IntelliJ Rust** というプラグインが JetBrains 公式になります。

- [IntelliJ Rust](https://www.jetbrains.com/rust/)

このプラグインを入れるだけで Rust 開発に対応した IntellJ になりそうです。

### インストール

## Day 3 のまとめ
