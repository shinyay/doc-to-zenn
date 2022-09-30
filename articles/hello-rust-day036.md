---
title: "100日後にRustをちょっと知ってる人になる: [Day 36]はじめての Web フレームワーク"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 36 のテーマ

[Day 35](https://zenn.dev/shinyay/articles/hello-rust-day035) では、非同期処理の動きをみようと思い Web サーバを作ってみました。昨日の時点ではシングルスレッドの Web サーバでしたが公式ドキュメントの方では、あの実装からスレッドプールを実装しマルチスレッドにしたサーバの説明が行われていました。

- [シングルスレッド・サーバーをマルチスレッド・サーバーにする](https://doc.rust-lang.org/book/ch20-02-multithreaded.html)

このドキュメントに沿えばマルチスレッド化できます。コードの説明は丁寧に行われれているのですが、コンパイルエラーを見ながら、コードを実装していくという流れになっているので少し読みにくいかもしれませんけれど。

さて、Web サーバを作ってみたりしましたが、実際は自分で Web サーバを書き上げることはきっとしないですよね。車輪の再発明のようなことになりますよね。
例えば、Java のアプリケーションを思い浮かべてみると、サーバ用コンポーネントになる [Apache Tomcat](https://tomcat.apache.org/) を自分で実装する人はいないですよね。多くの人は Web フレームワークの [Spring Boot](https://spring.io/projects/spring-boot) を使って**組み込み Tomcat** を使ったりする人が多いのではないでしょうか。

Java と同様に Rust にも Web フレームワークがあります。ただ、Java の **Spring** のようなデファクトと言えるものはまだ確立されていないように見えます。ということで、ぼくの観測範囲で見つけている Rust の Web フレームワークを紹介します。

## Rust Web フレームワーク

アクティブなプロジェクトや、非アクティブなプロジェクトもあると思いますが次のようなフレームワークがあります。
(全量の中からはまだまだ１部分のはず)

|名称|公式サイト|GitHubリポジトリ|ドキュメント|
|---|--------|---------------|----------|
|actix-web|https://actix.rs/|https://github.com/actix/actix-web|https://docs.rs/actix-web/latest/actix_web/|
|rocket|https://rocket.rs/|https://github.com/SergioBenitez/rocket|https://rocket.rs/v0.5-rc/guide/introduction/|
|||||
|||||
|||||
|||||
|||||
|||||
|||||
|||||
|||||


## Day 36 のまとめ
