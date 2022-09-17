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

たとえば、[Day 24](https://zenn.dev/shinyay/articles/hello-rust-day024) でプロジェクトを作成するために使用した **create-rust-webpack (rust-webpack-template)** でもプロジェクトテンプレートとして、[rust-webpack-template](rust-webpack-template) を使用していました。
また、[Day 22](https://zenn.dev/shinyay/articles/hello-rust-day022) では、プロジェクトてとして、[wasm-pack-template](https://github.com/rustwasm/wasm-pack-template) が使用されていました。

- [Cargo Generate Documentation](https://cargo-generate.github.io/cargo-generate/index.html)
  - [Cargo Generate GitHub Repo](https://github.com/cargo-generate/cargo-generate)
  - [crates.io](https://crates.io/crates/cargo-generate)

### Cargo Generate のインストール

`cargo install` コマンドでインストールします。

```shell
cargo install cargo-generate
```

:::details 実行結果
```shell
    Updating crates.io index
  Downloaded cargo-generate v0.16.0
  Downloaded 1 crate (86.5 KB) in 0.44s
  Installing cargo-generate v0.16.0
  Downloaded dashmap v5.4.0
  Downloaded git-actor v0.10.1
  Downloaded fastrand v1.8.0
  Downloaded dialoguer v0.10.2
  Downloaded git2 v0.14.4
  Downloaded liquid-derive v0.26.0
  Downloaded home v0.5.3
  Downloaded scopeguard v1.1.0
  Downloaded percent-encoding v2.2.0
  Downloaded hex v0.4.3
  Downloaded bitflags v1.3.2
  Downloaded dirs-sys v0.3.7
  Downloaded minimal-lexical v0.2.1
  Downloaded regex-automata v0.1.10
  Downloaded idna v0.3.0
  Downloaded os_str_bytes v6.3.0
  Downloaded bstr v0.2.17
  Downloaded regex-syntax v0.6.27
  Downloaded ahash v0.8.0
  Downloaded git-date v0.0.1
  Downloaded openssl-sys v0.9.75
  Downloaded globset v0.4.9
  Downloaded generic-array v0.14.6
  Downloaded crypto-common v0.1.6
  Downloaded pest_derive v2.3.1
  Downloaded num_threads v0.1.6
  Downloaded names v0.14.0
  Downloaded smartstring v1.0.1
  Downloaded git-validate v0.5.5
  Downloaded clap_derive v3.2.18
  Downloaded console v0.15.1
  Downloaded btoi v0.4.2
  Downloaded sanitize-filename v0.4.0
  Downloaded git-glob v0.3.2
  Downloaded git-ref v0.14.0
  Downloaded git-config v0.5.0
  Downloaded crossbeam-utils v0.8.11
  Downloaded clap v3.2.22
  Downloaded indexmap v1.9.1
  Downloaded quick-error v2.0.1
  Downloaded rhai_codegen v1.4.2
  Downloaded proc-quote-impl v0.3.2
  Downloaded liquid-core v0.26.0
  Downloaded remove_dir_all v0.7.0
  Downloaded proc-quote v0.4.0
  Downloaded path-absolutize v3.0.13
  Downloaded liquid v0.26.0
  Downloaded git-hash v0.9.9
  Downloaded itoa v1.0.3
  Downloaded pest v2.3.1
  Downloaded block-buffer v0.10.3
  Downloaded rhai v1.10.0
  Downloaded libssh2-sys v0.2.23
  Downloaded anyhow v1.0.65
  Downloaded pest_meta v2.3.1
  Downloaded ignore v0.4.18
  Downloaded pest_generator v2.3.1
  Downloaded remove_dir_all v0.5.3
  Downloaded typenum v1.15.0
  Downloaded version_check v0.9.4
  Downloaded same-file v1.0.6
  Downloaded url v2.3.1
  Downloaded unicode-segmentation v1.10.0
  Downloaded thiserror v1.0.35
  Downloaded time-macros v0.2.4
  Downloaded static_assertions v1.1.0
  Downloaded walkdir v2.3.2
  Downloaded unicode-normalization v0.1.22
  Downloaded rand_core v0.6.4
  Downloaded ucd-trie v0.1.5
  Downloaded unicode-bidi v0.3.8
  Downloaded tempfile v3.3.0
  Downloaded thiserror-impl v1.0.35
  Downloaded time v0.3.14
  Downloaded unicode-width v0.1.10
  Downloaded memmap2 v0.5.7
  Downloaded zeroize v1.5.7
  Downloaded tinyvec v1.6.0
  Downloaded tinyvec_macros v0.1.0
  Downloaded unicode-bom v1.1.4
  Downloaded serde v1.0.144
  Downloaded terminal_size v0.1.17
  Downloaded libgit2-sys v0.13.4+1.4.2
  Downloaded semver v1.0.14
  Downloaded libz-sys v1.1.8
  Downloaded lock_api v0.4.8
  Downloaded sha1 v0.10.5
  Downloaded num-traits v0.2.15
  Downloaded serde_derive v1.0.144
  Downloaded nom v7.1.1
  Downloaded form_urlencoded v1.1.0
  Downloaded thread_local v1.1.4
  Downloaded heck v0.4.0
  Downloaded parking_lot_core v0.9.3
  Downloaded openssl-src v111.22.0+1.1.1q
  Downloaded textwrap v0.15.1
  Downloaded pkg-config v0.3.25
  Downloaded sha1_smol v1.0.0
  Downloaded jobserver v0.1.24
  Downloaded signal-hook v0.3.14
  Downloaded proc-macro-error v1.0.4
  Downloaded regex v1.6.0
  Downloaded toml v0.5.9
  Downloaded smallvec v1.9.0
  Downloaded signal-hook-registry v1.4.0
  Downloaded proc-macro-error-attr v1.0.4
  Downloaded proc-macro-hack v0.5.19
  Downloaded itertools v0.10.4
  Downloaded number_prefix v0.4.0
  Downloaded indicatif v0.16.2
  Downloaded dirs v4.0.0
  Downloaded clap_lex v0.2.4
  Downloaded git-features v0.21.1
  Downloaded paste v1.0.9
  Downloaded path-dedot v3.0.17
  Downloaded liquid-lib v0.26.0
  Downloaded kstring v2.0.0
  Downloaded git-tempfile v2.0.4
  Downloaded git-sec v0.2.0
  Downloaded git-lock v2.1.1
  Downloaded digest v0.10.5
  Downloaded fnv v1.0.7
  Downloaded cpufeatures v0.2.5
  Downloaded lazy_static v1.4.0
  Downloaded either v1.8.0
  Downloaded anymap2 v0.13.0
  Downloaded git-path v0.2.0
  Downloaded git-object v0.19.0
  Downloaded doc-comment v0.3.3
  Downloaded aho-corasick v0.7.19
  Downloaded 130 crates (15.0 MB) in 3.24s (largest was `openssl-src` at 5.1 MB)
   Compiling libc v0.2.132
   Compiling proc-macro2 v1.0.43
   Compiling quote v1.0.21
   Compiling unicode-ident v1.0.4
   Compiling autocfg v1.1.0
   Compiling syn v1.0.99
   Compiling cfg-if v1.0.0
   Compiling memchr v2.5.0
   Compiling once_cell v1.14.0
   Compiling thiserror v1.0.35
   Compiling version_check v0.9.4
   Compiling lazy_static v1.4.0
   Compiling pkg-config v0.3.25
   Compiling regex-automata v0.1.10
   Compiling serde_derive v1.0.144
   Compiling itoa v1.0.3
   Compiling serde v1.0.144
   Compiling smallvec v1.9.0
   Compiling regex-syntax v0.6.27
   Compiling proc-macro-hack v0.5.19
   Compiling ucd-trie v0.1.5
   Compiling hashbrown v0.12.3
   Compiling remove_dir_all v0.5.3
   Compiling fastrand v1.8.0
   Compiling parking_lot_core v0.9.3
   Compiling same-file v1.0.6
   Compiling static_assertions v1.1.0
   Compiling scopeguard v1.1.0
   Compiling bitflags v1.3.2
   Compiling signal-hook v0.3.14
   Compiling quick-error v2.0.1
   Compiling minimal-lexical v0.2.1
   Compiling tinyvec_macros v0.1.0
   Compiling percent-encoding v2.2.0
   Compiling hex v0.4.3
   Compiling log v0.4.17
   Compiling either v1.8.0
   Compiling time-macros v0.2.4
   Compiling sha1_smol v1.0.0
   Compiling unicode-width v0.1.10
   Compiling unicode-bidi v0.3.8
   Compiling anymap2 v0.13.0
   Compiling ppv-lite86 v0.2.16
   Compiling doc-comment v0.3.3
   Compiling crossbeam-utils v0.8.11
   Compiling semver v1.0.14
   Compiling os_str_bytes v6.3.0
   Compiling unicode-segmentation v1.10.0
   Compiling names v0.14.0
   Compiling anyhow v1.0.65
   Compiling heck v0.4.0
   Compiling fnv v1.0.7
   Compiling zeroize v1.5.7
   Compiling unicode-bom v1.1.4
   Compiling textwrap v0.15.1
   Compiling number_prefix v0.4.0
   Compiling paste v1.0.9
   Compiling home v0.5.3
   Compiling path-dedot v3.0.17
   Compiling thread_local v1.1.4
   Compiling proc-macro-error-attr v1.0.4
   Compiling proc-macro-error v1.0.4
   Compiling ahash v0.8.0
   Compiling num-traits v0.2.15
   Compiling lock_api v0.4.8
   Compiling smartstring v1.0.1
   Compiling indexmap v1.9.1
   Compiling walkdir v2.3.2
   Compiling tinyvec v1.6.0
   Compiling form_urlencoded v1.1.0
   Compiling itertools v0.10.4
   Compiling clap_lex v0.2.4
   Compiling path-absolutize v3.0.13
   Compiling unicode-normalization v0.1.22
   Compiling bstr v0.2.17
   Compiling aho-corasick v0.7.19
   Compiling nom v7.1.1
   Compiling getrandom v0.2.7
   Compiling tempfile v3.3.0
   Compiling signal-hook-registry v1.4.0
   Compiling num_threads v0.1.6
   Compiling terminal_size v0.1.17
   Compiling memmap2 v0.5.7
   Compiling dirs-sys v0.3.7
   Compiling git-sec v0.2.0
   Compiling remove_dir_all v0.7.0
   Compiling jobserver v0.1.24
   Compiling rand_core v0.6.4
   Compiling idna v0.3.0
   Compiling time v0.3.14
   Compiling console v0.15.1
   Compiling dirs v4.0.0
   Compiling dashmap v5.4.0
   Compiling rand_chacha v0.3.1
   Compiling cc v1.0.73
   Compiling git-date v0.0.1
   Compiling git-validate v0.5.5
   Compiling git-glob v0.3.2
   Compiling proc-quote-impl v0.3.2
   Compiling dialoguer v0.10.2
   Compiling regex v1.6.0
   Compiling rand v0.8.5
   Compiling url v2.3.1
   Compiling git-tempfile v2.0.4
   Compiling openssl-src v111.22.0+1.1.1q
   Compiling btoi v0.4.2
   Compiling git-lock v2.1.1
   Compiling libz-sys v1.1.8
   Compiling openssl-sys v0.9.75
   Compiling libssh2-sys v0.2.23
   Compiling libgit2-sys v0.13.4+1.4.2
   Compiling globset v0.4.9
   Compiling sanitize-filename v0.4.0
   Compiling indicatif v0.16.2
   Compiling git-actor v0.10.1
   Compiling ignore v0.4.18
   Compiling proc-quote v0.4.0
   Compiling thiserror-impl v1.0.35
   Compiling liquid-derive v0.26.0
   Compiling rhai_codegen v1.4.2
   Compiling clap_derive v3.2.18
   Compiling rhai v1.10.0
   Compiling git-hash v0.9.9
   Compiling pest v2.3.1
   Compiling git-path v0.2.0
   Compiling git-features v0.21.1
   Compiling git-object v0.19.0
   Compiling clap v3.2.22
   Compiling pest_meta v2.3.1
   Compiling git-ref v0.14.0
   Compiling pest_generator v2.3.1
   Compiling git-config v0.5.0
   Compiling pest_derive v2.3.1
   Compiling kstring v2.0.0
   Compiling toml v0.5.9
   Compiling liquid-core v0.26.0
   Compiling liquid-lib v0.26.0
   Compiling liquid v0.26.0
   Compiling git2 v0.14.4
   Compiling cargo-generate v0.16.0
    Finished release [optimized] target(s) in 3m 37s
  Installing /Users/yanagiharas/.cargo/bin/cargo-generate
   Installed package `cargo-generate v0.16.0` (executable `cargo-generate`)
```
:::

### Cargo Generate によるプロジェクトの作成

それでは、`cargo generate` でプロジェクトを作成してみます。使用するプロジェクトテンプレートは、[[wasm-pack-template](https://github.com/rustwasm/wasm-pack-template)]

```shell
cargo generate --git https://github.com/rustwasm/wasm-pack-template
```

:::details 実行結果
```shell
🤷   Project Name : wasm-pack
🔧   Destination: /Users/yanagiharas/Works/webpack/wasm-pack ...
🔧   Generating template ...
[ 1/12]   Done: .appveyor.yml
[ 2/12]   Done: .gitignore
[ 3/12]   Done: .travis.yml
[ 4/12]   Done: Cargo.toml
[ 5/12]   Done: LICENSE_APACHE
[ 6/12]   Done: LICENSE_MIT
[ 7/12]   Done: README.md
[ 8/12]   Done: src/lib.rs
[ 9/12]   Done: src/utils.rs
[10/12]   Done: src
[11/12]   Done: tests/web.rs
[12/12]   Done: tests
🔧   Moving generated files into: `/Users/yanagiharas/Works/webpack/wasm-pack`...
💡   Initializing a fresh Git repository
✨   Done! New project created /Users/yanagiharas/Works/webpack/wasm-pack
```
:::

以下のような構成が作れました。
```shell
wasm-pack
├── Cargo.toml
├── LICENSE_APACHE
├── LICENSE_MIT
├── README.md
├── src
│  ├── lib.rs
│  └── utils.rs
└── tests
   └── web.rs
```

つまり、`wasm-pack new` コマンドで作成した構成と同じ内容を作ることができました。
この `cargo gemerate` コマンドの方が、テンプレートを知っていれば、様々なテンプレートからプロジェクトを新規作成できるので汎用性が高いプロジェクト作成コマンドだと思います。

### Cargo Generate で指定できるプロジェクトテンプレート

以下に利用できるテンプレートがいくつか紹介されていました:

- [Available Templates](https://github.com/cargo-generate/cargo-generate/blob/main/TEMPLATES.md)
|テンプレート|説明|
|----------|---|
|PyO3|Python ライブラリ|
|wasm-pack|WebAssembly|
|CLI|コマンドライン|
|rocket-base:|Rocket を使った Web アプリケーション|
|rust-samp-sdk|samp プラグイン|
|actix-tera|Actix-web と Tera を使った Web アプリケーション|
|procmacro-quickstart|手続き型マクロ|
|bluepill|blue pill' stm32 マイクロコントローラボード mendelt |
|cmdr|対話的なコマンドラインアプリケーション|
|ggez|ggez を使用したゲーム|
|generust|Actix-web サーバ, WASM クライアント, サポートコード|
|template-rust-backend-with-electron-frontend|Electron フロントエンドで Rust ネイティブの cdylib バックエンド|
|OrbTk|OrbTk を使ったユーザインタフェース|
|swift-rust-xcode-template|Swift と Rust による iOSアプリ|
|QuickStart WebAssembly|RWebassemblyアプリケーション|
|Win32|低レベルの Win32 アプリケーション|
|rust-starter|Clap で をブートストラップRust CLIアプリケーション|
|rust-cli-template|ベンチマークやテスト用のボイラープレートに加えて、color_eyre とトレースが既に設定された CLI|
|mongodb-service-template|mongodb を使った graphql サービス|
|godot-rust-template|Godot と Rust を使ったゲーム|

## Day 25 のまとめ

と、いうわけで、今日は簡単にですけれど、`cargo` のサブコマンドな `cargo-generate` を見てきました。
Java で言うところの、**Maven** の **mvn archetype:generate** のようなものだと理解しましたよ。
さて、この `cargo-generate` コマンド、Wasm 用なプロジェクト以外にも対応していることが分かったので、このコマンド、利用していこうと思います。
