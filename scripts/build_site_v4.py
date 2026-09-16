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

    scope_description = (
        '        <p class="scope-description">カテゴリーをまたいで、登録されている実績を通して読む。'
        '目次は表示条件ではなく、各カテゴリーへのページ内リンク。</p>\n'
    )
    if scope_description not in page:
        raise RuntimeError('scope description marker not found in build_site_v3 output')
    page = page.replace(scope_description, '', 1)

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
