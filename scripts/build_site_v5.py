#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import unicodedata
from pathlib import Path

import build_site_v4 as previous


_render_v4 = previous.render


CATEGORY_GROUPS = (
    (
        "main",
        "MAIN ROUTE",
        "核時代の本編",
        (
            "achievements/00_science.md",
            "achievements/00_manhattan_project.md",
            "achievements/00_wartime_politics.md",
            "achievements/01_hiroshima_nagasaki.md",
            "achievements/02_aftermath_memory.md",
            "achievements/03_cold_war_deterrence.md",
            "achievements/04_civil_nuclear.md",
            "achievements/05_national_cases.md",
            "achievements/05_alliance_nuclear.md",
        ),
    ),
    (
        "side",
        "SIDE ARCHIVE",
        "本編から枝分かれする資料",
        (
            "achievements/00_atomic_espionage.md",
            "achievements/05_greenland_nuclear.md",
            "achievements/00_japan_wartime_research.md",
            "achievements/05_science_sidepaths.md",
            "achievements/05_history_of_ideas.md",
        ),
    ),
    (
        "people",
        "PEOPLE & CULTURE",
        "個人の記憶と文化史",
        (
            "achievements/02_harimoto_isao.md",
            "achievements/02_tezuka_osamu.md",
            "achievements/02_miyazaki_hayao.md",
        ),
    ),
    (
        "future",
        "FUTURE / LOCKED",
        "まだ歴史になっていないもの",
        ("achievements/06_future.md",),
    ),
)

GROUP_BY_PATH = {
    path: group_key
    for group_key, _label, _description, paths in CATEGORY_GROUPS
    for path in paths
}
GROUP_META = {
    group_key: {"label": label, "description": description}
    for group_key, label, description, _paths in CATEGORY_GROUPS
}

RELATED_CATEGORY_PATHS = {
    "achievements/00_science.md": ("achievements/00_japan_wartime_research.md",),
    "achievements/00_manhattan_project.md": ("achievements/00_atomic_espionage.md",),
    "achievements/00_wartime_politics.md": ("achievements/00_japan_wartime_research.md",),
    "achievements/01_hiroshima_nagasaki.md": ("achievements/02_harimoto_isao.md",),
    "achievements/02_aftermath_memory.md": ("achievements/02_harimoto_isao.md",),
    "achievements/03_cold_war_deterrence.md": (
        "achievements/00_atomic_espionage.md",
        "achievements/05_greenland_nuclear.md",
    ),
    "achievements/05_greenland_nuclear.md": ("achievements/03_cold_war_deterrence.md",),
}


def _grouped_category_nav(categories) -> str:
    by_path = {category.path: category for category in categories}
    chunks = [
        '<a class="category-link category-link-all" href="#top">'
        '<span class="category-link-title">すべて表示</span>'
        '<span class="category-link-count" data-category-count="all"></span>'
        '</a>'
    ]
    for group_key, label, description, paths in CATEGORY_GROUPS:
        group_categories = [by_path[path] for path in paths if path in by_path]
        if not group_categories:
            continue
        links = ''.join(
            '<a class="category-link" href="#category-{id}">'
            '<span class="category-link-title">{title}</span>'
            '<span class="category-link-count" data-category-count="{id}"></span>'
            '</a>'.format(
                id=html.escape(category.id, quote=True),
                title=html.escape(category.title),
            )
            for category in group_categories
        )
        chunks.append(
            '<section class="category-nav-group category-nav-group-{group}">'
            '<div class="category-nav-group-title">{label}</div>'
            '<div class="category-nav-group-description">{description}</div>'
            '{links}'
            '</section>'.format(
                group=group_key,
                label=html.escape(label),
                description=html.escape(description),
                links=links,
            )
        )
    return ''.join(chunks)


