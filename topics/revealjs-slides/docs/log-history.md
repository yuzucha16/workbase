# 経緯（log-history）

## Log

### 2026-11-06 トピックを作成し、PC1 の写真から書き起こす
- PC1 の room stock の内容（ノート 3 枚、`layouts.qmd` 8 枚）が写真で `exmem/inbox/` に来た（フォルダ 2 つ、約 5MB × 11）。
- 写真を読んで、ノートは `records/2026-11-05-revealjs-diagram-layout-note.md`、CSS は `records/revealjs-diagram-theme.scss`、見本は `records/revealjs-diagram-layouts.qmd` に書き起こした（見本の繰り返しは生成スクリプトで作った）。
- Windows の Quarto 1.11.9 で render し、Edge ヘッドレスで撮った 6 枚を目視。崩れなし。
- 命名の意見: 型は `*-output`（`exmem/lessons/` の流儀）。部品（見本・CSS）は lessons に入れず、トピックの `records/` に置く案。
- 写真フォルダの削除は、自動判定で拒否された。ユーザーに依頼。
- 統合（11-06）: ノートを `exmem/lessons/revealjs-diagram-layout-output.md` に統合（新規）。タグ 4 つ（tool/quarto、tool/revealjs、slides、diagram）を `tags.md` に追加。書き起こしノートは削除。写真フォルダはユーザーが削除。
- room での確認（11-06）: `room-myenv` に見本を `/tmp` で render（Quarto 1.11.9、Chromium 1248、マウントなし）。7 枚、同じ見え方。部屋の Chromium は `--no-sandbox` `--disable-dev-shm-usage` が要る。シェル変数は `wsl -- bash -c '...'` の中で展開されず、スクリプトを base64 で渡して実行した。アイコン定義を `include-before-body` に出す案を Windows で試験し、通った。push は `fcd1e93` まで（別セッションの `fc51744` は除く）。
