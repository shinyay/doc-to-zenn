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

![](https://storage.googleapis.com/zenn-user-upload/dbab6a58664b-20221219.png)

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

v0.7.0 では次のようなフィーチャーが追加されていました:

- [Hashicorp Vault との統合](https://github.com/fermyon/spin/pull/798)
- [MySQL データベースへの接続の実験的サポート](https://github.com/fermyon/spin/pull/864)
- [既存のアプリケーションにコンポーネントを追加する「spin add」コマンド](https://github.com/fermyon/spin/pull/889)
- [Redis のセット操作に対応](https://github.com/fermyon/spin/pull/915)
- [Web URL からの Wasm モジュールのフェッチに対応](https://github.com/fermyon/spin/pull/890)
- [Linux ARM64上でのSpinの実行をサポート](https://github.com/fermyon/spin/pull/926)
- [JavaScriptおよびTypescriptアプリケーションの実験的サポート](https://github.com/fermyon/spin-js-sdk)

また、次のような連絡事項もありました。

- [Ubuntu 18.04 のサポートを終了](https://github.com/fermyon/spin/issues/990)
- [テンプレートはローカルでも更新が必要な場合あり](https://github.com/fermyon/spin/issues/990)
  - `spin templates install --git https://github.com/fermyon/spin --update`

ここで挙げられているアップデート内容をいくつか掘り下げて見てみたいと思います。

### Hashicorp Vault との統合

![](https://storage.googleapis.com/zenn-user-upload/8661dcb6de56-20221219.png)

**Hashicorp Vault** はとても有名な機密情報の管理ツールなのでご存知の方も多いのではないでしょうか。**トークン**や、**パスワード**、また**証明書**、**暗号鍵**といった機密情報へのアクセスを安全に保管し、厳密に制御するオープンソースツールです。**UI**、**CLI**、**HTTP API**を使用して機密データへのアクセスを安全に行うことができます。

- [Hashicorp Vault](https://www.vaultproject.io/)