def _grouped_mobile_toc(categories) -> str:
    by_path = {category.path: category for category in categories}
    chunks = ['<a class="category-link" href="#top">先頭</a>']
    for group_key, label, _description, paths in CATEGORY_GROUPS:
        group_categories = [by_path[path] for path in paths if path in by_path]
        if not group_categories:
            continue
        chunks.append(
            f'<span class="mobile-toc-group mobile-toc-group-{group_key}">'
            f'{html.escape(label)}</span>'
        )
        chunks.extend(
            f'<a class="category-link" href="#category-{html.escape(category.id, quote=True)}">'
            f'{html.escape(category.title)}</a>'
            for category in group_categories
        )
    return (
        '<nav class="mobile-toc" aria-label="モバイル目次">'
        '<span class="mobile-toc-label">目次</span>'
        + ''.join(chunks)
        + '</nav>'
    )


GAME_UI_CSS = r'''
/* Game archive UI: keep the reading surface calm, make the cards read as HUD entries. */
.content { counter-reset: chapter; }
.category-group { counter-increment: chapter; }
.category-header {
  position:relative;
  overflow:hidden;
  padding:1.45rem 1rem .95rem;
  border:1px solid var(--line);
  border-left:.22rem solid var(--accent);
  border-radius:.2rem;
  background:color-mix(in srgb,var(--group) 88%,var(--card));
}
.category-header::before {
  content:"CHAPTER " counter(chapter, decimal-leading-zero);
  position:absolute;
  top:.35rem;
  left:1rem;
  color:var(--accent);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.64rem;
  font-weight:800;
  letter-spacing:.16em;
}
.category-header::after {
  content:"";
  position:absolute;
  top:0;
  right:0;
  width:3.2rem;
  height:2px;
  background:var(--accent);
  opacity:.72;
}
.section-heading {
  display:flex;
  align-items:center;
  gap:.65rem;
}
.section-heading::before {
  content:"SECTION";
  flex:0 0 auto;
  padding:.08rem .32rem;
  border:1px solid var(--line);
  color:var(--muted);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.61rem;
  font-weight:800;
  letter-spacing:.13em;
}
.achievement {
  position:relative;
  overflow:hidden;
  margin:.9rem 0;
  padding:0 1.1rem 1rem;
  border:1px solid var(--line);
  border-radius:.2rem;
  background:
    linear-gradient(var(--accent),var(--accent)) left top / 24px 2px no-repeat,
    linear-gradient(var(--accent),var(--accent)) left top / 2px 24px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 18px 1px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 1px 18px no-repeat,
    var(--card);
  box-shadow:0 2px 0 color-mix(in srgb,var(--fg) 5%,transparent);
  transition:border-color .14s ease, box-shadow .14s ease, transform .14s ease;
}
.achievement.future {
  border-style:dashed;
  background:
    linear-gradient(var(--accent),var(--accent)) left top / 24px 2px no-repeat,
    linear-gradient(var(--accent),var(--accent)) left top / 2px 24px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 18px 1px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 1px 18px no-repeat,
    color-mix(in srgb,var(--card) 92%,var(--chip));
}
.achievement.reference {
  border-left:2px solid color-mix(in srgb,var(--accent) 72%,var(--line));
  background:
    linear-gradient(var(--accent),var(--accent)) left top / 24px 2px no-repeat,
    linear-gradient(var(--accent),var(--accent)) left top / 2px 24px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 18px 1px no-repeat,
    linear-gradient(var(--line),var(--line)) right bottom / 1px 18px no-repeat,
    color-mix(in srgb,var(--card) 94%,var(--group));
}
.achievement.reference .date::before { content:"REFERENCE"; }
.reference-source {
  margin:-.12rem 0 .46rem;
  color:var(--muted);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.68rem;
  font-weight:800;
  letter-spacing:.06em;
}
.achievement .date {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:.8rem;
  margin:0 -1.1rem .8rem;
  padding:.43rem 1.1rem .4rem;
  border-bottom:1px solid var(--line);
  background:color-mix(in srgb,var(--chip) 64%,transparent);
  color:var(--accent);
  font-size:.78rem;
  font-weight:800;
  font-variant-numeric:tabular-nums;
  letter-spacing:.035em;
}
.achievement .date::before {
  content:"ARCHIVE ENTRY";
  color:var(--muted);
  font-size:.64rem;
  font-weight:900;
  letter-spacing:.16em;
  white-space:nowrap;
}
.achievement.future .date::before {
  content:"LOCKED ENTRY";
  color:var(--accent);
}
.achievement h5 {
  margin:.08rem 0 .4rem;
  font-size:1.16rem;
  line-height:1.48;
  letter-spacing:.01em;
}
.unlock-condition {
  margin:.72rem 0 1rem;
  padding:.68rem .75rem .72rem;
  border:1px solid var(--line);
  border-left:2px solid var(--accent);
  background:color-mix(in srgb,var(--chip) 38%,transparent);
}
.unlock-condition strong {
  margin-bottom:.28rem;
  color:var(--accent);
  font-size:.68rem;
  letter-spacing:.12em;
}
.achievement-description { line-height:1.85; }
.chips {
  gap:.35rem;
  margin-top:.82rem;
  padding-top:.68rem;
  border-top:1px dashed var(--line);
}
.card-tag {
  padding:.12rem .48rem;
  border-radius:.2rem;
  background:transparent;
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.72rem;
  letter-spacing:.015em;
}
.card-tag::before {
  content:"[";
  color:currentColor;
}
.card-tag::after {
  content:"]";
  color:currentColor;
}
.tag-check {
  display:none;
  margin-right:.18rem;
  color:currentColor;
  font-weight:900;
}
.tag.active .tag-check,
.card-tag.active .tag-check,
.tag[aria-pressed="true"] .tag-check,
.card-tag[aria-pressed="true"] .tag-check {
  display:inline;
}
.tag.active,
.card-tag.active,
.tag[aria-pressed="true"],
.card-tag[aria-pressed="true"] {
  border-color:var(--accent);
  background:color-mix(in srgb,var(--accent) 12%,var(--chip));
  color:var(--accent);
  font-weight:800;
  box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 48%,transparent);
}
.tag:focus-visible,
.card-tag:focus-visible {
  outline:2px solid var(--accent);
  outline-offset:2px;
}
@media (hover:hover) {
  .achievement:hover {
    transform:translateX(2px);
    border-color:color-mix(in srgb,var(--accent) 58%,var(--line));
    box-shadow:-3px 0 0 var(--accent), 0 7px 18px color-mix(in srgb,var(--fg) 8%,transparent);
  }
}
@media (max-width:700px) {
  .achievement { padding:0 .9rem .9rem; }
  .achievement .date { margin:0 -.9rem .75rem; padding:.42rem .9rem .38rem; }
  .achievement h5 { font-size:1.08rem; }
  .achievement .date::before { font-size:.6rem; letter-spacing:.11em; }
}
'''


