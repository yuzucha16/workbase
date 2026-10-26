#!/usr/bin/env python3
"""find-knowledge.ps1 の Python 版（標準ライブラリだけ。pwsh が無い環境、例: AI 作業部屋用）。

`stock-hook.md` の手順「既存の知識と重なるか確認する」の検索を行う。
exmem/lessons/ のファイル名、見出し（^#）、frontmatter の tags / aliases / title を、キーワードで検索し、
ヒットしたキーワードの種類が多い順に、ファイルを最大 3 件まで示す。
各ファイルに大きさ（KB）を、ヒットした見出しに節の行の範囲（L開始-終了）を添える。

使い方: python find_knowledge.py [--body] [--top N] キーワード... （日本語と英語の両方。大文字小文字は区別しない。リテラル一致）
  --body  本文の行も検索する。見出しに無い語（コマンド名、エラー文言、変数名）で探すとき
読み取り専用。lessons/ は編集しない。

作業の言葉の索引（2026-10-25。設計は topics/md-link-graph/records/design-triggers.md）:
  python find_knowledge.py --triggers "<依頼文>" [--top N]   依頼文に triggers: の語を含むノートを示す（表は持たず、毎回 frontmatter を読む）
  python find_knowledge.py --list-triggers                   全ノートの「語 → ノート」の表（人が見る用）
  python find_knowledge.py --check-triggers                  lessons と guides/explain の全ノートに triggers:（1〜15 語）があるか
  python find_knowledge.py --check-index                      exmem-index.md の行と lessons/ のノートが一致するか（抜け・存在しない行・重複）

期限のあるナレッジ（logbook/。型は logbook/README.md。2026-10-26）:
  python find_knowledge.py --check-aging [--today YYYY-MM-DD]  review_by を過ぎた・budget を超えた・frontmatter が欠けたファイル
"""
import argparse
import datetime
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


TRIGGERS_MAX = 15


def trigger_sources(repo):
    """(ラベル, ディレクトリ) の一覧。inbox は未統合のメモ（README を除く）。"""
    return [("lessons", repo / "exmem" / "lessons"), ("explain", repo / "guides" / "explain"), ("inbox", repo / "exmem" / "inbox")]


def read_triggers(path):
    """frontmatter の `triggers: [a, b]` の語の一覧。frontmatter が無い・行が無いときは None。"""
    head = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---(?:\n|$)", head, re.S)
    if not m:
        return None
    t = re.search(r"^triggers:\s*\[(.*?)\]\s*$", m.group(1), re.M)
    if not t:
        return None
    return [w.strip() for w in t.group(1).split(",") if w.strip()]


def trigger_files(repo):
    for label, d in trigger_sources(repo):
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                if label == "inbox" and f.name.lower() == "readme.md":
                    continue
                yield label, f


def lookup_triggers(repo, query, top):
    """依頼文 query に、triggers の語が（大文字小文字を区別せず）含まれるノートを、一致した語の数が多い順に示す。"""
    q = query.lower()
    found = []
    for label, f in trigger_files(repo):
        words = read_triggers(f) or []
        hit = [w for w in words if len(w) >= 2 and w.lower() in q]
        if hit:
            found.append((len(hit), max(len(w) for w in hit), label, f, hit))
    if not found:
        print("該当なし（triggers の語が依頼文に無い）。必要なら exmem/exmem-index.md を引く")
        return 0
    found.sort(key=lambda x: (-x[0], -x[1], str(x[3])))
    for n, _, label, f, hit in found[:top]:
        mark = "（未統合）" if label == "inbox" else ""
        print(f"{f.relative_to(repo).as_posix()}  ({round(f.stat().st_size / 1024)}KB)  [{n}語: {', '.join(hit)}]{mark}")
    if len(found) > top:
        print(f"ほか {len(found) - top} 件（--top で増やせる）")
    return 0


def check_triggers(repo):
    """lessons と explain の全ノートに triggers: があり、15 語以内か。問題の数を返す。inbox は check_inbox の担当。"""
    bad = 0
    for label, f in trigger_files(repo):
        if label == "inbox":
            continue
        words = read_triggers(f)
        rel = f.relative_to(repo).as_posix()
        if words is None:
            print(f"FAIL: triggers が無い: {rel}")
            bad += 1
        elif not 1 <= len(words) <= TRIGGERS_MAX:
            print(f"FAIL: triggers が {len(words)} 語（1〜{TRIGGERS_MAX}）: {rel}")
            bad += 1
    print(f"RESULT: triggers fail={bad}")
    return bad


def check_index(repo):
    """exmem-index.md の [[名前]] の行と exmem/lessons/ のノートが一致するか（抜け、存在しない行、重複）。説明文は手書きなので比べない。問題の数を返す。"""
    index = repo / "exmem" / "exmem-index.md"
    lessons = {f.stem for f in (repo / "exmem" / "lessons").glob("*.md")}
    listed = re.findall(r"^- \[\[([^\]|#]+)", index.read_text(encoding="utf-8-sig"), re.M)
    bad = 0
    for name in sorted(lessons - set(listed)):
        print(f"FAIL: 索引に無い: {name}")
        bad += 1
    for name in sorted(set(listed) - lessons):
        print(f"FAIL: 索引にあるがノートが無い: {name}")
        bad += 1
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        print(f"FAIL: 索引に重複: {name}")
        bad += 1
    print(f"RESULT: index fail={bad}（索引 {len(listed)} 行 / lessons {len(lessons)} 本）")
    return bad


