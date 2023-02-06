---
title: "WebAssembly + Docker = Hello World"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [webassembly, wasm, rust, docker]
published: false
---
## テーマ: Rust と Docker Desktop で WASM な Hello World アプリ を作る

Zenn をご覧な方であれば、**WebAssembly** (WASM)  というキーワードを耳にしたり目にしたりしたことがある方は多いのではないでしょうか。昨年くらいから急に注目を集めはじめ、次世代のクラウドネイティブ技術とも言われ始めているテクノロジーです。

簡単に WebAssembly を説明すると次のように言えるでしょう。

:::message
WebAssemblyは、高速かつ効率的に設計されたスタックベースの仮想マシンのバイナリ命令形式です。低レベルのアセンブリのように使用することができ、ネイティブに近い速度でコードを実行する方法を提供し、ブラウザ上で動作させることが可能です。Chrome、Firefox、Safari、Edgeなど、主要な Web ブラウザでサポートされています。
:::

また、WebAssembly (WASM) はブラウザ以外の環境で実行することも可能です。そのために必要となる仕様が、**WebAssembly System Interface** (WASI) です。WASI は、ホストのファイルやネットワークなどの資源に安全にアクセスさせるための仕様です。

