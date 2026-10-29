#!/usr/bin/env python3
"""docs/due.md の表から、期日が今日以前（または --days 日以内）の行を出す（読み取り専用）。

`review 消化` が最初に実行する。出た単発の行は Next Actions に上げ、定例は次回の期日に書き換える（手順は review-hook.md）。
表の列: 期日 | 種別 | 内容 | 担当。期日が YYYY-MM-DD でない行は読み飛ばす。

使い方: python -I due.py [--days N] [--today YYYY-MM-DD] [due.md のパス...]
  パスの既定 = docs/due.md（作業ディレクトリから）。複数渡すと、パスごとに見出しを付けて出す。
  該当が無いときは「なし」と出す。期日が過ぎている行には、超過日数を付ける。
"""
import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|\s*$")


def due_rows(path, limit):
    """limit 以前の期日の行を、(期日, 種別, 内容, 担当) の並びで返す（期日の昇順）。"""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        day = date.fromisoformat(m.group(1))
        cells = [c.strip() for c in m.group(2).split("|")]
        if day <= limit and len(cells) >= 3:
            rows.append((day, cells[0], cells[1], cells[2]))
    return sorted(rows, key=lambda r: r[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", default=["docs/due.md"])
    ap.add_argument("--days", type=int, default=0, help="今日から何日先の期日まで出すか（既定 0）")
    ap.add_argument("--today", help="今日の日付（テスト用）")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    today = date.fromisoformat(args.today) if args.today else date.today()
    limit = today + timedelta(days=args.days)
    for p in args.paths:
        path = Path(p)
        if not path.is_file():
            print(f"{p}: ファイルが無い", file=sys.stderr)
            continue
        rows = due_rows(path, limit)
        print(f"## {p}（{today.isoformat()} 時点）")
        if not rows:
            print("なし")
            continue
        for day, kind, text, who in rows:
            late = (today - day).days
            mark = f"（{late}日超過）" if late > 0 else ""
            print(f"- {day.isoformat()}{mark} [{kind}] {text} / {who}")


if __name__ == "__main__":
    main()
