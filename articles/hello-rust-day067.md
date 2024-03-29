---
title: "100日後にRustをちょっと知ってる人になる: [Day 67]lib.rs"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 67 のテーマ

[Day 66](https://zenn.dev/shinyay/articles/hello-rust-day066) では、クレートをいろいろなカテゴリ別におすすめのもの分類して紹介していくれている **[Blessed.rs](https://blessed.rs/crates)** の紹介を行いました。その、Bleesed.rs の中でも紹介はされていたのですが、今日は少し **lib.rs** について見てみたいと思います。

## lib.rs

![](https://storage.googleapis.com/zenn-user-upload/a02e2455c34e-20221121.png)

- [lib.rs](https://lib.rs/)

Blessed.rs では次の様に lib.rs のことが紹介されています。

> lib.rsはより自動化されたアプローチ（ダウンロード数でクレートを並べる）をとり、また優れた検索機能を備えています。

Blessed.rs では、サイトオーナーの Nico Burns が中心となってクレートの評価と分類が行われていました。一方で、lib.rs はクレートのダウンロード数から**自動的**に人気なものだと判別し公開しているようです。Blessed.rs で紹介されていないクレートなども lib.rs でいち早く見つけることができるかもしれないですね。

lib.rs では次の様なセクションでクレートを表示することができます。

- カテゴリー (Categories)
  - Blessed.rs のように目的・機能別にクレートを表示
- 新着やトレンド (New and Trending)
  - 新規リリースされたり、当月中に注目を集めたクレートを表示
- 人気 (Popular)
  - ダウンロード数順でクレートを表示

それらとは別に統計情報が確認できます。

![](https://storage.googleapis.com/zenn-user-upload/43819c13b63e-20221121.png)

これを見ると、2015 年に Rust 1.0 がリリースされてからのクレートのダウンロード数の推移が確認できます。かなりの勢いで Rust の普及が進んできていることがわかります。年率で 1.9 倍で増えてきていということなので、2023 - 2024 年あたりでは Rust をとりまく世界で何か起こりそうな気がしますね。

![](https://storage.googleapis.com/zenn-user-upload/2a87c4f1f578-20221121.png)

## lib.rs でのカテゴリー

さて、それでは Blessed.rs 同様に lib.rs でもどのようなカテゴリー分類がされているかを確認しておきたく思います。

- [Rustパターン](https://lib.rs/rust-patterns)
  - Rust でのプログラミングに特有の状況に対する解決策
- [ネットワークプログラミング](https://lib.rs/network-programming)
  - FTP、HTTP、SSHなどの上位ネットワークプロトコルや、TCP、UDPなどの下位ネットワークプロトコルを扱うクレート
- [データ構造](https://lib.rs/data-structures)
  - 特定の目的のためにデータを整理する特定の方法
- [開発ツール](https://lib.rs/development-tools)
  - テスト、デバッグ、Lint、パフォーマンスプロファイリング、オートコンプリート、フォーマットなど、開発者向けの機能を提供するクレート
- [デバッギング](https://lib.rs/development-tools/debugging)
  - ロギング、トレース、アサーションなど、コードで何が起こっているかを把握するのに役立つクレート
- [ビルドユーティリティ](https://lib.rs/development-tools/build-utils)
  - ビルドスクリプトやその他のビルドステップ用のユーティリティ
- [テスト](https://lib.rs/development-tools/testing)
  - コードの正しさを検証するためのクレート
- [FFI](https://lib.rs/development-tools/ffi)
  - 他の言語とのインターフェイスを改善するために役立ちます。これには、バインディングジェネレータや便利な言語構成が含まれます
- [プロファイリング](https://lib.rs/development-tools/profiling)
  - コードのパフォーマンスを把握
- [手続き型マクロ](https://lib.rs/development-tools/procedural-macro-helpers)
  - 手続き的なマクロを書くためのクレート
- [Cargo プラグイン](https://lib.rs/development-tools/cargo-plugins)
  - Cargoの機能を拡張するサブコマンド
- [アルゴリズム](https://lib.rs/algorithms)
  - ハッシュ、ソート、検索などのコアアルゴリズム
- [暗号技術](https://lib.rs/cryptography)
  - データの安全性を確保するためのアルゴリズム
- [データエンコード](https://lib.rs/encoding)
  - あるデータフォーマットから別のデータフォーマットへのエンコードやデコードを実施
- [テキスト処理](https://lib.rs/text-processing)
  - テキスト形式で表現された人間の言葉の複雑さを扱うためのクレート
- [非同期処理](https://lib.rs/asynchronous)
  - futures、promise、waiting、eventingなどの技術を使用して、メインプログラムの流れとは別にイベントを処理
- [並行処理](https://lib.rs/concurrency)
  - 同時並行計算を実装
- [パーサーの実装](https://lib.rs/parser-implementations)
  - 特定のフォーマットや言語向けに実装されたパーサー
- [オペレーティングシステム](https://lib.rs/os)
  - オペレーティングシステム固有のAPIへのバインディング
- [Unix API](https://lib.rs/os/unix-apis)
  - Linux や *BSD システムを含む、Unix 固有の API へのバインディング
- [Windows API](https://lib.rs/os/windows-apis)
  - Microsoft Windows 固有のAPIへのバインディング
- [macOSとiOSのAPI](https://lib.rs/os/macos-apis)
  - macOS または iOS/iPadOS の API、およびその他の Apple 固有の技術とのインターフェイス
- [サイエンス](https://lib.rs/science)
  - 数学、物理学、化学、生物学、機械学習、地球科学、その他の科学分野の問題解決に関するクレート
- [数学](https://lib.rs/science/math)
  - 数学の問題解決に関連するクレート
- [機械学習](https://lib.rs/science/ml)
  - 人工知能、ニューラルネットワーク、ディープラーニング、推薦システム、統計学
- [ロボティクス](https://lib.rs/science/robotics)
  - ロボティクスに関連するクレートです。ロボット、ドローン、自律型マシンのファームウェアを構築
- [パーサツーリング](https://lib.rs/parsing)
  - あらゆるファイル形式のパーサーを作成・生成するためのユーティリティ・ライブラリ
- [Web プログラミング](https://lib.rs/web-programming)
  - Web用アプリケーションを作成するためのクレート
- [HTTP クライアント](https://lib.rs/web-programming/http-client)
  - HTTP ネットワークリクエストを行うためのクレート
- [HTTP サーバー](https://lib.rs/web-programming/http-server)
  - HTTPでデータを提供するためのクレート
- [WebSocket](https://lib.rs/web-programming/websocket)
  - WebSocketプロトコルで通信するためのクレート
- [ハードウェアサポート](https://lib.rs/hardware-support)
  - 特定の CPU やその他のハードウェアの機能に対応するためのクレート
- [WebAssembly](https://lib.rs/wasm)
  - WebAssembly をターゲットとするときに使用するクレート、または WebAssembly を操作するためのクレート
- [組込み開発](https://lib.rs/embedded)
  - 主に組込み機器やOSを持たない機器に有効なクレート
- [ファイルシステム](https://lib.rs/filesystem)
  - ファイルやファイルシステムを扱うためのクレート
- [圧縮](https://lib.rs/compression)
  - データをより小さくするためのアルゴリズム
- [コマンドラインインタフェース](https://lib.rs/command-line-interface)
  - 引数パーサ、ラインエディット、出力のカラーリングやフォーマットなど、コマンドラインインターフェイスの作成を支援
- [コマンドラインユーティリティ](https://lib.rs/command-line-utilities)
  - コマンドラインから実行するアプリケーション
- [メモリ管理](https://lib.rs/memory-management)
  - メモリ割り当て、メモリマッピング、ガベージコレクション、参照カウント、または外部メモリマネージャへのインタフェースを支援す
- [日付と時間](https://lib.rs/date-and-time)
  - 4次元を扱う固有の複雑さを管理するためのクレート
- [データベースインターフェース](https://lib.rs/database)
  - データベース管理システムとのインターフェイス
- [データベース実装](https://lib.rs/database-implementations)
  - Rust で実装されたデータベース管理システム。大量のデータを効率的に保存し、クエリすることが可能
- [値の書式設定](https://lib.rs/value-formatting)
  - アプリケーションがユーザーに表示する値を様々な言語や地域に表示を適合したフォーマットするためのクレートです。
- [テンプレートエンジン](https://lib.rs/template-engine)
  - テンプレートとデータを組み合わせて、結果文書を作成するために設計されたクレートで、通常はテキストの処理に重点が置かれています。
- [コンフィギュレーション](https://lib.rs/config)
  - アプリケーションのコンフィギュレーション管理を容易にするためのクレート
- [GUI](https://lib.rs/gui)
  - グラフィカルユーザーインターフェースの作成を支援するクレート
- [マルチメディア](https://lib.rs/multimedia)
  - オーディオ、ビデオ、画像処理またはレンダリングエンジンを提供
- [画像](https://lib.rs/multimedia/images)
  - 画像を処理したり、グラフィックを生成するクレート
- [オーディオ](https://lib.rs/multimedia/audio)
  - オーディオを記録、出力、処理
- [ビデオ](https://lib.rs/multimedia/video)
  - 映像を記録、出力、処理
- [レンダリング](https://lib.rs/rendering)
2Dまたは3Dグラフィックスのリアルタイムまたはオフラインでのレンダリング
- [グラフィックス API](https://lib.rs/rendering/graphics-api)
  - ハードウェアやオペレーティングシステムのレンダリング機能に直接アクセスするためのクレート
- [Gfxデータフォーマット](https://lib.rs/rendering/data-formats)
  - 3D モデルやアニメーションシートなど、2D や 3D レンダリングに関連するデータフォーマットの読み込みとパース処理
- [レンダリングエンジン](https://lib.rs/rendering/engine)
  - 画面への描画のためのハイレベルなソリューション
- [標準ライブラリ不要](https://lib.rs/no-std)
  - Rust の標準ライブラリ無しで動作するクレート
- [可視化](https://lib.rs/visualization)
  - プロットやグラフなどのデータの見方
- [認証](https://lib.rs/authentication)
  - 認証を支援するクレート
- [キャッシング](https://lib.rs/caching)
  - 計算結果を再利用するために、過去の計算結果を保存するクレート
- [ゲーム開発](https://lib.rs/game-development)
  - ゲーム制作を支援するクレート
- [ゲーム](https://lib.rs/games)
  - Rust で書かれたゲームや、既存のゲーム用のツールや MOD
- [テキストエディター](https://lib.rs/text-editors)
  - テキストを編集するためのアプリケーション
- [国際化](https://lib.rs/internationalization)
  - 様々な言語や地域に適応したソフトウェアを開発するためのクレート (ローカライゼーションソフトを含む)
- [プログラミング言語](https://lib.rs/compilers)
  - プログラミング言語のためのツール：コンパイラ、インタプリタ、トランスパイラ、仮想マシン
- [電子メール](https://lib.rs/email)
  - 電子メールの送受信、書式設定、解析に役立つクレート
- [エミュレータ](https://lib.rs/emulators)
  - あるコンピュータを別のコンピュータのように動作させるもので、多くの場合、ホストコンピュータでネイティブに利用できないソフトウェアを実行できるようにするもの
- [シミュレーション](https://lib.rs/simulation)
  - ネットワークプロトコルのシミュレーションなど、ある活動のモデル化またはモデル構築に使用するクレート
- [アクセシビリティ](https://lib.rs/accessibility)
  - 様々な人が使いやすくなるための支援


## Day 67 のまとめ

**[Blessed.rs](https://blessed.rs/crates)** と **[lib.rs](https://lib.rs/)** を見れば、サードパーティ製のクレートでどういう時にどのようなものを使えばいいか、ということが Rust 初学者であっても勘が身につきそうなきがします。今後いろいろなクレートの学習をしてみたいと思っています。
