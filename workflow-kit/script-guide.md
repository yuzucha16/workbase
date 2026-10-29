# スクリプトの作り方・動かし方

スクリプトや変換を作る・動かすときの、全 type 共通（`dev` `inv` とも）の規約。`dev-deliverable-guide.md` から移した（2026-10-24、ユーザーの承認。本文は原文のまま。節の見出しを `##` のまま移した）。部屋で完結させる方針、言語の選び方（Python → ps1 → bat）、Windows で実行するスクリプトの型を持つ。**スクリプトを書く・動かすときに読む**（`dev` の成果物の構成、文書、テスト、チェックは `dev-deliverable-guide.md`）。

## 実行の方針: 部屋で完結させ、Windows 依存部を小さくする

スクリプトや変換を作る・動かすときの方針（2026-10-21 のユーザーの依頼。全 type 共通）。

1. **部屋で完結できるなら、すべて部屋（WSL）で実行する。** 作って終わりにせず、部屋で実行して結果を確かめる。人に回すのは、部屋で実行できない部分だけ。
2. **Excel・COM などの Windows 依存部は、できるだけ小さくし、人の手数を少なくする。**

**言語の選び方（2026-10-21 のユーザーの依頼。AI は「Python でよいか」「ps1 がよいか」とユーザーに聞かず、この順で自分で決める）**: Windows 依存を減らすため、優先順位は **Python → ps1 → bat**。

1. **Python**（既定。2026-10-21 のユーザーの決定で、Windows 依存の薄い層も Python にした）。部屋で実行できる処理に加え、Windows 依存の操作（Excel の COM は `pywin32`、レジストリは `winreg`、アプリの起動は `subprocess`）も Python で書く。実行は `uv run --script`（Windows の実行先に Python と uv があることは確認済み）。Python の版と呼び方は、下の「Python の版と呼び方」に従う。
2. **ps1**。実行先に Python（uv）が無いと分かっているとき、または PowerShell の cmdlet でしか操作できない Windows 依存の操作のときだけ。薄い層にする。
3. **bat**。`uv run`（または ps1）を起動するだけの 3 行（下の「Windows で実行するスクリプト」）。ロジックは書かない。

上の順で決められない事情（実行先の制約が不明など）があるときだけ、ユーザーに聞く。決めたら、報告に使った言語と理由を 1 行書く。

部屋で使える道具（確認: 2026-10-21、実機の部屋 Ubuntu 26.04.1。`room init` が入れる。AI は入れ足さない）:

| 道具 | 版 | 注意 |
|---|---|---|
| Python | 正本の版（`workflow-kit/room/.python-version`。今は 3.13.14）を uv で入れ、`python3` で呼ぶ（案。`room init` の段は未実装）。システムの 3.14.4 は apt の道具が使うので上書きしない | `pip` は無い。依存が要るときは `uv`（`uv run --script`、`uv add`）で版を固定する。外部の取得はネットワークと証明書に依存する（未確認）。テストは標準ライブラリの `unittest` |
| uv | 0.13.4 | Python の版・依存・仮想環境の管理 |
| git | 2.53.0 | 部屋のローカルの git（`room-context.md`） |
| PowerShell 7 | 7.6.7（Linux 版）+ PSScriptAnalyzer 1.25.0 + Pester 5.9.1 | 下の節の点検とテスト用。Windows 固有の動作は再現しない |
| Node.js | 24 | |
| LibreOffice / pandoc / Chromium（`room-chrome`）/ mermaid-cli（`room-mmdc`） | 26.2 / 3.7 / — / 12.0.0 | xlsx・docx・pptx の変換と再計算、Markdown の HTML 化、mermaid の画像化、HTML の PDF 化 |

切り分けの手順:

1. 処理を工程に分け、工程ごとに「部屋で実行できるか」を判定する。判定の目安は、Windows のアプリ（Excel の VBA 実行、ピボットの作成、COM）、レジストリ、Windows のパスと権限、実行先の環境（インストール、環境変数）に触れるかどうか。触れなければ部屋で完結する。
2. **Excel は、LibreOffice で足りないかを先に確かめる。** xlsx の読み書き、変換、再計算は、部屋で完結できる。Windows に回すのは、VBA の実行確認、ピボットの作成、見た目の完全な再現だけ（LibreOffice は Excel と結果が違う）。
3. 部屋で完結する工程（判定、変換、検証、整形、ファイルの生成）は、部屋で Python（または部屋の道具）で書き、**部屋で実行してテストする**。部屋の Python と同じ言語で書くので、薄い層との境目は「Windows 依存の操作を、小さな関数に包むかどうか」で決まる。
4. Windows 依存の工程だけを、**薄い層**として切り出す（成果物の中の専用ディレクトリ、例: `windows/`）。薄い層は、部屋が作った入力ファイルを読み、Windows 依存の操作だけを行い、結果をファイルに書く。判定や変換を持たない。部屋で実行できないので、検証項目に「人が実行」と書き、報告の「実環境で未確認の点」に書く。
5. **人の手数を減らす。** 人が打つのは 1 コマンドにする（下の「束ねる ps1」と起動用 bat）。実行の前提（Excel を閉じる、入力ファイルの有無、実行場所）は、束ねる側が先に確認して、満たされなければ、何をすればよいかを表示して止まる。人が覚える手順を、スクリプトの外に残さない。結果は、人が見るべき要約（成否、件数、出力の場所）を最後に表示する。

## Windows で実行するスクリプト（Python が既定、ps1 は例外。起動用 bat）

上の方針で残った、**Windows 依存の薄い層**を、人が Windows で実行するときの規約（2026-10-21 のユーザーの決定。全 type 共通。Python を既定にしたのも同日のユーザーの決定）。bat は、束ねる役を 1 回で実行したいという人の手間を省くための入口にすぎず、bat 自体に価値は無い。bat の失敗（日本語の文字化け、LF でラベルが見つからない、`call` 忘れ）は、bat にロジックを書くから起きる。

### Python の薄い層（既定）

