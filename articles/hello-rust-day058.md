---
title: "100日後にRustをちょっと知ってる人になる: [Day 58]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 58 のテーマ

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056) と [Day 57](https://zenn.dev/shinyay/articles/hello-rust-day056) と続いて、Fermyon のソリューションについて紹介をしました。

- Fermyon Cloud
- Fermyon Spin

この 2 日間 Fermyon に注目した理由というのは、今週 (10月 24 - 28) アメリカのデトロイトで、**[KubeCon + CloudNativeCon](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/)** が開催されていたからなのです。
そのイベントに併せて併設開催されていたイベントに、**[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** が開催されていたのです。

![](https://storage.googleapis.com/zenn-user-upload/c9e07391e9a0-20221028.png)

このイベントは名前通り、**Wasm** (WebAssembly) をテーマにしたものです。様々な **WebAssembly** に取り組んでいる企業が参加いて先進的な内容の発表がおこなわれていました。

さて、このイベントのダイアモンドスポンサーになっていたのが、この **Fermyon** だったのです。(それと Docker, Inc です。)
![](https://storage.googleapis.com/zenn-user-upload/f5480f842019-20221028.png)

Docker も、このイベントの中で注目を集めるアナウンスをしていましたよね。知名度で言うと Docker はやはり高いので、目にされた方も多かったのではないでしょうか。

- [これ (Beta)](https://docs.docker.com/desktop/wasm/)

こちらの話はまたどこかでと、この場では置いておいて、注目したのは次のセッションで **Fermyon Cloud** のアナウンスがあったのです。

- [Keynote: WebAssembly Development is Easy - Matt Butcher, CEO & Radu Matei, CTO, Fermyon Technologies, Inc.](https://cloudnativewasmdayna22.sched.com/event/1AUDA/keynote-webassembly-development-is-easy-matt-butcher-ceo-radu-matei-cto-fermyon-technologies-inc?iframe=no&w=100%&sidebar=yes&bg=no)

![](https://storage.googleapis.com/zenn-user-upload/c4bc9ea08840-20221028.png)

もともと Rust を学び始めたきっかけになったのも、この Fermyon Spin を使いこなしたいなっていう思いからというのもあったので、今回の発表に注目をしていたのでした。

というわけで、今日は [Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056) に引き続き、改めて **Fermyon Cloud** を見てみたいと思います。

## Fermyon Cloud ふたたび

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056#4.-fermyon-cloud-%E3%81%B8%E3%81%AE%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3) で Fermyon Cloud にログインしてデプロイをするということを行いました。

デプロイ自体は `spin deploy` というコマンド 1 つで実施を行いました。とはいえ、このコマンドが発行されたあと、裏側でどのように デプロイの挙動をしているかが気になる人もきっといるのではないでしょうか。
そこの答えの鍵になるのが、**Fermyon Cloud** が **Fermyon Platform** をベースにしているという点です。

- [Fermyon Platform](https://www.fermyon.com/platform)

前回も紹介したように、Fermyon Platform は WebAssembly アプリケーションのためのオープンソーステクノロジーベースのクラウドアプリケーションプラットフォームです。

次のプロジェクトが利用されています。

- [bytecodealliance/wasmtime](https://github.com/bytecodealliance/wasmtime)
- [deislabs/bindle](https://github.com/deislabs/bindle)
- [deislabs/hippo](https://github.com/deislabs/hippo)
- [fermyon/spin](https://github.com/fermyon/spin)
- [hashicorp/consul](https://github.com/hashicorp/consul)
- [hashicorp/nomad](https://github.com/hashicorp/nomad)
- [hashicorp/terraform](https://github.com/hashicorp/terraform)
- [traefik/traefik](https://github.com/traefik/traefik)


## Day 58 のまとめ