GROUP_UI_CSS = r'''
/* Reading hierarchy: main history route first, thematic archives second. */
.content { counter-reset:main-chapter; }
.category-group { counter-increment:none; }
.category-group.group-main { counter-increment:main-chapter; }

.route-divider {
  margin:4.4rem 0 1.2rem;
  padding:.75rem 0 .7rem;
  border-top:2px solid var(--line);
  border-bottom:1px solid var(--line);
}
.route-divider:first-child { margin-top:2rem; }
.route-divider span {
  display:block;
  color:var(--muted);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.66rem;
  font-weight:900;
  letter-spacing:.16em;
}
.route-divider strong {
  display:block;
  margin-top:.08rem;
  font-size:1.05rem;
  line-height:1.45;
}
.route-divider-main { border-top-color:var(--accent); }
.route-divider-main span { color:var(--accent); }

.category-group .category-header::before {
  content:"ARCHIVE";
  color:var(--muted);
}
.category-group.group-main .category-header::before {
  content:"MAIN ROUTE · CHAPTER " counter(main-chapter, decimal-leading-zero);
  color:var(--accent);
}
.category-group.group-side .category-header::before { content:"SIDE ARCHIVE"; }
.category-group.group-people .category-header::before { content:"PEOPLE & CULTURE"; }
.category-group.group-future .category-header::before {
  content:"LOCKED ARCHIVE";
  color:var(--accent);
}

.category-group.group-side .category-header,
.category-group.group-people .category-header {
  padding:1.25rem 1rem .85rem;
  border-left-width:2px;
  border-left-color:var(--line);
  background:color-mix(in srgb,var(--group) 54%,var(--card));
}
.category-group.group-side .category-header::after,
.category-group.group-people .category-header::after {
  background:var(--line);
  opacity:.55;
}
.category-group.group-side .category-header h2,
.category-group.group-people .category-header h2 { font-size:1.34rem; }

.category-group.group-future .category-header {
  border:1px dashed var(--line);
  border-left:2px dashed var(--accent);
  background:color-mix(in srgb,var(--group) 42%,var(--card));
}
.category-group.group-future .category-header::after { opacity:.35; }

.related-categories {
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  gap:.35rem .55rem;
  margin-top:.65rem;
  padding-top:.55rem;
  border-top:1px dashed var(--line);
  font-size:.76rem;
}
.related-categories > span {
  color:var(--muted);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.63rem;
  font-weight:900;
  letter-spacing:.12em;
}
.related-category-link {
  color:var(--accent);
  text-decoration:none;
}
.related-category-link:hover { text-decoration:underline; }

.category-nav { gap:.38rem; }
.category-link-all {
  margin-bottom:.25rem;
  border-color:var(--line);
  background:color-mix(in srgb,var(--card) 66%,transparent);
}
.category-nav-group {
  display:grid;
  gap:.08rem;
  margin-top:.3rem;
  padding-top:.62rem;
  border-top:1px solid var(--line);
}
.category-nav-group-title {
  padding:0 .65rem;
  color:var(--muted);
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
  font-size:.64rem;
  font-weight:900;
  letter-spacing:.12em;
}
.category-nav-group-main .category-nav-group-title { color:var(--accent); }
.category-nav-group-description {
  padding:.08rem .65rem .24rem;
  color:var(--muted);
  font-size:.67rem;
  line-height:1.45;
}
.category-nav-group-side .category-link,
.category-nav-group-people .category-link {
  padding-top:.43rem;
  padding-bottom:.43rem;
  color:color-mix(in srgb,var(--fg) 82%,var(--muted));
}
.category-nav-group-future .category-link { border-style:dashed; }

.mobile-toc-group {
  flex:0 0 auto;
  margin-left:.35rem;
  color:var(--muted);
  font-size:.61rem;
  font-weight:900;
  letter-spacing:.09em;
  white-space:nowrap;
}
.mobile-toc-group-main { color:var(--accent); }

@media (max-width:700px) {
  .route-divider { margin:3rem 0 1rem; }
  .category-group.group-side .category-header h2,
  .category-group.group-people .category-header h2 { font-size:1.22rem; }
  .related-categories { align-items:flex-start; }
}
'''


