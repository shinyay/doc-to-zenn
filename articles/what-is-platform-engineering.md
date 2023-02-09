---
title: "プラットフォームエンジニアリング (Platform Engineering) とは？"
emoji: "⚡"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [platformengineering]
published: false
---
![](https://storage.googleapis.com/zenn-user-upload/10dc59576b4e-20230209.png)

## テーマ

昨年、2022 年頃から急激に注目を集め始めバズワードとなっている "**Platform Engineering**" については、Zenn を見ている方たちの多くも注目をしているのではないかなと思います。
日本国内でも関心の高まりはいたるところで目にするようになってきているので、どういうものなのか簡単に "製品ベンダーの中の人" の目線から説明してみたいと思います。

### 注釈

"製品ベンダーの中の人" の目線と書いたように、ぼく自身は決して **Platform Engineer** ではありません。そのため、実践した経験をもとに Platform Engineering について説明しているわけではないことを了承していただければと思います。
どうしても、Platform Engineer のコンセプト的に製品ベンダーの人が話す内容と、実践している **Platform Engineer** の視点とは現実味が異なると思います。今後、ぼく自身も **Platform Engineering** を実践されている人たちの話を聞きたいな、と思い期待しています。

## Platform Engineering が注目する背景

DevOps という土壌があったからというのは、まず大事な要因だと思います。

![](https://storage.googleapis.com/zenn-user-upload/06df5c310612-20230209.png)

DevOps については、もはや細かな説明が不要なくらい浸透していると思います。

- ✅ 基盤エンジニアリング - 運用エンジニア -　開発エンジニア をつなぐための取り組み
- ✅ Infrasturecture as Code や テスト自動化など様々な自動化の実践
- ✅ パイプラインを用意し開発工程の様々な作業の連携

などといった取り組みでした。



## Key Takeaways