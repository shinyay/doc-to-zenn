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