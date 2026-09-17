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

## 共通ネガティブ方針

各項目の negative prompt には、必要に応じて次を含める。

`photorealistic archival photo, fake documentary photograph, graphic gore, blood, exposed wounds, corpse spectacle, anime, chibi, glossy 3D render, fantasy, modern objects, anachronistic clothing, inaccurate military hardware, readable text, letters, subtitles, watermark, logo, UI, deformed hands, extra fingers, duplicate people`

---

## 科学史・核物理の成立

### 1911 — 原子の中はほとんど空っぽ

**狙い:** 金箔散乱実験を「ほとんど直進するが、ごく一部だけ大きく曲がる」という一枚で見せる。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, restrained museum-exhibit tone, early 20th century physics laboratory, a thin gold foil target inside a simple scattering apparatus, a narrow alpha-particle beam crossing the chamber, most faint light trajectories passing straight through while a very small number deflect sharply backward, brass instruments, dark wood workbench, period-accurate scientific equipment, cinematic side composition, muted amber and charcoal palette, subtle paper grain, physically plausible rather than fantastical, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, colorful atom icon, planetary electron orbits, giant glowing nucleus, laser laboratory, modern electronics, science-fiction machinery, incorrect gold foil experiment geometry, readable labels, equations as text, watermark, logo, anime, glossy 3D render
```

### 1938/12 — バリウムがいる。なぜ？

**狙い:** 「ウランを調べていたのに、化学分析で軽い元素が出てきた」という違和感を実験机で表す。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, late-1930s radiochemistry laboratory in Berlin, two chemists shown from the side and back comparing glass test tubes and precipitates under warm bench lamps, a heavy uranium sample apparatus on one side and unexpectedly separated pale crystalline material on the other, notebooks and period glassware without legible writing, visual mood of scientific surprise rather than celebration, muted green gray and warm tungsten light, subtle paper grain, historically grounded laboratory details, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, mushroom cloud, nuclear bomb, glowing radioactive slime, giant atom symbols, modern laboratory, digital screens, readable periodic table text, readable notes, fantasy chemistry, watermark, logo, anime, glossy 3D render
```

---

## マンハッタン計画

### 1942–1943 — 街ごと作ります

**狙い:** 研究所ではなく「都市そのものが巨大な開発装置」になったことを見せる。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, 1944 Oak Ridge Tennessee seen from a high oblique viewpoint, enormous wartime industrial complexes connected by roads and power lines, a huge U-shaped diffusion plant in the distance, rows of temporary houses, buses and construction traffic, wooded Tennessee ridges surrounding a rapidly built secret city, scale emphasized by tiny workers and vehicles, overcast wartime atmosphere, muted olive brown and steel gray palette, detailed but not map-like, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic aerial photograph, fake archival photo, futuristic city, skyscrapers, modern cars, solar panels, readable signs, exact classified map, glowing nuclear symbols, mushroom cloud, watermark, logo, anime, glossy 3D render
```

### 1943–1945 — 銅がないので銀を貸してください

**狙い:** 財務省の銀が巨大電磁石の導体へ変わる、マンハッタン計画らしい資源動員の異様さを一枚にする。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, wartime industrial interior at the Y-12 electromagnetic separation plant, enormous calutron magnet structures and heavy electrical coils dominating the hall, workers handling plain silver-colored bullion bars and thick conductor material as industrial stock rather than treasure, cranes and wartime factory scaffolding, sense of national-scale resource mobilization, 1940s work clothes and safety gear, muted metallic gray and warm industrial light, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, jewelry, treasure chest, gold bars, modern factory robots, modern PPE, glowing radiation, bomb assembly, detailed weapon blueprint, readable signs, watermark, logo, anime, glossy 3D render
```

### 1944–1945 — 球対称なら解けます

