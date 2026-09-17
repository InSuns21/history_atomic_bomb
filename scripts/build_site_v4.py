#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
from pathlib import Path

import build_site as legacy
import build_site_v2 as base
import build_site_v3 as previous


FORBIDDEN_META_PHRASES = (
    'ゲーム用',
    'タイトルは創作',
    '実績名は創作',
    '実際の発言ではない',
    '本人の発言ではない',
)


def mobile_toc(categories: list[base.Category]) -> str:
    links = [
        '<a class="category-link" href="#top">全実績</a>'
    ]
    links.extend(
        f'<a class="category-link" href="#category-{html.escape(c.id, quote=True)}">'
        f'{html.escape(c.title)}'
        f'</a>'
        for c in categories
    )
    return (
        '<nav class="mobile-toc" aria-label="モバイル目次">'
        '<span class="mobile-toc-label">目次</span>'
        + ''.join(links)
        + '</nav>'
    )


def remove_empty_representative_artifacts(items: list[legacy.Achievement]) -> None:
    # The legacy parser can mistake a Markdown horizontal rule (`---`) at the end of
    # an achievement block for an empty list item and append `代表例：。`.
    for item in items:
        if item.body.endswith('代表例：。'):
            item.body = item.body.removesuffix('代表例：。').rstrip()


def validate_meta_wording() -> list[str]:
    errors: list[str] = []
    for path in sorted(Path('achievements').glob('*.md')):
        for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            hits = [phrase for phrase in FORBIDDEN_META_PHRASES if phrase in line]
            if not hits:
                continue
            errors.append(
                f'{path}:{line_no}: メタなタイトル注記は禁止: '
                f'{", ".join(hits)}。由来や史実上の留保を本文として直接説明してください'
            )
    return errors


