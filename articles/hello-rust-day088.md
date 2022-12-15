---
title: "100日後にRustをちょっと知ってる人になる: [Day 88]Wasm Workers Server 0.6.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust, webassembly, wasm]
published: false
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
- [attr マクロハンドラを worker にリネーム](https://github.com/vmware-labs/wasm-workers-server/pull/48)

修正事項などを含むアップデート内容の全ては以下のリポジトリの README に記述されています:

- [v0.6.0](https://github.com/vmware-labs/wasm-workers-server/releases/tag/v0.6.0)

## Day 88 のまとめ
