---
title: "100日後にRustをちょっと知ってる人になる: [Day 88]Wasm Workers Server 0.6.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust, webassembly, wasm]
published: false
---
## Day 88 のテーマ

[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087) では、Rust を用いて開発された WebAssebmly を Apache HTTP Server で動作させるための **mod_wasm** について見てみました。そこでも紹介したように、mod_wasm は **VMware Wasm Labs** が公開しているオープンソースです。また、記事の中でも触れましたが [Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) で紹介をした **Wasm Workers Server** も同じく **VMware Wasm Labs** が公開しているオープンソースの WebAssembly をサーバーレスとして動作させる実行環境でした。

ふと、この **Wasm Workers Server** のリポジトリを見ていると、ぼくが使用しているバージョンから上がっていたので今日はそのアップデートについて見てみたいかなと思います。



## Day 88 のまとめ
