---
title: "100日後にRustをちょっと知ってる人になる: [Day 15]dev container"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 15 のテーマ

Day 14 では **GitHub Codespaces** で Rust 環境を作ることにチャレンジしてみました。
昨日の結果として分かったことは次の２つでした。

- Codespaces で提供されるデフォルトのコンテナ環境には Rust のランタイム環境が入っていないということ
- **[dev container](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/introduction-to-dev-containers)** という仕組みを使ってランタイム環境をカスタマイズできるということ

というわけで、今日は **dev container** を使って Rust 環境を作ろうと思います。

## Day 15 のまとめ
