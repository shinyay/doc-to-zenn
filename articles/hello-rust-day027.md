---
title: "100日後にRustをちょっと知ってる人になる: [Day 27]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 27 のテーマ

この数日間、Rust を使っての WebAssembly プロジェクトの作成やビルドについて調べてきました。ただ、WebAssembly バイナリを作るだけにしても、いろいろな作り方があることがわかりました。
場当たり的に確認をしていたので、ここで一度整理をしておこうと思います。

## WebAssembly プロジェクトの作成

Rust はコンパイラが標準で WebAssembly に対応しているので、敢えて特別なプロジェクト構成にしなくても WebAssembly バイナリのビルドを行うことは可能です。ですが、Rust のパッケージマネージャの **Cargo** を使うことで便利になったりなど、いろいろなプロジェクト作成の方法がありました。

- プレーンディレクトリ (`mkdir`)
- `cargo new`
- `cargo generate`
- `wasm-pack new`
- `npm init rust-webpack`

### プレーンディレクトリ (`mkdir`)

これは、適当なディレクトリを設けてそこで自由に構成して `rustc` コマンドで直接コンパイルするような場合のみな気がします。

[Day 20](https://zenn.dev/shinyay/articles/hello-rust-day020) で **WASI** のビルドを行ったときにも適当なディレクトリをプロジェクトを開発ディレクトリとして扱いました。

## Day 27 のまとめ
