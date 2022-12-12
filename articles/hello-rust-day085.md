---
title: "100日後にRustをちょっと知ってる人になる: [Day 85]書籍: Rust プログラミング完全ガイド その9"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [rust]
published: false
---
## Day 85 のテーマ

![](https://storage.googleapis.com/zenn-user-upload/942b1e806720-20221205.png)

[Day 84](https://zenn.dev/shinyay/articles/hello-rust-day084) までに Rust の書籍の **[Rustプログラミング完全ガイド](https://book.impress.co.jp/books/1121101129)** の 1 章から 18 章までを読み終わりました。

- [第1章 Rustを始めよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC1%E7%AB%A0-rust%E3%82%92%E5%A7%8B%E3%82%81%E3%82%88%E3%81%86)
- [第2章 数値演算などの基本を把握しよう](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC2%E7%AB%A0-%E6%95%B0%E5%80%A4%E6%BC%94%E7%AE%97%E3%81%AA%E3%81%A9%E3%81%AE%E5%9F%BA%E6%9C%AC%E3%82%92%E6%8A%8A%E6%8F%A1%E3%81%97%E3%82%88%E3%81%86)
- [第3章 オブジェクトに名前を付ける](https://zenn.dev/shinyay/articles/hello-rust-day076#%E7%AC%AC3%E7%AB%A0-%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E5%90%8D%E5%89%8D%E3%82%92%E4%BB%98%E3%81%91%E3%82%8B)
- [第4章 実行の流れを制御する](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC4%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第5章 データシーケンスを使う](https://zenn.dev/shinyay/articles/hello-rust-day078#%E7%AC%AC5%E7%AB%A0-%E5%AE%9F%E8%A1%8C%E3%81%AE%E6%B5%81%E3%82%8C%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)
- [第6章 基本のデータ型を使う](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC6%E7%AB%A0-%E5%9F%BA%E6%9C%AC%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B%E3%82%92%E4%BD%BF%E3%81%86)
- [第7章 列挙と照合](https://zenn.dev/shinyay/articles/hello-rust-day079#%E7%AC%AC7%E7%AB%A0-%E5%88%97%E6%8C%99%E3%81%A8%E7%85%A7%E5%90%88)
- [第8章 混成的なデータ構造を使う](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC8%E7%AB%A0-%E6%B7%B7%E6%88%90%E7%9A%84%E3%81%AA%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0%E3%82%92%E4%BD%BF%E3%81%86)
- [第9章 関数を定義する](https://zenn.dev/shinyay/articles/hello-rust-day080#%E7%AC%AC9%E7%AB%A0-%E9%96%A2%E6%95%B0%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第10章 ジェネリックな関数や型を定義する](https://zenn.dev/shinyay/articles/hello-rust-day081#%E7%AC%AC10%E7%AB%A0-%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AA%E3%83%83%E3%82%AF%E3%81%AA%E9%96%A2%E6%95%B0%E3%82%84%E5%9E%8B%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第11章 メモリを割り当てる](https://zenn.dev/shinyay/articles/hello-rust-day081#%E7%AC%AC11%E7%AB%A0-%E3%83%A1%E3%83%A2%E3%83%AA%E3%82%92%E5%89%B2%E3%82%8A%E5%BD%93%E3%81%A6%E3%82%8B)
- [第12章 データの実装](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC12%E7%AB%A0-%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E5%AE%9F%E8%A3%85)
- [第13章 クロージャを定義する](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC13%E7%AB%A0-%E3%82%AF%E3%83%AD%E3%83%BC%E3%82%B8%E3%83%A3%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)
- [第14章 変更可能な文字列を使う](https://zenn.dev/shinyay/articles/hello-rust-day082#%E7%AC%AC14%E7%AB%A0-%E5%A4%89%E6%9B%B4%E5%8F%AF%E8%83%BD%E3%81%AA%E6%96%87%E5%AD%97%E5%88%97%E3%82%92%E4%BD%BF%E3%81%86)
- [第15章 範囲とスライス](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC15%E7%AB%A0-%E7%AF%84%E5%9B%B2%E3%81%A8%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9)
- [第16章 イテレータを使う](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC16%E7%AB%A0-%E3%82%A4%E3%83%86%E3%83%AC%E3%83%BC%E3%82%BF%E3%82%92%E4%BD%BF%E3%81%86)
- [第17章 入出力とエラー処理](https://zenn.dev/shinyay/articles/hello-rust-day083#%E7%AC%AC17%E7%AB%A0-%E5%85%A5%E5%87%BA%E5%8A%9B%E3%81%A8%E3%82%A8%E3%83%A9%E3%83%BC%E5%87%A6%E7%90%86)
- [第18章 データのカプセル化［メソッドとモジュール］](https://zenn.dev/shinyay/articles/hello-rust-day084#%E7%AC%AC18%E7%AB%A0-%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E3%82%AB%E3%83%97%E3%82%BB%E3%83%AB%E5%8C%96%EF%BC%BB%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89%E3%81%A8%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%EF%BC%BD)
- 第19章 トレイトを使う
- 第20章 オブジェクト指向プログラミング
- 第21章 標準ライブラリのコレクション
- 第22章 所有権、移動、コピー
- 第23章 借用とライフタイム
- 第24章 さらにライフタイムについて

## 第19章 トレイトを使う

この章での内容:

- トレイトを使えば、ジェネリック関数の呼び出しに関するコンパイラのエラーメッセージが読みやすくなる>こと
- ジェネリックパラメータの制約が 1 つにまとまったり、複数のトレイトに分かれたりする理由
- ジェネリックパラメータに制約がないと、できることがどれほど少ないか
- トレイトに入れた関数のスコープ
- 複数のメソッドを含むトレイトを作る方法
- 複数のトレイトに渡すジェネリックパラメータを制約する方法
- トレイト継承を使う方法
- トレイトを使って外部型にメソッドを追加する方法
- 標準トレイトの `Display` と `Debug` を実装する方法
- 便利なジェネリックトレイトを宣言する方法
- 型指定を持たないトレイトをシンプルに使える関連型
- イテレータの実装

### トレイトの概要についてメモ

**[Day 17](https://zenn.dev/shinyay/articles/hello-rust-day017)** などの振り返りになりますが、**トレイト**とはどういうものなのか、大事なことなので改めて自分のことばで表してみます。

他の言語仕様との比較をしながら、いろいろと振り返りを行っているので**トレイト**についても Java ではどういうことかを考えてみます。
まず、**トレイト**の定義ですが、様々な型に対して抽象化した任意の振る舞い (関数) を持たせることができる言語仕様でした。つまり、**トレイト**として意味のあるまとまりとして振る舞い (関数) のシグネチャを定義します。この時点では振る舞いの実体はなくてよくて、抽象化したシグネチャとして定義できていればよいです。この抽象化した振る舞いが定義された**トレイト**を、何らかの型 (構造体など) に対して関連付け (実装) を行って使用します。

つまり、トレイトとは Java で言うところの、**インターフェース**や**抽象クラス**のような役割をするものになります。

本に書かれている例として、平行根をもとめるメソッドを浮動小数点型 `f32` や `f64` に持たせることを行っていました。まずトレイトとしては次のように定義をします。

```rust
trait HasSqareRoot {
    fn sqrt(self) -> Self;
}
```

その実装としてそれぞれ次のようにしています。

```rust
impl HasSquareRoot for f32 {
    fn sq_root(self) -> Self { self.sqrt() }
}

impl HasSquareRoot for f64 {
    fn sq_root(self) -> Self { self.sqrt() }
}
```

他の例でも考えてみます。例えば、よくある演算として面積を求めるものを考えてみます。三角形と四角形、そして台形では面積の求め方がことなります。しかし、"面積を求める"という振る舞い自体は共通です。振る舞いが同じで挙動が異なるということになります。そこで、まず面積を求めるという振る舞いをするメソッドをトレイトに定義します。

```rust
trait Area {
    fn calc(&self) -> f64;
}
```

そして面積を求める対象の形に関する構造体を定義します。

```rust
struct Triangle {
    base: f64,
    height: f64,
}

struct Rectangle {
    base: f64,
    height: f64,
}

struct Trapezoid {
    top_base: f64,
    bottom_base: f64,
    height: f64,
}
```

この形に対して面積を求めるトレイトを実装します。

```rust
impl Area for Triangle {
    fn calc(&self) -> f64 {
        (self.base * self.height) / 2.0
    }
}

impl Area for Rectangle {
    fn calc(&self) -> f64 {
        self.base * self.height
    }
}

impl Area for Trapezoid {
    fn calc(&self) -> f64 {
        (self.top_base + self.bottom_base) * self.height / 2.0
    }
}
```

```rust
let triangle = Triangle {base: 10.0, height: 20.0};
let rectangle = Rectangle {base: 10.0, height: 20.0};
let trapezoid = Trapezoid {top_base: 10.0, bottom_base: 20.0, height: 10.0};

println!("三角形: {}", triangle.calc);
println!("四角形: {}", rectangle.calc);
println!("台形: {}", trapezoid.calc);
```

## Day 85 のまとめ

この書籍の中でトレイトがこの後半になって出てくるのが少し意外でした。トレイトをつかって様々な振る舞いを複数の型に対して定義をしていくことが可能になってくるというものなので、もう少し前半に出ていても良かったのかなと思いました。ですが、次の章でオブジェクト指向について考えることになるので、オブジェクト指向の前にトレイトを見て、オブジェクト指向言語ではない Rust に存在しているオブジェクト指向のような捉え方ということの認識が深まればよいのかな、と改めて思いました。そんな考えも踏まえて、改めて公式ドキュメントのトレイトに関して**共有する振る舞い**ということについて考えてみると、いろいろと理解が深まりました。

- [Traits: Defining Shared Behavior](https://doc.rust-lang.org/book/ch10-02-traits.html)

以下の内容が今日復習したことです。

- **第19章 トレイトを使う**
  - トレイトを使えば、ジェネリック関数の呼び出しに関するコンパイラのエラーメッセージが読みやすくなる>こと
  - ジェネリックパラメータの制約が 1 つにまとまったり、複数のトレイトに分かれたりする理由
  - ジェネリックパラメータに制約がないと、できることがどれほど少ないか
  - トレイトに入れた関数のスコープ
  - 複数のメソッドを含むトレイトを作る方法
  - 複数のトレイトに渡すジェネリックパラメータを制約する方法
  - トレイト継承を使う方法
  - トレイトを使って外部型にメソッドを追加する方法
  - 標準トレイトの `Display` と `Debug` を実装する方法
  - 便利なジェネリックトレイトを宣言する方法
  - 型指定を持たないトレイトをシンプルに使える関連型
  - イテレータの実装
