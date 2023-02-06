---
title: "5 分で WebAssembly + Docker = Hello World"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [webassembly, wasm, rust, docker]
published: false
---
## テーマ: Rust と Docker Desktop で WebAssembly な Hello World アプリ を作る

Zenn をご覧な方であれば、**WebAssembly** (WASM)  というキーワードを耳にしたり目にしたりしたことがある方は多いのではないでしょうか。昨年くらいから急に注目を集めはじめ、次世代のクラウドネイティブ技術とも言われ始めているテクノロジーです。

簡単に WebAssembly を説明すると次のように言えるでしょう。

:::message
WebAssembly は、高速かつ効率的に設計されたスタックベースの仮想マシンのバイナリ命令形式です。低レベルのアセンブリのように使用することができ、ネイティブに近い速度でコードを実行する方法を提供し、ブラウザ上で動作させることが可能です。Chrome、Firefox、Safari、Edgeなど、主要な Web ブラウザでサポートされています。
:::

また、WebAssembly (WASM) はブラウザ以外の環境で実行することも可能です。そのために必要となる仕様が、**WebAssembly System Interface** (WASI) です。WASI は、ホストのファイルやネットワークなどの資源に安全にアクセスさせるための仕様です。これは、WASM モジュールがホスト環境と対話するための標準化されたシステムコールのセットを提供します。この WASI により、WASM のコードをバックエンドで実行することができるようになります。

:::message
WebAssembly のもう一つの重要な点は、言語にとらわれないということです。
つまり、Rust、C++、Cなどのさまざまなプログラミング言語で書かれたコードを WASM にコンパイルして、ブラウザで実行することができるのです。これにより、開発者はWebアプリケーションを構築する際の選択肢が増え、さまざまな言語の長所を生かすことができます。
:::

## Rust と WebAssembly パッケージのインストール

5 分で WebAssembly アプリを作ると第していますが、ほぼほとんど全ての時間は準備をする時間です。
使用するものは、Rust と Docker Desktop です。それらの導入や構成の手順を紹介しながら、WASM バイナリを作成していきます。

### Rust のインストール

まず、プログラミング言語**Rust** をコンピュータにインストールする必要があります。Rust は、公式サイトの説明に従ってインストールすることができます。

- [Rust 公式サイト](https://www.rust-lang.org/tools/install)

それでは、以下の `curl` コマンドでインストールを行いましょう。

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

そのコマンドにより、パッケージマネージャの **Cargo** と一緒に Rust がインストールされます。インストールしたら、以下のコマンドを実行して、`$PATH` 変数を更新します。

```shell
source "$HOME/.cargo/env"
```

Rust がインストールされたことを確認しておきましょう。

```shell
rustc --version
```

今日インストールしたなら、バージョンは `1.67.0` ですね。

```shell
rustc 1.67.0 (fc594f156 2023-01-24)
```

### Rust のプロジェクト作成

パッケージマネージャ `cargo` を使用して、Rust のプロジェクトを作成します。以下のコマンドを実行します。

```shell
cargo new wasm-docker-helloworld
```

これにより、Rust ライブラリの基本構造を持つ "wasm-docker-helloworld" という新しいディレクトリが作成されます。
このプロジェクトの `src/lib.rs` にはすでに次の Hello World のコードが入っています。

```rust
fn main() {
    println!("Hello, world!");
}
```

これをビルドしてみます。以下のコマンドを実行します。

```shell
cargo build
```

これでバイナリファイルが作成され、`target/debug` の下に置かれます。これを直接実行することができます。

```shell
./target/debug/wasm-docker-helloworld
```

### WebAssembly バイナリの作成

さて、WebAssembly ランタイム用にプロジェクトをビルドするために、新しいターゲットを追加する必要があります。

```shell
rustup target add wasm32-wasi
```

そして、このターゲットをビルドコマンドで使用することができます。

```shell
cargo build --target wasm32-wasi
```

このコマンドにより、WebAssembly バイナリを作成し、`target/wasm32-wasi` の下に配置します。

```shell
target
├── CACHEDIR.TAG
├── debug
│   ├── build
│   ├── deps
│   ├── examples
│   ├── wasm-docker-helloworld
│   ├── wasm-docker-helloworld.d
│   └── incremental
└── wasm32-wasi
    ├── CACHEDIR.TAG
    └── debug
        ├── build
        ├── deps
        ├── examples
        ├── wasm-docker-helloworld.d
        ├── wasm-docker-helloworld.wasm
        └── incremental
```

### Docker イメージの作成

なお、これは現在プレビュー機能であり、**Docker Desktop** でのみ利用可能です。Docker Desktop で WebAssembly コンテナをビルドまたは実行できるようにするには、まず設定から **containerd pulling and storing feature** を有効にする必要があります。

![](https://storage.googleapis.com/zenn-user-upload/89c63ddbc914-20230206.png)

まず、以下の内容でDockerfileを作成します。

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch
COPY ./target/wasm32-wasi/debug/hello-wasm.wasm /hello.wasm
ENTRYPOINT [ "hello.wasm" ]
```

次に、以下のコマンドでビルドします。

```shell
docker buildx build --platform wasi/wasm32 -t hello-wasm .
```

Dockerイメージを確認してみましょう。

```shell
docker image ls
```

```shell
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
hello-wasm   latest    779ebd5f5914   56 seconds ago   519kB
```

イメージが作成され、サイズは半分のメガバイトになります。次のコマンドで実行してみましょう。

```shell
docker run --runtime=io.containerd.wasmedge.v1 --platform=wasi/wasm32 hello-wasm
```

次のように表示されます。

```shell
Hello, world!
```

## まとめ

**WebAssembly** はネイティブに近いパフォーマンスを提供し、プラットフォーム非依存です。
**Docker Desktop** には **WasmEdge** ランタイムが付属しており、WebAssembly アプリを Docker コンテナにラップし Docker Compose で非 WASM コンテナと一緒に実行することも可能になります。
