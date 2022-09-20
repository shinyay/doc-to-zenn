---
title: "100日後にRustをちょっと知ってる人になる: [Day 28]The State of WebAssembly 2022"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
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
- 関心のある機能

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



![](https://storage.googleapis.com/zenn-user-upload/dbb5130a1b0b-20220920.png)

## ランタイム

## 関心のある機能


## Day 28 のまとめ

