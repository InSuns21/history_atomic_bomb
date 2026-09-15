from pathlib import Path
import re

# Add a small cross-cutting tag for surrender/end-of-war events that would otherwise become tagless
# after removing the old Hiroshima/Nagasaki section tag.
ap=Path('ACHIEVEMENTS.md')
a=ap.read_text(encoding='utf-8')
for title in ['あらかじめ裏切られた条約','100万の兵を救った……？','みなさん、これが最後です']:
    pat=rf'(^\|[^\n]*\*\*{re.escape(title)}\*\*\s*\|)([^|]*)(\|)'
    m=re.search(pat,a,re.M)
    if not m:
        raise SystemExit(f'missing achievement for end-of-war tag: {title}')
    tags=[t.strip() for t in m.group(2).split(',') if t.strip()]
    if '終戦' not in tags:
        tags.append('終戦')
    a=a[:m.start(2)]+' '+', '.join(tags)+' '+a[m.end(2):]
ap.write_text(a,encoding='utf-8')

p=Path('scripts/build_site.py')
s=p.read_text(encoding='utf-8')
repls={
'    "1": ["広島・長崎"],':'    "1": [],',
'    "2": ["被爆後", "復興"],':'    "2": [],',
'    "4": ["原子力", "デュアルユース"],':'    "4": [],',
'    (r"V2から宇宙", ["ミサイル", "宇宙開発"]),':'    (r"V2から宇宙", ["ミサイル"]),',
'    (r"潜水艦|SSBN|Nautilus", "原潜・SLBM"),':'    (r"潜水艦|SSBN|Nautilus", "原潜"),\n    (r"SLBM|Polaris|Poseidon|Trident", "SLBM"),',
'    (r"事故", "原発事故"),':'    (r"スリーマイル|チェルノブイリ|福島第一|ナトリウム.*漏", "原子力事故"),',
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'missing build-site patch target: {old}')
    s=s.replace(old,new)

needle='''\n\n@dataclass\nclass Achievement:'''
insert='''\n\nFORBIDDEN_TAGS = {"広島・長崎", "原潜・SLBM", "原発事故"}\n\n@dataclass\nclass Achievement:'''
if 'FORBIDDEN_TAGS =' not in s:
    if needle not in s:
        raise SystemExit('missing dataclass insertion target')
    s=s.replace(needle,insert,1)

old='''        if not a.tags:\n            errors.append(f"missing tags: '{a.title}' line {a.source_line}")\n        elif strict_tags and not a.tags_explicit:\n            errors.append(f"tags must be explicit in ACHIEVEMENTS.md: '{a.title}' line {a.source_line}")\n'''
new='''        if not a.tags:\n            errors.append(f"missing tags: '{a.title}' line {a.source_line}")\n        elif strict_tags and not a.tags_explicit:\n            errors.append(f"tags must be explicit in ACHIEVEMENTS.md: '{a.title}' line {a.source_line}")\n        forbidden = sorted(set(a.tags) & FORBIDDEN_TAGS)\n        if forbidden:\n            errors.append(f"forbidden legacy tags in '{a.title}' line {a.source_line}: {', '.join(forbidden)}")\n        if a.future and not {"未来", "未解除"}.issubset(set(a.tags)):\n            errors.append(f"future achievement missing future tags: '{a.title}' line {a.source_line}")\n'''
if old not in s:
    raise SystemExit('missing validation insertion target')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched end-of-war tags plus tag fallback and validation rules')
