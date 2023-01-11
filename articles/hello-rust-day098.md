---
title: "100日後にRustをちょっと知ってる人になる: [Day 98]Rust に対する魅力と今後の期待"
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
- コンパイラによる最適化
- 移植性
- エラー検出

簡潔な言語仕様という観点は Rust には学習曲線がやや厳しいというように見られているところもあるので、当てはまりにくいところもあるかもしれません。一方で、一旦習得してしまうとかゆいところに手が届くとも言われているので、ある段階の壁を越えると一気に便利さを感じるかもしれません。
とすると、やはり人気となってくる理由としてあがってくるのは、最適化やエラー検出といった優れたコンパイラの動作の観点は強く影響しているのかもしれません。

実際、ぼくもコードを書いて、コンパイルをして、エラーを見ながらコードを修正する、といったテストドリブン開発ならぬ、コンパイルエラードリブン開発のようなことをしながら Rust の学習をしていました。

実際、コンパイルエラードリブン開発と読んでいる人たちもいるようでした。

- [reddit: Compiler Error Driven Development](https://www.reddit.com/r/rust/comments/q8t2uk/compiler_error_driven_development/)

難しい言語だとしても、習得していくための環境が整っているのが Rust のいいところ言えるかもしれません。

## Rust の安全性

安全なアプリケーション開発ができるという謳い文句になっている Rust の背景にあるのは、1 つには先に述べたようなメモリの扱いに関する安全性があると思います。
Java や Python などの言語に採用されているガベージコレクションのように、プログラムを組む側が意識しないところで動作するのは便利な反面、コントロールしきれないという悩みも出てしまいます。そのため、実際に実行している際に発生するオーバーヘッドをある程度許容する必要がでてきます。
Rust では、その C や 初期の C++ のように `malloc` や `free` など用いてメモリ領域の確保から開放までを自らコントロールするまでではないのですが、自分でメモリをコントロールするという手段をとっている、次のようなアプローチが斬新だと思いました。

1. Rust上に存在する「**値**」は「**変数**」に格納され、その変数を、その値の「**所有者**」と呼ぶ
2. **値**の**所有者**になれる変数は、あるタイミングで **1 つのみ**
3. **所有者**である変数が「**スコープ**」を出た時に、その値は利用できなくなる

このシンプルだけど、厳密なルールによってメモリの安全性を担保しています。
これが、低レベルで透過的に行われているのではなく、プログラマチックに開発者が自らのコードでコントロールすることができる点が Rustを安全かつ人気とさせている理由にもなっているのではないかなと思います。

## 2023 年、そして今後の Rust

最後に Rust に対する観測的希望ようなコメントになりますが、今年 2023 年は今まで以上に Rust が脚光を浴びる 1 年になってくるのではないかなと思っています。

昨年、Linus Torvalds が発表されていたように、Linux 6.1 のメインライン開発ではじめて Rust が採用されました。いわゆる低レベルの開発として機能を発揮した成果の 1 つとも言えると思います。

- [Linux 6.1 by Linus Torvalds - 11 Dec 2022](https://lkml.org/lkml/2022/12/11/206)

また、昨年ふたたび注目を集め始めた **WebAssembly** の動向の中でも Rust は注目を集めていますよね。

- [Web­Assembly](https://www.rust-lang.org/what/wasm)

さらに マイクロサービスアーキテクチャも Rust を用いて実現する話も昨年は見え始めてきていました。

- [Microservices with Rust and WASM using Fermyon](https://medium.com/@shyamsundarb/microservices-with-rust-and-wasm-using-fermyon-30245673cdbb)
- [Building Microservices With WebAssembly and Fermyon Spin](https://www.thorsten-hans.com/building-microservices-with-webassembly-and-fermyon-spin/)
- [Rust microservices in server-side WebAssembly](https://blog.logrocket.com/rust-microservices-server-side-webassembly/)

このように様々なところで Rust の活用が目に見えてくることが増えてくるのではないかなと期待しています。

## Day 98 のまとめ

今回は、ほぼポエムような内容になってしまいましたが、この 約 100 日の Rust の学習を通して気づいてきた魅力と、これからの期待などについて書いてみました。
このような期待を書いている時点で分かると思いますが、この 100 日が終わっても僕の Rust の学習はまだまだ終わらないです。
そもそも、100日後にRustを**ちょっと知ってる**人になる、なので全然まだまだなレベルなのですから。
