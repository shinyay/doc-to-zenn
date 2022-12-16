---
title: "100日後にRustをちょっと知ってる人になる: [Day 89]mod_wasm サンプルアプリケーションの実行"
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

## Dockerfile で準備する mod_wasm 環境

![](https://storage.googleapis.com/zenn-user-upload/dcb8451237e7-20221214.png)

Dockerfile の中では、**mod_wasm.so** と **libwasm_runtime.so** をそれぞれビルドして準備をしているのが分かります。

```dockerfile
################################################################################
# [`wasm_runtime.so` Builder]
################################################################################
FROM $IMAGE_REPOSITORY/library/rust:1.65.0-slim as builder-wasm_runtime.so
ARG WASM_RUNTIME_PATH=/usr/src/wasm_runtime
RUN apt-get update && apt-get install make
WORKDIR $WASM_RUNTIME_PATH
COPY ./wasm_runtime ./
ENV CARGO_UNSTABLE_SPARSE_REGISTRY=true
RUN rustup update nightly
RUN cargo +nightly -Z sparse-registry install cbindgen
RUN make clean_all
RUN make all
```

```dockerfile
################################################################################
# [`mod_wasm.so` Builder]
################################################################################
FROM $IMAGE_REPOSITORY/library/httpd:2.4 as builder-mod_wasm.so
ARG WASM_RUNTIME_PATH=/usr/src/wasm_runtime
ARG MOD_WASM_PATH=/usr/src/mod_wasm
ARG DIST_DIR=$MOD_WASM_PATH/dist
RUN apt-get update && apt-get install apache2-dev build-essential pkg-config libtool libapr1-dev libaprutil1-dev make gcc libtool-bin libxml2-dev libpcre2-dev subversion pkg-config -y
WORKDIR $MOD_WASM_PATH
COPY ./mod_wasm $MOD_WASM_PATH
COPY ./dist $DIST_DIR
COPY --from=builder-wasm_runtime.so $WASM_RUNTIME_PATH/target/release/libwasm_runtime.so $WASM_RUNTIME_PATH/target/release/libwasm_runtime.so
COPY --from=builder-wasm_runtime.so $WASM_RUNTIME_PATH/include/ $WASM_RUNTIME_PATH/include/
RUN mkdir -p $MOD_WASM_PATH/dist/conf $DIST_DIR/modules
RUN HTTPD_DIR=/usr/local/apache2 ./build.sh
```

## Day 89 のまとめ

今回は、[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087) で紹介していた **mod_wasm** のサンプルアプリケーションの実行について見てみました。Dockerfile の構成を見てもらうと分かるように、**mod_wasm** を構成する 2 つのモジュール `wasm_runtime.so` と `mod_wasm.so` があれば、簡単に WebAssembly モジュールを動かすことができるようになる事が分かると思います。
自分で作った WebAssembly モジュールの動作をサーバサイドで試してみようと、このサンプル動作をみて僕も思っています。
