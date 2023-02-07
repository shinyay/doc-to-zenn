---
title: "WebAssembly のこれから"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [webassembly, wasm, wasi]
published: false
---
## TL;DR

**Bytecode Alliance** が毎月配信しているコミュニティミーティングを見て内容のサマリーや関係することについてまとめています。
参照したコミュニティミーティングは、2 月 1 日に配信されたものです。

https://www.youtube.com/watch?v=9pLa7PUhPYA

2023 年に Bytecode Alliance が見据えている次のような WebAssembly の仕様動向について語られています。

- ✅ WASI Preview 2 
- ✅ コンポーネント レジストリ

## Bytecode Alliance Foundation

![](https://storage.googleapis.com/zenn-user-upload/8fff11292fbd-20230207.png)

**Bytecode Alliance Foundation** は、WebAssembly の仕様の標準化を推進する団体です。
**WebAssembly (Wasm)** や **WebAssembly System Interface (WASI)**など、W3C 標準に基づくソフトウェア基盤の実装に取り​​組んでいる非営利団体です。

- [Bytecode Alliance](https://bytecodealliance.org/)

この Bytecode Alliance には **Technical Steering Committee** があります。

- [Bytecode Alliance Technical Steering Committee Charter](https://github.com/bytecodealliance/governance/blob/main/TSC/charter.md)

この Technical Steering Committee に新しく任命された Bailey Hayes がコミュニティミーティングをリードしていました。

## 開発言語を統合していくことは可能か？

> 必要なプログラミング言語のライブラリを使用して、それらを一緒にコンパイルする方法があればどうでしょうか? そして、開発者がそれを遠い将来ではなく、年末までに行うことができたらどうでしょうか?

Bailey によると、まさにこの問いかけこそが Bytecode Alliance が今年解決していこうとしている問題なのです。

## WebAssembly System Interface (WASI)

![](https://storage.googleapis.com/zenn-user-upload/1adeab504a15-20230207.png)

もともと、**WASI** は「ポータブル オペレーティング システム インターフェイス」を指す「POSIX -like」と呼ばれていました。
これは、ウィキペディアで「オペレーティング システム間の互換性を維持するために IEEE Computer Society によって指定された標準のファミリー」として定義されています。

しかし、Bailey は次のようにコメントしています。

> これは POSIX を意図したものではありません。
私たちが本当に意図していたのは、あなたが期待する共通の API セットがあり、開発者は、あなたがターゲットにしているランタイムのように扱うことができ、それによってあなたはブラウザの外で本当にうまく実行できるようになる、ということです。
ほぼすべてのアプリケーションが依存する、あるいは期待するものがあります。それがなければ、WebAssembly モジュールに許されることは非常に限られてしまいます。

WASI とは、APIのセットです。つまり、ファイルシステムへのアクセスや標準I/Oなど、開発者が `libc` から得られる機能を開発者に提供するものです。この API のセットをターゲットにすれば、ブラウザの外でも、どんな JavaScript ランタイムの外でも実行できるようにするものです。

### WASI Preview 1

現在さまざまな実装で使用されている WASI は、**WASI Preview 1** です。

- [WASI](https://wasi.dev/)

次のような WASI 実装のランタイムがあります。

- [Wasmtime](https://wasmtime.dev/)
- [Wasmer](https://wasmer.io/)
- [WebAssembly Micro Runtime (WAMR) ](https://bytecodealliance.github.io/wamr.dev/)

### WASI Preview 2

現在 ByteCode Alliance が取り組んでいるのが、**WASI Preview 2** で、2023 年中にリリース予定になっています。

この WASI Preview 2 では WebAssembly アプリケーションを構築するための新しいモデルが検討されています。それが、コンポーネントモデルです。

- [Component Model design and specification](https://github.com/webassembly/component-model)

  - コンポーネントモデルを使用すると、開発者は C++ でライブラリを作成し、Rust でライブラリを作成し、 Python でライブラリを作成し、または JavaScript を含むその他の言語でライブラリを作成し、それらをレゴブロックのように組み合わせてアプリケーションを作成できるようになります。

  - そして、WebAssemblyモジュールという点では、厳密な型を持ち、その型をコンポーネントである他のWebAssemblyモジュールに公開することができるようになります。

このコンポーネントモデルについて、Bailey は次のようにコメントをしています。

:::message
これは、今日のソフトウェアの書き方を完全に変えることを意味します。20年間存在したサイロがすべてなくなるということです。
:::

## コンポーネント レジストリ

Bytecode Alliance では、**コンポーネント レジストリ**の構築に取り組んでいます。
コンポーネント レジストリの目標は、コンポーネントの種類を知るなど、他のレジストリがコンポーネントの言語を話すことができるようにプロトコルを設計することです。

たとえば、`npm` をエコシステムとする JavaScript を例にとってみます。

そのレジストリに、`npm install` を実行した場合、コンポーネントを扱っているという新しいフラグがあり、**WARG プロトコル（WebAssembly registry protocol）** と呼ぶものを使っているコンポーネントを引っ張ってきます。
そうすれことにより、理論的にはどの言語で書かれたコンポーネントでもインストールできるようになり、他の言語を学ぶ必要がなくなります。開発者は、ライブラリのどの部分が必要で、どの関数を呼び出せばいいのか、ということだけを知っていればいいのです。

## いま WebAssembly から始められること

WASI Preview 2 の詳細については、まだまだ調整中です。
しかし、WebAssembly で標準化されているものの中には、開発者が試せるものがたくさんあります。

JavaScriptを知っていてC++を少し学びたい人や、C++を知っていてWebでアプリを動作させるためにJavaScriptでほんの少し何かをする方法を学びたい人に Emscriptenツールチェーン は良い出発地点です。

![](https://storage.googleapis.com/zenn-user-upload/d12a561c5235-20230207.png)

- [Emscripten](https://emscripten.org/index.html)

Rust であれば、WebAssembly 開発との相性の良さがわかると思います。
`cargo` を使ってビルドを行うと、wasm32バイナリをターゲットとし、WasmtimeなどのWasmランタイムで実行することができます。

そして、Wasmtimeによって、デスクトップやエッジ、サーバーレス機能など、さまざまな場所にWasmモジュールを置くことが可能になります。

## Key Takeaways

2023 年は、Bytecode Alliance により昨年以上に WebAssembly の標準化に向けた動きが加速すると思われます。
特に、WASI を用いたブラウザ以外での WebAssembly の活用については期待をもって注目していてもよいのかなと思っています。
