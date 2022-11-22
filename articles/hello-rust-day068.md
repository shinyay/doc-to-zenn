---
title: "100日後にRustをちょっと知ってる人になる: [Day 68]Lintツール: Clippy"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 68 のテーマ
[Day 66](https://zenn.dev/shinyay/articles/hello-rust-day066) で **[Blessed.rs](https://blessed.rs/crates)** の紹介をしました。おすすめのクレートを紹介してくれているサイトでした。とはいえ、そこで紹介しているクレートは全く見ていなかったので、今後見ながら使い方を学んでいこうと思います。

![](https://storage.googleapis.com/zenn-user-upload/56c77826cbc7-20221122.png)

というわけで、Blessed.rs を開いて上から見ていこうとおもったのですけど、一番上は `rustup` で普通に使っている CLI だったのでその次の **clippy** について見ていきたいと思います。Lint ツールなので、Rust 初学者でない人達にとっては普通に使っているツールなのだろうと思いつつも、ぼくはまだ使ったことがないので改めて今回見てみたいなと思います。

## clippy

- [clippy](https://github.com/rust-lang/rust-clippy)

**clippy** は Blessed.rs ユースケースとしても説明されているように、**Linting** つまり Lint ツールや、Linter と呼ばれているプログラムコードの静的チェックツールです。Lint ツールに馴染みのない人向けに簡単に説明をすると、予め特定の言語の書き方に対するルールを定めておき、そのルールに対して記述しているコードを照らし合わせて適切なのかどうかをチェックしてくれるツールです。
例えば、次のような内容をチェックします。

- 型が一致しない関数を呼び出しているかどうか
- ソースコード内に未使用の変数が存在するかどうか
- 初期化されていない変数があるかどうか

など、プログラムコードとしてあるべき状態をチェックしてくれます。参考までに、Linter は Rust に限らず様々な言語で提供されているのでコーディングの効率をあげるという意味でも導入してもよいのではないでしょうか。また、PR を出す前に礼儀として linter でチェックはしておいた方がいいかもしれません。

### インストール

`rustup` により **clippy** とその依存関係をインストールすることができます。
すでにRustupがインストールされている場合は、最新の rustup とコンパイラにアップデートしてください。

```shell
rustup update
```

rustupと最新の安定版がインストールされたら、以下のコマンドを実行します。

```shell
rustup component add clippy
```

`cargo` のサブコマンドに追加されます。

```shell
$ cargo --list

Installed Commands:
  :
clippy               Checks a package to catch common mistakes and improve your Rust code.
  :
```

これで、以下のコマンドを対象のフォルダで実行することで clippy を使用できます。

```shell
cargo clippy
```

### clippy 実行例

次のような円の面積を求めるコードを書いているとします。

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("半径:{} の円の面積は {}",r , x * r * r);
}
```

```shell
$ cargo run

半径:8 の円の面積は 201.056
```

実行すると特に問題なく正常に動作します。このコードを `clippy` でチェックをすると次のようなエラーを出してくれます。

```shell
cargo clippy
```

```shell
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant

error: could not compile `day_68_clippy` due to previous error
```

円周率の値として、マニュアルで定めていた `3.1415` という値を判別して、正確な円周率の定数の存在を示してくれました。

情報として示されたリンク先も確認してみます。

- <https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant>

以下のようなコードの場合、

```rust
let x = 3.14;
let y = 1_f64 / x;
```

正確な定数として以下のような定義をしなさいとルール付けされていました。

```rust
let x = std::f32::consts::PI;
let y = std::f64::consts::FRAC_1_PI;
```

予め定められている定数の存在を知らないような場合、このように教えてくれるのはありがたいですね。
というわけで、アドバイスに従ってコードを以下のように書き換えます。

```rust
fn main() {
    let x = std::f32::consts::PI;
    let r = 8.0;
    println!("半径:{} の円の面積は {}",r , x * r * r);
}
```

これで `clippy` からのエラーはなくなりました。また、実行結果も当然ですがより正確な値になりました。

```shell
$ cargo run

半径:8 の円の面積は 201.06194
```

### clippy のルール

ところで、先程の clippy を実行したときに追加情報としてのリンクが表示されていました。

- <https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant>

ここの `index.html` を見ておこうと思います。

![](https://storage.googleapis.com/zenn-user-upload/37036c7d9892-20221123.png)

- [Clippy Lints](https://rust-lang.github.io/rust-clippy/master/index.html)

ここに様々な定義済みのルールが記載されています。現在 550 を越えるくらいのルールがあるようです。

定義されているルールを全部を予め見ておくことは、なかなか難しいと思うので今後コードを書いていく中で毎回 `clippy` でチェックしながら覚えていこうと思います。

## Day 68 のまとめ

Rust の Lint ツールな `clippy` をインストールして使ってみました。
正しいコードの書き方を覚えていくことは大事だと思うので、Rust を学び始めている今からも積極的にコードチェックをしながら覚えていきたいと思います。

また、今はまだ CI を使うほどのコードを書いてはいないのですが、**Travis CI** の中で `clippy` を使用する方法も紹介されていました。

- <https://github.com/rust-lang/rust-clippy#travis-ci>

今後使ってみたいかなと思います。
