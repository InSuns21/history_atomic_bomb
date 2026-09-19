# イラスト生成プロンプト案

> 実績カードへイラストを付ける場合の Text-to-Image 用プロンプト台帳。史実本文の正本ではなく、`ACHIEVEMENTS.md` / `achievements/*.md` に対応する生成素材として管理する。

## 基本方針

- **権利・史実上のリスクが低い実績は原則として画像生成対象にする。** ただし、生成対象にするカードはすべて本ファイルで個別に監査し、`狙い` / Positive prompt / Negative prompt を手書きする。本文から scene prompt を自動補完しない。
- 被爆・事故では、遺体や重傷者の直接的な再現より、三輪車・弁当箱・石段・水・舟艇・路面電車・建物などから出来事を見せる。
- 史実写真と誤認されないよう、共通して **historical editorial illustration / clearly illustrated, not a documentary photograph** を指定する。
- 人物の内心、正確な顔貌、写真にしか存在しない瞬間を「再現写真」のように生成しない。
- 兵器内部は説明図化しすぎず、製造・作動の具体的手順を与える精密図面にはしない。
- 画像内に文字を生成させない。実績名・年月・キャプションはサイト側で重ねる。
- 初期生成は横長 `16:9` を想定する。カード側でトリミングする場合も主対象を中央寄りに置く。

## 権利・参照ルール

- **博物館・資料館・報道機関・出版社などが権利管理する写真や画像を、そのまま入力参照画像として使わない。** 利用条件を確認し、必要な許諾が取れていないものは非参照とする。
- **歴史資料そのものを描く場合は、公開された史実・文章情報・一般に知られた外形情報をもとに、構図・背景・視点を独自に作る。** 「公式写真のイラスト化」にはしない。
- 三輪車、弁当箱、人影の石、慰霊碑、建物遺構などは、**資料の事実**を描くのであって、**特定写真の表現**を写すのではない。
- **既存の漫画・アニメ・映画・ゲーム・書籍・ポスター等の固有キャラクターや表紙、コマ、ロゴ、象徴的な構図は再現しない。**
- 手塚治虫作品、`はだしのゲン`、`沈黙の艦隊` など**創作物そのものを実績で扱う場合も、画像は作品の歴史的文脈・制作時代・受容状況を独自の情景として描き、作品ビジュアルそのものの再現は避ける。**
- 新聞紙面、ポスター、パンフレット、館内展示パネルなどは、実在版面の再現になりやすい。必要な場合も**読める文字や固有ロゴを出さず、雰囲気描写に留める。**
- 生成時の共通 Negative prompt では、**museum photo / archival photo / manga panel / book cover / anime character / logo / direct copy** 系の誤生成をまとめて抑制する。

## 共通スタイルプロンプト

> 個別実績のプロンプトへ共通して付与する画風。Node の生成処理では `illustrations/config.json` の同内容を正として、各実績の手書き scene prompt の前後へ結合する。

**Common Positive prompt**
```text
historical editorial illustration, clearly illustrated and not a documentary photograph, original composition based on historical facts rather than any single archival or museum photograph, (lineart:1.2), (clean line art:1.2), (contour emphasis:1.4), bold outlines, strong edges, crisp ink lines, sharp edge definition, clean white outline stroke around the subject, white edge highlight, white contour accent, readable white trim separating the subject from the background, (flat colors:1.1), limited palette, clean cel shading, minimal gradients, simple and readable composition, strong silhouette readability, museum-exhibit tone, respectful historical tone, semi-realistic proportions, slightly poster-like clarity, clear foreground and background separation, subtle paper-like texture, restrained color design, no text in the image, no captions, no labels
```

**Common Negative prompt**
```text
photorealistic, documentary photograph, fake archival photo, exact recreation of a museum catalog image, exact recreation of a news photo, direct copy of an official reference photo, direct copy of a manga panel, direct copy of a book cover, copyrighted character, famous anime character, franchise mascot, recognizable logo, readable brand mark, hyperrealism, painterly brushwork, messy sketch, rough doodle, watercolor bleed, oil painting, soft edges, blurry outlines, weak silhouette, low contrast edges, overrendered shading, heavy gradients, glossy rendering, shiny surfaces, 3D render, CGI, plastic texture, anime exaggeration, chibi, super-deformed style, cute mascot style, fantasy elements, sci-fi effects, magic glow, graphic gore, excessive blood, exposed organs, corpse spectacle, modern objects, modern clothing, contemporary architecture where inappropriate, anachronistic military hardware, inaccurate machinery, readable text, letters, subtitles, speech bubbles, watermark, logo, UI, deformed hands, extra fingers, duplicate people, distorted anatomy, malformed face, cluttered composition, overcrowded scene
```

生成時は、既存の個別 prompt に残る `semi-realistic gouache and ink` など旧画風の共通句をスクリプト側で除去してから、この共通画風を先頭へ付与する。個別 prompt は主に **主題・場所・年代・構図・避けたい誤生成・権利上避けたい再現対象** を担当する。

### 手動監査・生成運用

`node scripts/generate_illustrations.mjs` は、本 Markdown の手書き実績 prompt と `achievements/*.md` の現行タイトル・年月を突き合わせる。現在は `manual_only=true` とし、**権利上の除外対象を除くすべての生成対象に手書き prompt を要求する。** 未登録カードを本文から自動補完する処理は使わず、欠落は `--check` の `[MISSING]` としてCIを失敗させる。

すでに同じ実績の画像が存在する場合は既定でスキップし、--force 指定時のみ再生成する。API・モデル・共通ポジネガ・出力サイズ・自動生成除外は illustrations/config.json で管理する。生成前には、旧共通句の除去に加えて、**権利衝突リスクの高い共通 NG 語**（museum photo, manga panel, book cover, anime character, logo など）を必ず付与する。

#### 標準ワークフロー

画像は「実績を追加したら全部まとめて生成」ではなく、**少数を確認 → prompt を直す → 系列へ展開**の順で扱う。

1. 先に `achievements/*.md` 側で実績本文・年月・タイトルを確定する。
2. 画像化してよい題材かを確認する。既存作品・現存著作物など権利衝突を起こしやすいカードは除外設定へ入れる。
3. 画像化するカードごとに、**主役・構図・歴史的手掛かり・感情トーン・禁止事項を人間が確認**し、`狙い` / Positive prompt / Negative prompt を手書きする。
4. `npm run gen:illustrations:check` で旧タイトル・年月ズレ・重複・手書き prompt 欠落を検査し、すべて0件にする。
5. `--dry-run` で対象と出力ファイル名を確認する。
6. `--only` で1～数枚だけ生成し、構図・時代考証・画風・権利上の独自性を確認する。
7. 問題があれば prompt を修正し、必要なカードだけ `--force` で再生成する。
8. 系列で画風が揃ったら残りへ広げる。

代表的なコマンド:

```bash
# 現行実績と手書きpromptの整合性を検査
npm run gen:illustrations:check

# 手動監査済みの生成対象を一覧表示
node scripts/generate_illustrations.mjs --list

# 生成・変換対象だけ確認
npm run gen:illustrations:dry -- --only "原子雲の上へ"

# 1枚だけ生成
npm run gen:illustrations -- --only "原子雲の上へ"

# 複数枚を部分一致で選ぶ
npm run gen:illustrations -- --only "原子雲の上へ,妻はロザリオを残した"

# 既存画像も再生成
npm run gen:illustrations:force -- --only "原子雲の上へ"

# 従来の equals 形式も利用可能
node scripts/generate_illustrations.mjs --only="原子雲の上へ"
```

#### 出力とスキップ規則

- 新規生成画像は `assets/illustrations/` に JPEG (`.jpg`) で保存する。
- 同じ実績の `.jpg` が既にある場合は、既定で API を呼ばずスキップする。
- `.png` / `.webp` / `.jpeg` だけがある場合は、API を呼ばずローカルで `.jpg` に正規化する。
- `--force` は既存画像がある場合にも再生成するため、**構図や prompt を変えたカードだけに限定して使う**。
- 生成時のモデル、最終 prompt、出力ファイルなどは `.meta.json` に保存する。
- ファイル名は**現行の実績年月・実績名**を正規化して作る。手書き prompt のタイトルが古いままなら --check が STALE として検出する。
- タイトル変更前の既存画像ファイルは自動リネームしない。変更後の現行タイトルを新規生成対象として扱うため、旧ファイルを残すか削除・移行するかはレビューして決める。

#### 手書きプロンプトと権利リスク除外

非除外カードはすべて、`achievements/*.md` の本文を読んだうえで **年月・実績名・史実上の留保・権利リスク・前後カードとの構図重複**を個別に確認し、本ファイルへ手書き prompt を置く。`--check` は現行実績と照合し、手書き prompt が欠けていれば `[MISSING]`、旧タイトルなら `[STALE]`、年月不一致なら `[DATE]`、二重登録なら `[DUP]` として失敗する。

既存作品のビジュアルそのものへ近づきやすい題材や、現存著作権の造形物そのものを主役にせざるを得ない題材は `illustrations/config.json` の `auto_prompts.exclude_source_files / exclude_tags / exclude_titles` で生成対象から外す。設定名 `auto_prompts` は既存スクリプトとの互換のため残しているが、自動 scene prompt 補完は無効化している。

除外は「永久に画像化しない」という意味ではない。作品そのものを描かず、**制作史・時代背景・受容史などを独自構図で描ける安全な手書き prompt** を人間が設計・レビューした場合は、その手書き prompt を明示的に採用できる。

#### プロンプト設計のチェックリスト

各カードは最低限、次の5点を決めてから生成する。

1. **主役** — 何を最初に見せるか。人物、物、建物、風景、抽象記号のどれか。
2. **構図** — 近景、遠景、俯瞰、斜め構図、縦方向の流れ、左右対比、群像など。
3. **歴史的手掛かり** — 年代、服装、建築、車両、器具、地形など。
4. **感情トーン** — 恐怖、静かな喪失、緊張、復興、倫理的不穏さなど。
5. **禁止事項** — 写真の直接再現、可読文字、現代物、過剰な宗教演出、兵器礼賛、ショック目的の残酷描写など。

個別 prompt に画風指定を詰め込みすぎず、**個別側は「何を、どこから、どう見せるか」へ集中**する。画風の正本は `illustrations/config.json` の共通 prompt とする。

#### 構図の重複を避ける

同一人物・同一時代のカードが連続する場合は、内容が違っていても全身人物の正面構図を繰り返さない。シリーズ全体で、たとえば次のように役割を分散する。

- **静物** — ロザリオ、弁当箱、三輪車など、物証を主役にする。
- **行為** — 救護、実験、移動など、人物の動作を見せる。
- **研究・記録** — 机、ノート、器具など、知的作業を主役にする。
- **建築・場所** — 如己堂、天主堂、工場など、空間そのものを見せる。
- **縦構図** — 上昇、巨大構造物、雲など、上下方向の意味を使う。
- **群像** — 子ども、救護者、作業員など、共同体を見せる。
- **抽象対比** — 科学と破壊、希望と不穏さなど、二つの意味を並置する。
- **総括構図** — 人物を中央に置き、左右や前後へ人生の対立要素を配置する。

永井隆関連では、**ロザリオ＝静物 / 救護＝斜め群像 / 原爆症研究＝机上 / 原子雲の上へ＝縦方向 / 如己堂＝建築 / 原子への希望＝抽象対比 / 子どもと本＝群像 / 最終カード＝左右対比**とし、同一人物カードの連続感を抑えている。

#### 生成後レビュー

採用前に、少なくとも次を確認する。

- 実績本文を読まなくても主題がおおむね分かるか。
- 前後カードと構図・距離・人物配置が重複していないか。
- 時代考証を大きく壊す現代物や誤った機械・服装がないか。
- 読める文字、ロゴ、ブランド、UI が紛れ込んでいないか。
- 史料写真・館蔵写真・既存宗教画・漫画・映画の一場面を直接再現したように見えないか。
- 被爆・戦争・事故を、見世物的な残酷描写や娯楽的スペクタクルへ寄せていないか。
- 宗教的・政治的な解釈を、画像だけで史実上の確定事項のように断定していないか。
- 原子力・核兵器を扱う場合、意図せず礼賛ポスターや兵器広告のようになっていないか。

画像生成は本文の代わりではない。**曖昧な史実を画像で確定させない**こと、画像の印象が本文の留保を上書きしないことを優先する。

---

## 科学史・核物理の成立

> この区画は全件手動監査済み。後世の「原子マーク」へ逃げず、各時代に実際にあった観測・実験・理論作業を主役にする。

### 1896 — 原子は静かではなかった

**狙い:** 放射能発見を「光らないのに写真乾板が感光した」という実験上の違和感から見せる。

**Positive prompt**
```text
late-19th-century French physics worktable, wrapped photographic plates kept inside dark black paper beside small uranium-salt crystals and simple laboratory glassware, one developed plate showing a darkened exposure pattern without any visible light source, subdued daylight from a high window, period wooden bench and brass instruments, composition centered on an unexpected photographic effect rather than a glowing radioactive object, no recognizable scientist portrait, no readable notes, 16:9
```

**Negative prompt**
```text
green radioactive glow, nuclear symbol, modern Geiger counter, modern laboratory, x-ray skeleton, mushroom cloud, readable labels, exact recreation of a famous archival photograph
```

### 1899 — 二種類ある

**狙い:** α線・β線の区別を、名称ではなく「物質を通り抜ける度合いが違う」実験として描く。

**Positive prompt**
```text
1890s radiation laboratory, a small uranium source in a shielded holder facing two simple ionization detectors, thin metal and paper absorbers placed at different distances, one path stopped quickly while another reaches farther through material, faint abstract trajectory cues only to clarify the experiment, dark wood bench, brass electrometer and period apparatus, analytical mood, no Greek letters or readable labels, 16:9
```

**Negative prompt**
```text
colorful textbook rays, giant alpha beta symbols, atom icon, modern electronics, laser beams, glowing uranium ore, readable graphs, exact historical photo recreation
```

### 1900–1903 — では三種類

**狙い:** さらに透過力の強い第三の放射線が加わったことを、遮蔽の厚さの差で示す。

**Positive prompt**
```text
early-1900s radiophysics bench, one radioactive source aligned with a sequence of increasingly thick paper, metal and dense shielding plates, three detector positions arranged so that two components are stopped earlier while a third penetrates much farther, subtle restrained path cues, period electroscopes and brass fittings, clean side-on experimental composition, no letters or textbook labels, 16:9
```

**Negative prompt**
```text
gamma symbol, superhero radiation beam, modern lead-lined lab, digital screens, glowing green effects, nuclear weapon imagery, readable annotations
```

### 1905 — 見えない衝突

**狙い:** ブラウン運動を、分子そのものではなく「顕微鏡下の粒子が不規則に動く」観測で表す。

**Positive prompt**
```text
1905 European laboratory, a researcher seen from behind looking through a brass microscope at suspended microscopic particles in a glass cell, beside the microscope a non-readable sketch card showing a wandering irregular particle path made of many short direction changes, simple water vessel and period instruments, warm natural light, emphasis on inferring invisible molecular collisions from visible random motion, no portrait likeness, 16:9
```

**Negative prompt**
```text
giant molecules, cartoon atoms colliding, modern fluorescence microscope, digital display, readable equations, psychedelic particle field, exact Einstein portrait
```

### 1905/09 — ほんの少しの質量で

**狙い:** E=mc²を巨大な原爆の閃光へ直結させず、「質量と放射エネルギーを同じ収支で考える」理論机として描く。

**Positive prompt**
```text
early-20th-century theoretical physics desk, a small precision balance with a tiny metal sample on one side, a prism and lamp producing a restrained beam of light across the desk, handwritten mathematical pages deliberately out of focus and unreadable, a physicist shown only as a seated silhouette working with pencil, quiet conceptual composition linking mass and emitted energy without any nuclear imagery, muted cream and charcoal palette, 16:9
```

**Negative prompt**
```text
readable E=mc2 formula, nuclear explosion, mushroom cloud, glowing atom icon, exact portrait of Einstein, modern calculator, science-fiction energy beam
```

### 1908 — 原子は計算道具じゃない

**狙い:** ペランの仕事を、ブラウン運動と沈降平衡から同じ原子数へ迫る「測定の積み重ね」として見せる。

**Positive prompt**
```text
1908 physical chemistry laboratory, microscope focused on suspended colloidal particles beside a tall narrow glass sedimentation vessel, repeated sample slides and measurement notebooks arranged methodically, a researcher comparing observations from two different experimental setups, no portrait likeness, atmosphere of patient quantitative verification, period brass microscope and wood furniture, no readable numbers or equations, 16:9
```

**Negative prompt**
```text
giant atom models, colorful molecule graphics, modern laboratory, readable Avogadro number, digital microscope, celebratory award scene
```

### 1910–1913 — 半端な電荷はありません

**狙い:** 油滴実験を、電極の間で一粒の油滴を追う精密測定として描く。

**Positive prompt**
```text
Millikan-era oil-drop experiment in an early-1910s laboratory, two horizontal metal electrode plates inside a compact chamber, a tiny illuminated oil droplet suspended between them and observed through a side telescope, simple lamp, battery apparatus and brass adjustment knobs, careful precision-measurement atmosphere, side cutaway-like editorial view without technical dimensions, no readable scale markings, 16:9
```

**Negative prompt**
```text
modern vacuum chamber, laser trap, floating glowing orb, giant electron symbol, exact textbook diagram, readable voltage values, modern oscilloscope
```

### 1911 — 原子の中はほとんど空っぽ

**狙い:** 金箔散乱実験を「ほとんど直進するが、ごく一部だけ大きく曲がる」という一枚で見せる。

**Positive prompt**
```text
early 20th century physics laboratory, a thin gold foil target inside a simple scattering apparatus, a narrow alpha-particle beam crossing the chamber, most faint light trajectories passing straight through while a very small number deflect sharply backward, brass instruments, dark wood workbench, period-accurate scientific equipment, cinematic side composition, muted amber and charcoal palette, physically plausible rather than fantastical, clear emphasis on experimental observation rather than later textbook iconography, no readable text, 16:9
```

**Negative prompt**
```text
colorful atom icon, planetary electron orbits, giant glowing nucleus, laser laboratory, modern electronics, science-fiction machinery, incorrect gold foil experiment geometry, readable labels, equations as text
```

### 1914 — エネルギーが足りない

**狙い:** β線の連続スペクトルを、後世のニュートリノではなく「測ったら一つの値に揃わなかった」実験上の問題として描く。

**Positive prompt**
```text
1914 radiation-measurement setup, beta source feeding particles through a magnetic field into a curved detector arrangement, a researcher recording many different deflection positions on paper, a simple non-readable dark band widening across a photographic plate to suggest a continuous energy spread, heavy brass magnets and period counters, puzzled analytical mood, no later neutrino imagery, 16:9
```

**Negative prompt**
```text
neutrino ghost particle, modern particle detector, colorful spectrum chart, readable graph axes, nuclear bomb, glowing radiation, digital screens
```

### 1919 — 原子核にも中身がある

**狙い:** 窒素へのα粒子照射から水素核が飛び出す実験を、核模型ではなく検出の瞬間として描く。

**Positive prompt**
```text
1919 nuclear physics laboratory, compact gas chamber containing nitrogen placed in line with a small alpha source, scintillation screen and microscope detector at one side, researcher watching for tiny flashes from emitted hydrogen nuclei, brass tubing and darkened observation area, restrained visual cues showing one secondary particle emerging from the chamber, no modern atom diagram, 16:9
```

**Negative prompt**
```text
giant proton symbol, modern cloud chamber, laser beam, colorful atomic nucleus, readable labels, bomb imagery, exact Rutherford portrait
```

### 1928 — 壁を抜けました

**狙い:** 量子トンネルを魔法の壁抜けにせず、α崩壊を説明する理論模型として見せる。

**Positive prompt**
```text
late-1920s theoretical physics office, chalkboard with an intentionally unreadable smooth hill-shaped potential curve and a small particle mark appearing on the far side, desk holding radioactive-decay measurements and a simple nucleus model made from plain spheres, physicist shown from behind connecting experiment to theory, restrained academic atmosphere, no fantasy portal or glowing effects, 16:9
```

**Negative prompt**
```text
magic wall, teleportation portal, superhero phase-through effect, readable equations, modern quantum computer, giant atom icon, nuclear weapon
```

### 1930–1934 — 何か一個足りない

**狙い:** β崩壊の「失われたように見えるエネルギー」を、見えない粒子を断定的に描かず測定収支の欠落として表す。

**Positive prompt**
```text
early-1930s theoretical and experimental physics workspace, beta-decay measurement apparatus on one side and a balance-like conceptual energy ledger on paper with one visibly incomplete segment, a physicist writing a speculative note at a desk, one detector receiving the electron while an uninstrumented empty direction remains open, subtle sense of a missing carrier without drawing a glowing invisible particle, period laboratory details, no readable text, 16:9
```

**Negative prompt**
```text
ghost particle, glowing neutrino, cartoon question mark, readable Pauli letter, modern detector, science-fiction visualization, nuclear bomb
```

### 1932 — 電荷を持たない弾丸

**狙い:** 中性子発見を、ベリリウム照射→パラフィン→反跳陽子という実験連鎖で見せる。

**Positive prompt**
```text
1932 Cavendish-style laboratory, alpha source aimed at a small beryllium target, neutral radiation crossing toward a paraffin block, recoil particles then entering a simple ionization detector, apparatus arranged clearly from left to right on a dark wooden bench, researcher observing instruments from the side, period brass and glass equipment, no glowing beams except faint editorial trajectory cues, 16:9
```

**Negative prompt**
```text
rifle bullet, giant neutron icon, modern particle accelerator, digital detector, radioactive green glow, weapon schematic, readable labels
```

### 1935 — 原子核をつなぐもの

**狙い:** 湯川の中間子論を、人物肖像ではなく「短距離の核力を媒介する粒子」という理論模型で表す。

**Positive prompt**
```text
mid-1930s Japanese theoretical physics study, two simple nucleus-model spheres representing proton and neutron set close together on a desk, a smaller intermediary bead-like model between them to suggest a short-range exchanged particle, handwritten pages and chalkboard diagrams deliberately unreadable, Japanese physicist shown only from behind in period academic clothing, quiet Kyoto-university atmosphere, no exact portrait, 16:9
```

**Negative prompt**
```text
anime scientist, exact Yukawa portrait, colorful quantum-field visualization, readable equations, giant atom icon, nuclear explosion, modern university laboratory
```

### 1949 — 予言した粒子は、いました

**狙い:** π中間子確認を、賞状ではなく宇宙線写真乾板に残った粒子飛跡から見せる。

**Positive prompt**
```text
late-1940s particle-physics laboratory, researcher examining a developed nuclear-emulsion photographic plate under a microscope, enlarged projected view showing a crisp charged-particle track that changes and ends in a characteristic secondary track pattern, stacks of cosmic-ray emulsion plates nearby, subdued postwar laboratory setting, emphasis on observed evidence matching an earlier prediction, no prize ceremony, no readable annotations, 16:9
```

**Negative prompt**
```text
Nobel medal close-up, exact portrait of Yukawa, colorful collider event display, modern accelerator hall, readable track labels, glowing particle fantasy
```

### 1933 — Everything is made from a dream

**狙い:** 楽曲のビジュアルは一切使わず、シラードがロンドンで連鎖反応を着想した「まだ核分裂すら未発見の段階」を描く。

**Positive prompt**
```text
London street in 1933 under gray autumn light, a solitary Central European physicist in period coat paused at a pedestrian crossing while buses and cars pass, his notebook open with only abstract branching dots and arrows too small to read, visual metaphor of one event producing several successors emerging subtly from the page, ordinary city life surrounding a private scientific idea, no resemblance to any musician or album artwork, no nuclear explosion, 16:9
```

**Negative prompt**
```text
Mr.Children imagery, album cover, concert stage, song lyrics, readable English text, mushroom cloud, glowing atom icon, exact Szilard portrait, modern London traffic
```

### 1934 — とりあえず中性子を当ててみよう

**狙い:** フェルミらの系統的照射実験を、多数の試料とパラフィンによる減速という「片っ端から試す研究」として描く。

**Positive prompt**
```text
1934 Rome physics laboratory, long bench lined with many small element samples in simple holders, a compact neutron source being moved from sample to sample, paraffin blocks placed around one test position, researchers in shirtsleeves comparing detector responses, cluttered but disciplined experimental workflow, warm Mediterranean daylight and period instruments, no exact portraits, no readable element names, 16:9
```

**Negative prompt**
```text
modern reactor, glowing neutron beam, giant periodic table, readable labels, cartoon trial-and-error scene, bomb laboratory, modern PPE
```

### 1938/12 — バリウムがいる。なぜ？

**狙い:** 「ウランを調べていたのに、化学分析で軽い元素が出てきた」という違和感を実験机で表す。

**Positive prompt**
```text
late-1930s radiochemistry laboratory in Berlin, two chemists shown from the side and back comparing glass test tubes and precipitates under warm bench lamps, a heavy uranium sample apparatus on one side and unexpectedly separated pale crystalline material on the other, notebooks and period glassware without legible writing, visual mood of scientific surprise rather than celebration, muted green gray and warm tungsten light, historically grounded laboratory details, no readable text, 16:9
```

**Negative prompt**
```text
mushroom cloud, nuclear bomb, glowing radioactive slime, giant atom symbols, modern laboratory, digital screens, readable periodic table text, readable notes, fantasy chemistry
```

### 1938/12–1939/02 — 原子核は割れる

**狙い:** 核分裂の解釈を、巨大な爆発ではなく「液滴模型が二つに分かれる」理論的理解として見せる。

**Positive prompt**
```text
winter 1938-1939 theoretical physics setting, two physicists in heavy coats seated at a simple outdoor bench or cabin table, notebook showing an unlabeled droplet-shaped nucleus sketch stretching and dividing into two large fragments, pencil calculations intentionally unreadable, snowy northern landscape beyond, calm intellectual breakthrough rather than spectacle, no exact portraits of Meitner or Frisch, 16:9
```

**Negative prompt**
```text
atomic bomb, mushroom cloud, giant exploding atom, exact famous portrait, readable equations, fantasy energy burst, modern laboratory
```

### 1939 — 一個割れたら、次も割れる

**狙い:** 連鎖反応を兵器設計ではなく、「一回の核分裂から複数の中性子が次へ進む」物理現象として描く。

**Positive prompt**
```text
1939 laboratory editorial illustration, small uranium sample target in a simple experimental chamber, one incoming neutron path followed by a split event and several outgoing neutron paths reaching neighboring sample nuclei, restrained diagram-like trajectories embedded in a real period laboratory scene, detectors and counters around the chamber, scientists observing from a distance, no bomb geometry or critical-mass dimensions, 16:9
```

**Negative prompt**
```text
weapon blueprint, bomb core, critical mass dimensions, mushroom cloud, colorful textbook atom cartoon, modern reactor, readable formulas
```

### 1939 — 同じウランではない

**狙い:** U-235とU-238の違いを「見た目は同じ、質量差だけがわずかに違う」分離問題として見せる。

**Positive prompt**
```text
late-1930s isotope-physics laboratory, two visually identical uranium sample containers on a precision mass-spectrograph workbench, subtle branching ion paths bending by slightly different amounts through a magnetic field, large industrial separation machinery only faintly suggested in the background as a future engineering consequence, analytical restrained composition, no isotope numbers visible, 16:9
```

**Negative prompt**
```text
different colored uranium rocks, readable U-235 or U-238 labels, bomb core, enrichment blueprint, modern centrifuges, glowing radiation, textbook diagram
```

### 1941/02 — もう一つの燃料

**狙い:** プルトニウムを「第二の爆弾材料」ではなく、まず人工元素の微量試料として描く。

**Positive prompt**
```text
1941 Berkeley laboratory, large cyclotron equipment looming in the background while chemists at a small bench handle a tiny irradiated target disk and minute chemical sample in glassware, contrast between enormous accelerator machinery and almost invisible amount of newly produced element, researchers shown as small non-identifying figures, no weapon parts, muted industrial gray and warm lab light, 16:9
```

**Negative prompt**
```text
plutonium bomb core, weapon assembly, glowing green sample, modern accelerator, readable element symbol, superhero radiation effect, exact scientist portraits
```

### 1942/12/02 — 連鎖は止められる

**狙い:** 世界初の制御連鎖反応を、スタジアム下の黒鉛パイルと制御棒という「爆発しない核反応」で見せる。

**Positive prompt**
```text
under the stands of Stagg Field in Chicago on December 2 1942, massive roughly spherical stack of dark graphite blocks and uranium components filling a cramped indoor court, long control rods entering the pile, scientists standing at simple instruments and a manual control station, subdued tense concentration, no flash or explosion, industrial improvised atmosphere, no exact famous group-photo composition, no readable text, 16:9
```

**Negative prompt**
```text
nuclear explosion, glowing reactor core, modern control room, cooling towers, exact archival group photograph, readable CP-1 sign, futuristic reactor
```


---

## 日本の原爆研究 ― ニ号研究とF研究

> この区画は全件手動監査済み。日本側の研究を「あと一歩で原爆完成」へ誇張せず、基礎科学・小規模実験・資源探索・工業力差をそれぞれ別の絵にする。

### 1937 — 日本にもサイクロトロン

**狙い:** サイクロトロンを最初から原爆装置だったように描かず、戦前日本の基礎核物理研究装置として見せる。

**Positive prompt**
```text
1937 RIKEN physics laboratory in Tokyo, early Japanese cyclotron dominating the room with large round magnet poles, vacuum chamber and period control equipment, researchers in lab coats adjusting instruments for nuclear-physics experiments, sample holders and biological-research materials visible on side benches to suggest broad scientific use, no military personnel and no weapon imagery, original historical editorial composition, no readable labels, 16:9
```

**Negative prompt**
```text
atomic bomb, mushroom cloud, military propaganda, modern particle accelerator, glowing radiation, exact archival photograph recreation, readable RIKEN signage
```

### 1940 — 原爆、できるんですか？

**狙い:** 軍が最先端の核物理へ「兵器になるのか」と問い始めた段階を、研究者と軍人の距離で描く。

**Positive prompt**
```text
1940 Japanese research institute meeting room, nuclear physicists at a laboratory table with uranium samples and detector apparatus while army aviation officers in uniform ask questions from the opposite side, notebooks and simple fission sketches deliberately unreadable, no bomb model and no sense of an established weapons program, restrained atmosphere of feasibility inquiry rather than production, 16:9
```

**Negative prompt**
```text
completed Japanese atomic bomb, secret superweapon poster, readable military orders, exact portraits, modern lab, giant atom icon, triumphant nationalism
```

### 1942/08 — 米国でも間に合わないでしょう

**狙い:** 「理論上可能」と「戦時中に工業化できる」は別だと見積もった海軍研究会を、巨大必要設備の計算で示す。

**Positive prompt**
```text
August 1942 Japanese naval nuclear-physics study meeting, senior scientists and naval officers around a long table comparing small laboratory apparatus with huge paper estimates of industrial buildings, electric power and uranium processing, all figures and writing blurred, one wall map of the United States shown only generically, skeptical technical atmosphere emphasizing scale and time rather than impossibility in principle, no exact portraits, 16:9
```

**Negative prompt**
```text
readable calculations, exact historical meeting photo, finished bomb design, dismissive comedy, propaganda caricature of the United States, modern presentation slides
```

### 1941/04–1943/01 — 夢見る学者じゃいられない@日本

**狙い:** 基礎研究者が軍委託の戦時研究へ組み込まれる移行を、同じ研究室に軍文書と濃縮装置が入ってくる変化で描く。

**Positive prompt**
```text
RIKEN laboratory transitioning from 1941 to early 1943, physicists beside cyclotron and neutron experiments while a sealed army research commission folder arrives on the workbench, in the background technicians begin assembling a tall thermal-diffusion apparatus for uranium isotope work, no weapon parts, visual emphasis on basic nuclear science being redirected into wartime commissioned research, period Tokyo laboratory, 16:9
```

**Negative prompt**
```text
atomic bomb assembly, readable military contract, exact Nishina portrait, heroic wartime propaganda, modern enrichment plant, mushroom cloud
```

### 1943–1945 — 陸軍とは別口です

**狙い:** F研究をニ号研究の単なる別名にせず、京都帝大側で海軍ルートの別計画が並行した構図にする。

