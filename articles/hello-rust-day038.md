---
title: "100日後にRustをちょっと知ってる人になる: [Day 38]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 38 のテーマ

[Day36](https://zenn.dev/shinyay/articles/hello-rust-day036)、 [Day 37](https://zenn.dev/shinyay/articles/hello-rust-day037)と Rust 用の Web フレームワークを見てきました。そして、この Web フレームワークを見始めた理由としては、Rust での非同期処理について学ぼうと考えていたのが発端でした。
フレームワークという見方をかえるとすると、**Rocket** も **actix-web** もいずれも非同期処理の機能を提供するモジュール（クレート）を使用しているということになります。



非同期処理という点では、[Day 34](https://zenn.dev/shinyay/articles/hello-rust-day034) の **Rust 1.64** の特徴を紹介した中で `IntoFuture` による非同期処理についてふれました。その文脈で、非同期処理の仕組みとして `await`/`async` キーワードについて簡単に説明しています。
`async` キーワードを関数に対して宣言することにより、該当の関数を非同期で動作させるというものでした。



## Day 38 のまとめ
