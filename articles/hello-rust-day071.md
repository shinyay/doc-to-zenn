---
title: "100日後にRustをちょっと知ってる人になる: [Day 71]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 71 のテーマ

[Day 70](https://zenn.dev/shinyay/articles/hello-rust-day068) で、**Cargo.toml** を編集して依存関係を管理する **[cargo-edit](https://github.com/killercup/cargo-edit)** の使い方を見てみました。以下のような `cargo` のサブコマンドが追加されて、依存関係の管理・編集を行うことができました。

- `cargo add`
- `cargo rm`
- `cargo upgrade`
- `cargo set-version`

ところで、`cargo upgrade` を使って依存関係のバージョンを最新化することができましたが、現在使っている依存関係が古くなっているかどうか調べるにはどうしたらいいでしょうか。
そのような時に役立ちそうなのが、**cargo-outdated** です。

## cargo-outdated

cargo-outdatedは、依存関係に新しいバージョンがある場合に表示するためのものです。

- [cargo-outdated](https://github.com/kbknapp/cargo-outdated)

## Day 71 のまとめ
