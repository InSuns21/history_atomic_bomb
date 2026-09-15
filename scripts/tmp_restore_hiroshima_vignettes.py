from pathlib import Path

path = Path('ACHIEVEMENTS.md')
text = path.read_text(encoding='utf-8')

repls = {
    '明日も遊びたかった': '銕谷伸一ちゃん（3歳11か月）は、東白島町の自宅前で大好きな三輪車に乗って遊んでいる最中、爆心地から約1.5kmで被爆。全身に重い火傷を負い、その夜に死亡した。父・信男さんは、幼い息子が一人で墓に入れば寂しがるだろう、死んでからも遊べるようにと、伸一ちゃんを焼け焦げた三輪車とともに自宅の庭へ埋葬した。',
    'お弁当食べたかった': '県立広島第二中学校1年生の折免滋さん（13歳）は、中島新町の建物疎開作業現場で被爆。母・シゲコさんは8月9日早朝、滋さんの遺体と、腹の下に抱きかかえるように残された真っ黒に焼けた弁当箱を発見した。弁当のおかずは、召集中の父と兄に代わって滋さん自身が開墾した畑から初めて収穫した作物で作られ、滋さんは喜んで持っていった。その弁当を食べる時間は来なかった。',
}

lines = text.splitlines()
seen = set()
for i, line in enumerate(lines):
    if not line.startswith('|'):
        continue
    for title, body in repls.items():
        if f'**{title}**' in line:
            parts = line.split('|')
            if len(parts) < 6:
                raise SystemExit(f'bad row for {title}')
            parts[4] = f' {body} '
            lines[i] = '|'.join(parts)
            seen.add(title)
            break

missing = set(repls) - seen
if missing:
    raise SystemExit(f'missing titles: {sorted(missing)}')

path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'restored {len(seen)} Hiroshima vignettes')