**Positive prompt**
```text
wartime Kyoto Imperial University physics laboratory, academic researchers working around neutron-measurement equipment and a conceptual centrifuge prototype while a naval liaison officer delivers a separate project folder, distant inset of Tokyo-based army research kept visually separate, no direct connection line between the two, emphasis on parallel but distinct military-sponsored research programs, no exact scientist portraits, no readable labels, 16:9
```

**Negative prompt**
```text
single unified Japanese bomb project, completed centrifuge cascade, exact Yukawa portrait, readable F-research documents, modern laboratory, weapon blueprint
```

### 1943–1945 — ウランはどこですか

**狙い:** 原爆研究が鉱山・輸送・資源探索の問題でもあったことを、東アジア各地の鉱石調査で見せる。

**Positive prompt**
```text
wartime geological field survey in East Asia, Japanese geologists and military logistics personnel examining dark mineral samples at a rough mine site, crates, assay tools and railway transport maps spread on a field table, additional sample sacks arriving from several distant regions, harsh logistical atmosphere showing scarcity and search rather than abundance, no readable place names, no weapon imagery, 16:9
```

**Negative prompt**
```text
glowing uranium ore, treasure-mine fantasy, exact occupation map with readable labels, atomic bomb, triumphant resource conquest poster, modern mining machinery
```

### 1944/03–1945/04 — 10パーセントを10キロください

**狙い:** 数字が「完成寸前」を意味しないよう、研究室規模の熱拡散塔と必要量の巨大な隔たりを一枚で見せる。

**Positive prompt**
```text
1944 RIKEN building interior, tall experimental thermal-diffusion column occupying a modest laboratory while researchers collect only tiny sample containers at the bottom, nearby storage shelves and scales make the desired kilogram-scale quantity feel impossibly large by comparison, wartime blackout windows and improvised equipment, no enrichment percentage text or bomb components, sober engineering reality, 16:9
```

**Negative prompt**
```text
readable 10 percent or 10 kilogram labels, weapon-grade uranium ingot, completed bomb, giant industrial enrichment factory, modern centrifuge, heroic breakthrough scene
```

### 1945 — 同じ物理、違いすぎる工業力

**狙い:** 研究者の物理学水準ではなく、国家規模の工業基盤の差が決定的だったことを左右のスケール差で示す。

**Positive prompt**
```text
1945 comparative editorial scene, on one side a compact Japanese university or RIKEN laboratory with cyclotron, small isotope-separation apparatus and a handful of researchers, on the other side vast American wartime industrial complexes, reactors, power lines, rail yards and large workforces seen from far away, no national triumphalism and no weapons shown, dramatic difference in scale rather than intelligence, no readable labels, 16:9
```

**Negative prompt**
```text
racial or national superiority caricature, exact facility maps, completed Japanese bomb, cheering American propaganda, readable statistics, mushroom cloud
```

### 1945/08/08–13 — 作れなかった、僕たちには無理だった

**狙い:** 「作れなかった研究者」が、広島で自分たちの核物理を使って原爆を同定する逆説を調査現場で描く。

**Positive prompt**
```text
Hiroshima in August 1945, Japanese nuclear physicists examining damaged x-ray film, simple radiation detectors and scorched material samples at a temporary investigation table among city ruins, no bodies and no dramatic blast recreation, their own small scientific instruments foregrounded against destruction created by a weapon their wartime programs could not build, restrained analytical grief, no exact portraits, 16:9
```

**Negative prompt**
```text
graphic casualties, triumphant discovery, completed Japanese bomb, exact archival investigation photo, readable notes, glowing radiation, mushroom-cloud spectacle
```

### 1945/11/24 — 海へ沈むサイクロトロン

**狙い:** 軍事利用との境界が、基礎研究装置そのものの破壊として現れた敗戦後の断絶を描く。

**Positive prompt**
```text
Tokyo Bay in November 1945, dismantled heavy cyclotron magnet sections and scientific equipment being lowered by crane from a barge toward the water under occupation supervision, Japanese physicists watching from a distance, overcast gray sea, no weapon present, composition centered on a research instrument being physically removed because of its wartime association, sober end-of-era tone, no readable military markings, 16:9
```

**Negative prompt**
```text
nuclear bomb dumping, exact archival photo reproduction, triumphant occupation propaganda, modern crane ship, glowing equipment, readable signs
```

---

## 核諜報 ― 原爆の秘密をめぐる情報戦

> この区画は全件手動監査済み。スパイ映画のような銃・尾行ではなく、機密資料・正規アクセス・複数経路・暗号解読という情報の流れを主役にする。

### 1944–1945 — 最高機密、共有済み

**狙い:** 一人の「超スパイ」ではなく、複数の独立情報源から同じ秘密が照合された構造を描く。

**Positive prompt**
```text
wartime intelligence editorial composition, three separate anonymous source paths beginning from different Manhattan Project workplaces and converging on one Soviet intelligence desk, each path carrying sealed folders, microfilm or handwritten technical notes with all details unreadable, analysts comparing overlapping diagrams without any actionable weapon geometry, no famous spy portraits, tense documentary tone emphasizing redundancy of sources, 16:9
```

**Negative prompt**
```text
detailed bomb blueprint, readable classified documents, James Bond-style spy action, guns, exact Klaus Fuchs or Theodore Hall portrait, Soviet propaganda poster
```

### 1944–1946 — 通行証は本物です

**狙い:** コヴァルの強みが偽装侵入ではなく「正式な米兵・正式な最高機密資格」だったことをアクセス管理で見せる。

**Positive prompt**
```text
1944-1945 Manhattan Project security checkpoint, uniformed US Army technical specialist presenting a legitimate identification badge to enter multiple restricted laboratory and industrial areas, guards wave him through while sealed health-physics equipment cases and access logs remain in view, second scene transition shows a different sensitive facility reached with the same credentials, no exact portrait of George Koval, no readable badge data, 16:9
```

**Negative prompt**
```text
forged passport, trench-coat spy cliché, burglary, weapon blueprint, exact Koval portrait, readable security badge, action-thriller lighting
```

### 1950/02/02 — 一人捕まえたら、網が見えた

**狙い:** フックス逮捕から連絡役・家族・別の協力者へ捜査が広がった「ネットワーク可視化」を資料と尋問で描く。

**Positive prompt**
```text
1950 British-American counterintelligence office, one detained physicist shown only as a distant seated silhouette while investigators place several anonymous contact cards and files onto a wall board connected by simple thread lines, each new file leading to additional names and locations but all writing unreadable, VENONA-derived clue sheet kept as one source among others, procedural investigation rather than thriller action, 16:9
```

**Negative prompt**
```text
exact Fuchs portrait, torture scene, readable suspect names, sensational conspiracy wall with photos, guns, courtroom drama, bomb design
```

### 1953/06/19 — 最高機密の代価は死刑

**狙い:** ローゼンバーグ事件を「二人とも同じ程度の役割だった」と画像で断定せず、判決と後世の史料評価の非対称を示す。

**Positive prompt**
```text
early-1950s American legal-document scene, two defendant files side by side beneath a death-sentence court order with all text blurred, one file visibly thicker with multiple intelligence documents while the other contains fewer and more ambiguous records, prison exterior only faintly suggested in background, no execution method shown and no exact portraits, sober historical controversy rather than guilt spectacle, 16:9
```

**Negative prompt**
```text
electric chair, execution scene, exact Rosenberg portraits, readable verdict, partisan innocence-or-guilt poster, sensational Cold War propaganda
```

### 1995/07 — 暗号は陰謀を忘れない

**狙い:** VENONA公開を「秘密が突然暴かれた」ではなく、保存された暗号通信が半世紀後に史料へ変わる過程として描く。

**Positive prompt**
```text
1995 US intelligence archive room, declassified boxes opened beside enlarged facsimiles of old Soviet encrypted cable pages with all groups of characters deliberately blurred, historians and archivists compare wartime intercept tapes with later partial decryptions, redaction stamps and release folders present but unreadable, quiet archival revelation after decades, no spy-action imagery, 16:9
```

**Negative prompt**
```text
readable cipher text, hacker computer code, exact VENONA page reproduction, spy thriller silhouettes, guns, bomb blueprint, modern cyberattack imagery
```

---

## マンハッタン計画

> この区画は全件手動監査済み。兵器内部の精密な構造ではなく、国家規模の施設・資源・計算・検証・航空・兵站が一つの計画へ収束していく過程を描く。

### 1942/08/13 — 地図にはない計画

**狙い:** 「マンハッタン」という名前と実際の巨大施設が全米へ分散していた落差を、司令部の机と複数拠点で見せる。

**Positive prompt**
```text
1942 US Army engineering planning office, a large wall map of the United States with several unlabeled pinned locations connected by plain thread, stacks of construction folders, procurement ledgers and rolled blueprints without readable text, uniformed engineers and civilian administrators viewed from behind around a long table, no single laboratory dominating the scene, visual emphasis on a secret nationwide industrial program emerging from paperwork and logistics, muted olive and paper tan palette, 16:9
```

**Negative prompt**
```text
readable classified map labels, exact Manhattan Project document reproduction, nuclear bomb, mushroom cloud, modern command center, glowing atom symbols, heroic propaganda poster
```

### 1942–1943 — 街ごと作ります

**狙い:** 研究所ではなく「都市そのものが巨大な開発装置」になったことを見せる。

**Positive prompt**
```text
1944 Oak Ridge Tennessee seen from a high oblique viewpoint, enormous wartime industrial complexes connected by roads and power lines, a huge U-shaped diffusion plant in the distance, rows of temporary houses, buses and construction traffic, wooded Tennessee ridges surrounding a rapidly built secret city, scale emphasized by tiny workers and vehicles, overcast wartime atmosphere, muted olive brown and steel gray palette, detailed but not map-like, no readable text, 16:9
```

**Negative prompt**
```text
futuristic city, skyscrapers, modern cars, solar panels, readable signs, exact classified map, glowing nuclear symbols, mushroom cloud
```

### 1943 — 砂漠に現れた街

**狙い:** ロスアラモスを「天才科学者の研究室」ではなく、山中に急造された閉鎖都市として描く。

**Positive prompt**
```text
1943 Los Alamos mesa in New Mexico, newly built wartime laboratory buildings, barracks, dirt roads and utility lines spreading across a high desert plateau, school-like older buildings mixed with rapid military construction, buses and small groups of scientists and workers arriving, distant mountains and dry pine landscape, high oblique view emphasizing an isolated town created for one secret purpose, no readable signs, 16:9
```

**Negative prompt**
```text
modern Los Alamos campus, exact aerial archival photograph, futuristic research city, mushroom cloud, giant portraits of scientists, readable road signs
```

### 1942–1943 — 同じ元素なんですけど

**狙い:** 化学的にはほぼ同じ同位体を、わずかな質量差だけで分ける難しさを実験と工場の中間として示す。

**Positive prompt**
```text
wartime isotope-separation laboratory transitioning into industry, two nearly identical streams of material entering a large generic separation apparatus, precision balances and mass-spectrograph components in the foreground, faint silhouettes of three different large-scale separation halls beyond glass, emphasis on tiny physical difference requiring enormous machinery, no isotope numbers or process dimensions visible, muted steel gray and tan palette, 16:9
```

**Negative prompt**
```text
readable U-235 U-238 labels, centrifuge cascade blueprint, weapon diagram, glowing uranium, modern enrichment facility, exact technical schematic
```

### 1943–1944 — 三つとも作ります

**狙い:** 一方式に賭けず、異なる三つの濃縮方式を同時並行で建設した「不確実性を資金で潰す」構図にする。

**Positive prompt**
```text
1943-1944 Oak Ridge panoramic industrial composition divided naturally into three neighboring production environments: large electromagnetic magnet halls, a vast diffusion-process building, and rows of tall thermal-diffusion columns, construction cranes and wartime workers linking the facilities by roads and pipelines, no process labels, visual emphasis on three expensive approaches being built at once before any clear winner was known, overcast Tennessee landscape, 16:9
```

**Negative prompt**
```text
three labeled textbook diagrams, exact process schematics, readable facility names, modern centrifuges, bomb assembly, triumphant propaganda composition
```

### 1943–1945 — 銅がないので銀を貸してください

**狙い:** 財務省の銀が巨大電磁石の導体へ変わる、マンハッタン計画らしい資源動員の異様さを一枚にする。

**Positive prompt**
```text
wartime industrial interior at the Y-12 electromagnetic separation plant, enormous calutron magnet structures and heavy electrical coils dominating the hall, workers handling plain silver-colored bullion bars and thick conductor material as industrial stock rather than treasure, cranes and wartime factory scaffolding, sense of national-scale resource mobilization, 1940s work clothes and safety gear, muted metallic gray and warm industrial light, no readable text, 16:9
```

**Negative prompt**
```text
jewelry, treasure chest, gold bars, modern factory robots, modern PPE, glowing radiation, bomb assembly, detailed weapon blueprint, readable signs
```

### 1943–1945 — 穴をもっと小さく

**狙い:** 気体拡散の核心を「巨大工場」と「均一な微細孔を持つ障壁材」というスケール差で見せる。

**Positive prompt**
```text
inside the wartime K-25 gaseous-diffusion plant, immense repeating rows of sealed industrial process units and pipework disappearing into perspective, foreground engineer examining a small round porous barrier sample under a magnifier, tiny texture emphasized but no microscopic pore dimensions, contrast between a hand-sized material problem and factory-scale infrastructure, period protective clothing, no readable gauges or labels, 16:9
```

**Negative prompt**
```text
microscopic pore blueprint, exact UF6 process diagram, modern centrifuge hall, glowing gas, bomb components, readable technical annotations
```

### 1944/07–09 — 69日で建てました

**狙い:** S-50の異常な突貫工事を、完成前から運転される分離塔群と建設作業の同居で描く。

**Positive prompt**
```text
summer 1944 wartime construction site at Oak Ridge, long rows of tall narrow thermal-diffusion columns already operating on one side while scaffolding, welding crews and unfinished pipework continue immediately beside them, muddy ground, cranes and temporary lighting, sense of a factory being commissioned before construction is fully complete, no process labels or dimensions, muted industrial brown and steel palette, 16:9
```

**Negative prompt**
```text
modern refinery, futuristic tower array, exact engineering blueprint, readable construction signs, bomb imagery, celebratory ribbon cutting
```

### 1945 — 0.7パーセントを拾い集めて

**狙い:** 三方式を直列につないで濃縮度を上げたことを、兵器そのものではなく「工場から工場へ渡される材料」で見せる。

**Positive prompt**
```text
1945 Oak Ridge industrial logistics scene, sealed generic process containers moving in sequence from a thermal-diffusion area to a vast diffusion plant and then toward electromagnetic separation halls, workers and small rail carts linking the three stages, composition flowing left to right to show progressive refinement, final container small relative to enormous facilities behind it, no bomb parts and no concentration percentages visible, 16:9
```

**Negative prompt**
```text
Little Boy weapon, uranium core, enrichment percentages as text, detailed process flowchart, modern centrifuges, glowing radioactive material, readable facility labels
```

### 1943/11/04 — まずはここで作ってみます

**狙い:** X-10を「研究炉から工業生産への橋渡し」として、黒鉛炉と隣接する化学工程を一枚に入れる。

**Positive prompt**
```text
1943 Oak Ridge X-10 site, blocky graphite reactor building in the foreground with technicians operating simple period instruments, adjacent modest radiochemical processing building and shielded transfer equipment visible across a service yard, small carts moving irradiated material between stages, emphasis on a pilot-scale production chain rather than a single experiment, autumn Tennessee setting, no readable signage, 16:9
```

**Negative prompt**
```text
modern commercial reactor, cooling towers, glowing core, bomb factory poster, exact facility photograph, readable labels, detailed chemical process diagram
```

### 1944/09 — 炉が止まりました。毒です

**狙い:** キセノン毒を「故障した機械」ではなく、出力が落ちた原子炉と追加燃料管の余裕設計で表す。

**Positive prompt**
```text
Hanford B Reactor control area in September 1944, analog instrument needles dropping unexpectedly while engineers study a wall-sized reactor-face representation with many unused generic channel positions still available, one team calmly preparing additional fuel loading equipment, tense diagnostic atmosphere, no visible radiation or explosion, emphasis on unexpected physics being overcome by engineering margin, period control room details, no readable numbers, 16:9
```

**Negative prompt**
```text
reactor meltdown, green gas cloud, poison bottle, exact reactor loading pattern, actionable core diagram, modern control screens, readable gauges
```

### 1944/12/26 — 人が入れないので、工場を遠隔操作します

**狙い:** T Plantを、厚い遮蔽壁越しに巨大セルを操作する「人が近づけない化学工場」として描く。

**Positive prompt**
```text
1944 Hanford chemical-separation plant interior, operators standing safely behind very thick concrete shielding and heavy viewing windows, using long mechanical remote manipulators and analog controls to handle sealed equipment in a distant processing cell, industrial cranes and shielded transfer casks, visual separation between human workspace and inaccessible radioactive process area, sober utilitarian atmosphere, no readable labels, 16:9
```

**Negative prompt**
```text
modern robotic arms, exposed glowing plutonium, worker inside hot cell, bomb components, detailed chemical recipe, exact process schematic, readable controls
```

### 1943–1945 — 頭脳 つかいかた

**狙い:** フォン・ノイマン個人の肖像ではなく、数学・衝撃波・爆薬工学が同じ机へ集まることで兵器化されたことを描く。

**Positive prompt**
```text
1940s Los Alamos interdisciplinary workroom, mathematicians, physicists and explosives engineers gathered around one large table covered with unreadable hydrodynamic plots, mechanical calculators, slide rules and generic shock-wave test photographs, a plain spherical experimental object in the background without internal details, no identifiable celebrity portrait, visual emphasis on abstract calculation becoming engineering decisions, muted sepia and steel blue, 16:9
```

**Negative prompt**
```text
exact von Neumann portrait, weapon cutaway, implosion lens blueprint, detonator layout, readable equations, modern computers, heroic genius poster
```

### 1944/07 — 小さい男の子のようには扱えない

**狙い:** プルトニウム砲身型の断念を、爆弾内部ではなく「長い砲身型案が設計机から外され、別方式へ研究が移る」転換として描く。

**Positive prompt**
```text
July 1944 Los Alamos design office, an elongated generic weapon-shaped engineering mockup resting unused against a wall under a dust cover while the active worktable has shifted to abstract compression-test photographs and a simple featureless spherical test object, engineers discussing with concerned body language, no internal weapon components shown, composition communicates abandonment of one approach and redirection to another, no readable drawings, 16:9
```

**Negative prompt**
```text
detailed gun-type bomb cutaway, plutonium core dimensions, assembly instructions, labeled Thin Man or Little Boy text, operational weapon diagram, modern CAD
```

### 1944–1945 — 球対称なら解けます

**狙い:** 数学・パンチカード計算・衝撃波研究が爆縮工学へ接続されたことを、兵器の精密設計図にせず表す。

**Positive prompt**
```text
1940s Los Alamos calculation room, mathematicians and engineers around IBM punch-card equipment and drafting tables, abstract concentric pressure-wave sketches represented as non-labeled circles on paper, a small generic spherical test assembly in the background without internal weapon details, emphasis on mathematics becoming engineering, desk lamps, punch cards, rulers and mechanical calculators, tense focused atmosphere, muted sepia blue-gray palette, no readable text, 16:9
```

**Negative prompt**
```text
cutaway nuclear weapon, detailed implosion lens geometry, dimensions, wiring diagram, detonator layout, actionable weapon schematic, modern computers, readable equations, readable labels, mushroom cloud
```

### 1944–1945 — 中身は見えないので、透かして見ます

**狙い:** RaLa実験を、放射線源そのものより「破壊される試験体の密度変化を外から測る」診断技術として描く。

**Positive prompt**
```text
1944 Los Alamos outdoor diagnostics experiment, generic non-nuclear spherical compression test assembly at the center of a rugged test stand, shielded radiation source and several external detectors arranged around it, technicians observing from protected instrumentation shelters connected by cables, visual emphasis on measuring internal compression indirectly from outside, no detailed internal geometry, desert mesa background, 16:9
```

**Negative prompt**
```text
weapon cutaway, explosive lens details, radioactive source handling instructions, exact detector geometry, nuclear core, mushroom cloud, readable technical labels
```

### 1943–1945 — 超過荷重です!

**狙い:** 原爆をB-29へ載せるため、機体側まで専用改修が必要だったことを航空工学として描く。

**Positive prompt**
```text
wartime aircraft hangar, modified B-29 bomber raised for maintenance while mechanics reinforce and alter the bomb-bay structure, removed defensive turret components and weight-reduction parts stacked to one side, heavy generic test load on a ground trolley beneath the aircraft without resembling a detailed nuclear weapon, engineers checking landing gear and propellers, practical aviation-engineering atmosphere, no readable nose art, 16:9
```

**Negative prompt**
```text
detailed atomic bomb replica, exact Enola Gay markings, modern aircraft maintenance, jet engines, weapons glamour shot, readable technical drawings
```

### 1944–1945 — カボチャで練習します

**狙い:** Pumpkin bombを原爆そのものと誤認させず、同じ重量・空力特性を持つ訓練用模擬弾として描く。

**Positive prompt**
```text
1944-1945 US airfield training scene, a rounded orange-brown practice bomb shape on a loading trolley beside a B-29, ground crew measuring balance and suspension points while another similar inert practice body lies nearby, emphasis on repeated handling and ballistic training rather than combat, no nuclear markings and no internal details, dusty runway and wartime equipment, no readable text, 16:9
```

**Negative prompt**
```text
Halloween pumpkin face, nuclear core, detailed Fat Man replica, explosion, city target, readable bomb markings, celebratory weapon advertisement
```

### 1944–1945 — 一撃離脱の練習

**狙い:** 投下後155度旋回という異例の退避を、爆発ではなく反復飛行訓練の軌跡として描く。

**Positive prompt**
```text
high-altitude Pacific training flight in 1944-1945, B-29 bomber immediately banking into a very steep escape turn after releasing a generic inert practice bomb far below, another aircraft in the distance repeating the maneuver, broad ocean and island range underneath, subtle curved flight-path cue without numbers or tactical annotations, emphasis on unusual evasive flying rather than attack spectacle, no explosion, 16:9
```

**Negative prompt**
```text
atomic explosion, city below, detailed bombing procedure diagram, readable heading numbers, modern jet bomber, heroic combat poster, targeting UI
```

### 1945/04–08 — 秘密の組み立て（盛大）

**狙い:** 「最高機密」なのに実戦投入には島全体規模の人員・建屋・輸送が必要だった逆説を、テニアンの兵站で見せる。

**Positive prompt**
```text
Tinian airbase in summer 1945, specialized assembly buildings, loading pits, B-29 parking areas, trucks, crates and mixed teams of military personnel and civilian technical specialists spread across a busy tropical base, one large generic covered bomb-shape being moved under tarpaulin with no internal details, broad logistical panorama emphasizing how much infrastructure secrecy still required, no readable unit markings, 16:9
```

**Negative prompt**
```text
detailed nuclear weapon, open bomb internals, exact Enola Gay nose art, modern airbase, tropical vacation imagery, readable classified labels, propaganda poster
```

### 1945/07/16 — 我は死神なり、世界の破壊者なり

**狙い:** トリニティ実験を、後世の回想と混同しない「遠くから爆発を見た人々」の構図にする。

**Positive prompt**
```text
pre-dawn New Mexico desert during the 1945 Trinity test, an enormous intensely bright nuclear fireball rising far beyond the horizon, low desert scrub and test-site silhouettes, a few observers seen only as dark distant figures behind protective positions, dramatic contrast between violet dawn sky and orange-white blast, no city, no victims, awe mixed with dread rather than triumph, no quoted text, 16:9
```

**Negative prompt**
```text
close-up portrait of a famous physicist, quoted lettering, religious scripture as text, city destruction, bodies, gore, celebratory fireworks, fantasy colors, modern vehicles
```

---

## 戦時政治 ― 原爆を使うまで

> この区画は全件手動監査済み。政治家の顔を主役にせず、書簡・会議・報告書・標的選定・命令・記者会見という意思決定の媒体を中心に描く。

### 1939/08/02 — ナチスよりも早く

**狙い:** アインシュタイン＝シラード書簡を「原爆計画開始のボタン」にせず、政府へ危険性を知らせる最初期の働きかけとして描く。

**Positive prompt**
```text
summer 1939 study room on Long Island, two European refugee physicists shown from side and back drafting a formal typed letter at a wooden table, uranium research papers and a map of Central Europe nearby with labels deliberately unreadable, sealed envelope prepared for the White House, quiet urgency rather than prophecy, no exact Einstein portrait and no bomb imagery, period typewriter and desk lamp, 16:9
```

**Negative prompt**
```text
exact Einstein portrait, readable letter text, mushroom cloud, finished atomic bomb, Nazi propaganda symbols dominating frame, modern office, glowing atom icon
```

### 1941/10/09 — 大統領案件になりました

**狙い:** 核研究が研究者の案件から大統領レベルの国家計画へ上がった瞬間を、机上の説明と建設計画で示す。

**Positive prompt**
```text
1941 White House-style executive office meeting, senior civilian science administrator briefing two government leaders across a desk using folders, cost sheets and rolled industrial-construction plans with no readable text, no laboratory equipment in the room, restrained wartime atmosphere, figures shown at medium distance without exact presidential likenesses, emphasis on research becoming a state-level construction decision, 16:9
```

**Negative prompt**
```text
exact Roosevelt portrait, readable MAUD report, dramatic bomb model on desk, modern Situation Room, glowing nuclear symbol, celebratory propaganda
```

### 1943/08/19 — 同盟国にも勝手に使わせません

**狙い:** ケベック協定を、共同開発なのに使用権まで相互拘束する「同盟内の鍵の共有」として描く。

**Positive prompt**
```text
1943 Allied wartime conference room in Quebec, American and British delegations seated on opposite sides of a polished table, a closed agreement folder placed exactly between them beside two plain fountain pens, small neutral national flags present but not dominant, figures viewed from an oblique distance without exact leader portraits, visual emphasis on shared control and mutual consent over a secret project, no readable document text, 16:9
```

**Negative prompt**
```text
exact Roosevelt or Churchill portrait, readable Quebec Agreement, oversized flags, handshake propaganda poster, nuclear explosion, weapon on conference table
```

### 1944/09/18–19 — 日本ではなく、日本人に

**狙い:** “used against the Japanese” の一語を煽情的に可視化せず、首脳間の覚書にその表現が残った事実だけを静かに示す。

**Positive prompt**
```text
private 1944 wartime estate meeting between two Allied leaders shown mostly in silhouette at a small table, one memorandum folder open between them with lines of typed text intentionally blurred and unreadable, a plain map of the Pacific and Japan nearby without targeting marks, quiet confidential atmosphere, visual focus on wording being fixed in a memorandum rather than on civilians or violence, no exact portrait likeness, 16:9
```

**Negative prompt**
```text
readable quoted phrase, racial caricature, Japanese civilian crowd as target, exact Hyde Park memorandum reproduction, atomic explosion, propaganda poster, exact leader portraits
```

### 1945/04/25 — 寝耳に水の大統領

**狙い:** 新大統領が、すでに巨大化した秘密計画を終盤で初めて詳しく知らされる時間差を描く。

**Positive prompt**
```text
April 1945 executive office briefing, newly seated US president viewed from behind at a large desk while the Secretary of War opens a thick highly classified project folder, wall clock and stacks of ordinary wartime paperwork emphasizing that the secret program already exists beyond the room, a small rolled industrial-site plan and expenditure ledger beside the folder, no bomb model, no exact Truman portrait, sober inherited-responsibility mood, 16:9
```

**Negative prompt**
```text
exact Truman portrait, shocked comic expression, readable classified document, atomic bomb on desk, mushroom cloud, modern Oval Office decor
```

### 1945/05–07 — 京都はやめてください

**狙い:** 「文化財を守った美談」だけにせず、標的候補から一都市を外し、別の都市が入る重い選択として描く。

**Positive prompt**
```text
1945 military target-selection room, several aerial city photographs and generic Japanese urban maps spread across a large table, one folder containing imagery of a historic temple city being physically removed from a target stack by a senior official's hand while another unlabeled city folder remains, officers and analysts watching, no city names readable and no targeting reticles, morally weighty administrative decision rather than heroic rescue, 16:9
```

**Negative prompt**
```text
tourist Kyoto postcard, readable city names, red target crosshair over temples, exact target committee documents, cheerful preservation scene, mushroom cloud
```

### 1945/05/31–06/06 — 警告なしで使います

**狙い:** 暫定委員会の勧告を、都市爆撃の絵ではなく「実演案が机から外され、直接使用案が残る」政策判断として描く。

**Positive prompt**
```text
late-May 1945 government committee room, two concept folders on a table: one containing an image of an empty desert demonstration tower and another containing an abstract industrial-city aerial view, officials moving the desert folder aside while retaining the city-target folder, all captions unreadable, restrained formal atmosphere, no civilians shown and no explosion, visual emphasis on policy selection before use, 16:9
```

**Negative prompt**
```text
city being bombed, civilian suffering, readable committee minutes, detailed weapon plan, exact historical meeting photo, triumphal military mood
```

### 1945/06/11 — まず見せるだけでは？

**狙い:** フランク報告を、科学者たちが「実戦使用以外の出口」を文書化した行為として描く。

**Positive prompt**
```text
June 1945 metallurgy laboratory office in Chicago, several scientists gathered around a typed report and a tabletop model of an isolated desert observation site with distant viewing stands, papers about international control stacked nearby, figures shown as working scientists rather than activists at a rally, no exact portraits, no readable report text, visual contrast between empty demonstration landscape and unseen city warfare, 16:9
```

**Negative prompt**
```text
readable Franck Report, protest signs, exact scientist portraits, mushroom cloud over city, propaganda poster, modern conference room
```

### 1945/06/16 — 実演では止まりません

**狙い:** 科学顧問団の結論を「科学者全員が賛成した」絵にせず、意見が割れた末に代替案を出せなかった会議として描く。

**Positive prompt**
```text
June 1945 Los Alamos-style conference room, four senior scientists seated around a table with visibly divided body language, an empty-desert demonstration photograph on one side and a generic military-use folder on the other, neither presented triumphantly, notes and calculations unreadable, no exact portraits, subdued gray-brown palette, visual emphasis on disagreement and lack of an accepted alternative, 16:9
```

**Negative prompt**
```text
four smiling famous scientist portraits, unanimous vote gesture, readable recommendation text, nuclear explosion, celebratory weapon poster, modern meeting room
```

### 1945/07/17 — 使う前に条件を示してください

**狙い:** シラード請願を、署名運動の具体的な紙と研究者の手で示し、後世の抗議集会のようには描かない。

**Positive prompt**
```text
July 1945 wartime research laboratory, scientists quietly passing a formal petition sheet from hand to hand beside workbenches, multiple signature lines visible only as illegible marks, a sealed envelope addressed generically to the executive branch without readable text, laboratory coats and period instruments in background, serious ethical deliberation within the project rather than public protest, no exact scientist portraits, 16:9
```

**Negative prompt**
```text
readable signatures, protest placards, modern anti-nuclear rally, exact Szilard petition reproduction, mushroom cloud, heroic dissident poster
```

### 1945/07/21 — 日本には民間人はいない

**狙い:** カニンガム報告の総力戦的な論理を、民間人の惨状ではなく「地図上で社会全体が軍事目標へ吸収される」情報分析として描く。

**Positive prompt**
```text
July 1945 US military intelligence office, large unlabeled map of the Japanese home islands on a wall surrounded by layers of generic icons for factories, railways, civil-defense groups and military units until civilian and military categories visually overlap, an analyst writing an official report at a desk in foreground, sober bureaucratic atmosphere, no civilians depicted as enemies and no modern political comparison, no readable quotation, 16:9
```

**Negative prompt**
```text
racial caricature, civilians under attack, readable dehumanizing quote, Gaza imagery, contemporary political figures, propaganda poster, nuclear explosion
```

### 1945/07/25 — 8月3日以降、晴れ次第

**狙い:** 原爆使用が理念ではなく、天候条件つきの具体的な航空作戦命令へ変わったことを見せる。

**Positive prompt**
```text
late-July 1945 US Army Air Forces operations room in the Pacific, weather charts with cloud symbols, four unlabeled Japanese city-location pins on a broad map, mission folders and B-29 readiness board, officers comparing forecast windows while a sealed special-mission order lies on the desk, no readable city names or order text, no bomb shown, procedural operational atmosphere, 16:9
```

**Negative prompt**
```text
readable target list, red crosshairs, detailed bombing instructions, nuclear weapon diagram, city destruction, modern weather radar screen
```

