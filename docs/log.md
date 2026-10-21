# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。2026-10-19 に整理した（整理前の全文は `log-history.md` の同日の項）。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-10-21 | 定例 | daily の振り返り（毎営業日。`start 改善4`。規模は `retrospective-method.md` の v6: 3章・500字） | ユーザー |
| 2026-10-26 | 定例 | weekly の振り返り（毎週月曜。4章・1,000字）。仮決めの期限切れを数える（R-05） | ユーザー |
| 2026-10-26 | 定例 | monthly の振り返り（最終営業日を含む最後の5営業日の初日。5章・1,500字）。初回は材料の weekly が1回だけ。次は 11-24 | ユーザー |
| 2026-10-25 | 単発 | 保留中の Open Questions（Stop フックの記録の置き場） | ユーザー |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断（Open Questions。計画のやり方の品質チェックの後） | ユーザー |
| 2026-10-26 | 単発 | 振り返りの手順書 v6（v5 の続き）の仮決め。定例の初回で字数を測る（項目 5） | ユーザー |
| 2026-10-28 | 単発 | 仮決め: 題材ごとのトピックと `records/` の仕訳（2か所）を、正式化するか（`decisions.md` の 10-21。正式化なら `start-plan.md` の置き場の表を直す） | ユーザー |
| 2026-11-02 | 単発 | `remote` の type の要否（項目 10 の後） | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |

## 状態

- 経路は整備済み: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`。cwd はリポジトリのトップだけ。フックの権限は `hooks.md` の「領域とフックの権限」が正本。
- 仕組みの決定は `review 消化` の3段で承認する（`approval-screening.md`）。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`（変更・調査1・調査2・振り返り1）。作り方は `exmem/lessons/method-creation.md`、改善の記録は `topics/kit-growth/records/`。
- room（`workflow-kit/room/`）: 実機の通しは済み（2026-10-18）。Ubuntu 26.04 の部屋（`init`）、`data:` の none / mask / restore（10-21 に `data:` を廃止し、状態で決める形にした。単体テストのみ）、`room shell` と Node の流れは、実機で確認済み（ユーザー、2026-10-19）。`room init` の `wsl --install` の早戻りは、次に再現するまで保留（`log-history.md` の同日の項）。`room aws-key` は、10-20 に原因（`sh -c` の引数経路で代入した変数が空になる）を直し、PC1 で動作を確認した（`08202a7`）。
- room の変換の道具（2026-10-20）: `init` が LibreOffice・日本語フォント・pandoc・Chromium・mermaid-cli を root で入れる（v1。PC2 で確認、PC1 は未確認）。`room run`（v2・v3）は案のみ。経緯と使い方は `guides/explain/ai-room-convert-tools.md`、決定は `decisions.md` の同日の項。
- room の Area を跨ぐ共有知（2026-10-21）: `room pull`（Area の `knowledge/` から条件で絞り、`_noai/raw/area/` へ）と、`restore` の Area 書き出し（`ai/out/knowledge/` → `areas/<Area>/knowledge/`。人が変えた既存ファイルがあれば止まる、`--force` で上書き）を実装し、実機の通しで問題なし。統合は部屋の作業（works の AI は実名を読まない）。手順は `guides/howto/ai-room-setup-script.md` の 4.1・6.1、理解は `guides/explain/cross-area-shared-knowledge.md`、決定は `topics/private-knowledge/docs/decisions.md`。
- room のコミットのトレーラー（2026-10-21）: `init` `open` `rename-area` `start` `readme` `close` のコミットに `Room-Op` / `Room-Rev` / `Room-Area` / `Room-Project` を付ける（`room/README.md`、決定は `decisions.md` の同日の項）。`Room-Rev` を基点に `git diff <Room-Rev>..HEAD -- workflow-kit/room` で、既存の Area / Project に対する room の変更を確認できる。`restore` / `pull` の版は未記録。実機での確認は未実施（単体テストのみ）。room の単体テストは PC1 でスキップを含む全件パス（10-21。短縮名の不一致を直し、`openssl` が無い環境では CA のテストをスキップ。`9a9c8d2`）。
- 計画のやり方（6R → 憲章 → 成果物 WBS → マイルストーン）: トピック `topics/planning-method/`（Project 型。状態は同 `docs/log.md`）。2026-10-20 に試験運用で `workflow-kit/` に取り込んだ（`start 計画`、`start-plan.md`）。次は PC1 の品質チェック3回。試行の元ファイルは Project の共有フォルダ `notes/planning-method/`（クラウド側の控え。PC 環境からは見えない）。測ったことは `topics/kit-growth/records/planning-method-record.md`。

