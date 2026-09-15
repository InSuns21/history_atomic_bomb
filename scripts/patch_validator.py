from pathlib import Path

p = Path('scripts/build_site.py')
s = p.read_text(encoding='utf-8')
s = s.replace('MIN_BODY_CHARS = 180\nPREFERRED_BODY_CHARS = 200\n', '''MIN_BODY_CHARS = 120
PREFERRED_BODY_CHARS = 160

# These phrases are editorial guidance accidentally copied into many achievement bodies in an
# earlier migration. They are useful at chapter level, but per-card repetition is padding.
BANNED_BOILERPLATE = [
    "年表の一行として覚えるだけでなく",
    "結果を知る現在から当時を単純化せず",
    "この実績名はゲーム用の表現であり",
    "出来事そのものと、後世に与えられた象徴的な意味は別である",
    "技術上の成功、政治上の判断、倫理上の評価は同じ尺度では測れない",
    "被爆史を大きな死者数だけで語ると",
    "大量の破壊能力を維持することが『使わないための条件』とされた点に",
    "核抑止が機能したという評価と、誤警報・事故・誤算で破局し得たという評価は両立する",
    "年表の一行として",
]
''')
needle = '''        if not a.tags:\n            errors.append(f"missing tags: '{a.title}' line {a.source_line}")\n'''
insert = '''        for phrase in BANNED_BOILERPLATE:\n            if phrase in a.body:\n                errors.append(f"boilerplate padding in body: '{a.title}' line {a.source_line}: {phrase}")\n\n        if not a.tags:\n            errors.append(f"missing tags: '{a.title}' line {a.source_line}")\n'''
if needle not in s:
    raise SystemExit('validator insertion point not found')
s = s.replace(needle, insert, 1)

# Add cross-card repeated-sentence detection before returning from validate().
needle2 = '''    return errors, warnings\n\n\ndef esc(s: str) -> str:\n'''
insert2 = '''    sentence_owners: dict[str, list[Achievement]] = {}\n    for a in items:\n        for sentence in re.split(r"(?<=[。！？])", a.body):\n            sig = re.sub(r"\\s+|[。、・,.!?！？「」『』（）()：:]", "", unicodedata.normalize("NFKC", sentence))\n            if len(sig) >= 42:\n                sentence_owners.setdefault(sig, []).append(a)\n    for owners in sentence_owners.values():\n        unique_titles = list(dict.fromkeys(x.title for x in owners))\n        if len(unique_titles) >= 3:\n            errors.append("repeated long sentence across achievements: " + ", ".join(repr(x) for x in unique_titles[:6]))\n\n    return errors, warnings\n\n\ndef esc(s: str) -> str:\n'''
if needle2 not in s:
    raise SystemExit('return insertion point not found')
s = s.replace(needle2, insert2, 1)
p.write_text(s, encoding='utf-8')
print('patched body-quality validator')
