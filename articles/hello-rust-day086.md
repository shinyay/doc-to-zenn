---
title: "100日後にRustをちょっと知ってる人になる: [Day 86]Manning の Rust 本リスト"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 86 のテーマ

[Day 85](https://zenn.dev/shinyay/articles/hello-rust-day085) までの数日間 Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** を読みながら感想を書いてきました。まだ少し残りもあるので、続きを読み進めたいところなのですが今日は趣向を変えようと思います。
というのも、今月は技術書を数多く出版している **[Manning](https://www.manning.com/)** がセールをしているので何かここでも Rust の本を買おうと思っています。そこで、いろいろと試読しながら次に買う本を決めようとしています。今日はその Manning の Rust に関する本のリストを作ろうと思います。

## Manning の Rust 書籍リスト

### Rust in Action

![](https://storage.googleapis.com/zenn-user-upload/9faeb5123d98-20221213.png)

- [Rust in Action](https://www.manning.com/books/rust-in-action)
  - by Tim McNamara

- コンテンツ内容
  - 1 Introducing Rustfree audio
  - 2 Language foundations
  - 3 Compound data types
  - 4 Lifetimes, ownership, and borrowing
  - 5 Data in depth
  - 6 Memory
  - 7 Files and storage
  - 8 Networking
  - 9 Time and timekeeping
  - 10 Processes, threads, and containers
  - 11 Kernel
  - 12 Signals, interrupts, and exceptions

こちらの本は日本語に翻訳されていて、翔泳社から**詳解Rustプログラミング**として出版されています。

- [詳解Rustプログラミング](https://www.shoeisha.co.jp/book/detail/9784798173856)

### Refactoring to Rust

![](https://storage.googleapis.com/zenn-user-upload/6dff1b8c2457-20221213.png)

- [Refactoring to Rust](https://www.manning.com/books/refactoring-to-rust)
  - by Lily Mara, Joel Holmes

- コンテンツ内容
  - 1 Why Refactor to Rust
  - 2 An overview of Rust
  - 3 Introduction to C FFI and Unsafe Rust
  - 4 Advanced FFI
  - 5 Structuring Rust libraries
  - 6 Integrating with dynamic languages
  - 7 Testing your Rust integrations

この書籍は、MEAP (Manning Early Access Program) 、つまり、まだ出版前の書籍です。執筆中の書籍を未完成の段階で購入し、章が完成するごとに読みすすめられるという形式になっています。

読みやすいスタイルでRustを紹介し、構文やコンセプトを明確に説明しています。Rust のパターンマッチで `FizzBuzz` を解いたり、Python コードの実行速度を大幅に向上させるなど、親しみやすい例を使って、Rust でプログラムを拡張する方法を実践的に学ぶことができます。また、既存のあらゆるソフトウェアに適用できる Rust プラグインを構築するテクニックを習得できるようになっています。

### Rust Servers, Services, and Apps

![](https://storage.googleapis.com/zenn-user-upload/751da3d120da-20221213.png)

- [Rust Servers, Services, and Apps](https://www.manning.com/books/rust-servers-services-and-apps)
  - by Prabhu Eshwarla

- コンテンツ内容
  - 1 Why Rust for web applications?
  - 2 Writing a basic web server from scratch
  - 3 Building a RESTful web service
  - 4 Performing database operations
  - 5 Handling errors
  - 6 Evolving the APIs and fearless refactoring
  - 7 Introduction to server-side web apps in Rust
  - 8 Working with templates for tutor registration
  - 9 Working with forms for course maintenance
  - 10 Understanding Async Rust
  - 11 Building a P2P node with Async Rust
  - 12 Deploying web services with Docker

**Rust Servers, Services, and Apps** も MEAPです。
この本は、Rust でモダンな分散型 Web アプリケーションを開発するためのハンズオンガイドになっています。。効率的なサービスの構築、カスタム Web サーバの作成、そしてエンドツーエンドのフルスタックアプリケーションの構築を Rust で行う方法について学ぶことができます。
Rust を使用して HTTP サーバと RESTful API を構築し、安全性を確保し、デバッグし、リファクタリングで進化させるという基礎的な部分から始めることができます。また、自分のプロジェクトに適用できるコードサンプルと、Rust がどのように動作するかを理解するのに役立つ詳細なアノテーションを提供しています。

### Code Like a Pro in Rust

![](https://storage.googleapis.com/zenn-user-upload/e3d6efcf7281-20221213.png)

- [Code Like a Pro in Rust](https://www.manning.com/books/code-like-a-pro-in-rust)
  - by Brenden Matthews

- コンテンツ内容
  - 1 Feelin' Rusty
  - 2 Project management with Cargo
  - 3 Rust tooling
  - 4 Data structures
  - 5 Working with memory
  - 6 Unit testing
  - 7 Integration testing
  - 8 Design pattern building blocks
  - 9 Design patterns: beyond the basics
  - 10 Advanced design patterns
  - 11 Async Rust
  - 12 Optimizations

**Code Like a Pro in Rust** も MEAPです。
この本では、言語の癖やコンパイラの問題、予想外の複雑さに時間をとられることなく、Rust プログラムを素早く作成する方法を紹介しています。Rust の開発者であるBrenden Matthews がデザインパターンとショートカットを直接提供し、既存の Rust の知識に基づいて構成されています。**Rust-analyzer**、**Clippy**、**Cargo**などの重要な Rust ツールの使い方や、ユニットテストやコードの最適化に関するベストプラクティスも学べます。また、ユニットテストやコード最適化のベストプラクティスも紹介されています。

### Rust Web Development

![](https://storage.googleapis.com/zenn-user-upload/f554daee7170-20221213.png)

- [Rust Web Development](https://www.manning.com/books/rust-web-development)
  - by Bastian Gruber

- コンテンツ内容
  - 1 Why Rust?
  - 2 Laying the foundation
  - 3 Create your first route handler
  - 4 Implement a RESTful API
  - 5 Cleanup your codebase
  - 6 Logging, tracing and debugging
  - 7 Add a database to your application
  - 8 Integrate 3rd party APIs
  - 9 Add authentication and authorization
  - 10 Deploy your application
  - 11 Testing your Rust application

**Rust Web Development** は、12 月に発売されたばかりの本です。
この本では、Rust を使ってサーバーサイドの Web アプリケーションを構築する方法を、非同期ランタイムの `tokio`、Web サーバーと API の `warp`、外部HTTPリクエストを実行する `reqwest` などの重要な Rust ライブラリとともに学ぶことができます。本書には、例題、コードサンプル、プロジェクトのセットアップやコードの整理に関するプロ向けのヒントが掲載されています。実際の開発プロジェクトのように、章ごとにコードを繰り返しながら、完全な Q&A Webサービスを構築することができるようになっています。

### Multiplayer Game Development in Rust

![](https://storage.googleapis.com/zenn-user-upload/f835977f1768-20221213.png)

- [Multiplayer Game Development in Rust](https://www.manning.com/books/multiplayer-game-development-in-rust)
  - by Stephan Dilly and Lyon Beckers

- コンテンツ内容
  - 1 Introducing Rust in games
  - 2 Building a game client
  - 3 Building a game server
  - 4 Making a multiplayer client
  - 5 Error handling

**Multiplayer Game Development in Rust** は MEAP です。
この本では、マルチプレイヤーゲームを構築することを学びます。シンプルなゲームクライアントを構築しますが、本来の処理はバックエンドで行われます。章ごとに、スケーラビリティ、永続性、ベンチマーク、トレースを追加していき、リアルタイムのマルチプレイヤー・スコアリング、リーダーボード、サーバーからクライアントへのメッセージングなどのゲーム機能をサポートします。その過程で、Rust がゲーム開発に最適な理由や、クラウドを最大限に活用した最先端の技術について、プロからのアドバイスを受けることができます。さらに、リアルタイムサーバ技術を必要とするあらゆるアプリケーションに応用することができます。

## Day 86 のまとめ

試し読みを少しずつつまみ食いをしてみました。結果、今日購入した本は [Rust Web Development](https://www.manning.com/books/rust-web-development) です。

https://twitter.com/recvonline/status/1602531702055870467

著者の Bastian Gruber さんから楽しんでねとメッセージを頂いたので、この本をしばらく楽しみたいなと思っています✨
