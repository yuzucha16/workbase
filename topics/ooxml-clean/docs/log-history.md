# 作業ログの経緯（log-history）

## Log

### 2026-11-03（語のマスクを必須から外し、room clean を入れた）
- ユーザーの決定: mask / restore / pull の単体スクリプト化はしない。strict を既定にする。人名だけ語で管理する利点が薄く（金額・KPI は列挙できない）、external は一から作るので業務データが入らない、という指摘で、語のマスクは external・internal とも必須にしない。削除は使ってから決める。internal の入口は明示の `room clean`。
- 実装: `area_gate_terms` を語が空でも通す形に、`room clean`（`clean_project`、strict、`_noai/reports/`、manifest は pending）を追加。単体テストは 207 件を通した。決定は `decisions.md` の同日の項。

### 2026-11-03（境界の見直しの確認が済み、知識用の経路を外した）
- NA 1: PC1 の確認 5 点はすべて問題なし(ユーザー)。残りの単体スクリプト化と cleankit の internal 既定は、`mask` への組み込み(NA 2)と一緒に決める(使わないと分かってから、が元の方針)。
- NA 3: internal のダミーで `mask.toml` なしで止まることを確認(ユーザー)。`restore`・`pull` の知識用の経路をコードから外した(8c14faa。詳細は直下の `docs/log-history.md`)。
- NA 4 は 11-02 に実装済みで、今回の確認で閉じた。

### 2026-11-02（外向け Area の共有（旧 NA3）の動作確認を閉じた）
- ユーザーが PC1 の external のダミー Area で、手順 1〜8 をすべて OK と報告。cleankit の点検は金額・メール・電話・割合を検出して何も運ばずに止まり（表示は分かりやすい）、通せば `ai/knowledge/`・`ai/docs/` に着き、人が変えた先と、記録の無い先は上書きしない（B は同じ内容で「済み」）。`ctx/area/` への写し、`docs/inbox.md` 除外（`room.py:1365` の `AREA_AI_SKIP`。`start` 前の inbox の編集は写しに影響しないのが正しい）、1 MiB 上限、AI が読めることも問題なし。
- 既知の限界: 本文の個人名は形で検出できず、`--terms` の語を渡したときだけ当たる。
- 手順書きの反省: 手順 6 は「inbox が写らないこと」を確認点として書くべきだった（効果を探させた）。

### 2026-11-02（NA4: external と internal の出口を `room stock` の一本にした）
- 依頼: internal の Area への `--dst area` と `ctx/area/` の適用。ユーザーの決定: 違いは入口だけ（internal は人が通した業務データを入れられる）、出口は行き先を内容だけで選ぶ一本、知識は実名なしで書くので `--dst area` で完結する。経緯: 別セッションで `stock` の経路を忘れた実績があり、2 経路は慣れると分からなくなる、との指摘。
- 実装: `room.py`（`area_gate_terms` 新設、`stock_to_area` と `snapshot_area_ai` の external 限定を外し、internal は `mask.toml` の語が空なら止める）、部屋の AI への案内文、`room-context.md`、`room/README.md`、テスト（`StockAreaTest`、`AreaAiSnapshotTest` 通過。全件は 1 件が私のテストの誤りで失敗し、直して該当 14 件を通した。全件の再実行はしていない）。コミット 200cd86。
- 判断は root の `docs/decisions.md` の 2026-11-02「知識の出口を `room stock --dst kit|area` の一本にし」の項。

### 2026-11-02（pptxtext の動作確認を閉じた）
- ユーザーが PC1 の実 pptx で `pptxtext.py` を回し、問題なしと報告。NA 0（動作確認と要件の拡充）を閉じた。要件の拡充は、足りないところが見えたときに積む。

