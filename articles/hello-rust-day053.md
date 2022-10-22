---
title: "100日後にRustをちょっと知ってる人になる: [Day 53]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 53 のテーマ

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) 〜 [Day 52](https://zenn.dev/shinyay/articles/hello-rust-day052) と **[Wasm Workers Server](https://github.com/vmware-labs/wasm-workers-server)** について見てみました。

WebAssembly を用いたサーバーレスなアプリケーションを動作させる HTTP サーバーの導入、そしてサーバーレスなアプリケーションな **ハンドラ** の作成を行い、実際に動かしてみました。

さて、この **Wasm Workers Server** の目指しているコンセプトは、**互換性**と**シンプルさ**でした。そのため、作成するワーカーは互換性ある標準準拠したものになります。

Rust によるハンドラを作成する場合、**[wasm-workers-server-kit](https://github.com/vmware-labs/wasm-workers-server/tree/main/examples#rust-handlers)** クレートを使用する必要があります。今回は、この**wasm-workers-server-kit** について見てみようと思います。

ところで、

## Day 53 のまとめ
