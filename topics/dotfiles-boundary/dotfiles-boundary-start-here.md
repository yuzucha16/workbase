# 窓口: workbase と dotfiles の切り分け（dotfiles-boundary）

- 型: Project 型。完了条件: 手順書3本を dotfiles へ移し、workbase から dotfiles の挙動の写しを消し、線を exmem に残す。
- 何か: dotfiles は取り込まない。PC に置かれる・実行されるものは dotfiles、読まれるものは workbase。依存は dotfiles → workbase の一方向。理由は `docs/decisions.md`。

## いま

方針と workbase 側の洗い出しまで。どちらのリポジトリにも未反映。詳細は `docs/log.md`。

## あなた待ち

要判断 4（手順書の移動先、手順書の書式規則の置き場、「割る」の4ノート、`docs-rules.md` の push の理由）。中身は `docs/log.md`。

## 次の一手

要判断の4つを1つずつ確認する（どこでも）。その後は PC。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `notes/dotfiles-boundary-procedure.md`（PC での手順）、`notes/dotfiles-boundary-inventory.md`（ファイルごとの仕分け）

## リポジトリに無いローカルの状態

dotfiles 側は未確認（PC で `dotfiles` と workbase の両方を開ける場所で作業する）。