SYNC_TAG_STATE_OLD = """  document.querySelectorAll('[data-filter-tag]').forEach(b => b.classList.toggle('active', active.has(b.dataset.filterTag)));
  document.querySelectorAll('[data-card-tag]').forEach(b => b.classList.toggle('active', active.has(b.dataset.cardTag)));
"""

SYNC_TAG_STATE_NEW = """  document.querySelectorAll('[data-filter-tag]').forEach(b => {
    const selected = active.has(b.dataset.filterTag);
    b.classList.toggle('active', selected);
    b.setAttribute('aria-pressed', selected ? 'true' : 'false');
  });
  document.querySelectorAll('[data-card-tag]').forEach(b => {
    const selected = active.has(b.dataset.cardTag);
    b.classList.toggle('active', selected);
    b.setAttribute('aria-pressed', selected ? 'true' : 'false');
  });
"""

REFERENCE_CARD_OLD = """  return `<article class="achievement ${a.future?'future':''}"><div class="date">${escapeHtml(a.date)}</div><h5>${escapeHtml(a.title)}</h5>${bodyHtml}<div class="chips">"""

REFERENCE_CARD_NEW = """  const referenceClass = a.is_reference ? ' reference' : '';
  const referenceSource = a.is_reference && a.canonical_category
    ? `<div class="reference-source">正本: ${escapeHtml(a.canonical_category)}</div>`
    : '';
  return `<article class="achievement ${a.future?'future':''}${referenceClass}"><div class="date">${escapeHtml(a.date)}</div><h5>${escapeHtml(a.title)}</h5>${referenceSource}${bodyHtml}<div class="chips">"""

