---
title: "100日後にRustをちょっと知ってる人になる: [Day 62]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 62 のテーマ

[Day 61](https://zenn.dev/shinyay/articles/hello-rust-day061) でお伝えしたように、6 週間ごとのリリースサイクルの中、11/3 に Rust `1.65` の **Stable** 版が公開されます。

昨日は、その 1.65 で対応するアップデート一覧を列挙しましたが、つまりは列挙しただけで理解できない項目が多く、まだまだ Rust 力が足らないと改めて認識したのでした笑。これを糧にもっと知ってる人になろうと思えるわけで、6 週間ごとに自分を見つめ直せるのはいいことかなと前向きに思ったのでした。

さて、その数多くの `1.65` のアップデートの中でも一番注目を浴びている内容は抑えておきたいと思うので、それを今日は見てみたいと思います。

## Generic Associated Types (GATs)

日本語では、**汎用関連型** と呼ぶものだと思われる **Generic Associated Types (GATs)** が今回のアップデート内容の中で **待望**と言われいるくらいのものです。

- [汎用関連型 (Generic Associated Types) の安定化](https://github.com/rust-lang/rust/pull/96709/)

この Generic Associated Types ですが、調べて見ると最初に Request for Comments (RFC) が開設されから既に 6 年も経っていたようです。たしかに待望と言われるのがわかります。

- **[RFC: Generic associated types (associated type constructors)](https://github.com/rust-lang/rfcs/pull/1598)**

### RFC: Generic associated types (associated type constructors)

少し RFC を見てみます。

サマリ:

> 型コンストラクタをトレイトと関連付けることができるようになりました。これは、Rust ユーザーの間で要望の多い "上位互換の型" と呼ばれる一般的な機能への段階的なステップです。この機能（関連型コンストラクタ）は、上位概念に関する最も一般的なユースケースの1つを解決するもので、他の上位概念ポリモフィズムに比べると比較的単純な拡張です。また、将来導入されるかもしれないより複雑な上位のポリモフィズムとの前方互換性があります。

次のトレイトを見てみます。

```rust
trait StreamingIterator {
    type Item<'a>;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
```

`next` に渡された参照のライフタイムに関連したライフタイムを持つイテレータの生成を可能にするようなものになっています。標準的な Iterator インターフェースを使用すると、このような実装は無効です。なぜなら、各スライスは next によって開始された借用と同じ期間ではなく、iterator と同じ期間だけ存在する必要があるためです。
これは、現在の Rust では表現することができません。

## Generic associated types とは

**Generic associated types** は、関連型に対して Generics をもたせることを可能にしたものです。
つまり、トレイト (関連型) の中のエイリアスに Generics をもたせる事ができるようになります。

### 現状での制約

次の記事に現時点で公開される **Generic associated types** の制約事項が記載されていました。

- [Generic associated types to be stable in Rust 1.65](https://blog.rust-lang.org/2022/10/28/gats-stabilization.html)

制約事項だけでなく、バグもまだ含まれていることが書かれています。

> We plan to fix these bugs and remove these limitations as part of ongoing efforts driven by the newly-formed types team. (Stayed tuned for more details in an official announcement soon!)

- [Implied 'static requirement from higher-ranked trait bounds](https://blog.rust-lang.org/2022/10/28/gats-stabilization.html#implied-static-requirement-from-higher-ranked-trait-bounds)
- [Traits with GATs are not object safe](https://blog.rust-lang.org/2022/10/28/gats-stabilization.html#traits-with-gats-are-not-object-safe)
- [The borrow checker isn't perfect and it shows](https://blog.rust-lang.org/2022/10/28/gats-stabilization.html#the-borrow-checker-isnt-perfect-and-it-shows)
- [Non-local requirements for where clauses on GATs](https://blog.rust-lang.org/2022/10/28/gats-stabilization.html#the-borrow-checker-isnt-perfect-and-it-shows)

## Day 62 のまとめ

関連型に対して Generics をもたせることができるようになったのはとても便利だと思います。
一方で、ここに上げられているバグや制約事項に対して、どういう時に遭遇するのかが想像できず、まだ理解が追いついていないのが実体です。`1.65.0` 公開後に、Rustaceans のレビューなど見つつ勉強したいと思います。
