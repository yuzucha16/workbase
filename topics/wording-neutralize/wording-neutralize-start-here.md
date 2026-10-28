# 窓口: wording-neutralize

- 型: Project 型。完了条件: 公開リポジトリの現在の文言と履歴から、環境を特定させる表現（対象語は `records/2026-10-27-impact-analysis.md`）が、性質を表す書き方に置き換わっている。
- 何の取り組みか: 公開されても差し支えない表現にする。きっかけは、スクリプトのコマンド例などに環境を特定する語が残り、ユーザーが公開リポジトリで読むたびに気になること（ユーザーの動機は「隠したい」）。新しい固有名は作らず、性質（TLS 検査がある環境、隔離ソースなど）で書く。影響分析は [[2026-10-27-impact-analysis]]。

## いま

段階 1〜4 すべて適用済み（段階 4 は 2026-10-29 に force push）。残りは他の clone の作り直しだけ。詳細は `docs/log.md`。

## あなた待ち

- 他の clone（PC2、WSL の部屋、`works_sub*`）の `git fetch && git reset --hard origin/main`。作者の揃え直しの要否。

## 次の一手

clone の作り直しが済んだら、トピックを閉じる（`topics/AGENTS.md` の手順）。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/2026-10-27-impact-analysis.md`（影響分析の全文）

## リポジトリに無いローカルの状態

なし。ただし、他の clone（PC2、WSL の部屋、`works_sub*`）は、段階 4 の force push の後に作り直しが要る。
