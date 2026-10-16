# dotfiles-boundary: 現在状態（正本）

更新: 2026-10-15。状態の写しをほかに置かない。決定は `decisions.md`。

## 状態

方針（`decisions.md`）と、workbase 側の洗い出し（`notes/dotfiles-boundary-inventory.md`、44 ファイル）まで。**workbase にも dotfiles にも、まだ何も反映していない**。dotfiles の中身はモバイルから読めないので、dotfiles 側は PC で確認する。

## 項目

| # | 項目 | 状態 | 場所 |
|---|---|---|---|
| 1 | 要判断4つの確認（下の「あなた待ち」） | 未 | どこでも |
| 2 | dotfiles から workbase への参照の洗い出し | 未 | PC |
| 3 | 手順書3本（win11 / debian-family / fonts-setup）を dotfiles へ移す | 未 | PC |
| 4 | workbase の規則・索引を直す | 未 | PC |
| 5 | 「割る」「削る」 | 未 | PC |
| 6 | 線と一方向の規則を exmem に残す | 未 | どこでも |

手順の詳細は `notes/dotfiles-boundary-procedure.md` の同じ番号。

## あなた待ち

1. 手順書の移動先。案: dotfiles の `docs/setup/`（既存の `windows/claude/README.md` の置き方と合わせるかは PC で見る）。
2. `guides/AGENTS.md` の手順書の書式・文体の規則を、残すか dotfiles へ移すか。案: 移す。
3. 「割る」の4ノート。案: `pc-setup-manuals` と `zed-dotfiles` は割る、`shell-command-usecases` の種の正本は dotfiles へ、`obsidian-vault` は削るだけ。
4. `docs-rules.md` の push の対象外の理由。案: 「public 前提で扱うため、push の前に人が確認する」に書き換え、対象外は維持（kit の変更）。

## Next Actions

1. 要判断の4つを1つずつ確認する（モバイル可）。
2. PC で 2 → 3 → 4 → 5 → 6 の順に進める。dotfiles の push はエージェントが行わず、コマンドを報告する。

## 完了の条件

1〜6 が済む。そのとき、このディレクトリを削除し、`topics-index.md` の行を消す。
