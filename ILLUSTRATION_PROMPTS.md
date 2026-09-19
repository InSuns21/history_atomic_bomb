# イラスト生成プロンプト案

> 実績カードへイラストを付ける場合の Text-to-Image 用プロンプト台帳。史実本文の正本ではなく、`ACHIEVEMENTS.md` / `achievements/*.md` に対応する生成素材として管理する。

## 基本方針

- 全実績へ機械的に付けず、**一枚の具体物・場所・構図で歴史の意味が伝わる実績**を優先する。
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
- 自動生成の既定プロンプトでは、**museum photo / archival photo / manga panel / book cover / anime character / logo / direct copy** 系の誤生成をまとめて抑制する。

## 共通スタイルプロンプト

> 個別実績のプロンプトへ共通して付与する画風。Node の自動生成では `illustrations/config.json` の同内容を正として、各実績の scene prompt の前後へ結合する。

**Common Positive prompt**
```text
historical editorial illustration, clearly illustrated and not a documentary photograph, original composition based on historical facts rather than any single archival or museum photograph, (lineart:1.2), (clean line art:1.2), (contour emphasis:1.4), bold outlines, strong edges, crisp ink lines, sharp edge definition, clean white outline stroke around the subject, white edge highlight, white contour accent, readable white trim separating the subject from the background, (flat colors:1.1), limited palette, clean cel shading, minimal gradients, simple and readable composition, strong silhouette readability, museum-exhibit tone, respectful historical tone, semi-realistic proportions, slightly poster-like clarity, clear foreground and background separation, subtle paper-like texture, restrained color design, no text in the image, no captions, no labels
```

**Common Negative prompt**
```text
photorealistic, documentary photograph, fake archival photo, exact recreation of a museum catalog image, exact recreation of a news photo, direct copy of an official reference photo, direct copy of a manga panel, direct copy of a book cover, copyrighted character, famous anime character, franchise mascot, recognizable logo, readable brand mark, hyperrealism, painterly brushwork, messy sketch, rough doodle, watercolor bleed, oil painting, soft edges, blurry outlines, weak silhouette, low contrast edges, overrendered shading, heavy gradients, glossy rendering, shiny surfaces, 3D render, CGI, plastic texture, anime exaggeration, chibi, super-deformed style, cute mascot style, fantasy elements, sci-fi effects, magic glow, graphic gore, excessive blood, exposed organs, corpse spectacle, modern objects, modern clothing, contemporary architecture where inappropriate, anachronistic military hardware, inaccurate machinery, readable text, letters, subtitles, speech bubbles, watermark, logo, UI, deformed hands, extra fingers, duplicate people, distorted anatomy, malformed face, cluttered composition, overcrowded scene
```

自動生成時は、既存の個別 prompt に残る `semi-realistic gouache and ink` など旧画風の共通句をスクリプト側で除去してから、この共通画風を先頭へ付与する。個別 prompt は主に **主題・場所・年代・構図・避けたい誤生成・権利上避けたい再現対象** を担当する。

### 自動生成運用

`node scripts/generate_illustrations.mjs` はこの Markdown の `###` 実績見出しと `Positive prompt` / `Negative prompt` を読み取り、ModelsLab API で画像を生成して `assets/illustrations/` へ保存する。すでに同じ実績の画像が存在する場合は既定でスキップし、`--force` 指定時のみ再生成する。API・モデル・共通ポジネガ・出力サイズは `illustrations/config.json` で管理する。生成前には、旧共通句の除去に加えて、**権利衝突リスクの高い共通 NG 語**（museum photo, manga panel, book cover, anime character, logo など）を必ず付与する。

---

## 科学史・核物理の成立

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

---

## マンハッタン計画

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

---

## 復興・被爆後・記憶継承

### 1954/03/01 — 三度目の悲劇

**狙い:** 第五福竜丸と放射性降下物を、爆心そのものではなく「遠く離れた漁船まで届いた核実験」として見せる。

**Positive prompt**
```text
1954 Japanese tuna fishing boat at sea near the Marshall Islands, the Daigo Fukuryu Maru represented as a modest wooden fishing vessel beneath an uncanny bright distant horizon, fine pale fallout dust settling across deck ropes and nets like ash, crew members shown only as small concerned silhouettes, tropical ocean otherwise calm, contrast between ordinary fishing work and invisible radiological danger, muted blue gray palette, no readable text, 16:9
```

