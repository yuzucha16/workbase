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


## 2026-10-15 type: dev の成果物の置き場と、Area の共通ルールの届け方（ユーザーが1つずつ承認）

他環境（`projects/` の下に Area と Project を重ねていた旧 kit）の AI 開発環境プレイブックを、この環境の `areas/` `projects/` の分離に当てはめた。知識の本体は `exmem/lessons/ai-tool-deliverable-structure.md`（共通部）と `excel-vba-ai-development.md`（VBA 固有）。

### 【汎用】成果物は `ai/out/<成果物名>/` に一式で置く（2026-10-15）
- 決めたこと: README、`src/`、`docs/`、`tests/`、`tools/` を `ai/out/<成果物名>/` にまとめる。`ai/docs/` は作業の記録だけ。参考資料は `ai/in/`、中間成果物は `ai/work/`、元データは `_noai/raw/`。1 Project = 1 成果物（`open-hook.md` の判断基準）。
- 根拠: 自己完結で配布の単位になり、`room restore`（`ai/out/` の置換）がそのまま掛かる。`out/` 直下の `close.md` や `stock/` と混ざらない。
- 却下案: `ai/work/` を正本、`ai/out/` を派生物にする（コピーの工程が増え、手数が重い）。
- → lessons/ai-tool-deliverable-structure

### 【汎用】検証を2層に分け、実環境の結果は人が実データの語を伏せて AI に渡す（2026-10-15）
- 決めたこと: 部屋の中で完結する検証は AI、実環境が要る検証は人が Windows で実行する。実行結果を AI に渡すときは、人が実データの語を伏せる（規約）。
- 根拠: 部屋は `interop` と C: のマウントを無効にするので、AI は Excel などを動かせない。規約は手数が増えず、すぐ運用できる。
- 却下案: `room` に結果の受け取り口（マスクして `ai/in/` へ）を作る（実装が要る。Next Actions に残した）。部屋の `interop` を有効にする（境界が破れる）。
- → lessons/ai-tool-deliverable-structure

### 【汎用】Area の共通ルールは Area の README に書き、`room start` が `ai/ctx/area-README.md` に写す（2026-10-15）
- 決めたこと: Project を跨ぐ約束（旧プレイブックの親フォルダの共通ルール）は、Area の README に置く。`room start` が Area の README を読み取り専用で `ai/ctx/area-README.md` に写し、AI が開始時に読む。16 KiB を超えたら `start` が警告する（止めない）。
- 根拠: 既存のパス（`ai/ctx/`）を使え、`room` の変更が小さい。`ai/ctx/` は追跡せず、`start` の終了ごとに消えるので蓄積しない。Area は境界の単位なので、同じ Area の Project 名しか写らない。
- 却下案: Project の README に写す（Area 側と二重になり古くなる）。Project の `ai/docs/decisions.md` に持つ（Area に1つのルールを複数の Project が重複して持つ）。
- ユーザーが昇格を承認（2026-10-15）。ラベルを【この件】から【汎用】に直した。
- → inbox/2026-10-15-area-readme-room-context

### 【この件】kit に `type: dev` の成果物の手順を足す（2026-10-15）
- 決めたこと: `open-hook.md` の Project の構造（`type: dev` の行）に、部屋の Project では成果物を `ai/out/<成果物名>/` に置くと追記した。作り方は新しい `dev-deliverable-guide.md`（`type: dev` の `open` / `start` のときだけ読む短い手順。理由は lessons へのリンクだけ）。コミット `b6c3199`。
- 根拠: kit は手順書を薄くする方針。`type: dev` のときだけ読むなら、他の作業の読み込みが増えない。
- 却下案: 未検討（提案をそのまま承認）。

## 2026-10-16 AI が使えない間の `_noai/final/` の扱い（ユーザーが最小案を承認）

### 【汎用】復元は、人が変えた `_noai/final/` を上書きせず止める
- 決めたこと: `room restore`（`start` の終わりを含む）は、`_noai/final/` のファイルが前回の復元の書き出しと違えば、何も書かずに一覧を出して止める。`--force` で上書きできる。前回の書き出しのハッシュは `_noai/map/final-manifest.json`（追跡外）。AI だけが変えたときは止まらない。
- 根拠: 設計で、人が `final/` でピボットの更新などの仕上げをする。無条件の上書きはそれを消す。
- 却下案（今は採らない）: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束。実 Project の1巡で足りないと分かってから決める。
- 実装: `room.py` の `restore_project`、テスト `test_restore_stops_when_final_was_edited_by_human`。

### Facts
- `room` の単体テストは51件。`SharedPermissionTest` の2件（`test_snippet_creates_file_when_missing`、`test_snippet_merges_keeps_existing_and_is_idempotent`）が失敗する。今回の変更の前から同じ（確認: 2026-10-15、根拠: 変更を外して実行し、同じ2件が失敗）。原因は未調査。