CARD_TAG_OLD = '<button type="button" class="card-tag" data-card-tag="${escapeHtml(t)}">#${escapeHtml(t)}</button>'
CARD_TAG_NEW = (
    '<button type="button" class="card-tag" data-card-tag="${escapeHtml(t)}" aria-pressed="false">'
    '<span class="tag-check" aria-hidden="true">✓</span>'
    '<span class="tag-label">#${escapeHtml(t)}</span>'
    '</button>'
)

FILTER_TAG_PATTERN = re.compile(
    r'<button class="tag" type="button" data-filter-tag="([^"]+)">([^<]+)</button>'
)


def _reference_key(date: str, title: str) -> str:
    norm_title = unicodedata.normalize("NFKC", title).replace("🔒", "").strip()
    return f"{date}|{norm_title}"


def _date_sort_key(date: str) -> tuple[int, int, int]:
    """Best-effort start-date key used only to merge reference cards into an existing timeline."""
    match = re.search(r"(?P<year>\d{4})(?:/(?P<month>\d{1,2}))?(?:/(?P<day>\d{1,2}))?", date)
    if match:
        return (
            int(match.group("year")),
            int(match.group("month") or 0),
            int(match.group("day") or 0),
        )

    century = re.search(r"(?P<century>\d{1,2})世紀(?P<part>前半|後半)?", date)
    if century:
        base = (int(century.group("century")) - 1) * 100
        offset = {"前半": 25, "後半": 75}.get(century.group("part"), 0)
        return (base + offset, 0, 0)

    return (9999, 13, 32)


def _collect_reference_items(items, categories):
    """Resolve view-only references while keeping the canonical achievement in one source file."""
    target_by_key = {item.key: item for item in items}
    references = []
    seen = set()

    for category in categories:
        path = Path(category.path)
        current_section = ""
        reference_target_section = ""
        in_reference_section = False
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if stripped == "<!-- timeline-references":
                in_reference_section = True
                reference_target_section = current_section
                continue
            if stripped == "-->" and in_reference_section:
                in_reference_section = False
                continue
            if line.startswith("## "):
                heading = line[3:].strip()
                if heading == "既存実績への参照":
                    raise RuntimeError(
                        f"{category.path}:{line_no}: 可視の参照章は使わず、"
                        "<!-- timeline-references ... --> で直前の史実セクションへ参照を差し込んでください"
                    )
                current_section = heading
                continue
            if not in_reference_section:
                continue

            match = re.match(r"^- \*\*(?P<label>.+?)\*\*(?:\s+—.*)?$", stripped)
            if not match:
                continue

            label = match.group("label").strip()
            parts = re.split(r"[　\t]+|\s{2,}", label, maxsplit=1)
            if len(parts) != 2:
                raise RuntimeError(
                    f"{category.path}:{line_no}: 参照実績は『年月　実績名』の形式で記述してください"
                )
            date, title = (part.strip() for part in parts)
            key = _reference_key(date, title)
            target = target_by_key.get(key)
            if target is None:
                raise RuntimeError(
                    f"{category.path}:{line_no}: 参照先の正本実績が見つかりません: {date} {title}"
                )

            ref_id = (category.id, key)
            if ref_id in seen:
                continue
            seen.add(ref_id)

            clone = copy.copy(target)
            clone.category = category.title
            clone.category_id = category.id
            clone.section = reference_target_section or target.section
            clone.subsection = ""
            clone.is_reference = True
            clone.canonical_category = getattr(target, "category", "")
            clone.canonical_category_id = getattr(target, "category_id", "")
            clone.canonical_source_file = getattr(target, "source_file", "")
            references.append(clone)

    return references


