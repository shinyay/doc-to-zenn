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

## mod_wasm アーキテクチャ

**mod_wasm** は 2 つのライブラリから構成されています。

![](https://storage.googleapis.com/zenn-user-upload/dcb8451237e7-20221214.png)

- **mod_wasm.so**
- **libwasm_runtime.so**

### mod_wasm.so

- C により開発

**mod_wasm.so** は、Apache HTTP Server の拡張モジュールとして動作します。
これは、Apache HTTP Server が持つ API と Wasmtime ランタイムを管理する Rust ライブラリの間のインターフェースの役割をします。

- WebAssembly に関する構成をする新しいディレクティブの処理
- `post_config()` と `content_handler()`

httpd.conf に次のように `wasm-handler` と WebAssembly バイナリファイルへのパス `<Location>` を定義することで、**mod_wasm** を有効にすることができます。

```conf
LoadModule wasm_module modules/mod_wasm.so

<Location /hello-wasm>
  SetHandler wasm-handler
  WasmModule /var/www/modules/hello_wasm.wasm
</Location>
```

### libwasm_runtime.so

- Rust により開発

**libwasm_runtime.so** は、Wasmtime ランタイムを介して WebAssembly モジュールを管理するための高レベルの API を提供しています。
Apache HTTP Server が受けた HTTP リクエストを受け取り、WebAssembly モジュールを設定して実行を行います。そして、レスポンス内容を解析して `mod_wasm.so` に制御を返します。

### Wasmtime

WebAssembly のランタイムで、Bytecode Alliance より提供されています。

- [Wasmtime 公式](https://wasmtime.dev/)

### 全体のシーケンス

Apache HTTP Server から Wasmtime までの処理の流れは次のようになります。

![](https://storage.googleapis.com/zenn-user-upload/484746d69142-20221214.png)

**mod_wasm** を有効にした Apache HTTP Server を起動すると、WebAssembly モジュールがメモリ上にプリロードされます。その動作の流れは次のようになります。

1. Apache HTTP Server の起動・初期化フェーズでは、**mod_wasm.so** が `httpd.conf` に定義した設定を読み込む
2. **libwasm_runtime.so** に定義情報を渡す
3. WebAssembly モジュールがファイルシステムから読み込まれて、Wasmtime でメモリ上にプリロードする

この処理は、リクエストを受け取るたびに最初から WebAssembly モジュールをロードするというものではないので、リクエスト処理の高速化に繋がります。

Apache HTTP Server が起動したので、リクエスト処理の準備ができたことになります。次に、**mod_wasm.so** は定義されたパスに属する全てを処理するために、全てのリクエストの評価を行います。そして、リクエストが処理されて **libwasm_runtime.so** に渡されます。このライブラリでは、HTTP ヘッダとリクエストボディを含む新しい wasmtime コンテキストを設定します。そして、モジュールを実行します。

情報の受け渡しには、WebAssembly のモジュラーシステムインターフェースである **WebAssembly System Interface (WASI)** を使用します。
WASI では、以下のような一般的なシステムインターフェースを設定することができます。

- 環境変数
- ファイルシステム
- 標準入出力
など

**libwasm_runtime.so** は、これらの機能を利用して以下のことを行います。

- HTTP ヘッダを環境変数として設定
- リクエストボディを標準入力で受け渡す

最後に WebAssembly モジュールは標準出力を通して全てのデータを返します。
HTTP レスポンスヘッダを先頭にし、そして次にコンテンツを探し、レスポンスを処理します。

このような一連の処理の流れによって **mod_wasm** は動作しています。

## Day 87 のまとめ
