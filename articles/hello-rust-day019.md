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

- [ケイパビリティベース・セキュリティ](#ケイパビリティベース・セキュリティ)

外部リソースへのアクセスは、ハンドラ (ケイパビリティ) で表されます。WASI では、リソースの名前を提供する文字列やその他のユーザー制御の識別子を提供することによってハンドルを要求する方法は存在しません。
リソースへのアクセスを得る唯一の方法は、明示的にハンドルを与えられるか、新しいハンドルを返すハンドルに対する操作を実行することです。

#### ケイパビリティベース・セキュリティ

広く使われているセキュリティアプローチは、ID ベースセキュリティです。認証された ID に基づいてアクセス制御を行うというものです。ケイパビリティベース・セキュリティは、ID ベースセキュリティとは異なるアプローチです。

まず、ケイパビリティとは、オブジェクトやリソースへの偽造不可能なな参照と、そのリソースにアクセスするための権限を指します。
機能ベースのセキュリティとは、ユーザー プログラムが機能を直接共有するようにユーザー プログラムを設計するという原則です。

- [Capability-based securitys](https://ja.wikipedia.org/wiki/Capability-based_security)

ID ベースのシステムでは、誰でもリソースへのアクセスを試みることができますが、アクセスが拒否される可能性があります。
ケイパビリティベースのシステムでは、リソースにアクセスする機能がない場合、リソースにリクエストを送信することはできません。

### WASI 設計原則 - Interposition

WASI のコンテキストの中での Interposition は、WebAssembly のインスタンスが与えられた WASI インターフェースを実装し、この実装を透過的に使用出来るようにすることです。
これによって、WASI API 使用するコードをへんこうすることなく、WASI API の機能を適用することができます。

WASI では、"**Link-Time Virturalization**" というメカニズムによって、Interposition が設定される、ということです。（Link-Time Virtualization については別途調べます…)

- [Link-Time Virtualization](https://github.com/WebAssembly/module-linking/blob/main/proposals/module-linking/Explainer.md#link-time-virtualization)
- [How and Why to Link WebAssembly Modules](https://training.linuxfoundation.org/blog/how-and-why-to-link-webassembly-modules/)


### WASI 設計原則 - Compatibility

WASIでは、WASI API自体に互換性の問題がないことを目指し、WASI libcなどのライブラリやツールを通じて互換性を提供しています。

これは、既存のアプリケーションやホストプラットフォームとの互換性が、API全体のクリーンさや安全性、パフォーマンスなどと相反する場合があるため、そのような問題かからの回避のためです。このようにすることで、互換性を必要としないアプリケーションは、負担を受ける必要がなくなります。

### WASI 設計原則 - Portability

WASI はモジュール方式をとっているため、WASI の全てのAPI を実装しなくてもよく、ホスト環境によって実装できないからといってAPIを排除する必要もありません。

## WASI の実装

この WASI はインターフェース仕様なので、これだけでは動作させることができません。WASI を実装したランタイムが必要になります。

WASI の実装ランタイムとしていろいろとあるのですが、以下のものが人気のようです。

- [Wasmtime](https://docs.wasmtime.dev/)
  - [Wasmtime - Repo](https://github.com/bytecodealliance/wasmtime)
- [Wasmer](https://wasmer.io/)
  - [Wasmer - Repo](https://github.com/wasmerio/wasmer)
- [Wasm3](https://wapm.io/vshymanskyy/wasm3)
  - [Wasm3 - Repo](https://github.com/wasm3/wasm3)
- [WasmEdge](https://wasmedge.org/)
  - [WasmEdge](https://github.com/WasmEdge/WasmEdge)

これら WASI ランタイムは `Hello World` しながら明日いててみたいなと思います。

## WebAssembly のユースケース

ｓて、今日見てきた **WASI** はまだまだ現在進行系で仕様策定をすすめている技術です。この WASI の発展と普及がすすむことで Web ブラウザ以外の様々なプラットフォームでの WebAssembly の利用が期待できるようになってくると思います。

最後に、今後の WebAssembly のユースケースとして考えられていることがリストされていたので、それを見ておきます。

- [Use Cases](https://webassembly.org/docs/use-cases/)

- **ブラウザの内部**
  - 画像・動画編集
  - ゲーム
  - ピアツーピア アプリケーション:
    - ゲーム
    - 共同編集
    - 分散型および集中型
  - 音楽ストリーミングサービス
  - 画像認識
  - ライブ ビデオ拡張
  - VR / AR
  - CAD アプリケーション
  - 科学的な視覚化とシミュレーション
  - インタラクティブな教育ソフトウェア
  - ニュース記事
  - プラットフォームのシミュレーション/エミュレーション
  - 言語インタープリターと仮想マシン
  - 既存の POSIX アプリケーションの移植を可能にする POSIX ユーザー空間環境
  - 開発者ツール:
    - エディター
    - コンパイラ
    - デバッガー
    - など
  - リモートデスクトップ
  - VPN
  - 暗号化
  - ローカル Web サーバー
  - Netscape Plugin Application Programming Interface (NPAPI)
  - エンタープライズ アプリケーション (データベースなど) のファット クライアント
- **ブラウザの外**
  - ゲーム配信サービス
  - サーバー側アプリケーション
  - モバイル デバイス上のハイブリッドネイティブアプリ
  - メインフレームアプリケーション

## Day 19 のまとめ

今日と今日で、Rust のユースケースとしても人気がある **Wasm (WebAssembly)** と ブラウザ以外の環境での動作のためのインターフェース仕様な **WASI** についてみてきました。
この WASI を実際に動かしてみるには、実装であるランタイムをインストールしておく必要があります。明日は、WASI ランタイムをいれて、`Hello World` してみたいなと思います。
