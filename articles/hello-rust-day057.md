---
title: "100日後にRustをちょっと知ってる人になる: [Day 57]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 57 のテーマ

[Day 56](https://zenn.dev/shinyay/articles/hello-rust-day056) では、**[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** で発表のあった **Fermyon Cloud** について使い方とシンプルなアプリケーションの作成＆デプロイの流れを見てみました。
しかし、流れを見ただけであって、実際には "何"をしているのかまでは説明を割愛していたところがあります。そこで、今日以降の中で **Fermyyon** のソリューションについて少し眺めつつ、それが Rust によるアプリケーションと組み合わせの効果がどのようにあるのか、そんなところを考えていきたいと思います。


さて、Day 56 で次のように伝えて居たと思います:

>WebAssembly アプリケーションの実行環境としての **Fermyon Cloud** の前に、本来だったら Fermyon が提供している次のプロジェクトを説明しておく必要があるのです。
>
>- ✅ **Spin**
>- ✅ **Fermyon Platform**

ということで、今日は **Spin** について少し見ていきたいと思います。

## Spin

**[Spin](https://github.com/fermyon/spin)** は WebAssembly コンポーネントを用いてイベント・ドリブンなサーバーサイド アプリケーションを作り、そして動かすためのフレームワークです。つまり、HTTP リクエストに対してレスポンスを返すような機能を持つ WebAssembly モジュールを書くためのインターフェースを提供するが、**Spin** なのです。

また、この **Spin** の注目すべき点は、多言語フレームワークであることです。**WebAssembly** と耳にすると、**Rust** や **Go** を思い浮かべるかもしれません。Spin ではもちろん Rust と Go をサポートしていますが、それ以外の言語もサポートをしています。

- サポート言語
  - Rust
  - Go
  - C/C++
  - Python
  - Ruby
  - AssemblyScript
    - <https://www.assemblyscript.org/>
  - Grain
    - <https://grain-lang.org/>
  - Zig
    - <https://ziglang.org/>
  - C#
  - その他 .NET 言語 (F# など)

## Day 57 のまとめ
