#!/usr/bin/env python3
from __future__ import annotations

import copy
import re
import unicodedata
from pathlib import Path

import build_site_v4 as previous


_render_v4 = previous.render


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


def _collect_reference_items(items, categories):
    """Resolve view-only references without duplicating canonical achievement sources."""
    target_by_key = {item.key: item for item in items}
    references = []
    seen = set()

    for category in categories:
        path = Path(category.path)
        in_reference_section = False
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                in_reference_section = "参照" in line[3:]
                continue
            if not in_reference_section:
                continue

            match = re.match(r"^- \*\*(?P<label>.+?)\*\*(?:\s+—.*)?$", line.strip())
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
            clone.section = "既存実績への参照"
            clone.subsection = f"正本: {getattr(target, 'category', '')}"
            references.append(clone)

    return references


def render(items, categories) -> str:
    display_items = list(items)
    display_items.extend(_collect_reference_items(items, categories))
    page = _render_v4(display_items, categories)
    style_marker = '</style>'
    if style_marker not in page:
        raise RuntimeError('style closing marker not found in build_site_v4 output')
    page = page.replace(style_marker, GAME_UI_CSS + '\n' + style_marker, 1)

    if SYNC_TAG_STATE_OLD not in page:
        raise RuntimeError('tag state synchronization marker not found in build_site_v4 output')
    page = page.replace(SYNC_TAG_STATE_OLD, SYNC_TAG_STATE_NEW, 1)

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
