#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html

import build_site as legacy
import build_site_v2 as base
import build_site_v3 as previous


def mobile_toc(categories: list[base.Category]) -> str:
    buttons = [
        '<button class="category-link" type="button" data-scope="all">全実績</button>'
    ]
    buttons.extend(
        f'<button class="category-link" type="button" data-scope="{html.escape(c.id, quote=True)}">'
        f'{html.escape(c.title)}'
        f'</button>'
        for c in categories
    )
    return (
        '<nav class="mobile-toc" aria-label="モバイル目次">'
        '<span class="mobile-toc-label">目次</span>'
        + ''.join(buttons)
        + '</nav>'
    )


def remove_empty_representative_artifacts(items: list[legacy.Achievement]) -> None:
    # The legacy parser can mistake a Markdown horizontal rule (`---`) at the end of
    # an achievement block for an empty list item and append `代表例：。`.
    for item in items:
        if item.body.endswith('代表例：。'):
            item.body = item.body.removesuffix('代表例：。').rstrip()


def render(items: list[legacy.Achievement], categories: list[base.Category]) -> str:
    page = previous.render(items, categories)

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
