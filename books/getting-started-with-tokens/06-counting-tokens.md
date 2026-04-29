---
title: "第5章 — トークンを数える"
---

> **一言で:** 気にすべきコスト（金、レイテンシ、コンテキスト予算）はすべて**トークン数**から始まる。だから、コードで**正確に**、ブラウザで**ざっくり**、頭の中で**概算**で測る方法 — 三段階の道具を持つ必要がある。

---

## なぜこの章があるか

ここまで4章かけて「トークンとは何か」「言語で違う」を学びました。ここからは**実用フェーズ**。最初の問いは:

> **「このテキストは何トークン？」** に、すぐ答えられるか？

答えられないなら、**請求書もレイテンシもコンテキスト窓も推測でしか語れません**。本章で、3つの計測モード（正確・近似・概算）と、ほぼあらゆるプロンプトに使える**予算化ワークフロー**を身につけます。

---

## なぜ数えるのか

LLM の**意味のある制約はすべてトークン建て**:

- **金**: 入力トークン × 単価 + 出力トークン × 単価
- **レイテンシ**: 入力トークン数 + 出力トークン数 にほぼ比例
- **コンテキスト窓**: ハードな天井。超えるとリクエスト失敗、または古い内容が黙って削除

数えられないと、これらすべてが**勘**になります。英語散文で「安全」に感じる勘は、コード・JSON・非ラテン文字では**桁違いにズレる**ことを第4章で見ました。

問題は「数えるかどうか」ではなく「**どれくらいの精度で数えるか**」です。

---

## 3つの計測モード

```
   正確              近似               概算
 ┌────────┐         ┌──────────┐      ┌────────────┐
 │ コード │ ─────▶ │ Web ツール │ ───▶│ ルールオブ │
 │tokenizer│       │ ブラウザ  │      │ サム       │
 └────────┘        └──────────┘      └────────────┘
   遅い、            速い、            一瞬、
   精密              だいたい合う      ザックリ
```

判断の重みに応じて使い分けます:

- **本番出荷前のコスト見積もり** → **正確**
- **下書きプロンプトの感触チェック** → **近似**
- **ホワイトボードで構成スケッチ** → **概算**

---

## モード1: 正確（コードで）

モデルの**実際の tokenizer** でエンコードし、長さを取る方法。**金・レイテンシ・コンテキスト上限が絡む判断は、これしか信用しない**。

第3章の繰り返し: 各モデルファミリは独自の語彙を持ちます。**間違った tokenizer で数えると 10〜30% 誤差**。最初の問いは常に「**実際に呼ぶモデルに対応する tokenizer はどれか？**」。

### Python — `tiktoken`（OpenAI 系）

```python
import tiktoken

text = "How many tokens is this sentence?"

# モデル名から解決（ライブラリが正しい語彙にマップしてくれる）
enc = tiktoken.encoding_for_model("gpt-4o")

token_ids = enc.encode(text)
print(len(token_ids))    # 欲しいカウント
print(token_ids[:10])    # 整数 ID のリスト（デバッグに有用）

# どう分割されたか「見える化」する
for tid in token_ids:
    print(f"{tid:6d} -> {repr(enc.decode([tid]))}")
```

注意点:
1. tokenizer を直接選ばず、**モデル名**を渡す。後でモデルを切り替えたら**必ず再解決**
2. `encode` は整数 ID のリスト。カウントは `len(...)`。**個別 ID をデコード**して見ると、「どこで割れたか」が分かり直感が育つ

### Python — Hugging Face `transformers`（オープン系）

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")
# 認証が必要なリポジトリの場合: HF_TOKEN を環境変数に

# 注: encode() のデフォルトは add_special_tokens=True なので、
# テキスト本体だけを正確に数えたいときは明示的に False を渡すこと
token_ids = tokenizer.encode(
    "How many tokens is this sentence?",
    add_special_tokens=False,
)
print(len(token_ids))
```

`AutoTokenizer` は BPE / WordPiece / SentencePiece などを判別し、**統一インターフェース**を返します。重要なフラグ:

- `add_special_tokens=False` — `<bos>`, `<eos>` を含めずに**テキスト本体だけ**カウント
- `return_tensors=None`（デフォルト）— Python リストで返る（カウントにはこれ）

### JavaScript / TypeScript

ブラウザでも Node でもいくつかの選択肢:

```ts
// 1. js-tiktoken (GPT 系の JS port)
import { encodingForModel } from "js-tiktoken";

const enc = encodingForModel("gpt-4o");
const ids = enc.encode("How many tokens is this sentence?");
console.log(ids.length);
```

```ts
// 2. gpt-tokenizer (依存ゼロ、語彙同梱)
// ルート import (`from "gpt-tokenizer"`) はライブラリのデフォルト encoding を返すだけなので、
// モデルに合わせた正確な計測には model 別 import を使う
import { encode } from "gpt-tokenizer/model/gpt-4o";