### 1945/07/26 — 迅速かつ完全な壊滅

**狙い:** ポツダム宣言を、原爆を明示しない降伏要求文書と、すでに動いている軍事準備の並行として描く。

**Positive prompt**
```text
July 1945 Potsdam setting, formal proclamation sheets being duplicated and transmitted from a wartime communications desk while in the background separate military logistics folders and aircraft schedules remain active, Allied conference-room silhouettes distant and secondary, no nuclear weapon visible because the declaration does not name it, restrained final-warning atmosphere, all document text unreadable, 16:9
```

**Negative prompt**
```text
readable Potsdam Declaration text, mushroom cloud printed on document, exact famous conference photo, victory celebration, propaganda leaflet close-up with legible words
```

### 1945/07/28 — 様子見します → 拒絶します（意訳）

**狙い:** 「黙殺＝単純な誤訳」説へ寄せず、日本政府内の様子見と、記者会見で外へ出た強い言葉のずれをメディア空間で描く。

**Positive prompt**
```text
Tokyo government press room in late July 1945, prime-ministerial press briefing seen from behind reporters and period microphones, officials at a table with closed diplomatic cables and newspapers, one side of the composition suggesting cautious internal waiting through unopened telegram folders while the public-facing microphones dominate the other side, no exact portrait of Suzuki Kantaro, no readable Japanese words, tense ambiguity of message and reception, 16:9
```

**Negative prompt**
```text
readable mokusatsu characters, comic mistranslation joke, exact Suzuki portrait, modern press conference, exaggerated angry gesture, mushroom cloud, propaganda caricature
```

---

## 1945年8月・被爆

### 1945/08/06 — 明日も遊びたかった

**狙い:** 人物を直接再現せず、三輪車という具体物から一人の生活を見せる。

**Positive prompt**
```text
respectful museum-exhibit still life, an original composition showing a small 1940s Japanese child's tricycle scorched and rusted, resting alone on bare earth beside a modest damaged wooden house wall, a tiny child's sandal nearby but no person present, soft late-afternoon light, quiet empty composition, muted brown gray palette with faint warm highlights, emphasis on ordinary childhood interrupted by war, based on the known historical artifact but not a copy of any museum catalog photograph, no readable text, 16:9
```

**Negative prompt**
```text
museum artifact photo, exact recreation of a museum display photo, child corpse, injured child, gore, blood, flames engulfing people, sentimental angel imagery, toy-store brightness, modern bicycle, readable museum label
```

### 1945/08/06 — お弁当食べたかった

**狙い:** 焼けた弁当箱と中身だけで、登校・作業・昼食という日常が途切れたことを示す。

**Positive prompt**
```text
respectful still life of a blackened 1940s Japanese metal lunch box lying on dusty ground, charred traces of a simple vegetable lunch visible inside, a school cap and work glove partly in frame, ruined city textures softly out of focus behind it, morning light filtered through smoke, quiet composition centered on the ordinary meal that was never eaten, muted charcoal brown palette, based on historical artifact knowledge but not on any single official photograph, no readable text, 16:9
```

**Negative prompt**
```text
artifact photo, exact recreation of a museum catalog image, corpse, body parts, gore, blood, graphic burns, abundant modern food, plastic lunch box, bright cute bento, readable name tags
```

### 1945/08/06 — 人影の石

**狙い:** 「人が蒸発して影だけ残った」という誤解を強化せず、熱線で表面差が生じた石段そのものを描く。

**Positive prompt**
```text
close view of broad stone entrance steps in devastated Hiroshima, the stone surface bleached lighter by intense heat with one darker seated human-shaped protected area remaining on a step, damaged masonry and dust around it, no body present, quiet forensic museum-like composition, overcast gray light, historically respectful, based on the known phenomenon and material appearance rather than any direct copy of a specific archival photo, no readable text, 16:9
```

**Negative prompt**
```text
archival artifact photo, exact recreation of a famous museum image, vaporizing person, ghost silhouette standing upright, supernatural shadow, skeleton, corpse, gore, blood, dramatic fireball, readable bank sign, horror art
```

### 1945/08/06 — 水をください

**狙い:** 負傷描写ではなく、水そのものが救護現場の最重要資源になったことを見せる。

**Positive prompt**
```text
improvised 1945 Hiroshima relief station, a dented metal bucket of water and simple ladle in the foreground, several dusty hands reaching carefully toward cups, exhausted medics and evacuees suggested only as soft silhouettes in the background, broken water pipes and smoke beyond, emphasis on thirst, scarcity and emergency care rather than injury, muted gray brown palette, no readable text, 16:9
```

**Negative prompt**
```text
graphic burns, exposed wounds, corpse, gore, blood, screaming close-up faces, abundant clean bottled water, modern medical equipment, readable text
```

### 1945/08/06– — 八面六臂の暁部隊

**狙い:** 軍事輸送用に整備された人員・舟艇・車両が、そのまま救援インフラへ転用されたことを見せる。

**Positive prompt**
```text
Hiroshima waterfront on August 6 1945, Japanese Army shipping-unit soldiers and medics rapidly loading wounded civilians represented respectfully under blankets onto small military boats, trucks and stretchers moving in coordinated directions, Ujina harbor in the background under a smoke-filled sky, strong sense of logistics repurposed for emergency rescue, no heroic posing, muted khaki gray and river blue palette, no readable text, 16:9
```

**Negative prompt**
```text
gore, blood, exposed wounds, corpses, triumphant military propaganda pose, charging soldiers, combat scene, modern rescue vehicles, modern uniforms, readable insignia text
```

### 1945/08/09 — 路面電車は我らの誇り

**狙い:** 焼け跡の中を再び走り始めた路面電車を、復旧する都市機能として描く。

**Positive prompt**
```text
Hiroshima three days after the atomic bombing, a battered 1940s streetcar moving slowly along hastily repaired tracks through a heavily damaged streetscape, utility workers repairing overhead wires, a few civilians waiting quietly, no cheering crowd, morning sunlight breaking through smoke and dust, visual emphasis on restored urban function amid ruins, muted gray with restrained warm light, no readable text, 16:9
```

**Negative prompt**
```text
modern tram, pristine rebuilt city, cheerful tourism poster, gore, bodies, giant mushroom cloud, readable destination sign
```

### 1945/08/09 — 僅かな雲の切れ目から

**狙い:** 長崎投下の偶然性・視界・燃料制約を、「雲の穴」と航空機の構図だけで示す。

**Positive prompt**
```text
high-altitude view above Nagasaki on August 9 1945, a silver B-29 bomber crossing a broad layer of thick summer cloud, one narrow irregular break in the clouds revealing only a small portion of the valley city far below, tense navigational atmosphere, aircraft shown externally with period-correct silhouette but no glorification, soft sunlight above cloud tops and dark shadow below, no explosion yet, no readable text, 16:9
```

**Negative prompt**
```text
modern aircraft, incorrect jet engines, giant open target reticle, readable nose art, bomb cutaway, detailed weapon mechanics, city already exploding, celebratory composition
```

### 1945/08/09 — キリストは再び贄となった

**狙い:** 「燔祭」論をゲーム自身の断定にせず、浦上天主堂の壊滅と宗教共同体の喪失を静かに描く。

**Positive prompt**
```text
ruins of Urakami Cathedral in Nagasaki after the atomic bombing, broken red-brick arches, collapsed masonry, damaged religious statuary partly visible among debris, a church bell and fragments of stained glass in the foreground, no bodies, no supernatural light, solemn Catholic memorial atmosphere without endorsing a theological interpretation, cloudy late-day sky, muted brick red and ash gray palette, no readable text, 16:9
```

**Negative prompt**
```text
crucified living person, divine apparition, angels, miraculous beam of light, gore, corpses, blood, triumphal religious propaganda, intact modern cathedral, readable text
```

### 1945/08/09–11 — 妻はロザリオを残した

**狙い:** 妻の死を人物の再現ではなく、焼け跡から拾われたロザリオという一つの物証へ凝縮する。原子雲・教会・聖母像とは別の、手元の静物構図にする。

**Positive prompt**
```text
close intimate view in the burned ruins of Urakami after the Nagasaki atomic bombing, a wounded Japanese physician's hand carefully lifting a heat-damaged Catholic rosary from gray ash and broken household debris, the rosary beads and small cross as the clear focal point, only fragments of a modest 1940s home in soft background, quiet grief conveyed through objects rather than faces, low eye-level still-life composition, restrained ash gray and dark brown palette, original composition based on the documented event and not on any single museum or archival photograph, no readable text, 16:9
```

**Negative prompt**
```text
exact museum artifact photo, exact recreation of a known rosary photograph, corpse, bones, body parts, graphic burns, blood, religious miracle scene, glowing cross, cathedral altar composition, Madonna statue, mushroom cloud dominating the frame, modern household objects, readable text
```

### 1945/08/09–10/08 — 自分も被爆者ですが、患者を診ます

**狙い:** 永井自身の負傷と救護を同時に見せる。研究机ではなく、臨時救護所を斜めに使った複数人物の現場構図にする。

**Positive prompt**
```text
improvised Nagasaki medical relief station in August 1945, a Japanese physician with a bandaged right side of the head leaning forward to examine a wounded civilian while clearly injured himself, another patient under a blanket and one helper nearby, simple 1940s medical supplies, notebooks and water basin on a rough table, diagonal active composition showing emergency care in a damaged temporary setting, exhausted concentration rather than heroism, respectful distance from injuries, muted khaki gray and brown palette, original historical editorial composition, no readable text, 16:9
```

**Negative prompt**
```text
modern hospital, pristine operating room, graphic wounds, gore, blood, exposed organs, heroic propaganda pose, smiling doctor, modern scrubs, modern monitors, exact portrait recreation, readable medical chart, mushroom cloud as background spectacle
```


### 1945 ～08 — そういえばこの街は空襲がない

**狙い:** 広島が無傷だったことを「幸運」ではなく、通常爆撃から外されていた不気味な平穏として描く。

**Positive prompt**
```text
Hiroshima in the summer of 1945 before August 6, dense wooden neighborhoods, streetcars, military offices and civilians moving through an intact wartime city under a clear morning sky, air-raid shelter entrances and blackout preparations visible but no large-scale fire damage, distant aircraft-watch observers scanning an otherwise empty sky, calm ordinary life with subtle unease, no hindsight mushroom cloud or targeting marks, original wide urban composition, 16:9
```

**Negative prompt**
```text
mushroom cloud, destroyed Hiroshima, red target crosshair, cheerful tourism scene, exact wartime aerial photograph, modern buildings, readable signs
```

### 1945/08/06 — 神よ、我々は何をしたのだ

**狙い:** 後世の口頭回想ではなく、機上で雲を見ながら手書き記録を残した事実へ寄せる。

**Positive prompt**
```text
inside a B-29 cockpit and navigator area shortly after the Hiroshima bombing, one crew member seen in profile writing urgently in a small flight notebook while through a side window a vast rising cloud is visible far behind the aircraft, other crew silhouettes quiet rather than celebratory, instrument panel period-accurate but unreadable, moral shock conveyed through posture and the act of writing, no legible quotation and no exact portrait of Robert Lewis, 16:9
```

**Negative prompt**
```text
readable famous quote, smiling crew, victory pose, exact crew photograph recreation, close detailed bomb mechanics, city casualties, gore, modern cockpit
```

### 1945/08– — 昨日まで元気だったはずだ

**狙い:** 急性放射線症候群を、爆発瞬間ではなく「数日後に症状が現れる時間差」として病床・記録・日用品で見せる。

**Positive prompt**
```text
improvised Hiroshima or Nagasaki medical ward several days after the bombing, a patient who appears externally less injured resting under a simple blanket while a medic checks temperature and a laboratory worker examines a basic blood-count slide nearby, a few loose hair strands on a pillow and small purple marks suggested discreetly on an arm without graphic detail, calendar pages or daylight changes implying passage of days, subdued clinical atmosphere, no gore, 16:9
```

**Negative prompt**
```text
graphic bleeding, corpse, exposed burns, radiation glow, mutation imagery, modern hospital monitors, exact patient portrait, sensational disaster scene
```

### 1945/08/08 — あらかじめ裏切られた条約

**狙い:** 日ソ中立条約の法的評価を画像で断定せず、日本の対ソ仲介期待が宣戦で崩れた外交上の転換を描く。

**Positive prompt**
```text
Tokyo diplomatic office on August 8 1945, an older neutrality-treaty folder and recent diplomatic telegrams laid side by side on a desk, a large unlabeled map showing the Soviet Far East, Manchuria and Sakhalin in the background, Japanese officials receiving an urgent new message while separate folders for mediation talks remain open, atmosphere of a diplomatic assumption collapsing, no readable treaty clauses or accusations, 16:9
```

**Negative prompt**
```text
readable treaty text, caricatured Soviet soldiers, propaganda poster, battlefield gore, modern map graphics, definitive legal verdict written in image
```

### 1945/08/09 — 運命の4分間

**狙い:** 史料上留保のある警報を断定的に再現せず、「11時直前に退避情報が流れたとされる」という短い時間幅をラジオと時計で示す。

**Positive prompt**
```text
late morning August 9 1945 regional Japanese radio studio and household listening scene combined in one composition, analog studio clock hands just before eleven, operator at a wartime microphone and transmitter, in the background a Nagasaki valley household with tabletop radio and people pausing to listen, visual sense of only a few minutes remaining without readable announcement text, historically cautious and non-dramatic, no explosion yet, 16:9
```

**Negative prompt**
```text
readable evacuation announcement, exact 10:58 timestamp as printed text, guaranteed citywide reception, modern radio equipment, countdown timer UI, mushroom cloud
```

### 1945/08/09 — 最後の業火か……？

**狙い:** 「最後の核攻撃都市」という現在までの位置づけを、長崎の爆発自体は遠景に置き、娯楽的スペクタクルにしない。

**Positive prompt**
```text
distant ridge view over Nagasaki valley at 11:02 on August 9 1945, overwhelming white-orange blast cloud rising over the Urakami area while foreground hills and rooftops remain dark silhouettes, cathedral ruins not yet individually detailed, no visible bodies or close suffering, enormous scale conveyed through landscape and distance, somber historical tone rather than spectacle, restrained palette with harsh central light, 16:9
```

**Negative prompt**
```text
celebratory mushroom cloud poster, close-up fireball glamour, bodies, gore, fantasy apocalypse, modern Nagasaki skyline, readable text
```

### 1945/08/09 — 二重の業火を浴びて

**狙い:** 二重被爆を山口彊一人の肖像へ固定せず、広島から長崎へ戻った移動そのものを一枚で示す。

**Positive prompt**
```text
August 1945 Japanese wartime train interior, a bandaged office worker seen from behind traveling with a small briefcase and damaged clothing, through one window the train leaves a devastated western Japanese city and through the forward side of the composition it approaches another city under an ominous summer sky, rail route and station details generic and unlabeled, emphasis on one person carrying the first bombing into the geography of the second, no exact portrait of Tsutomu Yamaguchi, 16:9
```

**Negative prompt**
```text
split-screen two mushroom clouds, exact Yamaguchi portrait, readable tickets or station names, graphic injuries, modern train, heroic survivor poster
```

### 1945/08/11 — 国際法規を無視せる残虐の新型爆弾

**狙い:** 新聞見出しそのものを複製せず、日本政府の対外抗議と国内報道の論調変化を並べる。

**Positive prompt**
```text
Tokyo on August 10-11 1945, Foreign Ministry-style desk with a diplomatic protest cable being prepared for transmission through a neutral embassy, beside it bundles of newspapers with front pages reduced to unreadable black headline bars, telegraph equipment and wartime office staff in background, composition showing the shift from uncertainty about a new bomb toward legal and humanitarian condemnation, no exact newspaper layout or readable quotation, 16:9
```

**Negative prompt**
```text
exact Asahi Shimbun page, readable headline, modern international-law symbols, graphic bombing victims, propaganda caricature, mushroom cloud montage
```

### 1945/08/11 — ぼろぼろで握れない

**狙い:** 江頭千代子の家族の死を、遺体や自決的なショック描写ではなく「鍋へ納めようとして崩れる焼骨」という物と手の距離で記録する。

**Positive prompt**
```text
quiet burned residential ruins in Nagasaki two days after the bombing, a dented household cooking pot placed on ash-covered ground while an adult woman's hands carefully try to gather small pale calcined bone fragments that crumble into ash, only hands and sleeves visible, no bodies or identifiable remains beyond fragmentary material, intimate respectful close composition centered on the impossibility of collecting family remains, muted gray-brown palette, 16:9
```

**Negative prompt**
```text
corpse, skeleton, skull, graphic human remains, gore, blood, close-up crying face, horror imagery, exact reenactment photograph, sentimental supernatural effects
```

### 1945/08/15 — 100万の兵を救った……？

**狙い:** 「100万人」を確定した数字として描かず、本土侵攻計画と複数の損害見積もりが戦後一つの物語へ圧縮されたことを示す。

**Positive prompt**
```text
postwar historical-analysis desk, Operation Downfall-style invasion maps of southern and central Japan shown generically alongside several separate casualty-estimate memoranda with visibly different bar lengths and ranges but no readable numbers, a newspaper clipping stack and later speech notes in the background, historian's hands comparing sources rather than selecting one figure, neutral documentary-editorial atmosphere, no battle scene, 16:9
```

**Negative prompt**
```text
large readable one-million number, definitive casualty counter, propaganda poster proving or disproving the bombing, graphic invasion combat, exact classified documents, political campaign imagery
```

### 1945/08/20 — みなさん、これが最後です

**狙い:** 真岡郵便電信局の女性交換手の死を、自決手段ではなく「終戦後も続く戦闘の中で途切れた通信」として描く。

**Positive prompt**
```text
August 20 1945 telephone exchange room in southern Sakhalin, long manual switchboard with many cords and small indicator lamps, several young female operators in period work clothes at their stations while distant smoke and battle light are visible through high windows, one final line lamp glowing as empty chairs and dropped headsets suggest communication ending, solemn restrained composition, no depiction of suicide method or bodies, no readable message, 16:9
```

**Negative prompt**
```text
suicide method, poison, bodies, gore, romanticized self-sacrifice, readable final words, anime schoolgirls, modern call center, propaganda poster
```

### 1945/09/27 — わたしはどうなってもいい

**狙い:** 有名なマッカーサーとの立ち写真を再現せず、会見そのものと、後年の回想録・日本側記録の差を一枚にする。

**Positive prompt**
```text
September 1945 occupation-era meeting room in Tokyo, Japanese emperor and American supreme commander shown seated at a table in distant non-identifying profile rather than the famous standing photograph pose, an aide's contemporaneous meeting notes on one side and a later memoir volume on the other with all text unreadable, visual emphasis on the meeting and differing documentary records, restrained diplomatic atmosphere, no exact facial likeness, 16:9
```

**Negative prompt**
```text
exact famous MacArthur-Hirohito standing photo, exact portraits, readable quotation, propaganda comparison of height, caricature, modern room, triumphal occupation imagery
```

---

## 復興・被爆後・記憶継承

> この区画は全件手動監査済み。ただし既存作品そのものや現存著作権の彫刻を主役にするカードは別途「生成除外」とし、ここには安全な独自構図が成立するカードだけを置く。

### 1945– — うつるわけなかろうが

**狙い:** 被爆者差別を「病気の見た目」で描かず、医学的には感染しないのに人間関係で距離を置かれる社会的被害として描く。

**Positive prompt**
```text
postwar Japanese clinic consultation in the late 1940s or 1950s, a physician calmly explaining radiation effects to a young couple and family members seated with visible social distance, simple medical chart represented only by abstract body outlines and non-readable marks, no one shown as contagious or visibly monstrous, restrained everyday setting emphasizing stigma caused by misunderstanding rather than disease transmission, no readable text, 16:9
```

**Negative prompt**
```text
infection cloud, contagious radiation aura, mutation, deformed children, horror imagery, shaming caricature, readable medical poster, modern clinic
```

### 1947/12/07 — この犠牲を無駄にすることなく

**狙い:** 昭和天皇の広島巡幸を、肖像の再現よりも「占領下の大群衆へ向けた慰問と平和再建の言葉」の場として描く。

**Positive prompt**
```text
Hiroshima civic square in December 1947, a large crowd of citizens gathered in winter clothing facing a simple raised platform where the Japanese emperor appears only as a small distant figure speaking into a period microphone, damaged and rebuilding city blocks around the square, occupation-era atmosphere, no close facial likeness, visual emphasis on public address amid reconstruction, no readable banners or quotation, 16:9
```

**Negative prompt**
```text
exact emperor portrait, imperial propaganda poster, wartime military parade, readable speech text, modern Hiroshima skyline, celebratory nationalist imagery
```

### 1949 — 鯉は焼け跡から泳ぎ出す

**狙い:** 広島カープ誕生をロゴや選手肖像ではなく、市民募金と小さな球場の日常復興として描く。

**Positive prompt**
```text
Hiroshima around 1949-1950, modest postwar baseball ground with simple wooden stands and players in plain logo-free uniforms practicing in the distance, local residents dropping coins into a large donation barrel near the entrance, rebuilt shops and lingering vacant lots beyond the field, lively but humble civic atmosphere, baseball as ordinary life returning after destruction, no team logo or readable signage, 16:9
```

**Negative prompt**
```text
Hiroshima Carp logo, identifiable player portrait, modern stadium, branded merchandise, readable scoreboard, mascot, glossy sports advertisement
```

### 1954/03/01 — 三度目の悲劇

**狙い:** 第五福竜丸と放射性降下物を、爆心そのものではなく「遠く離れた漁船まで届いた核実験」として見せる。

**Positive prompt**
```text
1954 Japanese tuna fishing boat at sea near the Marshall Islands, the fishing vessel represented as a modest wooden working boat beneath an uncanny bright distant horizon, fine pale fallout dust settling across deck ropes and nets like ash, crew members shown only as small concerned silhouettes, tropical ocean otherwise calm, contrast between ordinary fishing work and invisible radiological danger, no readable hull name, 16:9
```

**Negative prompt**
```text
close-up radiation burns, gore, blood, famous monster character, fantasy green radiation glow, modern fishing vessel, readable hull text, exact news photograph
```

### 1955/10/25 — 生き延びてなお

**狙い:** 佐々木禎子を有名写真の似顔絵にせず、幼児期被爆から9年後の白血病へ続いた時間を病室の折り鶴で示す。

**Positive prompt**
```text
1955 Japanese hospital room, school-age girl's hands folding a small paper crane on a blanket-covered bed, several completed cranes hanging nearby, a simple bedside blood-test tray and school notebook suggesting illness interrupting childhood, face outside the frame or softly obscured, quiet daylight and restrained sorrow, no claim that exactly one thousand cranes were completed, no readable notes, 16:9
```

**Negative prompt**
```text
exact Sadako portrait, angel imagery, miraculous cure scene, graphic leukemia symptoms, hospital gore, anime child, readable medical chart
```

### 1958/05/05 — 千羽鶴の祈り

**狙い:** 現存彫刻の精密再現を避け、子どもたちの募金運動と折り鶴が公共の記憶へ変わったことを主役にする。

**Positive prompt**
```text
Hiroshima Peace Memorial Park in the late 1950s, groups of schoolchildren quietly hanging long strings of colorful origami cranes at a memorial area, donation envelopes and handmade crane bundles in the foreground, the Children's Peace Monument present only as a distant softly simplified silhouette without detailed sculptural reproduction, open sky and young park trees, hopeful but solemn civic memory scene, no readable plaques, 16:9
```

**Negative prompt**
```text
exact sculpture reproduction, close detailed copyrighted statue, tourist-photo recreation, kawaii mascot style, excessive rainbow saturation, readable inscriptions, modern smartphones
```

### 1959 — そして罪は償われた……？

**狙い:** 浦上天主堂再建を「復元してめでたし」で終わらせず、礼拝の再建と遺構保存の緊張を新旧二つの建築断片で描く。

**Positive prompt**
```text
Nagasaki in 1959, newly rebuilt Urakami Cathedral rising in the background while a surviving fragment of the bombed old cathedral masonry stands separately in the foreground, parishioners walking toward worship and preservation workers examining the ruin fragment, balanced composition showing living religious reconstruction beside retained evidence of destruction, no miraculous lighting, no exact postcard view, no readable signs, 16:9
```

**Negative prompt**
```text
perfect before-and-after split screen, supernatural glow, exact modern tourist photograph, bodies, gore, readable church signs, triumphal religious poster
```

### 1960年代～ — 夏なのになんで長袖？

**狙い:** ケロイドをショック描写にせず、暑い季節に傷を隠す日常の自己防衛と周囲の視線として描く。

**Positive prompt**
```text
1960s Japanese summer street or tram stop, an anonymous hibakusha wearing a long-sleeved shirt despite the heat while nearby people wear short sleeves, one cuff adjusted carefully so only a small non-graphic scar edge is barely visible, ordinary shopping bags and bright summer light, emotional emphasis on self-conscious social exposure rather than injury, face non-identifying, 16:9
```

**Negative prompt**
```text
graphic keloid close-up, medical freak-show framing, staring crowd caricature, exposed burns, gore, fetishized scars, modern fashion
```

### 1964/08/01 — この火が消えるその日まで

**狙い:** 現存する記念施設の意匠を精密複製せず、「核兵器がなくなるまで消さない火」という未完了状態を火そのもの中心で描く。

**Positive prompt**
```text
Hiroshima Peace Memorial Park at dusk in the mid-1960s, a steady memorial flame filling the foreground with only a simplified low stone support partly visible, the Atomic Bomb Dome far in the distance along the park axis, sparse visitors as small silhouettes, deep blue evening and warm flame as the sole strong color, contemplative unresolved mood, original viewpoint not matching a standard tourist photograph, no readable inscriptions, 16:9
```

**Negative prompt**
```text
exact architectural reproduction of memorial base, tourist postcard, fireworks, festival crowd, giant fantasy flame, city fire, readable monument text
```

### 1975 — 赤ヘル軍団爆誕

**狙い:** 球団ロゴを使わず、赤い帽子と街全体の初優勝祝賀で「惨事だけではない広島の戦後」を描く。

**Positive prompt**
```text
Hiroshima city in autumn 1975, jubilant but period-accurate baseball supporters wearing plain bright red caps with no logos, transistor radios and newspapers held up with text blurred, streetcars and postwar shopping streets in the background, celebratory civic crowd centered on an ordinary sports victory rather than war memory, warm documentary-editorial tone, no identifiable player portraits, 16:9
```

**Negative prompt**
```text
team logo, copyrighted mascot, branded jersey, readable newspaper headline, modern stadium, exact player likeness, commercial sports poster
```

### 1976/10 — 5ドルで見れる人類史の再現

**狙い:** 原爆投下再現ショーの不穏さを、観客の娯楽空間とB-29・地上爆薬の演出の落差で描く。

**Positive prompt**
```text
1976 Texas air show viewed from behind a paying crowd in casual period clothing, a B-29 passing overhead while a staged ground pyrotechnic blast creates an intentionally theatrical mushroom-shaped smoke effect far across the field, ticket booth and folding chairs in foreground with prices unreadable, unsettling contrast between family entertainment setting and reenactment of atomic bombing, no exact aircraft markings or identifiable pilot portrait, 16:9
```

**Negative prompt**
```text
actual nuclear explosion, exact FIFI markings, exact Paul Tibbets portrait, readable ticket price, cheerful fireworks mood, victims, gore, modern air show
```

### 1982/06/24 — ノーモアヒロシマ

**狙い:** 被爆地の訴えが自治体ネットワークへ制度化される起点を、国際会議と都市間の連結で見せる。

**Positive prompt**
```text
1982 international disarmament assembly hall, mayor of a Japanese city speaking at a podium seen from a distance with no exact facial likeness, delegates from many cities listening, behind the speaker an abstract globe graphic with small city lights connected by thin lines but no logos or readable place names, restrained institutional atmosphere, emphasis on municipal international networking rather than one politician, 16:9
```

**Negative prompt**
```text
exact UN emblem, readable speech, campaign poster, giant national flags, exact Araki Takeshi portrait, nuclear explosion
```

### 1984/05/25 — やめたあとならいけます

**狙い:** 現職ではなく「元大統領」として初めて広島を訪れた制度的距離を、献花と空いた公的席で表す。

**Positive prompt**
```text
Hiroshima Peace Memorial Park in 1984, an older former American president shown from behind placing a wreath at the cenotaph accompanied by a small civilian delegation, no active presidential motorcade or military ceremony, quiet visitors and museum buildings in background, visual emphasis on a private post-presidential visit rather than official state apology, no exact Jimmy Carter portrait, no readable inscriptions, 16:9
```

**Negative prompt**
```text
exact Carter portrait, presidential seal, official apology text, campaign imagery, modern security convoy, tourist postcard composition
```

### 1985/09/06 — もう子どもらに、こんな目にあってほしくないけぇ

**狙い:** 三輪車が私的な埋葬品から公共資料へ移る転換を、庭の掘り出しと引き渡しで描く。

**Positive prompt**
```text
Hiroshima family garden in 1985, elderly father's hands and museum staff carefully lifting a small rusted scorched child's tricycle from earth beside a simple excavation area, a covered container for reburial of remains kept respectfully separate and not shown open, composition focused on the object moving from private family memory toward public preservation, no exact portrait, no museum display recreation, 16:9
```

**Negative prompt**
```text
human remains, bones, corpse, gore, exact artifact photograph, smiling donation ceremony, toy-store brightness, readable museum labels
```

### 1995 — 展示することすら戦争

**狙い:** スミソニアン論争を「どちらが正しい展示か」と決めず、展示脚本そのものが政治的争点になったことを描く。

**Positive prompt**
```text
mid-1990s museum preparation warehouse, a large silver B-29 fuselage section partly visible behind scaffolding while curators, historians and veterans' representatives examine multiple exhibition-panel drafts covered with red editorial marks and sticky notes, some panels removed or boxed, all text unreadable, tense institutional negotiation rather than street protest, no exact Enola Gay markings, balanced composition with no side visually triumphant, 16:9
```

**Negative prompt**
```text
readable exhibit script, exact Smithsonian display photograph, partisan protest poster, nationalistic victory imagery, graphic Hiroshima victim photos, exact Enola Gay nose art
```

### 1996/12/05 — あの日ドームの上で

**狙い:** 原爆ドームが「勝手に残った廃墟」ではなく、保存運動と国際登録によって維持されたことを修復・審議で見せる。

**Positive prompt**
```text
Hiroshima Atomic Bomb Dome in the mid-1990s viewed from across the river, discreet conservation scaffolding and structural inspection equipment around parts of the ruin, in the foreground preservation documents and a generic international heritage committee folder with no emblem or readable text, citizens observing from the riverbank, composition linking physical conservation with international recognition, no standard postcard angle, 16:9
```

**Negative prompt**
```text
UNESCO logo, readable heritage certificate, exact tourist photograph, pristine reconstructed dome, mushroom cloud, celebratory travel poster
```

### 2005/06 — Remember Pearl Harbor!

**狙い:** 被爆者と原爆開発側の認識の隔たりを、発言テロップではなく対話の距離と姿勢で見せる。

**Positive prompt**
```text
2005 Hiroshima meeting room, an elderly American former nuclear-laboratory director seated across a small table from two elderly Japanese hibakusha, interpreter or aide nearby, all faces shown at respectful non-identifying distance, tense body language and long pause between speakers, peace-park window view in background, no readable quotation or Pearl Harbor imagery, original documentary-editorial composition, 16:9
```

**Negative prompt**
```text
readable quote, shouting match, exact Harold Agnew portrait, exact survivor portraits, Pearl Harbor attack montage, propaganda poster, caricature
```

### 2005/06 — その前にガス欠になると思うよ

**狙い:** アグニューの乾いた皮肉を文字で出さず、「核廃絶まで燃やす火」とそれを見る訪問者の温度差で表す。

**Positive prompt**
```text
2005 Hiroshima Peace Memorial Park, memorial flame in foreground while an elderly American visitor and local guide stand to one side, the guide gesturing toward the flame and the visitor reacting with a dry understated expression, faces not exact likenesses, no speech bubbles, dusk light and quiet park setting, irony carried only by composition rather than text, 16:9
```

**Negative prompt**
```text
speech bubble, readable joke, exact Harold Agnew portrait, gasoline can, literal empty fuel tank, slapstick comedy, tourist postcard
```

### 2016/05/27 — 謝罪はできないけれども

