#!/usr/bin/env python3
"""Windows で実行する Python スクリプト（.py と、それを呼ぶ起動用 .bat）を、実行せずに点検する。

script-guide.md の「Windows で実行するスクリプト（Python）」の規約のうち、機械的に確認できる項目を見る。
標準ライブラリだけで動く（AI 作業部屋でも Windows でも同じ結果になる）。check-ps1.ps1 の Python 版にあたる。

使い方: python check_py.py [--run-tests] [--show-pass] パス...
  パスはファイルかディレクトリ（ディレクトリは中の .py .bat .cmd を再帰で集める）。
  --run-tests: 見つけた test*.py を、置き場ごとに unittest で実行する。
  既定は FAIL と WARN の行と、最後の RESULT の行だけ。--show-pass で PASS の行も出す。
終了コード = FAIL の数。WARN は数えない。

見る項目: UTF-8（BOM なし）、改行の混在、構文（ast）、ruff（あれば。無ければ WARN）、
起動用 .bat が 3 行の型（@echo off / uv run --script "%~dp0<名前>.py" [%*] / pause）で、ASCII・CRLF・BOM なし、呼び先の .py が同じ場所にある、
束ねる .py が --log のときだけ ai/work/<名前>.log に出すログ機能（既定は出さない）を持つこと、bat の名前が工程名（run / verify / release）で、verify.py が毎回 verify-result.json を出す機能を持つこと（どちらも WARN）。
見ないもの（人が Windows で実行して確かめる）: Windows 固有の動作（COM、レジストリ、パスと権限）、実行先の uv と依存の取得。
pwsh を呼ぶ起動用 .bat は対象外（check-ps1.ps1 の担当）。
"""
import argparse
import ast
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
EXTENSIONS = {".py", ".bat", ".cmd"}
LAUNCHER_RE = re.compile(r'^uv run --script "%~dp0(?P<n>[^"\\/%]+\.py)"( %\*)?$', re.IGNORECASE)
PWSH_RE = re.compile(r"^pwsh\b.*\.ps1", re.IGNORECASE)


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
        print(f"  {level}: {name}" + (f" ({detail})" if detail else ""))


def collect(paths, c):
    files = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            c.report(False, f"パスが無い ({p})")
        elif path.is_dir():
            files += sorted(
                f for f in path.rglob("*")
                if f.is_file() and f.suffix.lower() in EXTENSIONS and not (SKIP_DIRS & set(f.parts))
            )
        else:
            files.append(path)
    return files


def check_launcher(f, c):
    raw = f.read_bytes()
    text = raw.decode("ascii", errors="replace")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if any(PWSH_RE.match(l) for l in lines):
        print("  (pwsh を呼ぶ bat は check-ps1.ps1 の担当。省略)")
        return
    c.report(not raw.startswith(b"\xef\xbb\xbf"), "起動用 bat に BOM が無い")
    c.report(all(b < 128 for b in raw), "起動用 bat 全体が ASCII（日本語のコメントや表示は書かない）")
    c.report(not re.search(rb"(?<!\r)\n", raw), "起動用 bat の改行が CRLF（LF だけの行がある）")
    target, shape = None, True
    for l in lines:
        if l.lower() in ("@echo off", "pause"):
            continue
        m = LAUNCHER_RE.match(l)
        if m and not target:
            target = m.group("n")
            continue
        shape = False
    c.report(shape and bool(target), '起動用 bat が 3 行の型だけ（@echo off / uv run --script "%~dp0<名前>.py" / pause）。ロジックは py に書く')
    if target:
        tp = f.parent / target
        c.report(tp.exists(), f"起動用 bat の呼び先 {target} が同じ場所にある")
        if tp.exists():
            body = tp.read_text(encoding="utf-8", errors="replace")
            ok = Path(target).stem == "release" or "--log" in body and "'work'" in body.replace('"', "'") and "argparse" in body
            c.report(ok, f"束ねる {target} が --log のときのログ出力の機能を持つ（argparse の --log、'work'）", "WARN")
            if Path(target).stem == "verify":
                c.report("verify-result.json" in body, f"束ねる {target} が毎回 verify-result.json を出す機能を持つ", "WARN")
        c.report(f.stem in ("run", "verify", "release"), f"起動用 bat の名前 {f.name} が工程名（run / verify / release）", "WARN")
    c.report(bool(lines) and lines[-1].lower() == "pause", "起動用 bat の最後が pause（終わっても画面が閉じない）")


def check_python(f, c, ruff):
    raw = f.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        c.report(False, "文字コードが UTF-8", detail="cp932 や UTF-16 の可能性。UTF-8 で保存し直す")
        return
    c.report(True, "文字コードが UTF-8")
    c.report(not raw.startswith(b"\xef\xbb\xbf"), "BOM が無い", "WARN")
    crlf, lf = text.count("\r\n"), len(re.findall(r"(?<!\r)\n", text))
    c.report(not (crlf and lf), "改行が混在していない", "WARN", f"CRLF {crlf} 行、LF {lf} 行")
    try:
        ast.parse(text, filename=str(f))
    except SyntaxError as e:
        c.report(False, "構文エラー", detail=f"行 {e.lineno}: {e.msg}")
        return
    c.report(True, "構文が通る")
    if ruff:
        r = subprocess.run([ruff, "check", "--no-cache", "--output-format", "concise", str(f)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        found = [l for l in r.stdout.splitlines() if re.search(r":\d+:\d+:", l)]
        for l in found:
            c.report(False, "ruff", "WARN", l)
        if not found:
            c.report(True, "ruff の指摘が無い")


def run_tests(files, c):
    dirs = sorted({f.parent for f in files if f.suffix == ".py" and re.match(r"test.*\.py$", f.name)})
    print("== unittest")
    if not dirs:
        c.report(False, "test*.py が見つからない", "WARN")
        return
    for d in dirs:
        r = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", str(d), "-p", "test*.py"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = (r.stderr.strip().splitlines() or [""])[-1]
        c.report(r.returncode == 0, f"unittest が全件合格 ({d.name}/)", detail=tail)
        if r.returncode != 0:
            print("\n".join(r.stderr.strip().splitlines()[-15:]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--run-tests", action="store_true")
    ap.add_argument("--show-pass", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(errors="replace")
    c = Counter(a.show_pass)
    files = collect(a.paths, c)
    if not files and not c.fail:
        print("点検するファイルが無い（.py .bat .cmd）")
        return 0
    ruff = shutil.which("ruff")
    if not ruff and any(f.suffix == ".py" for f in files):
        c.report(False, "ruff が無い。未定義の名前や未使用の import の検査を省いた", "WARN")
    for f in files:
        print(f"== {f}")
        if f.suffix.lower() == ".py":
            check_python(f, c, ruff)
        else:
            check_launcher(f, c)
    if a.run_tests:
        run_tests(files, c)
    print(f"RESULT: files={len(files)} pass={c.passed} fail={c.fail} warn={c.warn}")
    return c.fail


if __name__ == "__main__":
    sys.exit(main())
