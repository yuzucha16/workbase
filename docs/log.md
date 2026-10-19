# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。2026-10-19 に整理した（整理前の全文は `log-history.md` の同日の項）。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-10-25 | 単発 | 保留中の Open Questions 2 件（Stop フックの記録の置き場、`token-matrix.md` の観点） | ユーザー |
| 2026-10-26 | 単発 | 振り返りの手順書 v5 の仮決め（項目 38） | ユーザー |
| 2026-11-02 | 単発 | `remote` の type の要否（項目 10 の後） | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |

## 状態

- 経路は整備済み: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`。cwd はリポジトリのトップだけ。フックの権限は `hooks.md` の「領域とフックの権限」が正本。
- 仕組みの決定は `review 消化` の3段で承認する（`approval-screening.md`）。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`（変更・調査1・調査2・振り返り1）。作り方は `exmem/lessons/method-creation.md`、改善の記録は `topics/kit-growth/records/`。
- room（`workflow-kit/room/`）: 実機の通しは済み（2026-10-18）。Ubuntu 26.04 の部屋（`init`）、`data:` の none / mask / restore、`room shell` と Node の流れは、実機で確認済み（ユーザー、2026-10-19）。`room init` の `wsl --install` の早戻りは、次に再現するまで保留（`log-history.md` の同日の項）。

## Next Actions

1. `room aws-key` を実機で通す。PC1 で、部屋の `~/.aws/credentials` への `touch` が `ai` で失敗する。原因は未特定。確かめる: `wsl -d room-<Area> -- sh -c 'id; echo $HOME; ls -ld $HOME $HOME/.aws; touch $HOME/.aws/credentials; echo $?'` の出力と `touch` のエラー文。手書きの `credentials` では、Zed の Agent の Bedrock 認証が通っている。（旧 40）
2. `data:` の残り（旧 42）: ① `data: mask` の pptx・txt の実データの確認は、別セッションで行う。② Area 共通のマスク表の置き場を `areas/<Area>/_noai/` で試す（仕様は足さない。Area の README には語を書かない）。
3. room の実機の確認の残り（旧 39）: ① 実データで `mask` の警告量 ③ `base_stale` ⑤ `restore` が `mapping.json` の欠け・食い違いで止まるか ⑧ 部屋の AI が `stock` の下書きを書けるか。共有知の送付のサイズ（1.5MB、120 ファイル）は、増えたら測り直す。
4. room の改善 3 件の実機確認（旧 37。10-19 に実装、テストは `CaCertTest` の 2 件（`openssl` 無し）以外 OK）: ① `ROOM.md` の指示で、AI が `⟦CUST_nnn⟧` を書かなくなるか ② `room start` で信頼の確認が出ないか。`~/.claude.json` の `projects["/mnt/room/<名>"].hasTrustDialogAccepted` が効くか ③ `reap` が `-home-ai` の残りを警告するか。
5. 振り返り（旧 38、15、13）: 手順書 v5 で材料を集め直す実行（10-26 か同じ入力）、週次の使い方、施策 02〜05 の承認、改善5 の品質チェック3回、改善4 の使用回数（2/3）。
6. 暫定の数値（旧 24）: 続ける・切るの約10万 / 約2万トークンを、本物のフック列で3回以上再実験する（`~/claude-records/<フォルダ名>/sessions.jsonl` の記録を集計する）。Stop フックの費用記録（旧 29）は、Zed を使う PC で動作を確認した（10-19。dotfiles の `settings.json` のコマンドは `python "$HOME/.claude/hooks/stop-record.py"`）。`replies/<日付>.md` が 0 バイトだった件は、原因を特定して直した（10-19）: 環境変数 `PYTHONIOENCODING=utf-8:surrogateescape` の下で、標準入力に不正なバイトが入ると、書き込みで例外になり空ファイルだけが残る（lone surrogate で再現）。書き込みの `open` に `errors="replace"` を足した（実機の次のターンで中身が入るか確認する）。
7. 使いながら確かめる（旧 8）: 「変更のやり方」の最初の業務での使用。（領域 × r/w 表と部屋の `wrap` の差し替えは机上の点検で閉じた。`user-manual.md` の補正策は、帰属の分離と承認の添え書きを kit に反映した。10-19）

## Open Questions

- Stop フックの記録の置き場: 既定は `~/claude-records/`。部屋の中だけ `ai/records/` にするか。実機確認（Next Actions 6）の後に決める。【保留 〜2026-10-25】
- `remote` の type: 要否は項目 `dev-env` の実使用（Next Actions 7）の後に決める。【保留 〜2026-11-02】
- `repos/` の受け渡し（スナップショットと patch。未検証）: `remote` の type と `dev-env` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` が `_noai/final/` の人の変更を上書きする件（2026-10-18 の通しで未試験）: 正本の宣言と上書き前の警告を、次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
- `token-matrix.md` と `review` の入力 5: 第5の観点「温存」を足し、入力 5 を「TTL を超えて空いた後の書き込み量」に変えるか。今の役目の引き継ぎと基準値 103 の再設定を付け、分割して出し直す。【保留 〜2026-10-25】