**狙い:** 数学・パンチカード計算・衝撃波研究が爆縮工学へ接続されたことを、兵器の精密設計図にせず表す。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, 1940s Los Alamos calculation room, mathematicians and engineers around IBM punch-card equipment and drafting tables, abstract concentric pressure-wave sketches represented as non-labeled circles on paper, a small generic spherical test assembly in the background without internal weapon details, emphasis on mathematics becoming engineering, desk lamps, punch cards, rulers and mechanical calculators, tense focused atmosphere, muted sepia blue-gray palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, cutaway nuclear weapon, detailed implosion lens geometry, dimensions, wiring diagram, detonator layout, actionable weapon schematic, modern computers, readable equations, readable labels, mushroom cloud, watermark, logo, anime, glossy 3D render
```

### 1945/07/16 — 我は死神なり、世界の破壊者なり

**狙い:** トリニティ実験を、後世の回想と混同しない「遠くから爆発を見た人々」の構図にする。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, pre-dawn New Mexico desert during the 1945 Trinity test, an enormous intensely bright nuclear fireball rising far beyond the horizon, low desert scrub and test-site silhouettes, a few observers seen only as dark distant figures behind protective positions, dramatic contrast between violet dawn sky and orange-white blast, no city, no victims, awe mixed with dread rather than triumph, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, Oppenheimer close-up portrait, quoted text, Bhagavad Gita lettering, city destruction, bodies, gore, celebratory fireworks, fantasy colors, modern vehicles, watermark, logo, anime, glossy 3D render
```

---

## 1945年8月・被爆

### 1945/08/06 — 明日も遊びたかった

**狙い:** 人物を直接再現せず、三輪車という具体物から一人の生活を見せる。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, respectful museum-exhibit still life, a small 1940s Japanese child's tricycle scorched and rusted, resting alone on bare earth beside a modest damaged wooden house wall, a tiny child's sandal nearby but no person present, soft late-afternoon light, quiet empty composition, muted brown gray palette with faint warm highlights, emphasis on ordinary childhood interrupted by war, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic museum photo, fake archival photograph, child corpse, injured child, gore, blood, flames engulfing people, sentimental angel imagery, toy-store brightness, modern bicycle, readable museum label, watermark, logo, anime, chibi, glossy 3D render
```

### 1945/08/06 — お弁当食べたかった

**狙い:** 焼けた弁当箱と中身だけで、登校・作業・昼食という日常が途切れたことを示す。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, respectful still life of a blackened 1940s Japanese metal lunch box lying on dusty ground, charred traces of a simple vegetable lunch visible inside, a school cap and work glove partly in frame, ruined city textures softly out of focus behind it, morning light filtered through smoke, quiet composition centered on the ordinary meal that was never eaten, muted charcoal brown palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic artifact photo, fake archival photograph, corpse, body parts, gore, blood, graphic burns, abundant modern food, plastic lunch box, bright cute bento, readable name tags, watermark, logo, anime, chibi, glossy 3D render
```

### 1945/08/06 — 人影の石

**狙い:** 「人が蒸発して影だけ残った」という誤解を強化せず、熱線で表面差が生じた石段そのものを描く。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, close view of broad stone entrance steps in devastated Hiroshima, the stone surface bleached lighter by intense heat with one darker seated human-shaped protected area remaining on a step, damaged masonry and dust around it, no body present, quiet forensic museum-like composition, overcast gray light, subtle paper grain, historically respectful, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, vaporizing person, ghost silhouette standing upright, supernatural shadow, skeleton, corpse, gore, blood, dramatic fireball, readable bank sign, watermark, logo, anime, horror art, glossy 3D render
```

### 1945/08/06 — 水をください

**狙い:** 負傷描写ではなく、水そのものが救護現場の最重要資源になったことを見せる。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, improvised 1945 Hiroshima relief station, a dented metal bucket of water and simple ladle in the foreground, several dusty hands reaching carefully toward cups, exhausted medics and evacuees suggested only as soft silhouettes in the background, broken water pipes and smoke beyond, emphasis on thirst, scarcity and emergency care rather than injury, muted gray brown palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, graphic burns, exposed wounds, corpse, gore, blood, screaming close-up faces, abundant clean bottled water, modern medical equipment, readable text, watermark, logo, anime, glossy 3D render
```

### 1945/08/06– — 八面六臂の暁部隊

