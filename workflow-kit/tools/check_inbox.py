#!/usr/bin/env python3
"""check-inbox.ps1 の Python 版（標準ライブラリだけ。pwsh が無い環境、例: AI 作業部屋用）。

「ナレッジ化して」で作った inbox のメモを、機械的に点検する。
stock-hook.md の「書き方」「形式」のうち、機械的に確認できる項目だけを見る（手で確認する項目は、最後に一覧する）。

使い方: python check_inbox.py [--today YYYY-MM-DD] [--show-pass] [メモのパス...]
  パスを省略すると、exmem/inbox/ の今日の日付のメモ（README.md を除く）を点検する。
  既定は FAIL と WARN の行と、最後の RESULT の行だけ。--show-pass で PASS の行も出す。
終了コード = FAIL の数。WARN は数えない。

ps1 版との違い: ファイル名と tags の「英小文字」を、大文字を許さずに検査する（ps1 版は -match が大文字小文字を区別しないため通る）。
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

ORDER = ["Goal", "Principles", "Decisions", "Facts", "Gotchas", "Open Questions", "Next Actions"]
EMAIL_RE = (
    r"[\w.+-]+@(?!(?:[\w-]+\.)*(?:example\.(?:com|org|net)|local|invalid|test|example)(?![\w-]|\.\w))[\w-]+\.[\w.]+"
)


class Counter:
    def __init__(self, show_pass):
        self.fail = self.warn = self.passed = 0
        self.show_pass = show_pass

    def report(self, ok, name, level="FAIL", detail=""):
        if ok:
            self.passed += 1
            if self.show_pass:
                print(f"  PASS: {name}")
            return
        if level == "WARN":
            self.warn += 1
        else:
            self.fail += 1
        d = f" ({detail})" if detail else ""
        print(f"  {level}: {name}{d}")


def section(text, name, nxt):
    i = text.find(f"\n## {name}\n")
    if i < 0:
        return ""
    body = text[i + len(name) + 5:]
    if nxt:
        j = body.find(f"\n## {nxt}\n")
        if j >= 0:
            body = body[:j]
    return body.strip()


def count(text, pattern):
    return len(re.findall(pattern, text, re.M))


def check_file(path, today, c, spans):
    name = path.name
    print(f"== {name}")
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")

    c.report(bool(re.match(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+){1,4}\.md$", name)),
             "ファイル名が YYYY-MM-DD-<英単語2〜5語の kebab-case>.md", "FAIL", name)

    fm = re.match(r"---\n(.*?)\n---\n", raw, re.S)
    c.report(bool(fm), "frontmatter がある")
    front = fm.group(1) if fm else ""

    def get(k):
        m = re.search(rf"^{k}:\s*(.*)$", front, re.M)
        return m.group(1).strip() if m else ""

    c.report(get("type") == "inbox", "type が inbox")
    c.report(get("title") != "", "title がある")
    created = get("created")
    c.report(bool(re.match(r"^\d{4}-\d{2}-\d{2}$", created)), "created が YYYY-MM-DD")
    c.report(created == today, f"created が今日（{today}）", "WARN", created)
    m = re.search(r"tags:\n(.*?)(?=\n\S|\Z)", front, re.S)
    tag_block = m.group(1) if m else ""
    tags = re.findall(r"^\s+-\s+(\S+)\s*$", tag_block, re.M)
    c.report(3 <= len(tags) <= 6, "tags が3〜6個", "FAIL", f"{len(tags)}個")
    c.report(not [t for t in tags if not re.match(r"^[a-z0-9]+([-/][a-z0-9]+)*$", t)], "tags が英小文字の kebab-case（階層は /）")
    c.report(not [t for t in tags if t.lower() in ("inbox", "knowledge", "active", "superseded", "project", "index")], "tags に type / status の値を含まない")
    m = re.search(r"sources:\n(.*)", front, re.S)
    src_block = m.group(1) if m else ""
    srcs = re.findall(r"^\s+-\s+(.+)$", src_block, re.M)
    c.report(len(srcs) >= 1 and all(re.match(r'^.+ conversation ".+"$', s) for s in srcs), 'sources が `<AI名> conversation "<テーマ>"` の形')

    heads = re.findall(r"^## (.+?)\s*$", raw, re.M)
    c.report("|".join(heads) == "|".join(ORDER), "見出し7つが、定められた順番で、すべてある", "FAIL", ", ".join(heads))

    goal = section(raw, "Goal", "Principles")
    last_line = goal.split("\n")[-1]
    c.report(bool(re.search(r"^統合先の候補: .*((?:knowledge|lessons)/\S+?\.md|新規トピック)（キーワード: .+）", last_line)),
             "Goal の末尾が「統合先の候補: …（キーワード: …）」の行", "FAIL", last_line)

    # 「なし」は、見出しの直後に1語だけの行にする。補足が付くと、項目ありとみなされ、後続の点検が意味を成さない
    bad_none = {}
    for a, b in [("Principles", "Decisions"), ("Decisions", "Facts"), ("Facts", "Gotchas"), ("Gotchas", "Open Questions"),
                 ("Open Questions", "Next Actions"), ("Next Actions", "")]:
        if re.match(r"なし.+", section(raw, a, b), re.S):
            bad_none[a] = True
            c.report(False, f"{a} の「なし」が単独の行になっている", "FAIL", "「なし」は見出しの直後に1語だけで書く。補足は別の見出しか別のファイルに書く")
    if not bad_none:
        c.report(True, "「なし」と書いた見出しは、単独の行になっている")

    dec = section(raw, "Decisions", "Facts")
    if dec != "なし" and not bad_none.get("Decisions"):
        n = count(dec, r"^- \*\*")
        c.report(n >= 1, "Decisions が「なし」でなければ、項目がある")
        c.report(count(dec, r"^- \*\*.+\*\*（\d{4}-\d{2}-\d{2}") == n, "Decisions の全項目に日付がある")
        k = count(dec, r"^  - 根拠:")
        c.report(k == n, "Decisions の全項目に根拠がある", "FAIL", f"項目{n}、根拠{k}")
        k = count(dec, r"^  - 却下案:")
        c.report(k == n, "Decisions の全項目に却下案がある", "FAIL", f"項目{n}、却下案{k}")
        c.report(not re.search(r"(AI の提案[^\r\n]*未承認|^\s*- 提案[:：])", dec, re.M),
                 "Decisions に未承認の「AI の提案」が混ざっていない（提案は Open Questions へ）", "WARN")

    facts = section(raw, "Facts", "Gotchas")
    if facts != "なし" and not bad_none.get("Facts"):
        bad = [x for x in re.findall(r"^- .+$", facts, re.M) if not re.search(r"（確認: .+、根拠: .+）|（仮説", x)]
        detail = ""
        if bad:
            detail = bad[0][:40] + "…" if len(bad[0]) >= 40 else bad[0]
        c.report(not bad, "Facts の全項目に「（確認: …、根拠: …）」か「（仮説）」がある", "FAIL", detail)

    got = section(raw, "Gotchas", "Open Questions")
    if got != "なし" and not bad_none.get("Gotchas"):
        s = count(got, r"^- 状況:")
        cc = count(got, r"^  - 原因:")
        r = count(got, r"^  - 解決:")
        c.report(s >= 1 and s == cc and s == r, "Gotchas の全項目が「状況・原因・解決」の3行セット", "FAIL", f"状況{s}、原因{cc}、解決{r}")

    # メモをまたぐ重複の候補（Facts / Gotchas のインラインコード。判定は、ループの後）
    for span in re.findall(r"`([^`\n]+)`", facts + "\n" + got):
        if len(span) >= 8:
            spans.setdefault(span, set()).add(name)

    c.report(not re.search("この会話|上記|さっき|先ほど|前述", raw), "会話に依存する表現（この会話、上記、さっき、先ほど、前述）が無い")
    c.report(not re.search(r"(?i)[A-Za-z]:\\Users\\(?![<%$])[^\\\s`]+", raw) and not re.search(EMAIL_RE, raw),
             "共有したくない値（ユーザー名を含むパス、メールアドレス。example.com / *.local / *.invalid / *.test は例示用なので除く）が無い")
    c.report(not re.search(r"(?i)(token|secret|password|bearer)\s*[:=]\s*\S", raw), "秘匿値らしき行（token / secret / password / bearer の値）が無い")
    n_lines = len(raw.split("\n"))
    c.report(n_lines <= 150, "ファイル全体が150行以内（目安）", "WARN", f"{n_lines} 行")
    no_code = re.sub(r"`[^`\n]*`", "", raw)  # インラインコード内の <…> はコマンドの書式なので除く
    k = count(no_code, r"<[^>\n]+>")
    c.report(k == 0, "`<…>` が残っていない（インラインコード内は除く）", "WARN", f"{k} 件")


def main():
    ap = argparse.ArgumentParser(description="inbox のメモを機械的に点検する")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    ap.add_argument("--show-pass", action="store_true")
    args = ap.parse_args()

    paths = [Path(p) for a in args.paths for p in a.split(",") if p]
    if not paths:
        inbox = Path(__file__).resolve().parent.parent.parent / "exmem" / "inbox"
        paths = sorted(inbox.glob(f"{args.today}-*.md")) if inbox.is_dir() else []
    if not paths:
        print(f"点検するメモが無い（パス未指定で、{args.today} のメモも無い）")
        return 0

    c = Counter(args.show_pass)
    spans = {}
    for p in paths:
        check_file(p, args.today, c, spans)

    if len(paths) >= 2:
        print("== メモの間")
        dups = sorted((k, v) for k, v in spans.items() if len(v) >= 2)
        shown = "、".join("`" + k + "`（" + ", ".join(sorted(v)) + "）" for k, v in dups[:5])
        if len(dups) > 5:
            shown += f" ほか{len(dups) - 5}件"
        c.report(not dups, "同じインラインコードが、複数のメモの Facts / Gotchas に重複していない（候補があれば、同じ事実・落とし穴を重複して書いていないか確認する）", "WARN", shown)

    print()
    print(f"RESULT: files={len(paths)} pass={c.passed} fail={c.fail} warn={c.warn}")
    print("手で確認する項目: 1ファイル1テーマ / 同じ日の既存メモとの重複 / 作業ログ（何をいつやったか）の混在 / Decisions が、ユーザーの明示または承認した決定か / 確認した事実の根拠が本当か / 範囲を限定された場合は、その範囲だけか")
    return c.fail


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(c_exit if (c_exit := main()) is not None else 0)
