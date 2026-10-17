#!/usr/bin/env python3
"""find-knowledge.ps1 の Python 版（標準ライブラリだけ。pwsh が無い環境、例: AI 作業部屋用）。

`stock-hook.md` の手順「既存の知識と重なるか確認する」の検索を行う。
exmem/lessons/ のファイル名、見出し（^#）、frontmatter の tags / aliases / title を、キーワードで検索し、
ヒットしたキーワードの種類が多い順に、ファイルを最大 3 件まで示す。
各ファイルに大きさ（KB）を、ヒットした見出しに節の行の範囲（L開始-終了）を添える。

使い方: python find_knowledge.py [--body] [--top N] キーワード... （日本語と英語の両方。大文字小文字は区別しない。リテラル一致）
  --body  本文の行も検索する。見出しに無い語（コマンド名、エラー文言、変数名）で探すとき
読み取り専用。lessons/ は編集しない。
"""
import argparse
import re
import sys
from pathlib import Path


def find_lessons_dir():
    kit_root = Path(__file__).resolve().parent.parent
    candidates = [kit_root.parent / "exmem" / "lessons", kit_root.parent / "lessons"]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def scan(path, keywords, body):
    lines = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    # 見出しの階層。コードブロックの中の # は見出しに数えない
    level = {}
    fence = False
    for i, line in enumerate(lines):
        if re.match(r"^(```|~~~)", line):
            fence = not fence
            continue
        m = re.match(r"^(#{1,6})\s", line)
        if not fence and m:
            level[i] = len(m.group(1))
    heads = sorted(level)
    hit_kw = []
    evidence = []
    body_ev = []
    hits = 0
    in_front = False
    for i, line in enumerate(lines):
        if i == 0 and line == "---":
            in_front = True
            continue
        if in_front and line == "---":
            in_front = False
            continue
        target = False
        if in_front:
            target = bool(re.match(r"^(tags|aliases|title):", line) or re.match(r"^\s+-\s", line))
        elif line.startswith("#"):
            target = True
        is_body = False
        if not target and body and not in_front:
            target = True
            is_body = True
        if not target:
            continue
        low = line.lower()
        line_hit = False
        for k in keywords:
            if k.lower() in low:
                if k not in hit_kw:
                    hit_kw.append(k)
                line_hit = True
                if not is_body:
                    ev = f"L{i + 1}: {line.strip()}"
                    if i in level:
                        end = len(lines)
                        for h in heads:
                            if h > i and level[h] <= level[i]:
                                end = h
                                break
                        ev = f"L{i + 1}-{end}: {line.strip()}"
                    if len(evidence) < 3 and ev not in evidence:
                        evidence.append(ev)
        if line_hit:
            hits += 1
            if is_body and len(body_ev) < 2:
                t = line.strip()
                if len(t) > 110:
                    t = t[:110] + "…"
                body_ev.append(f"L{i + 1}: {t}")
    for k in keywords:  # ファイル名
        if k.lower() in path.stem.lower():
            if k not in hit_kw:
                hit_kw.append(k)
            evidence.append(f"ファイル名: {path.name}")
    if not hit_kw:
        return None
    evidence += [f"本文 {b}" for b in body_ev]
    return {"kinds": len(hit_kw), "hits": hits, "keywords": hit_kw, "evidence": evidence, "kb": round(path.stat().st_size / 1024)}


def main():
    ap = argparse.ArgumentParser(description="exmem/lessons/ を、キーワードで検索する")
    ap.add_argument("keyword", nargs="*")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--body", action="store_true")
    ap.add_argument("--lessons", help="lessons/ の場所（省略時は kit の隣の exmem/lessons）")
    args = ap.parse_args()
    keywords = [k for a in args.keyword for k in a.split(",") if k]
    if not keywords:
        print("キーワードを2〜4語、空白で並べる")
        return 1
    d = Path(args.lessons) if args.lessons else find_lessons_dir()
    if d is None or not d.is_dir():
        print(f"lessons/ が無い: {d}")
        return 1
    results = []
    for f in d.rglob("*.md"):
        r = scan(f, keywords, args.body)
        if r:
            r["file"] = f.relative_to(d).as_posix()
            results.append(r)
    if not results:
        print(f"ヒット無し（キーワード: {', '.join(keywords)}）。統合先の候補は「新規トピック」")
        return 0
    if args.body:
        results.sort(key=lambda r: (-r["kinds"], -r["hits"], r["file"]))
    else:
        results.sort(key=lambda r: (-r["kinds"], r["file"]))
    for r in results[: args.top]:
        print(f"lessons/{r['file']}  ({r['kb']}KB)  [{r['kinds']}/{len(keywords)} 語: {', '.join(r['keywords'])}]")
        for e in r["evidence"]:
            print(f"    {e}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