## Next Actions

11. room の変換の道具（v1。2026-10-20 実装、PC2 で確認）: ① PC1（TLS 検査、`--ca-cert` あり）で `init` を通し、Chromium と mermaid-cli の取得が通るか確かめる（結果で v1 の価値を判定し、通らなければ取得手順を直す。直せなければ v2 に上げる）② PlemolJP を `init` に戻す時期（使い捨ての部屋が不要になったら、`room.py` のコメントを外す。ユーザーが戻す）③ `room run`（v2）の実装は v1 の価値の判定の後。仕様の叩き台は、決定と `guides/explain/ai-room-convert-tools.md` の 7 章。
5. 振り返り（旧 38、15、13）: v5 の材料集めは AI 作業部屋の回を初実行として数えた（ユーザーが読んで比べる）、週次の使い方（引き継ぎは 10-26 の週次で）、改善5 の品質チェック3回。改善4 は 10-20 に定例化し、規模の Must を足した（v6。`decisions.md` の同日の項）。daily 10-20 は済み（第2回 470字、第3回 495字。空白を除く。含めると超える。数え方は 10-26 に決める。施策 R-2026-10-20-01・02 は承認待ち）。weekly と monthly（10-26）で、字数が収まったかを `retrospective-method-record.md` に足す。
6. 暫定の数値（旧 24）: 続ける・切るの約10万 / 約2万トークンを、本物のフック列で3回以上再実験する（`~/claude-records/<フォルダ名>/sessions.jsonl` の記録を集計する）。Stop フックの費用記録（旧 29）は、Zed を使う PC で動作を確認した（10-19。dotfiles の `settings.json` のコマンドは `python "$HOME/.claude/hooks/stop-record.py"`。Git Bash の無い PC の警告を止めるため、10-20 に `"shell": "powershell"` を足した。dotfiles `43a7192`、未 push）。`sessions.jsonl` は 10-20 に約50本を誤って消したので、再実験は記録が溜まってから。`replies/<日付>.md` が 0 バイトだった件は、原因を特定して直した（10-19）: 環境変数 `PYTHONIOENCODING=utf-8:surrogateescape` の下で、標準入力に不正なバイトが入ると、書き込みで例外になり空ファイルだけが残る（lone surrogate で再現）。書き込みの `open` に `errors="replace"` を足した（実機で確認済み: 同日 `replies/2026-10-19.md` に 16 KB が入った。`stop-record.py` は、この PC では `~/.claude/hooks/` と共有フォルダ（`_sharedai`）にあり、公開の dotfiles（`main`）には無い。Zed の PC に置いた版にも同じ修正が要る）。
9. ルールが見つかりにくい構造（2026-10-20）: works で `.bat` を作った AI が、dotfiles と exmem にあった ASCII ルール（2026-10-06）に届かず、`chcp 65001` で崩れた。ルールは `exmem/lessons/shell-script-testing-wsl.md` の後ろの追記節にあり、索引の1行に `.bat` の語が無く、dotfiles の `AGENTS.md` にも無かった。索引に語を足したのは補修で、恒久対策ではない。exmem の肥大化（大きいノートの後ろの追記節、索引の1行では引けない）と合わせて、領域全体の論点として議論する: 知識がどこにあれば、作業の最中に届くか（索引、ノートの分け方、作業側の `AGENTS.md` への写し、検索の仕組み）。議論の前に、似た見落としが他にもあるかを数える材料を集めてよい。ユーザーの指示（2026-10-20）。なお `.bat` は、暫定で全体 ASCII を正にし、cp932 の `.bat` と試験はやらない（cp932 の内容は lesson の草稿・優先度低。dotfiles は変更しない）。

