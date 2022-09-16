---
title: "100日後にRustをちょっと知ってる人になる: [Day 24]rust-webpack"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 24 のテーマ

Rust で生成した **WebAssembly**　を動作させるために Node.js にインポートすることはよくあると思います。
今日は、Rust で生成した **WebAssembly** と **[Webpack](https://webpack.js.org/)** を使って、Web アプリケーションを作成してみようと思います。

次の npm パッケージを使って Node.js と Rust のプロジェクトを用意していきます。

- [create-rust-webpack (rust-webpack-template)](https://www.npmjs.com/package/create-rust-webpack)

### Webpack

Node.js クラスタに住んでいないエンジニアの方だと、あまり聞き覚えがないかもしれないので、まず最初に、**Webpack** とは何かということについて簡単に説明しておきます。

JavaScript モジュールを束ねることができるツール（**モジュールバンドラ**）のことです。

Web アプリケーションを構成するリソースは複数あります。 例えば、Web ページを装飾するために **CSS** を使いますし、**画像**も必要です。
**Webpack** は、これらのリソース (HTML、SVG、JSX、CSS、JavaScript、PNG、JPG) を 1 つに束ねてくれるので、開発する際にリソースを扱いやすくなります。

Webpack を使うことのメリット:
✅ 依存関係のある JavaScript のモジュールを解決
✅ 適切な順序での JavaScript ファイルのコードを結合することが可能
✅ JavaScriptモジュールをブラウザで扱える形に変換可能
✅ 豊富なローダやプラグイン

### create-rust-webpack (rust-webpack-template)

**create-rust-webpack (rust-webpack-template)** を使ってプロジェクトテンプレートを作ってみます。

```shell
$ npm init rust-webpack my-app

 🦀 Rust + 🕸 WebAssembly + Webpack = ❤️
 Installed dependencies ✅
```

## Day 24 のまとめ
