"""`.excalidraw` を、ブラウザで見る自己完結の HTML にして開く（閲覧専用）。

room に依存しない。Windows でも WSL でも、Python 3 と Node.js (npm) があれば動く。

  python -I excalidraw_view.py a.excalidraw [b.excalidraw | ディレクトリ ...]
  python -I excalidraw_view.py a.excalidraw -o view.html --no-open
  python -I excalidraw_view.py --rebuild          # 閲覧用 JS を作り直す

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
SRC_FILES = ("package.json", "viewer_entry.jsx", "build_viewer.mjs")


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
    if is_wsl():
        win = subprocess.run(["wslpath", "-m", str(path)], capture_output=True, text=True, check=True).stdout.strip()
        return "file:" + win if win.startswith("//") else "file:///" + win
    return path.as_uri()


def make_html(files):
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
        f"<script>window.EXCALIDRAW_ASSET_PATH={json.dumps(asset)};window.__EXV_FILES__={payload};</script>"
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
    ap.add_argument("-o", "--output", help="出力 HTML（既定: 一時ディレクトリ）")
    ap.add_argument("--no-open", action="store_true", help="ブラウザで開かない")
    ap.add_argument("--rebuild", action="store_true", help="閲覧用 JS を作り直す")
    a = ap.parse_args()
    ensure_built(a.rebuild)
    if not a.paths:
        if a.rebuild:
            return
        ap.error("paths が要ります")
    out = Path(a.output) if a.output else Path(tempfile.gettempdir()) / "excalidraw-view.html"
    out.write_text(make_html(collect(a.paths)), encoding="utf-8")
    print("出力:", out)
    if not a.no_open:
        open_in_browser(out)


if __name__ == "__main__":
    main()
