---
title: "100日後にRustをちょっと知ってる人になる: [Day 90]Fermyon Spin v0.7.0"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 90 のテーマ

[Day 87](https://zenn.dev/shinyay/articles/hello-rust-day087)、そして[Day 88](https://zenn.dev/shinyay/articles/hello-rust-day088) といろいろなモジュールの新しくリリースされたバージョンを見てみました。
そして今日も新しいものの発表があったので、それを見てみようと思います。

[Day 57](https://zenn.dev/shinyay/articles/hello-rust-day087) で紹介をしていた **Fermyon Spin** が 12 月 16 日にv0.7.0 が発表されていました。今日はそのアップデートについて見たみたいと思います。

## Fermyon Spin

![](https://storage.googleapis.com/zenn-user-upload/dbab6a58664b-20221219.png)

Spin については [Day 57](https://zenn.dev/shinyay/articles/hello-rust-day087) の中で使い方について紹介をしているので、そちらを見て欲しいと思います。
簡単に少しだけ説明すると、**WebAssemby** をコンパイルターゲットとするフレームワークです。フレームワークというと、ある特定の言語で作業効率をよくするために用いられる事が多いと思います。この Spin は様々な多言語に対応しているフレームワークです。
Web アプリケーションやマイクロサービスのような HTTP リクエストへの応答を実行できる WebAssembly モジュールを作成するためのインターフェースを提供できるフレームワークになっています。

そして、ぼくがよく Spin を伝えるときに使っている代表的な 3 つのコマンドが次のものです。

✨spin new
🛠spin build
🚀spin deploy

極端な話でいうと、この 3　コマンドがあればビルドして実行することが可能となります。

## Spin v0.7.0 インストール

Spin v0.7.0 の内容を見ていく前にとりあえず、インストールを行います。アップグレードも上書きインストールです。

```shell
$ curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash

Step 1: Downloading: https://github.com/fermyon/spin/releases/download/v0.7.0/spin-v0.7.0-macos-amd64.tar.gz
Done...

Step 2: Decompressing: spin-v0.7.0-macos-amd64.tar.gz
x README.md
x LICENSE
x spin
spin 0.7.0 (73d315f 2022-12-15)
Done...

Step 3: Removing the downloaded tarball
Done...

You're good to go. Check here for the next steps: https://developer.fermyon.com/spin/quickstart
Run './spin' to get started

$ sudo mv spin /usr/local/bin/
```

これでアップグレード完了です。確認をしてみましょう。

```shell
$ spin -V

spin 0.7.0 (73d315f 2022-12-15)
```

`0.7.0` になっていました✨

## Spin v0.7.0

それでは、Spin v0.7.0 について見ていこうと思います。リリースノートはこちらです。

- [v0.7.0](https://github.com/fermyon/spin/releases/tag/v0.7.0)

v0.7.0 では次のようなフィーチャーが追加されていました:

- [Hashicorp Vault との統合](https://github.com/fermyon/spin/pull/798)
- [MySQL データベースへの接続の実験的サポート](https://github.com/fermyon/spin/pull/864)
- [既存のアプリケーションにコンポーネントを追加する「spin add」コマンド](https://github.com/fermyon/spin/pull/889)
- [Redis のセット操作に対応](https://github.com/fermyon/spin/pull/915)
- [Web URL からの Wasm モジュールのフェッチに対応](https://github.com/fermyon/spin/pull/890)
- [Linux ARM64上でのSpinの実行をサポート](https://github.com/fermyon/spin/pull/926)
- [JavaScriptおよびTypescriptアプリケーションの実験的サポート](https://github.com/fermyon/spin-js-sdk)
- [Wasmtime 3.0.0 ベース](https://github.com/fermyon/spin/pull/917)

また、次のような連絡事項もありました。

- [Ubuntu 18.04 のサポートを終了](https://github.com/fermyon/spin/issues/990)
- [テンプレートはローカルでも更新が必要な場合あり](https://github.com/fermyon/spin/issues/990)
  - `spin templates install --git https://github.com/fermyon/spin --update`

ここで挙げられているアップデート内容をいくつか掘り下げて見てみたいと思います。

### テンプレートはローカルでも更新が必要な場合あり

とりあえず、テンプレートの変更を行っておきます。

```shell
spin templates install --git https://github.com/fermyon/spin --update
```

以下のようなテンプレートが更新・インストールされました。

```shell
Copying remote template source
Installing template redis-rust...
Installing template static-fileserver...
Installing template http-grain...
Installing template http-swift...
Installing template http-c...
Installing template redirect...
Installing template http-rust...
Installing template http-go...
Installing template http-zig...
Installing template http-empty...
Installing template redis-go...
Installed 11 template(s)

+------------------------------------------------------------------------+
| Name                Description                                        |
+========================================================================+
| http-c              HTTP request handler using C and the Zig toolchain |
| http-empty          HTTP application with no components                |
| http-go             HTTP request handler using (Tiny)Go                |
| http-grain          HTTP request handler using Grain                   |
| http-rust           HTTP request handler using Rust                    |
| http-swift          HTTP request handler using SwiftWasm               |
| http-zig            HTTP request handler using Zig                     |
| redirect            Redirects a HTTP route                             |
| redis-go            Redis message handler using (Tiny)Go               |
| redis-rust          Redis message handler using Rust                   |
| static-fileserver   Serves static files from an asset directory        |
+------------------------------------------------------------------------+
```

以前は、8 種類だったので次のものが増えていますね。

- **http-empty**
- **redirect**
- **static-fileserver**

```shell
+-----------------------------------------------------------------+
| Name         Description                                        |
+=================================================================+
| http-c       HTTP request handler using C and the Zig toolchain |
| http-go      HTTP request handler using (Tiny)Go                |
| http-grain   HTTP request handler using Grain                   |
| http-rust    HTTP request handler using Rust                    |
| http-swift   HTTP request handler using SwiftWasm               |
| http-zig     HTTP request handler using Zig                     |
| redis-go     Redis message handler using (Tiny)Go               |
| redis-rust   Redis message handler using Rust                   |
+-----------------------------------------------------------------+
```


### Hashicorp Vault との統合

![](https://storage.googleapis.com/zenn-user-upload/8661dcb6de56-20221219.png)

**Hashicorp Vault** はとても有名な機密情報の管理ツールなのでご存知の方も多いのではないでしょうか。**トークン**や、**パスワード**、また**証明書**、**暗号鍵**といった機密情報へのアクセスを安全に保管し、厳密に制御するオープンソースツールです。**UI**、**CLI**、**HTTP API**を使用して機密データへのアクセスを安全に行うことができます。

- [Hashicorp Vault](https://www.vaultproject.io/)

それでは、Vault にデータを入れてみます。

```shell
vault server -dev -dev-root-token-id root
vault kv put secret/password value="my-name-is-yanashin18618!"
```

ここでは、`vault server` と `vault kv` というコマンドを使い登録を行いました。それぞれのコマンドの詳細な内容については次の公式ドキュメントで紹介されています。

- [vault server](https://developer.hashicorp.com/vault/docs/commands/server)
- [vault kv](https://developer.hashicorp.com/vault/docs/commands/kv)

このようにして Vault に登録したデータを `runtime-config.toml` を使用して **spin** に読み込み設定を行います。このファイルは spin の起動時に読み込まれる構成ファイルです。

- [Configuration for Spin applications](https://developer.fermyon.com/spin/configuration#runtime-configuration)

以下のような `toml` を定義します。

```toml
[[config_provider]]
type = "vault"
url = "<adress-to-vault>"
token = "root"
mount = "secret"
```

あとは、取得を行うのみです。

```rust
let password:Result<String, spin_sdk::config::Error> = spin_sdk::config::get("password");
```

### MySQL データベースへの接続の実験的サポート

v0.7.0 では、Spin アプリケーションから **MySQL** データベースへの接続をサポートされるようになりました。

このデータベースサポートは、WASI の提案の中で次の `wasi-sql` というものがあるのですが、それに従っているようです。

- [](https://github.com/WebAssembly/wasi-sql)

次のようにして、参照を行うようです。

```rust
fn get(id: i32) -> Result<Response> {

     let address = spin_sdk::config::get("database")?;

     let sql = "SELECT id, first_name, last_name FROM employee WHERE id = ?";
     let params = vec![ParameterValue::Int32(id)];
     let rowset = mysql::query(&address, sql, &params)?;

     match rowset.rows.first() {
         None => Ok(http::Response::builder().status(404).body(None)?),
         Some(row) => {
             let emp = as_emp(row)?;
             let response = format!("{:?}", emp);
             Ok(http::Response::builder()
                 .status(200)
                 .body(Some(response.into()))?)
         }
     }
 }
```

## 既存のアプリケーションにコンポーネントを追加する「spin add」コマンド

今までの Spin プロジェクトは、1 アプリケーションにつき、1 コンポーネントでした。`spin new` で作ったプロジェクトに含まれるコンポーネントで開発を行っていました。今回、`spin add` コマンドにより 1 プロジェクトに対して複数のコンポーネントを追加することができるようになりました。

空のプロジェクトを要して、追加をしてみます。

```shell
spin new http-empty
```

中身は toml が置かれているだけの空のプロジェクトです。

```shell
$ ls

spin.toml
```

`spin add` を使用して、コンポーネントを追加してみます。

```shell
$ spin add http-rust
$ spin add http-go
```

以下のようにコンポーネントが追加されています。これで、1 アプリケーションに複数のコンポーネント、それも複数の言語で作ることが可能になります。モジュラーモノリスのような構成が作れそうですね。

```shell
$ ls
go-component/   rust-component/ spin.toml
```

## JavaScriptおよびTypescriptアプリケーションの実験的サポート

12 月 3 日に spin v0.7.0 より一足先に公開されていたのが、この **JavaScript** と **TypeScript** の **SDK** です。

- [Introducing the Spin JavaScript and TypeScript SDK](https://www.fermyon.com/blog/spin-js-sdk)

この SDK に Spin が対応したことで、JavaScriptとTypeScriptのアプリケーションの開発が行えるようになりました。

JavaScript による Hello World なサンプルはこちらです。

```js
export async function handleRequest(request) {
  return {
    status: 200,
    headers: { "content-type": "text/plain" },
    body: encoder.encode("Hello JavaScript").buffer,
  };
}
```

### Wasmtime 3.0.0 ベース

この Spin v0.7.0 は **Wasmtime** 3.0.0 の上で開発されています。古いバージョンを使用している場合は、アップグレードをしてください。

例えば、次のように古いバージョンを使用している場合です。

```shell
$ wasmtime -V

wasmtime-cli 0.40.1
```

上書きインストールをして、アップグレードを行ってください。

```shell
curl https://wasmtime.dev/install.sh -sSf | bash
```

```shell
$ wasmtime -V

wasmtime-cli 3.0.1
```

## Day 90 のまとめ