**Python の版と呼び方**（2026-10-29 のユーザーの決定。`docs/decisions.md`）: Python は版に敏感なので、uv 管理の版を正本にして、トラブル時の切り分けを減らす。

| 場所 | 呼び方 | 版 |
|---|---|---|
| Windows・依存つき | `uv run --script` | 正本（`room/.python-version`） |
| Windows・room | `uv run room.py` | 正本 |
| Windows・uv が止まったとき | `python`（標準ライブラリだけの .py） | 保証しない |
| WSL（部屋） | `python3` | 正本（`room init` が uv で入れる。案） |
| PC2・クラウドの AI | `python -I` | 対象外 |

- 各 `.py` の `requires-python` は `==3.13.*`（正本の系列）にそろえる。下限指定（`>=`）だと、uv が新しい版を選んで正本とずれる。
- 古い版が要るモジュールを使うスクリプトだけ、`requires-python` に別の版を書き、理由を 1 行添える（スクリプトごとに選ばれるので、全体は巻き込まない）。
- 標準ライブラリだけの .py に、版の厳密さは求めない。

- **個別の処理は `<名前>.py`（snake_case）、それらを順に呼ぶ束ねる役を 1 本（動作確認なら `verify.py`。名前は下の「人が叩くスクリプトの名前」）にする。** 失敗したら止まる、最後に結果を出す、ログを 1 か所に出す、を束ねる側に持たせる。人は `uv run --script verify.py` を 1 回打つだけにする。判定・変換・検証は薄い層に置かない（上の「切り分けの手順」の 4）。
- **依存は、各 `.py` の先頭の `# /// script`（PEP 723）に書く**（`requires-python`、`dependencies`。Excel の COM なら `pywin32`）。実行は `uv run --script`。束ねる役が個別の処理を呼ぶときも `uv run --script` で呼ぶ（自分の Python には、呼び先の依存が無い）。
- **bat は、起動用の 3 行だけ許す**。ロジックは書かない。型は固定（`%*` は引数を渡したいときだけ。全体 ASCII、CRLF、BOM なし、`pause` を最後に必ず置く）:

  ```bat
  @echo off
  uv run --script "%~dp0verify.py" %*
  pause
  ```
- **束ねる役に、ログ出力の機能を持たせる。ただし既定では出さない**（ps1 と同じ決定。理由と実データの注意は、下の ps1 の節）。`--log` を付けると、Project の `ai/work/<束ねる役の名前>.log` の 1 本に出す。`--log-dir <パス>` なら、その場所に出す。個別の処理は、ログを作らない。型（動作確認済み: Windows の Python 3.13 と uv 0.13.0。既定ではログが出ない、`--log` で `ai/work/` に出る、失敗した工程・終了コード・スタックがログに残り終了コードが 1 になる。bat 経由の `--log` も同じ）:

  ```python
  # /// script
  # requires-python = "==3.13.*"
  # dependencies = []
  # ///
  """動作確認の束ねる役。前提を確かめ、工程を順に実行し、目視の項目を聞き、結果を ai/work/verify-result.json に毎回出す。--log のときだけ全文ログも出す。"""
  import argparse
  import hashlib
  import json
  import locale
  import os
  import platform
  import shutil
  import subprocess
  import sys
  import time
  import traceback
  from pathlib import Path

  NAME = "demo"                                   # 成果物名（ai/out/<NAME>/）。実際の名前に変える
  STEPS = ["step1.py", "step2.py"]                # 実際の工程名に変える
  CHECKS = ["画面の見た目が仕様どおりか"]           # 目視の項目。無ければ空にする
  NEEDS = ["uv"]                                  # 前提のコマンド。実際に変える
  HERE = Path(__file__).resolve().parent
  HOME = str(Path.home())
  SKIP_HASH = {"release.json"}                    # release が書くファイルはハッシュに入れない


  def find_ai() -> Path | None:
      for d in (HERE, *HERE.parents):
          if d.name == "ai" and (d / "work").is_dir():
              return d
      return None


  def scrub(s: str) -> str:
      """ユーザー名を含むホームのパスを伏せる。"""
      return s.replace(HOME, "%USERPROFILE%") if HOME else s


  def tree_hash(root: Path) -> str:
      h = hashlib.sha256()
      for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name not in SKIP_HASH and "__pycache__" not in p.parts):
          h.update(f.relative_to(root).as_posix().encode())
          h.update(f.read_bytes())
      return h.hexdigest()[:16]


  def env_facts() -> dict:
      uv = shutil.which("uv")
      ver = subprocess.run([uv, "--version"], capture_output=True, text=True).stdout.strip() if uv else None
      return {"os": platform.platform(), "python": platform.python_version(), "uv": ver,
              "preferred_encoding": locale.getpreferredencoding(False), "stdout_encoding": sys.stdout.encoding,
              "PYTHONUTF8": os.environ.get("PYTHONUTF8")}


  class Tee:
      def __init__(self, *streams):
          self.streams = streams

      def write(self, s):
          for st in self.streams:
              st.write(s)
          return len(s)

      def flush(self):
          for st in self.streams:
              st.flush()


  def run(result: dict) -> int:
      try:
          missing = [c for c in NEEDS if not shutil.which(c)]
          if missing:
              print(f"[STOP] 前提が足りない: {', '.join(missing)}（入れてから、もう一度実行する）")
              result["failure"] = {"type": "Preflight", "where": ",".join(missing)}
              return 1
          for step in STEPS:
              print(f"[STEP] {step}", flush=True)
              t0 = time.time()
              p = subprocess.Popen(["uv", "run", "--script", str(HERE / step)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONUTF8": "1"})
              for line in p.stdout:
                  print(line, end="")
              rc = p.wait()
              result["steps"].append({"name": step, "rc": rc, "sec": round(time.time() - t0, 1)})
              if rc != 0:
                  raise RuntimeError(f"{step} が終了コード {rc} で終わった")
          for item in CHECKS:
              if not sys.stdin.isatty():
                  result["manual"].append({"item": item, "ok": None, "note": "対話できないので未確認"})
                  continue
              ans = input(f"[CHECK] {item}  (y/n、ひとこと): ").strip()
              result["manual"].append({"item": item, "ok": ans[:1].lower() == "y", "note": ans[1:].strip()})
          bad = [m["item"] for m in result["manual"] if m["ok"] is not True]
          if bad:
              print(f"[NG] 目視が未確認または不合格: {', '.join(bad)}")
              return 1
          print("[OK] すべて完了")
          return 0
      except Exception as e:
          print(f"[ERROR] {e}")
          traceback.print_exc(file=sys.stdout)
          tb = traceback.extract_tb(e.__traceback__)[-1]
          result["failure"] = {"type": type(e).__name__, "where": f"{Path(tb.filename).name}:{tb.lineno}"}
          return 1


  def main() -> int:
      ap = argparse.ArgumentParser()
      ap.add_argument("--log", action="store_true", help="ai/work/<名前>.log に全文を出す")
      ap.add_argument("--log-dir", type=Path, help="この場所に全文ログを出す（--log は不要）")
      a = ap.parse_args()
      sys.stdout.reconfigure(errors="replace")
      ai = find_ai()
      work = (ai / "work") if ai else HERE / "work"          # Project の外（配布先）で実行したとき
      out = (ai / "out" / NAME) if ai else HERE.parent
      result = {"tool": "verify", "env": env_facts(), "steps": [], "manual": [], "failure": None}
      log, real = None, sys.stdout
      if a.log or a.log_dir:                                  # 既定では全文ログを出さない
          lp = (a.log_dir or work) / f"{Path(__file__).stem}.log"
          lp.parent.mkdir(parents=True, exist_ok=True)
          log = open(lp, "w", encoding="utf-8")
          sys.stdout = Tee(real, log)
          print(f"[LOG] {lp}")
      try:
          rc = run(result)
      finally:
          sys.stdout = real
          if log:
              log.close()
      result["ok"] = rc == 0
      result["out_hash"] = tree_hash(out) if out.is_dir() else None
      result["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
      work.mkdir(parents=True, exist_ok=True)                 # 結果ファイルは毎回出す（業務の値は入れない）
      (work / "verify-result.json").write_text(scrub(json.dumps(result, ensure_ascii=False, indent=1)), encoding="utf-8")
      print(f"[RESULT] {scrub(str(work / 'verify-result.json'))}")
      return rc


  if __name__ == "__main__":
      sys.exit(main())
  ```

  Python 版のログには、ps1 の transcript のようなヘッダー（ユーザー名とマシン名）は入らない。ただし、パス（ユーザー名を含みうる）とエラー文は入るので、`ai/` の中に出るログが部屋の AI から読める点は同じ（実データの扱いは ps1 の節）。
