# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。2026-10-19 に整理した（整理前の全文は `log-history.md` の同日の項）。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-10-21 | 定例 | daily の振り返り（毎営業日。`start 改善4`。規模は `retrospective-method.md` の v6: 3章・500字） | ユーザー |
| 2026-10-26 | 定例 | weekly の振り返り（毎週月曜。4章・1,000字）。仮決めの期限切れを数える（R-05） | ユーザー |
| 2026-10-26 | 定例 | monthly の振り返り（最終営業日を含む最後の5営業日の初日。5章・1,500字）。初回は材料の weekly が1回だけ。次は 11-24 | ユーザー |
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
- room の pwsh 7 と ps1 の静的チェッカー（2026-10-21）: 束ねる役も ps1、bat は起動用の 3 行だけ（`dev-deliverable-guide.md`、`room-context.md`）。`init` が pwsh 7.6.7・PSScriptAnalyzer・Pester 5 を root で入れ、`workflow-kit/tools/check-ps1.ps1` が点検する。方針「部屋で完結できるなら部屋で実行する。Windows 依存部は小さな層にする」も `dev-deliverable-guide.md`（節「実行の方針」）と `ROOM.md` に書いた。部屋（26.04）に入っていることは確認済み。決定は `decisions.md` の同日の項。
- room の Area を跨ぐ共有知（2026-10-21）: `room pull`（Area の `knowledge/` から条件で絞り、`_noai/raw/area/` へ）と、`restore` の Area 書き出し（`ai/out/knowledge/` → `areas/<Area>/knowledge/`。人が変えた既存ファイルがあれば止まる、`--force` で上書き）を実装し、実機の通しで問題なし。統合は部屋の作業（works の AI は実名を読まない）。手順は `guides/howto/ai-room-setup-script.md` の 4.1・6.1、理解は `guides/explain/cross-area-shared-knowledge.md`、決定は `topics/private-knowledge/docs/decisions.md`。
- room の `start` の自動コミットと部屋の git（2026-10-21、`df4ff0d`）: `start` は回収の後に既定でコミットする（`--no-commit`）。部屋に、ローカルの git（`/home/ai/gitdirs/<Project>`、回収で捨てる）と `git` のラッパーを用意する。単体テストのみ。実機は未確認。決定は `decisions.md` の同日。
- room の準備と異常処理（2026-10-21、`efc091c` `756d1bc`）: 置き場（`knowledge/`、`ai/docs/inbox.md`。のちに `deliverable/` `source/` も）は `init` が無ければ作る。後続の `pull` `restore` `close` は、置き場が無ければ作らず、復帰もせず、何も変えずに止まって `room init <Area>` を示す（一本化の方針）。単体テストのみ。止まる型になっていない手作り物が残っていないかの見直しは未了。決定は `decisions.md` の同日の項。
- room のコミットのトレーラー（2026-10-21）: `init` `open` `rename-area` `start` `readme` `close` のコミットに `Room-Op` / `Room-Rev` / `Room-Area` / `Room-Project` を付ける（`room/README.md`、決定は `decisions.md` の同日の項）。`Room-Rev` を基点に `git diff <Room-Rev>..HEAD -- workflow-kit/room` で、既存の Area / Project に対する room の変更を確認できる。`restore` / `pull` の版は未記録。実機での確認は未実施（単体テストのみ）。room の単体テストは PC1 でスキップを含む全件パス（10-21。短縮名の不一致を直し、`openssl` が無い環境では CA のテストをスキップ。`9a9c8d2`）。
- room の並行 start（2026-10-21）: 同じ Area の Project を、同じ部屋に同時に `start` できる（既定。止まるのは自分の Project のマウントが残っているときだけ）。共有ファイル（`~/shared`、git のラッパー、信頼・許可の設定）は置き換え方式で更新する。単体テストのみ（全 105 件パス）。決定は `decisions.md` の同日の項、使い方の約束は `room/README.md`。
- 計画のやり方（6R → 憲章 → 成果物 WBS → マイルストーン）: トピック `topics/planning-method/`（Project 型。状態は同 `docs/log.md`）。2026-10-20 に試験運用で `workflow-kit/` に取り込んだ（`start 計画`、`start-plan.md`）。次は PC1 の品質チェック3回。試行の元ファイルは Project の共有フォルダ `notes/planning-method/`（クラウド側の控え。PC 環境からは見えない）。測ったことは `topics/kit-growth/records/planning-method-record.md`。
- 計画と部屋の紐付け（2026-10-21）: `start 計画` の出力を、`room init` / `room open` が作る Area・Project の README に関連させる議論を、トピック `topics/plan-room-link/`（Project 型）で始めた。状態は同 `docs/log.md`。

