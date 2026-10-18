#!/usr/bin/env python3
"""*-hook.md の章立ての共通部を点検する（check-hook-outline.ps1 の Python 版）。

pwsh が無い環境（クラウドのセッション、AI 作業部屋など）で使う。点検の中身は
check-hook-outline.ps1 と同じ。どちらかを直したら、もう一方も合わせる。

使い方: python tools/check_hook_outline.py
終了コード = FAIL の数。
"""
import re
import sys
from pathlib import Path

COMMON = ["目的と契機", "場所と書き込みの制約", "手順", "報告の型"]
BEFORE_OK = ["導入項目の一覧", "入力"]
KIT = Path(__file__).resolve().parent.parent
STEP_RE = re.compile(r"^\s*[0-9]+\. \*\*(.+?)\*\*", re.M)
REF_RE = re.compile(r"(?:`?([a-z]+-hook\.md)`?\s*の)?手順「([^」]+)」")


def read(p):
    return Path(p).read_text(encoding="utf-8")


def step_titles(raw):
    return [m.group(1).rstrip("。:：") for m in STEP_RE.finditer(raw)]


def has_step(titles, name):
    return any(t.startswith(name) for t in titles)


def main():
    fail = 0
    hook_files = sorted(KIT.glob("*-hook.md"), key=lambda p: p.name)
    hooks = [p.name for p in hook_files]
    common_text = read(KIT / "hook-common.md")

    for f in hook_files:
        raw = read(f)
        h2 = [l[3:].strip() for l in raw.splitlines() if l.startswith("## ")]
        found = [h for h in h2 if h in COMMON]
        missing = [c for c in COMMON if c not in found]
        dup = sorted({h for h in found if found.count(h) > 1})
        ordered = found == [c for c in COMMON if c in found]
        head = re.split(r"(?m)^## ", raw, maxsplit=1)[0]
        body = {}
        for c in COMMON:
            m = re.search(r"(?ms)^## " + re.escape(c) + r"[^\r\n]*\r?\n(.*?)(?=^## |\Z)", raw)
            body[c] = m.group(1) if m else ""
        content = []
        last = h2.index("報告の型") if "報告の型" in h2 else -1
        early = [
            h2[i] for i in range(0, max(last, 0))
            if not any(h2[i] == c or h2[i].startswith(c + "（") for c in COMMON) and h2[i] not in BEFORE_OK
        ]
        if early:
            content.append("固有の章が共通部の途中にある: " + "、".join(early))
        if re.search(r"手順 ?[0-9０-９]|手順の ?[0-9０-９]|」の [0-9０-９] ", raw):
            content.append("手順を番号で参照している（手順「名前」で書く）")
        titles = step_titles(raw)
        refs = []
        for m in re.finditer(r"手順「([^」]+)」|「手順」の「([^」]+)」", raw):
            # 他のフックのファイル名つきの参照（`xxx-hook.md` の手順「名前」）は、ここでは数えない
            if m.group(1) and re.search(r"-hook\.md`?\s*の$", raw[: m.start()]):
                continue
            refs.append(m.group(1) or m.group(2))
        dead = sorted({r for r in refs if not has_step(titles, r)})
        if dead:
            content.append("手順の参照先が無い: " + "、".join(dead))
        if "`hooks.md`" not in head:
            content.append("冒頭に正本 hooks.md の記載が無い")
        if "hook-common.md" not in body["報告の型"]:
            content.append("報告の型が hook-common.md の共通の項目を指していない")
        imp = re.search(r"(?ms)^## このフックの改善[^\r\n]*\r?\n(.*?)(?=^## |\Z)", raw)
        if imp and "hook-common.md" not in imp.group(1):
            content.append("改善の章が hook-common.md を指していない")
        name = f.stem.replace("-hook", "")
        if not re.search(r"(?m)^\| `" + name + r"` \|", common_text):
            content.append("hook-common.md の記録の表に行が無い")
        annot = [h for h in h2 if re.search(r"[（(]", h)]
        if annot:
            content.append("見出しに括弧の注記がある: " + "、".join(annot))
        labels = [m.group(1) for m in re.finditer(r"(?m)^- \*\*([^*]+)\*\*", body["目的と契機"])]
        if ",".join(labels) not in ("目的,契機", "目的,契機,前提", "目的,契機,モード", "目的,契機,前提,モード"):
            content.append("目的と契機の項目が「目的 → 契機 → 前提（任意）→ モード（任意）」でない: " + "、".join(labels))
        items = re.findall(r"(?m)^([0-9]+)\. \*\*([^*]+)\*\*", body["報告の型"])
        if not items:
            content.append("報告の型が番号つきリスト（太字のラベル）でない")
        elif [n for n, _ in items] != [str(i) for i in range(1, len(items) + 1)]:
            content.append("報告の型の番号が連番でない")
        elif any(label == "改善案" for _, label in items):
            content.append("報告の型に「改善案」を載せない（hook-common.md の「改善」）")
        if missing or dup or not ordered or content:
            fail += 1
            msg = []
            if missing:
                msg.append("欠け: " + "、".join(missing))
            if dup:
                msg.append("重複: " + "、".join(dup))
            if not ordered:
                msg.append("順序: " + " → ".join(found))
            msg += content
            print(f"FAIL  {f.name}  " + " / ".join(msg))
        else:
            print(f"OK    {f.name}")

    # 表の点検: 全フックが表にあり、表のフック名のファイルが存在する
    for t in ("hooks.md", "README.md"):
        path = KIT / t
        if not path.exists():
            continue
        rows = [l for l in read(path).splitlines() if l.startswith("|")]
        text = "\n".join(rows)
        absent = [h for h in hooks if f"`{h}" not in text]
        ghost = sorted({m for m in re.findall(r"`([a-z]+-hook\.md)", text) if m not in hooks})
        if absent or ghost:
            fail += 1
            msg = []
            if absent:
                msg.append("表に無い: " + "、".join(absent))
            if ghost:
                msg.append("存在しないフック: " + "、".join(ghost))
            print(f"FAIL  {t}  " + " / ".join(msg))
        else:
            print(f"OK    {t}（表と全フックが一致）")

    # hook-matrix.md
    mpath = KIT / "hook-matrix.md"
    if mpath.exists():
        lines = read(mpath).splitlines()
        header = next((l for l in lines if l.startswith("| 項目 |")), "")
        cols = [c.strip() for c in header.split("|") if c.strip() and c.strip() not in ("項目", "区分")]
        names = [h.replace("-hook.md", "") for h in hooks]
        absent = [n for n in names if n not in cols]
        ghost = [c for c in cols if c not in names]
        if absent or ghost:
            fail += 1
            msg = []
            if absent:
                msg.append("列に無い: " + "、".join(absent))
            if ghost:
                msg.append("存在しないフック: " + "、".join(ghost))
            print("FAIL  hook-matrix.md  " + " / ".join(msg))
        else:
            print("OK    hook-matrix.md（列と全フックが一致）")
        must_fail = []
        for row in lines:
            if not row.startswith("| ") or row.startswith("| 項目 |") or row.startswith("|---"):
                continue
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            kind, vals = cells[1], cells[2:]
            has_dash = "—" in vals
            if kind == "Must" and has_dash:
                must_fail.append(f"Must の行に — がある: {cells[0]}")
            elif kind == "Want" and not has_dash:
                print(f"NOTE  hook-matrix.md  全フックが ○ か △: Must に上げる候補: {cells[0]}")
        for m in must_fail:
            fail += 1
            print(f"FAIL  hook-matrix.md  {m}")
        except_line = next((l for l in lines if "字数の例外" in l), "")
        for f in hook_files:
            n = len(read(f))
            hook_name = f.name.replace("-hook.md", "")
            if n > 5000 and hook_name not in except_line:
                print(f"NOTE  {f.name}  {n} 字で目安（5,000 字）を超えている。畳む案を出す（hook-matrix.md の肥大化の抑制）")
    else:
        fail += 1
        print("FAIL  hook-matrix.md  ファイルが無い")

    # 他のファイルからの手順の参照: `X-hook.md` の手順「Y」の形で書き、Y が X の手順の見出しにあること
    steps = {f.name: step_titles(read(f)) for f in hook_files}
    ref_fail = []
    skip = {"improvements.md", "hook-common.md", "check-hook-outline.ps1", "check_hook_outline.py"}
    for p in sorted(KIT.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".ps1", ".py"):
            continue
        if p.name.endswith("-hook.md") or p.name in skip:
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            for m in REF_RE.finditer(line):
                if not m.group(1):
                    ref_fail.append(f"{p.name}:{n} 手順「{m.group(2)}」にフックのファイル名が無い")
                elif not has_step(steps.get(m.group(1), []), m.group(2)):
                    ref_fail.append(f"{p.name}:{n} {m.group(1)} に手順「{m.group(2)}」が無い")
    for n, line in enumerate(common_text.splitlines(), 1):
        m = re.match(r"^\| `([a-z]+)` \|.*手順「([^」]+)」", line)
        if m and not has_step(steps.get(f"{m.group(1)}-hook.md", []), m.group(2)):
            ref_fail.append(f"hook-common.md:{n} {m.group(1)}-hook.md に手順「{m.group(2)}」が無い")
    if ref_fail:
        fail += len(ref_fail)
        for r in ref_fail:
            print(f"FAIL  参照  {r}")
    else:
        print("OK    手順の参照（他のファイルから）")
    return fail


if __name__ == "__main__":
    sys.exit(main())
