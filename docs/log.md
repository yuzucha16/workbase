# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。2026-10-19 に整理した（整理前の全文は `log-history.md` の同日の項）。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-10-20 | 定例 | daily の振り返り（毎営業日。`start 改善4`。規模は `retrospective-method.md` の v6: 3章・500字） | ユーザー |
| 2026-10-26 | 定例 | weekly の振り返り（毎週月曜。4章・1,000字）。仮決めの期限切れを数える（R-05） | ユーザー |
| 2026-10-26 | 定例 | monthly の振り返り（最終営業日を含む最後の5営業日の初日。5章・1,500字）。初回は材料の weekly が1回だけ。次は 11-24 | ユーザー |
| 2026-10-25 | 単発 | 保留中の Open Questions 2 件（Stop フックの記録の置き場、`token-matrix.md` の観点） | ユーザー |
| 2026-10-26 | 単発 | 振り返りの手順書 v6（v5 の続き）の仮決め。定例の初回で字数を測る（項目 5） | ユーザー |
| 2026-11-02 | 単発 | `remote` の type の要否（項目 10 の後） | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |

## 状態

- 経路は整備済み: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`。cwd はリポジトリのトップだけ。フックの権限は `hooks.md` の「領域とフックの権限」が正本。
- 仕組みの決定は `review 消化` の3段で承認する（`approval-screening.md`）。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`（変更・調査1・調査2・振り返り1）。作り方は `exmem/lessons/method-creation.md`、改善の記録は `topics/kit-growth/records/`。
- room（`workflow-kit/room/`）: 実機の通しは済み（2026-10-18）。Ubuntu 26.04 の部屋（`init`）、`data:` の none / mask / restore、`room shell` と Node の流れは、実機で確認済み（ユーザー、2026-10-19）。`room init` の `wsl --install` の早戻りは、次に再現するまで保留（`log-history.md` の同日の項）。`room aws-key` は、10-20 に原因（`sh -c` の引数経路で代入した変数が空になる）を直し、PC1 で動作を確認した（`08202a7`）。
- 計画のやり方（6R → 憲章 → 成果物 WBS → マイルストーン）: トピック `topics/planning-method/`（Project 型。状態は同 `docs/log.md`）。下書きは `workflow-kit/` には未反映で、3層の前（2026-10-19）。試行の元ファイルは Project の共有フォルダ `notes/planning-method/`（クラウド側の控え。PC 環境からは見えない）。測ったことは `topics/kit-growth/records/planning-method-record.md`。

## Next Actions

2. `data:` の残り（旧 42）: ① `data: mask` の pptx・txt の実データの確認は、別セッションで行う。② Area 共通のマスク表の置き場を `areas/<Area>/_noai/` で試す（仕様は足さない。Area の README には語を書かない）。10-20: `areas/office/_noai/mask-common.toml`（語なしの雛形）を置いた。番号は mask.toml の記載順に振られるので、共通表をコピーして固有語は各種類の節の末尾に足せば、Project 間で番号が揃うことをダミーで確認した（先頭に足すとずれる）。残り: ユーザーが実在の語を書き、新しい Project でコピーして使う。
3. room の実機の確認の残り（旧 39）: ① 実データで `mask` の警告量 ③ `base_stale` ⑤ `restore` が `mapping.json` の欠け・食い違いで止まるか ⑧ 部屋の AI が `stock` の下書きを書けるか。共有知の送付のサイズ（1.5MB、120 ファイル）は、増えたら測り直す。
4. room の改善 3 件の実機確認（旧 37。10-19 に実装、テストは `CaCertTest` の 2 件（`openssl` 無し）以外 OK）: ① `ROOM.md` の指示で、AI が `⟦CUST_nnn⟧` を書かなくなるか ② `room start` で信頼の確認が出ないか。`~/.claude.json` の `projects["/mnt/room/<名>"].hasTrustDialogAccepted` が効くか ③ `reap` が `-home-ai` の残りを警告するか。
5. 振り返り（旧 38、15、13）: v5 の材料集めは AI 作業部屋の回を初実行として数えた（ユーザーが読んで比べる）、週次の使い方（引き継ぎは 10-26 の週次で）、改善5 の品質チェック3回。改善4 は 10-20 に定例化し、規模の Must を足した（v6。`decisions.md` の同日の項）。定例の初回（daily 10-20、weekly と monthly 10-26）で、字数が収まったかを `retrospective-method-record.md` に足す。
6. 暫定の数値（旧 24）: 続ける・切るの約10万 / 約2万トークンを、本物のフック列で3回以上再実験する（`~/claude-records/<フォルダ名>/sessions.jsonl` の記録を集計する）。Stop フックの費用記録（旧 29）は、Zed を使う PC で動作を確認した（10-19。dotfiles の `settings.json` のコマンドは `python "$HOME/.claude/hooks/stop-record.py"`）。`replies/<日付>.md` が 0 バイトだった件は、原因を特定して直した（10-19）: 環境変数 `PYTHONIOENCODING=utf-8:surrogateescape` の下で、標準入力に不正なバイトが入ると、書き込みで例外になり空ファイルだけが残る（lone surrogate で再現）。書き込みの `open` に `errors="replace"` を足した（実機で確認済み: 同日 `replies/2026-10-19.md` に 16 KB が入った。`stop-record.py` は、この PC では `~/.claude/hooks/` と共有フォルダ（`_sharedai`）にあり、公開の dotfiles（`main`）には無い。Zed の PC に置いた版にも同じ修正が要る）。
7. 使いながら確かめる（旧 8）: 「変更のやり方」の最初の業務での使用。（領域 × r/w 表と部屋の `wrap` の差し替えは机上の点検で閉じた。`user-manual.md` の補正策は、帰属の分離と承認の添え書きを kit に反映した。10-19）
8. 計画のやり方の取り込み（2026-10-19）: 取り込みの手順と、取り込み前に閉じる未決 3 件（決定済み）は、`topics/planning-method/docs/log.md` の Next Actions に移した（2026-10-20）。
9. ルールが見つかりにくい構造（2026-10-20）: works で `.bat` を作った AI が、dotfiles と exmem にあった ASCII ルール（2026-10-06）に届かず、`chcp 65001` で崩れた。ルールは `exmem/lessons/shell-script-testing-wsl.md` の後ろの追記節にあり、索引の1行に `.bat` の語が無く、dotfiles の `AGENTS.md` にも無かった。索引に語を足したのは補修で、恒久対策ではない。exmem の肥大化（大きいノートの後ろの追記節、索引の1行では引けない）と合わせて、領域全体の論点として議論する: 知識がどこにあれば、作業の最中に届くか（索引、ノートの分け方、作業側の `AGENTS.md` への写し、検索の仕組み）。議論の前に、似た見落としが他にもあるかを数える材料を集めてよい。ユーザーの指示（2026-10-20）。なお `.bat` は、暫定で全体 ASCII を正にし、cp932 の `.bat` と試験はやらない（cp932 の内容は lesson の草稿・優先度低。dotfiles は変更しない）。

