---
title: "100日後にRustをちょっと知ってる人になる: [Day 73]乱数: rand"
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

10 回実行してみましたが、以下のようにランダムに数値が作成されていることが確認できます。

```shell
1: 1900450494
2: -608434321
3: -1802545885
4: -1866374950
5: 310430532
6: -799121282
7: -1903150211
8: 1267047284
9: 974367032
```

### モジュール

**rand** には次のようなモジュールがあります。

- **distributions**: 確率分布に基づいて乱数を生成する昨日を提供
- **rngs**: 乱数生成器を提供
- **seq**: シーケンスに関連した乱数生成機能を提供

#### distributions

- [Standard](https://docs.rs/rand/0.8.5/rand/distributions/struct.Standard.html)
- [Alphanumeric](https://docs.rs/rand/0.8.5/rand/distributions/struct.Alphanumeric.html): ASCII文字と数字（a-z, A-Z, 0-9）に一様に分布するu8をサンプリング
- [Uniform](https://docs.rs/rand/0.8.5/rand/distributions/struct.Uniform.html): 2つの境界の間で一様に値をサンプリング

`Alphanumeric` を用いたランダムな文字列生成

```rust
let chars: String = (0..7).map(|_| rng.sample(Alphanumeric) as char).collect();
println!("ランダムキャラクター{}: {}", n, chars);
```

`Uniform` を用いた数値間からのランダムな数値選択

```rust
let between = Uniform::from(10..10000);
println!("{}", between.sample(&mut rng));
```


#### rngs

次のような乱数生成器を提供しています。

- **OsRng**
  - オペレーティングシステムが提供する乱数へのインターフェース
- **ThreadRng**
  - スレッドローカルな CSPRNG
- **StdRng**
  - 性能の良さと安全性の信頼性（レビュー、成熟度、使用状況などから）から選ばれたCSPRNG
- **SmallRng**
  - 安全でない PRNG であり、高速でシンプル、必要なメモリ量が少なく、出力品質が高くなるように設計

#### seq

以下のような昨日を提供していまします。

- **SliceRandom**
  - スライスに関するトレイトで、シャッフルや要素の選択などに関するメソッドを提供
- **IteratorRandom**
  - イテレータに実装されているトレイトで、1つまたは複数の要素を選択するためのメソッドを提供
- **index::sample**
  - 0 〜 length の範囲からランダムに異なる量のインデックスを抽出し、ランダムな順序で完全にシャッフルして返す

##### SliceRandom

`choose` メソッド: ランダムな要素への参照

```rust
let choices = [1, 2, 4, 8, 16, 32, 64, 256];
println!("{}, {:?}",n, choices.choose(&mut rng));
```

`shuffle` メソッド: スライスを所定の位置でシャッフル

```rust
let mut y = [1, 2, 3, 4, 5];
println!("シャッフル前: {:?}", y);
y.shuffle(&mut rng);
println!("シャッフル後: {:?}", y);
```

## Day 73 のまとめ

今日は、Blessed.rs で紹介されているクレートの中から乱数を生成するための機能を提供している `rand` について見てみました。
単純に乱数を発生させるだけではなくて、乱数を発生させるための乱数生成器が充実していたり、またシードの生成から分布の扱いまで低レベルなところから乱数をコントロールすることができることが分かりました。

Rust の標準ライブラリ自体には乱数を扱う機能がないということなので、この [rand](https://crates.io/crates/rand/0.8.5) はいろいろなところで活用することがありそうなクレートだと思いました。

- [rand (carate.io)](https://crates.io/crates/rand)
- [rand (docs)](https://docs.rs/rand/0.8.5/rand/#)
- [rand (lib.rs)](https://lib.rs/crates/rand)