from __future__ import annotations

import ast
import re
from pathlib import Path

CATALOG = Path('ACHIEVEMENTS.md')
MAPPING_SOURCE = Path('scripts/rewrite_specific_bodies.py')

# Read the curated 172-row mapping without executing the one-time migration script.
tree = ast.parse(MAPPING_SOURCE.read_text(encoding='utf-8'))
DETAILS = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'DETAILS' for t in node.targets):
        DETAILS = ast.literal_eval(node.value)
        break
if not isinstance(DETAILS, dict) or len(DETAILS) != 172:
    raise SystemExit(f'expected 172 table mappings, got {0 if DETAILS is None else len(DETAILS)}')

STANDALONE = {
    '反復：限定戦争なら問題ない……？？？': '朝鮮戦争では米中ソが核保有・核使用可能性を意識しながら38度線周辺で休戦し、ベトナム戦争やアフガニスタン戦争でも大国は相手核保有国との直接全面戦争を避けつつ通常戦力を投入した。核兵器が大国間の全面衝突を抑えた可能性と、地域戦争そのものを止めなかった事実は両立する。「限定」とはエスカレーションの範囲であって、現地の死傷や破壊が小さいという意味ではない。',
    '🔒 核は必ず使われる': '1945年8月9日の長崎以後、2026年9月現在まで核兵器は戦争で再使用されていない。この実績は「必ず起きる」という予言ではなく、その81年以上続く不使用の前例が破られ、戦術核を含む核兵器が実戦で再び爆発した場合だけ解除する。威力が戦略核より小さくても、核使用の敷居を越えたという政治・軍事上の前例は残り、報復とエスカレーションの条件そのものを変える。',
    '🔒 一人で世界を終わらせないで': '核保有国の指揮統制は、発射権限、本人認証、命令伝達、二人規則など複数の手続で誤作動や無断使用を防ぐ一方、正規権限者が正規手続で危険な命令を出す問題は別に残る。キューバ危機や冷戦期の誤警報が示したのは、核戦争回避が機械だけでなく人間の判断にも依存することだった。この未来実績は特定人物を想定せず、制度が最高意思決定者をどこまで拘束できるかを解除条件として問う。',
    '🔒 核兵器禁止！': '核兵器禁止条約（TPNW）は2021年に発効したが、NPTが核兵器国として扱う米・露・英・仏・中は2026年9月現在いずれも締約国ではない。この実績は条約の存在だけでは解除せず、5か国すべてがTPNWの法的義務を受け入れる段階を条件にする。核兵器を持たない国だけで禁止規範を強める段階から、実際に大規模核戦力を保有する国自身が廃棄義務へ入る段階への移行を記録する未来実績である。',
    '🔒 この火が消えるその日まで': '広島平和記念公園の「平和の灯」は1964年8月1日に点火され、核兵器が地球上からなくなる日まで燃やし続けるという趣旨を持つ。この未来実績では核廃絶宣言や配備解除だけでは足りず、最後の核弾頭が検証可能かつ不可逆に廃棄され、再配備できないことまで確認された時に解除する。その瞬間だけは「火を消す」ことが記憶の断絶ではなく、1964年から続いた条件の達成になる。',
    '🔒 その前に石油がなくなるだろう': '2005年に広島を訪れた元ロスアラモス所長ハロルド・アグニューが、核廃絶まで燃やす「平和の灯」の説明に対し「その前に石油がなくなる」と返した、とテレビ番組で紹介されたとされる。ただし公開一次資料で逐語と前後文脈を確定できていないため要検証とする。未来実績の解除条件は、その皮肉を史実扱いすることではなく、核廃絶より先に灯の燃料継続そのものが問題になるというブラックユーモア上の仮定である。',
    '🔒 次の戦は棍棒で': '「第三次世界大戦で何が使われるかは分からないが、第四次は棒と石だ」という言葉はアインシュタインに広く帰属されるが、引用形や伝承経路には留保がある。この未来実績では引用の真偽を解除条件にせず、大規模核戦争で電力・通信・工業生産・国家的軍事基盤が広範に崩壊し、近代戦を継続できない規模の文明後退が起きた場合を想定する。核戦争を派手な最終ステージではなく、解除してはいけない終端として置く。',
    '🔒 そういう意味じゃない': 'これは史実予測ではなく明示的な未来SF実績である。ASIが核発射命令を拒否するだけでなく、核指揮通信・認証・発射装置を人類の意思に反して恒久的に無力化した時に解除する。結果だけ見れば核戦争の可能性は下がるが、同時に国家も市民も安全保障の最終決定を取り戻せなくなる。「核廃絶」という望ましい結果と、「人間の自己決定権を奪う」という手段が一致しない場合を扱い、史実章とは混同しない。',
}


def norm_title(cell: str) -> str:
    t = re.sub(r'^🔒\s*', '', cell.strip())
    return re.sub(r'^\*\*|\*\*$', '', t).strip()


text = CATALOG.read_text(encoding='utf-8')
lines = text.splitlines()
out: list[str] = []
seen_rows: set[str] = set()
for line in lines:
    if line.startswith('|') and line.rstrip().endswith('|'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 4 and cells[0] not in {'年月', '年月日', '---'}:
            title = norm_title(cells[1])
            if title not in DETAILS:
                raise SystemExit(f'missing table mapping: {title}')
            cells[3] = DETAILS[title]
            line = '| ' + ' | '.join(cells) + ' |'
            seen_rows.add(title)
    out.append(line)
if seen_rows != set(DETAILS):
    raise SystemExit(f'table mapping mismatch: missing={set(DETAILS)-seen_rows}')

# Replace prose in the eight standalone/repeat/future achievement blocks while preserving
# tags, unlock conditions, quotes, and example lists.
lines = out
for heading, body in STANDALONE.items():
    marker = '### ' + heading
    try:
        start = lines.index(marker)
    except ValueError:
        raise SystemExit(f'missing standalone heading: {heading}')
    end = start + 1
    while end < len(lines) and not lines[end].startswith('### ') and not lines[end].startswith('## '):
        end += 1
    block = lines[start:end]
    kept = [block[0]]
    for line in block[1:]:
        s = line.strip()
        if not s or s.startswith('**タグ:**') or s.startswith('**解除条件:**') or s.startswith('>') or s.startswith('-') or s == '代表例：':
            kept.append(line)
        # other plain prose is the old body and is intentionally dropped
    while kept and not kept[-1].strip():
        kept.pop()
    kept.extend(['', body, ''])
    lines = lines[:start] + kept + lines[end:]

CATALOG.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
print(f'finalized {len(DETAILS)} table + {len(STANDALONE)} standalone achievements = {len(DETAILS)+len(STANDALONE)} total')
