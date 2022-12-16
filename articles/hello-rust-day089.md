---
title: "100日後にRustをちょっと知ってる人になる: [Day 89]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust, webassembly, wasm]
published: false
---
## Day 89 のテーマ

[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087) で **VMware Wasm Labs** が公開しているオープンソースの **mod_wasm** のポストを見て興味を持たれた方はいらっしゃるでしょうか。概要だけしか書いていなかったので、実際に動かしてみたいなと思った方もいるのかなと思います。

というわけで、今日は **VMware Wasm Labs** が公開している内容ですがサンプルの動かし方について簡単に紹介します。
なにか自分でサンプルを作って動かすのもやってみたいので、それはまた後日に行いたいと思います。

## mod_wasm のサンプル実行

**mod_wasm** の構成は先日紹介したように、**Apache HTTP Server** と **mod_wasm** モジュールが必要です。それぞれをダウンロードしてきて起動をしてもいいのですが、**VMware Wasm Labs** が コンテナイメージを提供しています。

- [httpd-mod-wasm コンテナイメージ](https://github.com/vmware-labs/mod_wasm/pkgs/container/httpd-mod-wasm)

これを実行することで、mod_wasm の動作大変をすることができます。
それでは、コンテナイメージを実行してみます。

```shell
docker run -p 8080:8080 ghcr.io/vmware-labs/httpd-mod-wasm:latest
```

起動すると、このコンテナイメージには既にいくつかの WebAssembly モジュールが入っているので、それらにアクセスして見てみます。

- Hello Wasm
- PHP Hello
- PrettyFy App
- WordPress
- HTTP Request Viewer

### Hello Wasm

まずは、Rust で作られている Hello World サンプルを見てみます。

次のエンドポイントにアクセスします。

- <http://localhost:8080/hello-wasm>

このように表示されていれば、動作しています。

![](https://storage.googleapis.com/zenn-user-upload/04b610b405e3-20221216.png)

このアプリケーションコードは、以下をみると分かるように標準出力をしているだけのものになります。

https://github.com/vmware-labs/mod_wasm/blob/main/examples/rust-src/hello_wasm/src/main.rs

### PHP Hello

この **PHP Hello** には、次のエンドポイントからアクセスします。

- <http://localhost:8080/php-hello/>

これは、`phpinfo()` を呼び出し表示するだけのシンプルなアプリケーションです。

https://github.com/vmware-labs/mod_wasm/blob/main/examples/wasm_modules/php-scripts/php-hello/index.php

![](https://storage.googleapis.com/zenn-user-upload/d809a74501ed-20221216.png)

### PrettyFy App

**PrettyFy App** は、`uploads` ディレクトリに置かれている静的ファイルを URL パラメータで指定し画面表示するものです。

まず、以下のエンドポイントにアクセスすると `uploads` ディレクトリにあるファイル一覧が表示されます。
- <http://localhost:8080/prettyfy>

![](https://storage.googleapis.com/zenn-user-upload/bad110da3b1b-20221216.png)

それらのファイルを `?file=` パラメータで指定して表示を行います。

- <http://localhost:8080/prettyfy?file=uploaded_text.txt>

![](https://storage.googleapis.com/zenn-user-upload/68ff98ab8ffb-20221216.png)

- <http://localhost:8080/prettyfy?file=cgi_hello_python.py>

![](https://storage.googleapis.com/zenn-user-upload/f5f822904350-20221216.png)

### WordPress

これは、文字通り PHP インタプリタの WebAssembly ビルド上で動作する **WordPress** です。

- <http://localhost:8080/wordpress/>

https://github.com/vmware-labs/mod_wasm/tree/main/examples/wasm_modules/php-scripts/wordpress-patch

https://github.com/vmware-labs/mod_wasm/blob/main/examples/wasm_modules/php-scripts/wordpress-patch/wp-includes/blocks.php

https://github.com/vmware-labs/mod_wasm/blob/main/examples/wasm_modules/php-scripts/wordpress-patch/wp-includes/functions.php

https://github.com/vmware-labs/mod_wasm/blob/main/examples/wasm_modules/php-scripts/wordpress-patch/wp-content/db.php

次の `Dockerfile` の箇所を見てもらうと分かるように、特殊なことをしているわけではなく WebAssembly のPHP ランタイム上で WordPress を動かしているのです。

```dockerfile
RUN mkdir -p /usr/local/apache2/htdocs/wordpress
COPY --from=builder-demos /tmp/wordpress /usr/local/apache2/htdocs/wordpress
COPY ./examples/wasm_modules/php-scripts/wordpress-patch/ /usr/local/apache2/htdocs/wordpress
RUN chmod -R 777 /usr/local/apache2/htdocs/wordpress/wp-content/database
```
![](https://storage.googleapis.com/zenn-user-upload/f04ab6b75656-20221216.png)

## Day 89 のまとめ

