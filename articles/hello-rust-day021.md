---
title: "100日後にRustをちょっと知ってる人になる: [Day 21]Cargo による Wasm ビルド"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 21 のテーマ

昨日は `rustup` で **wasm32-wasi** ターゲットを追加して、WASI の実装ランタイムな **Wasmtime** をインストールして、`rustc` でWasm バイナリをコンパイルしてみました。

これらの Rust に関するツールチェーンで昨日やり残していたことをやってみようと思います。Rust のツールチェーンといえば、以下のコマンドがトピックに出てきますよね。

- `rustup`: Rust のツールチェーンマネージャ
  - [The rustup book](https://rust-lang.github.io/rustup/index.html)
- `rustc`: Rust コンパイラコマンド
- `cargo`: Rust のパッケージマネージャ 兼 ビルドツール

あと、ツールチェーンと言った時に含まれるのは、次のものです:

- **Rust の標準ライブラリ (std)**
- **Rust の API ドキュメント**

さて、この標準のツールチェーンで提供されるビルドツールの **cargo** を使った Wasm の扱いについて確認していませんでした。今日は、その確認をしておきたいと思います。

## Day 21 のまとめ
