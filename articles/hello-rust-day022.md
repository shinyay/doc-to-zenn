---
title: "100日後にRustをちょっと知ってる人になる: [Day 22]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 22 のテーマ

この数日間、Rust の観点から **WebAssembly** について見てきています。
この WebAssembly ですが、**WASI** の仕様ではブラウザ以外でも動くことを目的としていますが、もちろん WebAssembly 自体はブラウザ上でポータブルかつ安全に動作することを目的として誕生してきています。ブラウザ上でアプリケーションを動かすというと、**JavaScript** を思い浮かべると思います。では、WebAssembly が目指しているのは JavaScript の置き換えなのでしょうか？

次の記事に興味深い記述がありました。

- [Making WebAssembly better for Rust & for all languages](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/)

> **WebAssembly** は **JavaScript** に取って代わるものではなく、JavaScriptと一緒に使う素晴らしいツールになることを目指しています。

**WebAssembly** を介して、Rust と JavaScript の間で次のようなことが実現できるようになることが望まれているということなのです。

- Rust 開発者は、**Node.js 開発環境を必要とせず**に JavaScript で使用する WebAssembly パッケージを作成できる
- JavaScript 開発者は、**Rust 開発環境を必要とせず**に WebAssembly を使用できる

![](https://storage.googleapis.com/zenn-user-upload/6d2e5411eed5-20220914.png)

## wasm-pack

![](https://storage.googleapis.com/zenn-user-upload/ddd18f0b3f3c-20220914.png)

**wasm-pack** は WebAssembly をターゲットとする Rust クレートを組み立て、パッケージ化するためのツールです。これらのパッケージはnpmレジストリに公開され、他のパッケージと一緒に使用することができます。つまり、JSや他のパッケージと並べて使うことができ、様々な種類のアプリケーションで使うことができます。

- [wasm-pack](https://github.com/rustwasm/wasm-pack)

### wasm-pack インストール

次のシェルでインストールを行います。

```shell
curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
```

:::details wasm-pack -h
```shell
wasm-pack 0.10.3
The various kinds of commands that `wasm-pack` can execute

USAGE:
    wasm-pack [FLAGS] [OPTIONS] <SUBCOMMAND>

FLAGS:
    -h, --help       Prints help information
    -q, --quiet      No output printed to stdout
    -V, --version    Prints version information
    -v, --verbose    Log verbosity is based off the number of v used

OPTIONS:
        --log-level <log-level>    The maximum level of messages that should be logged by wasm-pack. [possible values:
                                   info, warn, error] [default: info]

SUBCOMMANDS:
    build      🏗️  build your npm package!
    help       Prints this message or the help of the given subcommand(s)
    login      👤  Add an npm registry user account! (aliases: adduser, add-user)
    new        🐑 create a new project with a template
    pack       🍱  create a tar of your npm package but don't publish!
    publish    🎆  pack up your npm package and publish!
    test       👩‍🔬  test your wasm!
```
:::

|サブコマンド|説明|
|----------|---|
|build   |NPM パッケージのビルド|
|help    |ヘルプメッセージの表示|
|login   |NPM レジストリにユーザーアカウントを追加|
|new     |プロジェクトテンプレートの新規作成|
|pack    |NPM パッケージの TAR を作成 (公開はしない)|
|publish |NPM パッケージの公開|
|test    |WASM のテスト|

### wasm-pack のクイックスタート

まずは `wasm-pack` の動きを確認してみたいと思います。

#### プロジェクトテンプレートの作成

`hello-wasm` という名前のプロジェクトを作成します。

```shell
wasm-pack new hello-wasm
```

:::details 実行結果
```shell
[INFO]: ⬇️  Installing cargo-generate...
🐑  Generating a new rustwasm project with name 'hello-wasm'...
🔧   Creating project called `hello-wasm`...
✨   Done! New project created /Users/yanagiharas/Works/hello-wasm
[INFO]: 🐑 Generated new project at /hello-wasm
```
:::


## Day 22 のまとめ