**狙い:** オバマ広島訪問を謝罪の有無で単純化せず、現職米大統領の献花と被爆者との対面という象徴行為を描く。

**Positive prompt**
```text
Hiroshima Peace Memorial Park in May 2016, sitting US president shown from behind and at medium distance placing a wreath at the cenotaph, elderly hibakusha waiting nearby for a later conversation, Atomic Bomb Dome faintly visible beyond trees, formal but subdued state-visit atmosphere, no exact Barack Obama facial likeness, no apology text or campaign imagery, 16:9
```

**Negative prompt**
```text
exact Obama portrait, readable speech, apology banner, campaign poster, giant American flag, partisan triumph, tourist-photo recreation
```

### 2023/05/19 — 広島に来て見んさい

**狙い:** G7首脳の資料館訪問と、核抑止を残す政策が同じ場に存在したことを、顔ではなく集団の動線で描く。

**Positive prompt**
```text
Hiroshima Peace Memorial Park during the 2023 G7 summit, a group of several national leaders in dark suits seen mostly from behind walking together from the museum area toward the cenotaph, wreaths and security present but understated, no individual face emphasized, distant Atomic Bomb Dome and museum architecture establishing place, solemn collective visit with unresolved policy tension rather than celebration, no readable summit branding, 16:9
```

**Negative prompt**
```text
exact current leader portraits, campaign imagery, readable G7 logo, victory pose, giant flags, partisan caricature, tourist selfie scene
```

### 2024/10/11 — 遅すぎた名誉

**狙い:** 日本被団協の平和賞を「栄光の受賞式」だけにせず、長年の証言活動の末に届いた遅い公的評価として描く。

**Positive prompt**
```text
formal 2024 peace-prize ceremony atmosphere, elderly Japanese hibakusha organization representatives seated together beneath soft stage lighting while a simple medal and certificate rest on a table in the foreground with all design details and text obscured, behind them faint projected silhouettes of decades of testimony meetings rather than graphic bombing images, dignified restrained mood emphasizing long passage of time, no exact Nobel medal reproduction or logo, 16:9
```

**Negative prompt**
```text
exact Nobel medal design, Nobel logo, readable certificate, celebrity red-carpet scene, triumphant confetti, exact survivor portraits
```

### 2026/08 — 最後の近距離被爆者

**狙い:** 「最後の一人」を死亡カウントのように扱わず、地下室で生き延びた場所を次世代へ語る現場として描く。

**Positive prompt**
```text
2026 visit to an old Hiroshima elementary-school basement, a very elderly male survivor shown from behind or side speaking to a small group of schoolchildren beside heavy masonry stairs, simple archival photographs held by a teacher but too small to identify, modern safety lighting carefully separated from preserved wartime structure, quiet intergenerational testimony scene, no exact facial likeness and no medical spectacle, 16:9
```

**Negative prompt**
```text
exact survivor portrait, medical close-up, chromosome graphics, dead child reenactment, sensational last-man headline, readable school displays
```

### 2026/08/06 — 今日は静かにする日なんじゃい

**狙い:** 「被爆者対活動家」の単純図式を作らず、追悼の静けさを求める人と抗議を続ける人が同じ公園にいる摩擦そのものを描く。

**Positive prompt**
```text
Hiroshima Peace Memorial Park on August 6 2026, quiet mourners with flowers and bowed heads occupying the central memorial space while a separate small anti-war protest group with blank unreadable placards stands at the edge beyond a low police or staff boundary, older and younger participants visible on both sides, no one caricatured or violent, early-morning memorial atmosphere with social tension conveyed by distance and body language, 16:9
```

**Negative prompt**
```text
readable political slogans, partisan symbols, violent clash, villainous protesters, saintly mourners, exact identifiable activists, propaganda poster
```

### 1948/08/09 — ノーモア・ナガサキ

**狙い:** 標語そのものを画像内に書かず、被爆地が早い段階から世界へ平和宣言を発した公共行為として描く。

**Positive prompt**
```text
Nagasaki peace ceremony in August 1948, local mayor or civic representative reading from a formal declaration at a simple outdoor podium before survivors and citizens, ruined and rebuilding Urakami landscape in the distance, international correspondence envelopes and radio microphone nearby suggesting a message sent beyond the city, no exact official portrait or readable slogan, restrained postwar atmosphere, 16:9
```

**Negative prompt**
```text
readable No More Nagasaki text, modern peace park, exact mayor portrait, campaign rally, giant banners, nuclear explosion
```

### 1949/06 — 長崎の鐘

**狙い:** 歌詞・レコードジャケットを再現せず、浦上の鐘の記憶がラジオと歌謡曲を通じ全国へ届く経路を描く。

**Positive prompt**
```text
1949 Japanese radio recording studio, period microphone and orchestra silhouettes in foreground while through a visual dissolve a damaged but surviving church bell and postwar Nagasaki hillside appear in the background, shellac record spinning on a turntable with blank label, emotional but restrained popular-culture scene, no singer portrait, no lyrics and no cover-art reproduction, 16:9
```

**Negative prompt**
```text
readable song lyrics, exact record label, exact Fujiyama Ichiro portrait, album cover, modern recording studio, supernatural church glow
```

### 1949/07–08 — 焼け跡を文化都市に

**狙い:** 復興理念をスローガンではなく、住民投票・都市計画・焼け跡の再建が制度で接続された場面として描く。

**Positive prompt**
```text
Nagasaki in 1949, civic planning office overlooking partially rebuilt city blocks, residents placing ballots into a simple box in foreground while planners compare street and public-building plans with bomb-damaged district maps, all text and ballot markings unreadable, cranes and reconstruction visible through windows, optimistic but practical institutional rebuilding atmosphere, 16:9
```

**Negative prompt**
```text
readable law title, political campaign poster, exact ballot paper, futuristic city plan, pristine rebuilt skyline, national propaganda
```

### 1953/05–06 — 治療は無料で

**狙い:** 無料診療事業を、制度名より「8年後も診療を必要とする被爆者と地域医療」の継続として描く。

**Positive prompt**
```text
1953 Nagasaki public clinic, modest waiting room with adult and elderly hibakusha patients in ordinary clothing, doctors and nurses performing blood tests and examinations at simple period desks, payment counter visibly inactive or waived without readable signage, atmosphere of practical community medicine years after the bombing, no graphic illness and no exact patient portraits, 16:9
```

**Negative prompt**
```text
charity propaganda, modern hospital, cash handout scene, graphic disease symptoms, readable medical forms, exact archival clinic photograph
```

### 1964 — 原爆は一日で終わらない

**狙い:** 後障害研究施設を、爆発の記録ではなく長期追跡の医学研究へ時間軸を伸ばす装置として描く。

**Positive prompt**
```text
1964 Nagasaki university medical research room, shelves of anonymized long-term patient files, microscope slides, blood samples and analog laboratory instruments, researchers comparing records spanning many years on a timeline chart with no readable names or numbers, hospital corridor and older survivors faintly visible beyond, emphasis on decades-long follow-up rather than acute disaster, 16:9
```

**Negative prompt**
```text
graphic cancer imagery, mutation, glowing radiation, modern genomics lab, readable patient names, exact institution logo, mushroom cloud
```

### 1975 — 聖母の帰還

**狙い:** 被爆マリアが長崎へ戻ることを、現存像の精密複製ではなく、損傷した宗教物が共同体へ返される行為として描く。

**Positive prompt**
```text
1975 Nagasaki Catholic community interior, a small damaged scorched Marian statue head carried carefully inside a plain protective box by clergy and parishioners, the object seen only partially and from an oblique distance to avoid exact sculptural reproduction, rebuilt Urakami church architecture suggested behind, homecoming and stewardship rather than miracle imagery, no readable plaques, 16:9
```

**Negative prompt**
```text
exact statue reproduction, museum catalog photo, pristine Virgin Mary statue, supernatural halo, miracle rays, readable religious text
```

### 1990 — 毎日毎日が8月9日の様な気がするのです

**狙い:** 江頭千代子の証言を1945年の惨状再演ではなく、45年後も現在形で語り続けるインタビューとして描く。

**Positive prompt**
```text
1990 Japanese television interview in a modest Nagasaki home, elderly woman survivor seated at a table speaking toward an interviewer and analog tape recorder, several family photographs placed face-down or softly blurred beside her, window light falling on ordinary household objects, emotional weight conveyed through age, silence and memory rather than flashback gore, no exact portrait and no readable quotation, 16:9
```

**Negative prompt**
```text
graphic bombing flashback, bones, corpses, exact survivor portrait, readable subtitles, melodramatic crying close-up, modern camera gear
```

### 1996/04/01 — 五十年後の資料館

**狙い:** 新資料館を建物写真だけにせず、個人の体験を保存・収集・常設展示へ移す制度として描く。

**Positive prompt**
```text
1996 Nagasaki atomic-bomb museum archive and exhibition preparation area, conservators placing damaged everyday objects into neutral cases while archivists catalog photographs and testimony tapes, visitors entering a subdued exhibition corridor in background, architecture present but not copied from a standard exterior photograph, visual emphasis on memory becoming institutional preservation, no readable labels or graphic victim photos, 16:9
```

**Negative prompt**
```text
exact museum promotional photo, readable exhibition text, graphic casualty photographs, tourist crowd selfie, museum logo, glossy attraction poster
```

### 2019/11/24 — 持っているだけなら平和ですか

**狙い:** 教皇の長崎演説を肖像礼賛にせず、爆心地で核保有・抑止そのものを倫理的に問う宗教的発言の場として描く。

**Positive prompt**
```text
rainy Nagasaki hypocenter memorial gathering in November 2019, white-robed Catholic pontiff shown from behind at a simple podium beneath an umbrella, hibakusha and citizens listening quietly, wet stone memorial landscape and distant Urakami context, no close facial likeness, no readable speech or church branding, solemn ethical-address atmosphere rather than political rally, 16:9
```

**Negative prompt**
```text
exact Pope Francis portrait, readable anti-nuclear slogan, Vatican logo dominating frame, campaign rally, nuclear explosion, saintly supernatural glow
```

### 2024– — どこからが被爆者ですか

**狙い:** 認定範囲の争いを、被爆者同士の対立ではなく「行政地図の境界線が救済の有無を分ける」制度問題として描く。

**Positive prompt**
```text
modern Nagasaki public-service consultation room, elderly applicants seated with health documents while an official examines a large simplified map showing several concentric or irregular eligibility zones with no readable place names, one household located just outside a boundary line highlighted only by position, medical certificates and appeal folders on the desk, neutral institutional tone emphasizing administrative borders and lived exposure, 16:9
```

**Negative prompt**
```text
exact government eligibility map, readable legal text, partisan protest poster, dismissive bureaucrat caricature, graphic radiation effects, modern political campaign imagery
```

---

## 張本勲 ― 忘れたい日から、伝える日へ

> この区画は全件手動監査済み。著名選手のスポーツ肖像ではなく、被爆記憶との距離が変化していく個人史を主役にする。

### 1945/08 — 一番好きだった姉さん

**狙い:** 姉の死を負傷描写で消費せず、幼い弟が「姉を待つ家」に戻ってきた時間として描く。

**Positive prompt**
```text
Hiroshima family home in August 1945 after the bombing, a five-year-old boy seen from behind sitting near the doorway while an older sister's folded summer clothing and simple hair ribbon rest beside a futon in a darkened room, damaged neighborhood visible outside, adults moving quietly in background, grief conveyed through absence and household objects rather than burns or death scene, no exact portrait of Isao Harimoto or his sister, 16:9
```

**Negative prompt**
```text
graphic burns, dying child, corpse, gore, exact family portrait, baseball imagery, sentimental angel scene, readable name tags
```

### 1959–1981頃 — ひょっとしたら、原爆症じゃないか

**狙い:** 現役選手として成功していても、体調不良のたびに原爆症を疑う長期不安が消えなかったことを描く。

**Positive prompt**
```text
1960s-1970s Japanese professional baseball clubhouse medical-check room, an anonymous star player in plain logo-free uniform sitting tensely while a doctor reviews annual examination results and listens to his chest, baseball glove and bat set aside in shadow, successful athletic career contrasted with private fear of delayed radiation illness, no exact Harimoto facial likeness, no readable team branding or medical results, 16:9
```

**Negative prompt**
```text
team logos, exact Harimoto portrait, triumphant baseball poster, cancer visualization, mutation, modern sports medicine equipment, readable diagnosis
```

### ～2006（要検証） — そこに行けない

**狙い:** 資料館へ入れないことを臆病さとして描かず、入口の先にある記憶へ踏み込めない距離として表す。

**Positive prompt**
```text
Hiroshima Peace Memorial Museum entrance in an unspecified pre-2007 period, older Japanese man seen from behind standing several steps away from the doorway while ordinary visitors enter, his posture stopped and slightly turned away, peace park trees and museum exterior kept secondary, emotional distance conveyed without dramatic tears, no exact portrait and no claim about a precise year, no readable museum signage, 16:9
```

**Negative prompt**
```text
exact Harimoto portrait, cowardice caricature, dramatic breakdown, readable museum sign, exact tourist photograph, baseball branding
```

### 2006/10 — 5日の次は7日でいい

**狙い:** 「8月6日を消したい」という感情を文字のカレンダーギャグにせず、記念日から目を背ける私的な時間として描く。

**Positive prompt**
```text
quiet 2006 Japanese home interior, elderly former athlete sitting alone near a wall calendar turned partly away, the early-August page visible only as blurred boxes with no readable numerals, television coverage of memorial candles softly out of focus in another room, hands clasped and gaze averted, composition centered on wanting distance from an anniversary everyone else asks him to remember, no exact portrait, 16:9
```

**Negative prompt**
```text
readable calendar joke, crossed-out August 6 text, exact Harimoto portrait, comic expression, baseball trophy display dominating frame, political slogan
```

### 2006–2007 — 忘れちゃだめです

**狙い:** 記憶継承が「被爆者→子ども」の一方向ではなく、一通の子どもの手紙が体験者を動かした反転として描く。

**Positive prompt**
```text
mid-2000s desk scene, an elderly man's hands holding a handwritten letter from an elementary-school child with all writing intentionally unreadable, beside it a simple school-trip brochure with museum imagery blurred, unopened personal memory box and old photographs nearby, warm but restrained light, visual emphasis on a younger generation prompting an older survivor to confront memory, no exact portrait or letter reproduction, 16:9
```

**Negative prompt**
```text
readable child's letter, exact handwriting reproduction, sentimental heart graphics, anime child, exact Harimoto portrait, baseball logos
```

### 2007/04（要検証） — 今度は、私が伝える番だ

**狙い:** 初入館年に留保を残しつつ、資料館展示を見ることが「語る側へ回る」転換点になったことを描く。

**Positive prompt**
```text
mid-2000s Hiroshima Peace Memorial Museum gallery, elderly former athlete shown from behind slowly viewing a display case containing a small scorched child's tricycle and other ordinary artifacts, museum labels unreadable and objects shown from an original non-catalog angle, one school group visible farther down the gallery, emotional transition from private avoidance toward public testimony, no exact portrait and no precise date signage, 16:9
```

**Negative prompt**
```text
exact museum display photograph, exact Harimoto portrait, readable labels, crying close-up, sports memorabilia, graphic victim photographs
```

### 2014 — 姉さんを思い出すね…

**狙い:** ケロイド写真そのものを再生成せず、展示を見た張本の記憶が姉へ直結する瞬間を観覧者側から描く。

**Positive prompt**
```text
2014 Hiroshima museum gallery, elderly Japanese man viewed from behind standing before a softly obscured historical medical-photo panel that is deliberately not reproduced in detail, his hand resting on the rail while a small old family photograph of an older sister is held low in the other hand, quiet connection between public evidence and private memory, no exact Harimoto portrait, no readable exhibit text or graphic wound detail, 16:9
```

**Negative prompt**
```text
reproduction of keloid photograph, graphic scar close-up, exact Harimoto portrait, readable museum text, melodramatic crying, baseball branding
```

### 2016/05/29 — 朽ち果てるまで許すことはできない

**狙い:** オバマ訪問への一被爆者の強い怒りを、被爆者全体の総意にはせず、テレビ番組で語る個人の立場として描く。

**Positive prompt**
```text
2016 Japanese television studio, elderly former baseball player shown in non-identifying three-quarter silhouette speaking firmly across a desk while a monitor behind shows only a blurred generic image of the Hiroshima memorial visit, studio host listening without confrontation, sober discussion atmosphere, no readable captions and no implication that all hibakusha share the same view, no exact portraits, 16:9
```

**Negative prompt**
```text
exact Harimoto portrait, exact Obama portrait, shouting match, readable political captions, partisan propaganda, baseball show graphics
```

### 2026/09/05 — その身朽ち果てようとも

**狙い:** 最晩年の核廃絶発言を英雄的遺言にしすぎず、電話取材で自分の経験を最後まで語った静かな終点として描く。

**Positive prompt**
```text
September 2026 quiet home interior, very elderly former athlete seated beside a telephone during a press interview, old baseball glove and an unobtrusive Hiroshima remembrance item resting separately on a shelf, notebook held by an unseen reporter implied through the call, late-afternoon light and physically frail but composed posture, no exact facial likeness, no readable quote or newspaper branding, 16:9
```

**Negative prompt**
```text
deathbed scene, corpse, exact Harimoto portrait, heroic halo, readable anti-nuclear slogan, team logos, sensational obituary design
```

---

## 永井隆 ― 個人史

### 1934/06–08 — 科学者、パウロになる

**狙い:** 「科学か信仰か」の二択にせず、放射線医学の研究者が洗礼と結婚を通じてカトリック共同体へ入る二重の生活を描く。

**Positive prompt**
```text
Nagasaki in 1934, modest Catholic church interior and adjacent medical-study desk joined in one balanced composition, young Japanese physician seen from behind placing a simple baptismal candle near a font while radiology textbooks, glass dosimeter and period medical instruments remain on a side table, a wedding ring box quietly present but secondary, no exact Nagai portrait, no miraculous light, science and faith shown as coexisting parts of one life, 16:9
```

**Negative prompt**
```text
exact Nagai portrait, saint halo, conversion miracle, readable Bible text, modern radiology equipment, nuclear explosion, anti-science caricature
```

### 1945/06 — 放射線を診ていたら、余命三年

**狙い:** 放射線医自身が白血病と診断される逆説を、医師が自分の血液検査を見る場面で静かに描く。

**Positive prompt**
```text
June 1945 Nagasaki medical laboratory, Japanese radiologist in a white coat seated alone examining his own blood smear under a microscope while a paper blood-count chart with unreadable values lies beside him, older x-ray apparatus and protective screens visible in background, posture still and reflective rather than melodramatic, no exact Nagai facial likeness, no future atomic-bomb imagery, restrained hospital palette, 16:9
```

**Negative prompt**
```text
readable blood counts, modern CT scanner, mushroom cloud foreshadowing, exact Nagai portrait, death clock, dramatic terminal-illness poster
```


### 1945/08– — 原子爆弾症！――研究しよう

**狙い:** 救護カードと被らないよう、患者を診る場面ではなく「未知の病態を記録して科学へ戻る」机上の研究構図にする。

**Positive prompt**
```text
late summer 1945 Nagasaki, a wounded Japanese physician-scientist seated at a rough temporary desk in a damaged medical shelter, handwritten case notes, simple blood-count charts without legible words, pencil, thermometer and basic period medical instruments spread across the table, his bandaged head and tired posture visible while he studies observations with intense concentration, patients only faintly suggested in the distant background, composition centered on recording and scientific inquiry amid catastrophe, no heroic pose, muted charcoal brown and gray-blue palette, original historical editorial illustration, no readable text, 16:9
```

**Negative prompt**
```text
modern laboratory, modern computer, digital monitor, detailed readable equations, readable medical records, treatment scene as the main subject, graphic wounds, gore, exact portrait recreation, glowing radiation, science-fiction equipment, triumphant scientist
```

### 1945以後（制作年要検証） — 原子雲の上へ

**狙い:** 永井が描いた「原爆死した妻を原子雲の上で昇天させる」発想を扱うが、既存作品の構図は再現しない。地上→原子雲→上空へ抜ける縦方向の象徴構図で、被爆マリアや浦上天主堂カードと明確に差別化する。

**Positive prompt**
```text
original symbolic memorial illustration inspired by the documented idea that Takashi Nagai depicted his deceased wife ascending above the Nagasaki atomic cloud, wide 16:9 frame organized with a strong vertical path through the center: tiny ruined Urakami rooftops far below, a pale towering atomic cloud rising through the middle distance, and a solitary modestly dressed 1940s Japanese woman represented as a small serene figure high above the cloud against an open pale sky, her upward placement conveyed as a visual metaphor rather than a literal supernatural event, sorrowful and restrained, no altar, no cathedral interior, no Madonna statue, no imitation of any known drawing by Nagai, original composition, no readable text
```

**Negative prompt**
```text
exact recreation of Takashi Nagai's drawing, copy of a known religious artwork, Madonna and Child icon, Virgin Mary statue, church altar composition, crucifixion scene, angels, halo, fantasy magic effects, dramatic heavenly rays, triumphal resurrection imagery, giant close-up face, gore, corpses, readable text
```

### 1948/03 — たった二畳の如己堂

**狙い:** 人物ではなく「二畳一間の小ささ」そのものを主役にする。外観の三-quarter view で、原爆カード群にない静かな空間構図を作る。

**Positive prompt**
```text
Nyokodo in Urakami Nagasaki around 1948, an extremely small simple wooden two-tatami hut shown from a slightly elevated three-quarter exterior view, modest earthen yard, a few recovering plants and simple household objects, one small seated figure visible near the doorway only for scale, strong emphasis on how tiny and humble the dwelling is, quiet postwar reconstruction atmosphere, soft overcast daylight, restrained wood brown and gray-green palette, original composition based on the known building rather than copying a tourist or museum photograph, no readable text, 16:9
```

**Negative prompt**
```text
exact tourist photograph, exact museum photograph, large traditional mansion, ornate temple, modern house, pristine landscaped garden, crowded visitors, dramatic mushroom cloud, religious apparition, readable signage, modern street furniture
```

### 1948/04 — それでも原子には希望があります

**狙い:** 原爆礼賛に見えないよう、兵器や爆発ではなく「原稿を書く人物」と「小さな原子エネルギーの抽象記号」を対置する。希望と倫理的不穏さを同居させる。

**Positive prompt**
```text
symbolic historical editorial illustration of Takashi Nagai reflecting on atomic energy after the Nagasaki bombing, a Japanese physician-writer seated beside an open manuscript and medical books in a very modest room, on one side a small abstract atom-like orbital motif rendered as a restrained geometric light shape, on the other side a dark damaged window frame and distant ruined skyline, balanced composition expressing scientific hope beside remembered destruction, thoughtful and morally uneasy rather than celebratory, no weapon, no explosion, no propaganda styling, original composition, no readable text, 16:9
```

**Negative prompt**
```text
nuclear bomb, missile, mushroom cloud as spectacle, cheerful atomic-age advertisement, smiling propaganda scientist, futuristic reactor, neon atom logo, magic glow, exact portrait recreation, readable manuscript, readable equations, triumphal technology poster
```

### 1950 — 子どもたちに、本を残す

**狙い:** 重い永井カード群の中で、子どもと本を主役にした明るい群像構図にする。如己堂の外観カードとは被らせない。

**Positive prompt**
```text
postwar Nagasaki around 1950, a small humble children's reading space with low wooden bookshelves and a simple book box, several Japanese children quietly reading or choosing books, a frail adult figure seated unobtrusively at the edge of the scene watching over them, warm daylight entering from one side, books and children's concentration as the main visual subject, modest community atmosphere rather than a formal library, gentle recovery after war, restrained warm brown and soft green palette, original historical editorial composition, no readable book titles, no readable text, 16:9
```

**Negative prompt**
```text
modern library, colorful modern children's books with readable covers, school uniforms from the wrong era, anime children, cute mascot style, luxury interior, dramatic religious imagery, mushroom cloud, exact portrait recreation, readable text
```

### 1951/05/01 — 科学に焼かれて、それでも科学を捨てなかった

**狙い:** 永井隆編の総括。中央人物＋左右対比で、片側に破壊、片側に医学ノート・本・穏やかな原子記号を置き、反科学にも科学礼賛にも寄せない。

**Positive prompt**
```text
symbolic summary portrait composition of Takashi Nagai as a physician, atomic-bomb survivor and writer, a frail Japanese doctor seated centrally in a modest postwar room, left side fading into broken brick, scorched timber and a dark ruined Nagasaki streetscape, right side containing medical notebooks, stacked books, a small reading lamp and a restrained abstract atom motif, clear left-right visual tension around the central figure, calm weary expression, knowledge continuing beside destruction, neither anti-science propaganda nor technological triumph, original composition not based on a single portrait photograph, muted charcoal brown with restrained pale highlights, no readable text, 16:9
```

**Negative prompt**
```text
split-screen graphic with labels, exact portrait photograph recreation, heroic scientist pose, smiling atomic-age propaganda, nuclear weapon, explosion, giant mushroom cloud, fantasy aura, saint halo, gore, hospital gore, modern electronics, readable notes, readable text
```

---

## 昭和天皇 ― お言葉でたどる戦争と原爆

> この区画は全件手動監査済み。顔や有名写真ではなく、御前会議・上奏・公式会見という発言の制度的な場を描く。

### 1941/09/06 — 四方の海

**狙い:** 和歌を引いたことを「開戦反対で政策を止めた」と美化せず、開戦方針が決まる御前会議の中で問いを投げた場面として描く。

**Positive prompt**
```text
September 1941 imperial conference room in Tokyo, senior military and civilian leaders seated formally around a long table while the emperor appears as a small restrained figure at the head, a slim poetry booklet or paper held open but all writing unreadable, maps and policy folders remain on the table to show the war-planning decision was not withdrawn, solemn institutional atmosphere, no exact facial likeness or imperial propaganda pose, 16:9
```

**Negative prompt**
```text
readable poem, exact emperor portrait, divine rays, antiwar hero poster, military victory propaganda, modern conference room
```

### 1945/08/08 — この兵器が使われた以上

**狙い:** 広島原爆後の終戦意向を、爆発の絵ではなく外相からの宮中上奏と報告書で描く。

**Positive prompt**
```text
August 8 1945 imperial palace briefing room, Japanese foreign minister presenting urgent translated reports and a simple aerial-damage map to the emperor seated at a low formal desk, both figures shown at respectful distance without exact facial likeness, other officials waiting quietly, visual emphasis on atomic-bomb information entering the highest level of decision-making and accelerating the end-war discussion, no readable report text or explosion spectacle, 16:9
```

**Negative prompt**
```text
exact emperor or Togo portrait, mushroom cloud dominating scene, readable US atomic statement, surrender ceremony, propaganda poster
```

### 1975/10/31 — 言葉のアヤ

**狙い:** 戦争責任への回答を「逃げた／無知だった」と表情で断定せず、公式記者会見の問いと答えの距離をそのまま描く。

**Positive prompt**
```text
1975 Japan National Press Club-style formal press conference, aging emperor seated at a table seen from medium distance while a foreign correspondent stands to ask a question from the press rows, microphones and notebooks between them, other reporters listening, all captions and notes unreadable, emotionally neutral composition focused on the public act of being questioned about war responsibility, no exact portrait likeness, 16:9
```

**Negative prompt**
```text
caricatured confused expression, readable quote, exact emperor portrait, courtroom imagery, partisan political poster, imperial symbolism dominating frame
```

### 1975/10/31 — やむを得ないことと私は思っています

**狙い:** 同じ会見でも、こちらは広島原爆への問いであることを、地方記者と被爆地資料の存在で区別する。

**Positive prompt**
```text
same 1975 formal press conference from a different side angle, regional Japanese broadcaster's reporter at a microphone asking a question while a small folder containing blurred Hiroshima memorial photographs rests on the press desk, aging emperor listening at the far end without close facial detail, sober uneasy atmosphere, no visual endorsement of the answer and no readable quotation, 16:9
```

**Negative prompt**
```text
readable quote, exact emperor portrait, mushroom cloud backdrop, cheering audience, condemnation poster, heroic or villainous caricature
```

---

## 冷戦・核抑止・軍縮

> この区画は全件手動監査。前半はV2からキューバ危機まで。兵器の精密構造より、運搬・警戒・隠密・意思決定のシステムを描く。

### 1944/09/08 — 音がする前に死ぬ

**狙い:** V2の本質を「超音速で落ち、警報や飛来音が間に合わない」都市防空の無力さとして描く。

**Positive prompt**
```text
London evening in September 1944, ordinary street and rooftops under wartime blackout while a V-2 ballistic missile descends steeply from very high altitude as a small dark shape, civil-defense observers below have no time to react, impact implied off-frame rather than shown graphically, visual tension from silent arrival before warning, period buses and architecture, no readable signs, 16:9
```

**Negative prompt**
```text
detailed missile cutaway, launch instructions, gore, bodies, heroic Nazi propaganda, modern city skyline, readable warning text, science-fiction rocket
```

### 1944–1945 — 味方をより殺してどうする

**狙い:** V2の「高性能兵器」より、地下工場の強制労働そのものが大量死を生んだ構造を主役にする。

**Positive prompt**
```text
Mittelwerk underground rocket factory in 1944, long damp tunnel filled with unfinished V-2 airframes and harsh industrial lighting, exhausted concentration-camp prisoners in striped or ragged work clothing forced to carry components under armed supervision, emaciation suggested respectfully without graphic suffering, cramped bunks and dust in side passages, oppressive production system rather than weapon glamour, no readable insignia, 16:9
```

**Negative prompt**
```text
gore, corpses, torture close-up, heroic rocket engineers, Nazi propaganda poster, swastika dominating frame, detailed missile internals, celebratory factory scene
```

### 1945–1946 — 敵の兵器ですが、技術者ごともらいます

**狙い:** 米ソがV2機材だけでなく技術者・資料まで競って回収したことを、戦後の「人と技術の移送」で描く。

**Positive prompt**
```text
Germany immediately after World War II, captured V-2 rocket sections, crates of technical papers and displaced German engineers at a rail yard where separate American and Soviet recovery teams load equipment in different directions, ruined industrial background, no side shown as heroic, emphasis on wartime technology being redistributed into two emerging blocs, no readable documents or unit markings, 16:9
```

**Negative prompt**
```text
rocket blueprint close-up, exact Operation Paperclip document, heroic von Braun portrait, triumphant flags, modern cargo terminal, propaganda caricature
```

### 1946–1952 — 真上に飛ばせば科学の進歩です

**狙い:** V2が兵器から上層大気・宇宙観測装置へ用途転換されたことを、砂漠の科学打上げで描く。

**Positive prompt**
```text
late-1940s White Sands New Mexico, captured V-2 rocket launching almost vertically from a desert test stand carrying scientific instruments, technicians and optical tracking equipment at a safe distance, the rocket rising toward a darkening high-altitude sky, a faint curved Earth horizon motif suggested above, visual contrast between military hardware and atmospheric science, muted desert tan and deep blue palette, no readable text, 16:9
```

**Negative prompt**
```text
London bombing, civilians under attack, modern orbital rocket, private-space-company style booster, astronauts, readable Nazi markings, propaganda symbols
```

### 1957/10/04 — 地球の向こうまで

**狙い:** Sputnikを「人工衛星の快挙」だけでなく、同じ大推力ロケットがICBMにもなる技術的ショックとして描く。

**Positive prompt**
```text
October 1957 Soviet launch site at dusk, tall R-7-derived rocket climbing above the pad while high in the same composition a small polished spherical satellite with four thin antennae circles the darkening Earth, distant Western radio operators listening to faint beeps on analog equipment, no triumphal propaganda, visual link between orbital launch capability and intercontinental reach, no readable slogans, 16:9
```

**Negative prompt**
```text
modern rocket, giant Soviet flag, exact propaganda poster, readable Sputnik lettering, nuclear warhead cutaway, science-fiction satellite
```

### 1946/07/29 — 帝国海軍の魂燃ゆ

**狙い:** 長門の最期を軍艦礼賛にせず、旧戦艦が核兵器効果実験の「標的物」へ変わった時代転換として描く。

**Positive prompt**
```text
Bikini Atoll in July 1946 after the underwater Crossroads test, damaged Japanese battleship Nagato listing heavily among other unmanned target ships on a radioactive lagoon, distant test instrumentation towers and support vessels kept far away, no sailors aboard, gray tropical dawn and contaminated spray haze, solemn end-of-era atmosphere rather than heroic naval image, no readable hull markings, 16:9
```

