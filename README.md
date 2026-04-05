# doc-to-zenn

> **Zenn publishing hub — 100 Days of Rust, Platform Engineering, WebAssembly, and GitHub Changelog の日本語テック記事**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://gist.githubusercontent.com/shinyay/56e54ee4c0e22db8211e05e70a63247e/raw/f3ac65a05ed8c8ea70b653875ccac0c6dbc10ba1/LICENSE)

[Zenn](https://zenn.dev/) に公開する日本語テック記事の管理リポジトリです。104 本の技術記事と 42 のサンプルコードプロジェクトを収録し、GitHub 連携で記事を自動公開しています。

📖 **Zenn プロフィール**: [zenn.dev/shinyay](https://zenn.dev/shinyay)

---

## 🚀 Quick Start

**Prerequisites:**

- [x] **Node.js 18+** (`node --version`)
- [x] **Git** (`git --version`)

### 1. Clone and install

```bash
git clone https://github.com/shinyay/doc-to-zenn.git
cd doc-to-zenn
npm install
```

### 2. Preview articles locally

```bash
npx zenn preview
# 🌐 Open http://localhost:8000 — browse all articles as they appear on Zenn
```

### 3. Create a new article

```bash
npx zenn new:article --slug my-new-article
# ✏️ Edit articles/my-new-article.md, then git push to publish
```

---

## 💡 Overview

This repository is the **single source of truth** for all Zenn articles published under [@shinyay](https://zenn.dev/shinyay). Articles are written in Markdown with YAML frontmatter, managed via [zenn-cli](https://zenn.dev/zenn/articles/zenn-cli-guide), and auto-published through GitHub integration on every push to `main`.

### Content Map

```
doc-to-zenn/
├── articles/          104 published articles (日本語)
│   ├── 🦀 Rust        100 articles (Day 1–100 daily series)
│   ├── ⚡ Platform      2 articles (Platform Engineering)
│   └── 🦀 WebAssembly   2 articles (Wasm + Docker)
├── codes/              42 companion sample projects
│   ├── day_*/          Per-day Rust exercises & projects
│   └── wasm-*/         WebAssembly demos
└── books/             (reserved for future use)
```

---

## ✨ Content Catalog

### 🦀 100日後にRustをちょっと知ってる人になる (100 Days of Rust)

100 日間の Rust 学習チャレンジ。基礎文法からWebAssembly、Webフレームワーク、PostgreSQL 連携まで。

| Phase | Days | Topics |
|-------|------|--------|
| **基礎** | Day 1–15 | Rust 概要, 変数, 型, 所有権, FizzBuzz |
| **型システム** | Day 16–50 | トレイト, ジェネリクス, エラー処理, String型, WebAssembly |
| **テスト & ツール** | Day 51–75 | ユニットテスト, Fermyon Cloud, Spin, Clippy, rustfmt, cargo拡張 |
| **Web & DB** | Day 76–100 | Rocket, Actix-web, Hyper, Axum, PostgreSQL, TODO アプリ |

### ⚡ Platform Engineering

| Article | Description |
|---------|-------------|
| [プラットフォームエンジニアリングとは？](https://zenn.dev/shinyay/articles/what-is-platform-engineering) | Platform Engineering の概念と製品ベンダー視点からの解説 |
| [IDP: 内部開発者プラットフォームとポータル](https://zenn.dev/shinyay/articles/idp-platform-portal) | Internal Developer Platform vs Portal の違い |

### 🦀 WebAssembly

| Article | Description |
|---------|-------------|
| [5分で WebAssembly + Docker = Hello World](https://zenn.dev/shinyay/articles/wasm-docker-helloworld) | Wasm + Docker の最速ハンズオン |
| [2023年の WebAssembly と Bytecode Alliance](https://zenn.dev/shinyay/articles/webassembly-and-the-future) | Wasm/WASI の将来展望 |

---

## 🏗️ Repository Structure

```
doc-to-zenn/
├── articles/                    # Zenn articles (Markdown + YAML frontmatter)
│   ├── hello-rust-day001.md     # 🦀 100 Days of Rust (Day 1–100)
│   ├── ...
│   ├── hello-rust-day100.md
│   ├── what-is-platform-engineering.md
│   ├── idp-platform-portal.md
│   ├── wasm-docker-helloworld.md
│   └── webassembly-and-the-future.md
├── books/                       # Zenn books (reserved)
├── codes/                       # Companion sample projects
│   ├── day_6_guessing_game/     #   Rust exercises per day
│   ├── day_36_hello_rocket/     #   Web frameworks
│   ├── day_91_hello_axum/       #   Axum HTTP server
│   └── wasm-docker-helloworld/  #   WebAssembly demos
├── package.json                 # zenn-cli dependency
├── .gitignore
└── README.md
```

---

## 📖 Usage

| I want to… | Do this |
|------------|---------|
| Preview all articles | `npx zenn preview` → http://localhost:8000 |
| Create a new article | `npx zenn new:article --slug article-name` |
| Create a new book | `npx zenn new:book --slug book-name` |
| Publish changes | `git add . && git commit -m "..." && git push` |
| Check Zenn CLI help | [📘 Zenn CLI Guide](https://zenn.dev/zenn/articles/zenn-cli-guide) |

### Article Frontmatter Format

```yaml
---
title: "記事タイトル (max 50文字)"
emoji: "🦀"
type: "tech"                    # tech or idea
topics: ["rust", "webassembly"] # 1–5 topics
published: true                 # true = 公開, false = 下書き
---
```

> [!TIP]
> `git push` するだけで Zenn に自動公開されます。`published: false` で下書き保存が可能です。

---

## 📚 References

| Resource | Link |
|----------|------|
| Zenn プロフィール | [zenn.dev/shinyay](https://zenn.dev/shinyay) |
| Zenn CLI ガイド | [zenn.dev/zenn/articles/zenn-cli-guide](https://zenn.dev/zenn/articles/zenn-cli-guide) |
| Zenn Markdown 記法 | [zenn.dev/zenn/articles/markdown-guide](https://zenn.dev/zenn/articles/markdown-guide) |
| gh-changelog-zenn | [github.com/shinyay/gh-changelog-zenn](https://github.com/shinyay/gh-changelog-zenn) |

---

## Licence

Released under the [MIT license](https://gist.githubusercontent.com/shinyay/56e54ee4c0e22db8211e05e70a63247e/raw/f3ac65a05ed8c8ea70b653875ccac0c6dbc10ba1/LICENSE)

## Author

- github: <https://github.com/shinyay>
- bluesky: <https://bsky.app/profile/yanashin.bsky.social>
- twitter: <https://twitter.com/yanashin18618>
- mastodon: <https://mastodon.social/@yanashin>
- linkedin: <https://www.linkedin.com/in/yanashin/>