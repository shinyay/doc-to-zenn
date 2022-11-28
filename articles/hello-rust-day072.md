---
title: "100日後にRustをちょっと知ってる人になる: [Day 72]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 72 のテーマ

この数日間、`cargo` のサブコマンドについて見てきました。コードの整形や Cargo.toml の編集など開発時に便利なものがありました。一方で運用時を見据えたことなども気になって来ますよね。最近では、**シフトレフト** など DevOps の文脈で言われて、従来後続フェーズで行っていたような作業を予め早い段階で実施することで品質をあげるというような取り組みです。
そこで気になってくるのは、サードパーティ製クレートなどに含まれる脆弱性ではないでしょうか。そんな心配におすすめな `cargo` のコマンドがありました。それが **cargo audit** です。

## RustSec - The Rust Security Advisory Database

Rust は比較的セキュアだと言語の特徴としても語られていることは聞いたことがあると思います。とはいえ、100 % 安全なものはないので Rust であっても当然ながら脆弱性のあるものは提供されてしまいます。そのような Rust で発見された脆弱性情報を公開しているのが **RustSec** (Rust Security Advisory Database) なのです。

- [RustSec - Rust Security Advisory Database](https://rustsec.org/advisories/)

![](https://storage.googleapis.com/zenn-user-upload/80c77163f988-20221128.png)

この脆弱性情報リポジトリは、[Rust Secure Code ワーキンググループ](https://www.rust-lang.org/governance/wgs/wg-secure-code)によってメンテナンスされています。

ここで提供されている脆弱性情報をもとに脆弱性チェックを行ってくれるコマンドが `cargo audit` です。

## cargo-audit

**cargo-audit** は **rustsec** 配下のリポジトリで公開されています。

- [rustsec/rustsec](https://github.com/RustSec/rustsec/tree/main/cargo-audit#rustsec-cargo-audit)

### インストール

それでは、この `cargo audit` コマンドをインストールしてみます。

```shell
cargo install cargo-audit
```

```shell
$ cargo --list

Installed Commands:
    add                  Add dependencies to a Cargo.toml manifest file
    audit
    b                    alias: build
    bench                Execute all benchmarks of a local package
    :
```

```shell
$ cargo audit --help

cargo-audit-audit
Audit Cargo.lock files for vulnerable crates

USAGE:
    cargo-audit audit [OPTIONS] [SUBCOMMAND]

OPTIONS:
    -c, --color <COLOR>                color configuration: always, never (default: auto)
    -d, --db <DB>                      advisory database git repo path (default:
                                       ~/.cargo/advisory-db)
    -D, --deny <DENY>                  exit with an error on: warnings (any), unmaintained, unsound,
                                       yanked
    -f, --file <FILE>                  Cargo lockfile to inspect (or `-` for STDIN, default:
                                       Cargo.lock)
    -h, --help                         output help information and exit
        --ignore <ADVISORY_ID>         Advisory id to ignore (can be specified multiple times)
        --ignore-source                Ignore sources of packages in Cargo.toml, matching advisories
                                       regardless of source
        --json                         Output report in JSON format
    -n, --no-fetch                     do not perform a git fetch on the advisory DB
    -q, --quiet                        Avoid printing unnecessary information
        --stale                        allow stale database
        --target-arch <TARGET_ARCH>    filter vulnerabilities by CPU (default: no filter)
        --target-os <TARGET_OS>        filter vulnerabilities by OS (default: no filter)
    -u, --url <URL>                    URL for advisory database git repo
        --version                      output version and exit

SUBCOMMANDS:
    bin     scan compiled binaries
    help    Print this message or the help of the given subcommand(s)
```
## Day 72 のまとめ
