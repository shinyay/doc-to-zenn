---
title: "100日後にRustをちょっと知ってる人になる: [Day 56]はじめての Fermyon Cloud"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: false
---
## Day 56 のテーマ

今日は2022年10月25日、ということで日本時間の昨夜未明から KubeCon + CloudNativeCon とそれの関連開催の各種カンファレンスがアメリカのデトロイトで始まりました。
昨晩はまだ KubeCon + CloudNativeCon 本体は開催されていなかったのですが、関連開催のいくとかのカンファレンスの中からぼくは **[Cloud Native Wasm Day](https://events.linuxfoundation.org/cloud-native-wasm-day-north-america/)** を見ていました。
文字通り、Wasm、WebAssembly 関連の発表があったわけなのですが、その中には先日も少し記事化していた **Wasm Workers Server** を提供している VMware からの発表もありました。
ですが、今回一番ぼくが関心を持ったのは、正確には以前から持っていたのは、**Fermyon** (日本語的にはフェルミオンと発音) の各種発表でした。中でも **Fermyon Cloud** の発表は、ついにやってきましたね、という感じでした。

というわけで、今日は はじめての Fermyon Cloud 、という感じで触ってみたいと思います。

## Fermyon Cloud の前に

WebAssembly アプリケーションの実行環境としての **Fermyon Cloud** の前に、本来だったら Fermyon が提供している次のプロジェクトを説明しておく必要があのです。

- ✅ **Spin**
- ✅ **Fermyon Platform**

今日はそれを一旦スキップして、WebAssembly アプリケーションをビルド＆デプロイして動作する流れを紹介したいと思います。

### Spin

**Spin** は、一言で説明するならば、**WebAssembly** を使用して、アプリケーションを構築、デプロイ、実行するためのフレームワークである、といえます。
また、**Spin** は、アプリケーションの作成、配布、実行を支援する CLI を提供しています。

この **Spin** の導入の仕方や使い方などは、また今度。

### Fermyon Platform

**Fermyon Platform** は、**Spin** によるアプリケーションや、その他の互換性のある **WebAssembly** ワークロードをホストするためのプラットフォームです。

Fermyon は 動作する際につぎのソリューションを使用しています:

- [Nomad](https://www.nomadproject.io/)
- [Consul](https://consul.io/)
- [Bindle](https://github.com/deislabs/bindle)
- [Traefik](https://doc.traefik.io/traefik/)
- [Hippo](https://github.com/deislabs/hippo)

この **Fermyon Platform** についても、また今度。

## Fermyon Cloud

**Spin** をリリースした日に次のような質問があったそうです。

> ホスティングサービスはありますか？Spinはすごいと思うけど、自分でサーバーを管理したくないんです。

開発者が自分のインフラをセットアップする必要がなくなると、もっと楽しい経験をすることができるはずだ、というモチベーションから **Fermyon Cloud** は生まれたそうです。

**Fermyon Cloud** は、**Spin** による Webアプリケーションを実行するためのプラットフォームです。
また、**Fermyon Cloud** のダッシュボードにログインして、アプリケーションの確認、ログファイルの閲覧、デプロイメントの管理を行うことができます。

この **Fermyon Cloud** が **Spin** アプリケーションを動作させるというところから想像できると思いますが、**Fermyon Cloud** は **Fermyon Platform** の上に構築されています。

- リリース管理: **Bindle**
- スケジューリング: **Nomad**
など

## Fermyon Cloud へのアプリケーションデプロイ

繰り返しますが、**Spin** についての詳細な説明は今回はしませんので、そういうものだと思ってください。

### 0. テンプレートの取得

初めて Spin を使う場合、プロジェクトテンプレートが存在しないので、取得を行います。

```shell
spin templates install --git https://github.com/fermyon/spin
```

## Day 56 のまとめ
