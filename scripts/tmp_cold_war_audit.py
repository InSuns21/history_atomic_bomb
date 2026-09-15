from pathlib import Path

path = Path('ACHIEVEMENTS.md')
text = path.read_text(encoding='utf-8')

repls = {
    'こちらの核は平和のためです': (
        '1949年のソ連核実験後、ソ連の宣伝は米国の原爆を「原子外交」や侵略の道具として非難する一方、自国の核保有については米国の核独占を終わらせ、平和陣営を強めたと語った。'
        '当時の米側によるソ連宣伝分析にも、ソ連の原爆保有を「平和の維持に重要な要因」とする論調が記録されている。敵の核は脅威、自国の核は抑止と平和のため、という語りは冷戦の両陣営で繰り返されることになる。'
    ),
    'きれいな核': (
        '1957年、米原子力委員会のルイス・ストローズやアーネスト・ローレンス、エドワード・テラーらは、核融合の比率を高めて放射性降下物を大幅に減らす「clean bomb」を公に論じた。'
        '同年の米政府文書にも、大出力の「clean bomb」を試験・開発する構想が現れる。核分裂生成物を減らせても、巨大な爆風・熱線・初期放射線そのものが消えるわけではない。「核兵器」と「きれい」が同じ語に収まった冷戦期の発想である。'
    ),
    '人類史上もっとも長い土曜日': (
        '1962年10月27日の「Black Saturday」には、キューバ上空で米U-2が撃墜され操縦士が死亡し、別のU-2はソ連領空へ迷い込みかけ、米軍内ではキューバ侵攻圧力も高まった。'
        '同日、米駆逐艦に追跡されたソ連潜水艦B-59では、艦長サヴィツキーが核魚雷の使用に近づく緊迫した状況となり、同乗していたアルヒーポフらの対応で発射には至らなかった。首脳が交渉していても、現場の誤認だけで核戦争へ転ぶ余地が残っていた。'
    ),
    'ボクも持ってるかもしれませんよ？': (
        'イスラエルの核政策は amimut（曖昧・不透明性）と呼ばれ、核兵器保有を公式には確認も否定もしない。核能力があると相手に推測させて抑止効果を狙いつつ、明示的な核保有宣言が引き起こす外交・不拡散上のコストを避ける構造である。'
        'そのため、核兵器をいつ完成・配備したかについて公開情報から一点の「保有開始日」を置くことは難しく、能力を示唆しながら確言を避けること自体が長期的な政策になった。'
    ),
}

# Correct the propaganda item's chronology to start with the verified 1949 test/propaganda shift.
lines = text.splitlines()
seen = set()
for i, line in enumerate(lines):
    if not line.startswith('|'):
        continue
    for title, body in repls.items():
        marker = f'**{title}**'
        if marker in line:
            parts = line.split('|')
            if len(parts) < 6:
                raise SystemExit(f'bad row for {title}')
            if title == 'こちらの核は平和のためです':
                parts[1] = ' 1949– '
            parts[4] = f' {body} '
            lines[i] = '|'.join(parts)
            seen.add(title)
            break

missing = set(repls) - seen
if missing:
    raise SystemExit(f'missing titles: {sorted(missing)}')

path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'updated {len(seen)} cold-war achievements')