const ids = encode("How many tokens is this sentence?");
console.log(ids.length);
```

```ts
// 3. @anthropic-ai/tokenizer は Claude 系の「近似」のみ。
//    課金や厳密なコンテキスト計測には絶対に使わず、
//    本物のトークン数は API の count_tokens エンドポイントで取ること。
import { countTokens } from "@anthropic-ai/tokenizer";
console.log(countTokens("How many tokens is this sentence?")); // 近似値
```

パターンは Python と同じ: **モデルに紐づく tokenizer をロード → encode → length**。違いはバンドルサイズと同梱語彙のラインナップ。

### プロバイダがローカル tokenizer を公開していない場合

Anthropic Claude や Google Gemini など、**tokenizer を非公開**にしているプロバイダもあります。公式手段は2つあり、それぞれ性質が大きく異なります:

- **API の `count_tokens` エンドポイント**（あれば）を呼ぶ。多くの場合**実際の生成は走らないので追加課金が発生せず**、返るのはプロバイダ側で確定したトークン数です（仕様はプロバイダごとに違うので必ずドキュメント確認）
- カウント用エンドポイントが無い場合は、**生成 API を最小限のリクエストで呼んで `usage.input_tokens` などを読む**。この方法は**実トークンを確実に消費**します

```python
# Anthropic 例: count_tokens は通常、課金されない見積もり
import anthropic
client = anthropic.Anthropic()

count = client.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello, world."}],
)
print(count.input_tokens)
```

```python
# OpenAI 例: 生成 API の usage を読む（こちらは実生成 → 課金される）
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=1,
)
print(resp.usage.prompt_tokens, resp.usage.completion_tokens)
```

> [!NOTE]
> **「カウント用エンドポイント」と「生成 API の usage を読む」は別物**です。前者は通常無料の見積もり、後者は実生成なので課金されます。CI でプロンプトサイズをチェックするような繰り返し計測では、**ローカル tokenizer がある場合はそちらを優先**し、無ければ**カウント用エンドポイントを優先**、生成 API は最後の手段にしてください。

---

## モード2: 近似（Web ツール）

主要プロバイダや tokenizer プロジェクトが、テキストを貼って色付き分割と数を返す Web ページを公開しています:

- OpenAI: `https://platform.openai.com/tokenizer`
- HuggingFace: `https://huggingface.co/spaces/Xenova/the-tokenizer-playground`
- Tiktokenizer: `https://tiktokenizer.vercel.app/`

**使うべき場面**:
- 手書きプロンプトの sanity check
- 絵文字・コード・混在スクリプトでの挙動探索
- 開発環境が手元にない時

**使ってはいけない場面**:
- スケール（1000本のプロンプトを順に貼れない）
- **機密データを含む入力**（テキストがマシンを離れる）
- ホストされていないクローズドモデル

**顕微鏡として使い、巻尺として使わない**。

---

## モード3: 概算（ルールオブサム）

ナプキン算用 — フィーチャーサイズを見積もる、コンテキストの塊が「大きすぎる気がする」を判定する、設計案を比較する — には正確な数は不要。**±30% の精度で十分**な場面に。

| コンテンツ種別 | 概算密度 | 等価 |
|---|---|---|
| 英語散文 | ~4 文字/token | ~0.75 token/word |
| ソースコード | ~3 文字/token | 散文より密 |
| JSON, XML, 引用多め | ~2-3 文字/token | さらに密 |
| CJK | 1 文字あたり 1〜3 token | 文字あたり多 token |
| その他複雑スクリプト | 大きく変動 | **必ず計測** |

具体例で感覚を:
- 200語の英語メール → 約 150 tokens
- 1,000文字の JS 関数 → 約 300〜350 tokens
- 1,000文字のネスト深い JSON → 400〜500 tokens
- 200文字の日本語段落 → 200〜600 tokens（tokenizer による）

> [!WARNING]
> 「**1 token ≈ 4文字**」は LLM 業界で最も引用され、**最も誤用される**数字。これは**特定ファミリの tokenizer での英語散文**の値。コード・JSON・非ラテン文字に当てはめると、**大幅に予算不足**になる。新しい入力タイプを見積もる時は、必ず1回は実測で校正。

---

## 単一文字列ではなく**会話全体**を数える

ここまでは**プレーンテキスト**を数えてきました。実際のプロンプトはプレーンテキストではない。**テンプレート化**されています。

Chat 形式の API では、各メッセージは role マーカと区切りトークンで包まれます:

```
<start>system
You are a helpful assistant.
<end>
<start>user
What's the capital of France?
<end>
<start>assistant
```

