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

## Day 20 のまとめ

