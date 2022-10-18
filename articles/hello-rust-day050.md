---
title: "100日後にRustをちょっと知ってる人になる: [Day 50]Wasm Workers Server"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 50 のテーマ

折返し地点の Day 50 になりました。思い返せば、Rust を勉強し始めた理由は **WebAssembly** を知ってる人になろうと思いはじめ、だったら Rust を知っておいた方が良さそうだ、という軽い気持ちでした。

今日はその動機のきっかけになった WebAssembly についてあらためて見てみようと思います。
というのも、ちょうど VMware がオープンソースのプロジェクトで **Wasm Worker Server** というものを今日発表したのです。その触ってみた内容をすこしまとめようと思います。

### Wasm Worker Server

まず最初に、この **Wasm Worker Server** が何かを説明します。
一言で言い表すならば、サーバーレスの仕組みを提供するプロジェクトです。ただし、サーバーレスとして動作させる対象のワークロードは、**ワーカー (Worker)** と呼ばれる軽量な構成で組み上げられたものになります。

そして、この**Wasm Worker Server**自体は自己完結型のバイナリとして実装されています。
これが単独で、ワーカーをホストしている WebAssembly ランタイムに対して HTTP リクエストをルーティングをします。

- [GitHub Repository](https://github.com/vmware-labs/wasm-workers-server)

## Day 50 のまとめ
