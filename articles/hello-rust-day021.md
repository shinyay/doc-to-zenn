---
title: "100日後にRustをちょっと知ってる人になる: [Day 21]Cargo による Wasm ビルド"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 21 のテーマ

昨日は `rustup` で **wasm32-wasi** ターゲットを追加して、WASI の実装ランタイムな **Wasmtime** をインストールして、`rustc` でWasm バイナリをコンパイルしてみました。

これらの Rust に関するツールチェーンで昨日やり残していたことをやってみようと思います。Rust のツールチェーンといえば、以下のコマンドがトピックに出てきますよね。

- `rustup`: Rust のツールチェーンマネージャ
  - [The rustup book](https://rust-lang.github.io/rustup/index.html)
- `rustc`: Rust コンパイラコマンド
- `cargo`: Rust のパッケージマネージャ 兼 ビルドツール

あと、ツールチェーンと言った時に含まれるのは、次のものです:

- **Rust の標準ライブラリ (std)**
- **Rust の API ドキュメント**

さて、この標準のツールチェーンで提供されるビルドツールの **cargo** を使った Wasm の扱いについて確認していませんでした。今日は、その確認をしておきたいと思います。

## Cargo を用いた Wasm ビルド

**Cargo** は先にも言ったように、パッケージマネージャ 兼 ビルドツールです。つまり、Java で使う **Maven** や **Gradle** と考えるととても分かりやすいですね（Java 経験者の人には)

### Cargo コマンド

![](https://storage.googleapis.com/zenn-user-upload/ae57b535e973-20220913.png)

ここで 改めて Cargo コマンドの概要を見ておこうと思います。

- [The Cargo Book](https://doc.rust-lang.org/cargo/)

```shell
cargo -h
```

以下が標準では言っている `cargo` のサブコマンドです。
|コマンド|説明|
|-------|---|
|build|現在のパッケージのコンパイル|
|check|現在のパッケージを解析してエラーを報告するが，オブジェクトファイルはビルドしない|
|clean|ターゲットディレクトリを削除|
|doc|現在のパッケージとその依存関係のドキュメントをビルド|
|new|新しいCargoパッケージを作成|
|init|既存のディレクトリに新しいCargoパッケージを作成|
|add|マニフェストファイルへの依存関係の追加|
|run|ローカルパッケージのバイナリやサンプルを実行|
|test|テストの実行|
|bench|ベンチマークを実行|
|update|Cargo.lockにリストされている依存関係を更新|
|search|レジストリを検索してクレートの発見|
|publish|パッケージを作成し、このパッケージをレジストリにアップロード|
|install|Rust バイナリのインストール。デフォルトのインストール先は $HOME/.cargo/bin|
|uninstall|Rust バイナリのアンインストール|

Cargo によるビルドは、`cargo build` で行います。このサブコマンドのコマンドオプションを見て見ると、`rustc` のコマンドオプション同様に `--target` オプションでターゲットトリプルを指定しています。つまりここで、`wasm32-wasi` を指定したら WebAssembly バイナリが生成できそうです。

```shell
cargo build -h
```

```shell
USAGE:
    cargo build [OPTIONS]

OPTIONS:
  :
        --target <TRIPLE>           Build for the target triple
  :
```

#### cargo build --target wasm32-wasi

cargo で Wasm バイナリのビルドをおこなってみます。

プロジェクトの作成
```shell
cargo new hello-wasm
```

```shell
cargo build --target wasm32-wasi

   Compiling hello-wasm v0.1.0 (/Users/yanagiharas/hello-wasm)
    Finished dev [unoptimized + debuginfo] target(s) in 0.83s
```

問題なくビルドが成功しました。そして、プロジェクトルートディレクトリに `target` ディレクトリが作られて成果物が以下のように生成されました。
ただし、以下の成果物の構成はデバッグ構成になっています。

```shell
target
├── CACHEDIR.TAG
├── debug
│  ├── build
│  ├── deps
│  ├── examples
│  └── incremental
└── wasm32-wasi
   ├── CACHEDIR.TAG
   └── debug
      ├── build
      ├── deps
      │  ├── hello_wasm-65874ca78a0b301f.d
      │  └── hello_wasm-65874ca78a0b301f.wasm
      ├── examples
      ├── hello-wasm.d
      ├── hello-wasm.wasm
      └── incremental
         └── hello_wasm-2gw1w9gjhbk0a
            ├── s-gdi3zdm6q6-rmj19w-1i7jph7a5jnjr
            │  ├── 1n6ltkmxf9v4hy1w.o
            │  ├── 2nju6fzobyf20ku7.o
            │  ├── 3i1fz70rutg39zgl.o
            │  ├── 37cam6tyso17g9op.o
            │  ├── 312qucrovy5m0gyp.o
            │  ├── 590sdpwwj3c6vwum.o
            │  ├── dep-graph.bin
            │  ├── lhqlb4oipl2go0q.o
            │  ├── query-cache.bin
            │  └── work-products.bin
            └── s-gdi3zdm6q6-rmj19w.lock
```

## Day 21 のまとめ