def _merge_reference_items(items, references, categories):
    """Insert references into their target section by date without reordering canonical cards."""
    refs_by_category = {}
    for reference in references:
        refs_by_category.setdefault(reference.category_id, {}).setdefault(reference.section, []).append(reference)
    for sections in refs_by_category.values():
        for refs in sections.values():
            refs.sort(key=lambda item: _date_sort_key(item.date))

    merged = []
    for category in categories:
        category_items = [item for item in items if item.category_id == category.id]
        pending_by_section = refs_by_category.get(category.id, {})
        for item in category_items:
            pending = pending_by_section.get(item.section, [])
            while pending and _date_sort_key(pending[0].date) < _date_sort_key(item.date):
                merged.append(pending.pop(0))
            merged.append(item)
        for pending in pending_by_section.values():
            merged.extend(pending)
    return merged


def _apply_grouped_ui(page: str, categories) -> str:
    category_group_data = json.dumps(GROUP_BY_PATH, ensure_ascii=False).replace("<", "\\u003c")
    category_group_meta = json.dumps(GROUP_META, ensure_ascii=False).replace("<", "\\u003c")
    related_category_paths = json.dumps(RELATED_CATEGORY_PATHS, ensure_ascii=False).replace("<", "\\u003c")

    js_marker = "const list = document.getElementById('list');"
    if js_marker not in page:
        raise RuntimeError("category grouping JS marker not found")

    grouping_js = (
        "const categoryGroupByPath = " + category_group_data + ";\n"
        "const categoryGroupMeta = " + category_group_meta + ";\n"
        "const relatedCategoryPaths = " + related_category_paths + ";\n"
        + r"""function categoryGroup(category) {
  return categoryGroupByPath[category.path] || 'side';
}
function relatedLinksHtml(category) {
  const paths = relatedCategoryPaths[category.path] || [];
  const links = paths.map(path => {
    const target = categories.find(candidate => candidate.path === path);
    return target
      ? `<a class="related-category-link" href="#category-${escapeHtml(target.id)}">${escapeHtml(target.title)}</a>`
      : '';
  }).filter(Boolean);
  return links.length
    ? `<div class="related-categories"><span>RELATED</span>${links.join('')}</div>`
    : '';
}
"""
    )
    page = page.replace(js_marker, grouping_js + js_marker, 1)

    chunks_marker = "  const chunks = [];\n  for (const category of categories) {"
    if chunks_marker not in page:
        raise RuntimeError("category renderer loop marker not found")
    chunks_new = r"""  const chunks = [];
  let previousGroup = null;
  for (const category of categories) {
    const group = categoryGroup(category);
    if (group !== previousGroup) {
      const groupInfo = categoryGroupMeta[group] || {label:'ARCHIVE', description:''};
      chunks.push(`<div class="route-divider route-divider-${escapeHtml(group)}"><span>${escapeHtml(groupInfo.label)}</span><strong>${escapeHtml(groupInfo.description)}</strong></div>`);
      previousGroup = group;
    }"""
    page = page.replace(chunks_marker, chunks_new, 1)

    category_push_old = r"""    chunks.push(`<section id="category-${escapeHtml(category.id)}" class="category-group"><header class="category-header"><h2>${escapeHtml(category.title)}</h2><p>${escapeHtml(category.description)}</p><div class="category-meta">${catItems.length} / ${total} 実績</div></header>${content}</section>`);"""
    if category_push_old not in page:
        raise RuntimeError("category renderer card marker not found")
    category_push_new = r"""    const related = relatedLinksHtml(category);
    chunks.push(`<section id="category-${escapeHtml(category.id)}" class="category-group group-${escapeHtml(group)}" data-group="${escapeHtml(group)}"><header class="category-header"><h2>${escapeHtml(category.title)}</h2><p>${escapeHtml(category.description)}</p>${related}<div class="category-meta">${catItems.length} / ${total} 実績</div></header>${content}</section>`);"""
    page = page.replace(category_push_old, category_push_new, 1)

    nav_pattern = re.compile(
        r'<nav class="category-nav" aria-label="カテゴリー">.*?</nav>',
        re.DOTALL,
    )
    page, nav_count = nav_pattern.subn(
        '<nav class="category-nav" aria-label="カテゴリー">'
        + _grouped_category_nav(categories)
        + "</nav>",
        page,
        count=1,
    )
    if nav_count != 1:
        raise RuntimeError("desktop category navigation marker not found")

    mobile_nav_pattern = re.compile(
        r'<nav class="mobile-toc" aria-label="モバイル目次">.*?</nav>',
        re.DOTALL,
    )
    page, mobile_nav_count = mobile_nav_pattern.subn(
        _grouped_mobile_toc(categories),
        page,
        count=1,
    )
    if mobile_nav_count != 1:
        raise RuntimeError("mobile category navigation marker not found")

    return page


