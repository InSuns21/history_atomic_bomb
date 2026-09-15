#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ACHIEVEMENTS.md"


@dataclass(frozen=True)
class Category:
    path: str
    title: str
    description: str
    codes: tuple[str, ...]


CATEGORIES = [
    Category(
        "achievements/00_science.md",
        "科学史・核技術の成立",
        "原子・放射能・核分裂・連鎖反応から、核融合や元素合成などの関連科学史まで。",
        ("0", "7"),
    ),
    Category(
        "achievements/01_hiroshima_nagasaki.md",
        "1945年8月・被爆",
        "広島・長崎への原爆投下、直後の被害、救護、そして終戦前後の出来事。",
        ("1",),
    ),
    Category(
        "achievements/02_aftermath_memory.md",
        "復興・被爆後・記憶継承",
        "被爆後障害、医療、都市復興、証言、資料館、追悼、外交と記憶の継承。",
        ("2", "8"),
    ),
    Category(
        "achievements/03_cold_war_deterrence.md",
        "冷戦・核抑止・軍縮",
        "核軍拡、ミサイル、第二撃能力、核抑止、軍縮と、核時代に反復する基本問題。",
        ("3", "6"),
    ),
    Category(
        "achievements/04_civil_nuclear.md",
        "原子力平和利用・デュアルユース",
        "Atoms for Peace、原子炉、核燃料サイクル、原子力事故、核融合発電への道。",
        ("4",),
    ),
    Category(
        "achievements/05_national_cases.md",
        "各国・地域の核史",
        "フランス、南アジア、北朝鮮など、各国・地域が核兵器と原子力をどう位置付けたか。",
        ("4A", "5", "5A"),
    ),
    Category(
        "achievements/06_future.md",
        "未来実績",
        "まだ解除されていない未来実績と、核時代の終端として残る二つの可能性。",
        ("9", "10"),
    ),
]

SECTION_RE = re.compile(r"(?m)^## (?P<heading>.+)$")
CODE_RE = re.compile(r"^(?P<code>\d+A?)\.")
TRAILING_RULE_RE = re.compile(r"(?:\n\s*---\s*)+$")


def split_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        raise ValueError("no level-2 sections found in ACHIEVEMENTS.md")

    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        heading = match.group("heading").strip()
        code_match = CODE_RE.match(heading)
        if not code_match:
            raise ValueError(f"section heading has no numeric code: {heading}")
        code = code_match.group("code")
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[match.start():end].strip()
        block = TRAILING_RULE_RE.sub("", block).rstrip()
        if code in sections:
            raise ValueError(f"duplicate section code: {code}")
        sections[code] = block
    return sections


def render_manifest() -> str:
    links = "\n".join(
        f"- [{c.title}]({c.path}) — {c.description}" for c in CATEGORIES
    )
    return f"""# 実績一覧（正本インデックス）

> 核兵器・原子力・被爆地の記憶・核軍縮・関連科学史を、史実イベントに対応する「実績」として整理する。
>
> 実績本文は `achievements/*.md` にカテゴリー別で分割し、このファイルを**正本インデックス**として構成・順序を管理する。GitHub Pages はこの一覧に記載されたファイルを順番に読み込む。

## 編集原則

- 実績名は創作。
- 日付・出来事は史実準拠を目指す。
- 心理描写・文学的説明は史実そのものと区別する。
- `🔒` は現時点で未解除の未来実績。
- `反復` は同種の出来事で複数回解除されうる実績。
- 年代・帰属が未確定のものは「要検証」とする。
- 各実績には複数のタグを明示し、GitHub Pages 上で横断的に絞り込めるようにする。
- タグは `TAGGING_GUIDELINES.md` に従い、場所・主題・技術・状態をできるだけ直交させて付ける。
- 本文は文字数を目的化しない。原則120字以上を最低線、160～300字程度を目安に、その実績固有の人物・場所・技術・因果関係で説明する。一般論の水増しは禁止する。
- 実績名が実在の発言・楽曲・作品・ゲーム文化などのオマージュである場合、元ネタが歴史的意味を担うなら本文で由来を残す。本人の実際の発言と誤認させない。
- 同一の史実イベントを複数カテゴリーへ重複登録しない。複数の観点を持つ場合はタグで横断する。

## カテゴリー

{links}

## 表示と検証

GitHub Pages はカテゴリーを同一ページ内で視覚的に区切って表示する。タグは上部のタグ一覧だけでなく、各実績カード上のタグからも絞り込みできる。

ローカル検証・ビルド:

```bash
python scripts/build_site_v2.py --check --strict-length --strict-tags
```
"""


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    if "achievements/00_science.md" in text:
        print("category migration already applied")
        return 0

    sections = split_sections(text)
    expected = {code for category in CATEGORIES for code in category.codes}
    actual = set(sections)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        raise SystemExit("missing expected sections: " + ", ".join(missing))
    if unexpected:
        raise SystemExit("unmapped sections: " + ", ".join(unexpected))

    for category in CATEGORIES:
        target = ROOT / category.path
        target.parent.mkdir(parents=True, exist_ok=True)
        body = "\n\n---\n\n".join(sections[code] for code in category.codes)
        target.write_text(
            f"# {category.title}\n\n> {category.description}\n\n{body}\n",
            encoding="utf-8",
        )
        print(f"wrote {target.relative_to(ROOT)}")

    SOURCE.write_text(render_manifest(), encoding="utf-8")
    print("rewrote ACHIEVEMENTS.md as category manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
