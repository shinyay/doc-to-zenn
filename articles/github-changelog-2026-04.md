---
title: "GitHub Changelog 2026年4月"
emoji: "📋"
type: "tech"
topics: ["github", "githubcopilot", "githubactions", "vscode", "devtools"]
published: true
---

2026年4月のGitHub Changelogデイリーサマリーです。毎日の更新内容をスライドと解説でお届けします。

4月1日〜3日は**17件のアップデート**がありました。Copilotクラウドエージェントの署名付きコミット対応、GPT-5.1 Codex廃止、Copilot SDK パブリックプレビュー開始など、AIエージェント機能の本格展開が加速しています。

📊 **全スライド一覧**: [GitHub Pages →](https://shinyay.github.io/gh-changelog-zenn/2026-04/)

---
<!-- DAILY_MARKER -->

## 📅 2026年4月10日（4件のアップデート）

![2026年4月10日のサマリー](/images/github-changelog-2026-04/2026-04-10-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/10/)

---


### 🏛️ Actionsワークフローの再実行が50回に制限

この制限は、特定のワークフローに対して数百回のリトライを試みる自動化がシステムに追加の負荷をかけていることへの対応として追加されました。GitHub Actions内の制限について詳しくは、[Actionsの制限に関するドキュメントページ](https://docs.github.com/actions/reference/limits)をご覧ください。


> **💡 ポイント**: CI/CD engineers and DevOps teams must audit existing retry automation to ensure no workflow rerun loop exceeds 50 iterations, refactoring aggressive retry logic to use exponential backoff or in-workflow step-level retries instead.


> **⚠️ 注意**: The article does not state whether this limit applies to GitHub Enterprise Server (GHES) or only to GitHub.com, leaving enterprise on-premises customers without clarity.


---


### 🤖 Copilot CLIアクティビティが使用メトリクスの合計値と機能別内訳に統合

今回のアップデートにより、CLIアクティビティは既存のメトリクスに統合されました。


> **💡 ポイント**: Enterprise admins and engineering managers will see higher top-level usage counts in dashboards, which could trigger threshold-based alerts or alter trend lines, requiring recalibration of monitoring and reporting systems.


> **⚠️ 注意**: Top-level totals have changed meaning silently under the same API version (2026-03-10), with no version bump, which means consumers who pinned to this version for stability may experience unexpected behavioral changes.


---


### 🤖 Copilotクラウドエージェントのバリデーションツールが20%高速化

これらのバリデーションツールは順次実行ではなく並列実行されるようになり、バリデーション時間が20%短縮されました。これにより、同じ品質を維持しながらCopilotの動作が高速化されます。


> **💡 ポイント**: Developers using Copilot cloud agent will experience approximately 20% faster turnaround on agent-completed tasks, reducing the wait time between task assignment and pull request creation with no degradation in code quality or security scanning coverage.


> **⚠️ 注意**: The 20% figure is a relative improvement with no absolute timing baseline provided—the actual time saved in seconds or minutes is unknown, making it difficult to assess real-world significance for specific workflows.


---


### 🤖 GitHub Copilot Proの新規無料トライアルを一時停止

* 現時点では、新規ユーザーはCopilot Proの無料トライアルを開始できません。
* 既存のトライアルには影響ありません。
* Copilot Freeおよび有料のCopilot Proサブスクリプションは引き続きご利用いただけます。


> **💡 ポイント**: Individual developers evaluating Copilot Pro must now either commit to a paid subscription without a trial period or use the limited Copilot Free tier to assess the product, reducing their ability to make informed purchasing decisions.


> **⚠️ 注意**: No specific timeline is provided for when trials will resume — 'as soon as' is the only temporal guidance, leaving the duration of the pause entirely open-ended.


---


<!-- /DAILY_ENTRY:2026-04-10 -->


## 📅 2026年4月9日（5件のアップデート）

![2026年4月9日のサマリー](/images/github-changelog-2026-04/2026-04-09-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/09/)

---


### 🔒 セキュリティ評価でCopilotに質問する機能が利用可能に

詳細については、[Code Securityリスク評価](https://docs.github.com/code-security/concepts/code-scanning/code-security-risk-assessment)または[シークレットリスク評価](https://docs.github.com/en/code-security/how-tos/secure-at-scale/configure-organization-security/configure-specific-tools/assess-your-secret-risk)の実行に関するドキュメントを...


> **💡 ポイント**: Organization admins gain an AI-powered advisor within their security assessment workflow, potentially reducing the time required to interpret complex aggregate security data and prioritize remediation efforts across large repository portfolios.


> **⚠️ 注意**: The article does not specify which Copilot subscription tier (Business, Enterprise, or potentially a standalone security tier) is required to access this feature. Organizations should verify their licensing before expecting to use it.


---


### 🏛️ コメント非表示メニューに新しい「Low Quality」オプションが追加

以前は、利用可能な分類オプション（例：**Spam**や**Abuse**）は従来の問題のあるコンテンツを想定して設計されており、役に立たない、またはその他の低品質なコメントの増加を正確に反映していませんでした。新しい**Low Quality**分類により、モデレーターはモデレーション時にこれらのコメントをより正確にカテゴリ分けできる精密なツールを利用できます。


> **💡 ポイント**: Repository maintainers and moderators gain a more precise tool for categorizing hidden comments, reducing the need to misclassify low-quality content as spam or abuse when neither label accurately describes the problem.


> **⚠️ 注意**: GitHub Enterprise Server (GHES) availability is not mentioned; it is unknown whether this feature will ship in future GHES releases or remains GitHub.com-only.


---


### 🛠️ 通知ページに新しい「Sort by」コントロールが追加

通知がリポジトリごとにグループ化されている場合、ソートはグループ自体の順序と各グループ内のアイテムの順序の両方に影響します。これにより、最後のページに移動して逆順にたどる必要なく、バックログを体系的に処理できます。


> **💡 ポイント**: Individual developers with notification backlogs gain a significantly streamlined triage workflow — switching to oldest-first sorting eliminates the need to paginate to the end of the notification list to address long-standing items.


> **⚠️ 注意**: The feature offers only two sort options (newest-first and oldest-first). There is no support for sorting by other dimensions such as repository name, notification type, or priority.


---


### 🛠️ Issueサイドバーのリリース情報とプロジェクトフィールドのデフォルト値

![Screenshot of an issue sidebar showing a linked pull request with a "Latest" release tag beneath it](https://github.com/user-attachments/assets/ec969161-8e22-487f-9336-40873cf3dedd)


> **💡 ポイント**: Project maintainers can reduce repetitive manual field entry by configuring default values, which is particularly impactful for large projects with many contributors adding items frequently.


> **⚠️ 注意**: The article does not state whether these features are available on GitHub Enterprise Server (GHES) or are limited to GitHub.com cloud.


---


### 🛠️ リポジトリメンバーのロールラベルがプルリクエスト一覧ビューに表示されるように

![The pull request list view showing different repository role member labels](https://github.com/user-attachments/assets/3fb440b9-649b-4107-9eea-8884fb0ccaa5)


> **💡 ポイント**: Open source maintainers gain a significant triage efficiency improvement, as they can now assess contributor context for all open PRs without leaving the list view, potentially saving minutes per triage session on active projects.


> **⚠️ 注意**: The feature is explicitly limited to public repositories. Private and internal repositories are not mentioned, and organizations relying on these for open source workflows will not benefit.


---


<!-- /DAILY_ENTRY:2026-04-09 -->


## 📅 2026年4月7日（6件のアップデート）

![2026年4月7日のサマリー](/images/github-changelog-2026-04/2026-04-07-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/07/)

---


### 🔒 コードスキャン：プルリクエストでセキュリティアラートの修正提案を一括適用

**Files changed**タブでコードスキャンアラートの修正をバッチに追加して適用できるようになり、複数のアラートをより迅速に処理できます。変更を単一のコミットにまとめることで、アラートごとに個別のスキャンを実行する代わりに1回のスキャンで済み、修正とレビューの時間を短縮してプルリクエストのスムーズな進行を支援します。


> **💡 ポイント**: Developers reviewing pull requests with multiple code scanning alerts will experience significantly reduced friction when applying suggested fixes, as they can now batch fixes and commit once rather than repeating the apply-commit-scan cycle for each alert individually.


> **⚠️ 注意**: GitHub Enterprise Server (GHES) availability is not stated. Organizations on GHES should not assume this feature is available and should monitor GHES release notes for inclusion in a future version.


---


### 🤖 Copilot CLIがBYOKおよびローカルモデルに対応

CLI起動前にいくつかの環境変数を設定することで、Copilot CLIをAzure OpenAI、Anthropic、または任意のOpenAI互換エンドポイントで使用できるよう構成できます。OpenAIやAzure OpenAIなどのリモートサービスに加え、Ollama、vLLM、Foundry Localなどのローカル実行モデルでも動作します。セットアップ手順については [Using your own LLM models in GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/custom...


> **💡 ポイント**: Developers in air-gapped or classified environments can now use Copilot CLI for the first time by combining offline mode with local model inference, opening the tool to defense, government, and regulated-industry users who were previously excluded.


> **⚠️ 注意**: The article does not clarify whether a paid Copilot subscription is required to use the CLI in BYOK mode, leaving the licensing model for this use case ambiguous.


---


### 🤖 DependabotアラートをAIエージェントに割り当てて修正が可能に

Dependabotアラートの詳細ページから**Assign to Agent**を選択し、Copilot、Claude、Codexなど希望のコーディングエージェントを選択します。割り当てられたエージェントは以下を実行します：


> **💡 ポイント**: Security teams gain a force multiplier for addressing their Dependabot alert backlog, particularly for complex vulnerabilities that require code changes beyond simple version bumps, potentially reducing mean-time-to-remediation by hours or days per alert.


> **⚠️ 注意**: The feature requires both GitHub Code Security and a Copilot plan that includes coding agent access. Organizations lacking either prerequisite cannot use agent assignment, and the specific Copilot plan tiers that qualify are not enumerated in the article.


---


### 🤖 DependabotバージョンアップデートがNixエコシステムに対応

Dependabotは古くなったflake入力ごとに個別のプルリクエストを作成します。GitHub、GitLab、Sourcehut、およびプレーンなgit入力がすべてサポートされています。


> **💡 ポイント**: **Nix developers** gain a native, zero-configuration dependency update workflow on GitHub, eliminating the need for custom CI scripts or third-party bots to keep flake inputs current.


> **⚠️ 注意**: Security updates are explicitly not supported—Dependabot will not open reactive PRs based on vulnerability advisories for Nix flake inputs. Teams must handle CVE response through other means.


---


### 🤖 npmトラステッドパブリッシングがCircleCIに対応

この拡張により、トラステッドパブリッシングはCIプロバイダー別でnpmパブリッシャーの大部分をカバーするようになりました。設定はnpmウェブサイトおよび`npm trust` CLIコマンドから利用可能です。セットアップ手順については、[トラステッドパブリッシングのドキュメント](https://docs.npmjs.com/trusted-publishers)をご参照ください。


> **💡 ポイント**: Package maintainers using CircleCI can now adopt trusted publishing to eliminate stored npm tokens, reducing their exposure to credential theft, secret sprawl, and token rotation burden. They should consult the trusted publishing documentation and update their CircleCI pipeline configurations.


> **⚠️ 注意**: The article does not specify which CircleCI plan tiers support OIDC token generation. Maintainers on free or open-source CircleCI plans may not have access to this feature.


---


### 🤖 Dynatraceのランタイムコンテキストでセキュリティアラートを優先順位付け

DynatraceをGitHubに接続すると、Dynatraceがリポジトリにマッピングしたコンテナイメージのデプロイメントコンテキストとランタイムリスクシグナルが表示されます。このコンテキストを活用して、デプロイ済みアーティファクトに影響するアラート、特にDynatraceがより高リスクのランタイム状態を検出した場合のアラートに修正作業を集中できます。


> **💡 ポイント**: Security engineers gain the ability to dramatically reduce alert fatigue by filtering out vulnerabilities in undeployed code, focusing remediation effort on the subset of alerts that represent actual production risk in Kubernetes environments.


> **⚠️ 注意**: The feature is explicitly limited to GitHub Enterprise Cloud customers — there is no mention of availability for GitHub Enterprise Server (GHES), GitHub Team plans, or free/pro individual plans.


---


<!-- /DAILY_ENTRY:2026-04-07 -->


## 📅 2026年4月6日（1件のアップデート）

![2026年4月6日のサマリー](/images/github-changelog-2026-04/2026-04-06-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/06/)

---


### 🤖 Copilot使用メトリクスでCopilotコードレビューのアクティブユーザーとパッシブユーザーを識別可能に

[APIレスポンス](https://docs.github.com/enterprise-cloud@latest/rest/copilot/copilot-usage-metrics?apiVersion=2026-03-10)内では、CCRの使用状況はユーザーレベルの2つのフィールドで表されます：


> **💡 ポイント**: Enterprise and organization admins gain the ability to produce differentiated adoption reports that separate active CCR engagement from passive auto-review exposure, enabling more credible ROI narratives for Copilot licensing renewals and expansions.


> **⚠️ 注意**: The feature appears to be limited to GitHub Enterprise Cloud based on the documentation path (`enterprise-cloud@latest`); GHES availability is not stated in the article.


---


<!-- /DAILY_ENTRY:2026-04-06 -->


## 📅 2026年4月8日（6件のアップデート）

![2026年4月8日のサマリー](/images/github-changelog-2026-04/2026-04-08-summary.png)

📊 [**詳細スライドを見る →**](https://shinyay.github.io/gh-changelog-zenn/2026-04/08/)

---


### 🔒 コードスキャン：プルリクエストでセキュリティアラートの修正提案を一括適用

**Files changed**タブでコードスキャンアラートの修正をバッチに追加して適用できるようになり、複数のアラートをより迅速に処理できます。変更を単一のコミットにまとめることで、アラートごとに個別のスキャンを実行する代わりに1回のスキャンで済み、修正とレビューの時間を短縮してプルリクエストのスムーズな進行を支援します。


> **💡 ポイント**: Developers reviewing pull requests with multiple code scanning alerts will experience significantly reduced friction when applying suggested fixes, as they can now batch fixes and commit once rather than repeating the apply-commit-scan cycle for each alert individually.


> **⚠️ 注意**: GitHub Enterprise Server (GHES) availability is not stated. Organizations on GHES should not assume this feature is available and should monitor GHES release notes for inclusion in a future version.


---


### 🤖 Copilot CLIがBYOKおよびローカルモデルに対応

CLI起動前にいくつかの環境変数を設定することで、Copilot CLIをAzure OpenAI、Anthropic、または任意のOpenAI互換エンドポイントで使用できるよう構成できます。OpenAIやAzure OpenAIなどのリモートサービスに加え、Ollama、vLLM、Foundry Localなどのローカル実行モデルでも動作します。セットアップ手順については [Using your own LLM models in GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/custom...


> **💡 ポイント**: Developers in air-gapped or classified environments can now use Copilot CLI for the first time by combining offline mode with local model inference, opening the tool to defense, government, and regulated-industry users who were previously excluded.


> **⚠️ 注意**: The article does not clarify whether a paid Copilot subscription is required to use the CLI in BYOK mode, leaving the licensing model for this use case ambiguous.


---


### 🤖 DependabotアラートをAIエージェントに割り当てて修正が可能に

Dependabotアラートの詳細ページから**Assign to Agent**を選択し、Copilot、Claude、Codexなど希望のコーディングエージェントを選択します。割り当てられたエージェントは以下を実行します：


> **💡 ポイント**: Security teams gain a force multiplier for addressing their Dependabot alert backlog, particularly for complex vulnerabilities that require code changes beyond simple version bumps, potentially reducing mean-time-to-remediation by hours or days per alert.


> **⚠️ 注意**: The feature requires both GitHub Code Security and a Copilot plan that includes coding agent access. Organizations lacking either prerequisite cannot use agent assignment, and the specific Copilot plan tiers that qualify are not enumerated in the article.


---


### 🤖 DependabotバージョンアップデートがNixエコシステムに対応

Dependabotは古くなったflake入力ごとに個別のプルリクエストを作成します。GitHub、GitLab、Sourcehut、およびプレーンなgit入力がすべてサポートされています。


> **💡 ポイント**: **Nix developers** gain a native, zero-configuration dependency update workflow on GitHub, eliminating the need for custom CI scripts or third-party bots to keep flake inputs current.


> **⚠️ 注意**: Security updates are explicitly not supported—Dependabot will not open reactive PRs based on vulnerability advisories for Nix flake inputs. Teams must handle CVE response through other means.


---


### 🤖 npmトラステッドパブリッシングがCircleCIに対応

この拡張により、トラステッドパブリッシングはCIプロバイダー別でnpmパブリッシャーの大部分をカバーするようになりました。設定はnpmウェブサイトおよび`npm trust` CLIコマンドから利用可能です。セットアップ手順については、[トラステッドパブリッシングのドキュメント](https://docs.npmjs.com/trusted-publishers)をご参照ください。


> **💡 ポイント**: Package maintainers using CircleCI can now adopt trusted publishing to eliminate stored npm tokens, reducing their exposure to credential theft, secret sprawl, and token rotation burden. They should consult the trusted publishing documentation and update their CircleCI pipeline configurations.


> **⚠️ 注意**: The article does not specify which CircleCI plan tiers support OIDC token generation. Maintainers on free or open-source CircleCI plans may not have access to this feature.


---


### 🤖 Dynatraceのランタイムコンテキストでセキュリティアラートを優先順位付け

DynatraceをGitHubに接続すると、Dynatraceがリポジトリにマッピングしたコンテナイメージのデプロイメントコンテキストとランタイムリスクシグナルが表示されます。このコンテキストを活用して、デプロイ済みアーティファクトに影響するアラート、特にDynatraceがより高リスクのランタイム状態を検出した場合のアラートに修正作業を集中できます。


> **💡 ポイント**: Security engineers gain the ability to dramatically reduce alert fatigue by filtering out vulnerabilities in undeployed code, focusing remediation effort on the subset of alerts that represent actual production risk in Kubernetes environments.


> **⚠️ 注意**: The feature is explicitly limited to GitHub Enterprise Cloud customers — there is no mention of availability for GitHub Enterprise Server (GHES), GitHub Team plans, or free/pro individual plans.


---


<!-- /DAILY_ENTRY:2026-04-08 -->


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
