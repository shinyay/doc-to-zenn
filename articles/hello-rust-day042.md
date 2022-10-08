---
title: "100日後にRustをちょっと知ってる人になる: [Day 42]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 42 のテーマ

[Day 41](https://zenn.dev/shinyay/articles/hello-rust-day041) では、**幽霊型 (Phantom Type)** という僕もあまり慣れない書式について見てみました。

そこで、幽霊型を使っている構造体から作ったオブジェクトの比較を行い、使わない型パラメータを仕込んでおくことにより異なる型として扱えることを見てみました。

そのオブジェクト同士の比較をするときなのですが、実は昨日は全く説明していないコードを記載していました。
これです

```rust
#[derive(Debug,PartialEq)]
```

これをどこで使っていたかというと、幽霊型を用いていた構造体の宣言時に使っていました。

```rust
#[derive(Debug,PartialEq)]
struct PhantomStruct<X, A> {
    value: A,
    phantom: PhantomData<X>
}
```

これは `derive` という属性を構造体に付与して、`derive` が提供している性質によって `Debug` と `PartialEq` という振る舞いを追加していたのです。

実はこの `derive` は Rust の**手続きマクロ**の一種になります。Rust にはマクロの定義の仕方が複数あります:

- 宣言型マクロ
- 手続き型マクロ
  - カスタム Derive マクロ
  - 属性型マクロ
  - 関数型マクロ

マクロ１つのとっても奥が深いです…

## Day 42 のまとめ