**これらの包み込みは見えませんが、実在しカウントされます**。短い2ターンの会話でも、「中身ゼロ」で**数十トークンの足場**を払っているのが普通です。

ルール: **テンプレート化されたプロンプトを tokenize する。生メッセージではない**。

```python
# transformers の例
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "What's the capital of France?"},
]

# テンプレート適用後の文字列
templated = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
print(templated)

# それを数える
ids = tok.encode(templated, add_special_tokens=False)
print(f"Templated tokens: {len(ids)}")
```

OpenAI の場合、公式ドキュメントに `num_tokens_from_messages()` のサンプルがあります（モデルバージョンごとにオーバーヘッド係数が違う）。

### tool / function 定義もカウントされる

モデルに利用可能なツールリストを渡すと、各ツール定義（名前、説明、パラメータスキーマ、ネスト全部）が**プロンプトに直列化されて tokenize**されます。

ユーザーには見えない。チャット UI にも出ない。**でも、毎ターン入力予算に乗っている**。

リッチに記述された数個のツールが、**ユーザーの質問本体より多くのトークン**を消費することは普通にあります。第10章で詳述。

---

## 出力を「予算化」する

入力は事前に正確に測れます。**出力は測れません** — 定義上、まだ生成されていないから。

代わりに、`max_tokens`（または `max_output_tokens`）で**上限**を設定:

```python
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    max_tokens=500,   # 500 tokens を超えたら中断
)
```

重要な性質:
- **大半のプロバイダは「実際に生成された数」で課金**。上限の値は課金額ではない
- 上限は**安全網であって目標ではない**。モデルは普通もっと早く止まる
- 上限が低すぎると**ぶつ切り回答**になる。**最長妥当応答**を基準にサイズすべき（平均ではなく）

見積もり用には、「上限の半分〜全部を使う」と仮定して予算化すると安全。

---

## 予算化ワークフロー

ほぼあらゆるプロンプト（一発スクリプトから長期エージェントまで）に使える流れ:

```
┌─────────────────────────────────────────────────┐
│ 1. コンテキスト窓の天井                         │  (モデル特性)
│        −                                        │
│ 2. 安全マージン (~10〜20%)                      │  (あなたの選択)
│        −                                        │
│ 3. 期待される出力上限                           │  (max_tokens)
│        =                                        │
│ 4. 入力予算                                     │
│                                                 │
│ 5. 入力トークンを実測 / 概算                    │
│        オーバーなら → trim, summarize, paginate │
└─────────────────────────────────────────────────┘
```

ステップごとに:

1. **天井**: 実際に呼ぶモデルのコンテキスト窓を調べる。**ハードな壁**として扱う
2. **安全マージン**: 上から 10〜20% を取る。chat テンプレートのオーバーヘッド、ツール定義、計測誤差をカバー。**壁にぶつかってクラッシュより、ヘッドルームを残す方が安い**
3. **出力上限**: 「これより長い回答は許容しない」という最大値を決め、その分予約。さもないと長い回答が**会話途中で入力空間を侵食**
4. **入力予算**: 残りが、システムプロンプト + 履歴 + 検索コンテキスト + ユーザーメッセージの**合計**に使える
5. **計測**: テンプレート済みプロンプトを tokenize（モード1）か概算（モード3）。オーバーなら何かを切る — 何をどう切るかは第13章

紙の上では当然に見えますが、実本番のプロンプトの多くがステップ2を完全に飛ばし、**障害でマージンの存在を発見**します。

### CI で予算チェック

「プロンプトテンプレートが入力予算に収まっているか」を CI で守るのは、**最も費用対効果の高いガード**の1つ。

```python
# tests/test_prompt_budget.py
import tiktoken
from myapp.prompts import build_system_prompt, build_tools_schema

MAX_INPUT_BUDGET = 6000  # コンテキスト窓 - 安全マージン - 出力予約

def test_system_prompt_within_budget():
    enc = tiktoken.encoding_for_model("gpt-4o")
    sys_tokens   = len(enc.encode(build_system_prompt()))
    tools_tokens = len(enc.encode(build_tools_schema()))
    static_total = sys_tokens + tools_tokens

    assert static_total < MAX_INPUT_BUDGET * 0.5, \
        f"Static prompt overhead too large: {static_total} tokens (>50% of budget)"
```

「**システム + tool 定義の固定費が予算の半分を超えたら警告**」のようなしきい値が、品質劣化を未然に防ぎます。

---

## Going deeper

### トークンはネットワーク上のバイトではない

API リクエストの JSON 包み（`"role"`, `"content"` のキー、波括弧、インデント）は**tokenize されない・課金されない**。プロンプトに渡る**値だけ**がカウント対象。

