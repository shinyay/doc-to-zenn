---
title: "100日後にRustをちょっと知ってる人になる: [Day 18]WebAssembly (Wasm)"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly, wasm]
published: false
---
## Day 18 のテーマ

Rust で作られたモノというものを見たことありますか？
多分なのですが、実際に自分で触ってみたりしたことがある Rust で作られたモノっていうのは、コマンドラインとかが多かったりしませんか？

たとえばこういうコマンドラインなどです：

- [bat (catの代替)](https://github.com/sharkdp/bat)
- [exa (lsの代替](https://github.com/ogham/exa)
- [fd (findの代替)](https://github.com/sharkdp/fd)
- [ripgrep (grepの代替](https://github.com/BurntSushi/ripgrep)
- [delta (diffの代替)](https://github.com/dandavison/delta)

他にも数多く Rust 製のコマンドがあります。軽いし便利なモノが多くて僕もイロイロと見つけては使ったりとしています。
このように Rust でコマンドが作られている理由の１つには、Rust がクロスプラットフォーム開発に対応しているから、ということも言えると思います。
一度作ったものを様々なところで使えるというのは便利ですよね。

まさに、かつて Java で言われ始めていた、**「Write once, Run anywhere」** という感じですよね。

今日はコマンドラインの作り方について考えるというのではなくて、新しい **「Write once, Run anywhere」** ともいわれている、**WebAssembly (Wasm)** についてです。

![](https://storage.googleapis.com/zenn-user-upload/a21d84ae3e5d-20220909.png)

## Day 18 のまとめ
