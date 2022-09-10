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

以下のように WASI のことを説明していました。

🙆🏻‍♂️ 標準化されたAPIのモジュール化されたコレクションである
🙅‍♀️ モノリシックな標準システムインターフェースではない

**WASI 設計原則**

WASI の設計指針として、次の 4 つの原則があります:

1. Capability-based security (ケイパビリティベース)
2. Interposition (割り込み)
3. Compatibility (互換性)　
4. Portability (ポータビリティ)

### WASI 設計原則 - Capability-based security

WASI はケイパビリティベースのセキュリティ原則によって作られています。このケイパビリティベース・セキュリティという原則、あまり聞き馴染みのない方もいると思います。まず、簡単にこの考え方についてまとめておきます。

- [ケイパビリティベース・セキュリティs](#ケイパビリティベース・セキュリティ)

#### ケイパビリティベース・セキュリティ

広く使われているセキュリティアプローチは、ID ベースセキュリティです。認証された ID に基づいてアクセス制御を行うというものです。ケイパビリティベース・セキュリティは、ID ベースセキュリティとは異なるアプローチです。

まず、ケイパビリティとは、オブジェクトやリソースへの偽造不可能なな参照と、そのリソースにアクセスするための権限を指します。
機能ベースのセキュリティとは、ユーザー プログラムが機能を直接共有するようにユーザー プログラムを設計するという原則です。

- [Capability-based securitys](https://ja.wikipedia.org/wiki/Capability-based_security)

ID ベースのシステムでは、誰でもリソースへのアクセスを試みることができますが、アクセスが拒否される可能性があります。
ケイパビリティベースのシステムでは、リソースにアクセスする機能がない場合、リソースにリクエストを送信することはできません。

### WASI 設計原則 - Interposition

### WASI 設計原則 - Compatibility

### WASI 設計原則 - Portability

## Day 19 のまとめ
