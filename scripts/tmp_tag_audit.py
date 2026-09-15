from collections import Counter
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
lines = (root/'ACHIEVEMENTS.md').read_text(encoding='utf-8').splitlines()

SECTION_TAGS = {
    '0':['科学史'],'1':['広島','長崎'],'2':['被爆後','復興'],'3':['冷戦'],'4':['原子力','デュアルユース'],
    '5':['南アジア'],'5A':['北朝鮮'],'6':['核時代'],'7':['科学史'],'8':['記憶継承','外交'],'9':['未来','未解除'],'10':['未来','終端']
}
KEYWORD_TAGS = [
    (r'広島|ヒロシマ|原爆ドーム|平和記念|カープ|張本|似島|折免|銕谷','広島'),
    (r'長崎|ナガサキ|浦上|永井隆|Fat Man|ボックスカー|小倉','長崎'),
    (r'被爆|原爆症|黒い雨|ケロイド|放射線障害','被爆'),
    (r'原爆.{0,20}投下|核兵器実戦使用|核使用','核兵器使用'),
    (r'救護|似島|治療|診療|医療','救護・医療'),
    (r'記憶|資料館|展示|証言|千羽鶴|平和の灯','記憶継承'),
    (r'大統領|G7|首脳|国連|外交|訪問','外交'),
    (r'核分裂|中性子|原子核|ウラン|U-235|プルトニウム|Pu-239','原子核物理'),
    (r'マンハッタン|Manhattan|ロスアラモス|Trinity|Little Boy|Fat Man|爆縮|濃縮|Y-12|K-25|S-50','マンハッタン計画'),
    (r'ICBM|SLBM|ミサイル|Polaris|Poseidon|Trident|Minuteman|R-7|V2','ミサイル'),
    (r'潜水艦|SSBN|Nautilus','原潜'),
    (r'SLBM|Polaris|Poseidon|Trident','SLBM'),
    (r'相互確証破壊|第二撃|核抑止|抑止','核抑止'),
    (r'NPT|TPNW|INF|START|SALT|軍縮|廃絶|パグウォッシュ|ABM条約','軍縮・条約'),
    (r'不拡散|保障措置|核拡散','核拡散'),
    (r'核融合|熱核|恒星|地上に太陽','核融合'),
    (r'核実験|Trinity|Castle Bravo|RDS-1|Tsar Bomba|Pokhran|Chagai|Starfish Prime|Rainier','核実験'),
    (r'原子炉|原発|もんじゅ|常陽|福島|チェルノブイリ|スリーマイル|再処理|MOX|プルサーマル','原子力'),
    (r'事故','原発事故'),
    (r'インド|パキスタン|Pokhran|Chagai|ガンジー','南アジア'),
    (r'北朝鮮|米朝|ハノイ|シンガポール','北朝鮮'),
    (r'ソ連|米ソ|冷戦|キューバ|レイキャビク','冷戦'),
    (r'イスラエル|ディモナ|amimut|核曖昧','イスラエル'),
    (r'映画|アニメ|ゴジラ|鉄腕アトム|カープ|歌謡|楽曲','文化'),
]

def strip_md(s):
    return re.sub(r'\*\*(.*?)\*\*', r'\1', s).strip()

def section_code(s):
    m=re.match(r'(\d+A?)\.',s)
    return m.group(1) if m else ''

items=[]
section=''; subsection=''
for lineno,line in enumerate(lines,1):
    if line.startswith('## '):
        section=strip_md(line[3:]); subsection=''; continue
    if line.startswith('### '):
        subsection=strip_md(line[4:]); continue
    if not (line.startswith('|') and line.rstrip().endswith('|')): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells)<4 or cells[0] in {'年月','年月日'} or all(re.fullmatch(r':?-{3,}:?',c.replace(' ','')) for c in cells): continue
    date,title,tags,body=cells[0],strip_md(cells[1]),[t.strip() for t in re.split(r'[,、]+',cells[2]) if t.strip()],strip_md(cells[-1])
    items.append((lineno,date,title,tags,body,section,subsection))

# standalone future/repeat achievements
for i,line in enumerate(lines):
    if not line.startswith('### '): continue
    title=strip_md(line[4:])
    j=i+1; block=[]
    while j<len(lines) and not lines[j].startswith('## ') and not lines[j].startswith('### '):
        block.append(lines[j]); j+=1
    if not any('**解除条件:**' in x for x in block): continue
    tag_line=next((x for x in block if x.strip().startswith('**タグ:**')), '')
    tags=[t.strip() for t in re.split(r'[,、]+',tag_line.replace('**タグ:**','').replace('**','')) if t.strip()]
    body=' '.join(strip_md(x.lstrip('> ')) for x in block if x.strip() and not x.strip().startswith('**タグ:**'))
    items.append((i+1,'20XX' if title.startswith('🔒') else '反復',title,tags,body,section,''))

counts=Counter(t for _,_,_,tags,_,_,_ in items for t in tags)
print('=== TAG COUNTS ===')
for tag,n in sorted(counts.items(),key=lambda x:(-x[1],x[0])): print(f'{n:3} {tag}')

print('\n=== COMPOSITE / SUSPICIOUS TAGS ===')
for tag,n in sorted(counts.items()):
    if any(ch in tag for ch in ['・','/','／']) or tag=='広島・長崎': print(f'{n:3} {tag}')

print('\n=== LIKELY MISSING TAGS ===')
for lineno,date,title,tags,body,section,subsection in items:
    hay=title+' '+body
    expected=set(SECTION_TAGS.get(section_code(section),[]))
    for pat,tag in KEYWORD_TAGS:
        if re.search(pat,hay,re.I): expected.add(tag)
    if title.startswith('🔒'): expected|={'未来','未解除'}
    missing=sorted(expected-set(tags))
    if missing: print(f'[{lineno}] {title} | missing={missing} | tags={tags}')

print('\n=== HIROSHIMA/NAGASAKI COMPOSITE ROWS ===')
for lineno,date,title,tags,body,section,subsection in items:
    if '広島・長崎' not in tags: continue
    hay=title+' '+body
    h=bool(re.search(r'広島|ヒロシマ|原爆ドーム|平和記念|カープ|張本|似島|折免|銕谷',hay))
    n=bool(re.search(r'長崎|ナガサキ|浦上|永井隆|Fat Man|ボックスカー|小倉',hay))
    loc=('広島' if h else '')+('+' if h and n else '')+('長崎' if n else '')
    print(f'[{lineno}] {title} | inferred_location={loc or "?"} | tags={tags}')

print('\n=== ALL ITEMS ===')
for lineno,date,title,tags,body,section,subsection in items:
    print(f'[{lineno}] {date} | {title} | {", ".join(tags)}')