**狙い:** 軍事輸送用に整備された人員・舟艇・車両が、そのまま救援インフラへ転用されたことを見せる。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, Hiroshima waterfront on August 6 1945, Japanese Army shipping-unit soldiers and medics rapidly loading wounded civilians represented respectfully under blankets onto small military boats, trucks and stretchers moving in coordinated directions, Ujina harbor in the background under a smoke-filled sky, strong sense of logistics repurposed for emergency rescue, no heroic posing, muted khaki gray and river blue palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, gore, blood, exposed wounds, corpses, triumphant military propaganda pose, charging soldiers, combat scene, modern rescue vehicles, modern uniforms, readable insignia text, watermark, logo, anime, glossy 3D render
```

### 1945/08/09 — 路面電車は我らの誇り

**狙い:** 焼け跡の中を再び走り始めた路面電車を、復旧する都市機能として描く。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, Hiroshima three days after the atomic bombing, a battered 1940s streetcar moving slowly along hastily repaired tracks through a heavily damaged streetscape, utility workers repairing overhead wires, a few civilians waiting quietly, no cheering crowd, morning sunlight breaking through smoke and dust, visual emphasis on restored urban function amid ruins, muted gray with restrained warm light, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, modern tram, pristine rebuilt city, cheerful tourism poster, gore, bodies, giant mushroom cloud, readable destination sign, watermark, logo, anime, glossy 3D render
```

### 1945/08/09 — 僅かな雲の切れ目から

**狙い:** 長崎投下の偶然性・視界・燃料制約を、「雲の穴」と航空機の構図だけで示す。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, high-altitude view above Nagasaki on August 9 1945, a silver B-29 bomber crossing a broad layer of thick summer cloud, one narrow irregular break in the clouds revealing only a small portion of the valley city far below, tense navigational atmosphere, aircraft shown externally with period-correct silhouette but no glorification, soft sunlight above cloud tops and dark shadow below, no explosion yet, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, modern aircraft, incorrect jet engines, giant open target reticle, readable nose art, bomb cutaway, detailed weapon mechanics, city already exploding, celebratory composition, watermark, logo, anime, glossy 3D render
```

### 1945/08/09 — キリストは再び贄となった

**狙い:** 「燔祭」論をゲーム自身の断定にせず、浦上天主堂の壊滅と宗教共同体の喪失を静かに描く。

**Positive prompt**

```text
historical editorial illustration, restrained semi-realistic gouache and ink, ruins of Urakami Cathedral in Nagasaki after the atomic bombing, broken red-brick arches, collapsed masonry, damaged religious statuary partly visible among debris, a church bell and fragments of stained glass in the foreground, no bodies, no supernatural light, solemn Catholic memorial atmosphere without endorsing a theological interpretation, cloudy late-day sky, muted brick red and ash gray palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, crucified living person, divine apparition, angels, miraculous beam of light, gore, corpses, blood, triumphal religious propaganda, intact modern cathedral, readable text, watermark, logo, anime, glossy 3D render
```

---

## 復興・被爆後・記憶継承

### 1954/03/01 — 三度目の悲劇

**狙い:** 第五福竜丸と放射性降下物を、爆心そのものではなく「遠く離れた漁船まで届いた核実験」として見せる。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, 1954 Japanese tuna fishing boat at sea near the Marshall Islands, the Daigo Fukuryu Maru represented as a modest wooden fishing vessel beneath an uncanny bright distant horizon, fine pale fallout dust settling across deck ropes and nets like ash, crew members shown only as small concerned silhouettes, tropical ocean otherwise calm, contrast between ordinary fishing work and invisible radiological danger, muted blue gray palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, close-up radiation burns, gore, blood, giant monster, Godzilla, fantasy green radiation glow, modern fishing vessel, readable hull text, watermark, logo, anime, glossy 3D render
```

### 1958/05/05 — 千羽鶴の祈り