**Negative prompt**
```text
imperial naval glory poster, active battle, sailors dying, gore, exact famous Crossroads photograph, giant flag, modern warship
```

### 1949/08/29 — しばらく独り占めするつもりだったのに

**狙い:** ソ連初核実験を、米国への挑発ポスターではなく「核独占が物理的に終わる」遠隔試験場の一枚で示す。

**Positive prompt**
```text
remote Semipalatinsk test range in August 1949, first Soviet nuclear test cloud rising over an empty steppe with instrument towers and observation bunkers far in foreground, no city or civilians, a separate Western intelligence monitoring station suggested by radio receivers and air-sampling filters in a corner motif, subdued historical tone emphasizing the end of nuclear monopoly, 16:9
```

**Negative prompt**
```text
Soviet victory propaganda, city destruction, exact RDS-1 device, bomb blueprint, cheering crowds, readable slogans
```

### 1950–1951 — 朝鮮戦争、危機一髪

**狙い:** 「核使用寸前」を爆弾の発射絵にせず、戦線拡大案と核選択肢が政権内で検討されながら抑えられた危機として描く。

**Positive prompt**
```text
1950-1951 Washington war-planning room, large unlabeled map of Korea and northeast China on the wall, field reports and air-operation folders spread across a table, one sealed nuclear-options folder kept physically apart while civilian leaders and uniformed commanders argue across the table, no exact portraits, no weapon shown, visual emphasis on escalation being considered but withheld, 16:9
```

**Negative prompt**
```text
nuclear strike on Korea or China, exact MacArthur portrait, readable target map, mushroom cloud, partisan political caricature, detailed bomb plan
```

### 1949– — こちらの核は平和のためです

**狙い:** 「敵の核は脅威、自国の核は平和」という冷戦の鏡像的宣伝を、特定ポスターのコピーなしに左右対称で見せる。

**Positive prompt**
```text
early Cold War editorial composition split into mirrored American and Soviet radio-news studios, each side showing speakers reassuring domestic audiences while the opposite bloc's distant mushroom-cloud silhouette appears on their background map, their own nuclear test imagery kept behind curtains or framed as defensive security, no readable slogans and no side visually endorsed, restrained symmetry exposing reciprocal rhetoric, 16:9
```

**Negative prompt**
```text
exact propaganda posters, readable peace slogans, caricatured nationalities, partisan endorsement, detailed weapons, giant flags dominating frame
```

### 1951/04/11 — 将軍、そこまでだ

**狙い:** マッカーサー解任を「核を使おうとしてクビ」へ単純化せず、文民統制と限定戦争方針の衝突として描く。

**Positive prompt**
```text
April 1951 presidential office, civilian president signing a dismissal order while a general's cap and Far East command map rest on the opposite side of the desk, military dispatches and public statements stacked nearby, figures shown from behind without exact Truman or MacArthur portraits, sober institutional scene about civilian control over war policy, no nuclear weapon visible, no readable order text, 16:9
```

**Negative prompt**
```text
exact Truman or MacArthur portrait, nuclear bomb on desk, triumphant firing scene, readable dismissal letter, campaign poster, caricature
```

### 1952/11/01 — 星を作ろう

**狙い:** Ivy Mikeを実用爆弾としてではなく、巨大な極低温設備を必要とした「熱核原理の実証装置」として描く。

**Positive prompt**
```text
Enewetak Atoll in 1952 before Ivy Mike, bulky cryogenic support equipment, pipes and refrigeration machinery surrounding a large test installation on an otherwise small tropical island, technicians departing toward distant bunkers, later in the same wide horizon an enormous test cloud rising where the island stood, no weapon cutaway or portable-bomb implication, sober scale contrast, 16:9
```

**Negative prompt**
```text
detailed thermonuclear design, weapon cross-section, assembly instructions, city destruction, cheering scientists, tropical vacation imagery, readable technical labels
```

### 1953 — 戦術核なら大丈夫……？

**狙い:** 戦術核を「小さいから安全」と描かず、通常戦場へ核兵器を持ち込むことで境界が曖昧になる不穏さを示す。

**Positive prompt**
```text
1950s European-style military exercise field, conventional artillery, short-range missile launcher and armored vehicles arranged together while one guarded special-weapons storage trailer sits among them, troops in ordinary field positions with no firing, visual emphasis on nuclear capability being inserted into a normal-looking battlefield system, muted olive and gray palette, no weapon internals or yield labels, 16:9
```

**Negative prompt**
```text
nuclear explosion, tactical nuclear firing instructions, detailed warhead diagram, heroic soldiers, recruitment poster, readable weapon names
```

### 1954 — 海の下に原子炉を

**狙い:** 原潜革命を、原子炉断面図ではなく「浮上せず長時間航行できる潜水艦」という運用変化で描く。

**Positive prompt**
```text
mid-1950s nuclear submarine underway beneath open ocean, USS Nautilus-like silhouette cruising steadily at depth while far above a conventional diesel submarine must surface near the horizon, engineering crew inside a generic machinery room checking analog gauges without visible reactor core, visual contrast between sustained submerged operation and older limitations, no exact hull markings, 16:9
```

**Negative prompt**
```text
reactor cutaway, detailed submarine schematics, nuclear weapon launch, exact Nautilus museum photo, modern submarine, glowing reactor core
```

### 1955/07/09 — 人間であることを思い出せ

**狙い:** ラッセル＝アインシュタイン宣言を有名人の集合写真にせず、科学者が国境を越えて一枚の声明へ署名する行為として描く。

**Positive prompt**
```text
1955 study and press setting, a long table holding a formal scientific manifesto with multiple illegible signatures, fountain pens from participants of different national backgrounds, globe and hydrogen-bomb test photograph blurred in background, one empty chair subtly suggesting a recently deceased signatory, no exact portraits of Russell, Einstein or Yukawa, sober appeal to shared humanity, no readable quotation, 16:9
```

**Negative prompt**
```text
exact signed manifesto reproduction, readable famous quote, celebrity portrait lineup, peace-symbol poster, mushroom cloud spectacle, partisan propaganda
```

### 1955/09/16 — 撃つときは浮上してください

**狙い:** 初期SLBMの未完成さを、潜水艦が発射時だけ海面へ姿を晒さなければならない構図で示す。

**Positive prompt**
```text
1955 Soviet diesel submarine surfaced on a gray northern sea preparing an early ballistic missile for test launch from the deck, crew working around a simple raised missile structure while radar horizon remains exposed, another submarine silhouette hidden below the water in conceptual contrast, no warhead details, emphasis on loss of concealment at the moment of firing, no readable markings, 16:9
```

**Negative prompt**
```text
submerged launch, detailed missile erection procedure, warhead cutaway, modern submarine, heroic Soviet poster, readable hull numbers
```

### 1956/02/02 — 次の攻撃はミサイルで

**狙い:** 核弾頭と弾道ミサイルが一体化した転換を、実核試験の遠隔打上げと観測で描く。

**Positive prompt**
```text
remote Soviet test range in winter 1956, medium-range ballistic missile launching from a sparse steppe site while instrumentation crews watch from distant bunkers and tracking stations, far beyond the horizon a test-zone flash is only faintly implied, emphasis on missile becoming a nuclear delivery system rather than on blast spectacle, no exact missile dimensions or markings, 16:9
```

**Negative prompt**
```text
city target, detailed launch checklist, warhead cutaway, readable R-5M labels, propaganda poster, close nuclear fireball
```

### 1950年代後半 — きれいな核

**狙い:** “clean bomb” の矛盾を、降下物を減らす技術議論と巨大な爆風・熱線が残る事実を同じ机に置く。

**Positive prompt**
```text
late-1950s US atomic-energy policy meeting, scientists and officials comparing two generic test photographs and fallout-contour sheets with text blurred, one diagram shows reduced downwind contamination while a distant large blast silhouette remains equally overwhelming, no exact device design, visual irony of trying to make a massive nuclear weapon 'cleaner' without making it harmless, no readable slogans, 16:9
```

**Negative prompt**
```text
readable clean bomb slogan, green eco-friendly bomb joke, detailed thermonuclear design, city destruction, exact Teller portrait, propaganda advertisement
```

### 1957/07 — 夢見る学者じゃいられない

**狙い:** 第1回パグウォッシュを、東西の科学者が政府外交とは別ルートで同じ机に座る場として描く。

**Positive prompt**
```text
Pugwash Nova Scotia in summer 1957, small seaside conference room with scientists from Western, Soviet and Japanese backgrounds seated closely around one plain table, notebooks, ashtrays and tea cups, ocean visible through windows, no national delegation staging and no exact famous portraits, intimate expert dialogue across Cold War blocs, no readable papers, 16:9
```

**Negative prompt**
```text
summit diplomacy with giant flags, exact scientist portraits, readable manifesto, peace rally poster, nuclear explosion, modern conference center
```

### 1957/08/21 — 大陸の向こうまで

**狙い:** R-7のICBM試験をSputnikと重ねず、長距離弾道飛行を追う地上追跡網と射程の変化で描く。

**Positive prompt**
```text
1957 Soviet missile test range, large R-7 rocket departing a launch complex while a chain of distant analog tracking stations and radar antennas follows its long flight across an abstract unlabeled Eurasian map motif, technicians at telemetry consoles in foreground, no satellite shown, emphasis on intercontinental range becoming technically real, no warhead details or trajectory numbers, 16:9
```

**Negative prompt**
```text
Sputnik satellite, exact rocket blueprint, warhead cutaway, readable range map, city target, propaganda poster
```

### 1957/09/19 — 地下でやれば問題ない

**狙い:** Rainierを「問題なし」ではなく、大気への降下物を減らす代わりに実験を地下へ移した転換として描く。

**Positive prompt**
```text
Nevada Test Site in September 1957, tunnel entrance cut into a barren mesa with cables and seismic instruments leading inward, observers in a distant control trailer as a contained underground test produces only subtle ground vibration and dust at the hillside rather than a mushroom cloud, geophones arranged across the desert, no tunnel interior or device details, restrained engineering tone, 16:9
```

**Negative prompt**
```text
underground bomb assembly, shaft dimensions, large surface crater, mushroom cloud, readable test diagrams, modern mining equipment
```

### 1958 — 頭脳 つかいかた その２

**狙い:** PERTを「管理手法の発明」として、ポラリス計画の膨大な依存関係を壁のネットワークで可視化する。

**Positive prompt**
```text
1958 US Navy project office, engineers and managers standing before a huge wall covered with a hand-drawn network of anonymous circles and connecting arrows representing thousands of dependent tasks, submarine hull section, navigation equipment and missile test hardware visible in separate workshop bays beyond, all node labels unreadable, visual emphasis on scheduling a complex system-of-systems rather than on weapon internals, 16:9
```

**Negative prompt**
```text
readable PERT chart, detailed missile blueprint, modern project-management software, exact Polaris internals, corporate infographic style
```

### 1958/08/03 — 氷の下なら誰も見ていない

**狙い:** 北極点潜航を探検英雄譚にせず、「原子力潜水艦なら氷の下を長時間通れる」という作戦空間の拡大として描く。

**Positive prompt**
```text
USS Nautilus-like nuclear submarine cruising silently beneath thick Arctic sea ice in 1958, jagged blue-white ice ceiling above and deep dark water below, sonar and navigation crew shown generically in a dim analog control room inset, no surfacing hole and no flag-planting triumph, visual emphasis on a new hidden route under the pole, no exact hull markings, 16:9
```

**Negative prompt**
```text
tourist submarine, exact Nautilus photo, nuclear missile launch, detailed sonar procedures, giant national flag, polar adventure poster
```

### 1959/10/31 — 次の攻撃はミサイルで：実戦配備

**狙い:** Atlas Dの配備を発射シーンではなく、液体酸素を要する初期ICBMが「警戒任務」に入った運用現場で描く。

**Positive prompt**
```text
1959 US ICBM alert site, Atlas-era missile standing at a semi-hardened launch facility while ground crews service cryogenic support equipment and analog readiness consoles inside a nearby blockhouse, no launch occurring, visual emphasis on a strategic missile kept on operational alert despite cumbersome preparation, no exact base location or technical procedure, 16:9
```

**Negative prompt**
```text
launch checklist, fueling instructions, warhead cutaway, modern silo, exact Atlas markings, city target, propaganda poster
```

### 1960/04/13 — 現在地がわからないと当たりません

**狙い:** TransitをGPS一般史ではなく、「隠れている潜水艦自身は自位置を正確に知る必要がある」軍事航法の逆説として描く。

**Positive prompt**
```text
1960 nuclear submarine navigation compartment at sea, navigator comparing inertial charts with signals from a small early navigation satellite shown overhead in a secondary sky inset, analog radio receiver and plotting table without readable coordinates, submarine remains hidden beneath the ocean while its own position is refined, emphasis on concealed platform needing precise self-location, no missile launch, 16:9
```

**Negative prompt**
```text
modern GPS smartphone, exact coordinates, targeting solution, ballistic trajectory calculations, modern satellite design, readable navigation data
```

### 1960/07/20 — 浮上する必要すらありません

**狙い:** 潜航発射を、発射手順の解説ではなく「海面下に隠れたままミサイルだけが水を破る」隠密性の変化として描く。

**Positive prompt**
```text
open Atlantic in 1960, submerged ballistic-missile submarine barely visible beneath dark blue water as a test missile breaks through the sea surface and climbs away, support observation ship far in the distance, no city or target shown, broad composition emphasizing the firing platform remaining hidden below, no internal launcher details, no exact hull markings, 16:9
```

**Negative prompt**
```text
submarine cutaway, launch sequence instructions, warhead details, city target, modern SLBM, propaganda poster, readable missile markings
```

### 1960 — 潜水艦はどこにいるかわからない

**狙い:** 第二撃能力を「発射する潜水艦」ではなく、「探しても見つからない広大な海」という生残性で描く。

**Positive prompt**
```text
vast cold Atlantic ocean at dusk viewed from high above, several surface search aircraft and ships spread widely while the actual ballistic-missile submarine is only a tiny dark silhouette deep below and offset from all search patterns, no missile firing, abstract faint search arcs without coordinates, visual emphasis on uncertainty and survivability rather than attack capability, 16:9
```

**Negative prompt**
```text
exact patrol area map, sonar evasion instructions, submarine tactics diagram, missile launch, readable coordinates, action-movie chase
```

### 1961 — ミサイルは北から来る

**狙い:** 核抑止を支える「撃たれたことを早く知る」インフラとして、極北レーダーの巨大さと孤立を描く。

**Positive prompt**
```text
Thule Greenland in 1961, enormous early-warning radar structures standing alone on a snow-covered Arctic plain under low polar light, technicians crossing between buildings and analog tracking room windows glowing warmly, faint abstract polar arc in the sky suggesting northern missile approach without an actual incoming missile, scale and remoteness emphasized, no readable base signs, 16:9
```

**Negative prompt**
```text
missiles visibly attacking, modern phased-array radar, exact classified layout, readable tracking data, science-fiction radar beam, propaganda poster
```

### 1961/10/30 — 爆弾の皇帝

**狙い:** 都市破壊ではなく、北極圏の核実験が「兵器というより超大国のデモンストレーション」だったことを示す。

**Positive prompt**
```text
remote Novaya Zemlya Arctic test range in 1961, an immense nuclear cloud towering over an empty snow-covered landscape and dark sea, viewed from very far away with a small Soviet bomber silhouette retreating at the edge of frame, overwhelming scale emphasized by the vast empty horizon, no city and no people near the blast, cold blue gray environment contrasted with white-orange cloud, ominous demonstration of scale rather than spectacle, no readable text, 16:9
```

**Negative prompt**
```text
city destruction, crowds, gore, heroic propaganda poster, detailed bomb cutaway, weapon blueprint, neon fantasy colors, readable slogans
```

### 1962 — いつでも、すぐに

**狙い:** Minutemanの即応性を発射の迫力ではなく、閉じたサイロで長時間待機できる「常時即応」の静けさで描く。

**Positive prompt**
```text
1962 Minuteman-era missile field on the American plains, closed underground silo hatch in an otherwise empty landscape with a small secure launch-control facility nearby, inside inset analog crew station remains staffed around the clock, no fueling trucks and no launch, visual emphasis on a solid-fuel missile waiting continuously ready beneath the ground, no exact site layout or procedures, 16:9
```

**Negative prompt**
```text
open silo launch, missile cutaway, launch codes, exact control console, targeting map, modern base, heroic weapon poster
```

### 1962/05/09 — 科学者は京都に集う

**狙い:** 京都会議をパグウォッシュの日本版コピーにせず、日本の科学者が国内で核・軍縮・科学者責任を継続議論する場として描く。

**Positive prompt**
```text
Kyoto academic conference in May 1962, Japanese scientists and intellectuals gathered around a long table in a modest university hall, chalkboard with unreadable headings and folders on nuclear disarmament, economics and ethics, traditional Kyoto rooftops faintly visible through windows, no exact portraits of Yukawa or Tomonaga, serious domestic scholarly debate rather than government diplomacy, 16:9
```

**Negative prompt**
```text
exact scientist portraits, readable conference statement, peace rally banners, giant atom icon, modern conference center, political campaign imagery
```

### 1962/07/09 — 破壊を伴わない破壊

**狙い:** Starfish Primeを地上破壊のない「高高度核爆発」が電力・人工衛星へ作用する別種の破壊として描く。

**Positive prompt**
```text
Pacific night in July 1962, enormous artificial auroral glow high above the horizon from a distant high-altitude nuclear test, Honolulu streetlights in a small foreground area flickering or going dark while several early satellites orbit above with one failing, no ground blast or destroyed city, visual connection between upper-atmosphere event, electrical disruption and space damage, no readable signs, 16:9
```

**Negative prompt**
```text
ground-level mushroom cloud over Hawaii, city vaporization, EMP weapon schematic, modern satellites, science-fiction laser, readable electrical diagrams
```

### 1962/10/16 — 喉元に突きつけられた剣

**狙い:** キューバ危機の発見段階を、ミサイルそのものよりU-2写真解析と地理的近さで見せる。

**Positive prompt**
```text
October 1962 US intelligence photo-analysis room, analysts leaning over large black-and-white aerial reconnaissance prints showing generic construction patterns in Cuba, transparent map overlay placing Cuba close to Florida without readable labels, magnifiers, light tables and period telephones, tension centered on interpreting imagery rather than launching weapons, no exact famous U-2 photograph reproduction, 16:9
```

**Negative prompt**
```text
exact reconnaissance photograph, readable target labels, missiles pointed at viewer, nuclear explosion, exact Kennedy portrait, modern satellite imagery
```

### 1962/10/27 — 人類史上もっとも長い土曜日

**狙い:** キューバ危機が首脳会議だけでなく、海中・上空・現場の誤認でも破局し得たことを多層構図で示す。

**Positive prompt**
```text
tense 1962 Cuban Missile Crisis triptych-like composition without text: a dim government crisis room with maps and telephones on the left, a U-2 reconnaissance aircraft high over tropical cloud in the center sky, and a Soviet diesel submarine deep under dark rough Atlantic water on the right lower section, no identifiable leader portraits, red indicator lights and paper folders suggesting compressed decision time, restrained cinematic tension, muted navy gray and tobacco brown palette, no readable text, 16:9
```

**Negative prompt**
```text
exact portrait of a famous president, exact portrait of a famous Soviet leader, nuclear explosions, city destruction, celebratory military poster, modern screens, readable map labels, readable documents
```

### 1962/10/27 — 人の言うことは最後まで聞く

**狙い:** 条件の違う二通のフルシチョフ書簡から妥協点を拾ったことを、二つのメッセージと秘密裏の返答経路で描く。

**Positive prompt**
```text
White House crisis office late October 1962, two separate translated Soviet messages lying side by side on a table with visibly different lengths but unreadable text, advisers choosing to answer the earlier document while a small sealed back-channel envelope is passed discreetly to another aide, Turkey and Cuba indicated only by unlabeled map shapes, no exact leader portraits, emphasis on patient interpretation under pressure, 16:9
```

**Negative prompt**
```text
readable Khrushchev letters, exact Kennedy portrait, secret deal text, nuclear explosion, comic 'ignore second letter' graphic, modern office
```

### 1963/08/05 — 地下だけ残しました

**狙い:** PTBTが「核実験全面禁止」ではなく、大気・宇宙・水中を閉じつつ地下を残した最初の大きな制限として見せる。

**Positive prompt**
```text
1963 treaty-signing editorial composition, three delegations at a long table with an abstract four-part environment motif behind them: open sky, outer space and ocean test imagery dimmed or closed off, while one underground tunnel entrance remains visibly open, no readable treaty clauses and no exact leader portraits, restrained institutional tone emphasizing the exception left underground, 16:9
```

**Negative prompt**
```text
readable treaty text, exact signing photograph, giant peace symbols, partisan victory poster, detailed underground test device, nuclear explosion spectacle
```

### 1960年代 — 約束された破壊の上で

**狙い:** MADを「双方が都市を焼く絵」にせず、先制攻撃後も残る第二撃能力というシステム配置で描く。

**Positive prompt**
```text
1960s Cold War strategic systems composition, two opposing continents shown abstractly with hardened missile silos, alert bombers and especially hidden ballistic-missile submarines on both sides, some land assets dimmed as if struck while surviving submarines remain at sea, no actual city destruction and no launch shown, visual symmetry emphasizing unavoidable retaliation and mutual vulnerability, no readable labels or target maps, 16:9
```

**Negative prompt**
```text
burning cities, mushroom-cloud spectacle, detailed target list, launch procedures, triumph for either side, video-game strategy map
```

### 1967/12/11 — 持ちこませず……？？？

**狙い:** 非核三原則と米核抑止依存の曖昧な接合を、国会の原則と港へ入る米艦船を一画面で並置する。

**Positive prompt**
```text
late-1960s Japan, parliamentary chamber in foreground with prime minister speaking from a distant podium while through a visual transition a US naval vessel enters a Japanese port in the background, ship armament status deliberately unknowable and no nuclear symbol shown, officials exchange sealed diplomatic folders without readable text, composition centered on ambiguity between public principle and alliance operations, no exact politician portrait, 16:9
```

**Negative prompt**
```text
readable Three Non-Nuclear Principles text, nuclear warhead visibly on ship, exact Sato portrait, partisan propaganda, modern Japanese warship, campaign imagery
```

### 1968/01/21 — 核兵器を積んでいたんですが

**狙い:** チューレ事故を核爆発のように描かず、海氷上のB-52残骸と放射性物質回収という「抑止運用が生んだ事故」で見せる。

**Positive prompt**
```text
Greenland near Thule in January 1968, wrecked B-52 debris scattered across dark sea ice under polar night, no nuclear detonation, Danish and American cleanup crews in period cold-weather protective gear collecting contaminated snow and aircraft fragments into sealed containers, floodlights and tracked vehicles against vast Arctic darkness, sober accident-response scene rather than combat, no readable markings, 16:9
```

**Negative prompt**
```text
nuclear mushroom cloud, intact warheads displayed, graphic casualties, modern hazmat equipment, exact crash photograph, heroic military poster
```

### 1968/05/31 — もう勝手に核を持ち込まないでください

**狙い:** 事故後の米デンマーク合意を、主権と同盟運用の境界を文書で引き直す外交場面として描く。

**Positive prompt**
```text
1968 diplomatic desk shared by Danish and American officials, map of Greenland centered between them, two exchanged formal letters and route diagrams with all text unreadable, one generic bomber-route line stopping outside Greenlandic airspace, flags small and secondary, no exact politician portraits, visual emphasis on consent and territorial control after the Thule accident, 16:9
```

**Negative prompt**
```text
readable diplomatic notes, giant flags, exact agreement text, nuclear weapon on table, partisan national caricature, modern Arctic base
```

### 1968/07/01 — 核は俺達で独占する

**狙い:** NPTの不拡散効果と制度的不平等を、五つの核兵器国の特別な位置と多数の非核国を同じ条約机で見せる。

**Positive prompt**
```text
1968 international treaty hall, many national delegations seated around a broad table, five folders on one inner row marked only by distinct neutral seals while numerous other delegations hold identical non-nuclear commitment folders, a separate peaceful-nuclear-technology display and disarmament folder visible to show the treaty's multiple bargains, no exact flags or readable clauses, balanced neutral institutional composition, 16:9
```

**Negative prompt**
```text
ranking podium of countries, readable NPT text, partisan accusation poster, nuclear weapon glamour, exact signing photo, giant national flags
```

### 1971/03/31 — 一発で一か所とは言っていない

**狙い:** MIRVを精密な兵器設計図ではなく、一発の運搬手段から複数の再突入体が分かれることで「数え方」が変わる問題として描く。

**Positive prompt**
```text
upper-atmosphere editorial view in the early 1970s, one distant ballistic-missile bus represented generically releasing several small reentry bodies that separate toward different empty ocean test zones, in foreground treaty analysts stare at a counting board where one launcher column branches into multiple blank markers, no cities, no target coordinates, no internal weapon details, 16:9
```

**Negative prompt**
```text
detailed MIRV deployment mechanism, targeting map, city impacts, warhead cutaway, exact missile specifications, instructional diagram
```

### 1972 — 盾を捨てて剣を封じる

**狙い:** ABM条約の逆説を「防御できない状態をあえて残す」制度として、迎撃網の縮小で表す。

**Positive prompt**
```text
1972 strategic-defense planning room, large map with many proposed missile-defense radar and interceptor sites being crossed out or removed until only a very limited protected area remains, while opposing strategic missiles stay represented only as distant silhouettes, negotiators on both sides review the reduced shield network, no launch or combat, no readable map labels, visual emphasis on limiting defense to stabilize deterrence, 16:9
```

**Negative prompt**
```text
missile-defense engineering instructions, interceptor blueprint, city under attack, giant shield fantasy icon, readable ABM Treaty text, partisan victory poster
```

### 1974/07/03 — 150キロトンまでなら

**狙い:** TTBTを「地下実験禁止」と誤認させず、地下実験を残したまま威力に上限を置く中途半端さを描く。

**Positive prompt**
```text
1974 US-Soviet arms-control scene, underground test tunnel and seismic instruments shown in the background while negotiators compare generic yield-monitoring charts whose numeric scale is intentionally unreadable, a clear horizontal threshold line divides allowed and disallowed regions without any number printed, no explosion visible, restrained technical-diplomatic tone, 16:9
```

**Negative prompt**
```text
readable 150 kiloton number, detailed test device, underground weapon design, exact treaty signing photo, giant mushroom cloud, infographic poster
```

### 1976/05/28 — 平和利用ですから

**狙い:** PNETの「平和目的核爆発」という分類の奇妙さを、土木計画と核実験監視が同じ机に置かれることで示す。

**Positive prompt**
```text
mid-1970s government engineering office, large civil-excavation and reservoir concept drawings with unreadable labels laid beside seismic monitoring records and a sealed nuclear-explosive project folder, US and Soviet technical delegates discussing limits across the table, no device or detonation shown, visual irony that peaceful earthmoving and weapon-test technology share the same nuclear-explosion category, 16:9
```

**Negative prompt**
```text
nuclear excavation instructions, exact device design, readable PNET text, cheerful atomic-earthmoving propaganda, city destruction, giant explosion
```

### 1979/06/18 — 減らすとは言っていない

**狙い:** SALT IIを「軍縮」より、巨大な既存戦力へ上限をかける管理として描く。

**Positive prompt**
```text
1979 Vienna-style summit signing room, American and Soviet leaders represented only as distant generic figures while aides compare two large counting boards filled with many missile, bomber and submarine markers near fixed ceiling lines, almost none of the markers physically removed, pens and treaty folders in foreground with text unreadable, visual emphasis on limiting growth rather than deep reduction, 16:9
```

**Negative prompt**
```text
exact Carter or Brezhnev portrait, readable SALT II clauses, empty arsenals, victory celebration, nuclear launch, giant flags
```

### 1979/10/20 — もう敵の近くまで行かなくていい

**狙い:** Trident Iの射程延長をミサイル性能表ではなく、SSBNがより安全な遠方海域から任務できる地理的効果として描く。

**Positive prompt**
```text
late-1970s Atlantic strategic map blended with open-ocean scene, ballistic-missile submarine patrolling far from an adversary coastline while a long generic range arc reaches across the ocean without coordinates or target cities, older shorter patrol zone shown faintly closer to the coast, emphasis on increased stand-off distance and submarine survivability, no launch or missile internals, 16:9
```

**Negative prompt**
```text
exact patrol areas, targeting coordinates, missile performance table, launch procedure, warhead cutaway, action-movie submarine chase
```

### 1979/12/12 — 減らすために、まず増やします

**狙い:** NATO二重決定を、配備と交渉が同時に進む二本線として描き、どちらかを正解扱いしない。

**Positive prompt**
```text
Western Europe around 1979, one side of a balanced composition shows military convoys carrying covered missile equipment toward prepared bases while the other side shows NATO and Soviet negotiators approaching a conference table, a separate peaceful protest crowd in the middle distance with blank placards, no side visually privileged, no exact missile details or slogans, tense paradox of deployment and negotiation happening together, 16:9
```

**Negative prompt**
```text
readable protest slogans, exact Pershing II blueprint, partisan NATO or Soviet propaganda, missile launch, exact politician portraits
```

### 1986/10/11–12 — あと一言がまとまらない

**狙い:** レイキャビク会談を単なる失敗ではなく、核削減で大きく近づきつつSDIで止まった「あと一歩」を机上の距離で描く。

**Positive prompt**
```text
Reykjavik meeting room in October 1986, two superpower leaders shown as distant non-identifying figures across a small table, stacks of proposed nuclear-reduction papers nearly aligned between them while a separate folder containing abstract space-based defense imagery remains physically between the final signature pens, cold Icelandic window light, no exact portraits or readable text, unresolved but close atmosphere, 16:9
```

**Negative prompt**
```text
exact Reagan or Gorbachev portrait, readable agreement draft, Star Wars movie imagery, laser battle in space, triumphal handshake poster
```

### 1987/12/08 — この種類は全部捨てます

**狙い:** INF条約の画期を署名写真ではなく、配備済みミサイルが査察下で実際に切断・破壊されることとして描く。

**Positive prompt**
```text
late-1980s missile elimination facility, rows of decommissioned ground-launched missile canisters and launcher vehicles being cut, crushed or rendered unusable under observation by American and Soviet inspectors, paperwork and measurement tools present but unreadable, no active warheads or firing, practical industrial dismantlement scene emphasizing an entire weapon category going to zero, 16:9
```

**Negative prompt**
```text
operational missile launch, warhead internals, dismantlement instructions, exact treaty ceremony, victory parade, readable serial numbers
```

### 1991/07/31 — 六千発まで減らしましょう

**狙い:** START Iを「6000発」という見出しだけでなく、詳細なデータ交換・検証と条約上の数え方で描く。

**Positive prompt**
```text
1991 arms-control verification office, US and Soviet inspectors comparing large inventory boards of strategic launchers and abstract warhead-count markers while sealed data books and inspection equipment sit between them, several rows visibly being removed or crossed down toward lower ceilings, all numbers unreadable, no exact leader portraits, emphasis on counting, declared data and verification rather than spectacle, 16:9
```

**Negative prompt**
```text
readable 6000 number, exact treaty text, pile of loose nuclear warheads, weapon internals, triumphal victory scene, infographic chart style
```

### 1991/09–10 — 条約はあとでいい、先に片付けよう

**狙い:** PNIsを条約署名ではなく、政治判断だけで戦術核が艦艇・部隊から倉庫へ戻される速さと、検証の弱さで描く。

**Positive prompt**
```text
1991 end-of-Cold-War logistics scene, tactical nuclear storage containers being unloaded from naval ships and army depots into secure central warehouses on both American and Soviet sides, television announcement podiums visible only as distant silhouettes, no treaty-signing table, inspectors notably absent or minimal, composition emphasizing rapid reciprocal political moves without a formal bilateral treaty, no weapon internals, 16:9
```

**Negative prompt**
```text
warhead cutaway, transport procedures, readable presidential announcements, exact leaders, celebratory disarmament parade, unsecured weapons
```

### 1996/09/10 — 地下にも逃げ場はない

**狙い:** CTBTを一枚の署名式より、地球規模の監視網が地下・大気・海中・宇宙を横断する検証制度として描く。

**Positive prompt**
```text
mid-1990s global monitoring network editorial illustration, world globe surrounded by seismic stations, infrasound arrays, hydroacoustic ocean sensors and radionuclide sampling stations connected by thin neutral lines, small icons of underground, atmospheric and underwater nuclear-test environments all shown inactive, international monitoring center with analysts in foreground, no exact CTBTO logo or readable map labels, 16:9
```

