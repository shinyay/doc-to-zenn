---
title: "100日後にRustをちょっと知ってる人になる: [Day 61]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 61 のテーマ

11 月になりました。今年ももうあと残すところ 2 ヶ月ですね。
1 年が過ぎ去るのがあっという間に感じるようになってきてしまいました。

同じ用に、OSS など製品やツールのバージョンアップの間隔ももあっという間のように感じるようになっています。
というわけで、11 月 3 日に **Stable** 版公開予定のバージョン `1.65.0` の内容を少し見てみたいかなと思います。

## Rust 1.65.0

GitHub に公開されている、`1.65.0` のリリースノートはこちらです。

- [Release Note](https://github.com/rust-lang/rust/blob/master/RELEASES.md#version-1650-2022-11-03)

リリースノートでは、毎回以下の観点でのアップデート情報が記載されます。

- 言語
- コンパイラ
- ライブラリ
- Cargo

正直、まだ僕の Rust 力 では、ひと目で内容を判別できないので分からない事がある前提で少しアップデート内容を拾い上げてみます。

### 言語

- [#[non_exhaustive] バリアントを持つ列挙型のキャストでエラー](https://github.com/rust-lang/rust/pull/92744/)
- [`let else`の安定化](https://github.com/rust-lang/rust/pull/93628/)
- [汎用関連型 (Generic Associated Types) の安定化](https://github.com/rust-lang/rust/pull/96709/)
- [Clippy から `let_underscore_drop`, `let_underscore_lock` および `let_underscore_must_use` の追加](https://github.com/rust-lang/rust/pull/97739/)
- [任意のラベル付きブロックからの `break` の安定化 ("label-break-value")](https://github.com/rust-lang/rust/pull/99332/)
- [未初期化の整数、浮動小数点、生ポインタは即時に**未定義動作**と見なされる (Undefined Behavior)](https://github.com/rust-lang/rust/pull/98919/)
- [Windows x86_64、aarch64、および thumbv7a 用の raw-dylib を安定化](https://github.com/rust-lang/rust/pull/99916/)
- [外部の ADT で `Drop` の実装を許可しない](https://github.com/rust-lang/rust/pull/99576/)
