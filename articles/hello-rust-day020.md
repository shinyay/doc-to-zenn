---
title: "100日後にRustをちょっと知ってる人になる: [Day 20]Rust で Wasm"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: true
---
## Day 20 のテーマ

Day 18, 19 と Rust のユースケースとしても注目を浴びている **WebAssembly (WASM)** と **WebAssembly System Interface (WASI)** について調べてみました。
まだ仕様を策定中であったりという現在進行系で進化している技術ですが、次世代の **Write once, Run anywhere** と言えるような技術に今後発展していきそうな期待を持つことができました。

ということで、Rust を使って WebAssembly の開発できるように、開発/実行環境をつくり、実際に WebAssebmly として動かしてみたいと思います。

## WASI ランタイム環境の準備

**WASI** 自体はインターフェース仕様なので、実際に動作させるためには WASI を実装したランタイムが必要になることは、[Day 19](https://zenn.dev/shinyay/articles/hello-rust-day019#wasi-%E3%81%AE%E5%AE%9F%E8%A3%85) の中でも書きました。そこで、ここでは ランタイムをいれてみようと思います。

### 代表的な WASI ランタイム

以下が代表的な WASI ランタイムです。

- [Wasmtime](https://docs.wasmtime.dev/)
  - [Wasmtime - Repo](https://github.com/bytecodealliance/wasmtime)
- [Wasmer](https://wasmer.io/)
  - [Wasmer - Repo](https://github.com/wasmerio/wasmer)
- [Wasm3](https://wapm.io/vshymanskyy/wasm3)
  - [Wasm3 - Repo](https://github.com/wasm3/wasm3)
- [WasmEdge](https://wasmedge.org/)
  - [WasmEdge](https://github.com/WasmEdge/WasmEdge)
- [WebAssembly Micro Runtime(WAMR)](https://github.com/bytecodealliance/wasm-micro-runtime)

この中でも **Wasmtime** がリファレンス実装と言われているようなので、それをインストールしようと思います。

### Wasmtime のインストール

**[Wasmtime](https://github.com/bytecodealliance/wasmtime)** は、WASI の仕様策定を推進している **[Bytecode Alliance](https://bytecodealliance.org/)** によるリファレンス実装です。

- [Wasmtime](https://wasmtime.dev/)

以下を実行してインストールし、ターミナルを開き直します。

```shell
curl https://wasmtime.dev/install.sh -sSf | bash
```

ちなみに、ぼくのターミナル環境は `fish` シェルなので以下の定義を `$HOME/.config/fish/config.fish` に追加しています。

```fish
string match -r ".wasmtime" "$PATH" > /dev/null; or set -gx PATH "$WASMTIME_HOME/bin" $PATH
```

### wasm32-wasi ターゲットのインストール

次に Rust のソースコードをコンパイルして WebAssebmly バイナリを出力するためのターゲットを追加します。Rust は言語仕様の標準で WebAssembly をサポートしているため、`--target` フラグで目的のターゲットを指定することで生成できます。

Rust のコンパイルターゲットの一覧は以下のようなものがあります。

```shell
# ターゲット一覧表示
rustc --print target-list
```

:::details target-list
```shell
aarch64-apple-darwin
aarch64-apple-ios
aarch64-apple-ios-macabi
aarch64-apple-ios-sim
aarch64-apple-tvos
aarch64-apple-watchos-sim
aarch64-fuchsia
aarch64-kmc-solid_asp3
aarch64-linux-android
aarch64-pc-windows-gnullvm
aarch64-pc-windows-msvc
aarch64-unknown-freebsd
aarch64-unknown-hermit
aarch64-unknown-linux-gnu
aarch64-unknown-linux-gnu_ilp32
aarch64-unknown-linux-musl
aarch64-unknown-netbsd
aarch64-unknown-none
aarch64-unknown-none-softfloat
aarch64-unknown-openbsd
aarch64-unknown-redox
aarch64-unknown-uefi
aarch64-uwp-windows-msvc
aarch64-wrs-vxworks
aarch64_be-unknown-linux-gnu
aarch64_be-unknown-linux-gnu_ilp32
arm-linux-androideabi
arm-unknown-linux-gnueabi
arm-unknown-linux-gnueabihf
arm-unknown-linux-musleabi
arm-unknown-linux-musleabihf
arm64_32-apple-watchos
armebv7r-none-eabi
armebv7r-none-eabihf
armv4t-unknown-linux-gnueabi
armv5te-unknown-linux-gnueabi
armv5te-unknown-linux-musleabi
armv5te-unknown-linux-uclibceabi
armv6-unknown-freebsd
armv6-unknown-netbsd-eabihf
armv6k-nintendo-3ds
armv7-apple-ios
armv7-linux-androideabi
armv7-unknown-freebsd
armv7-unknown-linux-gnueabi
armv7-unknown-linux-gnueabihf
armv7-unknown-linux-musleabi
armv7-unknown-linux-musleabihf
armv7-unknown-linux-uclibceabi
armv7-unknown-linux-uclibceabihf
armv7-unknown-netbsd-eabihf
armv7-wrs-vxworks-eabihf
armv7a-kmc-solid_asp3-eabi
armv7a-kmc-solid_asp3-eabihf
armv7a-none-eabi
armv7a-none-eabihf
armv7k-apple-watchos
armv7r-none-eabi
armv7r-none-eabihf
armv7s-apple-ios
asmjs-unknown-emscripten
avr-unknown-gnu-atmega328
bpfeb-unknown-none
bpfel-unknown-none
hexagon-unknown-linux-musl
i386-apple-ios
i586-pc-windows-msvc
i586-unknown-linux-gnu
i586-unknown-linux-musl
i686-apple-darwin
i686-linux-android
i686-pc-windows-gnu
i686-pc-windows-msvc
i686-unknown-freebsd
i686-unknown-haiku
i686-unknown-linux-gnu
i686-unknown-linux-musl
i686-unknown-netbsd
i686-unknown-openbsd
i686-unknown-uefi
i686-uwp-windows-gnu
i686-uwp-windows-msvc
i686-wrs-vxworks
m68k-unknown-linux-gnu
mips-unknown-linux-gnu
mips-unknown-linux-musl
mips-unknown-linux-uclibc
mips64-openwrt-linux-musl
mips64-unknown-linux-gnuabi64
mips64-unknown-linux-muslabi64
mips64el-unknown-linux-gnuabi64
mips64el-unknown-linux-muslabi64
mipsel-sony-psp
mipsel-unknown-linux-gnu
mipsel-unknown-linux-musl
mipsel-unknown-linux-uclibc
mipsel-unknown-none
mipsisa32r6-unknown-linux-gnu
mipsisa32r6el-unknown-linux-gnu
mipsisa64r6-unknown-linux-gnuabi64
mipsisa64r6el-unknown-linux-gnuabi64
msp430-none-elf
nvptx64-nvidia-cuda
powerpc-unknown-freebsd
powerpc-unknown-linux-gnu
powerpc-unknown-linux-gnuspe
powerpc-unknown-linux-musl
powerpc-unknown-netbsd
powerpc-unknown-openbsd
powerpc-wrs-vxworks
powerpc-wrs-vxworks-spe
powerpc64-unknown-freebsd
powerpc64-unknown-linux-gnu
powerpc64-unknown-linux-musl
powerpc64-wrs-vxworks
powerpc64le-unknown-freebsd
powerpc64le-unknown-linux-gnu
powerpc64le-unknown-linux-musl
riscv32gc-unknown-linux-gnu
riscv32gc-unknown-linux-musl
riscv32i-unknown-none-elf
riscv32im-unknown-none-elf
riscv32imac-unknown-none-elf
riscv32imac-unknown-xous-elf
riscv32imc-esp-espidf
riscv32imc-unknown-none-elf
riscv64gc-unknown-freebsd
riscv64gc-unknown-linux-gnu
riscv64gc-unknown-linux-musl
riscv64gc-unknown-none-elf
riscv64imac-unknown-none-elf
s390x-unknown-linux-gnu
s390x-unknown-linux-musl
sparc-unknown-linux-gnu
sparc64-unknown-linux-gnu
sparc64-unknown-netbsd
sparc64-unknown-openbsd
sparcv9-sun-solaris
thumbv4t-none-eabi
thumbv6m-none-eabi
thumbv7a-pc-windows-msvc
thumbv7a-uwp-windows-msvc
thumbv7em-none-eabi
thumbv7em-none-eabihf
thumbv7m-none-eabi
thumbv7neon-linux-androideabi
thumbv7neon-unknown-linux-gnueabihf
thumbv7neon-unknown-linux-musleabihf
thumbv8m.base-none-eabi
thumbv8m.main-none-eabi
thumbv8m.main-none-eabihf
wasm32-unknown-emscripten
wasm32-unknown-unknown
wasm32-wasi
wasm64-unknown-unknown
x86_64-apple-darwin
x86_64-apple-ios
x86_64-apple-ios-macabi
x86_64-apple-tvos
x86_64-apple-watchos-sim
x86_64-fortanix-unknown-sgx
x86_64-fuchsia
x86_64-linux-android
x86_64-pc-solaris
x86_64-pc-windows-gnu
x86_64-pc-windows-gnullvm
x86_64-pc-windows-msvc
x86_64-sun-solaris
x86_64-unknown-dragonfly
x86_64-unknown-freebsd
x86_64-unknown-haiku
x86_64-unknown-hermit
x86_64-unknown-illumos
x86_64-unknown-l4re-uclibc
x86_64-unknown-linux-gnu
x86_64-unknown-linux-gnux32
x86_64-unknown-linux-musl
x86_64-unknown-netbsd
x86_64-unknown-none
x86_64-unknown-none-linuxkernel
x86_64-unknown-openbsd
x86_64-unknown-redox
x86_64-unknown-uefi
x86_64-uwp-windows-gnu
x86_64-uwp-windows-msvc
x86_64-wrs-vxworks
```
:::

Wasm に関するターゲットとしては、以下のものがあります:

- wasm32-unknown-emscripten
- wasm32-unknown-unknown
- wasm32-wasi
- wasm64-unknown-unknown

この中から、標準ライブラリを統合している `wasm32-wasi` を使うことにします。
これは、WASI によるスタンドアロンバイナリを作ることを目的にしているようです。

`rustup` を使用して `wasm32-wasi` をインストールします。

```shell
rustup target add wasm32-wasi
```

インストールを確認してみます。

```shell
$ rustup show

installed targets for active toolchain
--------------------------------------

wasm32-wasi
x86_64-apple-darwin

active toolchain
----------------

stable-x86_64-apple-darwin (default)
rustc 1.63.0 (4b91a6ea7 2022-08-08)
```

#### Wasm ターゲット

|ターゲット名|説明|
|----------|---|
|wasm32-wasi|標準ライブラリと統合. スタンドアロンバイナリの生成を目的としています|
|wasm32-unknown-unknown|WASIと同じように単一の*.wasmバイナリを生成することに重点を置いていますが、標準ライブラリはほぼスタブ化されています。println!のようなマクロは動きません。|
|wasm32-unknown-emscripten|ウェブブラウザで動作することを意図しており、*.js ファイルと結合した *.wasm ファイルを生成し、wasmtime と互換性がありません。|
|wasm32-unknown-unknown|64 bit メモリ対応 [参考](https://doc.rust-lang.org/rustc/platform-support/wasm64-unknown-unknown.html)|

- [Writing WebAssembly - Rust](https://docs.wasmtime.dev/wasm-rust.html)

## はじめての Wasm - Hello World

というわけで、Wasm / WASI の開発・実行環境が出来上がりました。
ここでいつもの定番な **Hello World** を作って動かしてみます。

```shell
echo \
'fn main() {
    println!("Hello WebAssembly!");
}' > main.rs
```

コンパイルは、`--target` オプションで `wasm32-wasi` を指定して実行します。

```shell
rustc main.rs --target wasm32-wasi
```

以下のように Wasm バイナリが生成されます。

```shell
$ ls -l

-rw-r--r--  1 yanagiharas  staff       45 Sep 12 22:44 main.rs
-rwxr-xr-x  1 yanagiharas  staff  2041890 Sep 12 22:47 main.wasm*
```

これを、先にインストールしておいた `wasmtime` で実行してみます。

```shell
$ wasmtime main.wasm

Hello WebAssembly!
```

## Day 20 のまとめ

今日は Rust で **WebAssembly System Interface (WASI)** のバイナリを作って動かしてみました。
と言っても、Hello World なのでコンパイルの仕方と実行の仕方を確認したのみというのが実際確認できた内容です。

- WASI の 実装ランタイムの１つの `wasmtime` のインストール
- コンパイルターゲットの `wasm32-wasi` のインストール
- Hello World の作成
- Wasm バイナリの作成と、その実行

このようなことが確認できました。
ここまでのところでは特に難しいポイントはなかったと思うので、**Rust + Wasm** をもう少し深堀りすていってみたいなと思っています。
