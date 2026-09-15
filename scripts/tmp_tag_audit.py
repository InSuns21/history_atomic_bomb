from collections import Counter, defaultdict
from pathlib import Path
import importlib.util

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_site', root/'scripts'/'build_site.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
items = mod.parse_source((root/'ACHIEVEMENTS.md').read_text(encoding='utf-8'))

counts = Counter(t for a in items for t in a.tags)
print('=== TAG COUNTS ===')
for tag, n in sorted(counts.items(), key=lambda x:(-x[1], x[0])):
    print(f'{n:3} {tag}')

print('\n=== COMPOSITE / SUSPICIOUS TAGS ===')
for tag, n in sorted(counts.items()):
    if any(ch in tag for ch in ['・','/','／']) or tag in {'広島・長崎'}:
        print(f'{n:3} {tag}')

print('\n=== EXPLICIT VS DERIVED MISMATCHES ===')
for a in items:
    derived = set(mod.derive_tags(a.section, a.subsection, a.title, a.body))
    explicit = set(a.tags)
    missing = sorted(derived-explicit)
    extra = sorted(explicit-derived)
    if missing:
        print(f'[{a.source_line}] {a.title} | missing={missing} | tags={a.tags}')

print('\n=== HIROSHIMA/NAGASAKI COMPOSITE ROWS ===')
for a in items:
    if '広島・長崎' in a.tags:
        h = bool(__import__('re').search(r'広島|ヒロシマ|原爆ドーム|平和記念', a.title+' '+a.body))
        n = bool(__import__('re').search(r'長崎|ナガサキ|浦上', a.title+' '+a.body))
        print(f'[{a.source_line}] {a.title} | inferred_location={"広島" if h else ""}{"+" if h and n else ""}{"長崎" if n else ""} | tags={a.tags}')

print('\n=== TAGGED LOCATION WITHOUT TEXT CLUE ===')
for a in items:
    hay=a.title+' '+a.body
    if '広島' in a.tags and not __import__('re').search(r'広島|ヒロシマ|原爆ドーム|平和記念|カープ|張本|似島|折免|銕谷', hay):
        print(f'HIROSHIMA? [{a.source_line}] {a.title} | {a.tags}')
    if '長崎' in a.tags and not __import__('re').search(r'長崎|ナガサキ|浦上|永井隆|Fat Man|ボックスカー|小倉', hay):
        print(f'NAGASAKI? [{a.source_line}] {a.title} | {a.tags}')

print('\n=== ALL ITEMS ===')
for a in items:
    print(f'[{a.source_line}] {a.date} | {a.title} | {", ".join(a.tags)}')
