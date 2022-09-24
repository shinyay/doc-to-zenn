---
title: "100日後にRustをちょっと知ってる人になる: [Day 32]クロージャ"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 32 のテーマ

[Day 31](https://zenn.dev/shinyay/articles/hello-rust-day031) では、Rust の関数 (**関連関数**と**メソッド**) について見てみました。
今日はもう 1 つの関数の使い方の**クロージャ**について見てみようと思います。

### クロージャとは

Rust に限らず、いろいろな言語でも クロージャは提供されています。クロージャを使ったコーディングはいろいろなところで活用されてきていると思います。

- [Java](https://openjdk.org/projects/closures/)
- [Kotlin](https://kotlinlang.org/docs/lambdas.html#closures)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)

しかし、一方でクロージャとは何か？のような説明もあちこちで見かけたりしますよね。日本語で **[関数閉包](https://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%83%BC%E3%82%B8%E3%83%A3)** などとされているので分かりにくいのだと思います。簡単に説明すると、変数に束縛できて、関数の引数として渡すことができ名前のない関数 (**無名関数**) のことです。また、関数と異なり、クロージャはその呼び出し元のスコープにある変数をキャプチャすることも出来ます。
つまり、クロージャを使うと以下のような性質で関数が使えることになります。

✅ 生成や代入が可能な関数となる
✅ 引数や戻り値として受け渡しておき、あとから呼び出せる
✅ あとから呼び出した場合、定義した時点で有効な定数や変数にアクセスできる

### Rust でのクロージャ



## Day 32 のまとめ
