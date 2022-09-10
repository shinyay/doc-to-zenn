---
title: "100日後にRustをちょっと知ってる人になる: [Day 19]WASI"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 19 のテーマ

Day 18 では **WebAssembly (Wasm)** がどういうものなのかを、仕様や特徴について少し確認してみました。

簡単に Wasm が何かというと、**ブラウザなどの環境でアプリケーションを高速かつ安全に実行するための仕組み**というようなものでした。

- [WebAssembly (Wasm)](https://webassembly.org/)
- [W3C WebAssembly Working Group](https://github.com/w3c/wasm-wg/)
  - [WebAssembly Specification Release 2.0 (Draft 2022-09-01)](https://webassembly.github.io/spec/core/index.html)
  - [WebAssembly Specification Release 2.0 (Draft 2022-09-01) PDF](https://github.com/shinyay/doc-to-zenn/files/9539360/WebAssembly-Draft-2022-09-01.pdf)

そして、ブラウザ以外の環境でファイルやネットワーク、メモリなどのシステムリソースなどに安全にアクセスするための **API 標準仕様**として、**WebAssembly System Interface (WASI)** の策定が現在進行系で進んでいる、ということが分かりました。

- [WebAssembly System Interface (WASI)](https://wasi.dev/)

今日は、**WASI** を中心にして **WebAssembly** をもう少し深く見ていこうと思います。

![](https://storage.googleapis.com/zenn-user-upload/054d57c458d9-20220910.png)

## WebAssembly System Interface (WASI)

GitHub にある WASI のリポジトリを見てみます。

- [GitHub - WASI](https://github.com/WebAssembly/WASI)

🙆🏻‍♂️ 標準化されたAPIのモジュール化されたコレクションである
🙅‍♀️ モノリシックな標準システムインターフェースではない

## Day 19 のまとめ
