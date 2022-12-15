---
title: "100日後にRustをちょっと知ってる人になる: [Day 88]Wasm Workers Server 0.6.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust, webassembly, wasm]
published: true
---
## Day 88 のテーマ

[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087) では、Rust を用いて開発された WebAssebmly を Apache HTTP Server で動作させるための **mod_wasm** について見てみました。そこでも紹介したように、mod_wasm は **VMware Wasm Labs** が公開しているオープンソースです。また、記事の中でも触れましたが [Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) で紹介をした **Wasm Workers Server** も同じく **VMware Wasm Labs** が公開しているオープンソースの WebAssembly をサーバーレスとして動作させる実行環境でした。

ふと、この **Wasm Workers Server** のリポジトリを見ていると、**12 月 2 日** に、ぼくが使用しているバージョンから上がっていました。そこで、今日はそのアップデートについて見てみたいかなと思います。

## Wasm Workers Server

![](https://storage.googleapis.com/zenn-user-upload/89169fa9e991-20221215.png)

以前すでにこの **Wasm Workers Server** について説明を行ったので、今日は細かなことは記載しません。どういうものかは、以下の内容を見てください。

- [[Day 50]Wasm Workers Server](https://zenn.dev/shinyay/articles/hello-rust-day050)
- [[Day 51]Wasm Workers Server の動作](https://zenn.dev/shinyay/articles/hello-rust-day051)
- [[Day 52]Wasm Workers Server と KVS](https://zenn.dev/shinyay/articles/hello-rust-day052)
- [[Day 53]wasm-workers-server-kit クレート](https://zenn.dev/shinyay/articles/hello-rust-day053)

簡単に表現すると、**Wasm Workers Server** は、WebAssembly 上でアプリケーションを実行するためのHTTPサーバです。
そのアプリケーションは **workers** というパターンに従っており、すべての URL はリクエストを処理しレスポンスを提供する個別のモジュールに関連付けられるようになっているものです。

さて、一応改めてですが、現在の **Wasm Workers Server** のバージョン確認をしておきます。**Wasm Workers Server** の操作は `wws` CLI ツールで行います。

```shell
$ wws --version

wasm-workers-server 0.5.0
```

この `0.5.0` は最初に公開されたバージョンで、10 月 17 日のものです。

- [v0.5.0](https://github.com/vmware-labs/wasm-workers-server/releases/tag/v0.5.0)

## 最新版へのアップグレード

`wws` CLI からのアップグレードには対応しておらず、新規にインストールを行う同じ手順を実施し、上書きをする操作になります。次のコマンドで、アップグレードを行います。

```shell
curl https://raw.githubusercontent.com/vmware-labs/wasm-workers-server/main/install.sh | bash
```

```text
👋 Hello
I'm going to install Wasm Workers Server in your system
⚙️  Downloading
⚙️  Decompressing
x ./
x ./LICENSE
x ./README.md
x ./wws
⚙️  Installing
Wasm Workers Server will be installed in /usr/local/bin.
This requires sudo permissions. If you prefer to install it
in your current directory, run the installer with --local.
If you want it to be global, just type your password:
Password:
🧹 Cleaning up
🚀 Wasm Workers Server (wws) was installed correctly!
You can now try it: wws --help
```

```shell
$ wws --version

wasm-workers-server 0.6.0
```

というわけで、`0.6.0` に最新化できました。

## Wasm Workers Server 0.6.0

さて、今最新化した **## Wasm Workers Server 0.6.0** ですが、これは 12 月 2 日にリリースされたものになります。
それでは、アップデート内容について見ていきます。

- [Wasmtime のバージョンを 3.0.0 に更新](https://github.com/vmware-labs/wasm-workers-server/pull/40)
- [静的アセット用のフォルダのサポート](https://github.com/vmware-labs/wasm-workers-server/issues/7)
- [Rust workers への環境変数を設定・注入に対応](https://github.com/vmware-labs/wasm-workers-server/issues/34)
- [Rust workers からバイト配列を返却に対応](https://github.com/vmware-labs/wasm-workers-server/pull/45)
- [URL の前にパスを追加する prefix オプションを追加](https://github.com/vmware-labs/wasm-workers-server/pull/37)
- [GitHub Actions でコンテナのビルドを自動化](https://github.com/vmware-labs/wasm-workers-server/pull/52)
- [Rust マクロ属性の名前を worker に変更](https://github.com/vmware-labs/wasm-workers-server/pull/48)

修正事項などを含むアップデート内容の全ては以下のリポジトリの README に記述されています:

- [v0.6.0](https://github.com/vmware-labs/wasm-workers-server/releases/tag/v0.6.0)

### Wasmtime のバージョンを 3.0.0 に更新 のバージョンを 3.0.0 に更新

**Wasmtime** とは、**Bytecode Aliance** がスタンドアロンで WebAssembly　を動作させるために提供している **WASI (WebAssembly System Interface)** の実装のことでした。

- [[Day 29]Wasmtime 1.0.0](https://zenn.dev/shinyay/articles/hello-rust-day087)

その Wasmtime のバージョンが **11 月 22 日** に `v3.0.0` がリリースされています。（最新版 は 12 月 2 日にリリースされている `v3.0.1` です。）
この `v3.0.0` に対応させています。

### 静的アセット用のフォルダのサポート

`v0.5.0` では、静的アセットの管理は WebAssembly モジュールで行う必要がありました。そのため、次のような難しくなる点がありました。

- 静的アセットの更新が面倒
- WebAssembly モジュールによる静的アセットのハンドリング

この新しい `v0.6.0` からは、`public` フォルダが採用されました。アプリケーションで公開したい静的アセットは、この `public` フォルダをプロジェクトのルートに作成して使用することができるようになります。
`public/sample.png` は `/sample.png` としてアクセスできるようになります。

### Rust workers への環境変数を設定・注入に対応

多くのアプリケーションプラットフォームと異なり、WebAssembly ランタイムはモジュールを完全に分離しているため、デフォルトでは環境変数にアクセスをしません。
`v0.6.0` では WebAssembly worker に環境変数を注入するための新しい設定パラメータが追加されました。WebAssembly worker に環境変数を追加するには、`TOML` ファイルを作成して、`[vars]` エントリを設定します。

```toml
[vars]
JSON_MESSAGE = "Hello! このメッセージは、環境変数からのものです。
```

また、`$` 記法により、既存の環境変数を渡したり、名前を変更することができます。

```toml
[vars]
TOKEN = "$TOKEN"
```

### Rust workers からバイト配列を返却に対応

従来は、すべての `Worker` 関数はボディタイプとして `String` を返すようになっていました。バイナリレスポンスは `String` としてエンコードができないために Worker のユースケースを制限していました。
`v0.6.0` では、Worker はレスポンスボディに `Content` というカスタムタイプを返すようになります。これにより、Worker は **文字列** (`String`) あるいは **バイナリデータ** (`Vec<u8>`) をクライアントに返すことができるようになります。

```rust
#[worker]
fn handler(req: Request<String>) -> Result<Response<Content>> {
    let mut buf = BufWriter::new(Vec::new());
    :
    :
}
```

### Rust マクロ属性の名前を worker に変更

ネーミングを統一するために、マクロ属性を `handler` から `worker` に変更になっています。

変更前:

```rust
use wasm_workers_rs::{
   http::{self, Request, Response},
   handler, Content,
};

#[handler]
fn handler(req: Request<String>) -> Result<Response<Content>> {
   // ...
}
```

変更後:

```rust
use wasm_workers_rs::{
   http::{self, Request, Response},
   worker, Content,
};

#[worker]
fn handler(req: Request<String>) -> Result<Response<Content>> {
   // ...
}
```

## Day 88 のまとめ

**Wasm Workers Server** は `v0.6.0` になり、Web アプリケーションの実行環境としての使い勝手が随分とあがりました。
**静的アセット**や**環境変数**の利用などはすぐに使ってみたい機能だと思いました。
`v1.0.0` に向けての今後の発展が楽しみです。
