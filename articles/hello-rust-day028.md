---
title: "100日後にRustをちょっと知ってる人になる: [Day 28]The State of WebAssembly 2022"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: true
---
## Day 28 のテーマ

今日は趣向を変えて、WebAssembly に関するサーベイのレポートを眺めてみようと思います。
今年の 6 月に公開されていた **The State of WebAssembly 2022** の内容を見てみます。

- [The State of WebAssembly 2022](https://blog.scottlogic.com/2022/06/20/state-of-wasm-2022.html)

## The State of WebAssembly 2022

このサーベイは、**WebAssebmly** の開発や利用に関する 2022 時点の現在の状況について以下の項目について調査を行いまとめたものになっています。

- 開発言語
- ユースケース
- ランタイム
- ロードマップ

また調査対象の回答者は以下のうような分類になっているようです。

![](https://storage.googleapis.com/zenn-user-upload/aae6720e482e-20220920.png)
![](https://storage.googleapis.com/zenn-user-upload/2f38b6d87b1d-20220920.png)

WebAssembly への関心の高まりの現れなのか、回答してくれたエンジニアは WebAssembly 経験が 1 年未満の方よりも、2〜3 年の方が多い結果となっていました。また、バックエンドスキルに長けた方が多いのが意外でした。まあ、ぼくもバックエンドスキルの方が得意なんですけどね。

## 開発言語

現在 WebAssembly 開発に利用している言語についての質問です。この結果は、個人的には納得なのですが **Rust** がトップになっていました。昨年のサーベイ結果は見ていないのですが、昨年は **JavaScript** がトップだったようです。

![](https://storage.googleapis.com/zenn-user-upload/41cbdc10d0eb-20220920.png)

また次の結果も顕著で分かりやすいですね。次の質問は、今後 WebAssembly の開発に最も使用したい言語は何か？という調査です。今一番情報が普及しているのが Rust なので納得かなと思います。ただ、今後各言語が対応をしてきたときにも変わらず Rust がトップでいられるかどうか、そこか Rust の人気維持の踏ん張りどころなのかなって思いました。
個人的には、**Blazor** が追い上げてくるのでは !? と思っていたりします。

![](https://storage.googleapis.com/zenn-user-upload/581b81ae33a0-20220920.png)

## ユースケース

これも納得の結果かなと思います。大多数が Web 開発をユースケースとしています。

![](https://storage.googleapis.com/zenn-user-upload/5a4e931a92b0-20220920.png)

しかし、実は サーバレスやコンテナ化、またプラグイン環境としての利用が伸びてきているんですよね。そのため、相対的に Web 開発としてのユースケースは下がってきています。実際、事心も Kubecon の中でも WebAssembly についての関心の高まりを感じることができていました。軽量かつポータブルな特徴のある WebAssembly のユースケースは、今後さらに多種多様になってくるかもしれませんね。

![](https://storage.googleapis.com/zenn-user-upload/dbb5130a1b0b-20220920.png)

## ランタイム

[Day 19](http://localhost:8000/articles/hello-rust-day019) でも調べたように、WebAssembly はブラウザの利用以外でも使用されるケースが増えてきています。非ブラウザベースにユースケースのための仕様である WASI の策定もすすんできています。

Bytecode Alliance が提供している [WASI](https://wasi.dev/) のリファレンス実装と呼ばれている [wasmtime](https://github.com/bytecodealliance/wasmtime) の利用がトップですね。
この **wasmtime** ですが、たしか今日 9/20 にバージョン 1.0 になる、という予定なのですが、僕が確認した時点ではまだなっていませんでした。(9/21 0:00)

![](https://storage.googleapis.com/zenn-user-upload/c550382c130b-20220920.png)

## ロードマップ

Public Proposal として公開されている仕様 [WebAssembly proposals](https://github.com/WebAssembly/proposals) に関して関心のある対象についての調査です。

共有線形メモリとアトミックを追加するスレッドが最も関心を集めていました。また、例外処理の仕組みが次いで２位にきています。Rust だと Rust 自体には例外処理の仕様がないので Wasm 側にもっているのも面白いなとは思いました。

![](https://storage.googleapis.com/zenn-user-upload/6e069137294c-20220921.png)

次に [WASI](https://wasi.dev/) に関する仕様についての調査です。非ブラウザ環境での WebAssembly 利用の期待が高まってきているので、この WASI については重要になってきつつあります。

I/O がトップで、ソケット、ファイルシステム、ネイティブ スレッドがそれに続いていました。Wasm の仕様に対する期待と比較すると、WASI の結果は各仕様に対してまんべんなく期待が高い事が分かります。WASI そのものに対する期待が高いということが分かりますね。

![](https://storage.googleapis.com/zenn-user-upload/b6cdb7eb32a5-20220921.png)

最後の質問が、WebAssebmly が今後将来に成功するために最も必要とされることについて質問をしています。
ここでも、非ブラウザー用途での API がトップになっていました。これからも、やはり WASI に対する関心の高さと重要性が読み取れました。

![](https://storage.googleapis.com/zenn-user-upload/07dc4c32c807-20220921.png)

## Day 28 のまとめ

[The State of WebAssembly 2022](https://blog.scottlogic.com/2022/06/20/state-of-wasm-2022.html) で徴されていた、以下の観点について見てみました。

- 開発言語
- ユースケース
- ランタイム
- ロードマップ

Rust に対する注目が高まってきているということと、非ブラウザ用途での WebAssembly (WASI) に対する期待が高まってきているということが、改めて調査結果から分かりました。
