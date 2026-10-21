# 作業ログの経緯（log-history）

## Log

### 2026-10-21（試行のフィードバックを `start-plan.md` に反映し、品質チェック1回目を行った）
- 3題材（usage-viz、stock-modes、private-knowledge）のフィードバックを取り込み、`workflow-kit/start-plan.md` に反映した（ユーザーが承認）: stock-modes の所見6件（変更先の洗い出し、裏づけの確認方法と時期、前提の表の書式、〔資料〕の出典と推測の明記、完了時期のバッファ、見る単位は測る道具だけ）、問題意識は手段でなく論点で書く、works の置き場（Area 配下）、workbase の題材の置き場（題材のトピックの `records/`。仮決め 〜10-28）、上限3つは日付を持つ節目にだけ数える（束ねたときは理由を1行）、小さな題材の規模は変更先のファイル数で測る、WBS の第2層は成果物の種類で分ける、中間の記録は読み手がいれば葉にし、読み手のいない本当の中間物（テスト、作業用スクリプト）だけ親に含める。
- WBS の葉と実ファイル数のずれの真因（仮説）: 第2層が工程で分かれる、葉に中間の記録が入る、変更先を先に洗い出さない。最後の1点は「変更先の洗い出し」で手当てした。効果は次の題材で測る。
- 品質チェック1回目は `private-knowledge`（計画の質だけ。1週間の題材で2週の検証はできなかった）。実行は、Area を跨ぐ共有知の実装と実機の通し試験まで進んだ（`topics/private-knowledge/`）。記録は `topics/kit-growth/records/planning-method-record.md`。
- 変更した kit のファイル: `workflow-kit/start-plan.md`、`exmem/lessons/planning-method.md`（Decisions と Open Questions）。

### 2026-10-21
- 試行の題材を、それぞれトピックに切り出した（ユーザーの指示）: `topics/stock-modes/`、`topics/usage-viz/`。構造は `planning-method` と同じ（窓口・`docs/`・`records/`）。2026-10-20 の（2）〜（4）の経緯と、題材の【この件】の決定、計画の出力は、それぞれのトピックに移した。`records/` は2か所（測ったことは `kit-growth/records/`、各トピックの出力はそのトピック。`topics/private-knowledge/docs/decisions.md`）。

### 2026-10-20
- 計画のやり方を `topics/kit-growth/records/` から切り出し、`topics/planning-method/`（Project 型）を作った。下書き（骨子、Must と Want、登録の作業）は `planning-method-draft.md` に移し、records の `planning-method-record.md` は測ったことだけにした。決定は `docs/decisions.md`、次の一手は `docs/log.md` に置いた。ユーザーの指示（まず計画だけで様子を見る）。それ以前の経緯は直下の `docs/log-history.md` の 2026-10-19 の項。
