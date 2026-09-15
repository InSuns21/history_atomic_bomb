from pathlib import Path
import re

src = Path('ACHIEVEMENTS.md').read_text(encoding='utf-8').splitlines()
out = ['date\ttitle\ttags\tbody']
titles = []
for line in src:
    if not line.startswith('|'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) != 4 or cells[0] in {'年月','年月日','---'}:
        continue
    date, title, tags, body = cells
    title = re.sub(r'^🔒\s*', '', title)
    title = re.sub(r'^\*\*|\*\*$', '', title).strip()
    out.append('\t'.join([date, title, tags, body]))
    titles.append(f'{len(titles)+1:03d}\t{date}\t{title}')
Path('tmp_achievement_index.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
Path('tmp_titles.tsv').write_text('\n'.join(titles) + '\n', encoding='utf-8')