**狙い:** 個人の病と死が、子どもたちの募金運動を経て公共の記憶装置になった流れを象徴する。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, Children's Peace Monument in Hiroshima Peace Memorial Park in the late 1950s, the bronze girl figure holding an origami crane overhead, strings of colorful folded paper cranes gathering below, schoolchildren seen from behind placing more cranes quietly, open sky and young trees around the memorial, solemn but hopeful tone, color restrained except for the cranes, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic tourist photo, fake archival photograph, amusement-park mood, kawaii mascot style, excessive rainbow saturation, balloons, readable plaques, modern smartphones, watermark, logo, anime, chibi, glossy 3D render
```

### 1964/08/01 — この火が消えるその日まで

**狙い:** 「火が燃えている＝まだ核廃絶が完了していない」という状態を静かな一枚で可視化する。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, Hiroshima Peace Memorial Park at dusk, the Flame of Peace burning steadily in the foreground, memorial axis leading toward the Atomic Bomb Dome in the distance, calm reflecting water and sparse visitors shown as small silhouettes, deep blue evening sky, warm flame as the only strong color accent, contemplative unresolved mood rather than celebration, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic tourist photo, fake documentary photograph, fireworks, festival crowd, giant fantasy flame, city on fire, readable monument text, modern advertising, watermark, logo, anime, glossy 3D render
```

---

## 冷戦・核抑止

### 1946–1952 — 真上に飛ばせば科学の進歩です

**狙い:** 都市攻撃兵器V2と科学観測ロケットが同じ技術幹にあることを、用途の転換として描く。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, late-1940s White Sands New Mexico, captured V-2 rocket launching almost vertically from a desert test stand carrying scientific instruments, technicians and optical tracking equipment at a safe distance, the rocket rising toward a darkening high-altitude sky, a faint curved Earth horizon motif suggested above, visual contrast between military hardware and atmospheric science, muted desert tan and deep blue palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, London bombing, civilians under attack, modern orbital rocket, SpaceX-style booster, astronauts, readable Nazi markings, propaganda symbols, watermark, logo, anime, glossy 3D render
```

### 1961/10/30 — 爆弾の皇帝

**狙い:** 都市破壊ではなく、北極圏の核実験が「兵器というより超大国のデモンストレーション」だったことを示す。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, remote Novaya Zemlya Arctic test range in 1961, an immense nuclear cloud towering over an empty snow-covered landscape and dark sea, viewed from very far away with a small Soviet bomber silhouette retreating at the edge of frame, overwhelming scale emphasized by the vast empty horizon, no city and no people near the blast, cold blue gray environment contrasted with white-orange cloud, ominous demonstration of scale rather than spectacle, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, city destruction, crowds, gore, heroic propaganda poster, detailed bomb cutaway, weapon blueprint, neon fantasy colors, readable slogans, watermark, logo, anime, glossy 3D render
```

### 1962/10/27 — 人類史上もっとも長い土曜日

**狙い:** キューバ危機が首脳会議だけでなく、海中・上空・現場の誤認でも破局し得たことを多層構図で示す。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, tense 1962 Cuban Missile Crisis triptych-like composition without text: a dim government crisis room with maps and telephones on the left, a U-2 reconnaissance aircraft high over tropical cloud in the center sky, and a Soviet diesel submarine deep under dark rough Atlantic water on the right lower section, no identifiable leader portraits, red indicator lights and paper folders suggesting compressed decision time, restrained cinematic tension, muted navy gray and tobacco brown palette, subtle paper grain, clearly illustrated not a documentary photograph, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, exact Kennedy portrait, exact Khrushchev portrait, nuclear explosions, city destruction, celebratory military poster, modern screens, readable map labels, readable documents, watermark, logo, anime, glossy 3D render
```

---

## 原子力平和利用・デュアルユース

### 1951/12/20 — 四つの電球から

**狙い:** 原子力発電史の始まりを、巨大都市ではなく「まず4個の電球が点いた」という小さなスケールで見せる。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, interior of the early Experimental Breeder Reactor I facility in Idaho in 1951, four simple incandescent light bulbs glowing warmly from a small electrical panel in the foreground, engineers in period work clothes watching with restrained satisfaction, industrial reactor-room equipment and analog gauges behind them, emphasis on the modest first electrical output rather than futuristic grandeur, muted steel gray with warm amber bulbs, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic archival photo, fake documentary photograph, giant modern nuclear power plant cooling towers, futuristic reactor, neon blue radiation, modern LED bulbs, readable gauge text, celebratory sci-fi city, watermark, logo, anime, glossy 3D render
```