**Negative prompt**
```text
readable CTBT text, nuclear explosion montage, modern satellite-only surveillance fantasy, exact monitoring station blueprint, partisan treaty poster
```

### 2010/03/09 — 聞かなかったことになっていました

**狙い:** 核持ち込み密約問題を陰謀劇にせず、公開された公文書から「意図的に曖昧な運用」が検証される史料調査として描く。

**Positive prompt**
```text
2010 Japanese Foreign Ministry archive review room, historians and officials opening declassified boxes of 1960s diplomatic memoranda, old port-call records and typed meeting notes spread under document cameras, through a window or inset a generic US naval vessel at a Japanese harbor, all text blurred and no hidden-warhead imagery, sober archival investigation of institutional ambiguity, 16:9
```

**Negative prompt**
```text
secret-agent conspiracy scene, hidden nuclear bomb visibly smuggled ashore, readable classified documents, exact politician portraits, sensational red-string board
```

### 2021/01/22 — 過ちは繰返しませぬから（持ってないですけど）

**狙い:** TPNW発効を勝利画にせず、締約国が集まる一方で核保有国と日本が席にいない制度的な距離を可視化する。

**Positive prompt**
```text
2021 international treaty hall after entry into force of a nuclear-weapons-ban treaty, many delegations gathered around a central agreement table while several clearly empty outer seats represent absent nuclear-armed states and another separate empty seat represents Japan without labeling any country by text, Hiroshima memorial landscape faintly suggested in a background projection, neutral institutional tone showing both normative achievement and participation gap, no flags dominating frame, 16:9
```

**Negative prompt**
```text
readable TPNW text, ranking countries as good or bad, partisan campaign poster, exact current leaders, nuclear explosion, giant national flags
```

### 2026/09/18 — Infinite Life

**狙い:** 署名前の協定を確定済みの領土移転のように描かず、米国の強い安全保障権限という説明と、デンマーク・グリーンランド側の主権・自己決定維持という説明を同じ机に置く。

**Positive prompt**
```text
September 2026 Arctic diplomacy editorial scene, Greenland map centered on a table shared by American, Danish and Greenlandic delegations, an unsigned agreement folder and three sets of briefing papers with all text unreadable, background shows Pituffik-style radar and Arctic coastline rather than territorial handover imagery, delegates shown from behind without exact leader portraits, visual tension between expanded long-term security access and continued sovereignty/self-determination, agreement visibly pending formal signature, neutral balanced composition, 16:9
```

**Negative prompt**
```text
US flag planted over Greenland, annexation map, territorial conquest imagery, exact Trump or Frederiksen portrait, readable political slogan, signed treaty when not yet signed, partisan celebration
```



---

## 原子力平和利用・デュアルユース

> この区画は全件手動監査済み。炉型・燃料サイクル・事故・高速炉・核融合を「原発の冷却塔」一枚へ潰さず、それぞれ異なる技術的・制度的場面を主役にする。

### 1953/12/08 — 平和利用……だよ？

**狙い:** Atoms for Peaceを善意だけの物語にせず、平和利用の拡大と軍事転用防止という二重課題の出発点として描く。

**Positive prompt**
```text
United Nations assembly hall in December 1953, US president shown only as a distant speaker at a podium while delegates view a display of peaceful nuclear applications such as a small research reactor model, medical isotope vial and agricultural experiment, beside them a separate sealed safeguards ledger and controlled nuclear-material container suggest verification concerns, no exact Eisenhower portrait, no readable speech or UN logo, balanced hopeful but cautious tone, 16:9
```

**Negative prompt**
```text
exact Eisenhower portrait, readable Atoms for Peace slogan, propaganda poster, atomic bomb, giant glowing atom icon, exact UN emblem, triumphalist futuristic city
```

### 1957/12 — 原子の火で街を照らす

**狙い:** Shippingportを「世界初の原発」と誤解させず、大型民生PWRが送電網へ入る米国の実用化段階として描く。

**Positive prompt**
```text
Shippingport Pennsylvania in December 1957, early commercial-scale pressurized-water nuclear power station beside the Ohio River, turbine-generator hall and transmission lines carrying electricity toward a modest American town at dusk, operators visible through a control-room window with analog panels, no giant cooling-tower stereotype required, restrained industrial optimism, original viewpoint not copying a plant photograph, no readable signs, 16:9
```

**Negative prompt**
```text
world's first power plant claim written in image, futuristic reactor, glowing core, nuclear weapon imagery, modern digital control room, exact plant publicity photograph
```

### 1968～ — 平和利用は権利です

**狙い:** NPT第4条の「平和利用の権利」とIAEA保障措置を、技術提供と検証が同じ場にある制度として描く。

**Positive prompt**
```text
late-1960s international nuclear-cooperation facility, engineers from a non-nuclear-weapon state receiving reactor components and medical isotope equipment while neutral international inspectors independently seal material containers and check inventory records, two activities occurring side by side rather than in conflict, no exact IAEA logo or treaty text, institutional and technical atmosphere, 16:9
```

**Negative prompt**
```text
readable NPT article text, bomb-making laboratory, exact IAEA branding, national ranking imagery, glowing uranium, political propaganda
```

### 1970年代～ — 燃やすために、まず分けます

**狙い:** 再処理を「リサイクル」だけにせず、分離プルトニウムが資源でも拡散上の重要物質でもある二面性で描く。

**Positive prompt**
```text
1970s nuclear reprocessing plant, heavily shielded chemical-processing cells behind thick windows, remote manipulators moving spent-fuel process containers, downstream sealed containers marked only by shapes indicating recovered uranium and plutonium streams without text, international safeguards cameras and seals visible, no weapon components, industrial dual-use tension rather than green recycling imagery, 16:9
```

**Negative prompt**
```text
bomb core, plutonium weapon design, detailed chemical separation recipe, exact PUREX flow diagram, green recycling arrows, glowing radioactive liquid, readable labels
```

### 1979/03/28 — 平和利用は、たまに取り返しがつかない ×1

**狙い:** TMI事故を外観の大爆発にせず、表示設計・給水故障・運転員判断が重なる制御室事故として描く。

**Positive prompt**
```text
Three Mile Island control room in March 1979, dense wall of analog gauges, indicator lights and switches with operators trying to interpret conflicting signals, steam-generator and valve-status diagrams visible only as abstract unreadable shapes, plant exterior faint through a window with no explosion, tense human-factors scene focused on confusing information and partial core damage, no readable panel labels, 16:9
```

**Negative prompt**
```text
mushroom cloud, reactor building exploding, green radiation glow, graphic casualties, modern digital control room, exact control-panel photograph, readable procedures
```

### 1986/04/26 — 平和利用は、たまに取り返しがつかない ×2

**狙い:** チェルノブイリを「巨大爆発の一瞬」だけでなく、露出した炉心・黒鉛火災・消防・避難へ続く事故として描く。

**Positive prompt**
```text
Chernobyl Unit 4 before dawn on April 26 1986, shattered reactor building with an open damaged roof and deep orange graphite fire glow inside, firefighters and plant workers operating at respectful distance in period gear, no graphic acute-radiation injuries, nearby Pripyat apartment blocks dark in the background awaiting evacuation, sober industrial-disaster composition rather than apocalyptic spectacle, no readable Soviet signage, 16:9
```

**Negative prompt**
```text
nuclear mushroom cloud, mutant imagery, green radiation glow, graphic burns, corpses, exact famous rooftop photograph, modern hazmat suits, disaster-movie monsters
```

### 2011/03/11 — 平和利用は、たまに取り返しがつかない ×3

**狙い:** 福島第一事故を「原発が爆発する絵」だけに縮めず、津波・全電源喪失・緊急対応の複合災害として描く。

**Positive prompt**
```text
Fukushima Daiichi nuclear power station after the March 2011 tsunami, flooded service roads, damaged reactor buildings, emergency workers in protective gear moving cables and portable power equipment, dark powerless infrastructure with temporary lights, ocean and tsunami debris visible in the distance, no active explosion, sober disaster-response composition emphasizing station blackout and difficult stabilization work, no company logos or readable signs, 16:9
```

**Negative prompt**
```text
nuclear mushroom cloud, city vaporization, glowing green radiation, graphic casualties, bodies, gore, superhero hazmat suits, futuristic machinery, readable company logos
```

### 1951/12/20 — 四つの電球から

**狙い:** 原子力発電史の始まりを、巨大都市ではなく「まず4個の電球が点いた」という小さなスケールで見せる。

**Positive prompt**
```text
interior of Experimental Breeder Reactor I in Idaho in December 1951, four simple incandescent light bulbs glowing warmly from a small electrical panel in the foreground, engineers in period work clothes watching with restrained satisfaction, industrial reactor-room equipment and analog gauges behind them, emphasis on modest first electrical output within a larger breeder-reactor research program, no readable text, 16:9
```

**Negative prompt**
```text
giant modern nuclear power plant cooling towers, futuristic reactor, neon blue radiation, modern LED bulbs, readable gauge text, celebratory sci-fi city
```

### 1953 — 燃やした以上に増えました

**狙い:** 「増殖」を魔法の永久機関にせず、炉心の前後で核分裂性物質の収支を測る実験成果として描く。

**Positive prompt**
```text
1953 EBR-I research laboratory, engineers comparing sealed fuel samples and assay instruments before and after reactor irradiation, one neutral balance-like material-accounting board shows slightly more fissile-material markers after operation without readable numbers, reactor machinery in background, scientific verification of breeding rather than limitless-energy fantasy, no weapon imagery, 16:9
```

**Negative prompt**
```text
perpetual motion machine, infinite fuel icon, plutonium bomb, detailed breeding ratio numbers, glowing reactor, modern laboratory, readable charts
```

### 1977/04/24 — 常陽、昇る

**狙い:** 常陽を発電所ではなく、日本がナトリウム冷却高速炉技術を実機で蓄積する研究炉として描く。

**Positive prompt**
```text
Oarai Japan in April 1977, compact Joyo experimental fast-reactor facility under clear spring light, engineers in a control room with analog panels and a separate sodium-system maintenance area containing insulated piping and inert-gas handling equipment, no electricity-transmission glamour, visual emphasis on research operation and materials irradiation, no exact facility logo or standard publicity angle, 16:9
```

**Negative prompt**
```text
commercial power station cooling towers, sodium fire, nuclear explosion, exact Joyo promotional photo, modern control room, readable signage
```

### 1994/04/05 — 夢の原子炉、臨界

**狙い:** もんじゅ初臨界を「夢の実現」と断定せず、原型炉がようやく核反応を始めた期待の段階として描く。

**Positive prompt**
```text
Monju prototype fast-breeder reactor control room in April 1994, operators watching analog indicators rise into a stable critical state, large sodium-cooled plant systems visible only through simplified maintenance windows and piping corridors, no triumphant crowd, cautious engineering milestone atmosphere with the full facility still in commissioning mode, no readable plant name or control values, 16:9
```

**Negative prompt**
```text
full commercial success poster, nuclear explosion, exact Monju control-room photograph, readable criticality values, green radiation glow, futuristic reactor
```

### 1995/12/08 — そんなものを冷却剤につかうな

**狙い:** 液体ナトリウムの利点と反応性を、火災の派手さより漏洩した二次系配管と金属火災対応で描く。

**Positive prompt**
```text
Monju secondary cooling-system room in December 1995, metallic sodium leaking from damaged piping onto a steel floor and reacting with air in a localized bright orange metal fire, operators observing from a protected control area and emergency teams preparing appropriate dry extinguishing materials, no reactor-core breach and no radioactive cloud, technical accident scene focused on difficult coolant chemistry, no readable labels, 16:9
```

**Negative prompt**
```text
water hose sprayed onto sodium, nuclear mushroom cloud, reactor meltdown glow, graphic injuries, exact accident video frame recreation, modern fire equipment, readable plant branding
```

### 2010/05/06 — 十四年ぶりに、もう一度

**狙い:** 14年ぶり再開の重さと、ほどなく別トラブルで再停止する脆さを、再起動中の設備点検として描く。

**Positive prompt**
```text
Monju prototype reactor in May 2010, engineers carefully restarting long-idle systems after years of maintenance, inspection teams moving through piping galleries while analog and early-digital control panels show stable test operation, a large maintenance crane and reactor-vessel access equipment remain prominently present to suggest complexity and fragility, restrained cautious restart rather than celebration, no readable text, 16:9
```

**Negative prompt**
```text
victory ceremony, exact Monju photograph, falling equipment accident shown graphically, nuclear explosion, modern futuristic control room, readable status displays
```

### 2016/12 — 夢は廃炉になったのか

**狙い:** もんじゅ廃止を「高速炉研究そのものの終了」と誤解させず、一施設の廃炉決定と別の研究計画が分岐する構図にする。

**Positive prompt**
```text
2016 Japanese energy-policy and decommissioning scene, Monju facility entering long-term shutdown with maintenance covers and decommissioning planners in foreground, while a separate distant research-board display shows generic future fast-reactor experiments continuing elsewhere with no specific project claims, split-path composition emphasizing plant closure versus continuation of the technology field, no readable policy text, 16:9
```

**Negative prompt**
```text
all fast reactors globally abandoned, nuclear explosion, exact government press conference, readable slogans, anti-nuclear or pro-nuclear campaign poster
```

### 1952–1953 — たぶん動くと思います

**狙い:** Perhapsatronの名の軽さと、実際には不安定性に直面した初期制御核融合研究を実験装置で描く。

**Positive prompt**
```text
early-1950s Los Alamos fusion laboratory, compact Z-pinch experiment with a cylindrical plasma tube surrounded by heavy electrical banks, brief bright plasma column visibly kinking and touching the wall while researchers watch oscilloscopes from a safe distance, improvised experimental character and uncertainty, no weapon application or readable device name, 16:9
```

**Negative prompt**
```text
stable miniature sun, fusion power plant, nuclear weapon design, modern laser lab, readable Perhapsatron label, sci-fi reactor
```

### 1958/09 — ドーナツは東から

**狙い:** 最初期トカマクを「完成した核融合炉」にせず、ソ連がトロイダル磁場閉じ込め方式を国際社会へ提示した段階として描く。

**Positive prompt**
```text
1958 Geneva scientific conference and Soviet laboratory blended editorially, simple early toroidal plasma apparatus shown on a technical display table with copper coils and vacuum vessel, international scientists leaning in to study photographs and measurements, no glowing futuristic donut and no readable tokamak term, atmosphere of a new confinement geometry being introduced to the world, 16:9
```

**Negative prompt**
```text
ITER-like giant reactor, neon plasma ring, readable conference paper, Soviet propaganda, nuclear weapon, modern superconducting coils
```

### 1968/08–1969/08 — ソ連の数字、本当でした

**狙い:** 冷戦下で英国チームがソ連装置へ入り、独立測定で高温プラズマを確認した科学協力を描く。

**Positive prompt**
```text
late-1960s Soviet T-3 tokamak laboratory, British visiting scientists installing laser Thomson-scattering diagnostics beside Soviet researchers around the same machine, mixed teams comparing independent measurement equipment and paper plots with all numbers unreadable, no flags dominating the room, cooperative verification across Cold War blocs, plasma glow restrained and physically plausible, 16:9
```

**Negative prompt**
```text
spy laboratory, exact scientist portraits, readable temperature values, futuristic tokamak, propaganda handshake, nuclear explosion
```

### 1985/11 — 太陽だけは共同開発

**狙い:** 米ソが核兵器では対立しつつ、制御核融合では国際共同開発を支持した対比を、首脳写真より研究者側へ寄せる。

**Positive prompt**
```text
1985 Geneva diplomatic backdrop fading into an international fusion design workshop, American, Soviet, European and Japanese engineers gathered around a large generic toroidal-reactor model and shared drafting table, summit leaders only tiny distant silhouettes on a television monitor with faces indistinct, visual emphasis on political approval enabling multinational technical cooperation, no readable joint statement or ITER logo, 16:9
```

**Negative prompt**
```text
exact Reagan or Gorbachev portrait, readable summit declaration, futuristic completed power plant, national flags dominating, weapons imagery
```

### 1991/11/09 — 夢物語、1.7メガワット

**狙い:** JET初D-T実験を数字の派手さだけでなく、トリチウムを実際の燃料として扱い始めた運用段階として描く。

**Positive prompt**
```text
JET fusion facility in 1991, large toroidal machine surrounded by diagnostics while operators in control room monitor a short deuterium-tritium plasma pulse, shielded tritium-handling and fuel-processing equipment visible in a separate bay, restrained blue-white plasma, emphasis on first serious D-T operation and fuel management rather than commercial power generation, no readable output values, 16:9
```

**Negative prompt**
```text
powering a city, readable 1.7 MW display, exact JET publicity photo, sci-fi reactor, fusion weapon imagery, giant sun inside chamber
```

### 1997 — 16メガワットの数秒間

**狙い:** JETのメガワット級核融合を「発電成功」と誤認させず、短い高出力パルスと計測の成果として描く。

**Positive prompt**
```text
1997 JET control room during a high-performance D-T pulse, large analog-digital hybrid displays showing a brief rising pulse shape with axes unreadable, through a protected observation concept the toroidal plasma burns brightly for only a short interval, operators focused on diagnostics and fuel systems, no turbine generator or city power connection, visual emphasis on seconds-long experimental output, 16:9
```

**Negative prompt**
```text
commercial fusion power plant, readable 16 MW number, continuous endless plasma, exact control screen reproduction, sci-fi energy core
```

### 1998 — 1を超えた。ただし換算です

**狙い:** JT-60UのQ換算値を、実際のD-T利得1超と誤認させないよう「重水素実験→D-T換算」の二段階で描く。

**Positive prompt**
```text
1998 JT-60U research control room in Japan, deuterium-only plasma experiment running in the tokamak while scientists compare measured results with a separate theoretical D-T-equivalent calculation sheet represented by an unlabeled transformed curve, clear visual separation between actual experiment and converted estimate, no tritium fuel container present, no claim of net energy production, no readable numbers, 16:9
```

**Negative prompt**
```text
actual D-T burn, readable Q=1.25 text, commercial fusion output, exact JT-60U screen, futuristic reactor, city powered by fusion
```

### 2022/12/05 — 入れたより、出た

**狙い:** NIF点火を「発電所の黒字化」と誤解させず、標的へ届いたレーザー2.05MJと核融合出力3.15MJの標的利得として描く。

**Positive prompt**
```text
National Ignition Facility target chamber in December 2022, many laser beamlines converging on a tiny central target capsule inside a huge spherical chamber, scientists in a control room compare two abstract energy bars where fusion output exceeds laser energy delivered to the target, facility electrical infrastructure remains visibly much larger in the background to show this is not whole-plant net energy, no readable numbers or logos, 16:9
```

**Negative prompt**
```text
commercial fusion power station, grid electricity output, readable energy values, nuclear weapon design, exact NIF promotional photo, sci-fi death ray
```

### 2023/10/23 — もっと大きなドーナツを

**狙い:** JT-60SA初プラズマを、まだD-T核融合をしない大型超伝導トカマクの工学実証として描く。

**Positive prompt**
```text
JT-60SA facility in Japan in October 2023, enormous toroidal superconducting fusion device filling the experimental hall, first modest plasma glow confined inside the vacuum vessel while engineers monitor cryogenic, magnet and plasma-control systems, human figures tiny for scale, emphasis on assembling and controlling a huge research machine rather than achieving fusion power, no readable facility branding, 16:9
```

**Negative prompt**
```text
D-T fusion claim, commercial electricity generation, exact publicity photograph, ITER branding, giant miniature sun, readable plasma values
```

### 2023/09–11 — 40年目の卒業試験

**狙い:** JET最終D-Tキャンペーンを記録更新だけでなく、約40年の装置が次世代へデータと人材を渡す終幕として描く。

**Positive prompt**
```text
JET fusion facility during its final 2023 D-T campaign, veteran toroidal machine operating one last long experimental pulse while senior and younger researchers watch together in the control room, archival binders from decades of experiments stacked beside new ITER-oriented test plans with text unreadable, bittersweet handover atmosphere, no demolition or commercial-power claim, 16:9
```

**Negative prompt**
```text
graduation caps, literal school ceremony, readable 69.26 MJ number, exact JET photo, commercial reactor, futuristic city
```

### 2025/04/07 — 一度きりではありません

**狙い:** NIFの点火再現・出力向上を「商用化目前」と誇張せず、同じ巨大施設で複数回条件を改善する実験科学として描く。

**Positive prompt**
```text
National Ignition Facility in April 2025, target-preparation technicians installing another tiny capsule while a wall of previous shot records shows several successful pulse traces with all values unreadable, laser bays and target chamber vast around the small replaceable target, scientists comparing incremental experimental changes, emphasis on repeatability and improved target gain rather than power-plant readiness, no logos, 16:9
```

**Negative prompt**
```text
commercial fusion power, readable 8.6 MJ or 4.13 values, nuclear weapon blueprint, exact NIF publicity photo, sci-fi laser cannon, victory celebration
```

### 20XX — 🔒 いまだ夢物語か……

**狙い:** 未来実績として、実験室の成功と「送電・燃料・材料・保守・コストまで成立した発電所」の距離を未完の工学として描く。

**Positive prompt**
```text
speculative near-future fusion engineering site, a functioning experimental fusion core in one building connected only partially to unfinished turbine, tritium-breeding, remote-maintenance and materials-test systems, several major subsystems still under construction or validation, engineers reviewing an incomplete commissioning checklist with text unreadable, no claim of commercial operation, sober unresolved technological horizon, 16:9
```

**Negative prompt**
```text
fully operational fusion city, limitless free energy, finished commercial plant claim, readable future date, utopian advertising, giant sun fantasy, existing company branding
```

### 20XX — 🔒 地上に太陽を

**狙い:** 真の解除条件を「核融合が起きた」ではなく、燃料サイクル・材料・熱回収・保守まで統合した商用発電所の送電開始として描く。

**Positive prompt**
```text
speculative future first commercial fusion power station at the moment of verified grid connection, toroidal fusion plant integrated with turbine hall, heat exchangers, tritium breeding and fuel-processing systems, remote maintenance robotics and transmission substation all visibly operating as one coherent facility, engineers and grid operators observing normal stable operation rather than celebration, realistic industrial architecture, no corporate logos or exact date, 16:9
```

**Negative prompt**
```text
magic miniature sun floating outdoors, limitless-energy utopia, science-fiction city, weapon imagery, existing company branding, readable claims of infinite free power
```


---

## 軍事同盟の核戦略 ― NATOとワルシャワ条約機構

> この区画は全件手動監査済み。国旗とミサイルの並置ではなく、同盟内の協議・指揮権・配備・演習・作戦計画の違いを一枚ずつ分ける。

### 1957/05/23 — 通常兵器で負けそうなら核があります

**狙い:** NATO大量報復を「核を使いたい戦略」ではなく、通常戦力負担を抑えつつ核の脅威を前面に置く抑止設計として描く。

**Positive prompt**
```text
1957 NATO planning room, conventional ground-force markers appear relatively sparse on a large unlabeled European map while a separate strategic nuclear-response folder and bomber silhouettes sit prominently behind them, officers and civilian officials reviewing deterrence options without any launch, no exact national leaders, no readable doctrine text, visual emphasis on nuclear retaliation compensating for limited conventional strength, restrained Cold War institutional tone, 16:9
```

**Negative prompt**
```text
nuclear explosion, readable MC 14/2 document, exact NATO logo, warhead blueprint, triumphant military poster, giant flags
```

### 1966/12–1967/04 — 核会議を始めます

**狙い:** NPGを「核保有国だけの会議」にせず、非核加盟国も核政策協議へ入る制度化として描く。

**Positive prompt**
```text
1967 NATO ministerial conference room, delegates from many allied states seated around one circular table discussing generic nuclear-policy folders, a few seats associated with nuclear powers but most represented as non-nuclear allies, no weapon on the table, shared consultation emphasized through equal sight lines and microphones, no exact portraits or readable country names, 16:9
```

**Negative prompt**
```text
exact NATO emblem, readable Nuclear Planning Group text, giant flags, operational launch discussion, weapon blueprint, celebratory alliance poster
```

### 1967/12/12 — いきなり世界を終わらせないために

**狙い:** 柔軟反応を「核戦争を段階的に楽しむ図」にせず、通常戦力→戦術核→戦略核という選択肢増加の危うさを示す。

**Positive prompt**
```text
late-1960s NATO command exercise room, three distinct sealed option folders arranged from conventional defense to limited nuclear response to strategic nuclear response, commanders debating at a map table while the final folder remains closed and physically farthest away, no attack shown, visual emphasis on escalation ladders and the difficulty of deciding where to stop, no readable labels or doctrine text, 16:9
```

**Negative prompt**
```text
video-game escalation ladder, mushroom clouds at each step, detailed targeting plans, readable doctrine labels, heroic generals, exact NATO graphics
```

### 1979/12/12 — 配備します。交渉もします。

**狙い:** 二重決定を、ミサイル配備準備と軍備管理交渉が同時進行する二本線として描く。

**Positive prompt**
```text
Western Europe in 1979, left side shows covered missile equipment and base construction preparations moving forward, right side shows allied and Soviet negotiators taking seats at a conference table, a public protest march with blank placards crosses the middle distance, balanced composition with no side endorsed, no exact Pershing II details or readable slogans, 16:9
```

**Negative prompt**
```text
readable protest text, exact missile blueprint, missile launch, partisan propaganda, exact leaders, giant NATO or Soviet flags
```

### 1983/11/07–11 — これは演習です。本当に演習です。

**狙い:** Able Archer 83を「核戦争寸前だった」と断定せず、演習手順と相手側警戒が別々に進み得る誤認リスクとして描く。

**Positive prompt**
```text
November 1983 command-post exercise, NATO staff inside a bunker follow simulated nuclear-release procedures using clearly exercise-only blank cards and telephones, while in a separate distant Soviet early-warning room operators watch real readiness indicators with concern, no actual missiles launched and no exact historical claim of imminent war, split institutional perspective emphasizing misinterpretation risk, no readable exercise text, 16:9
```

**Negative prompt**
```text
actual nuclear attack, readable Able Archer documents, definitive 'almost WWIII' headline, exact leader portraits, modern digital command center, propaganda poster
```

### 1960年代～現在 — 核は共有します。核ボタンは共有しません。

**狙い:** NATO nuclear sharingを共同所有と誤解させず、米管理の核兵器・同盟国DCA・共同協議を分離して見せる。

**Positive prompt**
```text
European NATO airbase across several decades, a secure US-controlled weapons storage area kept physically separate from allied dual-capable aircraft and multinational planning staff, American custodial personnel at the vault while allied crews train on aircraft outside, no weapon exposed and no launch procedures, visual emphasis on shared mission but retained US custody and decision authority, no readable base markings, 16:9
```

**Negative prompt**
```text
open B61 bomb details, arming instructions, shared red launch button, exact aircraft squadron markings, NATO propaganda poster, readable nuclear-sharing diagram
```

### 2010/11/19～ — 核兵器がある限り、核同盟です

**狙い:** 「核廃絶を支持しつつ核同盟を維持する」NATOの緊張を、同じ戦略文書内の二方向で表す。

**Positive prompt**
```text
2010 NATO strategy meeting, delegates review one policy board where a long-term path toward fewer nuclear weapons points outward while a current deterrence posture remains active in a separate present-day column, nuclear-capable aircraft and conventional forces appear only as distant silhouettes, no exact leaders or logos, visual emphasis on simultaneous disarmament aspiration and deterrence maintenance, no readable text, 16:9
```

**Negative prompt**
```text
political endorsement, readable NATO strategic concept, nuclear explosion, simplistic peace-versus-war cartoon, exact current leader portraits
```

### 1960年代 — 核はモスクワで預かります

**狙い:** ワルシャワ条約機構の核任務で、東欧軍が運搬手段を持ちながら弾頭統制はソ連が握った集中管理を描く。

**Positive prompt**
```text
1960s Warsaw Pact military base, East European missile and aircraft crews train beside empty delivery systems while a separate heavily guarded Soviet-controlled storage compound remains closed behind fences, Soviet custodial officers hold sealed access records, no exposed warheads or procedures, visual emphasis on alliance participation with centralized nuclear custody, no readable national markings, 16:9
```

**Negative prompt**
```text
open nuclear warhead, arming procedures, exact base layout, heroic Soviet propaganda, giant flags, readable storage labels
```

### 1964 — 9日後、リヨン

**狙い:** 1964年計画を実際の戦争予測としてではなく、核交換後も西進を続ける作戦机上の前提の異様さとして描く。

**Positive prompt**
```text
1964 Warsaw Pact staff planning room, unlabeled Central European map covered with broad westward movement arrows continuing past several abstract nuclear-damage zones, officers calculate logistics and bridge crossings as though the campaign continues after nuclear use, no city names, no exact route or target list, sober archival-planning atmosphere rather than battle spectacle, 16:9
```

**Negative prompt**
```text
readable Lyon label, exact operational war plan, target coordinates, city nuclear explosions, detailed invasion instructions, video-game map
```

### 1975 — 核で道を開けます

**狙い:** SOYUZ-75の戦術核を「終戦兵器」ではなく、地上軍突破のための作戦火力として扱う危険な思想を演習図で示す。

**Positive prompt**
```text
1975 Warsaw Pact command exercise, tank and mechanized-unit markers wait behind a defensive line on an unlabeled map while several abstract nuclear-strike zones are drawn ahead as gaps intended for subsequent advance, staff officers continue planning movement after the strikes, no real detonation or exact targets, visual emphasis on nuclear use being integrated into battlefield maneuver, 16:9
```

**Negative prompt**
```text
actual nuclear battlefield, detailed strike coordinates, operational instructions, readable SOYUZ-75 plan, glorious tank charge, propaganda poster
```

### 1979 — 7日後、ライン川

**狙い:** 公開された戦争シナリオを、核交換で自陣営も被害を受けるのに作戦継続する机上計画として描く。

**Positive prompt**
```text
late-1970s Warsaw Pact planning table, map of Central Europe with several damaged home-region zones on the eastern side and broad westward arrows still reaching toward a major river line, staff continue calculating movement while casualty and infrastructure-loss folders pile up, all place names and numbers unreadable, no real combat, grim contradiction of continuing operations after catastrophic nuclear exchange, 16:9
```

**Negative prompt**
```text
readable Rhine label, exact Seven Days war plan, target list, nuclear fireball spectacle, detailed invasion route, video-game strategy art
```

### 1970年代末～1980年代 — できれば通常兵器でお願いします

**狙い:** 核廃絶ではなく、核戦力を維持したまま通常戦で戦える時間を伸ばす方向への変化として描く。

**Positive prompt**
```text
1980s Warsaw Pact field exercise, large conventional armored and artillery formations training with nuclear-capable systems kept covered and inactive at the rear, command staff focus on conventional maneuver maps while a sealed nuclear contingency folder remains unopened, visual emphasis on postponing nuclear escalation rather than abandoning nuclear forces, no exact unit markings or operational routes, 16:9
```

**Negative prompt**
```text
nuclear disarmament ceremony, actual nuclear strike, detailed battle plan, exact weapon specifications, heroic propaganda, readable maps
```

### 1987/05/28–29 — 今度は『厳格に防御的』

**狙い:** ワルシャワ条約機構末期の防御ドクトリン転換を、従来の西進矢印が消され国境防御へ書き換えられる作戦図で示す。

**Positive prompt**
```text
1987 East Berlin alliance meeting and staff-room transition, an older wall map with broad westward offensive arrows being removed or covered, replaced by defensive positions concentrated near alliance borders, political delegates approve a new doctrine folder while military planners revise exercise boards, no exact leaders, no readable doctrine text, restrained late-Cold-War atmosphere, 16:9
```

**Negative prompt**
```text
readable strictly defensive slogan, exact Warsaw Pact logo, victory propaganda, detailed current military plans, nuclear explosion, giant flags
```

---

## グリーンランド ― 核抑止の北極前哨

> この区画は全件手動監査済み。氷原の風景だけでなく、主権・基地・地下構想・小型原子炉・宇宙監視という別々の役割を描き分ける。

### 1941/04/09 — 本国の許可は取れていません

**狙い:** カウフマン協定を「独立宣言」のようにせず、占領下で本国の同意を得られないまま防衛権限を約束した主権のねじれとして描く。

