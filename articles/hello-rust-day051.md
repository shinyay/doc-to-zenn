---
title: "100日後にRustをちょっと知ってる人になる: [Day 51]Wasm Workers Server の動作"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust,webassembly,wasm]
published: true
---
## Day 51 のテーマ

[Day 50](https://zenn.dev/shinyay/articles/hello-rust-day050) では、OSS プロジェクトとして公開されたばかりの **Wasm Worker Server** について基本的なところを見て、さらにリクエストを受け付けて簡単な平文メッセージをレスポンスするだけのワーカーアプリケーションを作って動かしてみました。

チュートリアルの中でも動かし方を中心に追いかけるように環境を準備し、ワーカーを作成して動作を確認したのみだったので、もう少しどのように動くかを見てみようと思います。

## Wasm Workers Server に関する復習

**[Wasm Worker Server](https://github.com/vmware-labs/wasm-workers-server)** は、WebAessembly を用いてアプリケーションを動作させるための HTTP サーバーでした。
この動作させるアプリケーションのことは、ワーカー (Worker) と呼ばれ、一般的には Edge などで動作させたりするような軽量なアプリケーション仕様です。

- [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers)

このアプリケーションは、**ハンドラ** と呼ばれるモジュールを作成し、単一あるいは複数のハンドラを組み合わせて構成します。これらのハンドラは、それぞれアプリケーション内部で特定の HTTP パスに対してレスポンスする役割をもっています。

言語サポート:

|言語|Wasmモジュール|インタプリタ|
|---|------------|----------|
|Rust|🙆🏻‍♀️|🙅‍♂️|
|JavaScript|🙅‍♂️|🙆🏻‍♀️|
|拡張予定...|拡張予定...|拡張予定...|

というわけで、昨日は Rust でのハンドラモジュールを作成してみました。

## Wasm Workers Server の動作

ハンドラは次のように動作します:

- 👉 リクエストの受付けとレスポンスの返却
- 👉 WASI Standard Input / Output を介したデータの送受信

**STDIN** と **STDOUT** を使用したデータ送受信を行うインターフェースにすることにより、この **Wasm Workers Server** 以外の WASI ランタイム環境でも動作する互換性のあるハンドラを作成することができます。

サーバーは次のように動作します:

- 1️⃣ 指定したフォルダにある `.wasm` モジュールの識別
- 2️⃣ 各モジュールへの HTTP ルートの関連付け
- 3️⃣ (必要に応じて) Key / Value インメモリストア の作成
- 4️⃣ **Wasmtime** ランタイムの初期化
- 5️⃣ モジュールのコンパイルと初期化
- 6️⃣ リクエスト処理の開始のための HTTP サーバーの待機

## サンプルワーカーの復習

昨日作成したサンプルのワーカーは受け付けたリクエストに対してレスポンスを返すのみの非常にシンプルなものでした。

```rust
#[handler]
fn reply(req: Request<String>) -> Result<Response<String>> {
    Ok(http::Response::builder()
    .status(200)
    .header("x-generated-by", "wasm-workers-server")
    .body(String::from("Hello Wasm!").into())?)
}
```

とはいえ、中身を少しみてみようと思います。

`fn reply()` 関数に対して `handler` マクロを設定しています。

この `handler` マクロは次のように定義されているものです:

```rust
#[proc_macro_attribute]
pub fn handler(attr: TokenStream, item: TokenStream) -> TokenStream {
    expand::expand_macro(attr, item)
}
```

手続き型マクロを定義する関数になっていることが当然ですが分かります。`TokenStream` を入力として受け取って、`TokenStream` を出力として生成しています。`TokenStream` 型は Rust に内蔵されている `proc_macro` クレートで定義されていて、トークンの列を表すのものでした。

- [Struct proc_macro::TokenStream](https://doc.rust-lang.org/beta/proc_macro/struct.TokenStream.html)
- [Macros](https://doc.rust-lang.org/book/ch19-06-macros.html)

そして、`expand_macro()` は次のようになっています。

```rust
    let main_fn = quote! {
        use wasm_workers_rs::io::{Input, Output};
        use std::io::stdin;

        fn main() {
            let input = Input::new(stdin());
            let error = Output::new(
                "There was an error running the handler",
                500,
                None,
                None
            ).to_json().unwrap();

            if let Ok(input) = input {
                let mut cache = input.cache_data();

                if let Ok(response) = #func_call {
                    match Output::from_response(response, cache).to_json() {
                        Ok(res) => println!("{}", res),
                        Err(_) => println!("{}", error)
                    }
                } else {
                    println!("{}", error)
                }
            } else {
                println!("{}", error)
            }
        }

        #handler_fn
    };
```

まさに、ハンドラの動作の仕方のところで説明したように、データの送受信が `STDIN` と `STDOUT` が仕様されていることが分かります。

そしてレスポンスを構成している箇所は、`http::response::Builder` による定石通りです。

- レスポンスに対する **HTTP ステータス**
- **ヘッダー**
- レスポンスメッセージの本体となる**ボディ**

それ以外のことも `Builder` が提供するメソッドを通じて実装することも可能です。

- [Struct http::response::Builder](https://docs.rs/http/0.2.8/http/response/struct.Builder.html)

## Day 51 のまとめ

Day 50 でもハンドラの実装と実行を行いましたが、ハンドラモジュール自体にはサーバーエンジンを含まず関数だけでした。まさに WebAssembly によるサーバーレスアプリケーション、Function as a Service 的な動作の充実を期待したくなるものでした。
