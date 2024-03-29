---
title: "IDP: 内部開発者プラットフォームと内部開発者ポータル"
emoji: "⚡"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [platform, platformengineer]
published: true
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
実際のところ、アプリケーション開発者からすると Kubernetes に限らず、インフラストラクチャの技術を理解していくというのは難しいものだと思っています。

開発者からすると、とにかく開発者体験 **Developer Experience (DevEx)** の向上であり、生産性の向上だとおもいます。難しい基盤技術に対してどのように付き合っていけばよいのでしょうか。
その答えが、**Internal Developer Platform** であり、 **Internal Developer Portal** なのです。

## Internal Developer Platform (内部開発者プラットフォーム)

![](https://storage.googleapis.com/zenn-user-upload/75c94f2416c6-20230220.png)

開発者体験 **DevEx** の高い究極の形とはどのようなものだと思いますか？人それぞれ様々な考えがあるとおもいます。
僕は、ソースコードを書いたら、コマンドかボタン 1 つで実行環境にデプロイされて動作確認ができてしまうような状態だと思っています。つまり、ソースコードだけにに専念して、コーディングをしていればいい状態です。
もちろん設計に使う時間とは別ですけどね。

そのようなコードを書くことに専念できるような実行環境を実現してくれるのが、**Internal Developer Platform (内部開発者プラットフォーム)** です。そして、これを構築・整備・提供する人が **Platform Engineer** です。兼任などではなく、このチームの開発のために専属で構成されているエンジニア達です。Platform Engineer はこのプラットフォームに対するミッションを持っているので、プラットフォーム配下の基盤に対しても責任を負います。つまり、構築や整備を行うため意識をするひつようがあります。

しかし、開発者はプラットフォームが基盤を抽象化 (隠蔽化) するので複雑で難解と感じてしまう基盤を意識する必要がなくなります。

つまり、Kubernetes を習得しなければならないとか、コンテナのビルド方法について理解しなければならないとか、アプリケーション実行に必要なリソースが割り当てられた環境を用意しなければならないとか、というような考えることが負荷となりうること (**認知負荷**) というものをプラットフォームが解消してくれます。また、従来手作業や口頭などでアプリケーションのデプロイを担当者に依頼を行っていたような繰り返し作業や、面倒な作業 (**トイル**) というものをプラットフォームが自動化して対応してくれます。このように、開発者にとっての **Developer Experience** を向上させてくれるような仕組みが実装されているのが **Internal Developer Platform (内部開発者プラットフォーム)** なのです。

## Internal Developer Portal (内部開発者ポータル)

さて、Internal Developer Platform (内部開発者プラットフォーム) についてどのようなものかを紹介しました。これだけあれば、開発者の DevEx が向上して解決するじゃないかと思われのではないでしょうか。
実際そうです。Internal Developer Platform としての機能だけを提供しているようなツールや製品もあるでしょう。では、なぜ **Internal Developer Portal (内部開発者ポータル)** が必要なのでしょうか？

その答えは、開発チームや組織にとっての**最適化**なのです。

![](https://storage.googleapis.com/zenn-user-upload/0dc33f5cd2c5-20230220.png)

さまざまな自動化やセルフサービスな機能を提供してくれるのが、**Internal Developer Platform (内部開発者プラットフォーム)** でした。そのフロントエンドに構え、開発者や利用者が操作するユーザーインターフェースとなるのが **Internal Developer Portal (内部開発者ポータル)** です。**Platform Engineering** のコンセプトの中に大事なことがいくつかあるのですが、その中から次の 2 つをとりあげてポータルの必要性について紹介します。

- **ゴールデンパス**
- **製品としてのプラットフォーム**

**ゴールデンパス** とは、直訳すると黄金の道筋とでも言うのでしょうか。文字通り、黄金の最適なパスを提供することなのです。アプリケーションの開発ライフサイクルは大まかにはどこでも同じだと思います。

"要件" -> "設計" -> "実装" -> "テスト" -> "デプロイ" ですよね。

ですが、細かく見ていくと組織や開発チームごとに異なっているのではないでしょうか。使っているツールもきっと異なってきますよね。きっとあなたが今属している開発の流れが一番心地よくすすむ状態ではないでしょうか。そこに、便利だから別のツールを導入しましょうと言われてもなかなか受け入れられなかったりしませんか？
ゴールデンパスとは、予めそのチームが行っている最適な開発ラライフサイクルとツールをテンプレートとして定義して、それにのっとればみんな正しく、かつ心地よく開発ができるという考えです。

もし、プラットフォームが定義している仕組みに従わなければならないのである、というような開発であれば、便利だったとしても今までの慣れ親しんだ慣習から外れてしまい、DevEx は下がるかもしれませんよね。
**Internal Developer Portal (内部開発者ポータル)** は、このような開発チームが持っているゴールデンパスをテンプレートを定義しておくことができるのです。つまり、同じプラットフォームツールを使っていたとしても、組織や開発チームによって使われ方や動作が異なることが可能なのです。

次に **製品としてのプラットフォーム** です。
ゴールデンパスの説明の中でも強調したように、**Internal Developer Platform (内部開発者プラットフォーム)** を組織ごとや、開発チームごとに最適化して自分たちの使いやすい状態の色に染めあげていますよね。
これは、まさに今あなたが使用しているプラットフォームを、各組織ごとのブランドをつくっているようなものだと思いませんか？
つまり、どのような商用製品もブランディングし、価値を創造し、使用する人にとっての魅力をつけていきますね。**製品としてのプラットフォーム**という考え方は、まさにそれです。**Internal Developer Platform (内部開発者プラットフォーム)**にたいして、自分たちの組織のメンバーが使いたくなるような価値を作り上げていく（カスタマイズしていく）ことによって、成長しているプラットフォームになるというものなのです。

従来のインフラストラクチャや実行環境だと、一度作ってしまえばそれで終了というようなものもあったと思います。Platform Engineering では、構築したプラットフォームはその上で稼働するソフトウェアや、使用するエンジニアとともに成長していく**製品**なのです。

このように、利用者に応じた最適化を行うことができるのが、**Internal Developer Portal (内部開発者ポータル)** なのです。

## Key Takeaways

2 つの IDP, **Internal Developer Platform (内部開発者プラットフォーム)** と **Internal Developer Portal (内部開発者ポータル)** について紹介を行いました。
この 2 つの IDP の違いについて何か気づきをもってもらえたでしょうか。

Platform Engineering を始めるにあたって、何から導入したらいいかという質問がいろいろなところで見かけました。その際に多くの意見としては、Platform よりも先にまず Portal から着手しているという回答を目にしました。DevEx の向上に対して一番最初に効果が見えやすいからかもしれないですね。
代表的な **Internal Developer Portal (内部開発者ポータル)** は、Spotify が提供する OSS の **Backstage** が有名ですね。

- [Backstage](https://backstage.io/)

**Platform Engineering** は、技術やツールだけで成り立つものでは決してありません。ですが、新しく盛り上げってきている領域なので様々な OSS ツールや製品が登場してきています。それらについて、今後も注目していきたいなと思います。
