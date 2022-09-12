---
title: "100日後にRustをちょっと知ってる人になる: [Day 20]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 20 のテーマ

Day 18, 19 と Rust のユースケースとしても注目を浴びている **WebAssembly (WASM)** と **WebAssembly System Interface (WASI)** について調べてみました。
まだ仕様を策定中であったりという現在進行系で進化している技術ですが、次世代の **Write once, Run anywhere** と言えるような技術に今後発展していきそうな期待を持つことができました。

ということで、Rust を使って WebAssembly の開発できるように、開発/実行環境をつくり、実際に WebAssebmly として動かしてみたいと思います。

## WASI ランタイム環境の準備

**WASI** 自体はインターフェース仕様なので、実際に動作させるためには WASI を実装したランタイムが必要になることは、[Day 19](https://zenn.dev/shinyay/articles/hello-rust-day019#wasi-%E3%81%AE%E5%AE%9F%E8%A3%85) の中でも書きました。そこで、ここでは ランタイムをいれてみようと思います。

### 代表的な WASI ランタイム

以下が代表的な WASI ランタイムです。

- [Wasmtime](https://docs.wasmtime.dev/)
  - [Wasmtime - Repo](https://github.com/bytecodealliance/wasmtime)
- [Wasmer](https://wasmer.io/)
  - [Wasmer - Repo](https://github.com/wasmerio/wasmer)
- [Wasm3](https://wapm.io/vshymanskyy/wasm3)
  - [Wasm3 - Repo](https://github.com/wasm3/wasm3)
- [WasmEdge](https://wasmedge.org/)
  - [WasmEdge](https://github.com/WasmEdge/WasmEdge)

この中でも **Wasmtime** がリファレンス実装と言われているようなので、それをインストールしようと思います。

### Wasmtime のインストール


## Day 20 のまとめ

