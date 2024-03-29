---
title: "100日後にRustをちょっと知ってる人になる: [Day 71]依存関係管理: cargo-outdated"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 71 のテーマ

[Day 70](https://zenn.dev/shinyay/articles/hello-rust-day070) で、**Cargo.toml** を編集して依存関係を管理する **[cargo-edit](https://github.com/killercup/cargo-edit)** の使い方を見てみました。以下のような `cargo` のサブコマンドが追加されて、依存関係の管理・編集を行うことができました。

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

しばらくすると、`outdated` サブコマンドが追加されています。

```shell
$ cargo --list

Installed Commands:
    add                  Add dependencies to a Cargo.toml manifest file
    b                    alias: build
    bench                Execute all benchmarks of a local package
    :
    outdated
    :
```

## 動作確認

以下のように古いバージョンをしていた依存関係を追加してみます。

```toml
[package]
name = "day_71_cargo-outdated"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
clap = "1.0.0"
```

ちなみに、この `clap` は、今日時点で最新バージョンは `4.0.27` です。

- [clap](https://crates.io/crates/clap)

では、実行をおこなってみます。

```shell
$ cargo outdated

Name             Project  Compat  Latest   Kind    Platform
----             -------  ------  ------   ----    --------
clap             1.3.2    ---     4.0.27   Normal  ---
clap->ansi_term  0.6.3    ---     Removed  Normal  ---
clap->strsim     0.4.1    ---     0.10.0   Normal  ---
```

最新バージョンについて表示がおこなれました。これを参考にバージョン指定をすることができそうですよね。

## Day 71 のまとめ

`cargo upgrade` コマンドにより毎回依存関係のメンテナスをし続けていれば、依存関係の対応バージョンの整合性が合わなくなることはなと思います。とはいえ、毎回アップグレードし続けるのも難しい場合はあると重いmす。例えば、GitHub リポジトリを `git clone` してくるような場合だと、たしかに古いバージョンになっていると思います。
そのような時に、この `git outdated` を実行して依存関係の最新バージョンの確認をしてみるのは望ましいのではないかなって思いました。