---
title: "GitHub Changelog 2026年4月"
emoji: "📋"
type: "tech"
topics: ["github", "copilot", "githubactions"]
published: true
---

GitHub Changelog の日本語デイリーサマリーです。毎日の更新内容をスライド画像と解説でお届けします。

📊 **全スライド一覧**: [GitHub Pages →](https://shinyay.github.io/gh-changelog-zenn/2026-04/)

---
<!-- DAILY_MARKER -->

## 📅 2026年4月3日（4件のアップデート）

![2026年4月3日のサマリー](/images/github-changelog-2026-04/2026-04-03-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/03/)

---


### 🤖 Copilotクラウドエージェントがコミットに署名を付与

これにより、Copilotクラウドエージェントは[「Require signed commits」](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-signed-commits)ブランチ保護ルールまたはルールセットが有効になっているリポジトリでも動作するようになりました。以前は、このルールにエージェントが準拠できなかったため、該当リポジトリでの使用が完...


> **💡 ポイント**: Enterprise organizations with strict branch protection policies can now adopt Copilot cloud agent in repositories that previously blocked it due to signed commit requirements, potentially accelerating AI-assisted development adoption.


> **⚠️ 注意**: The article does not specify which signing mechanism is used (GPG, SSH, S/MIME, or GitHub-internal), which is critical for organizations performing independent signature verification.


---


### 🤖 GPT-5.1 Codex、GPT-5.1-Codex-Max、GPT-5.1-Codex-Miniが廃止

| モデル | 廃止日 | 推奨代替モデル |
| --- | --- | --- |
| GPT\-5\.1\-Codex | 2026\-04\-01 | GPT\-5\.3\-Codex |
| GPT\-5\.1\-Codex\-Mini | 2026\-04\-01 | GPT\-5\.3\-Codex |
| GPT\-5\.1\-Codex\-Max | 2026\-04\-01 | GPT\-5\.3\-Codex |


> **💡 ポイント**: Individual Copilot users who had selected any GPT-5.1-Codex variant as their preferred model will find it unavailable and must manually select a new model, potentially disrupting established workflows.


> **⚠️ 注意**: No advance deprecation notice period is mentioned in the article — it is unclear whether users received prior warnings via email, in-product notifications, or other channels before the April 1 removal date.


---


### 🤖 Copilotクラウドエージェントの Organization ファイアウォール設定

Organization管理者は、Organization内のすべてのリポジトリにわたってエージェントファイアウォールを管理できるようになりました。これにより、ニーズに合った適切なデフォルト設定とガードレールを備えたCopilotクラウドエージェントを大規模に展開することが容易になります。Organization管理者は以下のことが可能です：


> **💡 ポイント**: Organization admins gain a centralized control plane for Copilot agent security, reducing the operational burden of managing firewall settings across hundreds or thousands of repositories individually.


> **⚠️ 注意**: The article does not state whether these settings are available on GitHub Enterprise Server (GHES) or only on GitHub.com, which is critical information for on-premises enterprise customers.


---


### 🤖 Copilotクラウドエージェントの組織レベルランナー制御

デフォルトでは標準のGitHubホステッドランナーで実行されますが、チームは[エージェント環境をカスタマイズ](https://docs.github.com/enterprise-cloud@latest/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment)して、ラージランナーやセルフホステッドランナーを使用することで、パフォーマンスの向上や内部リソースへのアクセスなどが可能です。


> **💡 ポイント**: Organization administrators gain centralized control over Copilot cloud agent infrastructure, reducing the operational burden of managing runner configurations across potentially thousands of repositories and enabling consistent policy enforcement.


> **⚠️ 注意**: The article does not specify which GitHub plans (Free, Team, Enterprise) support this feature; the Enterprise Cloud documentation link suggests it may be limited to Enterprise Cloud.


---


<!-- /DAILY_ENTRY:2026-04-03 -->


## 📅 2026年4月2日（7件のアップデート）

![2026年4月2日のサマリー](/images/github-changelog-2026-04/2026-04-02-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/02/)

---


### 🤖 Copilotの組織カスタムインストラクションが一般提供開始

組織カスタムインストラクションを使用すると、Copilot BusinessおよびCopilot Enterpriseの組織管理者は、組織内のすべてのリポジトリにわたってCopilotの動作をガイドするデフォルトのインストラクションを設定できます。


> **💡 ポイント**: Organization administrators can now confidently deploy custom instructions in production knowing the feature is GA and supported, enabling centralized governance of Copilot behavior across all repositories.


> **⚠️ 注意**: The article does not specify whether organization custom instructions are available on GitHub Enterprise Server (GHES) or are limited to GitHub.com (cloud) deployments.


---


### 🤖 Copilot SDKがパブリックプレビューで利用可能に

Copilot SDKは、GitHub Copilotクラウドエージェントおよびcopilot CLIを支える、本番環境で実証済みの同じエージェントランタイムを公開します。独自のAIオーケストレーションレイヤーを構築する代わりに、ツール呼び出し、ストリーミング、ファイル操作、マルチターンセッションをすぐに利用できます。


> **💡 ポイント**: Application developers gain a production-tested agentic AI runtime that can be embedded into custom products, significantly reducing the effort required to build AI-powered features compared to assembling components from scratch using raw LLM APIs.


> **⚠️ 注意**: The SDK is in public preview, meaning the API surface is not guaranteed to be stable and breaking changes may occur before general availability. Production deployments carry risk of forced migrations.


---


### 🤖 Copilot使用メトリクスに組織レポートのユーザー別GitHub Copilot CLIアクティビティが追加

組織管理者は、CLIでアクティブな個々のユーザーを確認し、1日および28日レポートで使用状況の詳細を表示できるようになりました。以下の情報が含まれます：


> **💡 ポイント**: Organization administrators gain fine-grained visibility into individual developer CLI adoption and can now identify specific users who need enablement support, replacing previously available aggregate-only organization metrics.


> **⚠️ 注意**: The article does not state whether this feature is available on GitHub Enterprise Server (GHES) or is limited to GitHub Enterprise Cloud. The API documentation URL referencing `enterprise-cloud@latest` strongly suggests Cloud-only availability.


---


### 🏛️ GitHub Actions：2026年4月初旬のアップデート

多くのGitHub Actionsユーザーは、[サービスコンテナ](https://docs.github.com/actions/tutorials/use-containerized-services/use-docker-service-containers)のエントリポイントやコマンドをオーバーライドできないことに不満を抱えており、これらの問題を解決するためにさまざまな回避策を講じていました。今後は、新しい`entrypoint`および`command`キーを使用して、ワークフローYAMLからイメージのデフォルトをオーバーライドできます。命名と動作はDocker Composeと...


> **💡 ポイント**: DevOps engineers using service containers for databases, caches, or message brokers can now configure startup behavior directly in workflow YAML, eliminating custom wrapper images and shell-based workaround scripts that added maintenance burden and build time.


> **⚠️ 注意**: The service container entrypoint override feature does not specify whether shell form or exec form syntax is supported, nor whether environment variable interpolation works within the `entrypoint` and `command` values.


---


### 🤖 GitHub Copilot in Visual Studio — 3月アップデート

Visual Studio 2026の3月アップデートにおけるGitHub Copilotの新機能は以下のとおりです：


> **💡 ポイント**: Enterprise security and compliance teams should immediately configure MCP allowlist policies for their GitHub organizations to maintain control over which external data sources Copilot agents can access, preventing unauthorized data egress before developers begin creating custom agents.


> **⚠️ 注意**: The article does not state pricing implications — it is unknown whether custom agents, skills, or MCP connections consume additional Copilot quota or require a specific subscription tier.


---


### 🛠️ GitHub Issuesの改善された検索機能が一般提供開始

パブリックプレビュー以降、その結果は明白です。ユーザーが必要なものをより高い確率で見つけられるようになっただけでなく、検索に成功した場合、求めていた結果が上位3件以内に表示される割合は75%に達し、従来の検索の66%を上回っています。一般提供の開始に伴い、APIを通じてこの検索機能にアクセスすることも可能になりました。


> **💡 ポイント**: All GitHub users benefit from improved issue discoverability through natural-language search in the UI, with a reported 9-percentage-point improvement in top-3 result accuracy (75% vs. 66%) compared to traditional lexical search.


> **⚠️ 注意**: Semantic and hybrid search queries are rate-limited to 10 requests per minute, which may be insufficient for automated workflows, bots, or bulk search operations. The rate limit granularity (per-user, per-token, per-org) is not specified.


---


### 🔒 SecurityタブがSecurity & qualityに名称変更

* **Security**タブは、リポジトリ、Organization、Enterpriseの各レベルで**Security \& quality**になりました。
* リポジトリのサイドバーセクションで以前**Vulnerability alerts**と表示されていた項目が**Findings**になりました。
* リポジトリのサイドバーに、有効化ステータスを表示する新しい**Code quality**セクションが追加されました。
* リポジトリの**Policy**サイドバー項目が**Security policy**になりました。


> **💡 ポイント**: Developers will see a renamed tab and sidebar labels but experience no functional workflow changes; familiarity with the new layout will ease transition when Code Quality features reach GA.


> **⚠️ 注意**: The change is available only on github.com and is explicitly not included in GitHub Enterprise Server; no GHES version or timeline for inclusion is stated.


---


<!-- /DAILY_ENTRY:2026-04-02 -->


## 📅 2026年4月1日（6件のアップデート）

![2026年4月1日のサマリー](/images/github-changelog-2026-04/2026-04-01-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/01/)

---


### 🛠️ CodespacesがGitHub Enterprise（データレジデンシー対応）で一般提供開始

Codespacesは、データレジデンシー対応のGitHub Enterprise Cloudの全リージョンで利用可能です：


> **💡 ポイント**: Enterprise administrators in regulated industries (finance, healthcare, government, defense) can now adopt Codespaces without violating data residency compliance requirements, removing a key blocker for cloud development environment adoption.


> **⚠️ 注意**: User-owned codespaces are not supported for data residency accounts. Developers cannot create personal codespaces outside of organizational ownership, which limits flexibility for experimentation and personal projects.


---


### 🤖 GitHub Mobile: Issueからのエージェント割り当てがより速く、より柔軟に

エージェントを割り当てる際に、カスタム指示の追加や別のリポジトリの選択が可能になり、作業の委任方法をより細かく制御できます。これらのオプションは新しいIssueの作成時にも利用でき、フローを中断することなく作業を引き渡すことが容易になります。


> **💡 ポイント**: Mobile-first developers and engineering managers who triage issues on the go can now delegate work to Copilot agents without switching to a desktop browser, significantly reducing the time between issue identification and agent-initiated work.


> **⚠️ 注意**: The article does not specify which Copilot subscription tiers are required to see and use the 'Assign an Agent' option — it may require Copilot Enterprise, Business, or specific organizational settings.


---


### 🤖 GitHub Mobile：リフレッシュされたCopilotタブとネイティブセッションログでフローを維持

Androidでは、Copilotがナビゲーションバーに**Copilot**タブとして移動し、セッションやチャット履歴へのアクセスがより高速になりました。**Copilot**タブ内の新しいホームエクスペリエンスにより、エージェントセッションとチャット履歴の概要がより明確に表示され、必要な情報をすばやく見つけることができます。


> **💡 ポイント**: Developers using Copilot agents can now monitor, review, and act on autonomous coding sessions from anywhere, eliminating the requirement to be at a desktop to manage agent workflows and significantly reducing the feedback loop for agent-generated work.


> **⚠️ 注意**: The article does not specify which Copilot subscription tiers are required for mobile agent session management—it is unclear whether Copilot Individual, Business, and Enterprise all have equal access to these features.


---


### 🤖 GPT-5.4 miniがCopilot Studentの自動モデル選択で利用可能に

このモデルは、Visual Studio Code、Visual Studio、JetBrains IDE、Xcode、EclipseのGitHub Copilot ChatにおけるAutoの一部として利用できます。


> **💡 ポイント**: Copilot Student plan subscribers will experience potentially faster and more varied responses in Copilot Chat as the auto-selection system can now route appropriate queries to GPT-5.4 mini, which as a 'mini' model variant likely offers lower latency for simpler tasks.


> **⚠️ 注意**: The article is extremely brief (three substantive sentences plus a feedback link), providing minimal technical detail about the model itself or its integration specifics.


---


### 🤖 Copilotクラウドエージェントでリサーチ、計画、コーディング

これまで、Copilotクラウドエージェントを使用するにはプルリクエストを開く必要がありました。今後はCopilotがプルリクエストを作成せずにブランチ上で作業できるようになり、作業の進め方やタイミングをより柔軟に制御できます。


> **💡 ポイント**: Individual developers gain significantly more flexibility in how they interact with the agent, moving from a rigid 'task in → PR out' model to an iterative workflow that supports exploration, planning, and incremental refinement before committing to a deliverable.


> **⚠️ 注意**: The article does not specify any pricing changes or additional costs associated with the new research and planning capabilities, which likely consume significantly more compute resources than simple code generation.


---


### 🤖 GitHub CopilotにおけるClaude Sonnet 4の廃止予定

| モデル | 廃止日 | 推奨される代替モデル |
| --- | --- | --- |
| Claude Sonnet 4 | 2026\-05\-01 | Claude Sonnet 4\.6 |


> **💡 ポイント**: Individual Copilot users who currently use Claude Sonnet 4 as their preferred model must select an alternative (ideally Claude Sonnet 4.6) from the model selector in VS Code or github.com before May 1, 2026.


> **⚠️ 注意**: The article does not state what happens to users who fail to migrate before May 1, 2026—whether they will be auto-assigned a default model, encounter errors, or experience degraded functionality.


---


<!-- /DAILY_ENTRY:2026-04-01 -->
