# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認と置き場の実測、Vault 2 分割の両 PC 確認を済ませ、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用し、eg1（Web）の実験で構造を直した。同日、Marp・Slidev・Quarto の実機比較も済んだ（`records/2026-11-04-slide-tools-live-compare.md`）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【期日 11-11、起票 11-04】`inv` の工程別構造の実験 eg2（社内の Excel・テキスト。マスクの差分）を、別セッションで行う。結果は `records/` に残し、構造を直す。
- 【期日 11-11、起票 11-04】`init` に Marp CLI（`marp-cli@4.5.1`、版固定。ユーザー承認済み 11-04）の段を足す（`mmdc` と同じ型）。要点: ①`room-chrome` を指す `--browser-path` の薄い包み（`/usr/local/bin` に置き、`ai` が呼べる）、②標準入力を読むので呼ぶ側は `</dev/null`、③root が `PUPPETEER_SKIP_DOWNLOAD=1 npm i -g` で入れる。`INIT_STEPS`（`room.py`）にも段名を足す。単体テストと、部屋への `--only` での実機確認まで。Slidev は入れない。
- 【期日 11-11、起票 11-04】比較の結果（`records/2026-11-04-slide-tools-live-compare.md`。結論: pptx が成果物なら、お手軽は Marp 既定、初版を人が直すなら Quarto。Slidev は HTML 発表が主のときだけ）を `topics/office-output-types` に渡す。
- 【人・期日 11-05、起票 11-04】部屋に残る Slidev を root で消す（下記）。`~/cmp` は消した。

```
wsl -d room-myenv -u root -- bash -c 'npm rm -g @slidev/cli && rm -rf /usr/local/lib/node_modules/@slidev'
```

## Open Questions

- `inv` の基準文書は仮決めのまま（11-04 ユーザー「仮決めのままでよい」。見直しの期日は置かない）。
- Quarto の見た目を整える `reference-doc`（社内テンプレート）は、`topics/office-output-types` 側の論点。
