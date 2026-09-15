#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import build_site as legacy

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ACHIEVEMENTS.md"
OUT_DIR = ROOT / "_site"


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    path: str
    description: str


CATEGORY_CONFIG = [
    Category(
        "science",
        "科学史・核技術の成立",
        "achievements/00_science.md",
        "原子・放射能・核分裂・連鎖反応から、核融合や元素合成などの関連科学史まで。",
    ),
    Category(
        "bombing",
        "1945年8月・被爆",
        "achievements/01_hiroshima_nagasaki.md",
        "広島・長崎への原爆投下、直後の被害、救護、そして終戦前後の出来事。",
    ),
    Category(
        "aftermath",
        "復興・被爆後・記憶継承",
        "achievements/02_aftermath_memory.md",
        "被爆後障害、医療、都市復興、証言、資料館、追悼、外交と記憶の継承。",
    ),
    Category(
        "cold-war",
        "冷戦・核抑止・軍縮",
        "achievements/03_cold_war_deterrence.md",
        "核軍拡、ミサイル、第二撃能力、核抑止、軍縮と、核時代に反復する基本問題。",
    ),
    Category(
        "civil-nuclear",
        "原子力平和利用・デュアルユース",
        "achievements/04_civil_nuclear.md",
        "Atoms for Peace、原子炉、核燃料サイクル、原子力事故、核融合発電への道。",
    ),
    Category(
        "national-cases",
        "各国・地域の核史",
        "achievements/05_national_cases.md",
        "フランス、南アジア、北朝鮮など、各国・地域が核兵器と原子力をどう位置付けたか。",
    ),
    Category(
        "future",
        "未来実績",
        "achievements/06_future.md",
        "まだ解除されていない未来実績と、核時代の終端として残る二つの可能性。",
    ),
]

CATEGORY_BY_PATH = {c.path: c for c in CATEGORY_CONFIG}
CATEGORY_BY_CODE = {
    "0": CATEGORY_CONFIG[0],
    "7": CATEGORY_CONFIG[0],
    "1": CATEGORY_CONFIG[1],
    "2": CATEGORY_CONFIG[2],
    "8": CATEGORY_CONFIG[2],
    "3": CATEGORY_CONFIG[3],
    "6": CATEGORY_CONFIG[3],
    "4": CATEGORY_CONFIG[4],
    "4A": CATEGORY_CONFIG[5],
    "5": CATEGORY_CONFIG[5],
    "5A": CATEGORY_CONFIG[5],
    "9": CATEGORY_CONFIG[6],
    "10": CATEGORY_CONFIG[6],
}

