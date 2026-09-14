#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ACHIEVEMENTS.md"
OUT_DIR = ROOT / "_site"
MIN_BODY_CHARS = 180
PREFERRED_BODY_CHARS = 200

SECTION_TAGS = {
    "0": ["科学史"],
    "1": ["広島・長崎"],
    "2": ["被爆後", "復興"],
    "3": ["冷戦"],
    "4": ["原子力", "デュアルユース"],
    "5": ["南アジア"],
    "5A": ["北朝鮮"],
    "6": ["核時代"],
    "7": ["科学史"],
    "8": ["記憶継承", "外交"],
    "9": ["未来", "未解除"],
    "10": ["未来", "終端"],
}

SUBSECTION_TAGS = [
    (r"工学的課題", ["マンハッタン計画", "核燃料"]),
    (r"張本勲", ["広島", "被爆者証言", "記憶継承"]),
    (r"長崎戦後被爆史", ["長崎", "被爆後", "記憶継承"]),
    (r"V2から宇宙", ["ミサイル", "宇宙開発"]),
    (r"高速増殖炉", ["高速炉", "核燃料サイクル"]),
    (r"次の夢|星と核融合", ["核融合"]),
    (r"錬金術", ["元素変換"]),
]

KEYWORD_TAGS = [
    (r"広島|ヒロシマ|原爆ドーム|平和記念", "広島"),
    (r"長崎|ナガサキ|浦上", "長崎"),
    (r"被爆|原爆症|黒い雨|ケロイド|放射線障害", "被爆"),
    (r"原爆.{0,20}投下|核兵器実戦使用|核使用", "核兵器使用"),
    (r"救護|似島|治療|診療|医療", "救護・医療"),
    (r"記憶|資料館|展示|証言|千羽鶴|平和の灯", "記憶継承"),
    (r"大統領|G7|首脳|国連|外交|訪問", "外交"),
    (r"核分裂|中性子|原子核|ウラン|U-235|プルトニウム|Pu-239", "原子核物理"),
    (r"マンハッタン|Manhattan|ロスアラモス|Trinity|Little Boy|Fat Man|爆縮|濃縮|Y-12|K-25|S-50", "マンハッタン計画"),
    (r"ICBM|SLBM|ミサイル|Polaris|Poseidon|Trident|Minuteman|R-7|V2", "ミサイル"),
    (r"潜水艦|SSBN|Nautilus", "原潜・SLBM"),
    (r"相互確証破壊|第二撃|核抑止|抑止", "核抑止"),
    (r"NPT|TPNW|INF|START|SALT|軍縮|廃絶|パグウォッシュ|ABM条約", "軍縮・条約"),
    (r"不拡散|保障措置|核拡散", "核拡散"),
    (r"核融合|熱核|恒星|地上に太陽", "核融合"),
    (r"核実験|Trinity|Castle Bravo|RDS-1|Tsar Bomba|Pokhran|Chagai|Starfish Prime|Rainier", "核実験"),
    (r"原子炉|原発|もんじゅ|常陽|福島|チェルノブイリ|スリーマイル|再処理|MOX|プルサーマル", "原子力"),
    (r"事故", "原発事故"),
    (r"インド|パキスタン|Pokhran|Chagai|ガンジー", "南アジア"),
    (r"北朝鮮|米朝|ハノイ|シンガポール", "北朝鮮"),
    (r"ソ連|米ソ|冷戦|キューバ|レイキャビク", "冷戦"),
    (r"イスラエル|ディモナ|amimut|核曖昧", "イスラエル"),
    (r"映画|アニメ|ゴジラ|鉄腕アトム|カープ|歌謡", "文化"),
    (r"要検証|史料上の留保|留保あり|演出名|帰属には.*留保", "要検証"),
]


@dataclass
class Achievement:
    date: str
    title: str
    body: str
    tags: list[str]
    section: str
    subsection: str
    source_line: int
    future: bool = False
    repeatable: bool = False
    tags_explicit: bool = False

    @property
    def body_len(self) -> int:
        return len(re.sub(r"\s+", "", self.body))

    @property
    def key(self) -> str:
        norm_title = unicodedata.normalize("NFKC", self.title).replace("🔒", "").strip()
        return f"{self.date}|{norm_title}"


