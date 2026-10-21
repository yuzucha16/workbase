---
type: inbox
title: 作業部屋に変換の道具（LibreOffice・Chromium・pandoc）を入れる
tags:
  - tool/wsl
  - tool/libreoffice
  - tool/chromium
  - fonts
  - ai-room
created: 2026-10-21
sources:
  - Claude Code conversation "部屋の中で pwsh・pandoc・Excel を使う方法"
---

# 作業部屋に変換の道具（LibreOffice・Chromium・pandoc）を入れる

## Goal
interop を切った専用 WSL の部屋の中で、Markdown の HTML 化、mermaid の画像化、xlsx の変換と再計算を、AI が最後まで行えるようにした。道具の入れ方と、実機で遭遇した落とし穴を残す。
統合先の候補: lessons/ai-isolated-work-room.md（キーワード: 部屋, room, chromium, フォント）

## Principles
- 部屋の道具は、root が版を固定して入れ、AI には入れさせない。理由: 取得元と版を AI が選ぶと部屋の中身が実行ごとに変わり、AI が書き換えることもできてしまう。
- Linux の道具で完結する変換は、部屋の中で完結させ、Windows が要る範囲を狭く保つ。理由: 人の操作が残るほど、忘れて未実行になりやすい。
- 日本語の PDF や画像を作る部屋では、フォントの優先を明示する。理由: CJK のフォントは日本語・簡体字・繁体字・韓国語を同居させ、既定では簡体字が選ばれて漢字が中国式の字形になる。
- 大きな取得物は、版と SHA-256 を固定し、必要な部分だけを置き、入っていれば取り直さない。理由: 部屋の再実行のたびに数百 MB を取り直さずに済み、取得物の差し替えも検出できる。

## Decisions
- **部屋の変換の道具は、部屋を作る `init` で root が入れる**（2026-10-20）
  - 根拠: 証明書や Node.js と同じ扱いになり、AI が書き換えられず、同じ Area の部屋で版がそろう。
  - 却下案: AI がホームに入れる（取得元と版を AI が選ぶ）、入れない（HTML 化は Python、実行は人が毎回操作を覚える）。
- **mermaid の画像化は部屋で完結させる。Chromium は Playwright 版を使う**（2026-10-20）
  - 根拠: 作る側が最後まで持つ、というユーザーの方針。Ubuntu 26.04 の apt の chromium は使えなかった。
  - 却下案: 画像化だけ Windows で人が実行する（人の操作が残る）。
- **等幅フォント PlemolJP の取得は、使い捨ての部屋での試験が安定するまで `init` から外す**（2026-10-20）
  - 根拠: zip が約 220 MB で、試験のたびに待つ。手順は残してあり、コメントを外せば戻せる。
  - 却下案: 入れたまま試験する（毎回の待ち時間が長い）。

## Facts
- Ubuntu 26.04（resolute）の apt に `chromium` の候補は無く、`chromium-browser` は snap への移行パッケージ（`2:1snap1-0ubuntu4`）だった（確認: 2026-10-20、根拠: `apt-cache policy` の出力をユーザーが報告）。
- Playwright 1.64.1 の Chromium は、部屋で `libasound2t64` を apt で足すだけで起動した。`ldd` の `not found` は `libasound.so.2` だけだった（確認: 2026-10-20、根拠: ユーザーが貼った `ldd` と `--dump-dom` の出力）。
- `/etc/fonts/local.conf` で Noto Sans CJK JP を優先すると、Chromium の PDF に埋め込まれたフォントが `NotoSansCJKjp` になった。優先なしの LibreOffice の PDF には `NotoSansCJKsc` が埋め込まれていた（確認: 2026-10-20、根拠: ユーザーが貼った `strings` の出力）。
- LibreOffice 26.2 は、headless で xlsx の再計算（`=B2*3` が 6）と PDF 変換が通った（確認: 2026-10-20、根拠: ユーザーが貼った出力）。
- mermaid-cli 12.0.0 で作った PNG に、日本語ラベルが四角にならず出た（確認: 2026-10-20、根拠: ユーザーが画像を目で確認）。
- PlemolJP v3.1.0 の zip は約 220 MB で無圧縮、各書体は約 5.6 MB。ライセンスのファイルは zip に入っていない（確認: 2026-10-20、根拠: zip を取得して `unzip -l` で一覧した）。
- 部屋を作る `init` は、LibreOffice・Chromium・mermaid-cli を含めて 3 分 27 秒で通った（確認: 2026-10-20、根拠: ユーザーが貼った画面）。
- TLS 検査のある環境でも、Chromium と mermaid-cli の取得が通る（仮説）。補足: 勤務先の証明書を `--ca-cert` で入れ、Node の取得には `NODE_EXTRA_CA_CERTS` でシステムのバンドルを指しているが、その環境では試していない。

## Gotchas
- 状況: Ubuntu 26.04 の部屋で、apt で chromium を入れようとした
  - 原因: apt の chromium が snap への移行パッケージで、部屋では snap を使えない
  - 解決: Playwright の Chromium を、root が `/opt` に入れた
- 状況: `chrome --headless --dump-dom 'data:text/html,<p>日本語</p>'` の出力が文字化けした
  - 原因: `data:` URL に文字コードの指定が無く、Latin-1 として読まれた（Chromium の不具合ではない）
  - 解決: `data:text/html;charset=utf-8,…` と指定した
- 状況: Chromium の実行で `dbus ... Failed to call method` の ERROR 行が出た
  - 原因: 部屋に dbus が無い
  - 解決: 無害な警告なので無視した

## Open Questions
- TLS 検査のある環境（勤務先の PC）で、`init` を通して Chromium と mermaid-cli の取得が通るか。
- 画像・PDF は、マスク後の語が絵になり、復元の対象にならない。マスクして復元する Project（復元の対象は `ai/out/`）では、画像・PDF をどこに置くか（`ai/work/` に置く、または復元の対象外の派生物置き場を作る）。
- PlemolJP を `init` に戻す時期。

## Next Actions
- 勤務先の PC で `init`（`--ca-cert` あり）を通し、Chromium と mermaid-cli の取得を確かめる（2026-10-21 時点）。
