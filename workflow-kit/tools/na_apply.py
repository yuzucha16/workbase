#!/usr/bin/env python3
"""docs/log.md の Next Actions・Open Questions の項目を閉じる・期日から上げる（書き込みの置き場所だけを機械化する）。

判断（済・一部済・omit の仕分け、根拠の文面）は AI が行い、結果をこのスクリプトに渡す。文面は書き換えない。
想定外の書式（項目が一意に決まらない、`## Log` が無いなど）のときは、何も書かずに止まる。そのときは手で直す。
手順は `docs-write-map.md`。

使い方:
  python -I na_apply.py close --plan <plan.json | -> [--dry-run]
  python -I na_apply.py due-up --due <due.md> --log <log.md> [--only 語]... [--next 語=YYYY-MM-DD]... [--today YYYY-MM-DD] [--dry-run]

close の plan.json（UTF-8）:
  {"log": "docs/log.md", "history": "docs/log-history.md（省略時は log と同じ場所）", "due": "docs/due.md（省略可）",
   "date": "YYYY-MM-DD（省略時は今日）", "title": "履歴の見出しの括弧の中（項目ごとに上書き可）",
   "items": [{"item": 5 または "項目の一部の文字列", "section": "Next Actions"（省略時。"Open Questions" も可）,
              "kind": "done" | "omit" | "partial", "note": "根拠・結果（履歴に書く文）",
              "rewrite": "partial のとき、残りの作業だけに書き直した文（項目の番号は付けない）",
              "due_match": "due.md から消す行の一部の文字列（省略可）", "title": "この項目だけの見出し（省略可）"}]}
  項目の番号は振り直さない（他から参照されるため）。全項目を検証してから書く（1 件でも失敗したら何も書かない）。
"""
import argparse
import difflib
import json
import re
import sys
from datetime import date
from pathlib import Path

ITEM_START = re.compile(r"^(?:(\d+)\.\s|[-*]\s)")
DUE_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|\s*$")
SECTION_SHORT = {"Next Actions": "NA", "Open Questions": "OQ"}
KIND_LABEL = {"done": "済", "omit": "omit", "partial": "一部済"}


class Stop(Exception):
    """書式や指定が想定外。何も書かずに止まる理由を持つ。"""


def read_lines(path):
    p = Path(path)
    if not p.is_file():
        raise Stop(f"{path}: ファイルが無い")
    return p.read_text(encoding="utf-8").split("\n")


def find_section(lines, name):
    """`## <name>` の節の行範囲 [開始, 終了) を返す（見出しの次の行から、次の `## ` の手前まで）。"""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {name}":
            if start is not None:
                raise Stop(f"`## {name}` が複数ある")
            start = i + 1
    if start is None:
        raise Stop(f"`## {name}` が無い")
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def parse_items(lines, name):
    """節の項目を [{'num', 'start', 'end', 'text', 'marker'}] で返す。end は項目の最後の非空行の次。"""
    s, e = find_section(lines, name)
    starts = [i for i in range(s, e) if ITEM_START.match(lines[i])]
    items = []
    for k, st in enumerate(starts):
        limit = starts[k + 1] if k + 1 < len(starts) else e
        end = st + 1
        for j in range(st + 1, limit):
            if lines[j].strip():
                end = j + 1
        m = ITEM_START.match(lines[st])
        block = lines[st:end]
        text = "\n".join([lines[st][m.end():]] + block[1:])
        items.append({"num": int(m.group(1)) if m.group(1) else None, "start": st, "end": end,
                      "text": text, "marker": lines[st][:m.end()]})
    return items, (s, e)


def pick(items, selector, label):
    if isinstance(selector, int) or (isinstance(selector, str) and selector.isdigit()):
        n = int(selector)
        hit = [it for it in items if it["num"] == n]
    else:
        hit = [it for it in items if selector in it["text"]]
    if len(hit) != 1:
        raise Stop(f"{label} {selector!r}: 一意に決まらない（該当 {len(hit)} 件）")
    return hit[0]


def remove_block(lines, start, end):
    del lines[start:end]
    if start > 0 and start < len(lines) and not lines[start - 1].strip() and not lines[start].strip():
        del lines[start]


def add_history(lines, heading, bullets):
    """`## Log` の下の `### heading` に bullets を足す（無ければ先頭に見出しを作る）。"""
    log_at = [i for i, line in enumerate(lines) if line.strip() == "## Log"]
    if len(log_at) != 1:
        raise Stop("log-history.md の `## Log` が 1 つに決まらない")
    top = f"### {heading}"
    same = [i for i, line in enumerate(lines) if line.rstrip() == top]
    if len(same) > 1:
        raise Stop(f"履歴に同じ見出しが複数ある: {top}")
    if same:
        i = same[0] + 1
        last = same[0]
        while i < len(lines) and not lines[i].startswith("#"):
            if lines[i].strip():
                last = i
            i += 1
        lines[last + 1:last + 1] = bullets
        return
    at = log_at[0] + 1
    while at < len(lines) and not lines[at].strip():
        at += 1
    lines[at:at] = [top] + bullets + [""]
    if log_at[0] + 1 == at:
        lines.insert(at, "")


