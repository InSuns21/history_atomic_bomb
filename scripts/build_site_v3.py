#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from dataclasses import asdict

import build_site as legacy
import build_site_v2 as base


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(items: list[legacy.Achievement], categories: list[base.Category]) -> str:
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
        f'<button class="category-link" type="button" data-scope="{esc(c.id)}">'
        f'<span class="category-link-title">{esc(c.title)}</span>'
        f'<span class="category-link-count" data-category-count="{esc(c.id)}"></span>'
        f'</button>'
        for c in categories
    )

    template = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="核兵器・原子力・被爆史・冷戦・核軍縮・科学史を、実績形式で時系列に読む歴史ゲーム資料。">
<title>核実績ゲーム — Achievements</title>
<style>
:root {
  color-scheme: light dark;
  --bg:#f5f3ee;
  --fg:#191919;
  --muted:#686868;
  --card:#fff;
  --line:#d8d3c8;
  --accent:#9c2f2f;
  --chip:#ece7dc;
  --group:#ebe5d8;
  --sidebar:#efebe2;
  --hover:#e4ded1;
  --shadow:0 10px 30px rgba(0,0,0,.08);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#171717;
    --fg:#eee;
    --muted:#aaa;
    --card:#202020;
    --line:#383838;
    --accent:#ef9b9b;
    --chip:#2d2d2d;
    --group:#24211e;
    --sidebar:#1c1c1c;
    --hover:#292725;
    --shadow:0 10px 30px rgba(0,0,0,.28);
  }
}
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  margin:0;
  font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif;
  background:var(--bg);
  color:var(--fg);
  line-height:1.8;
}
button,input { font:inherit; }
button { color:inherit; }
.app-shell {
  min-height:100vh;
  display:grid;
  grid-template-columns:minmax(260px, 310px) minmax(0, 1fr);
}
.sidebar {
  position:sticky;
  top:0;
  height:100vh;
  overflow:auto;
  padding:1.15rem 1rem 1.5rem;
  background:var(--sidebar);
  border-right:1px solid var(--line);
  z-index:10;
}
.brand { margin:0 0 .35rem; font-size:1.35rem; line-height:1.35; }
.sidebar-lead { margin:0 0 1rem; color:var(--muted); font-size:.84rem; line-height:1.65; }
.search {
  width:100%;
  padding:.72rem .78rem;
  border:1px solid var(--line);
  border-radius:.7rem;
  background:var(--card);
  color:var(--fg);
}
.sidebar-section-title {
  margin:1.1rem 0 .45rem;
  color:var(--muted);
  font-size:.72rem;
  font-weight:800;
  letter-spacing:.08em;
  text-transform:uppercase;
}
.category-nav { display:grid; gap:.2rem; }
.category-link {
  width:100%;
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:.65rem;
  padding:.58rem .65rem;
  border:1px solid transparent;
  border-radius:.65rem;
  background:transparent;
  text-align:left;
  cursor:pointer;
}
.category-link:hover { background:var(--hover); }
.category-link[aria-current="page"] {
  border-color:color-mix(in srgb,var(--accent) 38%,var(--line));
  background:var(--card);
  color:var(--accent);
  font-weight:800;
}
.category-link-title { min-width:0; }
.category-link-count { color:var(--muted); font-size:.75rem; white-space:nowrap; padding-top:.08rem; }
.category-link[aria-current="page"] .category-link-count { color:inherit; }
.tag-panel {
  margin-top:1rem;
  border-top:1px solid var(--line);
  padding-top:.8rem;
}
.tag-panel summary {
  cursor:pointer;
  font-size:.9rem;
  font-weight:700;
  list-style:none;
  display:flex;
  justify-content:space-between;
  gap:.6rem;
}
.tag-panel summary::-webkit-details-marker { display:none; }
.tag-panel summary::after { content:'＋'; color:var(--muted); }
.tag-panel[open] summary::after { content:'−'; }
.tags {
  display:flex;
  flex-wrap:wrap;
  gap:.38rem;
  max-height:12rem;
  overflow:auto;
  margin-top:.65rem;
  padding-right:.2rem;
}
.tag,.card-tag,.clear-button {
  border:1px solid var(--line);
  border-radius:999px;
  background:var(--chip);
  color:var(--fg);
  cursor:pointer;
}
.tag { padding:.22rem .55rem; font-size:.78rem; }
.tag.active,.card-tag.active { border-color:var(--accent); color:var(--accent); font-weight:800; }
.tag:hover,.card-tag:hover,.clear-button:hover { border-color:var(--accent); }
.sidebar-meta { margin-top:.8rem; color:var(--muted); font-size:.78rem; }
.clear-button { width:100%; margin-top:.65rem; padding:.45rem .7rem; background:transparent; }
.content { min-width:0; }
.content-inner { max-width:920px; margin:0 auto; padding:2rem 2rem 4rem; }
.scope-header {
  margin-bottom:1.25rem;
  padding-bottom:1rem;
  border-bottom:1px solid var(--line);
}
.scope-eyebrow { color:var(--accent); font-size:.78rem; font-weight:850; letter-spacing:.06em; }
.scope-title { margin:.12rem 0 .35rem; font-size:clamp(1.65rem,4vw,2.45rem); line-height:1.35; }
.scope-description { margin:0; color:var(--muted); max-width:52rem; }
.scope-filter-note { margin-top:.6rem; color:var(--muted); font-size:.86rem; }
.category-group { margin:2rem 0 3rem; }
.category-header {
  margin:0 0 1rem;
  padding:.85rem 1rem;
  border-left:.32rem solid var(--accent);
  border-radius:.2rem .8rem .8rem .2rem;
  background:var(--group);
}
.category-header h2 { margin:0; font-size:1.4rem; line-height:1.45; }
.category-header p { margin:.2rem 0 0; color:var(--muted); font-size:.9rem; }
.category-meta { margin-top:.2rem; color:var(--muted); font-size:.78rem; }
.achievement {
  background:var(--card);
  border:1px solid var(--line);
  border-radius:1rem;
  padding:1rem 1.1rem;
  margin:.8rem 0;
  box-shadow:0 1px 0 rgba(0,0,0,.03);
}
.achievement.future { border-style:dashed; }
.achievement h3 { margin:.05rem 0 .25rem; font-size:1.25rem; line-height:1.45; }
.date { color:var(--accent); font-weight:850; font-variant-numeric:tabular-nums; }
.section { color:var(--muted); font-size:.84rem; }
.achievement p { margin:.65rem 0 .5rem; }
.chips { display:flex; flex-wrap:wrap; gap:.35rem; }
.card-tag { padding:.1rem .48rem; font-size:.76rem; }
.empty { display:none; padding:2rem 0; color:var(--muted); }
footer { margin-top:2rem; padding-top:1.2rem; border-top:1px solid var(--line); color:var(--muted); font-size:.8rem; }
.mobile-bar,.sidebar-scrim { display:none; }
@media (max-width:820px) {
  .app-shell { display:block; }
  .mobile-bar {
    position:sticky;
    top:0;
    z-index:20;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    padding:.7rem .9rem;
    border-bottom:1px solid var(--line);
    background:color-mix(in srgb,var(--bg) 92%,transparent);
    backdrop-filter:blur(12px);
  }
  .mobile-bar strong { font-size:.95rem; }
  .mobile-toggle {
    border:1px solid var(--line);
    border-radius:.65rem;
    padding:.4rem .7rem;
    background:var(--card);
    cursor:pointer;
  }
  .sidebar {
    position:fixed;
    inset:0 auto 0 0;
    width:min(86vw, 320px);
    height:100dvh;
    transform:translateX(-105%);
    transition:transform .2s ease;
    box-shadow:var(--shadow);
  }
  .sidebar.open { transform:translateX(0); }
  .sidebar-scrim {
    position:fixed;
    inset:0;
    z-index:9;
    background:rgba(0,0,0,.38);
  }
  .sidebar-scrim.show { display:block; }
  .content-inner { padding:1.35rem 1rem 3rem; }
}
</style>
</head>
<body>
<div class="mobile-bar">
  <strong>核実績ゲーム</strong>
  <button id="sidebar-toggle" class="mobile-toggle" type="button" aria-expanded="false" aria-controls="sidebar">目次・検索</button>
