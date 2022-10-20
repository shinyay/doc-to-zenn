---
title: "100日後にRustをちょっと知ってる人になる: [Day 51]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 51 のテーマ

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) では、OSS プロジェクトとして公開されたばかりの **Wasm Worker Server** について基本的なところを見て、さらにリクエストを受け付けて簡単な平文メッセージをレスポンスするだけのワーカーアプリケーションを作って動かしてみました。

チュートリアルの中でも動かし方を中心に追いかけるように環境を準備し、ワーカーを作成して動作を確認したのみだったので、もう少しどのように動くかを見てみようと思います。

## Wasm Workers Server に関する復習

**[Wasm Worker Server](https://github.com/vmware-labs/wasm-workers-server)** は、WebAessembly を用いてアプリケーションを動作させるための HTTP サーバーでした。
この動作させるアプリケーションのことは、ワーカー (Worker) と呼ばれ、一般的には Edge などで動作させたりするような軽量なアプリケーション仕様です。

- [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers)

このアプリケーションは、**ハンドラ** と呼ばれるモジュールを作成し、単一あるいは複数のハンドラを組み合わせて構成します。これらのハンドラは、それぞれアプリケーション内部で特定の HTTP パスに対してレスポンスする役割をもっています。

言語サポート:

|言語|Wasmモジュール|インタプリタ|
|---|------------|----------|
|Rust|🙆🏻‍♀️|🙅‍♂️|
|JavaScript|🙅‍♂️|🙆🏻‍♀️|
|拡張予定...|拡張予定...|拡張予定...|

というわけで、昨日は Rust でのハンドラモジュールを作成してみました。

## Wasm Workers Server の動作

ハンドラは次のように動作します:

- リクエストの受付けとレスポンスの返却
- WASI Standard Input / Output を介したデータの送受信

**STDIN** と **STDOUT** を使用したデータ送受信を行うインターフェースにすることにより、この **Wasm Workers Server** 以外の WASI ランタイム環境でも動作する互換性のあるハンドラを作成することができます。

サーバーは次のように動作します:

1️⃣
2️⃣
3️⃣
4️⃣
5️⃣
6️⃣

## Day 51 のまとめ
