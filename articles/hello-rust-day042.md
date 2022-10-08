---
title: "100日後にRustをちょっと知ってる人になる: [Day 42]属性 (アトリビュート)"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 42 のテーマ

[Day 41](https://zenn.dev/shinyay/articles/hello-rust-day041) では、**幽霊型 (Phantom Type)** という僕もあまり慣れない書式について見てみました。

そこで、幽霊型を使っている構造体から作ったオブジェクトの比較を行い、使わない型パラメータを仕込んでおくことにより異なる型として扱えることを見てみました。

そのオブジェクト同士の比較をするときなのですが、実は昨日は全く説明していないコードを記載していました。
これです

```rust
#[derive(Debug,PartialEq)]
```

これをどこで使っていたかというと、幽霊型を用いていた構造体の宣言時に使っていました。

```rust
#[derive(Debug,PartialEq)]
struct PhantomStruct<X, A> {
    value: A,
    phantom: PhantomData<X>
}
```

これは `derive` という属性を構造体に付与して、`derive` が提供している性質によって `Debug` と `PartialEq` という振る舞いを追加していたのです。

実はこの `derive` は Rust の**手続きマクロ**の一種になります。Rust にはマクロの定義の仕方が複数あります:

- 宣言型マクロ
- 手続き型マクロ
  - カスタム Derive マクロ
  - 属性型マクロ
  - 関数型マクロ

マクロ１つのとっても奥が深いです…

と、マクロについていろいろ言ったものの、まとまって今度マクロについて勉強しようと思います。
今日は、`derive` マクロではなく、`#[derive()]` について考えたいと思います。つまり、**属性 (アトリビュート)** について見てみます。

## 属性 (アトリビュート)

**属性 (アトリビュート)** とは、以下のような Rust の構文に対して **メタデータ (追加機能)** を追加できるような書式です:

- クレート
- モジュール
- 関数
- 構造体
など

書式としては、先に記載していた derive 属性の書き方にあったように、`#` と `[]` で定義します。

```rust
#[item_attribute]
```

それと、クレート全体に適用する場合の属性は、`!` を追加する必要があります。

```rust
#![crate_attribute]
```

属性に対するパラメータの設定はいくつかの書式があります:

- `#[attribute = "value"]`
- `#[attribute(key = "value")]`
- `#[attribute(value)]`

もちろん、これらのパラメータを複数設定することが可能です。

- `#[attribute(value1, value2, value3)]`

### 属性の用途

Rust の公式公式ドキュメントを見ると、主に次のような用途で属性を使うようです:

- コンパイル時の条件分岐
- クレート名、バージョン、種類（バイナリか、ライブラリか）の設定
- リントの無効化 (警告の抑止)
- コンパイラ付属の機能（マクロ、glob、インポートなど）の有効化
- 外部ライブラリへのリンク
- ユニットテスト用の関数として明示
- ベンチマーク用の関数として明示

## 頻出の属性

使用頻度が比較的高いと思われる属性が次のものです:

- `test` 属性
- `cfg` 属性
- `derive` 属性
- `allow` 属性
- `deny` 属性

### test 属性

単体テストを作成するときに使用する属性です。
`#[test]` と属性がついている関数のみが単体テストとして実施されます。

`cargo test` で実行されます。

```rust
#[test]
fn it_works() {
    assert_eq!(2 + 2, 4);
}
```

### cfg 属性

条件を宣言し、コンパイル時のその条件に応じたコンパイルを実施するための属性です。

`#[cfg]` に条件をパラメータ設定して使用する。

```rust
#[cfg(windows)]
fn something_for_windows(){
   // Windows 環境に依存した処理を記述
}
```

### derive 属性

`derive` 属性に対応したトレイトの実装を自動的に構造体や列挙型に実装することのできる属性です。

`Debug` を実装する場合:

`Debug`トレイトの `fmt` 関数が自動的に実装されているので、`:?`フォーマット文字列をつかうことができます。

```rust
#[derive(Debug)]
struct Point{ x: i32, y: i32, z: i32 }

fn main(){
    let some_point = Point {x: 10, y: 20, z: 0};
    println!("Debug: {:?}", some_point);
}
```

```shell
[Running] 
Debug: Point { x: 10, y: 20, z: 0 }

[Done] exited with code=0 in _.___ seconds
```

### allow 属性

Rust には **Lint チェック**というソースコードの静的解析をしてくれるしくみがあります。

- [リント一覧](https://doc.rust-lang.org/rustc/lints/listing/index.html)

そのチェック対象とされているリント項目を無視するようにするための属性です。

```rust
fn used_function() {}

#[allow(dead_code)]
fn unused_function() {}

fn main() {
    used_function();
}
```

`unused_function` 関数は使用されていないので警告が通常なら出力されますが、`#[allow(dead_code)]` によりリントチェック `dead_code` ルールを無視するようにしています。そのため警告が出力されません。

- [](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#dead-code)

### deny 属性

`allow` 属性とは逆に、リントチェックの内容を全てエラーとする属性です。

次の例はアンチパターンとして有名なものなので、設定しないで欲しいのですが、問題があればビルドを停止させるために `deny` 属性でリントチェックの `warning` ルールを設定しています、＝。

```rust
#![deny(warnings)]

// 全て正しいコード
```

## Day 42 のまとめ

属性をつけるのみで機能や性質を追加することができるのでとても便利な仕組みだということが分かりました。
Rust のサンプルコードを見ていると頻繁に以下の書式な属性を目にすることがあります。

- `#[attribute = "value"]`
- `#[attribute(key = "value")]`
- `#[attribute(value)]`

これらを見つけたら、どんなメタデータを付加する属性なのか、パラメータによってどんな効果を期待しているのか都度都度調べようと思いました。
