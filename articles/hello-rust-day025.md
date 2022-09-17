---
title: "100日後にRustをちょっと知ってる人になる: [Day 25]cargo-generate"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---

## Day 25 のテーマ

Rust で開発を行うときに、**Cargo** は必須の CLI ですよね。それだけでもとても便利ですけど、`cargo install](https://doc.rust-lang.org/cargo/commands/cargo-install.html` で、[crates.io](https://crates.io/) からバイナリクレートをローカルにインストールして、もっと便利にすることもできます。

- [cargo install](https://doc.rust-lang.org/cargo/commands/cargo-install.html)

ちなみに、バイナリクレートとは、`src/main.rs` やバイナリとして指定された他のファイルをもつ場合に生成される **実行可能なプログラム**のことです。

[Day 21](https://zenn.dev/shinyay/articles/hello-rust-day021) でインストールした、WebAssembly 用のサブコマンドな `cargo-wasi` も `cargo install` でインストールしましたね。

```shell
cargo install cargo-wasi
```

:::details 参考までに今現在インストールされているサブコマンド
```shell
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
:::

このように、**Cargo** をより便利にしていくことができそうなので、いろいろとバイナリクレートを探していたりします。

今日は、この数日 **Rust** + **WebAssembly** をいろいろと見ているので、役に立ちそうな **Cargo Generate** をインストールして使ってみようと思います。

## Cargo Generate

Cargo Generate は、Rust プロジェクトのテンプレートとして Git レポジトリで管理されているものを利用して、Rust の新規プロジェクトを作成することができます。

- [Cargo Generate Documentation](https://cargo-generate.github.io/cargo-generate/index.html)
  - [Cargo Generate GitHub Repo](https://github.com/cargo-generate/cargo-generate)

## Day 25 のまとめ
