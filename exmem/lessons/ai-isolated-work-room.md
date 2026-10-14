---
type: knowledge
title: AI に見せる領域を分ける: 作業部屋（専用 WSL）方式
status: active
tags:
  - security
  - harness
  - tool/wsl
  - ai/claude
  - para
aliases:
  - AI 作業部屋
  - AI スコープの分離
  - 許可リスト方式の隔離
created: 2026-10-13
updated: 2026-10-14
sources:
  - Claude Code conversation "AI に見せる領域の分離設計" (2026-10-13)
---

# AI に見せる領域を分ける: 作業部屋（専用 WSL）方式

## Purpose

顧客データなど AI に見せたくない領域と、AI に作業させる領域を、設定の禁止リストでなく**物理的な分離**で分ける設計の判断と原則。実装は `workflow-kit/room/`、使い方は `guides/howto/ai-room-setup.md`、理由と経緯は `guides/explain/ai-room-why.md`。

## Principles

- 「全部見える・一部隠す」（禁止リスト）でなく、「何も見えない・渡したものだけ見える」（許可リスト）にする。理由: 禁止リストは、漏れ（`grep -r`、スクリプトの中、別のツール）を防げない。
- 境界は OS 層（別の WSL ディストリビューション、`automount` と `interop` を無効、AI は一般ユーザー）に置く。AI の権限設定（deny）は、Vault 側の安全網にとどめ、境界の保証としない。理由: 権限設定は AI のツール経由しか止められない。
- AI に渡すものは、マスクしたコピーにする。原本・対応表・復元済みの成果物は、AI から見えない場所（`_noai/`）に置き、git で追跡しない。
- 副作用のある手順（マウント、マスク、復元、移動、コミット）はスクリプトが行い、AI には実行させない。AI は判断（聞き取り、確認、下書き）を、決まったファイルに書いて渡す。2つの層の接点は、ファイルの受け渡しだけ。
- 外へ出すのは下書きだけにして、人の確認を通す。公開されうる共有知（workbase）へ、対応表の語を含むものを入れない。
- 境界（顧客・機密度）は、部屋の単位（Area）と一致させる。

## Decisions

- **Area ごとにディストロ、Project ごとにマウント（`ai/` だけを `/mnt/room/<Project>`）**（2026-10-12）
  - 根拠: ライフサイクルが分かりやすく、ログインと導入が Area の数で済む。ユーザーが決定。
  - 却下案: Project ごとのディストロ（数が増えて管理が重い）。
- **すべての projects / areas の AI 作業を、部屋の 1 パターンに揃える**（2026-10-12）
  - 根拠: ユーザーの「できれば1パターンに揃えたい。管理に自信がない」。
- **共有知（workbase）は、起動のたびに写しを `~/shared` に読み取り専用で送る（方式 A）。基準コミットを記録する**（2026-10-13）
  - 根拠: ユーザーが方式 A を選択。分離前と同じ環境になる。
  - 却下案: `resources/` を 2 つ目のマウントにする（B）、部屋の中で clone（C。認証情報が要る）。
- **共有知への戻しは下書きだけ（`ai/out/stock/`）。基準コミットと観測日を持たせ、基準が古ければ印を付け、`integrate` が 3 点で照らす**（2026-10-13）
  - 根拠: git の rebase にならい、検出は機械的に回収時、解決は意味の判断として統合時。ユーザーが方向に合意。

## Facts

- 実機（WSL）で、専用ディストリビューション、`/mnt/c` が空、`ai/` だけのマウント、Claude Code と Zed（WSL リモート）が部屋の中で動くことを確認した（確認: 2026-10-12、根拠: 実機検証 S1〜S6）。
- マスクは csv と xlsx（zip 内の XML を置換）。実際の Excel での開封と「すべて更新」は未確認（仮説）。
- Windows のネイティブでは Claude Code のサンドボックスが使えない。部屋の中（Linux）では、物理分離があるので重ねる意味が薄い。

## Gotchas

- 状況: 個人のグローバル ignore の `out/` が、`ai/out/` の新しい成果物を無視した
  - 原因: リポジトリの `.gitignore` より、グローバルの ignore が効いた
  - 解決: ワークスペースの `.gitignore` に `!**/ai/out/` を足して打ち消す
- 状況: Zed を部屋ではなくローカルのフォルダで開くと、エージェントが Windows 側で動き、Vault 全体が見える
  - 原因: Zed のエージェントは、開いたフォルダのある側で動く
  - 解決: Zed は WSL リモート接続でだけ使う

## Open Questions

- 対応表（`mapping.json`）を失ったときの扱い。追跡しないので、バックアップの方針が要る。
- Obsidian の中で AI と話す方法（Claudian は部屋に繋がらない）。

## Next Actions

- 実 Project（顧客データあり）で `open` から `close` まで試し、マスク漏れと復元の失敗を測る。

## Related

- [[ai-development-workflow]]
- [[claude-code-permissions]]
- [[git-rebase-chronology]]
- [[ai-tool-deliverable-structure]]
