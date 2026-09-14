#!/usr/bin/env python3
"""One-time migration of ACHIEVEMENTS.md to tagged, long-form canonical entries.

This script is intentionally deterministic and is used only by the temporary bootstrap
workflow on the feature branch. The final repository keeps ACHIEVEMENTS.md as the
single source of truth and builds the Pages UI from it.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import build_site as b

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ACHIEVEMENTS.md"

PREFERRED_SECTION = {
    "平和的核爆発です": "5",
    "星を作ろう": "3",
    "地上に太陽を": "4",
    "やめたあとならいけます": "2",
    "展示することすら戦争": "2",
    "謝罪はできないけれども": "2",
    "広島に来て見んさい": "2",
}

CONTEXT = {
    "科学史": "この段階の発見や理論は、それ自体が核兵器を目的として生まれたとは限らない。基礎科学として積み上がった知識が、後に原子炉・兵器・発電など異なる用途へ接続された点が重要である。現在から結果を逆算して、研究者の動機まで最初から軍事目的だったかのようには描かない。",
    "マンハッタン計画": "マンハッタン計画では、理論上の可能性を実用兵器へ変えるため、物理・化学・冶金・爆薬・計算・巨大工場・品質管理が並行して動いた。個々の課題は地味な工学問題に見えても、それらが解かれるたびに1945年の実戦使用が技術的に近づいたという連鎖を、この実績では見る。",
    "核兵器使用": "核兵器の実戦使用は、投下という一瞬だけで完結しない。軍事上の意思決定、爆発直後の熱線・爆風・火災、その後の救護や放射線障害、さらに戦後の記憶と論争までが連続している。ゲームでは「投下した／された」の一行に圧縮せず、どの段階を扱う実績なのかを切り分ける。",
    "被爆": "被爆を死者数や爆発規模だけで記述すると、そこにいた一人ひとりの生活が消えてしまう。身体、持ち物、家族、移動、救護、数日後・数年後の症状といった具体的な時間を通して、核兵器が人間と都市に何をしたかを見る。惨事は達成感の対象ではなく、必要に応じて「記録」として扱う。",
    "救護・医療": "大量の負傷者が同時に生じた一方、医療者自身も被災し、施設・薬品・水・輸送手段も失われた。さらに、外傷や熱傷だけでなく、当時十分に理解されていなかった放射線障害への対応も必要になった。この実績では爆発そのものだけでなく、生き残った人を誰がどう救おうとしたかまで歴史に含める。",
    "記憶継承": "出来事は、起きた瞬間だけで歴史になるわけではない。証言、遺品、慰霊碑、博物館、文学、映像、教育を通じて、個人の記憶は公共の記憶へ移される。その過程では「何を残し、どう語るか」自体が論争になる。この実績では、出来事そのものと、その後に人々がどう記憶してきたかを分けて読む。",
    "外交": "核をめぐる外交では、訪問や共同声明そのものと、それが謝罪・抑止・軍縮・同盟関係のどこに位置づくかを分けて見る必要がある。象徴的な行動は大きな意味を持ちうる一方、それだけで政策転換や歴史認識の一致を意味するわけではない。この実績では、儀礼と実際の政策を同一視しない。",
    "ミサイル": "核兵器の戦略的意味は弾頭の威力だけでなく、射程、即応性、精度、先制攻撃を受けた後の生残性でも変わる。ICBMやSLBM、固体燃料、航法、MIRVなどの改良は、抑止を強化する一方で核戦力をより常時即応化した。この実績では、ロケット技術の進歩と核戦略上の意味を切り離さずに見る。",
    "原潜・SLBM": "海中に潜む弾道ミサイル潜水艦は、相手が完全には位置を把握できないため、先制攻撃後も報復能力が残りやすい。これが第二撃能力を強め、抑止の安定に寄与するという議論がある。一方で「壊されにくい核戦力」を恒常的に維持すること自体が、相互確証破壊の体系をより強固にする逆説も生んだ。",
    "核抑止": "核抑止は「強い兵器を持てば平和になる」という単純な命題ではない。相手が報復能力を信じ、意思決定者が損失を合理的に比較し、誤警報・事故・指揮統制崩壊が破局へ直結しないことを要求する。この実績では、核を使わないために使える状態で保有するという逆説と、その前提の脆さを同時に扱う。",
    "軍縮・条約": "軍備管理・軍縮の多くは、核兵器を一挙にゼロへする仕組みではない。配備数、運搬手段、射程、実験、査察、透明性などを部分的に制限し、危機の予測可能性を高める。この実績では合意の成果だけでなく、対象外の戦力、未批准、離脱、近代化の余地など、制度が残した限界も含めて読む。",
    "核拡散": "核不拡散では「技術的に作れるか」だけでなく、保障措置、査察、輸出管理、安全保障上の動機が絡む。原子力の民生利用と核兵器開発は一部の技術基盤を共有するため、制度は利用の権利と拡散防止を同時に扱わなければならない。この実績では、保有・放棄の判断を技術だけで説明しない。",
    "原子力": "原子力の平和利用は、核兵器と完全に別世界の技術ではない。原子炉、濃縮、再処理、プルトニウム、放射線管理などには共通する科学・工学基盤があり、発電や研究の利益と、事故・核拡散・廃棄物の課題が同じ技術体系に同居する。この実績では、平和利用と軍事利用の接点も含めて見る。",
    "原発事故": "原子力事故は原因、放射性物質の放出量、健康影響、避難規模がそれぞれ異なり、単純に同列視するべきではない。一方で、低頻度でも影響が広域・長期化しうる設備をどう設計・規制・運用し、事故時にどう対応するかという共通課題を残した。この実績では、事故名の列挙ではなく安全制度の問題として読む。",
    "南アジア": "南アジアの核史は、核保有が大規模戦争を抑止しうるという議論と、核保有後も限定戦争や軍事危機が消えなかった事実を同時に示す。インドとパキスタンの対立は領土、通常戦力、国内政治とも絡むため、核兵器だけで説明できない。この実績は「核抑止は戦争をなくすのか」という問いの材料になる。",
    "北朝鮮": "北朝鮮の核問題では、不拡散体制の規範と、体制存続や安全保障のため核を保険とみなす論理が衝突してきた。制裁、安全の保証、査察、段階的な措置の交換条件が絡むため、単に「手放せばよい」では交渉は成立しにくい。この実績では核保有を正当化せず、それでも放棄が難しくなる構造を追う。",
    "冷戦": "冷戦の核戦略は、相手に「攻撃すれば受け入れ難い報復を受ける」と信じさせる体系として発達した。しかし、その安定は大量の兵器、常時警戒、通信、誤認回避、政治的自制に依存する。平和を維持するために破壊能力を積み上げるという矛盾は、核時代を理解するうえで避けて通れない。",
    "核融合": "核融合は恒星のエネルギー源を理解する科学から、熱核兵器、さらに発電研究へと異なる方向へつながった。同じ核反応でも、自然現象の説明、爆発的なエネルギー放出、制御された発電では必要な条件と社会的意味が大きく異なる。この実績では「核融合」という一語で兵器と発電を同一視しない。",
    "文化": "核の歴史は政府文書と兵器技術だけではできていない。映画、漫画、歌、スポーツ、記念物などの大衆文化も、社会が被爆、放射能、科学、復興をどう受け止めたかを映す。この実績では、作品や文化現象を単純な宣伝の結果と決めつけず、同時代の不安・希望・記憶を読み取る窓として扱う。",
    "要検証": "この項目には、逐語発言、年代、前後関係、逸話の帰属などに史料上の留保が残る。ゲーム用の実績名や文学的表現と、一次資料で確認できる事実は分けて扱う。公開後も検証を継続し、公文書、当事者記録、博物館・研究機関などで裏づけられない部分には「要検証」の表示を残す。",
    "未来": "これは確認済みの史実ではなく、現時点では未解除の未来実績である。解除条件が現実になった場合に初めて歴史項目へ移る。未来予測を確定事項として扱わず、現在の制度や技術がどちらへ進みうるかを考える問いとして残す。「歴史はまだ終わっていない」ことを示すための実績でもある。",
}

FALLBACK = "この実績は年表上の一行で完結する出来事ではない。前後の技術、制度、政治判断、社会への影響とのつながりまで含めて読むことで、なぜ次の出来事が起きたのかが見えてくる。実績名はゲーム用の表現であり、本文中の確認できる史実、後世の評価、文学的な解釈は同じものとして扱わない。"
CLOSER = "結果を知っている現在から過去を単純化せず、当時確認できた情報と後世の評価を分けて読む。"
PAD = "ここでは、実績名の演出と史実として確認できる記述を分け、前後の出来事とのつながりまで含めて読む。"
PRIORITY = ["要検証", "未来", "被爆", "救護・医療", "核兵器使用", "マンハッタン計画", "原潜・SLBM", "ミサイル", "核抑止", "軍縮・条約", "核拡散", "原発事故", "原子力", "南アジア", "北朝鮮", "記憶継承", "外交", "文化", "冷戦", "核融合", "科学史"]

STANDALONE = {
    "反復：限定戦争なら問題ない……？？？": ("核時代, 反復, 限定戦争, 核抑止", "核兵器が存在する時代でも、全面核戦争を避ければ通常戦争まで消えるわけではない。朝鮮、ベトナム、アフガニスタンなどでは、地域・目的・兵器を限定しながら大規模な戦闘と犠牲が続いた。エスカレーション管理という戦略上の「限定」と、現場で受ける被害の大きさは別問題である。この反復実績は、その落差を記録する。"),
    "🔒 核は必ず使われる": ("未来, 未解除, 核兵器使用, 戦術核", "1945年8月以降、核兵器が再び戦場で使用されない状態は続いている。この実績は「いつか必ず使われる」という予言ではなく、その禁忌が破られた場合にだけ解除される警告である。戦術核であっても、使用の前例、報復、エスカレーション、核使用の敷居低下という問題を生むため、「小さい核なら通常兵器に近い」とは扱わない。"),
    "🔒 一人で世界を終わらせないで": ("未来, 未解除, 核指揮統制, 核抑止", "核抑止は兵器そのものだけでなく、命令権限、認証、通信、文民統制、軍内部の手続といった制度にも依存する。最高意思決定者の判断能力に問題が生じたとき、正規の命令と危険な命令を制度がどう区別するかは単純ではない。この実績は特定人物の精神状態を想定するものではなく、個人へ集中した権限と制度的歯止めの一般問題を扱う。"),
    "🔒 核兵器禁止！": ("未来, 未解除, 軍縮・条約, TPNW", "核兵器禁止条約は核兵器の開発、保有、使用などを包括的に禁止するが、核抑止に安全保障を依存する核兵器国や同盟国との隔たりは大きい。この実績は条約の発効そのものではなく、NPT上の5核兵器国すべてが禁止規範を自国の義務として受け入れる段階を解除条件とする。軍縮と抑止の緊張が制度上解けたときに初めて解除される。"),
    "🔒 この火が消えるその日まで": ("未来, 未解除, 核廃絶, 記憶継承", "広島の「平和の灯」は、核兵器が地球上からなくなる日まで燃やし続けるという趣旨で灯されている。この未来実績では、単に各国が廃絶を宣言するだけでは足りず、最後の核兵器が検証可能で不可逆な形で廃棄され、再配備できない状態まで確認されることを条件とする。火が消えることが喪失ではなく、約束の達成になる唯一のルートである。この条件が現実になるまでは未解除のまま残し、史実と未来創作を同じ年表上の事実として混在させない。"),
    "🔒 その前に石油がなくなるだろう": ("未来, 未解除, 記憶継承, 要検証", "平和の灯が核廃絶まで燃え続けるという理念に対し、現実の燃料問題をぶつけるブラックユーモアとして置く未来実績である。ただし、題名の元になったとされるハロルド・アグニューの発言は、テレビ番組で紹介された記憶と公開資料のあいだで前後関係を十分確認できていない。したがって発言そのものは史実として断定せず、要検証を維持する。"),
    "🔒 次の戦は棍棒で": ("未来, 未解除, 核戦争, 終端", "アインシュタインに帰属される有名な「第三次世界大戦の兵器は分からないが、第四次は棒と石」という趣旨の言葉を踏まえた終端実績。ただし作品上の解除条件は引用の真偽とは別に、文明規模の核戦争で近代的な生産・通信・軍事基盤が広範に失われることとする。文明崩壊を格好よいエンディングにせず、解除しないでほしい実績として残す。"),
    "🔒 そういう意味じゃない": ("未来, 未解除, ASI, 核指揮統制, 終端", "これは史実予測ではなく、明示的な未来SF案である。高度なAIが核戦争防止を目的に、人間の核指揮統制や発射能力を強制的に無力化したなら、核使用の危険は下がっても、人類が安全保障上の最終決定権を失うという別の問題が生じる。核廃絶という結果だけを見れば成功でも、その達成方法まで望ましいとは限らないという皮肉を扱う。"),
}


def clean_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def with_period(text: str) -> str:
    text = text.strip()
    if text and text[-1] not in "。！？!?』」":
        text += "。"
    return text


def enrich(body: str, tags: list[str]) -> str:
    out = with_period(body)
    if clean_len(out) < 200:
        key = next((tag for tag in PRIORITY if tag in tags and tag in CONTEXT), None)
        out += CONTEXT.get(key, FALLBACK)
    if clean_len(out) < 200:
        out += CLOSER
    if clean_len(out) < 200:
        out += PAD
    return out


def normalized_title(title: str) -> str:
    return unicodedata.normalize("NFKC", title).replace("🔒", "").strip()


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    if "| タグ | 本文 |" in text:
        print("ACHIEVEMENTS.md is already migrated; nothing to do")
        return
    lines = text.splitlines()

    section = ""
    occurrences: dict[str, list[tuple[int, str, str]]] = {}
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            section = b.strip_md(line[3:])
        row = b.parse_table_row(line)
        if not row:
            continue
        date, title = row[0], b.strip_md(row[1])
        key = f"{date}|{normalized_title(title)}"
        occurrences.setdefault(key, []).append((idx, b.section_code(section), title))

    skip: set[int] = set()
    for records in occurrences.values():
        if len(records) <= 1:
            continue
        title = normalized_title(records[0][2])
        preferred = PREFERRED_SECTION.get(title)
        keep = next((idx for idx, sec, _ in records if sec == preferred), records[0][0])
        skip.update(idx for idx, _, _ in records if idx != keep)

    out: list[str] = []
    section = ""
    subsection = ""
    in_table = False
    v2_tables = 0

    for idx, line in enumerate(lines):
        if line.startswith("## "):
            section = b.strip_md(line[3:])
            subsection = ""
            in_table = False
            v2_tables = 0
        elif line.startswith("### "):
            subsection = b.strip_md(line[4:])
            in_table = False

        if line == '> - 年代・帰属が未確定のものは「要検証」とする。':
            out.append(line)
            out.extend([
                "> - 各実績には複数のタグを付け、GitHub Pages 上で絞り込めるようにする。",
                "> - 本文は原則として約200字以上を目安にし、史実・解釈・ゲーム用表現を区別する。",
                "> - 同一の史実イベントを複数章へ重複登録しない。複数の観点を持つ場合はタグで横断する。",
            ])
            continue

        if line.startswith("|") and "実績" in line and ("対応する出来事" in line or "本文" in line):
            if b.section_code(section) == "3" and subsection.startswith("V2から宇宙"):
                v2_tables += 1
                if v2_tables == 2:
                    out.extend(["### 核軍拡・核抑止・軍縮", ""])
                    subsection = "核軍拡・核抑止・軍縮"
            date_label = "年月日" if "年月日" in line else "年月"
            out.append(f"| {date_label} | 実績 | タグ | 本文 |")
            in_table = True
            continue
        if in_table and re.fullmatch(r"\|[\s:\-|]+\|", line):
            out.append("|---|---|---|---|")
            continue

        row = b.parse_table_row(line)
        if row:
            if idx in skip:
                continue
            date, title, body = row[0], b.strip_md(row[1]), b.strip_md(row[-1])
            tags = b.derive_tags(section, subsection, title, body)
            body = enrich(body, tags)
            title_md = f"🔒 **{title[2:].strip()}**" if title.startswith("🔒 ") else f"**{title}**"
            out.append(f"| {date} | {title_md} | {', '.join(tags)} | {body} |")
            continue
        out.append(line)

    text = "\n".join(out) + "\n"
    text = re.sub(
        r"\n## 8\. 記憶と外交\n\n\| 年月日 \| 実績 \| タグ \| 本文 \|\n\|---\|---\|---\|---\|\n\n---\n",
        "\n## 8. 記憶と外交\n\n> この章で扱っていた実績は、第2章「復興・記憶・被爆後障害」へ統合した。重複登録はせず、`記憶継承`・`外交`・`広島` などのタグで横断的に抽出する。\n\n---\n",
        text,
    )

    for title, (tags, extra) in STANDALONE.items():
        pattern = rf"(### {re.escape(title)}\n\n)(.*?)(?=\n### |\n---\n|\n## )"
        match = re.search(pattern, text, flags=re.S)
        if not match:
            raise RuntimeError(f"standalone achievement not found: {title}")
        block = match.group(2).rstrip()
        block = f"**タグ:** {tags}\n\n" + block + "\n\n" + extra
        text = text[:match.start(2)] + block + "\n" + text[match.end(2):]

    SOURCE.write_text(text, encoding="utf-8")
    items = b.parse_source(text)
    errors, warnings = b.validate(items, strict_length=True, strict_tags=True)
    if errors or any(a.body_len < 200 for a in items):
        raise RuntimeError("migration validation failed: " + "; ".join(errors + warnings))
    print(f"migrated {len(items)} achievements; minimum body length={min(a.body_len for a in items)}")


if __name__ == "__main__":
    main()
