---
title: "100日後にRustをちょっと知ってる人になる: [Day 61]1.65.0 のリリースノート"
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

### コンパイラ

- [Linuxでの `-Csplit-debuginfo` フラグの安定化](https://github.com/rust-lang/rust/pull/98051/)
- [複数のバリアントがデータを持っている場合でも、ニッチフィリング最適化を使用する](https://github.com/rust-lang/rust/pull/94075/)
- [関連型射影が、基礎となるタイプを解決する前に整形されているかどうか確認される](https://github.com/rust-lang/rust/pull/99217/#issuecomment-1209365630)
- [非短縮形の可視性を正しく文字列化](https://github.com/rust-lang/rust/pull/100350/)
- [サイズ変更時に構造体フィールドの型を正規化](https://github.com/rust-lang/rust/pull/101831/)
- [LLVM 15 へのアップデート](https://github.com/rust-lang/rust/pull/99464/)
- [aarch64 の ABI 呼び出しを修正](https://github.com/rust-lang/rust/pull/97800/)
- [列挙型に対する　C++　ライクなエンコーディングを一般化](https://github.com/rust-lang/rust/pull/98393/)
- [`special_module_name` lint の追加](https://github.com/rust-lang/rust/pull/94467/)

### ライブラリ

- [derive(PartialEq) で `PartialEq::ne` を生成しない](https://github.com/rust-lang/rust/pull/98655/)
- [Windows RNG: デフォルトで `BCRYPT_RNG_ALG_HANDLE` を使用](https://github.com/rust-lang/rust/pull/101325/)
- [システムアロケータコールと `System::alloc` 混在を禁止](https://github.com/rust-lang/rust/pull/101394/)

### Cargo

- [部分的ハッシュでも GitHub のファストパスを適用](https://github.com/rust-lang/cargo/pull/10807/)
- [`$HIME/bin` のパスが既にある場合は PATH に追加しない](https://github.com/rust-lang/cargo/pull/11023/)
- [ペンディングキュー内の優先順位を考慮](https://github.com/rust-lang/cargo/pull/11032/)

## Day 61 のまとめ

正直、細かなところはやっぱり僕の理解度ではまだまだ追いつけない内容がほとんどでした…

さて、今回のアップデートの内容で一番注目を集めているのは、待望と言われている **[汎用関連型 (Generic Associated Types) の安定化](https://github.com/rust-lang/rust/pull/96709/)** です。
この内容について、明日にかけてもみていきたいな、と思っています。
