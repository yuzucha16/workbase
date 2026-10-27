---
type: knowledge
title: Windows の 8.3 短縮名で relative_to が失敗するのを避ける
status: active
tags:
  - tool/wsl
  - shell
  - testing
  - windows
aliases:
  - windows-8dot3-relative-to
triggers: [8.3, 短縮名, relative_to, resolve, テスト, PC1 だけ失敗, Path, 短いパス]
created: 2026-10-21
updated: 2026-10-27
sources:
  - Claude Code conversation "room のテストが PC1 だけ失敗する件" (2026-10-21)
---

# Windows の 8.3 短縮名で relative_to が失敗するのを避ける

全体の方針は [[shell-script-testing-wsl]]（2026-10-27 に、追記の節を切り出した）。

## Windows の 8.3 短縮名で `relative_to` が失敗するのを避ける（2026-10-21 追記）

同じコミットで、ある PC ではテストが通り、別の PC では `relative_to` の `ValueError` で落ちた原因と、外部コマンドに依存するテストの扱い。

### Principles（パスとテスト）

- パスの包含判定（`relative_to`）や比較は、両側を同じ方法で正規化（`resolve()`）してから行う。理由: 一方が8.3短縮名、他方が長い名前だと、同じ場所でも文字列が一致せず失敗する。
- 環境ごとに結果が違うテスト失敗は、仮説を立てる前に、失敗した PC のトレースバックを取る。理由: 通る環境では再現せず、原因はパスや外部コマンドなど環境側にあることが多い。
- `PATH` 上の外部コマンド（`openssl` など）に依存するテストは、`skipUnless(shutil.which(...))` で、無い環境ではスキップにする。理由: 環境の都合による失敗が、コードの退行と見分けられなくなる。

### Decisions（パスとテスト）

- **表示用の相対パスは、両側を `resolve()` してから `relative_to` する**（2026-10-21）
  - 根拠: ユーザーが原因の修正を依頼し、テストが通る形になった。
  - 却下案: テスト側の一時ディレクトリだけを `resolve()` する（本体コードが同じ状況で落ちる）。
- **`openssl` が無い環境では CA 証明書のテストをスキップにする**（2026-10-21）
  - 根拠: ユーザーが「skip にしてほしい」と指示した。
  - 却下案: テストで証明書を Python だけで作る（作り直しが大きく、今回は求められていない）。

### Facts（パスとテスト）

- `tempfile` の一時ディレクトリは、ユーザー名が長い PC では8.3短縮名（`~1` を含む形）で返り、`Path.resolve()` は長い名前に展開する（確認: 2026-10-21、根拠: 失敗した PC のトレースバックで、片方が短縮名、もう片方が長い名前だった）。
- 修正後、失敗した PC でスキップを含む全テストが通った（確認: 2026-10-21、根拠: ユーザーの報告）。
- 修正前に、ユーザー名が短い PC では同じテストが通っていた（確認: 2026-10-21、根拠: ユーザーの報告と、別の PC での実行）。
- 実物にも反映されている: `room.py` の相対パスの表示は `Path(ctx.vault).resolve()` を使い、`test_room.py` の CA 証明書のテストは `skipUnless(shutil.which("openssl"), …)` が付いている（確認: 2026-10-21、根拠: `room.py` と `test_room.py` を検索した）。

### Gotchas（パスとテスト）

- 状況: `ctx.vault`（短縮名）と、そこから別の経路で作ったパス（長い名前）に `relative_to` を使った
  - 原因: 同じ場所を指しているのに、文字列の接頭辞が一致しない
  - 解決: 両側に `resolve()` をかけてから `relative_to` した

### Open Questions（パスとテスト）

- 同じ原因で落ちる `relative_to` の呼び出しが他にもないか、他の `Path` の組み合わせも点検するか。

### Next Actions（パスとテスト）

- テストを複数の PC で回して、環境差で落ちるものが残っていないか確認する。

## Related

- [[shell-script-testing-wsl]]