**Positive prompt**
```text
Washington diplomatic office in April 1941, Danish envoy and American officials sign a Greenland defense agreement while a telephone and sealed cable from occupied Copenhagen sit unanswered at the edge of the desk, large map of Greenland between them, Danish sovereignty symbolically retained through a small neutral document seal, no exact portraits or readable clauses, uneasy wartime diplomacy rather than triumph, 16:9
```

**Negative prompt**
```text
Greenland annexation map, readable treaty, exact Henrik Kauffmann portrait, US flag planted on Greenland, conquest imagery, modern diplomacy
```

### 1951/04/27 — 北極に基地を置きます

**狙い:** チューレ基地建設を一つの滑走路ではなく、北極圏へ爆撃機・通信・補給・後の警戒機能が集積する拠点化として描く。

**Positive prompt**
```text
northwest Greenland in the early 1950s, large new Arctic airbase under construction with long runway, hangars, fuel storage, radar and communications masts, cargo ships unloading supplies in a short ice-free season, tiny workers and heavy equipment emphasizing logistical scale, no nuclear weapons visible, stark snow and rock landscape, no readable signs, 16:9
```

**Negative prompt**
```text
modern Pituffik base, visible nuclear bombs, exact aerial base map, annexation symbolism, futuristic Arctic city, readable unit markings
```

### 1960–1962 — 氷の下なら見つからない

**狙い:** Project Icewormを実現済み基地のように描かず、氷床下の巨大ミサイル網という未実現構想を設計模型として示す。

**Positive prompt**
```text
early-1960s US Army Arctic planning room, large conceptual cutaway model of Greenland ice sheet showing an imagined branching tunnel network and movable missile shelters far beneath the surface, planners compare the model with ice-deformation measurements and cracked tunnel supports from Camp Century, all dimensions and routes intentionally generic and unreadable, clearly presented as a proposal rather than built reality, 16:9
```

**Negative prompt**
```text
operational hidden missile network, exact Iceworm map, launch instructions, detailed silo engineering, readable missile counts, science-fiction underground city
```

### 1960/10/03 — 氷の下にも原子炉を

**狙い:** Camp CenturyのPM-2Aを「平和な小型炉」でも「核兵器施設」でもなく、遠隔軍事基地の電源として描く。

**Positive prompt**
```text
Camp Century Greenland in 1960, snow tunnels and prefabricated military living spaces powered by a compact portable nuclear-reactor plant housed in a practical insulated chamber, engineers monitor analog systems while electrical cables and heating lines serve the remote base, ice walls slowly deform around tunnel supports, no weapon connection or glowing reactor core, documentary engineering tone, 16:9
```

**Negative prompt**
```text
nuclear bomb, detailed reactor core cutaway, exact PM-2A blueprint, futuristic underground city, green radiation glow, readable military labels
```

### 2004/08/06 — 基地は一つだけ残りました

**狙い:** 冷戦後の施設縮小と、残る一拠点の戦略的重要性を「消えた基地跡」と現役レーダーの対比で描く。

**Positive prompt**
```text
Greenland in 2004, broad Arctic map-like landscape showing several former US defense sites faded or abandoned while one active Thule-area base remains with runway and radar facilities, Danish and Greenlandic civilian representatives join American officials at a consultation table in foreground, no exact map labels or sovereignty claims, visual emphasis on contraction to one enduring strategic area, 16:9
```

**Negative prompt**
```text
readable treaty map, annexation imagery, exact base layout, nuclear weapons, giant flags, modern political propaganda
```

### 2023/04/06 — チューレからピトゥフィクへ

**狙い:** 改称を単なる看板交換にせず、グリーンランド語名への変更と宇宙・ミサイル警戒任務の継続を同時に描く。

**Positive prompt**
```text
Arctic space-surveillance base in Greenland in April 2023, crews replace an old generic English-language base sign with a new sign whose actual lettering is intentionally blurred, local Greenlandic representatives present alongside US Space Force personnel, large missile-warning radar and space-tracking equipment continue operating unchanged in background, cultural recognition and mission continuity shown together, no exact logos, 16:9
```

**Negative prompt**
```text
readable Thule or Pituffik signage, exact Space Force logo, partisan sovereignty imagery, futuristic laser radar, exact ceremony photograph, giant flags
```


---

## 各国・地域の核史 ― フランスと英国

### 1945/10/18 — 共和国は原子を選んだ

**狙い:** CEA設立を「原発機関」か「兵器機関」のどちらかへ寄せず、科学・産業・国防を同じ国家機関が扱う出発点として描く。

**Positive prompt**
```text
Paris government office in October 1945, newly created atomic-energy commission staff seated around a table with three distinct folders for scientific research, industrial power development and national defense, uranium ore samples and laboratory apparatus beside state planning documents, no weapon or power plant dominating the image, postwar reconstruction atmosphere, no exact politician portraits or readable decree text, 16:9
```

**Negative prompt**
```text
atomic bomb on table, modern French reactor, exact CEA logo, readable decree, nationalistic propaganda, giant tricolor flag
```

### 1954/12/28 — ド・ゴールより先に始めてました

**狙い:** フランス核武装をド・ゴール一人の決断へ単純化せず、第四共和政下の官僚・軍・CEAで既に軍事研究組織ができていたことを描く。

**Positive prompt**
```text
mid-1950s French atomic-energy administrative office, civilian nuclear scientists, military officers and government administrators establish a small classified studies bureau inside a larger atomic-energy institution, filing cabinets and research plans fill the room, an empty later-leader portrait space deliberately left irrelevant, no exact Mendes-France or de Gaulle likeness, emphasis on bureaucratic continuity before 1958, no readable files, 16:9
```

**Negative prompt**
```text
de Gaulle as sole founder hero, readable BEG documents, atomic bomb blueprint, political campaign poster, modern office
```

### 1956–1958 — 同じ原子から二つの未来

**狙い:** マルクールの炉・発電・再処理から民生電力と軍事用プルトニウムが枝分かれするデュアルユース性を描く。

**Positive prompt**
```text
Marcoule France in the late 1950s, gas-graphite reactor buildings and early electrical generation equipment connected to a reprocessing facility, one material stream represented as electricity flowing to the grid while another sealed plutonium-bearing process stream goes into guarded state custody, no weapon assembly, balanced industrial composition showing civil and military branches sharing infrastructure, no readable signs, 16:9
```

**Negative prompt**
```text
bomb core, detailed plutonium separation recipe, exact facility flowchart, glowing radiation, modern French nuclear plant, propaganda poster
```

### 1960/02/13 — 青いトビネズミ

**狙い:** フランス初核実験を「第四の核大国」礼賛にせず、サハラの実験と植民地・脱植民地化の地理を同時に見せる。

**Positive prompt**
```text
French Sahara near Reggane in February 1960, distant nuclear test cloud over an empty desert test area with instrument towers and military observers far from ground zero, nearby map table includes Algeria's political transition context without readable labels, local desert workers and military infrastructure present but not caricatured, sober colonial-history undertone, no exact test photograph recreation, 16:9
```

**Negative prompt**
```text
triumphal French nuclear poster, giant flag, city destruction, local victims used as spectacle, exact Gerboise Bleue photo, bomb blueprint
```

### 1964/10/08 — 自分の核ボタン

**狙い:** 独自核戦力を「赤いボタン」ギャグにせず、Mirage IV部隊が他国の指揮系統と切り離された国家運用へ入ることとして描く。

**Positive prompt**
```text
1964 French strategic air-force base, Mirage IV bombers and tanker aircraft prepared on alert while a separate national command room receives orders through French-only communication channels, no NATO command staff present, aircraft shown externally without visible nuclear bomb details, emphasis on independent national decision chain rather than a literal launch button, no readable markings, 16:9
```

**Negative prompt**
```text
giant red nuclear button, bomb cutaway, launch procedures, exact Mirage squadron markings, de Gaulle portrait, patriotic propaganda
```

### 1966/03–07 — 同盟は抜けない。指揮系統は抜ける。

**狙い:** NATO脱退ではなく統合軍事機構からの離脱を、二つの制度の線を分けることで示す。

**Positive prompt**
```text
1966 diplomatic-military planning room, French delegation remains seated at an Atlantic alliance treaty table while French military command boxes and headquarters lines are physically moved out of a larger integrated command diagram, allied political connection remains intact, no exact flags or leader portraits, clear visual distinction between staying in the alliance and leaving integrated command, no readable labels, 16:9
```

**Negative prompt**
```text
France leaving NATO entirely, exact NATO logo, readable treaty article, de Gaulle propaganda portrait, giant flags, military confrontation with allies
```

### 1972/01/28 — 海の底にも共和国

**狙い:** フランス独自抑止が第二撃能力へ進む転換を、初SSBNの抑止哨戒出航で描く。

**Positive prompt**
```text
French Atlantic naval base in January 1972, first French ballistic-missile submarine departing quietly for patrol under gray winter sky, tugboats and dock workers small in foreground, no missile launch or exposed weapons, distant national command communications building suggested ashore, composition centered on hiding retaliatory capability at sea, no exact hull number or markings, 16:9
```

**Negative prompt**
```text
submarine cutaway, missile launch procedure, warhead details, exact Le Redoutable museum photo, heroic naval poster, readable markings
```

### 1974/03/06 — 中東に頭を下げるくらいなら

**狙い:** メスメル計画を反中東感情の絵にせず、石油危機後に輸入燃料依存を減らすため原発建設を国家規模で加速した政策として描く。

**Positive prompt**
```text
France in 1974 energy-planning office, oil-import price charts and tanker routes lie beside a nationwide map filled with multiple planned standardized reactor construction sites, engineers and government planners compare electricity-demand forecasts with domestic nuclear build schedules, no Middle Eastern people depicted and no hostile imagery, emphasis on energy autonomy through infrastructure, no readable numbers, 16:9
```

**Negative prompt**
```text
anti-Arab caricature, political slogan, exact Messmer portrait, giant cooling-tower propaganda, readable construction targets, modern renewable debate imagery
```

### 1995/09–1996/01 — これで最後だ

**狙い:** 仏核実験再開と終了を、一回の爆発ではなく「抗議の中で最後の試験系列を消化し、閉じる」過程として描く。

**Positive prompt**
```text
Mururoa Atoll in 1995-1996, remote underground nuclear-test infrastructure on a coral atoll with monitoring vessels offshore, international protest boats and distant demonstrators present outside the restricted zone, final test sequence represented by a row of completed blank test log cards ending at a closed folder, no surface nuclear blast and no exact activist logos, tense finality rather than triumph, 16:9
```

**Negative prompt**
```text
surface mushroom cloud over atoll, exact Greenpeace branding, exact Chirac portrait, readable test count, bomb design, celebratory French propaganda
```

### 2010/01/05 — 砂漠と環礁は忘れない

**狙い:** 核実験補償法を、実験史の後に残った健康影響と認定手続きの長期性として描く。

**Positive prompt**
```text
2010 French compensation-review office, elderly former workers and residents from Sahara and Polynesian test regions submit medical files while officials compare exposure maps and disease records, split background evokes desert test grounds and tropical atolls decades later, all personal data unreadable, no graphic illness, neutral administrative tone focused on delayed recognition and compensation, 16:9
```

**Negative prompt**
```text
graphic cancer imagery, exact claimant portraits, readable medical records, nuclear explosion spectacle, partisan compensation poster, tourism imagery
```

### 2023–2024 — 環境フリークはお得意様

**狙い:** タイトルの皮肉をドイツ人への嘲笑にせず、欧州電力市場で仏原発回復・独脱原発・再エネ・需要が混ざる実際の送電関係として描く。

**Positive prompt**
```text
2024 European cross-border electricity control center, French nuclear plants, German wind and solar farms, hydro reservoirs and major transmission interconnectors represented on a neutral grid map, power-flow arrows change direction according to market conditions, operators monitor supply and demand without national caricature, no claim that one technology alone explains trade, all numbers and country labels unreadable, 16:9
```

**Negative prompt**
```text
mocking German environmentalist caricature, France-versus-Germany propaganda, readable 89 TWh number, one-way permanent power arrow, giant cooling towers crushing wind turbines
```

### 1946 — 昨日まで一緒に作ってましたよね？

**狙い:** マクマホン法後の英米断絶を、共同開発の机から情報共有の扉が閉じる瞬間として描く。

**Positive prompt**
```text
1946 Anglo-American nuclear research office, British scientists who previously worked beside Americans now stand outside a newly restricted archive and information-control desk, wartime joint project photographs blurred in background while classified folders are returned behind a locked cabinet, no hostility or spy imagery, postwar policy rupture emphasized, no exact scientist portraits or readable law text, 16:9
```

**Negative prompt**
```text
British theft scene, readable McMahon Act, exact famous scientists, bomb blueprint, national caricature, modern security systems
```

### 1952/10/03 — じゃあ自分で作ります

**狙い:** 英国初核実験を単なる国威発揚にせず、戦後の情報遮断から独自能力を再構築した到達点として描く。

**Positive prompt**
```text
Montebello Islands off Australia in October 1952, British nuclear test conducted from a moored vessel in a remote bay, distant flash and rising cloud observed from instrument ships, engineers and military staff working quietly with test equipment, no city or civilians, visual context of an independent national test program rather than victory spectacle, no exact test photo recreation, 16:9
```

**Negative prompt**
```text
British imperial triumph poster, giant Union Jack, city destruction, bomb blueprint, exact Hurricane test photograph, cheering crowd
```

### 1957–1958 — 太陽も自前で

**狙い:** Grapple系列を一発で完成した水爆の神話にせず、複数試験を重ねて熱核能力へ到達した開発系列として描く。

**Positive prompt**
```text
late-1950s Pacific British thermonuclear test program, remote Christmas Island test infrastructure with a sequence of several blank test log panels and aircraft instrumentation missions, one distant megaton-scale cloud on the horizon while technicians compare results from previous shots, no weapon internals and no single-shot miracle framing, restrained experimental progression, 16:9
```

**Negative prompt**
```text
thermonuclear weapon cutaway, exact device design, giant national flag, exact test photo, triumphant propaganda, city destruction
```

### 1958/07/03 — また秘密を共有しましょう

**狙い:** 英国が能力を示した後に米英核協力が再開した逆説を、閉じていた情報経路が再接続される制度として描く。

**Positive prompt**
```text
1958 Anglo-American secure technical conference, British and American nuclear scientists exchange sealed research folders and material-accounting documents across a controlled table, previously locked archive cabinets now open under bilateral authorization, no weapon drawings visible, government security officers supervise, visual emphasis on renewed deep cooperation after independent British capability, no exact logos or readable agreement text, 16:9
```

**Negative prompt**
```text
detailed bomb plans, readable Mutual Defence Agreement, exact leaders, espionage scene, giant flags, propaganda handshake
```

### 1962/12–1963/04 — 独立してます。ミサイルは買います。

**狙い:** 英国の「独立核」が、政治判断は自国・運搬手段は米技術という混合構造であることを描く。

**Positive prompt**
```text
early-1960s British defense planning room, British national command chain remains on one side while a US-made Polaris missile procurement model and technical support crates arrive on the other, Royal Navy submarine design team links the purchased missile system into a British-controlled deterrent architecture, no exposed warhead or detailed engineering, no exact leader portraits, 16:9
```

**Negative prompt**
```text
readable sales agreement, missile cutaway, launch procedures, British subordination caricature, exact Macmillan or Kennedy portrait, patriotic propaganda
```

### 1969/04～ — 一隻は必ず海の中

**狙い:** CASDをミサイル発射ではなく、世代を越えて一隻が必ず哨戒中という継続運用で描く。

**Positive prompt**
```text
British ballistic-missile submarine cycle from 1969 onward, one submarine quietly departs port as another returns and a third undergoes maintenance, while a fourth remains invisible beneath a wide gray Atlantic shown only as a faint underwater silhouette, no launch or target map, visual emphasis on continuous patrol rotation sustaining second-strike capability for decades, no exact hull markings, 16:9
```

**Negative prompt**
```text
missile launch, submarine cutaway, exact patrol routes, warhead details, action-movie chase, giant Union Jack
```


---

## 各国・地域の核史 ― 中国とイスラエル

### 1957/10/15 — 同志、そこまで教えてくれるんですか

**狙い:** 中国核開発の初期がソ連技術移転に大きく依存していたことを、研究設備・模型・資料の受け渡しで描く。

**Positive prompt**
```text
late-1950s Sino-Soviet technical cooperation meeting, Soviet engineers and Chinese scientists examining generic reactor, enrichment and missile-development training models on a table, sealed technical manuals and laboratory equipment being transferred under formal supervision, no detailed weapon design and no exact leader portraits, cooperative but strategic atmosphere, no readable documents or national slogans, 16:9
```

**Negative prompt**
```text
detailed nuclear weapon blueprint, readable Soviet technical manuals, Mao portrait, Khrushchev portrait, propaganda friendship poster, operational missile instructions
```

### 1958 — 鉄は裏庭で、原爆は国家で

**狙い:** 大躍進の分散的大衆動員と、核計画の専門家集中という国家能力の非対称を左右対比で描く。

**Positive prompt**
```text
China in 1958 shown as a restrained split editorial composition: one side has chaotic village backyard furnaces with poorly made scrap metal and mass labor, the other side has a guarded professional nuclear research institute with trained scientists, precise instruments and centralized supply deliveries, no caricature of ordinary people, visual emphasis on dispersed political mobilization versus concentrated technical state project, no readable slogans, 16:9
```

**Negative prompt**
```text
mocking peasants, famine corpses, Mao propaganda poster, atomic bomb on laboratory table, readable Great Leap slogans, nationalist triumph imagery
```

### 1959/06/20 — 596

**狙い:** ソ連援助撤回を、数字のロゴ化ではなく「予定されていた模型・資料が届かなくなる」技術断絶として描く。

**Positive prompt**
```text
June 1959 Chinese nuclear research office, expected Soviet technical crates and model-delivery documents are abruptly marked canceled or removed while Chinese engineers remain around partially established laboratories and domestic project files, a calendar page and empty transport space suggest sudden withdrawal of promised assistance, no readable project number or political slogans, no exact leader portraits, 16:9
```

**Negative prompt**
```text
giant readable 596 text, anti-Soviet propaganda caricature, detailed weapon plans, exact diplomatic document, Mao portrait, Khrushchev portrait
```

### 1959–1962 — 飢饉でも、この計画は止めない

**狙い:** 大飢饉をショック描写で消費せず、社会全体が危機に陥る中でも核計画へ優先資源が流れ続けた政策判断を描く。

**Positive prompt**
```text
early-1960s China, austere state logistics hub where scarce rail cars, fuel drums and technical equipment are preferentially routed toward a guarded nuclear research complex while ordinary regional supply lines appear strained and sparse in the background, officials and engineers prioritize a narrow strategic project amid broader economic hardship, no starving bodies or sensational suffering, no readable directives, 16:9
```

**Negative prompt**
```text
famine corpses, grotesque hunger imagery, propaganda celebration, exact resource orders, bomb blueprint, simplistic evil-state caricature
```

### 1964/10/16 — 本当に飛躍したのはこっち

**狙い:** 初核実験成功を「大躍進の成功」にすり替えず、別系統の国家集中プロジェクトが兵器能力へ到達した事実として描く。

**Positive prompt**
```text
Lop Nur test range in October 1964, distant first Chinese nuclear test cloud over a barren desert while instrumentation teams and scientific observers work from remote shelters, no crowd celebration, a faint visual echo of abandoned backyard furnaces far outside the test context underscores contrast without mockery, emphasis on concentrated technical program reaching a milestone despite broader policy failure, no readable slogans, 16:9
```

**Negative prompt**
```text
Mao propaganda poster, giant Chinese flag, city destruction, detailed device design, triumphant military parade, exact test photograph recreation
```

### 1967/06/17 — 今度こそ大躍進

**狙い:** 原爆から水爆へ約32か月という技術的飛躍を、社会政策の成功と混同せず試験系列の短さで示す。

**Positive prompt**
```text
1967 Lop Nur thermonuclear test program, remote instrumentation center with a short sequence of dated but unreadable test folders linking the 1964 fission milestone to a much larger 1967 thermonuclear test cloud on the horizon, scientists compare results under strict state-project conditions, no city and no social-policy celebration, visual emphasis on unusually rapid weapons-development progression, no device internals, 16:9
```

**Negative prompt**
```text
detailed hydrogen-bomb design, readable 32 months text, Great Leap propaganda, city destruction, Mao portrait, victory parade
```

### 1950年代末～1960年代 — 砂漠の中の研究所

**狙い:** ディモナを「秘密核兵器工場」と断定せず、研究施設の外形と軍事能力の可能性が重なるデュアルユース問題として描く。

**Positive prompt**
```text
Negev Desert in the early 1960s, isolated research-reactor complex near Dimona with reactor building, laboratories and guarded service roads, civilian scientific activity visible but some areas remain opaque behind security fencing, American inspection interest suggested by visiting technical observers and aerial survey folders, no exposed weapons or definitive military label, restrained ambiguity, no readable signs, 16:9
```

**Negative prompt**
```text
visible Israeli nuclear warhead, definite bomb factory label, exact Dimona aerial photo, spy-thriller scene, giant flags, readable classified map
```

### 1963～ — 最初には持ち込みません

**狙い:** “introduce” の意味を意図的に曖昧にした定型句を、言葉の定義が書き換わる外交文書として描く。

**Positive prompt**
```text
1960s US-Israel diplomatic meeting, negotiators examine a short statement on a page where one key English verb is visibly present only as an unreadable blurred block surrounded by several competing marginal interpretations, sealed nuclear-policy folders remain closed, no weapons shown, visual emphasis on deliberate semantic ambiguity rather than deception thriller, no exact leader portraits, 16:9
```

**Negative prompt**
```text
readable quoted phrase, dictionary joke, exact diplomatic memorandum, nuclear bomb on table, leader caricatures, partisan propaganda
```

### 1960年代後半～ — ボクも持ってるかもしれませんよ？

**狙い:** amimutを「ウインクする国家キャラ」にせず、能力を示唆しつつ公式確認を避ける長期政策として描く。

**Positive prompt**
```text
late-1960s strategic editorial scene, guarded desert nuclear infrastructure, long-range aircraft and missile-capable systems remain partially visible through haze while an official press podium stands empty of any confirmation statement, intelligence analysts abroad compare indirect clues without a definitive declaration, no weapon itself displayed, sustained ambiguity rather than playful wink, no readable text, 16:9
```

**Negative prompt**
```text
cartoon wink, explicit Israeli nuclear warhead, readable declaration, exact missile inventory, propaganda poster, spy thriller
```

### 1969 — 知らないことにしておきましょう

**狙い:** 米側も問題を前面化しない方向へ進んだことを、正式承認ではなく「問わない／公表しない」という相互沈黙の制度で描く。

**Positive prompt**
```text
1969 Washington diplomatic office, American and Israeli officials leave a sensitive nuclear-policy folder closed between them while a public press statement stack deliberately omits the subject, background intelligence photographs remain face down, no handshake celebration and no formal recognition certificate, visual emphasis on mutual restraint in what would be publicly asked or acknowledged, no exact Nixon or Meir portraits, 16:9
```

**Negative prompt**
```text
formal treaty recognizing nuclear weapons, readable secret agreement, exact Nixon portrait, exact Golda Meir portrait, exposed warhead, conspiracy-thriller red strings
```


---

## 各国・地域の核史 ― 南アジアと北朝鮮

> 南アジアのゲーム文化由来2件は既存作品・ミームへの接近を避けるため生成除外を維持。それ以外は全件手動監査済み。

### 1947/08 — 二つに分ければ終わる……？

**狙い:** 印パ分離を国境線一本の政治地図にせず、人口移動と直後のカシミール紛争が核対立の前史になったことを描く。

**Positive prompt**
```text
South Asia in August 1947, crowded railway platforms and long civilian migration columns moving in opposite directions across a newly established border while a distant mountainous Kashmir map area remains unresolved and militarized, families carry ordinary household belongings rather than weapons, no graphic communal violence, sober historical composition emphasizing partition and unfinished territorial conflict, no readable place names, 16:9
```

**Negative prompt**
```text
graphic massacre, religious caricature, exact political border map, national propaganda, nuclear weapons, modern flags dominating frame
```

### 1948/01/30 — 非暴力の使徒、暴力に斃れる

**狙い:** ガンジー暗殺を「核ガンジー」ミームへ接続せず、独立後の宗派間融和を訴えていた人物が政治的暴力で殺された史実として描く。

**Positive prompt**
```text
New Delhi prayer gathering in January 1948, elderly Indian independence leader in simple white clothing walking toward a small crowd with hands gently joined, a sudden disturbance occurs at the edge of the gathering while the fatal violence itself remains off-frame, mourners and attendants react in shock, respectful historical distance, no exact photographic recreation and no game references, 16:9
```

**Negative prompt**
```text
graphic gunshot wound, blood, Nuclear Gandhi meme, Civilization game imagery, exact assassination photograph, political propaganda, caricature
```

### 1971 — 国境はもう一度動く

**狙い:** 1971年戦争を戦闘スペクタクルにせず、東パキスタンからバングラデシュ独立へ国境と国家構造が再び変わったことを描く。

**Positive prompt**
```text
South Asia in 1971, refugee columns crossing muddy border roads while a large unlabeled map in the background shows Pakistan's eastern wing separating into a new state, military vehicles remain distant and secondary, humanitarian and geopolitical transformation emphasized without graphic combat, no readable country labels, no nuclear imagery, 16:9
```

**Negative prompt**
```text
battlefield gore, exact war propaganda, national humiliation caricature, nuclear weapons, readable map labels, modern satellite map
```

### 1972 — 次は負けられない

**狙い:** パキスタン核計画本格化を、復讐の感情絵ではなく1971年敗戦後の安全保障政策・科学計画への資源集中として描く。

**Positive prompt**
```text
Pakistan in early 1972, senior civilian leaders, military officials and nuclear scientists gathered at a secure planning meeting after the recent national defeat, map of South Asia and files for laboratories, uranium research and industrial facilities spread across the table, no bomb model and no exact politician portraits, somber state-security project beginning rather than revenge propaganda, no readable documents, 16:9
```

**Negative prompt**
```text
nuclear bomb blueprint, readable Multan meeting notes, exact Bhutto portrait, revenge slogan, anti-India caricature, mushroom cloud
```

### 1974/05/18 — 平和的核爆発です

**狙い:** インド初核爆発を、政府呼称と技術上の軍民不可分性の緊張として描く。

**Positive prompt**
```text
Pokhran desert test site in May 1974, underground nuclear test evidenced by a rising dust mound and distant monitoring equipment rather than a towering mushroom cloud, government press desk in foreground holds a folder labeled only by blank lines suggesting a 'peaceful' civil-engineering rationale, foreign nuclear-supply officials examine safeguards concerns separately, no exact device design or readable wording, 16:9
```

**Negative prompt**
```text
readable peaceful nuclear explosion slogan, Nuclear Gandhi imagery, bomb blueprint, giant Indian flag, city destruction, exact test photograph
```

### 1998/05/28–30 — ならば、こちらも

**狙い:** パキスタン核実験を単なる対抗心ではなく、17日前のインド実験と国内・国際圧力の中で選ばれた政策判断として描く。

**Positive prompt**
```text
Chagai Hills region in May 1998, remote underground test mountains and instrumentation site under harsh daylight, Pakistani officials in a command center review foreign diplomatic cables and recent Indian test reports while domestic newspaper bundles remain unreadable, no triumphant crowd and no city target, emphasis on reciprocal escalation under pressure, no exact leader portraits, 16:9
```

**Negative prompt**
```text
giant national flag, celebratory nuclear poster, exact Chagai propaganda photo, readable diplomatic messages, bomb cutaway, anti-India caricature
```

### 1999 — 核を持っても戦争はなくならない

**狙い:** カルギル紛争を「核抑止失敗」と断定せず、核保有下でも限定的通常戦闘が発生し、全面戦争への拡大管理が問題になった事例として描く。

**Positive prompt**
```text
Kargil mountain front in 1999, small conventional infantry positions and artillery activity across high snowy ridges while far behind both sides abstract nuclear-deterrence symbols remain inactive and sealed in command centers, no nuclear use or city targets, tense limited-war composition emphasizing that conventional fighting can continue under a nuclear shadow, no exact unit markings, 16:9
```

**Negative prompt**
```text
nuclear explosion, graphic casualties, detailed battlefield tactics, exact military positions, propaganda victory scene, national caricature
```

### 1985/12/12 — 条約には入りました

**狙い:** 北朝鮮NPT加入と保障措置協定の遅れを、加盟署名と未完の査察制度の時間差として描く。

**Positive prompt**
```text
mid-1980s international treaty office, North Korean delegation submits accession papers to a global nonproliferation treaty while a separate safeguards agreement folder remains blank and unsigned on another desk, nuclear-research facility records wait for future inspection, no exact political leader portraits or flags dominating, institutional time-gap emphasized, no readable treaty text, 16:9
```

**Negative prompt**
```text
partisan rogue-state caricature, readable NPT clauses, nuclear bomb, exact leader portrait, propaganda poster, modern IAEA logo
```

### 1993/03/12–06/11 — 脱退します……いったん保留

**狙い:** NPT脱退通告が期限直前に「発効停止」され、法的曖昧さを残した状態を時計と二つの文書で示す。

**Positive prompt**
```text
1993 diplomatic crisis desk, one formal withdrawal notice lies beside a treaty calendar approaching a deadline while a second US-North Korean joint statement places a pause marker over the process, diplomats on both sides remain separated by a table, all dates and text unreadable, visual emphasis on a withdrawal procedure suspended rather than cleanly canceled, no exact leaders, 16:9
```

**Negative prompt**
```text
readable legal text, cartoon pause button, nuclear explosion, exact political portraits, partisan propaganda, modern conference room
```

### 1994/10/21 — 凍結します

**狙い:** 米朝枠組み合意を「非核化達成」とせず、既存黒鉛炉・関連施設の凍結と軽水炉・重油供給の交換として描く。

**Positive prompt**
```text
1994 nuclear agreement editorial scene, Yongbyon-style graphite reactor and reprocessing-related facilities shown powered down and sealed under monitoring while on the opposite side construction plans for two light-water reactors and fuel-oil deliveries are prepared, inspectors present but past plutonium-accounting files remain unresolved, no exact facility blueprint or leader portraits, no readable agreement text, 16:9
```

**Negative prompt**
```text
complete denuclearization celebration, weapon dismantlement not in agreement, exact Yongbyon aerial photo, readable Agreed Framework clauses, partisan propaganda
```

### 2003/01/10–11 — 条約は抜けられます

**狙い:** 2003年脱退を「条約違反」と画像で決めつけず、1993年の残り通知期間を数える北朝鮮の主張と法的論争を描く。

**Positive prompt**
```text
January 2003 international law and diplomacy scene, old 1993 withdrawal notice reopened beside a calendar with only a few blank remaining days while treaty lawyers and diplomats compare Article 10 procedures in separate folders, North Korean delegation announces resumed withdrawal from a podium at distance, no exact leader portraits, neutral legal ambiguity, all text unreadable, 16:9
```

**Negative prompt**
```text
readable treaty law, courtroom guilty verdict, partisan state caricature, nuclear launch, exact government propaganda imagery
```

### 2006/10/09 — ならず者国家、「成る」

**狙い:** 「ならず者国家」を客観分類として採用せず、初核実験によって不拡散側が最も懸念した能力が現実化した事実を遠隔検知で描く。

**Positive prompt**
```text
October 2006 northeast Asia, remote underground test site in North Korea indicated only by a subtle ground disturbance while regional seismic stations record an unusual signal and an atmospheric sampling aircraft collects trace gases, international analysts compare data in separate rooms, no triumphant test propaganda or leader portrait, emphasis on externally verifying a claimed nuclear test, 16:9
```

**Negative prompt**
```text
readable rogue state label, giant North Korean flag, mushroom cloud, exact test-tunnel layout, exact Kim Jong Il portrait, propaganda caricature
```

### 2018/06/12 — 完全な非核化へ……？

**狙い:** シンガポール会談を握手写真の再現にせず、大枠の言葉は合意したが工程表が空白だったことを文書構造で描く。

**Positive prompt**
```text
Singapore summit setting in June 2018, American and North Korean leaders shown only as distant non-identifying figures seated across a table after a formal meeting, a short joint statement folder lies signed while beside it a much thicker implementation binder remains visibly blank, nuclear-site maps and verification checklists are absent or unopened, no exact portraits or readable text, balanced diplomatic tone, 16:9
```