AGING_REQUIRED = ("type", "title", "created", "updated", "review_by", "budget")


def read_front(path):
    """frontmatter の `キー: 値` の辞書（1 行の値だけ）。frontmatter が無いときは None。"""
    head = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---(?:\n|$)", head, re.S)
    if not m:
        return None
    front = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_]+):\s*(.*?)\s*(?:#.*)?$", line)
        if kv:
            front[kv.group(1)] = kv.group(2).strip("\"'")
    return front


def parse_budget(text):
    """`8KB` `512B` `1MB` をバイト数に。読めなければ None。"""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(B|KB|MB)", text.strip(), re.I)
    if not m:
        return None
    return int(float(m.group(1)) * {"B": 1, "KB": 1024, "MB": 1024 * 1024}[m.group(2).upper()])


def check_aging(repo, today):
    """logbook/ の各ファイル（README を除く）を点検し、問題の数を返す。判断（捨てる・圧縮・昇格・延長）は月次の振り返りで行う。"""
    d = repo / "logbook"
    files = [f for f in sorted(d.glob("*.md")) if f.name.lower() != "readme.md"] if d.is_dir() else []
    bad = 0
    for f in files:
        rel = f.relative_to(repo).as_posix()
        front = read_front(f)
        if front is None:
            print(f"FAIL: frontmatter が無い: {rel}")
            bad += 1
            continue
        missing = [k for k in AGING_REQUIRED if not front.get(k)]
        if missing:
            print(f"FAIL: frontmatter に {', '.join(missing)} が無い: {rel}")
            bad += 1
        if front.get("type") and front["type"] != "logbook":
            print(f"FAIL: type が logbook でない（{front['type']}）: {rel}")
            bad += 1
        if front.get("review_by"):
            try:
                due = datetime.date.fromisoformat(front["review_by"])
            except ValueError:
                print(f"FAIL: review_by が日付でない（{front['review_by']}）: {rel}")
                bad += 1
            else:
                if due < today:
                    print(f"FAIL: review_by を過ぎた（{due}、{(today - due).days} 日）: {rel}")
                    bad += 1
        if front.get("budget"):
            limit = parse_budget(front["budget"])
            size = f.stat().st_size
            if limit is None:
                print(f"FAIL: budget が読めない（{front['budget']}。例: 8KB）: {rel}")
                bad += 1
            elif size > limit:
                print(f"FAIL: budget を超えた（{round(size / 1024, 1)}KB > {front['budget']}）: {rel}")
                bad += 1
    print(f"RESULT: aging fail={bad}（logbook {len(files)} 本、基準日 {today}）")
    return bad


def main():
    ap = argparse.ArgumentParser(description="exmem/lessons/ を、キーワードで検索する")
    ap.add_argument("keyword", nargs="*")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--body", action="store_true")
    ap.add_argument("--lessons", help="lessons/ の場所（省略時は kit の隣の exmem/lessons）")
    ap.add_argument("--triggers", metavar="依頼文", help="依頼文の言葉から、triggers: が当たるノートを引く（lessons・guides/explain・未統合の inbox。--top の既定は 5）")
    ap.add_argument("--check-triggers", action="store_true", help="lessons と guides/explain の全ノートに triggers: があるか点検する")
    ap.add_argument("--check-index", action="store_true", help="exmem-index.md の行と lessons/ のノートが一致するか点検する")
    ap.add_argument("--list-triggers", action="store_true", help="全ノートの triggers: を「語 → ノート」の表で出す（人が見る用。毎回ノートから作る）")
    ap.add_argument("--check-aging", action="store_true", help="logbook/ の review_by・budget・frontmatter を点検する")
    ap.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today(), help="--check-aging の基準日（既定は今日。YYYY-MM-DD）")
    ap.add_argument("--repo", help=argparse.SUPPRESS)  # 単体の確認用。既定は kit の 2 つ上
    args = ap.parse_args()
    repo = Path(args.repo) if args.repo else Path(__file__).resolve().parent.parent.parent
    if args.check_aging:
        return check_aging(repo, args.today)
    if args.check_triggers:
        return check_triggers(repo)
    if args.check_index:
        return check_index(repo)
    if args.list_triggers:
        for label, f in trigger_files(repo):
            words = read_triggers(f)
            if words:
                print(f"- {' / '.join(words)} → `{f.relative_to(repo).as_posix()}`" + ("（未統合）" if label == "inbox" else ""))
        return 0
    if args.triggers is not None:
        return lookup_triggers(repo, args.triggers, args.top if args.top != 3 else 5)
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
