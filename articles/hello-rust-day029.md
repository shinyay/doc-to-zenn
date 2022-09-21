---
title: "100日後にRustをちょっと知ってる人になる: [Day 29]Wasmtime 1.0.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: true
---
## Day 29 のテーマ

[Day 28](https://zenn.dev/shinyay/articles/hello-rust-day028) のランタイムのセクションでも[少し触れていた](https://zenn.dev/shinyay/articles/hello-rust-day028#%E3%83%A9%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%A0) **Wasmtime** の 1.0.0 リリースのについてですが、予定どおり本日リリースされました。

- **リリースアナウンス**
  - [Wasmtime Reaches 1.0: Fast, Safe and Production Ready!](https://bytecodealliance.org/articles/wasmtime-1-0-fast-safe-and-production-ready)
- **GitHub リポジトリ**
  - [v1.0.0: Release Wasmtime 1.0.0](https://github.com/bytecodealliance/wasmtime/releases/tag/v1.0.0)

ということで、今日は改めて **Wasmtime** について見ておきたいと思います。

## Wasmtime 概要

Wasmtime とは、**Bytecode Aliance** がスタンドアロンで **WebAssembly**　を動作させるために提供している **WASI (WebAssembly System Interface)** の実装のことです。

- **WASI (WebAssembly System Interface)**: ファイルシステムやソケット、乱数など OS のような機能へのアクセスを提供し、非ブラウザ環境でも WebAssembly を動作させるための API 仕様の標準化
- **Bytecode Aliance**: WebAssembly や WASI に関する仕様の標準化策定をリードする非営利団体

つまり、Wasmtime を実行環境とし、ブラウザ以外の環境でどこでも WebAssembly バイナリを動作させる事が可能になります。
また、WASI の仕様策定をすすめている Bytecode Aliance による実装のため、参照実装としての意味合いもある WASI の実行ランタイムです。
## Wasmtime 1.0.0 リリース

冒頭にも記載したように、この **Wasmtime** が本日 (9/20) に 1.0.0 にメジャーバージョンアップしました。

- [Wasmtime Reaches 1.0: Fast, Safe and Production Ready!](https://bytecodealliance.org/articles/wasmtime-1-0-fast-safe-and-production-ready)

このリリースアナウンスを少し見てみます。

### プロダクション・レディ

![](https://storage.googleapis.com/zenn-user-upload/6fe5383db11e-20220921.png)

今回のアナウンスの中で最も強くメッセージングしているキーワードが **プロダクション・レディ** です。つまり、**Wasitime** を使用して WebAssembly を本番稼働させてもよいクオリティになっていると謳われています。実際のところは、WebAssembly / WASI の仕様が現在進行系で策定が進んでいるところなので、より高度で成熟した WASI 仕様に準じた WebAseembly アプリケーションの開発ができるようになるのは、まだ少しさきかもしれません。しかし、動作させる WASI ランタイム環境としては、**超高速**で**超安全**なプラットフォームが利用できるようになったことは、喜ばしく感じます。

- [WebAssembly Proposals](https://github.com/WebAssembly/proposals/blob/main/README.md)
  - [Finished Proposals](https://github.com/WebAssembly/proposals/blob/main/finished-proposals.md)
  - [Inactive Proposals](https://github.com/WebAssembly/proposals/blob/main/inactive-proposals.md)

### Wasmtime による想定本番ユースケース

[Day 28](https://zenn.dev/shinyay/articles/hello-rust-day028) で参照していた **[The State of WebAssembly 2022](https://blog.scottlogic.com/2022/06/20/state-of-wasm-2022.html)** の中でも、ユースケースとして以下のものが言及されていました:

- **サーバレス**
- **コンテナ化**
- **プラグイン**

> The use of WebAssembly for Serverless, Containerisation and as a plug-in host has climbed significantly

![](https://storage.googleapis.com/zenn-user-upload/959fc6dfc1c5-20220921.png)

### サーバレス

今回のアナウンスの中でも、ユースケースとして同じものが挙げられていました。特に、最初に挙げられているユースケースの **サーバレス** はとてもはまるものだと思います。
起動にかかる時間が**マイクロ秒**単位のような、非常にフットプリントが小さいアプリケーションは、スケールアウト・スケールインを前提としているようなサーバレスアプリケーションやマイクロサービスには最適なアプリケーション実行形態だと言えます。

### プラグイン

あるプラットフォーム上でサードパーティ製のプラグインを動かしたい要望は多くあると思います。この際に懸念される一番の要件はサードパーティ製プラグインからプラットフォームへの依存です。何か不具合がプラグイン側に潜在していて、それが不用意にプラットフォームに持ち込まられることが一番避けるべき懸念のはずです。プラグインシステムの利便性とリスクが隣り合わせにあるのは、そこだと思います。
WASI の場合は、サンドボックス化されている(**Capability-based Security**)ため、明示的にリソースに対するアクセスのハンドルが与えられない限り、プラットフォームが危険に冒されることはありません。

- [Capability-based security (WASI Design Principles)](https://github.com/WebAssembly/WASI#capability-based-security)

プラグインシステムをセキュアに構築するために、WASI を活用することが望まれてるのは理にかなっていると思います。

![](https://storage.googleapis.com/zenn-user-upload/277acb700563-20220921.png)

### データベース内コード (ユーザー定義関数)

このデータベース内部で WwbAssembly を動作させてコードを実行するというユースケースは今まで考えたことがなかったのですが、とてもあり得るユースケースだと思いました。アプリケーションとデータベースの間に多数発生するクエリの発行を抑止して、データベース内部でコード処理を行って結果を返す、まさに次世代のストアドプロシジャか、PL/SQL かと、いうような使い方です。対応するデータベースの登場が待ち遠しいかなと思いました。
（調べていませんけど、もしかしたら既に登場しているんですかねー？）

![](https://storage.googleapis.com/zenn-user-upload/cbb497b2b495-20220921.png)

### Trusted Execution Environment (TEE)

Trusted Execution Environment (TEE) 自体は、ぼくもあまり詳しくないのですけど、**[Intel SGX](https://www.intel.co.jp/content/www/jp/ja/architecture-and-technology/software-guard-extensions.html)** や **[Arm TrustZone](https://www.arm.com/ja/technologies/trustzone-for-cortex-a)** のように、CPU によりメモリ上に **Enclave(エンクレーブ)** と呼ばれる暗号化されセキュアに分離された領域のことです。
WebAssembly は CPU アーキテクチャに依存せず、分離されたセキュアなサンドボックス空間として動作をするため、**TEE** としての利用が期待できると思います。

![](https://storage.googleapis.com/zenn-user-upload/18f9a6defaf2-20220921.png)

## Wasmtime の高速動作

Wasmtime はプロダクション・レディを担保する**高速性**をうたっています。その高速動作にするための理由が簡単に説明されていました。
ポイントは２つ、**インスタンス化** と **ランタイム**の効率性 です。

### インスタンス化

仮想メモリを活用し、インスタンス間で可能な限り多くのメモリを共有し、それらのインスタンスの 1 つがデータを変更する必要がある場合にのみメモリの新しいページを作成するという動作をとります。
これにより、新しいインスタンスを作成するたびに新しいメモリを作成する必要がなくなります。

また、WebAssembly のモジュールには、宣言されているが使用されない多くの関数が含まれる場合があります。そのような関数を、実際に使用されるまで初期化を遅延させます。
これにより、起動が高速化され、関数が使用されていない場合に実行する必要がある全体的な作業が削減されるということになります。

### ランタイムの効率性

ソースコードから WebAssembly バイナリなマシンコードに変換するコンパイラ **Cranelift** の進化により最適化されたマシン命令が選択されるようになっています。

- [Cranelift - A New Register Allocator](https://cfallin.org/blog/2022/06/09/cranelift-regalloc2/)

## 1.0 以降の Wasmtime

今後、Wasmtimeの新しいメジャーバージョンは **1 ヶ月に 1 回**提供される予定ということです。
毎月 5 日にバージョンを上げるためのプルリクエストが送られ、プルリクエストがマージされた時点でリリースが行われます。

今後の早いサイクルで進むバージョンアップによる進化に期待が膨らみます。

## Day 29 のまとめ

今日は、9/20 (日本時間の今日9/21) にリリースされた **Wasmtime 1.0.0** についていろいろと見てみました。
今後の発展に期待が膨らみます。今後も継続的に注目しておきたいと思います。