**Negative prompt**
```text
exact Trump or Kim Jong Un portrait, exact handshake photo, readable summit statement, partisan victory poster, nuclear explosion
```

### 2019/02/28 — ディール不成立

**狙い:** ハノイ会談失敗を人物ドラマではなく、寧辺廃棄範囲・制裁解除範囲・検証の交換条件が噛み合わなかった交渉として描く。

**Positive prompt**
```text
Hanoi summit room in February 2019 after talks break down, two delegations leave a conference table with unsigned joint statement pages and untouched lunch settings, one side's folder contains a generic nuclear-facility dismantlement map while the other contains sanctions lists, all details unreadable and neither visually privileged, no exact leader portraits, unresolved transaction rather than theatrical confrontation, 16:9
```

**Negative prompt**
```text
exact Trump or Kim portrait, readable sanctions list, mocking failed-deal cartoon, shouting match, propaganda poster, nuclear explosion
```

### 2022/09/08 — 平和のための核です

**狙い:** 北朝鮮核ドクトリンを宣伝文句として反復せず、抑止を第一目的としつつ危機時の先使用・自動性圧力も含む法制度として描く。

**Positive prompt**
```text
2022 North Korean state policy office represented neutrally, formal nuclear-forces law document on a desk with several abstract contingency branches leading from deterrence posture to emergency-use conditions, one branch shows disrupted command communications triggering a pre-authorized response concept without operational details, officials and military staff shown small and non-identifying, no missiles launching, all legal text unreadable, 16:9
```

**Negative prompt**
```text
readable nuclear-use law, launch codes, operational target plans, exact Kim Jong Un portrait, propaganda mural, partisan endorsement or ridicule
```


---

## 思想史の横道 ― 進歩の夢から自己破壊へ

### 1627 — 科学と工学でユートピアを

**狙い:** 『ニュー・アトランティス』を書影再現にせず、組織化された研究が社会を豊かにするという「ソロモンの館」の発想を独自構図で描く。

**Positive prompt**
```text
early-17th-century imagined research institution inspired by Baconian natural philosophy, scholars divided among observatory, botanical garden, mechanical workshop, specimen collection and experimental chamber inside one orderly civic complex, citizens receive practical inventions and medicines outside, architectural and editorial original composition rather than book illustration recreation, hopeful but grounded premodern atmosphere, no readable text or exact New Atlantis artwork, 16:9
```

**Negative prompt**
```text
exact historical book illustration, readable New Atlantis text, modern laboratory, steampunk fantasy city, magical alchemy, Francis Bacon portrait
```

### 1751/06/28 — 知識を集めれば、世界は良くなる

**狙い:** 『百科全書』を表紙ではなく、学問・工芸・機械仕事の知識を編集・図版化・印刷して共有する巨大出版事業として描く。

**Positive prompt**
```text
Paris printing and engraving workshop around 1751, editors compare manuscripts from science, crafts and mechanical trades while engravers prepare detailed but non-readable plates of tools and workshops, printers operate hand presses and stacks of bound volumes accumulate, artisans demonstrate techniques to illustrators, Enlightenment atmosphere of organizing practical knowledge for publication, no exact Encyclopedie page reproduction or portraits, 16:9
```

**Negative prompt**
```text
exact Encyclopedie engraving, readable French text, Diderot portrait, modern printing press, fantasy library, glowing knowledge symbols
```

### 18世紀後半〜19世紀 — 煙突と曇り空の帝国

**狙い:** 産業革命を蒸気機関一台にせず、工場・鉄道・都市化と煤煙・労働環境が同時に拡大する風景として描く。

**Positive prompt**
```text
British industrial city during the early 19th century, textile mills and foundries with tall smoking chimneys, steam locomotive crossing a viaduct, canal barges, dense worker housing and crowded factory gates, prosperity and transformed mobility visible alongside soot-darkened sky and harsh labor conditions, broad documentary panorama without nostalgia or dystopian exaggeration, no readable signs, 16:9
```

**Negative prompt**
```text
steampunk fantasy, pristine Victorian postcard, child-labor gore, modern skyscrapers, exact painting recreation, readable advertisements
```

### 1794/06/08 — 理性で宗教を作ります

**狙い:** 最高存在の祭典を単なる奇祭ではなく、革命政府が象徴・祝祭・道徳まで国家的に設計した市民宗教として描く。

**Positive prompt**
```text
Paris Festival of the Supreme Being in June 1794, vast civic procession and carefully staged artificial landscape with symbolic mountain, flowers and classical decorations, republican officials and citizens participating in a state-designed public ritual, composition inspired by documented festival elements but not reproducing Jacques-Louis David's drawings, no supernatural deity visible, no readable slogans, 16:9
```

**Negative prompt**
```text
exact David artwork recreation, supernatural god figure, readable revolutionary banners, guillotine spectacle, caricature of atheism or religion, modern festival
```

### 1820年代 — 歴史には進行方向があります

**狙い:** ヘーゲルの歴史哲学を矢印一本の「進歩チャート」にせず、講義室で革命・国家・自由の歴史を一つの体系として読む営みで描く。

**Positive prompt**
```text
1820s Berlin university lecture hall, philosophy professor seen from behind addressing students while a large chalkboard contains unreadable layered sketches of ancient polities, revolution and modern constitutional institutions connected through revisions rather than a simple upward arrow, shelves of history books and maps around the room, serious attempt to find meaning and freedom in historical change, no exact Hegel portrait, 16:9
```

**Negative prompt**
```text
simple inevitable-progress arrow, readable dialectic formula, exact Hegel portrait, political propaganda, modern lecture hall, mystical spirit figure
```

### 1830 — 社会にも法則があります

**狙い:** コントの実証主義を「社会を物理式で完全予測」する絵にせず、自然科学に続いて社会も観察・比較の対象にしようとする講義体系として描く。

**Positive prompt**
```text
Paris lecture room around 1830, lecturer organizes astronomy, physics, chemistry, biology and social observations across separate shelves and specimen tables, census-like records, city maps and comparative historical notes occupy the final desk, all text unreadable, visual emphasis on extending systematic observation toward society rather than reducing people to equations, no exact Comte portrait, 16:9
```

**Negative prompt**
```text
society controlled by equations, readable hierarchy of sciences, exact Comte portrait, futuristic social-engineering dashboard, propaganda poster
```

### 1915/04/22 — 科学は塹壕にも来ました

**狙い:** 毒ガスを残酷描写で消費せず、化学工業・気象・容器・軍組織が結びついて研究物質が兵器体系へ入った構造を描く。

**Positive prompt**
```text
Second Battle of Ypres in April 1915, distant trench line under a low drifting chlorine gas cloud released from rows of industrial cylinders, soldiers react by improvising protection and withdrawing, a secondary inset shows chemical factory filling cylinders and weather officers studying wind direction, no close-up dying bodies, sober connection between modern industry, science and battlefield weaponization, muted green-gray natural gas color without fantasy glow, 16:9
```

**Negative prompt**
```text
graphic choking deaths, gore, gas-mask horror close-up, modern chemical weapons, exact wartime photograph, heroic military propaganda
```

### 1929 — 世界を科学的に把握します

**狙い:** ウィーン学団を人物集合写真にせず、「何を意味ある科学的命題とするか」を論理・物理・経験の資料で議論する場として描く。

**Positive prompt**
```text
Vienna intellectual seminar in 1929, philosophers, mathematicians and scientists around a cafe-like table compare symbolic logic pages, relativity diagrams, observational reports and social-science data, all writing deliberately unreadable, metaphysical books set aside rather than burned, lively analytical discussion in interwar European setting, no exact Carnap, Hahn or Neurath portraits, 16:9
```

**Negative prompt**
```text
readable manifesto, exact Vienna Circle group photo, mystical symbols exploding, anti-religion propaganda, modern academic conference
```

### 1945/07/16 — 科学は成功しました

**狙い:** トリニティ火球の別カットにせず、核物理・工場・計算・爆薬・軍事行政が一つの成果へ統合された「巨大R&Dの成功」を描く。

**Positive prompt**
```text
1945 Manhattan Project systems montage rendered as one coherent editorial scene: physicists at Los Alamos calculation tables, Oak Ridge industrial enrichment halls, Hanford reactor and chemical plant, explosives diagnostics, military logistics and a distant Trinity test tower all connected by flows of crates, reports and personnel, final pre-dawn flash visible only as a small far horizon element, emphasis on organizational and engineering integration accomplishing a difficult goal, no exact photographs or weapon internals, 16:9
```

**Negative prompt**
```text
giant glamorous mushroom cloud, simple 'science bad' symbolism, detailed bomb blueprint, exact scientist portraits, readable project documents, propaganda triumph poster
```

### 1983/12/23 — 科学と工学で自滅できるようになりました

**狙い:** 核の冬を確定した未来予言としてではなく、煙・日射・気候・農業の連鎖をモデル計算で問題化した科学研究として描く。

**Positive prompt**
```text
early-1980s climate-modeling research room, scientists work at large mainframe terminals and paper maps showing several hypothetical smoke plumes spreading into the upper atmosphere, separate panels connect reduced sunlight to colder agricultural landscapes and stressed crop fields, all numerical results unreadable and uncertainty bands visible, no actual global nuclear war shown, emphasis on modeling civilization-scale consequences with uncertainty, 16:9
```

**Negative prompt**
```text
definitive frozen Earth prophecy, city nuclear explosions, readable TTAPS graph, exact Carl Sagan portrait, apocalypse movie poster, climate certainty slogan
```

---

## 科学史の横道

### 1919 — 元素は壊せる

**狙い:** 人工核変換を「酸素生成を直接見た」と誤解させず、窒素照射で水素核が飛び出す観測そのものを描く。

**Positive prompt**
```text
1919 Cavendish laboratory, alpha source aimed into a nitrogen-filled chamber while scintillation detector records unexpected fast hydrogen nuclei emerging, researcher peers through a microscope at tiny flashes, a later interpretive notebook suggests elemental transmutation only abstractly and unreadably, no direct oxygen sample displayed, period brass apparatus, 16:9
```

**Negative prompt**
```text
visible oxygen atom product labeled, giant alchemy symbol, modern detector, exact Rutherford portrait, nuclear bomb, readable reaction equation
```

### 1941/10/01 — 錬金術の夢

**狙い:** 水銀→金を錬金術の成功譚にせず、微量の放射性金同位体を作れても経済合理性がない核反応として描く。

**Positive prompt**
```text
1941 nuclear physics laboratory, neutron source irradiates a tiny mercury sample inside shielded apparatus, chemists later isolate an almost microscopic gold-colored deposit in a small vial while large expensive laboratory equipment fills the room, an old alchemical manuscript sits closed in the corner as historical contrast, no treasure pile or magical transformation, no readable isotope labels, 16:9
```

**Negative prompt**
```text
pile of gold bars, magic alchemy glow, philosopher's stone, profitable gold factory, readable Au-198 labels, modern reactor
```

### 1980 — 金より高い金

**狙い:** Bevalacの元素変換を「金製造技術」と誤解させず、巨大加速器で数千原子を作る採算崩壊をスケール差で描く。

**Positive prompt**
```text
1980 Lawrence Berkeley heavy-ion accelerator facility, massive beamline and magnets operate to bombard a tiny bismuth target, researchers collect an extremely small sample represented by a few detector counts while operating-cost paperwork and industrial-scale machinery dwarf the result, no literal visible gold nugget, wry scientific tone without cartoon humor, no readable numbers or logos, 16:9
```

**Negative prompt**
```text
gold bars, profitable transmutation machine, readable cost figures, exact Bevalac photo, sci-fi particle cannon, treasure imagery
```

### 1934/03/17 — 地上でも、くっつきました

**狙い:** D-D核融合を発電研究と混同せず、加速した重水素核を標的へ当てて反応生成物を検出する初期実験として描く。

**Positive prompt**
```text
1934 Cavendish laboratory, compact accelerator directs deuterium ions into a deuterated target while simple detectors on two sides register fast protons and neutrons from fusion reactions, researchers operate vacuum tubes and high-voltage equipment, no plasma confinement machine and no power generation, restrained experimental breakthrough, no readable reaction formulas, 16:9
```

**Negative prompt**
```text
tokamak, commercial fusion power, hydrogen bomb, miniature sun, modern accelerator, readable D-D equation
```

### 1939–1957 — 星は元素工場だった

**狙い:** 恒星核融合と元素合成を教科書図そのままにせず、観測スペクトル・理論計算・星内部モデルが結びつく研究として描く。

**Positive prompt**
```text
mid-20th-century astrophysics study, stellar spectra on photographic plates, hand calculations and a layered cutaway model of a star showing progressively different burning regions through color and texture without readable labels, astronomers compare observations to nuclear-reaction theory, later shelves of element-abundance data extend the work into nucleosynthesis, no exact portrait of Bethe, Hoyle or Burbidges, 16:9
```

**Negative prompt**
```text
textbook periodic table, giant readable reaction chains, fantasy star interior, exact scientist portraits, nuclear weapon imagery
```

### 1957～ — 星は鉄まで燃やしているらしい

**狙い:** 大質量星の燃焼段階を「玉ねぎ図」のコピーにせず、後の段階ほど短くなる層状進化として描く。

**Positive prompt**
```text
scientific editorial cutaway of a massive aging star based on mid-20th-century stellar-evolution theory, broad outer hydrogen and helium burning shells surrounding progressively thinner inner carbon, neon, oxygen and silicon burning regions, dense iron-rich core at center, nearby laboratory clock sequence or stacked observation notes subtly indicate shortening timescales, no readable element labels, original non-textbook composition, 16:9
```

**Negative prompt**
```text
exact textbook onion-shell diagram, readable element names, fantasy star explosion, nuclear bomb comparison, overly decorative space art
```

### 1957～ — 鉄で終わりです

**狙い:** 鉄族核付近で融合によるエネルギー獲得が行き詰まることを、結合エネルギーの山と重力崩壊前の星で表す。

**Positive prompt**
```text
astrophysics editorial scene, massive star with compact iron-rich core reaches a stalled final burning stage while a smooth unlabeled binding-energy curve on a nearby blackboard rises to a broad maximum near the middle and no longer rewards further fusion, outer stellar layers press inward under gravity, no supernova yet, no readable chemical symbols or equations, 16:9
```

**Negative prompt**
```text
readable iron label, exact textbook graph, immediate colorful supernova, nuclear weapon, fantasy black hole portal
```

### 1963/10/17 — 核実験を宇宙から見張る

**狙い:** Vela衛星を宇宙天文学ミッションとしてではなく、核実験禁止条約の検証用センサーとして描く。

**Positive prompt**
```text
1963 early American monitoring satellite in high Earth orbit with simple boxy body and radiation detectors scanning Earth for atmospheric or space nuclear-test signatures, ground analysts compare X-ray, gamma-ray and neutron sensor channels on analog equipment, treaty-verification context present through sealed documents but no exact logos, utilitarian Cold War surveillance mission rather than astronomy glamour, 16:9
```

**Negative prompt**
```text
modern telescope satellite, exact Vela blueprint, nuclear explosion over city, readable treaty text, spy-satellite camera fantasy, sci-fi spacecraft
```

### 1967/07/02 — これは核実験ではない

**狙い:** 最初のGRB記録を「その場で宇宙起源が判明した」ようにせず、監視器が説明不能な短い信号を拾った異常値として描く。

**Positive prompt**
```text
1967 Vela satellite monitoring room, analog strip-chart recorders show a sudden short gamma-ray spike that does not match expected nuclear-test timing patterns, puzzled analysts compare signals from two satellites and leave the source location uncertain, Earth and Sun diagrams remain crossed out only as later hypotheses, no dramatic cosmic source shown, no readable graph values, 16:9
```

**Negative prompt**
```text
visible gamma-ray burst galaxy at discovery moment, readable GRB 670702 label, nuclear explosion, modern digital displays, certainty about source location
```

### 1973/06/01 — 宇宙からの雷鳴

**狙い:** GRBが正式な天文学対象になるまで、複数年のVela記録を比較して地球・太陽起源を除外した解析を描く。

**Positive prompt**
```text
early-1970s Los Alamos analysis room, researchers spread many Vela burst timing records across a large table and compare detections from widely separated satellites, triangulation sketches point away from Earth and Sun toward an unknown cosmic sky with no specific source object, scientific paper manuscript prepared for publication but text unreadable, no exact scientist portraits, 16:9
```

**Negative prompt**
```text
specific neutron star merger shown before known, readable paper title, modern computer visualization, exact scientist portraits, nuclear blast
```

### 2017/08/17 — 宇宙が鳴って、光った

**狙い:** GW170817を重力波とガンマ線の「同じ現象を別の窓で観測した」マルチメッセンジャー事件として描く。

**Positive prompt**
```text
August 2017 multi-messenger astronomy editorial scene, two neutron stars merge in a distant galaxy while on Earth separate gravitational-wave interferometers register a chirp and gamma-ray satellites detect a short flash seconds later, optical telescopes around the world turn toward the same patch of sky, all instruments connected only conceptually and no readable data values, scientifically grounded rather than fantasy space art, 16:9
```

**Negative prompt**
```text
nuclear weapon explosion, audible sound waves traveling through space, readable GW170817 charts, exact observatory publicity photo, fantasy spaceship
```

---

## 追加手調整プロンプト — 被爆・記憶

> 以下は自動補完でも生成できるが、資料写真の直接再現やショック演出へ寄らないよう、構図を明示しておくカード。

### 1945/08/06 — ターゲットはT字橋

**狙い:** 「都市」ではなく、上空から識別しやすい一本の橋が照準点になったことを見せる。

**Positive prompt**
```text
Hiroshima on the morning of August 6 1945 viewed from a high oblique aerial perspective, the distinctive T-shaped Aioi Bridge and surrounding river channels clearly readable as a geographic landmark, a distant B-29 silhouette high above and offset from the bridge, intact pre-blast urban blocks below, restrained ominous calm before the bombing, original map-like editorial composition without copying any wartime reconnaissance photograph, no explosion, no readable labels, 16:9
```

**Negative prompt**
```text
nuclear explosion, mushroom cloud, destroyed city, targeting reticle, bomb sight UI, detailed weapons diagram, readable map labels, exact recreation of reconnaissance photography, heroic aircraft poster
```

### 1945/08/06 — 三人分の制服

**狙い:** 三人の学生の生活を、遺体ではなく制服・帽子・帯革・ゲートルの断片として示す。

**Positive prompt**
```text
respectful still-life editorial illustration of three separate sets of 1945 Japanese middle-school clothing fragments and personal school items arranged with clear spacing on a plain neutral surface, one cap and belt grouping, one dark student uniform grouping, one pair of gaiters grouping, subtle scorched and damaged fabric without graphic bodily traces, each grouping distinct to suggest three different students, quiet memorial tone, original arrangement not matching any museum display or catalog photograph, no readable names, 16:9
```

**Negative prompt**
```text
bodies, gore, burned flesh, exact museum showcase, catalog-photo lighting, mannequin wearing the items, school anime character, modern school uniform, readable name tags, sentimental halo
```

### 1945/08/06 — たまたま地下室にいただけで

**狙い:** 生死を分けた「地下にいた」という偶然を、階段と遮蔽で見せる。

**Positive prompt**
```text
interior of a 1945 Japanese elementary-school basement near central Hiroshima, heavy masonry walls and a short stairway rising toward an overexposed blast-lit entrance, a small child seen only from behind crouched low beside removed shoes, debris and dust entering from above while the underground space remains structurally sheltered, strong contrast between protected darkness below and destructive light above, no identifiable survivor portrait, no bodies, original reconstruction based on general historical context, 16:9
```

**Negative prompt**
```text
graphic casualties, dead children, exact portrait of a known survivor, modern school basement, nuclear fireball visible indoors, supernatural protection, readable school signs
```

### 1945/08/06 — 白と死の町

**狙い:** 近藤芳美の短歌そのものを文字で再現せず、「白い原子雲の残像」と死の町を視覚的に接続する。

**Positive prompt**
```text
post-bomb Hiroshima seen as a quiet devastated urban plain under a pale washed-out sky, broken masonry and skeletal structures receding into distance, a faint white cloud form lingering high above like an afterimage rather than an active explosion, almost monochrome pale gray and dusty white atmosphere, tiny distant human figures for scale, literary but historically grounded editorial composition, no written poem, no exact photograph recreation, 16:9
```

**Negative prompt**
```text
readable poetry, active nuclear blast, glamorous mushroom cloud, fantasy ghost city, corpses, gore, exact famous Hiroshima photograph, dramatic movie poster
```

### 1945/08/06 — 白と黒

**狙い:** 白い雲と黒い雨を、爆発スペクタクルではなく被爆後の空と降雨の対比で描く。

**Positive prompt**
```text
Hiroshima after the atomic blast, pale towering cloud already drifting away in the far background while dense dark rain bands fall over another part of the damaged city, wet streets and river surfaces catching charcoal-colored droplets, a few small evacuee silhouettes seeking shelter, visual emphasis on the contrast of pale sky and soot-dark rainfall, restrained scientific-historical editorial tone, no gore, no rainfall map, 16:9
```

**Negative prompt**
```text
close-up suffering, radioactive green glow, active fireball, weather radar map, scientific infographic, exact archival photo composition, sensational apocalypse art
```

### 1945/08/06– — 似島はもう一杯です

**狙い:** 似島を「島の巨大な臨時救護拠点」として、舟艇・桟橋・救護所の密度で見せる。

**Positive prompt**
```text
Ninoshima island military quarantine and aid facilities in Hiroshima Bay in August 1945, small boats arriving at a crowded wooden landing with wounded evacuees on simple stretchers, exhausted medics and soldiers directing people toward improvised treatment buildings, Seto Inland Sea visible behind, many patients implied through blankets and queues without graphic wounds, logistical overload rather than spectacle, original wide composition not based on a single archival photograph, 16:9
```

**Negative prompt**
```text
graphic injuries, piles of bodies, gore, modern ambulances, modern hospital equipment, exact historical photograph recreation, military triumph scene
```

### 1945/08/08 — 広島へ敵新型爆弾

**狙い:** 実在紙面をコピーせず、「壊滅から二日後、国内にはまだ『新型爆弾』として届いた」情報環境を描く。

**Positive prompt**
```text
Japanese newspaper printing and distribution scene in August 1945, rotary press, bundles of freshly printed newspapers, a worker handing a folded paper to waiting civilians near a dim wartime streetscape, the front page represented only by abstract black headline bars with no readable characters, anxious uncertainty rather than propaganda, original composition emphasizing delayed incomplete information, 16:9
```

**Negative prompt**
```text
readable Japanese headline, exact Asahi Shimbun front page, newspaper scan, logo, modern printing press, smiling propaganda crowd, atomic explosion montage
```

### 1945/08/12 — 白い下着は火傷防止に有効です

**狙い:** 原爆後も「防空心得」の延長で対策を考えざるを得なかった戦時広報の限界を描く。

**Positive prompt**
```text
late-war Japanese civilian air-raid preparedness scene inside a modest 1945 home or neighborhood shelter, white cotton undergarments and light-colored cloth laid beside darker fabric as improvised protective advice, a civilian defense volunteer demonstrating clothing choices to a small family, period blackout gear and simple first-aid items nearby, sober sense of inadequate countermeasures against a new weapon, no readable leaflet text, original composition, 16:9
```

**Negative prompt**
```text
fetishized underwear, comedy scene, readable wartime poster, exact newspaper illustration, modern clothing, nuclear explosion, scientific claim infographic, propaganda glamour
```

### 1945/08/14–15 — 敵ハ新ニ残虐ナル爆弾ヲ使用シテ

**狙い:** 玉音放送を天皇の肖像ではなく、録音盤・マイク・ラジオ受信というメディアの連鎖で示す。

**Positive prompt**
```text
August 1945 Japanese surrender-broadcast editorial scene, a period broadcast microphone and lacquer recording discs in the foreground, radio transmission equipment in a dim studio, dissolving into ordinary households and soldiers gathered around tabletop radios in the background, faces small and non-identifying, somber stillness, no exact portrait of the emperor, no readable transcript, original multi-layer composition, 16:9
```

**Negative prompt**
```text
exact emperor portrait, reenactment of a famous surrender photograph, readable imperial rescript, modern radio studio, celebratory victory parade, nationalistic poster
```

### 1945/10末 — 焼かれた聖母

**狙い:** 被爆マリアを「奇跡の宗教画」にせず、瓦礫から見つかった損傷した宗教物として描く。

**Positive prompt**
```text
late 1945 ruins of Urakami Cathedral, a damaged wooden Marian statue head with scorched surface and missing details being carefully lifted from masonry rubble by gloved hands, cathedral fragments and broken brick behind, object shown from an original oblique angle rather than a museum display view, restrained Catholic memorial context, no miraculous glow, no readable inscription, 16:9
```

**Negative prompt**
```text
exact museum catalog photo, exact modern display case, intact Virgin Mary statue, supernatural halo, miracle rays, gore, bodies, photorealistic relic photography
```

## 未来実績


### 未来 — 🔒 今度こそ、全部実験禁止

**狙い:** CTBT発効を「核実験がもうできない魔法の世界」にせず、最後の批准と180日後の法的発効、監視・現地査察制度が正式に動き出す制度的節目として描く。

**Positive prompt**
```text
speculative future international treaty-monitoring center on the day the Comprehensive Nuclear-Test-Ban Treaty finally enters into force, a world map links seismic, hydroacoustic, infrasound and radionuclide stations while one final ratification folder is placed into a complete set, inspection teams prepare neutral field equipment in the background, all nuclear-test environment icons shown inactive, no national leader portraits or readable treaty text, calm institutional milestone rather than triumphal celebration, 16:9
```

**Negative prompt**
```text
nuclear explosion, exact CTBTO logo, readable ratification country names, victory parade, giant flags, claim that nuclear weapons themselves are abolished
```

### 未来 — 🔒 核兵器禁止！

**狙い:** NPT上の5核兵器国がTPNWへ参加する未来を、首脳の握手ではなく「保有国自身が廃棄義務と検証へ入る」制度転換として描く。

**Positive prompt**
```text
speculative future treaty hall, five formerly nuclear-armed state delegations place sealed accession instruments beside an existing nuclear-weapons-ban treaty framework, behind the table international inspectors supervise secured dismantlement and verified inventory reduction using non-readable records, no intact operational warhead glamor, no single country centered or praised, sober transition from nonproliferation hierarchy toward shared prohibition obligations, 16:9
```

**Negative prompt**
```text
exact current political leaders, giant national flags, readable treaty clauses, instant magical disappearance of arsenals, victory propaganda, weapon blueprints
```

### 未来 — 🔒 その前に石油がなくなるだろう

**狙い:** アグニューの皮肉を文字で再演せず、「核兵器が残る一方で平和の灯を維持する設備側が老朽化する」というブラックユーモアを静かに描く。

**Positive prompt**
```text
speculative future Hiroshima Peace Memorial Park decades from now, the memorial flame still burning while maintenance workers inspect an aging fuel line, burner assembly and replacement energy system beneath the memorial infrastructure, distant news screens or abstract world map imply nuclear arsenals still exist but show no readable data, quiet ironic contrast between a peace symbol designed to last until disarmament and the ordinary physical systems that must keep it alive, no comedy props, 16:9
```

**Negative prompt**
```text
literal empty oil barrel joke, gas station sign, readable Harold Agnew quote, slapstick comedy, exact memorial engineering blueprint, nuclear explosion, claim that the flame has actually gone out
```


### 🔒 トラップカード「死の手」発動！

**狙い:** タイトルのカードゲーム感を絵に持ち込まず、ペリメトルを「破壊された指揮系統を迂回する最後の通信網」として描く。

**Positive prompt**
```text
speculative but historically grounded Soviet-era underground nuclear command bunker after a catastrophic attack, primary command consoles dark and damaged while a redundant communications relay network remains lit, abstract lines linking buried command posts and distant silos on a wall-sized non-readable schematic, a few small human operators still present to emphasize that the system is not a magical autonomous machine, tense fail-deadly logic without any missile launch, no trading card imagery, no readable launch codes, 16:9
```

**Negative prompt**
```text
trading card, collectible card game, Yu-Gi-Oh-like composition, autonomous evil AI face, active nuclear launch, detailed launch procedure, readable codes, exact control-room photograph, Soviet propaganda poster
```

### 🔒 主権者は、まだ人間です

**狙い:** ASIによる核廃絶を「AIに取り上げられた未来」と区別し、人間が決定しAIが検証・監査を支える関係として描く。

**Positive prompt**
```text
speculative future international nuclear disarmament verification room, human delegates and inspectors seated at the central decision table while an abstract non-humanoid AI audit system appears only as transparent geometric data links connecting sealed storage sites, satellites, sensors and verification instruments, a dismantled nonfunctional warhead transport cradle visible behind glass, humans visually remain the political center of the composition, calm institutional atmosphere, no national leader portraits, no readable treaty text, 16:9
```

**Negative prompt**
```text
humanoid robot ruler, AI throne, humans kneeling to machine, active operational warhead, detailed weapon internals, nationalistic flags dominating frame, readable treaty clauses, current political leader portrait, sci-fi hologram spectacle
```

### 🔒 過ちはもう繰り返しません

**狙い:** 「最後の核兵器が検証可能・不可逆に廃棄された」という未実現の未来を、勝利演出ではなく静かな終幕として描く。

**Positive prompt**
```text
speculative future editorial illustration in the same restrained visual language, a secure international dismantlement facility after the verified destruction of the world's final nuclear warhead, an empty transport cradle and dismantled nonfunctional metal components under inspection cameras, international inspectors shown only as small neutral figures, beyond the open facility doors a peaceful dawn sky, no national flag dominating the scene, calm irreversible ending rather than triumphal celebration, no readable text, 16:9
```

**Negative prompt**
```text
intact operational warhead, detailed weapon internals, assembly instructions, explosion, victory parade, nationalistic propaganda, giant flags, readable documents, readable labels
```

### 🔒 次の戦は棍棒で

**狙い:** 文明崩壊を派手な終末娯楽にせず、「近代的な再生産能力を失った世界」として対になる終端を描く。

**Positive prompt**
```text
decades after a civilization-scale nuclear war, overgrown abandoned industrial landscape with silent transmission towers, rusted rail lines and a distant ruined missile silo, a few tiny human figures walking with simple hand tools and salvaged wooden poles, no combat taking place, gray dawn light and vegetation reclaiming infrastructure, somber emphasis on lost industrial capacity rather than adventure, original composition rather than imitation of any existing post-apocalyptic film or game, no readable text, 16:9
```

**Negative prompt**
```text
active nuclear explosion, gore, corpses, mutant monsters, zombies, recognizable post-apocalyptic franchise character, famous movie costume, heroic wasteland warrior, glamorous survivalism, futuristic weapons, readable text
```

### 🔒 人類、核をボッシュートされる

**狙い:** ASIによる核使用能力の強制無力化を、人型ロボットではなく「人間の指揮系統より上位の制御層」として抽象化する。

**Positive prompt**
```text
a nuclear command room with physical launch consoles gone dark and disconnected, operators seen as small human figures facing powerless equipment, above and behind the room an abstract non-humanoid network of pale geometric light linking satellites, communication nodes and locked launch facilities, all weapon systems visually inactive, uneasy ambiguity between safety and loss of human control, no robot face, no triumph, muted graphite blue palette, original abstract composition without borrowing imagery from existing AI or robot franchises, no readable text, 16:9
```

**Negative prompt**
```text
humanoid killer robot, recognizable science-fiction robot franchise, glowing red evil AI face, active missile launch, nuclear explosion, detailed launch codes, readable console text, hacker code, national propaganda
```

---

## 生成順のおすすめ

最初の試験生成では、画風とカード内での見え方を確認しやすい次の6枚を優先する。

1. **明日も遊びたかった** — 小物中心で、画風の良し悪しを判断しやすい。
2. **路面電車は我らの誇り** — 人・都市・車両のバランスを確認できる。
3. **街ごと作ります** — 大規模施設・俯瞰構図への適性を確認できる。
4. **我は死神なり、世界の破壊者なり** — 光量差の大きい象徴的場面を試せる。
5. **千羽鶴の祈り** — 記憶継承側の明るいカードも同じ画風で成立するか確認できる。
6. **人類史上もっとも長い土曜日** — 複数要素を一枚へ整理するプロンプト追従性を確認できる。

この6枚で画風を固めた後、同一モデル・同一基調で残りへ広げる。モデルを途中で頻繁に変えるより、まず同一モデルで seed / prompt / guidance を調整した方がカード群の統一感を保ちやすい。
