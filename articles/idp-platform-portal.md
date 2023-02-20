---
title: "IDP: 内部開発者プラットフォームと内部開発者ポータル"
emoji: "⚡"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [platform, platformengineer]
published: false
---
![](https://storage.googleapis.com/zenn-user-upload/10dc59576b4e-20230209.png)

## TL;DR

先日、"Platforn Engineering" が盛り上がってきていますよね、というような紹介と僕のもつ理解について記事に簡単にまとめました。

- [プラットフォームエンジニアリング (Platform Engineering) とは？](https://zenn.dev/shinyay/articles/what-is-platform-engineering)

その記事の中で、詳しくは触れていなかった **IDP** についての自分の理解を紹介していきたいと思います。
ここで、IDP を **Internal Developer Platform** と記述しなかったのは、前回も記載していたように IDP と略して Internal Developer **Portal** 、あるいは Internal Developer **Platform** を意図しているものがあるからです。これは意図的に分けて定義をしている文章もあれば、その説明文章を書いている製品ベンダーが提供している製品が**プラットフォーム**なのか**ポータル**なのかという理由だったりもしそうです。

ですが、Gartner の記事を読んでいても **Internal Developer Platform** と **Internal Developer Portal** は異なる要件・用途として別々に定義がなされていたりします。
そこで整理の意味を兼ねて **Internal Developer Platform** と **Internal Developer Portal** についてきょうはまとめたいと思います。

### 注釈

前回も記載していたように、Platform Engineering は明確な定義がまだ存在しているものではありません。**Gartner** が言っていたり、**Humanitec** などの Platform Engineering 製品を提供しているベンダーのエンジニアが言っているものはあるのですが公式の団体が定義しているものはまだありません。
ですので、ここで紹介する僕の理解も現状の理解であり、今後変わっていくこともあることを了承ください。

## Internal Developer Platform と Internal Developer Potal の関係

まず最初に、結論的な理解を伝えたいと思います。
**Internal Developer Platform** と **Internal Developer Portal** という 2 つの **IDP** が存在しているわけなのですが、どのような関係にあるかということです。
名前からピンとくる方も多いと思います。一方は**プラットフォーム**、もう片方は**ポータル**です。
プラットフォームの方は、ファウンデーション (土台) なイメージを名前から感じますよね。
ポータルの方は、UI というイメージを感じませんか。

そのイメージで 8 割正しいと思っています。

![](https://storage.googleapis.com/zenn-user-upload/861c02c171a9-20230220.png)

開発者が直接操作するフロントエンド側に **Internal Developer Portal** があり、そこからバックエンドで動作している **Internal Developer Platform** に対してアクセスするというものです。ここの関係の中で、忘れてはいけないのが **Internal Developer Platform** のさらに背後に**基盤**が存在していることです。つまり、"ポータルがプラットフォームを操作"し、"プラットフォームが基盤を操作する"というような構図になっているということです。

それでは、**Internal Developer Platform** と **Internal Developer Portal** のそれぞれについて紹介します。

## IDP (プラットフォームやポータル) のない状態

IDP (プラットフォームやポータル) がなぜ求められているかを考えるために、IDP がない状態についてまず考えてみます。

![](https://storage.googleapis.com/zenn-user-upload/2cfdc83c9fdc-20230220.png)

IDP がない状態、つまりインフラストラクチャを素の状態で使うということです。ここでいうインフラストラクチャは、オンプレミス環境であったり、オンプレミス上の仮想環境やパブリッククラウド、また Kubernetes などのコンテナオーケストレーション環境です。

これらのインフラストラクチャ環境を扱うのは難しくありませんか？

特に基盤エンジニアではなく、アプリケーション開発者のみなさんにとっては。以前 Java 開発者の方に "Kubernetes をつかいたいか？" というような質問をしたことがあります。回答としては、"興味はあるけれど、難しそう"、"学ぶ時間がない"、"使えたほうがいいのは分かる" というような、難しそうという意見がほとんどで、ポジティブに学びたいという意見はごく少数の方からでした。