def plan_close(plan):
    log_path = plan["log"]
    hist_path = plan.get("history") or str(Path(log_path).with_name("log-history.md"))
    today = plan.get("date") or date.today().isoformat()
    log = read_lines(log_path)
    hist = read_lines(hist_path)
    due = read_lines(plan["due"]) if plan.get("due") else None
    groups = {}
    jobs = []
    for spec in plan["items"]:
        section = spec.get("section", "Next Actions")
        kind = spec.get("kind")
        if kind not in KIND_LABEL:
            raise Stop(f"kind は done|omit|partial: {kind!r}")
        if not spec.get("note"):
            raise Stop(f"{spec.get('item')!r}: note（根拠）が空")
        items, _ = parse_items(log, section)
        it = pick(items, spec["item"], section)
        if kind == "partial" and not spec.get("rewrite"):
            raise Stop(f"{spec['item']!r}: partial には rewrite が要る")
        jobs.append((it, spec, section))
    seen = set()
    for it, _, section in jobs:
        if (section, it["start"]) in seen:
            raise Stop("同じ項目が重複して指定されている")
        seen.add((section, it["start"]))
    # 行番号がずれないよう、後ろの項目から log を直す
    for it, spec, section in sorted(jobs, key=lambda j: -j[0]["start"]):
        kind = spec["kind"]
        short = SECTION_SHORT.get(section, section)
        ref = f"{short}{it['num']}" if it["num"] is not None else short
        bullet = [f"- {KIND_LABEL[kind]}（{ref}）: {spec['note']}"]
        if kind != "partial":
            bullet.append("  - 元の項目: " + " ".join(it["text"].split()))
        title = spec.get("title") or plan.get("title")
        if not title:
            raise Stop("title（履歴の見出し）が無い")
        groups.setdefault(f"{today}（{title}）", []).insert(0, bullet)
        if kind == "partial":
            log[it["start"]:it["end"]] = [it["marker"] + spec["rewrite"]]
        else:
            remove_block(log, it["start"], it["end"])
        if spec.get("due_match"):
            if due is None:
                raise Stop("due_match があるのに plan に due が無い")
            rows = [i for i, line in enumerate(due) if DUE_ROW.match(line) and spec["due_match"] in line]
            if len(rows) != 1:
                raise Stop(f"due_match {spec['due_match']!r}: 一意に決まらない（該当 {len(rows)} 件）")
            del due[rows[0]]
    for heading, bullet_lists in groups.items():
        add_history(hist, heading, [b for bl in bullet_lists for b in bl])
    out = [(log_path, log), (hist_path, hist)]
    if due is not None:
        out.append((plan["due"], due))
    return out


def plan_due_up(due_path, log_path, only, nexts, today):
    due = read_lines(due_path)
    log = read_lines(log_path)
    items, (s, e) = parse_items(log, "Next Actions")
    nums = [it["num"] for it in items if it["num"] is not None]
    numbered = bool(nums) or not items
    next_num = (max(nums) + 1) if nums else 1
    insert_at = items[-1]["end"] if items else s
    new_lines, skipped, taken = [], [], []
    for i, line in list(enumerate(due)):
        m = DUE_ROW.match(line)
        if not m or date.fromisoformat(m.group(1)) > today:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 3:
            continue
        day, kind, text = m.group(1), cells[0], cells[1]
        if only and not any(w in line for w in only):
            continue
        nxt = next((v for k, v in nexts if k in line), None)
        if kind == "定例" and not nxt:
            skipped.append(f"{day} [定例] {text}（--next 語=YYYY-MM-DD で次回の期日が要る）")
            continue
        marker = f"{next_num}. " if numbered else "- "
        item = f"{marker}【起票 {today:%m-%d}、期日 {day[5:]}】{text}"
        if cells[2]:
            item += f"（担当: {cells[2]}）"
        new_lines.append(item)
        next_num += 1
        if kind == "定例":
            date.fromisoformat(nxt)
            due[i] = line.replace(day, nxt, 1)
        else:
            taken.append(i)
    for i in sorted(taken, reverse=True):
        del due[i]
    log[insert_at:insert_at] = new_lines
    return [(due_path, due), (log_path, log)], new_lines, skipped


def show_or_write(outputs, dry, originals):
    for path, new in outputs:
        text = "\n".join(new)
        if dry:
            diff = difflib.unified_diff(originals[path].split("\n"), new, path, path, lineterm="", n=0)
            print("\n".join(diff) or f"{path}: 変更なし")
        else:
            Path(path).write_text(text, encoding="utf-8", newline="")
            print(f"書いた: {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("close")
    c.add_argument("--plan", required=True)
    d = sub.add_parser("due-up")
    d.add_argument("--due", required=True)
    d.add_argument("--log", required=True)
    d.add_argument("--only", action="append", default=[])
    d.add_argument("--next", action="append", default=[], metavar="語=YYYY-MM-DD")
    d.add_argument("--today")
    for p in (c, d):
        p.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        if args.cmd == "close":
            raw = sys.stdin.buffer.read().decode("utf-8") if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
            plan = json.loads(raw)
            outputs = plan_close(plan)
            extra = []
        else:
            nexts = [tuple(v.split("=", 1)) for v in args.next]
            today = date.fromisoformat(args.today) if args.today else date.today()
            outputs, extra, skipped = plan_due_up(args.due, args.log, args.only, nexts, today)
            for s in skipped:
                print("上げなかった:", s)
        originals = {p: "\n".join(read_lines(p)) for p, _ in outputs}
        show_or_write(outputs, args.dry_run, originals)
        for line in extra:
            print("上げた:", line)
    except (Stop, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"止まった（何も書いていない）: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
