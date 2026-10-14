# 次のステップ: 作業の進め方の型

背景と決定は [[improvement-methods-handover]]。PC のセッションで、この順に進める。

## TODO（済んだら `[x]`）

- [ ] kit の点検を実行する（下の「1」）
- [ ] 作業側の `events` の定義に `goal_change` を足す（下の「2」）
- [ ] `start` のモードを、次の2〜3セッションで試す（下の「3」）
- [ ] 推測の項目をユーザーに確認する（下の「4」）
- [x] inbox の6本を lessons へ統合する（下の「5」。2026-10-14、フラットに6ファイル。取扱説明書は `user-manual`、A/B とモードは `session-goal-modes`）
- [ ] 反映が終わったら、`mobile-session/improvement-methods/` を削除し、`mobile-session-index.md` の行を消す

## 1. kit の点検

- `pwsh -NoProfile -File workflow-kit/tools/check-hook-outline.ps1` を実行する。`start-hook.md`（手順を1つ足し、番号を振り直した）と `hook-common.md`（記録の表の1行）が対象。
- `hook-matrix.md` の字数（start は 3.7k に直した）を、同ファイルの測り方で測り直す。5,000 字の目安に収まっているはず。
- 失敗したら、番号参照の有無（手順は名前で参照する）と、記録の表の行を見る。

## 2. 作業側の定義

- 作業側（Vault のトップ。このリポジトリの外）の `AGENTS.md` にある `events` の `kind` の定義に、`goal_change`（探索型でゴールが変わったとき）を足す。無ければ記録しない規則なので、足さなくても動作はする。

## 3. 試す

- 次の2〜3セッションで、`start` の1問（確定型か探索型か）を使う。ユーザーは型を先に言ってよい（「問題解決2で始めて」など）。
- 見る点: 再伝達（`again`）と漏れ（`gap`）の件数、ゴール変更（`goal_change`）の回数、探索型で全体4回に収まるか。
- 現行のインタビューとの比較は、1回ずつだと n=1。差は参考値にとどめる。`typed`（型を指定して始める）を開始の形に足すかは、実測のあとに決める。

## 4. ユーザーに確認する推測

1. 取扱説明書の「やらないことを先に決める」「引き継ぎ前提で終える」は合っているか（`exmem/inbox/2026-10-13-user-manual.md` の Facts）。
2. モードの目安（成果物の合否を事前に書けるか）が、ユーザーの実例に合うか。
3. 型の判定を、AI の推奨とユーザーの1問確認にする方式でよいか。

## 5. 統合（`integrate` の手順に従う）

- 対象の6本: `exmem/inbox/` の `2026-10-13-*`（5本）と `2026-10-14-session-goal-modes.md`。
- 置き場を決める（各ノートの Open Questions に提案がある）:
  - やり方集: 1ファイル（`lessons/problem-solving-methods.md` を想定）に章立てするか、系列ごとに分けるか。問題解決1・2、改善1・2を、まとめて決める。
  - 取扱説明書: `lessons/` に新規ノート（`user-manual` を想定）か、`human-ai-decision-loop` への追記か。提案は新規ノート。
  - A/B とモード: やり方集に入れるか、`workflow-kit` の記述（`start`）の根拠として別ノートにするか。
- 統合後、`exmem/README.md` の索引に1行足す。`[[2026-10-13-...]]` の inbox 名のリンクは、統合後の名前に直す。
- 統合したら、start-hook から型のノートを指すか（指すなら lessons 側の名前）を決める。