def render(items, categories) -> str:
    references = _collect_reference_items(items, categories)
    display_items = _merge_reference_items(items, references, categories)
    page = _render_v4(display_items, categories)
    style_marker = '</style>'
    if style_marker not in page:
        raise RuntimeError('style closing marker not found in build_site_v4 output')
    page = page.replace(style_marker, GAME_UI_CSS + GROUP_UI_CSS + '\n' + style_marker, 1)

    if SYNC_TAG_STATE_OLD not in page:
        raise RuntimeError('tag state synchronization marker not found in build_site_v4 output')
    page = page.replace(SYNC_TAG_STATE_OLD, SYNC_TAG_STATE_NEW, 1)

    if REFERENCE_CARD_OLD not in page:
        raise RuntimeError('reference card renderer marker not found in build_site_v4 output')
    page = page.replace(REFERENCE_CARD_OLD, REFERENCE_CARD_NEW, 1)

    if CARD_TAG_OLD not in page:
        raise RuntimeError('card tag renderer marker not found in build_site_v4 output')
    page = page.replace(CARD_TAG_OLD, CARD_TAG_NEW, 1)

    page, filter_tag_count = FILTER_TAG_PATTERN.subn(
        lambda match: (
            f'<button class="tag" type="button" data-filter-tag="{match.group(1)}" aria-pressed="false">'
            f'<span class="tag-check" aria-hidden="true">✓</span>'
            f'<span class="tag-label">{match.group(2)}</span>'
            '</button>'
        ),
        page,
    )
    if filter_tag_count == 0:
        raise RuntimeError('filter tag buttons not found in build_site_v4 output')

    page = _apply_grouped_ui(page, categories)

    page = page.replace(
        'Generated by <code>scripts/build_site_v3.py</code>',
        'Generated by <code>scripts/build_site_v5.py</code>',
        1,
    )
    return page


def main() -> int:
    previous.render = render
    return previous.main()


if __name__ == '__main__':
    raise SystemExit(main())
