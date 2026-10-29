# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `logbook/` の型を 2026-10-26 に決め（7 点、`decisions.md`）、`logbook/README.md` と `find_knowledge.py --check-aging` を入れた。`exmem/lessons/` の 6 ファイルに版依存の印を付けた（78df71b）。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は ①時系列の観測・測定、②版・時点に縛られる事実、③試行の途中。個人の好み・1 回きりの構成記録は含めない。
- ② は移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。降格するのは ①③ だけ。判断は 3 段チェック（確認の単位はファイル、降格と印の単位は節）。
- 第1〜3陣の本文確認と、畳み候補の「済」「聞」「前」の処理は済み。2026-10-29 に「残」のうち、claude-code-storage の旧キーの OQ/NA と obsidian-vault-backup の `10_env.bat` の NA を閉じた。
- `logbook/` へは、README と、親の lessons からの wikilink で 1 ホップで着く（2026-10-29 に確認）。`triggers:` は付けていない（対象外）。

## Next Actions

1. 畳み候補の残り: room の OQ 4 項（マウントの可視性、プリンタ設定、マスクから復元までの通し、pptx。2026-10-27 の「9 項完了」に含まれないと、ユーザーが 2026-10-29 に回答）。obsidian-vault-backup の NA 2 項（WSL の張り直し〔`GHQ_ROOT` は WSL の中で確認〕、`vault-backup.bat` 〔未了のまま残す〕）。実機でしか確かめられない。
2. `--check-aging` の FAIL 1 件: `logbook/user-thinking-habits.md` が budget 32KB を 40 バイト超過（他の 4 本は合格）。圧縮か budget の付け直しは 2026-11-29 の月次で決める。
3. `logbook/` を `--triggers` の対象にするかは、2026-11-08 の引当率の測定（`topics/md-link-graph/` NA 1）の後に判断する。入れるなら、出力に「版・時点依存」「確認日」を付ける案がある（`--check-aging` の仕組み）。
4. 試行: 2026-11-29 の月次の振り返りで、週次の記録(`kit-growth/records/`)を 1 回手で畳む(置き場は変えない)。
5. 追記の型 (b)（OQ・NA を本体に 1 つ）の実施: 次の lessons 追記から。既存ファイルの直しは `review 消化` で。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか（品質ブレの懸念あり）。Next Actions 3 で判断する。

### 待ち行列

空。