- **Windows 固有の操作（COM、レジストリ）は、小さな関数に包む。** `pywin32` は Windows 専用で、部屋では import できない。関数の中で import するか、`sys.platform` で分け、部屋のテストでは `unittest.mock.patch` で関数ごと差し替える。差し替えない本物の動作は、人が Windows で実行する層に回し、検証項目に「人が実行」と書く。
- **部屋の中で、作った直後に静的チェッカーを実行する**（標準ライブラリだけ。実行はしない）:

  ```
  python3 ~/shared/workflow-kit/tools/check_py.py <成果物のディレクトリ>
  python3 ~/shared/workflow-kit/tools/check_py.py --run-tests <成果物のディレクトリ>   # test*.py を unittest で実行する
  ```

  FAIL は直してから人に渡す。WARN は理由を見て判断する。終了コードは FAIL の数。見るもの: UTF-8、改行の混在、構文、起動用 bat の型（上の 3 行、呼び先の存在）、束ねる役のログ機能、ruff（入っていれば。`room init` は入れないので、通常は WARN。未定義の名前の誤りは、部屋のテストで補う）。
- **部屋の中では分からないこと**（報告の「実環境で未確認の点」に書く）: Windows 固有の動作（COM、レジストリ、パス、権限）、実行先の `uv` による依存の取得（ネットワークと証明書。型の確認では依存が空だった）。結果を AI に戻すときは、`--log` を付けて再実行し、ログを読むよう AI に伝える（ps1 と同じ）。

### 人が叩くスクリプトの名前: `run` / `verify` / `release`（2026-10-24 の仮決め）

人が Windows で叩くスクリプトは、**工程で名前を固定する**。`.py`（束ねる役）と、起動用の `.bat`（上の 3 行）を、同じ名前で成果物の `tools/` に置く。AI への合図も同じ語（「verify して」「release OK」）。必要な工程だけ作る。

| 工程 | 名前 | 役目 |
|---|---|---|
| 本番実行 | `run.py` / `run.bat` | 実データに対して使う（繰り返し使うツールだけ）。結果ファイルは `ai/work/run-result.json`（業務の値は入れない）、全文ログは `ai/` の外（`_noai/user/`） |
| 動作確認 | `verify.py` / `verify.bat` | Windows でしか動かない層の実行、実アプリでの単体テスト、目視の確認 |
| リリース | `release.py` / `release.bat` | 動作確認の済んだ成果物に版を振り、記録する（束ね先は未決） |

`finalize` は使わない（release と意味が紛れる）。`verify.py` が、上の「Python の薄い層」の束ねる役の型（`verify.py` として載せた）。

**`verify` の手順**（1 回叩けば済むようにする）:

1. プリフライト: 前提（uv、Excel を閉じる、入力の有無）を確かめ、満たさなければ何をすればよいかを出して止まる。
2. 工程を順に実行する。
3. 目視の項目を 1 つずつ y/n（とひとこと）で聞く。
4. `ai/work/verify-result.json` を**毎回**上書きで出す（環境の事実、工程ごとの結果、失敗の型と場所、目視の回答、`ai/out/<成果物名>/` のハッシュ）。業務の値・ユーザー名は入れない。全文ログは今まで通り `--log` のとき。
5. 人が AI に返すのは「verify 済み」の一言。AI は結果ファイルを読む。

