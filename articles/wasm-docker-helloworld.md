---
title: "WebAssembly + Docker = Hello World"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [webassembly, wasm, rust, docker]
published: false
---
## テーマ: Rust と Docker Desktop で WASM な Hello World アプリ を作る

Zenn をご覧な方であれば、**WebAssembly** というキーワードを耳にしたり目にしたりしたことがある方は多いのではないでしょうか。昨年くらいから急に注目を集めはじめ、次世代のクラウドネイティブ技術とも言われ始めているテクノロジーです。

簡単に WebAssembly を説明すると次のように言えるでしょう。

:::message
WebAssembly (WASM) は、高速かつ効率的に設計されたスタックベースの仮想マシンのバイナリ命令形式です。低レベルのアセンブリのように使用することができ、ネイティブに近い速度でコードを実行する方法を提供します。さらにネイティブ環境だけでなく、ブラウザ上でも動作させることが可能です。Chrome、Firefox、Safari、Edgeなど、主要な Web ブラウザでサポートされています。
:::