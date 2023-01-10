---
title: "100日後にRustをちょっと知ってる人になる: [Day 98]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 98 のテーマ

**100日後にRustをちょっと知ってる人になる** と銘打って勉強しはじめた Rust ですが、ほんの少しは分かってきたと思います。とは言え、どんな技術も同じだと思いますが学び続けることと、使い続けることが知識と経験の習得には欠かせないと思っています。100 日までのあと 3 回の中でこれからの Rust の学習の仕方などを考えていこうと思います。

## あらためて Rust についての振り返り

この 約 100 日の間に Rust について言語仕様やサードパーティを含めたエコシステム、またアプリケーションの作り方など様々な観点で学習してきました。それらを通して Rust のいいところについて考えてみました。

### 高レベルでのいいところ

セキュアなプログラム言語とよく言われているので、メモリの取り扱い周りはもちろんなのですけど実際にアプリケーションを書いていく上でも便利な点があると思いました。

- ✅ [メモリの安全性](https://doc.rust-lang.org/nomicon/meet-safe-and-unsafe.html)
- ✅ [トレイト（オブジェクト指向のインターフェース的な機能）](https://doc.rust-lang.org/book/ch10-02-traits.html)
- ✅ 関数パターン
  - [コンビネータ](https://doc.rust-lang.org/rust-by-example/error/option_unwrap/map.html)
  - [イテレータ](https://doc.rust-lang.org/book/ch13-02-iterators.html)
  - [パターンマッチング](https://doc.rust-lang.org/book/ch18-00-patterns.html)
- ✅ [メモリの自動 Drop](https://doc.rust-lang.org/std/ops/trait.Drop.html)
- ✅ [簡単なマルチスレッドライブラリ](https://lib.rs/concurrency)
- ✅ [マクロ拡張(言語のシンタックスを自由に拡張可能)](https://doc.rust-lang.org/book/ch19-06-macros.html)

これらの点は一部だと思いますが、それでも高レベルな観点で Rust のいいところを紹介する代表的な特徴だと思います。

### 低レベルでのいいところ

Rust 自体は高水準言語として位置づけられていますが、低水準の操作までもサポートしています。

- ✅ [メモリポインタ](https://doc.rust-lang.org/std/primitive.pointer.html)
- ✅ [コンパイラ](https://rustc-dev-guide.rust-lang.org/about-this-guide.html)
- ✅ 組み込みでの動作可能

このように高レベルから低レベルのコンピュータの挙動を操作することができる言語として、またそれを安全に構築することができるという点で Rust を利用するメリットがあると思っています。

## Rust の人気

年々 Rust の人気が高まってきているのは、様々な記事などを見ていると感じるところはあるのではないでしょうか。実際、[Stack Overflow](https://survey.stackoverflow.co/2022/#section-most-loved-dreaded-and-wanted-programming-scripting-and-markup-languages) の調査では、7 年連続で最も愛されているプログラム言語に選ばれています。
しかし、なぜこのように Rust の人気が高まってきているのでしょうか。先に書いた Rust のいいところという点ももちろんありますけれど、それ以上にいろいろな観点があって人気と需要がでてきているのだと思います。

プログラム言語として一般的に人気がでる観点としては次のようなポイントがあると思います。

- 簡潔な言語仕様

## Day 98 のまとめ