**`release` の手順**（束ね先は未決。`artifacts/` の案は取り下げ）。型は `release.py`（`verify.py` の `NAME` `tree_hash` `find_ai` を使うので、同じ `tools/` に置く。release が書く `release.json` はハッシュに入れない。変更が無いのに再リリースはしない）:

1. `verify-result.json` が全部 OK で、そのハッシュが今の成果物と一致しなければ、止まる（古い版を出さない）。
2. 版を振り、`verify-result.json` を添えて、README の状況表に記録する。版は `YYYY-MM-DD.N`（日付と、その日の連番。N は 1 から。kit が使っていた版と同じ書式）。束ねる先（Project の成果物の置き場）は未決。

Project の成果物は、`ai/out/`（マスクした Project は復元後の `_noai/final/`）の1本（ユーザー、2026-10-25。人の成果物を別の置き場から混ぜる案は取り下げ）。人が `ai/out/` を直接直すのは、マスクに関係しない箇所だけ。`release` の入力はこの成果物で、束ね先は未決。

型（`verify.py` は上の束ねる役の型。`release.py` は下。部屋の Linux の Python 3.13 と、`uv` の代わりの偽物で、非対話（目視が未確認になり NG）、対話（y で OK）、`release` の各 STOP と版の連番を確認した。**Windows の Python 3.13 と uv では未確認**）:

  ```python
  # /// script
  # requires-python = "==3.13.*"
  # dependencies = []
  # ///
  """リリース。verify の結果が全部 OK で、成果物が verify したときと同じでなければ止まる。版 YYYY-MM-DD.N を振り、release.json に記録する。"""
  import json
  import sys
  import time
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parent))
  import verify  # 同じ場所の verify.py（NAME、tree_hash、find_ai を共有する）


  def main() -> int:
      ai = verify.find_ai()
      if not ai:
          print("[STOP] Project の ai/ の中で実行する")
          return 1
      rf = ai / "work" / "verify-result.json"
      out = ai / "out" / verify.NAME
      if not rf.exists():
          print("[STOP] verify の結果が無い。先に verify を実行する")
          return 1
      r = json.loads(rf.read_text(encoding="utf-8"))
      if not r.get("ok"):
          print("[STOP] verify が OK でない。直して verify をやり直す")
          return 1
      if r.get("out_hash") != verify.tree_hash(out):
          print("[STOP] verify のあとに成果物が変わっている。verify をやり直す")
          return 1
      log = out / "release.json"
      history = json.loads(log.read_text(encoding="utf-8")) if log.exists() else []
      if history and history[-1]["out_hash"] == r["out_hash"]:
          print(f"[STOP] この版はリリース済み（{history[-1]['version']}）。変更が無いので振り直さない")
          return 1
      today = time.strftime("%Y-%m-%d")
      ver = f"{today}.{1 + sum(1 for h in history if h['version'].startswith(today + '.'))}"
      history.append({"version": ver, "out_hash": r["out_hash"], "released": time.strftime("%Y-%m-%dT%H:%M:%S")})
      log.write_text(json.dumps(history, ensure_ascii=False, indent=1), encoding="utf-8")
      print(f"[OK] リリース {ver}（{log.name}）。README の状況表に版を書く")
      return 0


  if __name__ == "__main__":
      sys.exit(main())
  ```

`verify-result.json` の中身: `env`（OS、Python・uv の版、`preferred_encoding`、`stdout_encoding`、`PYTHONUTF8`）、`steps`（名前・終了コード・秒）、`manual`（目視の項目・ok・ひとこと）、`failure`（例外の型と `ファイル名:行`。メッセージは入れない）、`ok`、`out_hash`。ホームのパスは `%USERPROFILE%` に置換する。2026-10-21 の「既定ではログを出さない」は、全文ログ（`--log`）に限る（ユーザーの承認: 2026-10-25）。

**`run` の手順**（実データに対して使う。`verify` と `release` の済んだツールを、人が繰り返し叩く）:

1. プリフライト: 前提のコマンドと、入力のパスがあるかを確かめ、無ければ止まる。
2. 工程を順に実行する。入力のパス（`run.bat <ファイル>` の引数）は、各工程に渡す。
3. `ai/work/run-result.json` を**毎回**上書きで出す（`verify-result.json` から `manual` と `out_hash` を除き、入力の件数 `inputs` を足したもの）。実データの名前と業務の値は入れない（失敗の型と `ファイル名:行` だけ）。
4. 全文ログは `--log` のときだけ、Project の `_noai/user/run.log` に出す（実データの語が出うるので `ai/` の外。AI に見せるのは人が伏せてから）。

