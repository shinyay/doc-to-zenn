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

確認するとインストールされています。

```shell
$ cargo --list

Installed Commands:
    add                  Add dependencies to a Cargo.toml manifest file
    audit
    b                    alias: build
    bench                Execute all benchmarks of a local package
    :
```

以下が `cargo audit`　のヘルプです。

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

### 実行サンプル

RustSec で最近公開されていた次の脆弱性のクレートを意図的に追加してみます。

- [RUSTSEC-2022-0066: Denial of Service from unchecked request length](https://rustsec.org/advisories/RUSTSEC-2022-0066.html)

脆弱性の内容にはここでは振れませんが、**[conduit-hyper](https://crates.io/crates/conduit-hyper)** に関する脆弱性で、バージョン `0.4.2` 以前のものが対象にリスクが発生します。

そこで、次のように依存関係を **Cargo.toml** に追加してみました。

```toml
[dependencies]
conduit-hyper = "0.1.3"
```

ここで、`cargo audit` を実行してみます。すると対象のクレートの依存関係に関連した依存関係ツリーも同時に表示されます。

```text
$ cargo audit

    Fetching advisory database from `https://github.com/RustSec/advisory-db.git`
      Loaded 470 security advisories (from /Users/yanagiharas/.cargo/advisory-db)
    Updating crates.io index
    Scanning Cargo.lock for vulnerabilities (95 crate dependencies)
Crate:     hyper
Version:   0.12.36
Title:     Integer overflow in `hyper`'s parsing of the `Transfer-Encoding` header leads to data loss
Date:      2021-07-07
ID:        RUSTSEC-2021-0079
URL:       https://rustsec.org/advisories/RUSTSEC-2021-0079
Solution:  Upgrade to >=0.14.10
Dependency tree:
hyper 0.12.36
└── conduit-hyper 0.1.3
    └── day_72_cargo-audit 0.1.0

Crate:     hyper
Version:   0.12.36
Title:     Lenient `hyper` header parsing of `Content-Length` could allow request smuggling
Date:      2021-07-07
ID:        RUSTSEC-2021-0078
URL:       https://rustsec.org/advisories/RUSTSEC-2021-0078
Solution:  Upgrade to >=0.14.10

Crate:     regex
Version:   0.1.80
Title:     Regexes with large repetitions on empty sub-expressions take a very long time to parse
Date:      2022-03-08
ID:        RUSTSEC-2022-0013
URL:       https://rustsec.org/advisories/RUSTSEC-2022-0013
Solution:  Upgrade to >=1.5.5
Dependency tree:
regex 0.1.80
└── semver-parser 0.6.2
    └── semver 0.5.1
        ├── conduit-hyper 0.1.3
        │   └── day_72_cargo-audit 0.1.0
        └── conduit 0.8.1
            └── conduit-hyper 0.1.3

Crate:     thread_local
Version:   0.2.7
Title:     Data race in `Iter` and `IterMut`
Date:      2022-01-23
ID:        RUSTSEC-2022-0006
URL:       https://rustsec.org/advisories/RUSTSEC-2022-0006
Solution:  Upgrade to >=1.1.4
Dependency tree:
thread_local 0.2.7
└── regex 0.1.80
    └── semver-parser 0.6.2
        └── semver 0.5.1
            ├── conduit-hyper 0.1.3
            │   └── day_72_cargo-audit 0.1.0
            └── conduit 0.8.1
                └── conduit-hyper 0.1.3

Crate:     time
Version:   0.1.45
Title:     Potential segfault in the time crate
Date:      2020-11-18
ID:        RUSTSEC-2020-0071
URL:       https://rustsec.org/advisories/RUSTSEC-2020-0071
Solution:  Upgrade to >=0.2.23
Dependency tree:
time 0.1.45
└── hyper 0.12.36
    └── conduit-hyper 0.1.3
        └── day_72_cargo-audit 0.1.0

Crate:     tokio
Version:   0.1.22
Title:     Data race when sending and receiving after closing a `oneshot` channel
Date:      2021-11-16
ID:        RUSTSEC-2021-0124
URL:       https://rustsec.org/advisories/RUSTSEC-2021-0124
Solution:  Upgrade to >=1.8.4, <1.9.0 OR >=1.13.1
Dependency tree:
tokio 0.1.22
└── hyper 0.12.36
    └── conduit-hyper 0.1.3
        └── day_72_cargo-audit 0.1.0

Crate:     net2
Version:   0.2.38
Warning:   unmaintained
Title:     `net2` crate has been deprecated; use `socket2` instead
Date:      2020-05-01
ID:        RUSTSEC-2020-0016
URL:       https://rustsec.org/advisories/RUSTSEC-2020-0016
Dependency tree:
net2 0.2.38
├── miow 0.2.2
│   └── mio 0.6.23
│       ├── tokio-tcp 0.1.4
│       │   └── hyper 0.12.36
│       │       └── conduit-hyper 0.1.3
│       │           └── day_72_cargo-audit 0.1.0
│       ├── tokio-reactor 0.1.12
│       │   ├── tokio-tcp 0.1.4
│       │   ├── tokio 0.1.22
│       │   │   └── hyper 0.12.36
│       │   └── hyper 0.12.36
│       └── tokio 0.1.22
├── mio 0.6.23
└── hyper 0.12.36

error: 6 vulnerabilities found!
warning: 1 allowed warning found
```

## 脆弱性の修正: fix フィーチャー

このように発見された脆弱性の修正を実施する機能を、現時点では正式公開していませんが実験的機能として `fix` フィーチャーを提供しています。
以下のコマンドでインストールを行ってみます。

```shell
cargo install cargo-audit --features=fix
```

## Day 72 のまとめ
