---
title: "100日後にRustをちょっと知ってる人になる: [Day 67]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 67 のテーマ

[Day 66](https://zenn.dev/shinyay/articles/hello-rust-day066) では、クレートをいろいろなカテゴリ別におすすめのもの分類して紹介していくれている **[Blessed.rs](https://blessed.rs/crates)** の紹介を行いました。その、Bleesed.rs の中でも紹介はされていたのですが、今日は少し **lib.rs** について見てみたいと思います。

## lib.rs

![](https://storage.googleapis.com/zenn-user-upload/a02e2455c34e-20221121.png)

- [lib.rs](https://lib.rs/)

Blessed.rs では次の様に lib.rs のことが紹介されています。

> lib.rsはより自動化されたアプローチ（ダウンロード数でクレートを並べる）をとり、また優れた検索機能を備えています。

Blessed.rs では、サイトオーナーの Nico Burns が中心となってクレートの評価と分類が行われていました。一方で、lib.rs はクレートのダウンロード数から**自動的**に人気なものだと判別し公開しているようです。Blessed.rs で紹介されていないクレートなども lib.rs でいち早く見つけることができるかもしれないですね。

lib.rs では次の様なセクションでクレートを表示することができます。

- カテゴリー (Categories)
  - Blessed.rs のように目的・機能別にクレートを表示
- 新着やトレンド (New and Trending)
  - 新規リリースされたり、当月中に注目を集めたクレートを表示
- 人気 (Popular)
  - ダウンロード数順でクレートを表示

それらとは別に統計情報が確認できます。

![](https://storage.googleapis.com/zenn-user-upload/43819c13b63e-20221121.png)

これを見ると、2015 年に Rust 1.0 がリリースされてからのクレートのダウンロード数の推移が確認できます。かなりの勢いで Rust の普及が進んできていることがわかります。年率で 1.9 倍で増えてきていということなので、2023 - 2024 年あたりでは Rust をとりまく世界で何か起こりそうな気がしますね。

## lib.rs でのカテゴリー

さて、それでは Blessed.rs 同様に lib.rs でもどのようなカテゴリー分類がされているかを確認しておきたく思います。

- [Rustパターン](https://lib.rs/rust-patterns)
  - Rust でのプログラミングに特有の状況に対する解決策
- [ネットワークプログラミング](https://lib.rs/network-programming)
  - FTP、HTTP、SSHなどの上位ネットワークプロトコルや、TCP、UDPなどの下位ネットワークプロトコルを扱うクレート
- [データ構造](https://lib.rs/data-structures)
  - 特定の目的のためにデータを整理する特定の方法
- [開発ツール](https://lib.rs/development-tools)
  - テスト、デバッグ、Lint、パフォーマンスプロファイリング、オートコンプリート、フォーマットなど、開発者向けの機能を提供するクレート
- [デバッギング](https://lib.rs/development-tools/debugging)
  - ロギング、トレース、アサーションなど、コードで何が起こっているかを把握するのに役立つクレート
- [ビルドユーティリティ](https://lib.rs/development-tools/build-utils)
  - ビルドスクリプトやその他のビルドステップ用のユーティリティ

## Day 67 のまとめ