型（`verify.py` の `find_ai` `scrub` `env_facts` `Tee` を使うので、同じ `tools/` に置く。部屋の Linux の Python 3.13 と `uv` の偽物で、成功、工程の失敗と `--log`、入力が無いとき、`uv` が無いときを確認した。結果ファイルに入力の名前が出ないことも確認。**Windows の Python 3.13 と uv では未確認**）:

  ```python
  # /// script
  # requires-python = "==3.13.*"
  # dependencies = []
  # ///
  """本番実行の束ねる役。実データに対して工程を順に実行し、結果（業務の値は入れない）を ai/work/run-result.json に毎回出す。--log のときだけ全文ログを _noai/user/ に出す。"""
  import argparse
  import json
  import os
  import shutil
  import subprocess
  import sys
  import time
  import traceback
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parent))
  import verify  # 同じ場所の verify.py（find_ai、scrub、env_facts、Tee を共有する）

  STEPS = ["step1.py", "step2.py"]                # 実際の工程名に変える。入力のパスは各工程に渡す
  NEEDS = ["uv"]                                  # 前提のコマンド。実際に変える
  HERE = Path(__file__).resolve().parent


  def run(result: dict, inputs: list[str]) -> int:
      try:
          missing = [c for c in NEEDS if not shutil.which(c)]
          if missing:
              print(f"[STOP] 前提が足りない: {', '.join(missing)}（入れてから、もう一度実行する）")
              result["failure"] = {"type": "Preflight", "where": ",".join(missing)}
              return 1
          absent = [p for p in inputs if not Path(p).exists()]
          if absent:
              print(f"[STOP] 入力が無い: {', '.join(absent)}")
              result["failure"] = {"type": "Preflight", "where": f"入力 {len(absent)} 件"}   # 実データの名前は結果ファイルに入れない
              return 1
          for step in STEPS:
              print(f"[STEP] {step}", flush=True)
              t0 = time.time()
              p = subprocess.Popen(["uv", "run", "--script", str(HERE / step), *inputs], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONUTF8": "1"})
              for line in p.stdout:
                  print(line, end="")
              rc = p.wait()
              result["steps"].append({"name": step, "rc": rc, "sec": round(time.time() - t0, 1)})
              if rc != 0:
                  raise RuntimeError(f"{step} が終了コード {rc} で終わった")
          print("[OK] すべて完了")
          return 0
      except Exception as e:
          print(f"[ERROR] {e}")
          traceback.print_exc(file=sys.stdout)
          tb = traceback.extract_tb(e.__traceback__)[-1]
          result["failure"] = {"type": type(e).__name__, "where": f"{Path(tb.filename).name}:{tb.lineno}"}
          return 1


  def main() -> int:
      ap = argparse.ArgumentParser()
      ap.add_argument("inputs", nargs="*", help="実データのパス（各工程に渡す）")
      ap.add_argument("--log", action="store_true", help="Project の _noai/user/<名前>.log に全文を出す")
      ap.add_argument("--log-dir", type=Path, help="この場所に全文ログを出す（--log は不要）")
      a = ap.parse_args()
      sys.stdout.reconfigure(errors="replace")
      ai = verify.find_ai()
      work = (ai / "work") if ai else HERE / "work"          # Project の外（配布先）で実行したとき
      noai = (ai.parent / "_noai" / "user") if ai else work  # 実データの語が出うるので、全文ログは ai/ の外
      result = {"tool": "run", "env": verify.env_facts(), "inputs": len(a.inputs), "steps": [], "failure": None}
      log, real = None, sys.stdout
      if a.log or a.log_dir:                                  # 既定では全文ログを出さない
          lp = (a.log_dir or noai) / f"{Path(__file__).stem}.log"
          lp.parent.mkdir(parents=True, exist_ok=True)
          log = open(lp, "w", encoding="utf-8")
          sys.stdout = verify.Tee(real, log)
          print(f"[LOG] {lp}")
      try:
          rc = run(result, a.inputs)
      finally:
          sys.stdout = real
          if log:
              log.close()
      result["ok"] = rc == 0
      result["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
      work.mkdir(parents=True, exist_ok=True)                 # 結果ファイルは毎回出す（業務の値・入力の名前は入れない）
      (work / "run-result.json").write_text(verify.scrub(json.dumps(result, ensure_ascii=False, indent=1)), encoding="utf-8")
      print(f"[RESULT] {verify.scrub(str(work / 'run-result.json'))}")
      return rc


  if __name__ == "__main__":
      sys.exit(main())
  ```

`release` の束ね先は未決（2026-10-25）。

### 原因の台帳（Windows で実行したときの失敗）

環境の違い（文字コード、パス、権限、uv の取得など）で同じ失敗を繰り返さないための置き場（2026-10-25 ユーザーの承認。仮決めは `topics/hook-room-alignment/docs/decisions.md` の 2026-10-24）。works 共通の置き場は作らない。Area ごとに持ち、一般の原因だけ workbase に上げる。

1. **人が失敗を伝えたら**（「verify が失敗した」など）、部屋の AI はまず `ai/work/<名前>-result.json`（`verify-result.json` か `run-result.json`）を読む。`env` と `failure`（型と `ファイル名:行`）から当たりを付ける。それで足りないときだけ、`--log`（ps1 は `-Log`）での再実行を頼む。
2. **直す前に台帳を引く**: Area の台帳は、人が `room pull --where kind=lesson` で渡すと `ai/in/area/` に入る（ファイル名はハッシュに変わるので、`title: Windows 実行の原因の台帳` の行で探す）。あれば読む。一般の原因は `python3 ~/shared/workflow-kit/tools/find_knowledge.py <失敗の型や語>` で `exmem/lessons/` を探す。
3. **原因が分かったら台帳に書く**: `ai/out/knowledge/windows-run-causes.md`（title は `Windows 実行の原因の台帳`）に書く。`ai/in/area/` に前の版があれば、それを写して足す（`restore` が Area の同じ名前のファイルを置き換える）。形は `room-context.md` の `stock` の `area`（`kind: lesson`、`stock-hook.md` の7見出し）。原因は Gotchas に、3行セットで1件ずつ書く。`状況:` の行の末尾に `（回数 N、最終 YYYY-MM-DD）` を付け、同じ原因がまた出たら新しく足さずに回数を増やす。マスクのまま書き、業務の値は書かない。人が `room restore` で Area に置く。
4. **一般の原因**（実名や社内の事情を剥がしても成り立つ。例: cp932 の bat、`PYTHONUTF8` が無い）は、`scope: public` の `stock` の下書き（`ai/out/stock/`）にも書く。人が `room stock` で `exmem/inbox/` に運び、`exmem/lessons/` に統合する。
5. **3 回で点検に昇格する**: 同じ原因の回数が 3 になったら、`check_py.py`（ps1 なら `check-ps1.ps1`）の規則の候補として、`public` の下書きの Open Questions に「提案」と書く。規則を足すかは workbase 側で決める。

弱点（承知の上）: PC1 の知見が他の Area に届くのは、人が PC2 へ運んだ後。業務固有の原因は Area ごとに重複しうる。

### ps1 の薄い層（Python が使えないときだけ）

