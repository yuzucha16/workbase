"""デジタル庁のアイコン素材（SVG, line 版）から、図解レイアウト用の symbol 定義を作る。

使い方: python -I build_dads_icons.py <designsystem-assets/icon/svg のパス>   # 素材から作り直す
        python -I build_dads_icons.py                                           # プレビューだけ作り直す
出力:   revealjs-diagram-icons-dads.html（同じディレクトリ。手で直さず作り直す）
        revealjs-diagram-icons-dads-preview.html（ブラウザで開いて見る一覧。素材の全アイコンと id）

素材: 「イラストレーション・アイコン素材」（デジタル庁）
      https://www.digital.go.jp/policies/servicedesign/designsystem/Illustration_Icons
      商用利用可。編集・加工して使うときは出典と加工内容を明示する（利用規約 1-2）。
加工: 塗りの色 #1A1A1C を currentColor に置換し、clip-path を除いた（形は変えていない）。
      サイズは 24px の viewBox のみ使う。symbol の id は i-dads-<素材名>（_line を除く）。
"""
import re
import sys
from pathlib import Path

# 今のレイアウト（札のアイコン・手順・注釈）に合うものだけを選ぶ。意味は資料全体で固定する。
PICK = {
    "add": "追加・新規",
    "application": "アプリ・画面",
    "arrow_right": "流れ・次へ",
    "arrow_down": "下へ・展開",
    "attention": "注意",
    "authentication": "認証",
    "certification": "証明・認定",
    "complete": "完了",
    "copy": "複製・コピー",
    "documents": "文書・ファイル",
    "download": "取得・ダウンロード",
    "e_application": "電子申請・手続き",
    "help": "ヘルプ・疑問",
    "history": "履歴",
    "information": "情報・補足",
    "inbox": "受信・入力",
    "laws": "規則・法令",
    "mailing": "メール・送付",
    "me": "自分・ユーザー",
    "menu": "メニュー・一覧",
    "new_window": "外部リンク",
    "notification": "通知",
    "password": "パスワード・鍵",
    "printer": "印刷・出力",
    "privacy_protection": "プライバシー保護",
    "search": "検索",
    "smartphone": "スマートフォン",
    "specialist": "担当者・専門家",
    "transactions": "やり取り・取引",
    "update": "更新",
    "work": "仕事・業務",
    "code_reader": "コード読み取り",
}


def symbol(name, svg):
    body = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.S)
    body = re.sub(r"</?svg[^>]*>|</?g[^>]*>", "", body)
    body = body.replace('fill="#1A1A1C"', 'fill="currentColor"')
    body = re.sub(r"\s+", " ", body).strip()
    return f'<symbol id="i-{name}" viewBox="0 0 24 24">{body}</symbol>'


def preview():
    here = Path(__file__).parent
    dads = (here / "revealjs-diagram-icons-dads.html").read_text(encoding="utf-8")

    def section(title, text):
        ids = re.findall(r'<symbol id="i-([^"]+)"', text)
        cells = "".join(
            f'<div class="c"><svg viewBox="0 0 24 24" width="48" height="48"><use href="#i-{i}"/></svg><br>{i}</div>'
            for i in ids)
        return f"<h2>{title}（{len(ids)}）</h2><div class=\"g\">{cells}</div>"

    page = ("<!doctype html><meta charset=\"utf-8\"><title>DADS アイコン一覧</title>"
            "<style>body{font-family:sans-serif;margin:24px;color:#1a1a1a}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,120px);gap:12px}"
            ".c{text-align:center;font-size:12px;border:1px solid #ddd;padding:10px 4px;border-radius:6px}"
            "svg{color:#0017c1}</style>"
            + dads
            + "<h1>デジタル庁のアイコン（札の icon に id を書く）</h1>"
            + section("デジタル庁の素材（line 版）", dads))
    (here / "revealjs-diagram-icons-dads-preview.html").write_text(page, encoding="utf-8", newline="\n")


def main(src):
    syms = []
    for name in PICK:
        syms.append(symbol(name, (Path(src) / f"{name}_line.svg").read_text(encoding="utf-8")))
    out = ('<!-- 「イラストレーション・アイコン素材」（デジタル庁）を元に、色を currentColor に変えて symbol 化。'
           'https://www.digital.go.jp/policies/servicedesign/designsystem/Illustration_Icons -->\n'
           '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
           + "".join(syms) + "</defs></svg>\n")
    Path(__file__).with_name("revealjs-diagram-icons-dads.html").write_text(out, encoding="utf-8", newline="\n")
    print(len(syms), "icons")
    preview()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        preview()
