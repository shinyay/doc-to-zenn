---
title: "100日後にRustをちょっと知ってる人になる: [Day 18]WebAssembly (Wasm)"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: true
---
## Day 18 のテーマ

Rust で作られたモノというものを見たことありますか？
多分なのですが、実際に自分で触ってみたりしたことがある Rust で作られたモノっていうのは、コマンドラインとかが多かったりしませんか？

たとえばこういうコマンドラインなどです：

- [bat (catの代替)](https://github.com/sharkdp/bat)
- [exa (lsの代替](https://github.com/ogham/exa)
- [fd (findの代替)](https://github.com/sharkdp/fd)
- [ripgrep (grepの代替](https://github.com/BurntSushi/ripgrep)
- [delta (diffの代替)](https://github.com/dandavison/delta)

他にも数多く Rust 製のコマンドがあります。軽いし便利なモノが多くて僕もイロイロと見つけては使ったりとしています。
このように Rust でコマンドが作られている理由の１つには、Rust がクロスプラットフォーム開発に対応しているから、ということも言えると思います。
一度作ったものを様々なところで使えるというのは便利ですよね。
まさに、かつて Java で言われ始めていた、**「Write once, Run anywhere」** という感じですよね。

今日はコマンドラインの作り方について考えるというのではなくて(完全に前フリではコマンドラインでしたけど…)、新しい **「Write once, Run anywhere」** ともいわれている、**WebAssembly (Wasm)** についてです。

### WebAssembly (Wasm)

**WebAssembly (Wasm)** について知らない方、または Rust で **WebAssembly (Wasm)** というところにイメージが持てない方などいらっしゃると思います。
しかし、Rust の公式サイトを見ると…

![](https://storage.googleapis.com/zenn-user-upload/a21d84ae3e5d-20220909.png)

はっきりと、**WebAssembly** という項目が書かれているんですよね。それくらい、Rust の用途として **WebAssebly** というものが注目を浴びているのです。

それでは、**WebAssembly** が何かということを追いかけていきたいと思います。

#### WebAssembly とは?

最近よく目にする WebAssembly のユースケースとして、Web ブラウザ上でアプリケーションを動かすというものを目にすることが増えています。そのため、ブラウザ用のアプリケーション技術と思う方もいるかもしれません。しかし、実態としては Webブラウザ以外でも動作させることができます。たとえば、ブロックチェーンのプラットフォーム上で動かすこともできます。

きちんとした定義を策定された仕様から確認してみます。

- [WebAssembly Specification Release 2.0 (Draft 2022-09-01)](https://webassembly.github.io/spec/core/intro/introduction.html)

> WebAssembly (abbreviated Wasm) is a safe, portable, low-level code format designed for efficient execution and compact representation. Its main goal is to enable high performance applications on the Web, but it does not make any Web-specific assumptions or provide Web-specific features, so it can be employed in other environments as well.

- [webassembly.org](https://webassembly.org)

> WebAssembly (abbreviated Wasm) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications.

つまり、**スタックベースの仮想マシンのためのバイナリ命令フォーマット** というところが定義のポイントになりそうですよね。この仮想マシンで仮想的な CPU の命令セットの構造を持ち、Web ブラウザのような環境上でネイティブコードのように実行できるのが WebAssembly というのが適切かもしれないです。

この仮想マシンですが、特定の実在のCPUのコードではないため、仮想マシンでコードを解釈して実行環境のCPUの命令に変換しながら実行していくという動きをとるようです。つまり、この動き方はスクリプト言語の動き方に近いのですが、**WebAssembly** は一般的な CPU の命令セットに似た構造となっているため、構文の解釈や変換は非常に高速に行うことができるそうです。

また、ブラウザ等の実行環境上に、独立した仕様になっている仮想マシンを用意して動作させることができるので、様々な環境や OS に対応することができるのが WebAssembly のメリットと言えます。さらに、仮想マシンを経由しての実行となるので、ネイティブコードより安全だと言うことができます。

### つまり Wasm の特徴とは?

✅ **Java** ような **Portable Executable**
✅ **.NET CLI (Common Language Infrastructure)** のような **共通言語バイトコード**
✅ **eBPF** のような **セキュアサンドボックス**
✅ **Lua** のような **組み込みランタイム**

#### デザインゴール

WebAssembly のデザインゴールについて仕様の中の以下について触れられています。

- [Design Goals](https://webassembly.github.io/spec/core/intro/introduction.html#design-goals)

**高速、安全、移植可能なセマンティクス**
✨ 高速
✨ 安全
✨ Well-Defined
✨ ハードウェア非依存
✨ 言語非依存
✨ プラットフォーム非依存
✨ オープン

**効率的でポータブルな表現**
🚀 コンパクト
🚀 モジュラー
🚀 効率的
🚀 ストリーミング可能
🚀 並列化可能
🚀 ポータブル

### Webブラウザ用途以外の Wasm (WASI)

ところで、Wasm の仕様や定義を見てみましたが、ブラウザ以外の環境で動作させるための仕様やインターフェースについてはふれられていませんでした。
Web ブラウザ以外で Wasm を動かすためのインターフェースが、**[WebAssembly System Interface (WASI)](https://wasi.dev/)** というものなのです。

**WASI** の誕生について調べてみると、つぎの発表の中ではじめて宣言がなされていました。

- [Standardizing WASI: A system interface to run WebAssembly outside the web](https://hacks.mozilla.org/2019/03/standardizing-wasi-a-webassembly-system-interface/)

> WebAssembly が概念的なマシンのアセンブリ言語であるように、WebAssembly は単一のオペレーティングシステムではなく、概念的なオペレーティング システムのシステム インターフェイスを必要とします。
このようにして、すべての異なる OS で実行できます。これが WASI であり、WebAssembly プラットフォームのシステム インターフェイスです。

また、次の WASI の概要にも記載がありますが、このWASI によって目指しているところが、ブラウザに依存しないように設計をしブラウザ以外のプラットフォームでもWasm を動かすようにするというものです。

- [WASI: WebAssembly System Interface](https://github.com/bytecodealliance/wasmtime/blob/main/docs/WASI-overview.md)

そして、この WASI の仕様自体の策定も現在進行系で進んでいる最中です。

> Work in Progress
WASI is currently experimental. Feedback is welcome!

WASI について改めて学んでみたいと思います。

## Day 18 のまとめ

今日は Rust のユースケースにもあげられている WebAssembly について調べてみました。
Webブラウザ上で高速・安全にアプリケーションを動かす仕組みとして誕生した **WebAssembly (Wasm)** が、ブラウザ以外のプラットフォームでも動作できるように **WebAssembly System Interface(WASI)** というインターフェース仕様を進めているということが分かりました。しかし、まだまだ深いところまでは読み取れていないので、Wasm / WASI について改めて深堀りをしていきたいと思います。
