---
title: "100日後にRustをちょっと知ってる人になる: [Day 63]RustConf 2022 を見る"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 63 のテーマ

先週はじつはまるっと KubeCon + CloudNativeCon を夜な夜なみていたのですが、技術系カンファレンスって見るのは楽しいですよね。新しいこと、知らなかったことを学べるいい機会だと思ってあちこちみています。KubeCon 併設カンファレンスの WasmDay もありましたしね。

と、ふと思ったのが Rust に関するカンファレンスもきっとありますよね？ってことでした。そういえば、Rust を学び始めて間もないので Rust 関連のカンファレンスについて見たことも調べたこともなかったのです。というわけで、今回 Rust のカンファレンスについて見てみたいと思います。

## RustConf

調べめてみたら、ありました。（まあ、当然ですよね…）

**RustConf** というカンファレンスが大体毎年 8 〜 9 月くらいに開催されているようです。それも、2016 年から開催されていたんですね。Rustaceans な皆さん、本当にすみません、全く知りませんでした…

- [RustConf](https://rustconf.com/)

以下、過去のカンファレンスサイトです。

- [RustConf 2016](http://2016.rustconf.com/)
- [RustConf 2017](http://2017.rustconf.com/)
- [RustConf 2018](http://2018.rustconf.com/)
- [RustConf 2019](http://2019.rustconf.com/)
- [RustConf 2020](http://2020.rustconf.com/)
- [RustConf 2021](http://2021.rustconf.com/)

それと、録画された動画の再生リストもこちらにありました。

- [RustConf 2016](https://www.youtube.com/playlist?list=PL85XCvVPmGQgoU1-KQGUaQk_YRFDE1P8y)
- [RustConf 2017](https://www.youtube.com/playlist?list=PL85XCvVPmGQhUSX_QBkxb4g1-o56cCqI9)
- [RustConf 2018](https://www.youtube.com/playlist?list=PL85XCvVPmGQi3tivxDDF1hrT9qr5hdMBZ)
- [RustConf 2019](https://www.youtube.com/playlist?list=PL85XCvVPmGQhDOUIZBe6u388GydeACbTt)
- [RustConf 2020](https://www.youtube.com/playlist?list=PL85XCvVPmGQijqvMcMBfYAwExx1eBu1Ei)
- [RustConf 2021](https://www.youtube.com/playlist?list=PL85XCvVPmGQgACNMZlhlRZ4zlKZG_iWH5)
- [RustConf 2022](https://www.youtube.com/playlist?list=PL85XCvVPmGQhXeH3QiYct6eMLH1un1dcu)

一気に 追いかける対象の動画コンテンツが積ん読ならぬ、積ん見になってしまいました。

## RustConf 2022 - 基調講演 by Josh Triplett and Tyler Mandry

というわけで、RustConf 2022 - 基調講演 を見てみようと思います。

https://www.youtube.com/watch?v=37yASSgrdGE&list=PL85XCvVPmGQhXeH3QiYct6eMLH1un1dcu

(現在視聴中… 感想は後ほど)

###

![](https://storage.googleapis.com/zenn-user-upload/5e6c596f0fa0-20221111.png)

エラーハンドリングに関する Crate や、スタンダードライブラリの中でのエラーハンドリングの進化に関する説明が行われます。

- [Error](https://doc.rust-lang.org/beta/core/error/trait.Error.html)
- [Crate failure](https://docs.rs/failure/latest/failure/)
  - `failure` は非推奨です。`failure` のAPIが好きだった人は、以下の利用を検討してみてください。
  - [Crate anyhow](https://docs.rs/anyhow/1.0.66/anyhow/)
    - `failure::Error` の良い代替
  - [Crate thiserror](https://docs.rs/thiserror/1.0.0/thiserror/)
    - `#[derive(Fail)]` をほぼそのまま置き換え可能
- [Crate eyre](https://docs.rs/eyre/latest/eyre/)

![](https://storage.googleapis.com/zenn-user-upload/938ef05fe0e9-20221116.png)
![](https://storage.googleapis.com/zenn-user-upload/2ecbe147fdc8-20221116.png)
![](https://storage.googleapis.com/zenn-user-upload/2f79f0a61c9b-20221116.png)
![](https://storage.googleapis.com/zenn-user-upload/6a5a0ef9d1f6-20221116.png)
![](https://storage.googleapis.com/zenn-user-upload/bdd3b0edabee-20221116.png)

エラーハンドリングの進化の中で見て分かるように標準ライブラリに昇格したり、Crate で提供したりと様々な実現方法がありました。そこで多くの人はなぜ１つの標準方式で行わないのだろうと考えると思います。答えとしては、Rust はエコシステムともに進化するということをコンセプトにしているからなのです。

![](https://storage.googleapis.com/zenn-user-upload/d99fd425f3cf-20221116.png)

Rust の構造としては、アプリケーションを作るために言語仕様そのものや標準ライブラリなどがファンデーションとしてありますが、それだけではなく実験的に開発された Crate とそれがいろいろと使われてフィードバックのもと修正され確立された Crate などがアーキテクチャの礎になっています。

![](https://storage.googleapis.com/zenn-user-upload/a8c4c537cd35-20221116.png)

このアーキテクチャを支える要素の進化は継続的に行われます。アプリケーションの中で実験的な Crate が試されテストされてフィードバックを得てそこから改善されて、Rust の標準ライブラリの言語仕様に含まれたり、確立された Crate されていきます。

![](https://storage.googleapis.com/zenn-user-upload/bb486048ed03-20221116.png)

堅牢なシステムを気づくためには、ミスをしない人だけで開発するのではなくて、ミスを見つけたりあるいは発生しないようにするためのツールやプロセスも併せて必要になってきます。

![](https://storage.googleapis.com/zenn-user-upload/94d153382295-20221108.png)
![](https://storage.googleapis.com/zenn-user-upload/2363d3ec2f73-20221116.png)



## Day 63 のまとめ

RustConf のコンテンツ、アジェンダだけざっと見てみましたけど、なんだか良さそうでした。追いかけてみていこうと思います。
あと、毎年オレゴン州のポートランドでこの RustConf は開催されているみたいです。ポートランドといえば、アメリカの中でも住みたい都市ランキングで必ず上位に入っているところです。まだ行ったことがないので、来年あたりタイミングが合えば行ってみたいなって思いました。

基調講演の内容については後ほど振り返りで記載したいかなって思います。
