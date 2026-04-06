---
title: "GitHub Changelog 2026年4月"
emoji: "📋"
type: "tech"
topics: ["github", "githubcopilot", "githubactions", "vscode", "devtools"]
published: false
---

2026年4月のGitHub Changelogデイリーサマリーです。毎日の更新内容をスライドと解説でお届けします。

4月1日〜3日は**17件のアップデート**がありました。Copilotクラウドエージェントの署名付きコミット対応、GPT-5.1 Codex廃止、Copilot SDK パブリックプレビュー開始など、AIエージェント機能の本格展開が加速しています。

📊 **全スライド一覧**: [GitHub Pages →](https://shinyay.github.io/gh-changelog-zenn/2026-04/)

---
<!-- DAILY_MARKER -->

## 📅 2026年4月3日（4件のアップデート）

![2026年4月3日のサマリー](/images/github-changelog-2026-04/2026-04-03-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/03/)

---


### 🤖 Copilotクラウドエージェントがコミットに署名を付与

これにより、Copilotクラウドエージェントは[「Require signed commits」](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-signed-commits)ブランチ保護ルールまたはルールセットが有効になっているリポジトリでも動作するようになりました。以前は、このルールにエージェントが準拠できなかったため、該当リポジトリでの使用が完...


> **💡 ポイント**: 署名付きコミット要件が有効なリポジトリでもCopilotクラウドエージェントが利用可能になり、Enterprise環境でのAI活用が加速します。
---


### 🤖 GPT-5.1 Codex、GPT-5.1-Codex-Max、GPT-5.1-Codex-Miniが廃止

| モデル | 廃止日 | 推奨代替モデル |
| --- | --- | --- |
| GPT\-5\.1\-Codex | 2026\-04\-01 | GPT\-5\.3\-Codex |
| GPT\-5\.1\-Codex\-Mini | 2026\-04\-01 | GPT\-5\.3\-Codex |
| GPT\-5\.1\-Codex\-Max | 2026\-04\-01 | GPT\-5\.3\-Codex |


> **💡 ポイント**: GPT-5.1-Codexシリーズを使用していたユーザーは、GPT-5.3-Codexへの移行が必要です。自動モデル選択を利用している場合は影響ありません。
---


### 🤖 Copilotクラウドエージェントの Organization ファイアウォール設定

Organization管理者は、Organization内のすべてのリポジトリにわたってエージェントファイアウォールを管理できるようになりました。これにより、ニーズに合った適切なデフォルト設定とガードレールを備えたCopilotクラウドエージェントを大規模に展開することが容易になります。Organization管理者は以下のことが可能です：


> **💡 ポイント**: Organization管理者がCopilotエージェントのファイアウォールを一元管理できるようになり、大規模展開時のセキュリティガバナンスが大幅に向上します。
---


### 🤖 Copilotクラウドエージェントの組織レベルランナー制御

デフォルトでは標準のGitHubホステッドランナーで実行されますが、チームは[エージェント環境をカスタマイズ](https://docs.github.com/enterprise-cloud@latest/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment)して、ラージランナーやセルフホステッドランナーを使用することで、パフォーマンスの向上や内部リソースへのアクセスなどが可能です。


> **💡 ポイント**: Organization管理者がランナー設定を一元的に制御でき、全リポジトリに一貫したインフラポリシーを適用できるようになります。
---


<!-- /DAILY_ENTRY:2026-04-03 -->


## 📅 2026年4月2日（7件のアップデート）

![2026年4月2日のサマリー](/images/github-changelog-2026-04/2026-04-02-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/02/)

---


### 🤖 Copilotの組織カスタムインストラクションが一般提供開始

組織カスタムインストラクションを使用すると、Copilot BusinessおよびCopilot Enterpriseの組織管理者は、組織内のすべてのリポジトリにわたってCopilotの動作をガイドするデフォルトのインストラクションを設定できます。


> **💡 ポイント**: 組織カスタムインストラクションがGA（一般提供）となり、全リポジトリにわたるCopilotの動作ガバナンスを本番環境で安心して運用できます。
---


### 🤖 Copilot SDKがパブリックプレビューで利用可能に

Copilot SDKは、GitHub Copilotクラウドエージェントおよびcopilot CLIを支える、本番環境で実証済みの同じエージェントランタイムを公開します。独自のAIオーケストレーションレイヤーを構築する代わりに、ツール呼び出し、ストリーミング、ファイル操作、マルチターンセッションをすぐに利用できます。


> **💡 ポイント**: 本番実績のあるAIエージェントランタイムをSDKとして利用でき、LLM APIを直接使うよりも大幅に少ない工数でAI機能を構築できます。
---


### 🤖 Copilot使用メトリクスに組織レポートのユーザー別GitHub Copilot CLIアクティビティが追加

組織管理者は、CLIでアクティブな個々のユーザーを確認し、1日および28日レポートで使用状況の詳細を表示できるようになりました。以下の情報が含まれます：


> **💡 ポイント**: 組織管理者が個々の開発者のCLI利用状況を詳細に把握でき、サポートが必要なユーザーを特定できるようになりました。
---


### 🏛️ GitHub Actions：2026年4月初旬のアップデート

多くのGitHub Actionsユーザーは、[サービスコンテナ](https://docs.github.com/actions/tutorials/use-containerized-services/use-docker-service-containers)のエントリポイントやコマンドをオーバーライドできないことに不満を抱えており、これらの問題を解決するためにさまざまな回避策を講じていました。今後は、新しい`entrypoint`および`command`キーを使用して、ワークフローYAMLからイメージのデフォルトをオーバーライドできます。命名と動作はDocker Composeと...


> **💡 ポイント**: サービスコンテナのエントリポイントとコマンドをワークフローYAMLから直接オーバーライドでき、カスタムラッパーイメージが不要になります。
---


### 🤖 GitHub Copilot in Visual Studio — 3月アップデート

Visual Studio 2026の3月アップデートにおけるGitHub Copilotの新機能は以下のとおりです：


> **💡 ポイント**: Visual StudioでのCopilotが大幅に強化され、MCPサーバー接続やカスタムエージェント作成など、エージェント機能の本格的な統合が進みました。
---


### 🛠️ GitHub Issuesの改善された検索機能が一般提供開始

パブリックプレビュー以降、その結果は明白です。ユーザーが必要なものをより高い確率で見つけられるようになっただけでなく、検索に成功した場合、求めていた結果が上位3件以内に表示される割合は75%に達し、従来の検索の66%を上回っています。一般提供の開始に伴い、APIを通じてこの検索機能にアクセスすることも可能になりました。


> **💡 ポイント**: 自然言語によるIssue検索がGAとなり、上位3件の精度が従来の66%から75%に向上。APIからも利用可能になりました。
---


### 🔒 SecurityタブがSecurity & qualityに名称変更

* **Security**タブは、リポジトリ、Organization、Enterpriseの各レベルで**Security \& quality**になりました。
* リポジトリのサイドバーセクションで以前**Vulnerability alerts**と表示されていた項目が**Findings**になりました。
* リポジトリのサイドバーに、有効化ステータスを表示する新しい**Code quality**セクションが追加されました。
* リポジトリの**Policy**サイドバー項目が**Security policy**になりました。


> **💡 ポイント**: SecurityタブがSecurity & qualityに名称変更され、Code Quality機能の統合に向けたUI整備が進んでいます。機能面の変更はありません。
---


<!-- /DAILY_ENTRY:2026-04-02 -->


## 📅 2026年4月1日（6件のアップデート）

![2026年4月1日のサマリー](/images/github-changelog-2026-04/2026-04-01-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/01/)

---


### 🛠️ CodespacesがGitHub Enterprise（データレジデンシー対応）で一般提供開始

Codespacesは、データレジデンシー対応のGitHub Enterprise Cloudの全リージョンで利用可能です：


> **💡 ポイント**: データレジデンシー対応のEnterprise CloudでCodespacesがGA。規制産業の組織もコンプライアンスを維持したままクラウド開発環境を導入できます。
---


### 🤖 GitHub Mobile: Issueからのエージェント割り当てがより速く、より柔軟に

エージェントを割り当てる際に、カスタム指示の追加や別のリポジトリの選択が可能になり、作業の委任方法をより細かく制御できます。これらのオプションは新しいIssueの作成時にも利用でき、フローを中断することなく作業を引き渡すことが容易になります。


> **💡 ポイント**: モバイルからIssueのトリアージとエージェント委任がワンストップで完結。デスクトップに切り替える必要がなくなりました。
---


### 🤖 GitHub Mobile：リフレッシュされたCopilotタブとネイティブセッションログでフローを維持

Androidでは、Copilotがナビゲーションバーに**Copilot**タブとして移動し、セッションやチャット履歴へのアクセスがより高速になりました。**Copilot**タブ内の新しいホームエクスペリエンスにより、エージェントセッションとチャット履歴の概要がより明確に表示され、必要な情報をすばやく見つけることができます。


> **💡 ポイント**: AndroidでCopilotタブがナビゲーションバーに昇格し、エージェントセッションの監視からPR作成までモバイルで完結できるようになりました。
---


### 🤖 GPT-5.4 miniがCopilot Studentの自動モデル選択で利用可能に

このモデルは、Visual Studio Code、Visual Studio、JetBrains IDE、Xcode、EclipseのGitHub Copilot ChatにおけるAutoの一部として利用できます。


> **💡 ポイント**: Copilot StudentプランでGPT-5.4 miniが自動モデル選択に追加。VS Code、JetBrains、Xcodeなど5つのIDEで利用可能です。
---


### 🤖 Copilotクラウドエージェントでリサーチ、計画、コーディング

これまで、Copilotクラウドエージェントを使用するにはプルリクエストを開く必要がありました。今後はCopilotがプルリクエストを作成せずにブランチ上で作業できるようになり、作業の進め方やタイミングをより柔軟に制御できます。


> **💡 ポイント**: PRを開かずにブランチ上で作業でき、リサーチ→計画→コーディングの反復的なワークフローが可能になりました。エージェントの使い方の自由度が大幅に向上します。
---


### 🤖 GitHub CopilotにおけるClaude Sonnet 4の廃止予定

| モデル | 廃止日 | 推奨される代替モデル |
| --- | --- | --- |
| Claude Sonnet 4 | 2026\-05\-01 | Claude Sonnet 4\.6 |


> **💡 ポイント**: Claude Sonnet 4が2026年5月1日に廃止予定。Claude Sonnet 4.6への移行が推奨されています。Enterprise管理者は事前にモデルポリシーの確認が必要です。
---


<!-- /DAILY_ENTRY:2026-04-01 -->
