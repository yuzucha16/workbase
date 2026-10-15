# ai-workspace-boundary: 決定

旧 `ai-room-next-steps.md` の「2」（2026-10-12 に確定）をそのまま移した。新しい決定は、この下に日付つきで足す。背景は `notes/ai-room-handover.md`、詳細は `notes/ai-room-design.md`。

## 2026-10-12 未決9項目の確定（ユーザーが1つずつ確認し、最後に一覧で確定）

最初はこれで開始する。使ってみて修正が入る可能性はある。ここで決めたことが、前の P1〜P8 と食い違うところは、この節が優先。

| # | 決定 |
|---|---|
| 1 | 部屋は **Area ごとのディストロ**、Project ごとにマウントする部屋（P1 を変更）。同じ Area の中では、会話履歴などを共有する。**顧客・機密度の境界は Area で切る**（顧客の違う Project は別の Area に置く）。理由: ライフサイクルが分かりやすく、ログインと導入が Area の数で済む |
| 1補 | 境界を守る歯止め: (a) Project の `README.md` に `area:` を必須にし、ディストロ名（`room-<Area>`）と一致しない Project は、マウントを拒否する。(b) Area の `README.md` に `boundary:`（顧客・機密度の印）を持たせ、`room open` で入力を必須にする。(c) 来歴チェック: `ai/in/` の各ファイルの由来（Area と Project）を manifest に記録し、記録のないファイルや由来の違うファイルがあれば止める。(d) 毎回の `room start` で、日時・Area・Project・ディストロ・マウントしたパス・manifest のハッシュ・チェック結果を `ai/records/` に追記する。(e) 同じディストロに、同時に複数の Project をマウントしない。(f) 顧客をまたぐ横展開は、汎用化した成果だけを【汎用】の経路（部屋の AI が `ai/out/stock/` に下書き → 人が確認して workbase の `exmem/inbox/` へ）で行う。限界: 人が Windows 側で Area をまたいでファイルをコピーすること自体は止められない（来歴チェックで検出して記録する） |
| 2 | スクリプトは Windows 側の Python 1本（`room.py`）。**uv 管理で、バージョンを pin 留め**（`.python-version`、`requires-python`、`uv.lock`。コミットする）。部屋の中の Python も uv で入れて pin する。標準ライブラリ中心。pwsh は薄いラッパーのみ。置き場は `workflow-kit/` 配下（手順書を書く段階で決める）。Windows には `uv` 0.13.0 と Python 3.13 が導入済み |
| 3 | `projects/<名>/ai/` だけをマウント（P3）。`_noai/` は `ai/` の外に置き、git で追跡しない。`docs/` は `ai/docs/` へ移す。**マウント点は `/mnt/room/<Project 名>`**（Claude Code の履歴が作業ディレクトリのパスごとに分かれるので、Project 単位で処理できる）。マウントは作業中の Project の `ai/` だけに限り、終わったらアンマウントする。既存: `archives/` の2件は移さない。`projects/` の1件は、最初の試行で移す。Area の `ai/` は、Area の部屋を初めて開くときに作る。Vault トップの `docs/` はそのまま（Vault 側の作業記録） |
| 4 | 人が言うコマンドは `room open` / `room start` / `room close`（P4）。既存のフック（`open` `start` `wrap` `close`）は、部屋の中で AI が判断の部分を行う |
| 5 | Area への同期は郵便受け（P5）。`room start` の回収で、同じ Area の【案件】の項目を Area の `ai/docs/inbox.md` へ（Windows 側の `room.py` が追記）。【汎用】は `exmem/inbox/` の経路 |
| 6 | マスク: (6-1) プレースホルダーは場所で2種類。定義名・シート名は ASCII（`SHEET_001`、`NAME_001`）、それ以外は `⟦CUST_001⟧` 形式（種類の接頭辞つき）。実測: `⟦⟧` はシート名には使えるが、定義名には使えない。(6-2) 数値は既定でマスクしない。語は `_noai/` の `mask.toml` の `[terms]`、列は `[columns]`（`シート名!列名`）で指定。(6-3) xlsx は zip レベルの置換を基本に、作成者・会社名のプロパティは無条件に空に、`printerSettings*.bin` は削除（`[Content_Types].xml` と `.rels` も直す）、置換後に全 part を点検して、対応表の語が残っていれば止める。**対象は csv と xlsx**。docx・pptx も同じ zip 方式で揃えるが、変更は xlsx を基準にし、まず小さく動かして決める |
| 7 | reap は close から14日を既定に、**設定で変更可能**（置き場は設定ファイルか Project の `README.md` の frontmatter。実装時に決める）。次の `room close` で期限切れを一覧にし、承認して実行する（`room reap <名>` でも可）。履歴は `ai/records/sessions/` に写してから消す。zombie の実体は、Project ごとの会話履歴（`~/.claude/projects/-mnt-room-<名>/`）と `~/tmp/<名>/` |
| 8 | Vault 側で `projects/` `areas/` `archives/` を丸ごと deny（`Read` と `Edit`）。ワークスペースの `.claude/settings.json` の雛形に入れる。安全網であって境界の保証ではない（`grep -r` やスクリプトの中は止まらない）。`room.py` は AI に実行させない（`AGENTS.md` に明記）。Windows ネイティブで絶対パスの deny が効くかは、雛形を作るときに実機で確認する |
| 9 | Codex・Copilot は今は設定しない。必要になったら部屋の中へ導入する（境界は物理分離なので、AI の種類に依存しない）。部屋の規約の正本は `AGENTS.md`、`CLAUDE.md` は `@AGENTS.md` で読ませる。エディタ内蔵の Copilot（部屋の外で動く）は、機密を扱う Project では使わない |

実測から決まった事項（上の「1」の実測結果の「設計に足すこと」）も、同じく確定: AI は一般ユーザーで動かす、Zed は WSL リモート接続でだけ使う、`~$*` は無視する、大量の一時ファイルは `~/tmp/`、`rg` はパスを明示する、AI が書くスクリプトに標準ライブラリと同名を付けない。

