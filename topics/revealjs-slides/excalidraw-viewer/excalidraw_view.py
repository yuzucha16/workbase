"""`.excalidraw` を、ブラウザで見る自己完結の HTML にして開く（閲覧専用）。

room に依存しない。Windows でも WSL でも、Python 3 と Node.js (npm) があれば動く。

  python -I excalidraw_view.py a.excalidraw [b.excalidraw | ディレクトリ ...]
  python -I excalidraw_view.py a.excalidraw -o view.html --no-open
  python -I excalidraw_view.py --rebuild          # 閲覧用 JS を作り直す
  python -I excalidraw_view.py a.excalidraw --export svg,png -o out_dir   # 画面なしで SVG・PNG（Edge か Chrome が要る）

初回だけ、閲覧用 JS をキャッシュ (~/.cache/excalidraw-viewer) に作る（npm install と esbuild。
数分・約 40MB）。以後は npm を使わない。Excalidraw 本体・React・esbuild はすべて MIT。
ページ上の「SVG を保存」で、見た目のとおりの SVG を書き出せる。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".cache" / "excalidraw-viewer"
LINUX_BROWSER = False
SRC_FILES =("package.json", "viewer_entry.jsx", "build_viewer.mjs")


def is_wsl():
    return sys.platform.startswith("linux") and "microsoft" in Path("/proc/version").read_text().lower()


def run(cmd, cwd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def build():
    npm = shutil.which("npm")
    if not npm:
        sys.exit("npm が見つかりません。Node.js を入れてください。")
    src = CACHE / "src"
    src.mkdir(parents=True, exist_ok=True)
    for n in SRC_FILES:
        shutil.copy2(HERE / n, src / n)
    run([npm, "install", "--ignore-scripts", "--no-audit", "--no-fund"], src)
    node = shutil.which("node")
    run([node, "build_viewer.mjs", str(CACHE / "viewer.js")], src)
    fonts = src / "node_modules" / "@excalidraw" / "excalidraw" / "dist" / "prod" / "fonts"
    dst = CACHE / "fonts"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(fonts, dst)


def ensure_built(force):
    if force or not ((CACHE / "viewer.js").exists() and (CACHE / "fonts").exists()):
        build()


def collect(paths):
    found = []
    for p in map(Path, paths):
        if p.is_dir():
            found += sorted(p.rglob("*.excalidraw"))
        elif p.exists():
            found.append(p)
        else:
            sys.exit(f"見つかりません: {p}")
    if not found:
        sys.exit(".excalidraw がありません")
    return found


def to_uri(path):
    """ブラウザが読める file URI。WSL では Windows 側から見える形にする。"""
    path = Path(path).resolve()
    if is_wsl() and not LINUX_BROWSER:
        win = subprocess.run(["wslpath", "-m", str(path)], capture_output=True, text=True, check=True).stdout.strip()
        return "file:" + win if win.startswith("//") else "file:///" + win
    return path.as_uri()


def find_browser():
    for p in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ):
        if Path(p).exists():
            return p
    # room（WSL）の Playwright 版 Chromium（root が /opt/ms-playwright に入れる）
    root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or "/opt/ms-playwright")
    hits = sorted(root.glob("chromium-*/chrome-linux*/chrome")) if root.is_dir() else []
    if hits:
        return str(hits[-1])
    for n in ("msedge", "microsoft-edge", "google-chrome", "chromium", "chromium-browser", "chrome"):
        w = shutil.which(n)
        if w:
            return w
    sys.exit("Edge か Chrome が見つかりません（--export に必要）")


def export_files(files, outdir, kinds):
    """headless のブラウザで SVG を書き出す。png も要るときは、その SVG を撮る。"""
    import html as htmlmod
    import re
    import urllib.parse

    global LINUX_BROWSER
    browser = find_browser()
    LINUX_BROWSER = browser.startswith("/")  # WSL 内の Linux 版なら、Linux のパスの URI にする
    outdir = outdir.resolve()  # ブラウザの --screenshot は相対パスだと保存に失敗する
    outdir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="exv-"))
    page = tmp / "export.html"
    page.write_text(make_html(files, export=True), encoding="utf-8")
    # file:// のフォントを exportToSvg が取れるように許可する（自分で作った一時ページだけを開く）
    prof = ["--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--user-data-dir={tmp / 'prof'}"]
    if sys.platform.startswith("linux"):
        prof.append("--no-sandbox")  # room の Chromium は sandbox が使えない環境がある
    # フォント取得などの実時間の I/O が仮想時間と競合し、まれに結果が空になる（試験: 5 回に 2 回ほど）。数回やり直す。
    m = None
    for _ in range(6):
        r = subprocess.run([browser, *prof, "--virtual-time-budget=30000", "--dump-dom", to_uri(page)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r'<pre id="exv-out">(.*?)</pre>', r.stdout, re.S)
        if m:
            break
    if not m:
        sys.exit("書き出しに失敗しました（6 回やり直しても出力なし）。" + r.stderr[-400:])
    results = json.loads(htmlmod.unescape(m.group(1)))
    done = []
    for item in results:
        base = Path(item["name"]).stem
        if "error" in item:
            print("失敗:", item["name"], item["error"])
            continue
        svg = item["svg"]
        if not svg.startswith("<?xml"):
            svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg
        if "svg" in kinds:
            (outdir / f"{base}.svg").write_text(svg, encoding="utf-8")
            done.append(outdir / f"{base}.svg")
        if "png" in kinds:
            m2 = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
            w, h = (int(float(m2.group(1))), int(float(m2.group(2)))) if m2 else (1200, 800)
            # SVG を直接開くと Linux の Chromium でスクロールバーが出て空になるので、余白なしの HTML に入れて撮る
            sp = tmp / f"{base}.html"
            sp.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden}svg{display:block}</style>'
                          + svg.split("?>", 1)[-1], encoding="utf-8")
            png = outdir / f"{base}.png"
            # Linux の Chromium（headless=new）は、窓の高さから約 85px を引いた領域しか撮らないため、
            # Playwright 同梱の headless shell があればそれで撮る（窓の大きさがそのまま画像になる）。
            shells = sorted(Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or "/opt/ms-playwright")
                            .glob("chromium_headless_shell-*/chrome-headless-shell-linux*/chrome-headless-shell"))
            if shells:
                shot = [str(shells[-1]), "--no-sandbox", "--disable-gpu", f"--user-data-dir={tmp / 'prof2'}"]
            else:
                shot = [browser, *prof]
            subprocess.run([*shot, "--force-device-scale-factor=2", f"--window-size={w},{h}",
                            "--virtual-time-budget=10000", f"--screenshot={png}", to_uri(sp)],
                           capture_output=True)
            if png.exists():
                done.append(png)
            else:
                print("PNG を作れませんでした:", base)
    shutil.rmtree(tmp, ignore_errors=True)
    return done


def make_html(files, export=False):
    items = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            sys.exit(f"読めません: {f} ({e})")
        items.append({"name": f.name, "data": data})
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    asset = to_uri(CACHE) + "/"
    js = (CACHE / "viewer.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    return (
        "<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\">"
        "<title>Excalidraw viewer</title>"
        "<style>html,body,#root{margin:0;height:100%}</style></head><body><div id=\"root\"></div>"
        f"<script>window.EXCALIDRAW_ASSET_PATH={json.dumps(asset)};window.__EXV_FILES__={payload};"
        f"{'window.__EXV_EXPORT__=true;' if export else ''}</script>"
        f"<script>{js}</script></body></html>"
    )


def open_in_browser(html):
    if os.name == "nt":
        os.startfile(html)
    elif is_wsl():
        win = subprocess.run(["wslpath", "-w", str(html)], capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["explorer.exe", win])
    else:
        import webbrowser
        webbrowser.open(Path(html).as_uri())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help=".excalidraw ファイルかディレクトリ（再帰で探す）")
    ap.add_argument("-o", "--output", help="出力 HTML（既定: 一時ディレクトリ）。--export のときは出力ディレクトリ")
    ap.add_argument("--no-open", action="store_true", help="ブラウザで開かない")
    ap.add_argument("--rebuild", action="store_true", help="閲覧用 JS を作り直す")
    ap.add_argument("--export", metavar="KINDS", help="画面を出さず書き出す。svg、png、svg,png。出力先は -o（ディレクトリ。既定は入力と同じ場所）")
    a = ap.parse_args()
    ensure_built(a.rebuild)
    if not a.paths:
        if a.rebuild:
            return
        ap.error("paths が要ります")
    if a.export:
        kinds = {k.strip() for k in a.export.split(",")}
        if not kinds <= {"svg", "png"}:
            ap.error("--export は svg、png、svg,png のどれか")
        files = collect(a.paths)
        outdir = Path(a.output) if a.output else files[0].parent
        for p in export_files(files, outdir, kinds):
            print("出力:", p)
        return
    out = Path(a.output) if a.output else Path(tempfile.gettempdir()) / "excalidraw-view.html"
    out.write_text(make_html(collect(a.paths)), encoding="utf-8")
    print("出力:", out)
    if not a.no_open:
        open_in_browser(out)


if __name__ == "__main__":
    main()