12. 会議録のナレッジ化（`topics/private-knowledge/`。2026-10-21 開始）: Area を跨ぐ共有知の仕組み（`room pull`、`restore` の Area 書き出し、型）を実装し、実機の通し試験で問題なし（ダミーの Area）。`stock-modes` との重なりは整理済み（10-21。衝突なし、仕様の追加2点・削除なし）。次は、実例1件で指標を測ること、統合の手順書の整備、型の整理は別セッション（状態は同 `docs/log.md`）。続きは「private-knowledge の続き」。
13. 題材ごとのトピックと `records/` の仕訳（仮決め 〜2026-10-28。`decisions.md` の同日）: `stock-modes/`（M1〜M3 は 10-21 に通した。次は実機: 実際の題材で `stock 理解` → `integrate`、`room stock`。`start 計画` へのフィードバック案8件は `topics/planning-method/planning-method-feedback-stock-modes-m1.md`、`review 消化` で承認）、`private-knowledge/` を、同じ構造で運用する（`usage-viz/` は 10-21 に閉じた。HTML の見た目はブラウザで未確認）。10-28 に正式化するかを `review 消化` で決める。
14. room の Area の置き場の設計（2026-10-21）: `data:` 廃止の次。知識置き場は `areas/<Area>/_noai/knowledge/` に移した（`decisions.md` の同日）。`_noai/source/` と `pull --from source` も実装した（単体テストのみ）。`_noai/deliverable/`（`ai/out/deliverable/` → Area）も実装した（単体テストのみ）。残り: ① 旧 `areas/pilot2/knowledge/`（試験用のダミー。未追跡。ユーザーが移す）② 実機で `data:` なしの `open`（`mask.toml` のひな形つき）/ `start` / `restore` と、`source` → `pull` → `restore` → `deliverable` の通しを確かめる ③ 部屋の AI に渡す文書へ、成果物を `ai/out/deliverable/` に置く案内を足すか確かめる ④ `guides/explain/cross-area-shared-knowledge.md` の設計の軸（「戻り」「統合」）を、新しい置き場の分け方に合わせる（`exmem/inbox/2026-10-21-area-data-layout-flow.md` を `integrate` するときに整合）。

## Open Questions

- `stock-hook.md` の手順「既存の知識と重なるか確認する」/ 理解のとき、近い既存ガイドが新しい内容で古くなる場合の扱いが曖昧（`stock-explain.md` は「同じテーマがあればメモを作らず報告」とだけ書く）。案: テーマが違うなら作り、既存ガイドの更新が要る点は、メモの「要確認事項」に書く（2026-10-21 は、この形で作った）。

- 【案件】の行き先: `para-operations`（2026-10-07）は Area の `docs/decisions.md`、実装（2026-10-14）は Area の `ai/docs/inbox.md`。現行はどちらか（`topics/private-knowledge/` の確認 #2）。
- Stop フックの記録の置き場: 既定は `~/claude-records/`。部屋の中だけ `ai/records/` にするか。実機確認（Next Actions 6）の後に決める。【保留 〜2026-10-25】
- `remote` の type: 要否は項目 `dev-env` の実使用（済み。10-20 にユーザーが業務で使った）を踏まえて決める。【保留 〜2026-11-02】
- `repos/` の受け渡し（スナップショットと patch。未検証）: `remote` の type と `dev-env` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` が `_noai/final/` の人の変更を上書きする件（2026-10-18 の通しで未試験）: 正本の宣言と上書き前の警告を、次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