## Next Actions

11. room の変換の道具: `room run`（v2）の実装は、ユーザーが時期を見て依頼する。仕様の叩き台は、決定と `guides/explain/ai-room-convert-tools.md` の 7 章。（① PC1 での `init` の確認、② PlemolJP を戻す時期は、完了または依頼待ちのため削除。ユーザー、10-21）
5. 振り返り（旧 38、15、13）: v5 の材料集めは AI 作業部屋の回を初実行として数えた（ユーザーが読んで比べる）、週次の使い方（引き継ぎは 10-26 の週次で）、改善5 の品質チェック3回。改善4 は 10-20 に定例化し、規模の Must を足した（v6。`decisions.md` の同日の項）。daily 10-20 は済み（第2回 470字、第3回 495字。空白を除く。含めると超える。数え方は 10-26 に決める。施策 R-2026-10-20-01・02 は承認待ち）。weekly と monthly（10-26）で、字数が収まったかを `retrospective-method-record.md` に足す。
9. ルールが見つかりにくい構造（2026-10-20）: works で `.bat` を作った AI が、dotfiles と exmem にあった ASCII ルール（2026-10-06）に届かず、`chcp 65001` で崩れた。ルールは `exmem/lessons/shell-script-testing-wsl.md` の後ろの追記節にあり、索引の1行に `.bat` の語が無く、dotfiles の `AGENTS.md` にも無かった。索引に語を足したのは補修で、恒久対策ではない。exmem の肥大化（大きいノートの後ろの追記節、索引の1行では引けない）と合わせて、領域全体の論点として議論する: 知識がどこにあれば、作業の最中に届くか（索引、ノートの分け方、作業側の `AGENTS.md` への写し、検索の仕組み）。議論の前に、似た見落としが他にもあるかを数える材料を集めてよい。ユーザーの指示（2026-10-20）。なお `.bat` は、暫定で全体 ASCII を正にし、cp932 の `.bat` と試験はやらない（cp932 の内容は lesson の草稿・優先度低。dotfiles は変更しない）。

12. 会議録のナレッジ化（`topics/private-knowledge/` は 2026-10-21 に閉じた。決定は `decisions.md` の同日の項）の残り: ① 統合の手順書の整備（部屋の AI に統合させる指示 =「`ai/out/knowledge/` に `kind: integrated` で書く」を `room-context.md` か手順書に固める。いまは `guides/howto/ai-room-setup-script.md` の例だけ）② 型・理解ガイドの型の整理と改善は別セッション（ユーザーの指示、10-21）③ 指標（冒頭の行数の上限〔仮 10 行〕、人が直した箇所の数）は、使いながら測る（実機で「完了」の報告はあったが、数字は未記録）。
13. 題材ごとのトピックと `records/` の仕訳（仮決め 〜2026-10-28。`decisions.md` の同日）: 今は `planning-method/` が同じ構造で運用している（`usage-viz/` `stock-modes/` `private-knowledge/` は 10-21 に閉じた。`usage-viz` の HTML の見た目はブラウザで未確認。`start 計画` へのフィードバック案8件は `topics/planning-method/planning-method-feedback-stock-modes-m1.md`、`review 消化` で承認）。10-28 に正式化するかを `review 消化` で決める。
14. room の Area の置き場の設計（2026-10-21）: `data:` 廃止の次。知識置き場は `areas/<Area>/_noai/knowledge/` に移した（`decisions.md` の同日）。`_noai/source/` と `pull --from source` も実装した（単体テストのみ）。`_noai/deliverable/`（`ai/out/deliverable/` → Area）も実装した（単体テストのみ）。残り: ① 旧 `areas/pilot2/knowledge/`（試験用のダミー。未追跡。ユーザーが移す）② 実機で `data:` なしの `open`（`mask.toml` のひな形つき）/ `start` / `restore` と、`source` → `pull` → `restore` → `deliverable` の通しを確かめる ③ 部屋の AI に渡す文書へ、成果物を `ai/out/deliverable/` に置く案内を足すか確かめる ④ `guides/explain/cross-area-shared-knowledge.md` の設計の軸（「戻り」「統合」）を、新しい置き場の分け方に合わせる（`exmem/inbox/2026-10-21-area-data-layout-flow.md` を `integrate` するときに整合）。
18. 【起票 10-21】部屋の Stop フックの記録を `ai/records/` に置く実装（`decisions.md` の同日。案 B）: ① `init` が部屋に Stop フックを置き、`sessions.jsonl` と `replies/` を Project の `ai/records/` に向ける（今の `room.py` には無い）② 記録するとき Windows のユーザー名入りのパス（`C:\Users\<名>`、`/mnt/c/Users/<名>`）を `%USERPROFILE%` に置換する（ユーザーの承認 10-21。懸念: 部屋の AI が Windows のパスを出し、pwsh スクリプトの引数にユーザー名が入った。原因は次に再現したときに追う）③ `~/claude-records/room/` の 9 本が、部屋の中から書かれたものか、Windows 側かを確かめる ④ マスクの規則（`mask-spec.md` は `ai/records/` を追跡する）と矛盾しないか。

