---
title: "100日後にRustをちょっと知ってる人になる: [Day 22]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 22 のテーマ

この数日間、Rust の観点から **WebAssembly** について見てきています。
この WebAssembly ですが、**WASI** の仕様ではブラウザ以外でも動くことを目的としていますが、もちろん WebAssembly 自体はブラウザ上でポータブルかつ安全に動作することを目的として誕生してきています。ブラウザ上でアプリケーションを動かすというと、**JavaScript** を思い浮かべると思います。では、WebAssembly が目指しているのは JavaScript の置き換えなのでしょうか？

次の記事に興味深い記述がありました。

- [Making WebAssembly better for Rust & for all languages](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/)

> **WebAssembly** は **JavaScript** に取って代わるものではなく、JavaScriptと一緒に使う素晴らしいツールになることを目指しています。

**WebAssembly** を介して、Rust と JavaScript の間で次のようなことが実現できるようになることが望まれているということなのです。

- Rust 開発者は、**Node.js 開発環境を必要とせず**に JavaScript で使用する WebAssembly パッケージを作成できる
- JavaScript 開発者は、**Rust 開発環境を必要とせず**に WebAssembly を使用できる

![](https://storage.googleapis.com/zenn-user-upload/6d2e5411eed5-20220914.png)

## wasm-pack

![](https://storage.googleapis.com/zenn-user-upload/ddd18f0b3f3c-20220914.png)

**wasm-pack** は WebAssembly をターゲットとする Rust クレートを組み立て、パッケージ化するためのツールです。これらのパッケージはnpmレジストリに公開され、他のパッケージと一緒に使用することができます。つまり、JSや他のパッケージと並べて使うことができ、様々な種類のアプリケーションで使うことができます。

- [wasm-pack](https://github.com/rustwasm/wasm-pack)



## Day 22 のまとめ
