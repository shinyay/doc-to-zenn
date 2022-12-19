---
title: "100日後にRustをちょっと知ってる人になる: [Day 90]Fermyon Spin v0.7.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087)、そして[Day 88](https://zenn.dev/shinyay/articles/hello-rust-day088) といろいろなモジュールの新しくリリースされたバージョンを見てみました。
そして今日も新しいものの発表があったので、それを見てみようと思います。

[Day 57](https://zenn.dev/shinyay/articles/hello-rust-day087) で紹介をしていた **Fermyon Spin** が 12 月 16 日にv0.7.0 が発表されていました。今日はそのアップデートについて見たみたいと思います。

## Fermyon Spin

Spin については [Day 57](https://zenn.dev/shinyay/articles/hello-rust-day087) の中で使い方について紹介をしているので、そちらを見て欲しいと思います。
簡単に少しだけ説明すると、**WebAssemby** をコンパイルターゲットとするフレームワークです。フレームワークというと、ある特定の言語で作業効率をよくするために用いられる事が多いと思います。この Spin は様々な多言語に対応しているフレームワークです。
Web アプリケーションやマイクロサービスのような HTTP リクエストへの応答を実行できる WebAssembly モジュールを作成するためのインターフェースを提供できるフレームワークになっています。

そして、ぼくがよく Spin を伝えるときに使っている代表的な 3 つのコマンドが次のものです。

✨spin new
🛠spin build
🚀spin deploy

極端な話でいうと、この 3　コマンドがあればビルドして実行することが可能となります。

## Spin v0.7.0

それでは、Spin v0.7.0 について見ていこうと思います。リリースノートはこちらです。

- [v0.7.0](https://github.com/fermyon/spin/releases/tag/v0.7.0)
