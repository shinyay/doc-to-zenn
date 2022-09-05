---
title: "100日後にRustをちょっと知ってる人になる: [Day 14]GitHub Codespaces"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 14 のテーマ

今日は趣向を変えて、Rust の開発環境について考えてみたいと思います。
Day 2 で開発環境 "VS Code" と "IntelliJ IDEA" の環境を整えて今はそれを使って Rust のコード編集をしています。しかし、最近ではオンラインで Web 上でコード編集をすることも増えてきていますよね。そこで今日はオンラインで Rust のコード編集が出来るようにしていこうと思います。

## GitHub Codespaces

オンラインでコード開発をするサービスはいろいろと出ていると思います。
**クラウド IDE** などと呼ばれていることもありますよね。例えば:

- [AWS Cloud 9](https://aws.amazon.com/jp/cloud9/)
- [CodeAnywhere](https://codeanywhere.com/)
- [Codenvy(名前改め現在 Red Hat OpenShift Dev Spaces)](https://developers.redhat.com/products/openshift-dev-spaces/overview)
- [Koding](https://www.koding.com/)
- [Coder](https://coder.com/)
- などなど

いろいろと Cloud IDE はあるのですが、その中から **[GitHub Codespaces](https://github.com/features/codespaces)** を使ってみようと思います。文字通り GitHub が提供している開発環境です。

![](https://storage.googleapis.com/zenn-user-upload/e2c520146e96-20220905.png)

また、この GitHub Codespaces は **VS Code** にExtension をインストールすると、オンラインの内容とローカルの内容が同期されるということなので VS Code に Extension もあわせてインストールしようと思います。

- [GitHub Codespaces Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces)
[![](https://storage.googleapis.com/zenn-user-upload/6edaef0be174-20220905.png)](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces)

## GitHub Codespaces Extension インストール

VS Code のマーケットプレイスから **GitHub Codespaces** を見つけてインストールを行います。

![](https://storage.googleapis.com/zenn-user-upload/7c1ea546d932-20220905.png)

Extension をインストールすると、Remote Explorer のアイコンがサイドバーに表示されます。

![](https://storage.googleapis.com/zenn-user-upload/0c034df4d105-20220905.png)

## Day 14 のまとめ
