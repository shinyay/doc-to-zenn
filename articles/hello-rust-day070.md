---
title: "100日後にRustをちょっと知ってる人になる: [Day 70]依存関係管理: cargo-edit"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 70 のテーマ

この数日間見ているのが、**[Blessed.rs](https://blessed.rs/crates)** です。Rust 開発に役立つ様々なクレートを紹介しているサイトなのです。

![](https://storage.googleapis.com/zenn-user-upload/0b4e496ba2fb-20221124.png)

今日もこちらで紹介されているものを取りあてみたいと思います。

## cargo-edit

今日チェックしたいのが、**依存関係管理ツール**として紹介されている、**cargo-edit** です。名前から分かるように、`cargo` を拡張してサブコマンドとして機能を追加します。
コマンドラインから、**Cargo.toml** を変更し、**依存関係の追加**や**削除**、また**アップグレード**を可能とします。

というわけで、`cargo-edit` をインストールするまえに、現在の `cargo` のサブコマンドリストを見ておきます。

```text
$ cargo --list

Installed Commands:
    add                  Add dependencies to a Cargo.toml manifest file
    b                    alias: build
    bench                Execute all benchmarks of a local package
    build                Compile a local package and all of its dependencies
    c                    alias: check
    check                Check a local package and all of its dependencies for errors
    clean                Remove artifacts that cargo has generated in the past
    clippy               Checks a package to catch common mistakes and improve your Rust code.
    config               Inspect configuration values
    d                    alias: doc
    doc                  Build a package's documentation
    fetch                Fetch dependencies of a package from the network
    fix                  Automatically fix lint warnings reported by rustc
    fmt                  Formats all bin and lib files of the current crate using rustfmt.
    generate
    generate-lockfile    Generate the lockfile for a package
    git-checkout         This subcommand has been removed
    help                 Displays help for a cargo subcommand
    init                 Create a new cargo package in an existing directory
    install              Install a Rust binary. Default location is $HOME/.cargo/bin
    locate-project       Print a JSON representation of a Cargo.toml file's location
    login                Save an api token from the registry locally. If token is not specified, it will be read from stdin.
    logout               Remove an API token from the registry locally
    metadata             Output the resolved dependencies of a package, the concrete used versions including overrides, in machine-readable format
    miri
    new                  Create a new cargo package at <path>
    owner                Manage the owners of a crate on the registry
    package              Assemble the local package into a distributable tarball
    pkgid                Print a fully qualified package specification
    publish              Upload a package to the registry
    r                    alias: run
    read-manifest        Print a JSON representation of a Cargo.toml manifest.
    report               Generate and display various kinds of reports
    run                  Run a binary or example of the local package
    rustc                Compile a package, and pass extra options to the compiler
    rustdoc              Build a package's documentation, using specified custom flags.
    search               Search packages in crates.io
    t                    alias: test
    test                 Execute all unit and integration tests and build examples of a local package
    tree                 Display a tree visualization of a dependency graph
    uninstall            Remove a Rust binary
    update               Update dependencies as recorded in the local lock file
    vendor               Vendor all dependencies for a project locally
    verify-project       Check correctness of crate manifest
    version              Show version information
    wasi
    yank                 Remove a pushed crate from the index
```

## インストール

それでは、`cargo-edit` をインストールしてみます。

```shell
cargo install cargo-edit
```

インストール後、改めてサブコマンドを確認してみます。

```test
Installed Commands:
    add                  Add dependencies to a Cargo.toml manifest file
    b                    alias: build
    bench                Execute all benchmarks of a local package
    build                Compile a local package and all of its dependencies
    c                    alias: check
    check                Check a local package and all of its dependencies for errors
    clean                Remove artifacts that cargo has generated in the past
    clippy               Checks a package to catch common mistakes and improve your Rust code.
    config               Inspect configuration values
    d                    alias: doc
    doc                  Build a package's documentation
    fetch                Fetch dependencies of a package from the network
    fix                  Automatically fix lint warnings reported by rustc
    fmt                  Formats all bin and lib files of the current crate using rustfmt.
    generate
    generate-lockfile    Generate the lockfile for a package
    git-checkout         This subcommand has been removed
    help                 Displays help for a cargo subcommand
    init                 Create a new cargo package in an existing directory
    install              Install a Rust binary. Default location is $HOME/.cargo/bin
    locate-project       Print a JSON representation of a Cargo.toml file's location
    login                Save an api token from the registry locally. If token is not specified, it will be read from stdin.
    logout               Remove an API token from the registry locally
    metadata             Output the resolved dependencies of a package, the concrete used versions including overrides, in machine-readable format
    miri
    new                  Create a new cargo package at <path>
    owner                Manage the owners of a crate on the registry
    package              Assemble the local package into a distributable tarball
    pkgid                Print a fully qualified package specification
    publish              Upload a package to the registry
    r                    alias: run
    read-manifest        Print a JSON representation of a Cargo.toml manifest.
    report               Generate and display various kinds of reports
    rm
    run                  Run a binary or example of the local package
    rustc                Compile a package, and pass extra options to the compiler
    rustdoc              Build a package's documentation, using specified custom flags.
    search               Search packages in crates.io
    set-version
    t                    alias: test
    test                 Execute all unit and integration tests and build examples of a local package
    tree                 Display a tree visualization of a dependency graph
    uninstall            Remove a Rust binary
    update               Update dependencies as recorded in the local lock file
    upgrade
    vendor               Vendor all dependencies for a project locally
    verify-project       Check correctness of crate manifest
    version              Show version information
    wasi
    yank                 Remove a pushed crate from the index
```

ここで、初見で、おや？？と思ってしまったのが、`cargo edit` みたいなコマンドが追加されるのかと思っていたのです。そうではなくて、[GitHub リポジトリ: cargo-edit](https://github.com/killercup/cargo-edit#cargo-edit) にも書かれているように、追加されるのは次のコマンドでした。

- `cargo add`
- `cargo rm`
- `cargo upgrade`
- `cargo set-version`

これらコマンドを使って、**Cargo.toml** の編集を行ってみたいと思います。

### cargo add

`cargo add` は、文字通りパッケージ追加のためのコマンドです。

まず、ブランクのプロジェクトを作成しました。

```shell
cargo new day_70_cargo-edit
```

当然ながら、以下のように **Cargo.toml** の内容もブランクです。

```toml
[package]
name = "day_70_cargo-edit"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
```

ここに、正規表現のクレートな [regex](https://crates.io/crates/regex) を追加してみます。

```shell
cargo add regex
```

特にバージョンを指定しなくても、最新バージョンを取得してくれるようです。

```shell
    Updating crates.io index
      Adding regex v1.7.0 to dependencies.
             Features:
             + aho-corasick
             + memchr
             + perf
             + perf-cache
             + perf-dfa
             + perf-inline
             + perf-literal
             + std
             + unicode
             + unicode-age
             + unicode-bool
             + unicode-case
             + unicode-gencat
             + unicode-perl
             + unicode-script
             + unicode-segment
             - pattern
             - unstable
             - use_std
```

以下のように、依存関係 **regex** が Cargo.toml に追加されました。

```toml
[package]
name = "day_70_cargo-edit"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
regex = "1.7.0"
```

ところで、バージョンを明示的に指定して依存関係を追加したい場合はどのようにしたらよいでしょうか？
実はこれも簡単で、名前の後に `@バージョン` を付けるのみで対応が出来ます。

```shell
$ cargo add regex@1.6.0

    Updating crates.io index
      Adding regex v1.6.0 to dependencies.
```

```toml
[dependencies]
regex = "1.6.0"
```

また、`cargo add` コマンドで依存関係を追加したときに、フィーチャー一覧が表示されます。このフィーチャーを指定して依存関係の追加を行うことも可能です。
次のように、`--features` オプションをつけてコマンドを実行します。

```shell
cargo add regex --features="unicode"
```

```toml
[dependencies]
regex = { version = "1.6.0", features = ["unicode"] }
```

### cargo upgrade

先の手順サンプルの中で、**regex** のバージョンを古いものに変更してしまいました。そこで、最新バージョンにアップグレードをしたいと思います。その時に使用すコマンドが `cargo upgrade` です。

```shell
cargo upgrade
```

```shell
    Updating 'https://github.com/rust-lang/crates.io-index' index
    Checking day_70_cargo-edit's dependencies
name  old req compatible latest new req
====  ======= ========== ====== =======
regex 1.6.0   1.7.0      1.7.0  1.7.0
   Upgrading recursive dependencies
```

```toml
[dependencies]
regex = { version = "1.7.0", features = ["unicode"] }
```

### cargo rm

では、最後に **Cargo.toml** に追加した依存関係を削除したいと思います。
削除したい依存関係の名前を指定します。

```shell
$ cargo rm regex

    Removing regex from dependencies
```

はい、見事に消えました。

```toml
[package]
name = "day_70_cargo-edit"
version = "0.1.0"
edition = "2021"
```

## Day 70 のまとめ

`cargo` のサブコマンドになる **[cargo-edit](https://crates.io/crates/cargo-edit)** について見てみました。今まで、**Cargo.toml** の編集はエディタを使ってマニュアルで実施していたので、このコマンドはとても便利だと思います。編集だけではなくて、バージョンをメンテナンスしてくれるのも便利ですね。CI を使い始めたら、このような依存関係のアップグレードなどはさらに役立つのではないかなと思いました。

マニュアルで定義ファイルを編集するのは、人為的なミスも発生するリスクがあるので今後はこの `cargo-edit` を使っていきたいなと思います。