下の規約は、実行先に Python（uv）が無いと分かっているとき、または PowerShell の cmdlet でしか操作できないときの、ps1 の薄い層に適用する。

- **Windows 側の処理は ps1 に書く（Windows 依存の操作だけ。判定・変換・検証は部屋側）。束ねる役も ps1 にする**: 個別の処理を `<名前>.ps1` に分け、それらを順に呼ぶ 1 本（例: `run-all.ps1`）を置く。失敗したら止まる、ログを 1 か所に出す、最後に結果の一覧を出す、を束ねる側に持たせる。人は `pwsh -File run-all.ps1` を 1 回打つだけにする。
- **bat は、起動用の 3 行だけ許す**。ダブルクリックで動かしたい場合の入口で、ロジック（`if`、`goto`、ラベル、変数、`setlocal`）は書かない。型は固定:

  ```bat
  @echo off
  pwsh -NoProfile -File "%~dp0run-all.ps1"
  pause
  ```

  1 行目は省いてよい。2 行目の `run-all.ps1` は、同じ場所にある呼び先の名前に変える。ファイルは全体 ASCII、CRLF、BOM なしで書く（`exmem/lessons/shell-script-testing-wsl.md` の bat の落とし穴は、この型に従えば出ない）。`pause` を最後に必ず置く（終わっても画面が閉じない）。
- **束ねる ps1 に、ログ出力の機能を持たせる。ただし既定では出さない**（2026-10-21 のユーザーの依頼と訂正。ログは `ai/` の中に出ると部屋の AI から読めるので、人が付けたときだけ出す）。`-Log` を付けると、Project の `ai/work/<束ねる ps1 の名前>.log` の 1 本に出す。`-LogDir <パス>` なら、その場所に出す（`-Log` は不要）。成果物（`ai/out/<成果物名>/`）の中には出さない（配布物に混ざるため）。`ai/work/` は、束ねる ps1 の置き場から親をたどって、`work/` を持つ `ai` ディレクトリを探す。見つからないとき（Project の外、配布先で実行したとき）は、束ねる ps1 の隣の `work/`。実行のたびに上書きする。個別の ps1 は、ログを作らない。エラーが出たら、人が `-Log` を付けて再実行し、AI に「`ai/work/<名前>.log` を読んで」と伝える。起動用 bat に引数を渡したいときは、2 行目の末尾に ` %*` を足してよい（`run-all.bat -Log`）。型（動作確認済み: Windows の pwsh 7.6.7、失敗した工程・終了コード・スタックがログに残る）:

  ```powershell
  #Requires -Version 7
  param([switch]$Log, [string]$LogDir)
  Set-StrictMode -Version Latest
  $ErrorActionPreference = 'Stop'

  function Find-AiWork {
    $dir = Get-Item -LiteralPath $PSScriptRoot
    while ($dir) {
      if ($dir.Name -eq 'ai' -and (Test-Path -LiteralPath (Join-Path $dir.FullName 'work'))) { return Join-Path $dir.FullName 'work' }
      $dir = $dir.Parent
    }
    return Join-Path $PSScriptRoot 'work'             # Project の外で実行したとき
  }
  $logging = $Log -or [bool]$LogDir                   # 既定ではログを出さない（-Log か -LogDir を付けたときだけ）
  if ($logging) {
    if (-not $LogDir) { $LogDir = Find-AiWork }
    $logPath = Join-Path $LogDir ([IO.Path]::GetFileNameWithoutExtension($PSCommandPath) + '.log')
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    Start-Transcript -Path $logPath -Force | Out-Null
    Write-Host "[LOG] $logPath"
  }
  $exitCode = 0
  try {
    foreach ($step in 'step1.ps1', 'step2.ps1') {   # 実際の工程名に変える
      Write-Host "[STEP] $step"
      $global:LASTEXITCODE = 0                        # Set-StrictMode の下で、未設定の参照を避ける
      & (Join-Path $PSScriptRoot $step)
      if ($LASTEXITCODE -ne 0) { throw "$step が終了コード $LASTEXITCODE で終わった" }
    }
    Write-Host '[OK] すべて完了'
  } catch {
    Write-Host "[ERROR] $($_.Exception.Message)"      # catch の中で書く（finally の後ではログに入らない）
    Write-Host $_.ScriptStackTrace
    $exitCode = 1
  } finally {
    if ($logging) { Stop-Transcript | Out-Null }
  }
  exit $exitCode
  ```

  **`-Log` のログは `ai/` の中に出るので、部屋の AI から読める**（マスクを通らない）。ログの先頭（transcript のヘッダー）に Windows のユーザー名とマシン名が入り、パス（ユーザー名を含みうる）やエラー文も入る。実データを処理する実行（マスクして復元する Project の本番）では、実データの語がログに出ないことを確認するか、`-LogDir` で `ai/` の外（例: `_noai/user/`）に出す。部屋の AI に見せるのは、人が伏せてからにする。
