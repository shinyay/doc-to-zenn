---
title: "tokopt 入門 — リポジトリの「always-on 税」を測ってから最適化する"
emoji: "🪙"
type: "tech"
topics: ["llm", "githubcopilot", "tokenization", "go", "ai"]
published: true
---

## はじめに — これは姉妹記事です

先日、Zenn Book として『[トークン超入門 — LLM の「単位」を腑に落とす](https://zenn.dev/shinyay/books/getting-started-with-tokens)』を公開しました。全 20 章で、トークンとは何か、どこで消費されるのか、なぜ最適化が単なる節約ではないのか、を first-principles から積み上げた本です。

その最終章（巻末コラム）で、私はひとつだけ「次にやること」を読者に予告しました。

> 本書で議論した規律を、毎週・毎 PR で自動的に回すための小さなツールキットがある。`tokopt` という。**使い方は別記事で扱う。**

本記事がその「別記事」です。本書を読んでくださった方には**規律を持続可能にする道具**として、まだ読んでいない方には**なぜそんな道具が必要なのか**を、それぞれ届けたいと思っています。

:::message
本書を読んでいない方への 30 秒サマリー：

- LLM の課金・レイテンシ・品質はすべて **トークン** という単位に還元される
- 全最適化は 3 つの move のいずれか — **より少なく送る／より少なく受ける／トークンあたり安く払う**
- 学ぶ価値ある技法は 7 ファミリ（Output control / Context scoping / Prompt compression / Model tiering / Caching 規律 / Tool 規律 / Workflow 選択）
- スローガンは 2 つ — **「数字は変わるが、構造は変わらない」** と **Be fluent in the unit**（単位に流暢になれ）
:::

---

## なぜ tokopt を作ったか

本書では、トークン健康のための **10 の原則**と **14 のアンチパターン**を扱いました。たとえば kitchen-sink システムプロンプト、cache-busting prefix、MCP / ツール過剰、病的な history 成長など。

これらは「**チェックリストで見つかる**」種類の問題です。難しい技術ではありません。難しいのは「**今日やる**」を「**毎週・毎 PR でやる**」に変えることです。

実務で起きるのは、こういうことです：

- `AGENTS.md` は誰かが「もう 1 行だけ」を続けるうちに、いつのまにか倍になる
- Copilot CLI の `/chronicle improve` のような自動追記は、**気付かないうちに** instructions を膨らませる
- 「カスタムエージェント」「スキル」を増やすと、**always-on 税**（毎ターン必ず払うトークン）が PR ごとに数百ずつ伸びる
- 誰もそれを止めない。請求か遅延が「不快」レベルに達するまで

本書 第16章「最適化へのロードマップ」の going deeper で、私は **四半期トークン audit** を提案しました。これは正しい cadence ですが、現実には `AGENTS.md` は四半期より速く drift します。**audit を「四半期 1 回・1 時間」から「PR 毎・60 秒」に降ろす**のが、tokopt の動機です。

---

## tokopt の 1 行モデル

> **tokopt はリポジトリの静的設定が背負うトークン税を測る、計測ファースト（measurement-first）な CLI です。**

`tokopt` は **静的解析ツール**です。ディスク上のファイル — たとえば `.github/copilot-instructions.md`, `AGENTS.md`, `.github/instructions/**`, agent / skill 定義、MCP 設定など — を読み、ローカル tokenizer でトークン数を数え、内訳を出します。

何を**測らない**かも明示しておきます：

| 測る（静的） | 測らない（動的） |
|---|---|
| copilot-instructions.md / AGENTS.md のサイズ | 実セッションのチャット往復 |
| 各 instructions / skill / agent ファイル | `#file:` で添付された内容の実トークン |
| ツール定義ファイル（あれば） | MCP サーバが runtime で広告するスキーマ |
| 7 セグメントに分解した擬似プロンプト | 会話履歴の累積成長 |

ライブセッションの可視化はベンダーのダッシュボードに任せ、tokopt は **Git で版管理できる部分**に徹します。これは妥協ではなく、**CI に組み込めるサイズに収めるための設計判断**です。

---

## クイックスタート

### インストール

`tokopt` は Go 製の単一バイナリです。Go 1.23 以上があれば 1 行で入ります。

```bash
go install github.com/shinyay/getting-started-with-token-optimization/tools/tokopt/cmd/tokopt@latest
```

`$(go env GOPATH)/bin` を `PATH` に通したら、動作確認：

```bash
tokopt --version
```

### 最初の計測

任意の Copilot リポジトリの中で：

```bash
tokopt audit .
```

実出力はこんな形です（フィールドの一部を抜粋）：

> ```
> tokopt audit  root=.  encoding=o200k_base
> always-on tax: 2532 tokens
> conditional:   11414 tokens (paid only when triggered: applyTo, agent step, agent invoked)
> on-demand:     38397 tokens (skills loaded only when matched)
> ```

3 つのバケットの読み方：

- **always-on**：毎ターン必ず払うトークン。代表例は `AGENTS.md` や `.github/copilot-instructions.md`。**最初に攻めるのは常にここ**
- **conditional**：`applyTo:` などで条件付きにロードされる instructions と agent persona
- **on-demand**：ユーザーや agent が明示的に呼んだときだけ載る skill 群

「合計 5 万トークン」は怖く見えますが、**毎ターン払うのは always-on の 2,532 だけ**です。

---

## コマンドカタログ

`tokopt` の責務は 6 つです。本書のどの章を「自動化」するかも併記します。

| Command | 役割 | 本書で対応する章 |
|---|---|---|
| `count <file>` | 単一ファイルのトークン数 | 第5章「トークンを数える」 |
| `audit [path]` | always-on / conditional / on-demand 内訳 | 第9章「トークンはどこで消費されるか」+ 第12章「トークン hygiene の原則」 |
| `anatomy` | プロンプトを 7 セグメントに分解 | 第9章「トークンはどこで消費されるか」 |
| `detect [path]` | アンチパターンを静的検出 | 第14章「アンチパターンと落とし穴」 |
| `tail --input <file>` | 利用ログから p50/p90/p95/p99/max と外れ値 | 第13章「トークンを計測する」 |
| `report --threshold N` | audit + detect + ランク付き提案、CI ゲート | 第13章「トークンを計測する」+ 第16章「最適化へのロードマップ」 |

### count

```bash
tokopt count AGENTS.md
```

`AGENTS.md` は Copilot CLI のすべてのターンに乗ります。まず `count` で現在値を把握し、**チームのベースラインから黄・赤の閾値を合意するのが安全**です。後述のケーススタディでは 1,416 トークンの `AGENTS.md` に対し、約 500 トークンを当面の削減目安としました。

### audit / anatomy

`audit` はクイックスタートで見たコマンドです。`--format json` で機械可読、`--format md` で PR コメントに貼れる Markdown が出ます。

`anatomy` は新しいエージェントの設計時に、システムプロンプト・ツールカタログ・想定ユーザーメッセージを与えて **7 セグメント分布**を確認できます。「ユーザー本文が入力全体の 1% 未満」「system + always-on + tools が 50% 超」のような **balance 警告**が、本書 9 章の語彙そのままで返ってきます。

### detect

本書 14 章のアンチパターンのうち、**静的設定だけで判定できるもの**を検出します。残りは利用ログや routing telemetry が必要なので、ログ化できるものは `tail`、モデル選択や RAG の妥当性は別途人間の判断が要ります。

各 finding には `confidence` フィールドが付きます：

- **measured** — トークン数を実測した上での提案
- **heuristic** — パターンとしては実在するが、影響は挙動的（出力スタイル、reasoning verbosity など）で静的には数値化できないもの

`heuristic` な finding は、measured な削減見込みとは**別枠**で扱います。静的に測れない影響を、measured な節約量に混ぜて ranked recommendation に載せない、というのが基本方針です。これは本書 preface の「**唯一解を押し付けない**」規律を、ツール側で機械的に守るための仕掛けです。

### tail

利用ログ（JSONL か CSV、トークン数フィールドあり）から **p50/p90/p95/p99/max** と上位外れ値を出します。

```bash
tokopt tail --input usage.jsonl --top 10
```

「**上位 1% のターンが全体トークンの 30% を超えています**」のようなヒントが出れば、本書 13 章の **heavy tail** が効いている証拠です。巨大ファイル添付、過剰なツールコール、RAG の取り過ぎなどが疑いの出発点になります。

### report

`audit` と `detect` を統合し、ランク付きの推奨を 1 画面で出します。CI のための **exit code ゲート**もここに付いています：

```bash
tokopt report . --threshold 1500
```

- exit `0` — always-on 税が閾値以下（合格）
- exit `2` — always-on 税が閾値超過（**マージ不可**）
- exit `1` — 実行時エラー

ゲートは **always-on のみ**にかけます。conditional / on-demand は毎回払うものではないので gate しても意味がありません。本書 9 章の「always-on tax」概念が、そのまま CI 規律に対応します。

---

## 実例 — テンプレートリポジトリの実測

ある実在の Copilot テンプレートリポジトリ（スキル 26 個、エージェント 9 個、`AGENTS.md` 1,416 トークン）に対する実測ベースラインです。

| バケット | トークン | 内訳 |
|---|---:|---|
| always-on | 2,532 | `AGENTS.md` (1,416) + `.github/copilot-instructions.md` (1,116) |
| conditional | 11,414 | instructions 5 ファイル (3,300) + agent 9 ファイル (8,114) |
| on-demand | 38,397 | skill 26 ファイル |

`detect` を回すと、**measured な finding が 2 つ**出ました：

| Severity | パターン | 場所 | 現在 | 削減見込み |
|---|---|---|---:|---:|
| INFO | `huge-agents-md` | `AGENTS.md` | 1,416 | 〜916 |
| WARN | `kitchen-sink-system-prompt` | `.github/copilot-instructions.md` | 1,116 | 〜616 |

合計約 1,500 トークンの always-on 税削減余地。1 ターンあたりは小さく見えても、1 日数千ターン回るチームでは線形に効きます。本書 第15章「**コールあたり小勝利はスケールで大**」が、まさにこの数字に対応します。

### before / after を JSON で diff する

文章を直したら、本当に減ったかを数字で確認します（bash / zsh、`jq` 必要）：

```bash
tokopt --format json audit . > /tmp/before.json
# ... AGENTS.md を編集 ...
tokopt --format json audit . > /tmp/after.json
diff <(jq '.totals' /tmp/before.json) <(jq '.totals' /tmp/after.json)
```

PR の本文にそのまま貼れば、「**always-on を 2,532 → 1,920 に**」と数字で語れます。「なんか減らしました」より説得力が桁違いです。

### 余談 — ツール自身が自分のバグを暴いた

このケーススタディの最初のラン、`audit` の出力がどうにも小さく見えました。`token-doctor`（tokopt をラップする小さなエージェント）が、別経路で `.github/agents/` 配下を独立に数え直したところ、**9 ファイル・8,114 トークンを audit が under-report していた**ことが判明しました。修正後の正しい数字が、上の 11,414 です。

教訓は明快で、**自分のツールの出力をクロスチェックできる手段を agent に与えると、agent はテストハーネスとして機能する**ということです。「LLM が計測機具のバグを発見する」というのは、これから増えていくパターンだと思います。

---

## 7 ファミリ × tokopt の役割マッピング

本書 16 章の **7 技法ファミリ**と、tokopt がカバーする部分／しない部分を整理します。**できないことを正直に書く**のは、本書 preface の規律そのものです。

| ファミリ（採用順） | tokopt の関与 |
|---|---|
| 1. Output control | `detect` の `polite-filler` / `format-inflation`（heuristic） |
| 2. Context scoping | `audit` で `applyTo:` が機能しているか（conditional に落ちているか）を検証 |
| 3. Prompt compression | `count` で before/after、`detect` の `kitchen-sink-system-prompt` |
| 4. Model tiering | **対象外**（モデル選択は人間の判断） |
| 5. Caching 規律 | **対象外**（runtime の prefix キャッシュ挙動が要る） |
| 6. Tool / MCP 規律 | `detect` の `mcp-overload` / `verbose-tool-descriptions` |
| 7. Workflow 選択 | **対象外**（ask vs edit vs agent はタスク判断） |

カバーしない 3 つは、**tokopt が責任を持たないと宣言している領域**です。**測れることだけ測る、決めるのは人間**、という分業です。

---

## CI への組み込み — 最も効果が見えやすい使い方

tokopt の中でもペイバックが早くなりやすいのが、CI への組み込みです。GitHub Actions に 1 ファイル追加するだけで、**always-on 税の回帰を全 PR で止められます**。

**blocking ゲートとして使う場合**の最小構成例はこんな形です。閾値の値はあくまで例で、必ず**自リポジトリのベースライン + 余裕分**に置き換えてください：

```yaml
name: token-budget
on:
  push:
    branches: [main]
  pull_request:
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: { go-version: '1.23.x' }
      - run: go install github.com/shinyay/getting-started-with-token-optimization/tools/tokopt/cmd/tokopt@latest
      - run: tokopt audit .
      # 例: 自リポジトリのベースライン + バッファに置き換える
      - run: tokopt report --threshold 1500 .
```

> [!TIP]
> 初回導入では、まず `tokopt audit .` のみを回してベースラインを共有し、`tokopt report` のステップに `continue-on-error: true` を付けて**警告運用**から始めるのがおすすめです。`--threshold` の blocking 化は、チームが数字に慣れてから昇格させてください。

閾値を超えたら `exit 2` で PR ブロックされる構成です。**「`AGENTS.md` を 200 トークン増やす」というコミットが、テストカバレッジや lint と同じ温度感でレビュー対象になります。**

### 段階的に導入する

最初からブロックすると反発が出ます。本書で勧めた漸進ローンチと同じく、tokopt も段階導入を推奨します：

1. **Day 1** — 1 リポジトリで `tokopt audit .` と `tokopt detect .` を回し、ベースラインを共有
2. **Week 1** — `--threshold` を**ベースライン + 50** にして、まず**警告のみ**の PR チェック
3. **Week 2** — スケジュール実行で全リポジトリを audit、worst offender を特定
4. **Month 1** — 2 週間 pass し続けたリポジトリから、ゲートを **blocking** に昇格
5. **Month 2** — 新エージェント・新スキル設計時に `tokopt anatomy` を必須化
6. **Month 3+** — CLI セッションログがあれば `tokopt tail` で runtime 外れ値も追う

「**コスト規律をマージ条件にする**」 — これが達成できると、`AGENTS.md` のサイズについての議論が要らなくなります。**あらかじめ合意した閾値が、議論の出発点を作ってくれる**からです。

---

## 週次 audit の実運用フロー

本書 16 章の **四半期トークン audit**は、tokopt があれば**週次**、あるいは**毎日**の習慣に降ろせます。

- **個人**：`alias tokpre='tokopt audit . && tokopt detect .'` を shell 起動に。長いセッションの前に `tokpre`
- **チーム**：スケジュール実行で全リポジトリを毎週 audit、結果を Issue や Slack にロールアップ
- **PR**：`tokopt --format md report . > audit.md` を sticky comment として貼り、レビュアーが PR 画面を離れずに内訳を見られるようにする

これらは全部、本書 13 章「**測ってから最適化せよ**」の自動化です。手で四半期に 1 回やる代わりに、機械が毎日 60 秒でやる。

---

## 設計思想 — 本書の規律をコードに落とす

`tokopt` には**意図的にやらないこと**が複数あります。本書 preface の編集規律を、ツール側で機械的に守るための制約です：

1. **ドル金額を出さない** — 価格は変わる
2. **コンテキスト窓サイズを仮定しない** — `--reference-window N` を**明示的に渡したときだけ**、N に対する割合を併記する
3. **measured と heuristic を必ずラベルで分ける** — 静的に測れないものは別枠で扱う
4. **ローカル tokenizer による近似であることを明言** — billing oracle ではない
5. **品質判定はしない** — トークンは測れる、品質は別軸。両者を混ぜない
6. **runtime セッションを覗かない** — 静的解析に徹し、動的部分はベンダーのダッシュボードに委ねる

「**数字は変わるが、構造は変わらない**」を体現するには、**変わる数字（価格・モデル名・窓サイズ）に依存しないツールである必要がある**、という素直な帰結です。

---

## ロードマップ

`tokopt` はまだ初期段階のツールです。本書のアンチパターン 14 個のうち、現在カバーしているのは静的に判定できるもの。残りは **runtime ログや routing telemetry**が必要なので、次に取り組みたい領域です。

意図的に**増やさないもの**もあります：モデル選択ルール、料金計算、品質評価。ツールを「便利機能の倉庫」にしないことが、**ツール自身がアンチパターンになる**のを防ぐ唯一の方法だと思っています。

---

## おわりに — Spend wisely

『トークン超入門』は、こう締めくくりました：

> Good luck. Spend wisely. そして、楽しんで。

本書のもう一つの合言葉は **Be fluent in the unit** — 単位に流暢になれ、でした。`tokopt` は、その**流暢さを毎 PR の習慣に変える**ための器具です。本を読み、語彙を手にし、規律を頭で理解する — そこまでが本の仕事でした。**それを PR 毎の習慣に変える**のが、この CLI の仕事です。

読み終わったら、最初の `tokopt audit .` を、いま開いているリポジトリで実行してみてください。**最初の数字が、たぶん少し驚き**になります。**驚きが要点**です。本書 16 章でも書いた通り、その驚きが「**どのファミリから手を付けるか**」を教えてくれます。

> 数字は変わるが、構造は変わらない。

その構造の上に、計測ファーストの習慣を載せていきましょう。

---

### 関連リンク

- 📘 姉妹書：[トークン超入門 — LLM の「単位」を腑に落とす](https://zenn.dev/shinyay/books/getting-started-with-tokens)
- 🛠 tokopt（GitHub）: [shinyay/getting-started-with-token-optimization](https://github.com/shinyay/getting-started-with-token-optimization)
