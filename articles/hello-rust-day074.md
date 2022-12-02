---
title: "100日後にRustをちょっと知ってる人になる: [Day 74]日時操作: time"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 74 のテーマ

[Day 73](https://zenn.dev/shinyay/articles/hello-rust-day073) では、**乱数**を扱うクレートについて見てみました。そこでも少しふれましたけれど、他のプログラム言語であれば標準ライブラリで提供していそうな乱数の機能が Rust ではないということに驚いていました。また、今回もいかにも標準ライブラリで提供していそうな**日時**を扱う機能について見てみたいとおもっています。

また別の言語のことですが、Java では日時計算を行う時に利用する API として、[Date and Time API](https://docs.oracle.com/javase/8/docs/technotes/guides/datetime/index.html) が標準 API として提供されています。
このように、他のプログラム言語の経験者からすると標準ライブラリで充実した機能が提供されていないことに違和感を持ってしまうかもしれないですよね。

僕自身標準提供されている API を知るということよりも、多くのクレートで何ができるかを知っていくことも大事だと思っているところです。逆に考えれば、それだけ Rust の場合はエコシステムが広がりを見せてきているのかもしれないのかなと感じていたりします。とは
言っても、クレートをいろいろと覚えていかなければならないので学習範囲は広がりそうですけどね。

というわけで、今日は**日時**を扱う **time** というクレートを見ていきたいなと思います。

## time

日時を扱うクレートで代表的なものには、**time** と **chrono** という 2 つがあるようです。今日は **time** について使い方を学びたいなと思います。

以下が、**time** クレートに関するプロジェクトやドキュメントへのリンクです。

- [time (crate.io)](https://crates.io/crates/time)
- [lib.rs](https://lib.rs/crates/time)
- [GitHub](https://github.com/time-rs/time)
- [Book - time](https://time-rs.github.io/book/)
- [docs.rs](https://docs.rs/time/latest/time/#)

**Book** 中心にして **time** について見てみたいと思います。

まず最初に謳い文句として特徴についてです。

- **簡単・安全**
  - わかりやすい API 提供しているそうです。
    - たしかに、[time::OffsetDateTime](https://time-rs.github.io/api/time/struct.OffsetDateTime.html) で提供しているメソッドを見てみると、例えば **UTC時間での取得**や**日曜日から始まる週番号の取得**など直感的にやりたいことを実施できるようなメソッドなどが用意されていそうです。

- **最適化・効率化**
  - `time` は、ナノ秒の精度で **±9999** 年の範囲の日付をサポートしています。
  - さらに大きな範囲で、**±999,999** までの範囲は、`large-dates` 機能でサポートされています。
    - [time - Feature flags](https://docs.rs/time/latest/time/index.html#feature-flags)

- **シリアライズ・デシリアライズ**
  - シリアライゼーションするデファクトなフレームワークの `serde` に対応ということを銘打っています
  - [serde](https://crates.io/crates/serde)
    - (まだ使ったことないです)

- **マクロ**で簡単に日付を作成
  - [time::macros](https://time-rs.github.io/api/time/macros/index.html)

- Windows、Linux、macOS、WebAssemblyターゲットなどをサポート

## 使い方

それではとにかく使ってみます。

まず依存関係を `Cargo.toml` に追加します。
ちなみに、今日時点の最新バージョンは [v0.3.17](https://crates.io/crates/time/0.3.17) でした。
また、ここでは、`macros` フィーチャーを有効にしています。

```shell
cargo add time --features macros
```

:::details コマンド実行結果
```shell
    Updating crates.io index
      Adding time v0.3.17 to dependencies.
             Features:
             + alloc
             + macros
             + std
             - formatting
             - large-dates
             - local-offset
             - parsing
             - quickcheck
             - rand
             - serde
             - serde-human-readable
             - serde-well-known
             - wasm-bindgen
```
:::

```toml
[dependencies]
time = { version = "0.3.17", features = ["macros"] }
```

次に UTC 時間を取得する `now_utc` メソッドで現在時間を取得してみます。

```rust
use time::OffsetDateTime;
fn main() {
    let now = OffsetDateTime::now_utc();
    println!("Hello, world at {:?}", now);
}
```

実行結果:

```shell
Hello, world at 2022-12-01 23:49:32.605876 +00:00:00
```

簡単に日時を取得できたことが分かると思います。
こうなると次は現地時間 (ここでは日本時間) を取得したくなりますよね。その場合は、次のフィーチャーを有効にします。

- `local-offset`

```toml
[dependencies]
time = { version = "0.3.17", features = ["macros", "local-offset"] }
```

そして、`now_utc` メソッドを `now_local` メソッドに変更するのみです。

```rust
    let now = OffsetDateTime::now_local();
    println!("Hello, world at {:?}", now);
```

特徴としても言われているように日時取得がかなり簡単にできることが分かります。

## いろいろな日時

日時に関する構造体がいろいろとあるのを見つけました。

- [time::Date](https://docs.rs/time/latest/time/struct.Date.html)
- [time::Time](https://docs.rs/time/latest/time/struct.Time.html)
- [time::OffsetDateTime](https://docs.rs/time/latest/time/struct.OffsetDateTime.html)
- [time::PrimitiveDateTime](https://docs.rs/time/latest/time/struct.PrimitiveDateTime.html)

### time::Date

この型は、グレゴリアン暦における日付で使用します。

```rust
let date = Date::from_iso_week_date(2022, 48, time::Weekday::Friday).unwrap();
```

また、マクロから次のように簡単に `Date` を作成できます。

```rust
let _ = date!(2022-12-01);
```

### time::Time

`Time` では、とある日付内の時刻表現を担当しています。その精度はナノ秒で行われます。

```rust
let datetime = date.with_hms(11, 22, 33).unwrap();
```

### time::PrimitiveDateTime

日付と時刻を組み合わせたものです。

```rust
let date = Date::from_iso_week_date(2022, 48, time::Weekday::Friday).unwrap();
let datetime: PrimitiveDateTime = date.with_hms(11, 22, 33).unwrap();
```

日時間隔の計算も直感的に行うことができます。

```rust
let start = datetime!(2022-01-01 0:00:00);
let end = datetime!(2022-12-31 23:59:59);
let duration = end - start;
```

ここで使用している `datetime!` は `PrimitiveDateTime` 型の日時を作成するマクロです。

## Day 74 のまとめ

**time** クレートを使うことにより、日付表現を簡単に行うことが分かりました。かなり直感的に日付捜査ができるので日々使いながらもっといろいろな機能に見つけ慣れていきたいと思うクレートでした。