## Open Questions

- 会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。`private-knowledge` を閉じるときに移した。
- Windows の実行先に Python（または uv）があるか（2026-10-21。言語の優先順位は Python → ps1 → bat に決まった。この答えで、Windows 側の薄い層を Python にできるかが変わる）: あれば、`dev-deliverable-guide.md` の「実行の方針」の Windows 依存の薄い層を ps1 でなく Python にでき、`check-ps1.ps1` に相当する Python 側の点検が要る。今は薄い層を ps1（pwsh 7 は会社の PC で使えることを確認済み）にしている。
- `room init --only changed`（2026-10-21）: 既存の部屋に、足された段だけを自動で入れる案。`Room-Rev`（トレーラー）から現在の版までの `room.py` の差分で、変わった段を選ぶ。段と変更箇所の対応表が要る（今は人が差分を見て `--only` に渡す）。`--only` の実機での使い心地を見てから決める。
- `stock-hook.md` の手順「既存の知識と重なるか確認する」/ 理解のとき、近い既存ガイドが新しい内容で古くなる場合の扱いが曖昧（`stock-explain.md` は「同じテーマがあればメモを作らず報告」とだけ書く）。案: テーマが違うなら作り、既存ガイドの更新が要る点は、メモの「要確認事項」に書く（2026-10-21 は、この形で作った）。

- 計画と部屋の README の紐付け（2026-10-21。`topics/plan-room-link/`）: 場所 = `workflow-kit/room/room.py`（`cmd_start`、`README_TEMPLATE`）、`workflow-kit/templates/project/README.template.md`、`start-plan.md`、`room-context.md`、`room/README.md`、`exmem/lessons/planning-method.md`。問題 = `start 計画` の出力が README に結び付いていない。承認（`start --adopt`）のたびに手で README を直すと漏れる。案 = 部屋の AI が計画と一緒に `ai/work/plan/readme-block.md` を書き、人が `ai/in/plan/` に置いて `--adopt` したとき、`room start` が README の印つきの節「計画」だけを機械的に差し替える。Area の README と `open-hook.md` と `close` の雛形チェックは変えない。論点 1〜6 の仮決めと変更先の一覧は `topics/plan-room-link/plan-room-link-issues.md`（4 章）。スクリーニングの注意: 論点 6 件を 1 承認にまとめると型 D。2026-10-19 の「`open` は触らない」の見直しを含む（`open` 自体は変えない）。

- 【案件】の行き先: `para-operations`（2026-10-07）は Area の `docs/decisions.md`、実装（2026-10-14）は Area の `ai/docs/inbox.md`。現行はどちらか（`topics/private-knowledge/` の確認 #2）。
- `remote` の type: 要否は項目 `dev-env` の実使用（済み。10-20 にユーザーが業務で使った）を踏まえて決める。【保留 〜2026-11-02】
- `repos/` の受け渡し（スナップショットと patch。未検証）: `remote` の type と `dev-env` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` が `_noai/final/` の人の変更を上書きする件（2026-10-18 の通しで未試験）: 正本の宣言と上書き前の警告を、次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
