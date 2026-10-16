# dotfiles-boundary: 現在状態（正本）

更新: 2026-10-16。状態の写しをほかに置かない。決定は `decisions.md`。

## 状態

方針（`decisions.md`）と、workbase 側の洗い出し（`notes/dotfiles-boundary-inventory.md`、44 ファイル）に加え、2026-10-16 に手順書3本を dotfiles の `docs/setup/` へ移した（項目 3）。項目 4 は一部、5・6 は未。

## 項目

| # | 項目 | 状態 | 場所 |
|---|---|---|---|
| 1 | 要判断4つの確認 | 済（2026-10-16） | どこでも |
| 2 | dotfiles から workbase への参照の洗い出し | 済（2026-10-16。手順書の参照は直した。残りは許可された参照） | PC |
| 3 | 手順書3本（win11 / debian-family / fonts-setup）を dotfiles へ移す | 済（2026-10-16。dotfiles `6f9cae5` を push 済み。workbase 側の削除は同日コミット） | PC |
| 4 | workbase の規則・索引を直す | 一部（`guides-index.md`・`guides/AGENTS.md` は済。残りは inventory の「直す」の表） | PC |
| 5 | 「割る」「削る」 | 未 | PC |
| 6 | 線と一方向の規則を exmem に残す | 未 | どこでも |

手順の詳細は `notes/dotfiles-boundary-procedure.md` の同じ番号。

## あなた待ち

1. 手順書の移動先。案: dotfiles の `docs/setup/`（既存の `windows/claude/README.md` の置き方と合わせるかは PC で見る）。
2. `guides/AGENTS.md` の手順書の書式・文体の規則を、残すか dotfiles へ移すか。案: 移す。
3. ~~「割る」の4ノート~~ 決定済み（2026-10-16、`decisions.md`）。割るのは `pc-setup-manuals` と `zed-dotfiles`、`obsidian-vault` は削るだけ、`shell-command-usecases` は exmem が正本のまま（割らない）。
4. ~~`docs-rules.md` の push の理由~~ クローズ（2026-10-16）。kit の push の規則は更新済みで、書き換え不要。

判断 1・2 も決定済み（`decisions.md`）。**判断 2 の食い違い**: `guides/howto/` には `ai-room-setup.md` と `bedrock-first-hello.md` が残る（空にならない）。そのため `guides/AGENTS.md` の書式・文体の規則は消さず、dotfiles 依存の部分だけ直した。`dotfiles/docs/setup/README.md` に規則の写しがあり重複している。全部移すか、残す側を1つにするかをユーザーに確認する。

## Next Actions

1. 判断 2 の食い違いを確認する。
2. PC で 2 → 3 → 4 → 5 → 6 の順に進める。dotfiles の push は、dotfiles の `AGENTS.md` の許可リストと `docs-rules.md` の「push」に従う。

## 完了の条件

1〜6 が済む。そのとき、このディレクトリを削除し、`topics-index.md` の行を消す。
