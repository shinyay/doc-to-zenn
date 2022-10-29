---
title: "100日後にRustをちょっと知ってる人になる: [Day 59]Fermyon Spin VS Code Extension"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm,vscode]
published: false
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

このリポジトリの REDME にも書かれていますが、このエクステンションはまだ開発初期段階にあるようです。現時点で提供されている次のもののみです。

- Spinアプリケーションを構築するためのタスク(`spin:build`)
- Spinアプリケーションを実行するためのタスク(`spin:up`)

### Spin VS Code Extention のインストール

この Spin VS Code Extention は、Visual Studio Marketplace で入手できます。

- [](https://marketplace.visualstudio.com/items?itemName=fermyon.spin-vscode&ssr=false#overview)

## Day 59 のまとめ
