# 核実績ゲーム — history_atomic_bomb

核兵器・原子力・被爆史・冷戦・核軍縮・関連科学史を、時系列の「実績」として読み進める歴史ゲーム企画です。

プレイヤーが過去を改変するのではなく、史実イベントを見届けながら実績または「記録」を解除していく構成を基本としています。

## 公開ページ

**GitHub Pages:** https://insuns21.github.io/history_atomic_bomb/

実績一覧を1ページで閲覧できます。ページ内ではカテゴリーごとにまとまりを分け、検索とタグによる横断的な絞り込みに対応しています。上部のタグ一覧だけでなく、各実績カードに表示されたタグ自体もクリックして絞り込めます。複数タグを選んだ場合は、選択したタグをすべて含む実績を表示します。

## このプロジェクトで扱うもの

- 原子核物理・核分裂・核融合などの科学史
- 核兵器を実物へ変換した巨大工学・マンハッタン計画
- 核研究の政策化、使用論争、標的選定などの戦時政治・外交
- 広島・長崎の被爆、救護、被爆後障害、復興、記憶継承
- 冷戦、核軍拡、核抑止、MAD、ICBM・SLBM・戦術核
- NPT、TPNW、パグウォッシュ会議などの核軍縮・不拡散
- 原子力平和利用、核燃料サイクル、原子力事故
- 各国の核武装史、外交、文化、政治的和解
- 現代から見た未来実績（史実とは明確に区別）

単純に「核兵器は悪い」と結論だけを置くのではなく、**なぜ作ったのか、なぜ使ったのか、なぜ使った後も増やしたのか、なぜ使わないために持つのか、なぜ減らそうとしてもなくならないのか、そして人類はどう記憶してきたのか**を追います。

## 実績データの正本

[`ACHIEVEMENTS.md`](./ACHIEVEMENTS.md) を正本インデックスとし、実績本文は `achievements/*.md` にカテゴリー別で分割します。カテゴリーの構成と表示順は `ACHIEVEMENTS.md` に記載された一覧で管理します。

科学史から1945年8月へ至る部分は、**科学史・核物理の成立 → 核兵器開発・巨大工学 → 戦時政治 ― 原爆を使うまで**の三段階に分け、自然科学上の発見、兵器化の工学、国家の使用判断を同じものとして扱わない構成にしています。

実績名やゲーム内の文学的表現は創作できますが、史実、実際の発言、後世の回想、解釈、ゲーム用表現は区別します。年代・帰属などに不確かな点がある場合は `要検証` として扱います。

未来実績には `🔒` を付け、確認済みの史実と混在させません。

## タグ

各実績には複数のタグを明示し、GitHub Pages 上でカテゴリーをまたいで絞り込めるようにしています。タグの付与方針は [`TAGGING_GUIDELINES.md`](./TAGGING_GUIDELINES.md) を参照してください。

## ビルドと検証

GitHub Pages は `main` への push を契機に GitHub Actions で生成・公開されます。

ローカルでは次のコマンドで、カテゴリー別Markdownを読み込み、実績データの検証とサイト生成を実行できます。

```bash
python scripts/build_site_v2.py --check --strict-length --strict-tags
```

CI では本文長、タグ、重複などをカテゴリー横断で検証したうえで `_site` を GitHub Pages へデプロイします。

## 実績イラストの生成

イラスト候補と個別プロンプトは [`ILLUSTRATION_PROMPTS.md`](./ILLUSTRATION_PROMPTS.md) で管理します。共通の画風・ModelsLab設定は [`illustrations/config.json`](./illustrations/config.json) に置き、`scripts/generate_illustrations.mjs` が Markdown 内の各 `###` 実績見出しと `Positive prompt` / `Negative prompt` を読み取って生成します。

画像変換には `sharp` を使うため、最初に依存を入れます。

```bash
npm install
```

ModelsLab API キーを環境変数へ設定して実行します。

```bash
export MODELSLAB_API_KEY="..."
npm run gen:illustrations
```

生成画像は `assets/illustrations/` に **JPEG (`.jpg`)** として保存します。ModelsLab から PNG / WebP 等で返された場合も、ダウンロード後に JPEG へ正規化します。JPEG品質は `illustrations/config.json` の `jpeg_quality` で調整できます。

既に同じ実績の `.jpg` が存在する場合は API を呼ばずにスキップします。`.jpeg` / `.png` / `.webp` だけが存在する場合も API は呼ばず、ローカルで `.jpg` へ変換します。既定では変換成功後に元の非JPG画像を削除し、リポジトリ上の画像形式をJPGへ揃えます。実績・プロンプトを追加した後に同じコマンドを再実行すれば、未生成分だけAPI生成されます。

画像と `.meta.json` はリポジトリへコミットする想定です。

主なオプション:

```bash
# APIを呼ばず、生成・変換対象だけ確認
npm run gen:illustrations:dry

# パースされた実績を一覧表示
node scripts/generate_illustrations.mjs --list

# タイトル・見出しを部分一致で絞る
node scripts/generate_illustrations.mjs --only="明日も遊びたかった,路面電車"

# 既存画像があっても再生成
npm run gen:illustrations:force

# 並列生成
node scripts/generate_illustrations.mjs --concurrency=2
```

モデルは既定で `flux`。一時的に変更する場合は `MODELSLAB_MODEL_ID`、恒久的に変更する場合は `illustrations/config.json` の `model_id` を変更します。

```bash
MODELSLAB_MODEL_ID="flux-dev" npm run gen:illustrations
```

## 編集方針

被爆や核事故などの惨事は、単なる「達成感」の演出に寄せず、必要に応じて「記録されました」という扱いを想定します。一方で、一覧を惨事だけで埋めず、科学史、救護、復興、文化、軍縮、外交、技術史、希望、未解決問題も同じ時間軸上で扱います。

とくに広島・長崎については大きな数字だけでなく、三輪車、水、路面電車、黒い雨、似島、千羽鶴、浦上天主堂など、具体的な人・物・場所から歴史を見ることを重視します。

---

> **1945年に何が起こるかは、もう知っている。では、その後の人類は何をしたのか。**
