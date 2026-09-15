from pathlib import Path

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

anchor='''KEYWORD_TAGS = [\n'''
# Add forbidden legacy tags after the keyword table, immediately before the dataclass.
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
print('patched tag fallback and validation rules')