**Negative prompt**
```text
close-up radiation burns, gore, blood, famous giant monster character, fantasy green radiation glow, modern fishing vessel, readable hull text
```

### 1958/05/05 — 千羽鶴の祈り

**狙い:** 個人の病と死が、子どもたちの募金運動を経て公共の記憶装置になった流れを象徴する。

**Positive prompt**
```text
Children's Peace Monument in Hiroshima Peace Memorial Park in the late 1950s, the bronze girl figure holding an origami crane overhead, strings of colorful folded paper cranes gathering below, schoolchildren seen from behind placing more cranes quietly, open sky and young trees around the memorial, solemn but hopeful tone, color restrained except for the cranes, not a copy of any specific tourist or museum photograph, no readable text, 16:9
```

**Negative prompt**
```text
amusement-park mood, kawaii mascot style, excessive rainbow saturation, balloons, readable plaques, modern smartphones
```

### 1964/08/01 — この火が消えるその日まで

**狙い:** 「火が燃えている＝まだ核廃絶が完了していない」という状態を静かな一枚で可視化する。

**Positive prompt**
```text
Hiroshima Peace Memorial Park at dusk, the Flame of Peace burning steadily in the foreground, memorial axis leading toward the Atomic Bomb Dome in the distance, calm reflecting water and sparse visitors shown as small silhouettes, deep blue evening sky, warm flame as the only strong color accent, contemplative unresolved mood rather than celebration, not a copy of any specific tourist photo, no readable text, 16:9
```

**Negative prompt**
```text
fireworks, festival crowd, giant fantasy flame, city on fire, readable monument text, modern advertising
```

---

## 永井隆 ― 個人史

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

## 冷戦・核抑止

### 1946–1952 — 真上に飛ばせば科学の進歩です

**狙い:** 都市攻撃兵器V2と科学観測ロケットが同じ技術幹にあることを、用途の転換として描く。

**Positive prompt**
```text
late-1940s White Sands New Mexico, captured V-2 rocket launching almost vertically from a desert test stand carrying scientific instruments, technicians and optical tracking equipment at a safe distance, the rocket rising toward a darkening high-altitude sky, a faint curved Earth horizon motif suggested above, visual contrast between military hardware and atmospheric science, muted desert tan and deep blue palette, no readable text, 16:9
```

**Negative prompt**
```text
London bombing, civilians under attack, modern orbital rocket, private-space-company style booster, astronauts, readable Nazi markings, propaganda symbols
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

---

## 原子力平和利用・デュアルユース

### 1951/12/20 — 四つの電球から

**狙い:** 原子力発電史の始まりを、巨大都市ではなく「まず4個の電球が点いた」という小さなスケールで見せる。

**Positive prompt**
```text
interior of the early Experimental Breeder Reactor I facility in Idaho in 1951, four simple incandescent light bulbs glowing warmly from a small electrical panel in the foreground, engineers in period work clothes watching with restrained satisfaction, industrial reactor-room equipment and analog gauges behind them, emphasis on the modest first electrical output rather than futuristic grandeur, muted steel gray with warm amber bulbs, no readable text, 16:9
```

**Negative prompt**
```text
giant modern nuclear power plant cooling towers, futuristic reactor, neon blue radiation, modern LED bulbs, readable gauge text, celebratory sci-fi city
```

### 2011/03/11 — 平和利用は、たまに取り返しがつかない ×3

**狙い:** 福島第一事故を「原発が爆発する絵」だけに縮めず、津波・全電源喪失・緊急対応の複合災害として描く。

**Positive prompt**
```text
Fukushima Daiichi nuclear power station after the March 2011 tsunami, flooded service roads, damaged reactor buildings, emergency workers in protective gear moving cables and portable equipment, dark powerless infrastructure with temporary lights, ocean and tsunami debris visible in the distance, no active explosion, no sensational radiation glow, sober disaster-response composition emphasizing loss of power and difficult stabilization work, cool gray palette, no readable text, 16:9
```

**Negative prompt**
```text
nuclear mushroom cloud, city vaporization, glowing green radiation, graphic casualties, bodies, gore, superhero hazmat suits, futuristic machinery, readable company logos, readable signs
```

---

## 未来実績

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