MANIFEST_LINK_RE = re.compile(
    r"^- \[(?P<title>[^\]]+)\]\((?P<path>achievements/[^)]+\.md)\)(?:\s+—\s+(?P<description>.+))?$",
    re.MULTILINE,
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def categories_from_manifest(text: str) -> list[Category]:
    found: list[Category] = []
    for m in MANIFEST_LINK_RE.finditer(text):
        path = m.group("path")
        configured = CATEGORY_BY_PATH.get(path)
        if configured:
            found.append(
                Category(
                    configured.id,
                    m.group("title").strip(),
                    path,
                    (m.group("description") or configured.description).strip(),
                )
            )
        else:
            stem = Path(path).stem
            found.append(
                Category(
                    re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-") or stem,
                    m.group("title").strip(),
                    path,
                    (m.group("description") or "").strip(),
                )
            )
    return found


def load_items() -> tuple[list[legacy.Achievement], list[Category]]:
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    categories = categories_from_manifest(manifest_text)
    items: list[legacy.Achievement] = []

    if categories:
        missing = [c.path for c in categories if not (ROOT / c.path).exists()]
        if missing:
            raise FileNotFoundError("manifest references missing category files: " + ", ".join(missing))
        for category in categories:
            text = (ROOT / category.path).read_text(encoding="utf-8")
            parsed = legacy.parse_source(text)
            for item in parsed:
                item.category = category.title
                item.category_id = category.id
                item.source_file = category.path
            items.extend(parsed)
        return items, categories

    # Migration-safe fallback: before the category split lands, the new builder can still
    # render the legacy monolithic ACHIEVEMENTS.md grouped by the same category mapping.
    parsed = legacy.parse_source(manifest_text)
    for item in parsed:
        code = legacy.section_code(item.section)
        category = CATEGORY_BY_CODE.get(code, CATEGORY_CONFIG[0])
        item.category = category.title
        item.category_id = category.id
        item.source_file = "ACHIEVEMENTS.md"
    return parsed, CATEGORY_CONFIG


def render(items: list[legacy.Achievement], categories: list[Category]) -> str:
    payload = []
    for a in items:
        row = asdict(a)
        row.update(
            {
                "body_len": a.body_len,
                "category": getattr(a, "category", ""),
                "category_id": getattr(a, "category_id", ""),
                "source_file": getattr(a, "source_file", ""),
            }
        )
        payload.append(row)

    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    category_data = json.dumps(
        [
            {
                "id": c.id,
                "title": c.title,
                "path": c.path,
                "description": c.description,
            }
            for c in categories
        ],
        ensure_ascii=False,
    ).replace("<", "\\u003c")
    tags = sorted({t for a in items for t in a.tags})
    tag_buttons = "\n".join(
        f'<button class="tag" type="button" data-filter-tag="{esc(t)}">#{esc(t)}</button>'
        for t in tags
    )
    category_nav = "\n".join(
        f'<a class="category-link" href="#{esc(c.id)}">{esc(c.title)} <span data-category-count="{esc(c.id)}"></span></a>'
        for c in categories
    )

    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="核兵器・原子力・被爆史・冷戦・核軍縮・科学史を、実績形式で時系列に読む歴史ゲーム資料。">
<title>核実績ゲーム — Achievements</title>
<style>
:root {{ color-scheme: light dark; --bg:#f5f3ee; --fg:#191919; --muted:#686868; --card:#fff; --line:#d8d3c8; --accent:#9c2f2f; --chip:#ece7dc; --group:#ebe5d8; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#171717; --fg:#eee; --muted:#aaa; --card:#202020; --line:#383838; --accent:#ef9b9b; --chip:#2d2d2d; --group:#24211e; }} }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; scroll-padding-top:13rem; }}
body {{ margin:0; font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif; background:var(--bg); color:var(--fg); line-height:1.8; }}
button,input {{ font:inherit; }}
header {{ padding:2.2rem 1rem 1.1rem; max-width:1100px; margin:auto; }}
h1 {{ margin:0 0 .35rem; font-size:clamp(1.7rem,4vw,2.7rem); }}
.lead {{ color:var(--muted); max-width:60rem; }}
.category-nav {{ max-width:1100px; margin:0 auto 1.2rem; padding:0 1rem; display:flex; gap:.45rem; flex-wrap:wrap; }}
.category-link {{ text-decoration:none; border:1px solid var(--line); border-radius:.7rem; padding:.3rem .65rem; color:var(--fg); background:var(--card); font-size:.88rem; }}
.category-link:hover {{ border-color:var(--accent); color:var(--accent); }}
.controls {{ position:sticky; top:0; z-index:4; backdrop-filter:blur(12px); background:color-mix(in srgb,var(--bg) 88%,transparent); border-block:1px solid var(--line); }}
.controls-inner {{ max-width:1100px; margin:auto; padding:.8rem 1rem; display:grid; gap:.7rem; }}
.search {{ width:100%; padding:.75rem .9rem; border:1px solid var(--line); border-radius:.7rem; background:var(--card); color:var(--fg); font-size:1rem; }}
.tags {{ display:flex; gap:.45rem; flex-wrap:wrap; max-height:7.4rem; overflow:auto; }}
.tag,.card-tag {{ border:1px solid var(--line); border-radius:999px; padding:.28rem .65rem; background:var(--chip); color:var(--fg); cursor:pointer; }}
.tag.active,.card-tag.active {{ border-color:var(--accent); color:var(--accent); font-weight:700; }}
.card-tag {{ font-size:.78rem; padding:.12rem .5rem; }}
.tag:hover,.card-tag:hover {{ border-color:var(--accent); }}
.meta-bar {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; color:var(--muted); font-size:.9rem; }}
.filter-note {{ color:var(--muted); font-size:.82rem; }}
main {{ max-width:1100px; margin:1.4rem auto 4rem; padding:0 1rem; }}
.category-group {{ margin:2.2rem 0 3.2rem; }}
.category-header {{ margin:0 0 1rem; padding:1rem 1.15rem; border-left:.35rem solid var(--accent); border-radius:.2rem .9rem .9rem .2rem; background:var(--group); }}
.category-header h2 {{ margin:0; font-size:clamp(1.35rem,3vw,1.8rem); }}
.category-header p {{ margin:.25rem 0 0; color:var(--muted); }}
.category-header .category-meta {{ margin-top:.25rem; font-size:.84rem; color:var(--muted); }}
.achievement {{ background:var(--card); border:1px solid var(--line); border-radius:1rem; padding:1rem 1.1rem; margin:.8rem 0; box-shadow:0 1px 0 rgba(0,0,0,.03); }}
.achievement.future {{ border-style:dashed; }}
.achievement h3 {{ margin:.05rem 0 .25rem; font-size:1.25rem; line-height:1.45; }}
.date {{ color:var(--accent); font-weight:800; font-variant-numeric:tabular-nums; }}
.section {{ color:var(--muted); font-size:.86rem; }}
.achievement p {{ margin:.65rem 0 .4rem; }}
.chips {{ display:flex; flex-wrap:wrap; gap:.35rem; }}
.empty {{ display:none; padding:2rem 0; color:var(--muted); }}
footer {{ max-width:1100px; margin:0 auto; padding:0 1rem 3rem; color:var(--muted); }}
@media (max-width:680px) {{
  html {{ scroll-padding-top:17rem; }}
  .controls {{ position:static; }}
  .tags {{ max-height:9rem; }}
  .meta-bar {{ align-items:flex-start; flex-direction:column; gap:.4rem; }}
}}
</style>
</head>
<body>
<header><h1>核実績ゲーム</h1><p class="lead">1945年に何が起こるかは、もう知っている。では、その後の人類は何をしたのか。科学史、被爆、復興、核抑止、軍縮、平和利用、そしてまだ解除されていない未来実績までを読む。</p></header>
<nav class="category-nav" aria-label="カテゴリー">{category_nav}</nav>
<div class="controls"><div class="controls-inner">
<input id="search" class="search" type="search" placeholder="実績名・本文・タグ・年代・カテゴリーを検索" aria-label="実績を検索">
<div class="tags" aria-label="タグで絞り込み">{tag_buttons}</div>
<div class="meta-bar"><div><span id="count"></span><span id="filter-note" class="filter-note"></span></div><button id="clear" class="tag" type="button">絞り込み解除</button></div>
</div></div>
<main><div id="list"></div><p id="empty" class="empty">条件に一致する実績はありません。</p></main>
<footer>Source: <code>ACHIEVEMENTS.md</code> + <code>achievements/*.md</code> / Generated by <code>scripts/build_site_v2.py</code></footer>
<script id="achievement-data" type="application/json">{data}</script>
<script id="category-data" type="application/json">{category_data}</script>
<script>
const items = JSON.parse(document.getElementById('achievement-data').textContent);
const categories = JSON.parse(document.getElementById('category-data').textContent);
const list = document.getElementById('list');
const count = document.getElementById('count');
const empty = document.getElementById('empty');
const search = document.getElementById('search');
const filterNote = document.getElementById('filter-note');
const active = new Set();
function escapeHtml(s){{return String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]));}}
function syncTagState(){{
 document.querySelectorAll('[data-filter-tag]').forEach(b=>b.classList.toggle('active',active.has(b.dataset.filterTag)));
 document.querySelectorAll('[data-card-tag]').forEach(b=>b.classList.toggle('active',active.has(b.dataset.cardTag)));
 filterNote.textContent=active.size?` — タグ: ${{[...active].map(t=>'#'+t).join(' × ')}}（すべて含む）`:'';
}}
function toggleTag(tag){{ active.has(tag)?active.delete(tag):active.add(tag); render(); }}
function cardHtml(a){{
 return `<article class="achievement ${{a.future?'future':''}}"><div class="date">${{escapeHtml(a.date)}}</div><h3>${{escapeHtml(a.title)}}</h3><div class="section">${{escapeHtml(a.section)}}${{a.subsection?' / '+escapeHtml(a.subsection):''}}</div><p>${{escapeHtml(a.body)}}</p><div class="chips">${{a.tags.map(t=>`<button type="button" class="card-tag" data-card-tag="${{escapeHtml(t)}}">#${{escapeHtml(t)}}</button>`).join('')}}</div></article>`;
}}
function render(){{
 const q=search.value.trim().toLowerCase();
 const shown=items.filter(a=>{{
   const hay=[a.date,a.title,a.body,a.section,a.subsection,a.category,...a.tags].join(' ').toLowerCase();
   const tagOK=[...active].every(t=>a.tags.includes(t));
   return (!q||hay.includes(q))&&tagOK;
 }});
 const chunks=[];
 for(const category of categories){{
   const catItems=shown.filter(a=>a.category_id===category.id);
   const total=items.filter(a=>a.category_id===category.id).length;
   const badge=document.querySelector(`[data-category-count="${{category.id}}"]`);
   if(badge) badge.textContent=`(${{catItems.length}}/${{total}})`;
   if(!catItems.length) continue;
   chunks.push(`<section class="category-group" id="${{escapeHtml(category.id)}}"><header class="category-header"><h2>${{escapeHtml(category.title)}}</h2><p>${{escapeHtml(category.description)}}</p><div class="category-meta">${{catItems.length}} / ${{total}} 実績</div></header>${{catItems.map(cardHtml).join('')}}</section>`);
 }}
 list.innerHTML=chunks.join('');
 count.textContent=`${{shown.length}} / ${{items.length}} 実績`;
 empty.style.display=shown.length?'none':'block';
 document.querySelectorAll('[data-card-tag]').forEach(b=>b.addEventListener('click',()=>toggleTag(b.dataset.cardTag)));
 syncTagState();
}}
document.querySelectorAll('[data-filter-tag]').forEach(b=>b.addEventListener('click',()=>toggleTag(b.dataset.filterTag)));
search.addEventListener('input',render);
document.getElementById('clear').addEventListener('click',()=>{{active.clear();search.value='';render();}});
render();
</script>
</body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate source before building")
    parser.add_argument(
        "--strict-length",
        action="store_true",
        help=f"fail when a body is shorter than {legacy.MIN_BODY_CHARS} characters",
    )
    parser.add_argument(
        "--strict-tags",
        action="store_true",
        help="require tags to be written explicitly in category markdown files",
    )
    args = parser.parse_args()

    try:
        items, categories = load_items()
    except (OSError, ValueError) as exc:
        print(f"::error::{exc}")
        return 2

    errors, warnings = legacy.validate(items, args.strict_length, args.strict_tags)
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
    (OUT_DIR / "index.html").write_text(render(items, categories), encoding="utf-8")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(items)} achievements in {len(categories)} categories -> {OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
