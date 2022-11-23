---
title: "100日後にRustをちょっと知ってる人になる: [Day 69]"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 69 のテーマ

[Day 68](https://zenn.dev/shinyay/articles/hello-rust-day068) では、**[Blessed.rs](https://blessed.rs/crates)** で紹介されている Lint ツールの **clippy** の使い方を見てみました。今日も引き続き、Blessed.rs で紹介されているクレートを見てみたいかなと思います。

![](https://storage.googleapis.com/zenn-user-upload/cd796ca47507-20221123.png)

というわけで、開発ツールで紹介されている **コードフォーマット**ツールの **rustfmt** について今日は見てみたいかなと思います。

## rustfmt

以下が **rustfmt** のリポジトリです。見てもらえば分かるように、先日の Lint ツールの [clippy](https://github.com/rust-lang/rust-clippy) 同様に、この rustfmt も **[rust-lang](https://github.com/rust-lang)** の配下におかれる Rust の公式なコードフォーマットツールです。

- [rust-lang/rustfmt](https://github.com/rust-lang/rustfmt)

この rustfmt は、コードのスタイルガイドラインに従って、作成するコードを整形するために用いられるものです。
デフォルトでは、次のスタイルガイドに準拠しているようです。

- [Rust Style Guide](https://github.com/rust-lang/fmt-rfcs/blob/master/guide/guide.md)

インデントやライン幅、空白行、またモジュールレベルの項目やステートメント、式、型などの項目でそれぞれフォーマットを定義しています。

## インストール

```shell
rustup component add rustfmt
```

これで、次のコマンドでコードフォーマットを実行できます。

```shell
rustfmt
```

あるいは

```shell
cargo fmt
```

## コードフォーマット実行

次のような、コードスタイルがおかしなサンプルコードを作成してみます。

```rust
fn main(){
for n in 0..10{
println!("{n}: Hello, Rust!");
}
}
```

インデントが崩れていて、ひと目でおかしなコードだとわかりますよね。ただ、コード的には間違いはないので実行はできます。

```shell
$ cargo run

0: Hello, Rust!
1: Hello, Rust!
2: Hello, Rust!
3: Hello, Rust!
4: Hello, Rust!
5: Hello, Rust!
6: Hello, Rust!
7: Hello, Rust!
8: Hello, Rust!
9: Hello, Rust!
```

あと、`clippy` も実施してみましたが特にエラーは発生しませんでした。

ここで、`cargo fmt` を実行してみます。特にメッセージが表示されるわけではないのですが、実行後にソースコードを見てください。

```shell
$git diff

-fn main(){
-for n in 0..10{
-println!("{n}: Hello, Rust!");
+fn main() {
+    for n in 0..10 {
+        println!("{n}: Hello, Rust!");
+    }
 }
-}
```

つまり、以下のようにコードが整形されていました。

```rust
fn main() {
    for n in 0..10 {
        println!("{n}: Hello, Rust!");
    }
}
```

ソースコードをコミットする前には必ず `rustfmt` を実行するという習慣をつけておくといいかもしれないですね。

## スタイルガイド設定

先にも書いていたように、`rustfmt` では、[RFC](https://github.com/rust-lang/fmt-rfcs) で規定された Rust スタイルガイドに準拠したスタイルになっています。利用可能なスタイルオプションは、次のコマンドで確認出来ます。

```shell
rustfmt --help=config
```

スタイルガイドをカスタマイズしたい場合は、`rustfmt.toml` というファイルを作成して定義を行うことが可能です。

次のコマンドを実行することで、デフォルト設定を書き出してくれるので、それをベースにカスタマイズするといいと思います。

```shell
rustfmt --print-config default rustfmt.toml 
```

## オプション一覧


|option名|設定値|説明|
|--:|:--|:--|
| verbose | \<boolean\><br>Default: false | Use verbose output|
| skip_children | \<boolean\><br>Default: false | Don't reformat out of line modules|
| [max_width]| \<unsigned integer\><br>Default: 100 | Maximum width of each line|
| ideal_width | \<unsigned integer\><br>Default: 80 | Ideal width of each line|
| [tab_spaces] | \<unsigned integer\><br>Default: 4 | Number of spaces per tab|
| [fn_call_width] | \<unsigned integer\><br>Default: 60 | Maximum width of the args of a function call before falling back to vertical formatting|
| [struct_lit_width] | \<unsigned integer\><br>Default: 16 | Maximum width in the body of a struct lit before falling back to vertical formatting|
| newline_style | [Windows&#124;<br>Unix&#124;<br>Native] <br>Default: Unix | Unix or Windows line endings|
| [fn_brace_style] | [AlwaysNextLine&#124;<br>PreferSameLine&#124;<br>SameLineWhere] <br>Default: SameLineWhere | Brace style for functions|
| [item_brace_style] | [AlwaysNextLine&#124;<br>PreferSameLine&#124;<br>SameLineWhere] <br>Default: SameLineWhere | Brace style for structs and enums|
| [impl_empty_single_line] | \<boolean\><br>Default: true | Put empty-body implementations on a single line|
| [fn_empty_single_line] | \<boolean\><br>Default: true | Put empty-body functions on a single line|
| [fn_single_line] | \<boolean\><br>Default: false | Put single-expression functions on a single line|
| [fn_return_indent] | [WithArgs&#124;<br>WithWhereClause] <br>Default: WithArgs | Location of return type in function declaration|
| [fn_args_paren_newline] | \<boolean\><br>Default: true | If function argument parenthesis goes on a newline|
| [fn_args_density] | [Compressed&#124;<br>Tall&#124;<br>CompressedIfEmpty&#124;<br>Vertical] <br>Default: Tall | Argument density in functions|
| [fn_args_layout] | [Visual&#124;<br>Block&#124;<br>BlockAlways] <br>Default: Visual | Layout of function arguments|
| [fn_arg_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Visual |Indent on function arguments|
| [type_punctuation_density] | [Compressed&#124;<br>Wide] <br>Default: Wide | Determines if '+' or '=' are wrapped in spaces in the punctuation of types|
| [where_density] | [Compressed&#124;<br>Tall&#124;<br>CompressedIfEmpty&#124;<br>Vertical] <br>Default: CompressedIfEmpty | Density of a where clause|
| [where_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Tabbed | Indentation of a where clause|
| [where_layout] | [Vertical&#124;<br>Horizontal&#124;<br>HorizontalVertical&#124;<br>Mixed] <br>Default: Vertical | Element layout inside a where clause|
| [where_pred_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Visual | Indentation style of a where predicate|
| [where_trailing_comma] | \<boolean\><br>Default: false | Put a trailing comma on where clauses|
| [generics_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Visual | Indentation of generics|
| [struct_trailing_comma] | [Always&#124;<br>Never&#124;<br>Vertical] <br>Default: Vertical | If there is a trailing comma on structs|
| [struct_lit_trailing_comma] | [Always&#124;<br>Never&#124;<br>Vertical] <br>Default: Vertical | If there is a trailing comma on literal structs|
| [struct_lit_style] | [Visual&#124;<br>Block] <br>Default: Block | Style of struct definition|s
| [struct_lit_multiline_style] | [PreferSingle&#124;<br>ForceMulti] <br>Default: PreferSingle |
| [enum_trailing_comma] | \<boolean\><br>Default: true | Put a trailing comma on enum declarations|
| report_todo | [Always&#124;<br>Unnumbered&#124;<br>Never] <br>Default: Never | Report all, none or unnumbered occurrences of TODO in source file comments|
| report_fixme | [Always&#124;<br>Unnumbered&#124;<br>Never] <br>Default: Never | Report all, none or unnumbered occurrences of FIXME in source file comments|
| [chain_base_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Visual | Indent on chain base|
| [chain_indent] | [Inherit&#124;<br>Tabbed&#124;<br>Visual] <br>Default: Visual | Indentation of chain|
| [reorder_imports] | \<boolean\><br>Default: false | Reorder import statements alphabetically|
| [single_line_if_else] | \<boolean\><br>Default: false | Put else on same line as closing brace for if statements|
| [format_strings] | \<boolean\><br>Default: true | Format string literals where necessary|
| [force_format_strings] | \<boolean\><br>Default: false | Always format string literals|
| [chains_overflow_last] | \<boolean\><br>Default: true | Allow last call in method chain to break the line|
| [take_source_hints] | \<boolean\><br>Default: true | Retain some formatting characteristics from the source code|
| [hard_tabs] | \<boolean\><br>Default: false | Use tab characters for indentation, spaces for alignment|
| [wrap_comments] | \<boolean\><br>Default: false | Break comments to fit on the line|
| [normalise_comments] | \<boolean\><br>Default: true |Convert /* */ comments to // comments where possible|
| [wrap_match_arms] | \<boolean\><br>Default: true | Wrap multiline match arms in blocks|
| [match_block_trailing_comma] | \<boolean\><br>Default: false | Put a trailing comma after a block based match arm (non-block arms are not affected)|
| [match_wildcard_trailing_comma] | \<boolean\><br>Default: true | Put a trailing comma after a wildcard arm|
| write_mode | [Replace&#124;<br>Overwrite&#124;<br>Display&#124;<br>Diff&#124;<br>Coverage&#124;<br>Plain&#124;<br>Checkstyle] <br>Default: Replace | What Write Mode to use when none is supplied: Replace, Overwrite, Display, Diff, Coverage|

## Day 69 のまとめ

`rustfmt` はコードを自動に整形してくれてとても便利なツールだとわかりました。都度都度コードを整形しながらキレイな状態で保っていくとよさそうかなと思います。
また、PR するときなども礼儀として整形されたコードでコミットしたいかなと思いました。
