---
type: explain
title: AI 作業部屋: 変換の道具（LibreOffice・Chromium・pandoc）を部屋に入れた理由と、room run の案（理解ガイド）
tags:
  - security
  - tool/wsl
  - tool/excel
---

# AI 作業部屋: 変換の道具を部屋に入れた理由と、room run の案（理解ガイド）

部屋の中で、Markdown の HTML 化、mermaid や SVG の画像出力、Excel の変換と再計算までを、AI が最後まで行えるようにした経緯と、入れた道具、実機で分かったこと、まだ作っていない `room run`（Windows が要る実行を 1 つの操作に固定する案）を、自分で説明できるところまで理解するための文書。部屋の作り方は [[ai-room-setup]]、`init` の使い方は [[ai-room-setup-script]]、部屋の設計の理由は [[ai-room-why]]。

> **状態: 草稿（未レビュー）。** 2026-10-20 のスレッドの議論と、PC2 の使い捨ての部屋（`room-scratch`）での試験の結果をまとめた。PC1（TLS 検査のある環境）での確認は未了。

## 1. 背景と問い

- 部屋の AI に、Markdown の HTML 化、mermaid の画像出力、スクリプトの実行、場合によっては Excel の処理を任せたい。
- ユーザーの方針は「作る側（AI）が最後まで持つ。中途半端なところで分担したくない」。操作は忘れるので、人の手は少なく、決まった形にしたい。
- 部屋は `interop` と `/mnt/c` を切っているので、Windows のプログラム（pwsh.exe、Excel）を呼べない。ここで、次の 2 つに分けて考えた。

| 場面 | 部屋の中で完結できるか | 方針 |
|---|---|---|
| Markdown の HTML 化、mermaid・SVG の画像化、xlsx・docx・pptx の PDF/HTML/csv への変換と再計算 | できる（Linux の道具で足りる） | **v1**: 道具を `init` で入れる |
| Windows の pwsh での実行、Excel 固有の機能（VBA の実行確認、ピボットの作成） | できない | **v2 / v3**: AI がスクリプトを作り、人が `room run` で実行する（未実装） |

## 2. v1・v2・v3

ユーザーの呼び分け（2026-10-20）。

| 版 | 中身 | 状態 |
|---|---|---|
| v1 | 部屋に LibreOffice・Chromium（mermaid-cli）・pandoc を `init` で入れる。`room run` は作らない | 実装済み。PC2 で確認。PC1 は未確認 |
| v2 | `room run`: AI が書いた `.ps1` を、人が 1 件ずつ指定して Windows で実行する。実データには使わない（マスクして復元する Project には使わない） | 案のみ。v1 に価値がなければ v2 に上げる |
| v3 | v2 に、実データ（マスクして復元する Project）への実行を足す | 案のみ（条件は 7 章） |

v1 の見立て: 変換と mermaid の画像化が部屋で完結するので、目的の大半は v1 で済む。`room run` が要るのは、VBA の確認とピボットの作成だけになる見込み。

## 3. v1 で入れたもの

`room init`（`--resume` でも）が、次を root で入れる。AI は書き換えられない（Node.js と証明書と同じ扱い）。

| 道具 | 用途 | 入れ方 |
|---|---|---|
| LibreOffice（calc・writer・impress） | xlsx・docx・pptx の PDF/HTML/csv 変換、数式の再計算 | apt（`--no-install-recommends`） |
| `fonts-noto-cjk` | 無いと PDF・画像の日本語が四角になる | apt。`/etc/fonts/local.conf` で JP を優先（既定だと簡体字 `sc` が選ばれ、漢字が中国式の字形になる） |
| pandoc | Markdown の HTML 化 | apt |
| Chromium | mermaid の画像化、HTML の PDF 化 | Playwright 1.64.1 の Chromium を `/opt/ms-playwright` へ。不足していた `libasound2t64` も入れる |
| mermaid-cli 12.0.0 | mermaid の PNG/SVG 出力 | `npm install -g`（Chromium の自前取得は止める） |

部屋の中で使う呼び出し:

| やりたいこと | コマンド |
|---|---|
| mermaid を PNG に | `room-mmdc -i d.mmd -o d.png`（puppeteer の設定と `--no-sandbox` を含む） |
| HTML を PDF に | `room-chrome --no-pdf-header-footer --print-to-pdf=x.pdf <URL またはファイル>` |
| xlsx を PDF に、再計算した xlsx に | `soffice --headless --convert-to pdf t.xlsx`、`soffice --headless --convert-to xlsx --outdir re t.xlsx` |
| Markdown を HTML に | `pandoc -f markdown -t html` |

等幅フォント PlemolJP（v3.1.0、zip 約 220 MB、SHA-256 を固定）の手順も `room.py` に書いてある。取得に時間がかかるので、試験が安定するまで `init` から外している（コメントアウト。戻すときは `step_script` の行のコメントを外す）。

## 4. 境界への影響

- Linux の道具を足すだけで、`interop` と `/mnt/c` の無効、sudo 不可は変わらない（`init` の分離の確認はそのまま通る）。
- **復元の制約**: 復元（マスクして対応表ができた Project の終了時）は `ai/out/` の png と pdf を復元できず、「復元できない形式」で止まる。画像と PDF はマスク後の語が絵になるので、復元の対象にもならない。画像・PDF の出力が実用になるのは、マスクしていない Project（復元が動かない）。マスクして復元する Project では、`ai/work/` に置くか、テキスト形式（HTML、xlsx、csv）の成果物に限る。
- ネットワーク: Chromium と mermaid-cli の取得で外へ出る。TLS 検査のある環境では、`--ca-cert` に加えて、Node の取得がシステムの証明書ストアを見ない点に注意（`init` は `NODE_EXTRA_CA_CERTS` と `NPM_CONFIG_CAFILE` を指す。PC1 では未確認）。
- Chromium のサンドボックスは、非特権ユーザー名前空間の制限で動かないことがある。`--no-sandbox` で動かすので、信頼できないページは開かない（自作の mermaid テキストと、自分で作った HTML の PDF 化だけに使う）。

