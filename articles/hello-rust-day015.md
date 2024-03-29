---
title: "100日後にRustをちょっと知ってる人になる: [Day 15]dev container"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: true
---
## Day 15 のテーマ

Day 14 では **GitHub Codespaces** で Rust 環境を作ることにチャレンジしてみました。
昨日の結果として分かったことは次のことでした。

- 「GitHub」+「Visual Studio Code」+「Ubuntu」が動作するクラウド環境ということ
- Codespaces で提供されるデフォルトのコンテナ環境には Rust のランタイム環境が入っていないということ
- **[dev container](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/introduction-to-dev-containers)** という仕組みを使ってランタイム環境をカスタマイズできるということ

というわけで、今日は **dev container** を使って Rust 環境を作ろうと思います。

## dev container の作成

**dev container** はプロジェクトルートに以下のような構成でファイルを配置して設定を行います。

```shell
.devcontainer/
├── Dockerfile
└── devcontainer.json
```

- **devcontainer.json**: Codespaces の設定ファイル
- **Dockerfile**: dev container の実態

これらの設定ファイルを用意していきます。

### VS Code からの作成

VS Code にインストールした Codespaces の拡張機能では、**dev container** を作成する機能が提供されています。それを使用して `.devcontainer` を作成していきます。

#### 1. コマンドパレットから dev container 作成メニューの選択

**⌘ + ⇧ + P** で VS Code のコマンドパレットを開きます。
メニューに `Codespaces` と入力し、`Codespaces: Add Development Container Config...` を選択します。