def render(items: list[legacy.Achievement], categories: list[base.Category]) -> str:
    page = previous.render(items, categories)

    branding_replacements = (
        (
            '<meta name="description" content="核兵器・原子力・被爆史・冷戦・核軍縮・科学史を、実績形式で時系列に読む歴史ゲーム資料。">',
            '<meta name="description" content="核兵器・原子力・被爆史・冷戦・核軍縮・関連科学史を、ゲーム実績風のカードで時系列にたどる資料庫。">',
        ),
        (
            '<title>核実績ゲーム — Achievements</title>',
            '<title>核時代資料庫 — 実績でたどる、原子と人類の歴史</title>',
        ),
        (
            '  <strong>核実績ゲーム</strong>',
            '  <strong>核時代資料庫</strong>',
        ),
        (
            '    <h1 class="brand">核実績ゲーム</h1>',
            '    <h1 class="brand">核時代資料庫</h1>',
        ),
        (
            '        <div class="scope-eyebrow">全カテゴリー</div>',
            '        <div class="scope-eyebrow">核時代資料庫</div>',
        ),
        (
            '        <h2 class="scope-title">全実績・時系列</h2>',
            '        <h2 class="scope-title">実績でたどる、原子と人類の歴史</h2>',
        ),
    )
    for old, new in branding_replacements:
        if old not in page:
            raise RuntimeError(f'branding marker not found in build_site_v3 output: {old}')
        page = page.replace(old, new, 1)

    font_head_marker = '<style>\n'
    font_head = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?'
        'family=BIZ+UDPGothic:wght@400;700&'
        'family=M+PLUS+1+Code:wght@400;500;600;700;800;900&display=swap" '
        'rel="stylesheet">\n'
    )
    if font_head_marker not in page:
        raise RuntimeError('style marker not found in build_site_v3 output')
    page = page.replace(font_head_marker, font_head + font_head_marker, 1)

    body_font_marker = '  font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif;\n'
    body_font = '  font-family:"BIZ UDPGothic","Yu Gothic UI","Meiryo",sans-serif;\n'
    if body_font_marker not in page:
        raise RuntimeError('body font marker not found in build_site_v3 output')
    page = page.replace(body_font_marker, body_font, 1)

    ui_font_marker = 'button,input { font:inherit; }\n'
    ui_font_css = '''button,input,
.brand,
.scope-eyebrow,
.scope-title,
.sidebar-section-title,
.category-link,
.tag-panel summary,
.sidebar-meta,
.category-header h2,
.section-heading,
.subsection-heading,
.mobile-bar,
.mobile-toc,
.date,
.achievement h5,
.unlock-condition strong,
footer,
code {
  font-family:"M PLUS 1 Code","BIZ UDPGothic",monospace;
}
'''
    if ui_font_marker not in page:
        raise RuntimeError('UI font marker not found in build_site_v3 output')
    page = page.replace(ui_font_marker, ui_font_marker + ui_font_css, 1)

    old_mobile_breakpoint = '@media (max-width:820px) {'
    if old_mobile_breakpoint not in page:
        raise RuntimeError('mobile breakpoint marker not found in build_site_v3 output')
    page = page.replace(old_mobile_breakpoint, '@media (max-width:700px) {', 1)

    scope_description = (
        '        <p class="scope-description">カテゴリーをまたいで、登録されている実績を通して読む。'
        '目次は表示条件ではなく、各カテゴリーへのページ内リンク。</p>\n'
    )
    new_scope_description = (
        '        <p class="scope-description">核兵器・原子力・被爆史・冷戦・核軍縮・関連科学史を、'
        '史実イベントに対応するゲーム実績風のカードとして時系列に整理する資料庫。</p>\n'
    )
    if scope_description not in page:
        raise RuntimeError('scope description marker not found in build_site_v3 output')
    page = page.replace(scope_description, new_scope_description, 1)

    css_marker = '  .mobile-bar strong { font-size:.95rem; }\n'
    css_extra = '''  .mobile-bar { flex-wrap:wrap; }
  .mobile-toc {
    display:flex;
    flex:1 0 100%;
    align-items:center;
    gap:.35rem;
    min-width:0;
    overflow-x:auto;
    padding-top:.45rem;
    scrollbar-width:thin;
  }
  .mobile-toc-label {
    flex:0 0 auto;
    color:var(--muted);
    font-size:.72rem;
    font-weight:800;
    letter-spacing:.08em;
  }
  .mobile-toc .category-link {
    width:auto;
    flex:0 0 auto;
    padding:.28rem .55rem;
    border-color:var(--line);
    background:var(--bg);
    font-size:.78rem;
    white-space:nowrap;
  }
'''
    if css_marker not in page:
        raise RuntimeError('mobile bar CSS marker not found in build_site_v3 output')
    page = page.replace(css_marker, css_marker + css_extra, 1)

    card_css_marker = '.achievement p { margin:.65rem 0 .5rem; }\n'
    card_css_extra = '''.unlock-condition {
  margin:.7rem 0 1rem;
  padding:0 0 .8rem;
  border-bottom:1px solid var(--line);
}
.unlock-condition strong {
  display:block;
  margin-bottom:.18rem;
  color:var(--muted);
  font-size:.78rem;
  letter-spacing:.04em;
}
.achievement-description { margin-top:0; }
'''
    if card_css_marker not in page:
        raise RuntimeError('achievement paragraph CSS marker not found in build_site_v3 output')
    page = page.replace(card_css_marker, card_css_marker + card_css_extra, 1)

    old_card_html = '''function cardHtml(a) {
  return `<article class="achievement ${a.future?'future':''}"><div class="date">${escapeHtml(a.date)}</div><h5>${escapeHtml(a.title)}</h5><p>${escapeHtml(a.body)}</p><div class="chips">${a.tags.map(t=>`<button type="button" class="card-tag" data-card-tag="${escapeHtml(t)}">#${escapeHtml(t)}</button>`).join('')}</div></article>`;
}
'''
    new_card_html = '''function cardHtml(a) {
  const conditionMatch = a.body.match(/^解除条件：(.+?。)\\s*(.*)$/s);
  const bodyHtml = conditionMatch
    ? `<div class="unlock-condition"><strong>解除条件</strong><div>${escapeHtml(conditionMatch[1])}</div></div>${conditionMatch[2] ? `<p class="achievement-description">${escapeHtml(conditionMatch[2])}</p>` : ''}`
    : `<p class="achievement-description">${escapeHtml(a.body)}</p>`;
  return `<article class="achievement ${a.future?'future':''}"><div class="date">${escapeHtml(a.date)}</div><h5>${escapeHtml(a.title)}</h5>${bodyHtml}<div class="chips">${a.tags.map(t=>`<button type="button" class="card-tag" data-card-tag="${escapeHtml(t)}">#${escapeHtml(t)}</button>`).join('')}</div></article>`;
}
'''
    if old_card_html not in page:
        raise RuntimeError('achievement card renderer marker not found in build_site_v3 output')
    page = page.replace(old_card_html, new_card_html, 1)

    old_toggle_tag = '''function toggleTag(tag) {
  active.has(tag) ? active.delete(tag) : active.add(tag);
  render();
}
'''
    new_toggle_tag = '''function cardAnchor(card) {
  if (!card) return null;
  return {
    date: card.querySelector('.date')?.textContent || '',
    title: card.querySelector('h5')?.textContent || '',
    tags: [...card.querySelectorAll('[data-card-tag]')].map(button => button.dataset.cardTag).join('\\u001f'),
    top: card.getBoundingClientRect().top,
  };
}
function visibleCardAnchor() {
  const mobileBar = document.querySelector('.mobile-bar');
  const viewportTop = mobileBar && getComputedStyle(mobileBar).display !== 'none'
    ? mobileBar.getBoundingClientRect().bottom
    : 0;
  const cards = [...document.querySelectorAll('.achievement')];
  const card = cards.find(candidate => {
    const rect = candidate.getBoundingClientRect();
    return rect.bottom > viewportTop && rect.top < window.innerHeight;
  });
  return cardAnchor(card);
}
function restoreCardAnchor(anchor) {
  if (!anchor) return;
  const card = [...document.querySelectorAll('.achievement')].find(candidate =>
    (candidate.querySelector('.date')?.textContent || '') === anchor.date &&
    (candidate.querySelector('h5')?.textContent || '') === anchor.title &&
    [...candidate.querySelectorAll('[data-card-tag]')].map(button => button.dataset.cardTag).join('\\u001f') === anchor.tags
  );
  if (!card) return;
  const delta = card.getBoundingClientRect().top - anchor.top;
  if (Math.abs(delta) > 1) {
    window.scrollBy({top: delta, left: 0, behavior: 'instant'});
  }
}
function toggleTag(tag, preferredAnchor = null) {
  const removing = active.has(tag);
  const anchor = preferredAnchor || (removing ? visibleCardAnchor() : null);
  removing ? active.delete(tag) : active.add(tag);
  render(anchor);
}
'''
    if old_toggle_tag not in page:
        raise RuntimeError('tag toggle marker not found in build_site_v3 output')
    page = page.replace(old_toggle_tag, new_toggle_tag, 1)

    old_render_signature = 'function render() {\n'
    if old_render_signature not in page:
        raise RuntimeError('render function marker not found in build_site_v3 output')
    page = page.replace(old_render_signature, 'function render(anchor = null) {\n', 1)

    old_render_tail = '''  updateFilterHeader(shown.length);
  syncTagState();
}
'''
    new_render_tail = '''  updateFilterHeader(shown.length);
  syncTagState();
  restoreCardAnchor(anchor);
}
'''
    if old_render_tail not in page:
        raise RuntimeError('render tail marker not found in build_site_v3 output')
    page = page.replace(old_render_tail, new_render_tail, 1)

    old_card_tag_handler = "document.querySelectorAll('[data-card-tag]').forEach(b => b.addEventListener('click', () => toggleTag(b.dataset.cardTag)));"
    new_card_tag_handler = "document.querySelectorAll('[data-card-tag]').forEach(b => b.addEventListener('click', () => toggleTag(b.dataset.cardTag, cardAnchor(b.closest('.achievement')))));"
    if old_card_tag_handler not in page:
        raise RuntimeError('card tag handler marker not found in build_site_v3 output')
    page = page.replace(old_card_tag_handler, new_card_tag_handler, 1)

    old_clear_handler = "document.getElementById('clear').addEventListener('click', () => { active.clear(); search.value=''; render(); });"
    new_clear_handler = '''document.getElementById('clear').addEventListener('click', () => {
  const anchor = visibleCardAnchor();
  active.clear();
  search.value='';
  render(anchor);
});'''
    if old_clear_handler not in page:
        raise RuntimeError('clear filter handler marker not found in build_site_v3 output')
    page = page.replace(old_clear_handler, new_clear_handler, 1)

    old_mobile_header = (
        '  <button id="sidebar-toggle" class="mobile-toggle" type="button" '
        'aria-expanded="false" aria-controls="sidebar">目次・検索</button>\n'
        '</div>'
    )
    new_mobile_header = (
        '  <button id="sidebar-toggle" class="mobile-toggle" type="button" '
        'aria-expanded="false" aria-controls="sidebar">検索・タグ</button>\n'
        f'  {mobile_toc(categories)}\n'
        '</div>'
    )
    if old_mobile_header not in page:
        raise RuntimeError('mobile header marker not found in build_site_v3 output')
    return page.replace(old_mobile_header, new_mobile_header, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='validate source before building')
    parser.add_argument(
        '--strict-length',
        action='store_true',
        help=f'fail when a body is shorter than {legacy.MIN_BODY_CHARS} characters',
    )
    parser.add_argument(
        '--strict-tags',
        action='store_true',
        help='require tags to be written explicitly in category markdown files',
    )
    args = parser.parse_args()

    try:
        items, categories = base.load_items()
    except (OSError, ValueError) as exc:
        print(f'::error::{exc}')
        return 2

    remove_empty_representative_artifacts(items)

    errors, warnings = legacy.validate(items, args.strict_length, args.strict_tags)
    errors.extend(validate_meta_wording())
    for warning in warnings:
        print(f'::warning::{warning}')
    for error in errors:
        print(f'::error::{error}')
    if not items:
        print('::error::no achievements parsed')
        return 2
    if errors:
        return 1

    try:
        page = render(items, categories)
    except RuntimeError as exc:
        print(f'::error::{exc}')
        return 2

    base.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (base.OUT_DIR / 'index.html').write_text(page, encoding='utf-8')
    (base.OUT_DIR / '.nojekyll').write_text('', encoding='utf-8')
    print(
        f'built {len(items)} achievements in {len(categories)} categories '
        f'-> {base.OUT_DIR / "index.html"}'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())