ネットワーク帯域で測ると、課金トークン数より遥かに大きい数字が出ます。**この差は正常**で、追いかけても意味がない。

### 空白と正規化は実装で違う

異なる tokenizer は、先頭空白・連続空白・改行を**それぞれ違う**ように扱います。先頭空白を次のトークンに含める実装、独立トークンにする実装、削除する実装。

実用上の含意: **tokenizer 間でトークン数を比較しない**。「1,000トークンのプロンプト」は**特定モデルに対してのみ意味がある**。

### Chat テンプレートはモデルファミリで違う

同じ tokenizer を使う2つのモデルでも、**chat メッセージの role マーカ・区切り**が違うことがあります。同じメッセージリストでも、**ターゲットモデルで違うトークン数**になる。

モデルファミリを切り替えたら、**テンプレート済みプロンプトを再計測**。「カウントは可搬」という思い込みは禁物。

### カウントをキャッシュする

プロンプトの**静的部分**（システム指示、tool 定義、few-shot 例）は、毎リクエスト数え直す必要がない:

```python
class PromptCounter:
    def __init__(self):
        self.enc = tiktoken.encoding_for_model("gpt-4o")
        self._static = len(self.enc.encode(build_system_prompt()))
        self._tools  = len(self.enc.encode(build_tools_schema()))

    def total(self, dynamic_text: str) -> int:
        return self._static + self._tools + len(self.enc.encode(dynamic_text))
```

数百万コールに乗ると、**静的部分の repeated tokenization は実コスト**。起動時に1回数えて、動的部分とだけ足し算する。

### 「スペシャルトークン」のオン/オフ

`tiktoken` の `encode` には `disallowed_special` というオプションがあります。デフォルトで `<|endoftext|>` のような特殊トークンが入力に含まれていると **エラー** になります（プロンプト注入対策）。

```python
enc.encode(text, disallowed_special=())  # 全許可（信頼できる入力にのみ）
```

ユーザー由来の入力では、**デフォルトのまま**にして、特殊トークン injection を弾くのが安全。

---

## よくある誤解 / FAQ

### Q1. 「文字数 / 4 で十分では？」
A. 英語散文だけ。日本語、コード、JSON では**桁違いにズレ**ます。新しいタイプの入力は**最初の1回は必ず実測**。

### Q2. 「tokenizer をモデル間で使い回せる？」
A. **不可**。モデルファミリごとに語彙が違う。GPT-4 用の `tiktoken` で Claude を測ると、誤差は20%以上になることがある。

### Q3. 「`tiktoken` は本番のレイテンシボトルネック？」
A. ほぼ無視できる。Rust 実装で μs オーダー。LLM 呼び出し自体（数百 ms 〜数秒）に比べると塵レベル。

### Q4. 「履歴が長くなったら毎回全部数えるの？」
A. **増分カウント**で十分。新しいメッセージだけ tokenize して、累計に足す。

### Q5. 「出力トークン数を予測する方法は？」
A. **ない**（生成してみるしかない）。ただし、過去の同種タスクの出力長を統計的に学習し、**信頼区間を持った見積もり**を作ることは可能。本番監視で `usage.completion_tokens` を log すると、後でモデル化できます。

---

## まとめ

- 計測は基礎。**測れない予算は管理できない**
- 判断の重さに応じてモードを使い分け: 本番＝コード、確認＝Web、設計＝概算
- ルールオブサムは tokenizer 依存。**「1 token = 4 文字」**は英語散文専用
- **テンプレート化済みプロンプト**を測る — chat role マーカ、tool 定義を含めて
- **出力は事前に測れない**。`max_tokens` で上限を切り、安全マージン + 出力予約を引いた残りが**入力予算**
- 静的部分の**カウントはキャッシュ**して、動的部分とだけ加算

---

## 章末演習

**演習 5.1**（5分）  
あなたの最近の Slack DM を1本コピーし、`tiktoken` で `cl100k_base` と `o200k_base` の両方で数えてください。差はどれくらいですか？

**演習 5.2**（10分）  
あなたのアプリのシステムプロンプト + tool 定義 + 典型的なユーザーメッセージを**テンプレート化済み形式**で組み立て、トークン数を出してください。**ツール定義が全体の何 %** を占めますか？

**演習 5.3**（CI 化チャレンジ）  
上記計測を pytest テストにし、しきい値（例: 静的固定費 < 2000 tokens）を超えたら fail するようにしてください。プロンプトの**意図しない肥大化**を未然に防ぐガードレールになります。

---

## 次の章へ

数えられるようになりました。次に問うべきは: **何と戦っているか** — すべてのプロンプト・履歴ターン・検索ドキュメントが収まらなければならない、ハードな天井。それが**コンテキスト窓**です。

→ [第6章 — コンテキスト窓](07-context-window)
