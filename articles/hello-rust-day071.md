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

Cargo.toml でのバージョン指定は、SemVer (セマンティックバージョニング) です。この指定するバージョンですが、**npm** のバージョン記述で使用する `^`(キャレット)と同じ様に扱われます。つまり、以下のようにバージョンが `0.1.0` と指定されている場合は、範囲としては **0.1.0 以上、0.2.0 未満**となり、この範囲で新しいバージョンになっていれば、`cargo update` で最新バージョンが洗濯されます。

```toml
[dependencies]
toml = "0.1.0"
```

しかし、`0.2.0` よりも新しいバージョンが出ている場合だと検索にひっかからずに最新の依存関係へのアップデートが行われません。
そこで、`cargo outdated` を実行することで新しいバージョンが公開されているかどうかを確認することが可能になります。

## インストール

以下のコマンドでインストールを行います。

```shell
cargo install --locked cargo-outdated
```


## Day 71 のまとめ