### 2026-11-02（外向け Area の共有を決め、`room stock --dst` と `ctx/area/` の写しを実装した）
- 依頼: NA1「外向け Area で Area そのものを共有する是非」。棚卸し（`notes/area-share/2026-11-02-area-share-inventory.md`、project files）で、部屋が Area 単位で見るのは README の写しだけ、drvfs は配下除外ができず Area 全体のマウントは `_noai/` が見える、と確認。
- ユーザーの決定: 共有したい中身は `knowledge/` と `docs/`（過去の決定・経緯を今の判断のデータソースにする）。Area の `ai/` は部屋へ「写し」で見せる（直接書く案は `stock` の経路の勘違いが原因で取り下げ）。知識の運び先は `room stock --dst kit|area`（省くと止まる）、`area` は cleankit の点検を必須の関門にする。書き場所は `ai/out/stock/` 一本、`scope` と `dest` で振り分け。internal への適用は未議論で na に積んだ。動作確認は別セッション。
- 実装（2bd9328、3e1e4be、main に push）: `room.py`（`cmd_stock`、`stock_to_area`、`stock_to_kit`、`snapshot_area_ai`）、`cleankit.py`（`sensitive_hits`）、テスト（206 件通過）。副産物の修正 2 件: `load_terms` が実際の `mask.toml` の形で空を返していた、メールの検出が句読点の無い長い文で極端に遅くなり止まっていた。
- 判断は root の `docs/decisions.md` の 2026-11-02「`room stock` に `--dst kit|area` を足し」の項。

### 2026-11-02（pptx を実ファイルで確認、読ませる用途は取り出しに割り切った）
- ユーザーが PC1 の実 pptx を `cleankit.py` で通した。動作・開くのは問題なし。ただし背景・帯の社名を消すには `strict` が要り、`unseen-text` が使っていないレイアウト・マスターの文字と混ざって区別できなかった。cleankit の確認（旧 NA 2）はここで閉じた。
- 原因の整理は `notes/ooxml-clean/2026-11-02-pptx-extract-vs-clean.md`（project files）。ユーザーの決定: 読ませるだけに割り切り（分析・示唆抽出・論点整理）、まずシンプルに作って仕様を足す（`decisions.md`）。
- 実装: `workflow-kit/room/pptxtext.py` v0 と `tests/test_pptxtext.py`（3 件通過）、`room/README.md` に節（5b84cf7、main に push）。`docs/due.md` の 11-03 の行を削除。動作確認と要件の拡充は別セッション（NA 0）。
### 2026-10-30（掃除の room 組み込みの方針を決めた。pptx の確認は 11-03）
- 組み込みの影響とメリットを整理し、ユーザーが承認（`decisions.md` の同日の項）。`raw` → 掃除 → マスク → `ai/in`、既定 `standard`、掃除の設定のハッシュを差分判定へ、報告は `_noai/` 内の専用ディレクトリ（直下は不可）。
- pptx は `cleankit.py` が点検（`check_pptx`）と掃除（`clean_pptx`）に対応済み。ダミーでの単体テストまでで、PC1 の実 pptx と PowerPoint で開く確認は未。11-03 に PC1 で行う（`due.md`）。組み込みはその後。
### 2026-10-30（PC1 の実 xlsx で動作確認、`unseen-text` の雑音を 1 つ除いた）
- ユーザーが PC1 の実 xlsx で `check` と `clean`（standard / strict）を通した（NA 1）。基本動作は問題なし。`unseen-text` に出た文字を元ファイルで見える状態に戻すと、掃除で正しくすべて消えた。`unseen-text` は報告のみで、消えるのは掃除の動作による（途中で「戻しても消えない」との疑問があったが、状態を覚える仕組みはない。`sheet1.xml` の図形・コメント類の unseen は、シート内のコントロール・図形の名前や代替テキストが見えている文字に数えられないためと推測。未再現）。
- `xl/workbook.xml` の unseen の `microsoft.com:RD` `Single` `FV` `LET_WF` などは、Excel が書く `xcalcf:calcFeatures`（計算機能の一覧）の `name` で、ユーザーの文字ではなかった。`text_candidates` で調べない対象に追加（コミット bfd21f5、単体テスト 1 件追加、全 19 件通過）。ユーザーの承認で main に push。
- ユーザーの確認（同日）: `strict` の見た目・数式も問題なし。Next Actions の旧 2 を閉じた。
- 手順書 `guides/howto/ooxml-clean.md` への「`unseen-text` は報告のみ」の追記は、ユーザーが保留（10-30）。