### 2011/03/11 — 平和利用は、たまに取り返しがつかない ×3

**狙い:** 福島第一事故を「原発が爆発する絵」だけに縮めず、津波・全電源喪失・緊急対応の複合災害として描く。

**Positive prompt**

```text
historical editorial illustration, semi-realistic gouache and ink, Fukushima Daiichi nuclear power station after the March 2011 tsunami, flooded service roads, damaged reactor buildings, emergency workers in protective gear moving cables and portable equipment, dark powerless infrastructure with temporary lights, ocean and tsunami debris visible in the distance, no active explosion, no sensational radiation glow, sober disaster-response composition emphasizing loss of power and difficult stabilization work, cool gray palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic news photo, fake documentary photograph, nuclear mushroom cloud, city vaporization, glowing green radiation, graphic casualties, bodies, gore, superhero hazmat suits, futuristic machinery, readable company logos, readable signs, watermark, anime, glossy 3D render
```

---

## 未来実績

### 🔒 過ちはもう繰り返しません

**狙い:** 「最後の核兵器が検証可能・不可逆に廃棄された」という未実現の未来を、勝利演出ではなく静かな終幕として描く。

**Positive prompt**

```text
speculative future editorial illustration in the same restrained semi-realistic gouache and ink style, a secure international dismantlement facility after the verified destruction of the world's final nuclear warhead, an empty transport cradle and dismantled nonfunctional metal components under inspection cameras, international inspectors shown only as small neutral figures, beyond the open facility doors a peaceful dawn sky, no national flag dominating the scene, calm irreversible ending rather than triumphal celebration, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic news photo, fake documentary photograph, intact operational warhead, detailed weapon internals, assembly instructions, explosion, victory parade, nationalistic propaganda, giant flags, readable documents, readable labels, watermark, logo, anime, glossy 3D render
```

### 🔒 次の戦は棍棒で

**狙い:** 文明崩壊を派手な終末娯楽にせず、「近代的な再生産能力を失った世界」として対になる終端を描く。

**Positive prompt**

```text
speculative future editorial illustration, restrained semi-realistic gouache and ink, decades after a civilization-scale nuclear war, overgrown abandoned industrial landscape with silent transmission towers, rusted rail lines and a distant ruined missile silo, a few tiny human figures walking with simple hand tools and salvaged wooden poles, no combat taking place, gray dawn light and vegetation reclaiming infrastructure, somber emphasis on lost industrial capacity rather than adventure, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic news photo, fake documentary photograph, active nuclear explosion, gore, corpses, mutant monsters, zombies, Mad Max fashion, heroic post-apocalyptic warriors, glamorous survivalism, futuristic weapons, readable text, watermark, logo, anime, glossy 3D render
```

### 🔒 人類、核をボッシュートされる

**狙い:** ASIによる核使用能力の強制無力化を、人型ロボットではなく「人間の指揮系統より上位の制御層」として抽象化する。

**Positive prompt**

```text
speculative future editorial illustration, restrained semi-realistic gouache and ink with subtle modern graphic abstraction, a nuclear command room with physical launch consoles gone dark and disconnected, operators seen as small human figures facing powerless equipment, above and behind the room an abstract non-humanoid network of pale geometric light linking satellites, communication nodes and locked launch facilities, all weapon systems visually inactive, uneasy ambiguity between safety and loss of human control, no robot face, no triumph, muted graphite blue palette, subtle paper grain, clearly illustrated not a documentary photograph, no readable text, 16:9
```

**Negative prompt**

```text
photorealistic news photo, fake documentary photograph, humanoid killer robot, Terminator imagery, glowing red evil AI face, active missile launch, nuclear explosion, detailed launch codes, readable console text, hacker code, national propaganda, watermark, logo, anime, glossy 3D render
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