def strip_md(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    return text.strip()


def section_code(heading: str) -> str:
    m = re.match(r"(\d+A?)\.", heading)
    return m.group(1) if m else ""


def unique(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    return [x for x in seq if x and not (x in seen or seen.add(x))]


def parse_tag_text(text: str) -> list[str]:
    text = strip_md(text).replace("#", "")
    return unique([t.strip() for t in re.split(r"[,、]+", text) if t.strip()])


def derive_tags(section: str, subsection: str, title: str, body: str) -> list[str]:
    tags = list(SECTION_TAGS.get(section_code(section), []))
    for pattern, extra in SUBSECTION_TAGS:
        if re.search(pattern, subsection):
            tags.extend(extra)
    haystack = " ".join([title, body])
    for pattern, tag in KEYWORD_TAGS:
        if re.search(pattern, haystack, re.I):
            tags.append(tag)
    if title.startswith("🔒") or section_code(section) == "9":
        tags.extend(["未来", "未解除"])
    if "反復" in title:
        tags.append("反復")
    return unique(tags)


def parse_table_row(line: str) -> list[str] | None:
    if not line.startswith("|") or not line.rstrip().endswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 3:
        return None
    if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
        return None
    if cells[0] in {"年月", "年月日"} and "実績" in cells[1]:
        return None
    return cells


def parse_source(text: str) -> list[Achievement]:
    lines = text.splitlines()
    out: list[Achievement] = []
    section = ""
    subsection = ""
    i = 0
    while i < len(lines):
        raw = lines[i]
        if raw.startswith("## "):
            section = strip_md(raw[3:])
            subsection = ""
            i += 1
            continue
        if raw.startswith("### "):
            subsection = strip_md(raw[4:])
            j = i + 1
            block: list[str] = []
            while j < len(lines) and not lines[j].startswith("## ") and not lines[j].startswith("### "):
                block.append(lines[j])
                j += 1
            joined = "\n".join(block)
            if "**解除条件:**" in joined:
                title = subsection
                tag_line = next((x.strip() for x in block if x.strip().startswith("**タグ:**")), "")
                explicit_tags = parse_tag_text(tag_line.replace("**タグ:**", "", 1)) if tag_line else []
                body_parts: list[str] = []
                examples: list[str] = []
                for bline in block:
                    s = bline.strip()
                    if not s or s.startswith("**タグ:**"):
                        continue
                    if s.startswith("**解除条件:**"):
                        body_parts.append(strip_md(s.replace("**解除条件:**", "解除条件：", 1)))
                    elif s.startswith(">"):
                        content = strip_md(s.lstrip("> "))
                        if content:
                            body_parts.append(content)
                    elif s.startswith("-"):
                        examples.append(strip_md(s.lstrip("- ")))
                    elif not s.startswith("|"):
                        body_parts.append(strip_md(s))
                if examples:
                    body_parts.append("代表例：" + "、".join(examples) + "。")
                body = " ".join(x for x in body_parts if x)
                tags = explicit_tags or derive_tags(section, subsection, title, body)
                out.append(Achievement(
                    date="20XX" if title.startswith("🔒") else "反復",
                    title=title,
                    body=body,
                    tags=tags,
                    section=section,
                    subsection="",
                    source_line=i + 1,
                    future=title.startswith("🔒"),
                    repeatable="反復" in title,
                    tags_explicit=bool(explicit_tags),
                ))
            i += 1
            continue
        row = parse_table_row(raw)
        if row:
            date, title, body = row[0], strip_md(row[1]), strip_md(row[-1])
            explicit_tags = parse_tag_text(row[2]) if len(row) >= 4 else []
            tags = explicit_tags or derive_tags(section, subsection, title, body)
            out.append(Achievement(
                date=date,
                title=title,
                body=body,
                tags=tags,
                section=section,
                subsection=subsection,
                source_line=i + 1,
                future=title.startswith("🔒"),
                repeatable="反復" in title,
                tags_explicit=bool(explicit_tags),
            ))
        i += 1
    return out


def validate(items: list[Achievement], strict_length: bool, strict_tags: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    by_key: dict[str, Achievement] = {}
    by_exact_body: dict[str, Achievement] = {}
    for a in items:
        if a.key in by_key:
            b = by_key[a.key]
            errors.append(f"duplicate achievement key: {a.key} (lines {b.source_line}, {a.source_line})")
        else:
            by_key[a.key] = a
        body_sig = re.sub(r"\s+|[。、・,.!?！？「」『』（）()：:]", "", unicodedata.normalize("NFKC", a.body))
        if len(body_sig) >= 50:
            if body_sig in by_exact_body:
                b = by_exact_body[body_sig]
                errors.append(f"duplicate achievement body: '{a.title}' and '{b.title}'")
            else:
                by_exact_body[body_sig] = a
        if not a.tags:
            errors.append(f"missing tags: '{a.title}' line {a.source_line}")
        elif strict_tags and not a.tags_explicit:
            errors.append(f"tags must be explicit in ACHIEVEMENTS.md: '{a.title}' line {a.source_line}")
        if a.body_len < MIN_BODY_CHARS:
            msg = f"short body ({a.body_len} chars): '{a.title}' line {a.source_line}"
            (errors if strict_length else warnings).append(msg)
        elif a.body_len < PREFERRED_BODY_CHARS:
            warnings.append(f"body below preferred {PREFERRED_BODY_CHARS} chars ({a.body_len}): '{a.title}' line {a.source_line}")
    return errors, warnings


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(items: list[Achievement]) -> str:
    payload = [asdict(a) | {"body_len": a.body_len} for a in items]
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    tags = sorted({t for a in items for t in a.tags})
    tag_buttons = "\n".join(f'<button class="tag" data-tag="{esc(t)}">#{esc(t)}</button>' for t in tags)
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="核兵器・原子力・被爆史・冷戦・核軍縮・科学史を、実績形式で時系列に読む歴史ゲーム資料。">
<title>核実績ゲーム — Achievements</title>
<style>
:root {{ color-scheme: light dark; --bg:#f5f3ee; --fg:#191919; --muted:#686868; --card:#fff; --line:#d8d3c8; --accent:#9c2f2f; --chip:#ece7dc; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#171717; --fg:#eee; --muted:#aaa; --card:#202020; --line:#383838; --accent:#ef9b9b; --chip:#2d2d2d; }} }}
* {{ box-sizing:border-box; }} body {{ margin:0; font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif; background:var(--bg); color:var(--fg); line-height:1.8; }}
header {{ padding:2.2rem 1rem 1.3rem; max-width:1100px; margin:auto; }} h1 {{ margin:0 0 .35rem; font-size:clamp(1.7rem,4vw,2.7rem); }} .lead {{ color:var(--muted); max-width:60rem; }}
.controls {{ position:sticky; top:0; z-index:4; backdrop-filter:blur(12px); background:color-mix(in srgb,var(--bg) 88%,transparent); border-block:1px solid var(--line); }}
.controls-inner {{ max-width:1100px; margin:auto; padding:.8rem 1rem; display:grid; gap:.7rem; }}
.search {{ width:100%; padding:.75rem .9rem; border:1px solid var(--line); border-radius:.7rem; background:var(--card); color:var(--fg); font-size:1rem; }}
.tags {{ display:flex; gap:.45rem; flex-wrap:wrap; max-height:7.4rem; overflow:auto; }} .tag {{ border:1px solid var(--line); border-radius:999px; padding:.28rem .65rem; background:var(--chip); color:var(--fg); cursor:pointer; }} .tag.active {{ border-color:var(--accent); color:var(--accent); font-weight:700; }}
.meta-bar {{ display:flex; justify-content:space-between; gap:1rem; color:var(--muted); font-size:.9rem; }} main {{ max-width:1100px; margin:1.4rem auto 4rem; padding:0 1rem; }}
.achievement {{ background:var(--card); border:1px solid var(--line); border-radius:1rem; padding:1rem 1.1rem; margin:.8rem 0; box-shadow:0 1px 0 rgba(0,0,0,.03); }} .achievement.future {{ border-style:dashed; }}
.achievement h2 {{ margin:.05rem 0 .25rem; font-size:1.25rem; line-height:1.45; }} .date {{ color:var(--accent); font-weight:800; font-variant-numeric:tabular-nums; }} .section {{ color:var(--muted); font-size:.86rem; }}
.achievement p {{ margin:.65rem 0 .4rem; }} .chips {{ display:flex; flex-wrap:wrap; gap:.35rem; }} .chip {{ font-size:.78rem; padding:.12rem .5rem; border-radius:999px; background:var(--chip); }}
.empty {{ display:none; padding:2rem 0; color:var(--muted); }} footer {{ max-width:1100px; margin:0 auto; padding:0 1rem 3rem; color:var(--muted); }}
</style>
</head>
<body>
<header><h1>核実績ゲーム</h1><p class="lead">1945年に何が起こるかは、もう知っている。では、その後の人類は何をしたのか。科学史、被爆、復興、核抑止、軍縮、平和利用、そしてまだ解除されていない未来実績までを時系列で読む。</p></header>
<div class="controls"><div class="controls-inner">
<input id="search" class="search" type="search" placeholder="実績名・本文・タグ・年代を検索" aria-label="実績を検索">
<div class="tags" aria-label="タグで絞り込み">{tag_buttons}</div>
<div class="meta-bar"><span id="count"></span><button id="clear" class="tag" type="button">絞り込み解除</button></div>
</div></div>
<main><div id="list"></div><p id="empty" class="empty">条件に一致する実績はありません。</p></main>
<footer>Source: <code>ACHIEVEMENTS.md</code> / Generated by <code>scripts/build_site.py</code></footer>
<script id="achievement-data" type="application/json">{data}</script>
<script>
const items = JSON.parse(document.getElementById('achievement-data').textContent);
const list = document.getElementById('list'); const count = document.getElementById('count'); const empty = document.getElementById('empty'); const search = document.getElementById('search');
const active = new Set();
function escapeHtml(s){{return s.replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]));}}
function render(){{
 const q=search.value.trim().toLowerCase();
 const shown=items.filter(a=>{{ const hay=[a.date,a.title,a.body,a.section,a.subsection,...a.tags].join(' ').toLowerCase(); const tagOK=[...active].every(t=>a.tags.includes(t)); return (!q||hay.includes(q))&&tagOK; }});
 list.innerHTML=shown.map(a=>`<article class="achievement ${{a.future?'future':''}}"><div class="date">${{escapeHtml(a.date)}}</div><h2>${{escapeHtml(a.title)}}</h2><div class="section">${{escapeHtml(a.section)}}${{a.subsection?' / '+escapeHtml(a.subsection):''}}</div><p>${{escapeHtml(a.body)}}</p><div class="chips">${{a.tags.map(t=>`<span class="chip">#${{escapeHtml(t)}}</span>`).join('')}}</div></article>`).join('');
 count.textContent=`${{shown.length}} / ${{items.length}} 実績`;
 empty.style.display=shown.length?'none':'block';
}}
document.querySelectorAll('[data-tag]').forEach(b=>b.addEventListener('click',()=>{{const t=b.dataset.tag; active.has(t)?active.delete(t):active.add(t); b.classList.toggle('active'); render();}}));
search.addEventListener('input',render); document.getElementById('clear').addEventListener('click',()=>{{active.clear(); search.value=''; document.querySelectorAll('[data-tag]').forEach(b=>b.classList.remove('active')); render();}}); render();
</script>
</body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate source before building")
    parser.add_argument("--strict-length", action="store_true", help=f"fail when a body is shorter than {MIN_BODY_CHARS} characters")
    parser.add_argument("--strict-tags", action="store_true", help="require tags to be written explicitly in ACHIEVEMENTS.md")
    args = parser.parse_args()
    text = SOURCE.read_text(encoding="utf-8")
    items = parse_source(text)
    errors, warnings = validate(items, args.strict_length, args.strict_tags)
    for warning in warnings:
        print(f"::warning::{warning}")
    for error in errors:
        print(f"::error::{error}")
    if not items:
        print("::error::no achievements parsed")
        return 2
    if errors:
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(render(items), encoding="utf-8")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(items)} achievements -> {OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
