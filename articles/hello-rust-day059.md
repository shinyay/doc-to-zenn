---
title: "100日後にRustをちょっと知ってる人になる: [Day 59]Fermyon Spin VS Code Extension"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm,vscode]
published: true
---
## Day 59 のテーマ

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056) 〜 [Day 58](https://zenn.dev/shinyay/articles/hello-rust-day056) と **Fermyon** の **WebAssembly** 関連のソリューションについて見てみました。

- Spin
- Fermyon Platform
- Fermyon Cloud

今日もその流れで Fermyon 関連のソリューションについてまた見てみたいと思います。

Spin のアプリケーションを作って動かす際には必ず **Spin** コマンドを使用します。
この Spin の利便性をあげるために VS Code のエクステンションが提供されています。それを今日は導入して使ってみたいと思います。

## Spin VS Code Extention

**Spin VS Code Extention** は以下のリポジトリで公開されています。

- [Spin VS Code Extention リポジトリ](https://github.com/fermyon/spin-vscode)

このリポジトリの REDME にも書かれていますが、このエクステンションはまだ開発初期段階にあるようです。現時点で提供されている次のもののみのようです。

- Spinアプリケーションを構築するためのタスク(`spin:build`)
- Spinアプリケーションを実行するためのタスク(`spin:up`)

### Spin VS Code Extention のインストール

この Spin VS Code Extention は、Visual Studio Marketplace で入手できます。

![](https://storage.googleapis.com/zenn-user-upload/b13d3d34c455-20221029.png)

- [](https://marketplace.visualstudio.com/items?itemName=fermyon.spin-vscode&ssr=false#overview)

VS Code 上からも検索してインストールすることができます。

![](https://storage.googleapis.com/zenn-user-upload/df2ad4f646f5-20221029.png)

### VS Code からの Spin コマンド

次のようにコマンドパレットから、Spin コマンドが見えるようになります。

![](https://storage.googleapis.com/zenn-user-upload/cb407bf7d950-20221029.png)

Spin コマンドを予めインストールしていなくても、ここから導入ができそうです。

## Day 59 のまとめ

エクステンションの導入をしてみましたが、冒頭にまだ開発初期段階のものだとリポジトリの README にかかれていると説明しました。
正直、現時点では入れるメリットがほとんどありません。

あらかじめ Spin コマンドがターミナル上で使えるようにダウンロードしてパスを通している人がほとんどだと思います。そのような環境では、わざわざこのエクステンションを入れなくてもいいかな、と思いました。

今後の進化に期待したいですね。
