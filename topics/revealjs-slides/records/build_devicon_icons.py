"""Devicon のアイコン（SVG）から、図解レイアウト用の symbol 定義を作る。ソフトウェア開発系（言語・基盤・ツール）のストック。

使い方: python -I build_devicon_icons.py <devicon の icons ディレクトリ>   # 素材から作り直す
出力:   revealjs-diagram-icons-devicon.html（同じディレクトリ。手で直さず作り直す）
        revealjs-diagram-icons-devicon-preview.html（ブラウザで開いて見る一覧と id）
        devicon-LICENSE.txt は素材の LICENSE をそのまま置く（再配布の条件: 著作権表示と許諾文を同梱する）。

素材: Devicon https://devicon.dev （MIT License。Copyright (c) 2015 konpa。devicon-LICENSE.txt）
      版: コミット 32fe1d3（2026-11-06 に取得。GitHub の devicons/devicon の master、icons/<名前>/<名前>-<種類>.svg）
      各ロゴの商標は各社のもの。ロゴを使うことは、その製品との提携・推奨を示さない。
加工: 単色化した。svg の外枠を除き、塗り（元は各社の色）を捨てて <g fill="currentColor"> に統一した（形は変えていない）。
      Lucide（線）と違い、塗りの面で描く。色は CSS の color で変わる（Lucide と同じ）。
      種類は plain（単色の輪郭）だけ使う（original は多色で単色にすると崩れる。line は線が細く薄い）。
      symbol の id は i-dv-<名前>（自作・DADS・Lucide の id と衝突しない）。viewBox は 0 0 128 128。
取得: 素材は新しい空のディレクトリへ置く（信頼できない入力として扱う）。plain が無い名前は飛ばして一覧に出す。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
G_OPEN = '<g fill="currentColor">'
KINDS = ("plain",)  # line は線が細く単色にすると薄いので使わない（2026-11-06 ユーザーの決定）

# プレビューの区分（意味は資料全体で固定する）。数は半分ほどに絞った（使いそうな上位。ユーザーが 11-06 に判断を任せた）。
# 足すときは名前を足して作り直す。
GROUPS = {
    "言語": "python javascript typescript java csharp cplusplus go ruby php swift kotlin bash powershell",
    "Web": "html5 css3 nodejs vuejs nextjs django",
    "Git・CI": "git gitlab githubactions",
    "OS": "linux ubuntu debian",
    "クラウド・インフラ": "docker kubernetes terraform ansible amazonwebservices azure googlecloud",
    "データベース": "postgresql sqlite mongodb redis",
    "ビルド・テスト": "npm webpack vitejs eslint jest pytest",
    "エディタ・IDE": "vscode vim intellij",
    "データ・AI": "pandas numpy claude",
    "ファイル形式": "yaml",
}
PICK = " ".join(GROUPS.values()).split()


def symbol(name, svg):
    body = re.sub(r"<svg[^>]*>|</svg>", "", svg, flags=re.S)
    body = re.sub(r'\s+fill="(?!none")[^"]*"', "", body)  # 元の色を捨てる（fill="none" は残す）
    body = re.sub(r"\s+", " ", body).strip()
    body = re.sub(r"\s*/>", "/>", body)
    return f'<symbol id="i-dv-{name}" viewBox="0 0 128 128">{G_OPEN}{body}</g></symbol>'


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    syms, got, missing = [], [], []
    for name in dict.fromkeys(PICK):
        for kind in KINDS:
            f = src / name / f"{name}-{kind}.svg"
            if f.exists():
                break
        else:
            missing.append(name)
            continue
        svg = f.read_text(encoding="utf-8")
        # 素材は信頼しない。図形（path/circle/rect/polygon/ellipse/g）以外、描画を変える属性が混じっていたら止める
        tags = set(re.findall(r"<([a-zA-Z][\w:-]*)", svg)) - {"svg", "path", "circle", "rect", "polygon", "ellipse", "g", "polyline", "line"}
        if tags or re.search(r"\bon\w+=|href=|\bstyle=|\bclass=|\bstroke=|\bopacity=|\btransform=", svg, re.I):
            raise SystemExit(f"想定外の要素・属性があります: {f.name} {sorted(tags)}")
        if 'viewBox="0 0 128 128"' not in svg:
            raise SystemExit(f"viewBox が 128 角ではありません: {f.name}")
        syms.append(symbol(name, svg))
        got.append((name, kind))
    head = ("<!-- Devicon（MIT License。Copyright (c) 2015 konpa。https://devicon.dev）のロゴを元に、塗りを単色（currentColor）にして symbol 化。"
            "コミット 32fe1d3。ライセンスは devicon-LICENSE.txt。ロゴの商標は各社のもの -->\n")
    defs = head + '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(syms) + "</defs></svg>\n"
    (HERE / "revealjs-diagram-icons-devicon.html").write_text(defs, encoding="utf-8", newline="\n")
    lic = src.parent / "LICENSE"
    if lic.exists():
        (HERE / "devicon-LICENSE.txt").write_text(lic.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    have = {n for n, _ in got}
    kind_of = dict(got)
    sections = [(t, [n for n in ns.split() if n in have]) for t, ns in GROUPS.items()]
    cells = lambda ns: "".join(
        f'<div class="c"><svg viewBox="0 0 128 128" width="40" height="40"><use href="#i-dv-{n}"/></svg><br>dv-{n}'
        f'{"<br>(line)" if kind_of[n] == "line" else ""}</div>' for n in ns)
    page = ('<!doctype html><meta charset="utf-8"><title>Devicon アイコン一覧</title>'
            "<style>body{font-family:sans-serif;margin:24px;color:#1a1a1a}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,130px);gap:10px}"
            ".c{text-align:center;font-size:11px;border:1px solid #ddd;padding:8px 2px;border-radius:6px}"
            "svg{color:#0017c1}</style>" + defs
            + f"<h1>Devicon アイコン（{len(got)}）</h1><p>使い方: 札の icon に <code>dv-名前</code> のように書く。単色。</p>"
            + "".join(f"<h2>{t}（{len(ns)}）</h2><div class=\"g\">{cells(ns)}</div>" for t, ns in sections if ns))
    (HERE / "revealjs-diagram-icons-devicon-preview.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"{len(got)} 種を出力しました。素材に無い名前: {' '.join(missing) or 'なし'}")


if __name__ == "__main__":
    main()