## 5. 実機で分かったこと（PC2、2026-10-20）

| 症状・疑問 | 原因 | 対処 |
|---|---|---|
| apt の `chromium` に候補が無い | Ubuntu 26.04（resolute）の `chromium-browser` は snap への移行パッケージ。WSL の部屋では snap を使えない見込み | Playwright の Chromium を使う |
| Chromium が `libasound.so.2` で起動しない | 不足していたライブラリはこれだけ | `libasound2t64` を apt で入れる |
| `--dump-dom` の日本語が化ける | `data:` URL に文字コードの指定が無く、Latin-1 として読まれる | `data:text/html;charset=utf-8,…` と指定する（Chromium の不具合ではない） |
| `dbus ... Failed to call method` の行が出る | 部屋に dbus が無い | 無害な警告。無視してよい |
| PDF のフォントが `NotoSansCJKsc` になる | `fonts-noto-cjk` は JP・SC・TC・KR を同居させ、既定で SC が選ばれる | `local.conf` で JP を優先。実機で `NotoSansCJKjp` になった |
| PlemolJP の zip が大きい | 全書体を 1 つの zip に入れている（約 220 MB）。zip は無圧縮（store） | 取得は 1 回。必要な 4 書体だけを置く。入っていれば取り直さない |

## 6. 試験の結果

| # | 確かめたこと | 結果 |
|---|---|---|
| 1 | `init` に LibreOffice・日本語フォント・pandoc を足して通る | 通った（LibreOffice 26.2.6.3、pandoc 3.7.0.2） |
| 2 | xlsx の PDF 変換と再計算、日本語 | 通った（再計算の値 6、PDF に日本語フォントが埋め込まれた） |
| 3 | Chromium の起動 | 通った（案 A の apt は不可、案 B の Playwright で通った） |
| 4 | mermaid の PNG（日本語ラベル） | 通った（ユーザーが画像を目で確認） |
| 組み込み | `init` を通して、`mmdc --version` が最後に出る | 通った（3 分 27 秒） |
| 5 | PC1（TLS 検査）で 1〜4 | **未実施** |

v1 の価値の判定: 3〜4 が通ったので v1 で足りる見込み。PC1 だけ通らないときは、取得の手順（`--ca-cert`、環境変数）を直して再試験し、直せなければ v2 に上げる。

## 7. room run の案（未実装）

v2 の設計。`room.py` はまだ変えていない。

- **流れ**: AI が `ai/work/run/<成果物名>.ps1` を書き（使い捨てのスクリプトの置き場は `ai/work/`）、`ai/work/run/requests.json` に依頼を足す。人が `room run <Project> <成果物名>` を打つ。`room` が中身（全文）とハッシュを見せ、承認したときだけ実行する。承認なしの自動実行はしない。
- **スコープ**: 1 回に 1 件、名前で指した成果物だけ。名前を省くと、その Project の未実行を一覧するだけで実行しない。全体実行と Area 単位の実行は作らない（実行のたびに成果物が変わりうるため）。
- **気づく仕組み**: 依頼（AI が書く）と実行の記録（`room` だけが書く `ai/records/run-log.json`）を分ける。AI が「実行済み」を偽れず、実行後に書き換えたら「変更あり」と出る。`room start` の冒頭に「未実行 N 件、変更あり M 件、失敗 K 件」を出し、`room close` は未実行があれば止める。限界: 検出は次に `room` を使ったときになる。
- **成果物の置き場**: `ai/out/<成果物名>/dist/`（全 type 共通の派生物置き場）。実データ由来のものは `_noai/final/<成果物名>/dist/`。`dist/` は `restore` の対象外にする（要実装）。
- **実行環境**: pwsh 7 を既定にする（PC1 で使えることを確認済み）。無いときだけ `powershell.exe` 5.1。
- **v3（実データへの実行）の条件**（ユーザーの承認: 2026-10-20）: 実行前の静的検査（ネットワーク系・削除・Project 外のパスで止める）、原本は渡さず入力のコピーに実行、書き出しは `_noai/final/` だけ、ログは `_noai/`。弱点: 難読化は防げない。最後の関門は人が読むこと。AI が書いたコードが、ユーザーの Windows 権限で実データに触れる点が、部屋の保証（AI は実データを見ず、Windows に触れない）からの後退になる。
- **LibreOffice で解消する問い**: xlsx の変換と再計算は部屋で完結するので、`room run` に回す件が減る。解消しないのは、VBA の実行確認、ピボットの作成（LibreOffice は Excel と結果が違う）、見た目の完全な再現。

## 8. 未確認・残り

- PC1 での `init`（`--ca-cert` あり）による Chromium と mermaid-cli の取得。
- PlemolJP を `init` に戻す時期。
- `room run`（v2）と v3 の実装は、v1 の価値の判定の後。成果物（xlsx、docx など）の `dist/` の `restore` の扱い。
- 字形の優先（JP）は PDF のフォント名で確認した。見た目の確認は、漢字の字形が中国式になっていないかを、実際の PDF で見る。
