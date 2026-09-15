from pathlib import Path

path = Path('ACHIEVEMENTS.md')
text = path.read_text(encoding='utf-8')

rule = '> - 実績名が実在の発言・楽曲・作品・ゲーム文化などのオマージュである場合、元ネタが歴史的意味を担うなら本文で由来を残す。オマージュを本人の実際の発言と誤認させない。\n'
anchor = '> - 本文は文字数を目的化しない。原則120字以上を最低線、160～300字程度を目安に、その実績固有の人物・場所・技術・因果関係で説明する。一般論の水増しは禁止する。史実・解釈・ゲーム用表現を区別する。\n'
if rule not in text:
    if anchor not in text:
        raise SystemExit('intro anchor not found')
    text = text.replace(anchor, anchor + rule, 1)

new_body = (
    'シラードは1933年9月、ロンドンで、一つの核反応が複数の中性子を放ち次の反応を起こすなら自己持続的連鎖反応が可能になると着想した。'
    '当時、核分裂はまだ未発見だった。実績名はMr.Childrenの楽曲『Everything is made from a dream』へのオマージュ。'
    '同曲は、核爆弾や細菌兵器も名もない化学者の純粋で小さな夢から始まったのではないかと問い、科学や「夢」の両義性を歌う。'
    'シラード本人の言葉ではなく、後世の作品を重ねたゲーム用表現である。'
)

lines = text.splitlines()
count = 0
for i, line in enumerate(lines):
    if '| 1933 | **Everything is made from a dream** |' in line:
        lines[i] = f'| 1933 | **Everything is made from a dream** | 科学史, 原子核物理 | {new_body} |'
        count += 1
if count != 1:
    raise SystemExit(f'expected one target row, found {count}')

path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('audited achievements 001-010: one homage restoration, nine retained')