- **人が叩く名前（`run` / `verify` / `release`）は ps1 でも同じ**。`verify.ps1` と `release.ps1` の型を下に置く（2026-10-25）。手順・結果ファイル・止まる条件は、上の「人が叩くスクリプトの名前」と同じ。`verify-result.json` の `env` は Python 版と項目が違う（`pwsh`、`culture`、`ansi_codepage`〔日本語の Windows なら 932〕、`console_encoding`、`output_encoding`）。成果物のハッシュは Python 版と同じ値になる（隠しファイルも含める）ので、`verify.ps1` の結果を `release.py` が読んでもよい。`run.ps1` は、`verify.ps1` から目視とハッシュを除き、結果ファイルの名前を `run-result.json`、`-Log` の既定の置き場を Project の `_noai/user/` に変えて作る。部屋の Linux の pwsh 7.4 で、非対話（目視が未確認になり NG）、対話の y と n、前提が無いとき、工程の失敗と `-Log`、Project の外、`release` の各 STOP と版の連番、Python 版とのハッシュの一致を確認した。対話の日本語のひとことは、部屋の pwsh（globalization が invariant）では文字化けした（Python 版は化けない）。**Windows の pwsh では未確認**（日本語の入力を含めて PC2 で 1 回確かめる）。

  `verify.ps1`（上の束ねる ps1 の型に、プリフライト・目視・結果ファイルを足したもの。`release.ps1` から関数だけを読み込めるよう、関数の後で止まる）:

  ```powershell
  #Requires -Version 7
  # 動作確認の束ねる役（ps1 版）。前提を確かめ、工程を順に実行し、目視の項目を聞き、結果を ai/work/verify-result.json に毎回出す。-Log のときだけ全文ログも出す。
  param([switch]$Log, [string]$LogDir)
  Set-StrictMode -Version Latest
  $ErrorActionPreference = 'Stop'

  $Name     = 'demo'                                  # 成果物名（ai/out/<Name>/）。実際の名前に変える
  $Steps    = @('step1.ps1', 'step2.ps1')             # 実際の工程名に変える
  $Checks   = @('画面の見た目が仕様どおりか')           # 目視の項目。無ければ @() にする
  $Needs    = @()                                     # 前提のコマンド。実際に変える
  $SkipHash = @('release.json')                       # release が書くファイルはハッシュに入れない

  function Find-Ai {
    $dir = Get-Item -LiteralPath $PSScriptRoot
    while ($dir) {
      if ($dir.Name -eq 'ai' -and (Test-Path -LiteralPath (Join-Path $dir.FullName 'work'))) { return $dir.FullName }
      $dir = $dir.Parent
    }
    return $null
  }

  function Protect-Text([string]$s) {                  # ユーザー名を含むホームのパスを伏せる
    if ($HOME) { return $s.Replace($HOME, '%USERPROFILE%') } else { return $s }
  }

  function Get-TreeHash([string]$root) {              # verify.py の tree_hash と同じ値になる
    [string[]]$files = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force | Where-Object { $_.Name -notin $SkipHash -and $_.FullName -notmatch '[\\/]__pycache__[\\/]' } |
      ForEach-Object { [IO.Path]::GetRelativePath($root, $_.FullName).Replace('\', '/') })
    if ($files.Count -gt 1) {                         # 階層ごとに比べる（Python の Path の並びと同じ）
      [string[]]$keys = $files | ForEach-Object { $_.Replace('/', "`0") }
      [Array]::Sort($keys, $files, [StringComparer]::Ordinal)
    }
    $h = [Security.Cryptography.IncrementalHash]::CreateHash('SHA256')
    foreach ($rel in $files) {
      $h.AppendData([Text.Encoding]::UTF8.GetBytes($rel))
      $h.AppendData([IO.File]::ReadAllBytes((Join-Path $root $rel)))
    }
    return ([Convert]::ToHexString($h.GetHashAndReset())).ToLower().Substring(0, 16)
  }

  if ($MyInvocation.InvocationName -eq '.') { return } # release.ps1 が関数だけを読み込むとき

  $ai = Find-Ai
  $work = if ($ai) { Join-Path $ai 'work' } else { Join-Path $PSScriptRoot 'work' }       # Project の外（配布先）で実行したとき
  $out = if ($ai) { Join-Path $ai 'out' $Name } else { Split-Path -Parent $PSScriptRoot }
  $result = [ordered]@{
    tool    = 'verify'
    env     = [ordered]@{ os = [Runtime.InteropServices.RuntimeInformation]::OSDescription; pwsh = $PSVersionTable.PSVersion.ToString()
                          culture = (Get-Culture).Name; ansi_codepage = (Get-Culture).TextInfo.ANSICodePage
                          console_encoding = [Console]::OutputEncoding.WebName; output_encoding = $OutputEncoding.WebName }
    steps   = [Collections.Generic.List[object]]::new()
    manual  = [Collections.Generic.List[object]]::new()
    failure = $null
  }
  $logging = $Log -or [bool]$LogDir                   # 既定では全文ログを出さない（-Log か -LogDir を付けたときだけ）
  if ($logging) {
    if (-not $LogDir) { $LogDir = $work }
    $logPath = Join-Path $LogDir ([IO.Path]::GetFileNameWithoutExtension($PSCommandPath) + '.log')
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    Start-Transcript -Path $logPath -Force | Out-Null
    Write-Host "[LOG] $logPath"
  }
  $exitCode = 0
  try {
    $missing = @($Needs | Where-Object { -not (Get-Command $_ -ErrorAction SilentlyContinue) })
    if ($missing) {
      Write-Host "[STOP] 前提が足りない: $($missing -join ', ')（入れてから、もう一度実行する）"
      $result.failure = [ordered]@{ type = 'Preflight'; where = $missing -join ',' }
      $exitCode = 1
    } else {
      foreach ($step in $Steps) {
        Write-Host "[STEP] $step"
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $global:LASTEXITCODE = 0                        # Set-StrictMode の下で、未設定の参照を避ける
        & (Join-Path $PSScriptRoot $step)
        $result.steps.Add([ordered]@{ name = $step; rc = $LASTEXITCODE; sec = [math]::Round($sw.Elapsed.TotalSeconds, 1) })
        if ($LASTEXITCODE -ne 0) { throw "$step が終了コード $LASTEXITCODE で終わった" }
      }
      foreach ($item in $Checks) {
        if ([Console]::IsInputRedirected) { $result.manual.Add([ordered]@{ item = $item; ok = $null; note = '対話できないので未確認' }); continue }
        $ans = (Read-Host "[CHECK] $item  (y/n、ひとこと)").Trim()
        $result.manual.Add([ordered]@{ item = $item; ok = $ans -like 'y*'; note = if ($ans.Length -gt 1) { $ans.Substring(1).Trim() } else { '' } })
      }
      $bad = @($result.manual | Where-Object { $_.ok -ne $true } | ForEach-Object { $_.item })
      if ($bad) { Write-Host "[NG] 目視が未確認または不合格: $($bad -join ', ')"; $exitCode = 1 }
      else { Write-Host '[OK] すべて完了' }
    }
  } catch {
    Write-Host "[ERROR] $($_.Exception.Message)"      # catch の中で書く（finally の後ではログに入らない）
    Write-Host $_.ScriptStackTrace
    $inv = $_.InvocationInfo
    $result.failure = [ordered]@{ type = $_.Exception.GetType().Name; where = "$(Split-Path -Leaf $inv.ScriptName):$($inv.ScriptLineNumber)" }
    $exitCode = 1
  } finally {
    if ($logging) { Stop-Transcript | Out-Null }
  }
  $result.ok = $exitCode -eq 0
  $result.out_hash = if (Test-Path -LiteralPath $out -PathType Container) { Get-TreeHash $out } else { $null }
  $result.finished = Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'
  New-Item -ItemType Directory -Force -Path $work | Out-Null   # 結果ファイルは毎回出す（業務の値は入れない）
  $rf = Join-Path $work 'verify-result.json'
  [IO.File]::WriteAllText($rf, (Protect-Text ($result | ConvertTo-Json -Depth 5)), [Text.UTF8Encoding]::new($false))
  Write-Host "[RESULT] $(Protect-Text $rf)"
  exit $exitCode
  ```

  `release.ps1`（同じ場所の `verify.ps1` を読み込む。変数名 `$Log` は `verify.ps1` の引数と重なるので使わない）:

  ```powershell
  #Requires -Version 7
  # リリース（ps1 版）。verify の結果が全部 OK で、成果物が verify したときと同じでなければ止まる。版 YYYY-MM-DD.N を振り、release.json に記録する。
  Set-StrictMode -Version Latest
  $ErrorActionPreference = 'Stop'
  . (Join-Path $PSScriptRoot 'verify.ps1')            # 同じ場所の verify.ps1（$Name、Get-TreeHash、Find-Ai を共有する）

  $ai = Find-Ai
  if (-not $ai) { Write-Host '[STOP] Project の ai/ の中で実行する'; exit 1 }
  $rf = Join-Path $ai 'work' 'verify-result.json'
  $out = Join-Path $ai 'out' $Name
  if (-not (Test-Path -LiteralPath $rf)) { Write-Host '[STOP] verify の結果が無い。先に verify を実行する'; exit 1 }
  $r = Get-Content -LiteralPath $rf -Raw -Encoding utf8 | ConvertFrom-Json
  if (-not $r.ok) { Write-Host '[STOP] verify が OK でない。直して verify をやり直す'; exit 1 }
  if ($r.out_hash -ne (Get-TreeHash $out)) { Write-Host '[STOP] verify のあとに成果物が変わっている。verify をやり直す'; exit 1 }
  $histPath = Join-Path $out 'release.json'
  $history = @(if (Test-Path -LiteralPath $histPath) { Get-Content -LiteralPath $histPath -Raw -Encoding utf8 | ConvertFrom-Json })
  if ($history.Count -and $history[-1].out_hash -eq $r.out_hash) {
    Write-Host "[STOP] この版はリリース済み（$($history[-1].version)）。変更が無いので振り直さない"; exit 1
  }
  $today = Get-Date -Format 'yyyy-MM-dd'
  $ver = "$today.$(1 + @($history | Where-Object { $_.version.StartsWith("$today.") }).Count)"
  $history += [ordered]@{ version = $ver; out_hash = $r.out_hash; released = Get-Date -Format 'yyyy-MM-ddTHH:mm:ss' }
  [IO.File]::WriteAllText($histPath, (ConvertTo-Json -InputObject $history -Depth 3), [Text.UTF8Encoding]::new($false))
  Write-Host "[OK] リリース $ver（release.json）。README の状況表に版を書く"
  exit 0
  ```
- **実行は PowerShell 7（`pwsh`）に固定する**。ps1 の先頭に `#Requires -Version 7`、`Set-StrictMode -Version Latest`、`$ErrorActionPreference = 'Stop'` を置く。5.1（`powershell.exe`）では動かさない（UTF-8 の扱いと文字化けの差を避けるため）。ps1 は UTF-8 で保存する。
- **部屋の中で、作った直後に静的チェッカーを実行する**。実行はしない（部屋には Windows が無い）が、構文と規約の誤りは、人が Windows で実行する前に取れる:

  ```
  pwsh -NoProfile -File ~/shared/workflow-kit/tools/check-ps1.ps1 <成果物のディレクトリ>
  pwsh -NoProfile -File ~/shared/workflow-kit/tools/check-ps1.ps1 -RunTests <成果物のディレクトリ>   # *.Tests.ps1 を Pester 5 で実行する
  ```

  FAIL は直してから人に渡す。WARN は、理由を見て判断する。終了コードは FAIL の数。見るもの: UTF-8、改行の混在、構文、`#Requires`、`$ErrorActionPreference`、`Set-StrictMode`、PSScriptAnalyzer、起動用 bat の型（上の 3 行、呼び先の存在）。
- **部屋の中のテストは、外部とのやり取りを差し替える**。Windows 固有の部分（レジストリ、scoop、`setx`、Windows のパス）は、関数に包んで、Pester の `Mock` で差し替えて分岐を試す。差し替えない本物の動作は、人が Windows で実行する層（上の「テスト」の 2 層目）に回し、検証項目に「人が実行」と書く。
- **部屋の中では分からないこと**（報告の「実環境で未確認の点」に書く）: Windows 固有のコマンドの実際の動き、Windows のパスと権限、実行ポリシー、ネットワーク。部屋の pwsh は Linux 版（globalization は invariant）なので、文化依存の動作（日付や数値の書式）も本物と違いうる。
- 人が実行した結果を AI に戻すときは、`-Log` を付けて再実行し、ログ（`ai/work/<束ねる ps1 の名前>.log`。標準出力とエラーの全文、工程名つき）を読むよう AI に伝える。ログが `ai/` の外にあるときは、人が伏せてから `ai/in/` に置く（上の「テスト」と同じ）。`room run` のような、AI が Windows で実行する仕組みは無い。