### 2026-10-29（プロファイル方式の掃除）
- ユーザーの決定: 許可方式の掃除を「プロファイル方式」で進める（`--profile standard|strict`、部品の種類は `--allow` で残す）。手順書を `guides/` に作る（見本 dotfiles `windows/claude/readme.md`）。動作確認は別セッションで行う。
- 実装（`workflow-kit/room/cleankit.py`）: `STRIP_KINDS`（charts / images / embeddings / pivots / connections）と `PROFILES`、`strip_refs`（参照元の図形・要素ごと外す）、`strip_kinds`、サブコマンド `profiles`。外した部品の本体は `orphans` で消す。マクロは外さず報告のみ。
- 確かめたこと: 単体テスト（追加 5 件を含む全件）が通る。ダミーの xlsx（グラフ・画像のアンカー）と pptx（`p:pic`・`p:graphicFrame`）で、参照ごと外れ、整合の問題が出ない。Excel・PowerPoint で開く確認は未。
- 手順書 `guides/howto/ooxml-clean.md`、索引 `guides-index.md`、`room/README.md` を更新した。

### 2026-10-28（`check` に文字の検査を足した）
- ユーザーの選択（スレッドの決定カード）: 許可方式のうち「`check` に文字の検査だけ足す」を、このスレッドで行う。掃除の側は変えない。
- `unseen-text`: ファイルの中の文字（葉の要素の中身、自由な文字の属性 `name` `descr` `title` など、書式で割れた文字をつないだもの）を集め、見えている文字（見えているシートの見えている行・列のセルの値と数式、シート名、ヘッダー・フッター、見えているシートの図形・グラフの文字。pptx は見えているスライドと、その図・レイアウト・マスターの文字）と固定語に当たらないものを、部品ごとに出す。数・日付・番地・GUID・自動の名前（`グラフ 1`、`PlaceHolder 3` など）・ふりがな・書式とテーマの部品は数えない。数式の中は文字列の定数とシート名だけを見る。
- 確かめたこと: 単体テスト 13 件。openpyxl・python-pptx で作った架空のファイルと、それを LibreOffice で保存し直したものの 4 本で、非表示の行の値、非表示シートの文字とシート名、入力規則の候補、ノート、作成者（生成した道具の名前）が出て、見えている文字は出なかった。出た雑音（製品名、言語、表示形式 General、LibreOffice の `PlaceHolder N`、ノートの雛形の文字）は固定語・自動の名前・数えない要素に足した。Excel・PowerPoint で作った実ファイルでは未確認。

### 2026-10-28
- ユーザーの報告: 最新版の出力も Excel で開くと警告。`--keep` を付けると残り 2 件（外部リンクとコメント 180 件超）。
- 原因（合成 xlsx で再現）: 空のセル `<c .../>` の次のセルを、共有文字列の集計が読み落としていた。使っている文字列を「使っていない」として消し、番号が範囲の外になる（Excel は「読み取れない内容」として修復する。点検では残り 0 に見えていた）。中身のない非表示の行 `<row .../>` の次の行を、`--also hidden-rows` が空にしていた。両方を直し、共有文字列の番号の範囲を整合の確認（clean と check）に足した。
- `--keep` は「その動作をしない」指定なので、外した動作の分が残るのは仕様どおり。

### 2026-10-27
- ユーザーが PC1 の実 xlsx で点検（20 件: 非表示シート 3、グラフの写し 2、外部リンク、コメント 3 ほか）→ 掃除（8 項目、残り 4 件）。以降、外部リンクを切る動作、非表示の定義名（AccessDatabase）、`--also hidden-rows,hidden-cols`（共有数式を含む）を足し、残り 0 件になった。
- 出力先に `./` を指定して報告がリポジトリ内に出た件を受け、リポジトリ内への出力を止める守りを入れた（a3abd6b）。
- ユーザーの確認: これまで出力に「パーツがない」警告が出ていた。次回、最新版で確認して文面を知らせる。使い方は「不要な記載を消す → clean → 残り 0 を確認 → Excel で開いて確認 → 出力だけ AI へ」で合っている（本文の個人名は掃除では消えない）。

### 2026-10-26
- 依頼: 消したシートが XML に残り AI に見えた。仕組みの理解とクリーン化スクリプト（探索型）。残り方の一覧と方針案（`records/2026-10-26-mechanism-and-plan.md`）、方式 A に決定、実装（adfbfa6）。ダミーでは LibreOffice で出力が開き値が保たれた。
