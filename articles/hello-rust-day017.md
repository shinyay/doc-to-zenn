---
title: "100日後にRustをちょっと知ってる人になる: [Day 17]トレイト"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 17 のテーマ

Day 16 でクロージャの扱いについて考えている中で、きちんと Rust の**トレイト**という仕組みのことを理解した上でないと説明しきれないところがあると思いました。
ということで、今日は**トレイト**についてまとます。

## トレイト

基本に立ち戻り、[The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html) でのトレイトの定義を見てみようと思います。

- [Traits: Defining Shared Behavior](https://doc.rust-lang.org/book/ch10-02-traits.html)

> A trait defines functionality a particular type has and can share with other types.

つまり、**特定の型に対して任意の振る舞いを設定するための機能** です。言い換えると、**複数の型で利用目的や呼び出し方法が共通である関数があるとき**、それらをトレイトとしてまとめて使用します。

## Day 17 のまとめ
