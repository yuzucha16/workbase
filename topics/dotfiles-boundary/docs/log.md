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
| 4 | workbase の規則・索引を直す | 済（2026-10-16。`docs-rules.md` は不要でクローズ） | PC |
| 5 | 「割る」「削る」 | 済（2026-10-16。`pc-setup-manuals` と `zed-dotfiles` を割り、約19件を削った。`scripts/wsl` の改名の決定は dotfiles の `docs/decisions.md` へ移した） | PC |
| 6 | 線と一方向の規則を exmem に残す | ほぼ済（2026-10-16。`app-config-placement` の Principles に追記。ルートの `AGENTS.md` に1行足すかだけ、ユーザー確認待ち） | どこでも |

手順の詳細は `notes/dotfiles-boundary-procedure.md` の同じ番号。

## あなた待ち

1. ~~手順書の移動先~~ 決定済み: dotfiles の `docs/setup/`。
2. ~~書式・文体の規則の置き場~~ 決定済み: workbase の `guides/AGENTS.md` に1か所だけ残す（案 A）。
3. ~~「割る」の4ノート~~ 決定済み（2026-10-16、`decisions.md`）。割るのは `pc-setup-manuals` と `zed-dotfiles`、`obsidian-vault` は削るだけ、`shell-command-usecases` は exmem が正本のまま（割らない）。
4. ~~`docs-rules.md` の push の理由~~ クローズ（2026-10-16）。kit の push の規則は更新済みで、書き換え不要。

判断 1・2 も決定済み（`decisions.md`）。判断 2 は、`guides/howto/` に `ai-room-setup.md` などが残るため、書式規則は workbase の `guides/AGENTS.md` に1か所だけ残す形（案 A）に修正した。dotfiles の `docs/setup/README.md` は固有の規則と参照だけ。

## Next Actions

1. ルートの `AGENTS.md` の「共有の範囲」に、1行を足すかをユーザーに確認する（案: 「dotfiles の挙動（スクリプトの中身・配置）をこのリポジトリに書かない。名前とリンクで指す」）。
2. 確認が済んだら、このディレクトリを削除し、`topics-index.md` の行を消す（完了の条件）。

## 完了の条件

1〜6 が済む。そのとき、このディレクトリを削除し、`topics-index.md` の行を消す。