</div>
<div id="sidebar-scrim" class="sidebar-scrim"></div>
<div class="app-shell">
  <aside id="sidebar" class="sidebar" aria-label="実績ナビゲーション">
    <h1 class="brand">核実績ゲーム</h1>
    <p class="sidebar-lead">科学史から被爆、復興、冷戦、原子力利用、そして未来まで。章を選んで歴史を読む。</p>
    <input id="search" class="search" type="search" placeholder="この範囲から実績を検索" aria-label="実績を検索">

    <div class="sidebar-section-title">目次</div>
    <nav class="category-nav" aria-label="カテゴリー">
      <button class="category-link" type="button" data-scope="all">
        <span class="category-link-title">全実績・時系列</span>
        <span class="category-link-count" data-category-count="all"></span>
      </button>
      __CATEGORY_NAV__
    </nav>

    <details class="tag-panel" id="tag-panel">
      <summary><span>タグで絞り込む</span><span id="active-tag-count"></span></summary>
      <div class="tags" aria-label="タグで絞り込み">__TAG_BUTTONS__</div>
    </details>
    <div class="sidebar-meta"><span id="count"></span><span id="filter-note"></span></div>
    <button id="clear" class="clear-button" type="button">検索・タグを解除</button>
  </aside>

  <main class="content">
    <div class="content-inner">
      <header class="scope-header">
        <div id="scope-eyebrow" class="scope-eyebrow"></div>
        <h2 id="scope-title" class="scope-title"></h2>
        <p id="scope-description" class="scope-description"></p>
        <div id="scope-filter-note" class="scope-filter-note"></div>
      </header>
      <div id="list"></div>
      <p id="empty" class="empty">条件に一致する実績はありません。</p>
      <footer>Source: <code>ACHIEVEMENTS.md</code> + <code>achievements/*.md</code> / Generated by <code>scripts/build_site_v3.py</code></footer>
    </div>
  </main>
</div>
<script id="achievement-data" type="application/json">__DATA__</script>
<script id="category-data" type="application/json">__CATEGORY_DATA__</script>
<script>
const items = JSON.parse(document.getElementById('achievement-data').textContent);
const categories = JSON.parse(document.getElementById('category-data').textContent);
const list = document.getElementById('list');
const count = document.getElementById('count');
const empty = document.getElementById('empty');
const search = document.getElementById('search');
const filterNote = document.getElementById('filter-note');
const scopeEyebrow = document.getElementById('scope-eyebrow');
const scopeTitle = document.getElementById('scope-title');
const scopeDescription = document.getElementById('scope-description');
const scopeFilterNote = document.getElementById('scope-filter-note');
const activeTagCount = document.getElementById('active-tag-count');
const tagPanel = document.getElementById('tag-panel');
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebarScrim = document.getElementById('sidebar-scrim');
const active = new Set();
let scope = 'all';

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function scopeFromHash() {
  const raw = decodeURIComponent(location.hash.replace(/^#/, ''));
  if (raw === 'all') return 'all';
  if (categories.some(c => c.id === raw)) return raw;
  return categories.length ? categories[0].id : 'all';
}
function setScope(next) {
  const target = next || (categories[0] ? categories[0].id : 'all');
  if (location.hash.replace(/^#/, '') === target) {
    scope = target;
    render();
  } else {
    location.hash = encodeURIComponent(target);
  }
  closeSidebar();
}
function closeSidebar() {
  sidebar.classList.remove('open');
  sidebarScrim.classList.remove('show');
  if (sidebarToggle) sidebarToggle.setAttribute('aria-expanded', 'false');
}
function openSidebar() {
  sidebar.classList.add('open');
  sidebarScrim.classList.add('show');
  if (sidebarToggle) sidebarToggle.setAttribute('aria-expanded', 'true');
}
function syncTagState() {
  document.querySelectorAll('[data-filter-tag]').forEach(b => b.classList.toggle('active', active.has(b.dataset.filterTag)));
  document.querySelectorAll('[data-card-tag]').forEach(b => b.classList.toggle('active', active.has(b.dataset.cardTag)));
  activeTagCount.textContent = active.size ? `${active.size}件` : '';
  filterNote.textContent = active.size ? ` / ${[...active].map(t => '#'+t).join(' × ')}` : '';
  if (active.size) tagPanel.open = true;
}
function toggleTag(tag) {
  active.has(tag) ? active.delete(tag) : active.add(tag);
  render();
}
function cardHtml(a) {
  return `<article class="achievement ${a.future?'future':''}"><div class="date">${escapeHtml(a.date)}</div><h3>${escapeHtml(a.title)}</h3><div class="section">${escapeHtml(a.section)}${a.subsection?' / '+escapeHtml(a.subsection):''}</div><p>${escapeHtml(a.body)}</p><div class="chips">${a.tags.map(t=>`<button type="button" class="card-tag" data-card-tag="${escapeHtml(t)}">#${escapeHtml(t)}</button>`).join('')}</div></article>`;
}
function currentCategory() {
  return categories.find(c => c.id === scope) || null;
}
function updateScopeHeader(shownCount, scopedCount) {
  const category = currentCategory();
  if (scope === 'all' || !category) {
    scopeEyebrow.textContent = '全カテゴリー';
    scopeTitle.textContent = '全実績・時系列';
    scopeDescription.textContent = 'カテゴリーをまたいで、登録されている実績を通して読む。';
  } else {
    const index = categories.findIndex(c => c.id === scope);
    scopeEyebrow.textContent = `カテゴリー ${index + 1} / ${categories.length}`;
    scopeTitle.textContent = category.title;
    scopeDescription.textContent = category.description;
  }
  const bits = [];
  if (search.value.trim()) bits.push(`検索: 「${search.value.trim()}」`);
  if (active.size) bits.push(`タグ: ${[...active].map(t => '#'+t).join(' × ')}`);
  scopeFilterNote.textContent = bits.length ? `${shownCount} / ${scopedCount} 実績 — ${bits.join(' / ')}` : `${shownCount} 実績`;
}
function render() {
  const q = search.value.trim().toLowerCase();
  const scoped = scope === 'all' ? items : items.filter(a => a.category_id === scope);
  const shown = scoped.filter(a => {
    const hay = [a.date,a.title,a.body,a.section,a.subsection,a.category,...a.tags].join(' ').toLowerCase();
    const tagOK = [...active].every(t => a.tags.includes(t));
    return (!q || hay.includes(q)) && tagOK;
  });

  document.querySelectorAll('[data-scope]').forEach(b => {
    const selected = b.dataset.scope === scope;
    if (selected) b.setAttribute('aria-current', 'page');
    else b.removeAttribute('aria-current');
  });
  document.querySelector('[data-category-count="all"]').textContent = items.length;
  for (const category of categories) {
    const badge = document.querySelector(`[data-category-count="${category.id}"]`);
    if (badge) badge.textContent = items.filter(a => a.category_id === category.id).length;
  }

  const chunks = [];
  if (scope === 'all') {
    for (const category of categories) {
      const catItems = shown.filter(a => a.category_id === category.id);
      if (!catItems.length) continue;
      const total = items.filter(a => a.category_id === category.id).length;
      chunks.push(`<section class="category-group"><header class="category-header"><h2>${escapeHtml(category.title)}</h2><p>${escapeHtml(category.description)}</p><div class="category-meta">${catItems.length} / ${total} 実績</div></header>${catItems.map(cardHtml).join('')}</section>`);
    }
  } else {
    chunks.push(shown.map(cardHtml).join(''));
  }

  list.innerHTML = chunks.join('');
  count.textContent = `${shown.length} / ${scoped.length} 実績`;
  empty.style.display = shown.length ? 'none' : 'block';
  document.querySelectorAll('[data-card-tag]').forEach(b => b.addEventListener('click', () => toggleTag(b.dataset.cardTag)));
  updateScopeHeader(shown.length, scoped.length);
  syncTagState();
}

document.querySelectorAll('[data-scope]').forEach(b => b.addEventListener('click', () => setScope(b.dataset.scope)));
document.querySelectorAll('[data-filter-tag]').forEach(b => b.addEventListener('click', () => toggleTag(b.dataset.filterTag)));
search.addEventListener('input', render);
document.getElementById('clear').addEventListener('click', () => { active.clear(); search.value=''; render(); });
window.addEventListener('hashchange', () => { scope = scopeFromHash(); render(); window.scrollTo({top:0, behavior:'smooth'}); });
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.contains('open') ? closeSidebar() : openSidebar());
sidebarScrim.addEventListener('click', closeSidebar);
window.addEventListener('keydown', e => { if (e.key === 'Escape') closeSidebar(); });

scope = scopeFromHash();
if (!location.hash && scope !== 'all') history.replaceState(null, '', `#${encodeURIComponent(scope)}`);
render();
</script>
</body>
</html>'''

    return (
        template.replace("__DATA__", data)
        .replace("__CATEGORY_DATA__", category_data)
        .replace("__TAG_BUTTONS__", tag_buttons)
        .replace("__CATEGORY_NAV__", category_nav)
    )


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
        items, categories = base.load_items()
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

    base.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (base.OUT_DIR / "index.html").write_text(render(items, categories), encoding="utf-8")
    (base.OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(items)} achievements in {len(categories)} categories -> {base.OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