![](https://storage.googleapis.com/zenn-user-upload/1380768154dc-20220906.png)

#### 2. Rust 用の dev container 定義の選択

なんと今まで知らなかったのですけれど、**Rust 用の dev container** 定義が提供されていました！
ゼロベースで作る必要があると思っていたのですけど、これはうれしい。
ありがとう、VS Code 🙏
これを選んでみます。

![](https://storage.googleapis.com/zenn-user-upload/58bb19cdabba-20220906.png)

#### 3. Ubuntu(Debian) ベースイメージのバージョン選択

**buster** がデフォルトと表示されているので、これを選択します。

|Ubutu|Debian|略称|
|-----|------|---|
|18.04 - 19.10|10|buster|
|20.04 - 21.10|11|bullsye|

![](https://storage.googleapis.com/zenn-user-upload/b4e6fd4d3034-20220906.png)

#### 4. dev container 設定

**devcontainer.json** に定義されると思われる、dev container に含める CLI やツールをここで選択できるようです。

![](https://storage.googleapis.com/zenn-user-upload/4b5a41763c2e-20220906.png)

試しに dev container 内でコンテナを使用できるように **Docker in Docker** を選択してみます。

![](https://storage.googleapis.com/zenn-user-upload/ac2adb57cf1e-20220906.png)

dev container に含める **Docker Engine** のバージョンを選択します。

![](https://storage.googleapis.com/zenn-user-upload/da5209acd16e-20220906.png)

#### 5. .devcontainer の確認

以下のようにプロジェクトルートに ***.devcontainer** が作成されます。

![](https://storage.googleapis.com/zenn-user-upload/69d2ad717164-20220906.png)

**JSON** と **Dockerfile** にアクセスすると、閲覧・編集支援の以下のプラグインのインストールがリコメンドされたので、両方ともインストールしました。

- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

![](https://storage.googleapis.com/zenn-user-upload/de12d42af444-20220906.png)

- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

![](https://storage.googleapis.com/zenn-user-upload/7899d5de9cc5-20220906.png)

## dev container の確認

以下のような構成で **.devcontainer** が作成されました。

```shell
.devcontainer/
├── Dockerfile
└── devcontainer.json
```

作成されたファイルの内容を確認していきます。

### devcontainer.json

以下の JSON が自動生成されたものです。

```json
{
	"name": "Rust",
	"build": {
		"dockerfile": "Dockerfile",
		"args": {
			"VARIANT": "buster"
		}
	},
	"runArgs": [
		"--cap-add=SYS_PTRACE",
		"--security-opt",
		"seccomp=unconfined"
	],

	"customizations": {
		"vscode": {
			"settings": { 
				"lldb.executable": "/usr/bin/lldb",
				"files.watcherExclude": {
					"**/target/**": true
				},
				"rust-analyzer.checkOnSave.command": "clippy"
			},
			
			"extensions": [
				"vadimcn.vscode-lldb",
				"mutantdino.resourcemonitor",
				"rust-lang.rust-analyzer",
				"tamasfe.even-better-toml",
				"serayuzgur.crates"
			]
		}
	},

	"remoteUser": "vscode",
	"features": {
		"docker-in-docker": "latest"
	}
}

```

**customizations.vscode.extensions** に **rust-lang.rust-analyzer** が入っていました。

- [rust-lang/rust-analyze](https://github.com/rust-lang/rust-analyzer)

これは VS Code 上で Rust の補完を行ったりする拡張機能のようです。

### Dockerfile

以下の Dockerfile が自動生成されたものです。

```dockerfile
ARG VARIANT="buster"
FROM mcr.microsoft.com/vscode/devcontainers/rust:0-${VARIANT}
```

## dev container の実行

エラーが出てしまいました…

**rust-analyzer** の ブートストラップエラーが出ていました。
さて、調べて直していくとしましょうか。。。

```shell
INFO [9/6/2022, 7:11:22 AM]: Using server binary at /home/vscode/.vscode-remote/extensions/rust-lang.rust-analyzer-0.3.1194-linux-x64/server/rust-analyzer
ERROR [9/6/2022, 7:11:22 AM]: Bootstrap error Error: Failed to execute /home/vscode/.vscode-remote/extensions/rust-lang.rust-analyzer-0.3.1194-linux-x64/server/rust-analyzer --version
    at OS (/home/vscode/.vscode-remote/extensions/rust-lang.rust-analyzer-0.3.1194-linux-x64/out/main.js:85:2328)
    at processTicksAndRejections (node:internal/process/task_queues:96:5)
    at xS (/home/vscode/.vscode-remote/extensions/rust-lang.rust-analyzer-0.3.1194-linux-x64/out/main.js:84:1220)
    at fv (/home/vscode/.vscode-remote/extensions/rust-lang.rust-analyzer-0.3.1194-linux-x64/out/main.js:84:891)
    at E._activate (/vscode/bin/linux-x64/784b0177c56c607789f9638da7b6bf3230d47a8c/out/vs/workbench/api/node/extensionHostProcess.js:85:8224)
    at E._waitForDepsThenActivate (/vscode/bin/linux-x64/784b0177c56c607789f9638da7b6bf3230d47a8c/out/vs/workbench/api/node/extensionHostProcess.js:85:8166)
    at E._initialize (/vscode/bin/linux-x64/784b0177c56c607789f9638da7b6bf3230d47a8c/out/vs/workbench/api/node/extensionHostProcess.js:85:7530)
```

### 問題対応

とりあえず、問題切り分けのために、とりあえずで入れていた **Docker in Docker** を外してみます。
以下の部分を削除します。

```json
"features": {
    "docker-in-docker": "latest"
}
```

あれ？？
外しただけで動くようになりました。

![](https://storage.googleapis.com/zenn-user-upload/fef02726d70c-20220906.png)

Route Cause を見つけてないのですけど…
とりあえず、今はこれで進めておこうと思います。そもそも使う用途なく Docker in Docker を追加していたことが問題なので…

## GitHub Codespaces 上で Rust を実行

問題なく動作しました！

![](https://storage.googleapis.com/zenn-user-upload/b36b758cb81c-20220906.png)

## Day 15 のまとめ

今日は、 昨日 Day 14 に引き続いて **GitHub Codespaces** で Rust の環境を整えてみました。
エラーが発生して戸惑ったものの、単に Rust を実行する環境だけであれば難なく作れそうなことが分かりました。
あとは、Codespaces 上の VS Code に対する設定と、それを動かすコンテナ環境の準備の仕方 (**dec container**) が少しわかりました。この昨日は便利に活用していきたいかなと思います。
