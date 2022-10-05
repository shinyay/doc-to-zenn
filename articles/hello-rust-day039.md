---
title: "100日後にRustをちょっと知ってる人になる: [Day 39]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 39 のテーマ

[Day 38](https://zenn.dev/shinyay/articles/hello-rust-day038) では Web フレームワークを構成する非同期処理ランタイムについて調べました。そして次のようなクレートが様々なフレームワークのベースとして使われていました。

- **[tokio](https://tokio.rs/)**
- **[async-std](https://book.async.rs/)**
- **[hyper](https://hyper.rs/)**

今日はこれらの非同期処理クレートについて確認してみようと思います。

## hyper

- **[hyper](https://hyper.rs/)**

まず最初に **hyper** は実際は非同期処理のクレートではありませんでした。非同期処理ランタイムと組み合わせて動作させる 非同期、Multipart 対応の　HTTP/HTTP2 のクライアント/サーバ用の **低レベル**な機能を提供するクレートです。

### 特徴

✅ Web サービスと対話するためのクライアント
✅ Web サービスを構築するためのサーバ
✅ "超"高速
✅ ノンブロッキング・ソケットによる並行性
✅ HTTP/1 および HTTP/2 のサポート

### 使い方

まず **hyper** のクレートのバージョンを確認します。

- [crates.io](https://crates.io/crates/hyper/versions)

![](https://storage.googleapis.com/zenn-user-upload/413ca7a25887-20221005.png)

'Cargo.toml' に依存関係を追加します。

```toml
[dependencies]
hyper = { version = "0.14.20", features = ["full"] }
```

## tokio

- **[tokio](https://tokio.rs/)**

## async-std

- **[async-std](https://book.async.rs/)**

## Day 39 のまとめ
