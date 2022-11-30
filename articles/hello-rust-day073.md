---
title: "100日後にRustをちょっと知ってる人になる: [Day 73]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 73 のテーマ

**[Blessed.rs](https://blessed.rs/crates)** で紹介されているクレートについて今日も見てみたいと思います。この 1 週間 **Blessed.rs** 見てきているので、Blessed.rs で紹介されているクレートに関心を持った人もいるのではないでしょうか。

![](https://storage.googleapis.com/zenn-user-upload/76cc64f215c6-20221129.png)

いろいろと見てはきていますが、Day 68 〜 Day 72 ではクレートはクレートでも `cargo` コマンドのサブコマンドとして使用するツールを見てきました。ここで趣向を少し変えて、Rust の標準ライブラリとして提供されていないので提供されるクレートを用いて補完するようなものを見てみたいと思います。

そこで、まず今回は**乱数生成**について見ていこうと思います。

## 乱数生成

Rust 以外の言語、例えば **Java** であれば乱数を生成するときには、標準 API で `java.util.Random` や `Math.random()`、また **Kotlin** であれば `kotlin.random.Random` のようの提供をしています。しかし、Rust では標準ライブラリから乱数を生成する機能を提供していないのです。

そこで、Rust で乱数を生成するときに使用するためには、Rust 開発チームから提供されているクレートの **rand** を使用します。

- [rand](https://docs.rs/rand/latest/rand/)
  - [GitHub リポジトリ](https://docs.rs/rand/latest/rand/)

ところで、乱数生成と言っていますが、ここで言っている乱数生成は正確には**疑似乱数生成器 (PRNG - Pseudo Random Number Generators)** のことなのですよね。ソフトウェア上でプログラムにより生成される乱数は、真の意味ではランダムではなくて、とある分布に基づいたアルゴリズムによって生成されているもののことを言います。
では、真の意味での乱数生成は？と、疑問に思われるとおもいますが、それは**真性乱数生成器 (TRNG - True Random Number Generators)** と呼ばれています。これはアルゴリズムに従っているようなものではなく、同位体の放射性崩壊や電波静的など、予測できない外部の物理変数を使用して乱数の生成を行っています。
つまり、プログラムで扱っている乱数生成のほぼ全て、**PRNG** だと思っていれば間違いありません。

ちなみに、他の言語ですが、Java の乱数生成のドキュメントでも、**PRNG** として説明がされています。

- [Java による乱数](https://docs.oracle.com/en/java/javase/17/core/pseudorandom-number-generators.html)

それでは、`rand` による疑似乱数生成器については、以下に記述がありました。

- [Our RNGs](https://rust-random.github.io/book/guide-seeding.html)

ここを見てみると、**rand** には、疑似乱数生成器 (PRNG) と 暗号論的疑似乱数生成器 (CSPRNG) があるようです。この 2 つの異なる点は乱数に対するセキュリティ、性能、メモリ使用量、などの観点での考え方のです。乱数に対する品質を重要視すると性能が落ちてしまうようなトレードオフが発生します。暗号論的擬似乱数生成器は性能よりもセキュリティを重要視しているアプローチです。一方で通常の疑似乱数生成器は、バランスを重要視したものになります。

## rand クレート

それでは実際に rand クレートを使用した乱数の生成について見てみます。

- [rand v0.8.5](https://crates.io/crates/rand/0.8.5)

この文書を書いている今日 (2022.11.30) 時点での rand の最新バージョンは `0.8.5` です。以下のように依存関係を `Cargo.toml` に追加します。

```toml
[dependencies]
rand = "0.8.5"
```

まずは一番シンプルな乱数の生成の仕方を見てみます。

```rust
let mut rng = rand::thread_rng();
```

`thread_rng()` によって、スレッドローカルな疑似乱数生成器を初期化します。そして、次に `Rng` トレイトに定義されている `gen()` メソッドによって標準分布に対応した乱数値を取得します。

- [Rng トレイト](https://docs.rs/rand/0.8.5/rand/trait.Rng.html)

```rust
let x: i32 = rng.gen();
```

## Day 73 のまとめ
 