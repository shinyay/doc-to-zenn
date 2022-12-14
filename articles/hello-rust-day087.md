---
title: "100日後にRustをちょっと知ってる人になる: [Day 87]mod_wasm"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust, webassembly, wasm]
published: false
---
## Day 87 のテーマ

今日も少し趣向を変えて、Rust の使い方ではなく、Rust がどのようなところで利用されているのかということを見てみたいと思います。特に最近では、Rust を使って WebAssembly という話はよく目にすると思います。実際ぼくも [Day 20](https://zenn.dev/shinyay/articles/hello-rust-day020) あたりや、[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) あたりで WebAssembly について勉強をしていました。Rust の公式サイトにもユースケースとして WebAssembly が書かれていますよね。

![](https://storage.googleapis.com/zenn-user-upload/e1126622ef9e-20221214.png)

今日は WebAssembly のイメージの作り方ではなくて、Rust を使って作られた WebAssembly のライブラリが使用されているモジュールについて見ていきたいと思います。

## VMware Wasm Labs による mod_wasm

**mod_wasm** という、モジュールをご存知でしょうか？ 名前からも察することはできると思いますが、Apache Http Server 用の WebAssembly ランタイムのモジュールです。今年の 10 月に VMware の Wasm Labs が公開しました。

- [mod_wasm: run WebAssembly with Apache](https://wasmlabs.dev/articles/apache-mod-wasm/)

また、この **mod_wasm** に関する内容を同じく 10 月に開催されたカンファレンスの [Cloud Native Wasm Day North America](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/) の中でも発表をされていました。

![](https://storage.googleapis.com/zenn-user-upload/7ab2840de34a-20221214.png)

以下がその時の動画とスライドです。

https://www.youtube.com/watch?v=jXe8kulUscQ&list=PLj6h78yzYM2PzLhPvZIihwPShNuXP01C5
- [スライド](https://cloudnativewasmdayna22.sched.com/event/1AUDk/modwasm-bringing-webassembly-to-apache-daniel-lopez-ridruejo-rafael-fernandez-lopez-vmware?iframe=no)

動画の中で、この mod_wasm については説明されているのですが、自分の理解を深めるために自分の言葉で説明していこうと思います。

## mod_wasm 概要

Apache HTTP Server は通常は `mod_proxy` や `ModSecurity` などを利用してプロキシサーバだったり WAF として使用したりしていることが多いのではないでしょうか。**mod_wasm** は **WebAssembly** モジュールを Apache Http Server で実行することを可能にするもジューリなのです。
mod_wasm を実装した Apache Http Server は、WebAssembly にコンパイルされたアプリケーションにより外部からの HTTP リクエストに対して応答する事が可能になります。内部的には、**Wasmtime** ランタイムを使用していて、WebAssembly モジュールの設定や初期化、そして実行を行います。

Wasmtime については以前 `1.0.0` がリリースされた時に記事を書いています。

- [[Day 29]Wasmtime 1.0.0](https://zenn.dev/shinyay/articles/hello-rust-day029)
- [Wasmtime 公式](https://wasmtime.dev/)

## mod_wasm アーキテクチャ

**mod_wasm** は 2 つのライブラリから構成されています。

![](https://storage.googleapis.com/zenn-user-upload/dcb8451237e7-20221214.png)

- **mod_wasm.so**
- **libwasm_runtime.so**

### mod_wasm.so
### libwasm_runtime.so

## Day 87 のまとめ
