---
title: "100日後にRustをちょっと知ってる人になる: [Day 58]Fermyon Cloud へのデプロイとアップグレード"
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

## Fermyon Cloud デプロイの仕組み

先の OSS プロジェクトリストを見ると、詳しいかたはピンときたかもしれません。
Fermyon Cloud では、**[Bindle](https://github.com/deislabs/bindle)** を用いて Spin アプリケーションの**パッケージ化**と**デプロイ**を行っています。

### Bindle とは

公式な説明として、**集約オブジェクトストレージシステム (Aggregate Object Storage System)** と言われています。

これだけだとなかなかよく分からないですよね。
例えば、スプーンやフォーク、おはしなどを探そうとする時に、別々のところは探さないですよね。同じところを探すと思います。このように、関連したアイテムをまとめて保管しておくことが、集約オブジェクトストレージシステムの考え方になります。

Bindle では、保管する対象のオブジェクトを **コレクション** として保管します。

Bindle の仕組みを理解するためには、構成する次のパーツを知っておく必要があります。

- **パーセル (parcel)**
  - 関連するデータの入れもの。単一のバイナリの場合もあれば、数百もの個別なデータオブジェクト (画像、ドキュメント、実行バイナリ など) の場合もあり、何が含まれるかは問いません。
- **インボイス (invoice)**
  - 関連付けられたパーセルのセットをリストするドキュメント
  - `invoice.toml` として記載する

Bindle は 1 つ以上のパーセルとインボイスを含んで構成します。
そして、この Bindle は一度構成されると不変なものとして管理されるため、上書きすることはできません。
Bindle は各パッケージにバージョンを付けて区別をおこないます。

### Fermyon Cloud でのデプロイプロセス

繰り返しになりますが、Fermyon Cloud は Fermyon Platform 上に構成されています。つまり、Bindle インスタンスをホストしています。よって、`spin deploy` コマンドを実行すると Bindle を使った処理が裏で実行されます。

- アプリケーションのパッケージングと Fermyon Cloud へのアップロード
- アプリケーションの作成とアップグレード

#### アプリケーションのパッケージングとアップロード

まず、全てのファイルをパッケージ化して、インボイスの生成が行われます。
Bindle は `spin.toml` を使用します。

- 名前
- バージョン
- ビルド文字列
など

```toml
spin_version = "1"
authors = ["shinyay <shinyay@abc.xyz>"]
description = "Sping Getting Started"
name = "hello-rust"
trigger = { type = "http", base = "/" }
version = "0.1.0"
```

パッケージング後、不変なオブジェクトとして扱われ Fermyon Cloud にアップロードされます。

#### アプリケーションの作成とアップグレード

Fermyon Cloud のアプリケーションは複数のリビジョンを持つことができ、それらはチャンネルに関連付けられます。
アプリケーションをデプロイすると、チャンネル、リビジョンの両方が Fermyon Cloud に作成されます。

アプリケーションがすでに存在する場合は、アップグレードが行われます。
新しいリビジョンが作成され、これが正常であると判断されるとすぐに、トラフィックは新しいリビジョンにルーティングし始めます。

## Fermyon Cloud へのデプロイとアップグレード

あらためて、Fermyon Cloud へのデプロイとアップグレードを試してみたいと思います。

### デプロイ

まず、Fermyon Cloud にログインします。

```shell
spin login
```

次に、`spin.toml` が配置されているディレクトリからデプロイを行います。

```shell
spin deploy

Uploading hello-fermyon-cloud version 0.1.0+XXXXXXXX...
Deploying...
Waiting for application to become ready...... ready
Available Routes:
  hello-fermyon-cloud: https://hello-fermyon-cloud-XXXXXXXX.fermyon.app/hello
```

![](https://storage.googleapis.com/zenn-user-upload/a52e57c26bcf-20221029.png)

### アップグレード

次にアップグレードを行います。

バージョンを書き換えた `spin.toml` を用意し、デプロイし直すことによりアップグレードが行えます。

変更前:

```toml
version = "0.1.0"
```

変更後:

```toml
version = "0.1.1"
```

修正した後、改めて `spin deploy` コマンドを実行します。

```shell
spin deploy

Uploading hello-fermyon-cloud version 0.1.1+XXXXXXXX...
Deploying...
Waiting for application to become ready... ready
Available Routes:
  hello-fermyon-cloud: https://hello-fermyon-cloud-XXXXXXXX.fermyon.app/hello
```

バージョンが上がりました。またアクセスする URL には変更がないということも確認ができました。

![](https://storage.googleapis.com/zenn-user-upload/4807cb6a1376-20221029.png)

## Day 58 のまとめ

Fermyon Cloud へのアプリケーションのデプロイの仕組みについて少し詳しく見てみました。
また、デプロイ済のアプリケーションのアップグレードも行いました。

デプロイに関して使われている技術は、**Bindle** ですが、一切その Bindle にふれることなく処理を行えたことはデプロイの流れを通して分かったと思います。