10. `room rename-area`（2026-10-20 実装、単体テストのみ）の実機確認: 実際の `areas/` で改名し、`room init <新>` で部屋を作り直して `start` が通るか（来歴チェック、リンク）。旧の部屋 `room-<旧>` は手で `wsl --unregister`。

## Open Questions

- Stop フックの記録の置き場: 既定は `~/claude-records/`。部屋の中だけ `ai/records/` にするか。実機確認（Next Actions 6）の後に決める。【保留 〜2026-10-25】
- `remote` の type: 要否は項目 `dev-env` の実使用（Next Actions 7）の後に決める。【保留 〜2026-11-02】
- `repos/` の受け渡し（スナップショットと patch。未検証）: `remote` の type と `dev-env` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` が `_noai/final/` の人の変更を上書きする件（2026-10-18 の通しで未試験）: 正本の宣言と上書き前の警告を、次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
- `token-matrix.md` と `review` の入力 5: 第5の観点「温存」を足し、入力 5 を「TTL を超えて空いた後の書き込み量」に変えるか。今の役目の引き継ぎと基準値 103 の再設定を付け、分割して出し直す。【保留 〜2026-10-25】
- `workflow-kit/room/room.py` / `Wsl.push`（`sh -c` の引数経路）は、代入した変数を含むスクリプトを渡すと、空に展開されて壊れる。規則は `exmem` にあったが、10-14 に続き 10-19 に再発した / 案: `push` の入口で、スクリプト内の代入（`name=`）を検出して `RoomError` にするか、関数の説明文に規則を書く。AI の提案で、未承認。`push_shared` は代入を使わないので影響なし。
- `workflow-kit/` / 計画のやり方（`start 計画`。6R → 憲章 → 成果物 WBS → マイルストーン）の取り込み / 案: `topics/planning-method/planning-method-draft.md` の骨子を、`workflow-kit/` の新ファイルと `methods.md` の新区分「計画」に、試験運用で昇格する。ユーザーの決定（2026-10-19）は `topics/planning-method/docs/decisions.md` に書いた。先行する決定: `start` の引数つきモードは試験運用（`docs/decisions.md` 2026-10-16）。`start` のインタビュー・`open`・基準文書・改善4は触らない。3層（`approval-screening.md`）を通すまで未反映。6R 自体は3層に乗せない。
- `exmem/lessons/retrospective-method.md`（改善4）/ 振り返りに計画（6R → 憲章 → WBS → マイルストーン）を入力として足す / 案（ユーザーが 2026-10-20 にカードで選択。5点）: ① 計画は評価の対象でなく**基準**にする（憲章の目標とマイルストーンを計画とし、実績との差を見る。計画づくりの出来は `planning-method-record.md` で測る）。② **weekly から**（初回 10-26。daily と monthly は変えない）。③ 比べるのは**ユーザーが承認した計画だけ**。無ければ「計画なし」と1行。④ 承認した憲章・WBS・マイルストーンは repo の **`topics/kit-growth/plans/`** に置く（kit の題材に限る。実務の題材は Project の `ai/in/`）。⑤ **字数は据え置き**（4章・1,000字）。目標の行は憲章から取り、章 3 の頭に 計画 / 実績 / 差 / 所在 の表を置く。先行する決定: 取り込みの論点 B4「改善4は触らない」（2026-10-19、`topics/planning-method/docs/decisions.md`）を変える。v6 の規模は【仮 〜2026-10-26】。出どころ: `topics/kit-growth/inbox.md` の 10-19「振り返りは計画とセットにする」。10-26 の weekly の前の `review 消化` で判断する。
